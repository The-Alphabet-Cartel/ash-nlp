#!/usr/bin/env python3
"""
Docker-Compatible Ensemble Mode Testing
Tests ensemble mode switching by restarting Docker container with different environment variables

This test works with Docker by:
1. Modifying docker-compose environment or .env file
2. Restarting the Docker container to pick up new environment variables
3. Testing the ensemble modes

Usage:
    python tests/test_ensemble_mode_docker.py [--container-name ash-nlp]
"""

import os
import sys
import time
import json
import requests
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 60  # Longer timeout for Docker restarts
DEFAULT_CONTAINER_NAME = "ash-nlp"

class DockerEnsembleTest:
    """Docker-compatible ensemble mode testing"""
    
    def __init__(self, container_name: str = DEFAULT_CONTAINER_NAME):
        self.container_name = container_name
        self.original_env_backup = None
        self.test_results = {}
        
    def check_docker_setup(self) -> bool:
        """Check if Docker and docker-compose are available"""
        try:
            # Check if docker-compose is available
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ docker-compose not found")
                return False
            
            # Check if the container exists in docker-compose.yml
            result = subprocess.run(['docker-compose', 'config'], 
                                  capture_output=True, text=True)
            if self.container_name not in result.stdout:
                print(f"⚠️ Container '{self.container_name}' not found in docker-compose.yml")
                print("Available services:")
                # Show available services
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip().endswith(':') and not line.startswith(' '):
                        service_name = line.strip().rstrip(':')
                        if service_name not in ['version', 'services', 'volumes', 'networks']:
                            print(f"  - {service_name}")
                return False
            
            print("✅ Docker setup verified")
            return True
            
        except FileNotFoundError:
            print("❌ Docker or docker-compose not found")
            return False
        except Exception as e:
            print(f"❌ Error checking Docker setup: {e}")
            return False
    
    def backup_env_file(self) -> str:
        """Create backup of .env file"""
        env_file = ".env"
        if not os.path.exists(env_file):
            print("⚠️ No .env file found")
            return ""
        
        backup_path = f".env.backup_docker_test_{int(time.time())}"
        subprocess.run(['cp', env_file, backup_path])
        print(f"✅ Created backup: {backup_path}")
        return backup_path
    
    def restore_env_file(self, backup_path: str):
        """Restore original .env file"""
        if backup_path and os.path.exists(backup_path):
            subprocess.run(['cp', backup_path, '.env'])
            os.remove(backup_path)
            print("✅ Restored original .env file")
    
    def modify_env_for_mode(self, ensemble_mode: str, 
                           extra_vars: Dict[str, str] = None) -> bool:
        """Modify .env file for specific ensemble mode"""
        try:
            env_vars = {
                'NLP_ENSEMBLE_MODE': ensemble_mode
            }
            
            # Add mode-specific variables
            if ensemble_mode == 'weighted':
                env_vars.update({
                    'NLP_DEPRESSION_MODEL_WEIGHT': '0.6',
                    'NLP_SENTIMENT_MODEL_WEIGHT': '0.2',
                    'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': '0.2'
                })
            elif ensemble_mode == 'consensus':
                env_vars.update({
                    'NLP_GAP_DETECTION_THRESHOLD': '0.2',
                    'NLP_DISAGREEMENT_THRESHOLD': '0.3'
                })
            elif ensemble_mode == 'majority':
                env_vars.update({
                    'NLP_GAP_DETECTION_THRESHOLD': '0.25',
                    'NLP_DISAGREEMENT_THRESHOLD': '0.35'
                })
            
            # Add any extra variables
            if extra_vars:
                env_vars.update(extra_vars)
            
            # Read current .env content
            env_content = []
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    env_content = f.readlines()
            
            # Update or add variables
            updated_vars = set()
            for i, line in enumerate(env_content):
                for var_name, var_value in env_vars.items():
                    if line.strip().startswith(f"{var_name}="):
                        env_content[i] = f"{var_name}={var_value}\n"
                        updated_vars.add(var_name)
                        break
            
            # Add variables that weren't found
            for var_name, var_value in env_vars.items():
                if var_name not in updated_vars:
                    env_content.append(f"{var_name}={var_value}\n")
            
            # Write back to file
            with open('.env', 'w') as f:
                f.writelines(env_content)
            
            print(f"✅ Updated .env for {ensemble_mode} mode")
            return True
            
        except Exception as e:
            print(f"❌ Failed to modify .env: {e}")
            return False
    
    def restart_container(self) -> bool:
        """Restart the Docker container to pick up new environment variables"""
        print(f"🔄 Restarting container '{self.container_name}'...")
        
        try:
            # Stop the container
            print("  📥 Stopping container...")
            stop_result = subprocess.run(
                ['docker-compose', 'stop', self.container_name],
                capture_output=True, text=True, timeout=30
            )
            
            if stop_result.returncode != 0:
                print(f"⚠️ Stop command had issues: {stop_result.stderr}")
            
            # Start the container
            print("  🚀 Starting container...")
            start_result = subprocess.run(
                ['docker-compose', 'up', '-d', self.container_name],
                capture_output=True, text=True, timeout=60
            )
            
            if start_result.returncode != 0:
                print(f"❌ Failed to start container: {start_result.stderr}")
                return False
            
            print("✅ Container restarted successfully")
            return True
            
        except subprocess.TimeoutExpired:
            print("⏰ Container restart timed out")
            return False
        except Exception as e:
            print(f"❌ Error restarting container: {e}")
            return False
    
    def wait_for_service_ready(self, max_attempts: int = 20) -> bool:
        """Wait for service to be ready after restart"""
        print("⏳ Waiting for service to be ready...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get('status') == 'healthy':
                        # Check if models are loaded
                        models_loaded = health_data.get('models_loaded', False)
                        if models_loaded:
                            print(f"✅ Service ready after {attempt + 1} attempts")
                            return True
                        else:
                            print(f"⏳ Models still loading... (attempt {attempt + 1})")
                    else:
                        print(f"⏳ Service not healthy yet... (attempt {attempt + 1})")
                else:
                    print(f"⏳ Service not responding properly... (attempt {attempt + 1})")
            except Exception:
                print(f"⏳ Service not reachable yet... (attempt {attempt + 1})")
            
            if attempt < max_attempts - 1:
                time.sleep(10)  # Longer wait for Docker
        
        print(f"❌ Service not ready after {max_attempts} attempts")
        return False
    
    def get_current_ensemble_status(self) -> Dict[str, Any]:
        """Get current ensemble status"""
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
    
    def test_ensemble_mode(self, mode: str, test_message: str) -> Dict[str, Any]:
        """Test a specific ensemble mode"""
        print(f"\n🎯 Testing {mode.upper()} mode")
        print("=" * 50)
        
        # Update environment variables
        if not self.modify_env_for_mode(mode):
            return {'success': False, 'error': 'Failed to modify environment'}
        
        # Restart container
        if not self.restart_container():
            return {'success': False, 'error': 'Failed to restart container'}
        
        # Wait for service to be ready
        if not self.wait_for_service_ready():
            return {'success': False, 'error': 'Service not ready after restart'}
        
        # Verify the mode was applied
        status = self.get_current_ensemble_status()
        current_mode = status.get('ensemble_info', {}).get('ensemble_mode', 'unknown')
        
        print(f"📊 Current ensemble mode: {current_mode}")
        
        if current_mode.lower() != mode.lower():
            print(f"⚠️ Warning: Expected {mode}, service reports {current_mode}")
        
        # Test the analysis
        print(f"📝 Testing message: '{test_message}'")
        
        try:
            payload = {
                "message": test_message,
                "user_id": f"test_user_{mode}",
                "channel_id": f"test_channel_{mode}"
            }
            
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Extract key metrics
                ensemble_analysis = result_data.get('ensemble_analysis', {})
                consensus = ensemble_analysis.get('consensus', {})
                gap_detection = ensemble_analysis.get('gap_detection', {})
                individual_results = ensemble_analysis.get('individual_results', {})
                
                metrics = {
                    'prediction': consensus.get('prediction', 'unknown'),
                    'confidence': round(consensus.get('confidence', 0), 4),
                    'method': consensus.get('method', 'unknown'),
                    'gap_detected': gap_detection.get('gap_detected', False),
                    'requires_review': gap_detection.get('requires_review', False),
                    'models_used': len([k for k, v in individual_results.items() if v])
                }
                
                print(f"📊 Result: {metrics['prediction']} (confidence: {metrics['confidence']})")
                print(f"🔍 Method: {metrics['method']}")
                print(f"⚠️ Gap detected: {metrics['gap_detected']}")
                print(f"👁️ Requires review: {metrics['requires_review']}")
                print(f"🧠 Models used: {metrics['models_used']}")
                
                return {
                    'success': True,
                    'mode': mode,
                    'current_mode_reported': current_mode,
                    'metrics': metrics,
                    'raw_data': result_data,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ Analysis failed: {error_msg}")
                return {'success': False, 'mode': mode, 'error': error_msg}
                
        except Exception as e:
            error_msg = f"Analysis exception: {e}"
            print(f"❌ {error_msg}")
            return {'success': False, 'mode': mode, 'error': error_msg}
    
    def compare_mode_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compare results across different modes"""
        print(f"\n📊 ENSEMBLE MODE COMPARISON")
        print("=" * 60)
        
        successful_results = {mode: data for mode, data in results.items() 
                            if data.get('success', False)}
        
        if len(successful_results) < 2:
            print("❌ Not enough successful results to compare")
            return {'error': 'Insufficient results'}
        
        # Compare all pairs
        modes = list(successful_results.keys())
        differences_found = 0
        
        for i, mode1 in enumerate(modes):
            for mode2 in modes[i+1:]:
                print(f"\n🔄 Comparing {mode1.upper()} vs {mode2.upper()}:")
                
                metrics1 = successful_results[mode1]['metrics']
                metrics2 = successful_results[mode2]['metrics']
                
                # Check for differences
                pred_diff = metrics1['prediction'] != metrics2['prediction']
                conf_diff = abs(metrics1['confidence'] - metrics2['confidence'])
                method_diff = metrics1['method'] != metrics2['method']
                gap_diff = metrics1['gap_detected'] != metrics2['gap_detected']
                
                print(f"   Prediction: {metrics1['prediction']} vs {metrics2['prediction']} {'(DIFFERENT)' if pred_diff else '(SAME)'}")
                print(f"   Confidence: {metrics1['confidence']} vs {metrics2['confidence']} (diff: {conf_diff:.4f})")
                print(f"   Method: {metrics1['method']} vs {metrics2['method']} {'(DIFFERENT)' if method_diff else '(SAME)'}")
                print(f"   Gap Detection: {metrics1['gap_detected']} vs {metrics2['gap_detected']} {'(DIFFERENT)' if gap_diff else '(SAME)'}")
                
                # Count significant differences
                if pred_diff or conf_diff > 0.05 or method_diff or gap_diff:
                    differences_found += 1
        
        print(f"\n🎯 COMPARISON SUMMARY:")
        print(f"   Total comparisons: {len(modes) * (len(modes) - 1) // 2}")
        print(f"   Comparisons with differences: {differences_found}")
        
        modes_working = differences_found > 0
        
        if modes_working:
            print("   ✅ ENSEMBLE MODES ARE WORKING!")
            print("   Different modes produce different results as expected.")
        else:
            print("   ❌ ENSEMBLE MODES MAY NOT BE WORKING!")
            print("   All modes produce identical results.")
        
        return {
            'modes_tested': len(successful_results),
            'comparisons_made': len(modes) * (len(modes) - 1) // 2,
            'differences_found': differences_found,
            'modes_working': modes_working
        }
    
    def run_full_test(self, test_message: str = None) -> Dict[str, Any]:
        """Run the complete Docker ensemble mode test"""
        if test_message is None:
            test_message = "This exam is killing me but I think I can handle it"
        
        print("🚀 Docker Ensemble Mode Test Suite")
        print("=" * 60)
        print(f"📝 Test message: '{test_message}'")
        
        # Check Docker setup
        if not self.check_docker_setup():
            return {'error': 'Docker setup check failed'}
        
        # Backup environment
        backup_path = self.backup_env_file()
        
        try:
            modes_to_test = ['consensus', 'majority', 'weighted']
            results = {}
            
            # Test each mode
            for mode in modes_to_test:
                result = self.test_ensemble_mode(mode, test_message)
                results[mode] = result
                
                # Brief pause between tests
                time.sleep(2)
            
            # Compare results
            comparison = self.compare_mode_results(results)
            
            # Generate summary
            successful_tests = sum(1 for r in results.values() if r.get('success', False))
            
            summary = {
                'test_suite': 'docker_ensemble_mode_test',
                'test_message': test_message,
                'total_modes_tested': len(modes_to_test),
                'successful_tests': successful_tests,
                'failed_tests': len(modes_to_test) - successful_tests,
                'results': results,
                'comparison': comparison,
                'overall_success': comparison.get('modes_working', False) if successful_tests >= 2 else False,
                'timestamp': datetime.now().isoformat()
            }
            
            return summary
            
        finally:
            # Restore original environment
            if backup_path:
                self.restore_env_file(backup_path)
                print("\n🔄 Restoring original configuration...")
                self.restart_container()
                self.wait_for_service_ready()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Docker-compatible ensemble mode test')
    parser.add_argument('--container-name', default=DEFAULT_CONTAINER_NAME,
                       help=f'Docker container name (default: {DEFAULT_CONTAINER_NAME})')
    parser.add_argument('--message', 
                       default="This exam is killing me but I think I can handle it",
                       help='Test message to analyze')
    parser.add_argument('--save', action='store_true',
                       help='Save results to JSON file')
    
    args = parser.parse_args()
    
    print("🐳 Docker Ensemble Mode Test Suite")
    print("=" * 50)
    
    # Create test instance
    test_suite = DockerEnsembleTest(container_name=args.container_name)
    
    # Run the test
    results = test_suite.run_full_test(test_message=args.message)
    
    if 'error' in results:
        print(f"\n❌ Test suite failed: {results['error']}")
        return 1
    
    # Save results if requested
    if args.save:
        timestamp = int(time.time())
        filename = f"docker_ensemble_test_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to {filename}")
    
    # Print final result
    print(f"\n🎯 FINAL RESULT:")
    if results.get('overall_success', False):
        print("✅ DOCKER ENSEMBLE MODE TEST PASSED!")
        print("   Ensemble modes are working correctly with Docker configuration.")
        return 0
    else:
        print("❌ DOCKER ENSEMBLE MODE TEST FAILED!")
        print("   Ensemble modes may not be working properly.")
        
        # Show some debugging info
        comparison = results.get('comparison', {})
        if comparison.get('modes_tested', 0) < 2:
            print("   Issue: Not enough modes tested successfully")
        elif comparison.get('differences_found', 0) == 0:
            print("   Issue: All modes produce identical results")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())