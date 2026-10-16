# Reviewer Pass — "No Labels, No Problem: Unsupervised Terrain Fingerprinting..."

**Pass date:** 2026-04-09
**Target:** Remote Sensing of Environment (RSE)
**Verdict:** Revise substantially before submission. The science is sound and the contribution is real, but there are methodological transparency gaps that an RSE reviewer will pierce, and the framing inconsistencies will generate a rejection before anyone gets to the interesting parts.

Severity: **CRITICAL** (likely rejection trigger) / **MAJOR** (significant revision required) / **MINOR** (fixable at proofing).

---

## Title and Abstract

**[MAJOR] Title undermines discoverability and signals methodological narrowness.**
"No Labels, No Problem" is a catchy blog title. RSE editors have seen every permutation of this construction. More importantly, leading with the demonstration case ("Cannabis") suppresses citation uptake in the remote sensing community. A paper titled around a controlled substance gets systematically excluded from syllabi, corporate citation networks, and grant proposals that use keyword screening. The UTF framework — the actual contribution — is buried in the subtitle. Consider: "Unsupervised Terrain Fingerprinting: Recovering Crop Suitability Archetypes from Unlabeled Earth Observation Data" with the Emerald Triangle application as the demonstration case in the subtitle or byline. Let the method lead.

**[MAJOR] Abstract introduces "EO" as a term before defining it.**
The final results sentence uses "EO" (Earth Observation) in the context of ablation results without having introduced it earlier in the abstract. A reader skimming the abstract for the first time does not know what was ablated. Either spell it out ("removing Sentinel-2 NDVI features") or define EO on first use in the abstract.

**[MAJOR] Abstract validation sentence is missing the chi-square value.**
The abstract reads `$p = 3.8 \times 10^{-8}$` without the chi-square statistic. RSE reviewers expect the test statistic and degrees of freedom alongside the p-value. Should be: `$\chi^2(4) = 40.3$, $p = 3.8 \times 10^{-8}$, Cramér's $V = 0.33$`.

---

## §2 Cannabis Environmental Requirements

**[MAJOR] VPD unit mismatch degrades verification table credibility.**
The verification table shows a checkmark for VPD, but the comparison is between indoor cultivation targets (typically expressed in kPa, measured at canopy level, reflecting relative humidity and temperature at the plant surface) and Daymet daily maximum atmospheric VPD in Pa. These are not the same quantity. The caption acknowledges this is a "directional comparison," but the checkmark in the body of the table implies quantitative agreement. An RSE reviewer with any crop physiology background will object. Options: (a) remove the checkmark and replace with a direction arrow, or (b) add a column that makes the unit mismatch explicit. As-is, this looks like you're trying to slip something past the reviewer.

**[MINOR] UNODC citation for "25,000–50,000 cultivation sites" is probably wrong.**
UNODC's World Drug Report covers global and national estimates, not sub-county Emerald Triangle counts. Verify this number is actually in UNODC 2022 and that it refers to the Emerald Triangle specifically. If it's a national or statewide estimate, either replace the citation with a California-specific source or remove the specific number. A reviewer who checks this reference and finds it doesn't support the claim will flag the entire introduction.

---

## §4 Data and Features

**[CRITICAL] Cluster 3 "data void/coast" is unexplained and methodologically suspicious.**
The paper states that 639 cells form a "data void/coast" cluster. How did 639 valid 2 km hex cells — cells that were generated over the study area and included in the feature matrix — end up with insufficient data to be clustered with the rest? If they were median-imputed at the edge (as stated in §4/§5 Methods), they should not form a separate cluster unless their imputed values systematically differ from all other clusters. This looks like a data quality issue that's being quietly absorbed by the clustering. An RSE reviewer will ask: were these cells included in the 8,900 or excluded? If excluded, where does 8,648 come from? If included, what does it mean that one entire cluster is a data artifact? This needs explicit treatment in Methods §5.1 (data assembly) and a note in Limitations.

**[MAJOR] Cell count inconsistency: 8,900 vs 8,648.**
The paper consistently references 8,900 hex cells (study area grid) but the bootstrap caption says "applied to all 8,648 cells." The feature ablation presumably also uses 8,648. What happened to 252 cells? If edge cells were dropped during feature assembly, this should be stated explicitly in the Methods data assembly step. As-is, a reviewer who notices this will think you don't know your own sample size.

---

## §5 Methods

