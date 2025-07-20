#!/usr/bin/env python3
"""
Threshold Tuning Helper for Ash NLP Service
Analyzes test results and suggests optimal thresholds
"""

import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from collections import defaultdict
import itertools

class ThresholdOptimizer:
    def __init__(self, csv_file: str = "test_results.csv"):
        self.csv_file = csv_file
        self.test_data = []
        self.load_test_data()
    
    def load_test_data(self):
        """Load test results from CSV"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.test_data = list(reader)
                print(f"✅ Loaded {len(self.test_data)} test results from {self.csv_file}")
        except FileNotFoundError:
            print(f"❌ Test results file {self.csv_file} not found. Run the testing script first.")
            self.test_data = []
    
    def analyze_confidence_distribution(self):
        """Analyze the distribution of confidence scores"""
        if not self.test_data:
            return
        
        # Group by expected level
        levels = defaultdict(list)
        for row in self.test_data:
            expected = row['expected']
            confidence = float(row['confidence'])
            levels[expected].append(confidence)
        
        print("\n📊 CONFIDENCE SCORE DISTRIBUTION")
        print("=" * 50)
        
        for level in ['none', 'low', 'medium', 'high']:
            if level in levels:
                scores = levels[level]
                print(f"\n{level.upper()}:")
                print(f"  Count: {len(scores)}")
                print(f"  Min: {min(scores):.3f}")
                print(f"  Max: {max(scores):.3f}")
                print(f"  Mean: {np.mean(scores):.3f}")
                print(f"  Median: {np.median(scores):.3f}")
                print(f"  Std: {np.std(scores):.3f}")
                
                # Show percentiles
                p25, p75 = np.percentile(scores, [25, 75])
                print(f"  25th percentile: {p25:.3f}")
                print(f"  75th percentile: {p75:.3f}")
    
    def find_optimal_thresholds(self) -> Tuple[float, float, float]:
        """Find optimal thresholds using grid search"""
        if not self.test_data:
            return 0.3, 0.6, 0.8
        
        print("\n🔍 FINDING OPTIMAL THRESHOLDS")
        print("=" * 50)
        
        # Extract confidence scores and expected levels
        confidences = [float(row['confidence']) for row in self.test_data]
        expected_levels = [row['expected'] for row in self.test_data]
        
        # Define threshold ranges to test
        threshold_range = np.arange(0.1, 0.95, 0.05)
        
        best_accuracy = 0
        best_thresholds = (0.3, 0.6, 0.8)
        
        print("Testing threshold combinations...")
        
        # Grid search through threshold combinations
        total_combinations = 0
        for low_thresh in threshold_range:
            for medium_thresh in threshold_range:
                for high_thresh in threshold_range:
                    # Ensure proper ordering
                    if low_thresh < medium_thresh < high_thresh:
                        total_combinations += 1
                        accuracy = self.calculate_accuracy_with_thresholds(
                            confidences, expected_levels, low_thresh, medium_thresh, high_thresh
                        )
                        
                        if accuracy > best_accuracy:
                            best_accuracy = accuracy
                            best_thresholds = (low_thresh, medium_thresh, high_thresh)
        
        print(f"Tested {total_combinations} threshold combinations")
        print(f"Best accuracy: {best_accuracy:.3f}")
        print(f"Best thresholds: low={best_thresholds[0]:.3f}, medium={best_thresholds[1]:.3f}, high={best_thresholds[2]:.3f}")
        
        return best_thresholds
    
    def calculate_accuracy_with_thresholds(self, confidences: List[float], 
                                         expected_levels: List[str],
                                         low_thresh: float, 
                                         medium_thresh: float, 
                                         high_thresh: float) -> float:
        """Calculate accuracy with given thresholds"""
        correct = 0
        total = len(confidences)
        
        for confidence, expected in zip(confidences, expected_levels):
            predicted = self.map_confidence_to_level(confidence, low_thresh, medium_thresh, high_thresh)
            if predicted == expected:
                correct += 1
        
        return correct / total if total > 0 else 0
    
    def map_confidence_to_level(self, confidence: float, 
                               low_thresh: float, 
                               medium_thresh: float, 
                               high_thresh: float) -> str:
        """Map confidence score to crisis level using thresholds"""
        if confidence >= high_thresh:
            return 'high'
        elif confidence >= medium_thresh:
            return 'medium'
        elif confidence >= low_thresh:
            return 'low'
        else:
            return 'none'
    
    def analyze_misclassifications(self):
        """Analyze misclassified cases to understand patterns"""
        if not self.test_data:
            return
        
        print("\n❌ MISCLASSIFICATION ANALYSIS")
        print("=" * 50)
        
        misclassified = [row for row in self.test_data if row['correct'] == 'False']
        
        if not misclassified:
            print("✅ No misclassifications found!")
            return
        
        print(f"Total misclassifications: {len(misclassified)}")
        
        # Group by expected vs predicted
        confusion = defaultdict(list)
        for row in misclassified:
            key = f"{row['expected']} → {row['predicted']}"
            confusion[key].append({
                'message': row['message'],
                'confidence': float(row['confidence']),
                'categories': row['categories']
            })
        
        print("\nMisclassification patterns:")
        for pattern, cases in confusion.items():
            print(f"\n{pattern}: {len(cases)} cases")
            # Show a few examples
            for i, case in enumerate(cases[:3]):  # Show max 3 examples
                print(f"  Example {i+1}: '{case['message'][:60]}...' (conf: {case['confidence']:.3f})")
    
    def generate_threshold_code(self, thresholds: Tuple[float, float, float]):
        """Generate updated code with optimal thresholds"""
        low_thresh, medium_thresh, high_thresh = thresholds
        
        code = f'''
def map_score_to_crisis_level(crisis_score):
    """Map crisis score to response level (optimized thresholds)"""
    
    # Optimized thresholds based on test data analysis
    if crisis_score >= {high_thresh:.3f}:
        return 'high'      # High confidence prediction
    elif crisis_score >= {medium_thresh:.3f}:
        return 'medium'    # Medium confidence
    elif crisis_score >= {low_thresh:.3f}:
        return 'low'       # Low confidence
    else:
        return 'none'      # No significant risk detected
'''
        
        print("\n📝 UPDATED THRESHOLD CODE")
        print("=" * 50)
        print(code)
        
        # Save to file
        with open("optimized_thresholds.py", "w") as f:
            f.write("# Optimized thresholds generated by threshold tuner\n")
            f.write(f"# Based on test data analysis\n\n")
            f.write(code)
        
        print("💾 Code saved to optimized_thresholds.py")
    
    def create_performance_report(self):
        """Create a comprehensive performance report"""
        if not self.test_data:
            print("❌ No test data available for report")
            return
        
        print("\n📈 PERFORMANCE REPORT")
        print("=" * 60)
        
        # Overall statistics
        total_tests = len(self.test_data)
        correct_tests = len([row for row in self.test_data if row['correct'] == 'True'])
        accuracy = correct_tests / total_tests if total_tests > 0 else 0
        
        print(f"Overall Performance:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Correct Predictions: {correct_tests}")
        print(f"  Accuracy: {accuracy:.3f} ({accuracy:.1%})")
        
        # Performance by category
        categories = defaultdict(lambda: {'total': 0, 'correct': 0})
        for row in self.test_data:
            cat = row['test_category']
            categories[cat]['total'] += 1
            if row['correct'] == 'True':
                categories[cat]['correct'] += 1
        
        print(f"\nPerformance by Category:")
        for cat, stats in sorted(categories.items()):
            cat_accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            print(f"  {cat}: {cat_accuracy:.3f} ({stats['correct']}/{stats['total']})")
        
        # Response time analysis
        response_times = [float(row['response_time_ms']) for row in self.test_data if row['response_time_ms']]
        if response_times:
            print(f"\nResponse Time Analysis:")
            print(f"  Average: {np.mean(response_times):.1f}ms")
            print(f"  Median: {np.median(response_times):.1f}ms")
            print(f"  95th percentile: {np.percentile(response_times, 95):.1f}ms")
            print(f"  Max: {max(response_times):.1f}ms")

def main():
    """Main optimization function"""
    print("🎯 ASH NLP THRESHOLD OPTIMIZER")
    print("=" * 60)
    
    optimizer = ThresholdOptimizer()
    
    if not optimizer.test_data:
        print("Please run the testing script first to generate test data.")
        return
    
    # Analyze current performance
    optimizer.create_performance_report()
    
    # Analyze confidence distributions
    optimizer.analyze_confidence_distribution()
    
    # Find optimal thresholds
    optimal_thresholds = optimizer.find_optimal_thresholds()
    
    # Analyze misclassifications
    optimizer.analyze_misclassifications()
    
    # Generate optimized code
    optimizer.generate_threshold_code(optimal_thresholds)
    
    print("\n🎉 OPTIMIZATION COMPLETE")
    print("=" * 60)
    print("Next steps:")
    print("1. Review the optimized thresholds above")
    print("2. Update your main.py with the new threshold function")
    print("3. Re-run tests to validate improved accuracy")
    print("4. Deploy the updated service")

if __name__ == "__main__":
    main()