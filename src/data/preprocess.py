"""
Data preprocessing module for Mini Outbreak Detector
Handles cleaning, resampling, and feature engineering
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

from src.config.settings import (
    ROLLING_WINDOW,
    MIN_DATA_POINTS,
    INTERPOLATION_METHOD
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess time series data for anomaly detection and forecasting"""

    def __init__(self, rolling_window: int = ROLLING_WINDOW):
        self.rolling_window = rolling_window

    def clean_and_resample(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean data and ensure continuous daily time series

        Args:
            df: DataFrame with 'date' and 'cases' columns

        Returns:
            Cleaned DataFrame with continuous daily index
        """
        if len(df) < MIN_DATA_POINTS:
            raise ValueError(
                f"Insufficient data: {len(df)} rows. "
                f"Minimum required: {MIN_DATA_POINTS}"
            )

        # Create a copy
        cleaned = df.copy()

        # Ensure date is datetime and set as index
        cleaned["date"] = pd.to_datetime(cleaned["date"])
        cleaned = cleaned.set_index("date")

        # Sort by date
        cleaned = cleaned.sort_index()

        # Remove duplicates (keep last)
        cleaned = cleaned[~cleaned.index.duplicated(keep="last")]

        # Create continuous daily range
        date_range = pd.date_range(
            start=cleaned.index.min(),
            end=cleaned.index.max(),
            freq="D"
        )

        # Reindex to fill missing dates
        cleaned = cleaned.reindex(date_range)

        # Fill missing cases with interpolation
        cleaned["cases"] = cleaned["cases"].interpolate(
            method=INTERPOLATION_METHOD,
            limit_direction="both"
        )

        # Fill any remaining NaNs with 0
        cleaned["cases"] = cleaned["cases"].fillna(0)

        # Ensure non-negative values
        cleaned["cases"] = cleaned["cases"].clip(lower=0)

        logger.info(
            f"Cleaned data: {len(cleaned)} days, "
            f"range: {cleaned.index.min()} to {cleaned.index.max()}"
        )

        return cleaned

    def compute_rolling_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute rolling statistics for anomaly detection

        Args:
            df: DataFrame with 'cases' column

        Returns:
            DataFrame with additional rolling statistics columns
        """
        enriched = df.copy()

        # Rolling mean
        enriched["rolling_mean"] = (
            enriched["cases"]
            .rolling(window=self.rolling_window, min_periods=1, center=False)
            .mean()
        )

        # Rolling standard deviation
        enriched["rolling_std"] = (
            enriched["cases"]
            .rolling(window=self.rolling_window, min_periods=1, center=False)
            .std()
        )

        # Handle zero std (replace with small value to avoid division by zero)
        enriched["rolling_std"] = enriched["rolling_std"].replace(0, 1e-6)
        enriched["rolling_std"] = enriched["rolling_std"].fillna(1e-6)

        # Rolling slope (linear regression slope)
        enriched["rolling_slope"] = self._compute_rolling_slope(
            enriched["cases"],
            window=self.rolling_window
        )

        logger.info("Computed rolling statistics")
        return enriched

    def _compute_rolling_slope(
        self,
        series: pd.Series,
        window: int
    ) -> pd.Series:
        """
        Compute rolling linear regression slope

        Args:
            series: Time series data
            window: Window size

        Returns:
            Series with rolling slopes
        """
        def calculate_slope(y_values):
            """Calculate slope for a window"""
            if len(y_values) < 2:
                return 0

            x = np.arange(len(y_values))
            y = np.array(y_values)

            # Remove NaN values
            mask = ~np.isnan(y)
            if mask.sum() < 2:
                return 0

            x = x[mask]
            y = y[mask]

            # Linear regression slope: (n*Σxy - Σx*Σy) / (n*Σx² - (Σx)²)
            n = len(x)
            slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / \
                    (n * np.sum(x ** 2) - np.sum(x) ** 2 + 1e-6)

            return slope

        slopes = series.rolling(window=window, min_periods=2).apply(
            calculate_slope,
            raw=True
        )

        return slopes.fillna(0)

    def prepare_for_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Full preprocessing pipeline

        Args:
            df: Raw DataFrame

        Returns:
            Preprocessed DataFrame ready for analysis
        """
        # Clean and resample
        cleaned = self.clean_and_resample(df)

        # Compute rolling statistics
        enriched = self.compute_rolling_stats(cleaned)

        return enriched

    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute summary statistics

        Args:
            df: Preprocessed DataFrame

        Returns:
            Dictionary with summary statistics
        """
        stats = {
            "total_cases": int(df["cases"].sum()),
            "mean_daily_cases": float(df["cases"].mean()),
            "max_daily_cases": int(df["cases"].max()),
            "min_daily_cases": int(df["cases"].min()),
            "std_daily_cases": float(df["cases"].std()),
            "data_points": len(df),
            "date_range": {
                "start": df.index.min().strftime("%Y-%m-%d"),
                "end": df.index.max().strftime("%Y-%m-%d"),
            },
            "trend": self._determine_trend(df["rolling_slope"]),
        }

        return stats

    def _determine_trend(self, slopes: pd.Series) -> str:
        """
        Determine overall trend from slopes

        Args:
            slopes: Rolling slope series

        Returns:
            Trend description: "increasing", "decreasing", or "stable"
        """
        recent_slope = slopes.tail(14).mean()  # Last 2 weeks

        if recent_slope > 0.5:
            return "increasing"
        elif recent_slope < -0.5:
            return "decreasing"
        else:
            return "stable"

    def to_json_records(self, df: pd.DataFrame) -> list:
        """
        Convert DataFrame to JSON-serializable records

        Args:
            df: DataFrame with datetime index

        Returns:
            List of dictionaries
        """
        df_reset = df.reset_index()
        df_reset["date"] = df_reset["date"].dt.strftime("%Y-%m-%d")

        records = df_reset.to_dict(orient="records")
        return records
