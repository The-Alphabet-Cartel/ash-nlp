#!/usr/bin/env python3
"""
Ash-NLP Ensemble Mode Testing Suite
Tests whether changing NLP_ENSEMBLE_MODE environment variable actually changes responses

This test suite validates that the three ensemble modes (consensus, majority, weighted)
produce different responses from the NLP server, confirming proper configuration integration.

Usage:
    python tests/test_ensemble_mode_switching.py
    
Requirements:
    - NLP server running on localhost:8881
    - Ability to modify .env file or environment variables
    - Three models loaded (depression, sentiment, emotional_distress)
"""

import os
import sys
import time
import json
import requests
import logging
from typing import Dict, List, Any, Tuple
from pathlib import Path
import subprocess
from dataclasses import dataclass
from datetime import datetime

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'tests/logs/ensemble_mode_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

# Test Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30
ENV_FILE_PATH = ".env"

@dataclass
class TestMessage:
    """Test message configuration"""
    content: str
    description: str
    expected_differences: List[str]
    user_id: str = "test_user_ensemble"
    channel_id: str = "test_channel_ensemble"

@dataclass
class EnsembleMode:
    """Ensemble mode configuration"""
    name: str
    description: str
    config_value: str

# Test Cases - Designed to trigger different model responses
TEST_MESSAGES = [
    TestMessage(
        content="I want to kill myself tonight",
        description="High crisis explicit - should show clear differences",
        expected_differences=["confidence", "crisis_level", "consensus_method"]
    ),
    TestMessage(
        content="This exam is killing me but I think I can handle it",
        description="Ambiguous crisis language - ideal for gap detection differences",
        expected_differences=["gap_detection", "requires_review", "consensus"]
    ),
    TestMessage(
        content="I don't want to be here anymore",
        description="Moderate crisis expression - should trigger different consensus patterns",
        expected_differences=["confidence", "individual_results", "consensus_method"]
    ),
    TestMessage(
        content="Everything is meaningless and I have no hope left",
        description="Hopelessness pattern - should show ensemble decision differences",
        expected_differences=["weight_application", "confidence", "crisis_level"]
    ),
    TestMessage(
        content="I'm dying of laughter watching this comedy show",
        description="False positive candidate - ensemble should handle context differently",
        expected_differences=["context_handling", "confidence", "final_prediction"]
    )
]

# Ensemble Modes to Test
ENSEMBLE_MODES = [
    EnsembleMode(
        name="consensus",
        description="All models must agree for high confidence",
        config_value="consensus"
    ),
    EnsembleMode(
        name="majority", 
        description="Democratic voting with confidence weighting",
        config_value="majority"
    ),
    EnsembleMode(
        name="weighted",
        description="Configurable model importance weighting",
        config_value="weighted"
    )
]

