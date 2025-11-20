"""
Data loading module for Mini Outbreak Detector
Supports loading from CSV files and OWID API
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List
import logging

from src.config.settings import RAW_DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load disease case data from various sources"""

    def __init__(self, data_dir: Path = RAW_DATA_DIR):
        self.data_dir = data_dir

    def load_from_csv(
        self,
        filename: str,
        date_col: str = "date",
        cases_col: str = "new_cases",
        country_col: str = "location",
        disease_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load data from a CSV file

        Args:
            filename: Name of CSV file in data/raw/
            date_col: Name of date column
            cases_col: Name of new cases column
            country_col: Name of country/location column
            disease_col: Name of disease column (optional)

        Returns:
            DataFrame with standardized columns
        """
        filepath = self.data_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")

        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} rows from {filename}")

            # Standardize column names
            rename_map = {
                date_col: "date",
                cases_col: "cases",
                country_col: "country"
            }

            if disease_col:
                rename_map[disease_col] = "disease"

            df = df.rename(columns=rename_map)

            # Convert date to datetime
            df["date"] = pd.to_datetime(df["date"])

            # Ensure cases is numeric
            df["cases"] = pd.to_numeric(df["cases"], errors="coerce")

            return df

        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise

    def load_owid_covid(self) -> pd.DataFrame:
        """
        Load COVID-19 data from Our World in Data

        Returns:
            DataFrame with COVID-19 cases
        """
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

        try:
            logger.info("Fetching COVID-19 data from OWID...")
            df = pd.read_csv(url)

            # Standardize columns
            df = df.rename(columns={
                "date": "date",
                "new_cases": "cases",
                "location": "country"
            })

            # Add disease column
            df["disease"] = "COVID-19"

            # Filter relevant columns
            df = df[["date", "country", "cases", "disease"]]

            # Convert date
            df["date"] = pd.to_datetime(df["date"])

            # Ensure cases is numeric
            df["cases"] = pd.to_numeric(df["cases"], errors="coerce")

            logger.info(f"Loaded {len(df)} rows from OWID")
            return df

        except Exception as e:
            logger.error(f"Error loading OWID data: {e}")
            raise

    def filter_data(
        self,
        df: pd.DataFrame,
        country: str,
        disease: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Filter data by country, disease, and date range

        Args:
            df: Input DataFrame
            country: Country name
            disease: Disease name (optional)
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            Filtered DataFrame
        """
        filtered = df.copy()

        # Filter by country
        filtered = filtered[filtered["country"] == country]

        if filtered.empty:
            raise ValueError(f"No data found for country: {country}")

        # Filter by disease if specified
        if disease and "disease" in filtered.columns:
            filtered = filtered[filtered["disease"] == disease]

            if filtered.empty:
                raise ValueError(f"No data found for disease: {disease}")

        # Filter by date range
        if start_date:
            filtered = filtered[filtered["date"] >= pd.to_datetime(start_date)]

        if end_date:
            filtered = filtered[filtered["date"] <= pd.to_datetime(end_date)]

        # Sort by date
        filtered = filtered.sort_values("date").reset_index(drop=True)

        logger.info(f"Filtered to {len(filtered)} rows for {country}")
        return filtered

    def get_available_countries(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of available countries in dataset

        Args:
            df: Input DataFrame

        Returns:
            Sorted list of country names
        """
        if "country" not in df.columns:
            return []

        countries = df["country"].dropna().unique().tolist()
        return sorted(countries)

    def get_available_diseases(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of available diseases in dataset

        Args:
            df: Input DataFrame

        Returns:
            Sorted list of disease names
        """
        if "disease" not in df.columns:
            return []

        diseases = df["disease"].dropna().unique().tolist()
        return sorted(diseases)
