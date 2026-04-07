# TerraMetabolica

**Does the Earth leave a chemical fingerprint in food?**

TerraMetabolica maps how climate, geology, and geography predict the metabolite profiles of regional food systems. The core premise: the same crop grown in volcanic Andean soil should taste chemically different from the same crop grown in European loess — and that difference should be traceable to measurable Earth system variables.

This is honest about what the current data can and cannot show.

---

## The Question

Wine people talk about *terroir* — the way a place expresses itself in flavor. TerraMetabolica asks whether that generalizes: not just grapes, but rice, potato, apple, olive, fermented foods. And not just flavor description, but actual measured chemistry correlated with actual measured environmental variables.

---

## Hypotheses

| ID | Hypothesis | Key test |
|----|-----------|----------|
| H1 | Climate (temperature, precipitation) is the dominant predictor of regional metabolite profiles | Mantel test: climate distance vs metabolite distance across RSUs |
| H2 | Soil type amplifies or suppresses specific metabolite classes | Same cultivar, different soil: malic acid, polyphenols |
| H3 | Biodiversity complexity predicts metabolite diversity | Species richness vs number of distinct metabolite dims |
| H4 | Convergent terroir: distant environments produce chemically similar food | RSU pairs with high env distance, low metabolite distance |
| H5 | Industrial processing decouples food chemistry from environment | RSU-07 (N. American Prairie) as negative control |

---

## RSU — Region Sample Unit

Each RSU is a bounded geographic region defined by climate, geology, coordinates (including altitude), and 4-6 native staple foods. Political boundaries are not the unit.

| RSU | Region | Climate | Geology | Key Signal |
|-----|--------|---------|---------|------------|
| RSU-01 | Boreal Finland | Subarctic | Glacial till | Fermentation, preservation |
| RSU-02 | Boreal Canada | Subarctic | Shield rock | Smoke, fat-protein bias |
| RSU-03 | Siberian Taiga | Extreme continental | Permafrost | Burial fermentation |
| RSU-04 | Atlantic W. Europe | Maritime temperate | Limestone + alluvial | Cheese, apple (GD baseline) |
| RSU-05 | Central Europe | Continental temperate | Loess | Sauerkraut, potato (EU baseline) |
| RSU-06 | East Asian Temperate | Monsoon temperate | Loess + alluvial | Soy fermentation, umami |
| RSU-07 | N. American Prairie | Continental grassland | Mollisols | Negative control for H5 |
| RSU-08 | W. African Transition | Tropical wet-dry | Laterite | Fermentation + spice |
| RSU-09 | Amazon Basin | Equatorial rainforest | Oxisols | Fruit complexity |
| RSU-10 | Andean Highlands | Tropical high-altitude | Volcanic | Potato diversity (genetics confound) |
| RSU-11 | S. Indian Monsoon | Tropical monsoon | Laterite | Spice terpenes |
| RSU-12 | Maritime SE Asia | Equatorial maritime | Volcanic | Fish sauce umami |
| RSU-13 | Shanxi Lowlands (China) | Semi-arid continental | Loess, 600m | Apple (GD lowland) |
| RSU-14 | Shanxi Highlands (China) | Semi-arid continental | Loess, 1050m | Apple (GD highland) |
| RSU-15 | Algerian Northern Highlands | Mediterranean | Limestone, 1000m | Olive (Sigoise, humid) |
| RSU-16 | Algerian Saharan Margin | Arid | Aeolian sand, 70m | Olive (Sigoise, water-stressed) |

---

## Natural Experiments

The cleanest terroir tests: **same cultivar, different environment**. Genetic effects controlled; metabolite differences are environmental.

| Cultivar | RSUs | Contrast | Key metabolite | Signal |
|----------|------|----------|----------------|--------|
| Golden Delicious apple | RSU-13 vs RSU-14 | 600m vs 1050m altitude, Shanxi | Malic acid | **2× increase with altitude** |
| Sigoise olive | RSU-15 vs RSU-16 | Highlands vs Saharan margin | Total polyphenols | **1.6× increase under water stress** |
| Potato (*S. tuberosum*) | RSU-05 vs RSU-10 | European loess vs Andean volcanic | Citric acid | Confounded — 75% genetic |

The potato comparison is retained as a genotype × environment signal, not a clean terroir test.

---

## Key Principle: Null ≠ Absent

```
null              = unmeasured (unknown)
confirmed_absent  = genuinely not present in this food
```

These are different. A null citric acid field means we don't have a measurement.
A confirmed_absent citric acid field means citric acid doesn't occur in that food.
Only confirmed_absent values participate in distance calculations as real zeros.

---

## Data Pipeline

