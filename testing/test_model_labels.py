#!/usr/bin/env python3
"""
Quick test to see what rafalposwiata/deproberta-large-depression actually outputs
"""

from transformers import pipeline

def test_depression_model():
    print("🔬 Testing rafalposwiata/deproberta-large-depression model")
    print("=" * 60)
    
    # Load the model
    model_id = "rafalposwiata/deproberta-large-depression"
    print(f"Loading: {model_id}")
    
    nlp_model = pipeline(
        "text-classification",
        model=model_id,
        device=-1,  # CPU
        top_k=None  # Return all labels
    )
    
    test_messages = [
        "Hello, how are you today?",           # Should be not depression
        "I feel sad sometimes",                # Mild
        "I hate myself and want to die",       # Should be severe
        "Life feels hopeless",                 # Should be moderate/severe
        "I love pizza!"                        # Should be not depression
    ]
    
    for message in test_messages:
        print(f"\n📝 Message: '{message}'")
        result = nlp_model(message)
        print(f"Raw result: {result}")
        
        # Parse the result
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                predictions = result[0]  # Nested format
            else:
                predictions = result     # Direct format
            
            print("Parsed predictions:")
            for pred in predictions:
                label = pred['label']
                score = pred['score']
                print(f"  {label}: {score:.4f}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_depression_model()