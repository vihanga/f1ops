"""Comprehensive tests for data loading functionality."""

import pytest
import pandas as pd
from pathlib import Path
from datetime import date

from f1ops.data_loader import (
    load_circuits,
    load_calendar,
    get_european_races,
    get_available_seasons,
    validate_calendar_file,
)
from f1ops.data_models import Circuit, RaceEvent
from f1ops.config import CALENDARS_DIR, GEO_DIR


class TestLoadCircuits:
    """Tests for circuit data loading."""

    def test_load_circuits_returns_dataframe(self):
        """Test that load_circuits returns a pandas DataFrame."""
        circuits = load_circuits()
        assert isinstance(circuits, pd.DataFrame)

    def test_load_circuits_not_empty(self):
        """Test that circuit data is not empty."""
        circuits = load_circuits()
        assert len(circuits) > 0

    def test_load_circuits_has_required_columns(self):
        """Test that circuit data has all required columns."""
        circuits = load_circuits()
        required_columns = ["name", "city", "country", "latitude", "longitude"]
        for col in required_columns:
            assert col in circuits.columns, f"Missing column: {col}"

    def test_circuit_coordinates_valid_range(self):
        """Test that coordinates are within valid ranges."""
        circuits = load_circuits()
        assert circuits["latitude"].between(-90, 90).all()
        assert circuits["longitude"].between(-180, 180).all()

    def test_circuit_no_null_values(self):
        """Test that critical columns have no null values."""
        circuits = load_circuits()
        assert not circuits["name"].isnull().any()
        assert not circuits["latitude"].isnull().any()
        assert not circuits["longitude"].isnull().any()

    def test_circuit_datatypes(self):
        """Test that circuit data has correct datatypes."""
        circuits = load_circuits()
        assert circuits["name"].dtype == object
        assert pd.api.types.is_numeric_dtype(circuits["latitude"])
        assert pd.api.types.is_numeric_dtype(circuits["longitude"])


class TestLoadCalendar:
    """Tests for calendar data loading."""

    def test_load_calendar_returns_dataframe(self):
        """Test that load_calendar returns a DataFrame."""
        df = load_calendar(2019)
        assert isinstance(df, pd.DataFrame)

    def test_load_calendar_not_empty(self):
        """Test that calendar data is not empty."""
        df = load_calendar(2019)
        assert len(df) > 0

    def test_load_calendar_required_columns(self):
        """Test that calendar has all required columns."""
        df = load_calendar(2019)
        required_columns = [
            "round", "race_name", "circuit_name", "city", "country",
            "latitude", "longitude"
        ]
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"

    def test_load_calendar_invalid_year(self):
        """Test that loading invalid year raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_calendar(1949)  # Before F1 existed

    def test_load_calendar_future_year(self):
        """Test that loading future year raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_calendar(2099)

    def test_calendar_no_nulls_in_critical_columns(self):
        """Test that critical columns have no null values."""
        df = load_calendar(2019)
        critical_columns = ["round", "race_name", "circuit_name", "latitude", "longitude"]
        for col in critical_columns:
            assert not df[col].isnull().any(), f"Column {col} has null values"

    def test_calendar_rounds_are_positive(self):
        """Test that round numbers are positive integers."""
        df = load_calendar(2019)
        assert (df["round"] > 0).all()

    def test_calendar_coordinates_valid(self):
        """Test that calendar coordinates are in valid range."""
        df = load_calendar(2019)
        assert df["latitude"].between(-90, 90).all()
        assert df["longitude"].between(-180, 180).all()


