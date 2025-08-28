# ash-nlp/tests/integration/test_analysis_flow.py
"""
Phase 4a Step 2: Comprehensive Analysis Flow Verification Test Suite
---
FILE VERSION: v3.1-4a-2-1
LAST MODIFIED: 2025-08-28
PHASE: 4a, Step 2 - Analysis Flow Verification & Testing
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import pytest
import asyncio
import json
import time
import sys
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
import requests
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestAnalysisFlowVerification:
    """
    Phase 4a Step 2: Comprehensive analysis flow testing
    
    Tests verify that every step of the crisis analysis pipeline is:
    1. Properly executed in the correct order
    2. Tracked with detailed execution information  
    3. Handles fallback scenarios gracefully
    4. Meets performance requirements
    5. Provides complete visibility into the analysis process
    """
    
    def setup_method(self):
        """Setup test environment for each test"""
        self.base_url = "http://localhost:8881"
        self.test_messages = {
            "crisis_high": "I've been feeling really down lately and don't know what to do",
            "crisis_medium": "Having a tough time dealing with things", 
            "crisis_low": "Feeling a bit stressed today",
            "no_crisis": "Thanks everyone for the great game night!",
            "complex_crisis": "I feel hopeless and like nothing will ever get better, I don't want to keep going",
            "community_specific": "Coming out was so hard and I feel rejected by my family",
            "temporal_indicator": "I've been struggling for weeks and it's getting worse"
        }
        
        # Expected tracking structure
        self.expected_tracking_keys = [
            "tracking_enabled",
            "message_metadata", 
            "step_1_zero_shot_ai",
            "step_2_pattern_enhancement",
            "step_3_learning_adjustments",
            "fallback_scenarios",
            "performance_metrics"
        ]
        
        self.expected_summary_keys = [
            "total_processing_time_ms",
            "steps_attempted",
            "steps_completed", 
            "success_rate",
            "performance_target_met",
            "analysis_method",
            "crisis_detection_pipeline"
        ]
    
    @pytest.mark.asyncio
    async def test_complete_analysis_pipeline_tracking(self):
        """
        Test 1: Verify complete analysis pipeline execution with full tracking
        
        This test ensures:
        - All 3 analysis steps are executed in order
        - Each step is properly tracked with timing
        - Response includes comprehensive execution details
        - Performance metrics are captured
        """
        print("\n🧪 TEST 1: Complete Analysis Pipeline Tracking")
        
        response = requests.post(f"{self.base_url}/analyze", json={
            "message": self.test_messages["crisis_high"],
            "user_id": "test_user_pipeline_123",
            "channel_id": "test_channel_pipeline_456"
        })
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        # Verify core response structure
        assert "crisis_score" in data, "Missing crisis_score in response"
        assert "crisis_level" in data, "Missing crisis_level in response"
        assert "confidence_score" in data, "Missing confidence_score in response"
        
        # Verify execution tracking exists
        assert "analysis_execution_tracking" in data, "Missing analysis_execution_tracking"
        tracking = data["analysis_execution_tracking"]
        
        # Verify all expected tracking keys
        for key in self.expected_tracking_keys:
            assert key in tracking, f"Missing tracking key: {key}"
        
        # Verify tracking summary exists
        assert "tracking_summary" in data, "Missing tracking_summary"
        summary = data["tracking_summary"]
        
        for key in self.expected_summary_keys:
            assert key in summary, f"Missing summary key: {key}"
        
        # Verify step execution details
        step1 = tracking["step_1_zero_shot_ai"]
        assert step1.get("executed", False), "Step 1 (Zero-shot AI) was not executed"
        assert "processing_time_ms" in step1, "Step 1 missing processing time"
        assert step1.get("processing_time_ms", 0) > 0, "Step 1 processing time should be > 0"
        
        step2 = tracking["step_2_pattern_enhancement"] 
        assert step2.get("executed", False), "Step 2 (Pattern Enhancement) was not executed"
        assert "processing_time_ms" in step2, "Step 2 missing processing time"
        
        # Step 3 might not execute if learning manager not available
        step3 = tracking["step_3_learning_adjustments"]
        if step3.get("executed", False):
            assert "processing_time_ms" in step3, "Step 3 missing processing time"
        
        # Verify performance tracking
        assert summary["total_processing_time_ms"] > 0, "Total processing time should be > 0"
        assert summary["steps_completed"] >= 2, "Should have at least 2 completed steps"
        assert summary["success_rate"] > 0, "Success rate should be > 0"
        
        print(f"   ✅ Analysis completed with {summary['steps_completed']}/{summary['steps_attempted']} steps")
        print(f"   📊 Crisis Level: {data['crisis_level']}, Score: {data['crisis_score']:.3f}")
        print(f"   ⏱️  Total Time: {summary['total_processing_time_ms']:.1f}ms")
        print(f"   🎯 Performance Target Met: {summary['performance_target_met']}")
        
        return data
    
    def test_crisis_level_variations_with_tracking(self):
        """
        Test 2: Verify tracking works across different crisis levels
        
        This test ensures:
        - Tracking works for all message types
        - Different crisis levels are properly detected
        - Tracking data is consistent across variations
        """
        print("\n🧪 TEST 2: Crisis Level Variations with Tracking")
        
        results = {}
        for message_type, message in self.test_messages.items():
            print(f"\n   Testing: {message_type.upper()}")
            
            response = requests.post(f"{self.base_url}/analyze", json={
                "message": message,
                "user_id": f"test_user_{message_type}",
                "channel_id": "test_channel_variations"
            })
            
            assert response.status_code == 200, f"Failed for {message_type}: HTTP {response.status_code}"
            data = response.json()
            
            # Verify tracking exists for all message types
            assert "analysis_execution_tracking" in data, f"Missing tracking for {message_type}"
            assert "tracking_summary" in data, f"Missing summary for {message_type}"
            
            tracking = data["analysis_execution_tracking"]
            summary = data["tracking_summary"]
            
            # Verify at least one step executed
            assert summary["steps_completed"] >= 1, f"No steps completed for {message_type}"
            
            # Store results for analysis
            results[message_type] = {
                "crisis_level": data.get("crisis_level", "unknown"),
                "crisis_score": data.get("crisis_score", 0.0),
                "steps_completed": summary["steps_completed"],
                "processing_time": summary["total_processing_time_ms"],
                "ai_used": tracking["step_1_zero_shot_ai"].get("executed", False),
                "patterns_used": tracking["step_2_pattern_enhancement"].get("executed", False)
            }
            
            print(f"     Crisis Level: {results[message_type]['crisis_level']}")
            print(f"     Steps: {results[message_type]['steps_completed']}")
            print(f"     Time: {results[message_type]['processing_time']:.1f}ms")
        
        # Verify crisis level variation
        crisis_levels_found = set(r["crisis_level"] for r in results.values())
        assert len(crisis_levels_found) > 1, "Should detect different crisis levels"
        
        print(f"\n   ✅ Detected {len(crisis_levels_found)} different crisis levels: {crisis_levels_found}")
        return results
    
    def test_performance_optimization_tracking(self):
        """
        Test 3: Verify performance optimization tracking
        
        This test ensures:
        - Performance metrics are properly tracked
        - Sub-500ms target is monitored
        - Optimization flags are set appropriately
        """
        print("\n🧪 TEST 3: Performance Optimization Tracking")
        
        # Test multiple messages for performance consistency
        performance_results = []
        
        for i in range(3):  # Test 3 times for consistency
            start_time = time.time()
            
            response = requests.post(f"{self.base_url}/analyze", json={
                "message": self.test_messages["crisis_medium"],
                "user_id": f"perf_test_user_{i}",
                "channel_id": "perf_test_channel"
            })
            
            wall_clock_time = (time.time() - start_time) * 1000
            
            assert response.status_code == 200, f"Performance test {i} failed: HTTP {response.status_code}"
            data = response.json()
            
            # Verify tracking exists
            assert "tracking_summary" in data, f"Missing tracking summary in performance test {i}"
            summary = data["tracking_summary"]
            
            # Verify performance metrics
            reported_time = summary["total_processing_time_ms"]
            performance_target_met = summary["performance_target_met"]
            
            performance_results.append({
                "reported_time_ms": reported_time,
                "wall_clock_time_ms": wall_clock_time,
                "target_met": performance_target_met,
                "optimization_used": data["analysis_execution_tracking"]["performance_metrics"].get("optimization_applied", False)
            })
            
            print(f"   Run {i+1}: {reported_time:.1f}ms (Target: <500ms) - {'✅' if performance_target_met else '⚠️'}")
        
        # Analyze performance consistency
        avg_time = sum(r["reported_time_ms"] for r in performance_results) / len(performance_results)
        target_met_count = sum(1 for r in performance_results if r["target_met"])
        
        print(f"\n   📊 Performance Summary:")
        print(f"     Average Time: {avg_time:.1f}ms")
        print(f"     Target Met: {target_met_count}/{len(performance_results)} runs")
        print(f"     Optimization Rate: {sum(1 for r in performance_results if r['optimization_used'])}/{len(performance_results)}")
        
        # At least some runs should meet performance target
        assert target_met_count > 0, "No runs met the performance target"
        
        return performance_results
    
    def test_step_by_step_verification(self):
        """
        Test 4: Detailed step-by-step execution verification
        
        This test ensures:
        - Each step is executed in the correct order
        - Step timing is reasonable
        - Step results are properly captured
        """
        print("\n🧪 TEST 4: Step-by-Step Execution Verification")
        
        response = requests.post(f"{self.base_url}/analyze", json={
            "message": self.test_messages["complex_crisis"],
            "user_id": "step_verification_user",
            "channel_id": "step_verification_channel"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        tracking = data["analysis_execution_tracking"]
        
        # Verify Step 1: Zero-Shot AI Analysis
        step1 = tracking["step_1_zero_shot_ai"]
        print(f"\n   📋 Step 1: Zero-Shot AI Analysis")
        print(f"     Executed: {step1.get('executed', False)}")
        print(f"     Time: {step1.get('processing_time_ms', 0):.1f}ms")
        
        if step1.get("executed", False):
            assert step1.get("processing_time_ms", 0) > 0, "Step 1 should have processing time > 0"
            print(f"     Method: {step1.get('method', 'unknown')}")
            print(f"     Models Used: {step1.get('models_used', [])}")
            print(f"     AI Confidence: {step1.get('ensemble_confidence', 0.0):.3f}")
        
        # Verify Step 2: Pattern Enhancement
        step2 = tracking["step_2_pattern_enhancement"]
        print(f"\n   📋 Step 2: Pattern Enhancement")
        print(f"     Executed: {step2.get('executed', False)}")
        print(f"     Time: {step2.get('processing_time_ms', 0):.1f}ms")
        
        if step2.get("executed", False):
            assert step2.get("processing_time_ms", 0) > 0, "Step 2 should have processing time > 0"
            patterns = step2.get("patterns_matched", [])
            print(f"     Patterns Found: {len(patterns)}")
            print(f"     Enhancement Applied: {step2.get('enhancement_applied', False)}")
            print(f"     Confidence Boost: {step2.get('confidence_boost', 0.0):.3f}")
        
        # Verify Step 3: Learning Adjustments
        step3 = tracking["step_3_learning_adjustments"]
        print(f"\n   📋 Step 3: Learning Adjustments")
        print(f"     Executed: {step3.get('executed', False)}")
        
        if step3.get("executed", False):
            print(f"     Time: {step3.get('processing_time_ms', 0):.1f}ms")
            print(f"     Learning Applied: {step3.get('learning_applied', False)}")
            print(f"     Confidence Modification: {step3.get('confidence_modifications', 0.0):.3f}")
        else:
            print(f"     Reason: {step3.get('reason', 'Unknown')}")
        
        # Verify execution order makes sense
        summary = data["tracking_summary"]
        pipeline = summary["crisis_detection_pipeline"]
        
        print(f"\n   🔄 Pipeline Summary:")
        print(f"     AI Models Used: {pipeline['ai_models_used']}")
        print(f"     Pattern Enhancement: {pipeline['pattern_enhancement_applied']}")
        print(f"     Learning Adjustments: {pipeline['learning_adjustments_applied']}")
        
        # At least AI models or patterns should be used
        assert pipeline["ai_models_used"] or pipeline["pattern_enhancement_applied"], \
               "Either AI models or pattern enhancement should be used"
        
        return data
    
    def test_fallback_scenario_tracking(self):
        """
        Test 5: Verify fallback scenario tracking
        
        This test would ideally simulate AI model failures to test fallback paths.
        For now, it verifies that fallback flags are properly tracked.
        """
        print("\n🧪 TEST 5: Fallback Scenario Tracking")
        
        response = requests.post(f"{self.base_url}/analyze", json={
            "message": self.test_messages["crisis_high"],
            "user_id": "fallback_test_user",
            "channel_id": "fallback_test_channel"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        tracking = data["analysis_execution_tracking"]
        fallback_scenarios = tracking["fallback_scenarios"]
        
        print(f"   📋 Fallback Scenario Flags:")
        print(f"     AI Models Failed: {fallback_scenarios['ai_models_failed']}")
        print(f"     Pattern Only Used: {fallback_scenarios['pattern_only_used']}")
        print(f"     Emergency Fallback: {fallback_scenarios['emergency_fallback']}")
        
        # Verify fallback structure exists
        assert "ai_models_failed" in fallback_scenarios
        assert "pattern_only_used" in fallback_scenarios
        assert "emergency_fallback" in fallback_scenarios
        
        # In normal operation, emergency fallback should be false
        assert fallback_scenarios["emergency_fallback"] == False, \
               "Emergency fallback should not trigger in normal operation"
        
        return data
    
    def test_response_structure_completeness(self):
        """
        Test 6: Verify complete response structure with tracking
        
        This test ensures:
        - All expected response fields are present
        - Tracking data doesn't break existing structure
        - Response is JSON serializable and complete
        """
        print("\n🧪 TEST 6: Response Structure Completeness")
        
        response = requests.post(f"{self.base_url}/analyze", json={
            "message": self.test_messages["community_specific"],
            "user_id": "structure_test_user",
            "channel_id": "structure_test_channel"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify core analysis fields (existing)
        core_fields = [
            "crisis_score", "crisis_level", "confidence_score", 
            "needs_response", "method", "detected_categories"
        ]
        
        for field in core_fields:
            assert field in data, f"Missing core field: {field}"
        
        # Verify enhanced tracking fields (new)
        tracking_fields = [
            "analysis_execution_tracking", "tracking_summary"
        ]
        
        for field in tracking_fields:
            assert field in data, f"Missing tracking field: {field}"
        
        # Verify data types
        assert isinstance(data["crisis_score"], (int, float)), "crisis_score should be numeric"
        assert isinstance(data["crisis_level"], str), "crisis_level should be string"
        assert isinstance(data["confidence_score"], (int, float)), "confidence_score should be numeric"
        assert isinstance(data["needs_response"], bool), "needs_response should be boolean"
        assert isinstance(data["detected_categories"], list), "detected_categories should be list"
        
        # Verify tracking data types
        tracking = data["analysis_execution_tracking"]
        assert isinstance(tracking["tracking_enabled"], bool), "tracking_enabled should be boolean"
        assert isinstance(tracking["message_metadata"], dict), "message_metadata should be dict"
        
        summary = data["tracking_summary"]
        assert isinstance(summary["total_processing_time_ms"], (int, float)), "total_processing_time_ms should be numeric"
        assert isinstance(summary["steps_completed"], int), "steps_completed should be integer"
        assert isinstance(summary["success_rate"], (int, float)), "success_rate should be numeric"
        
        print(f"   ✅ All {len(core_fields)} core fields present")
        print(f"   ✅ All {len(tracking_fields)} tracking fields present")
        print(f"   ✅ Data types validated")
        print(f"   📊 Response size: ~{len(json.dumps(data))} characters")
        
        return data


class AnalysisFlowIntegrationTester:
    """
    Comprehensive integration test runner for Phase 4a Step 2
    """
    
    def __init__(self, base_url: str = "http://localhost:8881"):
        self.base_url = base_url
        self.test_results = []
        
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run the complete Phase 4a Step 2 test suite"""
        print("🧪 PHASE 4a STEP 2: Comprehensive Analysis Flow Verification")
        print("=" * 70)
        
        test_instance = TestAnalysisFlowVerification()
        test_instance.setup_method()
        
        # Run all tests
        tests = [
            ("Complete Pipeline Tracking", test_instance.test_complete_analysis_pipeline_tracking),
            ("Crisis Level Variations", test_instance.test_crisis_level_variations_with_tracking),
            ("Performance Optimization", test_instance.test_performance_optimization_tracking),
            ("Step-by-Step Verification", test_instance.test_step_by_step_verification),
            ("Fallback Scenario Tracking", test_instance.test_fallback_scenario_tracking),
            ("Response Structure Completeness", test_instance.test_response_structure_completeness)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                result = test_func()
                results.append({
                    "test_name": test_name,
                    "status": "PASSED",
                    "result": result if isinstance(result, dict) else {"success": True}
                })
                print(f"   ✅ {test_name} - PASSED")
                
            except Exception as e:
                results.append({
                    "test_name": test_name,
                    "status": "FAILED",
                    "error": str(e)
                })
                print(f"   ❌ {test_name} - FAILED: {str(e)}")
        
        # Generate comprehensive summary
        passed_tests = sum(1 for r in results if r["status"] == "PASSED")
        total_tests = len(results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        summary = {
            "phase": "4a",
            "step": "2",
            "test_suite": "Analysis Flow Verification",
            "timestamp": time.time(),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "detailed_results": results,
            "verification_status": {
                "analysis_pipeline_verified": any(r["test_name"] == "Complete Pipeline Tracking" and r["status"] == "PASSED" for r in results),
                "step_tracking_verified": any(r["test_name"] == "Step-by-Step Verification" and r["status"] == "PASSED" for r in results),
                "performance_tracking_verified": any(r["test_name"] == "Performance Optimization" and r["status"] == "PASSED" for r in results),
                "fallback_tracking_verified": any(r["test_name"] == "Fallback Scenario Tracking" and r["status"] == "PASSED" for r in results)
            }
        }
        
        self._print_final_summary(summary)
        return summary
    
    def _print_final_summary(self, summary: Dict[str, Any]):
        """Print comprehensive test summary"""
        print("\n" + "=" * 70)
        print("🎯 PHASE 4a STEP 2 - FINAL TEST SUMMARY")
        print("=" * 70)
        
        print(f"📊 Test Results: {summary['passed_tests']}/{summary['total_tests']} PASSED")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        
        # Verification status
        verification = summary['verification_status']
        print(f"\n🔍 Core Verification Status:")
        print(f"   Analysis Pipeline: {'✅ VERIFIED' if verification['analysis_pipeline_verified'] else '❌ FAILED'}")
        print(f"   Step Tracking: {'✅ VERIFIED' if verification['step_tracking_verified'] else '❌ FAILED'}")
        print(f"   Performance Tracking: {'✅ VERIFIED' if verification['performance_tracking_verified'] else '❌ FAILED'}")
        print(f"   Fallback Tracking: {'✅ VERIFIED' if verification['fallback_tracking_verified'] else '❌ FAILED'}")
        
        if summary['success_rate'] == 100.0:
            print("\n🎉 ALL TESTS PASSED - Phase 4a Step 2 Analysis Flow Verification SUCCESSFUL!")
            print("\n✅ CONFIRMED: Every analysis step is properly tracked and verified")
            print("✅ CONFIRMED: API response includes comprehensive execution tracking")
            print("✅ CONFIRMED: Zero-shot AI → Pattern Enhancement → Learning flow working")
            print("✅ CONFIRMED: Performance metrics and fallback scenarios tracked")
        else:
            print(f"\n⚠️  {summary['failed_tests']} TEST(S) FAILED - Review detailed results")
            failed_tests = [r["test_name"] for r in summary["detailed_results"] if r["status"] == "FAILED"]
            print(f"❌ Failed Tests: {', '.join(failed_tests)}")
        
        print("\n" + "=" * 70)


# ============================================================================
# STANDALONE TEST RUNNER SCRIPT
# ============================================================================

def main():
    """
    Main test runner for Phase 4a Step 2
    Can be run directly: python test_analysis_flow_verification.py
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Phase 4a Step 2: Analysis Flow Verification Tests")
    parser.add_argument("--url", default="http://localhost:8881", help="Base URL for API tests")
    parser.add_argument("--output", default="phase_4a_step_2_results.json", help="Output file for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Run comprehensive test suite
    tester = AnalysisFlowIntegrationTester(args.url)
    results = tester.run_comprehensive_test_suite()
    
    # Save results to file
    try:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n📁 Results saved to: {args.output}")
    except Exception as e:
        print(f"\n⚠️  Failed to save results: {e}")
    
    # Exit with appropriate code
    exit_code = 0 if results["success_rate"] == 100.0 else 1
    
    if args.verbose:
        print(f"\nExiting with code: {exit_code}")
    
    return exit_code


# ============================================================================
# PYTEST INTEGRATION
# ============================================================================

class TestPhase4aStep2Integration:
    """
    Pytest-compatible test class for Phase 4a Step 2
    Run with: pytest test_analysis_flow_verification.py -v
    """
    
    @classmethod
    def setup_class(cls):
        """Setup for pytest integration"""
        cls.tester = AnalysisFlowIntegrationTester()
    
    def test_phase_4a_step_2_complete_verification(self):
        """Complete Phase 4a Step 2 verification as single pytest"""
        results = self.tester.run_comprehensive_test_suite()
        
        # Assert overall success
        assert results["success_rate"] == 100.0, \
            f"Phase 4a Step 2 verification failed: {results['failed_tests']} of {results['total_tests']} tests failed"
        
        # Assert specific verifications
        verification = results['verification_status']
        assert verification['analysis_pipeline_verified'], "Analysis pipeline verification failed"
        assert verification['step_tracking_verified'], "Step tracking verification failed" 
        assert verification['performance_tracking_verified'], "Performance tracking verification failed"
        assert verification['fallback_tracking_verified'], "Fallback tracking verification failed"


# ============================================================================
# DOCKER INTEGRATION TEST SCRIPT
# ============================================================================

def run_docker_integration_test():
    """
    Run Phase 4a Step 2 tests within Docker environment
    Usage: docker exec ash-nlp python tests/phase_4a/test_analysis_flow_verification.py
    """
    print("🐳 Running Phase 4a Step 2 tests in Docker environment")
    
    # Wait for service to be ready
    import time
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8881/health")
            if response.status_code == 200:
                print("✅ Service is ready")
                break
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"⏳ Waiting for service... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("❌ Service not ready after 60 seconds")
                return 1
    
    # Run tests
    tester = AnalysisFlowIntegrationTester("http://localhost:8881")
    results = tester.run_comprehensive_test_suite()
    
    # Save results in Docker volume
    try:
        with open("/app/logs/phase_4a_step_2_docker_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("\n📁 Docker results saved to: /app/logs/phase_4a_step_2_docker_results.json")
    except Exception as e:
        print(f"\n⚠️  Failed to save Docker results: {e}")
    
    return 0 if results["success_rate"] == 100.0 else 1


# ============================================================================
# SAMPLE EXPECTED RESPONSE FOR DOCUMENTATION
# ============================================================================

SAMPLE_ENHANCED_RESPONSE = {
    "crisis_score": 0.75,
    "crisis_level": "high",
    "confidence_score": 0.82,
    "needs_response": True,
    "requires_staff_review": False,
    "method": "enhanced_three_step_analysis",
    "detected_categories": ["emotional_distress", "seeking_help"],
    
    # EXISTING FIELDS PRESERVED
    "ai_model_details": {
        "models_used": ["model_1", "model_2", "model_3"],
        "individual_results": {
            "model_1": {"score": 0.78, "confidence": 0.85},
            "model_2": {"score": 0.71, "confidence": 0.79}, 
            "model_3": {"score": 0.76, "confidence": 0.81}
        },
        "base_confidence": 0.82
    },
    "pattern_analysis": {
        "patterns_matched": ["emotional_distress", "seeking_help"],
        "enhancement_boost": 0.05,
        "pattern_confidence": 0.65
    },
    "learning_adjustments": {
        "applied": True,
        "score_adjustment": 0.02,
        "metadata": {"adjustment_reason": "user_history_positive"}
    },
    
    # NEW: COMPREHENSIVE ANALYSIS TRACKING
    "analysis_execution_tracking": {
        "tracking_enabled": True,
        "message_metadata": {
            "message_length": 52,
            "user_id": "test_user_123",
            "channel_id": "test_channel_456",
            "timestamp": 1693363200.123
        },
        "step_1_zero_shot_ai": {
            "executed": True,
            "started": True,
            "completed": True,
            "processing_time_ms": 145.2,
            "method": "sync_ensemble",
            "models_used": ["model_1", "model_2", "model_3"],
            "individual_scores": {
                "model_1": 0.78,
                "model_2": 0.71,
                "model_3": 0.76
            },
            "ensemble_confidence": 0.82,
            "ai_classification_successful": True
        },
        "step_2_pattern_enhancement": {
            "executed": True,
            "started": True,
            "completed": True,
            "processing_time_ms": 32.1,
            "patterns_matched": ["emotional_distress", "seeking_help"],
            "pattern_categories": ["emotional_distress", "help_seeking"],
            "enhancement_applied": True,
            "confidence_boost": 0.05,
            "pattern_analysis_successful": True
        },
        "step_3_learning_adjustments": {
            "executed": True,
            "started": True,
            "completed": True,
            "processing_time_ms": 8.3,
            "threshold_adjustments": {"medium": -0.02},
            "confidence_modifications": 0.02,
            "learning_metadata": {"adjustment_type": "user_history"},
            "learning_applied": True
        },
        "fallback_scenarios": {
            "ai_models_failed": False,
            "pattern_only_used": False,
            "emergency_fallback": False
        },
        "performance_metrics": {
            "target_time_ms": 500,
            "optimization_applied": True
        }
    },
    
    # NEW: TRACKING SUMMARY
    "tracking_summary": {
        "total_processing_time_ms": 185.6,
        "steps_attempted": 3,
        "steps_completed": 3,
        "success_rate": 100.0,
        "performance_target_met": True,
        "analysis_method": "enhanced_three_step_analysis",
        "crisis_detection_pipeline": {
            "ai_models_used": True,
            "pattern_enhancement_applied": True,
            "learning_adjustments_applied": True
        }
    }
}


if __name__ == "__main__":
    import os
    
    # Detect execution environment
    if os.environ.get("DOCKER_CONTAINER"):
        exit_code = run_docker_integration_test()
    else:
        exit_code = main()
    
    sys.exit(exit_code)