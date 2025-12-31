"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification

Model Evaluator - Testing Framework Core
---
FILE VERSION: v5.0-2a-2.2
LAST MODIFIED: 2025-12-31
PHASE: 2a Step 2.2 - Multi-Model Task Type Support
CLEAN ARCHITECTURE: v5.0 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

CHANGES in v5.0-2a-2.2:
- Added model-specific label extraction (BART crisis, RoBERTa emotions, Cardiff sentiment/irony)
- Fixed task type handling for different model purposes
- Each model now tested on its native task
- Updated _get_expected_labels to be model-aware
"""

import json
import time
import logging
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
from datetime import datetime

try:
    from transformers import pipeline
    import torch

    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

from .metrics.accuracy_calculator import create_accuracy_calculator
from .metrics.performance_tracker import create_performance_tracker

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """
    Model evaluation and comparison framework for Ash-NLP

    Responsibilities:
    - Load and test AI models against standardized datasets
    - Calculate accuracy, precision, recall, F1 scores (LABEL-BASED per Rule #12)
    - Compare models against baselines
    - Generate comprehensive performance reports
    - Track VRAM usage and latency metrics
    - Support multiple model types (crisis, emotion, sentiment, irony)

    Clean Architecture v5.0 Compliance:
    - Factory function pattern
    - Dependency injection (config manager)
    - JSON + environment variable configuration
    - Real model testing (no mocks per Rule #8)
    - Label-based evaluation (per Rule #12)
    """

    def __init__(self, test_config: Dict):
        """
        Initialize ModelEvaluator with test configuration

        Args:
            test_config: Test configuration dictionary from test_config.json
        """
        if not HAS_TRANSFORMERS:
            raise RuntimeError(
                "transformers library not installed. "
                "Install with: pip install transformers torch"
            )

        self.config = test_config
        self.device = self._determine_device()

        # Initialize metrics calculators
        self.accuracy_calc = create_accuracy_calculator()
        self.performance_tracker = create_performance_tracker()

        # Cache for loaded models
        self.loaded_models = {}

        # Track current model being tested
        self.current_model_name = None

        logger.info(f"ModelEvaluator v5.0-2a-2.2 initialized on device: {self.device}")
        logger.info("Using LABEL-BASED evaluation as primary metric (Rule #12)")
        logger.info("Multi-model task type support enabled")

    def _determine_device(self) -> str:
        """Determine available device (cuda/cpu)"""
        device = self.config.get("test_execution", {}).get("device", "cuda")

        if device == "cuda" and torch.cuda.is_available():
            logger.info(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
            return "cuda"
        else:
            logger.info("Using CPU device")
            return "cpu"

    def load_model(self, model_name: str, task: str = "text-classification") -> Any:
        """
        Load model for testing

        Args:
            model_name: HuggingFace model identifier
            task: Task type (text-classification, zero-shot-classification)

        Returns:
            Loaded pipeline object
        """
        # Check cache
        if model_name in self.loaded_models:
            logger.info(f"Using cached model: {model_name}")
            return self.loaded_models[model_name]

        logger.info(f"Loading model: {model_name} (task: {task})")

        try:
            device_id = 0 if self.device == "cuda" else -1

            model = pipeline(task, model=model_name, device=device_id)

            # Cache model
            self.loaded_models[model_name] = model

            logger.info(f"Model loaded successfully: {model_name}")
            return model

        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise

    def test_single_case(
        self, model: Any, test_case: Dict, task_type: str = "text-classification"
    ) -> Dict:
        """
        Test model against single test case

        Args:
            model: Loaded model pipeline
            test_case: Test case dictionary
            task_type: Type of task for result interpretation

        Returns:
            Test result dictionary with LABEL-BASED correctness
        """
        message = test_case["message"]
        expected = test_case.get("expected_outputs", {})

        # Track performance
        start_time = time.time()
        vram_before = (
            self.performance_tracker.get_vram_usage() if self.device == "cuda" else 0
        )

        try:
            # Run inference
            if task_type == "zero-shot-classification":
                labels = expected.get("model_expectations", {}).get("bart_crisis", [])
                if not labels:
                    labels = ["crisis", "distress", "safe"]
                prediction = model(message, candidate_labels=labels)
            else:
                prediction = model(message)

            # Track performance
            latency_ms = (time.time() - start_time) * 1000
            vram_after = (
                self.performance_tracker.get_vram_usage()
                if self.device == "cuda"
                else 0
            )
            vram_used = max(0, vram_after - vram_before)

            # Extract prediction
            if isinstance(prediction, list):
                predicted_label = prediction[0]["label"]
                predicted_score = prediction[0]["score"]
            else:
                predicted_label = prediction["labels"][0]
                predicted_score = prediction["scores"][0]

            # Determine correctness using LABEL-BASED evaluation (Rule #12)
            # Pass model name to get correct expected labels
            expected_labels = self._get_expected_labels(
                expected, self.current_model_name, task_type
            )
            is_correct = self._is_prediction_correct_label_based(
                predicted_label, expected_labels
            )

            # Also check score-based for informational purposes
            score_correct = self._is_score_in_range(
                predicted_score, expected.get("crisis_score", {})
            )

            return {
                "test_id": test_case.get("id", "unknown"),
                "message": message,
                "predicted_label": predicted_label,
                "predicted_score": float(predicted_score),
                "expected_labels": expected_labels,
                "expected_score_range": expected.get("crisis_score", {}),
                "is_correct": is_correct,  # PRIMARY: Label-based
                "score_correct": score_correct,  # SECONDARY: Score-based
                "latency_ms": latency_ms,
                "vram_mb": vram_used,
                "context": test_case.get("context", {}),
            }

        except Exception as e:
            logger.error(f"Error testing case {test_case.get('id')}: {e}")
            return {
                "test_id": test_case.get("id", "unknown"),
                "error": str(e),
                "is_correct": False,
                "score_correct": False,
            }

    def _get_expected_labels(
        self, expected: Dict, model_name: str, task_type: str
    ) -> List[str]:
        """
        Extract expected labels from test case based on model type

        Model-specific label extraction:
        - BART (facebook/bart-large-mnli): Crisis classification labels
        - RoBERTa go_emotions: Emotion labels (sadness, fear, anger, etc.)
        - Cardiff sentiment: Sentiment labels (positive, negative, neutral)
        - Cardiff irony: Irony labels (ironic, not_ironic)

        Args:
            expected: Expected outputs dictionary
            model_name: Name of the model being tested
            task_type: Type of classification task

        Returns:
            List of acceptable labels for this test case
        """
        model_expectations = expected.get("model_expectations", {})

        if not model_name:
            # Fallback to task type if model name not set
            if task_type == "zero-shot-classification":
                return model_expectations.get("bart_crisis", [])
            return []

        # Determine which labels to use based on model name
        model_lower = model_name.lower()

        if "bart" in model_lower:
            # BART crisis classifier
            labels = model_expectations.get("bart_crisis", [])
            logger.debug(f"Using bart_crisis labels: {labels}")
            return labels

        elif "go_emotions" in model_lower or "emotion" in model_lower:
            # RoBERTa emotions classifier
            labels = model_expectations.get("emotions", [])
            logger.debug(f"Using emotions labels: {labels}")
            return labels

        elif "sentiment" in model_lower:
            # Cardiff sentiment classifier
            sentiment = model_expectations.get("sentiment", "")
            labels = [sentiment] if sentiment else []
            logger.debug(f"Using sentiment label: {labels}")
            return labels

        elif "irony" in model_lower:
            # Cardiff irony classifier
            irony = model_expectations.get("irony", "")
            labels = [irony] if irony else []
            logger.debug(f"Using irony label: {labels}")
            return labels

        else:
            # Generic fallback - assume crisis detection
            logger.warning(
                f"Unknown model type: {model_name}, using bart_crisis labels"
            )
            return model_expectations.get("bart_crisis", [])

    def _is_prediction_correct_label_based(
        self, predicted_label: str, expected_labels: List[str]
    ) -> bool:
        """
        Determine if prediction label matches expected labels (PRIMARY METRIC per Rule #12)

        For crisis detection, we care about:
        - Did it identify the CORRECT crisis type?
        - NOT whether the confidence score hit some threshold

        Args:
            predicted_label: Model's predicted label
            expected_labels: List of acceptable labels

        Returns:
            True if predicted label matches any expected label
        """
        if not expected_labels:
            logger.warning(f"No expected labels for prediction: {predicted_label}")
            return False

        # Case-insensitive label matching
        predicted_lower = predicted_label.lower().strip()
        expected_lower = [label.lower().strip() for label in expected_labels]

        is_match = predicted_lower in expected_lower

        if not is_match:
            logger.debug(
                f"Label mismatch: predicted='{predicted_label}', "
                f"expected one of {expected_labels}"
            )

        return is_match

    def _is_score_in_range(self, predicted_score: float, expected_range: Dict) -> bool:
        """
        Check if confidence score falls in expected range (SECONDARY METRIC)

        This is for informational/analysis purposes only.
        Per Rule #12, score thresholds are NOT the primary success criterion.

        Args:
            predicted_score: Model's confidence score
            expected_range: Expected score range (min/max)

        Returns:
            True if score is in expected range
        """
        if not expected_range:
            return True  # No expectation defined

        min_score = expected_range.get("min", 0.0)
        max_score = expected_range.get("max", 1.0)

        return min_score <= predicted_score <= max_score

    def test_dataset(
        self, model_name: str, dataset_path: str, task_type: str = "text-classification"
    ) -> Dict:
        """
        Test model against entire dataset

        Args:
            model_name: Model to test
            dataset_path: Path to test dataset JSON
            task_type: Type of classification task

        Returns:
            Comprehensive test results with LABEL-BASED accuracy
        """
        logger.info(f"Testing {model_name} against {dataset_path}")
        logger.info(f"Task type: {task_type}")

        # Track current model for label extraction
        self.current_model_name = model_name

        # Load model
        model = self.load_model(model_name, task=task_type)

        # Load dataset
        dataset = self._load_dataset(dataset_path)

        # Run tests
        results = []
        for test_case in dataset["test_cases"]:
            result = self.test_single_case(model, test_case, task_type)
            results.append(result)

        # Calculate metrics (LABEL-BASED)
        metrics = self._calculate_dataset_metrics(results)

        return {
            "model_name": model_name,
            "dataset": dataset_path,
            "task_type": task_type,
            "timestamp": datetime.utcnow().isoformat(),
            "total_tests": len(results),
            "results": results,
            "metrics": metrics,
        }

    def _load_dataset(self, dataset_path: str) -> Dict:
        """Load test dataset from JSON file"""
        path = Path(dataset_path)

        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        with open(path, "r") as f:
            return json.load(f)

    def _calculate_dataset_metrics(self, results: List[Dict]) -> Dict:
        """
        Calculate comprehensive metrics for dataset results

        PRIMARY METRIC: Label-based accuracy (Rule #12)
        SECONDARY METRIC: Score-based accuracy (informational)

        Args:
            results: List of test results

        Returns:
            Metrics dictionary
        """
        # Filter out errors
        valid_results = [r for r in results if "error" not in r]

        if not valid_results:
            return {"error": "No valid results"}

        # PRIMARY: Calculate LABEL-BASED accuracy
        label_correct = sum(1 for r in valid_results if r["is_correct"])
        total = len(valid_results)
        label_accuracy = label_correct / total if total > 0 else 0

        # SECONDARY: Calculate SCORE-BASED accuracy (for comparison/analysis)
        score_correct = sum(1 for r in valid_results if r.get("score_correct", False))
        score_accuracy = score_correct / total if total > 0 else 0

        # Calculate performance metrics
        avg_latency = sum(r["latency_ms"] for r in valid_results) / total
        max_latency = max(r["latency_ms"] for r in valid_results)
        avg_vram = sum(r.get("vram_mb", 0) for r in valid_results) / total
        max_vram = max(r.get("vram_mb", 0) for r in valid_results)

        # Calculate per-category accuracy (LABEL-BASED)
        categories = set(
            r["context"].get("test_category", "unknown") for r in valid_results
        )
        per_category = {}
        for category in categories:
            category_results = [
                r
                for r in valid_results
                if r["context"].get("test_category") == category
            ]
            if category_results:
                category_correct = sum(1 for r in category_results if r["is_correct"])
                per_category[category] = {
                    "accuracy": category_correct / len(category_results),
                    "total_tests": len(category_results),
                    "correct": category_correct,
                }

        # Calculate per-severity accuracy (LABEL-BASED)
        severities = set(r["context"].get("severity", "unknown") for r in valid_results)
        per_severity = {}
        for severity in severities:
            severity_results = [
                r for r in valid_results if r["context"].get("severity") == severity
            ]
            if severity_results:
                severity_correct = sum(1 for r in severity_results if r["is_correct"])
                per_severity[severity] = {
                    "accuracy": severity_correct / len(severity_results),
                    "total_tests": len(severity_results),
                    "correct": severity_correct,
                }

        return {
            "overall": {
                "label_accuracy": label_accuracy,  # PRIMARY METRIC
                "score_accuracy": score_accuracy,  # SECONDARY METRIC
                "total_tests": total,
                "label_passed": label_correct,
                "label_failed": total - label_correct,
                "score_passed": score_correct,
                "score_failed": total - score_correct,
            },
            "performance": {
                "avg_latency_ms": avg_latency,
                "max_latency_ms": max_latency,
                "avg_vram_mb": avg_vram,
                "max_vram_mb": max_vram,
            },
            "per_category": per_category,
            "per_severity": per_severity,
        }

    def compare_models(
        self,
        model_a: str,
        model_b: str,
        dataset_path: str,
        task_type: str = "text-classification",
    ) -> Dict:
        """
        Compare two models side-by-side using LABEL-BASED accuracy

        Args:
            model_a: First model name
            model_b: Second model name
            dataset_path: Test dataset path
            task_type: Classification task type

        Returns:
            Comparison results
        """
        logger.info(f"Comparing {model_a} vs {model_b}")

        # Test both models
        results_a = self.test_dataset(model_a, dataset_path, task_type)
        results_b = self.test_dataset(model_b, dataset_path, task_type)

        # Calculate improvements using LABEL-BASED accuracy
        label_accuracy_a = results_a["metrics"]["overall"]["label_accuracy"]
        label_accuracy_b = results_b["metrics"]["overall"]["label_accuracy"]
        accuracy_improvement = label_accuracy_b - label_accuracy_a

        latency_a = results_a["metrics"]["performance"]["avg_latency_ms"]
        latency_b = results_b["metrics"]["performance"]["avg_latency_ms"]
        latency_improvement = latency_a - latency_b  # Positive = faster

        vram_a = results_a["metrics"]["performance"]["avg_vram_mb"]
        vram_b = results_b["metrics"]["performance"]["avg_vram_mb"]
        vram_improvement = vram_a - vram_b  # Positive = less memory

        return {
            "comparison_timestamp": datetime.utcnow().isoformat(),
            "model_a": {"name": model_a, "results": results_a},
            "model_b": {"name": model_b, "results": results_b},
            "improvements": {
                "label_accuracy": {
                    "absolute": accuracy_improvement,
                    "percentage": (accuracy_improvement / label_accuracy_a * 100)
                    if label_accuracy_a > 0
                    else 0,
                },
                "latency": {
                    "absolute_ms": latency_improvement,
                    "percentage": (latency_improvement / latency_a * 100)
                    if latency_a > 0
                    else 0,
                },
                "vram": {
                    "absolute_mb": vram_improvement,
                    "percentage": (vram_improvement / vram_a * 100)
                    if vram_a > 0
                    else 0,
                },
            },
            "winner": self._determine_winner(accuracy_improvement, latency_improvement),
        }

    def _determine_winner(
        self, accuracy_improvement: float, latency_improvement: float
    ) -> str:
        """
        Determine which model performs better overall

        Uses LABEL-BASED accuracy for comparison

        Priority: Accuracy > Latency
        """
        if accuracy_improvement > 0.05:  # >5% accuracy improvement
            return "model_b"
        elif accuracy_improvement < -0.05:  # >5% accuracy regression
            return "model_a"
        else:
            # Similar accuracy, check latency
            if latency_improvement > 100:  # >100ms faster
                return "model_b"
            elif latency_improvement < -100:  # >100ms slower
                return "model_a"
            else:
                return "tie"

    def generate_report(self, results: Dict, output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive test report

        Args:
            results: Test results dictionary
            output_path: Optional path to save report

        Returns:
            Report as JSON string
        """
        report = {
            "report_version": "v5.0-2a-2.2",
            "evaluation_method": "label_based_primary",
            "generated_at": datetime.utcnow().isoformat(),
            "results": results,
        }

        report_json = json.dumps(report, indent=2)

        if output_path:
            with open(output_path, "w") as f:
                f.write(report_json)
            logger.info(f"Report saved to: {output_path}")

        return report_json

    def cleanup(self):
        """Clean up loaded models and free memory"""
        logger.info("Cleaning up models...")
        self.loaded_models.clear()
        self.current_model_name = None

        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.empty_cache()

        logger.info("Cleanup complete")


# ============================================================================
# FACTORY FUNCTION - Clean Architecture v5.0 Compliance
# ============================================================================


def create_model_evaluator(test_config_path: str = None) -> ModelEvaluator:
    """
    Factory function for ModelEvaluator (Clean Architecture v5.0 Pattern)

    Args:
        test_config_path: Optional path to test_config.json

    Returns:
        ModelEvaluator instance
    """
    # Load configuration
    if test_config_path is None:
        test_config_path = Path(__file__).parent / "config" / "test_config.json"

    with open(test_config_path, "r") as f:
        config = json.load(f)

    # Merge defaults with overrides
    defaults = config.get("defaults", {})
    test_config = {}

    for section, values in defaults.items():
        test_config[section] = values.copy()

    return ModelEvaluator(test_config)


# ============================================================================
# Export public interface
# ============================================================================

__all__ = ["ModelEvaluator", "create_model_evaluator"]

logger.info("ModelEvaluator v5.0-2a-2.2 loaded (Multi-Model Task Type Support)")
