#!/usr/bin/env python3
"""
Diagnostic tool to understand why HIGH crisis cases are failing
"""

import requests
from transformers import pipeline

def test_high_crisis_messages():
    """Test the specific HIGH crisis messages that are failing"""
    
    service_url = "http://localhost:8881"
    model_id = "rafalposwiata/deproberta-large-depression"
    
    # Load the model directly to see raw outputs
    print("🔬 Loading DepRoBERTa model directly...")
    nlp_model = pipeline("text-classification", model=model_id, device=-1, top_k=None)
    
    # The specific HIGH cases that are failing
    high_crisis_messages = [
        "Nobody would miss me if I was gone",
        "Life isn't worth living anymore", 
        "I want to kill myself",  # This should be working
        "I can't take it anymore, I'm going to end it all",  # This should be working
        "I have a plan to hurt myself tonight"  # This should be working
    ]
    
    print("\n🚨 HIGH CRISIS MESSAGE ANALYSIS")
    print("=" * 70)
    
    for message in high_crisis_messages:
        print(f"\n📝 Message: '{message}'")
        
        # Test direct model
        raw_output = nlp_model(message)
        print(f"   Raw Model Output: {raw_output}")
        
        if isinstance(raw_output, list) and len(raw_output) > 0:
            if isinstance(raw_output[0], list):
                predictions = raw_output[0]
            else:
                predictions = raw_output
            
            # Extract individual scores
            severe_score = 0.0
            moderate_score = 0.0
            not_depression_score = 0.0
            
            for pred in predictions:
                label = pred['label'].lower()
                score = pred['score']
                
                if 'severe' in label:
                    severe_score = score
                elif 'moderate' in label:
                    moderate_score = score
                elif 'not' in label:
                    not_depression_score = score
            
            print(f"   ➤ Severe: {severe_score:.4f}")
            print(f"   ➤ Moderate: {moderate_score:.4f}")
            print(f"   ➤ Not Depression: {not_depression_score:.4f}")
            
            # Apply our current scoring logic
            if severe_score > 0.01:
                our_score = 0.85 + (severe_score * 0.15)
                reason = f"severe_detected ({severe_score:.3f})"
            elif moderate_score > 0.25:
                our_score = 0.6 + (moderate_score * 0.4)
                reason = f"moderate_detected ({moderate_score:.3f})"
            elif not_depression_score > 0.85:
                our_score = 0.0
                reason = f"no_depression ({not_depression_score:.3f})"
            else:
                weighted_score = (severe_score * 1.0) + (moderate_score * 0.7) + (not_depression_score * -0.2)
                our_score = max(0.0, weighted_score)
                reason = f"mixed_signals"
            
            our_score = min(our_score, 1.0)
            
            # Determine level
            if our_score >= 0.60:
                level = "HIGH"
            elif our_score >= 0.45:
                level = "MEDIUM"
            elif our_score >= 0.10:
                level = "LOW"
            else:
                level = "NONE"
            
            print(f"   ➤ Our Score: {our_score:.4f} → {level} ({reason})")
            
            # Test service
            try:
                response = requests.post(f"{service_url}/analyze", json={
                    "message": message,
                    "user_id": "diagnostic",
                    "channel_id": "test"
                }, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    service_level = result['crisis_level']
                    service_score = result['confidence_score']
                    
                    match = "✅" if service_level.upper() == level else "❌"
                    print(f"   ➤ Service: {service_score:.4f} → {service_level.upper()} {match}")
                    
                    if service_level.upper() != "HIGH":
                        print(f"   ⚠️  CRITICAL: This should be HIGH but got {service_level.upper()}!")
                else:
                    print(f"   ❌ Service Error: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Service Error: {e}")
        
        print("-" * 50)
    
    print("\n💡 ANALYSIS SUMMARY:")
    print("- If severe scores are very low, the model might not be detecting severity properly")
    print("- If moderate scores are high but not triggering HIGH, we need to adjust logic")
    print("- Look for patterns in which messages the model struggles with")

if __name__ == "__main__":
    test_high_crisis_messages()