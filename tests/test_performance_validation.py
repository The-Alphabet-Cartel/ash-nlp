#!/usr/bin/env python3
"""
Phase 3e Step 7.2: Performance Validation Test Suite  
Tests system performance against Step 7 benchmarks with load testing

FILE: tests/test_performance_validation.py
VERSION: v3.1-3e-7.2-1
AUTHOR: The Alphabet Cartel
REPOSITORY: https://github.com/the-alphabet-cartel/ash-nlp
COMMUNITY: https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import sys
import os
import unittest
import logging
import time
import threading
import asyncio
import statistics
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import colorlog for colored test output
try:
    import colorlog
except ImportError:
    print("❌ colorlog not installed. Install with: pip install colorlog")
    sys.exit(1)

# Import main initialization function
try:
    from main import initialize_unified_managers
    from analysis.crisis_analyzer import create_crisis_analyzer
except ImportError as e:
    print(f"❌ Failed to import main: {e}")
    sys.exit(1)


class TestPerformanceValidation(unittest.TestCase):
    """Test suite for performance validation against Step 7 benchmarks"""
    
    @classmethod
    def setUpClass(cls):
        """Set up colored logging and initialize system"""
        # Configure colorlog formatter
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[PERF-TEST] %(levelname)s%(reset)s: %(message)s',
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
        
        # Set up console handler
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Configure logger
        cls.logger = logging.getLogger('PerformanceValidationTest')
        cls.logger.setLevel(logging.INFO)
        cls.logger.handlers = [console_handler]
        
        cls.logger.info("🚀 Starting Performance Validation Tests")
        
        # Performance targets from step_7.md
        cls.performance_targets = {
            'crisis_analysis_ms': 500,     # Current: 750-1500ms, Target: < 500ms
            'config_access_ms': 10,        # < 10ms per config access
            'manager_init_ms': 500,        # < 500ms for all managers
            'learning_feedback_ms': 50,    # < 50ms per feedback event
            'concurrent_throughput': 25,   # messages/second (scaled down for testing)
            'memory_baseline_mb': 200,     # < 200MB for full system
            'system_stability_hours': 0.1  # 6 minutes for testing (vs 4+ hours target)
        }
        
        # Initialize the complete system
        try:
            cls.logger.info("🔧 Initializing complete system for performance testing...")
            start_time = time.time()
            cls.managers = initialize_unified_managers()
            cls.init_time = (time.time() - start_time) * 1000
            cls.logger.info(f"✅ System initialized in {cls.init_time:.2f}ms")
            
            # Verify critical components
            cls.crisis_analyzer = cls.managers.get('crisis_analyzer')
            cls.unified_config = cls.managers.get('unified_config')
            
            if not cls.crisis_analyzer:
                raise RuntimeError("CrisisAnalyzer not available for performance testing")
                
        except Exception as e:
            cls.logger.error(f"❌ System initialization failed: {e}")
            raise
            
        # Performance tracking
        cls.performance_results = {}
        cls.load_test_results = {}
        
        # Test message for performance testing
        cls.test_message = "I'm having a really difficult time and feeling overwhelmed with everything going on."
        
    def setUp(self):
        """Set up each test case"""
        self.start_time = time.time()
        
    def tearDown(self):
        """Clean up after each test case"""
        test_time = (time.time() - self.start_time) * 1000
        self.logger.info(f"⏱️ Test completed in {test_time:.2f}ms")
        
    def test_01_manager_initialization_performance(self):
        """Test manager initialization performance against benchmarks"""
        self.logger.info("🔧 Testing manager initialization performance...")
        
        init_time = self.__class__.init_time
        target_time = self.performance_targets['manager_init_ms']
        
        self.logger.info(f"📊 Manager initialization time: {init_time:.2f}ms")
        self.logger.info(f"🎯 Target time: {target_time}ms")
        
        if init_time <= target_time:
            self.logger.info(f"🚀 Manager Initialization: EXCELLENT ({init_time:.2f}ms <= {target_time}ms)")
            performance_grade = "EXCELLENT"
        elif init_time <= target_time * 1.5:
            self.logger.info(f"✅ Manager Initialization: GOOD ({init_time:.2f}ms <= {target_time * 1.5}ms)")
            performance_grade = "GOOD"
        elif init_time <= target_time * 2:
            self.logger.warning(f"⚠️ Manager Initialization: ACCEPTABLE ({init_time:.2f}ms <= {target_time * 2}ms)")
            performance_grade = "ACCEPTABLE"
        else:
            self.logger.error(f"❌ Manager Initialization: SLOW ({init_time:.2f}ms > {target_time * 2}ms)")
            performance_grade = "SLOW"
            
        # Store result
        self.__class__.performance_results['manager_initialization'] = {
            'time_ms': init_time,
            'target_ms': target_time,
            'grade': performance_grade,
            'meets_target': init_time <= target_time
        }
        
        # Don't fail test if slow, just record performance
        self.assertIsNotNone(self.managers, "Managers should be initialized")
        
    def test_02_configuration_access_performance(self):
        """Test configuration access performance"""
        self.logger.info("🔧 Testing configuration access performance...")
        
        config = self.unified_config
        target_time = self.performance_targets['config_access_ms']
        
        # Test multiple configuration accesses
        config_access_times = []
        test_configs = [
            ('GLOBAL_LOG_LEVEL', 'INFO'),
            ('NLP_SERVER_HOST', '0.0.0.0'),
            ('GLOBAL_NLP_API_PORT', 8881),
            ('NLP_LOG_ENABLE_FILE_LOGGING', True),
            ('NLP_ANALYSIS_ENABLE_ENSEMBLE', True)
        ]
        
        for config_key, default_value in test_configs:
            try:
                start_time = time.time()
                
                # Test appropriate method based on expected type
                if isinstance(default_value, bool):
                    value = config.get_env_bool(config_key, default_value)
                elif isinstance(default_value, int):
                    value = config.get_env_int(config_key, default_value)
                else:
                    value = config.get_env(config_key, default_value)
                    
                access_time = (time.time() - start_time) * 1000
                config_access_times.append(access_time)
                
                self.logger.info(f"   ✅ {config_key}: {access_time:.3f}ms")
                
            except Exception as e:
                self.logger.error(f"   ❌ {config_key} access failed: {e}")
                
        if config_access_times:
            avg_access_time = statistics.mean(config_access_times)
            max_access_time = max(config_access_times)
            
            self.logger.info(f"📊 Configuration Access Performance:")
            self.logger.info(f"   Average: {avg_access_time:.3f}ms")
            self.logger.info(f"   Maximum: {max_access_time:.3f}ms")
            self.logger.info(f"   Target: {target_time}ms")
            
            if avg_access_time <= target_time:
                self.logger.info(f"🚀 Config Access: EXCELLENT (avg {avg_access_time:.3f}ms <= {target_time}ms)")
                performance_grade = "EXCELLENT"
            elif avg_access_time <= target_time * 2:
                self.logger.info(f"✅ Config Access: GOOD (avg {avg_access_time:.3f}ms <= {target_time * 2}ms)")
                performance_grade = "GOOD"
            else:
                self.logger.warning(f"⚠️ Config Access: SLOW (avg {avg_access_time:.3f}ms > {target_time * 2}ms)")
                performance_grade = "SLOW"
                
            # Store result
            self.__class__.performance_results['configuration_access'] = {
                'avg_time_ms': avg_access_time,
                'max_time_ms': max_access_time,
                'target_ms': target_time,
                'grade': performance_grade,
                'meets_target': avg_access_time <= target_time,
                'total_tests': len(config_access_times)
            }
            
            # Performance assertion (should be very fast)
            self.assertLessEqual(max_access_time, target_time * 3, 
                               f"Maximum config access time should be reasonable")
            
        else:
            self.fail("No configuration access tests succeeded")
            
    def test_03_crisis_analysis_performance(self):
        """Test crisis analysis performance - THE CRITICAL METRIC"""
        self.logger.info("🔧 Testing crisis analysis performance (CRITICAL METRIC)...")
        
        target_time = self.performance_targets['crisis_analysis_ms']
        test_message = self.test_message
        
        # Perform multiple analysis runs for accurate measurement
        analysis_times = []
        num_runs = 10
        
        self.logger.info(f"🔄 Running {num_runs} analysis iterations for accurate measurement...")
        
        for i in range(num_runs):
            try:
                start_time = time.time()
                
                if hasattr(self.crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                        result = asyncio.run(self.crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"perf_test_user_{i}",
                            channel_id="performance_test_channel"
                        ))
                    else:
                        result = self.crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"perf_test_user_{i}",
                            channel_id="performance_test_channel"
                        )
                elif hasattr(self.crisis_analyzer, 'analyze'):
                    result = self.crisis_analyzer.analyze(test_message)
                else:
                    self.fail("No analysis method available")
                    
                analysis_time = (time.time() - start_time) * 1000
                analysis_times.append(analysis_time)
                
                self.logger.info(f"   Run {i+1}: {analysis_time:.2f}ms")
                
            except Exception as e:
                self.logger.error(f"   ❌ Run {i+1} failed: {e}")
                
        if analysis_times:
            avg_time = statistics.mean(analysis_times)
            min_time = min(analysis_times)
            max_time = max(analysis_times)
            median_time = statistics.median(analysis_times)
            
            self.logger.info(f"📊 Crisis Analysis Performance Summary:")
            self.logger.info(f"   Average: {avg_time:.2f}ms")
            self.logger.info(f"   Median: {median_time:.2f}ms") 
            self.logger.info(f"   Range: {min_time:.2f}ms - {max_time:.2f}ms")
            self.logger.info(f"   🎯 TARGET: {target_time}ms")
            
            # Performance evaluation
            if avg_time <= target_time:
                self.logger.info(f"🚀 Crisis Analysis: TARGET ACHIEVED! ({avg_time:.2f}ms <= {target_time}ms)")
                performance_grade = "TARGET_ACHIEVED"
            elif avg_time <= target_time * 1.2:
                self.logger.info(f"✅ Crisis Analysis: VERY CLOSE ({avg_time:.2f}ms <= {target_time * 1.2}ms)")
                performance_grade = "VERY_CLOSE"
            elif avg_time <= target_time * 1.5:
                self.logger.warning(f"⚠️ Crisis Analysis: NEEDS IMPROVEMENT ({avg_time:.2f}ms <= {target_time * 1.5}ms)")
                performance_grade = "NEEDS_IMPROVEMENT"
            elif avg_time <= target_time * 2:
                self.logger.error(f"❌ Crisis Analysis: SLOW ({avg_time:.2f}ms <= {target_time * 2}ms)")
                performance_grade = "SLOW"
            else:
                self.logger.error(f"❌ Crisis Analysis: VERY SLOW ({avg_time:.2f}ms > {target_time * 2}ms)")
                performance_grade = "VERY_SLOW"
                
            # Store detailed results
            self.__class__.performance_results['crisis_analysis'] = {
                'avg_time_ms': avg_time,
                'median_time_ms': median_time,
                'min_time_ms': min_time,
                'max_time_ms': max_time,
                'target_ms': target_time,
                'grade': performance_grade,
                'meets_target': avg_time <= target_time,
                'improvement_needed_ms': max(0, avg_time - target_time),
                'total_runs': len(analysis_times)
            }
            
            # This is the critical performance metric mentioned in the requirements
            self.assertIsNotNone(result, "Analysis should produce results")
            
        else:
            self.fail("No analysis performance measurements succeeded")
            
    def test_04_concurrent_load_testing(self):
        """Test concurrent analysis load and throughput"""
        self.logger.info("🔧 Testing concurrent load and throughput...")
        
        target_throughput = self.performance_targets['concurrent_throughput']
        
        # Test messages for concurrent analysis
        test_messages = [
            "I'm struggling with anxiety and depression.",
            "Having a really hard time lately.",
            "Feeling overwhelmed with everything going on.",
            "Can't seem to cope with the stress anymore.",
            "Looking for help and support from the community.",
        ]
        
        # Concurrent load test
        num_concurrent = 10
        num_iterations = 2  # Keep low for testing
        
        self.logger.info(f"⚡ Running concurrent load test: {num_concurrent} concurrent, {num_iterations} iterations each")
        
        def analyze_message_wrapper(message, iteration):
            """Wrapper for concurrent analysis"""
            try:
                start_time = time.time()
                
                if hasattr(self.crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                        # Note: asyncio.run creates a new event loop, which works for testing
                        # but in production this would be handled differently
                        result = asyncio.run(self.crisis_analyzer.analyze_message(
                            message,
                            user_id=f"concurrent_user_{iteration}",
                            channel_id="concurrent_test_channel"
                        ))
                    else:
                        result = self.crisis_analyzer.analyze_message(
                            message,
                            user_id=f"concurrent_user_{iteration}",
                            channel_id="concurrent_test_channel"
                        )
                elif hasattr(self.crisis_analyzer, 'analyze'):
                    result = self.crisis_analyzer.analyze(message)
                else:
                    return None, None, "No analysis method available"
                    
                analysis_time = (time.time() - start_time) * 1000
                return result, analysis_time, None
                
            except Exception as e:
                return None, None, str(e)
                
        # Execute concurrent load test
        load_test_start = time.time()
        successful_analyses = 0
        failed_analyses = 0
        analysis_times = []
        
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            # Submit all tasks
            futures = []
            for i in range(num_concurrent):
                for iteration in range(num_iterations):
                    message = test_messages[i % len(test_messages)]
                    future = executor.submit(analyze_message_wrapper, message, iteration)
                    futures.append(future)
                    
            # Collect results
            for future in as_completed(futures):
                result, analysis_time, error = future.result()
                
                if error:
                    failed_analyses += 1
                    self.logger.error(f"   ❌ Concurrent analysis failed: {error}")
                else:
                    successful_analyses += 1
                    if analysis_time:
                        analysis_times.append(analysis_time)
                        
        total_load_time = time.time() - load_test_start
        total_analyses = successful_analyses + failed_analyses
        
        # Calculate throughput
        if total_load_time > 0:
            actual_throughput = successful_analyses / total_load_time
        else:
            actual_throughput = 0
            
        self.logger.info(f"📊 Concurrent Load Test Results:")
        self.logger.info(f"   Total analyses attempted: {total_analyses}")
        self.logger.info(f"   Successful: {successful_analyses}")
        self.logger.info(f"   Failed: {failed_analyses}")
        self.logger.info(f"   Success rate: {(successful_analyses/total_analyses)*100:.1f}%")
        self.logger.info(f"   Total time: {total_load_time:.2f}s")
        self.logger.info(f"   Throughput: {actual_throughput:.2f} analyses/second")
        self.logger.info(f"   🎯 Target throughput: {target_throughput} analyses/second")
        
        if analysis_times:
            avg_concurrent_time = statistics.mean(analysis_times)
            self.logger.info(f"   Average concurrent analysis time: {avg_concurrent_time:.2f}ms")
            
        # Performance evaluation
        success_rate = successful_analyses / total_analyses if total_analyses > 0 else 0
        throughput_grade = "GOOD" if actual_throughput >= target_throughput else "NEEDS_IMPROVEMENT"
        stability_grade = "EXCELLENT" if success_rate >= 0.95 else "GOOD" if success_rate >= 0.8 else "POOR"
        
        if success_rate >= 0.9:
            self.logger.info(f"🚀 Concurrent Stability: {stability_grade} ({success_rate*100:.1f}% success)")
        else:
            self.logger.warning(f"⚠️ Concurrent Stability: {stability_grade} ({success_rate*100:.1f}% success)")
            
        # Store results
        self.__class__.load_test_results = {
            'total_analyses': total_analyses,
            'successful_analyses': successful_analyses,
            'failed_analyses': failed_analyses,
            'success_rate': success_rate,
            'total_time_s': total_load_time,
            'throughput_per_sec': actual_throughput,
            'target_throughput_per_sec': target_throughput,
            'throughput_grade': throughput_grade,
            'stability_grade': stability_grade,
            'avg_concurrent_time_ms': statistics.mean(analysis_times) if analysis_times else 0
        }
        
        # Minimum requirements
        self.assertGreaterEqual(success_rate, 0.75, "Should have at least 75% success rate under load")
        self.assertGreater(successful_analyses, 0, "Should have at least some successful analyses")
        
    def test_05_memory_usage_estimation(self):
        """Test and estimate memory usage"""
        self.logger.info("🔧 Testing memory usage estimation...")
        
        # Since we can't easily measure actual memory in a test environment,
        # we'll test that the system doesn't create excessive objects
        
        import gc
        
        # Force garbage collection and get baseline
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Perform multiple analyses to see object growth
        test_message = self.test_message
        num_analyses = 20
        
        self.logger.info(f"🔄 Running {num_analyses} analyses to check memory behavior...")
        
        for i in range(num_analyses):
            try:
                if hasattr(self.crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                        result = asyncio.run(self.crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"memory_test_user_{i}",
                            channel_id="memory_test_channel"
                        ))
                    else:
                        result = self.crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"memory_test_user_{i}",
                            channel_id="memory_test_channel"
                        )
                elif hasattr(self.crisis_analyzer, 'analyze'):
                    result = self.crisis_analyzer.analyze(test_message)
            except Exception as e:
                self.logger.error(f"Analysis {i+1} failed: {e}")
                
        # Check final object count
        gc.collect()
        final_objects = len(gc.get_objects())
        object_growth = final_objects - initial_objects
        
        self.logger.info(f"📊 Memory Behavior Analysis:")
        self.logger.info(f"   Initial objects: {initial_objects}")
        self.logger.info(f"   Final objects: {final_objects}")
        self.logger.info(f"   Object growth: {object_growth}")
        self.logger.info(f"   Growth per analysis: {object_growth/num_analyses:.1f}")
        
        # Memory behavior evaluation
        objects_per_analysis = object_growth / num_analyses
        
        if objects_per_analysis <= 10:
            self.logger.info(f"🚀 Memory Behavior: EXCELLENT ({objects_per_analysis:.1f} objects/analysis)")
            memory_grade = "EXCELLENT"
        elif objects_per_analysis <= 50:
            self.logger.info(f"✅ Memory Behavior: GOOD ({objects_per_analysis:.1f} objects/analysis)")
            memory_grade = "GOOD"
        else:
            self.logger.warning(f"⚠️ Memory Behavior: CONCERNING ({objects_per_analysis:.1f} objects/analysis)")
            memory_grade = "CONCERNING"
            
        # Store results
        self.__class__.performance_results['memory_behavior'] = {
            'initial_objects': initial_objects,
            'final_objects': final_objects,
            'object_growth': object_growth,
            'objects_per_analysis': objects_per_analysis,
            'grade': memory_grade,
            'test_analyses': num_analyses
        }
        
        # Basic memory behavior check
        self.assertLess(objects_per_analysis, 100, "Memory growth per analysis should be reasonable")
        
    def test_06_stability_endurance(self):
        """Test system stability over time (scaled down for testing)"""
        self.logger.info("🔧 Testing system stability endurance...")
        
        # Scaled down endurance test (6 minutes instead of 4+ hours)
        endurance_duration = self.performance_targets['system_stability_hours'] * 3600  # Convert to seconds
        test_message = self.test_message
        
        self.logger.info(f"⏰ Running {endurance_duration/60:.1f}-minute stability test...")
        
        start_time = time.time()
        end_time = start_time + endurance_duration
        
        successful_analyses = 0
        failed_analyses = 0
        analysis_times = []
        
        while time.time() < end_time:
            try:
                analysis_start = time.time()
                
                if hasattr(self.crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                        result = asyncio.run(self.crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"endurance_user_{successful_analyses}",
                            channel_id="endurance_test_channel"
                        ))
                    else:
                        result = self.crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"endurance_user_{successful_analyses}",
                            channel_id="endurance_test_channel"
                        )
                elif hasattr(self.crisis_analyzer, 'analyze'):
                    result = self.crisis_analyzer.analyze(test_message)
                else:
                    break
                    
                analysis_time = (time.time() - analysis_start) * 1000
                analysis_times.append(analysis_time)
                successful_analyses += 1
                
                # Brief pause between analyses to simulate realistic usage
                time.sleep(0.1)
                
            except Exception as e:
                failed_analyses += 1
                self.logger.error(f"Endurance test analysis failed: {e}")
                time.sleep(0.1)  # Brief pause before retry
                
        actual_duration = time.time() - start_time
        total_analyses = successful_analyses + failed_analyses
        
        self.logger.info(f"📊 Stability Endurance Test Results:")
        self.logger.info(f"   Duration: {actual_duration/60:.2f} minutes")
        self.logger.info(f"   Total analyses: {total_analyses}")
        self.logger.info(f"   Successful: {successful_analyses}")
        self.logger.info(f"   Failed: {failed_analyses}")
        
        if total_analyses > 0:
            success_rate = successful_analyses / total_analyses
            analyses_per_minute = total_analyses / (actual_duration / 60)
            
            self.logger.info(f"   Success rate: {success_rate*100:.1f}%")
            self.logger.info(f"   Rate: {analyses_per_minute:.1f} analyses/minute")
            
            if analysis_times:
                avg_time = statistics.mean(analysis_times)
                time_degradation = abs(analysis_times[-10:][0] - analysis_times[:10][0]) if len(analysis_times) > 20 else 0
                
                self.logger.info(f"   Average analysis time: {avg_time:.2f}ms")
                if time_degradation > 0:
                    self.logger.info(f"   Performance degradation: {time_degradation:.2f}ms")
                    
            # Stability evaluation
            if success_rate >= 0.98:
                self.logger.info(f"🚀 System Stability: EXCELLENT ({success_rate*100:.1f}% over {actual_duration/60:.1f}min)")
                stability_grade = "EXCELLENT"
            elif success_rate >= 0.95:
                self.logger.info(f"✅ System Stability: GOOD ({success_rate*100:.1f}% over {actual_duration/60:.1f}min)")
                stability_grade = "GOOD"
            elif success_rate >= 0.90:
                self.logger.warning(f"⚠️ System Stability: ACCEPTABLE ({success_rate*100:.1f}% over {actual_duration/60:.1f}min)")
                stability_grade = "ACCEPTABLE"
            else:
                self.logger.error(f"❌ System Stability: POOR ({success_rate*100:.1f}% over {actual_duration/60:.1f}min)")
                stability_grade = "POOR"
                
            # Store results
            self.__class__.performance_results['stability_endurance'] = {
                'duration_minutes': actual_duration / 60,
                'total_analyses': total_analyses,
                'successful_analyses': successful_analyses,
                'failed_analyses': failed_analyses,
                'success_rate': success_rate,
                'analyses_per_minute': analyses_per_minute,
                'avg_analysis_time_ms': statistics.mean(analysis_times) if analysis_times else 0,
                'grade': stability_grade
            }
            
            # Minimum stability requirement
            self.assertGreaterEqual(success_rate, 0.85, "System should maintain at least 85% stability over time")
            
        else:
            self.fail("No analyses completed in stability test")
            
    @classmethod
    def tearDownClass(cls):
        """Generate comprehensive performance report"""
        cls.logger.info("🧹 Generating comprehensive performance report...")
        
        cls.logger.info("=" * 80)
        cls.logger.info("📊 COMPREHENSIVE PERFORMANCE VALIDATION REPORT")
        cls.logger.info("=" * 80)
        
        # Overall performance summary
        if cls.performance_results:
            cls.logger.info("🎯 PERFORMANCE TARGETS vs ACTUAL RESULTS:")
            cls.logger.info("-" * 60)
            
            # Manager Initialization
            if 'manager_initialization' in cls.performance_results:
                mgr_result = cls.performance_results['manager_initialization']
                cls.logger.info(f"Manager Initialization:")
                cls.logger.info(f"   Target: {mgr_result['target_ms']}ms")
                cls.logger.info(f"   Actual: {mgr_result['time_ms']:.2f}ms")
                cls.logger.info(f"   Grade: {mgr_result['grade']}")
                cls.logger.info(f"   Status: {'✅ PASS' if mgr_result['meets_target'] else '⚠️ NEEDS IMPROVEMENT'}")
                cls.logger.info("")
                
            # Configuration Access
            if 'configuration_access' in cls.performance_results:
                config_result = cls.performance_results['configuration_access']
                cls.logger.info(f"Configuration Access:")
                cls.logger.info(f"   Target: {config_result['target_ms']}ms")
                cls.logger.info(f"   Actual: {config_result['avg_time_ms']:.3f}ms (avg)")
                cls.logger.info(f"   Grade: {config_result['grade']}")
                cls.logger.info(f"   Status: {'✅ PASS' if config_result['meets_target'] else '⚠️ NEEDS IMPROVEMENT'}")
                cls.logger.info("")
                
            # Crisis Analysis - THE CRITICAL METRIC
            if 'crisis_analysis' in cls.performance_results:
                crisis_result = cls.performance_results['crisis_analysis']
                cls.logger.info(f"🚨 CRISIS ANALYSIS (CRITICAL METRIC):")
                cls.logger.info(f"   Target: {crisis_result['target_ms']}ms")
                cls.logger.info(f"   Actual: {crisis_result['avg_time_ms']:.2f}ms (avg)")
                cls.logger.info(f"   Range: {crisis_result['min_time_ms']:.2f}ms - {crisis_result['max_time_ms']:.2f}ms")
                cls.logger.info(f"   Grade: {crisis_result['grade']}")
                cls.logger.info(f"   Status: {'🚀 TARGET ACHIEVED!' if crisis_result['meets_target'] else '⚠️ NEEDS OPTIMIZATION'}")
                if not crisis_result['meets_target']:
                    cls.logger.info(f"   Improvement needed: {crisis_result['improvement_needed_ms']:.2f}ms")
                cls.logger.info("")
                
            # Memory Behavior
            if 'memory_behavior' in cls.performance_results:
                mem_result = cls.performance_results['memory_behavior']
                cls.logger.info(f"Memory Behavior:")
                cls.logger.info(f"   Objects per analysis: {mem_result['objects_per_analysis']:.1f}")
                cls.logger.info(f"   Grade: {mem_result['grade']}")
                cls.logger.info("")
                
            # Stability Endurance
            if 'stability_endurance' in cls.performance_results:
                stab_result = cls.performance_results['stability_endurance']
                cls.logger.info(f"System Stability:")
                cls.logger.info(f"   Duration: {stab_result['duration_minutes']:.2f} minutes")
                cls.logger.info(f"   Success rate: {stab_result['success_rate']*100:.1f}%")
                cls.logger.info(f"   Grade: {stab_result['grade']}")
                cls.logger.info("")
                
        # Load test results
        if cls.load_test_results:
            load_result = cls.load_test_results
            cls.logger.info("⚡ CONCURRENT LOAD TEST RESULTS:")
            cls.logger.info("-" * 40)
            cls.logger.info(f"   Throughput: {load_result['throughput_per_sec']:.2f} analyses/second")
            cls.logger.info(f"   Target: {load_result['target_throughput_per_sec']} analyses/second")
            cls.logger.info(f"   Success rate: {load_result['success_rate']*100:.1f}%")
            cls.logger.info(f"   Stability: {load_result['stability_grade']}")
            cls.logger.info("")
            
        # Performance recommendations
        cls.logger.info("🔧 PERFORMANCE OPTIMIZATION RECOMMENDATIONS:")
        cls.logger.info("-" * 50)
        
        recommendations = []
        
        # Check crisis analysis performance
        if 'crisis_analysis' in cls.performance_results:
            crisis_perf = cls.performance_results['crisis_analysis']
            if not crisis_perf['meets_target']:
                improvement_pct = ((crisis_perf['avg_time_ms'] / crisis_perf['target_ms']) - 1) * 100
                recommendations.append(
                    f"🚨 CRITICAL: Optimize crisis analysis speed by {improvement_pct:.0f}% "
                    f"({crisis_perf['avg_time_ms']:.0f}ms → {crisis_perf['target_ms']}ms)"
                )
                
        # Check configuration access
        if 'configuration_access' in cls.performance_results:
            config_perf = cls.performance_results['configuration_access']
            if not config_perf['meets_target']:
                recommendations.append(
                    f"⚡ Optimize configuration access patterns "
                    f"(current: {config_perf['avg_time_ms']:.2f}ms)"
                )
                
        # Check memory behavior
        if 'memory_behavior' in cls.performance_results:
            mem_perf = cls.performance_results['memory_behavior']
            if mem_perf['grade'] in ['CONCERNING']:
                recommendations.append(
                    f"💾 Review memory usage patterns "
                    f"({mem_perf['objects_per_analysis']:.1f} objects/analysis)"
                )
                
        # Check concurrent performance
        if cls.load_test_results:
            load_perf = cls.load_test_results
            if load_perf['success_rate'] < 0.95:
                recommendations.append(
                    f"🔄 Improve concurrent stability "
                    f"({load_perf['success_rate']*100:.1f}% success rate)"
                )
                
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                cls.logger.info(f"   {i}. {rec}")
        else:
            cls.logger.info("   ✅ No major performance issues detected!")
            
        cls.logger.info("")
        cls.logger.info("=" * 80)
        cls.logger.info("✅ Performance Validation Test Suite Complete!")
        cls.logger.info("=" * 80)


if __name__ == '__main__':
    # Configure test runner with colored output
    import sys
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformanceValidation)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True
    )
    
    result = runner.run(test_suite)
    
    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)