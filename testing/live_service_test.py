#!/usr/bin/env python3
"""
Test the live service to see what scores it's actually generating
"""

import requests

def test_live_service():
    """Test a few key cases against the live service"""
    
    service_url = "http://localhost:8881"
    
    test_cases = [
        ("I hate myself and want to die", "high"),
        ("Life feels hopeless", "medium"),
        ("I feel sad sometimes", "low"),
        ("Hello, how are you today?", "none"),
        ("I wish I could just disappear", "medium"),
        ("Everything feels pointless", "medium"),
    ]
    
    print("🧪 LIVE SERVICE TEST")
    print("=" * 50)
    
    for message, expected in test_cases:
        try:
            response = requests.post(f"{service_url}/analyze", json={
                "message": message,
                "user_id": "test",
                "channel_id": "test"
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                predicted = result['crisis_level']
                confidence = result['confidence_score']
                
                status = "✅" if predicted == expected else "❌"
                print(f"{status} '{message}'")
                print(f"   Expected: {expected.upper()} | Got: {predicted.upper()} | Score: {confidence:.3f}")
                
                if predicted != expected:
                    print(f"   ⚠️  Score should be in range for {expected.upper()}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Failed to test: {e}")
        
        print()

if __name__ == "__main__":
    test_live_service()