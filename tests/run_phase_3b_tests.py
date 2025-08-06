#!/usr/bin/env python3
"""
Phase 3b Comprehensive Test Runner
Executes all Phase 3b tests and provides comprehensive reporting

Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('phase_3b_test_results.log')
    ]
)
logger = logging.getLogger(__name__)

class Phase3bTestRunner:
    """Comprehensive test runner for Phase 3b"""
    
    def __init__(self):
        self.test_directory = Path(__file__).parent
        self.start_time = None
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'error_tests': 0,
            'skipped_tests': 0,
            'warnings': 0,
            'test_suites': {},
            'errors': [],
            'warnings_list': [],
            'execution_time': 0
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 3b tests and return comprehensive results"""
        logger.info("🚀 Starting Phase 3b Comprehensive Test Suite")
        logger.info("=" * 80)
        
        self.start_time = time.time()
        
        # Define test suites to run
        test_suites = [
            {
                'name': 'AnalysisParametersManager Unit Tests',
                'file': 'test_analysis_parameters_manager.py',
                'description': 'Core functionality tests for AnalysisParametersManager'
            },
            {
                'name': 'Phase 3b Integration Tests',
                'file': 'test_phase_3b_integration.py',
                'description': 'Full integration tests for Phase 3b components'
            },
            {
                'name': 'Configuration Validation Tests',
                'file': 'test_phase_3b_config_validation.py',
                'description': 'JSON configuration and environment variable validation'
            }
        ]
        
        # Run each test suite
        for suite in test_suites:
            self._run_test_suite(suite)
        
        # Calculate final results
        self._calculate_final_results()
        
        # Generate comprehensive report
        self._generate_report()
        
        return self.test_results
    
    def _run_test_suite(self, suite: Dict[str, str]) -> None:
        """Run a single test suite"""
        logger.info(f"🧪 Running {suite['name']}...")
        logger.info(f"📋 Description: {suite['description']}")
        
        suite_results = {
            'name': suite['name'],
            'file': suite['file'],
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'warnings': 0,
            'execution_time': 0,
            'status': 'unknown',
            'error_details': [],
            'warning_details': []
        }
        
        suite_start_time = time.time()
        
        try:
            # Check if test file exists
            test_file_path = self.test_directory / suite['file']
            if not test_file_path.exists():
                logger.warning(f"⚠️ Test file not found: {suite['file']}")
                suite_results['status'] = 'not_found'
                suite_results['errors'] = 1
                self.test_results['test_suites'][suite['name']] = suite_results
                return
            
            # Run pytest on the specific file
            cmd = [
                sys.executable, '-m', 'pytest',
                str(test_file_path),
                '-v',
                '--tb=short',
                '--disable-warnings',
                '--json-report',
                '--json-report-file=temp_test_results.json'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.test_directory
            )
            
            # Parse results from pytest output
            self._parse_pytest_output(result, suite_results)
            
        except Exception as e:
            logger.error(f"❌ Error running {suite['name']}: {e}")
            suite_results['status'] = 'error'
            suite_results['errors'] = 1
            suite_results['error_details'].append(str(e))
        
        suite_results['execution_time'] = time.time() - suite_start_time
        self.test_results['test_suites'][suite['name']] = suite_results
        
        # Log suite results
        self._log_suite_results(suite_results)
    
    def _parse_pytest_output(self, result: subprocess.CompletedProcess, suite_results: Dict[str, Any]) -> None:
        """Parse pytest output to extract test results"""
        # Determine overall status from return code
        if result.returncode == 0:
            suite_results['status'] = 'passed'
        elif result.returncode == 1:
            suite_results['status'] = 'failed'
        else:
            suite_results['status'] = 'error'
        
        # Parse output for test counts (simplified parsing)
        stdout_lines = result.stdout.split('\n')
        stderr_lines = result.stderr.split('\n')
        
        # Look for pytest summary line
        for line in stdout_lines + stderr_lines:
            line = line.strip()
            
            # Look for test result summary patterns
            if 'passed' in line or 'failed' in line or 'error' in line:
                # Try to extract numbers (simplified)
                words = line.split()
                for i, word in enumerate(words):
                    if word == 'passed' and i > 0:
                        try:
                            suite_results['passed'] = int(words[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif word == 'failed' and i > 0:
                        try:
                            suite_results['failed'] = int(words[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif word == 'error' and i > 0:
                        try:
                            suite_results['errors'] = int(words[i-1])
                        except (ValueError, IndexError):
                            pass
            
            # Capture error messages
            if 'ERROR' in line or 'FAILED' in line:
                suite_results['error_details'].append(line)
            
            # Capture warnings
            if 'WARNING' in line or 'WARN' in line:
                suite_results['warnings'] += 1
                suite_results['warning_details'].append(line)
        
        # If we didn't get specific counts, make reasonable assumptions
        if suite_results['status'] == 'passed' and suite_results['passed'] == 0:
            suite_results['passed'] = 1  # At least one test passed
        elif suite_results['status'] == 'failed' and suite_results['failed'] == 0:
            suite_results['failed'] = 1  # At least one test failed
        elif suite_results['status'] == 'error' and suite_results['errors'] == 0:
            suite_results['errors'] = 1  # At least one error occurred
    
    def _log_suite_results(self, suite_results: Dict[str, Any]) -> None:
        """Log the results of a test suite"""
        status_emoji = {
            'passed': '✅',
            'failed': '❌',
            'error': '💥',
            'not_found': '❓'
        }
        
        emoji = status_emoji.get(suite_results['status'], '❓')
        logger.info(f"{emoji} {suite_results['name']}: {suite_results['status'].upper()}")
        
        if suite_results['passed'] > 0:
            logger.info(f"   ✅ Passed: {suite_results['passed']}")
        if suite_results['failed'] > 0:
            logger.info(f"   ❌ Failed: {suite_results['failed']}")
        if suite_results['errors'] > 0:
            logger.info(f"   💥 Errors: {suite_results['errors']}")
        if suite_results['warnings'] > 0:
            logger.info(f"   ⚠️ Warnings: {suite_results['warnings']}")
        
        logger.info(f"   ⏱️ Execution time: {suite_results['execution_time']:.2f}s")
        
        # Log error details if any
        if suite_results['error_details']:
            logger.info("   📋 Error details:")
            for error in suite_results['error_details'][:3]:  # Limit to first 3 errors
                logger.info(f"      - {error}")
    
    def _calculate_final_results(self) -> None:
        """Calculate final aggregate results"""
        for suite_name, suite_results in self.test_results['test_suites'].items():
            self.test_results['total_tests'] += (
                suite_results['passed'] + 
                suite_results['failed'] + 
                suite_results['errors'] + 
                suite_results['skipped']
            )
            self.test_results['passed_tests'] += suite_results['passed']
            self.test_results['failed_tests'] += suite_results['failed']
            self.test_results['error_tests'] += suite_results['errors']
            self.test_results['skipped_tests'] += suite_results['skipped']
            self.test_results['warnings'] += suite_results['warnings']
            
            # Aggregate errors and warnings
            self.test_results['errors'].extend(suite_results['error_details'])
            self.test_results['warnings_list'].extend(suite_results['warning_details'])
        
        self.test_results['execution_time'] = time.time() - self.start_time
    
    def _generate_report(self) -> None:
        """Generate comprehensive test report"""
        logger.info("=" * 80)
        logger.info("📊 PHASE 3B TEST RESULTS SUMMARY")
        logger.info("=" * 80)
        
        # Overall status
        overall_status = "PASSED" if (
            self.test_results['failed_tests'] == 0 and 
            self.test_results['error_tests'] == 0
        ) else "FAILED"
        
        status_emoji = "🎉" if overall_status == "PASSED" else "❌"
        logger.info(f"{status_emoji} Overall Status: {overall_status}")
        logger.info("")
        
        # Test counts
        logger.info("📈 Test Statistics:")
        logger.info(f"   Total Tests: {self.test_results['total_tests']}")
        logger.info(f"   ✅ Passed: {self.test_results['passed_tests']}")
        logger.info(f"   ❌ Failed: {self.test_results['failed_tests']}")
        logger.info(f"   💥 Errors: {self.test_results['error_tests']}")
        logger.info(f"   ⏭️ Skipped: {self.test_results['skipped_tests']}")
        logger.info(f"   ⚠️ Warnings: {self.test_results['warnings']}")
        logger.info("")
        
        # Success rate
        if self.test_results['total_tests'] > 0:
            success_rate = (self.test_results['passed_tests'] / self.test_results['total_tests']) * 100
            logger.info(f"📊 Success Rate: {success_rate:.1f}%")
        
        # Execution time
        logger.info(f"⏱️ Total Execution Time: {self.test_results['execution_time']:.2f}s")
        logger.info("")
        
        # Test suite breakdown
        logger.info("🧪 Test Suite Breakdown:")
        for suite_name, suite_results in self.test_results['test_suites'].items():
            status_emoji = {
                'passed': '✅',
                'failed': '❌',
                'error': '💥',
                'not_found': '❓'
            }.get(suite_results['status'], '❓')
            
            logger.info(f"   {status_emoji} {suite_name}")
            logger.info(f"      Status: {suite_results['status'].upper()}")
            logger.info(f"      Passed: {suite_results['passed']}, Failed: {suite_results['failed']}, Errors: {suite_results['errors']}")
            logger.info(f"      Time: {suite_results['execution_time']:.2f}s")
        logger.info("")
        
        # Phase 3b specific validations
        self._generate_phase_3b_report()
        
        # Recommendations
        self._generate_recommendations()
    
    def _generate_phase_3b_report(self) -> None:
        """Generate Phase 3b specific validation report"""
        logger.info("🎯 Phase 3b Validation Results:")
        
        # Check which Phase 3b components were tested
        phase_3b_components = {
            'AnalysisParametersManager': False,
            'SettingsManager Integration': False,
            'Configuration Validation': False,
            'Environment Variable Overrides': False,
            'Parameter Validation': False
        }
        
        # Analyze test suite results to determine component coverage
        for suite_name, suite_results in self.test_results['test_suites'].items():
            if 'AnalysisParametersManager' in suite_name:
                phase_3b_components['AnalysisParametersManager'] = suite_results['status'] == 'passed'
            if 'Integration' in suite_name:
                phase_3b_components['SettingsManager Integration'] = suite_results['status'] == 'passed'
            if 'Configuration' in suite_name or 'Validation' in suite_name:
                phase_3b_components['Configuration Validation'] = suite_results['status'] == 'passed'
                phase_3b_components['Environment Variable Overrides'] = suite_results['status'] == 'passed'
                phase_3b_components['Parameter Validation'] = suite_results['status'] == 'passed'
        
        for component, status in phase_3b_components.items():
            emoji = "✅" if status else "❌"
            logger.info(f"   {emoji} {component}")
        logger.info("")
    
    def _generate_recommendations(self) -> None:
        """Generate recommendations based on test results"""
        logger.info("💡 Recommendations:")
        
        if self.test_results['failed_tests'] > 0:
            logger.info("   - Review failed tests and fix underlying issues")
            logger.info("   - Check parameter validation logic")
            logger.info("   - Verify environment variable handling")
        
        if self.test_results['error_tests'] > 0:
            logger.info("   - Investigate test execution errors")
            logger.info("   - Check test environment setup")
            logger.info("   - Verify import paths and dependencies")
        
        if self.test_results['warnings'] > 0:
            logger.info("   - Review warnings for potential issues")
            logger.info("   - Consider updating deprecated functionality")
        
        if self.test_results['failed_tests'] == 0 and self.test_results['error_tests'] == 0:
            logger.info("   🎉 All tests passed! Phase 3b implementation is ready for deployment")
            logger.info("   - Proceed with deployment to test environment")
            logger.info("   - Conduct integration testing with full system")
            logger.info("   - Monitor for any runtime issues")
        
        logger.info("")
        logger.info("📋 Next Steps:")
        logger.info("   1. Address any failed tests or errors")
        logger.info("   2. Update documentation with test results")
        logger.info("   3. Prepare for Phase 3c: Threshold Mapping Configuration")
        logger.info("=" * 80)
    
    def save_results_to_file(self, filename: str = None) -> str:
        """Save test results to a JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase_3b_test_results_{timestamp}.json"
        
        import json
        
        # Prepare results for JSON serialization
        results_for_json = {
            'timestamp': datetime.now().isoformat(),
            'phase': '3b',
            'total_tests': self.test_results['total_tests'],
            'passed_tests': self.test_results['passed_tests'],
            'failed_tests': self.test_results['failed_tests'],
            'error_tests': self.test_results['error_tests'],
            'skipped_tests': self.test_results['skipped_tests'],
            'warnings': self.test_results['warnings'],
            'execution_time': self.test_results['execution_time'],
            'success_rate': (self.test_results['passed_tests'] / max(self.test_results['total_tests'], 1)) * 100,
            'overall_status': 'PASSED' if (self.test_results['failed_tests'] == 0 and self.test_results['error_tests'] == 0) else 'FAILED',
            'test_suites': self.test_results['test_suites'],
            'errors': self.test_results['errors'][:10],  # Limit errors in JSON
            'warnings_list': self.test_results['warnings_list'][:10]  # Limit warnings in JSON
        }
        
        with open(filename, 'w') as f:
            json.dump(results_for_json, f, indent=2)
        
        logger.info(f"📄 Test results saved to: {filename}")
        return filename


def main():
    """Main function to run Phase 3b tests"""
    runner = Phase3bTestRunner()
    
    try:
        results = runner.run_all_tests()
        
        # Save results to file
        results_file = runner.save_results_to_file()
        
        # Return appropriate exit code
        if results['failed_tests'] > 0 or results['error_tests'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("🛑 Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Unexpected error during test execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()