# tests/phase/3/e/test_learning_system_manager_integration.py
"""
LearningSystemManager Integration Test Suite for Phase 3e Step 3
FILE VERSION: v3.1-3e-3.4-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 3.4 - Integration Testing
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
import os
from pathlib import Path
from datetime import datetime

# Import managers to test
from managers.learning_system_manager import LearningSystemManager, create_learning_system_manager
from managers.unified_config_manager import UnifiedConfigManager
from managers.shared_utilities import SharedUtilitiesManager
from managers.analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager
from managers.threshold_mapping_manager import ThresholdMappingManager, create_threshold_mapping_manager


class TestLearningSystemManagerIntegration(unittest.TestCase):
    """
    Integration test suite for LearningSystemManager
    
    Tests the complete integration of LearningSystemManager with other managers
    and validates that Phase 3e Step 3 consolidation works correctly.
    """
    
    def setUp(self):
        """Set up test environment for each test"""
        # Create mock dependencies
        self.mock_unified_config = Mock(spec=UnifiedConfigManager)
        self.mock_shared_utilities = Mock(spec=SharedUtilitiesManager)
        
        # Set up UnifiedConfigManager mock methods
        self.mock_unified_config.get_env_bool.side_effect = self._mock_get_env_bool
        self.mock_unified_config.get_env_float.side_effect = self._mock_get_env_float
        self.mock_unified_config.get_env_int.side_effect = self._mock_get_env_int
        self.mock_unified_config.get_env_str.side_effect = self._mock_get_env_str
        
        # Set up SharedUtilitiesManager mock methods
        self.mock_shared_utilities.validate_range.return_value = True
        self.mock_shared_utilities.handle_error_with_fallback.side_effect = self._mock_handle_error
        
        # Create temporary directory for persistence testing
        self.temp_dir = tempfile.mkdtemp()
        self.persistence_file = os.path.join(self.temp_dir, 'test_adjustments.json')
    
    def tearDown(self):
        """Clean up after each test"""
        # Clean up temporary files
        if os.path.exists(self.persistence_file):
            os.remove(self.persistence_file)
        os.rmdir(self.temp_dir)
    
    def _mock_get_env_bool(self, key: str, default: bool) -> bool:
        """Mock environment boolean getter"""
        env_values = {
            'NLP_ANALYSIS_LEARNING_ENABLED': True,
        }
        return env_values.get(key, default)
    
    def _mock_get_env_float(self, key: str, default: float) -> float:
        """Mock environment float getter"""
        env_values = {
            'NLP_ANALYSIS_LEARNING_RATE': 0.01,
            'NLP_ANALYSIS_LEARNING_MIN_CONFIDENCE_ADJUSTMENT': 0.05,
            'NLP_ANALYSIS_LEARNING_MAX_CONFIDENCE_ADJUSTMENT': 0.30,
            'NLP_ANALYSIS_LEARNING_FEEDBACK_WEIGHT': 0.1,
            'NLP_ANALYSIS_LEARNING_ADJUSTMENT_LIMIT': 0.05,
            'NLP_ANALYSIS_LEARNING_MAX_DRIFT': 0.1,
            'NLP_ANALYSIS_LEARNING_MIN_SENSITIVITY': 0.5,
            'NLP_ANALYSIS_LEARNING_MAX_SENSITIVITY': 1.5,
            'NLP_ANALYSIS_LEARNING_FALSE_POSITIVE_FACTOR': -0.1,
            'NLP_ANALYSIS_LEARNING_FALSE_NEGATIVE_FACTOR': 0.1,
            'NLP_ANALYSIS_LEARNING_SEVERITY_HIGH': 3.0,
            'NLP_ANALYSIS_LEARNING_SEVERITY_MEDIUM': 2.0,
            'NLP_ANALYSIS_LEARNING_SEVERITY_LOW': 1.0,
        }
        return env_values.get(key, default)
    
    def _mock_get_env_int(self, key: str, default: int) -> int:
        """Mock environment integer getter"""
        env_values = {
            'NLP_ANALYSIS_LEARNING_MAX_ADJUSTMENTS_PER_DAY': 50,
            'NLP_ANALYSIS_LEARNING_MIN_SAMPLES': 5,
        }
        return env_values.get(key, default)
    
    def _mock_get_env_str(self, key: str, default: str) -> str:
        """Mock environment string getter"""
        env_values = {
            'NLP_ANALYSIS_LEARNING_PERSISTENCE_FILE': self.persistence_file,
        }
        return env_values.get(key, default)
    
    def _mock_handle_error(self, error, fallback_value, context, operation):
        """Mock error handler that returns fallback value"""
        return fallback_value
    
    # ========================================================================
    # FACTORY FUNCTION AND DEPENDENCY INJECTION TESTS
    # ========================================================================
    
    def test_factory_function_creation(self):
        """Test LearningSystemManager factory function with valid dependencies"""
        manager = create_learning_system_manager(
            self.mock_unified_config,
            self.mock_shared_utilities
        )
        
        self.assertIsInstance(manager, LearningSystemManager)
        self.assertEqual(manager.unified_config, self.mock_unified_config)
        self.assertEqual(manager.shared_utilities, self.mock_shared_utilities)
    
    def test_factory_function_missing_dependencies(self):
        """Test factory function with missing dependencies"""
        with self.assertRaises(RuntimeError):
            create_learning_system_manager(None, self.mock_shared_utilities)
        
        with self.assertRaises(RuntimeError):
            create_learning_system_manager(self.mock_unified_config, None)
    
    def test_dependency_injection_working(self):
        """Test that dependency injection works correctly"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        # Test that manager uses injected dependencies
        status = manager.get_learning_status()
        self.assertIn('enabled', status)
        
        # Verify UnifiedConfigManager was called
        self.mock_unified_config.get_env_bool.assert_called()
        self.mock_unified_config.get_env_float.assert_called()
    
    # ========================================================================
    # LEARNING PARAMETER ACCESS TESTS
    # ========================================================================
    
    def test_get_learning_parameters_integration(self):
        """Test learning parameter access via UnifiedConfigManager"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        params = manager.get_learning_parameters()
        
        # Verify all expected parameters are present
        expected_keys = [
            'enabled', 'learning_rate', 'min_confidence_adjustment',
            'max_confidence_adjustment', 'max_adjustments_per_day',
            'persistence_file', 'feedback_weight', 'min_samples',
            'adjustment_limit', 'max_drift', 'sensitivity_bounds',
            'adjustment_factors', 'severity_multipliers'
        ]
        
        for key in expected_keys:
            self.assertIn(key, params)
        
        # Verify specific values
        self.assertEqual(params['learning_rate'], 0.01)
        self.assertEqual(params['enabled'], True)
        self.assertEqual(params['max_adjustments_per_day'], 50)
    
    def test_validate_learning_parameters_integration(self):
        """Test learning parameter validation using SharedUtilities"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        validation_result = manager.validate_learning_parameters()
        
        # Verify validation structure
        self.assertIn('valid', validation_result)
        self.assertIn('errors', validation_result)
        self.assertIn('warnings', validation_result)
        self.assertIn('parameter_count', validation_result)
        
        # Verify SharedUtilities validate_range was called
        self.mock_shared_utilities.validate_range.assert_called()
    
    # ========================================================================
    # FALSE POSITIVE/NEGATIVE ADJUSTMENT TESTS
    # ========================================================================
    
    def test_false_positive_threshold_adjustment(self):
        """Test false positive threshold adjustment functionality"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        # Test adjustment
        original_threshold = 0.5
        adjusted_threshold = manager.adjust_threshold_false_positive(original_threshold, "high")
        
        # Should be reduced (false positive factor is negative)
        self.assertLess(adjusted_threshold, original_threshold)
        
        # Should be within reasonable bounds
        self.assertGreater(adjusted_threshold, 0.0)
        self.assertLess(adjusted_threshold, 1.0)
    
    def test_false_negative_threshold_adjustment(self):
        """Test false negative threshold adjustment functionality"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        # Test adjustment
        original_threshold = 0.5
        adjusted_threshold = manager.adjust_threshold_false_negative(original_threshold, "high")
        
        # Should be increased (false negative factor is positive)
        self.assertGreater(adjusted_threshold, original_threshold)
        
        # Should be within reasonable bounds
        self.assertGreater(adjusted_threshold, 0.0)
        self.assertLess(adjusted_threshold, 1.0)
    
    def test_feedback_processing_integration(self):
        """Test feedback processing with both types"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        # Test false positive feedback
        fp_data = {
            'current_threshold': 0.6,
            'severity': 'medium'
        }
        
        result = manager.process_feedback('false_positive', fp_data)
        self.assertTrue(result)
        self.assertIn('adjusted_threshold', fp_data)
        self.assertIn('adjustment_made', fp_data)
        
        # Test false negative feedback
        fn_data = {
            'current_threshold': 0.4,
            'severity': 'high'
        }
        
        result = manager.process_feedback('false_negative', fn_data)
        self.assertTrue(result)
        self.assertIn('adjusted_threshold', fn_data)
        self.assertIn('adjustment_made', fn_data)
    
    def test_daily_adjustment_limits(self):
        """Test that daily adjustment limits are enforced"""
        # Mock to simulate reaching daily limit
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        # Fill up daily adjustment count
        today = datetime.now().strftime('%Y-%m-%d')
        manager.adjustment_counts[today] = 50  # Max limit
        
        # Try to make adjustment
        original_threshold = 0.5
        adjusted_threshold = manager.adjust_threshold_false_positive(original_threshold, "medium")
        
        # Should return unchanged threshold when limit reached
        self.assertEqual(adjusted_threshold, original_threshold)
    
    # ========================================================================
    # INTEGRATION WITH ORIGIN MANAGERS TESTS
    # ========================================================================
    
    def test_analysis_parameters_manager_learning_methods_removed(self):
        """Test that AnalysisParametersManager no longer provides learning methods"""
        # Create mock for AnalysisParametersManager test
        mock_config = Mock(spec=UnifiedConfigManager)
        mock_config.substitute_environment_variables.return_value = {
            'ensemble_analysis': {'voting_strategy': 'weighted_average'},
            'confidence_scoring': {'base_confidence_weight': 0.6},
            'pattern_matching': {'case_sensitive': False}
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open_json({})):
            
            manager = AnalysisParametersManager(mock_config)
            
            # Test that learning methods return references
            learning_params = manager.get_learning_system_parameters()
            self.assertIn('use_instead', learning_params)
            self.assertIn('LearningSystemManager', learning_params['use_instead'])
            
            learning_validation = manager.validate_learning_system_parameters()
            self.assertIn('use_instead', learning_validation)
            self.assertIn('LearningSystemManager', learning_validation['use_instead'])
    
    def test_threshold_mapping_manager_learning_integration(self):
        """Test that ThresholdMappingManager provides learning integration info"""
        mock_config = Mock(spec=UnifiedConfigManager)
        mock_config.substitute_environment_variables.return_value = {
            'threshold_mapping_by_mode': {
                'consensus': {
                    'crisis_level_mapping': {
                        'crisis_to_high': 0.5,
                        'crisis_to_medium': 0.3
                    }
                }
            },
            'learning_thresholds': {
                'learning_rate': 0.1,
                'max_adjustments_per_day': 50
            }
        }
        mock_config.get_env_str.return_value = 'consensus'
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open_json({})):
            
            manager = ThresholdMappingManager(mock_config)
            
            # Test learning integration info
            adaptive_info = manager.get_adaptive_threshold_info()
            self.assertIn('LearningSystemManager', adaptive_info['note'])
            self.assertIn('workflow', adaptive_info)
            
            # Test learning thresholds include reference
            learning_thresholds = manager.get_learning_thresholds()
            self.assertIn('note', learning_thresholds)
            self.assertIn('LearningSystemManager', learning_thresholds['note'])
    
    # ========================================================================
    # PERSISTENCE AND HISTORY TESTS
    # ========================================================================
    
    def test_adjustment_persistence(self):
        """Test that adjustments are persisted correctly"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        # Make an adjustment
        manager.adjust_threshold_false_positive(0.5, "medium")
        
        # Check that persistence file was created and contains data
        self.assertTrue(os.path.exists(self.persistence_file))
        
        with open(self.persistence_file, 'r') as f:
            data = json.load(f)
        
        self.assertIn('history', data)
        self.assertIn('adjustment_counts', data)
        self.assertIn('last_adjustment_time', data)
        self.assertGreater(len(data['history']), 0)
    
    def test_adjustment_history_loading(self):
        """Test loading of existing adjustment history"""
        # Create existing history file
        history_data = {
            'history': [
                {
                    'timestamp': '2025-08-17T10:00:00',
                    'type': 'false_positive',
                    'old_threshold': 0.5,
                    'new_threshold': 0.45,
                    'severity': 'medium'
                }
            ],
            'adjustment_counts': {'2025-08-17': 1},
            'last_adjustment_time': {'false_positive': '2025-08-17T10:00:00'}
        }
        
        with open(self.persistence_file, 'w') as f:
            json.dump(history_data, f)
        
        # Create manager and verify history is loaded
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        history = manager.get_adjustment_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['type'], 'false_positive')
    
    # ========================================================================
    # STATUS AND HEALTH TESTS
    # ========================================================================
    
    def test_learning_status_reporting(self):
        """Test learning system status reporting"""
        manager = LearningSystemManager(self.mock_unified_config, self.mock_shared_utilities)
        
        status = manager.get_learning_status()
        
        required_fields = [
            'enabled', 'adjustments_today', 'adjustments_remaining',
            'total_adjustments', 'learning_rate', 'status'
        ]
        
        for field in required_fields:
            self.assertIn(field, status)
        
        self.assertEqual(status['status'], 'healthy')
        self.assertEqual(status['enabled'], True)
        self.assertEqual(status['adjustments_remaining'], 50)  # No adjustments made yet
    
    def test_error_handling_integration(self):
        """Test error handling using SharedUtilities"""
        # Create manager with error-prone config
        error_config = Mock(spec=UnifiedConfigManager)
        error_config.get_env_bool.side_effect = Exception("Config error")
        
        manager = LearningSystemManager(error_config, self.mock_shared_utilities)
        
        # Verify SharedUtilities handle_error_with_fallback was called
        self.mock_shared_utilities.handle_error_with_fallback.assert_called()
        
        # Manager should still function with fallback config
        status = manager.get_learning_status()
        self.assertIn('status', status)


# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def mock_open_json(json_data):
    """Helper function to mock JSON file opening"""
    from unittest.mock import mock_open
    return mock_open(read_data=json.dumps(json_data))


# ========================================================================
# TEST SUITE EXECUTION
# ========================================================================

if __name__ == '__main__':
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLearningSystemManagerIntegration)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"LEARNING SYSTEM MANAGER INTEGRATION TEST RESULTS")
    print(f"="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"✅ ALL INTEGRATION TESTS PASSED!")
        print(f"🎉 LearningSystemManager integration is working correctly!")
    else:
        print(f"❌ Some tests failed. Check output above for details.")
    
    print(f"="*60)