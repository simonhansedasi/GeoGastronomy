# Kush Country — Reframing Notes
## UTF-First Restructuring

---

## Core Diagnosis

The paper currently reads as a **cannabis study with a methods contribution**.
The science supports it reading as a **methods paper with cannabis as its hardest test case**.

The fix is structural, not substantive. The results don't change. The order in which the
reader encounters the framing does.

---

## Abstract

### Problem with current version
- Opens with the labeling problem (good)
- Narrows immediately to cannabis / DCC suppression (too early — reads as a cannabis paper)
- UTF is not named until the final sentence
- Generalizability claim is buried

### Suggested rewrite arc

**Sentence 1–2:** Name and define UTF upfront.
> "We introduce Unsupervised Terrain Fingerprinting (UTF), a framework for recovering
> specialty crop suitability archetypes from environmental data alone when labeled
> cultivation locations are unavailable or suppressed. UTF requires no observed farm
> locations at any stage: landscape archetypes are derived from terrain, climate, soil,
> and satellite-derived canopy structure, and matched to known agronomic envelopes
> from the literature."

**Sentence 3–4:** Motivate with the hardest test case.
> "Outdoor cannabis in California's Emerald Triangle presents the sharpest instance of
> this problem: the Department of Cannabis Control deliberately suppresses all spatial
> information for licensed cultivators, making supervised approaches structurally
> infeasible."

**Sentences 5–end:** Results as UTF demonstration, not cannabis findings.
- The clustering result, within-zone regression, validation lift — all framed as
  UTF performing on a suppressed-label problem, not as findings about cannabis per se.

**Final sentence:** Generalizability claim moves here from conclusion.
> "UTF generalizes to any specialty crop with a sufficiently constrained environmental
> niche for which labeled cultivation locations are unavailable or suppressed."

---

## Introduction

### Problem with current structure
- §1 paragraph 1: labeling problem (good opening)
- §1 paragraph 2: pivots immediately to California cannabis / DCC — UTF not yet introduced
- UTF framework not named or explained until halfway through §1
- Hierarchical filtering model gestured at in §2.5, briefly in §5.2, fully articulated
  only in §7.4 — the paper's most distinctive conceptual claim arrives very late

### Suggested restructuring

**Paragraph 1 — General problem (keep mostly as-is)**
Suitability modeling requires labels. Labels are unavailable across a growing range of
agricultural and regulatory contexts. This is the setup. Keep it broad.

**Paragraph 2 — Introduce UTF as the response (currently missing)**
This paragraph does not exist in the current draft and needs to be written.
UTF should be named here, defined in one sentence, and its core logic stated:
environmental fingerprinting + unsupervised archetype discovery + agronomic
literature matching = no labels needed.

**Paragraph 3 — Cannabis as the test case (currently paragraph 2)**
DCC suppression, Emerald Triangle, why this is the hardest version of the problem.
This becomes the *motivation* for needing UTF rather than the framing of the whole paper.

**Paragraph 4 — Preview the hierarchical filtering payoff (currently §7.4 only)**
One paragraph here gesturing at the two-scale model — biophysical envelope at
landscape scale, social/economic filtering at parcel scale — gives reviewers a
conceptual anchor and makes the Moran (2017) reconciliation land with more force
when it reappears in the discussion.

**Paragraph 5 — Three contributions (keep as-is, reorder if needed)**
With the UTF framing established, the three contributions read as UTF contributions,
not cannabis contributions.

---

## Discussion

### §7.1
Currently titled "Unsupervised Recovery of a Known Archetype" — this is fine but
could be sharpened to "UTF Recovers a Known Archetype Without Labeled Input" to
keep the method name active throughout.

### §7.4 Hierarchical Filtering
This is the paper's best conceptual contribution and it arrives too late. The
introduction rewrite above partially addresses this, but §7.4 itself could open
with a stronger callback:
> "The two-scale hierarchical filtering model previewed in the introduction is
> directly confirmed by the relationship between our landscape-level result and
> Moran's [11] parcel-level findings."

### §7.5 Data Suppression
Currently frames UTF generalizability as a forward-looking claim. Worth adding
one sentence explicitly connecting to the Hawaiian specialty coffee context as a
parallel application — different crop, different regulatory environment, same
structural problem of constrained environmental niche + data limitations.
(Especially relevant given the companion paper.)

---

## Validation Language (§7.3)

Current framing reads slightly defensive around the enforcement bias issue.
Suggested reframe: make the bias directionality explicit and use it to strengthen
rather than hedge the result.

> "RWQCB enforcement in remote interior terrain is likely undercounted relative to
> accessible lowland sites, due to complaint-driven triggers and access constraints.
> Under this bias, the observed lift of 3.41 in cluster 0 is a conservative lower bound
> on the true concentration of cultivation in the UTF suitability zone."

---

## NDVIstd Circularity (§5.3)

The current hedge is methodologically correct but buried. The Stack C ablation result
— cannabis archetype recoverable at 4/4 criteria without any EO input — should be
**flagged in the abstract or introduction** as a pre-registered robustness check, not
only disclosed in the methods. This defuses the circularity concern before reviewers
raise it.

---

## Summary of Changes Required

| Location | Type | Priority |
|---|---|---|
| Abstract sentences 1–4 | Rewrite | High |
| Introduction paragraph 2 | Write from scratch | High |
| Introduction paragraph 3 | Reorder / reframe | High |
| Introduction paragraph 4 | Write from scratch (hierarchical filtering preview) | Medium |
| §5.3 circularity hedge | Move forward / flag earlier | Medium |
| §7.1 title | Minor reword | Low |
| §7.3 enforcement bias | Reframe as conservative bound | Medium |
| §7.4 opening sentence | Add callback to introduction | Low |
| §7.5 generalizability | Add one sentence on coffee companion paper | Low |

---

*Notes generated from editorial review, April 2026.*
