#!/usr/bin/env python3
"""
Test the balanced scoring logic
"""

def test_balanced_scoring():
    """Test balanced scoring against known cases"""
    
    print("🧪 TESTING BALANCED SCORING LOGIC")
    print("Target: HIGH=0.70+, MEDIUM=0.40-0.69, LOW=0.15-0.39, NONE=0.00-0.14")
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
        
        # Apply balanced scoring logic
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
        elif moderate > 0.35:
            base_score = 0.40
            moderate_boost = (moderate - 0.35) * 1.0
            severe_support = severe * 2.0
            crisis_score = base_score + moderate_boost + severe_support
            logic = f"strong_moderate (0.40 + excess={moderate-0.35:.3f} + {severe:.3f}*2)"
            
        # TIER 4: Moderate depression signals → LOW/MEDIUM (0.15-0.40)
        elif moderate > 0.20:
            base_score = 0.15
            moderate_boost = moderate * 0.6
            severe_support = severe * 3.0
            crisis_score = base_score + moderate_boost + severe_support
            logic = f"moderate_depression (0.15 + {moderate:.3f}*0.6 + {severe:.3f}*3)"
            
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
        
        # Map to level using balanced thresholds
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
    
    print(f"\n💡 BALANCED APPROACH:")
    print(f"• Severe signals (>0.05): 0.70 base + 4x boost → HIGH")
    print(f"• Very strong moderate (>0.60): 0.70 base + 2x excess → HIGH") 
    print(f"• Strong moderate (>0.35): 0.40 base + 1x excess → MEDIUM")
    print(f"• Moderate signals (>0.20): 0.15 base + 0.6x boost → LOW/MEDIUM")
    print(f"• Clear score ranges: HIGH≥0.70, MEDIUM≥0.40, LOW≥0.15")

if __name__ == "__main__":
    test_balanced_scoring()