"""Emissions modeling for F1 logistics."""

from typing import Dict

from f1ops.config import DEFAULT_EMISSIONS_PARAMS
from f1ops.data_models import EmissionsBreakdown, Leg


def calculate_leg_emissions(
    leg: Leg, num_trucks: int = 8, freight_tonnes: float = 120.0, params: Dict[str, float] = None
) -> EmissionsBreakdown:
    """
    Calculate emissions breakdown for a single leg.

    Args:
        leg: Travel leg
        num_trucks: Number of trucks
        freight_tonnes: Total freight weight
        params: Emissions parameters (uses defaults if None)

    Returns:
        EmissionsBreakdown with road and air emissions
    """
    if params is None:
        params = DEFAULT_EMISSIONS_PARAMS.copy()

    distance_km = leg.distance_km

    # Road freight emissions
    road_g_co2e_per_km = params["road_freight_g_co2e_per_km"]
    road_co2e_g = road_g_co2e_per_km * distance_km * num_trucks
    road_co2e_kg = road_co2e_g / 1000.0

    # Air freight emissions (if any portion is shipped by air)
    air_fraction = params["air_freight_fraction"]
    air_co2e_kg = 0.0

    if air_fraction > 0:
        air_freight_tonnes = freight_tonnes * air_fraction
        air_g_co2e_per_tonne_km = params["air_freight_g_co2e_per_tonne_km"]
        air_co2e_g = air_g_co2e_per_tonne_km * distance_km * air_freight_tonnes
        air_co2e_kg = air_co2e_g / 1000.0

        # Reduce road emissions proportionally
        road_co2e_kg *= 1.0 - air_fraction

    return EmissionsBreakdown(
        road_co2e_kg=round(road_co2e_kg, 2), air_co2e_kg=round(air_co2e_kg, 2)
    )


def calculate_season_emissions(
    legs: list, num_trucks: int = 8, freight_tonnes: float = 120.0, params: Dict[str, float] = None
) -> EmissionsBreakdown:
    """
    Calculate total emissions for all legs in a season.

    Args:
        legs: List of Leg or LegAnalysis objects
        num_trucks: Number of trucks
        freight_tonnes: Total freight weight
        params: Emissions parameters

    Returns:
        Aggregated EmissionsBreakdown
    """
    total_road = 0.0
    total_air = 0.0

    for item in legs:
        # Handle both Leg and LegAnalysis objects
        leg = item.leg if hasattr(item, "leg") else item
        emissions = calculate_leg_emissions(
            leg, num_trucks=num_trucks, freight_tonnes=freight_tonnes, params=params
        )

        total_road += emissions.road_co2e_kg
        total_air += emissions.air_co2e_kg

    return EmissionsBreakdown(road_co2e_kg=round(total_road, 2), air_co2e_kg=round(total_air, 2))


def get_emissions_per_km(emissions: EmissionsBreakdown, distance_km: float) -> float:
    """
    Calculate emissions per kilometer.

    Args:
        emissions: Emissions breakdown
        distance_km: Total distance

    Returns:
        CO2e per kilometer in kg
    """
    if distance_km == 0:
        return 0.0
    return emissions.total_co2e_kg / distance_km


def compare_transport_modes(
    distance_km: float, freight_tonnes: float, num_trucks: int = 8
) -> Dict[str, EmissionsBreakdown]:
    """
    Compare emissions for different transport mode scenarios.

    Args:
        distance_km: Distance to travel
        freight_tonnes: Total freight weight
        num_trucks: Number of trucks for road option

    Returns:
        Dictionary with scenarios: all_road, all_air, mixed_50
    """
    from f1ops.data_models import Circuit

    # Create a dummy leg for calculations
    dummy_circuit = Circuit(
        name="Start", city="Start", country="Europe", latitude=0.0, longitude=0.0
    )
    dummy_leg = Leg(
        from_circuit=dummy_circuit,
        to_circuit=dummy_circuit,
        distance_km=distance_km,
        method="haversine",
    )

    scenarios = {}

    # All road
    all_road_params = DEFAULT_EMISSIONS_PARAMS.copy()
    all_road_params["air_freight_fraction"] = 0.0
    scenarios["all_road"] = calculate_leg_emissions(
        dummy_leg, num_trucks=num_trucks, freight_tonnes=freight_tonnes, params=all_road_params
    )

    # All air
    all_air_params = DEFAULT_EMISSIONS_PARAMS.copy()
    all_air_params["air_freight_fraction"] = 1.0
    scenarios["all_air"] = calculate_leg_emissions(
        dummy_leg, num_trucks=num_trucks, freight_tonnes=freight_tonnes, params=all_air_params
    )

    # 50/50 mixed
    mixed_params = DEFAULT_EMISSIONS_PARAMS.copy()
    mixed_params["air_freight_fraction"] = 0.5
    scenarios["mixed_50"] = calculate_leg_emissions(
        dummy_leg, num_trucks=num_trucks, freight_tonnes=freight_tonnes, params=mixed_params
    )

    return scenarios


def calculate_carbon_offset_cost(
    emissions_kg: float, offset_price_eur_per_tonne: float = 20.0
) -> float:
    """
    Calculate cost of carbon offsetting.

    Args:
        emissions_kg: Total CO2e emissions in kg
        offset_price_eur_per_tonne: Price per tonne of CO2e

    Returns:
        Offset cost in EUR
    """
    emissions_tonnes = emissions_kg / 1000.0
    return emissions_tonnes * offset_price_eur_per_tonne
