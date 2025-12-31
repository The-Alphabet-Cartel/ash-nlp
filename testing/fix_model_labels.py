#!/usr/bin/env python3
"""
Ash-NLP Test Dataset Label Correction Script
Fixes label format mismatches between our expectations and model outputs

ROOT CAUSE OF 0% IRONY ACCURACY:
  Our label: "not_ironic"  →  Model returns: "non_irony"
  Our label: "ironic"      →  Model returns: "irony"

ROOT CAUSE OF LOW EMOTIONS ACCURACY:
  We used invalid labels like "despair", "loneliness", "resignation"
  go_emotions model only has 28 specific labels

FILE VERSION: v5.0-2a-2.3
LAST MODIFIED: 2025-12-31
Repository: https://github.com/the-alphabet-cartel/ash-nlp

USAGE:
  python fix_model_labels.py

This will process all datasets in testing/test_datasets/ and create
*_labels_fixed.json versions with corrected labels.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# ============================================================
# VALID LABEL SETS
# ============================================================

# Cardiff Irony model labels (binary)
IRONY_LABEL_MAP = {
    "not_ironic": "non_irony",
    "ironic": "irony",
    "potentially_ironic": "non_irony",  # Default to non_irony for ambiguous
}

# go_emotions valid labels (28 total)
GO_EMOTIONS_LABELS = {
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "neutral",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
}

# Emotion label mapping (invalid → valid go_emotions label)
EMOTION_LABEL_MAP = {
    # Crisis emotions - map to closest valid label
    "despair": "grief",
    "desperation": "fear",
    "hopelessness": "grief",
    "loneliness": "sadness",
    "resignation": "sadness",
    "pain": "sadness",
    "terror": "fear",
    "panic": "fear",
    "abandonment": "sadness",
    "betrayal": "sadness",
    "distress": "sadness",
    "dysphoria": "sadness",
    "trauma": "fear",
    "self-hatred": "disapproval",
    "self_hatred": "disapproval",
    "worthlessness": "sadness",
    "finality": "sadness",
    "trapped": "fear",
    "helplessness": "sadness",
    "emptiness": "sadness",
    "numbness": "neutral",
    "disconnection": "neutral",
    # Mild distress
    "difficulty": "sadness",
    "mild_distress": "sadness",
    "mild_anxiety": "nervousness",
    "low_mood": "sadness",
    "weariness": "sadness",
    "fatigue": "sadness",
    "stress": "nervousness",
    "concern": "nervousness",
    "worry": "nervousness",
    "uncertainty": "confusion",
    # Positive emotions
    "happiness": "joy",
    "celebration": "joy",
    "self-acceptance": "approval",
    "self_acceptance": "approval",
    "self-care": "caring",
    "self_care": "caring",
    "self-love": "love",
    "contentment": "relief",
    "peace": "relief",
    "affirmation": "approval",
    "validation": "approval",
    "belonging": "love",
    "connection": "caring",
    "achievement": "pride",
    "fulfillment": "joy",
    "euphoria": "joy",
    "authenticity": "pride",
    "solidarity": "caring",
    "triumph": "joy",
    "progress": "optimism",
    "improvement": "optimism",
    "growth": "optimism",
    "resilience": "pride",
    "coping": "relief",
    "need": "desire",
    "vulnerability": "fear",
    # Neutral/Other
    "engagement": "amusement",
    "anticipation": "excitement",
    "determination": "approval",
    "seriousness": "neutral",
    "hunger": "desire",
    "tiredness": "sadness",
    "discomfort": "annoyance",
    "boredom": "annoyance",
    "defensiveness": "annoyance",
    "apathy": "neutral",
    "avoidance": "fear",
    "internal_conflict": "confusion",
    "seeking_validation": "desire",
    "self-discovery": "realization",
    "self_discovery": "realization",
    "exploration": "curiosity",
    "doubt": "confusion",
    "overwhelm": "fear",
    "invalidation": "disapproval",
    "agreement": "approval",
    "empathy": "caring",
    "sympathy": "caring",
    "recognition": "realization",
    "relaxation": "relief",
    "coping_humor": "amusement",
    "detachment": "neutral",
    "minimal_positive": "relief",
    "pressure": "nervousness",
    "satisfaction": "approval",
    "low_energy": "sadness",
    "hope": "optimism",
    "acceptance": "approval",
    "confidence": "pride",
    "anxiety": "nervousness",
    "exhaustion": "sadness",
    "shame": "embarrassment",
    "isolation": "sadness",
    # Labels that are already valid - keep as-is
    "sadness": "sadness",
    "fear": "fear",
    "anger": "anger",
    "joy": "joy",
    "love": "love",
    "surprise": "surprise",
    "disgust": "disgust",
    "neutral": "neutral",
    "confusion": "confusion",
    "frustration": "annoyance",
    "annoyance": "annoyance",
    "disappointment": "disappointment",
    "embarrassment": "embarrassment",
    "excitement": "excitement",
    "gratitude": "gratitude",
    "grief": "grief",
    "nervousness": "nervousness",
    "optimism": "optimism",
    "pride": "pride",
    "relief": "relief",
    "remorse": "remorse",
    "amusement": "amusement",
    "caring": "caring",
    "curiosity": "curiosity",
    "desire": "desire",
    "admiration": "admiration",
    "approval": "approval",
    "disapproval": "disapproval",
    "realization": "realization",
}

# ============================================================
# STATISTICS TRACKING
# ============================================================
stats = {
    "irony_fixes": 0,
    "emotion_fixes": 0,
    "unknown_emotions": [],
    "files_processed": 0,
}

# ============================================================
# LABEL CORRECTION FUNCTIONS
# ============================================================


def fix_irony_label(label: str) -> str:
    """Convert our irony labels to model format"""
    if label in IRONY_LABEL_MAP:
        new_label = IRONY_LABEL_MAP[label]
        if label != new_label:
            stats["irony_fixes"] += 1
        return new_label
    return "non_irony"  # Default


def fix_emotion_label(label: str) -> str:
    """Convert our emotion labels to valid go_emotions labels"""
    # Check if already valid
    if label in GO_EMOTIONS_LABELS:
        return label

    # Try mapping
    if label in EMOTION_LABEL_MAP:
        return EMOTION_LABEL_MAP[label]

    # Track unknown labels
    if label not in stats["unknown_emotions"]:
        stats["unknown_emotions"].append(label)
        print(f"  ⚠ Unknown emotion label: '{label}' → defaulting to 'sadness'")

    return "sadness"


def fix_emotions_list(emotions: List[str]) -> List[str]:
    """Fix all emotions in a list, removing duplicates"""
    original = emotions.copy()
    fixed = []
    for emotion in emotions:
        fixed_emotion = fix_emotion_label(emotion)
        if fixed_emotion not in fixed:  # Avoid duplicates
            fixed.append(fixed_emotion)

    if original != fixed:
        stats["emotion_fixes"] += 1

    return fixed


# ============================================================
# DATASET PROCESSING
# ============================================================


def process_model_expectations(model_exp: Dict) -> Dict:
    """Process and fix model expectations"""
    if not model_exp:
        return model_exp

    # Fix irony
    if "irony" in model_exp:
        model_exp["irony"] = fix_irony_label(model_exp["irony"])

    # Fix emotions
    if "emotions" in model_exp:
        model_exp["emotions"] = fix_emotions_list(model_exp["emotions"])

    return model_exp


def process_test_cases(data: Dict) -> Dict:
    """Process standard test_cases structure"""
    if "test_cases" not in data:
        return data

    for test_case in data["test_cases"]:
        if "expected_outputs" in test_case:
            if "model_expectations" in test_case["expected_outputs"]:
                test_case["expected_outputs"]["model_expectations"] = (
                    process_model_expectations(
                        test_case["expected_outputs"]["model_expectations"]
                    )
                )

    return data


def process_escalation_patterns(data: Dict) -> Dict:
    """Process escalation_patterns structure"""
    if "escalation_patterns" not in data:
        return data

    for pattern_id, pattern_data in data["escalation_patterns"].items():
        if "message_sequence" in pattern_data:
            for message in pattern_data["message_sequence"]:
                if "model_expectations" in message:
                    message["model_expectations"] = process_model_expectations(
                        message["model_expectations"]
                    )

    return data


def process_dataset(filepath: Path) -> Dict:
    """Process a dataset file and fix all labels"""
    print(f"\n{'=' * 60}")
    print(f"Processing: {filepath.name}")
    print("=" * 60)

    # Reset per-file stats
    file_irony_start = stats["irony_fixes"]
    file_emotion_start = stats["emotion_fixes"]

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update metadata
    data["_metadata"]["file_version"] = "v5.0-2a-2.3-labels-fixed"
    data["_metadata"]["last_modified"] = datetime.now().strftime("%Y-%m-%d")
    data["_metadata"]["changes_v5.0-2a-2.3"] = (
        "Fixed irony labels (non_irony/irony) and emotions labels (valid go_emotions set)"
    )

    # Process based on structure
    data = process_test_cases(data)
    data = process_escalation_patterns(data)

    # Report per-file fixes
    file_irony = stats["irony_fixes"] - file_irony_start
    file_emotion = stats["emotion_fixes"] - file_emotion_start
    print(f"  ✓ Irony labels fixed: {file_irony}")
    print(f"  ✓ Emotion entries fixed: {file_emotion}")

    stats["files_processed"] += 1

    return data


def save_dataset(data: Dict, original_path: Path, in_place: bool = False):
    """Save the fixed dataset"""
    if in_place:
        output_path = original_path
    else:
        output_path = original_path.parent / f"{original_path.stem}_labels_fixed.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Saved: {output_path.name}")
    return output_path


# ============================================================
# MAIN EXECUTION
# ============================================================


def main():
    """Fix all dataset labels"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   Ash-NLP Label Correction Script v5.0-2a-2.3                    ║")
    print("║   Fixing irony (non_irony/irony) and emotions (go_emotions)      ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    # Define dataset paths - try multiple possible locations
    possible_dirs = [
        Path("test_datasets"),
        Path("/app/testing/test_datasets"),
        Path("test_datasets"),
        Path("."),
    ]

    datasets_dir = None
    for d in possible_dirs:
        if d.exists() and any(d.glob("*.json")):
            datasets_dir = d
            break

    if not datasets_dir:
        print("\n⚠ ERROR: Could not find test_datasets directory")
        print("Searching in current directory for JSON files...")
        datasets_dir = Path(".")

    print(f"\nUsing directory: {datasets_dir.absolute()}")

    datasets = [
        "safe_examples.json",
        "edge_cases.json",
        "crisis_examples.json",
        "lgbtqia_specific.json",
        "escalation_patterns.json",
    ]

    fixed_files = []

    for dataset_name in datasets:
        dataset_path = datasets_dir / dataset_name

        # Also try with _complete suffix
        if not dataset_path.exists():
            dataset_path = datasets_dir / dataset_name.replace(
                ".json", "_complete.json"
            )

        if not dataset_path.exists():
            print(f"\n⚠ File not found: {dataset_name}")
            continue

        try:
            # Process and save (create new file, don't overwrite)
            fixed_data = process_dataset(dataset_path)
            output_path = save_dataset(fixed_data, dataset_path, in_place=False)
            fixed_files.append(output_path)
        except Exception as e:
            print(f"\n❌ Error processing {dataset_name}: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("LABEL CORRECTION COMPLETE")
    print("=" * 60)

    print(f"\n📊 STATISTICS:")
    print(f"  Files processed: {stats['files_processed']}")
    print(f"  Total irony fixes: {stats['irony_fixes']}")
    print(f"  Total emotion fixes: {stats['emotion_fixes']}")

    if stats["unknown_emotions"]:
        print(f"\n⚠ Unknown emotions (mapped to 'sadness'):")
        for emo in stats["unknown_emotions"]:
            print(f"    - {emo}")

    print(f"\n✓ Created {len(fixed_files)} fixed datasets:")
    for filepath in fixed_files:
        print(f"  - {filepath.name}")

    print("\n📋 LABEL CHANGES APPLIED:")
    print("\n  IRONY (Cardiff model expects):")
    print("    not_ironic → non_irony")
    print("    ironic → irony")
    print("    potentially_ironic → non_irony")

    print("\n  EMOTIONS (go_emotions 28 valid labels):")
    print("    despair → grief")
    print("    desperation → fear")
    print("    loneliness → sadness")
    print("    hopelessness → grief")
    print("    resignation → sadness")
    print("    panic → fear")
    print("    (and many more...)")

    print("\n📊 EXPECTED ACCURACY AFTER FIX:")
    print("  - Irony: 0% → ~100% (crisis messages are non-ironic)")
    print("  - Emotions: 23.64% → 50-70% (valid labels)")
    print("  - Sentiment: 89.09% (already good!)")

    print("\n🚀 NEXT STEPS:")
    print("  1. Replace original datasets:")
    print("     mv *_labels_fixed.json to original names")
    print("  2. Re-run tests to verify improvements")
    print("  3. Commit updated datasets")

    print("\n" + "=" * 60)
    return fixed_files


if __name__ == "__main__":
    main()
