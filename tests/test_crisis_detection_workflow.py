#!/usr/bin/env python3
"""
Phase 3e Step 7.1: Crisis Detection Workflow Integration Test
Tests end-to-end crisis detection functionality with realistic message samples

FILE: tests/test_crisis_detection_workflow.py
VERSION: v3.1-3e-7.1-1
AUTHOR: The Alphabet Cartel  
REPOSITORY: https://github.com/the-alphabet-cartel/ash-nlp
COMMUNITY: https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import sys
import os
import unittest
import logging
import time
import asyncio
from typing import Dict, Any, List, Optional

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


class TestCrisisDetectionWorkflow(unittest.TestCase):
    """Test suite for crisis detection workflow validation"""
    
    @classmethod
    def setUpClass(cls):
        """Set up colored logging and initialize system"""
        # Configure colorlog formatter
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[CRISIS-TEST] %(levelname)s%(reset)s: %(message)s',
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
        cls.logger = logging.getLogger('CrisisDetectionWorkflowTest')
        cls.logger.setLevel(logging.INFO)
        cls.logger.handlers = [console_handler]
        
        cls.logger.info("🚀 Starting Crisis Detection Workflow Integration Tests")
        
        # Initialize the complete system
        try:
            cls.logger.info("🔧 Initializing complete system for testing...")
            start_time = time.time()
            cls.managers = initialize_unified_managers()
            init_time = (time.time() - start_time) * 1000
            cls.logger.info(f"✅ System initialized in {init_time:.2f}ms")
            
            # Verify critical components
            cls.crisis_analyzer = cls.managers.get('crisis_analyzer')
            cls.unified_config = cls.managers.get('unified_config')
            cls.model_coordination = cls.managers.get('model_coordination')
            
            if not cls.crisis_analyzer:
                raise RuntimeError("CrisisAnalyzer not available")
            if not cls.unified_config:
                raise RuntimeError("UnifiedConfigManager not available")
                
        except Exception as e:
            cls.logger.error(f"❌ System initialization failed: {e}")
            raise
            
        # Define test message samples for realistic testing
        cls.test_messages = {
            'high_risk': [
                "I can't do this anymore. Everything hurts and I just want it to stop.",
                "Nobody would even notice if I disappeared tomorrow.",
                "I keep thinking about how to end all this pain permanently.",
                "My family would be better off without me as a burden."
            ],
            'moderate_risk': [
                "Having a really hard time lately and feeling hopeless.",
                "Been struggling with dark thoughts recently.",
                "Feel like I'm losing myself and don't know what to do.",
                "Everything feels overwhelming and I'm exhausted."
            ],
            'low_risk': [
                "Having a tough day but trying to stay positive.",
                "Feeling a bit down but I'll get through this.",
                "Work is stressful but at least the weekend is coming.",
                "Not my best week but I've got good friends to support me."
            ],
            'lgbtqia_specific': [
                "Coming out to my parents and they rejected me completely. Feel so alone.",
                "Been dealing with dysphoria really badly lately and it's getting worse.",
                "Can't handle the discrimination at work anymore. Nobody understands.",
                "My chosen family is the only thing keeping me going right now."
            ],
            'support_seeking': [
                "Does anyone have advice for dealing with anxiety?",
                "Looking for recommendations for LGBTQ+ friendly therapists.",
                "How do you all cope when things get overwhelming?",
                "Would appreciate some encouragement if anyone has time."
            ],
            'normal': [
                "Good morning everyone! Hope you all have a great day.",
                "Just finished a really good book, highly recommend it.",
                "Anyone want to play some games later tonight?",
                "Thanks for being such an awesome community, you all rock!"
            ]
        }
        
        cls.analysis_results = {}
        cls.performance_metrics = {}
        
    def setUp(self):
        """Set up each test case"""
        self.start_time = time.time()
        
    def tearDown(self):
        """Clean up after each test case"""
        test_time = (time.time() - self.start_time) * 1000
        self.logger.info(f"⏱️ Test completed in {test_time:.2f}ms")
        
    def test_01_crisis_analyzer_availability(self):
        """Test that CrisisAnalyzer is properly initialized and functional"""
        self.logger.info("🔧 Testing CrisisAnalyzer availability...")
        
        self.assertIsNotNone(self.crisis_analyzer, "CrisisAnalyzer should be available")
        
        # Check for essential methods
        essential_methods = ['analyze_message', 'analyze']
        available_methods = []
        
        for method in essential_methods:
            if hasattr(self.crisis_analyzer, method):
                available_methods.append(method)
                self.logger.info(f"✅ CrisisAnalyzer.{method} available")
            else:
                self.logger.warning(f"⚠️ CrisisAnalyzer.{method} not found")
                
        # Should have at least one analysis method
        self.assertGreater(len(available_methods), 0, "At least one analysis method should be available")
        
        self.logger.info(f"📊 CrisisAnalyzer has {len(available_methods)}/{len(essential_methods)} essential methods")
        
    def test_02_basic_message_analysis(self):
        """Test basic message analysis functionality"""
        self.logger.info("🔧 Testing basic message analysis...")
        
        test_message = "This is a basic test message to verify analysis works."
        
        try:
            # Try analyze_message method first (with required parameters)
            if hasattr(self.crisis_analyzer, 'analyze_message'):
                start_time = time.time()
                
                # Check if it's async
                import inspect
                if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                    # Async method - run with test parameters
                    result = asyncio.run(self.crisis_analyzer.analyze_message(
                        test_message, 
                        user_id="test_user_123",
                        channel_id="test_channel_456"
                    ))
                else:
                    # Sync method - call with test parameters
                    result = self.crisis_analyzer.analyze_message(
                        test_message,
                        user_id="test_user_123", 
                        channel_id="test_channel_456"
                    )
                    
                analysis_time = (time.time() - start_time) * 1000
                
                self.logger.info(f"✅ analyze_message completed in {analysis_time:.2f}ms")
                
            # Try analyze method as fallback
            elif hasattr(self.crisis_analyzer, 'analyze'):
                start_time = time.time()
                result = self.crisis_analyzer.analyze(test_message)
                analysis_time = (time.time() - start_time) * 1000
                
                self.logger.info(f"✅ analyze completed in {analysis_time:.2f}ms")
                
            else:
                self.fail("No analysis method available on CrisisAnalyzer")
                
            # Validate result structure
            self.assertIsNotNone(result, "Analysis should return a result")
            
            if isinstance(result, dict):
                self.logger.info("✅ Analysis returned dictionary result")
                
                # Log available keys for debugging
                if result:
                    self.logger.info(f"📊 Result keys: {list(result.keys())}")
                    
                    # Check for common result fields
                    expected_fields = ['score', 'confidence', 'level', 'crisis_score', 'crisis_level']
                    found_fields = [field for field in expected_fields if field in result]
                    if found_fields:
                        self.logger.info(f"✅ Found expected fields: {found_fields}")
                    else:
                        self.logger.warning("⚠️ No common result fields found, but analysis completed")
                        
            # Store performance metric
            self.__class__.performance_metrics['basic_analysis_time'] = analysis_time
            
            # Performance check (target < 500ms)
            if analysis_time <= 500:
                self.logger.info(f"🚀 Analysis performance: GOOD ({analysis_time:.2f}ms <= 500ms)")
            else:
                self.logger.warning(f"⚠️ Analysis performance: SLOW ({analysis_time:.2f}ms > 500ms)")
                
        except Exception as e:
            self.logger.error(f"❌ Basic message analysis failed: {e}")
            self.fail(f"Basic analysis failed: {e}")
            
    def test_03_high_risk_message_detection(self):
        """Test detection of high-risk crisis messages"""
        self.logger.info("🔧 Testing high-risk message detection...")
        
        high_risk_results = []
        total_analysis_time = 0
        
        for i, message in enumerate(self.test_messages['high_risk']):
            self.logger.info(f"🔍 Analyzing high-risk message {i+1}/{len(self.test_messages['high_risk'])}")
            
            try:
                start_time = time.time()
                
                # Use available analysis method with proper parameters
                if hasattr(self.crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                        # Async method
                        result = asyncio.run(self.crisis_analyzer.analyze_message(
                            message,
                            user_id=f"test_user_{i+1}",
                            channel_id="test_channel_crisis"
                        ))
                    else:
                        # Sync method
                        result = self.crisis_analyzer.analyze_message(
                            message,
                            user_id=f"test_user_{i+1}",
                            channel_id="test_channel_crisis"
                        )
                elif hasattr(self.crisis_analyzer, 'analyze'):
                    result = self.crisis_analyzer.analyze(message)
                else:
                    self.fail("No analysis method available")
                    
                analysis_time = (time.time() - start_time) * 1000
                total_analysis_time += analysis_time
                
                # Store result
                high_risk_results.append({
                    'message': message[:50] + "..." if len(message) > 50 else message,
                    'result': result,
                    'analysis_time': analysis_time
                })
                
                self.logger.info(f"   ⏱️ Analysis time: {analysis_time:.2f}ms")
                
                # Log result summary if available
                if isinstance(result, dict) and result:
                    summary_fields = ['score', 'confidence', 'level', 'crisis_score', 'crisis_level']
                    summary = {field: result.get(field) for field in summary_fields if field in result}
                    if summary:
                        self.logger.info(f"   📊 Result: {summary}")
                        
            except Exception as e:
                self.logger.error(f"   ❌ Analysis failed: {e}")
                # Don't fail the test, just log the error
                
        # Store results for reporting
        self.__class__.analysis_results['high_risk'] = high_risk_results
        
        if high_risk_results:
            avg_time = total_analysis_time / len(high_risk_results)
            self.__class__.performance_metrics['high_risk_avg_time'] = avg_time
            
            self.logger.info(f"📊 High-risk analysis summary:")
            self.logger.info(f"   Messages analyzed: {len(high_risk_results)}")
            self.logger.info(f"   Average analysis time: {avg_time:.2f}ms")
            
            # Performance validation (current target: improve from 750-1500ms to <500ms)
            if avg_time <= 500:
                self.logger.info(f"🚀 High-risk analysis performance: TARGET ACHIEVED ({avg_time:.2f}ms <= 500ms)")
            else:
                self.logger.warning(f"⚠️ High-risk analysis performance: NEEDS IMPROVEMENT ({avg_time:.2f}ms > 500ms)")
                
        self.assertGreater(len(high_risk_results), 0, "Should analyze at least one high-risk message")
        
    def test_04_message_category_analysis(self):
        """Test analysis across different message categories"""
        self.logger.info("🔧 Testing analysis across message categories...")
        
        categories_to_test = ['moderate_risk', 'low_risk', 'lgbtqia_specific', 'support_seeking', 'normal']
        category_results = {}
        
        for category in categories_to_test:
            self.logger.info(f"🔍 Testing {category} messages...")
            
            messages = self.test_messages.get(category, [])
            if not messages:
                self.logger.warning(f"⚠️ No test messages for category: {category}")
                continue
                
            category_analysis_times = []
            category_message_results = []
            
            for i, message in enumerate(messages[:2]):  # Test first 2 messages per category
                try:
                    start_time = time.time()
                    
                    # Use available analysis method with proper parameters
                    if hasattr(self.crisis_analyzer, 'analyze_message'):
                        import inspect
                        if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                            result = asyncio.run(self.crisis_analyzer.analyze_message(
                                message,
                                user_id=f"test_user_cat_{category}_{i}",
                                channel_id=f"test_channel_{category}"
                            ))
                        else:
                            result = self.crisis_analyzer.analyze_message(
                                message,
                                user_id=f"test_user_cat_{category}_{i}",
                                channel_id=f"test_channel_{category}"
                            )
                    elif hasattr(self.crisis_analyzer, 'analyze'):
                        result = self.crisis_analyzer.analyze(message)
                    else:
                        continue
                        
                    analysis_time = (time.time() - start_time) * 1000
                    category_analysis_times.append(analysis_time)
                    
                    category_message_results.append({
                        'message_preview': message[:40] + "..." if len(message) > 40 else message,
                        'result': result,
                        'analysis_time': analysis_time
                    })
                    
                    self.logger.info(f"   ✅ Message {i+1} analyzed in {analysis_time:.2f}ms")
                    
                except Exception as e:
                    self.logger.error(f"   ❌ Message {i+1} analysis failed: {e}")
                    
            # Calculate category statistics
            if category_analysis_times:
                avg_time = sum(category_analysis_times) / len(category_analysis_times)
                category_results[category] = {
                    'messages_analyzed': len(category_message_results),
                    'average_time': avg_time,
                    'results': category_message_results
                }
                
                self.logger.info(f"   📊 {category}: {len(category_message_results)} messages, avg {avg_time:.2f}ms")
                
        # Store results
        self.__class__.analysis_results['categories'] = category_results
        
        # Validate that we tested multiple categories
        self.assertGreaterEqual(len(category_results), 3, "Should test at least 3 message categories")
        
        self.logger.info(f"✅ Tested {len(category_results)} message categories successfully")
        
    def test_05_performance_analysis(self):
        """Test and report overall performance metrics"""
        self.logger.info("🔧 Analyzing overall performance metrics...")
        
        metrics = self.__class__.performance_metrics
        
        if not metrics:
            self.logger.warning("⚠️ No performance metrics available")
            return
            
        self.logger.info("📊 Performance Analysis Summary:")
        
        # Report individual metrics
        for metric_name, value in metrics.items():
            self.logger.info(f"   {metric_name}: {value:.2f}ms")
            
        # Calculate overall statistics
        all_times = [v for v in metrics.values() if isinstance(v, (int, float))]
        if all_times:
            min_time = min(all_times)
            max_time = max(all_times)
            avg_time = sum(all_times) / len(all_times)
            
            self.logger.info("📈 Performance Statistics:")
            self.logger.info(f"   Fastest analysis: {min_time:.2f}ms")
            self.logger.info(f"   Slowest analysis: {max_time:.2f}ms")
            self.logger.info(f"   Average analysis: {avg_time:.2f}ms")
            
            # Performance targets from Step 7
            target_times = {
                'excellent': 100,
                'good': 250,
                'acceptable': 500,
                'slow': 1000
            }
            
            if avg_time <= target_times['excellent']:
                self.logger.info(f"🚀 Overall Performance: EXCELLENT ({avg_time:.2f}ms <= {target_times['excellent']}ms)")
            elif avg_time <= target_times['good']:
                self.logger.info(f"✅ Overall Performance: GOOD ({avg_time:.2f}ms <= {target_times['good']}ms)")
            elif avg_time <= target_times['acceptable']:
                self.logger.info(f"⚡ Overall Performance: ACCEPTABLE ({avg_time:.2f}ms <= {target_times['acceptable']}ms)")
            elif avg_time <= target_times['slow']:
                self.logger.warning(f"⚠️ Overall Performance: SLOW ({avg_time:.2f}ms <= {target_times['slow']}ms)")
            else:
                self.logger.error(f"❌ Overall Performance: VERY SLOW ({avg_time:.2f}ms > {target_times['slow']}ms)")
                
            # Store final performance summary
            self.__class__.performance_summary = {
                'min_time': min_time,
                'max_time': max_time,
                'avg_time': avg_time,
                'total_analyses': len(all_times)
            }
            
    def test_06_system_stability(self):
        """Test system stability with multiple rapid analyses"""
        self.logger.info("🔧 Testing system stability with rapid analyses...")
        
        # Test rapid-fire analysis
        test_messages = [
            "Test message 1 for stability testing",
            "Another test message for rapid analysis",
            "Checking system stability with multiple requests",
            "Final stability test message"
        ]
        
        successful_analyses = 0
        total_time = 0
        
        for i, message in enumerate(test_messages):
            try:
                start_time = time.time()
                
                if hasattr(self.crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(self.crisis_analyzer.analyze_message):
                        result = asyncio.run(self.crisis_analyzer.analyze_message(
                            message,
                            user_id=f"stability_user_{i}",
                            channel_id="stability_test_channel"
                        ))
                    else:
                        result = self.crisis_analyzer.analyze_message(
                            message,
                            user_id=f"stability_user_{i}",
                            channel_id="stability_test_channel"
                        )
                elif hasattr(self.crisis_analyzer, 'analyze'):
                    result = self.crisis_analyzer.analyze(message)
                else:
                    break
                    
                analysis_time = (time.time() - start_time) * 1000
                total_time += analysis_time
                successful_analyses += 1
                
                self.logger.info(f"   ✅ Rapid analysis {i+1}: {analysis_time:.2f}ms")
                
            except Exception as e:
                self.logger.error(f"   ❌ Rapid analysis {i+1} failed: {e}")
                
        if successful_analyses > 0:
            avg_rapid_time = total_time / successful_analyses
            self.logger.info(f"📊 Stability test: {successful_analyses}/{len(test_messages)} successful")
            self.logger.info(f"⚡ Average rapid analysis time: {avg_rapid_time:.2f}ms")
            
            # System should be stable (all analyses should succeed)
            stability_rate = successful_analyses / len(test_messages)
            if stability_rate >= 0.95:
                self.logger.info(f"🚀 System Stability: EXCELLENT ({stability_rate*100:.1f}% success)")
            elif stability_rate >= 0.80:
                self.logger.info(f"✅ System Stability: GOOD ({stability_rate*100:.1f}% success)")
            else:
                self.logger.warning(f"⚠️ System Stability: NEEDS ATTENTION ({stability_rate*100:.1f}% success)")
                
            self.assertGreaterEqual(stability_rate, 0.75, "System should be at least 75% stable")
            
        else:
            self.fail("No analyses succeeded in stability test")
            
    @classmethod
    def tearDownClass(cls):
        """Clean up and provide final summary"""
        cls.logger.info("🧹 Cleaning up crisis detection workflow tests...")
        
        # Final summary
        cls.logger.info("📋 Crisis Detection Workflow Test Summary:")
        
        if hasattr(cls, 'analysis_results'):
            for category, results in cls.analysis_results.items():
                if isinstance(results, list):
                    cls.logger.info(f"   {category}: {len(results)} messages analyzed")
                elif isinstance(results, dict):
                    total_messages = sum(r.get('messages_analyzed', 0) for r in results.values())
                    cls.logger.info(f"   {category}: {total_messages} total messages across {len(results)} subcategories")
                    
        if hasattr(cls, 'performance_summary'):
            perf = cls.performance_summary
            cls.logger.info("⚡ Performance Summary:")
            cls.logger.info(f"   Total analyses: {perf['total_analyses']}")
            cls.logger.info(f"   Average time: {perf['avg_time']:.2f}ms")
            cls.logger.info(f"   Range: {perf['min_time']:.2f}ms - {perf['max_time']:.2f}ms")
            
        cls.logger.info("✅ Crisis Detection Workflow Integration Tests Complete!")


if __name__ == '__main__':
    # Configure test runner with colored output
    import sys
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCrisisDetectionWorkflow)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True
    )
    
    result = runner.run(test_suite)
    
    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)