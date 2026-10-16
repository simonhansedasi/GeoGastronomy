# Loading GrapeExpectations into QGIS

`export_powerbi.py` builds `dim_cells.csv` with a lat/lon **point** per hex
cell, because Looker Studio's map chart only takes a Location dimension --
and drawing 32,978 of those points client-side is exactly what crashed the
browser tab. QGIS doesn't have that problem: it's built to hold real
**polygon** geometry at any feature count and render it as one layer, not
one DOM element per row. That's the actual skill gap this exercise
practices -- desktop GIS vs. browser BI tooling, not "Looker but slower."

## 0. Generate the GeoPackage

```
cd ~/coding/GeoGastronomy/GrapeExpectations/powerbi_dashboard
python3 export_qgis.py
```

Writes `grapeexpectations.gpkg` -- one layer, `hex_cells`, 32,978 real hex
polygons (the same v2 grid `export_powerbi.py` uses), each carrying
terrain (`elev_mean`, `slope_mean`, `aspect_mean`, `curvature_mean`),
`ndvi_trend_per_year` (9-year linear trend, same number
`canopy_trend_map.py` colors by), and `ndvi_mean_<latest year>` (a plain
single-season snapshot). No cluster/vigor/health columns, same reason as
`export_powerbi.py`: `ML/clusters.csv` predates this grid's resolution and
doesn't line up with today's `tile_id` numbering.

## 1. Open it

Layer > Add Layer > Add Vector Layer... > pick `grapeexpectations.gpkg` >
Add. All 32,978 polygons render immediately, no import wizard, no
row-count wall.

## 2. First styling exercise: graduated symbology

1. Right-click the layer > Properties > Symbology.
2. Change the top dropdown from "Single Symbol" to **Graduated**.
3. Value: `ndvi_trend_per_year`.
4. Color ramp: pick a diverging one (RdBu or similar) so declining cells
   read as one color family and improving cells as the other -- same
   diverging-vs-sequential choice `canopy_trend_map.py` had to make
   explicitly for the same reason (this is a signed delta, not a
   magnitude).
5. Mode: Equal Interval or Quantile, ~7 classes, Classify.

This reproduces `canopy_trend_map.py`'s story (which cells built up vs.
declined) as an interactive layer instead of a static PNG -- pan, zoom,
click a cell to see its attribute table row.

## 3. Second exercise: a snapshot layer

Duplicate the layer, style the copy on `ndvi_mean_<latest year>` with a
**sequential** green ramp instead (a magnitude this time, not a delta --
same distinction `_mapping.py`'s `NDVI_CMAP` vs. `DELTA_CMAP` encodes).
Toggle the two layers to compare "how green is it right now" against "is
it trending up or down."

## 4. What this teaches vs. the Looker Studio version

Same underlying data, same two questions (trend, snapshot) -- but QGIS
holds the real geometry at full resolution instead of forcing an
aggregation-or-crash choice. The transferable skill is vector layer
styling (graduated/categorized symbology, diverging vs. sequential ramps,
attribute-driven classification) -- the exact vocabulary a GIS-analyst job
posting means by "QGIS experience."
