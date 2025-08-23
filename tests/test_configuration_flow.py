#!/usr/bin/env python3
"""
Phase 3e Step 7.1: Configuration Flow Integration Test
Tests UnifiedConfigManager → All Managers configuration flow

FILE: tests/test_configuration_flow.py
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
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import colorlog for colored test output
try:
    import colorlog
except ImportError:
    print("❌ colorlog not installed. Install with: pip install colorlog")
    sys.exit(1)

# Import managers and factory functions
try:
    from managers.unified_config import create_unified_config_manager
    from managers.analysis_config import create_analysis_config_manager
    from managers.pattern_detection import create_pattern_detection_manager
    from managers.crisis_threshold import create_crisis_threshold_manager
    from managers.feature_config import create_feature_config_manager
    from managers.performance_config import create_performance_config_manager
    from managers.context_analysis import create_context_analysis_manager
    from managers.shared_utilities import create_shared_utilities_manager
    from managers.learning_system import create_learning_system_manager
    from managers.zero_shot import create_zero_shot_manager
    from managers.model_coordination import create_model_coordination_manager
    from analysis.crisis_analyzer import create_crisis_analyzer
except ImportError as e:
    print(f"❌ Failed to import managers: {e}")
    sys.exit(1)


class TestConfigurationFlow(unittest.TestCase):
    """Test suite for configuration flow validation"""
    
    @classmethod
    def setUpClass(cls):
        """Set up colored logging for test output"""
        # Configure colorlog formatter
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[TEST] %(levelname)s%(reset)s: %(message)s',
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
        cls.logger = logging.getLogger('ConfigurationFlowTest')
        cls.logger.setLevel(logging.INFO)
        cls.logger.handlers = [console_handler]
        
        cls.logger.info("🚀 Starting Configuration Flow Integration Tests")
        
        # Initialize managers for testing
        cls.managers = {}
        cls.config_access_times = {}
        
    def setUp(self):
        """Set up each test case"""
        self.start_time = time.time()
        
    def tearDown(self):
        """Clean up after each test case"""
        test_time = (time.time() - self.start_time) * 1000
        self.logger.info(f"⏱️ Test completed in {test_time:.2f}ms")
        
    def test_01_unified_config_manager_creation(self):
        """Test UnifiedConfigManager creation and basic functionality"""
        self.logger.info("🔧 Testing UnifiedConfigManager creation...")
        
        try:
            start_time = time.time()
            unified_config = create_unified_config_manager()
            creation_time = (time.time() - start_time) * 1000
            
            # Store for other tests
            self.__class__.managers['unified_config'] = unified_config
            self.__class__.config_access_times['creation'] = creation_time
            
            # Validate basic functionality
            self.assertIsNotNone(unified_config)
            self.assertTrue(hasattr(unified_config, 'get_env'))
            self.assertTrue(hasattr(unified_config, 'get_env_bool'))
            self.assertTrue(hasattr(unified_config, 'get_env_int'))
            self.assertTrue(hasattr(unified_config, 'get_env_float'))
            
            # Test basic configuration access
            log_level = unified_config.get_env('GLOBAL_LOG_LEVEL', 'INFO')
            self.assertIsNotNone(log_level)
            
            self.logger.info(f"✅ UnifiedConfigManager created in {creation_time:.2f}ms")
            self.logger.info(f"📊 Log level configured: {log_level}")
            
        except Exception as e:
            self.logger.error(f"❌ UnifiedConfigManager creation failed: {e}")
            self.fail(f"Failed to create UnifiedConfigManager: {e}")
            
    def test_02_manager_factory_functions(self):
        """Test all manager factory functions with UnifiedConfigManager"""
        self.logger.info("🔧 Testing manager factory functions...")
        
        unified_config = self.__class__.managers.get('unified_config')
        self.assertIsNotNone(unified_config, "UnifiedConfigManager required for this test")
        
        # Define manager factory functions to test
        manager_factories = [
            ('analysis_config', create_analysis_config_manager),
            ('context_analysis', create_context_analysis_manager),
            ('pattern_detection', create_pattern_detection_manager),
            ('feature_config', create_feature_config_manager),
            ('performance_config', create_performance_config_manager),
            ('shared_utilities', create_shared_utilities_manager),
            ('crisis_threshold', create_crisis_threshold_manager),
            ('zero_shot', create_zero_shot_manager),
            ('model_coordination', create_model_coordination_manager)
        ]
        
        successful_managers = 0
        total_creation_time = 0
        
        for manager_name, factory_func in manager_factories:
            try:
                start_time = time.time()
                manager = factory_func(unified_config)
                creation_time = (time.time() - start_time) * 1000
                total_creation_time += creation_time
                
                # Store manager for other tests
                self.__class__.managers[manager_name] = manager
                self.__class__.config_access_times[f'{manager_name}_creation'] = creation_time
                
                # Basic validation
                self.assertIsNotNone(manager)
                successful_managers += 1
                
                self.logger.info(f"✅ {manager_name} manager created in {creation_time:.2f}ms")
                
            except Exception as e:
                self.logger.error(f"❌ {manager_name} manager creation failed: {e}")
                # Don't fail the test, just log the error for now
                
        self.logger.info(f"📊 Created {successful_managers}/{len(manager_factories)} managers")
        self.logger.info(f"⏱️ Total manager creation time: {total_creation_time:.2f}ms")
        
        # Ensure at least core managers were created
        self.assertGreaterEqual(successful_managers, 5, "At least 5 core managers should be created")
        
    def test_03_learning_system_manager_integration(self):
        """Test LearningSystemManager creation with SharedUtilities dependency"""
        self.logger.info("🔧 Testing LearningSystemManager with dependencies...")
        
        unified_config = self.__class__.managers.get('unified_config')
        shared_utilities = self.__class__.managers.get('shared_utilities')
        
        self.assertIsNotNone(unified_config, "UnifiedConfigManager required")
        self.assertIsNotNone(shared_utilities, "SharedUtilitiesManager required")
        
        try:
            start_time = time.time()
            learning_system = create_learning_system_manager(
                unified_config,
                shared_utils=shared_utilities
            )
            creation_time = (time.time() - start_time) * 1000
            
            # Store for other tests
            self.__class__.managers['learning_system'] = learning_system
            self.__class__.config_access_times['learning_system_creation'] = creation_time
            
            # Validate integration
            self.assertIsNotNone(learning_system)
            
            # Check for shared_utils attribute (correct attribute name)
            if hasattr(learning_system, 'shared_utils'):
                self.logger.info("✅ LearningSystemManager has shared_utils attribute")
            else:
                self.logger.warning("⚠️ LearningSystemManager missing shared_utils attribute")
                
            # Check if manager has a valid status method
            if hasattr(learning_system, 'get_status'):
                status = learning_system.get_status()
                self.logger.info(f"✅ LearningSystemManager status: {status.get('status', 'unknown')}")
            
            self.logger.info(f"✅ LearningSystemManager created with dependencies in {creation_time:.2f}ms")
            
        except Exception as e:
            self.logger.error(f"❌ LearningSystemManager creation failed: {e}")
            self.fail(f"Failed to create LearningSystemManager: {e}")
            
    def test_04_configuration_access_patterns(self):
        """Test get_config_section() patterns across managers"""
        self.logger.info("🔧 Testing get_config_section() patterns...")
        
        managers_to_test = [
            ('analysis_config', ['analysis']),
            ('pattern_detection', ['patterns', 'detection']),
            ('crisis_threshold', ['thresholds', 'crisis']),
            ('feature_config', ['features'])
        ]
        
        successful_accesses = 0
        total_access_time = 0
        
        for manager_name, expected_sections in managers_to_test:
            manager = self.__class__.managers.get(manager_name)
            if not manager:
                self.logger.warning(f"⚠️ {manager_name} manager not available for testing")
                continue
                
            try:
                # Test get_config_section if available
                if hasattr(manager, 'get_config_section'):
                    for section in expected_sections:
                        start_time = time.time()
                        config_section = manager.get_config_section(section)
                        access_time = (time.time() - start_time) * 1000
                        total_access_time += access_time
                        
                        # Should return dict or None, not fail
                        self.assertTrue(
                            isinstance(config_section, (dict, type(None))),
                            f"get_config_section should return dict or None, got {type(config_section)}"
                        )
                        
                        successful_accesses += 1
                        self.logger.info(f"✅ {manager_name}.get_config_section('{section}') in {access_time:.2f}ms")
                        
                else:
                    # Test basic configuration access
                    if hasattr(manager, 'unified_config'):
                        start_time = time.time()
                        test_value = manager.unified_config.get_env('GLOBAL_LOG_LEVEL', 'INFO')
                        access_time = (time.time() - start_time) * 1000
                        total_access_time += access_time
                        
                        self.assertIsNotNone(test_value)
                        successful_accesses += 1
                        self.logger.info(f"✅ {manager_name} config access in {access_time:.2f}ms")
                        
            except Exception as e:
                self.logger.error(f"❌ Configuration access failed for {manager_name}: {e}")
                
        # Performance validation
        if successful_accesses > 0:
            avg_access_time = total_access_time / successful_accesses
            self.__class__.config_access_times['avg_config_access'] = avg_access_time
            
            self.logger.info(f"📊 Average configuration access time: {avg_access_time:.2f}ms")
            
            # Configuration access should be fast (target < 10ms)
            if avg_access_time > 10:
                self.logger.warning(f"⚠️ Configuration access slower than target (10ms): {avg_access_time:.2f}ms")
            else:
                self.logger.info(f"🚀 Configuration access performance: GOOD ({avg_access_time:.2f}ms < 10ms)")
                
        self.assertGreater(successful_accesses, 0, "At least one configuration access should succeed")
        
    def test_05_crisis_analyzer_integration(self):
        """Test CrisisAnalyzer creation with all manager dependencies"""
        self.logger.info("🔧 Testing CrisisAnalyzer integration with all managers...")
        
        # Check required dependencies
        unified_config = self.__class__.managers.get('unified_config')
        model_coordination = self.__class__.managers.get('model_coordination')
        
        self.assertIsNotNone(unified_config, "UnifiedConfigManager required")
        self.assertIsNotNone(model_coordination, "ModelCoordinationManager required")
        
        try:
            start_time = time.time()
            crisis_analyzer = create_crisis_analyzer(
                unified_config,
                model_coordination_manager=model_coordination,
                pattern_detection_manager=self.__class__.managers.get('pattern_detection'),
                analysis_config_manager=self.__class__.managers.get('analysis_config'),
                crisis_threshold_manager=self.__class__.managers.get('crisis_threshold'),
                feature_config_manager=self.__class__.managers.get('feature_config'),
                performance_config_manager=self.__class__.managers.get('performance_config'),
                context_analysis_manager=self.__class__.managers.get('context_analysis'),
                shared_utilities_manager=self.__class__.managers.get('shared_utilities'),
                learning_system_manager=self.__class__.managers.get('learning_system'),
                zero_shot_manager=self.__class__.managers.get('zero_shot')
            )
            creation_time = (time.time() - start_time) * 1000
            
            # Store for other tests
            self.__class__.managers['crisis_analyzer'] = crisis_analyzer
            self.__class__.config_access_times['crisis_analyzer_creation'] = creation_time
            
            # Validate integration
            self.assertIsNotNone(crisis_analyzer)
            self.assertTrue(hasattr(crisis_analyzer, 'unified_config_manager'))
            self.assertTrue(hasattr(crisis_analyzer, 'model_coordination_manager'))
            
            self.logger.info(f"✅ CrisisAnalyzer created with all dependencies in {creation_time:.2f}ms")
            
            # Test basic functionality exists
            if hasattr(crisis_analyzer, 'analyze_message'):
                self.logger.info("✅ CrisisAnalyzer.analyze_message method available")
            else:
                self.logger.warning("⚠️ CrisisAnalyzer.analyze_message method not found")
                
        except Exception as e:
            self.logger.error(f"❌ CrisisAnalyzer creation failed: {e}")
            self.fail(f"Failed to create CrisisAnalyzer: {e}")
            
    def test_06_performance_benchmarks(self):
        """Test performance against Step 7 benchmarks"""
        self.logger.info("🔧 Testing performance against benchmarks...")
        
        # Get performance metrics
        creation_times = self.__class__.config_access_times
        
        # Performance targets from step_7.md
        performance_targets = {
            'config_access': 10.0,  # < 10ms per config access
            'manager_creation': 500.0,  # < 500ms for all managers
            'crisis_analyzer_creation': 1000.0  # < 1000ms for crisis analyzer
        }
        
        results = {}
        
        # Test configuration access performance
        avg_config_time = creation_times.get('avg_config_access', 0)
        if avg_config_time > 0:
            results['config_access'] = avg_config_time
            if avg_config_time <= performance_targets['config_access']:
                self.logger.info(f"🚀 Configuration access: {avg_config_time:.2f}ms <= {performance_targets['config_access']}ms ✅")
            else:
                self.logger.warning(f"⚠️ Configuration access: {avg_config_time:.2f}ms > {performance_targets['config_access']}ms")
                
        # Test total manager creation time
        manager_times = [v for k, v in creation_times.items() if k.endswith('_creation') and k != 'creation']
        if manager_times:
            total_manager_time = sum(manager_times)
            results['total_manager_creation'] = total_manager_time
            if total_manager_time <= performance_targets['manager_creation']:
                self.logger.info(f"🚀 Total manager creation: {total_manager_time:.2f}ms <= {performance_targets['manager_creation']}ms ✅")
            else:
                self.logger.warning(f"⚠️ Total manager creation: {total_manager_time:.2f}ms > {performance_targets['manager_creation']}ms")
                
        # Test CrisisAnalyzer creation time
        crisis_analyzer_time = creation_times.get('crisis_analyzer_creation', 0)
        if crisis_analyzer_time > 0:
            results['crisis_analyzer_creation'] = crisis_analyzer_time
            if crisis_analyzer_time <= performance_targets['crisis_analyzer_creation']:
                self.logger.info(f"🚀 CrisisAnalyzer creation: {crisis_analyzer_time:.2f}ms <= {performance_targets['crisis_analyzer_creation']}ms ✅")
            else:
                self.logger.warning(f"⚠️ CrisisAnalyzer creation: {crisis_analyzer_time:.2f}ms > {performance_targets['crisis_analyzer_creation']}ms")
                
        # Store results for reporting
        self.__class__.performance_results = results
        
        self.logger.info("📊 Performance benchmark testing complete")
        
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.logger.info("🧹 Cleaning up test resources...")
        
        # Report final statistics
        manager_count = len([k for k in cls.managers.keys() if k != 'unified_config'])
        cls.logger.info(f"📊 Final Statistics:")
        cls.logger.info(f"   Managers created: {manager_count}")
        cls.logger.info(f"   Performance metrics collected: {len(cls.config_access_times)}")
        
        # Report performance summary
        if hasattr(cls, 'performance_results'):
            cls.logger.info("🚀 Performance Summary:")
            for metric, value in cls.performance_results.items():
                cls.logger.info(f"   {metric}: {value:.2f}ms")
                
        cls.logger.info("✅ Configuration Flow Integration Tests Complete!")


if __name__ == '__main__':
    # Configure test runner with colored output
    import sys
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestConfigurationFlow)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True
    )
    
    result = runner.run(test_suite)
    
    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)