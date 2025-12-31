#!/usr/bin/env python3.11
"""
Ash-NLP: Calculate Label-Only Accuracy
---
Analyzes test results based on label correctness instead of score thresholds.

This shows the TRUE model performance - did it identify the right crisis type?

FILE VERSION: v5.0
LAST MODIFIED: 2025-12-31
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_test_dataset(dataset_path: Path) -> Dict[str, Any]:
    """Load the original test dataset to get expected labels"""
    with open(dataset_path, "r") as f:
        return json.load(f)


def load_results(results_path: Path) -> Dict[str, Any]:
    """Load the test results"""
    with open(results_path, "r") as f:
        return json.load(f)


def extract_expected_labels(test_case: Dict[str, Any]) -> List[str]:
    """Extract all acceptable labels from a test case"""
    expected = test_case.get("expected_outputs", {})
    model_expectations = expected.get("model_expectations", {})

    # Get BART crisis labels (primary)
    bart_labels = model_expectations.get("bart_crisis", [])

    # Also accept emotion labels as valid
    emotion_labels = model_expectations.get("emotions", [])

    # Combine all acceptable labels
    all_labels = bart_labels + emotion_labels

    return [label.lower().strip() for label in all_labels]


def normalize_label(label: str) -> str:
    """Normalize label for comparison"""
    return label.lower().strip()


def is_label_match(predicted: str, expected_labels: List[str]) -> bool:
    """Check if predicted label matches any expected label"""
    predicted_norm = normalize_label(predicted)

    # Exact match
    if predicted_norm in expected_labels:
        return True

    # Partial match (for compound labels like "self-harm thoughts")
    for expected in expected_labels:
        if predicted_norm in expected or expected in predicted_norm:
            return True

    return False


def analyze_label_accuracy(dataset_path: Path, results_path: Path):
    """Analyze accuracy based on label correctness only"""

    print(f"\n{'=' * 60}")
    print("Label-Only Accuracy Analysis")
    print(f"{'=' * 60}\n")

    # Load data
    dataset = load_test_dataset(dataset_path)
    results = load_results(results_path)

    # Create lookup of test cases by ID
    test_cases = {case["id"]: case for case in dataset.get("test_cases", [])}

    # Analyze each result
    correct = 0
    total = 0
    mismatches = []
    category_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    for result in results["results"]["results"]:
        test_id = result["test_id"]
        predicted_label = result["predicted_label"]
        predicted_score = result["predicted_score"]
        category = result["context"].get("test_category", "unknown")

        # Get expected labels
        test_case = test_cases.get(test_id)
        if not test_case:
            print(f"⚠ Warning: Test case {test_id} not found in dataset")
            continue

        expected_labels = extract_expected_labels(test_case)

        # Check if label matches
        is_correct = is_label_match(predicted_label, expected_labels)

        total += 1
        category_stats[category]["total"] += 1

        if is_correct:
            correct += 1
            category_stats[category]["correct"] += 1
        else:
            mismatches.append(
                {
                    "test_id": test_id,
                    "message": result["message"][:60] + "...",
                    "predicted": predicted_label,
                    "expected": expected_labels,
                    "score": predicted_score,
                    "category": category,
                }
            )

    # Calculate overall accuracy
    accuracy = (correct / total * 100) if total > 0 else 0

    # Print results
    print(f"Overall Label Accuracy: {accuracy:.2f}%")
    print(f"Correct: {correct}/{total}")
    print(f"Incorrect: {total - correct}/{total}")
    print()

    # Category breakdown
    print(f"\n{'Category Breakdown':-^60}")
    print(f"{'Category':<30} {'Accuracy':<15} {'Correct/Total':<15}")
    print("-" * 60)

    for category in sorted(category_stats.keys()):
        stats = category_stats[category]
        cat_accuracy = (
            (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        )
        print(
            f"{category:<30} {cat_accuracy:>6.1f}%         {stats['correct']}/{stats['total']}"
        )

    # Show mismatches
    if mismatches:
        print(f"\n{'Label Mismatches':-^60}")
        print(f"Total Mismatches: {len(mismatches)}\n")

        for i, mismatch in enumerate(mismatches[:10], 1):  # Show first 10
            print(f"{i}. [{mismatch['test_id']}] {mismatch['category']}")
            print(f"   Message: {mismatch['message']}")
            print(
                f"   Predicted: {mismatch['predicted']} (score: {mismatch['score']:.3f})"
            )
            print(f"   Expected: {', '.join(mismatch['expected'])}")
            print()

        if len(mismatches) > 10:
            print(f"   ... and {len(mismatches) - 10} more mismatches")

    print(f"\n{'=' * 60}")
    print(f"Label-Only Accuracy: {accuracy:.2f}%")

    # Get score-based accuracy from metrics
    score_accuracy = results["results"]["metrics"]["overall"]["accuracy"] * 100

    print(f"Score-Based Accuracy: {score_accuracy:.2f}%")
    print(f"Difference: +{accuracy - score_accuracy:.2f}%")
    print(f"{'=' * 60}\n")

    return accuracy


def main():
    """Analyze all test results"""

    # Paths
    dataset_path = Path("test_datasets/crisis_examples.json")
    results_path = Path("reports/output/baseline_v3.1.json")

    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        return

    if not results_path.exists():
        print(f"❌ Results not found: {results_path}")
        return

    # Analyze
    accuracy = analyze_label_accuracy(dataset_path, results_path)

    print("\n📊 Summary:")
    print(f"   Label-based evaluation is more meaningful for crisis detection")
    print(f"   because it measures whether the model identified the RIGHT type")
    print(f"   of crisis, regardless of confidence score.\n")


if __name__ == "__main__":
    main()
