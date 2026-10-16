# Loading GrapeExpectations into Looker Studio

Power BI Service gates signup behind a work/school email; a free Microsoft
dev tenant to get around that turned out to want a phone number and a
subscription plan on top. Looker Studio (Google's free BI tool,
lookerstudio.google.com) has none of that friction -- it works with a
regular Gmail account and runs entirely in the browser, which also sidesteps
the Linux/Windows-only-desktop-app problem Power BI and Tableau both have.

The underlying design doesn't change: this is still a star schema (a couple
of small dimension tables joined to a fact table), because that's the real
skill being practiced, not the specific vendor. But loading three tables and
drawing a map isn't a dashboard -- it's a connection test. The pages below
are built around actual questions this data can answer: how intensely does
a cell build up canopy each spring and shed it after harvest, which terrain
variable actually explains that (slope alone doesn't -- orientation does),
and whether the cells that are both steep AND south-facing look different
from the rest on anything else. That segment-vs-complement comparison is a
real BI move, not a data-science one -- Looker Studio does it natively with
`CASE WHEN`.

**A correction worth stating up front (2026-08-19).** This doc originally
used `ndvi_trend_per_year` -- a straight-line fit through each cell's 10
yearly NDVI *means* -- as the main "how is this cell doing" metric. That's
the wrong statistic for what these pages are actually trying to show:
averaging an entire growing season into one number per year throws away
the season's own shape (the spring build-up, the post-harvest decline)
before the trend is even fit, so the trend can only ever describe a slow
multi-year drift, not how intensely a given patch behaves within a season.
Pages 1-3 below now use two new per-cell rates that describe the shape
directly -- `buildup_rate_mean` and `decline_rate_mean`, both NDVI-per-day,
averaged across all 10 years. `ndvi_trend_per_year` is still in
`dim_cells.csv` and still valid for what it actually measures (long-run
direction, still used for the map's diverging color in Page 4), just not
for "intensity."

## 0. Generate the CSVs

```
cd ~/coding/GeoGastronomy/GrapeExpectations/powerbi_dashboard
python3 export_powerbi.py
```

Writes `dim_cells.csv` (33,028 rows, one per hex cell -- `tile_id`, `lon`,
`lat`, `lat_lon`, `elev_mean`, `slope_mean`, `aspect_mean`,
`curvature_mean`, `aspect_cos`, `aspect_sin`, `slope_x`, `slope_y`,
`profile_curv_mean`, `plan_curv_mean`, `ndvi_trend_per_year`,
`buildup_rate_mean`, `decline_rate_mean`), `dim_years.csv` (10 rows, one per
growing season -- `year`, `ppt_total`, `gdd`, `tmean_season`,
`vpdmax_season`, `vpdmax_peak`, `phenology_start_date`,
`phenology_peak_date`, `phenology_harvest_date`, `phenology_days_build`,
`phenology_days_decline`), and `fact_ndvi_yearly.csv` (~330,280 rows, one
per cell-year -- `tile_id`, `ndvi_mean`, `year`, `buildup_rate`,
`decline_rate`). Re-run any time the source pipeline data changes -- takes
~45s now, not instant, because `buildup_rate`/`decline_rate` read all 10
years of raw daily NDVI (not just the pre-aggregated yearly means) to find
each year's real spring-trough/peak/harvest dates.

**Two grains, on purpose -- don't confuse them.** `dim_cells.buildup_rate_mean`/
`decline_rate_mean` are each cell's 10-year *average* rate (one number per
cell -- what Pages 1-3 below use for ranking/mapping/segmenting). The same
two rates also live in `fact_ndvi_yearly.buildup_rate`/`decline_rate`
**without the `_mean` suffix** -- one row per (cell, year), the actual
season-by-season detail that went into that average. If you want "did this
cell build up faster in 2020 than 2024," or a chart of vineyard-wide
build-up/decline intensity year over year, that's in the fact table via
the Blend, not `dim_cells`. See Page 1b below.

**How `buildup_rate_mean`/`decline_rate_mean` are computed.** Same
trough/peak/harvest convention `canopy_trend_map.py` and
`harvest_decline_map.py` already used for a single season (2024) --
generalized across all 10 years in `export_powerbi.py`'s
`phenology_slopes()`: a shared vineyard-wide peak date (highest mean NDVI
before the harvest window), a shared trough date (lowest mean NDVI before
the peak), and a shared harvest date (lowest mean NDVI within the harvest
window, ISO weeks 36-43). `buildup_rate_mean` = (peak NDVI - trough NDVI) /
days between, `decline_rate_mean` = (harvest NDVI - peak NDVI) / days
between, each averaged across the 10 years. One addition needed to
generalize safely: the trough search is floored at Feb 1 each year
(`TROUGH_FLOOR_MD` in the script) so a winter/holiday-season dip can't get
picked as "start" -- 2 of the 10 years (2022, 2025) did exactly that before
the floor was added. Checked against all 10 years before picking Feb 1
specifically: it excludes both winter outliers without displacing any of
the already-sensible spring troughs, including the earliest legitimate one
(2016, Feb 8).

**Cluster/vigor/health columns are deliberately left out.** `ML/clusters.csv`
was generated against an older, coarser hex grid (3,598 cells) than the
terrain/NDVI data now uses (33,028 cells) and its cell numbering doesn't
line up with the current one. See the comment at the top of
`export_powerbi.py` for the full explanation. That clustering analysis
needs to be rerun against the current grid before it's trustworthy to put
on a dashboard.

## 1. Get each CSV into a Looker Studio data source

Looker Studio doesn't take a raw CSV directly as cleanly as Power BI does --
the reliable path is via Google Sheets:

1. Go to sheets.google.com, create a new blank sheet for each CSV
   (three sheets total: `dim_cells`, `dim_years`, `fact_ndvi_yearly`).
2. File > Import > Upload, pick the matching CSV, "Insert new sheet".
3. In Looker Studio (lookerstudio.google.com), **Create > Data source >
   Google Sheets**, pick the sheet, and connect it. Repeat for all three.

(If your account has the newer **File Upload** connector under Create >
Data source, you can skip Sheets and upload the CSVs straight in -- try it
first, fall back to Sheets if it's not available on your account.)

## 2. Join the tables with a Blend

Looker Studio's equivalent of Power BI's relationships is a **Blend**:

1. On a report page, **Add a chart**, but instead of picking one data
   source, choose **Blend data**.
2. Add `fact_ndvi_yearly` and `dim_cells` as the two tables, join key
   `tile_id` = `tile_id` (left join, fact table on the left).
3. Add `dim_years` as a third table in the same blend, join key
   `year` = `year`.
4. Save the blend -- it now behaves like one combined table you can reuse
   across multiple charts on the report, same as a Power BI relationship.

## 3. Report pages

### Page 1 -- Leaderboard: which cells build up fastest, which decline fastest

The most direct read of "intensity" is a ranked list, not a map -- 33,028
colored polygons make it hard to name a specific winner, a sorted table
does it in one glance. Two separate tables here, one per phase, since a
cell that builds up fast isn't necessarily the same one that declines fast
(checked: `corr(buildup_rate_mean, decline_rate_mean) = -0.63` across all
33,028 cells -- the two are meaningfully anti-correlated, fast spring
builders tend to decline faster after peak too, not slower).

1. **Add a chart > Table**, data source `dim_cells`.
2. Dimensions: `tile_id`, `slope_mean`, `aspect_mean`. Metric:
   `buildup_rate_mean`.
3. Sort descending -- top rows are the cells that green up fastest each
   spring. **Style tab > Row limit**: 20. That's the actual "ranking"
   skill -- Looker Studio does this with a sort direction and a row cap, no
   formula needed. Tableau's equivalent is a Top N filter on the same
   field.
4. Add a second table, same setup but metric `decline_rate_mean`, sorted
   **ascending** (most negative = fastest post-harvest decline first).

### Page 1b -- Season by season: the 10-year average hides real swings

`dim_cells.buildup_rate_mean`/`decline_rate_mean` are each cell's 10-year
*average* -- useful for ranking and mapping, but averages can hide exactly
the kind of variation this whole exercise started by asking about. The
year-by-year detail lives in `fact_ndvi_yearly.buildup_rate`/`decline_rate`
(same rates, no `_mean` suffix, one row per cell-year) via the Blend from
step 2. Checked vineyard-wide (average across all 33,028 cells, per year):

| year | buildup_rate | decline_rate |
|---|---|---|
| 2016 | 0.00167 | -0.00101 |
| 2017 | 0.00408 | -0.00143 |
| 2018 | 0.00245 | -0.00092 |
| 2019 | 0.00461 | -0.00178 |
| 2020 | 0.00156 | **-0.00287** |
| 2021 | 0.00210 | -0.00185 |
| 2022 | 0.00234 | -0.00131 |
| 2023 | 0.00318 | -0.00129 |
| 2024 | 0.00411 | -0.00067 |
| 2025 | **0.00098** | -0.00139 |

`buildup_rate` swings nearly 5x across years (0.00098 in 2025 to 0.00461 in
2019); `decline_rate` swings over 4x (-0.00066 in 2024 to -0.00287 in
2020). That's a real, large effect the 10-year average genuinely erases --
confirming this was worth building.

1. Use the Blend from step 2 (or a new one joining just `fact_ndvi_yearly`
   to `dim_years` on `year`).
2. **Add a chart > Line chart** (or Bar). Dimension: `year`. Metrics:
   `buildup_rate` and `decline_rate`, both set to **Average**.
3. This is a genuinely different chart from the map/leaderboard/scatter in
   Pages 1-3 -- those all answer "which cell," this answers "which year."
   Both are real questions; the star schema (`dim_cells` for the cell axis,
   `fact_ndvi_yearly` + `dim_years` for the time axis) is what makes both
   answerable from the same three CSVs without re-exporting anything.
4. Worth a look while you're here: `dim_years.phenology_days_decline` is
   only 30 days in 2020 (vs. 52-130 in every other year) -- the same year
   that had the steepest `decline_rate`. A short, steep decline and a
   long, gentle one can both be real; `days_build`/`days_decline` in
   `dim_years` is what tells them apart from the rate alone.

### Page 2 -- Does slope actually predict decline intensity? (scatter)

This is the honest version of "high slope, high NDVI change, what else is
true about those cells" -- a scatter plot, one point per cell, before
assuming any relationship exists. `decline_rate_mean` (post-harvest NDVI
loss per day) is the metric here, not `buildup_rate_mean` -- checked both,
and decline is the one that actually correlates with terrain (see below);
build-up barely does.

**Remember the 10,000-row hard cap on Looker Studio scatter/bubble
charts** (confirmed directly against this account, 2026-08-19 -- the
"Number of bubbles" control in the Style panel refuses anything above
10,000). With 33,028 cells, sorting by any field and letting the chart's
default row-fetch apply will silently show only the top/bottom slice of
*that* field -- not a random sample -- which looks exactly like "the shape
is gone" or "everything's one dot," depending on which end got kept. Fix
before building any scatter below: add a calculated field
`tile_mod = MOD(tile_id, 4)`, filter the chart to `tile_mod = 0` (an
unbiased ~8,257-row, ~25% sample -- `tile_id` is just an arbitrary
enumeration index from the hex-tiling step, not tied to geography or any
terrain variable), and leave Sort on `tile_id` rather than the metric so
the cap doesn't reintroduce the bias.

1. **Add a chart > Scatter chart**, data source `dim_cells`, with the
   `tile_mod = 0` filter from above applied.
2. Dimension: `tile_id`. Metric X: `slope_mean`. Metric Y:
   `decline_rate_mean`.
3. This one's a weak, small effect -- worth seeing as a contrast to what
   comes next. `corr(slope_mean, decline_rate_mean) = 0.10`. Binning
   `slope_mean` into 2°-wide ranges (checked against `dim_cells.csv`,
   2026-08-19): decline averages -0.00137/day at 0-2° slope, dips to its
   steepest at -0.00156/day around 4-6°, then eases back to -0.00111/day
   at 12-20°. Real, but the whole range is only about 0.0004/day wide --
   a mild dip, not the dominant story here.

**Why the scalar fields undersell this.** `slope_mean` (a magnitude) and
`aspect_mean` (a 0-360° compass bearing) each throw away information on
their own -- a slope's *magnitude* doesn't say which way the hillside
faces, and a bearing near 359° is actually right next to 1°, not far from
it, which breaks ordinary correlation and binning. The fix, already built
into this pipeline's terrain notebook
(`RegressionRidge/spark_pipeline/02_terrain_features.ipynb`), is to treat
slope + aspect as one 2D vector instead of two separate scalars:

```python
aspect_cos = cos(radians(aspect_mean))   # +1 = due north-facing, -1 = due south-facing
aspect_sin = sin(radians(aspect_mean))   # +1 = due east-facing,  -1 = due west-facing
slope_x    = tan(radians(slope_mean)) * aspect_cos   # north-south gradient component
slope_y    = tan(radians(slope_mean)) * aspect_sin   # east-west gradient component
```

These four columns are already in `dim_cells.csv` (added 2026-08-19 --
`export_powerbi.py`'s `load_terrain()` was only keeping the scalar fields
even though the source `terrain_100m2.csv` already had the vector ones;
re-run `python3 export_powerbi.py` if your copy predates this).

4. **Add a second scatter chart** (same `tile_mod = 0` filter): X =
   `slope_x`, Y = `decline_rate_mean`. This is the real relationship in
   the data -- `corr(slope_x, decline_rate_mean) = -0.21`, narrowly the
   strongest single correlation against decline intensity, just ahead of
   `corr(aspect_cos, decline_rate_mean) = -0.19` (both well past
   `slope_mean`'s 0.10 and raw `aspect_mean`'s -0.15). You'll see an
   actual diagonal cloud this time, not a blob. Since `slope_x` combines
   slope steepness with `aspect_cos` (north-facing-ness), and
   `decline_rate_mean` is a negative number (more negative = faster loss),
   the negative correlation means: **steep, north-facing cells lose NDVI
   fastest after peak; steep, south-facing cells hold up longest.** For a
   vineyard at ~46°N (Northern Hemisphere), that's the physically sensible
   read -- south-facing slopes get more direct solar exposure, and that
   extra warmth/light through fall tracks with canopy holding on longer
   into harvest rather than senescing fast.
5. The transferable lesson: when a directional/circular field (aspect,
   wind direction, time-of-day, day-of-year) doesn't correlate well as a
   raw number, decomposing it into sin/cos components before correlating
   or charting is the standard fix -- and it's not just a data-science
   trick, it's a one-line calculated field in Looker Studio or Tableau
   too (`COS(RADIANS(aspect_mean))`).

**Does the same trick work on curvature? Checked -- no, and that's worth
knowing too.** `curvature_mean` in this data is already a collapsed total
(literally `dxx + dyy` from the DEM's second derivatives), which mixes two
different physical things: curvature *along* the slope direction (controls
whether water/cold air speeds up or slows down as it flows downhill) and
curvature *across* the slope (controls whether flow converges into a
channel or spreads out over a ridge). The pipeline already computes both
separately -- `profile_curv_mean` (along-slope) and `plan_curv_mean`
(across-slope), also now in `dim_cells.csv`. Unlike the aspect case,
splitting curvature this way doesn't uncover a hidden signal against
either phenology rate: `corr(profile_curv_mean, decline_rate_mean) =
0.006` and `corr(plan_curv_mean, decline_rate_mean) = 0.015`, both about
as weak as `corr(curvature_mean, decline_rate_mean) = 0.015`; against
`buildup_rate_mean` the three are 0.041, -0.019, and 0.020 respectively --
still all weak. Add a third scatter (X = `profile_curv_mean`, Y =
`decline_rate_mean`) if you want to see this for yourself -- it'll look
like Page 2's first scatter (slope_mean), a flat blob, not like the second
one (slope_x). The lesson here is the opposite of the aspect case and just
as real: checking whether a decomposition reveals something is the actual
skill, not assuming it always will. Curvature genuinely isn't a driver in
this dataset, sliced either way -- which is also why Page 3's cohort
comparison below leaves it out of the `CASE WHEN` and only reports it as a
check.

### Page 3 -- Segment comparison: what IS different about the south-facing, steep cells

Page 2 found the real driver: `slope_x` (steepness combined with
orientation), narrowly ahead of `aspect_cos` alone. This page asks the
sharper version of Simon's original question with that in hand -- pick
cells that are BOTH relatively steep AND south-facing, and check whether
anything else about their terrain profile differs from everyone else's.
This is a calculated-field + grouped-bar pattern -- one of the most common
real BI dashboard moves, and Looker Studio does it with no formula beyond
`CASE WHEN`.

1. In the `dim_cells` data source, **Add a calculated field** named
   `cohort`:
   ```
   CASE
     WHEN aspect_cos <= -0.95 AND slope_mean >= 8.6
       THEN "South-facing + steep"
     ELSE "Everyone else"
   END
   ```
   (-0.95 and 8.6 are this data's actual 25th-percentile-most-negative
   cutoff for `aspect_cos` and 75th-percentile cutoff for `slope_mean` --
   recompute with `df['aspect_cos'].quantile(0.25)` /
   `df['slope_mean'].quantile(0.75)` if the pipeline data changes.)
2. **Add a chart > Bar chart** (or Column chart). Dimension: `cohort`.
   Metrics: `decline_rate_mean`, `buildup_rate_mean`, `elev_mean`,
   `curvature_mean` (set each to **Average**, not Sum, in the metric
   settings).
3. What you should see, checked against the current data (cohort n=2,853,
   rest n=30,175): `decline_rate_mean` is -0.00130/day for the cohort vs.
   -0.00147/day for everyone else -- the south-facing+steep cells decline
   more gently, consistent with Page 2's finding. `buildup_rate_mean`
   (0.00273 vs. 0.00271), `elev_mean` (184.8 vs. 185.2), and
   `curvature_mean` (0.00000 vs. -0.00001) are all flat between the two
   groups -- spring build-up speed, elevation, and local curvature don't
   explain anything once you've already selected on orientation and slope.
   That's the real finding this exercise surfaces: this cohort's
   distinctive trait is specifically how gently it declines after peak, not
   a general "does better on everything" effect, and orientation is doing
   the work rather than a second hidden terrain variable riding along with
   it.
4. This is the transferable pattern for a take-home or interview dashboard
   task: define a cohort with a `CASE WHEN` built on the variable you
   actually found evidence for, then compare its averages against the
   complement on every other dimension you have, to check whether that
   variable is really the whole story or just correlated with something
   else.

### Page 4 -- Map

A Google Maps or Bubble Map chart. These charts take ONE `Location`
dimension, not separate lat/lon fields -- `dim_cells.lat_lon` already has
them combined as `"lat,lon"` text, you just need to tell Looker Studio what
it is:
- In the field list (either in the data source editor, or click the field
  name in the chart's Location well), set **Type: Geo > Latitude, Longitude**
  on `lat_lon`. If your account doesn't show that exact geo subtype, use
  "Add a field" in the chart and write `CONCAT(lat, ",", lon)` instead, then
  type that.
- Location: `dim_cells.lat_lon`
- Color: `dim_cells.decline_rate_mean` (diverging color = which cells hold
  canopy longest into harvest vs. senesce fastest), `dim_cells.ndvi_trend_per_year`
  (the long-run 2016-2025 direction instead -- a different question, still
  valid for that), or `dim_cells.cohort` from Page 3 (categorical -- lets
  you see whether the "south-facing + steep" cells cluster spatially, which
  the scatter/bar charts can't show)
- Size: `dim_cells.elev_mean` or `dim_cells.slope_mean`

### Page 5 -- Weather

Line or column chart straight off `dim_years`:
- Dimension: `year`
- Metrics: `ppt_total`, `gdd`, `tmean_season`

### Scorecards

Total cell count, average `buildup_rate_mean`/`decline_rate_mean`, min/max
elevation, cohort size from Page 3 (`COUNT_DISTINCT(tile_id)` filtered to
`cohort = "South-facing + steep"`).

**Once clustering.ipynb is rerun against the current grid** and produces a
`clusters.csv` keyed to the current `tile_id`, add `load_clusters()` back
into `export_powerbi.py`'s `dim_cells` merge -- `cluster` becomes a real,
model-derived categorical dimension to color/breakdown by instead of the
hand-built `cohort` field above.

## 4. What this teaches vs. the matplotlib version

Same chart vocabulary you already know (map, line, scatter) plus two moves
matplotlib scripts don't usually practice: ranking with a live sort/row-limit
instead of `.sort_values().head()`, and defining a segment with a UI-native
`CASE WHEN` and comparing its averages against the complement -- the
calculated-field-plus-groupby pattern that shows up constantly in BI
take-homes regardless of vendor.

## 5. If Tableau access ever gets sorted out

`dim_cells.csv`, `dim_years.csv`, and `fact_ndvi_yearly.csv` are plain flat
files -- Tableau Public reads them directly via Data > Connect to Data >
Text File, no reshaping needed beyond what `export_powerbi.py` already
does. The join step is the same star-schema Blend/relationship concept
under a different name (Tableau calls it a Relationship, drag `tile_id` to
`tile_id` and `year` to `year` in the Data Source pane). The cohort
calculated field in Page 3 is a Tableau "Calculated Field" with the same
`CASE WHEN` syntax; the scatter and bar charts are built-in mark types
there too.

Parked for now, not built further: Tableau Public has no Linux desktop
client (Windows/Mac only, even on the free tier), so there's nothing to
actually author here until that's resolved one way or another.
