"""Geographic routing and distance calculation."""

from typing import List, Optional, Tuple

import requests
from geopy.distance import geodesic

from f1ops.config import OSRM_BASE_URL, USE_OSRM
from f1ops.data_models import Circuit, Leg, RaceEvent


def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate distance between two coordinates using Haversine formula.

    Args:
        coord1: Tuple of (latitude, longitude)
        coord2: Tuple of (latitude, longitude)

    Returns:
        Distance in kilometers
    """
    return geodesic(coord1, coord2).kilometers


def osrm_distance(
    coord1: Tuple[float, float], coord2: Tuple[float, float], base_url: str = OSRM_BASE_URL
) -> Optional[float]:
    """
    Get driving distance using OSRM API.

    Args:
        coord1: Tuple of (latitude, longitude)
        coord2: Tuple of (latitude, longitude)
        base_url: OSRM server base URL

    Returns:
        Distance in kilometers, or None if request fails
    """
    try:
        # OSRM expects longitude,latitude
        lon1, lat1 = coord1[1], coord1[0]
        lon2, lat2 = coord2[1], coord2[0]

        url = f"{base_url}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
        params = {"overview": "false", "steps": "false"}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == "Ok" and data.get("routes"):
            distance_m = data["routes"][0]["distance"]
            return distance_m / 1000.0

        return None
    except Exception as e:
        print(f"OSRM request failed: {e}")
        return None


def calculate_leg_distance(
    from_circuit: Circuit, to_circuit: Circuit, use_osrm: bool = USE_OSRM
) -> Leg:
    """
    Calculate distance between two circuits.

    Args:
        from_circuit: Starting circuit
        to_circuit: Destination circuit
        use_osrm: Whether to attempt OSRM routing

    Returns:
        Leg object with distance and method
    """
    coord1 = (from_circuit.latitude, from_circuit.longitude)
    coord2 = (to_circuit.latitude, to_circuit.longitude)

    distance_km = None
    method = "haversine"

    # Try OSRM if enabled
    if use_osrm:
        osrm_dist = osrm_distance(coord1, coord2)
        if osrm_dist is not None:
            distance_km = osrm_dist
            method = "osrm"

    # Fallback to Haversine
    if distance_km is None:
        distance_km = haversine_distance(coord1, coord2)
        method = "haversine"

    return Leg(
        from_circuit=from_circuit,
        to_circuit=to_circuit,
        distance_km=round(distance_km, 2),
        method=method,
    )


def build_season_legs(races: List[RaceEvent], use_osrm: bool = USE_OSRM) -> List[Leg]:
    """
    Build consecutive legs from a list of races.

    Args:
        races: List of race events (should be sorted chronologically)
        use_osrm: Whether to attempt OSRM routing

    Returns:
        List of legs connecting consecutive races
    """
    if len(races) < 2:
        return []

    legs = []
    for i in range(len(races) - 1):
        from_circuit = races[i].circuit
        to_circuit = races[i + 1].circuit

        leg = calculate_leg_distance(from_circuit, to_circuit, use_osrm=use_osrm)
        legs.append(leg)

    return legs


def get_circuit_coordinates(circuit: Circuit) -> Tuple[float, float]:
    """
    Extract coordinates from circuit.

    Args:
        circuit: Circuit object

    Returns:
        Tuple of (latitude, longitude)
    """
    return (circuit.latitude, circuit.longitude)


def get_bounding_box(circuits: List[Circuit]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Calculate bounding box for a list of circuits.

    Args:
        circuits: List of circuits

    Returns:
        Tuple of ((min_lat, min_lon), (max_lat, max_lon))
    """
    if not circuits:
        return ((0.0, 0.0), (0.0, 0.0))

    lats = [c.latitude for c in circuits]
    lons = [c.longitude for c in circuits]

    return ((min(lats), min(lons)), (max(lats), max(lons)))


def get_center_point(circuits: List[Circuit]) -> Tuple[float, float]:
    """
    Calculate center point of circuits.

    Args:
        circuits: List of circuits

    Returns:
        Tuple of (latitude, longitude)
    """
    if not circuits:
        return (0.0, 0.0)

    lats = [c.latitude for c in circuits]
    lons = [c.longitude for c in circuits]

    return (sum(lats) / len(lats), sum(lons) / len(lons))
