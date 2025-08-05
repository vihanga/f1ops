#!/usr/bin/env python3
"""Create sample F1 calendar data for testing (offline mode)."""

import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from f1ops.config import CALENDARS_DIR, GEO_DIR, EUROPEAN_COUNTRIES

# Sample F1 circuits in Europe with real coordinates
SAMPLE_CIRCUITS = [
    {"name": "Circuit de Barcelona-Catalunya", "city": "Montmeló", "country": "Spain",
     "latitude": 41.5700, "longitude": 2.2611},
    {"name": "Circuit de Monaco", "city": "Monte Carlo", "country": "Monaco",
     "latitude": 43.7347, "longitude": 7.4206},
    {"name": "Autodromo Nazionale di Monza", "city": "Monza", "country": "Italy",
     "latitude": 45.6205, "longitude": 9.2814},
    {"name": "Hungaroring", "city": "Budapest", "country": "Hungary",
     "latitude": 47.5818, "longitude": 19.2511},
    {"name": "Spa-Francorchamps", "city": "Spa", "country": "Belgium",
     "latitude": 50.4372, "longitude": 5.9714},
    {"name": "Silverstone Circuit", "city": "Silverstone", "country": "UK",
     "latitude": 52.0786, "longitude": -1.0169},
    {"name": "Red Bull Ring", "city": "Spielberg", "country": "Austria",
     "latitude": 47.2197, "longitude": 14.7647},
    {"name": "Hockenheimring", "city": "Hockenheim", "country": "Germany",
     "latitude": 49.3278, "longitude": 8.5656},
    {"name": "Nürburgring", "city": "Nürburg", "country": "Germany",
     "latitude": 50.3356, "longitude": 6.9475},
]

# Sample 2019 European season (simplified)
SAMPLE_2019_RACES = [
    {"round": 5, "race_name": "Spanish Grand Prix", "circuit_name": "Circuit de Barcelona-Catalunya",
     "city": "Montmeló", "country": "Spain", "race_date": "2019-05-12",
     "latitude": 41.5700, "longitude": 2.2611},
    {"round": 6, "race_name": "Monaco Grand Prix", "circuit_name": "Circuit de Monaco",
     "city": "Monte Carlo", "country": "Monaco", "race_date": "2019-05-26",
     "latitude": 43.7347, "longitude": 7.4206},
    {"round": 8, "race_name": "French Grand Prix", "circuit_name": "Circuit Paul Ricard",
     "city": "Le Castellet", "country": "France", "race_date": "2019-06-23",
     "latitude": 43.2506, "longitude": 5.7919},
    {"round": 9, "race_name": "Austrian Grand Prix", "circuit_name": "Red Bull Ring",
     "city": "Spielberg", "country": "Austria", "race_date": "2019-06-30",
     "latitude": 47.2197, "longitude": 14.7647},
    {"round": 10, "race_name": "British Grand Prix", "circuit_name": "Silverstone Circuit",
     "city": "Silverstone", "country": "UK", "race_date": "2019-07-14",
     "latitude": 52.0786, "longitude": -1.0169},
    {"round": 11, "race_name": "German Grand Prix", "circuit_name": "Hockenheimring",
     "city": "Hockenheim", "country": "Germany", "race_date": "2019-07-28",
     "latitude": 49.3278, "longitude": 8.5656},
    {"round": 12, "race_name": "Hungarian Grand Prix", "circuit_name": "Hungaroring",
     "city": "Budapest", "country": "Hungary", "race_date": "2019-08-04",
     "latitude": 47.5818, "longitude": 19.2511},
    {"round": 13, "race_name": "Belgian Grand Prix", "circuit_name": "Spa-Francorchamps",
     "city": "Spa", "country": "Belgium", "race_date": "2019-09-01",
     "latitude": 50.4372, "longitude": 5.9714},
    {"round": 14, "race_name": "Italian Grand Prix", "circuit_name": "Autodromo Nazionale di Monza",
     "city": "Monza", "country": "Italy", "race_date": "2019-09-08",
     "latitude": 45.6205, "longitude": 9.2814},
]


def create_sample_calendars() -> None:
    """Create sample calendar files for testing."""
    CALENDARS_DIR.mkdir(parents=True, exist_ok=True)

    # For simplicity, replicate 2019 data for all years 2010-2019
    for year in range(2010, 2020):
        races = []
        for race in SAMPLE_2019_RACES:
            race_copy = race.copy()
            race_copy["race_date"] = race["race_date"].replace("2019", str(year))
            races.append(race_copy)

        df = pd.DataFrame(races)
        output_file = CALENDARS_DIR / f"f1_calendar_{year}.csv"
        df.to_csv(output_file, index=False)
        print(f"Created {output_file}")


def create_circuits_database() -> None:
    """Create European circuits database."""
    GEO_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(SAMPLE_CIRCUITS)
    output_file = GEO_DIR / "circuits_europe.csv"
    df.to_csv(output_file, index=False)
    print(f"Created {output_file} with {len(SAMPLE_CIRCUITS)} circuits")


def main() -> None:
    """Main entry point."""
    print("Creating sample F1 data for testing...")
    print("=" * 50)

    create_sample_calendars()
    create_circuits_database()

    print("=" * 50)
    print("Sample data created successfully!")


if __name__ == "__main__":
    main()
