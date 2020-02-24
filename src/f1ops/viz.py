"""Visualization utilities for F1Ops."""

from typing import List, Optional

import folium
import plotly.graph_objects as go

from f1ops.data_models import Leg, LegAnalysis, SeasonAnalysis
from f1ops.geo import get_center_point


def create_route_map(
    legs: List[Leg], center: Optional[tuple] = None, zoom_start: int = 5
) -> folium.Map:
    """
    Create an interactive Folium map with route lines.

    Args:
        legs: List of travel legs
        center: Map center (lat, lon), auto-calculated if None
        zoom_start: Initial zoom level

    Returns:
        Folium map object
    """
    # Extract all circuits
    circuits = []
    for leg in legs:
        if leg.from_circuit not in circuits:
            circuits.append(leg.from_circuit)
        if leg.to_circuit not in circuits:
            circuits.append(leg.to_circuit)

    # Calculate center if not provided
    if center is None:
        center = get_center_point(circuits)

    # Create map
    m = folium.Map(location=center, zoom_start=zoom_start, tiles="OpenStreetMap")

    # Add circuit markers
    for circuit in circuits:
        folium.CircleMarker(
            location=[circuit.latitude, circuit.longitude],
            radius=6,
            popup=f"<b>{circuit.name}</b><br>{circuit.city}, {circuit.country}",
            color="red",
            fill=True,
            fillColor="red",
            fillOpacity=0.7,
        ).add_to(m)

    # Add route lines
    for idx, leg in enumerate(legs):
        coords = [
            [leg.from_circuit.latitude, leg.from_circuit.longitude],
            [leg.to_circuit.latitude, leg.to_circuit.longitude],
        ]

        folium.PolyLine(
            coords,
            color="blue",
            weight=3,
            opacity=0.6,
            popup=f"<b>Leg {idx + 1}</b><br>{leg.leg_name}<br>{leg.distance_km:.0f} km",
        ).add_to(m)

    return m


def create_distance_chart(leg_analyses: List[LegAnalysis]) -> go.Figure:
    """
    Create a bar chart of distances per leg.

    Args:
        leg_analyses: List of leg analyses

    Returns:
        Plotly figure
    """
    leg_names = [la.leg.leg_name for la in leg_analyses]
    distances = [la.leg.distance_km for la in leg_analyses]

    fig = go.Figure(
        data=[go.Bar(x=leg_names, y=distances, marker_color="lightblue", name="Distance (km)")]
    )

    fig.update_layout(
        title="Distance by Leg",
        xaxis_title="Leg",
        yaxis_title="Distance (km)",
        height=400,
        showlegend=False,
    )

    return fig


def create_cost_breakdown_chart(leg_analyses: List[LegAnalysis]) -> go.Figure:
    """
    Create a stacked bar chart of cost breakdown per leg.

    Args:
        leg_analyses: List of leg analyses

    Returns:
        Plotly figure
    """
    leg_names = [la.leg.leg_name for la in leg_analyses]
    fuel_costs = [la.cost.fuel_cost_eur for la in leg_analyses]
    labor_costs = [la.cost.labor_cost_eur for la in leg_analyses]
    toll_costs = [la.cost.toll_cost_eur for la in leg_analyses]
    fixed_costs = [la.cost.fixed_cost_eur for la in leg_analyses]

    fig = go.Figure(
        data=[
            go.Bar(name="Fuel", x=leg_names, y=fuel_costs),
            go.Bar(name="Labor", x=leg_names, y=labor_costs),
            go.Bar(name="Tolls", x=leg_names, y=toll_costs),
            go.Bar(name="Fixed", x=leg_names, y=fixed_costs),
        ]
    )

    fig.update_layout(
        barmode="stack",
        title="Cost Breakdown by Leg",
        xaxis_title="Leg",
        yaxis_title="Cost (EUR)",
        height=400,
    )

    return fig


def create_emissions_chart(leg_analyses: List[LegAnalysis]) -> go.Figure:
    """
    Create a bar chart of emissions per leg.

    Args:
        leg_analyses: List of leg analyses

    Returns:
        Plotly figure
    """
    leg_names = [la.leg.leg_name for la in leg_analyses]
    road_emissions = [la.emissions.road_co2e_kg / 1000 for la in leg_analyses]
    air_emissions = [la.emissions.air_co2e_kg / 1000 for la in leg_analyses]

    fig = go.Figure(
        data=[
            go.Bar(name="Road", x=leg_names, y=road_emissions),
            go.Bar(name="Air", x=leg_names, y=air_emissions),
        ]
    )

    fig.update_layout(
        barmode="stack",
        title="Emissions by Leg",
        xaxis_title="Leg",
        yaxis_title="CO2e (tonnes)",
        height=400,
    )

    return fig


def create_kpi_cards(analysis: SeasonAnalysis) -> dict:
    """
    Generate KPI data for display.

    Args:
        analysis: Season analysis

    Returns:
        Dictionary with KPI values
    """
    kpis = {
        "total_distance_km": round(analysis.total_distance_km, 0),
        "total_cost_eur": round(analysis.total_cost.total_cost_eur, 0),
        "total_co2e_tonnes": round(analysis.total_emissions.total_co2e_tonnes, 2),
        "num_legs": analysis.num_legs,
        "avg_leg_distance_km": round(analysis.avg_leg_distance_km, 0),
        "total_travel_hours": round(analysis.total_travel_hours, 1),
    }

    # Find longest leg
    if analysis.legs:
        longest_leg = max(analysis.legs, key=lambda x: x.leg.distance_km)
        kpis["longest_leg_name"] = longest_leg.leg.leg_name
        kpis["longest_leg_distance_km"] = round(longest_leg.leg.distance_km, 0)

    return kpis
