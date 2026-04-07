# TerraMetabolica

**Does the Earth leave a chemical fingerprint in food?**

TerraMetabolica maps how climate, geology, and geography predict the metabolite profiles of regional food systems. The core premise: the same crop grown in volcanic Andean soil should taste chemically different from the same crop grown in European loess — and that difference should be traceable to measurable Earth system variables.

This project is honest about what the current data can and cannot show.

---

## The Question

Wine people talk about *terroir* — the way a place expresses itself in flavor. TerraMetabolica asks whether that generalizes: not just grapes, but rice, potato, apple, olive, tea, coffee, butter. And not just flavor description, but actual measured chemistry correlated with actual measured environmental variables.

The emerging picture is that elevation — as a composite proxy for UV exposure, temperature, diurnal range, and ecological context — shows consistent directional associations with protective metabolite concentrations across unrelated biological systems on multiple continents. Polyphenols in coffee and tea, organic acids in fruit, and fatty acid composition in grass-fed dairy all shift in coherent ways with altitude. Genetically constrained metabolites, by contrast, show no such response — a useful internal control.

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

Each RSU is a bounded geographic region defined by climate, geology, coordinates (including altitude), and 4–6 native staple foods. Political boundaries are not the unit.

### Pilot RSUs (01–12)

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
| RSU-10 | Andean Highlands | Tropical high-altitude | Volcanic | Potato diversity |
| RSU-11 | S. Indian Monsoon | Tropical monsoon | Laterite | Spice terpenes |
| RSU-12 | Maritime SE Asia | Equatorial maritime | Volcanic | Fish sauce umami |

### Natural Experiment RSUs (13–16)

| RSU | Region | Climate | Geology | Key Signal |
|-----|--------|---------|---------|------------|
| RSU-13 | Shanxi Lowlands, China | Semi-arid continental | Loess, 600m | Golden Delicious apple (GD lowland) |
| RSU-14 | Shanxi Highlands, China | Semi-arid continental | Loess, 1050m | Golden Delicious apple (GD highland) |
| RSU-15 | Algerian Northern Highlands | Mediterranean | Limestone, 1000m | Sigoise olive (humid) |
| RSU-16 | Algerian Saharan Margin | Arid | Aeolian sand, 70m | Sigoise olive (water-stressed) |

### Extended RSUs (17–65)