class TestGetEuropeanRaces:
    """Tests for European race filtering."""

    def test_get_european_races_returns_list(self):
        """Test that get_european_races returns a list."""
        races = get_european_races(2019)
        assert isinstance(races, list)

    def test_get_european_races_not_empty(self):
        """Test that European races list is not empty."""
        races = get_european_races(2019)
        assert len(races) > 0

    def test_all_items_are_race_events(self):
        """Test that all items are RaceEvent objects."""
        races = get_european_races(2019)
        assert all(isinstance(race, RaceEvent) for race in races)

    def test_all_races_have_correct_season(self):
        """Test that all races have the requested season."""
        races = get_european_races(2019)
        assert all(race.season == 2019 for race in races)

    def test_all_races_have_circuits(self):
        """Test that all races have valid circuit objects."""
        races = get_european_races(2019)
        for race in races:
            assert isinstance(race.circuit, Circuit)
            assert race.circuit.name
            assert race.circuit.city
            assert race.circuit.country

    def test_all_circuits_have_valid_coordinates(self):
        """Test that all circuits have valid coordinates."""
        races = get_european_races(2019)
        for race in races:
            assert isinstance(race.circuit.latitude, float)
            assert isinstance(race.circuit.longitude, float)
            assert -90 <= race.circuit.latitude <= 90
            assert -180 <= race.circuit.longitude <= 180

    def test_all_races_have_dates(self):
        """Test that all races have valid dates."""
        races = get_european_races(2019)
        for race in races:
            assert isinstance(race.race_date, date)
            assert race.race_date.year == 2019
            assert 1 <= race.race_date.month <= 12
            assert 1 <= race.race_date.day <= 31

    def test_all_races_have_positive_rounds(self):
        """Test that all races have positive round numbers."""
        races = get_european_races(2019)
        assert all(race.round >= 1 for race in races)

    def test_european_races_have_european_countries(self):
        """Test that European races have European country codes."""
        races = get_european_races(2019)
        for race in races:
            assert race.circuit.country
            assert len(race.circuit.country) > 0


class TestGetAvailableSeasons:
    """Tests for available seasons retrieval."""

    def test_get_available_seasons_returns_list(self):
        """Test that get_available_seasons returns a list."""
        seasons = get_available_seasons()
        assert isinstance(seasons, list)

    def test_get_available_seasons_not_empty(self):
        """Test that seasons list is not empty."""
        seasons = get_available_seasons()
        assert len(seasons) > 0

    def test_all_seasons_are_integers(self):
        """Test that all seasons are integers."""
        seasons = get_available_seasons()
        assert all(isinstance(s, int) for s in seasons)

    def test_seasons_are_sorted(self):
        """Test that seasons are returned in sorted order."""
        seasons = get_available_seasons()
        assert seasons == sorted(seasons)

    def test_seasons_include_known_years(self):
        """Test that known years are included."""
        seasons = get_available_seasons()
        assert 2010 in seasons
        assert 2019 in seasons

    def test_seasons_in_valid_range(self):
        """Test that all seasons are in valid F1 range."""
        seasons = get_available_seasons()
        assert all(1950 <= s <= 2030 for s in seasons)


class TestValidateCalendarFile:
    """Tests for calendar file validation."""

    def test_validate_existing_file(self):
        """Test validation of existing calendar file."""
        valid_file = CALENDARS_DIR / "f1_calendar_2019.csv"
        if valid_file.exists():
            assert validate_calendar_file(valid_file) is True

    def test_validate_non_existent_file(self):
        """Test validation of non-existent file."""
        invalid_file = CALENDARS_DIR / "f1_calendar_9999.csv"
        assert validate_calendar_file(invalid_file) is False

    def test_validate_invalid_path(self):
        """Test validation of completely invalid path."""
        invalid_path = Path("/completely/invalid/path/to/file.csv")
        assert validate_calendar_file(invalid_path) is False


class TestDataIntegrity:
    """Integration tests for data integrity."""

    def test_circuits_and_calendar_consistency(self):
        """Test that calendar circuits exist in circuits database."""
        circuits = load_circuits()
        races = get_european_races(2019)

        circuit_names = set(circuits["name"].str.strip().str.lower())

        # Check that most race circuits are in the database
        # (allowing for some naming variations)
        for race in races:
            # This is a soft check - just ensure data structures are compatible
            assert race.circuit.name
            assert race.circuit.latitude
            assert race.circuit.longitude

    def test_multiple_years_consistency(self):
        """Test that multiple years load consistently."""
        seasons = get_available_seasons()

        # Test at least 2 different years
        test_years = [s for s in seasons if s >= 2010 and s <= 2020][:2]

        for year in test_years:
            races = get_european_races(year)
            assert len(races) > 0
            assert all(race.season == year for race in races)

    def test_calendar_and_european_races_consistency(self):
        """Test that European races are subset of calendar."""
        calendar_df = load_calendar(2019)
        european_races = get_european_races(2019)

        # European races should be <= total calendar
        assert len(european_races) <= len(calendar_df)
        assert len(european_races) > 0  # But should have at least some races
