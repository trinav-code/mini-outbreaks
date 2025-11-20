// Analysis Request & Response Types

export interface AnalyzeRequest {
  country: string;
  disease: string;
  data_source?: string;
  csv_filename?: string;
}

export interface DataPoint {
  date: string;
  cases: number;
  rolling_mean?: number;
  rolling_std?: number;
}

export interface Anomaly {
  date: string;
  cases: number;
  rolling_mean: number;
  z_score: number;
  anomaly_score: number;
  detected_by: string[];
}

export interface ForecastPoint {
  date: string;
  forecast: number;
  lower_bound: number;
  upper_bound: number;
}

export interface SummaryStats {
  total_cases: number;
  mean_daily_cases: number;
  max_daily_cases: number;
  min_daily_cases: number;
  std_daily_cases: number;
  data_points: number;
  date_range: {
    start: string;
    end: string;
  };
  trend: "increasing" | "decreasing" | "stable";
}

export interface AnomalyStats {
  total_anomalies: number;
  anomaly_rate: number;
  z_score_detections: number;
  isolation_forest_detections: number;
  average_anomaly_magnitude: number;
}

export interface ForecastStats {
  forecast_horizon_days: number;
  mean_forecast: number;
  max_forecast: number;
  min_forecast: number;
  trend: "increasing" | "decreasing" | "stable";
}

export interface AIExplanation {
  summary: string;
  risk_level: "low" | "medium" | "high";
  explanation: string;
  recommendations: string[];
  confidence: "low" | "medium" | "high";
}

export interface AnalysisResult {
  country: string;
  disease: string;
  cleaned_data: DataPoint[];
  anomalies: Anomaly[];
  forecast: ForecastPoint[];
  summary_stats: SummaryStats;
  anomaly_stats: AnomalyStats;
  forecast_stats: ForecastStats;
  ai_explanation: AIExplanation;
}
