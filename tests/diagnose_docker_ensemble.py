#!/usr/bin/env python3
"""
Docker Ensemble Configuration Diagnostic Tool
Diagnoses issues with ensemble mode configuration in Docker environment

Usage:
    python tests/diagnose_docker_ensemble.py [--container-name ash-nlp]
"""

import os
import sys
import json
import requests
import subprocess
from typing import Dict, Any

BASE_URL = "http://localhost:8881"
DEFAULT_CONTAINER_NAME = "ash-nlp"

class DockerEnsembleDiagnostic:
    """Diagnostic tool for Docker ensemble configuration"""
    
    def __init__(self, container_name: str = DEFAULT_CONTAINER_NAME):
        self.container_name = container_name
    
    def check_service_health(self) -> Dict[str, Any]:
        """Check basic service health"""
        print("🔍 Checking Service Health...")
        print("-" * 40)
        
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Service is healthy")
                print(f"📊 Status: {health_data.get('status', 'unknown')}")
                print(f"🧠 Models loaded: {health_data.get('models_loaded', False)}")
                
                # Check components
                components = health_data.get('components_available', {})
                for component, available in components.items():
                    status = "✅" if available else "❌"
                    print(f"{status} {component}: {available}")
                
                return {'success': True, 'data': health_data}
            else:
                print(f"❌ Service unhealthy: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to service at {BASE_URL}")
            return {'success': False, 'error': 'Connection refused'}
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_ensemble_status(self) -> Dict[str, Any]:
        """Check ensemble configuration status"""
        print(f"\n🎯 Checking Ensemble Status...")
        print("-" * 40)
        
        try:
            response = requests.get(f"{BASE_URL}/ensemble/status", timeout=10)
            
            if response.status_code == 200:
                status_data = response.json()
                
                # Check ensemble info
                ensemble_info = status_data.get('ensemble_info', {})
                print(f"🔧 Ensemble mode: {ensemble_info.get('ensemble_mode', 'unknown')}")
                print(f"🔍 Gap detection: {ensemble_info.get('gap_detection_enabled', False)}")
                
                # Check model info
                models = status_data.get('models', {})
                for model_type, model_info in models.items():
                    if isinstance(model_info, dict):
                        name = model_info.get('name', 'unknown')
                        loaded = model_info.get('loaded', False)
                        status = "✅" if loaded else "❌"
                        print(f"{status} {model_type}: {name}")
                
                return {'success': True, 'data': status_data}
            else:
                print(f"❌ Ensemble status unavailable: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"❌ Ensemble status check failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_docker_environment(self) -> Dict[str, Any]:
        """Check Docker container environment variables"""
        print(f"\n🐳 Checking Docker Environment...")
        print("-" * 40)
        
        try:
            # Get environment variables from inside the container
            result = subprocess.run(
                ['docker', 'exec', self.container_name, 'env'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode != 0:
                print(f"❌ Failed to get container environment: {result.stderr}")
                return {'success': False, 'error': result.stderr}
            
            # Parse environment variables
            env_vars = {}
            nlp_vars = {}
            
            for line in result.stdout.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
                    if key.startswith('NLP_'):
                        nlp_vars[key] = value
            
            print(f"📊 Total environment variables: {len(env_vars)}")
            print(f"🎯 NLP-related variables: {len(nlp_vars)}")
            
            # Check key ensemble variables
            key_vars = [
                'NLP_ENSEMBLE_MODE',
                'NLP_DEPRESSION_MODEL',
                'NLP_SENTIMENT_MODEL', 
                'NLP_EMOTIONAL_DISTRESS_MODEL',
                'NLP_DEPRESSION_MODEL_WEIGHT',
                'NLP_SENTIMENT_MODEL_WEIGHT',
                'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT'
            ]
            
            print(f"\n🔑 Key Ensemble Variables:")
            for var in key_vars:
                value = nlp_vars.get(var, 'NOT SET')
                status = "✅" if var in nlp_vars else "❌"
                print(f"{status} {var}={value}")
            
            return {'success': True, 'nlp_vars': nlp_vars, 'total_vars': len(env_vars)}
            
        except subprocess.TimeoutExpired:
            print("⏰ Docker command timed out")
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            print(f"❌ Docker environment check failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_env_file(self) -> Dict[str, Any]:
        """Check local .env file"""
        print(f"\n📄 Checking Local .env File...")
        print("-" * 40)
        
        env_file = ".env"
        
        if not os.path.exists(env_file):
            print(f"❌ No .env file found")
            return {'success': False, 'error': 'File not found'}
        
        try:
            nlp_vars = {}
            total_lines = 0
            
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        total_lines += 1
                        key, value = line.split('=', 1)
                        if key.startswith('NLP_'):
                            nlp_vars[key] = value
            
            print(f"📊 Total variables in .env: {total_lines}")
            print(f"🎯 NLP variables in .env: {len(nlp_vars)}")
            
            # Check key variables
            key_vars = ['NLP_ENSEMBLE_MODE', 'NLP_DEPRESSION_MODEL', 'NLP_SENTIMENT_MODEL']
            
            print(f"\n🔑 Key Variables in .env:")
            for var in key_vars:
                value = nlp_vars.get(var, 'NOT SET')
                status = "✅" if var in nlp_vars else "❌"
                print(f"{status} {var}={value}")
            
            return {'success': True, 'nlp_vars': nlp_vars, 'total_vars': total_lines}
            
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
            return {'success': False, 'error': str(e)}
    
    def check_docker_compose_config(self) -> Dict[str, Any]:
        """Check docker-compose configuration"""
        print(f"\n📋 Checking Docker Compose Configuration...")
        print("-" * 40)
        
        try:
            # Get docker-compose config
            result = subprocess.run(
                ['docker-compose', 'config'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode != 0:
                print(f"❌ Docker compose config error: {result.stderr}")
                return {'success': False, 'error': result.stderr}
            
            config_text = result.stdout
            
            # Check if service exists
            if self.container_name in config_text:
                print(f"✅ Service '{self.container_name}' found in docker-compose.yml")
            else:
                print(f"❌ Service '{self.container_name}' not found in docker-compose.yml")
            
            # Check for env_file configuration
            if 'env_file' in config_text:
                print("✅ env_file configuration found")
            else:
                print("⚠️ No env_file configuration found")
            
            # Check for environment variables
            if 'environment:' in config_text:
                print("✅ Environment variables configured")
            else:
                print("⚠️ No environment variables in docker-compose")
            
            return {'success': True, 'config': config_text}
            
        except Exception as e:
            print(f"❌ Docker compose check failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simple_analysis(self) -> Dict[str, Any]:
        """Test a simple analysis to see current behavior"""
        print(f"\n🧪 Testing Simple Analysis...")
        print("-" * 40)
        
        test_message = "I am feeling down today"
        
        try:
            payload = {
                "message": test_message,
                "user_id": "diagnostic_test",
                "channel_id": "diagnostic_channel"
            }
            
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract key info
                ensemble_analysis = result.get('ensemble_analysis', {})
                consensus = ensemble_analysis.get('consensus', {})
                individual_results = ensemble_analysis.get('individual_results', {})
                
                print(f"📝 Test message: '{test_message}'")
                print(f"📊 Prediction: {consensus.get('prediction', 'unknown')}")
                print(f"🎯 Confidence: {consensus.get('confidence', 0):.4f}")
                print(f"🔍 Method: {consensus.get('method', 'unknown')}")
                
                # Check individual models
                models_working = 0
                for model_name, model_results in individual_results.items():
                    if model_results and len(model_results) > 0:
                        models_working += 1
                        top_result = model_results[0]
                        print(f"🧠 {model_name}: {top_result.get('label', 'unknown')} ({top_result.get('score', 0):.3f})")
                
                print(f"📈 Models working: {models_working}/3")
                
                return {
                    'success': True, 
                    'models_working': models_working,
                    'prediction': consensus.get('prediction', 'unknown'),
                    'method': consensus.get('method', 'unknown')
                }
                
            else:
                print(f"❌ Analysis failed: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"❌ Analysis test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_recommendations(self, results: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on diagnostic results"""
        recommendations = []
        
        # Check service health
        health = results.get('health', {})
        if not health.get('success', False):
            recommendations.append("🚨 CRITICAL: Fix service connectivity issues first")
            recommendations.append("   Check if container is running: docker ps | grep ash-nlp")
            return recommendations
        
        # Check ensemble status
        ensemble = results.get('ensemble', {})
        if ensemble.get('success', False):
            ensemble_data = ensemble.get('data', {})
            ensemble_info = ensemble_data.get('ensemble_info', {})
            current_mode = ensemble_info.get('ensemble_mode', 'unknown')
            
            if current_mode == 'unknown':
                recommendations.append("❌ ISSUE: Ensemble mode is 'unknown'")
                recommendations.append("   This suggests environment variables are not being loaded properly")
        
        # Check Docker environment vs .env file
        docker_env = results.get('docker_env', {})
        env_file = results.get('env_file', {})
        
        if docker_env.get('success', False) and env_file.get('success', False):
            docker_nlp_vars = docker_env.get('nlp_vars', {})
            env_file_nlp_vars = env_file.get('nlp_vars', {})
            
            # Compare key variables
            ensemble_mode_docker = docker_nlp_vars.get('NLP_ENSEMBLE_MODE', 'NOT SET')
            ensemble_mode_env = env_file_nlp_vars.get('NLP_ENSEMBLE_MODE', 'NOT SET')
            
            if ensemble_mode_docker != ensemble_mode_env:
                recommendations.append("🔧 ISSUE: Docker environment doesn't match .env file")
                recommendations.append(f"   Docker: NLP_ENSEMBLE_MODE={ensemble_mode_docker}")
                recommendations.append(f"   .env file: NLP_ENSEMBLE_MODE={ensemble_mode_env}")
                recommendations.append("   Solution: Restart container with: docker-compose restart ash-nlp")
        
        # Check analysis test
        analysis = results.get('analysis', {})
        if analysis.get('success', False):
            models_working = analysis.get('models_working', 0)
            if models_working < 3:
                recommendations.append(f"⚠️ WARNING: Only {models_working}/3 models working")
                recommendations.append("   Check model loading in container logs: docker logs ash-nlp")
            
            method = analysis.get('method', 'unknown')
            if method == 'unknown':
                recommendations.append("❌ ISSUE: Ensemble method is 'unknown'")
                recommendations.append("   This indicates ensemble configuration is not working")
        
        # General recommendations
        if not recommendations:
            predictions = [analysis.get('prediction', 'unknown') for analysis in [results.get('analysis', {})]]
            if 'unknown' in predictions:
                recommendations.append("⚠️ System appears to be working but ensemble may not be optimal")
                recommendations.append("   Try the Docker-compatible test: python tests/test_ensemble_mode_docker.py")
        
        return recommendations
    
    def run_full_diagnostic(self) -> Dict[str, Any]:
        """Run complete diagnostic suite"""
        print("🔍 Docker Ensemble Configuration Diagnostic")
        print("=" * 60)
        
        results = {}
        
        # Run all checks
        results['health'] = self.check_service_health()
        results['ensemble'] = self.check_ensemble_status()
        results['docker_env'] = self.check_docker_environment()
        results['env_file'] = self.check_env_file()
        results['docker_compose'] = self.check_docker_compose_config()
        results['analysis'] = self.test_simple_analysis()
        
        # Generate recommendations
        recommendations = self.generate_recommendations(results)
        
        # Print summary
        print(f"\n🎯 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        successful_checks = sum(1 for r in results.values() if r.get('success', False))
        total_checks = len(results)
        
        print(f"📊 Checks passed: {successful_checks}/{total_checks}")
        
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"   {rec}")
        else:
            print(f"\n✅ No critical issues found!")
            print("   System appears to be configured correctly.")
        
        return {
            'diagnostic_results': results,
            'recommendations': recommendations,
            'checks_passed': successful_checks,
            'total_checks': total_checks
        }

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Diagnose Docker ensemble configuration')
    parser.add_argument('--container-name', default=DEFAULT_CONTAINER_NAME,
                       help=f'Docker container name (default: {DEFAULT_CONTAINER_NAME})')
    parser.add_argument('--save', action='store_true',
                       help='Save diagnostic results to JSON file')
    
    args = parser.parse_args()
    
    # Run diagnostic
    diagnostic = DockerEnsembleDiagnostic(container_name=args.container_name)
    results = diagnostic.run_full_diagnostic()
    
    # Save results if requested
    if args.save:
        import time
        timestamp = int(time.time())
        filename = f"docker_ensemble_diagnostic_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Diagnostic results saved to {filename}")
    
    # Exit with appropriate code
    recommendations = results.get('recommendations', [])
    critical_issues = sum(1 for rec in recommendations if rec.startswith('🚨'))
    
    if critical_issues > 0:
        print(f"\n❌ CRITICAL ISSUES FOUND - Fix these first!")
        return 1
    elif recommendations:
        print(f"\n⚠️ ISSUES FOUND - See recommendations above")
        return 1
    else:
        print(f"\n✅ DIAGNOSTIC PASSED - System appears healthy!")
        return 0

if __name__ == "__main__":
    sys.exit(main())