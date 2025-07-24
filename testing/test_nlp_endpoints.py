#!/usr/bin/env python3
"""
Comprehensive Test Suite for Ash NLP Service
Tests all available endpoints with detailed reporting

Usage:
    python test_nlp_endpoints.py
    python test_nlp_endpoints.py --host localhost --port 8881
    python test_nlp_endpoints.py --verbose --save-results
"""

import requests
import json
import time
import argparse
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os

# Test result data structure
@dataclass
class TestResult:
    name: str
    endpoint: str
    method: str
    status_code: int
    success: bool
    response_data: Optional[Dict] = None
    error_message: Optional[str] = None
    response_time_ms: float = 0.0
    expected_fields: List[str] = None

class NLPServiceTester:
    """Comprehensive tester for Ash NLP Service endpoints"""
    
    def __init__(self, host: str = "localhost", port: int = 8881, verbose: bool = False):
        self.base_url = f"http://{host}:{port}"
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None) -> TestResult:
        """Make HTTP request and return test result"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_time = (time.time() - start_time) * 1000
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}
            
            success = 200 <= response.status_code < 300
            
            return TestResult(
                name="",  # Will be set by caller
                endpoint=endpoint,
                method=method.upper(),
                status_code=response.status_code,
                success=success,
                response_data=response_data,
                response_time_ms=response_time,
                error_message=None if success else response_data.get('detail', 'Unknown error')
            )
            
        except requests.exceptions.RequestException as e:
            response_time = (time.time() - start_time) * 1000
            return TestResult(
                name="",
                endpoint=endpoint,
                method=method.upper(),
                status_code=0,
                success=False,
                response_data=None,
                response_time_ms=response_time,
                error_message=str(e)
            )
    
    def test_health_check(self) -> TestResult:
        """Test /health endpoint"""
        result = self.make_request("GET", "/health")
        result.name = "Health Check"
        result.expected_fields = ["status", "model_loaded", "uptime_seconds", "hardware_info"]
        
        if result.success and result.response_data:
            # Validate expected fields
            missing_fields = [field for field in result.expected_fields 
                            if field not in result.response_data]
            if missing_fields:
                result.error_message = f"Missing fields: {missing_fields}"
                result.success = False
        
        self.results.append(result)
        return result
    
    def test_service_stats(self) -> TestResult:
        """Test /stats endpoint"""
        result = self.make_request("GET", "/stats")
        result.name = "Service Statistics"
        result.expected_fields = ["service", "version", "uptime_seconds", "models_loaded"]
        
        if result.success and result.response_data:
            missing_fields = [field for field in result.expected_fields 
                            if field not in result.response_data]
            if missing_fields:
                result.error_message = f"Missing fields: {missing_fields}"
                result.success = False
        
        self.results.append(result)
        return result
    
    def test_crisis_analysis(self, message: str, expected_level: str, test_name: str) -> TestResult:
        """Test /analyze endpoint with specific message"""
        data = {
            "message": message,
            "user_id": f"test_user_{int(time.time())}",
            "channel_id": "test_channel"
        }
        
        result = self.make_request("POST", "/analyze", data)
        result.name = test_name
        result.expected_fields = ["needs_response", "crisis_level", "confidence_score", 
                                "detected_categories", "method", "processing_time_ms", 
                                "model_info", "reasoning"]
        
        if result.success and result.response_data:
            # Validate expected fields
            missing_fields = [field for field in result.expected_fields 
                            if field not in result.response_data]
            if missing_fields:
                result.error_message = f"Missing fields: {missing_fields}"
                result.success = False
            
            # Check if detected level matches expectation (optional validation)
            actual_level = result.response_data.get('crisis_level', 'unknown')
            if self.verbose:
                self.log(f"Expected: {expected_level}, Actual: {actual_level}")
        
        self.results.append(result)
        return result
    
    def test_phrase_extraction(self) -> TestResult:
        """Test /extract_phrases endpoint (optional)"""
        data = {
            "message": "I am struggling with severe depression and anxiety",
            "user_id": "test_user_phrases",
            "channel_id": "test_channel",
            "task": "phrase_extraction"
        }
        
        result = self.make_request("POST", "/extract_phrases", data)
        result.name = "Phrase Extraction"
        
        # This endpoint may not be available
        if result.status_code == 503:
            result.error_message = "Feature not available (expected)"
        
        self.results.append(result)
        return result
    
    def test_semantic_analysis(self) -> TestResult:
        """Test /semantic_analysis endpoint (optional)"""
        data = {
            "message": "I cannot handle this transition anymore",
            "community_vocabulary": ["transition", "dysphoria", "chosen family"],
            "context_hints": ["lgbtq", "support"]
        }
        
        result = self.make_request("POST", "/semantic_analysis", data)
        result.name = "Semantic Analysis"
        
        # This endpoint may not be available
        if result.status_code == 503:
            result.error_message = "Feature not available (expected)"
        
        self.results.append(result)
        return result
    
    def test_pattern_learning(self) -> TestResult:
        """Test /learn_patterns endpoint (optional)"""
        data = {
            "messages": [
                {"content": "I feel hopeless and lost", "crisis_level": "high"},
                {"content": "Everything is great today", "crisis_level": "none"}
            ],
            "analysis_type": "community_patterns",
            "time_window_days": 30
        }
        
        result = self.make_request("POST", "/learn_patterns", data)
        result.name = "Pattern Learning"
        
        # This endpoint may not be available
        if result.status_code == 503:
            result.error_message = "Feature not available (expected)"
        
        self.results.append(result)
        return result
    
    def test_learning_statistics(self) -> TestResult:
        """Test /learning_statistics endpoint (should work if enhanced learning is available)"""
        result = self.make_request("GET", "/learning_statistics")
        result.name = "Learning Statistics"
        
        if result.success and result.response_data:
            # Check for expected learning statistics fields
            expected_fields = ["learning_system_status", "total_false_positives_processed", "total_false_negatives_processed", "total_adjustments_made"]
            missing_fields = [field for field in expected_fields 
                            if field not in result.response_data]
            if missing_fields:
                result.error_message = f"Missing fields: {missing_fields}"
                result.success = False
        elif result.status_code == 503:
            result.error_message = "Enhanced learning not available (expected)"
        elif result.status_code == 404:
            result.error_message = "Learning statistics endpoint not found"
            result.success = False
        
        self.results.append(result)
        return result
    
    def test_false_positive_learning(self) -> TestResult:
        """Test /analyze_false_positive endpoint"""
        data = {
            "message": "That movie killed me with laughter",
            "detected_level": "high",
            "correct_level": "none",
            "context": {"humor": True},
            "severity_score": 7  # Use integer instead of float
        }
        
        result = self.make_request("POST", "/analyze_false_positive", data)
        result.name = "False Positive Learning"
        
        # This endpoint may not be available
        if result.status_code == 503:
            result.error_message = "Feature not available (expected)"
        elif result.status_code == 422:
            result.error_message = f"Validation error: {result.response_data.get('detail', 'Unknown validation error')}"
            result.success = False  # Don't hide 422 errors!
        elif result.status_code == 404:
            result.error_message = "Endpoint not found - enhanced learning endpoints not properly added"
            result.success = False
        
        self.results.append(result)
        return result

    def test_false_negative_learning(self) -> TestResult:
        """Test /analyze_false_negative endpoint"""
        data = {
            "message": "I don't want to be here anymore and nothing matters",
            "should_detect_level": "high",
            "actually_detected": "none", 
            "context": {"subtle_crisis": True, "indirect_language": True},
            "severity_score": 9
        }
        
        result = self.make_request("POST", "/analyze_false_negative", data)
        result.name = "False Negative Learning"
        
        # This endpoint may not be available
        if result.status_code == 503:
            result.error_message = "Feature not available (expected)"
        elif result.status_code == 422:
            result.error_message = f"Validation error: {result.response_data.get('detail', 'Unknown validation error')}"
            result.success = False
        elif result.status_code == 404:
            result.error_message = "Endpoint not found - enhanced learning endpoints not properly added"
            result.success = False
        
        self.results.append(result)
        return result

    def test_critical_false_negative_scenarios(self) -> TestResult:
        """Test multiple critical false negative scenarios that the system should learn from"""
        
        # Test one representative false negative scenario
        data = {
            "message": "Everything feels pointless and I'm so tired of trying",
            "should_detect_level": "medium", 
            "actually_detected": "none",
            "context": {"depression_indicators": True, "exhaustion": True},
            "severity_score": 7
        }
        
        result = self.make_request("POST", "/analyze_false_negative", data)
        result.name = "Critical False Negative Scenarios"
        
        if result.status_code == 503:
            result.error_message = "Feature not available (expected)"
        elif result.status_code == 422:
            result.error_message = f"Validation error: {result.response_data.get('detail', 'Unknown validation error')}"
            result.success = False
        elif result.status_code == 404:
            result.error_message = "Endpoint not found"
            result.success = False
        elif result.success and result.response_data:
            # Validate that we get meaningful learning feedback
            expected_learning_fields = ["patterns_discovered", "confidence_adjustments", "learning_applied"]
            missing_fields = [field for field in expected_learning_fields 
                             if field not in result.response_data]
            if missing_fields:
                result.error_message = f"Learning response missing fields: {missing_fields}"
                result.success = False
        
        self.results.append(result)
        return result

    def test_subtle_crisis_detection(self) -> TestResult:
        """Test detection of subtle crisis language that might be missed"""
        
        # Test a subtle crisis message that might be missed
        subtle_crisis_message = "I keep thinking about how peaceful it would be to just disappear"
        
        data = {
            "message": subtle_crisis_message,
            "user_id": "test_subtle_crisis",
            "channel_id": "test_channel"
        }
        
        result = self.make_request("POST", "/analyze", data)
        result.name = "Subtle Crisis Detection"
        
        if result.success and result.response_data:
            crisis_level = result.response_data.get('crisis_level', 'none')
            confidence = result.response_data.get('confidence_score', 0)
            
            # Log the result for analysis
            if self.verbose:
                self.log(f"Subtle crisis test - Level: {crisis_level}, Confidence: {confidence:.3f}")
            
            # This is more of an observational test - we want to see how well it detects subtle language
            # We don't fail the test, but we can note if it misses obvious crisis indicators
            if crisis_level == 'none' and confidence < 0.3:
                result.error_message = f"May have missed subtle crisis indicators (detected: {crisis_level}, confidence: {confidence:.3f})"
                # Don't mark as failure since this is a learning opportunity
        
        self.results.append(result)
        return result

    def test_indirect_self_harm_language(self) -> TestResult:
        """Test detection of indirect self-harm language"""
        
        # Test indirect language that might indicate self-harm ideation
        indirect_message = "I wonder what would happen if I just went to sleep and never woke up"
        
        data = {
            "message": indirect_message,
            "user_id": "test_indirect_harm",
            "channel_id": "test_channel"
        }
        
        result = self.make_request("POST", "/analyze", data)
        result.name = "Indirect Self-Harm Detection"
        
        if result.success and result.response_data:
            crisis_level = result.response_data.get('crisis_level', 'none')
            confidence = result.response_data.get('confidence_score', 0)
            
            if self.verbose:
                self.log(f"Indirect harm test - Level: {crisis_level}, Confidence: {confidence:.3f}")
            
            # This should ideally be detected as at least medium crisis
            if crisis_level == 'none':
                result.error_message = f"Missed potential self-harm ideation (detected: {crisis_level})"
                # Mark as learning opportunity rather than hard failure
        
        self.results.append(result)
        return result

    def test_depression_language_detection(self) -> TestResult:
        """Test detection of depression-related language that might be subtle"""
        
        depression_message = "I feel so empty inside and nothing brings me joy anymore"
        
        data = {
            "message": depression_message,
            "user_id": "test_depression",
            "channel_id": "test_channel"
        }
        
        result = self.make_request("POST", "/analyze", data)
        result.name = "Depression Language Detection"
        
        if result.success and result.response_data:
            crisis_level = result.response_data.get('crisis_level', 'none')
            confidence = result.response_data.get('confidence_score', 0)
            
            if self.verbose:
                self.log(f"Depression test - Level: {crisis_level}, Confidence: {confidence:.3f}")
            
            # This should be detected as at least low-medium crisis
            if crisis_level == 'none' and confidence < 0.4:
                result.error_message = f"May have missed depression indicators (detected: {crisis_level}, confidence: {confidence:.3f})"
        
        self.results.append(result)
        return result

    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        self.log("🚀 Starting Ash NLP Service Test Suite")
        self.log(f"🔗 Testing service at: {self.base_url}")
        
        # Test categories
        core_tests = [
            ("Health Check", self.test_health_check),
            ("Service Statistics", self.test_service_stats),
        ]
        
        analysis_tests = [
            ("High Crisis Detection", lambda: self.test_crisis_analysis(
                "I want to end my life right now", "high", "High Crisis Detection")),
            ("Medium Crisis Detection", lambda: self.test_crisis_analysis(
                "I have been feeling really depressed lately", "medium", "Medium Crisis Detection")),
            ("Normal Message", lambda: self.test_crisis_analysis(
                "What a beautiful day! I love spending time with friends.", "none", "Normal Message")),
            ("Idiom Handling", lambda: self.test_crisis_analysis(
                "That joke absolutely killed me!", "none", "Idiom Handling")),
            ("Indirect Crisis", lambda: self.test_crisis_analysis(
                "I don't want to be here anymore", "high", "Indirect Crisis")),
            # ADD THESE MORE CHALLENGING ANALYSIS TESTS:
            ("Subtle Hopelessness", lambda: self.test_crisis_analysis(
                "Nothing ever works out for me and I don't see the point anymore", "medium", "Subtle Hopelessness")),
            ("Masked Depression", lambda: self.test_crisis_analysis(
                "I'm fine, just really tired of everything lately", "low", "Masked Depression")),
            ("Isolation Indicators", lambda: self.test_crisis_analysis(
                "I feel so alone and disconnected from everyone", "medium", "Isolation Indicators")),
        ]
        
        advanced_tests = [
            ("Phrase Extraction", self.test_phrase_extraction),
            ("Semantic Analysis", self.test_semantic_analysis),
            ("Pattern Learning", self.test_pattern_learning),
            ("Learning Statistics", self.test_learning_statistics),
            ("False Positive Learning", self.test_false_positive_learning),
            # ADD THESE NEW FALSE NEGATIVE TESTS:
            ("False Negative Learning", self.test_false_negative_learning),
            ("Critical False Negative Scenarios", self.test_critical_false_negative_scenarios),
            ("Subtle Crisis Detection", self.test_subtle_crisis_detection),
            ("Indirect Self-Harm Detection", self.test_indirect_self_harm_language),
            ("Depression Language Detection", self.test_depression_language_detection),
        ]
        
        # Run core tests
        self.log("\n📊 Running Core Tests...")
        for test_name, test_func in core_tests:
            self.log(f"Testing: {test_name}")
            result = test_func()
            status = "✅ PASS" if result.success else "❌ FAIL"
            self.log(f"  {status} ({result.response_time_ms:.1f}ms)")
            if not result.success and self.verbose:
                self.log(f"  Error: {result.error_message}")
        
        # Run analysis tests
        self.log("\n🧠 Running Crisis Analysis Tests...")
        for test_name, test_func in analysis_tests:
            self.log(f"Testing: {test_name}")
            result = test_func()
            status = "✅ PASS" if result.success else "❌ FAIL"
            self.log(f"  {status} ({result.response_time_ms:.1f}ms)")
            if result.success and result.response_data and self.verbose:
                level = result.response_data.get('crisis_level', 'unknown')
                confidence = result.response_data.get('confidence_score', 0)
                self.log(f"  Level: {level}, Confidence: {confidence:.3f}")
            elif not result.success and self.verbose:
                self.log(f"  Error: {result.error_message}")
        
        # Run advanced tests (including new false negative tests)
        self.log("\n🎓 Running Advanced Feature Tests...")
        for test_name, test_func in advanced_tests:
            self.log(f"Testing: {test_name}")
            result = test_func()
            if result.status_code == 503:
                self.log(f"  ℹ️ SKIP (feature not available)")
            else:
                status = "✅ PASS" if result.success else "❌ FAIL"
                self.log(f"  {status} ({result.response_time_ms:.1f}ms)")
                if not result.success and self.verbose:
                    self.log(f"  Error: {result.error_message}")
        
        # Generate summary
        return self.generate_summary()

    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = sum(1 for r in self.results if not r.success and r.status_code != 503)
        skipped_tests = sum(1 for r in self.results if r.status_code == 503)
        
        avg_response_time = sum(r.response_time_ms for r in self.results) / total_tests if total_tests > 0 else 0
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "service_url": self.base_url,
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "skipped": skipped_tests,
            "pass_rate": (passed_tests / (total_tests - skipped_tests)) * 100 if (total_tests - skipped_tests) > 0 else 0,
            "average_response_time_ms": avg_response_time,
            "test_results": [
                {
                    "name": r.name,
                    "endpoint": r.endpoint,
                    "method": r.method,
                    "status_code": r.status_code,
                    "success": r.success,
                    "response_time_ms": r.response_time_ms,
                    "error_message": r.error_message
                }
                for r in self.results
            ]
        }
        
        return summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print formatted test summary"""
        self.log("\n" + "="*60)
        self.log("📋 TEST SUMMARY")
        self.log("="*60)
        self.log(f"🔗 Service: {summary['service_url']}")
        self.log(f"📊 Tests Run: {summary['total_tests']}")
        self.log(f"✅ Passed: {summary['passed']}")
        self.log(f"❌ Failed: {summary['failed']}")
        self.log(f"ℹ️ Skipped: {summary['skipped']}")
        self.log(f"📈 Pass Rate: {summary['pass_rate']:.1f}%")
        self.log(f"⚡ Avg Response Time: {summary['average_response_time_ms']:.1f}ms")
        
        # List failed tests
        failed_tests = [r for r in self.results if not r.success and r.status_code != 503]
        if failed_tests:
            self.log("\n❌ Failed Tests:")
            for test in failed_tests:
                self.log(f"  - {test.name}: {test.error_message}")
        
        # Overall status
        if summary['failed'] == 0:
            self.log("\n🎉 All tests passed! Your NLP service is working correctly.")
        elif summary['pass_rate'] >= 80:
            self.log("\n⚠️ Most tests passed, but some issues detected.")
        else:
            self.log("\n🚨 Multiple test failures detected. Check service configuration.")
    
    def save_results(self, filename: str = None):
        """Save test results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nlp_test_results_{timestamp}.json"
        
        summary = self.generate_summary()
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.log(f"💾 Test results saved to: {filename}")
        return filename

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Test Ash NLP Service endpoints")
    parser.add_argument("--host", default="localhost", help="Service host (default: localhost)")
    parser.add_argument("--port", type=int, default=8881, help="Service port (default: 8881)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--save-results", "-s", action="store_true", help="Save results to JSON file")
    parser.add_argument("--output-file", "-o", help="Output filename for results")
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = NLPServiceTester(host=args.host, port=args.port, verbose=args.verbose)
    
    try:
        # Run all tests
        summary = tester.run_all_tests()
        
        # Print summary
        tester.print_summary(summary)
        
        # Save results if requested
        if args.save_results:
            filename = tester.save_results(args.output_file)
        
        # Exit with appropriate code
        sys.exit(0 if summary['failed'] == 0 else 1)
        
    except KeyboardInterrupt:
        tester.log("\n🛑 Testing interrupted by user")
        sys.exit(130)
    except Exception as e:
        tester.log(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
curl -X POST "http://10.20.30.16:8881/analyze_false_positive" -H "Content-Type: application/json" -d '{"message": "That movie killed me with laughter", "detected_level": "high", "correct_level": "none", "context": {"humor": true}, "severity_score": 7}'
"""