import { AnalysisResult } from "@/types";

export const COUNTRIES = [
  "India",
  "United States",
  "United Kingdom",
  "Canada",
  "Brazil",
  "Germany",
  "France",
  "Italy",
  "Spain",
  "Australia",
];

export const DISEASES = [
  "COVID-19",
  "Influenza",
  "Measles",
  "Dengue",
  "Malaria",
  "Tuberculosis",
];

// Generate sample time series data
function generateDateRange(days: number): string[] {
  const dates: string[] = [];
  const startDate = new Date("2024-08-01");

  for (let i = 0; i < days; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    dates.push(date.toISOString().split("T")[0]);
  }

  return dates;
}

export const SAMPLE_ANALYSIS: AnalysisResult = {
  country: "Canada",
  disease: "Tuberculosis",
  cleaned_data: generateDateRange(90).map((date, i) => {
    // Create realistic pattern with anomalies
    let cases = 1000 + i * 2 + Math.random() * 100;

    // Add anomalies at specific points
    if (i === 25 || i === 52 || i === 77) {
      cases *= 2;
    }

    return {
      date,
      cases: Math.round(cases),
      rolling_mean: Math.round(1000 + i * 2),
      rolling_std: 50,
    };
  }),
  anomalies: [
    {
      date: "2024-08-26",
      cases: 2100,
      rolling_mean: 1050,
      z_score: 3.2,
      anomaly_score: -0.15,
      detected_by: ["z-score", "isolation-forest"],
    },
    {
      date: "2024-09-22",
      cases: 2200,
      rolling_mean: 1104,
      z_score: 3.5,
      anomaly_score: -0.18,
      detected_by: ["z-score", "isolation-forest"],
    },
    {
      date: "2024-10-18",
      cases: 2150,
      rolling_mean: 1154,
      z_score: 3.1,
      anomaly_score: -0.16,
      detected_by: ["z-score", "isolation-forest"],
    },
  ],
  forecast: generateDateRange(14).map((_, i) => {
    const startForecast = 1350;
    return {
      date: new Date(
        new Date("2024-10-30").getTime() + i * 24 * 60 * 60 * 1000
      )
        .toISOString()
        .split("T")[0],
      forecast: startForecast + i * 3,
      lower_bound: startForecast + i * 3 - 50,
      upper_bound: startForecast + i * 3 + 50,
    };
  }),
  summary_stats: {
    total_cases: 103450,
    mean_daily_cases: 1149.4,
    max_daily_cases: 2200,
    min_daily_cases: 1000,
    std_daily_cases: 125.3,
    data_points: 90,
    date_range: {
      start: "2024-08-01",
      end: "2024-10-29",
    },
    trend: "increasing",
  },
  anomaly_stats: {
    total_anomalies: 3,
    anomaly_rate: 0.033,
    z_score_detections: 3,
    isolation_forest_detections: 3,
    average_anomaly_magnitude: 2150,
  },
  forecast_stats: {
    forecast_horizon_days: 14,
    mean_forecast: 1369,
    max_forecast: 1389,
    min_forecast: 1350,
    trend: "increasing",
  },
  ai_explanation: {
    summary:
      "Analysis of Tuberculosis in Canada: Total of 103,450 cases detected. The current trend is increasing. Identified 3 anomalous outbreak periods. Forecast indicates increasing trend over next 14 days. Overall risk level: MEDIUM.",
    risk_level: "medium",
    explanation:
      "Based on the analysis of Tuberculosis cases in Canada, the data shows an upward trend with three significant anomalies detected over the past 90 days. These spikes occurred on August 26, September 22, and October 18, indicating potential localized outbreak events or reporting irregularities. The forecast model predicts continued growth in cases over the next two weeks, suggesting enhanced surveillance and preparedness measures may be warranted. The anomaly detection algorithm uses statistical methods to identify data points that deviate significantly from expected patterns.",
    recommendations: [
      "Maintain heightened surveillance",
      "Monitor key indicators daily",
      "Ensure adequate healthcare resources",
      "Prepare contingency plans",
      "Trend analysis suggests potential increase - prepare accordingly",
    ],
    confidence: "high",
  },
};
