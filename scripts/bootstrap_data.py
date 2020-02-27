#!/usr/bin/env python3
"""Bootstrap F1 calendar data from Ergast API and create circuit database."""

import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from f1ops.config import CALENDARS_DIR, EUROPEAN_COUNTRIES, GEO_DIR

ERGAST_API_BASE = "https://ergast.com/api/f1"


def fetch_season_calendar(year: int) -> List[Dict]:
    """
    Fetch F1 calendar for a specific season from Ergast API.

    Args:
        year: Season year

    Returns:
        List of race dictionaries
    """
    url = f"{ERGAST_API_BASE}/{year}.json"
    print(f"Fetching {year} calendar from Ergast API...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        races_data = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        print(f"  Found {len(races_data)} races")

        races = []
        for race in races_data:
            circuit = race.get("Circuit", {})
            location = circuit.get("Location", {})

            races.append(
                {
                    "round": int(race.get("round", 0)),
                    "race_name": race.get("raceName", "Unknown"),
                    "circuit_name": circuit.get("circuitName", "Unknown"),
                    "city": location.get("locality", "Unknown"),
                    "country": location.get("country", "Unknown"),
                    "race_date": race.get("date", "1900-01-01"),
                    "latitude": float(location.get("lat", 0.0)),
                    "longitude": float(location.get("long", 0.0)),
                }
            )

        return races
    except Exception as e:
        print(f"  Error fetching {year}: {e}")
        return []


def save_calendar(year: int, races: List[Dict]) -> None:
    """Save calendar data to CSV."""
    if not races:
        print(f"  No data to save for {year}")
        return

    df = pd.DataFrame(races)
    output_file = CALENDARS_DIR / f"f1_calendar_{year}.csv"
    df.to_csv(output_file, index=False)
    print(f"  Saved to {output_file}")


def create_circuits_database(years: List[int]) -> None:
    """
    Create a consolidated circuits database from all calendars.

    Args:
        years: List of years to process
    """
    all_circuits = {}

    for year in years:
        calendar_file = CALENDARS_DIR / f"f1_calendar_{year}.csv"
        if not calendar_file.exists():
            continue

        df = pd.read_csv(calendar_file)
        for _, row in df.iterrows():
            circuit_key = row["circuit_name"]
            if circuit_key not in all_circuits:
                all_circuits[circuit_key] = {
                    "name": row["circuit_name"],
                    "city": row["city"],
                    "country": row["country"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                }

    # Filter European circuits
    european_circuits = [
        c for c in all_circuits.values() if c["country"] in EUROPEAN_COUNTRIES
    ]

    df_circuits = pd.DataFrame(european_circuits)
    output_file = GEO_DIR / "circuits_europe.csv"
    df_circuits.to_csv(output_file, index=False)
    print(f"\nCreated European circuits database with {len(european_circuits)} circuits")
    print(f"  Saved to {output_file}")


def bootstrap_all_seasons(start_year: int = 2010, end_year: int = 2019) -> None:
    """
    Bootstrap calendar data for all seasons.

    Args:
        start_year: First season
        end_year: Last season (inclusive)
    """
    print("F1Ops Data Bootstrap")
    print("=" * 50)
    print(f"Fetching data for seasons {start_year}-{end_year}\n")

    # Ensure directories exist
    CALENDARS_DIR.mkdir(parents=True, exist_ok=True)
    GEO_DIR.mkdir(parents=True, exist_ok=True)

    years = list(range(start_year, end_year + 1))

    # Fetch and save each season
    for year in years:
        races = fetch_season_calendar(year)
        if races:
            save_calendar(year, races)

    # Create circuits database
    create_circuits_database(years)

    print("\n" + "=" * 50)
    print("Bootstrap complete!")
    print(f"Generated {len(years)} calendar files")
    print(f"Data directory: {CALENDARS_DIR}")


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Bootstrap F1 calendar data")
    parser.add_argument(
        "--start-year", type=int, default=2010, help="First season year (default: 2010)"
    )
    parser.add_argument(
        "--end-year", type=int, default=2019, help="Last season year (default: 2019)"
    )
    args = parser.parse_args()

    bootstrap_all_seasons(start_year=args.start_year, end_year=args.end_year)


if __name__ == "__main__":
    main()
