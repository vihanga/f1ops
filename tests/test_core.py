"""Core tests for F1Ops modules."""

import pytest
from f1ops.config import DEFAULT_COST_PARAMS
from f1ops.cost import calculate_leg_cost, estimate_travel_hours
from f1ops.data_models import Circuit, Leg
from f1ops.emissions import calculate_leg_emissions
from f1ops.geo import calculate_leg_distance, haversine_distance
from f1ops.optimize import optimize_fleet_allocation


@pytest.fixture
def barcelona():
    return Circuit(
        name="Circuit de Barcelona-Catalunya",
        city="Barcelona",
        country="Spain",
        latitude=41.57,
        longitude=2.26,
    )


@pytest.fixture
def monaco():
    return Circuit(
        name="Circuit de Monaco",
        city="Monte Carlo",
        country="Monaco",
        latitude=43.73,
        longitude=7.42,
    )


@pytest.fixture
def sample_leg(barcelona, monaco):
    return calculate_leg_distance(barcelona, monaco, use_osrm=False)


def test_haversine_distance():
    """Test Haversine distance calculation."""
    coord1 = (41.57, 2.26)
    coord2 = (43.73, 7.42)
    distance = haversine_distance(coord1, coord2)

    assert isinstance(distance, float)
    assert 480 < distance < 500  # Actual distance is ~486 km


def test_calculate_leg_distance(barcelona, monaco):
    """Test leg distance calculation."""
    leg = calculate_leg_distance(barcelona, monaco, use_osrm=False)

    assert isinstance(leg, Leg)
    assert leg.from_circuit == barcelona
    assert leg.to_circuit == monaco
    assert leg.distance_km > 0
    assert leg.method == "haversine"


def test_calculate_leg_cost(sample_leg):
    """Test leg cost calculation."""
    cost = calculate_leg_cost(sample_leg, num_trucks=8)

    assert cost.fuel_cost_eur > 0
    assert cost.labor_cost_eur > 0
    assert cost.toll_cost_eur > 0
    assert cost.fixed_cost_eur > 0
    assert cost.total_cost_eur > 0


def test_estimate_travel_hours():
    """Test travel time estimation."""
    hours = estimate_travel_hours(800.0, avg_speed_kmh=80.0)
    assert hours == 10.0


def test_calculate_leg_emissions(sample_leg):
    """Test emissions calculation."""
    emissions = calculate_leg_emissions(sample_leg, num_trucks=8)

    assert emissions.road_co2e_kg > 0
    assert emissions.air_co2e_kg == 0
    assert emissions.total_co2e_kg == emissions.road_co2e_kg


def test_optimize_fleet_allocation():
    """Test fleet optimization."""
    from_circuit = Circuit(name="A", city="A", country="A", latitude=40.0, longitude=0.0)
    to_circuit1 = Circuit(name="B", city="B", country="B", latitude=42.0, longitude=2.0)
    to_circuit2 = Circuit(name="C", city="C", country="C", latitude=44.0, longitude=4.0)

    leg1 = Leg(from_circuit=from_circuit, to_circuit=to_circuit1, distance_km=300.0, method="haversine")
    leg2 = Leg(from_circuit=to_circuit1, to_circuit=to_circuit2, distance_km=600.0, method="haversine")

    result = optimize_fleet_allocation([leg1, leg2], total_fleet_size=12)

    assert result.original_cost_eur > 0
    assert result.optimized_cost_eur > 0
    # Greedy optimization may not always produce savings, just check it runs
    assert isinstance(result.savings_eur, float)
    assert isinstance(result.savings_percent, float)


def test_data_models_validation():
    """Test Pydantic model validation."""
    # Valid circuit
    circuit = Circuit(name="Test", city="Test", country="Test", latitude=45.0, longitude=5.0)
    assert circuit.latitude == 45.0

    # Invalid latitude should raise
    with pytest.raises(Exception):
        Circuit(name="Test", city="Test", country="Test", latitude=100.0, longitude=5.0)
