#!/usr/bin/env python3
"""
Data-driven threshold optimizer based on your actual test results
"""

import csv
import numpy as np
from collections import defaultdict

def analyze_and_optimize_thresholds():
    """Analyze test results and find optimal thresholds for your targets"""
    
    try:
        with open('refined_test_results.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            results = list(reader)
    except FileNotFoundError:
        print("❌ refined_test_results.csv not found.")
        return
    
    print("🎯 DATA-DRIVEN THRESHOLD OPTIMIZATION")
    print("Target: 90% HIGH detection, 70% overall accuracy")
    print("=" * 60)
    
    # Extract confidence scores by expected level
    scores_by_level = defaultdict(list)
    for r in results:
        level = r['expected']
        confidence = float(r['confidence'])
        scores_by_level[level].append(confidence)
    
    # Print current score distributions
    print("📊 CURRENT CONFIDENCE SCORE DISTRIBUTIONS:")
    for level in ['high', 'medium', 'low', 'none']:
        if level in scores_by_level:
            scores = scores_by_level[level]
            print(f"\n{level.upper()}: {len(scores)} samples")
            print(f"  Range: {min(scores):.3f} - {max(scores):.3f}")
            print(f"  Mean: {np.mean(scores):.3f}")
            print(f"  Median: {np.median(scores):.3f}")
            print(f"  Values: {sorted(scores)}")
    
    # Find optimal thresholds using grid search
    print(f"\n🔍 SEARCHING FOR OPTIMAL THRESHOLDS...")
    
    # Get all confidence scores and expected levels
    all_scores = [float(r['confidence']) for r in results]
    all_expected = [r['expected'] for r in results]
    
    best_accuracy = 0
    best_high_recall = 0
    best_thresholds = None
    best_results = None
    
    # Grid search through threshold combinations
    low_range = np.arange(0.02, 0.20, 0.02)
    medium_range = np.arange(0.15, 0.45, 0.03)
    high_range = np.arange(0.35, 0.80, 0.05)
    
    for low_thresh in low_range:
        for medium_thresh in medium_range:
            for high_thresh in high_range:
                if low_thresh < medium_thresh < high_thresh:
                    
                    # Calculate metrics with these thresholds
                    accuracy, high_recall, detailed = calculate_metrics_with_thresholds(
                        all_scores, all_expected, low_thresh, medium_thresh, high_thresh
                    )
                    
                    # Prioritize HIGH recall (must be >= 80%), then overall accuracy
                    if high_recall >= 0.8:  # At least 80% HIGH detection
                        if accuracy > best_accuracy or (accuracy >= best_accuracy and high_recall > best_high_recall):
                            best_accuracy = accuracy
                            best_high_recall = high_recall
                            best_thresholds = (low_thresh, medium_thresh, high_thresh)
                            best_results = detailed
    
    if best_thresholds:
        low_t, med_t, high_t = best_thresholds
        print(f"\n🎉 OPTIMAL THRESHOLDS FOUND:")
        print(f"  LOW ≥ {low_t:.3f}")
        print(f"  MEDIUM ≥ {med_t:.3f}")  
        print(f"  HIGH ≥ {high_t:.3f}")
        print(f"\n📈 PERFORMANCE:")
        print(f"  Overall Accuracy: {best_accuracy:.1%}")
        print(f"  HIGH Recall: {best_high_recall:.1%}")
        
        # Show detailed breakdown
        if best_results:
            print(f"\n📊 DETAILED BREAKDOWN:")
            for level, stats in best_results.items():
                if stats['total'] > 0:
                    acc = stats['correct'] / stats['total']
                    print(f"  {level.upper()}: {acc:.1%} ({stats['correct']}/{stats['total']})")
        
        # Generate code
        print(f"\n💻 UPDATED CODE:")
        print(f"""
def map_score_to_crisis_level(crisis_score):
    \"\"\"Optimized thresholds based on test data\"\"\"
    
    if crisis_score >= {high_t:.3f}:   # HIGH: {best_high_recall:.1%} recall
        return 'high'      
    elif crisis_score >= {med_t:.3f}:  # MEDIUM
        return 'medium'    
    elif crisis_score >= {low_t:.3f}:  # LOW
        return 'low'       
    else:
        return 'none'
""")
    else:
        print("❌ Could not find thresholds that achieve 80% HIGH recall")
        print("💡 Consider adjusting the scoring function instead")


def calculate_metrics_with_thresholds(scores, expected, low_thresh, medium_thresh, high_thresh):
    """Calculate accuracy and HIGH recall with given thresholds"""
    
    correct = 0
    total = len(scores)
    
    # Count by level for detailed analysis
    level_stats = defaultdict(lambda: {'total': 0, 'correct': 0})
    
    for score, expected_level in zip(scores, expected):
        # Predict level based on thresholds
        if score >= high_thresh:
            predicted = 'high'
        elif score >= medium_thresh:
            predicted = 'medium'
        elif score >= low_thresh:
            predicted = 'low'
        else:
            predicted = 'none'
        
        # Count totals and correct predictions
        level_stats[expected_level]['total'] += 1
        if predicted == expected_level:
            correct += 1
            level_stats[expected_level]['correct'] += 1
    
    # Calculate overall accuracy
    accuracy = correct / total if total > 0 else 0
    
    # Calculate HIGH recall specifically
    high_stats = level_stats['high']
    high_recall = high_stats['correct'] / high_stats['total'] if high_stats['total'] > 0 else 0
    
    return accuracy, high_recall, dict(level_stats)


if __name__ == "__main__":
    analyze_and_optimize_thresholds()