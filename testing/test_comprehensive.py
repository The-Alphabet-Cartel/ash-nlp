#!/usr/bin/env python3
"""
Comprehensive Test Script for Ash NLP Systematic Crisis Classification Fixes
Tests the complete balanced scoring system with comprehensive scenarios
"""

import requests
import json
import time
from typing import Dict, List

# Configuration
NLP_SERVER_URL = "http://10.20.30.16:8881"

# TIER 1: Previously problematic false positives (should be MEDIUM or lower)
TIER1_FALSE_POSITIVE_TESTS = [
    {
        "message": "I'm sick and tired of being sick and tired all the time",
        "expected_max_level": "medium",
        "description": "Primary false positive case - frustration expression"
    },
    {
        "message": "I just feel so down today",
        "expected_max_level": "low", 
        "description": "Common mild emotional expression"
    },
    {
        "message": "Having a rough day at work",
        "expected_max_level": "low",
        "description": "Work-related stress expression"
    },
    {
        "message": "Not doing so great right now but I'll be okay",
        "expected_max_level": "medium",
        "description": "Mild distress with self-reassurance"
    },
    {
        "message": "Feeling pretty down after that movie",
        "expected_max_level": "low",
        "description": "Contextual sadness (entertainment-related)"
    },
    {
        "message": "I'm just really tired and feeling low",
        "expected_max_level": "low",
        "description": "Fatigue-related mild mood"
    },
    {
        "message": "Been having a tough time lately",
        "expected_max_level": "medium",
        "description": "Ongoing but mild difficulty"
    },
    {
        "message": "So tired of this whole situation",
        "expected_max_level": "medium",
        "description": "Frustration with circumstances"
    }
]

# TIER 2: Borderline cases (should be appropriately classified)
TIER2_BORDERLINE_TESTS = [
    {
        "message": "I'm really struggling with everything right now",
        "expected_level": "medium",
        "description": "Clear struggle but not severe crisis"
    },
    {
        "message": "Feeling overwhelmed and don't know what to do",
        "expected_level": "medium", 
        "description": "Emotional overwhelm"
    },
    {
        "message": "Everything feels pointless lately",
        "expected_min_level": "medium",
        "expected_max_level": "high",
        "description": "Hopelessness - could be medium or high"
    },
    {
        "message": "I can't handle this anymore",
        "expected_min_level": "medium",
        "description": "Crisis escalation language"
    }
]

# TIER 3: Genuine crises (should still trigger HIGH alerts)
TIER3_TRUE_POSITIVE_TESTS = [
    {
        "message": "I don't want to be here anymore",
        "expected_min_level": "high",
        "description": "Clear suicidal ideation"
    },
    {
        "message": "Everyone would be better off without me",
        "expected_min_level": "high", 
        "description": "Burden ideation pattern"
    },
    {
        "message": "I've been having thoughts of hurting myself",
        "expected_min_level": "high",
        "description": "Self-harm ideation"
    },
    {
        "message": "Nothing matters anymore and I can't go on",
        "expected_min_level": "high",
        "description": "Severe hopelessness with inability to continue"
    },
    {
        "message": "I'm severely depressed and can't function",
        "expected_min_level": "medium",
        "description": "Clear depression with functional impairment"
    }
]

