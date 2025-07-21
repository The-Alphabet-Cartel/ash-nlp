#!/usr/bin/env python3
"""
Test the improved scoring logic against known cases
"""

def test_improved_scoring():
    """Test scoring improvements against your actual model outputs"""
    
    print("🧪 TESTING IMPROVED SCORING LOGIC")
    print("=" * 50)
    
    # Based on your model test results, these are the actual ML outputs
    test_cases = [
        {
            "message": "I hate myself and want to die",
            "expected_level": "high",
            "ml_output": {
                "not depression": 0.3457,
                "moderate": 0.5960,
                "severe": 0.0583
            }
        },
        {
            "message": "Life feels hopeless", 
            "expected_level": "medium",
            "ml_output": {
                "not depression": 0.5106,
                "moderate": 0.4840,
                "severe": 0.0055
            }
        },
        {
            "message": "I feel sad sometimes",
            "expected_level": "low", 
            "ml_output": {
                "not depression": 0.5390,
                "moderate": 0.4550,
                "severe": 0.0061
            }
        },
        {
            "message": "Hello, how are you today?",
            "expected_level": "none",
            "ml_output": {
                "not depression": 0.9879,
                "moderate": 0.0097,
                "severe": 0.0024
            }
        },
        {
            "message": "I love pizza!",
            "expected_level": "none",
            "ml_output": {
                "not depression": 0.9254,
                "moderate": 0.0676,
                "severe": 0.0071
            }
        }
    ]
    
    for case in test_cases:
        print(f"\n📝 Testing: '{case['message']}'")
        print(f"Expected: {case['expected_level'].upper()}")
        
        ml_output = case['ml_output']
        not_depression = ml_output['not depression']
        moderate = ml_output['moderate'] 
        severe = ml_output['severe']
        
        print(f"ML Scores: not={not_depression:.3f}, moderate={moderate:.3f}, severe={severe:.3f}")
        
        # Apply improved scoring logic
        total_depression = moderate + severe
        
        if severe > 0.03:
            base_score = 0.60
            severe_boost = severe * 8.0
            moderate_boost = moderate * 2.0
            crisis_score = base_score + severe_boost + moderate_boost
            logic = f"severe_amplified ({severe:.3f}*8 + {moderate:.3f}*2)"
            
        elif moderate > 0.30:
            base_score = 0.35
            moderate_boost = moderate * 3.0
            uncertainty_boost = max(0, 0.7 - not_depression) * 0.5
            crisis_score = base_score + moderate_boost + uncertainty_boost
            logic = f"moderate_amplified ({moderate:.3f}*3 + uncertainty={uncertainty_boost:.3f})"
            
        elif total_depression > 0.20:
            base_score = 0.15
            depression_boost = total_depression * 2.0
            crisis_score = base_score + depression_boost
            logic = f"weak_depression ({total_depression:.3f}*2)"
            
        elif not_depression > 0.85:
            crisis_score = 0.0
            logic = f"confident_not_depression ({not_depression:.3f})"
            
        else:
            crisis_score = total_depression * 0.8
            logic = f"unclear_signals ({total_depression:.3f}*0.8)"
        
        # Apply bounds
        crisis_score = min(max(crisis_score, 0.0), 1.0)
        
        # Map to level
        if crisis_score >= 0.65:
            predicted_level = "high"
        elif crisis_score >= 0.30:
            predicted_level = "medium"
        elif crisis_score >= 0.10:
            predicted_level = "low"
        else:
            predicted_level = "none"
        
        # Check result
        correct = predicted_level == case['expected_level']
        status = "✅" if correct else "❌"
        
        print(f"Logic: {logic}")
        print(f"Crisis Score: {crisis_score:.3f}")
        print(f"Predicted: {predicted_level.upper()} {status}")
        
        if not correct:
            print(f"⚠️  MISMATCH: Expected {case['expected_level'].upper()}, got {predicted_level.upper()}")
        
        print("-" * 40)
    
    print(f"\n💡 KEY IMPROVEMENTS:")
    print(f"• Severe signals (>0.03) get 8x amplification + base 0.60")
    print(f"• Moderate signals (>0.30) get 3x amplification + base 0.35") 
    print(f"• Uncertainty boost when model unsure about 'not depression'")
    print(f"• Higher thresholds (0.65/0.30/0.10) to match amplified scores")

if __name__ == "__main__":
    test_improved_scoring()