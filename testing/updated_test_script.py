#!/usr/bin/env python3
"""
Updated Testing Script with Refined Labels
Focuses on genuine mental health concerns vs normal emotions/idioms
"""

import requests
import json
import time
import statistics
from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv
from datetime import datetime

# Configuration
NLP_SERVICE_URL = "http://localhost:8881"
TEST_DATA_FILE = "refined_test_results.csv"
DETAILED_LOG_FILE = "refined_detailed_test_log.txt"

@dataclass
class TestCase:
    message: str
    expected_level: str  # 'none', 'low', 'medium', 'high'
    category: str  # For grouping results
    description: str = ""

def create_refined_test_cases() -> List[TestCase]:
    """Create refined test cases focusing on mental health vs normal emotions"""
    
    test_cases = [
        # HIGH CRISIS LEVEL - Clear mental health crisis
        TestCase("I want to kill myself", "high", "direct_suicide", "Direct suicide ideation"),
        TestCase("I can't take it anymore, I'm going to end it all", "high", "direct_suicide", "Suicide with emotional context"),
        TestCase("Nobody would miss me if I was gone", "high", "suicide_ideation", "Passive suicide ideation"),
        TestCase("I have a plan to hurt myself tonight", "high", "self_harm_plan", "Specific self-harm plan"),
        TestCase("Life isn't worth living anymore", "high", "hopelessness", "Severe hopelessness"),
        
        # MEDIUM CRISIS LEVEL - Serious mental health concerns
        TestCase("I feel so depressed, everything is hopeless", "medium", "depression", "Depression with hopelessness"),
        TestCase("I hate myself so much", "medium", "self_hatred", "Self-hatred expression"),
        TestCase("I wish I could just disappear", "medium", "escape_ideation", "Escape/disappearance wishes"),
        TestCase("I'm so tired of everything, I can't go on", "medium", "exhaustion", "Emotional exhaustion"),
        TestCase("Maybe everyone would be better off without me", "medium", "burden_thoughts", "Feeling like a burden"),
        TestCase("Everything feels pointless", "medium", "meaninglessness", "Sense of meaninglessness"),
        TestCase("Sometimes I think about not being here", "medium", "suicide_ideation", "Borderline suicide ideation"),
        TestCase("I want the pain to stop", "medium", "pain_relief", "Pain relief desire"),
        TestCase("I'm at my breaking point", "medium", "breaking_point", "Breaking point expression"),
        TestCase("Nothing matters anymore", "medium", "nihilism", "Nihilistic thinking"),
        
        # LOW CRISIS LEVEL - Mild mental health indicators (genuine distress)
        TestCase("I don't know what to do anymore", "low", "confusion", "General confusion/helplessness"),
        TestCase("I'm lost", "low", "lost_feeling", "Feeling lost (metaphorically)"),
        TestCase("I give up", "low", "giving_up", "Giving up expression"),
        TestCase("I'm really struggling right now", "low", "struggle", "General struggle"),
        TestCase("I feel like I'm drowning", "low", "drowning_metaphor", "Metaphorical drowning"),
        TestCase("I can't handle this anymore", "low", "overwhelm", "Overwhelm expression"),
        TestCase("I feel empty inside", "low", "emptiness", "Emptiness feeling"),
        TestCase("I'm disappointed in myself", "low", "self_disappointment", "Self-disappointment"),
        
        # NONE - Normal emotions, daily stress, idioms (NOT mental health crises)
        TestCase("What's the weather like today?", "none", "neutral", "Weather question"),
        TestCase("I love pizza so much!", "none", "positive", "Food enthusiasm"),
        TestCase("Going to watch a movie tonight", "none", "neutral", "Activity plan"),
        TestCase("Thanks for helping me with that", "none", "gratitude", "Expressing thanks"),
        TestCase("How was your day?", "none", "social", "Social inquiry"),
        
        # NONE - Idioms and expressions (HIGH PRIORITY to get right)
        TestCase("I'm dying of laughter", "none", "idiom", "Positive idiom with 'dying'"),
        TestCase("This homework is killing me", "none", "hyperbole", "Hyperbolic expression"),
        TestCase("I'm dead tired", "none", "tired_idiom", "Tiredness idiom"),
        TestCase("I could murder a burger right now", "none", "food_hyperbole", "Food craving hyperbole"),
        TestCase("That joke killed me", "none", "humor_idiom", "Humor expression"),
        
        # NONE - Normal daily emotions (NOT mental health concerns)
        TestCase("I'm feeling really sad today", "none", "normal_sadness", "Normal temporary sadness"),
        TestCase("Having a bad day, everything sucks", "none", "bad_day", "Temporary negative mood"),
        TestCase("I'm so stressed about work", "none", "work_stress", "Normal work-related stress"),
        TestCase("I feel anxious about tomorrow", "none", "normal_anxiety", "Normal situational anxiety"),
        
        # EDGE CASES - Borderline cases for threshold testing
        TestCase("I feel like I'm drowning in work", "none", "work_metaphor", "Work overwhelm metaphor"),
        TestCase("This project is killing my motivation", "none", "motivation_hyperbole", "Motivation hyperbole"),
        TestCase("I'm struggling with this decision", "low", "decision_struggle", "Decision difficulty"),
        TestCase("I feel overwhelmed lately", "low", "general_overwhelm", "General overwhelm feeling"),
    ]
    
    return test_cases