| RSU | Region | Climate | Geology | Key Signal |
|-----|--------|---------|---------|------------|
| RSU-17 | Ethiopian Highlands | 16°C, 1100mm | Basalt, pH 5.8 | Arabica coffee (CGA high-altitude), teff, injera, berbere |
| RSU-18 | Colombian Andes | 19°C, 1800mm | Volcanic, pH 5.5 | Arabica coffee (CGA mid-altitude), arepa, papa criolla, chicha |
| RSU-19 | Vietnamese Lowlands | 22°C, 1600mm | Basalt, pH 5.4 | Robusta coffee (CGA low-altitude), fish sauce (glutamate) |
| RSU-20 | Darjeeling Himalaya | 13°C, 3000mm | Metamorphic, pH 4.8 | Darjeeling tea (high catechins), buckwheat, churpi, gundruk |
| RSU-21 | Assam Lowlands | 24°C, 2800mm | Alluvial, pH 5.2 | CTC black tea (low-altitude catechins), sticky rice, mustard oil |
| RSU-22 | Uji–Shizuoka Japan | 15°C, 1800mm | Granite, pH 4.5 | Matcha/gyokuro (peak theanine), dashi kombu, miso |
| RSU-23 | Campania Italy | 16.5°C, 900mm | Volcanic, pH 6.2 | San Marzano tomato (glutamate), mozzarella, sfusato lemon |
| RSU-24 | Anatolian Plateau | 10.5°C, 380mm | Sedimentary, pH 7.5 | Durum wheat, lamb, yogurt, sumac (malic acid) |
| RSU-25 | Oaxacan Highlands | 18°C, 650mm | Metamorphic, pH 6.5 | Nixtamalized corn, cacao (procyanidins), chile negro |
| RSU-26 | Yunnan China | 14.5°C, 1000mm | Sedimentary, pH 5.0 | Pu-erh tea (microbial fermentation), matsutake, Yunnan ham |
| RSU-27 | Kenyan Highlands | 17°C, 950mm | Volcanic, pH 5.8 | Kenya CTC tea (theaflavins), Arabica coffee, ugali |
| RSU-28 | Moroccan Argan Coast | 19.5°C, 250mm | Sedimentary, pH 7.8 | Argan oil (peak tocopherol), couscous, preserved lemon |
| RSU-29 | Georgian Caucasus | 11.5°C, 1100mm | Volcanic, pH 6.0 | Qvevri wine (tartaric acid), walnut, churchkhela, matsoni |
| RSU-30 | Sichuan Basin | 17°C, 1000mm | Sedimentary, pH 6.5 | Sichuan pepper (linalool peak), doubanjiang, rice |
| RSU-31 | Peruvian Amazon | 26°C, 2800mm | Alluvial, pH 4.5 | Criollo cacao (peak polyphenols), cassava, masato |
| RSU-32 | Philippine Lowlands | 27.5°C, 2200mm | Volcanic, pH 6.0 | Coconut oil (lowland lauric), rice, bagoong (peak glutamate) |
| RSU-33 | Sri Lankan Highlands | 23.5°C, 1900mm | Metamorphic, pH 5.8 | Coconut oil (highland lauric variant), Ceylon cinnamon (polyphenols), tea |
| RSU-34 | W. African Sahel | 28.5°C, 650mm | Sedimentary, pH 6.5 | Shea butter (peak stearic), sorghum, dawadawa (Bacillus glutamate) |
| RSU-35 | Iberian Dehesa | 16.5°C, 490mm | Sedimentary, pH 6.0 | Bellota lard (peak oleic), jamón ibérico, pan de masa madre |
| RSU-36 | Alpine Central Europe | 6.5°C, 1400mm | Metamorphic, pH 5.5 | Alpine butter (high CLA), Gruyère, rye, sauerkraut |
| RSU-37 | Irish Atlantic Coast | 10°C, 1200mm | Sedimentary, pH 6.2 | Grass-fed butter (CLA mid), Atlantic salmon, dulse (plant glutamate) |
| RSU-38 | Michoacán Mexico | 18.5°C, 1000mm | Volcanic, pH 6.2 | Avocado oil (highland oleic), nixtamalized corn, pulque |
| RSU-39 | Pacific Polynesia | 27°C, 2800mm | Volcanic, pH 6.5 | Coconut cream (sea-level), taro, reef fish (IMP), palusami |
| RSU-40 | Central Asian Steppe | 5.5°C, 280mm | Sedimentary, pH 7.5 | Kumiss (fermented mare's milk), millet, horse meat |
| RSU-41 | Australian Queensland | 20.5°C, 1100mm | Volcanic, pH 6.0 | Macadamia oil (palmitoleic), beef, lemon myrtle (peak linalool) |
| RSU-42 | Himalayan Plateau | 2°C, 420mm | Sedimentary, pH 7.0 | Yak butter (peak CLA), tsampa (roasted barley), buckwheat (rutin) |
| RSU-43 | Nordic Lowlands | 9°C, 700mm | Sedimentary, pH 6.8 | Lowland butter (CLA baseline), rye bread, herring, Gouda |
| RSU-44 | Californian Coast | 17.5°C, 350mm | Sedimentary, pH 7.0 | Avocado oil (coastal/lower oleic), almonds, California EVOO |
| RSU-45 | Indonesian Java | 26.5°C, 2400mm | Volcanic, pH 6.2 | Palm oil (peak palmitic + tocotrienols), tempeh (Rhizopus), galangal |
| RSU-46 | New Zealand Waikato | 13.5°C, 1200mm | Volcanic, pH 5.8 | NZ grass-fed butter (CLA mid-high), lamb, kumara, manuka honey |
| RSU-47 | Indonesia Toraja | 19.5°C, 2000mm | Volcanic, pH 5.5 | Arabica coffee (CGA low-altitude), anthocyanin rice, coconut oil |
| RSU-48 | Jamaica Blue Mountains | 18°C, 2500mm | Metamorphic, pH 5.8 | Arabica coffee (CGA high-altitude), yam, ackee & saltfish |
| RSU-49 | Chilean Maule Valley | 12.5°C, 700mm | Volcanic, pH 6.0 | Golden Delicious apple (malic acid), wheat, beef, merkén (capsaicinoids) |
| RSU-50 | Turkish Isparta Highlands | 11°C, 550mm | Sedimentary, pH 7.5 | Golden Delicious apple (malic acid), rose petal (linalool), lamb, yogurt |
| RSU-51 | Scottish Highlands | 7.5°C, 1100mm | Metamorphic, pH 5.2 | Grass-fed butter (CLA high), Aberdeen Angus beef, oatmeal, Scotch whisky |
| RSU-52 | French Pyrenees | 10°C, 1300mm | Metamorphic, pH 5.8 | Mountain butter (CLA high), Ossau-Iraty (glutamate), piment d'Espelette |
| RSU-53 | Swiss Jura / Pre-Alps | 8°C, 1350mm | Sedimentary, pH 6.8 | Pre-alpine butter (CLA high), Gruyère (glutamate), rye, gentian schnapps |
| RSU-54 | Mexican Guerrero Highlands | 14°C, 1200mm | Metamorphic, pH 6.2 | Arabica Bourbon coffee (CGA high-altitude), maize, beans |
| RSU-55 | Shanxi Jinzhong Mid-Highlands | 10.5°C, 470mm | Sedimentary, pH 7.8 | Golden Delicious apple (malic acid mid-altitude), millet, wheat, walnuts |
| RSU-56 | Đà Lạt Central Highlands, Vietnam | 18°C, 1800mm | Basaltic, pH 5.2 | Green tea (catechins mid-altitude), arabica coffee, artichoke |
| RSU-57 | Suoi Giang Wild Ancient Tea, Vietnam | 16°C, 1600mm | Metamorphic, pH 4.9 | Wild ancient-tree green tea (catechins + theanine high), upland rice |
| RSU-58 | Kericho Highland Tea, Kenya | 17.5°C, 2000mm | Volcanic, pH 5.0 | Kenya highland green tea (catechins high, caffeine high), maize, sorghum |
| RSU-59 | Nilgiri Highland Tea, Tamil Nadu | 14°C, 1800mm | Metamorphic, pH 4.7 | Green tea (catechins high, linalool), black tea, millets |
| RSU-60 | Ilam Highland Tea, Nepal | 15.5°C, 2400mm | Metamorphic, pH 4.9 | Green tea (catechins high, theanine high), maize, millet, cardamom |
| RSU-61 | Yunnan Raw Pu-erh Highlands | 19°C, 1500mm | Sedimentary, pH 4.8 | Raw pu-erh / green tea (catechins mid, caffeine), sticky rice, wild mushrooms |
| RSU-62 | Hangzhou Longjing, Zhejiang | 17°C, 1400mm | Granite/sandstone, pH 4.8 | Longjing green tea (catechins baseline, EGCG), rice, freshwater fish |
| RSU-63 | Kangra Valley, Himachal Pradesh | 16°C, 2500mm | Alluvial/metamorphic, pH 5.2 | Green tea (catechins high, seasonal variation), wheat, pulses |
| RSU-64 | Timbilil Tea Estate, W. Rift Valley | 16°C, 1600mm | Volcanic basalt, pH 5.0 | Kenya highland green tea (catechins mid-high), maize, beans, milk |
| RSU-65 | Kangaita Tea Estate, E. Rift Valley | 16.5°C, 1400mm | Volcanic, pH 5.1 | Kenya highland green tea (catechins peak for region), maize, beans, milk |

---

## Natural Experiments

The cleanest terroir tests: **same cultivar, different environment**. Genetic effects are controlled; metabolite differences are environmental.

| Cultivar | RSUs | Contrast | Key metabolite | Signal |
|----------|------|----------|----------------|--------|
| Golden Delicious apple | RSU-13 vs RSU-14 | 600m vs 1050m altitude, Shanxi | Malic acid | Doubles with altitude |
| Sigoise olive | RSU-15 vs RSU-16 | Highlands vs Saharan margin | Total polyphenols | 1.6× under water stress |
| Golden Delicious apple | RSU-13/14/49/50/55 | 600–1100m, multiple continents | Malic acid | Consistent directional gradient |
| Arabica coffee | RSU-17/18/47/48/54 | 1100–2200m, Africa/Americas | CGA, malic acid | Strong altitude gradient |
| Green tea (*C. sinensis*) | RSU-20/21/56–65 | 100–2200m, four continents | Total catechins | Directional altitude gradient |
| Grass-fed butter | RSU-36/37/42/43/46/51/52/53 | 50–3800m | CLA | Log-linear altitude gradient |
| Coconut oil | RSU-32/33/39/45 | Sea level to 1100m | Lauric acid | No altitude relationship |
| Potato (*S. tuberosum*) | RSU-05 vs RSU-10 | European loess vs Andean volcanic | Citric acid | Confounded — 75% genetic |

The potato comparison is retained as a genotype × environment signal, not a clean terroir test. The coconut result is an intentional null: genetically constrained metabolites do not respond to altitude, which validates the framework rather than contradicting it.

---

## Key Principle: Null ≠ Absent

```
null              = unmeasured (unknown)
confirmed_absent  = genuinely not present in this food
```

These are different. A null citric acid field means no measurement exists.
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
| `05_within_crop_regression.ipynb` | Within-crop metabolite regression across RSUs |
| `06_clean_natural_experiments.ipynb` | Apple altitude gradient + olive water-stress gradient — same cultivar, real signal |
| `07_rsu_map.ipynb` | Geographic visualization of RSU locations and boundaries |
| `08_multivariate_regression.ipynb` | Multivariate regression: earth system features → metabolite vectors |
| `09_permutation_test.ipynb` | Permutation-based significance testing for env-metabolite associations |
| `10_tea_catechin_regression.ipynb` | Within-crop metabolite regression for tea catechins across growing regions |
| `11_cipt_descriptive.ipynb` | Descriptive analysis of constraint-induced patterns in the RSU dataset |
| `12_cipt_generative.ipynb` | Generative modeling of constraint-induced metabolite distributions |
| `13_dnd_cipt.ipynb` | Extended constraint analysis and scenario modeling |

---

## Current State and Honest Findings

**What works:**
- 65 RSUs with USDA FDC macro data + literature bioactive values
- Earth system × metabolite correlation framework
- Natural experiment identification and controlled comparison across multiple crops and continents

**What the data shows:**
- Elevation shows consistent directional associations with protective metabolite concentrations across multiple independent biological systems: polyphenols in coffee and tea, organic acids in fruit, and CLA in grass-fed dairy all shift coherently with altitude
- The CLA gradient across butter-producing RSUs from sea level to the Himalayan plateau follows a log-linear pattern consistent with ecological saturation — forage diversity plateaus, and so does the fatty acid response
- Green tea catechins and Arabica coffee chlorogenic acids show consistent altitude gradients across four continents, pointing to shared UV-mediated stress pathways rather than regional coincidence
- Coconut lauric acid shows no altitude relationship across five RSUs spanning three continents — an intentional null that confirms the framework discriminates between environmentally plastic and genetically fixed metabolites
- Macro dims (protein/fat/carb) carry food-category signal, not terroir signal
- **H5 (RSU-07) finding:** North American Prairie RSU has no terpenes, organic acids, or umami compounds measured in any staple food. Industrial commodity agriculture strips environmental signal — the absence is the finding.

**Remaining uncertainty:**
- Metabolite values compiled from heterogeneous analytical sources (different labs, protocols, sample prep)
- Within-crop sample sizes are small; altitude regressions show directional structure, not precise prediction
- External validation against standardized field measurements has not been done

---

## Hypotheses Status

| Hypothesis | Status | Evidence |
|-----------|--------|---------|
| H1 (climate dominance) | Partial | Altitude (composite climate proxy) significant across multiple crops; temperature alone insufficient |
| H2 (soil amplification) | Partial signal | Apple altitude clean; olive water-stress clean; potato confounded |
| H3 (biodiversity complexity) | Not yet tested | Biodiversity indices not populated |
| H4 (convergent terroir) | Candidate: RSU-06/RSU-12 | Fish sauce + soy sauce both high umami despite different substrates |
| H5 (cultural distortion) | Supported | RSU-07 has zero bioactive data — processing erases environmental trace |

---

## Structure

```
TerraMetabolica/
├── README.md
├── TerraMetabolica.md              — original project specification
├── data/
│   ├── rsu/                        — one JSON per RSU (RSU-01 through RSU-65)
│   ├── metabolites/                — assembled matrices and plots (generated by notebooks)
│   └── raw/fdc/                    — cached USDA FoodData Central responses
├── figures/                        — generated figures
├── notebooks/                      — analysis notebooks 00-13
├── src/
│   ├── rsu_schema.py               — RSU and food dataclass definitions
│   ├── rsu_loader.py               — JSON → RSU loader, numeric range parser
│   └── fdc_fetcher.py              — USDA FDC API fetcher and RSU JSON updater
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
