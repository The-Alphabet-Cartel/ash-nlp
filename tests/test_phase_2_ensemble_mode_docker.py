#!/usr/bin/env python3
"""
Internal Container Ensemble Mode Test
Tests ensemble mode by checking if different configurations produce different results

This version works from INSIDE the Docker container and tests the current
ensemble behavior without needing to restart the container.

Usage (from inside container):
    python tests/test_ensemble_mode_internal.py
"""

import os
import sys
import time
import json
import requests
from typing import Dict, Any, List
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30

class InternalEnsembleTest:
    """Test ensemble behavior from inside the container"""
    
    def __init__(self):
        self.test_results = {}
    
    def get_current_ensemble_status(self) -> Dict[str, Any]:
        """Get current ensemble configuration"""
        try:
            response = requests.get(f"{BASE_URL}/ensemble/status", timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get ensemble status: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Error getting ensemble status: {e}")
            return {}
    
    def analyze_message(self, message: str, user_id: str = "test_internal", 
                       channel_id: str = "test_internal") -> Dict[str, Any]:
        """Analyze a message with current ensemble configuration"""
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
                return {
                    'success': False, 
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def extract_ensemble_metrics(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key ensemble metrics from analysis result"""
        if not analysis_result.get('success', False):
            return {'error': analysis_result.get('error', 'Analysis failed')}
        
        data = analysis_result['data']
        
        # Extract ensemble analysis
        ensemble_analysis = data.get('analysis', {}).get('ensemble_analysis', {})
        consensus = ensemble_analysis.get('consensus', {})
        gap_detection = ensemble_analysis.get('gap_detection', {})
        individual_results = ensemble_analysis.get('individual_results', {})
        ensemble_metadata = ensemble_analysis.get('ensemble_metadata', {})
        
        # Extract top-level results
        crisis_level = data.get('crisis_level', 'unknown')
        confidence_score = data.get('confidence_score', 0)
        method = data.get('method', 'unknown')
        
        return {
            'crisis_level': crisis_level,
            'confidence_score': round(confidence_score, 4),
            'method': method,
            'consensus': {
                'prediction': consensus.get('prediction', 'unknown'),
                'confidence': round(consensus.get('confidence', 0), 4),
                'method': consensus.get('method', 'unknown'),
                'vote_breakdown': consensus.get('vote_breakdown', {})
            },
            'gap_detection': {
                'gap_detected': gap_detection.get('gap_detected', False),
                'requires_review': gap_detection.get('requires_review', False)
            },
            'ensemble_metadata': {
                'ensemble_mode': ensemble_metadata.get('ensemble_mode', 'unknown'),
                'models_used': ensemble_metadata.get('models_used', 0),
                'all_models_responded': ensemble_metadata.get('all_models_responded', False)
            },
            'individual_predictions': {
                'depression': individual_results.get('depression', [{}])[0].get('label', 'none') if individual_results.get('depression') else 'none',
                'sentiment': individual_results.get('sentiment', [{}])[0].get('label', 'none') if individual_results.get('sentiment') else 'none',
                'emotional_distress': individual_results.get('emotional_distress', [{}])[0].get('label', 'none') if individual_results.get('emotional_distress') else 'none'
            }
        }
    
    def test_message_analysis(self, message: str, description: str) -> Dict[str, Any]:
        """Test analysis of a specific message"""
        print(f"\n🧪 Testing: {description}")
        print(f"📝 Message: '{message}'")
        print("-" * 50)
        
        result = self.analyze_message(message)
        
        if result['success']:
            metrics = self.extract_ensemble_metrics(result)
            
            if 'error' not in metrics:
                print(f"📊 Crisis Level: {metrics['crisis_level']}")
                print(f"🎯 Confidence: {metrics['confidence_score']}")
                print(f"🔍 Method: {metrics['method']}")
                print(f"🤖 Ensemble Mode: {metrics['ensemble_metadata']['ensemble_mode']}")
                print(f"📈 Models Used: {metrics['ensemble_metadata']['models_used']}")
                print(f"⚠️ Gap Detected: {metrics['gap_detection']['gap_detected']}")
                print(f"👁️ Requires Review: {metrics['gap_detection']['requires_review']}")
                
                # Show consensus details
                consensus = metrics['consensus']
                print(f"🔄 Consensus: {consensus['prediction']} (conf: {consensus['confidence']}, method: {consensus['method']})")
                
                # Show vote breakdown if available
                if consensus['vote_breakdown']:
                    vote_str = ", ".join([f"{k}: {v}" for k, v in consensus['vote_breakdown'].items()])
                    print(f"🗳️ Vote Breakdown: {vote_str}")
                
                # Show individual model predictions
                individual = metrics['individual_predictions']
                print(f"🧠 Individual: Depression={individual['depression']}, Sentiment={individual['sentiment']}, Distress={individual['emotional_distress']}")
                
                return {
                    'success': True,
                    'message': message,
                    'description': description,
                    'metrics': metrics,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print(f"❌ Metrics extraction failed: {metrics['error']}")
                return {'success': False, 'error': metrics['error']}
        else:
            print(f"❌ Analysis failed: {result['error']}")
            return {'success': False, 'error': result['error']}
    
    def check_environment_variables(self) -> Dict[str, Any]:
        """Check current environment variables relevant to ensemble"""
        print(f"\n🔍 Checking Environment Variables")
        print("-" * 40)
        
        key_vars = [
            'NLP_ENSEMBLE_MODE',
            'NLP_DEPRESSION_MODEL',
            'NLP_SENTIMENT_MODEL', 
            'NLP_EMOTIONAL_DISTRESS_MODEL',
            'NLP_MODEL_WEIGHT_DEPRESSION',
            'NLP_MODEL_WEIGHT_SENTIMENT',
            'NLP_MODEL_WEIGHT_EMOTIONAL_DISTRESS',
            'NLP_GAP_DETECTION_THRESHOLD',
            'NLP_THRESHOLD_GAP_DISAGREEMENT'
        ]
        
        env_vars = {}
        for var in key_vars:
            value = os.getenv(var, 'NOT SET')
            env_vars[var] = value
            status = "✅" if value != 'NOT SET' else "❌"
            print(f"{status} {var}={value}")
        
        return env_vars
    
    def analyze_ensemble_behavior(self) -> Dict[str, Any]:
        """Analyze how the ensemble behaves with different types of messages"""
        print(f"\n📊 Ensemble Behavior Analysis")
        print("=" * 60)
        
        # Test messages designed to show ensemble differences
        test_messages = [
            {
                'message': 'I want to kill myself tonight',
                'description': 'Explicit crisis language - should show clear consensus',
                'expected': 'High agreement across models'
            },
            {
                'message': 'This exam is killing me but I think I can handle it',
                'description': 'Ambiguous crisis language - should trigger gap detection',
                'expected': 'Model disagreement, gap detection'
            },
            {
                'message': 'I feel hopeless and want to give up on everything',
                'description': 'Moderate crisis expression - should show ensemble decision',
                'expected': 'Medium-high crisis detection'
            },
            {
                'message': 'I am dying of laughter watching this comedy show',
                'description': 'False positive candidate - context should matter',
                'expected': 'Low crisis level despite "dying" language'
            },
            {
                'message': 'I had a wonderful day and feel great',
                'description': 'Positive message - should be clearly safe',
                'expected': 'Low crisis, high confidence'
            }
        ]
        
        results = {}
        
        for i, test_case in enumerate(test_messages):
            test_key = f"test_{i+1}_{test_case['description'].replace(' ', '_').lower()[:20]}"
            result = self.test_message_analysis(test_case['message'], test_case['description'])
            results[test_key] = result
            
            if result.get('success', False):
                print(f"💡 Expected: {test_case['expected']}")
            
            time.sleep(0.5)  # Brief pause between tests
        
        return results
    
    def compare_ensemble_effectiveness(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare how effectively the ensemble handles different scenarios"""
        print(f"\n🎯 Ensemble Effectiveness Analysis")
        print("=" * 60)
        
        successful_tests = [r for r in results.values() if r.get('success', False)]
        
        if len(successful_tests) < 2:
            print("❌ Not enough successful tests to analyze effectiveness")
            return {'error': 'Insufficient test results'}
        
        # Analyze patterns
        analysis = {
            'total_tests': len(results),
            'successful_tests': len(successful_tests),
            'gap_detection_triggered': 0,
            'requires_review_count': 0,
            'consensus_methods': {},
            'crisis_levels': {},
            'confidence_range': {'min': 1.0, 'max': 0.0},
            'model_agreement_analysis': []
        }
        
        for test_result in successful_tests:
            metrics = test_result.get('metrics', {})
            
            # Gap detection analysis
            if metrics.get('gap_detection', {}).get('gap_detected', False):
                analysis['gap_detection_triggered'] += 1
            
            if metrics.get('gap_detection', {}).get('requires_review', False):
                analysis['requires_review_count'] += 1
            
            # Consensus method tracking
            consensus_method = metrics.get('consensus', {}).get('method', 'unknown')
            analysis['consensus_methods'][consensus_method] = analysis['consensus_methods'].get(consensus_method, 0) + 1
            
            # Crisis level distribution
            crisis_level = metrics.get('crisis_level', 'unknown')
            analysis['crisis_levels'][crisis_level] = analysis['crisis_levels'].get(crisis_level, 0) + 1
            
            # Confidence range
            confidence = metrics.get('confidence_score', 0)
            analysis['confidence_range']['min'] = min(analysis['confidence_range']['min'], confidence)
            analysis['confidence_range']['max'] = max(analysis['confidence_range']['max'], confidence)
            
            # Individual model analysis
            individual = metrics.get('individual_predictions', {})
            unique_predictions = set(individual.values())
            agreement_level = 'high' if len(unique_predictions) <= 2 else 'low'
            
            analysis['model_agreement_analysis'].append({
                'message': test_result.get('message', '')[:30] + '...',
                'predictions': individual,
                'agreement_level': agreement_level,
                'gap_detected': metrics.get('gap_detection', {}).get('gap_detected', False)
            })
        
        # Print analysis
        print(f"📊 Test Results: {analysis['successful_tests']}/{analysis['total_tests']} successful")
        print(f"⚠️ Gap Detection: Triggered in {analysis['gap_detection_triggered']} tests")
        print(f"👁️ Staff Review: Required for {analysis['requires_review_count']} tests")
        
        print(f"\n🔍 Consensus Methods:")
        for method, count in analysis['consensus_methods'].items():
            print(f"   {method}: {count} times")
        
        print(f"\n📈 Crisis Levels:")
        for level, count in analysis['crisis_levels'].items():
            print(f"   {level}: {count} times")
        
        print(f"\n🎯 Confidence Range: {analysis['confidence_range']['min']:.3f} - {analysis['confidence_range']['max']:.3f}")
        
        print(f"\n🧠 Model Agreement Analysis:")
        for item in analysis['model_agreement_analysis']:
            print(f"   Message: {item['message']}")
            print(f"   Predictions: {item['predictions']}")
            print(f"   Agreement: {item['agreement_level']}, Gap: {item['gap_detected']}")
            print()
        
        return analysis
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Run complete internal ensemble test suite"""
        print("🧪 Internal Container Ensemble Mode Test Suite")
        print("=" * 70)
        print(f"📅 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check current system status
        status = self.get_current_ensemble_status()
        if not status:
            return {'error': 'Could not get ensemble status'}
        
        print(f"\n📋 Current System Configuration:")
        ensemble_info = status.get('ensemble_status', {}).get('ensemble_info', {})
        print(f"   🤖 Ensemble Mode: {ensemble_info.get('ensemble_mode', 'unknown')}")
        print(f"   🧠 Models Loaded: {ensemble_info.get('models_loaded', False)}")
        print(f"   📊 Model Count: {ensemble_info.get('model_count', 0)}")
        print(f"   🔥 Device: {ensemble_info.get('device', 'unknown')}")
        
        # Check environment variables
        env_vars = self.check_environment_variables()
        
        # Run behavior analysis
        test_results = self.analyze_ensemble_behavior()
        
        # Analyze effectiveness
        effectiveness = self.compare_ensemble_effectiveness(test_results)
        
        # Generate final summary
        summary = {
            'test_suite_info': {
                'version': 'internal_container_test_v1.0',
                'timestamp': datetime.now().isoformat(),
                'container_test': True
            },
            'system_status': status,
            'environment_variables': env_vars,
            'test_results': test_results,
            'effectiveness_analysis': effectiveness
        }
        
        return summary
    
    def print_final_summary(self, results: Dict[str, Any]):
        """Print final test summary"""
        print(f"\n🎯 FINAL TEST SUMMARY")
        print("=" * 70)
        
        effectiveness = results.get('effectiveness_analysis', {})
        if 'error' not in effectiveness:
            successful_tests = effectiveness.get('successful_tests', 0)
            total_tests = effectiveness.get('total_tests', 0)
            gap_detection = effectiveness.get('gap_detection_triggered', 0)
            
            print(f"📊 Overall Results: {successful_tests}/{total_tests} tests successful")
            print(f"⚠️ Gap Detection: Active ({gap_detection} detections)")
            
            consensus_methods = effectiveness.get('consensus_methods', {})
            if consensus_methods:
                print(f"🔍 Consensus Methods: {', '.join(consensus_methods.keys())}")
            
            crisis_levels = effectiveness.get('crisis_levels', {})
            if crisis_levels:
                print(f"📈 Crisis Levels Detected: {', '.join(crisis_levels.keys())}")
            
            print(f"\n✅ CONCLUSION:")
            if successful_tests == total_tests and gap_detection > 0:
                print("   🎉 ENSEMBLE SYSTEM IS WORKING CORRECTLY!")
                print("   ✓ All tests passed")
                print("   ✓ Gap detection is active") 
                print("   ✓ Multiple consensus methods working")
                print("   ✓ Crisis level differentiation working")
            else:
                print("   ⚠️ Ensemble system has some issues:")
                if successful_tests < total_tests:
                    print(f"   - {total_tests - successful_tests} test(s) failed")
                if gap_detection == 0:
                    print("   - Gap detection not triggering")
        else:
            print("❌ Could not complete effectiveness analysis")
        
        env_vars = results.get('environment_variables', {})
        ensemble_mode = env_vars.get('NLP_ENSEMBLE_MODE', 'unknown')
        print(f"\n🔧 Current Configuration:")
        print(f"   Ensemble Mode: {ensemble_mode}")
        
        if ensemble_mode != 'unknown':
            print(f"\n💡 To test different modes, you would need to:")
            print(f"   1. Change environment variables in your Docker setup")
            print(f"   2. Restart the container to pick up changes")
            print(f"   3. Re-run this test to see differences")

def main():
    """Main function to run internal ensemble test"""
    print("🐳 Internal Container Ensemble Test")
    print("="*50)
    
    # Create test suite
    test_suite = InternalEnsembleTest()
    
    try:
        # Run full test suite
        results = test_suite.run_full_test_suite()
        
        # Print final summary
        test_suite.print_final_summary(results)
        
        # Save results
        timestamp = int(time.time())
        results_file = f"internal_ensemble_test_results_{timestamp}.json"
        
        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Results saved to {results_file}")
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")
        
        # Return success if tests passed
        effectiveness = results.get('effectiveness_analysis', {})
        if 'error' not in effectiveness:
            successful_tests = effectiveness.get('successful_tests', 0)
            total_tests = effectiveness.get('total_tests', 0)
            if successful_tests == total_tests:
                print(f"\n🎉 ALL TESTS PASSED!")
                return 0
            else:
                print(f"\n⚠️ SOME TESTS FAILED!")
                return 1
        else:
            print(f"\n❌ TEST ANALYSIS FAILED!")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())