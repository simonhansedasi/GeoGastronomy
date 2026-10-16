# GrapeExpectations → Kona Coffee Extension (Ridge + NDVI)

## Objective

Recreate the GrapeExpectations workflow for coffee farms in Kona (Big Island, Hawaii), using ridge regression and NDVI-derived vegetation response.

Goal:
> Learn environmental + biological fingerprints of coffee-growing land and predict similar regions within Hawaii.

---

## Scope

- Geographic scope: Big Island (expand later)
- Focus: environmental similarity + suitability scoring
- No yield prediction
- No soil modeling (MVP)

---

## Workflow Overview

1. Define region polygon
2. Generate sampling grid
3. Label coffee farms
4. Extract environmental features
5. Extract NDVI time series
6. Build feature matrix
7. Train ridge regression model
8. Predict across region
9. Visualize results

---

## 1. Region Definition

User provides polygon bounding Kona coffee region.

---

## 2. Grid Sampling

- Generate uniform grid (250m–500m resolution)
- Each grid cell = one sample

Each cell has:
- geometry
- centroid

---

## 3. Labeling

User draws polygons for coffee farms.

Cell labels:
- 1 = inside coffee polygon
- 0 = background (inside region, not labeled)
- -1 = ignore (optional)

Important:
- No manual negative labeling

---

## 4. Environmental Features

Per cell:

- elevation
- slope
- aspect
- rainfall_annual
- rainfall_seasonality
- temp_mean
- temp_range
- distance_to_coast

---

## 5. NDVI Time Series

Per cell:
- collect NDVI over time
- smooth (rolling mean or spline)

Derived features:

- ndvi_mean
- ndvi_variance
- ndvi_min
- ndvi_max
- ndvi_seasonality
- ndvi_stability

---

## 6. Feature Matrix

Each sample:

features = [env + ndvi]
label = 1 or 0

---

## 7. Model: Ridge Regression (REQUIRED)

We model:

Probability of coffee-suitable environment.

Form:

y = β0 + β1x1 + ... + βnxn

Loss:

MSE + λ * Σ(β^2)

Steps:
1. Normalize features
2. Train/test split
3. Train ridge model
4. Tune λ

---

## 8. Prediction

Apply model to all grid cells.

Output:
- continuous score per cell
- interpreted as suitability likelihood

---

## 9. Output

- Heatmap of suitability
- Highlight high-scoring regions

---

## 10. Interpretation

Expose coefficients:

- understand feature importance
- debug model

---

## 11. Validation

Model should:
- score known coffee regions highly
- show mid-elevation band
- suppress dry coastal zones

---

## 12. Design Principles

- Grid-based sampling
- Minimal manual labeling
- NDVI = vegetation response (not yield)
- Ridge regression = core model

---

## 13. Non-Goals

- No crop prediction
- No global search
- No black-box models

---

## 14. Implementation Priority

1. Grid generation
2. Label assignment
3. Feature extraction
4. NDVI processing
5. Ridge regression
6. Spatial prediction
7. Visualization

---

## Final Instruction

The modeling approach MUST follow ridge regression as used in GrapeExpectations. Do not substitute with clustering or black-box models in MVP.

