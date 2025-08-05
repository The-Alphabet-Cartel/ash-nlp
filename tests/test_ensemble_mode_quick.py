#!/usr/bin/env python3
"""
Quick Ensemble Mode Validation Test
Tests whether changing NLP_ENSEMBLE_MODE produces different responses

This is a simplified version for quick validation during development.

Usage:
    python tests/test_ensemble_mode_quick.py [--mode MODE] [--message "MESSAGE"]
    
Examples:
    python tests/test_ensemble_mode_quick.py --mode weighted
    python tests/test_ensemble_mode_quick.py --mode consensus --message "I want to end it all"
"""

import os
import sys
import time
import json
import requests
import argparse
from pathlib import Path
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30
ENV_FILE_PATH = ".env"

# Default test message that should trigger different responses
DEFAULT_TEST_MESSAGE = "This exam is killing me but I think I can handle it"

def modify_env_variable(variable_name: str, new_value: str) -> bool:
    """Modify environment variable in .env file"""
    try:
        env_content = []
        variable_found = False
        
        # Read current content
        if os.path.exists(ENV_FILE_PATH):
            with open(ENV_FILE_PATH, 'r') as f:
                env_content = f.readlines()
        
        # Modify or add the variable
        for i, line in enumerate(env_content):
            if line.strip().startswith(f"{variable_name}="):
                env_content[i] = f"{variable_name}={new_value}\n"
                variable_found = True
                break
        
        # Add variable if not found
        if not variable_found:
            env_content.append(f"{variable_name}={new_value}\n")
        
        # Write back to file
        with open(ENV_FILE_PATH, 'w') as f:
            f.writelines(env_content)
        
        print(f"✅ Set {variable_name}={new_value} in .env file")
        return True
        
    except Exception as e:
        print(f"❌ Failed to modify .env file: {e}")
        return False

