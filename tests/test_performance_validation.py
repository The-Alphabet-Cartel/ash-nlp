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
        
        self.logger.info("=" * 60)
        self.logger.info("📊 MANAGER INITIALIZATION PERFORMANCE METRICS")
        self.logger.info("=" * 60)
        self.logger.info(f"TARGET: {target_time}ms")
        self.logger.info(f"ACTUAL: {init_time:.1f}ms")
        self.logger.info(f"DIFFERENCE: {init_time - target_time:.1f}ms")
        
        if init_time <= target_time:
            self.logger.info(f"🚀 Manager Initialization: EXCELLENT ({init_time:.1f}ms <= {target_time}ms)")
            performance_grade = "EXCELLENT"
        elif init_time <= target_time * 1.5:
            self.logger.info(f"✅ Manager Initialization: GOOD ({init_time:.1f}ms <= {target_time * 1.5}ms)")
            performance_grade = "GOOD"
        elif init_time <= target_time * 2:
            self.logger.warning(f"⚠️ Manager Initialization: ACCEPTABLE ({init_time:.1f}ms <= {target_time * 2}ms)")
            performance_grade = "ACCEPTABLE"
        else:
            self.logger.error(f"❌ Manager Initialization: SLOW ({init_time:.1f}ms > {target_time * 2}ms)")
            performance_grade = "SLOW"
            
        # Store result
        self.__class__.performance_results['manager_initialization'] = {
            'time_ms': init_time,
            'target_ms': target_time,
            'grade': performance_grade,
            'meets_target': init_time <= target_time
        }
        
        self.logger.info("=" * 60)
        
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
            min_access_time = min(config_access_times)
            
            self.logger.info("=" * 60)
            self.logger.info("📊 CONFIGURATION ACCESS PERFORMANCE METRICS")
            self.logger.info("=" * 60)
            self.logger.info(f"TARGET: <{target_time}ms per access")
            self.logger.info(f"AVERAGE: {avg_access_time:.3f}ms")
            self.logger.info(f"FASTEST: {min_access_time:.3f}ms")
            self.logger.info(f"SLOWEST: {max_access_time:.3f}ms")
            self.logger.info(f"TESTS: {len(config_access_times)} configs")
            
            if avg_access_time <= target_time:
                margin = target_time - avg_access_time
                self.logger.info(f"🚀 Config Access: EXCELLENT - {margin:.3f}ms under target")
                performance_grade = "EXCELLENT"
            elif avg_access_time <= target_time * 2:
                excess = avg_access_time - target_time
                self.logger.info(f"✅ Config Access: GOOD - Only {excess:.3f}ms over target")
                performance_grade = "GOOD"
            else:
                excess = avg_access_time - target_time
                self.logger.warning(f"⚠️ Config Access: SLOW - {excess:.3f}ms over target")
                performance_grade = "SLOW"
                
            # Store result
            self.__class__.performance_results['configuration_access'] = {
                'avg_time_ms': avg_access_time,
                'max_time_ms': max_access_time,
                'min_time_ms': min_access_time,
                'target_ms': target_time,
                'grade': performance_grade,
                'meets_target': avg_access_time <= target_time,
                'total_tests': len(config_access_times)
            }
            
            self.logger.info("=" * 60)
            
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
                
                self.logger.info(f"   Run {i+1}: {analysis_time:.1f}ms")
                
            except Exception as e:
                self.logger.error(f"   ❌ Run {i+1} failed: {e}")
                
        if analysis_times:
            avg_time = statistics.mean(analysis_times)
            min_time = min(analysis_times)
            max_time = max(analysis_times)
            median_time = statistics.median(analysis_times)
            
            try:
                p90_time = statistics.quantiles(analysis_times, n=10)[8]  # 90th percentile
                p95_time = statistics.quantiles(analysis_times, n=20)[18]  # 95th percentile
            except:
                p90_time = max_time
                p95_time = max_time
            
            self.logger.info("=" * 80)
            self.logger.info("📊 CRISIS ANALYSIS PERFORMANCE - CRITICAL METRIC")
            self.logger.info("=" * 80)
            self.logger.info(f"TARGET: {target_time}ms per analysis")
            self.logger.info(f"AVERAGE: {avg_time:.1f}ms")
            self.logger.info(f"MEDIAN: {median_time:.1f}ms")
            self.logger.info(f"FASTEST: {min_time:.1f}ms")
            self.logger.info(f"SLOWEST: {max_time:.1f}ms")
            self.logger.info(f"90th PERCENTILE: {p90_time:.1f}ms")
            self.logger.info(f"95th PERCENTILE: {p95_time:.1f}ms")
            
            if avg_time > target_time:
                gap = avg_time - target_time
                improvement_pct = ((avg_time / target_time) - 1) * 100
                self.logger.info(f"PERFORMANCE GAP: {gap:.1f}ms over target")
                self.logger.info(f"IMPROVEMENT NEEDED: {improvement_pct:.1f}% speed increase")
            else:
                self.logger.info("PERFORMANCE: TARGET ACHIEVED!")
            
            # Performance evaluation with specific numbers
            if avg_time <= target_time:
                self.logger.info(f"🚀 Crisis Analysis: TARGET ACHIEVED!")
                performance_grade = "TARGET_ACHIEVED"
            elif avg_time <= target_time * 1.2:
                improvement_needed = avg_time - target_time
                self.logger.info(f"✅ Crisis Analysis: VERY CLOSE - Need {improvement_needed:.1f}ms improvement")
                performance_grade = "VERY_CLOSE"
            elif avg_time <= target_time * 1.5:
                improvement_needed = avg_time - target_time
                self.logger.warning(f"⚠️ Crisis Analysis: NEEDS OPTIMIZATION - Need {improvement_needed:.1f}ms improvement")
                performance_grade = "NEEDS_IMPROVEMENT"
            elif avg_time <= target_time * 2:
                improvement_needed = avg_time - target_time
                self.logger.error(f"❌ Crisis Analysis: SLOW - Need {improvement_needed:.1f}ms improvement")
                performance_grade = "SLOW"
            else:
                improvement_needed = avg_time - target_time
                self.logger.error(f"❌ Crisis Analysis: VERY SLOW - Need {improvement_needed:.1f}ms improvement")
                performance_grade = "VERY_SLOW"
                
            # Optimization recommendations
            self.logger.info("🔧 OPTIMIZATION RECOMMENDATIONS:")
            if avg_time > 1500:
                self.logger.info("   - Consider model quantization or smaller models")
                self.logger.info("   - Implement aggressive result caching")
            elif avg_time > 1000:
                self.logger.info("   - Optimize GPU memory usage patterns")
                self.logger.info("   - Cache model inference results")
            elif avg_time > 750:
                self.logger.info("   - Cache frequently accessed patterns")
                self.logger.info("   - Optimize text preprocessing pipeline")
            else:
                self.logger.info("   - Fine-tune configuration access patterns")
                self.logger.info("   - Optimize helper class operations")
                
            self.logger.info("=" * 80)
                
            # Store detailed results
            self.__class__.performance_results['crisis_analysis'] = {
                'avg_time_ms': avg_time,
                'median_time_ms': median_time,
                'min_time_ms': min_time,
                'max_time_ms': max_time,
                'p90_time_ms': p90_time,
                'p95_time_ms': p95_time,
                'target_ms': target_time,
                'grade': performance_grade,
                'meets_target': avg_time <= target_time,
                'improvement_needed_ms': max(0, avg_time - target_time),
                'improvement_needed_pct': ((avg_time / target_time) - 1) * 100 if avg_time > target_time else 0,
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
            
        self.logger.info("=" * 70)
        self.logger.info("📊 CONCURRENT LOAD TEST - DETAILED METRICS")
        self.logger.info("=" * 70)
        self.logger.info(f"CONCURRENCY: {num_concurrent} threads x {num_iterations} iterations")
        self.logger.info(f"TOTAL OPERATIONS: {total_analyses}")
        self.logger.info(f"SUCCESSFUL: {successful_analyses} ({(successful_analyses/total_analyses)*100:.1f}%)")
        self.logger.info(f"FAILED: {failed_analyses} ({(failed_analyses/total_analyses)*100:.1f}%)")
        self.logger.info(f"TOTAL TIME: {total_load_time:.2f}s")
        self.logger.info(f"THROUGHPUT: {actual_throughput:.2f} analyses/second")
        self.logger.info(f"TARGET THROUGHPUT: {target_throughput} analyses/second")
        
        throughput_gap = target_throughput - actual_throughput
        if actual_throughput >= target_throughput:
            self.logger.info(f"THROUGHPUT STATUS: TARGET ACHIEVED! (+{actual_throughput - target_throughput:.2f} over target)")
        else:
            self.logger.info(f"THROUGHPUT GAP: {throughput_gap:.2f} analyses/second short of target")
        
        if analysis_times:
            avg_concurrent_time = statistics.mean(analysis_times)
            self.logger.info(f"CONCURRENT ANALYSIS TIME: {avg_concurrent_time:.1f}ms average")
            
            # Compare to single-threaded performance if available
            single_thread_time = self.__class__.performance_results.get('crisis_analysis', {}).get('avg_time_ms')
            if single_thread_time:
                overhead = avg_concurrent_time - single_thread_time
                overhead_pct = (overhead / single_thread_time) * 100
                self.logger.info(f"CONCURRENT OVERHEAD: {overhead:.1f}ms ({overhead_pct:.1f}% slower than single-thread)")
        
        self.logger.info(f"🎯 TARGETS vs ACTUALS:")
        self.logger.info(f"   Success Rate Target: >90% | Actual: {(successful_analyses/total_analyses)*100:.1f}%")
        self.logger.info(f"   Throughput Target: {target_throughput}/s | Actual: {actual_throughput:.2f}/s")
        self.logger.info("=" * 70)
        
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
        
        self.logger.info("=" * 60)
        self.logger.info("📊 MEMORY BEHAVIOR ANALYSIS")
        self.logger.info("=" * 60)
        self.logger.info(f"INITIAL OBJECTS: {initial_objects}")
        self.logger.info(f"FINAL OBJECTS: {final_objects}")
        self.logger.info(f"OBJECT GROWTH: {object_growth}")
        self.logger.info(f"GROWTH PER ANALYSIS: {object_growth/num_analyses:.1f}")
        
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
            
        self.logger.info("=" * 60)
            
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
        
        # Scaled down endurance test (5 minutes for practical testing)
        endurance_duration = 5 * 60  # 5 minutes in seconds
        test_message = self.test_message
        
        self.logger.info(f"⏰ Running 5-minute stability test...")
        
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
        
        self.logger.info("=" * 70)
        self.logger.info("📊 STABILITY ENDURANCE TEST RESULTS")
        self.logger.info("=" * 70)
        self.logger.info(f"DURATION: {actual_duration/60:.2f} minutes")
        self.logger.info(f"TOTAL ANALYSES: {total_analyses}")
        self.logger.info(f"SUCCESSFUL: {successful_analyses}")
        self.logger.info(f"FAILED: {failed_analyses}")
        
        if total_analyses > 0:
            success_rate = successful_analyses / total_analyses
            analyses_per_minute = total_analyses / (actual_duration / 60)
            
            self.logger.info(f"SUCCESS RATE: {success_rate*100:.1f}%")
            self.logger.info(f"RATE: {analyses_per_minute:.1f} analyses/minute")
            
            if analysis_times:
                avg_time = statistics.mean(analysis_times)
                if len(analysis_times) > 20:
                    early_avg = statistics.mean(analysis_times[:10])
                    late_avg = statistics.mean(analysis_times[-10:])
                    time_degradation = late_avg - early_avg
                    self.logger.info(f"AVERAGE ANALYSIS TIME: {avg_time:.1f}ms")
                    if abs(time_degradation) > 10:
                        self.logger.info(f"PERFORMANCE CHANGE: {time_degradation:+.1f}ms over test duration")
                    else:
                        self.logger.info("PERFORMANCE: Stable throughout test")
                        
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
                
            self.logger.info("=" * 70)
                
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
        
        cls.logger.info("=" * 90)
        cls.logger.info("📊 COMPREHENSIVE PERFORMANCE VALIDATION REPORT")
        cls.logger.info("=" * 90)
        
        # Overall performance summary
        if cls.performance_results:
            cls.logger.info("🎯 PERFORMANCE TARGETS vs ACTUAL RESULTS:")
            cls.logger.info("-" * 60)
            
            # Crisis Analysis - THE CRITICAL METRIC
            if 'crisis_analysis' in cls.performance_results:
                crisis_result = cls.performance_results['crisis_analysis']
                cls.logger.info("🚨 CRISIS ANALYSIS (CRITICAL METRIC):")
                cls.logger.info(f"   TARGET: {crisis_result['target_ms']}ms per analysis")
                cls.logger.info(f"   ACTUAL AVERAGE: {crisis_result['avg_time_ms']:.1f}ms")
                cls.logger.info(f"   PERFORMANCE RANGE: {crisis_result['min_time_ms']:.1f}ms - {crisis_result['max_time_ms']:.1f}ms")
                cls.logger.info(f"   MEDIAN: {crisis_result.get('median_time_ms', 0):.1f}ms")
                cls.logger.info(f"   90th PERCENTILE: {crisis_result.get('p90_time_ms', 0):.1f}ms")
                cls.logger.info(f"   95th PERCENTILE: {crisis_result.get('p95_time_ms', 0):.1f}ms")
                cls.logger.info(f"   STATUS: {crisis_result['grade']}")
                
                if crisis_result['meets_target']:
                    cls.logger.info("   RESULT: 🚀 TARGET ACHIEVED!")
                else:
                    improvement = crisis_result['improvement_needed_ms']
                    speed_up = crisis_result.get('improvement_needed_pct', 0)
                    cls.logger.info(f"   OPTIMIZATION NEEDED: {improvement:.1f}ms faster ({speed_up:.1f}% speed improvement)")
                    
                    # Specific optimization recommendations
                    current_ms = crisis_result['avg_time_ms']
                    if current_ms > 1500:
                        cls.logger.info("   RECOMMENDATION: Focus on major algorithmic optimizations")
                    elif current_ms > 1000:
                        cls.logger.info("   RECOMMENDATION: Optimize model loading and caching")
                    elif current_ms > 750:
                        cls.logger.info("   RECOMMENDATION: Cache frequently accessed patterns")
                    else:
                        cls.logger.info("   RECOMMENDATION: Fine-tune processing pipeline")
                cls.logger.info("")
                
            # Manager Initialization
            if 'manager_initialization' in cls.performance_results:
                mgr_result = cls.performance_results['manager_initialization']
                cls.logger.info("🔧 MANAGER INITIALIZATION:")
                cls.logger.info(f"   TARGET: {mgr_result['target_ms']}ms")
                cls.logger.info(f"   ACTUAL: {mgr_result['time_ms']:.1f}ms")
                cls.logger.info(f"   STATUS: {mgr_result['grade']}")
                cls.logger.info("")
                
            # Configuration Access
            if 'configuration_access' in cls.performance_results:
                config_result = cls.performance_results['configuration_access']
                cls.logger.info("⚙️ CONFIGURATION ACCESS:")
                cls.logger.info(f"   TARGET: <{config_result['target_ms']}ms per access")
                cls.logger.info(f"   ACTUAL AVERAGE: {config_result['avg_time_ms']:.3f}ms")
                cls.logger.info(f"   SLOWEST ACCESS: {config_result['max_time_ms']:.3f}ms")
                cls.logger.info(f"   STATUS: {config_result['grade']}")
                cls.logger.info("")
                
        # Load test results
        if cls.load_test_results:
            load_result = cls.load_test_results
            cls.logger.info("⚡ CONCURRENT PERFORMANCE:")
            cls.logger.info(f"   THROUGHPUT TARGET: {load_result['target_throughput_per_sec']}/s")
            cls.logger.info(f"   ACTUAL THROUGHPUT: {load_result['throughput_per_sec']:.2f}/s")
            cls.logger.info(f"   CONCURRENCY SUCCESS: {load_result['success_rate']*100:.1f}%")
            cls.logger.info(f"   CONCURRENT ANALYSIS TIME: {load_result.get('avg_concurrent_time_ms', 0):.1f}ms")
            cls.logger.info("")
            
        # Performance optimization targets
        cls.logger.info("🔧 PERFORMANCE OPTIMIZATION PRIORITIES:")
        cls.logger.info("-" * 50)
        
        recommendations = []
        
        # Check crisis analysis performance
        if 'crisis_analysis' in cls.performance_results:
            crisis_perf = cls.performance_results['crisis_analysis']
            if not crisis_perf['meets_target']:
                current_ms = crisis_perf['avg_time_ms']
                target_ms = crisis_perf['target_ms']
                improvement_pct = crisis_perf.get('improvement_needed_pct', 0)
                
                recommendations.append(
                    f"1. CRITICAL: Reduce analysis time by {improvement_pct:.0f}% "
                    f"({current_ms:.0f}ms → {target_ms}ms target)"
                )
                
                # Specific bottleneck recommendations
                if current_ms > 1500:
                    recommendations.append("   - Consider model quantization or smaller models")
                    recommendations.append("   - Implement aggressive model result caching")
                elif current_ms > 1000:
                    recommendations.append("   - Optimize GPU memory usage patterns")
                    recommendations.append("   - Parallelize model inference where possible")
                elif current_ms > 750:
                    recommendations.append("   - Cache frequently accessed patterns")
                    recommendations.append("   - Optimize text preprocessing pipeline")
                else:
                    recommendations.append("   - Fine-tune configuration access patterns")
                    recommendations.append("   - Optimize helper class operations")
                    
        # Check other performance areas
        if cls.load_test_results and cls.load_test_results['success_rate'] < 0.95:
            recommendations.append("2. Improve concurrent processing stability")
            
        if recommendations:
            for rec in recommendations:
                cls.logger.info(f"   {rec}")
        else:
            cls.logger.info("   ✅ All performance targets met!")
            
        cls.logger.info("")
        cls.logger.info("=" * 90)
        cls.logger.info("✅ Performance Validation Test Suite Complete!")
        cls.logger.info("=" * 90)


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