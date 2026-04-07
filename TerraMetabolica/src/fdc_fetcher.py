"""
USDA FoodData Central API fetcher for TerraMetabolica.

Usage:
    export FDC_API_KEY=your_key_here   # free at https://fdc.nal.usda.gov/api-key-signup
    python fdc_fetcher.py              # fetches all foods defined in RSU JSONs

Caches raw API responses to data/raw/fdc/{fdc_id}.json so the API is only hit once per food.
Writes fdc_id and extracted metabolite values back into each RSU JSON.

Nutrient IDs used:
    1003  Protein (g)
    1004  Total lipid / fat (g)
    1005  Carbohydrate, by difference (g)
    1079  Fiber, total dietary (g)
    1008  Energy (kcal)
    2000  Sugars, total (g)
    1087  Calcium (mg)
    1089  Iron (mg)
    1091  Phosphorus (mg)
    1093  Sodium (mg)
    1258  Fatty acids, total saturated (g)
    1292  Fatty acids, total monounsaturated (g)
    1293  Fatty acids, total polyunsaturated (g)
    2047  Energy (kcal) - ATWATER
"""

import json
import os
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import HTTPError

BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# Nutrient IDs to extract
MACRO_NUTRIENT_IDS = {
    1003: "protein_g",
    1004: "fat_g",
    1005: "carb_g",
    1079: "fiber_g",
    1008: "energy_kcal",
    2000: "sugars_g",
    1258: "saturated_fat_g",
    1292: "monounsaturated_fat_g",
    1293: "polyunsaturated_fat_g",
}

# Preferred data types in priority order
DATA_TYPE_PRIORITY = ["Foundation", "SR Legacy", "Survey (FNDDS)", "Branded"]

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "fdc"
RSU_DIR = Path(__file__).resolve().parent.parent / "data" / "rsu"


def _api_key() -> str:
    key = os.environ.get("FDC_API_KEY", "DEMO_KEY")
    if key == "DEMO_KEY":
        print("Warning: using DEMO_KEY (30 req/hour limit). Set FDC_API_KEY env var for full access.")
    return key


def _get(url: str) -> dict:
    req = Request(url, headers={"User-Agent": "TerraMetabolica/0.3"})
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def search_food(query: str, api_key: str) -> list:
    """Search FDC by query string. Returns list of food hits sorted by data type priority."""
    params = urlencode({
        "query": query,
        "api_key": api_key,
        "dataType": "Foundation,SR Legacy",
        "pageSize": 10,
    })
    url = f"{BASE_URL}/foods/search?{params}"
    try:
        data = _get(url)
    except HTTPError as e:
        print(f"  HTTP {e.code} searching '{query}'")
        return []

    foods = data.get("foods", [])

    def priority(f):
        dt = f.get("dataType", "")
        try:
            return DATA_TYPE_PRIORITY.index(dt)
        except ValueError:
            return len(DATA_TYPE_PRIORITY)

    return sorted(foods, key=priority)


def fetch_food(fdc_id: int, api_key: str) -> dict:
    """Fetch full food detail by FDC ID. Uses local cache if available."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{fdc_id}.json"

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    url = f"{BASE_URL}/food/{fdc_id}?api_key={api_key}"
    try:
        data = _get(url)
    except HTTPError as e:
        print(f"  HTTP {e.code} fetching FDC ID {fdc_id}")
        return {}

    with open(cache_path, "w") as f:
        json.dump(data, f, indent=2)

    return data


def extract_macros(food_data: dict) -> dict:
    """
    Extract macro nutrients from a full FDC food record.
    Returns dict of {field_name: value_per_100g}.
    """
    nutrients = food_data.get("foodNutrients", [])
    result = {}

    for n in nutrients:
        # Foundation and SR Legacy use 'nutrient' sub-dict
        nutrient = n.get("nutrient", n)
        nid = nutrient.get("id") or n.get("nutrientId")
        if nid in MACRO_NUTRIENT_IDS:
            amount = n.get("amount") or n.get("value")
            if amount is not None:
                result[MACRO_NUTRIENT_IDS[nid]] = round(float(amount), 3)

    return result


def fetch_rsu_foods(rsu_path: Path, api_key: str, delay: float = 1.0) -> None:
    """
    For a single RSU JSON:
    - For each staple food without an fdc_id: search FDC, pick best match, set fdc_id
    - Fetch full food data, extract macros
    - Write macros into the food's metabolite_profile.primary_metabolites
    - Save updated RSU JSON
    """
    with open(rsu_path) as f:
        rsu = json.load(f)

    modified = False
    for food in rsu.get("staple_foods", []):
        name = food["name"]
        fdc_id = food.get("fdc_id")

        if fdc_id is None:
            search_term = food.get("fdc_search_term") or name
            print(f"  Searching: '{search_term}'")
            hits = search_food(search_term, api_key)
            time.sleep(delay)

            if not hits:
                print(f"    No results for '{search_term}' — skipping")
                continue

            best = hits[0]
            fdc_id = best["fdcId"]
            food["fdc_id"] = fdc_id
            print(f"    -> FDC ID {fdc_id}: {best.get('description', '')} [{best.get('dataType', '')}]")
            modified = True

        # Fetch full record
        food_data = fetch_food(fdc_id, api_key)
        time.sleep(delay)

        if not food_data:
            continue

        macros = extract_macros(food_data)
        if not macros:
            continue

        # Write macros into metabolite_profile.primary_metabolites
        mp = food.setdefault("metabolite_profile", {})
        pm = mp.setdefault("primary_metabolites", {})

        field_map = {
            "protein_g": "protein_content",
            "fat_g": "lipid_content",
            "carb_g": "starch_content",   # approximation; carb includes sugars
            "fiber_g": "fiber_content",
            "energy_kcal": "energy_kcal",
            "sugars_g": "glucose_concentration",
            "saturated_fat_g": "saturated_fat_g",
        }

        for src_key, dst_key in field_map.items():
            if src_key in macros and dst_key not in pm:
                pm[dst_key] = f"{macros[src_key]} g/100g [USDA FDC {fdc_id}]"

        food["metabolite_profile"]["primary_metabolites"] = pm
        food["metabolite_profile"]["_fdc_macros_raw"] = macros
        modified = True
        print(f"    Macros written: {list(macros.keys())}")

    if modified:
        with open(rsu_path, "w") as f:
            json.dump(rsu, f, indent=2)
        print(f"  Saved {rsu_path.name}")


def fetch_all(delay: float = 1.5) -> None:
    """Fetch FDC data for all RSU JSON files."""
    api_key = _api_key()
    paths = sorted(RSU_DIR.glob("RSU-*.json"))
    print(f"Processing {len(paths)} RSUs...")

    for path in paths:
        print(f"\n{path.name}")
        fetch_rsu_foods(path, api_key, delay=delay)


if __name__ == "__main__":
    fetch_all()
