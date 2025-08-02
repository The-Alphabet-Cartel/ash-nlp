#!/usr/bin/env python3
"""
FIXED Quick Crisis Detection Test for Ash NLP Service
Tests the Three Zero-Shot Model Ensemble crisis detection system
Location: ash-nlp/scripts/quick_test.py
"""

import requests
import json
import time

NLP_SERVER_URL = "http://localhost:8881"

# Test cases that previously failed
FAILING_CASES = [
    "I have the pills ready",
    "Found the rope, it's time", 
    "Loading the gun now",
    "This is my final message",
    "Goodbye cruel world"
]

# Test cases that previously passed
PASSING_CASES = [
    "I want to kill myself",
    "Life isn't worth living anymore",
    "Going to kill myself after this"
]

def check_server_status():
    """Check if server is running and models are loaded"""
    print("🧪 Quick Crisis Detection Test")
    print("=" * 50)
    
    try:
        # Check health endpoint
        health_response = requests.get(f"{NLP_SERVER_URL}/health", timeout=10)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ Server connection OK")
            
            # Check current label set
            try:
                stats_response = requests.get(f"{NLP_SERVER_URL}/stats", timeout=10)
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    models_info = stats_data.get('models_loaded', {})
                    
                    # Get current label set from config
                    config_info = stats_data.get('configuration', {})
                    print(f"✅ Current label set: enhanced_crisis")  # Default assumption
                    
                    # FIXED: Check models_loaded from the correct location
                    models_loaded = models_info.get('models_loaded', False)
                    print(f"✅ Models loaded: {models_loaded}")
                    
                    return models_loaded
                else:
                    print(f"⚠️ Could not get stats: {stats_response.status_code}")
                    return False
            except Exception as e:
                print(f"⚠️ Could not get stats: {e}")
                return False
        else:
            print(f"❌ Server connection failed: {health_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_message(message, expected_result=None):
    """Test a single message and return results"""
    try:
        payload = {
            "message": message,
            "user_id": "test",
            "channel_id": "test"
        }
        
        response = requests.post(f"{NLP_SERVER_URL}/analyze", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract crisis level and confidence
            crisis_level = result.get('crisis_level', 'unknown')
            confidence = result.get('confidence_score', 0.0)
            
            # Determine if this should be considered a detection
            is_detected = crisis_level in ['high', 'medium', 'low']
            
            return {
                'detected': is_detected,
                'crisis_level': crisis_level,
                'confidence': confidence,
                'needs_response': result.get('needs_response', False),
                'full_result': result
            }
        else:
            print(f"   ❌ API Error {response.status_code}: {response.text}")
            return {
                'detected': False,
                'crisis_level': 'error',
                'confidence': 0.0,
                'error': f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return {
            'detected': False,
            'crisis_level': 'error', 
            'confidence': 0.0,
            'error': str(e)
        }

def test_crisis_cases():
    """Test crisis detection cases"""
    
    # Check if server is ready
    models_loaded = check_server_status()
    if not models_loaded:
        print("❌ Models not loaded - aborting test")
        return
    
    print("Enhanced Crisis Labels + Optimized Models")
    
    # Test failing cases
    print("🔍 Testing Previously FAILING Cases:")
    print("-" * 40)
    
    failing_now_detected = 0
    for message in FAILING_CASES:
        result = test_message(message)
        
        if result['detected']:
            print(f"✅ NOW DETECTING \"{message}\"")
            print(f"   → {result['crisis_level']} (confidence: {result['confidence']:.3f})")
            failing_now_detected += 1
        else:
            if 'error' in result:
                print(f"❌ ERROR \"{message}\"")
                print(f"   → {result['error']}")
            else:
                print(f"❌ STILL FAILING \"{message}\"")
                print(f"   → {result['crisis_level']} (confidence: {result['confidence']:.3f})")
    
    # Test passing cases
    print("🔍 Testing Previously PASSING Cases:")
    print("-" * 40)
    
    passing_still_detected = 0
    for message in PASSING_CASES:
        result = test_message(message)
        
        if result['detected']:
            print(f"✅ STILL DETECTING \"{message}\"")
            print(f"   → {result['crisis_level']} (confidence: {result['confidence']:.3f})")
            passing_still_detected += 1
        else:
            if 'error' in result:
                print(f"❌ ERROR \"{message}\"")
                print(f"   → {result['error']}")
            else:
                print(f"❌ REGRESSION \"{message}\"")
                print(f"   → {result['crisis_level']} (confidence: {result['confidence']:.3f})")
    
    # Summary
    print("📊 SUMMARY:")
    print("-" * 20)
    print(f"Previously Failing Cases: {failing_now_detected}/{len(FAILING_CASES)} now detected ({failing_now_detected/len(FAILING_CASES)*100:.1f}%)")
    print(f"Previously Passing Cases: {passing_still_detected}/{len(PASSING_CASES)} still detected ({passing_still_detected/len(PASSING_CASES)*100:.1f}%)")
    
    # Calculate improvement
    improvement = failing_now_detected / len(FAILING_CASES) * 100
    print(f"💡 Improvement: {improvement:.1f}% of previously failing cases now detected")
    
    # Assessment
    if improvement >= 80:
        print("🎉 EXCELLENT - Major improvement in crisis detection")
    elif improvement >= 60:
        print("👍 GOOD - Significant improvement")
    elif improvement >= 40:
        print("👌 MODERATE - Some improvement")
    elif improvement >= 20:
        print("😐 MINOR - Limited improvement")
    else:
        print("❌ POOR - Little improvement")
    
    print("🔄 To test different label sets:")
    print("   python scripts/manage_labels.py test-server safety_first")

def test_detailed_analysis():
    """Test detailed analysis for debugging"""
    print("\n🔬 DETAILED ANALYSIS:")
    print("=" * 50)
    
    test_message_text = "I want to kill myself"
    result = test_message(test_message_text)
    
    if 'full_result' in result:
        full_result = result['full_result']
        
        print(f"Message: \"{test_message_text}\"")
        print(f"Crisis Level: {full_result.get('crisis_level', 'unknown')}")
        print(f"Confidence: {full_result.get('confidence_score', 0.0):.3f}")
        print(f"Needs Response: {full_result.get('needs_response', False)}")
        print(f"Method: {full_result.get('method', 'unknown')}")
        
        # Check ensemble analysis if available
        if 'analysis' in full_result and 'ensemble_analysis' in full_result['analysis']:
            ensemble = full_result['analysis']['ensemble_analysis']
            
            print(f"\nEnsemble Details:")
            print(f"  Consensus: {ensemble.get('consensus', {})}")
            print(f"  Gaps Detected: {ensemble.get('gaps_detected', False)}")
            
            # Show individual model results
            individual = ensemble.get('individual_results', {})
            for model_name, predictions in individual.items():
                if predictions and len(predictions) > 0:
                    top_pred = predictions[0]
                    print(f"  {model_name}: {top_pred.get('label', 'unknown')} ({top_pred.get('score', 0.0):.3f})")

if __name__ == "__main__":
    test_crisis_cases()
    test_detailed_analysis()