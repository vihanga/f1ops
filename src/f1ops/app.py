"""Streamlit dashboard for F1Ops."""

import streamlit as st

from f1ops import __version__
from f1ops.config import DEFAULT_COST_PARAMS, DEFAULT_EMISSIONS_PARAMS
from f1ops.cost import calculate_leg_cost, calculate_season_cost, estimate_travel_hours
from f1ops.data_loader import get_available_seasons, get_european_races
from f1ops.data_models import LegAnalysis, SeasonAnalysis
from f1ops.emissions import calculate_leg_emissions, calculate_season_emissions
from f1ops.geo import build_season_legs
from f1ops.optimize import optimize_fleet_allocation
from f1ops.viz import (
    create_cost_breakdown_chart,
    create_distance_chart,
    create_emissions_chart,
    create_kpi_cards,
    create_route_map,
)

# Title
st.title("F1Ops: Team Logistics Analysis")
st.markdown(f"*Version {__version__}* - Analyzing F1 team logistics across Europe")

# Sidebar
st.sidebar.header("Configuration")

# Season selection
available_seasons = get_available_seasons()
if not available_seasons:
    st.error("No calendar data available. Please run the bootstrap script to generate data.")
    st.stop()

selected_season = st.sidebar.selectbox(
    "Select Season", options=available_seasons, index=len(available_seasons) - 1
)

# Team profile
st.sidebar.subheader("Team Profile")
num_trucks = st.sidebar.slider("Number of Trucks", min_value=4, max_value=16, value=8)
freight_tonnes = st.sidebar.number_input(
    "Total Freight (tonnes)", min_value=50.0, max_value=200.0, value=120.0
)

# Cost parameters
st.sidebar.subheader("Cost Parameters")
fuel_price = st.sidebar.number_input(
    "Fuel Price (EUR/L)", value=DEFAULT_COST_PARAMS["fuel_price_eur_per_l"], format="%.2f"
)
driver_wage = st.sidebar.number_input(
    "Driver Wage (EUR/h)", value=DEFAULT_COST_PARAMS["driver_wage_eur_per_hour"], format="%.2f"
)
toll_rate = st.sidebar.number_input(
    "Toll Rate (EUR/km)", value=DEFAULT_COST_PARAMS["toll_eur_per_km"], format="%.2f"
)

# Emissions parameters
st.sidebar.subheader("Emissions Parameters")
air_fraction = st.sidebar.slider(
    "Air Freight Fraction", min_value=0.0, max_value=1.0, value=0.0, step=0.1
)

# Build custom params
cost_params = DEFAULT_COST_PARAMS.copy()
cost_params["fuel_price_eur_per_l"] = fuel_price
cost_params["driver_wage_eur_per_hour"] = driver_wage
cost_params["toll_eur_per_km"] = toll_rate

emissions_params = DEFAULT_EMISSIONS_PARAMS.copy()
emissions_params["air_freight_fraction"] = air_fraction

# Load data
try:
    races = get_european_races(selected_season)
    if len(races) < 2:
        st.warning(
            f"Only {len(races)} European race(s) found for {selected_season}. "
            "Need at least 2 for route analysis."
        )
        st.stop()

    legs = build_season_legs(races, use_osrm=False)

    # Calculate analyses
    leg_analyses = []
    for leg in legs:
        cost = calculate_leg_cost(leg, num_trucks=num_trucks, params=cost_params)
        emissions = calculate_leg_emissions(
            leg, num_trucks=num_trucks, freight_tonnes=freight_tonnes, params=emissions_params
        )
        travel_hours = estimate_travel_hours(leg.distance_km, avg_speed_kmh=cost_params["avg_speed_kmh"])

        leg_analysis = LegAnalysis(
            leg=leg, cost=cost, emissions=emissions, travel_hours=travel_hours, num_trucks=num_trucks
        )
        leg_analyses.append(leg_analysis)

    # Calculate totals
    total_distance = sum(leg.distance_km for leg in legs)
    total_cost = calculate_season_cost(legs, num_trucks=num_trucks, params=cost_params)
    total_emissions = calculate_season_emissions(
        legs, num_trucks=num_trucks, freight_tonnes=freight_tonnes, params=emissions_params
    )
    total_hours = sum(la.travel_hours for la in leg_analyses)

    season_analysis = SeasonAnalysis(
        season=selected_season,
        legs=leg_analyses,
        total_distance_km=total_distance,
        total_cost=total_cost,
        total_emissions=total_emissions,
        total_travel_hours=total_hours,
    )

