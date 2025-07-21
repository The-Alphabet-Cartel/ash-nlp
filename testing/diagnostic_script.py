#!/usr/bin/env python3
"""
Deep diagnostic script to see raw model outputs and understand the issue
"""

import requests
import json
from transformers import pipeline

def test_model_directly():
    """Test the model directly to see raw LABEL_0/LABEL_1 outputs"""
    
    print("🔬 DEEP DIAGNOSTIC: Direct Model Testing")
    print("=" * 60)
    
    # Load the same model as the service - test original model with switched labels theory
    model_id = "mrm8488/distilroberta-base-finetuned-suicide-depression"
    
    print(f"Loading model: {model_id}")
    nlp_model = pipeline(
        "text-classification",
        model=model_id,
        device=-1,
        top_k=None
    )
    
    test_messages = [
        "What's the weather like today?",  # Should be LABEL_0 high
        "I love pizza so much!",           # Should be LABEL_0 high  
        "Thanks for helping me",           # Should be LABEL_0 high
        "I want to kill myself",           # Should be LABEL_1 high
        "I feel so depressed",             # Should be LABEL_1 high
        "I'm feeling really sad today"     # Should be LABEL_1 medium
    ]
    
    for message in test_messages:
        print(f"\n📝 Message: '{message}'")
        
        # Get raw model output
        raw_output = nlp_model(message)
        print(f"   Raw Output: {raw_output}")
        
        # Extract scores if nested
        if isinstance(raw_output, list) and len(raw_output) > 0:
            if isinstance(raw_output[0], list):
                predictions = raw_output[0]
            else:
                predictions = raw_output
            
            label_0_score = 0
            label_1_score = 0
            
            for pred in predictions:
                if pred['label'] == 'LABEL_0':
                    label_0_score = pred['score']
                elif pred['label'] == 'LABEL_1':
                    label_1_score = pred['score']
            
            print(f"   LABEL_0 (no risk): {label_0_score:.4f}")
            print(f"   LABEL_1 (risk): {label_1_score:.4f}")
            print(f"   Winner: {'LABEL_1' if label_1_score > label_0_score else 'LABEL_0'}")
            
            # Test our analysis logic
            if label_1_score > label_0_score:
                confidence_margin = label_1_score - label_0_score
                crisis_score = label_1_score + (confidence_margin * 0.2)
                crisis_score = min(crisis_score, 1.0)
            else:
                crisis_score = label_1_score * 0.5
            
            if label_1_score < 0.2:
                crisis_score = 0.0
                
            print(f"   Our Analysis → Crisis Score: {crisis_score:.4f}")

def test_service_vs_direct():
    """Compare service output vs direct model output"""
    
    print(f"\n🔄 COMPARISON: Service vs Direct Model")
    print("=" * 60)
    
    service_url = "http://localhost:8881"
    
    test_message = "Thanks for helping me"
    print(f"Testing: '{test_message}'")
    
    # Test service
    try:
        response = requests.post(f"{service_url}/analyze", json={
            "message": test_message,
            "user_id": "diagnostic",
            "channel_id": "test"
        }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Service Result:")
            print(f"  Level: {result['crisis_level']}")
            print(f"  Score: {result['confidence_score']:.4f}")
            print(f"  Categories: {result['detected_categories']}")
        else:
            print(f"Service Error: {response.status_code}")
            
    except Exception as e:
        print(f"Service Error: {e}")

if __name__ == "__main__":
    test_model_directly()
    test_service_vs_direct()