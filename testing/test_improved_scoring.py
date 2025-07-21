#!/usr/bin/env python3
"""
Test the fine-tuned scoring logic
"""

def test_fine_tuned_scoring():
    """Test fine-tuned scoring with adjusted MEDIUM threshold"""
    
    print("🧪 TESTING FINE-TUNED SCORING LOGIC")
    print("Adjustment: MEDIUM threshold raised from 0.35 to 0.47")
    print("=" * 60)
    
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
        
        # Apply fine-tuned scoring logic
        total_depression = moderate + severe
        
        # TIER 1: Strong severe signals → HIGH (0.70-1.00)
        if severe > 0.05:
            base_score = 0.70
            severe_boost = severe * 4.0
            moderate_support = moderate * 0.5
            crisis_score = base_score + severe_boost + moderate_support
            logic = f"strong_severe (0.70 + {severe:.3f}*4 + {moderate:.3f}*0.5)"
            
        # TIER 2: Very strong moderate signals → HIGH (0.70-1.00)  
        elif moderate > 0.60:
            base_score = 0.70
            moderate_boost = (moderate - 0.60) * 2.0
            crisis_score = base_score + moderate_boost
            logic = f"very_strong_moderate (0.70 + excess={moderate-0.60:.3f}*2)"
            
        # TIER 3: Strong moderate signals → MEDIUM (0.40-0.69)
        # ADJUSTED: threshold raised to 0.47
        elif moderate > 0.47:
            base_score = 0.40
            moderate_boost = (moderate - 0.47) * 1.5
            severe_support = severe * 2.0
            crisis_score = base_score + moderate_boost + severe_support
            logic = f"strong_moderate (0.40 + excess={moderate-0.47:.3f}*1.5 + {severe:.3f}*2)"
            
        # TIER 4: Moderate depression signals → LOW (0.15-0.39)
        elif moderate > 0.20:
            base_score = 0.15
            moderate_boost = moderate * 0.5
            severe_support = severe * 3.0
            crisis_score = base_score + moderate_boost + severe_support
            logic = f"moderate_depression (0.15 + {moderate:.3f}*0.5 + {severe:.3f}*3)"
            
        # TIER 5: Very confident not depression → NONE (0.00)
        elif not_depression > 0.85:
            crisis_score = 0.0
            logic = f"confident_not_depression ({not_depression:.3f})"
            
        # TIER 6: Weak signals → LOW (0.05-0.20)
        elif total_depression > 0.10:
            base_score = 0.05
            depression_boost = total_depression * 0.5
            crisis_score = base_score + depression_boost
            logic = f"weak_depression (0.05 + {total_depression:.3f}*0.5)"
            
        # TIER 7: No significant signal → NONE (0.00)
        else:
            crisis_score = 0.0
            logic = f"no_significant_signal ({total_depression:.3f})"
        
        # Apply bounds
        crisis_score = min(max(crisis_score, 0.0), 1.0)
        
        # Map to level using thresholds
        if crisis_score >= 0.70:
            predicted_level = "high"
        elif crisis_score >= 0.40:
            predicted_level = "medium"
        elif crisis_score >= 0.15:
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
        
        print("-" * 50)
    
    print(f"\n💡 FINE-TUNED CHANGES:")
    print(f"• MEDIUM threshold: 0.35 → 0.47 (more selective)")
    print(f"• This should move 'I feel sad sometimes' from MEDIUM to LOW")
    print(f"• 'Life feels hopeless' (0.484 moderate) should still be MEDIUM")

if __name__ == "__main__":
    test_fine_tuned_scoring()