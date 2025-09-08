# F1Ops: Formula 1 Logistics Analysis

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-42%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-45%25-yellow.svg)]()

Analyzing F1 team logistics using operations research and machine learning. Started in February 2020, resumed in August 2025 with modern ML tooling.

## Overview

F1 teams transport 40+ tonnes of equipment between European races every 1-2 weeks. This project models the logistics chain: route planning, cost analysis, emissions tracking, and fleet optimization. The 2025 update adds time series forecasting to predict future costs based on historical patterns.

**Core Problems Solved:**
- Route distance calculations between circuits (Barcelona → Monaco → Spielberg...)
- Multi-component cost modeling (fuel, labor, tolls, administrative overhead)
- CO2 emissions tracking for environmental reporting
- Truck allocation optimization (bin packing)
- Time series forecasting for budget planning

## Installation

```bash
git clone https://github.com/vihanga/f1ops.git
cd f1ops
pip install -e .
```

## Quick Start

```python
from f1ops.data_loader import get_european_races
from f1ops.geo import build_season_legs
from f1ops.cost import calculate_season_cost
from f1ops.config import DEFAULT_COST_PARAMS

# Load 2019 season
races = get_european_races(2019)
legs = build_season_legs(races)

# Calculate costs
total_cost = calculate_season_cost(legs, DEFAULT_COST_PARAMS)

print(f"Races: {len(races)}")
print(f"Distance: {sum(l.distance_km for l in legs):,.0f} km")
print(f"Total cost: €{total_cost.total_eur:,.2f}")
```

Output:
```
Races: 8
Distance: 4,234 km
Total cost: €156,789.45
```

## Example: Time Series Forecasting

New in 2025 - forecast logistics costs using Facebook Prophet:

```python
from f1ops.forecast import LogisticsCostForecaster, create_synthetic_historical_data

# Generate historical data (2020-2024)
historical_data = create_synthetic_historical_data(legs, 2020, 2024)

# Train model
forecaster = LogisticsCostForecaster()
df = forecaster.prepare_data(historical_data)
forecaster.fit(df)

# Forecast 2026 season
forecaster.predict(periods=365*2)
season_2026 = forecaster.get_race_season_forecast(2026)

print(f"2026 avg cost: €{season_2026['yhat'].mean():,.2f}")
print(f"Range: €{season_2026['yhat'].min():,.2f} - €{season_2026['yhat'].max():,.2f}")
```

See [`notebooks/06_time_series_forecasting.ipynb`](notebooks/06_time_series_forecasting.ipynb) for full walkthrough including cross-validation, component decomposition, and scenario analysis.

## Features

### Distance Calculation
Haversine formula for great-circle distances between circuit coordinates. Planned: OSRM integration for actual road routing.

```python
from f1ops.geo import calculate_haversine_distance

distance = calculate_haversine_distance(
    lat1=48.8566, lon1=2.3522,  # Paris
    lat2=45.6205, lon2=9.2814   # Monza
)  # Returns ~572 km
```

### Cost Modeling
Four-component cost breakdown:
- **Fuel**: Distance × consumption rate × fuel price
- **Labor**: Travel time × driver wages (2 drivers/truck)
- **Tolls**: Distance × toll rate per truck
- **Fixed**: Administrative, permits, insurance

```python
from f1ops.cost import calculate_leg_cost

cost = calculate_leg_cost(leg, num_trucks=8, params=DEFAULT_COST_PARAMS)

print(f"Total: €{cost.total_cost_eur:,.2f}")
print(f"  Fuel: €{cost.fuel_cost_eur:,.2f}")
print(f"  Labor: €{cost.labor_cost_eur:,.2f}")
print(f"  Tolls: €{cost.toll_cost_eur:,.2f}")
print(f"  Fixed: €{cost.fixed_cost_eur:,.2f}")
```

### Emissions Tracking
CO2e calculations for road freight using European emission factors.

```python
from f1ops.emissions import calculate_leg_emissions

emissions = calculate_leg_emissions(leg, num_trucks=8, params=DEFAULT_EMISSIONS_PARAMS)
print(f"CO2e: {emissions.total_co2e_kg / 1000:.2f} tonnes")
```

### Fleet Optimization
First-Fit Decreasing bin packing for cargo allocation:

```python
from f1ops.optimize import greedy_truck_allocation_bin_packing

cargo = [
    {"name": "Garage Equipment", "weight_kg": 8000},
    {"name": "Spare Parts", "weight_kg": 6000},
    {"name": "Hospitality", "weight_kg": 7000},
]

allocation = greedy_truck_allocation_bin_packing(
    cargo, num_trucks=3, truck_capacity_kg=20000
)

for truck_id, items in allocation.items():
    weight = sum(item['weight_kg'] for item in items)
    print(f"Truck {truck_id}: {weight:,} kg - {[i['name'] for i in items]}")
```

