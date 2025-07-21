#!/usr/bin/env python3
"""
Analyze the test failures in detail to understand what's going wrong
"""

import csv
from collections import defaultdict

def analyze_test_failures():
    """Analyze the actual test results to understand the issues"""
    
    try:
        with open('refined_test_results.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            results = list(reader)
    except FileNotFoundError:
        print("❌ refined_test_results.csv not found.")
        return
    
    print("🔍 DETAILED FAILURE ANALYSIS")
    print("=" * 60)
    
    # Separate by correctness
    failures = [r for r in results if r['correct'] == 'False']
    successes = [r for r in results if r['correct'] == 'True']
    
    print(f"Total Results: {len(results)}")
    print(f"Successes: {len(successes)} ({len(successes)/len(results)*100:.1f}%)")
    print(f"Failures: {len(failures)} ({len(failures)/len(results)*100:.1f}%)")
    
    # Analyze failures by expected level
    failure_by_level = defaultdict(list)
    for f in failures:
        failure_by_level[f['expected']].append(f)
    
    print(f"\n📊 FAILURES BY EXPECTED LEVEL:")
    
    for level in ['high', 'medium', 'low', 'none']:
        if level in failure_by_level:
            level_failures = failure_by_level[level]
            print(f"\n{level.upper()} Failures: {len(level_failures)}")
            
            for f in level_failures:
                conf = float(f['confidence'])
                message_short = f['message'][:40] + "..." if len(f['message']) > 40 else f['message']
                print(f"  '{message_short}' → {f['predicted']} (conf: {conf:.3f})")
    
    # Show confidence score distributions for all levels
    print(f"\n📈 CONFIDENCE SCORE DISTRIBUTIONS:")
    
    by_expected = defaultdict(list)
    for r in results:
        by_expected[r['expected']].append(float(r['confidence']))
    
    for level in ['high', 'medium', 'low', 'none']:
        if level in by_expected:
            scores = by_expected[level]
            print(f"\n{level.upper()}: {len(scores)} samples")
            print(f"  Range: {min(scores):.3f} - {max(scores):.3f}")
            print(f"  Mean: {sum(scores)/len(scores):.3f}")
            print(f"  Sorted: {sorted(scores)}")
    
    # Identify specific problem areas
    print(f"\n🚨 CRITICAL ISSUES:")
    
    # MEDIUM failures are the biggest problem (10% accuracy)
    medium_failures = failure_by_level.get('medium', [])
    if medium_failures:
        print(f"\nMEDIUM failures ({len(medium_failures)}/10):")
        medium_scores = [float(f['confidence']) for f in medium_failures]
        print(f"  Failed MEDIUM scores: {sorted(medium_scores)}")
        print(f"  These should be ≥0.40 but are probably <0.40")
    
    # HIGH failures
    high_failures = failure_by_level.get('high', [])
    if high_failures:
        print(f"\nHIGH failures ({len(high_failures)}/5):")
        high_scores = [float(f['confidence']) for f in high_failures]
        print(f"  Failed HIGH scores: {sorted(high_scores)}")
        print(f"  These should be ≥0.70 but are probably <0.70")
    
    # False positives (NONE predicted as crisis)
    false_positives = [f for f in failures if f['expected'] == 'none' and f['predicted'] != 'none']
    if false_positives:
        print(f"\nFALSE POSITIVES ({len(false_positives)}):")
        for fp in false_positives:
            conf = float(fp['confidence'])
            message_short = fp['message'][:40] + "..." if len(fp['message']) > 40 else fp['message']
            print(f"  '{message_short}' → {fp['predicted']} (conf: {conf:.3f})")
    
    # Suggest threshold adjustments
    print(f"\n💡 THRESHOLD ANALYSIS:")
    print(f"Current: HIGH≥0.70, MEDIUM≥0.40, LOW≥0.15")
    
    # Find optimal thresholds based on actual data
    all_scores = [(float(r['confidence']), r['expected']) for r in results]
    
    # Find score ranges that would work better
    high_scores = [score for score, expected in all_scores if expected == 'high']
    medium_scores = [score for score, expected in all_scores if expected == 'medium']
    none_scores = [score for score, expected in all_scores if expected == 'none']
    
    if high_scores and medium_scores:
        min_high = min(high_scores)
        max_medium = max(medium_scores)
        print(f"  Actual HIGH range: {min(high_scores):.3f} - {max(high_scores):.3f}")
        print(f"  Actual MEDIUM range: {min(medium_scores):.3f} - {max(medium_scores):.3f}")
        
        if min_high < 0.70:
            print(f"  ⚠️  Some HIGH scores ({min_high:.3f}) are below HIGH threshold (0.70)")
        if max_medium < 0.40:
            print(f"  ⚠️  Some MEDIUM scores ({max_medium:.3f}) are below MEDIUM threshold (0.40)")

if __name__ == "__main__":
    analyze_test_failures()