"""Cost modeling for F1 logistics."""

from typing import Dict

from f1ops.config import DEFAULT_COST_PARAMS
from f1ops.data_models import CostBreakdown, Leg


def calculate_leg_cost(
    leg: Leg, num_trucks: int = 8, params: Dict[str, float] = None
) -> CostBreakdown:
    """
    Calculate cost breakdown for a single leg.

    Args:
        leg: Travel leg
        num_trucks: Number of trucks
        params: Cost parameters (uses defaults if None)

    Returns:
        CostBreakdown with detailed costs
    """
    if params is None:
        params = DEFAULT_COST_PARAMS.copy()

    distance_km = leg.distance_km

    # Fuel cost
    fuel_per_truck_l = (distance_km / 100.0) * params["fuel_consumption_l_per_100km"]
    total_fuel_l = fuel_per_truck_l * num_trucks
    fuel_cost = total_fuel_l * params["fuel_price_eur_per_l"]

    # Labor cost (based on travel time)
    avg_speed = params["avg_speed_kmh"]
    travel_hours = distance_km / avg_speed
    # Assume 2 drivers per truck working in shifts
    total_driver_hours = travel_hours * num_trucks * 2
    labor_cost = total_driver_hours * params["driver_wage_eur_per_hour"]

    # Toll costs
    toll_cost = distance_km * params["toll_eur_per_km"] * num_trucks

    # Fixed costs (permits, admin, etc.)
    fixed_cost = params["fixed_cost_per_leg_eur"]

    return CostBreakdown(
        fuel_cost_eur=round(fuel_cost, 2),
        labor_cost_eur=round(labor_cost, 2),
        toll_cost_eur=round(toll_cost, 2),
        fixed_cost_eur=round(fixed_cost, 2),
    )


def calculate_season_cost(
    legs: list, num_trucks: int = 8, params: Dict[str, float] = None
) -> CostBreakdown:
    """
    Calculate total cost for all legs in a season.

    Args:
        legs: List of Leg or LegAnalysis objects
        num_trucks: Number of trucks
        params: Cost parameters

    Returns:
        Aggregated CostBreakdown
    """
    total_fuel = 0.0
    total_labor = 0.0
    total_toll = 0.0
    total_fixed = 0.0

    for item in legs:
        # Handle both Leg and LegAnalysis objects
        leg = item.leg if hasattr(item, "leg") else item
        cost = calculate_leg_cost(leg, num_trucks=num_trucks, params=params)

        total_fuel += cost.fuel_cost_eur
        total_labor += cost.labor_cost_eur
        total_toll += cost.toll_cost_eur
        total_fixed += cost.fixed_cost_eur

    return CostBreakdown(
        fuel_cost_eur=round(total_fuel, 2),
        labor_cost_eur=round(total_labor, 2),
        toll_cost_eur=round(total_toll, 2),
        fixed_cost_eur=round(total_fixed, 2),
    )


def estimate_travel_hours(distance_km: float, avg_speed_kmh: float = 80.0) -> float:
    """
    Estimate travel time in hours.

    Args:
        distance_km: Distance in kilometers
        avg_speed_kmh: Average speed including stops

    Returns:
        Travel time in hours
    """
    return distance_km / avg_speed_kmh


def get_cost_per_km(cost: CostBreakdown, distance_km: float) -> float:
    """
    Calculate cost per kilometer.

    Args:
        cost: Cost breakdown
        distance_km: Total distance

    Returns:
        Cost per kilometer in EUR
    """
    if distance_km == 0:
        return 0.0
    return cost.total_cost_eur / distance_km


def optimize_truck_count(
    distance_km: float, freight_tonnes: float, truck_capacity_tonnes: float = 20.0
) -> int:
    """
    Calculate minimum number of trucks needed.

    Args:
        distance_km: Distance to travel
        freight_tonnes: Total freight weight
        truck_capacity_tonnes: Capacity per truck

    Returns:
        Minimum number of trucks required
    """
    import math

    return max(1, math.ceil(freight_tonnes / truck_capacity_tonnes))


def compare_scenarios(
    leg: Leg, truck_counts: list, params: Dict[str, float] = None
) -> Dict[int, CostBreakdown]:
    """
    Compare costs for different truck count scenarios.

    Args:
        leg: Travel leg
        truck_counts: List of truck counts to compare
        params: Cost parameters

    Returns:
        Dictionary mapping truck count to cost breakdown
    """
    results = {}
    for count in truck_counts:
        results[count] = calculate_leg_cost(leg, num_trucks=count, params=params)
    return results