**[CRITICAL] ndvi_std circularity: same variable in clustering and regression target.**
NDVI_std enters the feature matrix (features_scaled.pkl), participates in PCA, and therefore influences the cluster boundaries that define cluster 2. Then §5.3 uses NDVI_std as the regression target within cluster 2. This creates a circularity: the cells in cluster 2 were partly selected for having a certain NDVI_std signature (or absence thereof), and then you ask "what predicts NDVI_std within cluster 2?" The within-zone R² and the importance rankings may partly reflect the clustering's own selection criteria rather than independent relationships. This is the single most likely CRITICAL reviewer comment. You need to either: (a) acknowledge this explicitly and argue it's acceptable (e.g., the clustering was on 18+ features, NDVI_std is one of them, and pH dominance in regression reflects independent variance), or (b) re-run the clustering without NDVI_std and show the archetype is stable (then the regression is clean). Option (b) is cleaner but you have it partially via the ablation analysis — Stack C (no EO) still recovers the archetype at 4/4 criteria. Use this to your advantage.

**[MAJOR] Synthetic RF "sanity check" is methodologically unorthodox without citation.**
The PCA validation step (§5.1/ML/01) uses a synthetic RF trained on real-vs-shuffled labels to assess feature informativeness. This is an unusual procedure that is not standard in the remote sensing PCA literature. Without a citation for this method and a clear explanation of what it tests (feature independence from random noise? PCA loadings validation?), an RSE reviewer will either ask what it is or dismiss it. Either cite a paper that uses this approach, or replace it with a more conventional PCA validation (variance explained by component, loadings heatmap, Scree plot). If the synthetic RF is the source of the "permutation importance" results discussed later, the relationship between this step and §5.3's permutation importance needs to be clearly distinguished.

**[MAJOR] K=5 selection criterion is never stated.**
The paper says "We applied k-means with K=5" but never explains why K=5. Elbow plot? Silhouette score? Average Dunn index? An RSE reviewer will ask this in every cluster analysis paper. The robustness section shows 4/4 criteria recovery at K=4–7, which is excellent, but that's post-hoc justification, not an a priori selection criterion. Add one sentence in Methods §5.2: "K=5 was selected based on [criterion]; sensitivity to K choice is assessed in §5.5."

**[MAJOR] Feature weighting in sub-clustering (§5.4) is underspecified.**
"Sub-clustering on importance-weighted features" says nothing about how weighting was implemented. Did you multiply each feature column by its permutation importance score before standardizing? Use importance as sampling weights? Select the top-N features? This is a methodological choice that affects the result and needs to be specified precisely. A reviewer cannot assess reproducibility without this detail.

