# GrapeExpectations

Precision viticulture pipeline for predicting vineyard canopy health and frost risk at meter resolution across a Washington State wine production area.

---

## Overview

GrapeExpectations models per-cell NDVI — a proxy for vine canopy density and vigor — using 9 years of satellite imagery stacked with topographic, climate, and soil features. The target is a spatially explicit, annually updated picture of vineyard performance that can inform block-level management decisions.

A companion analysis identifies frost risk zones using topographic position, elevation deviation, and NDVI history.

**Key result:** Stacked ensemble (RF + ExtraTrees + GBM + XGBoost + KNN → ElasticNetCV) achieves random-split test R² = 0.9323, RMSE = 0.0229 NDVI units, across 8 harvest-window weeks (ISO 36–43). LOYO validation mean R² = 0.353 ± 0.114 across 10 vintages. Terrain accounts for 75.5% of SHAP attribution.

**Paper:** `RegressionRidge/paper.tex` — full draft with 14 figures, submitted target: *Precision Agriculture* (Springer).

---

## Study Area

- **Location:** Washington State wine country, USA
- **Scale:** 3,598 equal-area hexagonal cells, ~1,000 m² each
- **Temporal coverage:** 2016–2025 (9 growing seasons)

---

## Data Sources

| Source | Variables |
|--------|-----------|
| USGS 1m DEM | Elevation, slope, aspect, curvature, relief |
| Sentinel-2 via Google Earth Engine | NDVI, EVI, NDWI, SAVI, RENDVI, MCARI2 — daily composites |
| PRISM daily weather | Tmin, Tmax, precipitation, VPD |
| USGS gSSURGO | Sand/silt/clay %, AWC, CEC, organic matter, pH, EC |

---

## Pipeline

### Data Wrangling (`RegressionRidge/data_wrangling/`)

| Notebook | Purpose |
|----------|---------|
| `00_subsample_polygons.ipynb` | Convert vineyard block KML polygons into flat-top hexagonal cells; remove slivers |
| `01_clip_dem.ipynb` | Clip USGS 1m DEM to vineyard extent; reproject to UTM Zone 10 |
| `02_breakdown_dem.ipynb` | Extract topographic features: elevation, slope, aspect (cos/sin), curvature (profile/plan/total), relief, local relief |
| `03_get_temp_data.ipynb` | Ingest PRISM daily weather for 9 years; zip extraction, clipping, file cleanup |
| `04-2_ndvi_smol.ipynb` | Pull Sentinel-2 spectral indices via GEE; 9 years of daily imagery aggregated to phenological windows |
| `05_soil.ipynb` | Integrate gSSURGO soil properties per hexagonal cell |
| `06_assemble_data.ipynb` | Join all feature layers; output: 100+ features × 32,382 rows (cells × years), pickled |

### Machine Learning (`RegressionRidge/ML/`)

| Notebook | Purpose |
|----------|---------|
| `forest_ensemble.ipynb` | Stacked ensemble: RF + ExtraTrees + GBM + XGBoost + KNN → ElasticNetCV meta-learner; multi-output NDVI regression across weeks 36–43 |
| `clustering.ipynb` | GBM leaf embeddings → PCA → k-means (3 management zones) |
| `time_series.ipynb` | Per-plot OLS on NDVI trajectory; anomaly detection |
| `linear_regression.ipynb` | Ridge/Lasso baseline models |
| `decision_trees.ipynb` | Decision tree exploration |
| `neural_net.ipynb` | MLP regression variants |
| `LSTM.ipynb` | Sequence model on temporal NDVI |
| `regression.ipynb` | Additional regression experiments |

### Frost Risk

| Notebook | Purpose |
|----------|---------|
| `assess_frost_risk.ipynb` | Composite frost risk raster combining slope, elevation deviation from local mean, NDVI, and cell area |

---

## Structure

```
GrapeExpectations/
├── README.md
├── CONTEXT.md                      — detailed architecture and data specification
├── RegressionRidge/
│   ├── paper.tex                   — manuscript (full draft, 14 figures, target: Precision Agriculture)
│   ├── references.bib              — bibliography
│   ├── img/                        — all figure files (~30 PNGs)
│   ├── data_wrangling/             — numbered ingestion pipeline (00–06)
│   ├── ML/                         — model notebooks (forest_ensemble, clustering, SHAP, etc.)
│   └── data/                       — pickled DataFrames and raw raster subdirs (~5.5 GB)
├── assess_frost_risk.ipynb
├── sensing/                        — fiber-optic sensor deployment notebooks
├── experiments/                    — experimental analysis
└── docs/                           — grant materials, DTS fiber-optic proposal (TeX)
```

---

## Environment

Python 3.10+. Key dependencies: `geopandas`, `rasterio`, `earthengine-api`, `scikit-learn`, `xgboost`, `pandas`, `numpy`.

Google Earth Engine authenticated session required for `04-2_ndvi_smol.ipynb`.
