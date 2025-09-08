#!/usr/bin/env python3
"""Execute and modernize remaining Jupyter notebooks (03-05)."""

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys
from pathlib import Path

# Change to project root
project_root = Path(__file__).parent.parent
notebooks_dir = project_root / "notebooks"

notebooks_to_update = [
    "03_cost_emissions.ipynb",
    "04_optimization.ipynb",
    "05_visualization.ipynb",
]

# Modern imports template
modern_imports_03 = '''import sys
sys.path.insert(0, '../src')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from f1ops.data_loader import get_european_races
from f1ops.geo import build_season_legs
from f1ops.cost import calculate_leg_cost, calculate_season_cost, estimate_travel_hours
from f1ops.emissions import calculate_leg_emissions, calculate_season_emissions
from f1ops.config import DEFAULT_COST_PARAMS, DEFAULT_EMISSIONS_PARAMS

# Modern 2025 plotting style
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

%matplotlib inline'''

modern_imports_04 = '''import sys
sys.path.insert(0, '../src')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from f1ops.data_loader import get_european_races
from f1ops.geo import build_season_legs
from f1ops.cost import calculate_leg_cost
from f1ops.optimize import greedy_truck_allocation, optimize_fleet_allocation
from f1ops.config import DEFAULT_COST_PARAMS

# Modern 2025 plotting style
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

%matplotlib inline'''

modern_imports_05 = '''import sys
sys.path.insert(0, '../src')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins
import plotly.graph_objects as go
import plotly.express as px

from f1ops.data_loader import get_european_races, load_circuits
from f1ops.geo import build_season_legs
from f1ops.cost import calculate_leg_cost, calculate_season_cost
from f1ops.emissions import calculate_leg_emissions
from f1ops.viz import create_route_map, create_distance_chart
from f1ops.config import DEFAULT_COST_PARAMS, DEFAULT_EMISSIONS_PARAMS

# Modern 2025 plotting style
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

%matplotlib inline'''

imports_map = {
    "03_cost_emissions.ipynb": modern_imports_03,
    "04_optimization.ipynb": modern_imports_04,
    "05_visualization.ipynb": modern_imports_05,
}

version_updates = {
    "03_cost_emissions.ipynb": """# F1Ops Cost & Emissions Analysis

This notebook explores the cost structure and environmental impact of F1 team logistics.

**Version**: 1.0 (Updated September 2025)
**Focus**: Multi-modal transport analysis with emissions tracking""",
    "04_optimization.ipynb": """# F1Ops Fleet Optimization

This notebook explores fleet allocation strategies for F1 team logistics using greedy heuristics.

**Version**: 1.0 (Updated September 2025)
**Method**: Greedy allocation algorithm with fleet sizing analysis""",
    "05_visualization.ipynb": """# F1Ops Visualization & Reporting

This notebook demonstrates visualization techniques for F1 logistics data using Folium and Plotly.

**Version**: 1.0 (Updated September 2025)
**Libraries**: Folium 0.18, Plotly 5.24, Python 3.13""",
}

def execute_notebook(nb_file):
    """Execute a single notebook with modern syntax."""
    nb_path = notebooks_dir / nb_file
    print(f"\n{'='*60}")
    print(f"Processing: {nb_file}")
    print(f"{'='*60}")

    # Read notebook
    with open(nb_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Update version cell (first cell)
    if nb_file in version_updates:
        nb.cells[0]['source'] = version_updates[nb_file]
        print("✓ Updated version information")

    # Update imports cell (second cell, index 1)
    if nb_file in imports_map:
        nb.cells[1]['source'] = imports_map[nb_file]
        print("✓ Updated to modern 2025 imports")

    # Execute notebook
    ep = ExecutePreprocessor(timeout=300, kernel_name='python3')
    try:
        print("⏳ Executing notebook...")
        ep.preprocess(nb, {'metadata': {'path': str(notebooks_dir)}})

        # Save executed notebook
        with open(nb_path, 'w') as f:
            nbformat.write(nb, f)

        print(f"✅ {nb_file} executed successfully")
        return True
    except Exception as e:
        print(f"❌ Error executing {nb_file}:")
        print(f"   {str(e)[:200]}")
        return False

def main():
    """Execute all notebooks."""
    print("F1Ops Notebook Modernization & Execution")
    print("Python 3.13 | pandas 2.3 | matplotlib 3.10")

    results = {}
    for nb_file in notebooks_to_update:
        results[nb_file] = execute_notebook(nb_file)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for nb_file, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status:12} {nb_file}")

    success_count = sum(results.values())
    total_count = len(results)
    print(f"\nTotal: {success_count}/{total_count} notebooks executed successfully")

    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