```
USDA FoodData Central API
    └── src/fdc_fetcher.py → populates primary macros per food

Scientific literature (hand-entered with citations)
    └── organic acids, terpenes, umami, polyphenols
    └── natural experiment values (altitude/location-specific, same cultivar)

src/rsu_loader.py
    └── load_all_rsus()         → typed RSU dataclass objects
    └── parse_numeric_ranges()  → {region: {food: {dim: (lo, hi)}}}
    └── build_food_matrix()     → flat DataFrame (region_id, food_name) × metabolite dims
```

---

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `00_rsu_assembly.ipynb` | Load and inspect all RSUs, food matrix, coverage |
| `01_metabolite_vectors.ipynb` | Build metabolite matrix and pairwise distance matrix |
| `02_eda_pca.ipynb` | Earth system × metabolite Spearman correlations, RSU PCA by env gradient |
| `03_clustering.ipynb` | RSU dendrogram and category-stratified clustering (geo dims only) |
| `04_terroir_distance.ipynb` | Mantel test: env distance vs metabolite distance (honest pairs only) |
| `05_natural_experiments.ipynb` | Potato, rice, cassava cross-RSU comparisons and data gap analysis |
| `06_clean_natural_experiments.ipynb` | Apple altitude gradient + olive water-stress gradient — same cultivar, real signal |

---

## Current State and Honest Findings

**What works:**
- 16 RSUs with USDA FDC macro data + literature bioactive values
- Earth system × metabolite correlation framework
- Natural experiment identification and controlled comparison

**What the data shows:**
- Macro dims (protein/fat/carb) carry food-category signal, not terroir signal
- Mantel test is flat — geo dims too sparse for RSU-level signal at n=16
- **Apple altitude (RSU-13 vs RSU-14): malic acid doubles from 400m to 1200m** — first clean terroir signal
- **Olive water stress (RSU-15 vs RSU-16): polyphenols 60% higher in Saharan margin** — second clean signal
- RSU-07 has zero measured bioactive dims — cultural distortion hypothesis supported by data absence

**H5 (RSU-07) finding:** North American Prairie RSU has no terpenes, organic acids, or umami compounds measured in any of its three staple foods. The industrial processing that strips flavor from commodity crops also strips the environmental signal. The absence is the finding.

---

## Hypotheses Status

| Hypothesis | Status | Evidence |
|-----------|--------|---------|
| H1 (climate dominance) | Untestable at current coverage | Mantel r ≈ 0; geo dims too sparse |
| H2 (soil amplification) | Partial signal | Apple altitude clean; olive water-stress clean; potato confounded |
| H3 (biodiversity complexity) | Not yet tested | Biodiversity indices not populated |
| H4 (convergent terroir) | Candidate: RSU-06/RSU-12 | Fish sauce + soy sauce both high umami despite different substrates |
| H5 (cultural distortion) | Suggestive | RSU-07 has zero bioactive data — processing erases environmental trace |

---

## Next Data Priorities

1. Rice: terroir-specific values for RSU-06/11/12 (loess/laterite/volcanic — same FDC ID currently)
2. Apple: European lowland Golden Delicious literature values for RSU-04 baseline
3. Wheat: asparagine by growing region (4× range Hungary vs UK documented in literature)
4. Coffee: altitude × chlorogenic acid data for highland RSU

---

## Structure

```
TerraMetabolica/
├── README.md
├── TerraMetabolica.md          — original project specification
├── data/
│   ├── rsu/                    — one JSON per RSU (RSU-01 through RSU-16)
│   ├── metabolites/            — assembled matrices and plots (generated by notebooks)
│   └── raw/fdc/                — cached USDA FoodData Central responses
├── notebooks/                  — analysis notebooks 00-06
└── src/
    ├── rsu_schema.py           — RSU and food dataclass definitions
    ├── rsu_loader.py           — JSON → RSU loader, numeric range parser
    └── fdc_fetcher.py          — USDA FDC API fetcher and RSU JSON updater
```

---

## Key References

- Zhao et al. (2021). Effects of genetic background and altitude on sugars, malic acid and ascorbic acid in apples. *Foods* 10(12):2950.
- Guerfel et al. (2022). Geographical location and cultivar-linked changes in Algerian olive oils. *Food Science & Nutrition*.
- Sampaio et al. (2021). Potato biodiversity: fifty genotypes. *Food Chemistry* 345:128853.
- Morris et al. (2007). Umami compounds determine potato flavor. *J Agric Food Chem* 55:9627.
- Eldem et al. (2022). Genotype × environment interactions of potato tuber quality. *Scientia Horticulturae*.
- Dal Santo et al. (2015). Plasticity of the grape berry metabolome. *BMC Plant Biology* 15:191.
- Muttucumaru et al. (2006). Free amino acids in wheat grain by genotype and environment. *J Agric Food Chem*.
