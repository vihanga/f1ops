"""Optimization module for route and fleet allocation."""

from typing import Dict, List

from f1ops.config import DEFAULT_COST_PARAMS, OPTIMIZATION_PARAMS
from f1ops.cost import calculate_leg_cost, calculate_season_cost
from f1ops.data_models import Leg, LegAnalysis, OptimizationResult


def greedy_truck_allocation(
    legs: List[Leg],
    min_trucks: int = 4,
    max_trucks: int = 12,
    cost_params: Dict[str, float] = None,
) -> Dict[int, int]:
    """
    Greedy heuristic for truck allocation per leg.

    Allocates trucks to minimize cost while respecting capacity constraints.

    Args:
        legs: List of travel legs
        min_trucks: Minimum trucks per leg
        max_trucks: Maximum trucks per leg
        cost_params: Cost calculation parameters

    Returns:
        Dictionary mapping leg index to optimal truck count
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS.copy()

    allocation = {}

    for idx, leg in enumerate(legs):
        # Try different truck counts and pick the most cost-effective
        best_cost = float("inf")
        best_count = min_trucks

        for count in range(min_trucks, max_trucks + 1):
            cost = calculate_leg_cost(leg, num_trucks=count, params=cost_params)
            # Normalize by truck count to favor efficiency
            cost_per_truck = cost.total_cost_eur / count

            if cost_per_truck < best_cost:
                best_cost = cost_per_truck
                best_count = count

        allocation[idx] = best_count

    return allocation


def optimize_fleet_allocation(
    legs: List[Leg], total_fleet_size: int = 12, cost_params: Dict[str, float] = None
) -> OptimizationResult:
    """
    Optimize fleet allocation across legs with constrained total fleet.

    This is a simple greedy approach. For production, consider using OR-Tools.

    Args:
        legs: List of travel legs
        total_fleet_size: Total available trucks
        cost_params: Cost calculation parameters

    Returns:
        OptimizationResult with savings
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS.copy()

    # Calculate baseline cost (equal allocation)
    trucks_per_leg = max(1, total_fleet_size // max(len(legs), 1))
    baseline_costs = [
        calculate_leg_cost(leg, num_trucks=trucks_per_leg, params=cost_params) for leg in legs
    ]
    baseline_total = sum(c.total_cost_eur for c in baseline_costs)

    # Greedy optimization: prioritize longer legs
    leg_priorities = sorted(
        enumerate(legs), key=lambda x: x[1].distance_km, reverse=True
    )

    allocation = {}
    remaining_fleet = total_fleet_size

    # Allocate more trucks to longer legs
    for idx, leg in leg_priorities:
        if len(allocation) < len(legs) - 1:
            # Allocate proportionally, but ensure at least 1 truck
            proportion = leg.distance_km / sum(l.distance_km for l in legs)
            allocated = max(1, int(proportion * total_fleet_size))
            allocated = min(allocated, remaining_fleet - (len(legs) - len(allocation) - 1))
        else:
            # Last leg gets remaining trucks
            allocated = max(1, remaining_fleet)

        allocation[idx] = allocated
        remaining_fleet -= allocated

    # Calculate optimized cost
    optimized_costs = [
        calculate_leg_cost(legs[idx], num_trucks=allocation[idx], params=cost_params)
        for idx in range(len(legs))
    ]
    optimized_total = sum(c.total_cost_eur for c in optimized_costs)

    savings = baseline_total - optimized_total
    savings_pct = (savings / baseline_total * 100) if baseline_total > 0 else 0.0

    return OptimizationResult(
        original_cost_eur=round(baseline_total, 2),
        optimized_cost_eur=round(optimized_total, 2),
        savings_eur=round(savings, 2),
        savings_percent=round(savings_pct, 2),
        method="greedy_fleet_allocation",
        parameters={"total_fleet_size": total_fleet_size, "allocation": allocation},
    )


def check_driver_hours_compliance(
    legs: List[LegAnalysis], max_daily_hours: float = None
) -> Dict[int, bool]:
    """
    Check if travel hours comply with driver regulations.

    Args:
        legs: List of leg analyses with travel hours
        max_daily_hours: Maximum allowed driving hours per day

    Returns:
        Dictionary mapping leg index to compliance status
    """
    if max_daily_hours is None:
        max_daily_hours = OPTIMIZATION_PARAMS["max_driver_hours_per_day"]

    compliance = {}
    for idx, leg_analysis in enumerate(legs):
        # Simple check: is travel time within daily limit?
        is_compliant = leg_analysis.travel_hours <= max_daily_hours
        compliance[idx] = is_compliant

    return compliance


def suggest_route_splitting(
    leg: Leg, max_daily_hours: float = None, avg_speed_kmh: float = 80.0
) -> Dict[str, any]:
    """
    Suggest if a route should be split into multiple days.

    Args:
        leg: Travel leg
        max_daily_hours: Maximum driving hours per day
        avg_speed_kmh: Average travel speed

    Returns:
        Dictionary with splitting recommendation
    """
    if max_daily_hours is None:
        max_daily_hours = OPTIMIZATION_PARAMS["max_driver_hours_per_day"]

    travel_hours = leg.distance_km / avg_speed_kmh
    days_needed = int(travel_hours // max_daily_hours) + (
        1 if travel_hours % max_daily_hours > 0 else 0
    )

    return {
        "leg_name": leg.leg_name,
        "distance_km": leg.distance_km,
        "travel_hours": round(travel_hours, 2),
        "days_needed": max(1, days_needed),
        "requires_splitting": days_needed > 1,
        "recommended_stops": max(0, days_needed - 1),
    }


def calculate_optimization_scenarios(
    legs: List[Leg], fleet_sizes: List[int], cost_params: Dict[str, float] = None
) -> Dict[int, OptimizationResult]:
    """
    Calculate optimization results for different fleet sizes.

    Args:
        legs: List of travel legs
        fleet_sizes: List of fleet sizes to test
        cost_params: Cost calculation parameters

    Returns:
        Dictionary mapping fleet size to optimization result
    """
    scenarios = {}
    for size in fleet_sizes:
        result = optimize_fleet_allocation(legs, total_fleet_size=size, cost_params=cost_params)
        scenarios[size] = result

    return scenarios


def simple_lp_optimization(legs: List[Leg], num_trucks: int = 8) -> OptimizationResult:
    """
    Placeholder for LP-based optimization using OR-Tools.

    This would implement a more sophisticated optimization using linear programming.
    For the MVP, we use the greedy approach above.

    Args:
        legs: List of travel legs
        num_trucks: Number of trucks

    Returns:
        OptimizationResult
    """
    # For now, just call the greedy optimizer
    # In a future version, this could use OR-Tools' CP-SAT or linear solver
    return optimize_fleet_allocation(legs, total_fleet_size=num_trucks)
