# F1Ops: Formula 1 Team Logistics Analysis

A data-driven exploration of Formula 1 team logistics across the European season, analyzing travel routes, freight costs, emissions, and optimization opportunities.

## Features

- **Route Analysis**: Calculate distances between circuits using Haversine formula
- **Cost Modeling**: Parameterized cost estimation including fuel, labor, tolls, and fixed costs
- **Emissions Tracking**: CO2e emissions for road freight
- **Fleet Optimization**: Simple greedy heuristics for truck allocation
- **Interactive Dashboard**: Streamlit web app with maps, charts, and KPIs
- **Report Export**: CSV export for analysis results

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/f1ops.git
cd f1ops

# Set up environment
make setup
```

### Generate Calendar Data

```bash
# Generate sample data for 2010-2019
python scripts/create_sample_data.py
```

### Run the Dashboard

```bash
make run
# Or directly:
streamlit run src/f1ops/app.py
```

### Run Tests

```bash
make test
```

## Configuration

### Cost Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Number of Trucks | 8 | Fleet size |
| Fuel Consumption | 30 L/100km | Average truck fuel usage |
| Fuel Price | €1.50/L | Diesel price |
| Driver Wage | €35/hour | Labor cost |
| Average Speed | 80 km/h | Including stops |
| Toll Rate | €0.25/km | Per truck |
| Fixed Cost | €500/leg | Permits, admin |

### Emissions Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Road Freight | 850 g CO2e/km | Per truck |
| Air Fraction | 0% | Portion shipped by air |

## Data Sources

- F1 Calendar Data: Ergast Motor Racing API
- Circuit Coordinates: Public F1 circuit databases
- Routing: Haversine formula (default)

## Project Structure

```
f1ops/
├── src/f1ops/           # Core Python modules
│   ├── config.py        # Configuration and constants
│   ├── data_models.py   # Pydantic data models
│   ├── data_loader.py   # Calendar and circuit data loading
│   ├── geo.py           # Geographic routing
│   ├── cost.py          # Cost modeling
│   ├── emissions.py     # Emissions calculations
│   ├── optimize.py      # Fleet optimization
│   ├── viz.py           # Visualization utilities
│   └── app.py           # Streamlit dashboard
├── data/                # Calendar and circuit data
├── scripts/             # Utility scripts
├── tests/               # Unit tests
└── docs/                # Documentation
```

## Development

### Run Linters

```bash
make lint
make format
```

### Docker

```bash
make docker-build
make docker-run
# Access at http://localhost:8501
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Ergast Developer API for F1 data
- Formula 1 teams for inspiring logistics analysis
- Open source community for excellent tools

---

**Version**: 0.1.0
**Status**: Alpha
**Python**: 3.8+
