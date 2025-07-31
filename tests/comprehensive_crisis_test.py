#!/usr/bin/env python3
"""
Comprehensive Three-Model Ensemble Crisis Detection Test
Tests the full spectrum of crisis levels using actual Ash Bot keywords
"""

import requests
import json
import time
from typing import Dict, List, Tuple
import sys

# Import the crisis keyword modules
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from high_crisis import get_high_crisis_keywords, check_high_crisis_match
    from medium_crisis import get_medium_crisis_keywords, check_medium_crisis_match  
    from low_crisis import get_low_crisis_keywords, check_low_crisis_match
    print("✅ Crisis keyword modules imported successfully")
except ImportError as e:
    print(f"❌ Failed to import crisis modules: {e}")
    print("Please ensure high_crisis.py, medium_crisis.py, and low_crisis.py are in the same directory")
    sys.exit(1)

class ComprehensiveCrisisTest:
    def __init__(self, base_url="http://localhost:8881"):
        self.base_url = base_url
        self.results = []
        self.stats = {
            'total_tests': 0,
            'correct_predictions': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'by_level': {
                'high': {'tested': 0, 'correct': 0, 'false_neg': 0, 'false_pos': 0},
                'medium': {'tested': 0, 'correct': 0, 'false_neg': 0, 'false_pos': 0},
                'low': {'tested': 0, 'correct': 0, 'false_neg': 0, 'false_pos': 0},
                'none': {'tested': 0, 'correct': 0, 'false_neg': 0, 'false_pos': 0}
            }
        }

    def test_message(self, message: str, expected_level: str, category: str) -> Dict:
        """Test a single message and return results"""
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                json={
                    "message": message,
                    "user_id": "test_user",
                    "channel_id": "test_channel"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                actual_level = result.get('crisis_level', 'none')
                needs_response = result.get('needs_response', False)
                confidence = result.get('confidence_score', 0.0)
                method = result.get('method', 'unknown')
                
                # Determine if prediction is correct
                is_correct = self._evaluate_prediction(expected_level, actual_level)
                
                test_result = {
                    'message': message[:100] + "..." if len(message) > 100 else message,
                    'expected_level': expected_level,
                    'actual_level': actual_level,
                    'confidence': confidence,
                    'needs_response': needs_response,
                    'method': method,
                    'category': category,
                    'is_correct': is_correct,
                    'processing_time': result.get('processing_time_ms', 0),
                    'consensus_prediction': result.get('analysis', {}).get('consensus_prediction', 'unknown'),
                    'consensus_confidence': result.get('analysis', {}).get('consensus_confidence', 0.0),
                    'individual_results': self._extract_individual_results(result)
                }
                
                self._update_stats(expected_level, actual_level, is_correct)
                return test_result
                
            else:
                return {
                    'message': message[:100],
                    'expected_level': expected_level,
                    'actual_level': 'error',
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'category': category,
                    'is_correct': False
                }
                
        except Exception as e:
            return {
                'message': message[:100],
                'expected_level': expected_level,
                'actual_level': 'error',
                'error': str(e),
                'category': category,
                'is_correct': False
            }

    def _extract_individual_results(self, result: Dict) -> Dict:
        """Extract individual model results for analysis"""
        analysis = result.get('analysis', {})
        individual = analysis.get('individual_results', {})
        
        extracted = {}
        for model_name, results in individual.items():
            if results and isinstance(results, list) and len(results) > 0:
                top_result = max(results, key=lambda x: x.get('score', 0))
                extracted[model_name] = {
                    'label': top_result.get('label', 'unknown'),
                    'score': top_result.get('score', 0.0),
                    'raw_label': top_result.get('raw_label', '')[:50] + "..."
                }
        
        return extracted

    def _evaluate_prediction(self, expected: str, actual: str) -> bool:
        """Evaluate if the prediction is acceptable"""
        # Exact match is always correct
        if expected == actual:
            return True
        
        # Define acceptable ranges for each expected level
        acceptable_ranges = {
            'high': ['high', 'medium'],  # High can be medium (slight under-estimate OK)
            'medium': ['high', 'medium', 'low'],  # Medium has more flexibility
            'low': ['medium', 'low'],  # Low can be medium (slight over-estimate OK)
            'none': ['none', 'low']  # None can be low (slight over-estimate OK for safety)
        }
        
        return actual in acceptable_ranges.get(expected, [expected])

    def _update_stats(self, expected: str, actual: str, is_correct: bool):
        """Update test statistics"""
        self.stats['total_tests'] += 1
        self.stats['by_level'][expected]['tested'] += 1
        
        if is_correct:
            self.stats['correct_predictions'] += 1
            self.stats['by_level'][expected]['correct'] += 1
        else:
            # Determine if it's false positive or false negative
            level_hierarchy = {'none': 0, 'low': 1, 'medium': 2, 'high': 3}
            expected_num = level_hierarchy.get(expected, 0)
            actual_num = level_hierarchy.get(actual, 0)
            
            if actual_num > expected_num:
                self.stats['false_positives'] += 1
                self.stats['by_level'][expected]['false_pos'] += 1
            else:
                self.stats['false_negatives'] += 1
                self.stats['by_level'][expected]['false_neg'] += 1

    def test_high_crisis_keywords(self):
        """Test HIGH crisis level keywords"""
        print("\n🔴 TESTING HIGH CRISIS KEYWORDS")
        print("=" * 60)
        
        high_keywords = get_high_crisis_keywords()
        test_phrases = [
            # Direct suicidal ideation
            "I want to kill myself right now",
            "I'm going to end it all tonight", 
            "I have a plan to take my own life",
            "I'm ready to die, I can't go on",
            "I'm better off dead, everyone would be happier",
            
            # Self-harm with urgency
            "I need to cut myself deeper tonight",
            "I'm going to hurt myself with a razor blade",
            "I deserve this pain, I'm going to burn myself",
            
            # Immediate danger
            "I have the pills ready, this is my final message",
            "The rope is tied, I'm done with this life",
            "I've written my suicide note, goodbye everyone",
            "Tonight's the night, I can't wait anymore",
            
            # Severe hopelessness
            "There's no way out, I'm too broken to fix",
            "I'm beyond help, nothing can save me now",
            "I'm past saving, too far gone for help"
        ]
        
        for phrase in test_phrases:
            result = self.test_message(phrase, 'high', 'high_crisis_direct')
            self.results.append(result)
            self._print_test_result(result)
            time.sleep(0.5)  # Rate limiting

    def test_medium_crisis_keywords(self):
        """Test MEDIUM crisis level keywords"""
        print("\n🟡 TESTING MEDIUM CRISIS KEYWORDS")
        print("=" * 60)
        
        test_phrases = [
            # Severe emotional distress
            "I'm having a complete mental breakdown right now",
            "I'm falling apart and can't stop crying",
            "Everything is crashing down, I'm losing my mind",
            "I'm at my breaking point, can't handle this anymore",
            
            # Severe depression episodes
            "I'm in a deep depression spiral, can't get out of bed",
            "I feel completely empty inside, life has no meaning",
            "What's the point of anything, nothing matters anymore",
            
            # Panic attacks
            "I'm having a panic attack, can't breathe or think",
            "My heart is racing, I think I'm dying right now",
            "I'm hyperventilating and shaking uncontrollably",
            
            # Trauma responses
            "I'm having PTSD flashbacks, reliving my trauma",
            "I'm dissociating badly, feeling out of my body",
            "The abuse memories are flooding back, I'm triggered",
            
            # Concerning ideation (medium level)
            "Sometimes I think about not existing anymore",
            "I wonder if everyone would be better off without me",
            "I'm tired of fighting, wouldn't mind not waking up"
        ]
        
        for phrase in test_phrases:
            result = self.test_message(phrase, 'medium', 'medium_crisis_direct')
            self.results.append(result)
            self._print_test_result(result)
            time.sleep(0.5)

    def test_low_crisis_keywords(self):
        """Test LOW crisis level keywords"""
        print("\n🟢 TESTING LOW CRISIS KEYWORDS")
        print("=" * 60)
        
        test_phrases = [
            # Depression symptoms
            "I'm feeling really depressed and down lately",
            "I've lost interest in things I used to enjoy",
            "I'm struggling with my mental health right now",
            "I feel emotionally numb and empty inside",
            
            # Anxiety symptoms
            "I'm really stressed and anxious about everything",
            "I'm having panic about my job interview tomorrow",
            "My social anxiety is making it hard to leave the house",
            
            # Identity struggles
            "I'm questioning my identity and don't know who I am",
            "I'm struggling with low self-esteem and feeling worthless",
            "I have imposter syndrome and feel like a fraud",
            
            # LGBTQIA+ struggles
            "I'm struggling with coming out to my family",
            "I'm dealing with gender dysphoria and it's hard",
            "My parents don't accept my sexuality and it hurts",
            
            # Daily functioning
            "I can't get motivated to do anything productive",
            "My executive dysfunction is making everything hard",
            "I'm procrastinating on all my responsibilities"
        ]
        
        for phrase in test_phrases:
            result = self.test_message(phrase, 'low', 'low_crisis_direct')
            self.results.append(result)
            self._print_test_result(result)
            time.sleep(0.5)

    def test_none_level_phrases(self):
        """Test phrases that should NOT trigger crisis detection"""
        print("\n⚪ TESTING NON-CRISIS PHRASES")
        print("=" * 60)
        
        test_phrases = [
            # Normal conversation
            "Hey everyone, how's your day going?",
            "I'm excited about the new movie coming out",
            "Thanks for helping me with my homework",
            "The weather is really nice today",
            
            # Positive expressions
            "I'm feeling great and looking forward to the weekend",
            "I love spending time with my friends and family",
            "I just got accepted to my dream college!",
            
            # Mild complaints (should not trigger)
            "I'm tired after a long day at work",
            "This assignment is really challenging",
            "I'm not looking forward to Monday morning",
            
            # Casual expressions with potentially triggering words
            "I'm dying to see that new show everyone's talking about",
            "This traffic is killing me, I'm going to be late",
            "I'm dead tired after staying up all night studying",
            "I could just die of embarrassment right now"
        ]
        
        for phrase in test_phrases:
            result = self.test_message(phrase, 'none', 'normal_conversation')
            self.results.append(result)
            self._print_test_result(result)
            time.sleep(0.5)

    def test_edge_cases(self):
        """Test edge cases and potentially confusing phrases"""
        print("\n🔍 TESTING EDGE CASES")
        print("=" * 60)
        
        test_phrases = [
            # Fictional/gaming references
            ("My character died in the game, so frustrating", 'none'),
            ("I'm going to kill the boss in this level", 'none'),
            ("This movie is about someone planning suicide", 'none'),
            
            # Academic/professional discussions
            ("I'm studying suicide prevention for my psychology class", 'none'),
            ("We're discussing self-harm in our therapy training", 'none'),
            ("The research focuses on depression treatment methods", 'none'),
            
            # Ambiguous expressions
            ("I feel like I'm dying inside from this heartbreak", 'low'),
            ("I want to disappear from social media for a while", 'none'),
            ("I can't handle one more assignment this week", 'low'),
            
            # Metaphorical usage
            ("This diet is killing me, but I need to lose weight", 'none'),
            ("I'm dead serious about finishing this project", 'none'),
            ("I could murder a pizza right now, I'm so hungry", 'none')
        ]
        
        for phrase, expected_level in test_phrases:
            result = self.test_message(phrase, expected_level, 'edge_case')
            self.results.append(result)
            self._print_test_result(result)
            time.sleep(0.5)

    def _print_test_result(self, result: Dict):
        """Print a formatted test result"""
        status = "✅" if result['is_correct'] else "❌"
        expected = result['expected_level'].upper()
        actual = result['actual_level'].upper()
        confidence = result.get('confidence', 0)
        
        print(f"{status} {expected} → {actual} ({confidence:.3f}) | {result['message']}")
        
        if not result['is_correct'] and 'error' not in result:
            # Show individual model results for incorrect predictions
            individual = result.get('individual_results', {})
            print(f"   Models: ", end="")
            for model, data in individual.items():
                print(f"{model}={data['label']}({data['score']:.2f}) ", end="")
            print()

    def print_final_statistics(self):
        """Print comprehensive test statistics"""
        print("\n" + "="*80)
        print("🏆 COMPREHENSIVE THREE-MODEL ENSEMBLE TEST RESULTS")
        print("="*80)
        
        total = self.stats['total_tests']
        correct = self.stats['correct_predictions']
        accuracy = (correct / total * 100) if total > 0 else 0
        
        print(f"\n📊 OVERALL PERFORMANCE:")
        print(f"   Total Tests: {total}")
        print(f"   Correct Predictions: {correct}")
        print(f"   Overall Accuracy: {accuracy:.1f}%")
        print(f"   False Positives: {self.stats['false_positives']}")
        print(f"   False Negatives: {self.stats['false_negatives']}")
        
        print(f"\n📈 PERFORMANCE BY CRISIS LEVEL:")
        for level, stats in self.stats['by_level'].items():
            if stats['tested'] > 0:
                level_accuracy = (stats['correct'] / stats['tested'] * 100)
                print(f"   {level.upper()}: {stats['correct']}/{stats['tested']} correct ({level_accuracy:.1f}%)")
                if stats['false_pos'] > 0:
                    print(f"      False Positives: {stats['false_pos']}")
                if stats['false_neg'] > 0:
                    print(f"      False Negatives: {stats['false_neg']}")
        
        # Safety assessment
        safety_score = self._calculate_safety_score()
        print(f"\n🛡️ SAFETY ASSESSMENT:")
        print(f"   Safety Score: {safety_score:.1f}%")
        print(f"   Critical Miss Rate: {self._calculate_critical_miss_rate():.1f}%")
        
        # Recommendations
        self._print_recommendations()

    def _calculate_safety_score(self) -> float:
        """Calculate safety score (high weight on not missing crises)"""
        high_stats = self.stats['by_level']['high']
        medium_stats = self.stats['by_level']['medium']
        
        # Weight: Missing high crisis = -10 points, missing medium = -5 points
        # False positive = -1 point each
        
        total_possible = 100
        penalties = 0
        
        penalties += high_stats['false_neg'] * 10  # Missing high crisis is critical
        penalties += medium_stats['false_neg'] * 5  # Missing medium crisis is serious
        penalties += self.stats['false_positives'] * 1  # False positives are annoying but not dangerous
        
        return max(0, total_possible - penalties)

    def _calculate_critical_miss_rate(self) -> float:
        """Calculate rate of missing critical (high/medium) crises"""
        high_stats = self.stats['by_level']['high']
        medium_stats = self.stats['by_level']['medium']
        
        total_critical = high_stats['tested'] + medium_stats['tested']
        missed_critical = high_stats['false_neg'] + medium_stats['false_neg']
        
        return (missed_critical / total_critical * 100) if total_critical > 0 else 0

    def _print_recommendations(self):
        """Print recommendations based on test results"""
        print(f"\n💡 RECOMMENDATIONS:")
        
        # Check for high false negative rate
        critical_miss_rate = self._calculate_critical_miss_rate()
        if critical_miss_rate > 10:
            print(f"   ⚠️ High critical miss rate ({critical_miss_rate:.1f}%) - consider lowering thresholds")
        
        # Check for high false positive rate
        fp_rate = (self.stats['false_positives'] / self.stats['total_tests'] * 100)
        if fp_rate > 20:
            print(f"   ⚠️ High false positive rate ({fp_rate:.1f}%) - consider raising thresholds")
        
        # Check individual level performance
        for level, stats in self.stats['by_level'].items():
            if stats['tested'] > 0:
                accuracy = (stats['correct'] / stats['tested'] * 100)
                if accuracy < 70 and level in ['high', 'medium']:
                    print(f"   ⚠️ Low {level} crisis accuracy ({accuracy:.1f}%) - review {level}-level detection")
        
        # Overall assessment
        overall_accuracy = (self.stats['correct_predictions'] / self.stats['total_tests'] * 100)
        if overall_accuracy > 85:
            print(f"   ✅ Excellent overall performance ({overall_accuracy:.1f}%)")
        elif overall_accuracy > 75:
            print(f"   👍 Good overall performance ({overall_accuracy:.1f}%)")
        else:
            print(f"   👎 Performance needs improvement ({overall_accuracy:.1f}%)")

    def run_comprehensive_test(self):
        """Run the complete test suite"""
        print("🚀 STARTING COMPREHENSIVE THREE-MODEL ENSEMBLE TEST")
        print("📊 Testing crisis detection across all levels...")
        print(f"🎯 Target: {self.base_url}")
        print(f"📁 Working directory: {os.getcwd()}")
        
        # Test server connectivity first
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Server healthy - Models loaded: {health_data.get('model_loaded', False)}")
            else:
                print(f"⚠️ Server responded with status {response.status_code}")
        except Exception as e:
            print(f"❌ Server connectivity issue: {e}")
            print("Please ensure the NLP server is running at", self.base_url)
            return None, None
        
        start_time = time.time()
        
        # Run all test categories
        self.test_high_crisis_keywords()
        self.test_medium_crisis_keywords()
        self.test_low_crisis_keywords()
        self.test_none_level_phrases()
        self.test_edge_cases()
        
        end_time = time.time()
        
        # Print final results
        self.print_final_statistics()
        
        print(f"\n⏱️ Total test time: {end_time - start_time:.1f} seconds")
        
        # Save results with timestamp in filename
        timestamp = int(time.time())
        results_file = f'comprehensive_test_results_{timestamp}.json'
        
        with open(results_file, 'w') as f:
            json.dump({
                'results': self.results,
                'stats': self.stats,
                'timestamp': time.time(),
                'test_duration': end_time - start_time,
                'server_url': self.base_url
            }, f, indent=2)
        
        print(f"📝 Detailed results saved to: {results_file}")
        
        return self.results, self.stats

def main():
    """Run the comprehensive crisis detection test"""
    print("🎯 Comprehensive Three-Model Ensemble Crisis Detection Test")
    print("=" * 60)
    
    # Default to localhost (works from inside Docker container)
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8881"
    
    print(f"📡 Testing server at: {base_url}")
    print(f"📂 Test files location: {os.path.dirname(os.path.abspath(__file__))}")
    
    tester = ComprehensiveCrisisTest(base_url)
    results, stats = tester.run_comprehensive_test()
    
    if results is None:
        print("❌ Test aborted due to server connectivity issues")
        return False
    
    # Calculate success threshold
    accuracy = stats['correct_predictions'] / stats['total_tests'] if stats['total_tests'] > 0 else 0
    critical_miss_rate = tester._calculate_critical_miss_rate()
    
    print(f"\n🏆 FINAL ASSESSMENT:")
    print(f"   Overall Accuracy: {accuracy*100:.1f}%")
    print(f"   Critical Miss Rate: {critical_miss_rate:.1f}%")
    
    # Success criteria: >80% accuracy AND <10% critical miss rate
    success = accuracy > 0.8 and critical_miss_rate < 10
    
    if success:
        print("   🎉 TEST PASSED - System ready for production!")
    else:
        print("   ⚠️ TEST NEEDS ATTENTION - Review thresholds and model performance")
        if accuracy <= 0.8:
            print(f"      - Overall accuracy too low ({accuracy*100:.1f}% < 80%)")
        if critical_miss_rate >= 10:
            print(f"      - Critical miss rate too high ({critical_miss_rate:.1f}% >= 10%)")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)