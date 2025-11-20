# Mini Outbreak Detector

A lightweight ML-powered backend system for detecting infectious disease outbreaks through anomaly detection and time series forecasting.

## Overview

Mini Outbreak Detector analyzes disease case data to:
- Detect outbreak anomalies using multiple ML methods
- Forecast future case trends
- Generate AI-powered explanations and risk assessments
- Provide clean REST API endpoints for frontend integration

## Features

- **Dual Anomaly Detection**: Combines Z-score and Isolation Forest methods
- **Time Series Forecasting**: 14-day forecasts using Facebook Prophet
- **Automated Data Processing**: Cleaning, resampling, and feature engineering
- **AI Explanations**: Risk level assessment with actionable recommendations
- **REST API**: FastAPI-based endpoints with automatic documentation
- **Flexible Data Sources**: Support for OWID COVID data and custom CSV files

## Architecture

```
User → Frontend → API → ML Engine → Explanation Layer → API → Frontend
```

### Components

- **Data Module**: Loading and preprocessing
- **ML Module**: Anomaly detection and forecasting
- **AI Module**: Explanation generation
- **API Module**: FastAPI endpoints

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd mini-outbreak-detector
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

Note: Prophet may require additional system dependencies. See [Prophet installation guide](https://facebook.github.io/prophet/docs/installation.html) if you encounter issues.

## Quick Start

### Run the API Server

```bash
python -m src.api.server
```

Or with uvicorn directly:
```bash
uvicorn src.api.server:app --reload
```

The API will be available at:
- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Test the API

**Get list of diseases:**
```bash
curl http://localhost:8000/api/diseases
```

**Get available countries:**
```bash
curl http://localhost:8000/api/countries
```

**Analyze disease data:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "country": "India",
    "disease": "COVID-19",
    "data_source": "owid"
  }'
```

## API Endpoints

### GET `/api/diseases`
Returns list of supported diseases.

**Response:**
```json
["COVID-19", "Influenza", "Measles", "Dengue", "Malaria", "Tuberculosis"]
```

### GET `/api/countries`
Returns list of available countries from data source.

**Query Parameters:**
- `data_source` (optional): "owid" or "csv" (default: "owid")

### POST `/api/analyze`
Performs complete outbreak analysis.

**Request Body:**
```json
{
  "country": "India",
  "disease": "COVID-19",
  "data_source": "owid"
}
```

**Response:**
```json
{
  "country": "India",
  "disease": "COVID-19",
  "cleaned_data": [...],
  "anomalies": [...],
  "forecast": [...],
  "summary_stats": {...},
  "anomaly_stats": {...},
  "forecast_stats": {...},
  "ai_explanation": {...}
}
```

## Project Structure

```
mini-outbreak-detector/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/              # Raw data files
│   └── processed/        # Processed data cache
│
├── src/
│   ├── api/
│   │   ├── server.py     # FastAPI application
│   │   └── routes.py     # API endpoints
│   │
│   ├── data/
│   │   ├── loader.py     # Data loading
│   │   └── preprocess.py # Data cleaning & features
│   │
│   ├── ml/
│   │   ├── anomalies.py  # Anomaly detection
│   │   ├── forecast.py   # Time series forecasting
│   │   └── utils.py      # ML utilities
│   │
│   ├── ai/
│   │   └── explain.py    # AI explanations
│   │
│   └── config/
│       └── settings.py   # Configuration
│
└── notebooks/
    └── exploration.ipynb # Data exploration
```

## ML Pipeline

### 1. Data Preprocessing
- Continuous daily time series creation
- Missing value interpolation
- Rolling statistics (7-day window):
  - Mean
  - Standard deviation
  - Linear regression slope

### 2. Anomaly Detection

**Z-Score Method:**
```
z = (cases - rolling_mean) / rolling_std
anomaly if |z| > 2.5
```

**Isolation Forest:**
- Features: [cases, rolling_mean, rolling_std, rolling_slope]
- Contamination: 10%
- Ensemble: 100 trees

**Combined Decision:**
Mark as anomaly if EITHER method flags it.

### 3. Forecasting
- **Model**: Facebook Prophet
- **Horizon**: 14 days
- **Confidence**: 95% interval
- **Features**:
  - Weekly seasonality
  - Automatic yearly seasonality detection
  - Multiplicative seasonality mode

### 4. AI Explanation
- Risk level: Low / Medium / High
- Based on anomaly rate and forecast trend
- Actionable recommendations
- Confidence assessment

## Configuration

Edit `src/config/settings.py` to customize:

```python
# Anomaly detection
Z_SCORE_THRESHOLD = 2.5
ISOLATION_FOREST_CONTAMINATION = 0.1

# Preprocessing
ROLLING_WINDOW = 7
MIN_DATA_POINTS = 30

# Forecasting
FORECAST_HORIZON = 14
FORECAST_INTERVAL_WIDTH = 0.95
```

## Using Custom Data

### CSV Format
Place CSV files in `data/raw/` with these columns:
- `date`: Date (YYYY-MM-DD)
- `new_cases`: Daily case count
- `location`: Country/region name
- `disease`: Disease name (optional)

### API Call
```json
{
  "country": "YourCountry",
  "disease": "YourDisease",
  "data_source": "csv",
  "csv_filename": "your_data.csv"
}
```

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests (to be implemented)
pytest tests/
```

### Jupyter Notebooks
```bash
jupyter notebook notebooks/exploration.ipynb
```

## Error Handling

The API provides friendly error messages:

- **400**: Invalid input or insufficient data
- **404**: Data file not found
- **500**: Server error (check logs)

All errors return JSON:
```json
{
  "error": "Description of error",
  "detail": "Additional details"
}
```

## Performance

- Typical analysis time: 5-15 seconds
- Depends on:
  - Data size
  - Prophet model fitting
  - Isolation Forest training

## Future Enhancements

- [ ] LLM integration for enhanced explanations
- [ ] Support for ARIMA forecasting
- [ ] Multi-country comparative analysis
- [ ] Real-time data streaming
- [ ] Caching and optimization
- [ ] Authentication and rate limiting
- [ ] Frontend dashboard

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`

## Acknowledgments

- Data: [Our World in Data](https://ourworldindata.org/)
- Forecasting: [Facebook Prophet](https://facebook.github.io/prophet/)
- Framework: [FastAPI](https://fastapi.tiangolo.com/)

---

Built with Python, FastAPI, Prophet, and scikit-learn.
