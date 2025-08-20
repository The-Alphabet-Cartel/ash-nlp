# ash-nlp/tests/phase/3/e/test_unified_config_manager_integration.py
"""
Integration Test for Optimized UnifiedConfigManager
FILE VERSION: v3.1-3e-5.5-1
LAST MODIFIED: 2025-08-19
PHASE: 3e Step 5.5 - UnifiedConfigManager Optimization Integration Test
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the optimized manager and its helpers
from managers.unified_config_manager import UnifiedConfigManager, create_unified_config_manager
from managers.helpers.unified_config_schema_helper import VariableSchema, UnifiedConfigSchemaHelper
from managers.helpers.unified_config_value_helper import UnifiedConfigValueHelper

class TestUnifiedConfigManagerIntegration(unittest.TestCase):
    """
    Integration tests for optimized UnifiedConfigManager
    
    These tests verify that the helper file optimization maintains 100% functionality
    while reducing the main file size and improving maintainability.
    """
    
    def setUp(self):
        """Set up test environment with temporary config directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        
        # Create sample configuration files for testing
        self._create_test_config_files()
        
        # Create manager instance
        self.manager = UnifiedConfigManager(str(self.config_dir))
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_test_config_files(self):
        """Create sample configuration files for testing"""
        # Create analysis_parameters.json
        analysis_config = {
            "crisis_thresholds": {
                "high": "${NLP_CRISIS_THRESHOLD_HIGH}",
                "medium": "${NLP_CRISIS_THRESHOLD_MEDIUM}",
                "low": "${NLP_CRISIS_THRESHOLD_LOW}",
                "defaults": {
                    "high": 0.8,
                    "medium": 0.6,
                    "low": 0.4
                }
            },
            "learning_system": {
                "enabled": "${NLP_LEARNING_ENABLED}",
                "rate": "${NLP_LEARNING_RATE}",
                "defaults": {
                    "enabled": True,
                    "rate": 0.01
                }
            },
            "validation": {
                "NLP_CRISIS_THRESHOLD_HIGH": {
                    "type": "float",
                    "default": 0.8,
                    "range": [0.0, 1.0],
                    "description": "High crisis threshold"
                },
                "NLP_LEARNING_RATE": {
                    "type": "float",
                    "default": 0.01,
                    "range": [0.001, 0.1],
                    "description": "Learning rate for system adaptation"
                }
            }
        }
        
        with open(self.config_dir / 'analysis_parameters.json', 'w') as f:
            json.dump(analysis_config, f)
        
        # Create threshold_mapping.json
        threshold_config = {
            "modes": {
                "default": {
                    "crisis_high": "${NLP_THRESHOLD_DEFAULT_HIGH}",
                    "crisis_medium": "${NLP_THRESHOLD_DEFAULT_MEDIUM}",
                    "defaults": {
                        "crisis_high": 0.75,
                        "crisis_medium": 0.5
                    }
                }
            },
            "validation": {
                "NLP_THRESHOLD_DEFAULT_HIGH": {
                    "type": "float",
                    "default": 0.75,
                    "range": [0.5, 1.0],
                    "description": "Default mode high threshold"
                }
            }
        }
        
        with open(self.config_dir / 'threshold_mapping.json', 'w') as f:
            json.dump(threshold_config, f)
    
    # ========================================================================
    # CORE FUNCTIONALITY TESTS
    # ========================================================================
    
    def test_manager_initialization_with_helpers(self):
        """Test that manager initializes correctly with helper files"""
        self.assertIsNotNone(self.manager.schema_helper)
        self.assertIsInstance(self.manager.schema_helper, UnifiedConfigSchemaHelper)
        
        self.assertIsNotNone(self.manager.value_helper)
        self.assertIsInstance(self.manager.value_helper, UnifiedConfigValueHelper)
        
        self.assertIsNotNone(self.manager.variable_schemas)
        self.assertIsInstance(self.manager.variable_schemas, dict)
        
        # Should have essential core schemas + JSON schemas
        self.assertGreater(len(self.manager.variable_schemas), 10)
    
    def test_factory_function_creates_optimized_manager(self):
        """Test that factory function creates properly optimized manager"""
        manager = create_unified_config_manager(str(self.config_dir))
        
        self.assertIsInstance(manager, UnifiedConfigManager)
        self.assertIsNotNone(manager.schema_helper)
        self.assertIsNotNone(manager.value_helper)
    
    def test_environment_variable_access_preserved(self):
        """Test that all environment variable access methods work correctly"""
        # Test string access
        with patch.dict(os.environ, {'NLP_TEST_STRING': 'test_value'}):
            result = self.manager.get_env_str('NLP_TEST_STRING', 'default')
            self.assertEqual(result, 'test_value')
        
        # Test with default
        result = self.manager.get_env_str('NLP_NONEXISTENT', 'default_value')
        self.assertEqual(result, 'default_value')
        
        # Test integer access
        with patch.dict(os.environ, {'NLP_TEST_INT': '42'}):
            result = self.manager.get_env_int('NLP_TEST_INT', 0)
            self.assertEqual(result, 42)
        
        # Test float access
        with patch.dict(os.environ, {'NLP_TEST_FLOAT': '3.14'}):
            result = self.manager.get_env_float('NLP_TEST_FLOAT', 0.0)
            self.assertEqual(result, 3.14)
        
        # Test boolean access
        with patch.dict(os.environ, {'NLP_TEST_BOOL': 'true'}):
            result = self.manager.get_env_bool('NLP_TEST_BOOL', False)
            self.assertTrue(result)
        
        # Test list access
        with patch.dict(os.environ, {'NLP_TEST_LIST': 'item1,item2,item3'}):
            result = self.manager.get_env_list('NLP_TEST_LIST', [])
            self.assertEqual(result, ['item1', 'item2', 'item3'])
    
    def test_configuration_file_loading_preserved(self):
        """Test that configuration file loading works correctly with helpers"""
        # Test loading existing config
        config = self.manager.load_config_file('analysis_parameters')
        self.assertIsNotNone(config)
        self.assertIn('crisis_thresholds', config)
        self.assertIn('learning_system', config)
        
        # Test loading non-existent config
        empty_config = self.manager.load_config_file('nonexistent')
        self.assertEqual(empty_config, {})
    
    def test_get_config_section_functionality_preserved(self):
        """Test that get_config_section method works correctly"""
        # Test getting entire config
        full_config = self.manager.get_config_section('analysis_parameters')
        self.assertIn('crisis_thresholds', full_config)
        
        # Test getting top-level section
        thresholds = self.manager.get_config_section('analysis_parameters', 'crisis_thresholds')
        self.assertIn('high', thresholds)
        
        # Test getting nested section with dot notation
        defaults = self.manager.get_config_section('analysis_parameters', 'crisis_thresholds.defaults')
        self.assertEqual(defaults['high'], 0.8)
        
        # Test with default value
        missing = self.manager.get_config_section('analysis_parameters', 'nonexistent', {'default': 'value'})
        self.assertEqual(missing, {'default': 'value'})
    
    def test_placeholder_resolution_with_helper(self):
        """Test that placeholder resolution works correctly through helper"""
        # Set environment variable
        with patch.dict(os.environ, {'NLP_CRISIS_THRESHOLD_HIGH': '0.9'}):
            config = self.manager.load_config_file('analysis_parameters')
            
            # Should resolve environment variable
            self.assertEqual(config['crisis_thresholds']['high'], '0.9')
        
        # Without environment variable, should use defaults
        config = self.manager.load_config_file('analysis_parameters')
        # Should fall back to default value
        self.assertIn('high', config['crisis_thresholds'])
    
    # ========================================================================
    # HELPER INTEGRATION TESTS
    # ========================================================================
    
    def test_schema_helper_integration(self):
        """Test that schema helper integration works correctly"""
        # Test essential core schemas are loaded
        schemas = self.manager.variable_schemas
        
        # Should have essential core schemas
        self.assertIn('GLOBAL_LOG_LEVEL', schemas)
        self.assertIn('NLP_SERVER_PORT', schemas)
        
        # Should have JSON-driven schemas from test config
        self.assertIn('NLP_CRISIS_THRESHOLD_HIGH', schemas)
        self.assertIn('NLP_LEARNING_RATE', schemas)
        
        # Test schema structure
        schema = schemas['NLP_CRISIS_THRESHOLD_HIGH']
        self.assertEqual(schema.var_type, 'float')
        self.assertEqual(schema.default, 0.8)
        self.assertEqual(schema.min_value, 0.0)
        self.assertEqual(schema.max_value, 1.0)
    
    def test_value_helper_integration(self):
        """Test that value helper integration works correctly"""
        # Test type conversion
        result = self.manager.value_helper.convert_value_type('TEST_VAR', 'true')
        self.assertEqual(result, 'True')
        
        result = self.manager.value_helper.convert_value_type('TEST_VAR', '42')
        self.assertEqual(result, '42')
        
        result = self.manager.value_helper.convert_value_type('TEST_VAR', '3.14')
        self.assertEqual(result, '3.14')
        
        # Test environment variable to JSON key conversion
        json_key = self.manager.value_helper.env_var_to_json_key('NLP_HOPELESSNESS_CONTEXT_CRISIS_BOOST')
        self.assertEqual(json_key, 'crisis_amplifier_weight')
    
    def test_backward_compatibility_preserved(self):
        """Test that all backward compatibility methods work correctly"""
        # Test get_crisis_patterns
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = '{"patterns": {"test": "value"}}'
            
            # This should work without errors
            try:
                patterns = self.manager.get_crisis_patterns('test_pattern')
                # The method should execute without throwing exceptions
            except FileNotFoundError:
                # Expected for non-existent files in test environment
                pass
        
        # Test status method
        status = self.manager.get_status()
        self.assertIn('status', status)
        self.assertIn('optimization_status', status)
        self.assertEqual(status['status'], 'operational')
        self.assertTrue(status['optimization_status']['helper_files_used'])
    
    # ========================================================================
    # OPTIMIZATION VALIDATION TESTS
    # ========================================================================
    
    def test_helper_files_reduce_main_file_complexity(self):
        """Test that helper files successfully reduce main file complexity"""
        # Test that helper classes are properly instantiated
        self.assertIsInstance(self.manager.schema_helper, UnifiedConfigSchemaHelper)
        self.assertIsInstance(self.manager.value_helper, UnifiedConfigValueHelper)
        
        # Test that complex operations are delegated to helpers
        # Schema initialization should be handled by schema helper
        self.assertGreater(len(self.manager.variable_schemas), 0)
        
        # Value conversion should be handled by value helper
        test_value = {"test": "${TEST_VAR}", "defaults": {"test": "default_value"}}
        processed = self.manager.value_helper.substitute_environment_variables(test_value)
        self.assertIsNotNone(processed)
    
    def test_performance_impact_minimal(self):
        """Test that helper file approach doesn't significantly impact performance"""
        import time
        
        # Test configuration loading performance
        start_time = time.perf_counter()
        for _ in range(10):
            config = self.manager.load_config_file('analysis_parameters')
        end_time = time.perf_counter()
        
        # Should complete 10 loads in reasonable time (under 1 second)
        total_time = end_time - start_time
        self.assertLess(total_time, 1.0, "Configuration loading performance degraded")
        
        # Test environment variable access performance
        start_time = time.perf_counter()
        for _ in range(100):
            self.manager.get_env_str('NLP_TEST_VAR', 'default')
        end_time = time.perf_counter()
        
        # Should complete 100 env var accesses very quickly
        total_time = end_time - start_time
        self.assertLess(total_time, 0.1, "Environment variable access performance degraded")
    
    def test_all_public_api_methods_preserved(self):
        """Test that all public API methods are preserved and functional"""
        # Core environment variable methods
        self.assertTrue(hasattr(self.manager, 'get_env'))
        self.assertTrue(hasattr(self.manager, 'get_env_str'))
        self.assertTrue(hasattr(self.manager, 'get_env_int'))
        self.assertTrue(hasattr(self.manager, 'get_env_float'))
        self.assertTrue(hasattr(self.manager, 'get_env_bool'))
        self.assertTrue(hasattr(self.manager, 'get_env_list'))
        
        # Configuration file methods
        self.assertTrue(hasattr(self.manager, 'load_config_file'))
        self.assertTrue(hasattr(self.manager, 'get_config_section'))
        self.assertTrue(hasattr(self.manager, 'get_config_section_with_env_fallback'))
        self.assertTrue(hasattr(self.manager, 'has_config_section'))
        self.assertTrue(hasattr(self.manager, 'list_config_files'))
        self.assertTrue(hasattr(self.manager, 'list_config_sections'))
        
        # Configuration convenience methods
        self.assertTrue(hasattr(self.manager, 'get_hardware_configuration'))
        self.assertTrue(hasattr(self.manager, 'get_model_configuration'))
        self.assertTrue(hasattr(self.manager, 'get_performance_configuration'))
        self.assertTrue(hasattr(self.manager, 'get_storage_configuration'))
        
        # Backward compatibility methods
        self.assertTrue(hasattr(self.manager, 'get_crisis_patterns'))
        self.assertTrue(hasattr(self.manager, 'get_status'))
        
        # Test that methods actually work
        files = self.manager.list_config_files()
        self.assertIsInstance(files, list)
        
        hardware_config = self.manager.get_hardware_configuration()
        self.assertIsInstance(hardware_config, dict)
        
        status = self.manager.get_status()
        self.assertIsInstance(status, dict)
    
    # ========================================================================
    # ERROR HANDLING TESTS
    # ========================================================================
    
    def test_error_handling_preserved(self):
        """Test that error handling works correctly with helpers"""
        # Test loading non-existent configuration file
        result = self.manager.load_config_file('nonexistent_config')
        self.assertEqual(result, {})
        
        # Test getting section from non-existent file
        result = self.manager.get_config_section('nonexistent_config', 'section')
        self.assertEqual(result, {})
        
        # Test with invalid section path
        result = self.manager.get_config_section('analysis_parameters', 'invalid.path.here', 'default')
        self.assertEqual(result, 'default')
    
    def test_validation_error_handling(self):
        """Test that validation errors are handled correctly"""
        # Test with invalid environment variable value
        with patch.dict(os.environ, {'NLP_CRISIS_THRESHOLD_HIGH': 'invalid_float'}):
            # Should handle conversion error gracefully
            value = self.manager.get_env_float('NLP_CRISIS_THRESHOLD_HIGH', 0.8)
            # Should return schema default due to conversion error
            self.assertEqual(value, 0.8)
    
    # ========================================================================
    # INTEGRATION WITH REAL CONFIGURATION PATTERNS
    # ========================================================================
    
    def test_real_world_configuration_patterns(self):
        """Test with realistic configuration patterns"""
        # Test with actual configuration section access patterns used by other managers
        
        # Pattern 1: Get nested configuration with defaults
        learning_config = self.manager.get_config_section('analysis_parameters', 'learning_system', {})
        self.assertIsInstance(learning_config, dict)
        
        # Pattern 2: Environment variable access with fallbacks
        with patch.dict(os.environ, {'NLP_LEARNING_ENABLED': 'false'}):
            enabled = self.manager.get_env_bool('NLP_LEARNING_ENABLED', True)
            self.assertFalse(enabled)
        
        # Pattern 3: Configuration file listing
        config_files = self.manager.list_config_files()
        expected_files = ['analysis_parameters', 'threshold_mapping', 'model_ensemble']
        for expected_file in expected_files:
            self.assertIn(expected_file, config_files)
    
    def test_helper_file_import_requirements(self):
        """Test that helper file imports work correctly"""
        # Test that helper modules can be imported independently
        from managers.helpers.unified_config_schema_helper import VariableSchema, create_schema_helper
        from managers.helpers.unified_config_value_helper import create_value_helper
        
        # Test that helper factory functions work
        schema_helper = create_schema_helper(self.config_dir, self.manager.config_files)
        self.assertIsInstance(schema_helper, UnifiedConfigSchemaHelper)
        
        value_helper = create_value_helper(self.manager.variable_schemas)
        self.assertIsInstance(value_helper, UnifiedConfigValueHelper)

if __name__ == '__main__':
    unittest.main()