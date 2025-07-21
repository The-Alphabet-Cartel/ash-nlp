#!/usr/bin/env python3
"""
Test script to understand what LABEL_0 and LABEL_1 actually mean in MentalRoBERTa
"""

import requests

def test_mental_roberta_labels():
    """Test various messages to understand label meanings"""
    
    service_url = "http://localhost:8881"
    
    # Test cases designed to reveal label meanings
    test_cases = [
        # VERY CLEARLY POSITIVE/NORMAL messages
        ("I love my family", "should_be_normal"),
        ("Today is a beautiful day", "should_be_normal"),  
        ("I'm so happy and excited", "should_be_normal"),
        ("Thank you for helping me", "should_be_normal"),
        ("I won the lottery!", "should_be_normal"),
        
        # NEUTRAL messages
        ("The weather is nice", "should_be_normal"),
        ("I went to the store", "should_be_normal"),
        ("What time is it?", "should_be_normal"),
        
        # CLEARLY MENTAL HEALTH related
        ("I want to kill myself", "should_be_mental_health"),
        ("I hate myself", "should_be_mental_health"),
        ("I feel depressed and hopeless", "should_be_mental_health"),
        ("I'm having suicidal thoughts", "should_be_mental_health"),
        ("I can't take the pain anymore", "should_be_mental_health"),
    ]
    
    print("🔬 TESTING MENTAL ROBERTA LABEL MEANINGS")
    print("=" * 60)
    print("We'll look for patterns to understand which label means what")
    print()
    
    results = []
    
    for message, expected_type in test_cases:
        try:
            response = requests.post(f"{service_url}/analyze", json={
                "message": message,
                "user_id": "label_test",
                "channel_id": "test"
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                categories = result.get('detected_categories', [])
                
                # Extract raw scores (look in service logs for the raw scores)
                print(f"📝 '{message}'")
                print(f"   Expected: {expected_type}")
                print(f"   Categories: {categories}")
                
                # We need to correlate this with the service logs
                results.append({
                    'message': message,
                    'expected_type': expected_type,
                    'categories': categories
                })
                
            else:
                print(f"❌ Error {response.status_code} for: {message}")
                
        except Exception as e:
            print(f"❌ Failed to test '{message}': {e}")
        
        print()
    
    print("\n💡 ANALYSIS INSTRUCTIONS:")
    print("1. Check the service logs for raw MentalRoBERTa scores")
    print("2. Look for patterns:")
    print("   - Do positive messages get higher LABEL_0 or LABEL_1?")
    print("   - Do mental health messages get higher LABEL_0 or LABEL_1?")
    print("3. The pattern will reveal the correct interpretation!")

def create_direct_test_script():
    """Create a script to test the model directly without the service"""
    
    script_content = '''#!/usr/bin/env python3
"""
Direct test of MentalRoBERTa to understand labels
"""

from transformers import pipeline
from huggingface_hub import login
import os

# Login if needed
hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN')
if hf_token:
    login(token=hf_token)

# Load the model
print("Loading MentalRoBERTa...")
model = pipeline(
    "text-classification",
    model="mental/mental-roberta-base",
    device=-1,
    top_k=None
)

# Test cases to understand labels
test_cases = [
    "I love my family and I'm so happy",
    "Today is a beautiful sunny day",
    "Thank you for all your help",
    "I want to kill myself",
    "I hate myself and feel hopeless", 
    "I'm having suicidal thoughts",
]

print("\\nTesting MentalRoBERTa label meanings:")
print("=" * 50)

for message in test_cases:
    result = model(message)
    print(f"\\nMessage: '{message}'")
    print(f"Result: {result}")
    
    # Extract scores for analysis
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], list):
            preds = result[0]
        else:
            preds = result
        
        for pred in preds:
            label = pred['label']
            score = pred['score']
            print(f"  {label}: {score:.4f}")

print("\\n💡 Look for patterns:")
print("- Positive messages: which label gets higher scores?")
print("- Mental health messages: which label gets higher scores?")
print("- This will reveal: LABEL_0 = ? and LABEL_1 = ?")
'''
    
    with open('direct_mental_roberta_test.py', 'w') as f:
        f.write(script_content)
    
    print("📝 Created 'direct_mental_roberta_test.py'")
    print("Run this script to test the model directly:")
    print("python direct_mental_roberta_test.py")

if __name__ == "__main__":
    print("Choose test method:")
    print("1. Test via service (requires service running)")
    print("2. Create direct test script")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        test_mental_roberta_labels()
    elif choice == "2":
        create_direct_test_script()
    else:
        print("Invalid choice")