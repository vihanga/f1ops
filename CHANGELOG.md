# Changelog

All notable changes to F1Ops will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- OR-Tools integration for Vehicle Routing Problem
- Machine learning cost prediction
- Time series forecasting
- API migration from Ergast to alternatives

## [0.1.0] - 2020-02-28

### Added
- Initial project scaffolding and configuration
- Calendar data for seasons 2010-2019
- European circuits geographic database
- Haversine-based route distance estimation
- Parameterized cost model (fuel, labor, tolls, fixed costs)
- Road freight emissions model (CO2e)
- Basic greedy fleet allocation optimizer
- Streamlit dashboard with interactive map and KPIs
- Folium route visualization
- Plotly charts for cost and emissions breakdown
- Unit tests for core modules (geo, cost, emissions, optimize)
- Bootstrap script for data generation
- OSRM integration example script
- Documentation and README
- Docker containerization
- Pre-commit hooks (black, isort, flake8, mypy)
- F1 teams database for 2010-2019

### Notes
- Baseline release covering F1 seasons 2010-2019
- Offline-first design with Haversine distance calculation
- Optional external API calls gated behind feature flags
- Python 3.8, Streamlit 0.54.0, Pydantic v1

[Unreleased]: https://github.com/yourusername/f1ops/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/f1ops/releases/tag/v0.1.0
