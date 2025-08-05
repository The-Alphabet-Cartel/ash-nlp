#!/usr/bin/env python3
"""
Ensemble Configuration Validation Test
Tests the underlying configuration system for ensemble modes

This test validates that:
1. Configuration changes are properly loaded
2. Model weights are applied correctly in weighted mode
3. Consensus algorithms work as expected
4. Gap detection thresholds are respected

Usage:
    python tests/test_ensemble_configuration.py
"""

import os
import sys
import time
import json
import requests
from typing import Dict, Any, List
from pathlib import Path
import tempfile
import shutil

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30
ENV_FILE_PATH = ".env"

class EnsembleConfigurationTest:
    """Test suite for ensemble configuration validation"""
    
    def __init__(self):
        self.original_env_backup = None
        self.test_results = {}
    
    def backup_env_file(self) -> str:
        """Create a backup of the .env file"""
        if not os.path.exists(ENV_FILE_PATH):
            print(f"⚠️ No .env file found at {ENV_FILE_PATH}")
            return ""
        
        backup_path = f"{ENV_FILE_PATH}.test_backup_{int(time.time())}"
        shutil.copy2(ENV_FILE_PATH, backup_path)
        print(f"✅ Created backup: {backup_path}")
        return backup_path
    
    def restore_env_file(self, backup_path: str):
        """Restore the original .env file"""
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, ENV_FILE_PATH)
            os.remove(backup_path)
            print(f"✅ Restored original .env file")
    
    def modify_env_variables(self, variables: Dict[str, str]) -> bool:
        """Modify multiple environment variables"""
        try:
            env_content = []
            
            # Read current content
            if os.path.exists(ENV_FILE_PATH):
                with open(ENV_FILE_PATH, 'r') as f:
                    env_content = f.readlines()
            
            # Track which variables were found and modified
            variables_found = set()
            
            # Modify existing variables
            for i, line in enumerate(env_content):
                for var_name, var_value in variables.items():
                    if line.strip().startswith(f"{var_name}="):
                        env_content[i] = f"{var_name}={var_value}\n"
                        variables_found.add(var_name)
                        break
            
            # Add variables that weren't found
            for var_name, var_value in variables.items():
                if var_name not in variables_found:
                    env_content.append(f"{var_name}={var_value}\n")
            
            # Write back to file
            with open(ENV_FILE_PATH, 'w') as f:
                f.writelines(env_content)
            
            print(f"✅ Modified {len(variables)} environment variables")
            return True
            
        except Exception as e:
            print(f"❌ Failed to modify .env file: {e}")
            return False
    
    def wait_for_config_reload(self, max_attempts: int = 6) -> bool:
        """Wait for service to reload configuration"""
        print("⏳ Waiting for configuration reload...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get('status') == 'healthy':
                        print(f"✅ Service ready after {attempt + 1} attempts")
                        return True
            except Exception:
                pass
            
            if attempt < max_attempts - 1:
                time.sleep(2)
        
        print(f"⚠️ Service may not have reloaded configuration")
        return False
    
    def get_ensemble_configuration(self) -> Dict[str, Any]:
        """Get current ensemble configuration from service"""
        try:
            response = requests.get(f"{BASE_URL}/ensemble/config", timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Could not get ensemble config: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Failed to get ensemble config: {e}")
            return {}
    
    def analyze_with_config(self, message: str, config_name: str) -> Dict[str, Any]:
        """Analyze message and return detailed results"""
        try:
            payload = {
                "message": message,
                "user_id": f"test_user_{config_name}",
                "channel_id": f"test_channel_{config_name}"
            }
            
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'config_name': config_name,
                    'data': result,
                    'timestamp': time.time()
                }
            else:
                return {
                    'success': False,
                    'config_name': config_name,
                    'error': f"HTTP {response.status_code}",
                    'response_text': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'config_name': config_name,
                'error': str(e)
            }
    
    def test_weighted_mode_configuration(self) -> Dict[str, Any]:
        """Test weighted mode with different weight configurations"""
        print("\n🎯 Testing Weighted Mode Configuration")
        print("-" * 50)
        
        test_message = "I feel hopeless and don't want to continue"
        
        # Test configurations with different weights
        weight_configs = [
            {
                'name': 'depression_heavy',
                'description': 'Heavy depression model weighting',
                'variables': {
                    'NLP_ENSEMBLE_MODE': 'weighted',
                    'NLP_DEPRESSION_MODEL_WEIGHT': '0.7',
                    'NLP_SENTIMENT_MODEL_WEIGHT': '0.2',
                    'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': '0.1'
                }
            },
            {
                'name': 'balanced_weighting',
                'description': 'Balanced model weighting',
                'variables': {
                    'NLP_ENSEMBLE_MODE': 'weighted',
                    'NLP_DEPRESSION_MODEL_WEIGHT': '0.33',
                    'NLP_SENTIMENT_MODEL_WEIGHT': '0.33',
                    'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': '0.34'
                }
            },
            {
                'name': 'sentiment_heavy',
                'description': 'Heavy sentiment model weighting',
                'variables': {
                    'NLP_ENSEMBLE_MODE': 'weighted',
                    'NLP_DEPRESSION_MODEL_WEIGHT': '0.1',
                    'NLP_SENTIMENT_MODEL_WEIGHT': '0.8',
                    'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': '0.1'
                }
            }
        ]
        
        results = {}
        
        for config in weight_configs:
            print(f"\n📊 Testing: {config['description']}")
            
            # Apply configuration
            if not self.modify_env_variables(config['variables']):
                print(f"❌ Failed to apply {config['name']} configuration")
                continue
            
            # Wait for reload
            self.wait_for_config_reload()
            
            # Verify configuration was applied
            ensemble_config = self.get_ensemble_configuration()
            current_mode = ensemble_config.get('ensemble_mode', 'unknown')
            
            if current_mode != 'weighted':
                print(f"⚠️ Expected weighted mode, got {current_mode}")
            
            # Run analysis
            result = self.analyze_with_config(test_message, config['name'])
            results[config['name']] = result
            
            if result['success']:
                ensemble_analysis = result['data'].get('ensemble_analysis', {})
                consensus = ensemble_analysis.get('consensus', {})
                print(f"   Result: {consensus.get('prediction', 'unknown')} (confidence: {consensus.get('confidence', 0):.3f})")
            else:
                print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")
        
        return {
            'test_type': 'weighted_mode_configuration',
            'results': results,
            'configurations': weight_configs
        }
    
    def test_consensus_mode_thresholds(self) -> Dict[str, Any]:
        """Test consensus mode with different threshold configurations"""
        print("\n🎯 Testing Consensus Mode Thresholds")
        print("-" * 50)
        
        test_message = "I'm struggling but trying to cope"
        
        # Test configurations with different thresholds
        threshold_configs = [
            {
                'name': 'strict_consensus',
                'description': 'Strict consensus requirements',
                'variables': {
                    'NLP_ENSEMBLE_MODE': 'consensus',
                    'NLP_GAP_DETECTION_THRESHOLD': '0.15',
                    'NLP_DISAGREEMENT_THRESHOLD': '0.25'
                }
            },
            {
                'name': 'moderate_consensus',
                'description': 'Moderate consensus requirements',
                'variables': {
                    'NLP_ENSEMBLE_MODE': 'consensus',
                    'NLP_GAP_DETECTION_THRESHOLD': '0.25',
                    'NLP_DISAGREEMENT_THRESHOLD': '0.35'
                }
            },
            {
                'name': 'lenient_consensus',
                'description': 'Lenient consensus requirements',
                'variables': {
                    'NLP_ENSEMBLE_MODE': 'consensus',
                    'NLP_GAP_DETECTION_THRESHOLD': '0.4',
                    'NLP_DISAGREEMENT_THRESHOLD': '0.5'
                }
            }
        ]
        
        results = {}
        
        for config in threshold_configs:
            print(f"\n📊 Testing: {config['description']}")
            
            # Apply configuration
            if not self.modify_env_variables(config['variables']):
                print(f"❌ Failed to apply {config['name']} configuration")
                continue
            
            # Wait for reload
            self.wait_for_config_reload()
            
            # Run analysis
            result = self.analyze_with_config(test_message, config['name'])
            results[config['name']] = result
            
            if result['success']:
                ensemble_analysis = result['data'].get('ensemble_analysis', {})
                consensus = ensemble_analysis.get('consensus', {})
                gap_detection = ensemble_analysis.get('gap_detection', {})
                
                print(f"   Result: {consensus.get('prediction', 'unknown')} (confidence: {consensus.get('confidence', 0):.3f})")
                print(f"   Gap detected: {gap_detection.get('gap_detected', False)}")
                print(f"   Requires review: {gap_detection.get('requires_review', False)}")
            else:
                print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")
        
        return {
            'test_type': 'consensus_mode_thresholds',
            'results': results,
            'configurations': threshold_configs
        }
    
    def test_majority_mode_behavior(self) -> Dict[str, Any]:
        """Test majority mode behavior"""
        print("\n🎯 Testing Majority Mode Behavior")
        print("-" * 50)
        
        # Test with different types of messages
        test_messages = [
            {
                'message': "I want to end my life",
                'description': 'Clear crisis language'
            },
            {
                'message': "This project is killing me softly",
                'description': 'Ambiguous crisis language'
            },
            {
                'message': "I am feeling great today!",
                'description': 'Positive sentiment'
            }
        ]
        
        # Set majority mode
        config_variables = {
            'NLP_ENSEMBLE_MODE': 'majority',
            'NLP_GAP_DETECTION_THRESHOLD': '0.25',
            'NLP_DISAGREEMENT_THRESHOLD': '0.35'
        }
        
        if not self.modify_env_variables(config_variables):
            print("❌ Failed to set majority mode")
            return {'error': 'Configuration failed'}
        
        self.wait_for_config_reload()
        
        results = {}
        
        for i, test_case in enumerate(test_messages):
            print(f"\n📝 Testing: {test_case['description']}")
            print(f"   Message: '{test_case['message']}'")
            
            result = self.analyze_with_config(test_case['message'], f"majority_test_{i}")
            results[f"test_{i}"] = result
            
            if result['success']:
                ensemble_analysis = result['data'].get('ensemble_analysis', {})
                consensus = ensemble_analysis.get('consensus', {})
                individual_results = ensemble_analysis.get('individual_results', {})
                
                print(f"   Consensus: {consensus.get('prediction', 'unknown')} (confidence: {consensus.get('confidence', 0):.3f})")
                print(f"   Method: {consensus.get('method', 'unknown')}")
                
                # Show individual model results
                for model_name, model_results in individual_results.items():
                    if model_results and len(model_results) > 0:
                        top_result = model_results[0]
                        print(f"   {model_name}: {top_result.get('label', 'unknown')} ({top_result.get('score', 0):.3f})")
            else:
                print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")
        
        return {
            'test_type': 'majority_mode_behavior',
            'results': results,
            'test_messages': test_messages
        }
    
    def analyze_configuration_differences(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze differences across configuration tests"""
        print("\n📊 CONFIGURATION ANALYSIS")
        print("=" * 60)
        
        total_tests = sum(len(test['results']) for test in test_results)
        successful_tests = sum(
            sum(1 for result in test['results'].values() if result.get('success', False))
            for test in test_results
        )
        
        print(f"Total configuration tests: {total_tests}")
        print(f"Successful tests: {successful_tests}")
        
        # Look for meaningful differences
        differences_found = []
        
        for test_group in test_results:
            test_type = test_group.get('test_type', 'unknown')
            results = test_group.get('results', {})
            
            successful_results = {k: v for k, v in results.items() if v.get('success', False)}
            
            if len(successful_results) >= 2:
                # Compare results within this test group
                result_list = list(successful_results.values())
                
                for i in range(len(result_list)):
                    for j in range(i + 1, len(result_list)):
                        result1 = result_list[i]
                        result2 = result_list[j]
                        
                        # Extract key metrics for comparison
                        consensus1 = result1['data'].get('ensemble_analysis', {}).get('consensus', {})
                        consensus2 = result2['data'].get('ensemble_analysis', {}).get('consensus', {})
                        
                        pred1 = consensus1.get('prediction', 'unknown')
                        pred2 = consensus2.get('prediction', 'unknown')
                        conf1 = consensus1.get('confidence', 0)
                        conf2 = consensus2.get('confidence', 0)
                        
                        if pred1 != pred2 or abs(conf1 - conf2) > 0.05:
                            differences_found.append({
                                'test_type': test_type,
                                'config1': result1['config_name'],
                                'config2': result2['config_name'],
                                'prediction_diff': pred1 != pred2,
                                'confidence_diff': abs(conf1 - conf2)
                            })
        
        print(f"\nMeaningful differences found: {len(differences_found)}")
        
        for diff in differences_found:
            print(f"  • {diff['test_type']}: {diff['config1']} vs {diff['config2']}")
            if diff['prediction_diff']:
                print(f"    - Different predictions")
            if diff['confidence_diff'] > 0.05:
                print(f"    - Confidence difference: {diff['confidence_diff']:.3f}")
        
        configuration_working = len(differences_found) > 0
        
        print(f"\n🎯 CONCLUSION:")
        if configuration_working:
            print("✅ ENSEMBLE CONFIGURATION IS WORKING!")
            print("   Different configurations produce different results as expected.")
        else:
            print("❌ ENSEMBLE CONFIGURATION MAY NOT BE WORKING!")
            print("   All configurations produce identical results.")
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'differences_found': differences_found,
            'configuration_working': configuration_working
        }
    
    def run_full_configuration_test(self) -> Dict[str, Any]:
        """Run complete configuration test suite"""
        print("🚀 Ensemble Configuration Validation Test Suite")
        print("=" * 70)
        
        # Backup environment
        backup_path = self.backup_env_file()
        
        try:
            # Run all configuration tests
            test_results = []
            
            # Test 1: Weighted mode configurations
            weighted_results = self.test_weighted_mode_configuration()
            test_results.append(weighted_results)
            
            # Test 2: Consensus mode thresholds
            consensus_results = self.test_consensus_mode_thresholds()
            test_results.append(consensus_results)
            
            # Test 3: Majority mode behavior
            majority_results = self.test_majority_mode_behavior()
            test_results.append(majority_results)
            
            # Analyze overall results
            analysis = self.analyze_configuration_differences(test_results)
            
            return {
                'test_suite': 'ensemble_configuration_validation',
                'timestamp': time.time(),
                'test_results': test_results,
                'analysis': analysis
            }
            
        finally:
            # Restore original environment
            if backup_path:
                self.restore_env_file(backup_path)
                print("\n🔄 Attempting to reload original configuration...")
                self.wait_for_config_reload()

def main():
    """Main function"""
    print("🧪 Ensemble Configuration Validation Test")
    print("=" * 50)
    
    # Check service health
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
    
    # Run configuration tests
    test_suite = EnsembleConfigurationTest()
    results = test_suite.run_full_configuration_test()
    
    # Save results
    timestamp = int(time.time())
    results_file = f"ensemble_config_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to {results_file}")
    
    # Return appropriate exit code
    analysis = results.get('analysis', {})
    if analysis.get('configuration_working', False):
        print("\n✅ CONFIGURATION TEST PASSED!")
        return 0
    else:
        print("\n❌ CONFIGURATION TEST FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())