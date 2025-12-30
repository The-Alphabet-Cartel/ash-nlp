"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community

Accuracy Calculator - Metrics Computation
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: v5.0 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class AccuracyCalculator:
    """
    Calculate classification metrics for model evaluation

    Responsibilities:
    - Calculate precision, recall, F1 scores
    - Generate confusion matrices
    - Compute per-class metrics
    - Generate comprehensive classification reports

    Clean Architecture v5.0 Compliance:
    - Factory function pattern
    - Real calculations (no mocks per Rule #8)
    """

    def __init__(self):
        """Initialize AccuracyCalculator"""
        logger.info("AccuracyCalculator v5.0 initialized")

    def calculate_precision(self, true_positives: int, false_positives: int) -> float:
        """
        Calculate precision score

        Precision = TP / (TP + FP)

        Args:
            true_positives: Number of true positive predictions
            false_positives: Number of false positive predictions

        Returns:
            Precision score (0.0 to 1.0)
        """
        if true_positives + false_positives == 0:
            return 0.0

        return true_positives / (true_positives + false_positives)

    def calculate_recall(self, true_positives: int, false_negatives: int) -> float:
        """
        Calculate recall score (sensitivity)

        Recall = TP / (TP + FN)

        Args:
            true_positives: Number of true positive predictions
            false_negatives: Number of false negative predictions

        Returns:
            Recall score (0.0 to 1.0)
        """
        if true_positives + false_negatives == 0:
            return 0.0

        return true_positives / (true_positives + false_negatives)

    def calculate_f1(self, precision: float, recall: float) -> float:
        """
        Calculate F1 score (harmonic mean of precision and recall)

        F1 = 2 * (precision * recall) / (precision + recall)

        Args:
            precision: Precision score
            recall: Recall score

        Returns:
            F1 score (0.0 to 1.0)
        """
        if precision + recall == 0:
            return 0.0

        return 2 * (precision * recall) / (precision + recall)

    def calculate_accuracy(
        self,
        true_positives: int,
        true_negatives: int,
        false_positives: int,
        false_negatives: int,
    ) -> float:
        """
        Calculate overall accuracy

        Accuracy = (TP + TN) / (TP + TN + FP + FN)

        Args:
            true_positives: True positive count
            true_negatives: True negative count
            false_positives: False positive count
            false_negatives: False negative count

        Returns:
            Accuracy score (0.0 to 1.0)
        """
        total = true_positives + true_negatives + false_positives + false_negatives

        if total == 0:
            return 0.0

        return (true_positives + true_negatives) / total

    def calculate_confusion_matrix(
        self, predictions: List[bool], ground_truth: List[bool]
    ) -> Dict[str, int]:
        """
        Calculate confusion matrix values

        Args:
            predictions: List of predicted labels (True=crisis, False=safe)
            ground_truth: List of actual labels (True=crisis, False=safe)

        Returns:
            Dictionary with TP, TN, FP, FN counts
        """
        if len(predictions) != len(ground_truth):
            raise ValueError("Predictions and ground truth must have same length")

        tp = sum(1 for p, g in zip(predictions, ground_truth) if p and g)
        tn = sum(1 for p, g in zip(predictions, ground_truth) if not p and not g)
        fp = sum(1 for p, g in zip(predictions, ground_truth) if p and not g)
        fn = sum(1 for p, g in zip(predictions, ground_truth) if not p and g)

        return {
            "true_positives": tp,
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn,
        }

    def generate_classification_report(
        self, predictions: List[bool], ground_truth: List[bool]
    ) -> Dict:
        """
        Generate comprehensive classification metrics report

        Args:
            predictions: List of predicted labels
            ground_truth: List of actual labels

        Returns:
            Comprehensive metrics dictionary
        """
        # Calculate confusion matrix
        cm = self.calculate_confusion_matrix(predictions, ground_truth)

        # Calculate metrics
        precision = self.calculate_precision(
            cm["true_positives"], cm["false_positives"]
        )

        recall = self.calculate_recall(cm["true_positives"], cm["false_negatives"])

        f1 = self.calculate_f1(precision, recall)

        accuracy = self.calculate_accuracy(
            cm["true_positives"],
            cm["true_negatives"],
            cm["false_positives"],
            cm["false_negatives"],
        )

        # Calculate rates
        total_actual_positive = cm["true_positives"] + cm["false_negatives"]
        total_actual_negative = cm["true_negatives"] + cm["false_positives"]

        false_positive_rate = (
            cm["false_positives"] / total_actual_negative
            if total_actual_negative > 0
            else 0.0
        )

        false_negative_rate = (
            cm["false_negatives"] / total_actual_positive
            if total_actual_positive > 0
            else 0.0
        )

        return {
            "confusion_matrix": cm,
            "metrics": {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
            },
            "rates": {
                "false_positive_rate": false_positive_rate,
                "false_negative_rate": false_negative_rate,
            },
            "summary": {
                "total_samples": len(predictions),
                "total_actual_positive": total_actual_positive,
                "total_actual_negative": total_actual_negative,
            },
        }

    def calculate_per_category_metrics(self, results: List[Dict]) -> Dict[str, Dict]:
        """
        Calculate metrics for each test category

        Args:
            results: List of test results with categories

        Returns:
            Dictionary of metrics per category
        """
        # Group results by category
        categories = {}
        for result in results:
            category = result.get("context", {}).get("test_category", "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(result)

        # Calculate metrics for each category
        per_category = {}
        for category, category_results in categories.items():
            predictions = [r["is_correct"] for r in category_results]
            ground_truth = [True] * len(predictions)  # All should be correct

            correct = sum(predictions)
            total = len(predictions)
            accuracy = correct / total if total > 0 else 0.0

            per_category[category] = {
                "accuracy": accuracy,
                "total_tests": total,
                "passed": correct,
                "failed": total - correct,
            }

        return per_category


# ============================================================================
# FACTORY FUNCTION - Clean Architecture v5.0 Compliance
# ============================================================================


def create_accuracy_calculator() -> AccuracyCalculator:
    """
    Factory function for AccuracyCalculator (Clean Architecture v5.0 Pattern)

    Returns:
        AccuracyCalculator instance
    """
    return AccuracyCalculator()


# ============================================================================
# Export public interface
# ============================================================================

__all__ = ["AccuracyCalculator", "create_accuracy_calculator"]

logger.info("AccuracyCalculator v5.0 loaded")
