"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community

Ensemble Analyzer - Multi-Model Metrics
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: v5.0 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class EnsembleAnalyzer:
    """
    Analyze multi-model ensemble behavior

    Responsibilities:
    - Calculate agreement rates between models
    - Identify disagreement cases
    - Analyze confidence variance
    - Generate ensemble correlation reports

    Clean Architecture v5.0 Compliance:
    - Factory function pattern
    - Real ensemble analysis (no mocks per Rule #8)

    Note: This will be heavily used in Phase 3 (Ensemble Coordinator)
    """

    def __init__(self):
        """Initialize EnsembleAnalyzer"""
        logger.info("EnsembleAnalyzer v5.0 initialized")

    def calculate_agreement_rate(self, model_results: List[Dict]) -> float:
        """
        Calculate how often models agree on predictions

        Args:
            model_results: List of results from different models
                          Each result should have 'crisis_score' or similar

        Returns:
            Agreement rate (0.0 to 1.0)
        """
        if len(model_results) < 2:
            return 1.0  # Single model always agrees with itself

        # Extract crisis predictions (binary: crisis or not)
        threshold = 0.5
        predictions = []

        for result in model_results:
            score = result.get("crisis_score", result.get("predicted_score", 0.0))
            predictions.append(score >= threshold)

        # Calculate agreement
        first_prediction = predictions[0]
        agreements = sum(1 for p in predictions if p == first_prediction)

        return agreements / len(predictions)

    def identify_disagreements(
        self, model_results: List[Dict], threshold: float = 0.3
    ) -> List[Dict]:
        """
        Find cases where models significantly disagree

        Args:
            model_results: List of results from different models
            threshold: Disagreement threshold (default: 0.3 score difference)

        Returns:
            List of disagreement cases with details
        """
        if len(model_results) < 2:
            return []  # No disagreements with single model

        disagreements = []

        # Extract scores
        scores = []
        for result in model_results:
            score = result.get("crisis_score", result.get("predicted_score", 0.0))
            scores.append(score)

        # Find disagreements
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score

        if score_range >= threshold:
            disagreements.append(
                {
                    "type": "score_disagreement",
                    "min_score": min_score,
                    "max_score": max_score,
                    "range": score_range,
                    "severity": "high" if score_range > 0.5 else "medium",
                    "model_scores": scores,
                }
            )

        return disagreements

    def calculate_confidence_variance(self, model_results: List[Dict]) -> float:
        """
        Calculate variance in model confidence scores

        High variance indicates disagreement

        Args:
            model_results: List of results from different models

        Returns:
            Variance score
        """
        if len(model_results) < 2:
            return 0.0

        # Extract confidence scores
        scores = []
        for result in model_results:
            score = result.get("crisis_score", result.get("confidence", 0.0))
            scores.append(score)

        # Calculate variance
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)

        return variance

    def analyze_ensemble_correlation(
        self, model_a_results: List[float], model_b_results: List[float]
    ) -> Dict:
        """
        Analyze correlation between two models' predictions

        Args:
            model_a_results: List of scores from model A
            model_b_results: List of scores from model B

        Returns:
            Correlation analysis dictionary
        """
        if len(model_a_results) != len(model_b_results):
            raise ValueError("Result lists must have same length")

        if len(model_a_results) < 2:
            return {"error": "Insufficient data for correlation"}

        # Calculate means
        mean_a = sum(model_a_results) / len(model_a_results)
        mean_b = sum(model_b_results) / len(model_b_results)

        # Calculate correlation coefficient (Pearson)
        numerator = sum(
            (a - mean_a) * (b - mean_b)
            for a, b in zip(model_a_results, model_b_results)
        )

        denominator_a = sum((a - mean_a) ** 2 for a in model_a_results) ** 0.5
        denominator_b = sum((b - mean_b) ** 2 for b in model_b_results) ** 0.5

        if denominator_a == 0 or denominator_b == 0:
            correlation = 0.0
        else:
            correlation = numerator / (denominator_a * denominator_b)

        # Calculate agreement rate
        threshold = 0.5
        predictions_a = [s >= threshold for s in model_a_results]
        predictions_b = [s >= threshold for s in model_b_results]
        agreement_rate = sum(
            1 for a, b in zip(predictions_a, predictions_b) if a == b
        ) / len(predictions_a)

        return {
            "correlation": correlation,
            "agreement_rate": agreement_rate,
            "correlation_strength": self._interpret_correlation(correlation),
            "total_comparisons": len(model_a_results),
        }

    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation coefficient"""
        abs_corr = abs(correlation)

        if abs_corr >= 0.9:
            return "very_strong"
        elif abs_corr >= 0.7:
            return "strong"
        elif abs_corr >= 0.5:
            return "moderate"
        elif abs_corr >= 0.3:
            return "weak"
        else:
            return "very_weak"

    def generate_ensemble_report(self, model_results_list: List[List[Dict]]) -> Dict:
        """
        Generate comprehensive ensemble analysis report

        Args:
            model_results_list: List of result lists from each model
                               [model1_results, model2_results, ...]

        Returns:
            Comprehensive ensemble analysis
        """
        num_models = len(model_results_list)

        if num_models < 2:
            return {"error": "Need at least 2 models for ensemble analysis"}

        # Calculate overall agreement
        all_agreement_rates = []
        for i in range(len(model_results_list[0])):
            # Get all models' results for this test case
            case_results = [models[i] for models in model_results_list]
            agreement = self.calculate_agreement_rate(case_results)
            all_agreement_rates.append(agreement)

        avg_agreement = sum(all_agreement_rates) / len(all_agreement_rates)

        # Find disagreement cases
        disagreement_cases = []
        for i in range(len(model_results_list[0])):
            case_results = [models[i] for models in model_results_list]
            disagreements = self.identify_disagreements(case_results)

            if disagreements:
                disagreement_cases.append(
                    {"test_case_index": i, "disagreements": disagreements}
                )

        # Calculate pairwise correlations
        correlations = {}
        for i in range(num_models):
            for j in range(i + 1, num_models):
                scores_i = [
                    r.get("crisis_score", r.get("predicted_score", 0.0))
                    for r in model_results_list[i]
                ]
                scores_j = [
                    r.get("crisis_score", r.get("predicted_score", 0.0))
                    for r in model_results_list[j]
                ]

                corr_analysis = self.analyze_ensemble_correlation(scores_i, scores_j)
                correlations[f"model_{i}_vs_model_{j}"] = corr_analysis

        return {
            "ensemble_size": num_models,
            "total_test_cases": len(model_results_list[0]),
            "overall_agreement": {
                "average_rate": avg_agreement,
                "min_rate": min(all_agreement_rates),
                "max_rate": max(all_agreement_rates),
            },
            "disagreements": {
                "total_cases": len(disagreement_cases),
                "cases": disagreement_cases[:10],  # Limit to first 10 for brevity
            },
            "pairwise_correlations": correlations,
            "recommendations": self._generate_recommendations(
                avg_agreement, len(disagreement_cases), correlations
            ),
        }

    def _generate_recommendations(
        self, avg_agreement: float, num_disagreements: int, correlations: Dict
    ) -> List[str]:
        """Generate recommendations based on ensemble analysis"""
        recommendations = []

        if avg_agreement < 0.7:
            recommendations.append(
                "Low agreement rate (<70%) - consider reviewing model selection "
                "or adjusting consensus algorithm"
            )

        if num_disagreements > 10:
            recommendations.append(
                f"High number of disagreements ({num_disagreements}) - "
                "implement conflict resolution strategy"
            )

        # Check for low correlations
        low_corr_count = sum(
            1 for corr in correlations.values() if corr.get("correlation", 0) < 0.5
        )

        if low_corr_count > 0:
            recommendations.append(
                f"{low_corr_count} model pairs show weak correlation - "
                "this may indicate diverse perspectives (good) or model issues (bad)"
            )

        if not recommendations:
            recommendations.append(
                "Ensemble showing healthy agreement and correlation patterns"
            )

        return recommendations


# ============================================================================
# FACTORY FUNCTION - Clean Architecture v5.0 Compliance
# ============================================================================


def create_ensemble_analyzer() -> EnsembleAnalyzer:
    """
    Factory function for EnsembleAnalyzer (Clean Architecture v5.0 Pattern)

    Returns:
        EnsembleAnalyzer instance
    """
    return EnsembleAnalyzer()


# ============================================================================
# Export public interface
# ============================================================================

__all__ = ["EnsembleAnalyzer", "create_ensemble_analyzer"]

logger.info("EnsembleAnalyzer v5.0 loaded")
