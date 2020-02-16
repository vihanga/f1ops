"""Data loading utilities for F1Ops."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

from f1ops.config import CALENDARS_DIR, EUROPEAN_COUNTRIES, GEO_DIR
from f1ops.data_models import Circuit, RaceEvent


def load_circuits() -> pd.DataFrame:
    """
    Load circuit data from CSV.

    Returns:
        DataFrame with circuit information
    """
    circuits_file = GEO_DIR / "circuits_europe.csv"
    if not circuits_file.exists():
        raise FileNotFoundError(f"Circuits file not found: {circuits_file}")

    df = pd.read_csv(circuits_file)
    required_cols = ["name", "city", "country", "latitude", "longitude"]

    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Circuits CSV must contain columns: {required_cols}")

    return df


def load_calendar(season: int) -> pd.DataFrame:
    """
    Load calendar data for a specific season.

    Args:
        season: Year of the F1 season

    Returns:
        DataFrame with race calendar
    """
    calendar_file = CALENDARS_DIR / f"f1_calendar_{season}.csv"
    if not calendar_file.exists():
        raise FileNotFoundError(f"Calendar file not found: {calendar_file}")

    df = pd.read_csv(calendar_file)
    df["race_date"] = pd.to_datetime(df["race_date"])

    required_cols = ["round", "race_name", "circuit_name", "race_date", "latitude", "longitude"]

    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Calendar CSV must contain columns: {required_cols}")

    return df


def get_european_races(season: int, countries: Optional[List[str]] = None) -> List[RaceEvent]:
    """
    Get European races for a season.

    Args:
        season: Year of the F1 season
        countries: List of European countries to include (default: config.EUROPEAN_COUNTRIES)

    Returns:
        List of RaceEvent objects for European races
    """
    if countries is None:
        countries = EUROPEAN_COUNTRIES

    df = load_calendar(season)

    # Filter European races
    df_europe = df[df["country"].isin(countries)].copy()
    df_europe = df_europe.sort_values("round").reset_index(drop=True)

    races = []
    for _, row in df_europe.iterrows():
        circuit = Circuit(
            name=row["circuit_name"],
            city=row["city"],
            country=row["country"],
            latitude=row["latitude"],
            longitude=row["longitude"],
        )

        race = RaceEvent(
            season=season,
            round=int(row["round"]),
            race_name=row["race_name"],
            circuit=circuit,
            race_date=row["race_date"].date(),
        )
        races.append(race)

    return races


def get_available_seasons() -> List[int]:
    """
    Get list of seasons with available calendar data.

    Returns:
        Sorted list of available season years
    """
    if not CALENDARS_DIR.exists():
        return []

    seasons = []
    for file in CALENDARS_DIR.glob("f1_calendar_*.csv"):
        try:
            year = int(file.stem.split("_")[-1])
            seasons.append(year)
        except ValueError:
            continue

    return sorted(seasons)


def validate_calendar_file(file_path: Path) -> bool:
    """
    Validate calendar CSV file format.

    Args:
        file_path: Path to calendar CSV file

    Returns:
        True if valid, False otherwise
    """
    try:
        df = pd.read_csv(file_path)
        required_cols = [
            "round",
            "race_name",
            "circuit_name",
            "city",
            "country",
            "race_date",
            "latitude",
            "longitude",
        ]

        if not all(col in df.columns for col in required_cols):
            return False

        # Try parsing dates
        pd.to_datetime(df["race_date"])

        # Validate coordinates
        if not (df["latitude"].between(-90, 90).all()):
            return False
        if not (df["longitude"].between(-180, 180).all()):
            return False

        return True
    except Exception:
        return False
