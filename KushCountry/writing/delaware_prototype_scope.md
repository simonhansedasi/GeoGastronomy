# Delaware outdoor-cultivation siting prototype: scope (2026-10-07)

## Question
Which Delaware parcels could legally host an outdoor cultivation facility at each license tier, and which of those rank best on water, flood, soil and climate? Output is a ranked parcel list and a map, built for a licensee or applicant.

## Gate 0: is there anyone to build it for? (half a day, before any code)
1. OMC (omc.delaware.gov): are vacant cultivation licenses open, when, and who holds the 60? Any published premises addresses?
2. Read the zoning code of New Castle, Kent and Sussex counties and the big municipalities (Dover is known: cultivation allowed in M, IPM and A districts, 750 ft from residential, schools, hospitals, daycares). Question: is OUTDOOR cultivation allowed, or only enclosed/indoor? The failed SB 75 text talked about "indoor, fully enclosed" facilities, which suggests local codes may bar outdoor. If all three counties bar outdoor, stop: the state's acreage tiers are moot.
3. If gate 0 passes, name two or three people to show it to (applicants, existing licensees).

## Why this is not a Merascope site_type reweight
`site_type` (BESS) only reweights the existing 22 indicators on a ZCTA/fishnet grid. Delaware's legality is decided at the parcel level by local zoning and buffers, so this needs new parcel data. Precedent: `merascope/parcels/` (grant_county.py, tri_cities.py) already does county-level parcel work. Build outside the live Merascope repo (see the federal-funding and payments question), in `~/coding/de_siting/`, borrowing script patterns.

## Layers

Legal screen (hard filters):
| Layer | Source | Note |
|---|---|---|
| Parcels | DE FirstMap statewide parcels (de-firstmap-delaware.hub.arcgis.com) | Can lag county records; cross-check New Castle and Kent hubs |
| Zoning | New Castle hub, Kent hub; Sussex: not found, check Sussex GIS or FirstMap | Sussex is the gap |
| Sensitive uses (schools, daycare, hospitals, churches, treatment) | FirstMap facility layers, else OSM | Buffers per jurisdiction |
| Local rule table | Hand-built per county/municipality from codes: allowed districts, buffer ft, outdoor yes/no | Dover known; NCC and Sussex cultivation buffers not found (their known buffers are retail) |
| Parcel acreage vs tier | Computed | Tier 1 <=1 ac, T2 1.1-2.5, T3 2.6-5, T4 5.1-7.5 |
| Floodplain | FEMA NFHL | Exclude or flag |

Suitability (ranking, soft):
| Layer | Source | Note |
|---|---|---|
| GDD (base 10C), humidity/VPD, growing-season length | gridMET or Daymet | Mold, not GDD, dominates in humid Delaware; weight accordingly |
| Soil (drainage, pH, texture) | SSURGO | Via requests, no GDAL |
| Water stress | existing `merascope/data/DE/` outputs | Reuse |
| Slope | USGS DEM via np.gradient | Minor in flat Delaware |
| Road access | TIGER roads | Reuse KushCountry accessibility code |

## Output
- GeoJSON of eligible parcels with tier, acreage, jurisdiction, rule citation, score and per-layer reasons.
- One static Leaflet page (reuse the GrapeExpectations map pattern) plus CSV.
- Every parcel carries "why legal": the zoning district and the rule that admits it. Keep this visible, it is the credibility.

## Steps
1. Gate 0 (above). ~0.5 day.
2. Parcels + zoning + sensitive-use buffers for the one county that passes gate 0. ~1 day.
3. Local rule table for that county, hand-checked against code. ~0.5 day.
4. Suitability layers and score. ~1 day.
5. Map, CSV, one-page method note. ~0.5-1 day.
6. Extend to the other two counties only if step 5 gets a real reaction.
Total about 4 days for one county.

## Known unknowns
- Whether outdoor is permitted locally (gate 0, kill criterion).
- NCC and Sussex cultivation buffers, Sussex zoning download.
- Whether municipalities add their own bans (several reportedly restrict retail; check cultivation).
- Delaware has only 60 licenses: the buyer pool is small even if everything works.
- No validation data. Legal screen is checkable against code; the suitability rank is not. Say so on the page.
- Federal funding and payment-processor question for cannabis ancillary software, unresolved.