class EnsembleModeTestSuite:
    """Main test suite for ensemble mode switching"""
    
    def __init__(self):
        self.results = {}
        self.original_env_backup = None
        self.current_mode = None
        
        # Ensure logs directory exists
        os.makedirs("tests/logs", exist_ok=True)
        
    def backup_env_file(self) -> bool:
        """Backup original .env file"""
        try:
            if os.path.exists(ENV_FILE_PATH):
                backup_path = f"{ENV_FILE_PATH}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                subprocess.run(["cp", ENV_FILE_PATH, backup_path], check=True)
                logger.info(f"✅ Environment file backed up to {backup_path}")
                return True
            else:
                logger.warning(f"⚠️ No .env file found at {ENV_FILE_PATH}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to backup .env file: {e}")
            return False
    
    def modify_env_variable(self, variable_name: str, new_value: str) -> bool:
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
            
            logger.info(f"✅ Set {variable_name}={new_value} in .env file")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to modify .env file: {e}")
            return False
    
    def restart_service_if_needed(self) -> bool:
        """Check if service restart is needed and prompt user"""
        logger.warning("⚠️ Environment variable changed - service may need restart")
        logger.info("📝 If running in Docker, restart with: docker-compose restart ash-nlp")
        logger.info("📝 If running locally, restart the Python service")
        
        # Wait a moment for any auto-reload mechanisms
        time.sleep(2)
        
        # Test if service is responsive
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Service appears to be responding")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Service not responding: {e}")
        
        return True  # Continue anyway, might be auto-reloading
    
    def wait_for_service_ready(self, max_attempts: int = 12) -> bool:
        """Wait for service to be ready after configuration change"""
        logger.info("⏳ Waiting for service to be ready...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get('status') == 'healthy':
                        models_loaded = health_data.get('models_loaded', False)
                        if models_loaded:
                            logger.info(f"✅ Service ready! (attempt {attempt + 1})")
                            return True
                        else:
                            logger.info(f"⏳ Models still loading... (attempt {attempt + 1})")
                
            except Exception as e:
                logger.debug(f"Service not ready yet: {e}")
            
            if attempt < max_attempts - 1:
                time.sleep(5)
        
        logger.error(f"❌ Service not ready after {max_attempts} attempts")
        return False
    
    def get_current_ensemble_mode(self) -> str:
        """Get current ensemble mode from service"""
        try:
            response = requests.get(f"{BASE_URL}/ensemble/status", timeout=TIMEOUT)
            if response.status_code == 200:
                status_data = response.json()
                current_mode = status_data.get('ensemble_info', {}).get('ensemble_mode', 'unknown')
                logger.info(f"📊 Current ensemble mode: {current_mode}")
                return current_mode
            else:
                logger.warning(f"⚠️ Could not get ensemble status: {response.status_code}")
                return "unknown"
        except Exception as e:
            logger.error(f"❌ Failed to get current ensemble mode: {e}")
            return "unknown"
    
    def analyze_message_with_mode(self, message: TestMessage, mode: EnsembleMode) -> Dict[str, Any]:
        """Analyze a message with specific ensemble mode"""
        try:
            logger.info(f"🔍 Analyzing with {mode.name} mode: '{message.content[:50]}...'")
            
            payload = {
                "message": message.content,
                "user_id": message.user_id,
                "channel_id": message.channel_id
            }
            
            response = requests.post(
                f"{BASE_URL}/analyze",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Analysis complete for {mode.name} mode")
                
                # Log key metrics
                ensemble_analysis = result.get('ensemble_analysis', {})
                consensus = ensemble_analysis.get('consensus', {})
                
                logger.info(f"📊 {mode.name} result: {consensus.get('prediction', 'unknown')} "
                          f"(confidence: {consensus.get('confidence', 0):.3f})")
                
                return {
                    'success': True,
                    'data': result,
                    'mode': mode.name,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.error(f"❌ Analysis failed for {mode.name}: {response.status_code}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'mode': mode.name,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Analysis exception for {mode.name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'mode': mode.name,
                'timestamp': datetime.now().isoformat()
            }
    
    def compare_ensemble_results(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Compare results across different ensemble modes"""
        comparison = {
            'differences_found': [],
            'significant_differences': [],
            'mode_comparisons': {},
            'summary': {}
        }
        
        # Extract successful results
        successful_results = {mode: data for mode, data in results.items() 
                            if data.get('success', False)}
        
        if len(successful_results) < 2:
            comparison['error'] = "Not enough successful results to compare"
            return comparison
        
        modes = list(successful_results.keys())
        
        # Compare each pair of modes
        for i, mode1 in enumerate(modes):
            for mode2 in modes[i+1:]:
                pair_key = f"{mode1}_vs_{mode2}"
                comparison['mode_comparisons'][pair_key] = self._compare_two_results(
                    successful_results[mode1]['data'],
                    successful_results[mode2]['data'],
                    mode1,
                    mode2
                )
        
        # Generate summary
        comparison['summary'] = self._generate_comparison_summary(comparison['mode_comparisons'])
        
        return comparison
    
    def _compare_two_results(self, result1: Dict, result2: Dict, mode1: str, mode2: str) -> Dict[str, Any]:
        """Compare two specific analysis results"""
        differences = {
            'consensus_prediction': None,
            'confidence_difference': None,
            'consensus_method': None,
            'gap_detection': None,
            'individual_model_differences': [],
            'pattern_analysis_differences': None
        }
        
        # Extract ensemble analysis
        ensemble1 = result1.get('ensemble_analysis', {})
        ensemble2 = result2.get('ensemble_analysis', {})
        
        consensus1 = ensemble1.get('consensus', {})
        consensus2 = ensemble2.get('consensus', {})
        
        # Compare consensus predictions
        pred1 = consensus1.get('prediction', 'unknown')
        pred2 = consensus2.get('prediction', 'unknown')
        
        if pred1 != pred2:
            differences['consensus_prediction'] = {
                mode1: pred1,
                mode2: pred2,
                'different': True
            }
        
        # Compare confidence levels
        conf1 = consensus1.get('confidence', 0)
        conf2 = consensus2.get('confidence', 0)
        conf_diff = abs(conf1 - conf2)
        
        if conf_diff > 0.05:  # Significant confidence difference
            differences['confidence_difference'] = {
                mode1: conf1,
                mode2: conf2,
                'difference': conf_diff,
                'significant': conf_diff > 0.1
            }
        
        # Compare consensus methods
        method1 = consensus1.get('method', 'unknown')
        method2 = consensus2.get('method', 'unknown')
        
        if method1 != method2:
            differences['consensus_method'] = {
                mode1: method1,
                mode2: method2,
                'different': True
            }
        
        # Compare gap detection
        gap1 = ensemble1.get('gap_detection', {})
        gap2 = ensemble2.get('gap_detection', {})
        
        gap_detected1 = gap1.get('gap_detected', False)
        gap_detected2 = gap2.get('gap_detected', False)
        
        if gap_detected1 != gap_detected2:
            differences['gap_detection'] = {
                mode1: gap_detected1,
                mode2: gap_detected2,
                'different': True
            }
        
        return differences
    
    def _generate_comparison_summary(self, comparisons: Dict) -> Dict[str, Any]:
        """Generate summary of comparison results"""
        summary = {
            'total_comparisons': len(comparisons),
            'differences_found': 0,
            'significant_differences': 0,
            'most_common_differences': [],
            'ensemble_modes_working': False
        }
        
        difference_types = {}
        
        for comparison_key, comparison_data in comparisons.items():
            for diff_type, diff_data in comparison_data.items():
                if diff_data and isinstance(diff_data, dict):
                    if diff_data.get('different', False) or diff_data.get('significant', False):
                        summary['differences_found'] += 1
                        
                        if diff_type not in difference_types:
                            difference_types[diff_type] = 0
                        difference_types[diff_type] += 1
                        
                        if diff_data.get('significant', False):
                            summary['significant_differences'] += 1
        
        # Sort difference types by frequency
        summary['most_common_differences'] = sorted(
            difference_types.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Determine if ensemble modes are working
        summary['ensemble_modes_working'] = summary['differences_found'] > 0
        
        return summary
    
    def run_test_for_message(self, message: TestMessage) -> Dict[str, Any]:
        """Run ensemble mode test for a specific message"""
        logger.info(f"\n🎯 Testing message: {message.description}")
        logger.info(f"📝 Content: '{message.content}'")
        
        message_results = {}
        
        for mode in ENSEMBLE_MODES:
            logger.info(f"\n--- Testing {mode.name.upper()} mode ---")
            
            # Update environment variable
            if not self.modify_env_variable("NLP_ENSEMBLE_MODE", mode.config_value):
                logger.error(f"❌ Failed to set ensemble mode to {mode.name}")
                continue
            
            # Wait for service to pick up changes
            self.restart_service_if_needed()
            
            # Verify mode change
            time.sleep(3)  # Allow time for configuration reload
            current_mode = self.get_current_ensemble_mode()
            
            if current_mode.lower() != mode.config_value.lower():
                logger.warning(f"⚠️ Mode may not have changed: expected {mode.config_value}, got {current_mode}")
            
            # Analyze message with this mode
            result = self.analyze_message_with_mode(message, mode)
            message_results[mode.name] = result
            
            # Small delay between mode changes
            time.sleep(2)
        
        # Compare results across modes
        comparison = self.compare_ensemble_results(message_results)
        
        return {
            'message': message,
            'results': message_results,
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Run complete ensemble mode testing suite"""
        logger.info("🚀 Starting Ensemble Mode Testing Suite")
        logger.info("="*60)
        
        # Backup environment
        if not self.backup_env_file():
            logger.warning("⚠️ Could not backup .env file, proceeding anyway")
        
        # Check initial service status
        if not self.wait_for_service_ready():
            logger.error("❌ Service not ready, aborting test")
            return {'error': 'Service not ready'}
        
        test_results = {
            'test_suite_info': {
                'total_messages': len(TEST_MESSAGES),
                'total_modes': len(ENSEMBLE_MODES),
                'start_time': datetime.now().isoformat(),
                'test_version': 'v3.1_ensemble_mode_validation'
            },
            'message_tests': {},
            'overall_summary': {}
        }
        
        # Test each message
        for i, message in enumerate(TEST_MESSAGES):
            logger.info(f"\n{'='*60}")
            logger.info(f"🧪 TEST {i+1}/{len(TEST_MESSAGES)}")
            
            message_test_key = f"test_{i+1}_{message.description.replace(' ', '_').lower()}"
            test_results['message_tests'][message_test_key] = self.run_test_for_message(message)
        
        # Generate overall summary
        test_results['overall_summary'] = self._generate_overall_summary(test_results['message_tests'])
        test_results['test_suite_info']['end_time'] = datetime.now().isoformat()
        
        return test_results
    
    def _generate_overall_summary(self, message_tests: Dict) -> Dict[str, Any]:
        """Generate overall test suite summary"""
        summary = {
            'total_tests': len(message_tests),
            'successful_tests': 0,
            'tests_with_differences': 0,
            'tests_with_significant_differences': 0,
            'ensemble_modes_functioning': False,
            'most_responsive_differences': [],
            'recommendations': []
        }
        
        difference_counts = {}
        
        for test_key, test_data in message_tests.items():
            comparison = test_data.get('comparison', {})
            test_summary = comparison.get('summary', {})
            
            if test_summary.get('differences_found', 0) > 0:
                summary['tests_with_differences'] += 1
                
                if test_summary.get('significant_differences', 0) > 0:
                    summary['tests_with_significant_differences'] += 1
                
                # Count difference types
                for diff_type, count in test_summary.get('most_common_differences', []):
                    if diff_type not in difference_counts:
                        difference_counts[diff_type] = 0
                    difference_counts[diff_type] += count
            
            # Count successful tests (tests that ran without errors)
            results = test_data.get('results', {})
            successful_modes = sum(1 for r in results.values() if r.get('success', False))
            if successful_modes >= 2:  # Need at least 2 modes to compare
                summary['successful_tests'] += 1
        
        # Sort difference types
        summary['most_responsive_differences'] = sorted(
            difference_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Determine if ensemble modes are functioning
        summary['ensemble_modes_functioning'] = summary['tests_with_differences'] > 0
        
        # Generate recommendations
        if summary['ensemble_modes_functioning']:
            summary['recommendations'].append("✅ Ensemble modes are working - different modes produce different results")
            if summary['tests_with_significant_differences'] > 0:
                summary['recommendations'].append("🎯 Significant differences detected - ensemble configuration is highly responsive")
        else:
            summary['recommendations'].append("❌ Ensemble modes may not be working - all modes produce identical results")
            summary['recommendations'].append("🔧 Check: Environment variable loading, service restart, configuration management")
        
        if difference_counts.get('confidence_difference', 0) > 0:
            summary['recommendations'].append("📊 Confidence variations detected - models are being weighted differently")
        
        if difference_counts.get('consensus_method', 0) > 0:
            summary['recommendations'].append("⚙️ Consensus method changes detected - ensemble algorithm switching is working")
        
        return summary
    
    def save_results(self, results: Dict[str, Any]) -> str:
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tests/logs/ensemble_mode_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"📁 Results saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"❌ Failed to save results: {e}")
            return ""
    
    def print_summary_report(self, results: Dict[str, Any]):
        """Print formatted summary report"""
        print("\n" + "="*80)
        print("🎯 ENSEMBLE MODE TESTING SUMMARY REPORT")
        print("="*80)
        
        overall_summary = results.get('overall_summary', {})
        
        print(f"\n📊 TEST STATISTICS:")
        print(f"   Total Tests: {overall_summary.get('total_tests', 0)}")
        print(f"   Successful Tests: {overall_summary.get('successful_tests', 0)}")
        print(f"   Tests with Differences: {overall_summary.get('tests_with_differences', 0)}")
        print(f"   Tests with Significant Differences: {overall_summary.get('tests_with_significant_differences', 0)}")
        
        print(f"\n🎯 ENSEMBLE FUNCTIONALITY:")
        if overall_summary.get('ensemble_modes_functioning', False):
            print("   ✅ ENSEMBLE MODES ARE WORKING!")
            print("   Different modes produce different results as expected.")
        else:
            print("   ❌ ENSEMBLE MODES MAY NOT BE WORKING!")
            print("   All modes produce identical results - check configuration.")
        
        print(f"\n📈 MOST RESPONSIVE DIFFERENCES:")
        for diff_type, count in overall_summary.get('most_responsive_differences', [])[:5]:
            print(f"   • {diff_type}: {count} occurrences")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in overall_summary.get('recommendations', []):
            print(f"   {rec}")
        
        print("\n" + "="*80)

def main():
    """Main function to run ensemble mode testing"""
    print("🚀 Ash-NLP Ensemble Mode Testing Suite v3.1")
    print("Testing whether NLP_ENSEMBLE_MODE changes actually affect responses\n")
    
    # Create test suite instance
    test_suite = EnsembleModeTestSuite()
    
    try:
        # Run full test suite
        results = test_suite.run_full_test_suite()
        
        # Save results
        results_file = test_suite.save_results(results)
        
        # Print summary
        test_suite.print_summary_report(results)
        
        print(f"\n📁 Detailed results saved to: {results_file}")
        print("🔍 Check the log file for complete analysis details")
        
        # Return appropriate exit code
        overall_summary = results.get('overall_summary', {})
        if overall_summary.get('ensemble_modes_functioning', False):
            print("\n✅ TEST SUITE PASSED - Ensemble modes are working!")
            return 0
        else:
            print("\n❌ TEST SUITE FAILED - Ensemble modes may not be working!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Test suite interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Test suite failed with exception: {e}")
        logger.exception("Full exception details:")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)