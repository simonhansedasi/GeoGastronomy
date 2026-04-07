"""
Load RSU JSON files from data/rsu/ into RSU dataclass instances.
v0.3: metabolite profiles are per staple food, not per RSU.
Enforces strict empirical rule: null fields dropped, unknowns filtered.
"""

import json
import re
import dataclasses
from pathlib import Path

from rsu_schema import (
    RSU, Coordinates, Climate, Geology, Biodiversity, FunctionalGroupCounts,
    MetaboliteProfile, PrimaryMetabolites, FlavorBioactives, Terpenes,
    OrganicAcids, UmamiCompounds, FoodSystem, Culture, StapleFood
)

RSU_DIR = Path(__file__).resolve().parent.parent / "data" / "rsu"


def _filter_fields(cls, raw: dict) -> dict:
    """Return only keys valid on the dataclass, dropping unknown fields silently."""
    valid = {f.name for f in dataclasses.fields(cls)}
    return {k: v for k, v in raw.items() if k in valid and v is not None}


def _parse_numeric_range(value: str):
    """
    Extract (low, high) from strings like '5-25 g/100g' or '0.02-0.5 mg/L'.
    Handles ranges (X-Y) and single values (possibly negative, e.g. '-0.45').
    Returns None if no numeric range is parseable.
    """
    # Try explicit range first: two non-negative numbers separated by a dash/en-dash.
    # This avoids misreading "0.22-0.28" as (0.22, -0.28).
    range_match = re.search(r'(\d+\.?\d*)\s*[-\u2013]\s*(\d+\.?\d*)', value)
    if range_match:
        return float(range_match.group(1)), float(range_match.group(2))
    # Fall back to single number (may be negative, e.g. organic acid log values).
    single_match = re.search(r'[-+]?\d+\.?\d*', value)
    if single_match:
        v = float(single_match.group())
        return v, v
    return None


def _load_metabolite_profile(mp_raw: dict) -> MetaboliteProfile:
    return MetaboliteProfile(
        primary_metabolites=PrimaryMetabolites(**_filter_fields(PrimaryMetabolites, mp_raw.get("primary_metabolites", {}))),
        key_flavor_bioactives=FlavorBioactives(**_filter_fields(FlavorBioactives, mp_raw.get("key_flavor_bioactives", {}))),
        terpenes=Terpenes(**_filter_fields(Terpenes, mp_raw.get("terpenes", {}))),
        organic_acids=OrganicAcids(**_filter_fields(OrganicAcids, mp_raw.get("organic_acids", {}))),
        umami_compounds=UmamiCompounds(**_filter_fields(UmamiCompounds, mp_raw.get("umami_compounds", {}))),
    )


def _load_staple_food(fd: dict) -> StapleFood:
    mp_raw = fd.get("metabolite_profile", {})
    return StapleFood(
        name=fd["name"],
        macronutrient_category=fd["macronutrient_category"],
        fdc_search_term=fd.get("fdc_search_term"),
        fdc_id=fd.get("fdc_id"),
        metabolite_profile=_load_metabolite_profile(mp_raw),
        confirmed_absent=fd.get("confirmed_absent", []),
        feeding_type=fd.get("feeding_type"),
        notes=fd.get("notes", ""),
        data_sources=fd.get("data_sources", []),
    )


def load_rsu(path: Path) -> RSU:
    with open(path) as f:
        d = json.load(f)

    coords = Coordinates(**d["coordinates"])
    climate = Climate(**_filter_fields(Climate, d.get("climate", {})))
    geology = Geology(**_filter_fields(Geology, d.get("geology", {})))

    bio_raw = d.get("biodiversity", {})
    fgc = FunctionalGroupCounts(**_filter_fields(FunctionalGroupCounts, bio_raw.get("functional_group_counts", {})))
    biodiversity = Biodiversity(
        species_richness_index=bio_raw.get("species_richness_index"),
        functional_group_counts=fgc,
        endemic_species_fraction=bio_raw.get("endemic_species_fraction"),
    )

    staple_foods = [_load_staple_food(fd) for fd in d.get("staple_foods", [])]

    fs_raw = d.get("food_system", {})
    food_system = FoodSystem(
        dominant_staples=fs_raw.get("dominant_staples", []),
        known_processing_methods=fs_raw.get("known_processing_methods", []),
        fermentation_prevalence=fs_raw.get("fermentation_prevalence"),
    )

    culture = Culture(**_filter_fields(Culture, d.get("culture", {})))

    return RSU(
        region_id=d["region_id"],
        name=d["name"],
        coordinates=coords,
        climate=climate,
        geology=geology,
        biodiversity=biodiversity,
        staple_foods=staple_foods,
        absent_categories=d.get("absent_categories", []),
        food_system=food_system,
        culture=culture,
        notes=d.get("notes", ""),
    )


def load_all_rsus() -> list:
    rsus = []
    for path in sorted(RSU_DIR.glob("RSU-*.json")):
        rsus.append(load_rsu(path))
    return rsus


def parse_numeric_ranges(rsus: list) -> dict:
    """
    For each RSU and each staple food, parse numeric ranges from observed metabolite fields.
    Returns: {region_id: {food_name: {field: (low, high)}}}
    """
    result = {}
    for rsu in rsus:
        result[rsu.region_id] = {}
        for food in rsu.staple_foods:
            food_ranges = {}
            mp = food.metabolite_profile
            for cat_name in ["primary_metabolites", "key_flavor_bioactives", "terpenes", "organic_acids", "umami_compounds"]:
                cat = getattr(mp, cat_name)
                for fname, val in vars(cat).items():
                    if val is not None:
                        parsed = _parse_numeric_range(val)
                        if parsed is not None:
                            food_ranges[f"{cat_name}.{fname}"] = parsed
            if food_ranges:
                result[rsu.region_id][food.name] = food_ranges
    return result


def build_food_matrix(rsus: list) -> "pd.DataFrame":
    """
    Build a flat matrix: one row per (RSU, food), columns are metabolite fields.
    Values are midpoints of numeric ranges. None where unmeasured.
    Requires pandas.
    """
    import pandas as pd

    ranges = parse_numeric_ranges(rsus)
    rows = []
    for rsu in rsus:
        for food in rsu.staple_foods:
            food_ranges = ranges.get(rsu.region_id, {}).get(food.name, {})
            row = {
                "region_id": rsu.region_id,
                "rsu_name": rsu.name,
                "food_name": food.name,
                "category": food.macronutrient_category,
                "fdc_id": food.fdc_id,
                "n_confirmed_absent": len(food.confirmed_absent),
            }
            for field, (lo, hi) in food_ranges.items():
                row[field] = (lo + hi) / 2
            rows.append(row)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    rsus = load_all_rsus()
    print(f"Loaded {len(rsus)} RSUs")
    for rsu in rsus:
        obs = rsu.observed_metabolite_fields()
        total = sum(len(v) for v in obs.values())
        print(f"  {rsu.region_id} — {rsu.name}: {len(rsu.staple_foods)} foods, {total} observed metabolite fields")
        for food_name, fields in obs.items():
            if fields:
                print(f"    {food_name}: {fields}")
