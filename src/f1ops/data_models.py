"""Pydantic data models for F1Ops."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Circuit(BaseModel):
    """Represents an F1 circuit with geographic coordinates."""

    name: str
    city: str
    country: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @validator("latitude", "longitude")
    def validate_coordinates(cls, v: float) -> float:
        """Validate coordinate values."""
        if not isinstance(v, (int, float)):
            raise ValueError("Coordinates must be numeric")
        return float(v)


class RaceEvent(BaseModel):
    """Represents a race event in the F1 calendar."""

    season: int = Field(..., ge=1950, le=2100)
    round: int = Field(..., ge=1)
    race_name: str
    circuit: Circuit
    race_date: date

    @validator("season")
    def validate_season(cls, v: int) -> int:
        """Validate season year."""
        if v < 1950:
            raise ValueError("F1 seasons start from 1950")
        return v


class Leg(BaseModel):
    """Represents a travel leg between two circuits."""

    from_circuit: Circuit
    to_circuit: Circuit
    distance_km: float = Field(..., ge=0)
    method: str = "haversine"  # or "osrm"

    @property
    def leg_name(self) -> str:
        """Generate a human-readable leg name."""
        return f"{self.from_circuit.city} → {self.to_circuit.city}"


class CostBreakdown(BaseModel):
    """Cost breakdown for a travel leg or season."""

    fuel_cost_eur: float = Field(default=0.0, ge=0)
    labor_cost_eur: float = Field(default=0.0, ge=0)
    toll_cost_eur: float = Field(default=0.0, ge=0)
    fixed_cost_eur: float = Field(default=0.0, ge=0)

    @property
    def total_cost_eur(self) -> float:
        """Calculate total cost."""
        return (
            self.fuel_cost_eur
            + self.labor_cost_eur
            + self.toll_cost_eur
            + self.fixed_cost_eur
        )


class EmissionsBreakdown(BaseModel):
    """Emissions breakdown for a travel leg or season."""

    road_co2e_kg: float = Field(default=0.0, ge=0)
    air_co2e_kg: float = Field(default=0.0, ge=0)

    @property
    def total_co2e_kg(self) -> float:
        """Calculate total emissions."""
        return self.road_co2e_kg + self.air_co2e_kg

    @property
    def total_co2e_tonnes(self) -> float:
        """Calculate total emissions in tonnes."""
        return self.total_co2e_kg / 1000.0


class LegAnalysis(BaseModel):
    """Complete analysis for a single leg."""

    leg: Leg
    cost: CostBreakdown
    emissions: EmissionsBreakdown
    travel_hours: float = Field(..., ge=0)
    num_trucks: int = Field(default=8, ge=1)


class SeasonAnalysis(BaseModel):
    """Complete analysis for an entire season."""

    season: int
    legs: List[LegAnalysis]
    total_distance_km: float
    total_cost: CostBreakdown
    total_emissions: EmissionsBreakdown
    total_travel_hours: float

    @property
    def num_legs(self) -> int:
        """Return number of legs."""
        return len(self.legs)

    @property
    def avg_leg_distance_km(self) -> float:
        """Calculate average leg distance."""
        return self.total_distance_km / max(self.num_legs, 1)


class TeamProfile(BaseModel):
    """Team freight and personnel profile."""

    team_name: str = "Generic Team"
    total_freight_tonnes: float = Field(default=120.0, ge=0)
    num_personnel: int = Field(default=60, ge=1)
    garage_equipment_tonnes: float = Field(default=40.0, ge=0)
    spare_parts_tonnes: float = Field(default=30.0, ge=0)
    hospitality_tonnes: float = Field(default=50.0, ge=0)


class OptimizationResult(BaseModel):
    """Result from route optimization."""

    original_cost_eur: float
    optimized_cost_eur: float
    savings_eur: float
    savings_percent: float
    method: str = "greedy"
    parameters: dict = Field(default_factory=dict)

    @property
    def is_improved(self) -> bool:
        """Check if optimization improved the result."""
        return self.savings_eur > 0
