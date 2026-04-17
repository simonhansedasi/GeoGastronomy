# KushCountry

## Unsupervised Terrain Fingerprinting (UTF) — Cannabis Demonstration Case

Part of the [GeoGastronomy](../) research program. **Target journal: Remote Sensing (MDPI).**

---

## What this is

A demonstration of **Unsupervised Terrain Fingerprinting (UTF)**: a six-step framework for recovering land-use suitability archetypes from unlabeled Earth observation and environmental data. Cannabis cultivation in California's Emerald Triangle is the demonstration case.

California's Department of Cannabis Control deliberately withholds all spatial information for licensed cultivators — there are no cultivation polygons to train on. UTF sidesteps this by stacking terrain, climate, soil, and remotely sensed canopy structure (Sentinel-2 NDVI) across the Emerald Triangle, letting k-means clustering self-organize the landscape, and identifying which archetype matches documented cannabis cultivation conditions. The cannabis-suitable cluster emerged without any labeled input. The framework generalizes to any specialty crop where cultivation locations are suppressed, restricted, or absent.

---

## Study Area

Humboldt, Mendocino, and Trinity Counties, California — the Emerald Triangle. The established US outdoor cannabis appellation and the most climatically diverse three-county region in the state.

- EPSG:32610 (UTM Zone 10N) throughout
- 8,900 hexagonal cells at 2 km spacing
- Study extent from US Census TIGER 2023 county boundaries

---

## Pipeline

### Data Wrangling

| Notebook | What it does |
|----------|-------------|
| `00_study_area.ipynb` | Downloads Census TIGER county shapefile; filters to Emerald Triangle; saves county polygons + 2 km buffered study extent |
| `01_generate_grid.ipynb` | Generates 2 km hexagonal grid (8,900 cells) clipped to study extent |
| `02_clip_dem.ipynb` | Downloads 1 arc-second USGS DEM tiles via TNM API; deduplicates by vintage; mosaics with GDAL VRT; warps to UTM 10N |
| `03_dem_features.ipynb` | Zonal stats per cell: elevation (mean/max/std), slope, aspect (cos/sin), relief |
| `04_ndvi.ipynb` | Sentinel-2 SR via Google Earth Engine; July–October composite 2022–2024; ndvi_std (spatial heterogeneity proxy) |
| `05_climate.ipynb` | GEE Daymet V4 (NASA/ORNL); derives tmean, VPD, frost-free days, GDD (base 10°C), annual precip |
| `06_soil_features.ipynb` | SoilGrids ISRIC WCS 2.0.1; 6 variables × 3 depths → depth-weighted averages; warped to UTM |
| `07_assemble_features.ipynb` | Joins all layers on cell_id; median-imputes edge NaNs; StandardScaler normalization; saves feature matrix |

### Machine Learning

| Notebook | What it does |
|----------|-------------|
| `01_model.ipynb` | PCA on scaled features; synthetic RF task (real vs shuffled) for permutation importance; PC1 = coast–interior gradient |
| `02_clustering.ipynb` | K-means on StandardScaler-equalized PC scores; K=7; cluster 0 = cannabis archetype (GDD 1395, VPD 1568, elev 527m, pH 5.84); dissolves to suitability zone (1,924 cells, ~6,325 km², 22.2% of study area) |
| `03_ndvi_regression.ipynb` | RF regressor within cluster 0; target ndvi_std; CV R²=0.650 ± 0.043; slope is dominant driver (permutation importance 0.59), pH second (0.39), sand (0.13), SOC (0.11) |
| `04_subclustering.ipynb` | Sub-clusters cluster 0 using features weighted by ML/03 importance; K=6; prime stratum = 714 cells (pH 6.02, slope 19.0°, VPD 1624 Pa) |
| `05_validation.ipynb` | Scrapes RWQCB NOV PDF archive (510 PDFs); extracts APNs; geocodes via Humboldt parcel REST API; 91 parcels matched to hex grid; χ²(6)=36.6, p=2.1×10⁻⁶, Cramér's V=0.26; cluster 0 lift=3.41 |
| `06_robustness.ipynb` | K sensitivity (K=4–7, archetype 4/4 criteria at all K); bootstrap ARI (mean=0.974, n=50); feature ablation (terrain→+climate→+soil→+EO); Cramér's V |

---

## Key Results

- **Cannabis archetype identified without any labeled data.** Cluster 0 (K=7) matches documented cultivation conditions: mid-elevation interior (527m mean), warm-dry growing season (GDD 1395, VPD 1568 Pa), Mediterranean precip pattern (1,102 mm/yr). Covers 22.2% of study area.
- **Coastal fog belt correctly excluded.** Interior mid-elevation zones dominate the suitability zone.
- **Slope is the dominant driver of canopy heterogeneity within the suitability zone** (permutation importance 0.59), followed by soil pH (0.39), sand fraction (0.13), and SOC (0.11). Terrain geometry and soil chemistry govern productive variation within a climatically suitable envelope.
- **Sub-clustering identifies prime terrain:** 714 cells with near-optimal pH (6.02), accessible slopes (19.0°), elevated VPD (1624 Pa).
- **Enforcement-based validation directly confirms the archetype** (χ²(6)=36.6, p=2.1×10⁻⁶, Cramér's V=0.26): cluster 0 = only 2.9% of Humboldt terrain but 9.9% of RWQCB enforcement parcels (lift=3.41). Humboldt-corrected baseline is the correct reference for parcels drawn exclusively from Humboldt County records.
- **EO contributes non-redundant structure:** satellite-derived canopy heterogeneity (NDVI std) completes the partition geometry that terrain, climate, and soil alone cannot recover.
- **Robust to K choice:** cannabis archetype recovers at 4/4 agronomic criteria for K=4,5,6,7. Bootstrap stability mean ARI=0.974 across 50 subsamples.

---

## Data Sources

| Layer | Source | Resolution |
|-------|--------|-----------|
| Study extent | US Census TIGER 2023 | County polygons |
| DEM | USGS National Map 1 arc-second | ~30 m |
| NDVI | Sentinel-2 SR via GEE | 30 m composite |
| Climate | Daymet V4 via GEE (NASA/ORNL) | 1 km daily |
| Soil | SoilGrids ISRIC WCS 2.0.1 | 250 m |

**Note on soil units:** SoilGrids encodes pH ×10 (60 = actual pH 6.0), SOC in dg/kg, CEC in mmol/kg. All profile comparisons must account for this.

---

## Stack

Python 3.7+. `geopandas`, `rasterio`, `shapely`, `pyproj`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `requests`, `earthengine-api`.

GDAL command-line tools (`gdalbuildvrt`, `gdalwarp`, `gdaldem`, `gdal_calc.py`) for raster operations.

Google Earth Engine authenticated session required for `04_ndvi.ipynb` and `05_climate.ipynb`. Run `earthengine authenticate` once before first use.

See `requirements.txt`.

---

## Structure

```
KushCountry/
├── README.md
├── CONTEXT.md
├── CLAUDE.md
├── requirements.txt
├── data_wrangling/       00–07: ingestion and feature extraction
├── ML/                   01–06: PCA, clustering, regression, sub-clustering, validation, robustness
├── writing/              paper.tex + cover_letter.tex + references.bib (target: MDPI Remote Sensing)
├── data/
│   ├── raw/              TIGER, DEM tiles, hex grid, county polygons, NOV PDF cache
│   └── processed/        features, clusters, subclusters, zone gpkgs, validation, robustness
└── img/                  figures at 150 dpi (ML01–ML06)
```