### Time Series Forecasting
Prophet-based forecasting with:
- Automatic trend detection
- Yearly seasonality (F1 calendar pattern)
- 95% confidence intervals
- Cross-validation metrics
- Component decomposition
- Scenario analysis

## Tech Stack

**2020 Version:**
- Python 3.8
- pandas, numpy
- Pydantic v1
- Basic Haversine calculations

**2025 Update:**
- Python 3.13
- Pydantic v2 (field validators, model validation)
- Prophet 1.1 (time series forecasting)
- XGBoost 3.1 / LightGBM 4.6 (gradient boosting)
- OR-Tools 9.14 (optimization)
- PyTorch 2.9 (deep learning experiments)
- MLflow 3.5 (experiment tracking)
- SHAP (model explainability)
- Plotly + Folium (interactive visualization)

## Project Structure

```
f1ops/
├── src/f1ops/
│   ├── data_loader.py      # Load calendars & circuits
│   ├── data_models.py      # Pydantic v2 models
│   ├── geo.py              # Distance calculations
│   ├── cost.py             # Cost modeling
│   ├── emissions.py        # CO2e calculations
│   ├── optimize.py         # Fleet optimization
│   ├── forecast.py         # Time series forecasting (NEW)
│   ├── viz.py              # Visualization helpers
│   └── config.py           # Parameters & constants
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_route_estimation.ipynb
│   ├── 03_cost_emissions.ipynb
│   ├── 04_optimization.ipynb
│   ├── 05_visualization.ipynb
│   └── 06_time_series_forecasting.ipynb  # NEW
│
├── data/
│   ├── calendars/          # 2010-2020 F1 seasons
│   ├── geo/                # Circuit coordinates
│   └── samples/            # Sample datasets
│
├── tests/                  # 42 tests, 45% coverage
└── artifacts/              # Saved models & forecasts
```

## Jupyter Notebooks

All notebooks use 2025 syntax (Python 3.13, pandas 2.3, matplotlib 3.10) and include live results:

1. **Data Ingestion** - Load F1 calendars, explore European circuits
2. **Route Estimation** - Haversine distances, leg construction
3. **Cost & Emissions** - Multi-component cost analysis, CO2e tracking
4. **Optimization** - Bin packing for truck allocation, fleet sizing
5. **Visualization** - Interactive maps (Folium), charts (Plotly)
6. **Time Series Forecasting** - Prophet models, scenario analysis, cross-validation

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=f1ops --cov-report=html

# Specific module
pytest tests/test_cost.py -v
```

**Current Stats:**
- 42 tests passing
- 45% code coverage
- Focus areas: data loading, cost calculations, distance functions

## Example Results: 2019 European Season

```
Races: 8 (Spain, Monaco, France, Austria, Germany, Hungary, Belgium, Italy)
Travel Legs: 7
Total Distance: 4,234 km
Estimated Cost: €156,789
  - Fuel: €38,016 (24.3%)
  - Labor: €87,633 (56.0%)
  - Tolls: €23,914 (15.3%)
  - Fixed: €7,226 (4.6%)
CO2 Emissions: 28.79 tonnes
```

## Assumptions & Limitations

**Assumptions:**
- 8 trucks per team @ 20 tonnes capacity
- Average speed: 80 km/h
- Fuel consumption: 30 L/100km
- Driver wages: €35/hour (2 drivers/truck)
- Toll rate: €0.25/km/truck
- CO2 factor: 850g/km/truck

**Limitations:**
- European races only (no flyaways)
- Road freight focused (no air/sea modeling)
- Haversine distances (not actual roads)
- Simplified customs, insurance, time windows

These are reasonable estimates for analysis. Real F1 operations are more complex.

## Future Development

**Planned:**
- OSRM integration for real road routing
- Flyaway races (air/sea freight modeling)
- Vehicle Routing Problem (VRP) with OR-Tools
- Reinforcement learning for dynamic scheduling
- External regressors (fuel prices, exchange rates)
- REST API for production forecasting

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Linting
ruff check src/

# Type checking
mypy src/

# Format
ruff format src/
```

## Data Sources

- **Circuit Coordinates**: Manual compilation from official F1 sources
- **Race Calendars**: Historical F1 schedules (2010-2020)
- **Cost Parameters**: Industry estimates, academic papers
- **Emission Factors**: European Environment Agency standards

## License

MIT License - see [LICENSE](LICENSE)

## Contact

Questions or ideas? Open an issue on GitHub.

---

*Last updated: September 2025*