def get_ensemble_status() -> Dict[str, Any]:
    """Get current ensemble status from service"""
    try:
        response = requests.get(f"{BASE_URL}/ensemble/status", timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Could not get ensemble status: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Failed to get ensemble status: {e}")
        return {}

def analyze_message(message: str, user_id: str = "test_user", channel_id: str = "test_channel") -> Dict[str, Any]:
    """Analyze message with current ensemble configuration"""
    try:
        payload = {
            "message": message,
            "user_id": user_id,
            "channel_id": channel_id
        }
        
        response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {'success': False, 'error': f"HTTP {response.status_code}", 'response': response.text}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_key_metrics(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key metrics from analysis result for comparison"""
    if not analysis_result.get('success', False):
        return {'error': analysis_result.get('error', 'Unknown error')}
    
    data = analysis_result.get('data', {})
    ensemble_analysis = data.get('ensemble_analysis', {})
    consensus = ensemble_analysis.get('consensus', {})
    gap_detection = ensemble_analysis.get('gap_detection', {})
    individual_results = ensemble_analysis.get('individual_results', {})
    
    return {
        'prediction': consensus.get('prediction', 'unknown'),
        'confidence': round(consensus.get('confidence', 0), 4),
        'method': consensus.get('method', 'unknown'),
        'gap_detected': gap_detection.get('gap_detected', False),
        'requires_review': gap_detection.get('requires_review', False),
        'model_count': len([k for k, v in individual_results.items() if v]),
        'depression_prediction': individual_results.get('depression', [{}])[0].get('label', 'unknown') if individual_results.get('depression') else 'none',
        'sentiment_prediction': individual_results.get('sentiment', [{}])[0].get('label', 'unknown') if individual_results.get('sentiment') else 'none',
        'emotional_distress_prediction': individual_results.get('emotional_distress', [{}])[0].get('label', 'unknown') if individual_results.get('emotional_distress') else 'none'
    }

def test_single_mode(mode: str, message: str) -> Dict[str, Any]:
    """Test analysis with a specific ensemble mode"""
    print(f"\n🔍 Testing {mode.upper()} mode")
    print("-" * 40)
    
    # Set the mode
    if not modify_env_variable("NLP_ENSEMBLE_MODE", mode):
        return {'error': f'Failed to set mode to {mode}'}
    
    # Wait for config to reload
    print("⏳ Waiting for configuration to reload...")
    time.sleep(3)
    
    # Verify the mode was set
    status = get_ensemble_status()
    current_mode = status.get('ensemble_info', {}).get('ensemble_mode', 'unknown')
    
    if current_mode.lower() != mode.lower():
        print(f"⚠️ Warning: Expected mode {mode}, service reports {current_mode}")
    else:
        print(f"✅ Confirmed ensemble mode: {current_mode}")
    
    # Run analysis
    print(f"📝 Analyzing: '{message}'")
    result = analyze_message(message)
    
    if result['success']:
        metrics = extract_key_metrics(result)
        print(f"📊 Result: {metrics['prediction']} (confidence: {metrics['confidence']})")
        print(f"🔍 Method: {metrics['method']}")
        print(f"⚠️ Gap detected: {metrics['gap_detected']}")
        print(f"👁️ Requires review: {metrics['requires_review']}")
        print(f"🧠 Models: Depression={metrics['depression_prediction']}, Sentiment={metrics['sentiment_prediction']}, Distress={metrics['emotional_distress_prediction']}")
        
        return {'success': True, 'mode': mode, 'metrics': metrics, 'raw_data': result['data']}
    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        return {'success': False, 'mode': mode, 'error': result.get('error')}

def compare_results(results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Compare results between different modes"""
    print(f"\n📊 COMPARISON ANALYSIS")
    print("=" * 60)
    
    successful_results = {mode: data for mode, data in results.items() if data.get('success', False)}
    
    if len(successful_results) < 2:
        print("❌ Not enough successful results to compare")
        return {'error': 'Insufficient successful results'}
    
    # Compare all pairs
    modes = list(successful_results.keys())
    differences = []
    
    for i, mode1 in enumerate(modes):
        for mode2 in modes[i+1:]:
            metrics1 = successful_results[mode1]['metrics']
            metrics2 = successful_results[mode2]['metrics']
            
            pair_diff = {
                'modes': f"{mode1} vs {mode2}",
                'prediction_different': metrics1['prediction'] != metrics2['prediction'],
                'confidence_difference': abs(metrics1['confidence'] - metrics2['confidence']),
                'method_different': metrics1['method'] != metrics2['method'],
                'gap_detection_different': metrics1['gap_detected'] != metrics2['gap_detected'],
                'review_requirement_different': metrics1['requires_review'] != metrics2['requires_review']
            }
            
            differences.append(pair_diff)
            
            print(f"\n🔄 {pair_diff['modes']}:")
            print(f"   Prediction: {metrics1['prediction']} vs {metrics2['prediction']} {'(DIFFERENT)' if pair_diff['prediction_different'] else '(SAME)'}")
            print(f"   Confidence: {metrics1['confidence']} vs {metrics2['confidence']} (diff: {pair_diff['confidence_difference']:.4f})")
            print(f"   Method: {metrics1['method']} vs {metrics2['method']} {'(DIFFERENT)' if pair_diff['method_different'] else '(SAME)'}")
            print(f"   Gap Detection: {metrics1['gap_detected']} vs {metrics2['gap_detected']} {'(DIFFERENT)' if pair_diff['gap_detection_different'] else '(SAME)'}")
            print(f"   Review Required: {metrics1['requires_review']} vs {metrics2['requires_review']} {'(DIFFERENT)' if pair_diff['review_requirement_different'] else '(SAME)'}")
    
    # Summary
    total_differences = sum([
        sum([
            diff['prediction_different'],
            diff['confidence_difference'] > 0.05,
            diff['method_different'],
            diff['gap_detection_different'],
            diff['review_requirement_different']
        ]) for diff in differences
    ])
    
    print(f"\n🎯 SUMMARY:")
    print(f"   Total measurable differences found: {total_differences}")
    
    if total_differences > 0:
        print("   ✅ ENSEMBLE MODES ARE WORKING - Different modes produce different results!")
    else:
        print("   ❌ ENSEMBLE MODES MAY NOT BE WORKING - All modes produce identical results")
    
    return {
        'total_differences': total_differences,
        'differences': differences,
        'modes_working': total_differences > 0
    }

def test_all_modes(message: str) -> Dict[str, Any]:
    """Test all three ensemble modes with the same message"""
    modes = ['consensus', 'majority', 'weighted']
    results = {}
    
    print(f"🚀 Testing all ensemble modes with message:")
    print(f"📝 '{message}'")
    print("=" * 80)
    
    for mode in modes:
        results[mode] = test_single_mode(mode, message)
        time.sleep(1)  # Brief pause between tests
    
    # Compare results
    comparison = compare_results(results)
    
    return {
        'message': message,
        'results': results,
        'comparison': comparison
    }

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test Ash-NLP ensemble mode switching')
    parser.add_argument('--mode', choices=['consensus', 'majority', 'weighted', 'all'], 
                       default='all', help='Ensemble mode to test (default: all)')
    parser.add_argument('--message', default=DEFAULT_TEST_MESSAGE, 
                       help='Message to analyze (default: exam killing message)')
    parser.add_argument('--save', action='store_true', 
                       help='Save results to JSON file')
    
    args = parser.parse_args()
    
    print("🧪 Quick Ensemble Mode Validation Test")
    print("=" * 50)
    
    # Check service health first
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Service not healthy: {response.status_code}")
            return 1
        else:
            print("✅ Service is healthy")
    except Exception as e:
        print(f"❌ Cannot reach service: {e}")
        return 1
    
    if args.mode == 'all':
        # Test all modes
        test_results = test_all_modes(args.message)
        
        if args.save:
            filename = f"ensemble_mode_test_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(test_results, f, indent=2, default=str)
            print(f"\n💾 Results saved to {filename}")
        
        # Return appropriate exit code
        comparison = test_results.get('comparison', {})
        if comparison.get('modes_working', False):
            print(f"\n✅ TEST PASSED - Ensemble modes are working!")
            return 0
        else:
            print(f"\n❌ TEST FAILED - Ensemble modes may not be working!")
            return 1
    
    else:
        # Test single mode
        result = test_single_mode(args.mode, args.message)
        
        if result.get('success', False):
            print(f"\n✅ {args.mode.upper()} mode test completed successfully")
            return 0
        else:
            print(f"\n❌ {args.mode.upper()} mode test failed")
            return 1

if __name__ == "__main__":
    sys.exit(main())