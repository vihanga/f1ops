#!/usr/bin/env python3
"""Update all Jupyter notebooks to 2025 standards and execute them."""

import subprocess
import sys
from pathlib import Path

notebooks = [
    "01_data_ingestion.ipynb",
    "02_route_estimation.ipynb",
    "03_cost_emissions.ipynb",
    "04_optimization.ipynb",
    "05_visualization.ipynb",
]

notebooks_dir = Path("notebooks")

print("=" * 70)
print("Updating and executing all F1Ops notebooks to 2025 standards")
print("=" * 70)
print()

success_count = 0
failed_notebooks = []

for nb_file in notebooks:
    nb_path = notebooks_dir / nb_file
    print(f"Processing: {nb_file}")

    try:
        # Execute notebook and update in-place
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--inplace",
                str(nb_path),
                "--ExecutePreprocessor.timeout=300"
            ],
            capture_output=True,
            text=True,
            timeout=360
        )

        if result.returncode == 0:
            print(f"  ✅ Success - notebook updated with live results")
            success_count += 1
        else:
            print(f"  ❌ Failed - {result.stderr[:200]}")
            failed_notebooks.append(nb_file)

    except Exception as e:
        print(f"  ❌ Error - {e}")
        failed_notebooks.append(nb_file)

    print()

print("=" * 70)
print(f"Results: {success_count}/{len(notebooks)} notebooks updated successfully")

if failed_notebooks:
    print(f"\\nFailed notebooks: {', '.join(failed_notebooks)}")
    sys.exit(1)
else:
    print("\\n✅ All notebooks updated and executed with live results!")
    sys.exit(0)
