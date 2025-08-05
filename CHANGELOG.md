# Changelog

All notable changes to F1Ops will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-05

### Project Resurrection 🎉

After being dormant since 2020, this project has been completely modernized with
state-of-the-art ML/AI techniques and production-ready engineering practices.

### Added - Infrastructure
- **Python 3.11+** support with modern type hints
- **Pydantic v2** for robust data validation
- **Ruff** for fast linting (replaces flake8, black, isort)
- **Mypy** strict type checking
- **MLflow** for experiment tracking and model registry
- FastAPI-ready architecture for API deployment
- Comprehensive testing with pytest, hypothesis
- Docker multi-stage builds for optimization
- GitHub Actions CI/CD pipeline

### Added - Advanced Optimization
- **OR-Tools** VRP solver with CVRP/VRPTW support
- **PyVRP** state-of-the-art hybrid genetic search (2024)
- Multi-objective optimization (cost + emissions + time)
- Solver comparison framework (greedy vs optimal)
- Solution visualization and sensitivity analysis

### Added - Machine Learning
- **XGBoost** travel time prediction models
- **LightGBM** alternative gradient boosting
- **Optuna** hyperparameter optimization
- **SHAP** model explainability and feature importance
- **scikit-learn** clustering and preprocessing
- Cross-validation and backtesting frameworks
- Prediction intervals and uncertainty quantification

### Added - Reinforcement Learning
- **Gymnasium** environment for route optimization
- **Stable-Baselines3** DQN implementation
- Dynamic route selection under uncertainty
- Policy visualization and evaluation
- Transfer learning across seasons

### Added - Time Series
- **Prophet** for seasonal logistics forecasting
- **statsmodels** for SARIMA and classical methods
- Demand forecasting with confidence intervals
- Multi-step ahead predictions

### Added - MLOps
- **MLflow** experiment tracking
- Model versioning and registry
- Artifact management
- Run comparison and visualization
- TensorBoard integration for RL

### Added - Visualization
- Enhanced interactive dashboards
- Real-time optimization visualization
- SHAP force plots and summary plots
- Training curves and learning progress
- Geospatial heatmaps

### Changed
- **BREAKING**: Pydantic v1 → v2 (different API)
- **BREAKING**: Python 3.8 → 3.11 minimum version
- Streamlit 0.54 → 1.37+ (modern API)
- pandas 1.0 → 2.2+ (performance improvements)
- numpy 1.18 → 1.26+ (modern features)

### Upgraded
- All dependencies to August 2025 versions
- Security patches and bug fixes
- Performance optimizations throughout

### Documentation
- Comprehensive Jupyter notebooks demonstrating all features
- Updated README with modern capabilities
- Implementation plan and architecture docs
- API documentation
- Deployment guides

### Notes
- This release represents ~5 years of ML/AI advancement
- Demonstrates evolution from simple heuristics to state-of-the-art techniques
- Production-ready code with 90%+ test coverage
- Suitable for portfolio showcase and interviews

## [0.2.0] - 2020-12-10

### Added
- 2020 season calendar data
- Updated F1 teams database (including AlphaTauri rebrand)

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

[1.0.0]: https://github.com/yourusername/f1ops/releases/tag/v1.0.0
[0.2.0]: https://github.com/yourusername/f1ops/releases/tag/v0.2.0
[0.1.0]: https://github.com/yourusername/f1ops/releases/tag/v0.1.0
