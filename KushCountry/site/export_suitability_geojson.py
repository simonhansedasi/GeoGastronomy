"""Export per-cell cannabis-suitability indicators to GeoJSON for the Leaflet map.

Reuses the exact MCDA membership functions and agronomic thresholds from
ML/07_baselines.ipynb (Table 1 criteria) -- not re-derived here.

The display grid is NOT data/raw/hex_grid.gpkg's own cells. That source grid
tiles flat-top hexagons and -- confirmed via unary_union -- has small real
gaps between "adjacent" cells (~3.6% of a cell's area each, invisible at the
paper's whole-study-area zoom, obvious once zoomed in on an interactive
map). Rotating that grid 30deg gets pointy-top hexagons but tilts the whole
map; closing its native gaps needs a buffer that makes cells overlap.
Neither is acceptable for the product map, so this script instead builds a
fresh, correctly-spaced, axis-aligned pointy-top hex lattice from scratch
(same circumradius, so same ~2km resolution) and pulls each new cell's
indicator values from the nearest ORIGINAL cell (nearest-centroid, same
convention this repo already uses for parcel-to-hex joins in ML/08). Result:
true edge-to-edge tiling, no overlap, no gaps, map stays north-up. The
tradeoff: map cell_ids are a display-grid resample, not the paper's
cell_id -- `source_cell_id` on each feature records which original cell's
data was used, for traceability.

Run: conda run -n GrapeExpectations python site/export_suitability_geojson.py
"""
import gzip
import math
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from shapely.geometry import Point, Polygon

PROC = Path(__file__).resolve().parent.parent / "data" / "processed"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent / "data"
OUT_DIR.mkdir(exist_ok=True)

MCDA_COLS = ["gdd", "vpdmax", "ppt", "ph", "slope_mean", "ffd"]
RESAMPLE_COLS = ["gdd", "vpdmax", "ppt", "ph", "elev_mean", "slope_mean", "ffd"]


def ramp_up(x, lo, hi):
    return np.clip((x - lo) / (hi - lo), 0, 1)


def ramp_down(x, lo, hi):
    return np.clip((hi - x) / (hi - lo), 0, 1)


def trapezoid(x, a, b, c, d):
    return np.minimum(ramp_up(x, a, b), ramp_down(x, c, d))


def pointy_hex(cx, cy, r):
    pts = [
        (cx + r * math.cos(math.radians(90 - 60 * k)), cy + r * math.sin(math.radians(90 - 60 * k)))
        for k in range(6)
    ]
    return Polygon(pts)


def build_pointy_grid(bounds, r):
    """Axis-aligned pointy-top hex lattice (rows horizontal, alternate rows
    offset) -- the standard construction, not a rotated flat-top grid, so
    the overall extent stays north-up. https://www.redblobgames.com/grids/hexagons/"""
    minx, miny, maxx, maxy = bounds
    dx = math.sqrt(3) * r  # column spacing (same row)
    dy = 1.5 * r  # row spacing
    pad = 2 * r
    centers = []
    y = miny - pad
    row = 0
    while y <= maxy + pad:
        x_offset = (dx / 2) if (row % 2) else 0.0
        x = minx - pad + x_offset
        while x <= maxx + pad:
            centers.append((x, y))
            x += dx
        y += dy
        row += 1
    return centers


def main():
    features = pd.read_pickle(PROC / "features.pkl")
    hex_grid = gpd.read_file(RAW / "hex_grid.gpkg")
    src = hex_grid.merge(features, on="cell_id", how="inner")

    # Circumradius from the source hexagon's own geometry (max centroid-to-
    # vertex distance), not hardcoded -- matches its true ~2km resolution.
    g0 = src.geometry.iloc[0]
    c0 = g0.centroid
    r = max(c0.distance(Point(x, y)) for x, y in g0.exterior.coords[:-1])
    print(f"circumradius r={r:.1f}m")

    src_cx = src.geometry.centroid.x.values
    src_cy = src.geometry.centroid.y.values
    tree = cKDTree(np.column_stack([src_cx, src_cy]))

    centers = build_pointy_grid(src.geometry.total_bounds, r)
    dist, idx = tree.query(centers, k=1)

    # A point strictly inside the original coverage is always within r of
    # some original centroid (r = that hexagon's own circumradius). Drop
    # anything farther -- that's off the edge of real data (ocean etc.),
    # not a cell worth resampling.
    keep = dist <= r
    centers = np.array(centers)[keep]
    idx = idx[keep]

    src_reset = src.reset_index(drop=True)
    resampled = src_reset.iloc[idx][["cell_id"] + RESAMPLE_COLS].reset_index(drop=True)
    resampled = resampled.rename(columns={"cell_id": "source_cell_id"})

    geoms = [pointy_hex(cx, cy, r) for cx, cy in centers]
    out = gpd.GeoDataFrame(resampled, geometry=geoms, crs=src.crs)
    out.insert(0, "cell_id", [f"pcell_{i:05d}" for i in range(len(out))])
    print(f"{len(out)} display cells (resampled from {len(src)} source cells)")

    out["m_gdd"] = ramp_up(out["gdd"], 800, 1200)
    out["m_vpd"] = ramp_up(out["vpdmax"], 900, 1300)
    out["m_ppt"] = trapezoid(out["ppt"], 700, 800, 1600, 1800)
    out["m_ph"] = trapezoid(out["ph"], 50, 55, 68, 72)
    out["m_elev"] = trapezoid(out["elev_mean"], 300, 400, 1200, 1400)
    out["m_slope"] = ramp_down(out["slope_mean"], 20, 26.6)
    out["m_ffd"] = ramp_up(out["ffd"], 90, 120)
    out["nodata"] = (out[MCDA_COLS] == 0).all(axis=1)

    out = out.to_crs("EPSG:4326")

    keep_cols = [
        "cell_id", "source_cell_id", "geometry", "nodata",
        "m_gdd", "m_vpd", "m_ppt", "m_ph", "m_elev", "m_slope", "m_ffd",
        "gdd", "vpdmax", "ppt", "ph", "elev_mean", "slope_mean", "ffd",
    ]
    out = out[keep_cols].copy()
    for c in ["m_gdd", "m_vpd", "m_ppt", "m_ph", "m_elev", "m_slope", "m_ffd"]:
        out[c] = out[c].round(3)
    for c in ["gdd", "vpdmax", "ppt", "elev_mean", "slope_mean", "ffd"]:
        out[c] = out[c].round(1)
    out["ph"] = (out["ph"] / 10).round(2)  # SoilGrids x10 -> real pH for display

    geojson_path = OUT_DIR / "suitability.geojson"
    out.to_file(geojson_path, driver="GeoJSON")

    with open(geojson_path, "rb") as f_in, gzip.open(str(geojson_path) + ".gz", "wb") as f_out:
        f_out.writelines(f_in)

    raw_mb = geojson_path.stat().st_size / 1e6
    gz_mb = Path(str(geojson_path) + ".gz").stat().st_size / 1e6
    print(f"wrote {geojson_path} ({raw_mb:.2f} MB) + .gz ({gz_mb:.2f} MB)")
    print(f"nodata cells: {int(out['nodata'].sum())} / {len(out)}")

    counties = gpd.read_file(RAW / "emerald_counties.gpkg")[["NAME", "geometry"]]
    counties = counties.to_crs("EPSG:4326")
    counties_path = OUT_DIR / "counties.geojson"
    counties.to_file(counties_path, driver="GeoJSON")
    print(f"wrote {counties_path} ({counties_path.stat().st_size / 1e3:.0f} KB)")


if __name__ == "__main__":
    main()
