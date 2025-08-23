#!/usr/bin/env python3
"""
Phase 3e Step 7: Comprehensive Test Runner
Orchestrates all integration, performance, and production tests

FILE: tests/run_step7_tests.py
VERSION: v3.1-3e-7-1
AUTHOR: The Alphabet Cartel
REPOSITORY: https://github.com/the-alphabet-cartel/ash-nlp
COMMUNITY: https://discord.gg/alphabetcartel | https://alphabetcartel.org

Usage:
    python tests/run_step7_tests.py                    # Run all tests
    python tests/run_step7_tests.py --quick            # Run quick tests only
    python tests/run_step7_tests.py --performance      # Run performance tests only
    python tests/run_step7_tests.py --integration      # Run integration tests only
"""

import sys
import os
import argparse
import time
import logging
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import colorlog for colored output
try:
    import colorlog
except ImportError:
    print("❌ colorlog not installed. Install with: pip install colorlog")
    sys.exit(1)

def setup_colored_logging():
    """Setup colored logging for the test runner"""
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[STEP7-RUNNER] %(levelname)s%(reset)s: %(message)s',
        datefmt='%H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger('Step7TestRunner')
    logger.setLevel(logging.INFO)
    logger.handlers = [console_handler]
    
    return logger

def run_test_suite(test_file: str, logger: logging.Logger) -> Dict:
    """Run a specific test suite and return results"""
    logger.info(f"🚀 Running {test_file}...")
    
    start_time = time.time()
    
    try:
        # Import and run the test
        if test_file == 'test_configuration_flow.py':
            from test_configuration_flow import TestConfigurationFlow
            import unittest
            
            suite = unittest.TestLoader().loadTestsFromTestCase(TestConfigurationFlow)
            runner = unittest.TextTestRunner(verbosity=2, buffer=True)
            result = runner.run(suite)
            
        elif test_file == 'test_crisis_detection_workflow.py':
            from test_crisis_detection_workflow import TestCrisisDetectionWorkflow
            import unittest
            
            suite = unittest.TestLoader().loadTestsFromTestCase(TestCrisisDetectionWorkflow)
            runner = unittest.TextTestRunner(verbosity=2, buffer=True)
            result = runner.run(suite)
            
        elif test_file == 'test_performance_validation.py':
            from test_performance_validation import TestPerformanceValidation
            import unittest
            
            suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformanceValidation)
            runner = unittest.TextTestRunner(verbosity=2, buffer=True)
            result = runner.run(suite)
            
        elif test_file == 'test_full_integration.py':
            from test_full_integration import TestFullIntegration
            import unittest
            
            suite = unittest.TestLoader().loadTestsFromTestCase(TestFullIntegration)
            runner = unittest.TextTestRunner(verbosity=2, buffer=True)
            result = runner.run(suite)
            
        else:
            logger.error(f"❌ Unknown test file: {test_file}")
            return {'success': False, 'error': f'Unknown test file: {test_file}'}
            
        duration = time.time() - start_time
        
        if result.wasSuccessful():
            logger.info(f"✅ {test_file} completed successfully in {duration:.2f}s")
            return {
                'success': True,
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'duration': duration
            }
        else:
            logger.error(f"❌ {test_file} completed with issues in {duration:.2f}s")
            logger.error(f"   Failures: {len(result.failures)}")
            logger.error(f"   Errors: {len(result.errors)}")
            
            # Log specific failures for debugging
            for test, failure in result.failures[:3]:  # Show first 3 failures
                logger.error(f"   FAILURE: {test}")
                
            for test, error in result.errors[:3]:  # Show first 3 errors
                logger.error(f"   ERROR: {test}")
                
            return {
                'success': False,
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'duration': duration
            }
            
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"❌ {test_file} failed with exception: {e}")
        return {
            'success': False,
            'error': str(e),
            'duration': duration
        }

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(
        description='Phase 3e Step 7 Comprehensive Test Runner',
        epilog='The Alphabet Cartel - Crisis Detection System Testing'
    )
    
    parser.add_argument('--quick', action='store_true',
                       help='Run quick tests only (config flow + basic workflow)')
    parser.add_argument('--performance', action='store_true', 
                       help='Run performance tests only')
    parser.add_argument('--integration', action='store_true',
                       help='Run integration tests only (no performance)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_colored_logging()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Print header
    logger.info("🌈" * 30)
    logger.info("🚀 PHASE 3E STEP 7: COMPREHENSIVE TEST RUNNER")
    logger.info("🏳️‍🌈 The Alphabet Cartel - Crisis Detection System")
    logger.info("🌈" * 30)
    logger.info("")
    
    # Determine which tests to run
    if args.quick:
        test_files = [
            'test_configuration_flow.py',
            'test_crisis_detection_workflow.py'
        ]
        logger.info("⚡ Running QUICK test suite...")
    elif args.performance:
        test_files = [
            'test_performance_validation.py'
        ]
        logger.info("📊 Running PERFORMANCE test suite...")
    elif args.integration:
        test_files = [
            'test_configuration_flow.py',
            'test_crisis_detection_workflow.py'
        ]
        logger.info("🔗 Running INTEGRATION test suite...")
    else:
        test_files = [
            'test_configuration_flow.py',
            'test_crisis_detection_workflow.py', 
            'test_performance_validation.py',
            'test_full_integration.py'
        ]
        logger.info("🌟 Running COMPREHENSIVE test suite...")
        
    logger.info(f"📋 Tests to run: {len(test_files)}")
    logger.info("")
    
    # Run tests
    overall_start_time = time.time()
    test_results = {}
    
    for i, test_file in enumerate(test_files, 1):
        logger.info(f"📍 Test {i}/{len(test_files)}: {test_file}")
        logger.info("-" * 50)
        
        result = run_test_suite(test_file, logger)
        test_results[test_file] = result
        
        logger.info("")
        
    overall_duration = time.time() - overall_start_time
    
    # Generate summary report
    logger.info("🌈" * 30)
    logger.info("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
    logger.info("🌈" * 30)
    logger.info("")
    
    total_tests = 0
    total_passed = 0
    total_failed = 0
    successful_suites = 0
    
    for test_file, result in test_results.items():
        suite_name = test_file.replace('.py', '').replace('_', ' ').title()
        
        if result['success']:
            status = "✅ PASSED"
            successful_suites += 1
            tests_passed = result['tests_run'] - result.get('failures', 0) - result.get('errors', 0)
            total_passed += tests_passed
        else:
            status = "❌ FAILED"
            tests_passed = 0
            
        tests_run = result.get('tests_run', 0)
        duration = result.get('duration', 0)
        
        total_tests += tests_run
        if not result['success']:
            total_failed += tests_run - tests_passed
            
        logger.info(f"{suite_name}: {status}")
        logger.info(f"   Tests run: {tests_run}")
        logger.info(f"   Duration: {duration:.2f}s")
        
        if 'failures' in result:
            logger.info(f"   Failures: {result['failures']}")
        if 'errors' in result:
            logger.info(f"   Errors: {result['errors']}")
        if 'error' in result:
            logger.info(f"   Exception: {result['error']}")
            
        logger.info("")
    
    # Overall statistics
    logger.info("📈 OVERALL STATISTICS:")
    logger.info("-" * 25)
    logger.info(f"Test suites run: {len(test_files)}")
    logger.info(f"Successful suites: {successful_suites}/{len(test_files)}")
    logger.info(f"Total tests: {total_tests}")
    logger.info(f"Tests passed: {total_passed}")
    logger.info(f"Tests failed: {total_failed}")
    logger.info(f"Total duration: {overall_duration:.2f}s")
    
    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        logger.info(f"Success rate: {success_rate:.1f}%")
        
    logger.info("")
    
    # Final determination
    all_suites_passed = successful_suites == len(test_files)
    critical_tests_passed = (
        test_results.get('test_configuration_flow.py', {}).get('success', False) and
        test_results.get('test_crisis_detection_workflow.py', {}).get('success', False)
    )
    
    if all_suites_passed:
        logger.info("🏆 PHASE 3E STEP 7: ✅ FULLY SUCCESSFUL!")
        logger.info("   ✅ All integration tests passed")
        logger.info("   ✅ Crisis detection workflow validated") 
        logger.info("   ✅ Performance benchmarks established")
        logger.info("   ✅ Production readiness confirmed")
        exit_code = 0
    elif critical_tests_passed:
        logger.info("⚡ PHASE 3E STEP 7: ✅ CRITICAL TESTS PASSED!")
        logger.info("   ✅ Core integration functional")
        logger.info("   ✅ Crisis detection operational")
        if not test_results.get('test_performance_validation.py', {}).get('success', True):
            logger.info("   📊 Performance data collected for optimization")
        exit_code = 0
    else:
        logger.error("❌ PHASE 3E STEP 7: CRITICAL ISSUES FOUND")
        logger.error("   Core functionality needs attention before proceeding")
        exit_code = 1
        
    logger.info("")
    logger.info("🏳️‍🌈 The Alphabet Cartel - Crisis Detection Testing Complete")
    logger.info("💬 Discord: https://discord.gg/alphabetcartel")
    logger.info("🌐 Website: https://alphabetcartel.org") 
    logger.info("🌈" * 30)
    
    return exit_code

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)