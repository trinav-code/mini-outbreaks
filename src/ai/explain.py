"""
AI Explanation module for Mini Outbreak Detector
Generates human-readable explanations of analysis results
This is a placeholder - will be enhanced with LLM integration later
"""

from typing import Dict, Any, List
import logging

from src.config.settings import RISK_THRESHOLDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplanationGenerator:
    """Generate AI explanations for outbreak analysis"""

    def __init__(self):
        self.risk_thresholds = RISK_THRESHOLDS

    def generate_explanation(
        self,
        country: str,
        disease: str,
        summary_stats: Dict[str, Any],
        anomaly_stats: Dict[str, Any],
        forecast_stats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive explanation of analysis

        Args:
            country: Country name
            disease: Disease name
            summary_stats: Summary statistics
            anomaly_stats: Anomaly detection statistics
            forecast_stats: Forecast statistics

        Returns:
            Dictionary with explanation components
        """
        # Determine risk level
        risk_level = self._determine_risk_level(
            anomaly_stats.get("anomaly_rate", 0),
            forecast_stats.get("trend", "stable")
        )

        # Generate summary
        summary = self._generate_summary(
            country,
            disease,
            summary_stats,
            anomaly_stats,
            forecast_stats,
            risk_level
        )

        # Generate detailed explanation
        explanation = self._generate_detailed_explanation(
            summary_stats,
            anomaly_stats,
            forecast_stats,
            risk_level
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_level,
            anomaly_stats,
            forecast_stats
        )

        result = {
            "summary": summary,
            "risk_level": risk_level,
            "explanation": explanation,
            "recommendations": recommendations,
            "confidence": self._calculate_confidence(summary_stats, anomaly_stats)
        }

        logger.info(f"Generated explanation with risk level: {risk_level}")
        return result

    def _determine_risk_level(
        self,
        anomaly_rate: float,
        forecast_trend: str
    ) -> str:
        """
        Determine risk level based on anomaly rate and forecast

        Args:
            anomaly_rate: Proportion of anomalous data points
            forecast_trend: Forecast trend direction

        Returns:
            Risk level: "low", "medium", or "high"
        """
        # Base risk on anomaly rate
        if anomaly_rate > self.risk_thresholds["high"]:
            base_risk = "high"
        elif anomaly_rate > self.risk_thresholds["medium"]:
            base_risk = "medium"
        else:
            base_risk = "low"

        # Elevate risk if forecast is increasing
        if forecast_trend == "increasing" and base_risk == "low":
            return "medium"
        elif forecast_trend == "increasing" and base_risk == "medium":
            return "high"

        return base_risk

    def _generate_summary(
        self,
        country: str,
        disease: str,
        summary_stats: Dict[str, Any],
        anomaly_stats: Dict[str, Any],
        forecast_stats: Dict[str, Any],
        risk_level: str
    ) -> str:
        """Generate concise summary"""
        trend = summary_stats.get("trend", "stable")
        total_cases = summary_stats.get("total_cases", 0)
        n_anomalies = anomaly_stats.get("total_anomalies", 0)
        forecast_trend = forecast_stats.get("trend", "stable")

        summary = (
            f"Analysis of {disease} in {country}: "
            f"Total of {total_cases:,} cases detected. "
            f"The current trend is {trend}. "
        )

        if n_anomalies > 0:
            summary += f"Identified {n_anomalies} anomalous outbreak periods. "

        summary += f"Forecast indicates {forecast_trend} trend over next 14 days. "
        summary += f"Overall risk level: {risk_level.upper()}."

        return summary

    def _generate_detailed_explanation(
        self,
        summary_stats: Dict[str, Any],
        anomaly_stats: Dict[str, Any],
        forecast_stats: Dict[str, Any],
        risk_level: str
    ) -> str:
        """Generate detailed explanation"""
        explanations = []

        # Data overview
        data_points = summary_stats.get("data_points", 0)
        date_range = summary_stats.get("date_range", {})
        explanations.append(
            f"The analysis covers {data_points} days of data "
            f"from {date_range.get('start', 'N/A')} to {date_range.get('end', 'N/A')}."
        )

        # Case statistics
        mean_cases = summary_stats.get("mean_daily_cases", 0)
        max_cases = summary_stats.get("max_daily_cases", 0)
        explanations.append(
            f"Average daily cases: {mean_cases:.1f}. "
            f"Peak daily cases: {max_cases:,}."
        )

        # Anomaly analysis
        anomaly_rate = anomaly_stats.get("anomaly_rate", 0) * 100
        if anomaly_rate > 0:
            explanations.append(
                f"Anomaly detection identified unusual patterns in {anomaly_rate:.1f}% "
                f"of the data using both Z-score and Isolation Forest methods."
            )
        else:
            explanations.append("No significant anomalies detected in the time series.")

        # Forecast analysis
        mean_forecast = forecast_stats.get("mean_forecast", 0)
        forecast_trend = forecast_stats.get("trend", "stable")
        explanations.append(
            f"The 14-day forecast predicts an average of {mean_forecast:.1f} daily cases, "
            f"indicating a {forecast_trend} trajectory."
        )

        # Risk interpretation
        if risk_level == "high":
            explanations.append(
                "HIGH RISK: Multiple outbreak signals detected. "
                "Enhanced monitoring and intervention measures recommended."
            )
        elif risk_level == "medium":
            explanations.append(
                "MEDIUM RISK: Some concerning patterns identified. "
                "Continued surveillance advised."
            )
        else:
            explanations.append(
                "LOW RISK: Situation appears stable with no major outbreak indicators."
            )

        return " ".join(explanations)

    def _generate_recommendations(
        self,
        risk_level: str,
        anomaly_stats: Dict[str, Any],
        forecast_stats: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if risk_level == "high":
            recommendations.extend([
                "Activate emergency response protocols",
                "Increase testing and surveillance capacity",
                "Prepare healthcare facilities for surge capacity",
                "Enhance public communication and awareness campaigns",
                "Consider targeted intervention measures"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "Maintain heightened surveillance",
                "Monitor key indicators daily",
                "Ensure adequate healthcare resources",
                "Prepare contingency plans"
            ])
        else:
            recommendations.extend([
                "Continue routine monitoring",
                "Maintain preventive measures",
                "Update response plans as needed"
            ])

        # Add specific recommendations based on forecast
        forecast_trend = forecast_stats.get("trend", "stable")
        if forecast_trend == "increasing":
            recommendations.append("Trend analysis suggests potential increase - prepare accordingly")

        return recommendations

    def _calculate_confidence(
        self,
        summary_stats: Dict[str, Any],
        anomaly_stats: Dict[str, Any]
    ) -> str:
        """
        Calculate confidence level in analysis

        Args:
            summary_stats: Summary statistics
            anomaly_stats: Anomaly statistics

        Returns:
            Confidence level: "low", "medium", or "high"
        """
        data_points = summary_stats.get("data_points", 0)

        # More data points = higher confidence
        if data_points >= 90:  # 3+ months
            return "high"
        elif data_points >= 30:  # 1+ month
            return "medium"
        else:
            return "low"

    def generate_simple_explanation(self, text: str) -> Dict[str, Any]:
        """
        Generate simple explanation (placeholder for LLM integration)

        Args:
            text: Input text to explain

        Returns:
            Simple explanation dictionary
        """
        return {
            "summary": text,
            "risk_level": "unknown",
            "explanation": "Detailed analysis pending.",
            "recommendations": ["Continue monitoring"],
            "confidence": "medium"
        }
