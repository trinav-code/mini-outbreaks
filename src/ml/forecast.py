"""
Forecasting module for Mini Outbreak Detector
Uses Prophet for time series forecasting
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
import logging

# Prophet import with error handling
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logging.warning("Prophet not installed. Install with: pip install prophet")

from src.config.settings import (
    FORECAST_HORIZON,
    FORECAST_INTERVAL_WIDTH,
    PROPHET_SEASONALITY_MODE,
    PROPHET_CHANGEPOINT_PRIOR_SCALE,
    PROPHET_SEASONALITY_PRIOR_SCALE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Forecaster:
    """Forecast future disease cases using Prophet"""

    def __init__(
        self,
        horizon: int = FORECAST_HORIZON,
        interval_width: float = FORECAST_INTERVAL_WIDTH
    ):
        self.horizon = horizon
        self.interval_width = interval_width

        if not PROPHET_AVAILABLE:
            raise ImportError(
                "Prophet is required for forecasting. "
                "Install with: pip install prophet"
            )

    def forecast_prophet(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate forecast using Facebook Prophet

        Args:
            df: DataFrame with datetime index and 'cases' column

        Returns:
            DataFrame with forecast
        """
        # Prepare data for Prophet (needs 'ds' and 'y' columns)
        prophet_df = df.reset_index()[["date", "cases"]]
        prophet_df.columns = ["ds", "y"]

        # Ensure non-negative values
        prophet_df["y"] = prophet_df["y"].clip(lower=0)

        # Initialize Prophet model
        # Suppress cmdstanpy logs
        import warnings
        warnings.filterwarnings("ignore")

        model = Prophet(
            interval_width=self.interval_width,
            seasonality_mode=PROPHET_SEASONALITY_MODE,
            changepoint_prior_scale=PROPHET_CHANGEPOINT_PRIOR_SCALE,
            seasonality_prior_scale=PROPHET_SEASONALITY_PRIOR_SCALE,
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality="auto"
        )

        # Fit model
        logger.info("Training Prophet model...")
        model.fit(prophet_df)

        # Create future dataframe
        future = model.make_future_dataframe(periods=self.horizon)

        # Generate forecast
        logger.info(f"Generating {self.horizon}-day forecast...")
        forecast = model.predict(future)

        # Extract only future predictions
        forecast = forecast.tail(self.horizon)

        # Ensure non-negative predictions
        forecast["yhat"] = forecast["yhat"].clip(lower=0)
        forecast["yhat_lower"] = forecast["yhat_lower"].clip(lower=0)
        forecast["yhat_upper"] = forecast["yhat_upper"].clip(lower=0)

        logger.info("Forecast complete")
        return forecast

    def forecast_simple_moving_average(
        self,
        df: pd.DataFrame,
        window: int = 7
    ) -> pd.DataFrame:
        """
        Simple moving average forecast (fallback method)

        Args:
            df: DataFrame with 'cases' column
            window: Moving average window

        Returns:
            DataFrame with forecast
        """
        # Calculate moving average of last N days
        recent_avg = df["cases"].tail(window).mean()

        # Create future dates
        last_date = df.index.max()
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=self.horizon,
            freq="D"
        )

        # Create forecast dataframe
        forecast = pd.DataFrame({
            "ds": future_dates,
            "yhat": recent_avg,
            "yhat_lower": recent_avg * 0.8,
            "yhat_upper": recent_avg * 1.2
        })

        return forecast

    def generate_forecast(
        self,
        df: pd.DataFrame,
        method: str = "prophet"
    ) -> pd.DataFrame:
        """
        Generate forecast using specified method

        Args:
            df: Preprocessed DataFrame
            method: "prophet" or "simple"

        Returns:
            Forecast DataFrame
        """
        if method == "prophet":
            try:
                return self.forecast_prophet(df)
            except Exception as e:
                logger.warning(f"Prophet failed: {e}. Falling back to simple method.")
                return self.forecast_simple_moving_average(df)
        elif method == "simple":
            return self.forecast_simple_moving_average(df)
        else:
            raise ValueError(f"Unknown forecast method: {method}")

    def get_forecast_records(self, forecast_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Convert forecast to JSON-serializable records

        Args:
            forecast_df: Forecast DataFrame from Prophet

        Returns:
            List of forecast records
        """
        records = []

        for _, row in forecast_df.iterrows():
            record = {
                "date": row["ds"].strftime("%Y-%m-%d"),
                "forecast": float(row["yhat"]),
                "lower_bound": float(row["yhat_lower"]),
                "upper_bound": float(row["yhat_upper"])
            }
            records.append(record)

        return records

    def get_forecast_stats(self, forecast_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute forecast statistics

        Args:
            forecast_df: Forecast DataFrame

        Returns:
            Dictionary with forecast statistics
        """
        stats = {
            "forecast_horizon_days": self.horizon,
            "mean_forecast": float(forecast_df["yhat"].mean()),
            "max_forecast": float(forecast_df["yhat"].max()),
            "min_forecast": float(forecast_df["yhat"].min()),
            "trend": self._determine_forecast_trend(forecast_df["yhat"]),
        }

        return stats

    def _determine_forecast_trend(self, forecast_values: pd.Series) -> str:
        """
        Determine forecast trend

        Args:
            forecast_values: Series of forecast values

        Returns:
            Trend description
        """
        # Compare first and last values
        first_week = forecast_values.head(7).mean()
        last_week = forecast_values.tail(7).mean()

        change_rate = (last_week - first_week) / (first_week + 1e-6)

        if change_rate > 0.1:
            return "increasing"
        elif change_rate < -0.1:
            return "decreasing"
        else:
            return "stable"
