#!/usr/bin/env python3
"""
Ensemble Mode Test Runner
Coordinates and runs all ensemble mode tests with summary reporting

Usage:
    python tests/run_ensemble_tests.py [--quick] [--config] [--full] [--save]
    
Options:
    --quick     Run only the quick validation test
    --config    Run only the configuration test
    --full      Run the comprehensive test suite (default)
    --save      Save all results to timestamped files
"""

import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class EnsembleTestRunner:
    """Main test runner for ensemble mode validation"""
    
    def __init__(self, save_results: bool = False):
        self.save_results = save_results
        self.test_results = {}
        self.start_time = datetime.now()
        self.logs_dir = Path("tests/logs")
        
        # Ensure logs directory exists
        self.logs_dir.mkdir(exist_ok=True)
    
    def run_command(self, command: List[str], test_name: str) -> Dict[str, Any]:
        """Run a test command and capture results"""
        print(f"\n🚀 Running {test_name}...")
        print("=" * 60)
        
        start_time = time.time()
        
        try:
            # Run the test
            result = subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            duration = time.time() - start_time
            
            # Parse the result
            test_result = {
                'test_name': test_name,
                'command': ' '.join(command),
                'exit_code': result.returncode,
                'duration_seconds': duration,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0,
                'timestamp': datetime.now().isoformat()
            }
            
            # Print summary
            if result.returncode == 0:
                print(f"✅ {test_name} PASSED (duration: {duration:.1f}s)")
            else:
                print(f"❌ {test_name} FAILED (duration: {duration:.1f}s)")
                print(f"Exit code: {result.returncode}")
            
            # Show output (last 10 lines for brevity)
            if result.stdout:
                stdout_lines = result.stdout.strip().split('\n')
                if len(stdout_lines) > 10:
                    print("📄 Output (last 10 lines):")
                    for line in stdout_lines[-10:]:
                        print(f"   {line}")
                else:
                    print("📄 Output:")
                    for line in stdout_lines:
                        print(f"   {line}")
            
            if result.stderr and result.returncode != 0:
                print("🔥 Error output:")
                for line in result.stderr.strip().split('\n')[:5]:  # First 5 error lines
                    print(f"   {line}")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏰ {test_name} TIMED OUT after {duration:.1f}s")
            return {
                'test_name': test_name,
                'command': ' '.join(command),
                'exit_code': -1,
                'duration_seconds': duration,
                'success': False,
                'error': 'Timeout after 5 minutes',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 {test_name} CRASHED: {e}")
            return {
                'test_name': test_name,
                'command': ' '.join(command),
                'exit_code': -2,
                'duration_seconds': duration,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_quick_test(self) -> Dict[str, Any]:
        """Run the quick ensemble mode test"""
        command = [sys.executable, "tests/test_ensemble_mode_quick.py", "--mode", "all"]
        return self.run_command(command, "Quick Ensemble Mode Test")
    
    def run_configuration_test(self) -> Dict[str, Any]:
        """Run the configuration validation test"""
        command = [sys.executable, "tests/test_ensemble_configuration.py"]
        return self.run_command(command, "Ensemble Configuration Test")
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run the comprehensive ensemble mode test"""
        command = [sys.executable, "tests/test_ensemble_mode_switching.py"]
        return self.run_command(command, "Comprehensive Ensemble Mode Test")
    
    def check_prerequisites(self) -> bool:
        """Check if all test prerequisites are met"""
        print("🔍 Checking Prerequisites...")
        print("-" * 40)
        
        prerequisites_met = True
        
        # Check if test files exist
        test_files = [
            "tests/test_ensemble_mode_quick.py",
            "tests/test_ensemble_configuration.py", 
            "tests/test_ensemble_mode_switching.py"
        ]
        
        for test_file in test_files:
            if not os.path.exists(test_file):
                print(f"❌ Missing test file: {test_file}")
                prerequisites_met = False
            else:
                print(f"✅ Found: {test_file}")
        
        # Check if .env file exists
        if not os.path.exists(".env"):
            print("⚠️ No .env file found - tests will create one")
        else:
            print("✅ Found .env file")
        
        # Check if service is reachable
        try:
            import requests
            response = requests.get("http://localhost:8881/health", timeout=5)
            if response.status_code == 200:
                print("✅ NLP service is reachable")
            else:
                print(f"⚠️ NLP service returned status {response.status_code}")
                prerequisites_met = False
        except Exception as e:
            print(f"❌ Cannot reach NLP service: {e}")
            prerequisites_met = False
        
        print(f"\nPrerequisites check: {'✅ PASSED' if prerequisites_met else '❌ FAILED'}")
        return prerequisites_met
    
    def generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comprehensive summary report"""
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get('success', False))
        failed_tests = total_tests - successful_tests
        total_duration = sum(r.get('duration_seconds', 0) for r in results)
        
        summary = {
            'test_suite_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
                'total_duration_seconds': total_duration,
                'total_duration_formatted': f"{total_duration:.1f}s"
            },
            'test_results': results,
            'recommendations': [],
            'next_steps': [],
            'overall_status': 'PASSED' if successful_tests == total_tests else 'FAILED'
        }
        
        # Generate recommendations based on results
        if successful_tests == total_tests:
            summary['recommendations'].append("✅ All tests passed - ensemble mode switching is working correctly")
            summary['next_steps'].append("Consider integrating these tests into your CI/CD pipeline")
            summary['next_steps'].append("Monitor production for ensemble mode effectiveness")
        else:
            summary['recommendations'].append("❌ Some tests failed - investigate ensemble configuration")
            
            for result in results:
                if not result.get('success', False):
                    test_name = result.get('test_name', 'Unknown')
                    summary['recommendations'].append(f"🔧 Debug {test_name}: Check logs and service status")
            
            summary['next_steps'].append("Fix failing tests before deploying ensemble mode changes")
            summary['next_steps'].append("Verify .env file configuration and service restart procedures")
        
        return summary
    
    def save_test_results(self, summary: Dict[str, Any]) -> str:
        """Save test results to timestamped file"""
        if not self.save_results:
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.logs_dir / f"ensemble_test_suite_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            print(f"💾 Results saved to {filename}")
            return str(filename)
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return ""
    
    def print_final_report(self, summary: Dict[str, Any]):
        """Print formatted final report"""
        print("\n" + "="*80)
        print("🎯 ENSEMBLE MODE TEST SUITE - FINAL REPORT")
        print("="*80)
        
        test_summary = summary['test_suite_summary']
        
        print(f"\n📊 TEST STATISTICS:")
        print(f"   Total Tests: {test_summary['total_tests']}")
        print(f"   Successful: {test_summary['successful_tests']}")
        print(f"   Failed: {test_summary['failed_tests']}")
        print(f"   Success Rate: {test_summary['success_rate']:.1%}")
        print(f"   Total Duration: {test_summary['total_duration_formatted']}")
        
        print(f"\n🎯 OVERALL STATUS: {summary['overall_status']}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in summary['recommendations']:
            print(f"   {rec}")
        
        print(f"\n🚀 NEXT STEPS:")
        for step in summary['next_steps']:
            print(f"   • {step}")
        
        print(f"\n📋 INDIVIDUAL TEST RESULTS:")
        for result in summary['test_results']:
            status = "✅ PASSED" if result.get('success', False) else "❌ FAILED"
            duration = result.get('duration_seconds', 0)
            print(f"   {result['test_name']}: {status} ({duration:.1f}s)")
        
        print("\n" + "="*80)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run Ash-NLP ensemble mode test suite')
    parser.add_argument('--quick', action='store_true', help='Run only quick validation test')
    parser.add_argument('--config', action='store_true', help='Run only configuration test')
    parser.add_argument('--full', action='store_true', help='Run comprehensive test suite')
    parser.add_argument('--save', action='store_true', help='Save results to timestamped files')
    
    args = parser.parse_args()
    
    # Default to full if no specific test specified
    if not (args.quick or args.config or args.full):
        args.full = True
    
    print("🧪 Ash-NLP Ensemble Mode Test Suite Runner")
    print("=" * 60)
    
    # Create test runner
    runner = EnsembleTestRunner(save_results=args.save)
    
    # Check prerequisites
    if not runner.check_prerequisites():
        print("\n❌ Prerequisites not met - aborting test suite")
        return 1
    
    print(f"\n🕐 Test suite started at: {runner.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests based on arguments
    test_results = []
    
    if args.quick:
        result = runner.run_quick_test()
        test_results.append(result)
    
    if args.config:
        result = runner.run_configuration_test()
        test_results.append(result)
    
    if args.full:
        # Run all tests in sequence
        print("\n🚀 Running Full Test Suite...")
        
        # Quick test first
        result = runner.run_quick_test()
        test_results.append(result)
        
        # Then configuration test
        result = runner.run_configuration_test()
        test_results.append(result)
        
        # Finally comprehensive test
        result = runner.run_comprehensive_test()
        test_results.append(result)
    
    # Generate summary
    summary = runner.generate_summary_report(test_results)
    
    # Save results if requested
    results_file = runner.save_test_results(summary)
    
    # Print final report
    runner.print_final_report(summary)
    
    # Return appropriate exit code
    if summary['overall_status'] == 'PASSED':
        print("\n🎉 ALL TESTS PASSED - Ensemble mode switching is working!")
        return 0
    else:
        print("\n💥 SOME TESTS FAILED - Check the results and fix issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())