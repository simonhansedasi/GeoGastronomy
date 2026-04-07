"""
RSU (Region Sample Unit) schema for TerraMetabolica v0.3.

Metabolite profiles are now attached to individual staple foods, not the RSU as a whole.
Each RSU selects 4-5 native staple foods covering macronutrient categories:
  carb | fat | protein | aromatic | fermented

confirmed_absent lists metabolite fields that are genuinely absent from a food
(not just unmeasured). Absence is real data — it distinguishes from unknown.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Coordinates:
    lat: float
    lon: float
    altitude_m: Optional[float] = None   # metres above sea level — key for altitude gradient experiments


@dataclass
class Climate:
    temperature_mean: Optional[float] = None
    temperature_seasonality: Optional[float] = None
    precipitation_mean: Optional[float] = None
    precipitation_seasonality: Optional[float] = None


@dataclass
class Geology:
    parent_material: Optional[str] = None   # volcanic | sedimentary | metamorphic | alluvial
    soil_pH: Optional[float] = None
    soil_texture: Optional[str] = None      # sand | loam | clay
    drainage_class: Optional[str] = None    # low | medium | high


@dataclass
class FunctionalGroupCounts:
    fruiting_species: Optional[float] = None
    tuber_species: Optional[float] = None
    aromatic_species: Optional[float] = None
    fermentable_species: Optional[float] = None


@dataclass
class Biodiversity:
    species_richness_index: Optional[float] = None
    functional_group_counts: FunctionalGroupCounts = field(default_factory=FunctionalGroupCounts)
    endemic_species_fraction: Optional[float] = None


@dataclass
class PrimaryMetabolites:
    glucose_concentration: Optional[str] = None
    fructose_concentration: Optional[str] = None
    sucrose_concentration: Optional[str] = None
    starch_content: Optional[str] = None
    lipid_content: Optional[str] = None
    protein_content: Optional[str] = None
    amino_acid_content: Optional[str] = None
    ascorbic_acid: Optional[str] = None       # vitamin C — responsive to altitude and UV
    oleic_acid: Optional[str] = None          # % of total fatty acids — terroir signal in olive
    linoleic_acid: Optional[str] = None       # % of total fatty acids — climate sensitive
    lauric_acid: Optional[str] = None         # C12:0 saturated — dominant in coconut and palm kernel oil
    myristic_acid: Optional[str] = None       # C14:0 saturated — characteristic of coconut oil
    stearic_acid: Optional[str] = None        # C18:0 saturated — dominant in shea butter and cocoa butter
    palmitic_acid: Optional[str] = None       # C16:0 saturated — palm oil, lard, dairy fat
    palmitoleic_acid: Optional[str] = None    # C16:1 monounsaturated — macadamia, sea buckthorn; terroir-sensitive
    eicosenoic_acid: Optional[str] = None     # C20:1 monounsaturated — mustard oil, camelina


@dataclass
class FlavorBioactives:
    caffeine_concentration: Optional[str] = None
    theobromine_concentration: Optional[str] = None
    capsaicinoids: Optional[str] = None
    isothiocyanates: Optional[str] = None
    tannin_content: Optional[str] = None
    polyphenol_content: Optional[str] = None  # total polyphenols — strong water-stress / climate signal
    hydroxytyrosol: Optional[str] = None      # olive-specific antioxidant — location sensitive
    tocopherol_content: Optional[str] = None  # vitamin E — varies with growing conditions
    sesamol: Optional[str] = None             # sesame lignan antioxidant — UV and stress responsive
    conjugated_linoleic_acid: Optional[str] = None  # CLA — grass-fed dairy biomarker; diet-terroir signal


@dataclass
class Terpenes:
    limonene: Optional[str] = None
    myrcene: Optional[str] = None
    pinene: Optional[str] = None
    linalool: Optional[str] = None


@dataclass
class OrganicAcids:
    lactic_acid: Optional[str] = None
    acetic_acid: Optional[str] = None
    citric_acid: Optional[str] = None
    malic_acid: Optional[str] = None


@dataclass
class UmamiCompounds:
    glutamate: Optional[str] = None
    inosinate: Optional[str] = None
    guanylate: Optional[str] = None


@dataclass
class MetaboliteProfile:
    primary_metabolites: PrimaryMetabolites = field(default_factory=PrimaryMetabolites)
    key_flavor_bioactives: FlavorBioactives = field(default_factory=FlavorBioactives)
    terpenes: Terpenes = field(default_factory=Terpenes)
    organic_acids: OrganicAcids = field(default_factory=OrganicAcids)
    umami_compounds: UmamiCompounds = field(default_factory=UmamiCompounds)

    def observed_fields(self) -> list:
        """Flat list of field names that have measured values (not None)."""
        observed = []
        for cat_name in ["primary_metabolites", "key_flavor_bioactives", "terpenes", "organic_acids", "umami_compounds"]:
            cat = getattr(self, cat_name)
            for fname, val in vars(cat).items():
                if val is not None:
                    observed.append(f"{cat_name}.{fname}")
        return observed


@dataclass
class StapleFood:
    name: str
    macronutrient_category: str      # carb | fat | protein | aromatic | fermented
    fdc_search_term: Optional[str] = None   # search string for USDA FDC API
    fdc_id: Optional[int] = None            # populated by fdc_fetcher after search
    metabolite_profile: MetaboliteProfile = field(default_factory=MetaboliteProfile)
    confirmed_absent: list = field(default_factory=list)  # fields genuinely absent (not just unmeasured)
    cultivar: Optional[str] = None          # specific variety — required for natural experiment validity
    natural_experiment: list = field(default_factory=list)  # RSU IDs growing the same cultivar for comparison
    feeding_type: Optional[str] = None      # for animal products: grass-fed | mixed-feed | grain-fed | wild
    notes: str = ""
    data_sources: list = field(default_factory=list)


@dataclass
class FoodSystem:
    dominant_staples: list = field(default_factory=list)
    known_processing_methods: list = field(default_factory=list)
    fermentation_prevalence: Optional[float] = None


@dataclass
class Culture:
    agricultural_intensification_index: Optional[float] = None
    industrial_processing_index: Optional[float] = None


@dataclass
class RSU:
    region_id: str
    name: str
    coordinates: Coordinates
    climate: Climate = field(default_factory=Climate)
    geology: Geology = field(default_factory=Geology)
    biodiversity: Biodiversity = field(default_factory=Biodiversity)
    staple_foods: list = field(default_factory=list)   # list of StapleFood
    absent_categories: list = field(default_factory=list)  # macronutrient categories confirmed absent
    food_system: FoodSystem = field(default_factory=FoodSystem)
    culture: Culture = field(default_factory=Culture)
    notes: str = ""

    def foods_by_category(self) -> dict:
        return {f.macronutrient_category: f for f in self.staple_foods}

    def observed_metabolite_fields(self) -> dict:
        """Per-food observed field names. {food_name: [field, ...]}"""
        return {f.name: f.metabolite_profile.observed_fields() for f in self.staple_foods}
