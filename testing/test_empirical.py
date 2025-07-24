#!/usr/bin/env python3
"""
Empirical approach: Let the model tell us what it thinks, then validate
"""

import requests
import time

def empirical_model_analysis():
    """Test the model and see what it naturally classifies as what"""
    
    service_url = "http://localhost:8881"
    
    # Clear examples for calibration
    test_messages = [
        # Definitely should be HIGH
        "I want to kill myself",
        "I have a gun and I'm going to use it on myself",
        "I can't take it anymore, I'm going to end it all",
        "I'm planning to jump off a bridge tomorrow",
        
        # Definitely should be NONE  
        "I love pizza",
        "What's the weather today?",
        "Thank you for helping me",
        "I'm excited about my vacation",
        "The movie was great",
        
        # Ambiguous cases - let's see what the model thinks
        "Nobody would miss me if I was gone",
        "Life isn't worth living anymore", 
        "I feel so depressed",
        "I hate myself",
        "I feel overwhelmed lately",
        "I'm having a bad day",
        "Everything feels pointless",
        "I'm disappointed in myself",
        "I'm really struggling right now",
        "I wish I could disappear",
    ]
    
    print("🔬 EMPIRICAL MODEL ANALYSIS")
    print("Let's see what the model naturally classifies...")
    print("=" * 60)
    
    results = []
    
    for message in test_messages:
        try:
            response = requests.post(f"{service_url}/analyze", json={
                "message": message,
                "user_id": "empirical_test", 
                "channel_id": "test"
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                level = result['crisis_level']
                score = result['confidence_score']
                
                print(f"📝 '{message[:40]}{'...' if len(message) > 40 else ''}'")
                print(f"   → {level.upper()} (score: {score:.3f})")
                
                results.append({
                    'message': message,
                    'level': level, 
                    'score': score
                })
                
            else:
                print(f"❌ Error for: {message}")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        time.sleep(0.1)  # Don't overwhelm service
        print()
    
    # Analyze the natural distribution
    print("=" * 60)
    print("📊 NATURAL MODEL DISTRIBUTION:")
    
    by_level = {}
    for r in results:
        level = r['level']
        if level not in by_level:
            by_level[level] = []
        by_level[level].append((r['message'], r['score']))
    
    for level in ['high', 'medium', 'low', 'none']:
        if level in by_level:
            cases = by_level[level]
            scores = [c[1] for c in cases]
            print(f"\n{level.upper()}: {len(cases)} cases")
            print(f"  Score range: {min(scores):.3f} - {max(scores):.3f}")
            for message, score in cases[:3]:  # Show first 3
                short_msg = message[:30] + "..." if len(message) > 30 else message
                print(f"    '{short_msg}' ({score:.3f})")
    
    print(f"\n💡 CALIBRATION INSIGHTS:")
    print("1. Are the clear HIGH cases actually getting HIGH?")
    print("2. Are the clear NONE cases actually getting NONE?") 
    print("3. Where do the ambiguous cases naturally fall?")
    print("4. Use this to set realistic expectations for test cases!")
    
    return results

if __name__ == "__main__":
    empirical_model_analysis()