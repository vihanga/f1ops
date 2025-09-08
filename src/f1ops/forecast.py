"""Time series forecasting module for F1 logistics cost prediction.

This module uses Facebook Prophet for forecasting logistics costs,
travel times, and seasonal patterns in F1 team operations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    from prophet import Prophet
    from prophet.plot import plot_plotly, plot_components_plotly
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    Prophet = None

from f1ops.config import DATA_DIR, ARTIFACTS_DIR
from f1ops.cost import calculate_leg_cost, CostBreakdown
from f1ops.data_models import Leg


class LogisticsCostForecaster:
    """Forecast F1 logistics costs using Facebook Prophet."""

    def __init__(self, seasonality_mode: str = 'additive', changepoint_prior_scale: float = 0.05):
        """
        Initialize forecaster.

        Args:
            seasonality_mode: 'additive' or 'multiplicative'
            changepoint_prior_scale: Controls flexibility of trend (0.001-0.5)
        """
        if not PROPHET_AVAILABLE:
            raise ImportError(
                "Prophet is not installed. Install with: pip install prophet"
            )

        self.model = Prophet(
            seasonality_mode=seasonality_mode,
            changepoint_prior_scale=changepoint_prior_scale,
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
        )

        # Add custom seasonalities for F1 calendar
        self.model.add_seasonality(
            name='race_season',
            period=365.25,
            fourier_order=10,
            mode='additive'
        )

        self.fitted = False
        self.forecast_df: Optional[pd.DataFrame] = None

    def prepare_data(
        self,
        historical_legs: List[Tuple[str, Leg, Dict[str, float]]],
    ) -> pd.DataFrame:
        """
        Prepare historical data for Prophet.

        Args:
            historical_legs: List of (date_str, Leg, cost_params) tuples

        Returns:
            DataFrame with 'ds' (date) and 'y' (cost) columns
        """
        records = []

        for date_str, leg, cost_params in historical_legs:
            num_trucks = int(cost_params.get('num_trucks', 8))
            cost = calculate_leg_cost(leg, num_trucks, cost_params)

            records.append({
                'ds': pd.to_datetime(date_str),
                'y': cost.total_cost_eur,
                'distance_km': leg.distance_km,
                'leg_name': leg.leg_name,
            })

        df = pd.DataFrame(records)
        return df[['ds', 'y']]  # Prophet requires exactly these columns

    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit the Prophet model.

        Args:
            df: DataFrame with 'ds' and 'y' columns
        """
        # Add distance as a regressor if available
        if 'distance_km' in df.columns:
            self.model.add_regressor('distance_km', standardize=True)

        self.model.fit(df)
        self.fitted = True

    def predict(self, periods: int = 365, freq: str = 'D') -> pd.DataFrame:
        """
        Generate forecast.

        Args:
            periods: Number of periods to forecast
            freq: Frequency ('D' for daily, 'W' for weekly, 'M' for monthly)

        Returns:
            DataFrame with forecast including uncertainty intervals
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction")

        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        forecast = self.model.predict(future)

        self.forecast_df = forecast
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend']]

    def get_race_season_forecast(self, year: int) -> pd.DataFrame:
        """
        Get cost forecast for a specific F1 season.

        Args:
            year: Year to forecast (e.g., 2025)

        Returns:
            DataFrame with race season dates and forecasted costs
        """
        if self.forecast_df is None:
            raise ValueError("Must call predict() before get_race_season_forecast()")

        # F1 season typically runs March-November
        season_start = pd.to_datetime(f'{year}-03-01')
        season_end = pd.to_datetime(f'{year}-11-30')

        season_forecast = self.forecast_df[
            (self.forecast_df['ds'] >= season_start) &
            (self.forecast_df['ds'] <= season_end)
        ].copy()

        return season_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    def get_trend_analysis(self) -> Dict[str, float]:
        """
        Analyze cost trends.

        Returns:
            Dictionary with trend statistics
        """
        if self.forecast_df is None:
            raise ValueError("Must call predict() first")

        trend = self.forecast_df['trend'].values
        yhat = self.forecast_df['yhat'].values

        return {
            'overall_trend_slope': float(np.polyfit(range(len(trend)), trend, 1)[0]),
            'average_cost': float(yhat.mean()),
            'cost_std': float(yhat.std()),
            'min_forecast': float(yhat.min()),
            'max_forecast': float(yhat.max()),
        }

    def save_model(self, filepath: Optional[Path] = None) -> Path:
        """
        Save Prophet model to disk.

        Args:
            filepath: Path to save model (default: artifacts/prophet_model.json)

        Returns:
            Path where model was saved
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before saving")

        if filepath is None:
            filepath = ARTIFACTS_DIR / "forecast_model.json"

        from prophet.serialize import model_to_json

        with open(filepath, 'w') as f:
            f.write(model_to_json(self.model))

        return filepath

    @classmethod
    def load_model(cls, filepath: Path) -> 'LogisticsCostForecaster':
        """
        Load Prophet model from disk.

        Args:
            filepath: Path to saved model

        Returns:
            Loaded forecaster instance
        """
        from prophet.serialize import model_from_json

        with open(filepath, 'r') as f:
            model = model_from_json(f.read())

        forecaster = cls()
        forecaster.model = model
        forecaster.fitted = True

        return forecaster


