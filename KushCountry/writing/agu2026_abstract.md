# AGU Fall Meeting 2026 — Abstract Draft

**Deadline:** Wednesday, 5 August 2026, 23:59 EDT
**Suggested section:** GC105 — Remote Sensing for Sustainable Agriculture (retargeted from Biogeosciences 2026-07-09; GC002 "Food System Resilience" ruled out — cannabis isn't food and the paper is cross-sectional, not a resilience/dynamics study)

---

## Title

Unsupervised Terrain Fingerprinting for Data-Scarce Land-Use Suitability Mapping: A Cannabis Cultivation Case Study in California's Emerald Triangle

*(150 characters — well under the 300-character limit; can be shortened further if a session calls for it)*

## Authors

Simon-Hans Edasi *(add affiliation, co-authors if any)*

## Abstract body

*(1,907 characters excluding spaces — under the 2,000-character limit, but only ~93 characters of slack left; trim before adding anything else)*

Ground-truth cultivation locations are frequently unavailable for regulatory, security, or privacy reasons, limiting standard supervised land-use suitability mapping. We present Unsupervised Terrain Fingerprinting (UTF), a six-step framework that recovers suitability archetypes from unlabeled terrain, climate, soil, and remotely sensed vegetation data alone, demonstrated in California's Emerald Triangle (Humboldt, Mendocino, Trinity Counties), where the state Department of Cannabis Control withholds all cultivator coordinates by policy.

We assembled 23 features (terrain, Daymet climate, SoilGrids soil chemistry, Sentinel-2 NDVI heterogeneity) across 8,900 2-km hexagonal cells and applied PCA (PC1+PC2 = 71.5% variance) followed by k-means clustering (K=7). One cluster (22.2% of the study area) self-organized into a coherent, agronomically plausible archetype — mid-elevation (527 m), warm-dry growing season (GDD 1,395; VPD 1,568 Pa), Mediterranean precipitation (1,102 mm/yr) — that excludes the coastal fog belt entirely. Within this cluster, a random forest identifies slope (permutation importance 0.59) and soil pH (0.39) as the dominant drivers of canopy heterogeneity, and sub-clustering isolates a 714-cell prime stratum.

Satellite-derived NDVI heterogeneity contributes non-redundant structure beyond terrain, climate, and soil alone: an ablation series (terrain → +climate → +soil → +EO) shows the remotely sensed layer completing the partition geometry that ground-based variables cannot recover on their own.

Critically, the archetype is independently validated against 91 geocoded enforcement parcels drawn from state water-quality violation records: the suitability cluster covers 2.9% of Humboldt County terrain but accounts for 9.9% of enforcement parcels (χ²(6)=36.6, p=2.1×10⁻⁶, Cramér's V=0.26, lift=3.41). The archetype is robust to cluster count (K=4–7) and stable under bootstrap resampling (mean ARI=0.974, n=50).

UTF generalizes beyond cannabis to any specialty crop or land use where cultivation locations are suppressed, unmapped, or too sparse for supervised methods — offering a route to suitability mapping wherever ground truth cannot be observed directly.

---

## Notes

- Pulled directly from `writing/paper.tex` results (ML/01–06) — no numbers invented here; cross-check against the paper before submitting in case anything shifted since 2026-04-17.
- Retargeted to GC105 2026-07-09 (JavaScript went to GC002; KushCountry doesn't fit there — cannabis isn't food, and the paper is a static suitability snapshot, not a resilience/dynamics study). GC105 organizers (Wang, Wang, Deines, Guan) are remote-sensing-for-agriculture people, so the new EO-ablation sentence gives the satellite layer explicit standing rather than burying it as 1-of-23 features — check this reads naturally, it was added after the fact.
- Greek/special characters (χ², ×10⁻⁶, é, ²) are fine in AGU's submission form; if the portal chokes on Unicode, the plain-ASCII fallback is `chi-square`, `x10^-6`, `Cramer's V`.
- An optional single JPG/PNG figure can accompany the abstract — `img/ML02_suitability_zone.png` (the two-panel cluster map) is the natural choice; `img/ML06_ablation.png` (if it exists) would tie directly to the new EO-ablation sentence.
- If you need to cut ~100+ chars for further edits, the "sub-clustering isolates a 714-cell prime stratum" clause is the safest trim — it's a secondary result, not part of the core validation story.