except FileNotFoundError as e:
    st.error(f"Data not found: {e}")
    st.info("Please run `python scripts/create_sample_data.py` to generate calendar data.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Main content
st.header(f"Season {selected_season} - European Leg Analysis")

# KPIs
kpis = create_kpi_cards(season_analysis)

st.write(f"**Total Distance:** {kpis['total_distance_km']:,.0f} km")
st.write(f"**Total Cost:** €{kpis['total_cost_eur']:,.0f}")
st.write(f"**Total CO2e:** {kpis['total_co2e_tonnes']:.1f} tonnes")
st.write(f"**Travel Time:** {kpis['total_travel_hours']:.1f} hours")
st.write(f"**Number of Legs:** {kpis['num_legs']}")

if "longest_leg_name" in kpis:
    st.write(
        f"**Longest Leg:** {kpis['longest_leg_name']} "
        f"({kpis['longest_leg_distance_km']:.0f} km)"
    )

# Map
st.subheader("Route Map")
route_map = create_route_map(legs)
st.write(route_map._repr_html_(), unsafe_allow_html=True)

# Charts
st.subheader("Analysis Charts")

st.write("**Distance by Leg**")
fig_dist = create_distance_chart(leg_analyses)
st.plotly_chart(fig_dist)

st.write("**Cost Breakdown**")
fig_cost = create_cost_breakdown_chart(leg_analyses)
st.plotly_chart(fig_cost)

st.write("**Emissions**")
fig_emissions = create_emissions_chart(leg_analyses)
st.plotly_chart(fig_emissions)

# Per-leg details
st.subheader("Leg-by-Leg Breakdown")
for idx, la in enumerate(leg_analyses):
    with st.beta_expander(f"Leg {idx + 1}: {la.leg.leg_name} ({la.leg.distance_km:.0f} km)"):
        st.write("**Cost**")
        st.write(f"Fuel: €{la.cost.fuel_cost_eur:.2f}")
        st.write(f"Labor: €{la.cost.labor_cost_eur:.2f}")
        st.write(f"Tolls: €{la.cost.toll_cost_eur:.2f}")
        st.write(f"Fixed: €{la.cost.fixed_cost_eur:.2f}")
        st.write(f"**Total: €{la.cost.total_cost_eur:.2f}**")

        st.write("**Emissions**")
        st.write(f"Road: {la.emissions.road_co2e_kg:.2f} kg")
        st.write(f"Air: {la.emissions.air_co2e_kg:.2f} kg")
        st.write(f"**Total: {la.emissions.total_co2e_kg:.2f} kg**")

        st.write("**Logistics**")
        st.write(f"Distance: {la.leg.distance_km:.2f} km")
        st.write(f"Travel Time: {la.travel_hours:.2f} hours")
        st.write(f"Trucks: {la.num_trucks}")
        st.write(f"Method: {la.leg.method}")

# Optimization
st.subheader("Fleet Optimization")
if st.button("Run Optimization"):
    with st.spinner("Optimizing fleet allocation..."):
        opt_result = optimize_fleet_allocation(
            legs, total_fleet_size=num_trucks, cost_params=cost_params
        )

    if opt_result.is_improved:
        st.success(
            f"Optimization found {opt_result.savings_percent:.1f}% savings "
            f"(€{opt_result.savings_eur:.2f})"
        )
    else:
        st.info("Current allocation is already optimal.")

    st.write(f"Original Cost: €{opt_result.original_cost_eur:,.2f}")
    st.write(f"Optimized Cost: €{opt_result.optimized_cost_eur:,.2f}")

# Export
st.subheader("Export Data")
import pandas as pd

export_data = []
for idx, la in enumerate(leg_analyses):
    export_data.append(
        {
            "leg": idx + 1,
            "from": la.leg.from_circuit.city,
            "to": la.leg.to_circuit.city,
            "distance_km": la.leg.distance_km,
            "cost_eur": la.cost.total_cost_eur,
            "co2e_kg": la.emissions.total_co2e_kg,
            "travel_hours": la.travel_hours,
        }
    )
df_export = pd.DataFrame(export_data)
csv = df_export.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"f1ops_{selected_season}_analysis.csv",
    mime="text/csv",
)

# Footer
st.markdown("---")
st.markdown(
    f"Built with F1Ops | Data sources: Public F1 calendars | Version {__version__}"
)
