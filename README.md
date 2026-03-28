# GrapeExpectations

Precision viticulture research pipeline — fuses 9 years of satellite imagery, topographic data, and soil maps to model vineyard canopy health and microclimate frost risk at meter resolution. Stacked ensemble achieving R² = 0.967. Includes a research proposal for Distributed Temperature Sensing (DTS) fiber-optic deployment across vineyard rows.

---

## Data pipeline

Six-stage pipeline assembling a 100+ feature matrix across 3,598 hexagonal plot cells (32,382 training rows over 9 years).

### [00 — Subsample polygons](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/00_subsample_polygons.ipynb)

Subdivide vineyard blocks into hexagonal cells (~1,000 m² each) for equal-area spatial sampling and maximum feature variance.

### [01 — Clip DEM](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/01_clip_dem.ipynb)

Clip USGS 1m DEM to vineyard extent; reproject to UTM.

<p align="center">
  <img src="RegressionRidge/img/dem_clip.png" alt="DEM clipped to vineyard extent" width="600"/>
</p>

### [02 — Breakdown DEM](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/02_breakdown_dem.ipynb)

Zonal statistics per cell: elevation, slope, aspect (cos/sin encoded), profile/plan curvature, local relief.

<p align="center">
  <img src="RegressionRidge/img/dem_w_slope.png" alt="DEM with slope overlay" width="600"/>
</p>

### [03 — Temperature data](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/03_get_temp_data.ipynb)

Extract 9-year daily PRISM climate grid: tmin/tmax, precipitation, VPD, GDD.

<p align="center">
  <img src="RegressionRidge/img/temp_timeseries.png" alt="Temperature time series" width="600"/>
</p>

### [04 — Vegetation indices](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/04-2_ndvi_smol.ipynb)

Sentinel-2 composites via Google Earth Engine: NDVI, EVI, NDWI, SAVI, RENDVI, MCARI2. Smoothed and interpolated per cell across 9 seasons.

<p align="center">
  <img src="RegressionRidge/img/health.png" alt="Vegetation index time series" width="600"/>
</p>

### [05 — Soil](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/05_soil.ipynb)

Clip USGS gSSURGO soil database to vineyard; extract sand/silt/clay %, AWC, CEC7, organic matter, pH, EC.

<p align="center">
  <img src="RegressionRidge/img/soil.png" alt="Soil map" width="600"/>
</p>

### [06 — Assemble data](https://github.com/simonhansedasi/GrapeExpectations/blob/main/RegressionRidge/data_wrangling/06_assemble_data.ipynb)

Join all layers into a 100+ feature matrix: 3,598 cells × 9 years = 32,382 rows.

---

## Machine learning

### Stacked ensemble — NDVI prediction

Multi-output regression predicting NDVI for weeks 36–43 simultaneously.
- Base learners: Random Forest, Extra Trees, Gradient Boosting, XGBoost, KNN
- Meta-learner: ElasticNetCV (α and L1 ratio tuned via 5-fold CV)
- **R² = 0.967**, RMSE = 0.00033 on tune set

<p align="center">
  <img src="RegressionRidge/img/weekly_preds.png" alt="Weekly NDVI predictions vs. observed" width="600"/>
</p>

Residuals remain tight for near-term weeks and widen with prediction horizon — time-series modeling is the natural next step.

<p align="center">
  <img src="RegressionRidge/img/weekly_preds_resid.png" alt="Prediction residuals" width="600"/>
</p>

<p align="center">
  <img src="RegressionRidge/img/weekly_pct_preds_resid.png" alt="Percent prediction residuals" width="600"/>
</p>

### Spatial clustering — management zones

Gradient boosting leaf embeddings → PCA → k-means identifies 3 distinct management zones from soil and topographic features.

<p align="center">
  <img src="RegressionRidge/img/cluster_pca.png" alt="PCA cluster plot" width="600"/>
</p>

Zones mapped back to the vineyard DEM reveal spatially coherent blocks aligned with topographic gradients.

<p align="center">
  <img src="RegressionRidge/img/dem_w_cluster.png" alt="Clusters overlaid on DEM" width="600"/>
</p>

Radar chart shows which soil and topographic features drive each zone.

<p align="center">
  <img src="RegressionRidge/img/radar_cluster.png" alt="Cluster feature weights" width="600"/>
</p>

### Time-series regression

Per-plot OLS on NDVI trajectory for anomaly detection and yield trend monitoring across seasons.

<p align="center">
  <img src="RegressionRidge/img/ts_lr.png" alt="Time series linear regression" width="600"/>
</p>

### Frost risk map

Composite microclimate score (slope drainage × elevation deviation × NDVI vigor × plot area) rasterized to a spatial overlay for targeted frost protection decisions.

<p align="center">
  <img src="RegressionRidge/img/frost_risk.png" alt="Frost risk raster" width="600"/>
</p>

---

## DTS research proposal

`docs/GrapeExpectations.tex` proposes deploying Distributed Temperature Sensing (DTS) fiber-optic cables across vineyard rows — 1m spatial resolution, sub-minute temporal resolution, continuous canopy temperature monitoring at field scale. Pilot planned with Washington State University. Funding decision pending ~April 2026.

---

## Data sources

| Source | Layer | Resolution | Coverage |
|---|---|---|---|
| USGS National Map | DEM | 1 m | ~5 km² |
| ESA Sentinel-2 (Earth Engine) | NDVI + 5 indices | 10 m | 9 years, 2016–2025 |
| PRISM Oregon State | Daily weather | 4 km grid | 9 years, 2016–2025 |
| USGS gSSURGO | Soil properties | Map unit | Regional |
| Google Earth | Vineyard boundaries | Vector (KML) | Regression Ridge block |

## Tech

Python, scikit-learn, XGBoost, Google Earth Engine, rasterstats, rasterio, geopandas, GDAL, pandas, NumPy, matplotlib, Jupyter

## Status

Active research. Stacked ensemble and frost risk pipeline complete. DTS fiber-optic deployment proposal under review for funding with Washington State University.