**[MAJOR] Bootstrap prediction method is non-standard and needs justification.**
§5.5 describes bootstrap stability: "K-means fitted on 80% subsample and applied to all 8,648 cells." Applying a K-means fitted on a subsample to a full dataset is done by assigning each held-out point to its nearest centroid. This is a valid approach (it's essentially predicting cluster membership for out-of-sample points) but it's not standard and it has known issues: centroids estimated from subsamples may be biased, and held-out points that fall between centroids may be misassigned in ways that inflate ARI variance. Either cite a paper that uses this specific bootstrap ARI procedure (Hennig 2007? Fang & Wang 2012?) or add a brief justification for why nearest-centroid assignment is appropriate here.

---

## §6 Results

**[MAJOR] "Correctly separated" and "correctly partitioned" are teleological.**
These phrases appear in the cluster archetype discussion (and possibly the Discussion). There is no ground truth against which correctness can be measured — you defined the archetype by matching it to the literature after the fact. RSE reviewers are trained to flag this language in unsupervised learning papers. Replace with "consistent with documented cultivation conditions" or "matching the expected profile."

**[MAJOR] ARI=1.000 for Stack D is definitionally circular.**
The text explains this well in the body ("Stack D IS the reference"), but the figure and table still show ARI=1.000 as a data point. A reviewer scanning the figure will immediately write "authors claim ARI of 1.0 which is suspicious." Move the ARI comparison to C vs D (the meaningful comparison: 0.399 → 1.000) rather than plotting A vs B vs C vs D with D=1.000 as the endpoint. The figure as-is buries the meaningful comparison (60% reduction from removing EO) in a display that looks like you're claiming a perfect result.

**[MINOR] C0 SOC value (518 dg/kg) seems high relative to C1 (330 dg/kg) and C3 (426 dg/kg) but is never commented on.**
C0 has the highest SOC in the suitability zone. If C1 is the "prime" sub-cluster, and C0 has richer soil, what makes C1 prime rather than C0? The paper says C1 has "better pH" (5.96 vs 5.75) and "accessible gradient" (14.8° vs 19.5°), but C0's SOC advantage is never addressed. A reviewer will ask why SOC doesn't put C0 ahead of C1.

**[MINOR] Validation: "No enforcement parcels in cluster 3" is a tautological result.**
Cluster 3 is "data void/coast" — coastal/marine edge cells with incomplete environmental data. Of course there are no enforcement parcels there. Including this in the chi-square table and lift analysis adds nothing and dilutes the effect size interpretation. Either note it briefly and exclude it from the lift analysis, or address why it was included.

**[CRITICAL] Validation geography mismatch: chi-square is study-area-wide, parcels are Humboldt-only.**
The chi-square test uses all five cluster proportions computed across the full three-county study area (8,648 cells from Humboldt, Mendocino, AND Trinity), but the 91 enforcement parcels come exclusively from Humboldt County (via Humboldt parcel API). If Humboldt County has a different cluster composition than the full study area, the "expected" frequencies in the chi-square are biased. You're comparing Humboldt parcels against study-area-wide cluster baselines, not against Humboldt-specific cluster baselines. This is a methodological flaw that a reviewer will catch. The fix: compute expected frequencies from Humboldt County cells only, not the full study area. This may change the chi-square value and the lift estimates.

---

## §7 Discussion

**[CRITICAL] §7.1 states archetype emerged from "terrain, climate, and soil variation alone" — contradicts your own EO argument.**
The sentence "The archetype emerged from terrain, climate, and soil variation alone" appears in the Discussion (§7.1). This directly contradicts the central claim that EO (NDVI_std) contributed non-redundant structure. This error is presumably a holdover from an earlier draft. Either delete the sentence or change it to "terrain, climate, soil, and satellite-derived canopy structure."

**[MAJOR] Moran 2017 claim that his "sample is drawn almost entirely from terrain falling within our cluster 2" is asserted without evidence.**
This claim is the linchpin of the hierarchical filtering argument: if Moran's parcels are in your cluster 2, then of course social factors dominate within the biophysically constrained zone. But you haven't verified this. Did you check whether Moran's 99 sampled parcels (his study area is Humboldt County) spatially overlap your cluster 2? If you haven't checked, this is speculation. If you have, cite the verification method. Without this, a reviewer who has read Moran 2017 will immediately flag the unverified assertion.

**[MAJOR] The hierarchical filtering concept — the most interesting theoretical contribution — is invisible outside §7.3.**
It doesn't appear in the abstract, the introduction, or the conclusion. A reader who scans the abstract and conclusion will not know this argument exists. If you believe the hierarchical filtering framework is important (and it is — it's the best thing in the paper), put it in the abstract as a conceptual result: "We propose a two-scale hierarchical filtering model that reconciles landscape-level biophysical constraints with parcel-level social placement." This raises the paper's theoretical contribution from zero to visible.

**[MINOR] §7.4 "conflict-zone land use" application is unsupported speculation.**
The conclusion claims UTF generalizes to "conflict-zone land use." This is a significant claim with no support — not even a citation showing that EO can monitor conflict-zone agriculture. RSE reviewers will either ask for evidence or view this as overclaiming. Remove it or replace with "land cover monitoring in jurisdictions where administrative data is restricted or absent."

**[MINOR] §7.5 Limitations — "a 250m grid would better capture gradients" needs qualification.**
SoilGrids is already at 250m native resolution. You're already at 250m for soil. The 2km hex cell aggregates over it. A more precise statement: "A finer hex grid (e.g., 500m–1km cells) would reduce spatial averaging and better resolve the ridge-to-valley thermal gradients that govern frost risk."

**[MINOR] §7.3 "important implication for enforcement-based cannabis research more broadly" oversells 91 parcels from one county.**
Claiming broad methodological implications for an entire research subfield based on 91 enforcement records from Humboldt County alone is an overstatement. Soften: "This pattern suggests that enforcement-based proxies may be subject to systematic spatial bias; studies that use such data should account for the enforcement agency's jurisdictional mandate."

---

## Methods Architecture

