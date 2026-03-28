# Project Context — GrapeExpectations

Use this file to resume work in a new session.
Hand it to Claude at the start: "Here's the context file for GrapeExpectations."

---

## What this is

Precision viticulture research pipeline. Fuses 9 years of Sentinel-2 satellite imagery, USGS 1m DEM, PRISM climate grids, and USGS gSSURGO soil maps to model vineyard canopy health and microclimate frost risk at meter resolution. Includes a stacked ensemble ML model (R² = 0.967), spatial clustering for management zone identification, and a research proposal for Distributed Temperature Sensing (DTS) fiber-optic deployment with Washington State University.

---

## Architecture

```
grape_expectations/           Python package (data wrangling utilities)
  data/wrangling.py           KML → GeoDataFrame, hexagonal subdivision, zonal stats, geometry cleaning
  models/frost.py             Frost risk composite scoring
  io/loaders.py               Data I/O helpers
  config.py                   Paths and constants

RegressionRidge/
  data_wrangling/             6-stage pipeline (numbered notebooks)
    00_subsample_polygons     Vineyard blocks → 3,598 hexagonal cells (~1,000 m² each)
    01_clip_dem               Clip USGS DEM to vineyard extent (UTM reproject)
    02_breakdown_dem          Topographic features: elevation, slope, aspect (cos/sin), curvature, relief
    03_get_temp_data          PRISM daily weather (tmin/tmax, precip, VPD, GDD) — 9 years
    04-2_ndvi_smol            Sentinel-2 via GEE: NDVI, EVI, NDWI, SAVI, RENDVI, MCARI2 — 9 years
    05_soil                   USGS gSSURGO: sand/silt/clay %, AWC, CEC7, OM, pH, EC
    06_assemble_data          Join all layers → 100+ features, 32,382 rows
  ML/
    forest_ensemble           Stacked ensemble: RF + ExtraTrees + GBM + XGBoost + KNN → ElasticNetCV meta
    clustering                GB leaf embeddings → PCA → k-means (3 zones)
    time_series               Per-plot OLS on NDVI trajectory for anomaly detection
    neural_net                Exploratory LSTM/feedforward
  assess_frost_risk.ipynb     Composite frost risk raster: slope + elevation deviation + NDVI + area

docs/
  GrapeExpectations.tex       DTS research proposal (fiber-optic canopy sensing, WSU pilot)
  proposal/                   Grant submission docs (budget, CV, transmittal)
  index.md                    Data documentation
```

---

## Data sources

| Layer | Source | Resolution | Temporal |
|---|---|---|---|
| DEM | USGS National Map | 1 m | Static |
| NDVI + indices | ESA Sentinel-2 (Google Earth Engine) | 10 m | Daily 2016–2025 |
| Weather | PRISM Oregon State | 4 km grid | Daily 2016–2025 |
| Soil | USGS gSSURGO | Map unit | Survey-based |
| Polygons | Google Earth KML digitization | Vector | Static |

Data lives in `RegressionRidge/data/` (~5.5 GB total). Pickled DataFrames are the working units; raw rasters in subdirectories.

---

## Key results

- Stacked ensemble: **R² = 0.967**, RMSE = 0.00033 (tune set, multi-output weeks 36–43)
- 3,598 hexagonal plot cells from 4 vineyard blocks
- 32,382 training rows (cells × years)
- 3-cluster spatial zones from GB embeddings + k-means
- Frost risk raster mapped to vineyard DEM

---

## Status

Active research. Pipeline and models complete. DTS funding application submitted ~March 2026 (decision expected ~April 2026). Fiber-optic pilot in planning with Washington State University. If funded, this repo becomes the active codebase for DTS canopy temperature analysis.

---

## Notable decisions

**Hexagonal binning** — minimizes edge effects vs. rectangular grids; gives equal-area cells for unbiased feature distributions.

**Circular statistics for aspect** — aspect (0–360°) encoded as cos/sin pair before ML to handle cyclic nature correctly.

**Leakage prevention** — future NDVI and target-correlated spectral indices (MCARI2, RENDVI) explicitly dropped from feature set.

**DTS proposal** — goes beyond ML; argues for replacing point sensors with 1m-resolution fiber-optic cables for real-time irrigation, frost, and canopy stress monitoring at field scale.
