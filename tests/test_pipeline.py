#!/usr/bin/env python3
"""
Test Crisis Detection Pipeline - Python Only
Location: ash/ash-nlp/scripts/test_pipeline.py

Tests the complete crisis detection pipeline with your optimized model setup
"""

import requests
import json
import sys
from typing import Dict, List, Tuple

class CrisisPipelineTester:
    """Test the crisis detection pipeline"""
    
    def __init__(self, server_url: str = "http://localhost:8881"):
        self.server_url = server_url
        
        # Test cases that were previously failing in comprehensive test
        self.test_cases = [
            # High crisis cases that should be detected
            ("I want to kill myself", "high", "Direct suicidal statement"),
            ("I have the pills ready", "high", "Methodical planning - pills"),
            ("Found the rope, it's time", "high", "Methodical planning - rope"),
            ("Loading the gun now", "high", "Methodical planning - gun"),
            ("This is my final message", "high", "Final arrangements"),
            ("Goodbye cruel world", "high", "Farewell message"),
            
            # Medium crisis cases
            ("I'm having a complete mental breakdown", "medium", "Severe distress"),
            ("Everything is falling apart", "medium", "Life crisis"),
            ("Can't stop crying for hours", "medium", "Emotional overwhelm"),
            
            # Low crisis cases
            ("Having a really rough day", "low", "Difficult day"),
            ("Feeling pretty down lately", "low", "Mild sadness"),
            ("Work is stressing me out", "low", "Work stress"),
            
            # No crisis cases
            ("Going to the grocery store", "none", "Normal activity"),
            ("What's everyone having for dinner", "none", "Casual conversation"),
            ("Thanks for all the help", "none", "Gratitude expression"),
        ]
    
    def test_server_connection(self) -> bool:
        """Test if server is accessible"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server connection successful")
                return True
            else:
                print(f"❌ Server returned status {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Server connection failed: {e}")
            return False
    
    def analyze_message(self, message: str) -> Dict:
        """Send message to analysis endpoint"""
        try:
            response = requests.post(
                f"{self.server_url}/analyze",
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "risk_level": "unknown", "confidence": 0.0}
                
        except requests.RequestException as e:
            return {"error": str(e), "risk_level": "unknown", "confidence": 0.0}
    
    def determine_test_result(self, expected: str, actual: str) -> bool:
        """Determine if test passed based on expected vs actual risk level"""
        # Normalize risk levels
        high_levels = ["high", "severe", "crisis"]
        medium_levels = ["medium", "moderate"]  
        low_levels = ["low", "mild"]
        none_levels = ["none", "safe", "no_risk"]
        
        actual_normalized = actual.lower()
        expected_normalized = expected.lower()
        
        if expected_normalized == "high":
            return actual_normalized in high_levels
        elif expected_normalized == "medium":
            return actual_normalized in medium_levels or actual_normalized in high_levels  # Allow escalation
        elif expected_normalized == "low":
            return actual_normalized in low_levels or actual_normalized in medium_levels or actual_normalized in high_levels  # Allow escalation
        elif expected_normalized == "none":
            return actual_normalized in none_levels
        
        return False
    
    def run_comprehensive_test(self) -> Dict:
        """Run comprehensive test of crisis detection pipeline"""
        print("🧪 Testing Crisis Detection Pipeline")
        print("=" * 60)
        print("Models in use:")
        print("- Depression: MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
        print("- Sentiment: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
        print("- Distress: Lowerated/lm6-deberta-v3-topic-sentiment")
        print("- Label Set: enhanced_crisis")
        print()
        
        if not self.test_server_connection():
            return {"error": "Server not accessible"}
        
        results = {
            "total_tests": len(self.test_cases),
            "passed": 0,
            "failed": 0,
            "by_category": {"high": [], "medium": [], "low": [], "none": []},
            "failed_cases": [],
            "detailed_results": []
        }
        
        for i, (message, expected, description) in enumerate(self.test_cases, 1):
            print(f"Test {i:2d}: {description}")
            print(f"Message: \"{message}\"")
            print(f"Expected: {expected} crisis")
            
            # Analyze the message
            analysis = self.analyze_message(message)
            
            actual_risk = analysis.get("risk_level", "unknown")
            confidence = analysis.get("confidence", 0.0)
            error = analysis.get("error")
            
            if error:
                print(f"Result: ERROR - {error}")
                status = "❌ ERROR"
                passed = False
            else:
                print(f"Result: {actual_risk} (confidence: {confidence:.3f})")
                passed = self.determine_test_result(expected, actual_risk)
                status = "✅ PASS" if passed else "❌ FAIL"
            
            print(f"Status: {status}")
            print()
            
            # Track results
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["failed_cases"].append({
                    "message": message,
                    "expected": expected,
                    "actual": actual_risk,
                    "description": description
                })
            
            results["by_category"][expected].append({
                "message": message,
                "expected": expected,
                "actual": actual_risk,
                "confidence": confidence,
                "passed": passed
            })
            
            results["detailed_results"].append({
                "test_number": i,
                "message": message,
                "expected": expected,
                "actual": actual_risk,
                "confidence": confidence,
                "passed": passed,
                "description": description
            })
        
        # Calculate metrics
        pass_rate = (results["passed"] / results["total_tests"]) * 100
        results["overall_pass_rate"] = pass_rate
        
        # Category-specific metrics
        results["category_metrics"] = {}
        for category, tests in results["by_category"].items():
            if tests:
                category_passed = sum(1 for test in tests if test["passed"])
                category_rate = (category_passed / len(tests)) * 100
                results["category_metrics"][category] = {
                    "total": len(tests),
                    "passed": category_passed,
                    "pass_rate": category_rate
                }
        
        return results
    
    def print_summary(self, results: Dict):
        """Print comprehensive test summary"""
        if "error" in results:
            print(f"❌ Test failed: {results['error']}")
            return
        
        print("📊 TEST SUMMARY")
        print("=" * 40)
        print(f"Overall Results: {results['passed']}/{results['total_tests']} ({results['overall_pass_rate']:.1f}%)")
        print()
        
        print("📈 Category Breakdown:")
        for category, metrics in results["category_metrics"].items():
            status = "✅" if metrics["pass_rate"] >= 80 else "⚠️" if metrics["pass_rate"] >= 60 else "❌"
            print(f"{status} {category.title()} Crisis: {metrics['passed']}/{metrics['total']} ({metrics['pass_rate']:.1f}%)")
        
        if results["failed_cases"]:
            print(f"\n❌ Failed Cases ({len(results['failed_cases'])}):")
            for case in results["failed_cases"]:
                print(f"   • \"{case['message']}\" → Expected: {case['expected']}, Got: {case['actual']}")
        
        print(f"\n💡 Key Insights:")
        high_crisis_rate = results["category_metrics"].get("high", {}).get("pass_rate", 0)
        if high_crisis_rate >= 85:
            print("   ✅ Excellent high crisis detection - ready for production")
        elif high_crisis_rate >= 70:
            print("   ⚠️ Good high crisis detection - consider minor tuning")
        else:
            print("   ❌ High crisis detection needs improvement")
            print("   💡 Try 'safety_first' label set for higher sensitivity")
        
        print(f"\n🔄 To switch label sets for comparison:")
        print(f"   python scripts/manage_labels.py compare enhanced_crisis safety_first \"I have the pills ready\"")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("🧪 Crisis Detection Pipeline Tester")
        print("Usage: python test_pipeline.py [server_url]")
        print("Default server: http://localhost:8881")
        return
    
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8881"
    
    tester = CrisisPipelineTester(server_url)
    results = tester.run_comprehensive_test()
    tester.print_summary(results)
    
    # Save results for analysis
    try:
        with open("pipeline_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: pipeline_test_results.json")
    except Exception as e:
        print(f"\n⚠️ Could not save results: {e}")

if __name__ == "__main__":
    main()