**[MAJOR] No UTF framework diagram exists.**
The revision plan explicitly identified this as a minimum viable upgrade. A six-step framework with a named acronym (UTF) needs a schematic figure showing the pipeline: data sources → feature assembly → PCA → clustering → validation. RSE publishes methods papers that define frameworks; they universally include a framework diagram. Without it, the paper reads like a case study pipeline, not a generalizable method. This is the single highest-leverage addition.

**[MINOR] No discussion of potential dual-use or misuse of the framework.**
A paper that maps the biophysical envelope for illegal cultivation sites (pre-legalization, or in non-legalized jurisdictions) will draw editorial attention. The paper gestures at this in the data suppression discussion but doesn't address it head-on. A brief paragraph acknowledging the dual-use context and noting that the data sources used are all publicly available at coarser resolutions adds both intellectual honesty and preempts editorial hesitation.

---

## Statistics

**[MAJOR] Cramér's V application to a goodness-of-fit test is non-standard.**
Cramér's V is designed for contingency tables (two-way chi-square tests of association). You are running a one-way chi-square goodness-of-fit test (observed vs expected proportions). Applying V in this context is debatable — it's done, but not universally accepted. Either (a) justify the application explicitly, citing a source that uses V for GOF tests, or (b) switch to Cohen's w (which is the standard effect size for chi-square GOF), where `w = sqrt(chi2/n) = sqrt(40.3/91) = 0.666` — a large effect. Cohen's w is unambiguous in this context and easier to defend.

---

## Minor / Prose

**[MINOR] Cramér's V is reported as 0.33 in one place and 0.333 in others.** Pick one and be consistent. Recommend 0.33 throughout (two decimal places matches chi-square and p-value precision).

**[MINOR] "Demonstrating" is overused.** A quick grep will find it used four or more times in proximity. RSE prose should be more varied.

**[MINOR] C1 prime sub-cluster: the case for C1 over C3 is underdeveloped.** C3 has slightly better pH (6.04) and higher SOC. The paper says C1 is prime because of accessible slope and VPD, but doesn't compare these tradeoffs explicitly. One sentence quantifying the tradeoff ("C3's superior pH is offset by 9.4° steeper slopes and 363m higher elevation, constraining mechanized access and extending frost risk") would preempt reviewer questions.

---

## Summary Priority List

Fix before submission:
1. **CRITICAL** ✅ FIXED: Validation geography mismatch — Humboldt-corrected chi-square added (ML/05 cell 25). chi2=42.2, p=1.49e-08, V=0.341. Lift C2=3.34 (was 0.61). Paper fully updated.
2. **CRITICAL** ✅ FIXED: ndvi_std circularity acknowledged in §5.3 with Stack C ablation defense.
3. **CRITICAL** ✅ FIXED: "terrain, climate, and soil alone" → "terrain, climate, soil, and satellite-derived canopy structure features."
4. **MAJOR** ✅ FIXED: UTF framework diagram added as Figure 1 in Methods (img/utf_framework.png).
5. **MAJOR** ✅ FIXED: Moran 2017 claim softened to "likely drawn predominantly from terrain within the biophysically suitable envelope."
6. **MAJOR** ✅ FIXED: Cluster 3 / 8,648 cell count explained in §4 data assembly paragraph.
7. **MAJOR** ✅ FIXED: K=5 selection criterion — silhouette + elbow described in §5.2.
8. **MAJOR** ✅ FIXED: Feature weighting specified in §5.4 — StandardScaler then column-wise multiply by normalized importance weights.
9. **MAJOR** ✅ FIXED: Hierarchical filtering added to abstract. Conclusion has validation result + generalization paragraph.
10. **MAJOR** ✅ FIXED: VPD row changed to $\uparrow$ (directional) with $\dagger$ footnote.
11. **MAJOR** DEFERRED: Cramér's V vs Cohen's w — kept V=0.34 consistently. Methodological note in §5.5 (Effect size) cites the formula. Acceptable without change; if reviewer objects, switch to Cohen's w = 0.68.

Fix before final proofread:
- Remove "conflict-zone land use" or cite it
- Soften "important implication for enforcement-based cannabis research more broadly"
- Fix SOC advantage for C0 vs C1 — one sentence
- Consistent Cramér's V precision (0.33 everywhere)
- Cell count reconciliation (8,900 vs 8,648) — explicit note in Methods
- UNODC citation — verify it actually says what you claim
