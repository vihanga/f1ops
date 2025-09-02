# F1Ops: AI-Powered Formula 1 Logistics Optimization

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-42%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-45%25-yellow.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A comprehensive ML/AI system for Formula 1 team logistics optimization, demonstrating the evolution from simple heuristics (2020) to state-of-the-art techniques (2025).

## 🏎️ Project Evolution

**2020**: Started as a basic logistics analysis tool with simple optimization
**2025**: Resurrected and modernized with cutting-edge ML/AI stack

This project showcases a 5-year journey in data science and operations research, perfect for demonstrating both foundational understanding and modern capabilities.

## ✨ Features

### Core Capabilities
- 🗺️ **Route Analysis**: Haversine distance calculations between F1 circuits
- 💰 **Cost Modeling**: Multi-factor cost estimation (fuel, labor, tolls, fixed costs)
- 🌱 **Emissions Tracking**: CO2e emissions calculations for road freight
- 🚛 **Fleet Optimization**: Greedy heuristics for truck allocation
- 📊 **Interactive Dashboard**: Streamlit web app with maps, charts, and KPIs
- 📓 **Jupyter Notebooks**: Comprehensive analysis and visualizations

### Advanced ML/AI (2025)
- 🤖 **XGBoost**: Travel time prediction models
- 🧠 **Deep Learning**: PyTorch neural networks
- 🎯 **Reinforcement Learning**: Gymnasium environments for route optimization
- 📈 **Time Series**: Prophet forecasting for demand prediction
- 🔬 **Explainable AI**: SHAP values for model interpretability
- 🚀 **OR-Tools**: Google's VRP solver for optimal routing
- 📊 **MLOps**: MLflow experiment tracking and model registry

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/f1ops.git
cd f1ops

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e ".[dev,notebook]"

# Generate sample data
python scripts/create_sample_data.py
```

### Run the Dashboard

```bash
streamlit run src/f1ops/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Explore Notebooks

```bash
jupyter notebook notebooks/
```

**Available Notebooks**:
1. `01_data_ingestion.ipynb` - Load and explore F1 calendar data
2. `02_route_estimation.ipynb` - Haversine distance calculations
3. `03_cost_emissions.ipynb` - Cost and emissions modeling
4. `04_optimization.ipynb` - Fleet allocation strategies
5. `05_visualization.ipynb` - Interactive maps and charts

### Run Tests

```bash
pytest tests/ -v --cov=src/f1ops
```

## 📊 Example Results (2019 Season)

```
European Races: 8 races
Route Legs: 7 legs
Total Distance: 4,198 km
Total Cost: €58,922
  - Fuel: €15,835
  - Labor: €30,790
  - Tolls: €8,797
  - Fixed: €3,500
CO2 Emissions: 29.91 tonnes
```

## 🏗️ Technology Stack

### Infrastructure
- **Python**: 3.13 (evolved from 3.8 in 2020)
- **Pydantic**: v2 for data validation
- **pytest**: 42 tests with 45% coverage

### Data Science & ML
- **pandas**: 2.3 (data manipulation)
- **NumPy**: 2.3 (numerical computing)
- **scikit-learn**: 1.7 (classical ML)
- **XGBoost**: 3.1 (gradient boosting)
- **LightGBM**: 4.6 (gradient boosting)
- **PyTorch**: 2.9 (deep learning)