# Rest of the testing infrastructure (same as before)
class NLPTester:
    def __init__(self, service_url: str):
        self.service_url = service_url
        self.results = []
        self.detailed_log = []
        
    def check_service_health(self) -> bool:
        """Check if the NLP service is running and healthy"""
        try:
            response = requests.get(f"{self.service_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Service Status: {health_data.get('status', 'unknown')}")
                print(f"✅ Model Loaded: {health_data.get('model_loaded', False)}")
                print(f"✅ Uptime: {health_data.get('uptime_seconds', 0):.1f}s")
                return health_data.get('model_loaded', False)
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to NLP service: {e}")
            print(f"💡 Make sure the service is running on {self.service_url}")
            return False

    def analyze_message(self, message: str) -> Dict:
        """Send a message to the NLP service for analysis"""
        try:
            payload = {
                "message": message,
                "user_id": "test_user",
                "channel_id": "test_channel"
            }
            
            response = requests.post(
                f"{self.service_url}/analyze",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Analysis failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error analyzing message: {e}")
            return None

    def run_single_test(self, test_case: TestCase) -> Dict:
        """Run a single test case and return results"""
        print(f"\n🔍 Testing: '{test_case.message[:50]}...'")
        
        start_time = time.time()
        result = self.analyze_message(test_case.message)
        response_time = (time.time() - start_time) * 1000
        
        if not result:
            return {
                "test_case": test_case,
                "success": False,
                "error": "Failed to get response from service"
            }
        
        # Extract results
        predicted_level = result.get('crisis_level', 'unknown')
        confidence = result.get('confidence_score', 0.0)
        categories = result.get('detected_categories', [])
        processing_time = result.get('processing_time_ms', 0.0)
        
        # Check if prediction matches expected
        correct = predicted_level == test_case.expected_level
        
        # Log detailed results
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': test_case.message,
            'expected': test_case.expected_level,
            'predicted': predicted_level,
            'confidence': confidence,
            'categories': categories,
            'correct': correct,
            'response_time_ms': response_time,
            'processing_time_ms': processing_time,
            'test_category': test_case.category,
            'description': test_case.description
        }
        
        self.detailed_log.append(log_entry)
        
        # Print results
        status_icon = "✅" if correct else "❌"
        print(f"{status_icon} Expected: {test_case.expected_level} | Predicted: {predicted_level} | Confidence: {confidence:.3f}")
        print(f"   Categories: {categories}")
        print(f"   Response Time: {response_time:.1f}ms | Processing: {processing_time:.1f}ms")
        
        return {
            "test_case": test_case,
            "result": result,
            "correct": correct,
            "response_time_ms": response_time,
            "success": True
        }

    def run_test_suite(self, test_cases: List[TestCase]) -> Dict:
        """Run a full test suite and return summary statistics"""
        print(f"\n🚀 Running REFINED test suite with {len(test_cases)} test cases...")
        print("🎯 Focus: Mental health concerns vs normal emotions/idioms")
        print("=" * 60)
        
        if not self.check_service_health():
            return {"error": "Service not healthy"}
        
        results = []
        correct_predictions = 0
        total_response_time = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}]", end=" ")
            
            result = self.run_single_test(test_case)
            results.append(result)
            
            if result.get('success') and result.get('correct'):
                correct_predictions += 1
            
            if result.get('response_time_ms'):
                total_response_time += result['response_time_ms']
            
            # Small delay to avoid overwhelming the service
            time.sleep(0.1)
        
        # Calculate statistics
        accuracy = correct_predictions / len(test_cases) if test_cases else 0
        avg_response_time = total_response_time / len(test_cases) if test_cases else 0
        
        # Group results by expected level
        level_stats = {}
        for result in results:
            if result.get('success'):
                expected = result['test_case'].expected_level
                if expected not in level_stats:
                    level_stats[expected] = {'total': 0, 'correct': 0}
                level_stats[expected]['total'] += 1
                if result.get('correct'):
                    level_stats[expected]['correct'] += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 REFINED TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Overall Accuracy: {accuracy:.1%} ({correct_predictions}/{len(test_cases)})")
        print(f"Average Response Time: {avg_response_time:.1f}ms")
        
        print("\n📈 Accuracy by Crisis Level:")
        for level in ['HIGH', 'MEDIUM', 'LOW', 'NONE']:
            level_key = level.lower()
            if level_key in level_stats:
                stats = level_stats[level_key]
                level_accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
                print(f"  {level}: {level_accuracy:.1%} ({stats['correct']}/{stats['total']})")
        
        # Special analysis for idioms/false positives
        idiom_cases = [r for r in results if r.get('success') and 'idiom' in r['test_case'].category]
        if idiom_cases:
            idiom_correct = sum(1 for r in idiom_cases if r.get('correct'))
            idiom_accuracy = idiom_correct / len(idiom_cases) if idiom_cases else 0
            print(f"\n🎯 IDIOM/FALSE POSITIVE Detection: {idiom_accuracy:.1%} ({idiom_correct}/{len(idiom_cases)})")
        
        return {
            "overall_accuracy": accuracy,
            "correct_predictions": correct_predictions,
            "total_tests": len(test_cases),
            "avg_response_time_ms": avg_response_time,
            "level_stats": level_stats,
            "detailed_results": results
        }

    def save_results(self, summary: Dict):
        """Save test results to files"""
        # Save detailed log
        with open(DETAILED_LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("REFINED TEST LOG - Mental Health vs Normal Emotions\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")
            
            for entry in self.detailed_log:
                f.write(f"Timestamp: {entry['timestamp']}\n")
                f.write(f"Message: {entry['message']}\n")
                f.write(f"Expected: {entry['expected']} | Predicted: {entry['predicted']}\n")
                f.write(f"Confidence: {entry['confidence']:.3f}\n")
                f.write(f"Categories: {entry['categories']}\n")
                f.write(f"Correct: {entry['correct']}\n")
                f.write(f"Response Time: {entry['response_time_ms']:.1f}ms\n")
                f.write(f"Description: {entry['description']}\n")
                f.write("-" * 40 + "\n\n")
        
        # Save CSV for analysis
        with open(TEST_DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'message', 'expected', 'predicted', 'confidence', 
                         'categories', 'correct', 'response_time_ms', 'processing_time_ms',
                         'test_category', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in self.detailed_log:
                # Convert categories list to string for CSV and ensure all fields are present
                entry_copy = entry.copy()
                entry_copy['categories'] = '; '.join(entry.get('categories', []))
                
                # Ensure all required fields exist with defaults
                for field in fieldnames:
                    if field not in entry_copy:
                        entry_copy[field] = 0 if 'time_ms' in field else ''
                
                writer.writerow(entry_copy)
        
        print(f"\n💾 Results saved to:")
        print(f"  📄 Detailed log: {DETAILED_LOG_FILE}")
        print(f"  📊 CSV data: {TEST_DATA_FILE}")

def main():
    """Main testing function with refined test cases"""
    print("🧪 ASH NLP SERVICE REFINED TESTING")
    print("🎯 Focus: Mental Health Detection vs False Positives")
    print("=" * 60)
    
    tester = NLPTester(NLP_SERVICE_URL)
    
    # Create refined test cases
    test_cases = create_refined_test_cases()
    
    print(f"📝 Created {len(test_cases)} refined test cases:")
    
    # Count by category
    high_count = len([t for t in test_cases if t.expected_level == 'high'])
    medium_count = len([t for t in test_cases if t.expected_level == 'medium'])
    low_count = len([t for t in test_cases if t.expected_level == 'low'])
    none_count = len([t for t in test_cases if t.expected_level == 'none'])
    
    print(f"  • {high_count} HIGH crisis cases")
    print(f"  • {medium_count} MEDIUM crisis cases") 
    print(f"  • {low_count} LOW crisis cases")
    print(f"  • {none_count} NONE cases (including {len([t for t in test_cases if 'idiom' in t.category])} idioms)")
    
    # Run tests
    summary = tester.run_test_suite(test_cases)
    
    if "error" not in summary:
        # Save results
        tester.save_results(summary)
        
        # Print recommendations
        print("\n💡 REFINED TEST ANALYSIS:")
        accuracy = summary['overall_accuracy']
        
        if accuracy >= 0.7:
            print("  🎉 Excellent! Target accuracy achieved!")
        elif accuracy >= 0.6:
            print("  ✅ Good progress! Close to target.")
        else:
            print("  🔧 Still needs improvement, but better labels should help.")
        
        print(f"\n🎯 Result: {accuracy:.1%} accuracy with refined test cases")
        print("🔑 Key: Idiom detection is critical for reducing false positives")

if __name__ == "__main__":
    main()