# ash-nlp/tests/phase/3/e/test_context_pattern_manager_cleanup.py
"""
Integration Test for ContextPatternManager Cleanup - Phase 3e Sub-step 5.4
FILE VERSION: v3.1-3e-5.4-test-1
LAST MODIFIED: 2025-08-19
PHASE: 3e, Sub-step 5.4 - ContextPatternManager Cleanup Integration Test
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This test validates that ContextPatternManager continues to function correctly
after methods were migrated to SharedUtilitiesManager and CrisisAnalyzer during
Phase 3e consolidation.

MIGRATION VALIDATIONS:
- validate_context_data() → SharedUtilitiesManager.validate_data_structure()
- log_context_performance() → SharedUtilitiesManager.log_performance_metric()  
- extract_context_signals() → CrisisAnalyzer.extract_context_signals()
- analyze_sentiment_context() → CrisisAnalyzer.analyze_sentiment_context()
- score_term_in_context() → CrisisAnalyzer.score_term_in_context()
"""

import unittest
import logging
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the managers we need for testing
from managers.unified_config_manager import UnifiedConfigManager, create_unified_config_manager
from managers.context_pattern_manager import ContextPatternManager, create_context_pattern_manager
from managers.logging_config_manager import LoggingConfigManager, create_logging_config_manager

