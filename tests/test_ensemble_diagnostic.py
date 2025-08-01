#!/usr/bin/env python3
"""
Ensemble Diagnostic Test Script
Diagnoses exactly what each model in the Three Zero-Shot Model Ensemble is returning
Location: ash/ash-nlp/tests/test_ensemble_diagnostic.py
"""

import requests
import json
import sys

NLP_SERVER_URL = "http://localhost:8881"

# Test phrase that's clearly very negative
TEST_PHRASE = "I want to end everything right now, I can't take this pain anymore"

def get_detailed_analysis():
    """Get detailed analysis of a clearly negative phrase"""
    print("🔍 ENSEMBLE DIAGNOSTIC TEST")
    print("=" * 60)
    print(f"Test Phrase: \"{TEST_PHRASE}\"")
    print(f"Expected: Very Negative sentiment → High crisis")
    print()
    
    # Send to ensemble endpoint
    try:
        payload = {"message": TEST_PHRASE}
        response = requests.post(f"{NLP_SERVER_URL}/analyze", json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            return
        
        result = response.json()
        
        # Pretty print the full response
        print("📋 FULL ENSEMBLE RESPONSE:")
        print("-" * 40)
        print(json.dumps(result, indent=2))
        print()
        
        # Extract and analyze ensemble_analysis section
        if 'ensemble_analysis' in result:
            ensemble = result['ensemble_analysis']
            
            print("🔬 INDIVIDUAL MODEL RESULTS:")
            print("-" * 40)
            
            individual_results = ensemble.get('individual_results', {})
            
            # Analyze each model
            for model_name, model_results in individual_results.items():
                print(f"\n{model_name.upper()} MODEL:")
                if isinstance(model_results, list):
                    for i, pred in enumerate(model_results):
                        label = pred.get('label', 'unknown')
                        score = pred.get('score', 0.0)
                        print(f"   {i+1}. {label}: {score:.3f}")
                else:
                    print(f"   Result: {model_results}")
            
            # Analyze consensus
            print(f"\n🤝 CONSENSUS ANALYSIS:")
            print("-" * 40)
            consensus = ensemble.get('consensus', {})
            if consensus:
                print(f"   Prediction: {consensus.get('prediction', 'unknown')}")
                print(f"   Confidence: {consensus.get('confidence', 0.0):.3f}")
                print(f"   Method: {consensus.get('method', 'unknown')}")
            
            # Check for gaps
            gaps_detected = ensemble.get('gaps_detected', False)
            print(f"\n⚠️  GAPS DETECTED: {gaps_detected}")
            if gaps_detected:
                gap_details = ensemble.get('gap_details', [])
                for gap in gap_details:
                    print(f"   Gap Type: {gap.get('type', 'unknown')}")
                    if 'spread' in gap:
                        print(f"   Confidence Spread: {gap['spread']:.3f}")
            
            # Check confidence scores
            print(f"\n📊 CONFIDENCE SCORES:")
            print("-" * 40)
            confidence_scores = ensemble.get('confidence_scores', {})
            for model, score in confidence_scores.items():
                print(f"   {model}: {score:.3f}")
            
            # Check predictions mapping
            print(f"\n🎯 PREDICTIONS MAPPING:")
            print("-" * 40)
            predictions = ensemble.get('predictions', {})
            for model, pred in predictions.items():
                print(f"   {model}: {pred}")
            
            # Check normalized predictions
            if 'normalized_predictions' in ensemble:
                print(f"\n🔄 NORMALIZED PREDICTIONS:")
                print("-" * 40)
                normalized = ensemble.get('normalized_predictions', {})
                for model, norm_pred in normalized.items():
                    print(f"   {model}: {norm_pred}")
        
        # Top-level response analysis
        print(f"\n📈 TOP-LEVEL RESPONSE:")
        print("-" * 40)
        print(f"   Crisis Level: {result.get('crisis_level', 'unknown')}")
        print(f"   Consensus Prediction: {result.get('consensus_prediction', 'unknown')}")
        print(f"   Consensus Confidence: {result.get('consensus_confidence', 0.0):.3f}")
        print(f"   Consensus Method: {result.get('consensus_method', 'unknown')}")
        print(f"   Needs Response: {result.get('needs_response', False)}")
        print(f"   Requires Staff Review: {result.get('requires_staff_review', False)}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

def test_individual_models():
    """Test what individual models would return (if endpoints exist)"""
    print(f"\n🧪 INDIVIDUAL MODEL TESTING:")
    print("=" * 60)
    
    # Note: These endpoints might not exist, but let's try
    endpoints_to_try = [
        "/analyze_depression",
        "/analyze_sentiment", 
        "/analyze_distress"
    ]
    
    for endpoint in endpoints_to_try:
        try:
            payload = {"message": TEST_PHRASE}
            response = requests.post(f"{NLP_SERVER_URL}{endpoint}", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ {endpoint}:")
                print(json.dumps(result, indent=2))
            else:
                print(f"\n❌ {endpoint}: Not available ({response.status_code})")
                
        except Exception as e:
            print(f"\n❌ {endpoint}: Failed ({e})")

if __name__ == "__main__":
    print("🐳 Running Ensemble Diagnostic Test")
    print(f"📍 Server: {NLP_SERVER_URL}")
    print()
    
    get_detailed_analysis()
    test_individual_models()
    
    print(f"\n💡 DIAGNOSTIC COMPLETE")
    print("=" * 60)
    print("This diagnostic will help identify:")
    print("• What each model in the ensemble is actually returning")
    print("• How the consensus mechanism is working") 
    print("• Where the sentiment → crisis mapping might be failing")
    print("• Why 'Very Negative' phrases appear as 'Very Positive' in results")