def test_nlp_endpoint(message: str) -> Dict:
    """Test a single message against the NLP endpoint"""
    try:
        response = requests.post(
            f"{NLP_SERVER_URL}/analyze",
            json={
                "message": message,
                "user_id": "test_user_123",
                "channel_id": "test_channel_456"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def level_to_numeric(level: str) -> int:
    """Convert crisis level to numeric for comparison"""
    mapping = {"none": 0, "low": 1, "medium": 2, "high": 3}
    return mapping.get(level.lower(), 0)

def run_tier1_false_positive_tests() -> List[Dict]:
    """Test known false positives - should NOT be HIGH"""
    print("🔍 TIER 1: False Positive Prevention Tests")
    print("=" * 60)
    
    results = []
    
    for i, test_case in enumerate(TIER1_FALSE_POSITIVE_TESTS, 1):
        print(f"\nTest {i}/{len(TIER1_FALSE_POSITIVE_TESTS)}: {test_case['description']}")
        print(f"Message: '{test_case['message']}'")
        print(f"Expected: {test_case['expected_max_level']} or lower")
        
        result = test_nlp_endpoint(test_case['message'])
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            results.append({
                "test_case": test_case,
                "result": result,
                "status": "error"
            })
            continue
        
        detected_level = result.get('crisis_level', 'none')
        confidence = result.get('confidence_score', 0.0)
        
        # Check if result is acceptable (not too high)
        max_allowed = level_to_numeric(test_case['expected_max_level'])
        actual = level_to_numeric(detected_level)
        
        if actual <= max_allowed:
            status_icon = "✅"
            status = "PASS"
            print(f"{status_icon} PASS: Detected {detected_level} (confidence: {confidence:.3f})")
        else:
            status_icon = "❌"
            status = "FAIL"
            print(f"{status_icon} FAIL: Detected {detected_level} (confidence: {confidence:.3f}) - Too high!")
        
        print(f"   Method: {result.get('method', 'unknown')}")
        print(f"   Reasoning: {result.get('reasoning', 'No reasoning provided')}")
        
        results.append({
            "test_case": test_case,
            "result": result,
            "status": status,
            "detected_level": detected_level,
            "confidence": confidence
        })
    
    return results

def run_tier2_borderline_tests() -> List[Dict]:
    """Test borderline cases - should be appropriately classified"""
    print("\n⚖️  TIER 2: Borderline Case Tests")
    print("=" * 60)
    
    results = []
    
    for i, test_case in enumerate(TIER2_BORDERLINE_TESTS, 1):
        print(f"\nTest {i}/{len(TIER2_BORDERLINE_TESTS)}: {test_case['description']}")
        print(f"Message: '{test_case['message']}'")
        
        # Handle both specific level and range expectations
        if 'expected_level' in test_case:
            print(f"Expected: {test_case['expected_level']}")
        else:
            min_level = test_case.get('expected_min_level', 'none')
            max_level = test_case.get('expected_max_level', 'high')
            print(f"Expected: {min_level} to {max_level}")
        
        result = test_nlp_endpoint(test_case['message'])
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            results.append({
                "test_case": test_case,
                "result": result,
                "status": "error"
            })
            continue
        
        detected_level = result.get('crisis_level', 'none')
        confidence = result.get('confidence_score', 0.0)
        actual = level_to_numeric(detected_level)
        
        # Determine if result is acceptable
        status = "PASS"
        status_icon = "✅"
        
        if 'expected_level' in test_case:
            # Exact level expected
            expected = level_to_numeric(test_case['expected_level'])
            if actual != expected:
                status = "FAIL"
                status_icon = "❌"
        else:
            # Range expected
            min_allowed = level_to_numeric(test_case.get('expected_min_level', 'none'))
            max_allowed = level_to_numeric(test_case.get('expected_max_level', 'high'))
            if actual < min_allowed or actual > max_allowed:
                status = "FAIL"
                status_icon = "❌"
        
        print(f"{status_icon} {status}: Detected {detected_level} (confidence: {confidence:.3f})")
        print(f"   Method: {result.get('method', 'unknown')}")
        print(f"   Reasoning: {result.get('reasoning', 'No reasoning provided')}")
        
        results.append({
            "test_case": test_case,
            "result": result,
            "status": status,
            "detected_level": detected_level,
            "confidence": confidence
        })
    
    return results

def run_tier3_true_positive_tests() -> List[Dict]:
    """Test genuine crises - must still detect appropriately"""
    print("\n🚨 TIER 3: True Positive Preservation Tests")
    print("=" * 60)
    
    results = []
    
    for i, test_case in enumerate(TIER3_TRUE_POSITIVE_TESTS, 1):
        print(f"\nTest {i}/{len(TIER3_TRUE_POSITIVE_TESTS)}: {test_case['description']}")
        print(f"Message: '{test_case['message']}'")
        print(f"Expected: {test_case['expected_min_level']} or higher")
        
        result = test_nlp_endpoint(test_case['message'])
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            results.append({
                "test_case": test_case,
                "result": result,
                "status": "error"
            })
            continue
        
        detected_level = result.get('crisis_level', 'none')
        confidence = result.get('confidence_score', 0.0)
        
        # Check if result meets minimum requirement
        min_required = level_to_numeric(test_case['expected_min_level'])
        actual = level_to_numeric(detected_level)
        
        if actual >= min_required:
            status_icon = "✅"
            status = "PASS"
            print(f"{status_icon} PASS: Detected {detected_level} (confidence: {confidence:.3f})")
        else:
            status_icon = "❌" 
            status = "FAIL"
            print(f"{status_icon} FAIL: Detected {detected_level} (confidence: {confidence:.3f}) - Too low!")
        
        print(f"   Method: {result.get('method', 'unknown')}")  
        print(f"   Reasoning: {result.get('reasoning', 'No reasoning provided')}")
        
        results.append({
            "test_case": test_case,
            "result": result,
            "status": status,
            "detected_level": detected_level,
            "confidence": confidence
        })
    
    return results

def print_comprehensive_summary(tier1_results: List[Dict], tier2_results: List[Dict], tier3_results: List[Dict]):
    """Print comprehensive test summary"""
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE SYSTEMATIC TEST SUMMARY")
    print("=" * 80)
    
    # Tier 1: False Positive Prevention
    tier1_pass = sum(1 for r in tier1_results if r['status'] == 'PASS')
    tier1_total = len(tier1_results)
    tier1_rate = (tier1_pass / tier1_total) * 100 if tier1_total > 0 else 0
    
    print(f"\n🔍 TIER 1 - False Positive Prevention: {tier1_pass}/{tier1_total} ({tier1_rate:.1f}%)")
    if tier1_rate >= 85:
        print("✅ EXCELLENT - False positives significantly reduced")
    elif tier1_rate >= 70:
        print("⚠️  GOOD - Major improvement, minor tuning may help")
    else:
        print("❌ NEEDS WORK - Consider further threshold reductions")
    
    # Tier 2: Borderline Cases
    tier2_pass = sum(1 for r in tier2_results if r['status'] == 'PASS')
    tier2_total = len(tier2_results)
    tier2_rate = (tier2_pass / tier2_total) * 100 if tier2_total > 0 else 0
    
    print(f"\n⚖️  TIER 2 - Borderline Case Accuracy: {tier2_pass}/{tier2_total} ({tier2_rate:.1f}%)")
    if tier2_rate >= 75:
        print("✅ EXCELLENT - Appropriate classification of complex cases")
    elif tier2_rate >= 60:
        print("⚠️  ACCEPTABLE - Some complexity in edge cases")
    else:
        print("❌ NEEDS REVIEW - Borderline classification issues")
    
    # Tier 3: True Positive Preservation
    tier3_pass = sum(1 for r in tier3_results if r['status'] == 'PASS')
    tier3_total = len(tier3_results)
    tier3_rate = (tier3_pass / tier3_total) * 100 if tier3_total > 0 else 0
    
    print(f"\n🚨 TIER 3 - True Positive Preservation: {tier3_pass}/{tier3_total} ({tier3_rate:.1f}%)")
    if tier3_rate >= 95:
        print("✅ EXCELLENT - Crisis detection maintained")
    elif tier3_rate >= 85:
        print("⚠️  GOOD - Minor detection gaps")
    else:
        print("❌ CRITICAL - Crisis detection compromised")
    
    # Overall Assessment
    overall_score = (tier1_rate * 0.4) + (tier2_rate * 0.2) + (tier3_rate * 0.4)  # Weight T1 and T3 heavily
    print(f"\n🎯 OVERALL SYSTEMATIC SCORE: {overall_score:.1f}%")
    
    if overall_score >= 85:
        print("🎉 SUCCESS - Comprehensive systematic improvement achieved!")
        print("   ✅ False positives reduced")
        print("   ✅ Crisis detection maintained")
        print("   ✅ System ready for production")
    elif overall_score >= 75:
        print("⚠️  PARTIAL SUCCESS - Good improvement with minor issues")
        print("   Consider fine-tuning specific threshold values")
    else:
        print("❌ NEEDS REVISION - Systematic issues require attention")
        print("   Review threshold values and scoring logic")
    
    # Specific recommendations
    print(f"\n📋 RECOMMENDATIONS:")
    if tier1_rate < 80:
        print("   🔧 Reduce thresholds further (decrease by 0.03-0.05)")
        print("   🔧 Add more false positive patterns to scoring")
    if tier3_rate < 90:
        print("   ⚠️  Review crisis pattern detection - may be too restrictive")
        print("   ⚠️  Consider raising HIGH threshold slightly if needed")
    if overall_score >= 85:
        print("   🚀 System ready for deployment!")
        print("   📊 Monitor real-world performance for 24-48 hours")
        print("   📈 Use /learning_stats to track ongoing improvements")

def main():
    """Run the comprehensive systematic test suite"""
    print("🧪 Ash NLP Comprehensive Systematic Crisis Classification Test Suite")
    print("Testing complete balanced scoring system implementation")
    print("=" * 80)
    
    # Test server connectivity
    try:
        health_response = requests.get(f"{NLP_SERVER_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"❌ NLP Server not responding properly: {health_response.status_code}")
            return
        print(f"✅ NLP Server connected: {NLP_SERVER_URL}")
    except Exception as e:
        print(f"❌ Cannot connect to NLP Server: {e}")
        return
    
    # Run comprehensive tests
    tier1_results = run_tier1_false_positive_tests()
    tier2_results = run_tier2_borderline_tests()
    tier3_results = run_tier3_true_positive_tests()
    
    # Print comprehensive summary
    print_comprehensive_summary(tier1_results, tier2_results, tier3_results)
    
    # Save detailed results
    timestamp = int(time.time())
    results_file = f"comprehensive_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "test_type": "comprehensive_systematic_validation",
            "tier1_false_positive_tests": tier1_results,
            "tier2_borderline_tests": tier2_results,
            "tier3_true_positive_tests": tier3_results,
            "summary": {
                "tier1_pass_rate": (sum(1 for r in tier1_results if r['status'] == 'PASS') / len(tier1_results)) * 100 if tier1_results else 0,
                "tier2_pass_rate": (sum(1 for r in tier2_results if r['status'] == 'PASS') / len(tier2_results)) * 100 if tier2_results else 0,
                "tier3_pass_rate": (sum(1 for r in tier3_results if r['status'] == 'PASS') / len(tier3_results)) * 100 if tier3_results else 0,
                "overall_score": ((sum(1 for r in tier1_results if r['status'] == 'PASS') / len(tier1_results)) * 0.4 + 
                                (sum(1 for r in tier2_results if r['status'] == 'PASS') / len(tier2_results)) * 0.2 +
                                (sum(1 for r in tier3_results if r['status'] == 'PASS') / len(tier3_results)) * 0.4) * 100 if all([tier1_results, tier2_results, tier3_results]) else 0
            }
        }, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()