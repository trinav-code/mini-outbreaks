"""
Utility functions for ML pipeline
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that DataFrame has required columns

    Args:
        df: DataFrame to validate
        required_columns: List of required column names

    Returns:
        True if valid

    Raises:
        ValueError if validation fails
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return True


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers

    Args:
        numerator: Top value
        denominator: Bottom value
        default: Value to return if division fails

    Returns:
        Result of division or default
    """
    try:
        if denominator == 0 or np.isnan(denominator):
            return default
        result = numerator / denominator
        return result if not np.isnan(result) else default
    except:
        return default


def clip_negative_values(series: pd.Series) -> pd.Series:
    """
    Clip negative values to zero

    Args:
        series: Pandas Series

    Returns:
        Series with non-negative values
    """
    return series.clip(lower=0)


def format_large_number(num: float) -> str:
    """
    Format large numbers for display

    Args:
        num: Number to format

    Returns:
        Formatted string
    """
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values

    Args:
        old_value: Original value
        new_value: New value

    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0

    return ((new_value - old_value) / old_value) * 100


def get_date_range_days(start_date: pd.Timestamp, end_date: pd.Timestamp) -> int:
    """
    Get number of days between two dates

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        Number of days
    """
    return (end_date - start_date).days


def smooth_series(series: pd.Series, window: int = 7) -> pd.Series:
    """
    Smooth a time series using moving average

    Args:
        series: Time series data
        window: Window size for moving average

    Returns:
        Smoothed series
    """
    return series.rolling(window=window, min_periods=1, center=True).mean()


def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using IQR method

    Args:
        series: Data series
        multiplier: IQR multiplier (default 1.5)

    Returns:
        Boolean series indicating outliers
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    return (series < lower_bound) | (series > upper_bound)


def fill_missing_dates(
    df: pd.DataFrame,
    date_col: str = "date",
    freq: str = "D"
) -> pd.DataFrame:
    """
    Fill missing dates in time series

    Args:
        df: DataFrame with date column
        date_col: Name of date column
        freq: Frequency ('D' for daily)

    Returns:
        DataFrame with continuous dates
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)

    # Create complete date range
    date_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq=freq
    )

    # Reindex
    df = df.reindex(date_range)

    return df.reset_index()


def calculate_growth_rate(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    Calculate growth rate

    Args:
        series: Time series data
        periods: Number of periods for growth calculation

    Returns:
        Series with growth rates
    """
    return series.pct_change(periods=periods) * 100


def exponential_smoothing(
    series: pd.Series,
    alpha: float = 0.3
) -> pd.Series:
    """
    Apply exponential smoothing

    Args:
        series: Time series data
        alpha: Smoothing factor (0-1)

    Returns:
        Smoothed series
    """
    return series.ewm(alpha=alpha, adjust=False).mean()


def ensure_json_serializable(obj: Any) -> Any:
    """
    Convert object to JSON-serializable format

    Args:
        obj: Object to convert

    Returns:
        JSON-serializable object
    """
    if isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, dict):
        return {k: ensure_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ensure_json_serializable(item) for item in obj]
    else:
        return obj