## Not doing
No clustering, no KushCountry K-means, no paper, no production Merascope integration, no pricing.

## Gate 0 result (2026-10-07): NOT PASSED, leaning fail

Buyer side
- Lottery ran late 2024 (Aug 19-Sep 30 window, 1,269 applications): 60 cultivation licenses, 125 total. Winners hold conditional licenses, about 18 months to open, so many have already chosen sites. Some micro-cultivation licenses (New Castle) went vacant and were reassigned to Kent/Sussex. OMC said vacant-license applications would open in 2025; no confirmation found that a window opened. Licensee list/premises not found; OMC Reports page not checked.

Outdoor, by jurisdiction
- Dover (primary text read, Ordinance 2024-29): cultivation allowed in M, IPM and A zones, but every standard is written around "the building footprint within which a cultivation facility is to be located", 750 ft from residential zones, K-12, hospitals, colleges, daycare, treatment, and odor must be undetectable "outside the building". Reads as indoor in practice, even in the A zone. Not an explicit outdoor ban.
- Sussex: original ordinance (No. 3016, May 2024, per news reports, text not read) allows cultivation by right in AR-1, C-1, CR-2, C-3, LI, LI-2 but reportedly requires 3 miles from schools, churches, rehab centers and municipal boundaries. The Nov 2025 amendment cut the municipal distance to half a mile for RETAIL; whether cultivation changed is unconfirmed. If 3 miles still applies to cultivation, almost no Sussex land qualifies. The Sussex PDF the fetch returned (o2656) was an unrelated coastal-area ordinance, so the cultivation text is still unread.
- New Castle: Ordinance 24-138 (final form passed Dec 2024). Text fetch blocked (403). Outdoor/district rules unconfirmed.
- Kent: no cannabis cultivation provision found in searches; ecode360 Chapter 205 (zoning) not read.

Verdict: no jurisdiction confirmed to allow outdoor growing, one (Dover) effectively indoor, one (Sussex) has distances that may exclude nearly all land. State acreage tiers exist on paper but local codes look written for enclosed buildings.

Remaining to close gate 0 (about 1 hour): read primary text of Sussex Ord. 3016 and its 2025 amendment, NCC UDC cannabis sections (download the PDF by hand, WebFetch is blocked), Kent ecode360 Chapter 205 for "marijuana". If none allows outdoor, stop.

## CORRECTION (2026-10-07, later): Sussex primary text read, gate 0 verdict for Sussex reversed

Read Sussex Ordinance 3016 (May 14, 2024) and 4025 (Nov 18, 2025) from the county PDFs (scanned, read as images). The news reports above were wrong on scope:
- The 3-mile buffers (s.115-194.6, amended as 115-194.7) apply ONLY to Retail Marijuana Stores: municipal boundary, other retail stores, church/school/college/treatment facility. Cultivation, manufacturing and testing have NO county distance rules.
- Cultivation is a permitted use (no hearing) in AR-1, C-1, CR-1, C-3, LI-1, LI-2, HI-1 (per the preamble). Article-to-district mapping not yet verified. Table IV also lists cultivation as P in C-3.
- Preamble: facilities "are generally conducted indoors", but nothing in the ordinance requires indoor or bans outdoor. AR-1 is allowed because "the cultivation of marijuana is not entirely unlike the propagation of other crops". Commercial greenhouse already sits in the same agricultural-uses list.
- Municipalities in Sussex may prohibit cultivation (Title 4 s.1351(a)); many have. Unincorporated land is county jurisdiction, where the ordinance above governs.
- Still unchecked: Delaware OMC regulations on outdoor cultivation and any state-level buffers; per-parcel zoning; the Sussex zoning layer.
So Sussex County may actually be open for outdoor cultivation in AR-1. The gate verdict for Dover and New Castle stands (not read for NCC/Kent). Buyer problem (60 licenses, lottery done late 2024) is unchanged.
