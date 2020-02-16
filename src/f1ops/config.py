"""Configuration and constants for F1Ops."""

import os
from pathlib import Path
from typing import Dict, List

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CALENDARS_DIR = DATA_DIR / "calendars"
GEO_DIR = DATA_DIR / "geo"
SAMPLES_DIR = DATA_DIR / "samples"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

# Ensure directories exist
ARTIFACTS_DIR.mkdir(exist_ok=True)

# European countries for filtering
EUROPEAN_COUNTRIES: List[str] = [
    "Austria",
    "Azerbaijan",
    "Belgium",
    "France",
    "Germany",
    "Hungary",
    "Italy",
    "Monaco",
    "Netherlands",
    "Spain",
    "United Kingdom",
    "Russia",
    "Turkey",
]

# Default cost model parameters
DEFAULT_COST_PARAMS: Dict[str, float] = {
    "num_trucks": 8.0,
    "load_weight_kg": 15000.0,
    "fuel_consumption_l_per_100km": 30.0,
    "fuel_price_eur_per_l": 1.50,
    "driver_wage_eur_per_hour": 35.0,
    "avg_speed_kmh": 80.0,
    "toll_eur_per_km": 0.25,
    "fixed_cost_per_leg_eur": 500.0,
}

# Default emissions parameters (grams CO2e per km)
DEFAULT_EMISSIONS_PARAMS: Dict[str, float] = {
    "road_freight_g_co2e_per_km": 850.0,  # Per truck
    "air_freight_g_co2e_per_tonne_km": 500.0,
    "air_freight_fraction": 0.0,  # Default: all road
}

# OSRM configuration
OSRM_BASE_URL = os.getenv("OSRM_BASE_URL", "http://router.project-osrm.org")
USE_OSRM = os.getenv("USE_OSRM", "false").lower() == "true"

# Optimization parameters
OPTIMIZATION_PARAMS: Dict[str, float] = {
    "max_driver_hours_per_day": 9.0,
    "max_consecutive_driving_hours": 4.5,
    "min_rest_hours": 11.0,
    "max_weekly_driving_hours": 56.0,
}

# Available seasons
AVAILABLE_SEASONS = list(range(2010, 2025))

# Team freight profile defaults
DEFAULT_TEAM_PROFILE: Dict[str, float] = {
    "total_freight_tonnes": 120.0,
    "num_personnel": 60,
    "garage_equipment_tonnes": 40.0,
    "spare_parts_tonnes": 30.0,
    "hospitality_tonnes": 50.0,
}
