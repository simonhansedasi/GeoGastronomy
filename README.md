# GeoGastronomy

**GeoGastronomy** is the study and modeling of how Earth system variables — climate, geology, biodiversity — give rise to spatial patterns in flavor potential and culinary expression.

The core hypothesis: flavor complexity and intensity are partially predictable from structured Earth system features.

---

## Projects

### [GrapeExpectations](GrapeExpectations/)

Precision viticulture research pipeline — fuses 9 years of satellite imagery, topographic data, and soil maps to model vineyard canopy health and microclimate frost risk at meter resolution. Stacked ensemble achieving R² = 0.967. Includes a research proposal for Distributed Temperature Sensing (DTS) fiber-optic deployment across vineyard rows. Funding decision pending ~April 2026.

### [JavaScript](JavaScript/)

Machine-learning pipeline mapping current and future coffee suitability across the Big Island of Hawaiʻi (Kona and Kaʻu districts). Integrates terrain, climate (ERA5-Land + NEX-GDDP-CMIP6), satellite vegetation, and soil at 500 m resolution. Includes forward climate projections to ~2045 and a USDA NIFA SCRI grant application.

### [TerraMetabolica](TerraMetabolica/)

Global-scale deterministic mapping from observed regional food systems to measured metabolite profiles. Constructs Region Sample Units (RSUs) — bounded geographic regions defined by climate regime, geology, and endemic food ingredients — and analyzes metabolite-space structure through distance computation, PCA, and clustering. No inferred values; empirical data only.

---

## Causal Chain

```
Climate + Geology → Ecosystem Conditions → Biodiversity & Plant Chemistry
→ Ingredient Selection → Culinary Processing → Perceived Flavor
```

---

## Tech

Python, scikit-learn, XGBoost, Google Earth Engine, rasterstats, rasterio, geopandas, GDAL, pandas, NumPy, SciPy, matplotlib, Jupyter