def create_synthetic_historical_data(
    legs: List[Leg],
    start_year: int = 2020,
    end_year: int = 2024,
    cost_params: Dict[str, float] = None,
) -> List[Tuple[str, Leg, Dict[str, float]]]:
    """
    Create synthetic historical data for demonstration.

    Args:
        legs: List of race legs
        start_year: Start year for synthetic data
        end_year: End year for synthetic data
        cost_params: Cost parameters to use

    Returns:
        List of (date_str, Leg, cost_params) tuples
    """
    from f1ops.config import DEFAULT_COST_PARAMS

    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS.copy()

    historical_data = []

    for year in range(start_year, end_year + 1):
        # Assume races happen monthly from March to November
        for month in range(3, 12):
            for leg in legs[:2]:  # Use first 2 legs as representative
                date_str = f"{year}-{month:02d}-15"

                # Add some noise to simulate real variation
                noisy_params = cost_params.copy()
                noisy_params['fuel_price_eur_per_l'] *= (1 + np.random.normal(0, 0.1))

                historical_data.append((date_str, leg, noisy_params))

    return historical_data


def forecast_season_costs(
    historical_legs: List[Tuple[str, Leg, Dict[str, float]]],
    forecast_year: int = 2026,
    save_artifacts: bool = True,
) -> Tuple[pd.DataFrame, LogisticsCostForecaster]:
    """
    End-to-end forecasting workflow.

    Args:
        historical_legs: Historical data
        forecast_year: Year to forecast
        save_artifacts: Whether to save model and plots

    Returns:
        Tuple of (forecast DataFrame, fitted forecaster)
    """
    # Initialize and fit model
    forecaster = LogisticsCostForecaster()

    # Prepare data
    df = forecaster.prepare_data(historical_legs)

    # Fit model
    forecaster.fit(df)

    # Generate forecast
    forecaster.predict(periods=365 * 2)  # 2 years ahead

    # Get specific season forecast
    season_forecast = forecaster.get_race_season_forecast(forecast_year)

    # Get trend analysis
    trends = forecaster.get_trend_analysis()

    print(f"\n=== Cost Forecast for {forecast_year} F1 Season ===")
    print(f"Average forecasted cost: €{season_forecast['yhat'].mean():,.2f}")
    print(f"Cost range: €{season_forecast['yhat'].min():,.2f} - €{season_forecast['yhat'].max():,.2f}")
    print(f"\nTrend Analysis:")
    print(f"  Overall trend slope: €{trends['overall_trend_slope']:.2f}/day")
    print(f"  Average cost: €{trends['average_cost']:,.2f}")
    print(f"  Cost std dev: €{trends['cost_std']:,.2f}")

    # Save artifacts
    if save_artifacts:
        model_path = forecaster.save_model()
        print(f"\nModel saved to: {model_path}")

        forecast_csv = ARTIFACTS_DIR / f"cost_forecast_{forecast_year}.csv"
        season_forecast.to_csv(forecast_csv, index=False)
        print(f"Forecast saved to: {forecast_csv}")

    return season_forecast, forecaster