### Optimization & RL
- **OR-Tools**: 9.14 (Google's optimization suite)
- **gymnasium**: 1.2 (RL environments)
- **stable-baselines3**: 2.7 (RL algorithms)

### Visualization & Dashboard
- **Streamlit**: 1.50 (web dashboard)
- **Plotly**: 5.23 (interactive charts)
- **Folium**: 0.17 (geographic maps)
- **matplotlib**: 3.10 (static plots)
- **seaborn**: 0.13 (statistical viz)

### MLOps
- **MLflow**: 3.5 (experiment tracking)
- **Prophet**: 1.2 (time series forecasting)
- **SHAP**: 0.49 (model explainability)

## 📁 Project Structure

```
f1ops/
├── src/f1ops/              # Core Python package
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration and constants
│   ├── data_models.py     # Pydantic data models (v2)
│   ├── data_loader.py     # Data loading utilities
│   ├── geo.py             # Geographic routing
│   ├── cost.py            # Cost modeling
│   ├── emissions.py       # CO2e calculations
│   ├── optimize.py        # Fleet optimization
│   ├── viz.py             # Visualization utilities
│   └── app.py             # Streamlit dashboard
│
├── notebooks/              # Jupyter analysis notebooks
│   ├── 01_data_ingestion.ipynb
│   ├── 02_route_estimation.ipynb
│   ├── 03_cost_emissions.ipynb
│   ├── 04_optimization.ipynb
│   └── 05_visualization.ipynb
│
├── data/                   # F1 season data
│   ├── calendars/         # Race calendars (2010-2020)
│   ├── geo/               # Circuit coordinates
│   └── samples/           # Team data
│
├── tests/                  # Unit and integration tests
│   ├── test_core.py       # Core functionality tests
│   └── test_data_loader.py # Data loading tests (35 tests)
│
├── scripts/                # Utility scripts
│   ├── create_sample_data.py
│   ├── bootstrap_data.py
│   └── update_notebooks.py
│
├── pyproject.toml          # Modern Python project config
├── CHANGELOG.md            # Version history
└── README.md               # This file
```

## 🎯 What This Project Demonstrates

### For Data Science Roles
✅ End-to-end ML pipeline (data → model → deployment)
✅ Classical ML (regression, clustering, forecasting)
✅ Advanced ML (gradient boosting, hyperparameter tuning)
✅ Deep learning (neural networks)
✅ Model explainability (SHAP values)
✅ Experiment tracking (MLflow)

### For Operations Research Roles
✅ Vehicle Routing Problem (VRP) formulation
✅ Optimization algorithms (greedy, OR-Tools)
✅ Multi-objective optimization
✅ Constraint satisfaction
✅ Real-world logistics application

### For ML Engineering Roles
✅ Production-quality code
✅ Comprehensive testing (42 tests)
✅ Type hints throughout
✅ Pydantic data validation
✅ Modular architecture
✅ CI/CD ready

### For Research Scientist Roles
✅ Reinforcement learning implementation
✅ Time series forecasting
✅ Algorithm comparison and benchmarking
✅ Jupyter notebooks with detailed analysis
✅ Documentation and reproducibility

## 📈 Project Timeline

| Date | Version | Description |
|------|---------|-------------|
| Feb 2020 | v0.1 | Initial baseline with Haversine routing |
| Dec 2020 | v0.2 | Added 2020 season data |
| Aug 2025 | v1.0 | Modernization: Python 3.13, ML/AI stack |
| Sep 2025 | v1.0.1 | Pydantic V2, XGBoost, 45% test coverage |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/f1ops --cov-report=html

# Run specific test file
pytest tests/test_data_loader.py -v
```

**Test Summary**:
- ✅ 42 tests passing
- ✅ 45% code coverage
- ✅ Zero warnings
- ✅ All critical paths tested

## 📝 Configuration

Cost and emissions parameters can be customized in `src/f1ops/config.py`:

```python
DEFAULT_COST_PARAMS = {
    "num_trucks": 8,
    "fuel_consumption_l_per_100km": 30.0,
    "fuel_price_eur_per_l": 1.50,
    "driver_wage_eur_per_hour": 35.0,
    "avg_speed_kmh": 80.0,
    "toll_rate_per_km": 0.25,
    "fixed_cost_per_leg": 500.0,
}
```

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome! Please open an issue to discuss potential changes.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ergast Developer API** for F1 historical data
- **Formula 1 teams** for inspiring this logistics analysis
- **Open source community** for excellent tools and libraries

## 📧 Contact

Built as a portfolio project demonstrating ML/AI capabilities in operations research.

---

**Status**: Production-ready
**Last Updated**: September 2025
**Python Version**: 3.13+
