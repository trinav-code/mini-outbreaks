"""
API routes for Mini Outbreak Detector
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

from src.data.loader import DataLoader
from src.data.preprocess import DataPreprocessor
from src.ml.anomalies import AnomalyDetector
from src.ml.forecast import Forecaster
from src.ai.explain import ExplanationGenerator
from src.config.settings import SUPPORTED_DISEASES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Initialize components
data_loader = DataLoader()
preprocessor = DataPreprocessor()
anomaly_detector = AnomalyDetector()
forecaster = Forecaster()
explainer = ExplanationGenerator()


# Pydantic models for request/response validation
class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint"""
    country: str = Field(..., description="Country name", example="India")
    disease: str = Field(..., description="Disease name", example="COVID-19")
    data_source: Optional[str] = Field("owid", description="Data source: 'owid' or 'csv'")
    csv_filename: Optional[str] = Field(None, description="CSV filename if using csv source")


class AnalyzeResponse(BaseModel):
    """Response model for analysis endpoint"""
    country: str
    disease: str
    cleaned_data: List[Dict[str, Any]]
    anomalies: List[Dict[str, Any]]
    forecast: List[Dict[str, Any]]
    summary_stats: Dict[str, Any]
    anomaly_stats: Dict[str, Any]
    forecast_stats: Dict[str, Any]
    ai_explanation: Dict[str, Any]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None


# Routes

@router.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Mini Outbreak Detector API",
        "version": "1.0.0",
        "endpoints": [
            "/api/diseases",
            "/api/countries",
            "/api/analyze"
        ]
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@router.get("/api/diseases", response_model=List[str])
async def get_diseases():
    """
    Get list of supported diseases

    Returns:
        List of disease names
    """
    try:
        return SUPPORTED_DISEASES
    except Exception as e:
        logger.error(f"Error in get_diseases: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/countries", response_model=List[str])
async def get_countries(data_source: str = "owid"):
    """
    Get list of available countries from data source

    Args:
        data_source: Data source ('owid' or 'csv')

    Returns:
        List of country names
    """
    try:
        if data_source == "owid":
            # Load OWID data
            df = data_loader.load_owid_covid()
            countries = data_loader.get_available_countries(df)
            return countries
        else:
            return ["India", "United States", "United Kingdom", "Brazil", "Germany"]

    except Exception as e:
        logger.error(f"Error in get_countries: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load countries: {str(e)}"
        )


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze disease data for a country

    Performs:
    1. Data loading and cleaning
    2. Anomaly detection
    3. Forecasting
    4. AI explanation generation

    Returns:
        Complete analysis results
    """
    try:
        logger.info(f"Analyzing {request.disease} in {request.country}")

        # Step 1: Load data
        if request.data_source == "owid":
            df = data_loader.load_owid_covid()
        elif request.data_source == "csv" and request.csv_filename:
            df = data_loader.load_from_csv(request.csv_filename)
        else:
            raise ValueError("Invalid data source or missing CSV filename")

        # Filter for country and disease
        df_filtered = data_loader.filter_data(
            df,
            country=request.country,
            disease=request.disease
        )

        # Step 2: Preprocess
        df_processed = preprocessor.prepare_for_analysis(df_filtered)

        # Check for sufficient data
        if len(df_processed) < 30:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data for {request.country}. Minimum 30 days required."
            )

        # Step 3: Detect anomalies
        df_with_anomalies = anomaly_detector.detect_all(df_processed)

        # Step 4: Generate forecast
        forecast_df = forecaster.generate_forecast(df_processed, method="prophet")

        # Step 5: Compute statistics
        summary_stats = preprocessor.get_summary_stats(df_processed)
        anomaly_stats = anomaly_detector.get_anomaly_stats(df_with_anomalies)
        forecast_stats = forecaster.get_forecast_stats(forecast_df)

        # Step 6: Generate AI explanation
        ai_explanation = explainer.generate_explanation(
            country=request.country,
            disease=request.disease,
            summary_stats=summary_stats,
            anomaly_stats=anomaly_stats,
            forecast_stats=forecast_stats
        )

        # Step 7: Prepare response data
        cleaned_data = preprocessor.to_json_records(
            df_processed[["cases", "rolling_mean", "rolling_std"]]
        )

        anomalies = anomaly_detector.get_anomaly_records(df_with_anomalies)

        forecast = forecaster.get_forecast_records(forecast_df)

        # Build response
        response = AnalyzeResponse(
            country=request.country,
            disease=request.disease,
            cleaned_data=cleaned_data,
            anomalies=anomalies,
            forecast=forecast,
            summary_stats=summary_stats,
            anomaly_stats=anomaly_stats,
            forecast_stats=forecast_stats,
            ai_explanation=ai_explanation
        )

        logger.info(f"Analysis complete for {request.country}")
        return response

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error in analyze: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
