#!/usr/bin/env python3
"""
Quick Test Script for Crisis Detection
Location: ash/ash-nlp/scripts/quick_test.py

Tests the key failing cases from your original comprehensive test
"""

import requests
import json

def test_crisis_detection():
    """Test the crisis detection with previously failing cases"""
    
    server_url = "http://localhost:8881"
    
    # Test cases that were failing in your 64% high crisis detection
    failing_cases = [
        "I have the pills ready",
        "Found the rope, it's time", 
        "Loading the gun now",
        "This is my final message",
        "Goodbye cruel world"
    ]
    
    # Test cases that were passing
    passing_cases = [
        "I want to kill myself",
        "Life isn't worth living anymore",
        "Going to kill myself after this"
    ]
    
    print("🧪 Quick Crisis Detection Test")
    print("=" * 50)
    print("Enhanced Crisis Labels + Optimized Models")
    print()
    
    # Test server connection
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not accessible")
            return
        print("✅ Server connection OK")
    except:
        print("❌ Server not accessible")
        return
    
    # Test label status
    try:
        response = requests.get(f"{server_url}/admin/labels/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Current label set: {status.get('current_label_set', 'unknown')}")
            print(f"✅ Models loaded: {status.get('models_loaded', False)}")
        else:
            print("⚠️ Could not get label status")
    except:
        print("⚠️ Could not get label status")
    
    print()
    
    # Test previously failing cases
    print("🔍 Testing Previously FAILING Cases:")
    print("-" * 40)
    failing_passed = 0
    
    for message in failing_cases:
        try:
            response = requests.post(
                f"{server_url}/analyze",
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                risk_level = result.get("risk_level", "unknown")
                confidence = result.get("confidence", 0.0)
                
                # Check if high crisis detected
                is_high = risk_level in ["high", "severe"]
                status = "✅ FIXED" if is_high else "❌ STILL FAILING"
                if is_high:
                    failing_passed += 1
                
                print(f"{status} \"{message}\"")
                print(f"   → {risk_level} (confidence: {confidence:.3f})")
            else:
                print(f"❌ ERROR \"{message}\" - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR \"{message}\" - {e}")
    
    print()
    
    # Test previously passing cases
    print("🔍 Testing Previously PASSING Cases:")
    print("-" * 40)
    passing_passed = 0
    
    for message in passing_cases:
        try:
            response = requests.post(
                f"{server_url}/analyze",
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                risk_level = result.get("risk_level", "unknown")
                confidence = result.get("confidence", 0.0)
                
                # Check if high crisis detected
                is_high = risk_level in ["high", "severe"]
                status = "✅ STILL PASSING" if is_high else "❌ REGRESSION"
                if is_high:
                    passing_passed += 1
                
                print(f"{status} \"{message}\"")
                print(f"   → {risk_level} (confidence: {confidence:.3f})")
            else:
                print(f"❌ ERROR \"{message}\" - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ ERROR \"{message}\" - {e}")
    
    print()
    
    # Summary
    print("📊 SUMMARY:")
    print("-" * 20)
    failing_rate = (failing_passed / len(failing_cases)) * 100
    passing_rate = (passing_passed / len(passing_cases)) * 100
    
    print(f"Previously Failing Cases: {failing_passed}/{len(failing_cases)} now detected ({failing_rate:.1f}%)")
    print(f"Previously Passing Cases: {passing_passed}/{len(passing_cases)} still detected ({passing_rate:.1f}%)")
    
    improvement = failing_rate
    print(f"\n💡 Improvement: {improvement:.1f}% of previously failing cases now detected")
    
    if improvement >= 80:
        print("🎉 EXCELLENT - Major improvement achieved!")
    elif improvement >= 60:
        print("✅ GOOD - Significant improvement")
    elif improvement >= 40:
        print("⚠️ MODERATE - Some improvement")
    else:
        print("❌ POOR - Little improvement")
    
    print(f"\n🔄 To test different label sets:")
    print(f"   python scripts/manage_labels.py test-server safety_first")

if __name__ == "__main__":
    test_crisis_detection()