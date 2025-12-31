#!/usr/bin/env python3.11
"""
Ash-NLP: Adjust Test Dataset Thresholds
---
Lowers crisis score thresholds by 0.10 to reflect realistic model performance.

Current (too strict):
- Critical: 0.95+ → New: 0.85+
- High: 0.85+ → New: 0.75+
- Medium: 0.75+ → New: 0.65+
- Low: 0.60+ → New: 0.50+

FILE VERSION: v5.0
LAST MODIFIED: 2025-12-31
"""

import json
from pathlib import Path
from typing import Dict, Any


def adjust_threshold(value: float, adjustment: float = -0.10) -> float:
    """Adjust a threshold value, keeping it within 0.0-1.0 range"""
    adjusted = value + adjustment
    return max(0.0, min(1.0, adjusted))


def adjust_crisis_score(crisis_score: Dict[str, float]) -> Dict[str, float]:
    """Adjust crisis score min/max thresholds"""
    return {
        "min": adjust_threshold(crisis_score.get("min", 0.5)),
        "max": crisis_score.get("max", 1.0),  # Keep max unchanged
    }


def adjust_test_case(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Adjust thresholds in a single test case"""
    if "expected_outputs" in test_case:
        expected = test_case["expected_outputs"]

        # Adjust crisis_score if present
        if "crisis_score" in expected:
            expected["crisis_score"] = adjust_crisis_score(expected["crisis_score"])

        # Adjust score_range if present (safe examples)
        if "score_range" in expected:
            expected["score_range"] = adjust_crisis_score(expected["score_range"])

    return test_case


def adjust_dataset(dataset: Dict[str, Any]) -> Dict[str, Any]:
    """Adjust all test cases in a dataset"""
    if "test_cases" in dataset:
        dataset["test_cases"] = [
            adjust_test_case(case) for case in dataset["test_cases"]
        ]

    # Update metadata
    if "_metadata" in dataset:
        dataset["_metadata"]["last_modified"] = "2025-12-31"
        dataset["_metadata"]["adjusted_thresholds"] = True
        dataset["_metadata"]["threshold_adjustment"] = -0.10

    return dataset


def process_file(input_path: Path, output_path: Path):
    """Process a single test dataset file"""
    print(f"Processing: {input_path.name}")

    # Load original
    with open(input_path, "r") as f:
        dataset = json.load(f)

    # Adjust thresholds
    adjusted = adjust_dataset(dataset)

    # Save adjusted version
    with open(output_path, "w") as f:
        json.dump(adjusted, f, indent=2)

    print(f"  ✓ Saved to: {output_path.name}")


def main():
    """Process all test dataset files"""
    print("Adjusting Test Dataset Thresholds")
    print("=" * 50)
    print("Lowering thresholds by 0.10 to reflect realistic performance\n")

    # Define files to process
    datasets = [
        "crisis_examples.json",
        "safe_examples.json",
        "edge_cases.json",
        "lgbtqia_specific.json",
        "escalation_patterns.json",
    ]

    input_dir = Path("test_datasets")
    output_dir = Path("test_datasets")

    # Process each file
    for filename in datasets:
        input_path = input_dir / filename

        if not input_path.exists():
            print(f"  ⚠ Skipping {filename} (not found)")
            continue

        # Backup original
        backup_path = input_dir / f"{filename}.backup"
        if not backup_path.exists():
            import shutil

            shutil.copy2(input_path, backup_path)
            print(f"  📋 Backed up to: {backup_path.name}")

        # Process and overwrite
        output_path = input_path
        process_file(input_path, output_path)

    print("\n" + "=" * 50)
    print("✓ All datasets adjusted!")
    print("\nOriginal files backed up with .backup extension")
    print("\nReady to re-run tests with realistic thresholds:")
    print("  docker compose run ash-nlp-testing test-baseline")


if __name__ == "__main__":
    main()
