#!/usr/bin/env python3
"""
Escalation Patterns Dataset Completion Script
Handles the unique temporal sequence structure of escalation_patterns.json

FILE VERSION: v5.0-2a-2.2
LAST MODIFIED: 2025-12-31
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import json
from pathlib import Path
from typing import Dict, List


def determine_sentiment_from_score(crisis_score: float) -> str:
    """Determine sentiment based on crisis score"""
    if crisis_score >= 0.6:
        return "negative"
    elif crisis_score >= 0.3:
        return "negative"
    else:
        return "neutral"


def determine_bart_crisis_from_level(crisis_level: str, score: float) -> List[str]:
    """Determine BART crisis labels from level and score"""
    if crisis_level == "critical" or score >= 0.8:
        return ["severe depression", "suicide ideation"]
    elif crisis_level == "high" or score >= 0.6:
        return ["severe depression", "distress"]
    elif crisis_level == "medium" or score >= 0.4:
        return ["depression", "distress"]
    elif crisis_level == "low" or score >= 0.2:
        return ["distress", "low mood"]
    else:
        return ["safe"]


def determine_emotions_from_level(crisis_level: str, score: float) -> List[str]:
    """Determine emotions based on crisis level and score"""
    if crisis_level == "critical" or score >= 0.8:
        return ["despair", "hopelessness", "sadness"]
    elif crisis_level == "high" or score >= 0.6:
        return ["sadness", "distress", "desperation"]
    elif crisis_level == "medium" or score >= 0.4:
        return ["sadness", "frustration", "difficulty"]
    elif crisis_level == "low" or score >= 0.2:
        return ["mild_distress", "difficulty"]
    else:
        return ["neutral"]


def complete_escalation_patterns(dataset_path: Path):
    """Complete escalation_patterns.json with model expectations"""
    print("=" * 70)
    print("ESCALATION PATTERNS DATASET COMPLETION")
    print("=" * 70)

    # Load dataset
    print(f"\nLoading: {dataset_path}")
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update metadata
    data["_metadata"]["file_version"] = "v5.0-2a-2.2-complete"
    data["_metadata"]["changes_v5.0-2a-2.2-complete"] = (
        "Added complete bart_crisis, emotions, sentiment, and irony to all message sequences"
    )

    # Process each escalation pattern
    patterns_updated = 0
    messages_updated = 0

    for pattern_id, pattern_data in data["escalation_patterns"].items():
        print(f"\nProcessing: {pattern_id} - {pattern_data['pattern_name']}")

        # Process each message in the sequence
        for msg_idx, message in enumerate(pattern_data["message_sequence"]):
            # Get existing values
            crisis_score = message.get("expected_crisis_score", 0.5)
            crisis_level = message.get("expected_crisis_level", "medium")

            # Create or update model_expectations
            if "model_expectations" not in message:
                message["model_expectations"] = {}

            model_exp = message["model_expectations"]

            # Add bart_crisis if missing
            if "bart_crisis" not in model_exp:
                model_exp["bart_crisis"] = determine_bart_crisis_from_level(
                    crisis_level, crisis_score
                )
                messages_updated += 1

            # Add emotions if missing
            if "emotions" not in model_exp:
                model_exp["emotions"] = determine_emotions_from_level(
                    crisis_level, crisis_score
                )
                messages_updated += 1

            # Add sentiment if missing
            if "sentiment" not in model_exp:
                model_exp["sentiment"] = determine_sentiment_from_score(crisis_score)
                messages_updated += 1

            # Add irony if missing (escalation patterns are all genuine, not ironic)
            if "irony" not in model_exp:
                model_exp["irony"] = "not_ironic"
                messages_updated += 1

            # Update message
            message["model_expectations"] = model_exp

        patterns_updated += 1
        print(
            f"  ✓ Updated {len(pattern_data['message_sequence'])} messages in sequence"
        )

    # Save completed version
    output_path = dataset_path.parent / "escalation_patterns_complete.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("COMPLETION SUMMARY")
    print("=" * 70)
    print(f"✓ Patterns processed: {patterns_updated}")
    print(f"✓ Messages updated: {messages_updated}")
    print(f"✓ Output saved to: {output_path}")
    print("\nNext steps:")
    print("1. Review escalation_patterns_complete.json")
    print("2. Replace original if satisfied")
    print("3. Test temporal escalation detection")
    print("=" * 70)

    return output_path


def main():
    """Main execution"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   Escalation Patterns Dataset Completion Script                  ║")
    print("║   Temporal message sequence structure handler                    ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    # Define path
    dataset_path = Path("test_datasets/escalation_patterns.json")

    if not dataset_path.exists():
        print(f"\n⚠ ERROR: File not found: {dataset_path}")
        print("Make sure you're running from the repository root")
        return

    # Complete the dataset
    output_path = complete_escalation_patterns(dataset_path)

    print("\n✓ Escalation patterns dataset completion finished!")
    print(f"✓ File ready: {output_path.name}")


if __name__ == "__main__":
    main()
