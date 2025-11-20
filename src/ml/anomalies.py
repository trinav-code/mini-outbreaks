"""
Anomaly detection module for Mini Outbreak Detector
Implements Z-score and Isolation Forest methods
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any
import logging

from src.config.settings import (
    Z_SCORE_THRESHOLD,
    ISOLATION_FOREST_CONTAMINATION,
    ISOLATION_FOREST_RANDOM_STATE,
    ISOLATION_FOREST_N_ESTIMATORS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect anomalies in disease time series using multiple methods"""

    def __init__(
        self,
        z_threshold: float = Z_SCORE_THRESHOLD,
        contamination: float = ISOLATION_FOREST_CONTAMINATION,
        random_state: int = ISOLATION_FOREST_RANDOM_STATE
    ):
        self.z_threshold = z_threshold
        self.contamination = contamination
        self.random_state = random_state

    def detect_z_score_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies using rolling Z-score method

        Args:
            df: DataFrame with 'cases', 'rolling_mean', 'rolling_std'

        Returns:
            DataFrame with 'z_score' and 'z_anomaly' columns
        """
        result = df.copy()

        # Calculate Z-score
        result["z_score"] = (
            (result["cases"] - result["rolling_mean"]) / result["rolling_std"]
        )

        # Flag anomalies
        result["z_anomaly"] = np.abs(result["z_score"]) > self.z_threshold

        n_anomalies = result["z_anomaly"].sum()
        logger.info(f"Z-score method detected {n_anomalies} anomalies")

        return result

    def detect_isolation_forest_anomalies(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Detect anomalies using Isolation Forest

        Args:
            df: DataFrame with feature columns

        Returns:
            DataFrame with 'if_score' and 'if_anomaly' columns
        """
        result = df.copy()

        # Prepare features
        feature_cols = ["cases", "rolling_mean", "rolling_std", "rolling_slope"]

        # Check if all features are available
        missing = [col for col in feature_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        X = result[feature_cols].values

        # Handle any remaining NaN values
        X = np.nan_to_num(X, nan=0.0)

        # Train Isolation Forest
        iso_forest = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=ISOLATION_FOREST_N_ESTIMATORS,
            max_samples="auto",
            n_jobs=-1
        )

        # Predict (-1 for anomalies, 1 for normal)
        predictions = iso_forest.fit_predict(X)

        # Get anomaly scores (more negative = more anomalous)
        scores = iso_forest.score_samples(X)

        result["if_score"] = scores
        result["if_anomaly"] = predictions == -1

        n_anomalies = result["if_anomaly"].sum()
        logger.info(f"Isolation Forest detected {n_anomalies} anomalies")

        return result

    def combine_anomaly_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Combine Z-score and Isolation Forest signals

        Args:
            df: DataFrame with 'z_anomaly' and 'if_anomaly'

        Returns:
            DataFrame with combined 'is_anomaly' column
        """
        result = df.copy()

        # Mark as anomaly if EITHER method flags it
        result["is_anomaly"] = result["z_anomaly"] | result["if_anomaly"]

        n_anomalies = result["is_anomaly"].sum()
        logger.info(f"Combined detection: {n_anomalies} total anomalies")

        return result

    def detect_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run full anomaly detection pipeline

        Args:
            df: Preprocessed DataFrame

        Returns:
            DataFrame with all anomaly detection results
        """
        logger.info("Running anomaly detection...")

        # Z-score detection
        result = self.detect_z_score_anomalies(df)

        # Isolation Forest detection
        result = self.detect_isolation_forest_anomalies(result)

        # Combine signals
        result = self.combine_anomaly_signals(result)

        return result

    def get_anomaly_records(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Extract anomaly records for API response

        Args:
            df: DataFrame with anomaly detection results

        Returns:
            List of anomaly records
        """
        anomalies = df[df["is_anomaly"]].copy()

        if len(anomalies) == 0:
            return []

        # Reset index to get date as column
        anomalies = anomalies.reset_index()

        records = []
        for _, row in anomalies.iterrows():
            record = {
                "date": row["date"].strftime("%Y-%m-%d"),
                "cases": int(row["cases"]),
                "rolling_mean": float(row["rolling_mean"]),
                "z_score": float(row["z_score"]),
                "anomaly_score": float(row["if_score"]),
                "detected_by": self._get_detection_methods(row)
            }
            records.append(record)

        return records

    def _get_detection_methods(self, row: pd.Series) -> List[str]:
        """
        Get which methods detected this anomaly

        Args:
            row: DataFrame row

        Returns:
            List of method names
        """
        methods = []

        if row["z_anomaly"]:
            methods.append("z-score")

        if row["if_anomaly"]:
            methods.append("isolation-forest")

        return methods

    def get_anomaly_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute anomaly statistics

        Args:
            df: DataFrame with anomaly detection results

        Returns:
            Dictionary with anomaly statistics
        """
        total_points = len(df)
        n_anomalies = df["is_anomaly"].sum()
        anomaly_rate = n_anomalies / total_points if total_points > 0 else 0

        stats = {
            "total_anomalies": int(n_anomalies),
            "anomaly_rate": float(anomaly_rate),
            "z_score_detections": int(df["z_anomaly"].sum()),
            "isolation_forest_detections": int(df["if_anomaly"].sum()),
            "average_anomaly_magnitude": float(
                df[df["is_anomaly"]]["cases"].mean()
                if n_anomalies > 0
                else 0
            ),
        }

        return stats
