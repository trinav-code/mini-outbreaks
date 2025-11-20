"""
Configuration settings for Mini Outbreak Detector
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

# Data Processing
ROLLING_WINDOW = 7  # Days for rolling statistics
MIN_DATA_POINTS = 30  # Minimum data points required for analysis
INTERPOLATION_METHOD = "linear"

# Anomaly Detection - Z-Score
Z_SCORE_THRESHOLD = 2.5  # Standard deviations from mean

# Anomaly Detection - Isolation Forest
ISOLATION_FOREST_CONTAMINATION = 0.1  # Expected proportion of outliers
ISOLATION_FOREST_RANDOM_STATE = 42
ISOLATION_FOREST_N_ESTIMATORS = 100

# Forecasting
FORECAST_HORIZON = 14  # Days to forecast
FORECAST_INTERVAL_WIDTH = 0.95  # Confidence interval (95%)

# Prophet Settings
PROPHET_SEASONALITY_MODE = "multiplicative"
PROPHET_CHANGEPOINT_PRIOR_SCALE = 0.05
PROPHET_SEASONALITY_PRIOR_SCALE = 10.0

# Supported diseases (static for now)
SUPPORTED_DISEASES = [
    "COVID-19",
    "Influenza",
    "Measles",
    "Dengue",
    "Malaria",
    "Tuberculosis",
]

# Risk level thresholds
RISK_THRESHOLDS = {
    "low": 0.1,      # < 10% anomaly rate
    "medium": 0.2,   # 10-20% anomaly rate
    "high": 0.2,     # > 20% anomaly rate
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