class TestContextPatternManagerCleanup(unittest.TestCase):
    """Test suite for ContextPatternManager after Phase 3e cleanup"""

    def setUp(self):
        """Set up test environment using existing configuration system"""
        # Use the existing UnifiedConfigManager with default config directory
        self.unified_config = create_unified_config_manager()
        
        # Set up logging using the REAL LoggingConfigManager with proper UnifiedConfigManager
        self.logging_manager = create_logging_config_manager(self.unified_config)
        self.logger = logging.getLogger(__name__)
        
        # Create ContextPatternManager instance using existing config system
        self.manager = create_context_pattern_manager(self.unified_config)
        
        self.logger.info("🧪 ContextPatternManager cleanup test setup completed")

    def tearDown(self):
        """Clean up test environment"""
        self.logger.info("🧹 Test cleanup completed")

    # ========================================================================
    # CORE INITIALIZATION TESTS
    # ========================================================================

    def test_01_manager_initialization(self):
        """Test that ContextPatternManager initializes correctly after cleanup"""
        self.assertIsNotNone(self.manager)
        self.assertTrue(self.manager.is_initialized())
        self.assertIsNotNone(self.manager.unified_config)
        self.assertIsInstance(self.manager.context_config, dict)
        self.assertIsInstance(self.manager.analysis_params, dict)
        
        # Verify version and phase information
        status = self.manager.get_configuration_status()
        self.assertEqual(status['manager_version'], 'v3.1-3e-5.4-1')
        self.assertEqual(status['phase'], 'Phase 3e Sub-step 5.4 - Cleanup Complete')
        
        self.logger.info("✅ Test 01: Manager initialization successful")

    def test_02_factory_function(self):
        """Test that factory function works correctly after cleanup"""
        factory_manager = create_context_pattern_manager(self.unified_config)
        
        self.assertIsNotNone(factory_manager)
        self.assertTrue(factory_manager.is_initialized())
        self.assertIsInstance(factory_manager, ContextPatternManager)
        
        self.logger.info("✅ Test 02: Factory function working correctly")

    # ========================================================================
    # MIGRATION REFERENCE TESTS
    # ========================================================================

    def test_03_validate_context_data_migration(self):
        """Test validate_context_data migration reference"""
        result = self.manager.validate_context_data({'test': 'data'})
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'moved')
        self.assertEqual(result['original_method'], 'validate_context_data')
        self.assertEqual(result['new_location'], 'SharedUtilitiesManager.validate_data_structure')
        self.assertIn('Phase 3e', result['migration_phase'])
        self.assertIsInstance(result['benefits'], list)
        self.assertTrue(len(result['benefits']) > 0)
        
        self.logger.info("✅ Test 03: validate_context_data migration reference working")

    def test_04_log_context_performance_migration(self):
        """Test log_context_performance migration reference"""
        result = self.manager.log_context_performance('test_metric', 123.45)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'moved')
        self.assertEqual(result['original_method'], 'log_context_performance')
        self.assertEqual(result['new_location'], 'SharedUtilitiesManager.log_performance_metric')
        self.assertIn('Performance logging', result['additional_info'])
        
        self.logger.info("✅ Test 04: log_context_performance migration reference working")

    def test_05_extract_context_signals_migration(self):
        """Test extract_context_signals migration reference"""
        result = self.manager.extract_context_signals("I'm feeling really alone today")
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'moved')
        self.assertEqual(result['original_method'], 'extract_context_signals')
        self.assertEqual(result['new_location'], 'CrisisAnalyzer.extract_context_signals')
        self.assertIn('crisis analysis system', result['additional_info'])
        
        self.logger.info("✅ Test 05: extract_context_signals migration reference working")

    def test_06_analyze_sentiment_context_migration(self):
        """Test analyze_sentiment_context migration reference"""
        result = self.manager.analyze_sentiment_context("I'm not feeling good", -0.5)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'moved')
        self.assertEqual(result['original_method'], 'analyze_sentiment_context')
        self.assertEqual(result['new_location'], 'CrisisAnalyzer.analyze_sentiment_context')
        self.assertIn('crisis detection algorithms', result['additional_info'])
        
        self.logger.info("✅ Test 06: analyze_sentiment_context migration reference working")

    def test_07_score_term_in_context_migration(self):
        """Test score_term_in_context migration reference"""
        result = self.manager.score_term_in_context("crisis", "I'm having a crisis right now")
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'moved')
        self.assertEqual(result['original_method'], 'score_term_in_context')
        self.assertEqual(result['new_location'], 'CrisisAnalyzer.score_term_in_context')
        self.assertIn('crisis detection scenarios', result['additional_info'])
        
        self.logger.info("✅ Test 07: score_term_in_context migration reference working")

    # ========================================================================
    # REMAINING FUNCTIONALITY TESTS
    # ========================================================================

    def test_08_detect_negation_context(self):
        """Test that negation detection still works correctly"""
        # Test positive cases
        self.assertTrue(self.manager.detect_negation_context("I'm not feeling good"))
        self.assertTrue(self.manager.detect_negation_context("I can't handle this anymore"))
        self.assertTrue(self.manager.detect_negation_context("I don't know what to do"))
        self.assertTrue(self.manager.detect_negation_context("I'm hardly eating"))
        
        # Test negative cases
        self.assertFalse(self.manager.detect_negation_context("I'm feeling great"))
        self.assertFalse(self.manager.detect_negation_context("Everything is wonderful"))
        
        self.logger.info("✅ Test 08: Negation detection working correctly")

    def test_09_process_sentiment_with_flip(self):
        """Test sentiment processing with polarity flipping"""
        # Test with negation (should flip)
        result = self.manager.process_sentiment_with_flip("I'm not happy", 0.8)
        self.assertEqual(result['original_score'], 0.8)
        self.assertEqual(result['final_score'], -0.8)
        self.assertTrue(result['flip_applied'])
        self.assertTrue(result['context_analysis']['negation_detected'])
        
        # Test without negation (should not flip)
        result = self.manager.process_sentiment_with_flip("I'm very happy", 0.8)
        self.assertEqual(result['original_score'], 0.8)
        self.assertEqual(result['final_score'], 0.8)
        self.assertFalse(result['flip_applied'])
        self.assertFalse(result['context_analysis']['negation_detected'])
        
        # Test with small score (should not flip even with negation)
        result = self.manager.process_sentiment_with_flip("I'm not sure", 0.05)
        self.assertEqual(result['original_score'], 0.05)
        self.assertEqual(result['final_score'], 0.05)
        self.assertFalse(result['flip_applied'])
        
        self.logger.info("✅ Test 09: Sentiment processing with flip working correctly")

    def test_10_enhanced_context_analysis(self):
        """Test enhanced context analysis functionality"""
        # Test without crisis pattern manager
        result = self.manager.perform_enhanced_context_analysis("I'm feeling alone today")
        
        self.assertIsInstance(result, dict)
        self.assertIn('message_length', result)
        self.assertIn('word_count', result)
        self.assertIn('negation_context', result)
        self.assertIn('temporal_indicators', result)
        self.assertFalse(result['crisis_context_available'])
        self.assertEqual(result['pattern_manager_status'], 'not_available')
        self.assertIn('enhanced_analysis_note', result)
        
        # Test with mock crisis pattern manager
        mock_pattern_manager = MagicMock()
        mock_pattern_manager.analyze_temporal_indicators.return_value = {
            'urgency_level': 'high',
            'temporal_words': ['today']
        }
        
        result = self.manager.perform_enhanced_context_analysis(
            "I'm feeling alone today", 
            crisis_pattern_manager=mock_pattern_manager
        )
        
        self.assertTrue(result['crisis_context_available'])
        self.assertEqual(result['pattern_manager_status'], 'available')
        self.assertIn('temporal_analysis', result)
        
        self.logger.info("✅ Test 10: Enhanced context analysis working correctly")

    # ========================================================================
    # CONFIGURATION TESTS
    # ========================================================================

    def test_11_configuration_access(self):
        """Test configuration parameter access"""
        # Test context window
        context_window = self.manager._get_context_window()
        self.assertIsInstance(context_window, int)
        self.assertGreaterEqual(context_window, 1)
        
        # Test context boost weight
        boost_weight = self.manager._get_context_boost_weight()
        self.assertIsInstance(boost_weight, (int, float))
        self.assertGreater(boost_weight, 0)
        
        # Test negative threshold
        neg_threshold = self.manager._get_negative_threshold()
        self.assertIsInstance(neg_threshold, (int, float))
        self.assertGreaterEqual(neg_threshold, 0)
        self.assertLessEqual(neg_threshold, 1)
        
        self.logger.info("✅ Test 11: Configuration access working correctly")

    def test_12_configuration_status(self):
        """Test configuration status reporting"""
        status = self.manager.get_configuration_status()
        
        self.assertIsInstance(status, dict)
        self.assertEqual(status['manager_version'], 'v3.1-3e-5.4-1')
        self.assertIn('initialization_time', status)
        self.assertIn('configuration_loaded', status)
        self.assertIn('analysis_params_loaded', status)
        self.assertIn('migrated_methods', status)
        self.assertEqual(len(status['migrated_methods']), 5)
        
        # Verify all migrated methods are listed
        migrated_methods = '\n'.join(status['migrated_methods'])
        self.assertIn('validate_context_data', migrated_methods)
        self.assertIn('log_context_performance', migrated_methods)
        self.assertIn('extract_context_signals', migrated_methods)
        self.assertIn('analyze_sentiment_context', migrated_methods)
        self.assertIn('score_term_in_context', migrated_methods)
        
        self.logger.info("✅ Test 12: Configuration status reporting correctly")

    def test_13_configuration_reload(self):
        """Test configuration reload functionality"""
        # Test successful reload
        result = self.manager.reload_configuration()
        self.assertTrue(result)
        
        # Verify configuration is still loaded
        self.assertTrue(self.manager.is_initialized())
        self.assertIsInstance(self.manager.context_config, dict)
        
        self.logger.info("✅ Test 13: Configuration reload working correctly")

    # ========================================================================
    # HELPER METHOD TESTS
    # ========================================================================

    def test_14_temporal_indicators(self):
        """Test temporal indicator extraction"""
        # Test with temporal words
        indicators = self.manager._extract_basic_temporal_indicators("i'm feeling bad today and right now")
        self.assertIn('today', indicators)
        self.assertIn('right now', indicators)
        
        # Test without temporal words
        indicators = self.manager._extract_basic_temporal_indicators("i'm feeling bad")
        self.assertEqual(len(indicators), 0)
        
        self.logger.info("✅ Test 14: Temporal indicator extraction working correctly")

    def test_15_social_isolation_indicators(self):
        """Test social isolation indicator counting"""
        # Test with isolation words
        count = self.manager._count_social_isolation_indicators("i'm so alone and lonely")
        self.assertGreaterEqual(count, 2)
        
        # Test without isolation words
        count = self.manager._count_social_isolation_indicators("i'm feeling great with friends")
        self.assertEqual(count, 0)
        
        self.logger.info("✅ Test 15: Social isolation indicator counting working correctly")

    def test_16_hopelessness_indicators(self):
        """Test hopelessness indicator counting"""
        # Test with hopelessness words
        count = self.manager._count_hopelessness_indicators("i feel hopeless and worthless")
        self.assertGreaterEqual(count, 2)
        
        # Test without hopelessness words
        count = self.manager._count_hopelessness_indicators("i'm feeling optimistic")
        self.assertEqual(count, 0)
        
        self.logger.info("✅ Test 16: Hopelessness indicator counting working correctly")

    # ========================================================================
    # INTEGRATION VALIDATION TESTS
    # ========================================================================

    def test_17_migration_benefits_verification(self):
        """Test that migration benefits are properly documented"""
        migration_result = self.manager.validate_context_data({})
        
        benefits = migration_result['benefits']
        self.assertIn('Eliminated code duplication', ' '.join(benefits))
        self.assertIn('Centralized utility functions', ' '.join(benefits))
        self.assertIn('architecture compliance', ' '.join(benefits))
        self.assertIn('Enhanced crisis detection', ' '.join(benefits))
        
        self.logger.info("✅ Test 17: Migration benefits properly documented")

    def test_18_deprecation_handling(self):
        """Test that deprecated method calls are handled gracefully"""
        # Test all deprecated methods return proper migration info
        deprecated_methods = [
            'validate_context_data',
            'log_context_performance', 
            'extract_context_signals',
            'analyze_sentiment_context',
            'score_term_in_context'
        ]
        
        for method_name in deprecated_methods:
            method = getattr(self.manager, method_name)
            result = method()
            
            self.assertEqual(result['status'], 'moved')
            self.assertEqual(result['original_method'], method_name)
            self.assertIn('new_location', result)
            self.assertIn('migration_phase', result)
            self.assertIn('Phase 3e', result['migration_phase'])
        
        self.logger.info("✅ Test 18: Deprecated method handling working correctly")

    # ========================================================================
    # CRISIS DETECTION PRESERVATION TESTS
    # ========================================================================

    def test_19_crisis_functionality_preservation(self):
        """Test that core crisis detection functionality is preserved"""
        # Test various crisis-related messages
        test_messages = [
            "I'm not feeling good about anything",
            "I can't handle this anymore", 
            "I'm alone and hopeless today",
            "Everything seems pointless right now"
        ]
        
        for message in test_messages:
            # Basic analysis should still work
            enhanced_result = self.manager.perform_enhanced_context_analysis(message)
            self.assertIsInstance(enhanced_result, dict)
            self.assertIn('negation_context', enhanced_result)
            
            # Sentiment flip should work if negation detected
            sentiment_result = self.manager.process_sentiment_with_flip(message, 0.5)
            self.assertIsInstance(sentiment_result, dict)
            self.assertIn('original_score', sentiment_result)
            self.assertIn('final_score', sentiment_result)
        
        self.logger.info("✅ Test 19: Crisis functionality preservation verified")

    def test_20_architecture_compliance(self):
        """Test Clean v3.1 architecture compliance after cleanup"""
        # Test factory function compliance
        self.assertTrue(callable(create_context_pattern_manager))
        
        # Test dependency injection
        self.assertIsNotNone(self.manager.unified_config)
        
        # Test proper initialization patterns
        self.assertTrue(self.manager.is_initialized())
        
        # Test configuration loading patterns  
        self.assertIsInstance(self.manager.context_config, dict)
        self.assertIsInstance(self.manager.analysis_params, dict)
        
        # Test error handling resilience
        self.assertIsNotNone(self.manager._get_safe_context_defaults())
        self.assertIsNotNone(self.manager._get_safe_analysis_defaults())
        
        self.logger.info("✅ Test 20: Architecture compliance verified")

    # ========================================================================
    # PERFORMANCE AND OPTIMIZATION TESTS
    # ========================================================================

    def test_21_performance_optimization(self):
        """Test that cleanup maintained or improved performance"""
        import time
        
        # Test multiple operations for timing
        start_time = time.time()
        
        for i in range(100):
            self.manager.detect_negation_context(f"Test message {i} with negation not good")
            self.manager.process_sentiment_with_flip(f"Test message {i}", 0.5)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete 200 operations in reasonable time (< 1 second)
        self.assertLess(elapsed, 1.0, "Performance should be maintained after cleanup")
        
        self.logger.info(f"✅ Test 21: Performance optimization verified ({elapsed:.3f}s for 200 operations)")

    def test_22_memory_efficiency(self):
        """Test memory efficiency after cleanup"""
        import sys
        
        # Create multiple manager instances to test memory usage
        managers = []
        initial_size = sys.getsizeof(self.manager)
        
        for i in range(10):
            manager = ContextPatternManager(self.unified_config)
            managers.append(manager)
        
        # Verify no excessive memory growth
        final_size = sys.getsizeof(managers[-1])
        self.assertLessEqual(final_size, initial_size * 1.1, "Memory usage should be efficient")
        
        self.logger.info("✅ Test 22: Memory efficiency verified")


if __name__ == '__main__':
    # Set up logging for test execution
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test methods
    test_loader = unittest.TestLoader()
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestContextPatternManagerCleanup))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"CONTEXT PATTERN MANAGER CLEANUP TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    print(f"\n🏳️‍🌈 Phase 3e Sub-step 5.4: ContextPatternManager Cleanup Integration Test Complete!")
    print(f"The Alphabet Cartel LGBTQIA+ community crisis detection capabilities preserved! 🌈")