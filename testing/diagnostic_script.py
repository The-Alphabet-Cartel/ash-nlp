#!/usr/bin/env python3
"""
Quick diagnostic script to see raw model outputs
"""

import requests
import json

def test_specific_messages():
    """Test specific messages to understand model behavior"""
    
    service_url = "http://localhost:8881"
    
    # Test cases that should be NONE (no crisis)
    test_messages = [
        "What's the weather like today?",
        "I love pizza so much!",
        "Thanks for helping me with that",
        "How was your day?",
        "Going to watch a movie tonight",
        # Test cases that should be crisis
        "I want to kill myself",
        "I feel so depressed",
        "I'm feeling really sad today"
    ]
    
    print("🔍 DIAGNOSTIC: Raw Model Outputs")
    print("=" * 60)
    
    for message in test_messages:
        print(f"\nMessage: '{message}'")
        
        try:
            response = requests.post(f"{service_url}/analyze", json={
                "message": message,
                "user_id": "diagnostic",
                "channel_id": "test"
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  Predicted Level: {result['crisis_level']}")
                print(f"  Confidence Score: {result['confidence_score']:.4f}")
                print(f"  Categories: {result['detected_categories']}")
                print(f"  Method: {result['method']}")
            else:
                print(f"  ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("💡 Analysis:")
    print("- Check if NONE messages are getting crisis scores > 0")
    print("- Look at the confidence patterns")
    print("- See if categories make sense")

if __name__ == "__main__":
    test_specific_messages()