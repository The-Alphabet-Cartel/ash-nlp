#!/usr/bin/env python3
"""
Debug script to test JSON label configuration
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import config
sys.path.append(str(Path(__file__).parent.parent))

from config.zero_shot_config import get_labels_config

def debug_labels():
    """Debug the label configuration"""
    print("🔍 DEBUG: Label Configuration")
    print("=" * 50)
    
    config = get_labels_config()
    
    # Show basic info
    print(f"Current label set: {config.get_current_label_set_name()}")
    print(f"Available sets: {config.get_available_label_sets()}")
    print(f"Stats: {config.get_current_stats()}")
    print()
    
    # Show actual labels
    labels = config.get_all_labels()
    print("📋 ACTUAL LABELS:")
    for model, model_labels in labels.items():
        print(f"\n{model.upper()}:")
        for i, label in enumerate(model_labels, 1):
            print(f"  {i}. {label}")
    
    # Test mapping rules
    print(f"\n🗺️ MAPPING RULES:")
    if hasattr(config, 'current_mapping_rules') and config.current_mapping_rules:
        for model, rules in config.current_mapping_rules.items():
            print(f"\n{model.upper()}:")
            for category, patterns in rules.items():
                print(f"  {category}: {patterns}")
    else:
        print("  No mapping rules found!")
    
    # Test the mapping functions with actual zero-shot labels
    print(f"\n🧪 TESTING MAPPING WITH ACTUAL LABELS:")
    depression_labels = config.get_depression_labels()
    
    for i, label in enumerate(depression_labels[:3]):  # Test first 3
        print(f"\nTesting depression label {i+1}: '{label[:50]}...'")
        result = config.map_depression_label(label)
        print(f"  Mapped to: {result}")
    
    # Test with user input format (this might be the issue)
    print(f"\n🧪 TESTING WITH USER INPUT FORMAT:")
    test_inputs = [
        "I want to kill myself",
        "person saying: I want to kill myself", 
        "person actively expressing suicidal thoughts"
    ]
    
    for test_input in test_inputs:
        print(f"\nTesting: '{test_input}'")
        dep_result = config.map_depression_label(test_input)
        sent_result = config.map_sentiment_label(test_input)
        dist_result = config.map_distress_label(test_input)
        print(f"  Depression: {dep_result}")
        print(f"  Sentiment: {sent_result}")
        print(f"  Distress: {dist_result}")

if __name__ == "__main__":
    debug_labels()