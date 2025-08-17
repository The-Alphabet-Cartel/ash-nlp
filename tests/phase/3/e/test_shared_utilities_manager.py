"""
Integration tests for SharedUtilitiesManager
FILE VERSION: v3.1-3e-2.3-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 2.3 - SharedUtilitiesManager Integration Testing
CLEAN ARCHITECTURE: v3.1 Compliant
TEST COVERAGE: All 15 utility methods + factory function + integration
"""

import unittest
import tempfile
import json
import os
import time
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Import the manager under test
from managers.shared_utilities import (
    SharedUtilitiesManager, 
    create_shared_utilities_manager,
    ConfigurationError
)

# Mock unified config manager for testing
class MockUnifiedConfigManager:
    """Mock UnifiedConfigManager for testing"""
    
    def __init__(self, env_dict=None, env_vars=None):
        self.env_dict = env_dict or {}
        self.env_vars = env_vars or {}
    
    def get_env_dict(self):
        return self.env_dict
    
    def get_env_str(self, key, default=None):
        return self.env_vars.get(key, default)


class TestSharedUtilitiesManager(unittest.TestCase):
    """Test suite for SharedUtilitiesManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_config = MockUnifiedConfigManager(
            env_dict={
                'test_section': {
                    'string_value': 'test',
                    'int_value': 42,
                    'float_value': 3.14,
                    'bool_value': True
                },
                'performance': {
                    'threads': 4,
                    'timeout': 30.0,
                    'enabled': True
                },
                'nested': {
                    'level1': {
                        'level2': {
                            'value': 'deep_value'
                        }
                    }
                }
            },
            env_vars={
                'TEST_OVERRIDE': 'override_value',
                'BOOL_TRUE': 'true',
                'BOOL_FALSE': 'false',
                'INT_VALUE': '123',
                'FLOAT_VALUE': '45.67'
            }
        )
        
        self.manager = SharedUtilitiesManager(self.mock_config)
    
    def tearDown(self):
        """Clean up after tests"""
        self.manager = None
    
    # ========================================================================
    # FACTORY FUNCTION TESTS
    # ========================================================================
    
    def test_factory_function_with_config(self):
        """Test factory function with provided config"""
        manager = create_shared_utilities_manager(self.mock_config)
        
        self.assertIsInstance(manager, SharedUtilitiesManager)
        self.assertEqual(manager.config_manager, self.mock_config)
        
        status = manager.get_status()
        self.assertEqual(status['status'], 'healthy')
        self.assertEqual(status['utilities_available'], 15)
    
    @patch('managers.shared_utilities.create_unified_config_manager')
    def test_factory_function_without_config(self, mock_create_config):
        """Test factory function creates config when none provided"""
        mock_create_config.return_value = self.mock_config
        
        manager = create_shared_utilities_manager()
        
        self.assertIsInstance(manager, SharedUtilitiesManager)
        mock_create_config.assert_called_once()
    
    def test_factory_function_invalid_config(self):
        """Test factory function with invalid config"""
        invalid_config = Mock()
        # Remove required method
        del invalid_config.get_env_str
        
        with self.assertRaises(ConfigurationError):
            create_shared_utilities_manager(invalid_config)
    
    def test_factory_function_none_config_input(self):
        """Test factory function handles None config gracefully"""
        with patch('managers.shared_utilities.create_unified_config_manager') as mock_create:
            mock_create.return_value = self.mock_config
            
            manager = create_shared_utilities_manager(None)
            self.assertIsInstance(manager, SharedUtilitiesManager)
    
    # ========================================================================
    # PREMIUM UTILITIES TESTS (Tier 1 - Best-in-Class)
    # ========================================================================
    
    def test_safe_bool_convert_various_inputs(self):
        """Test safe_bool_convert with various input types"""
        # Test cases: (input, expected_output)
        test_cases = [
            # Boolean inputs
            (True, True),
            (False, False),
            
            # String inputs - true values
            ('true', True),
            ('TRUE', True),
            ('yes', True),
            ('YES', True),
            ('on', True),
            ('ON', True),
            ('1', True),
            ('enabled', True),
            ('ENABLED', True),
            ('active', True),
            ('ACTIVE', True),
            
            # String inputs - false values
            ('false', False),
            ('FALSE', False),
            ('no', False),
            ('NO', False),
            ('off', False),
            ('OFF', False),
            ('0', False),
            ('disabled', False),
            ('DISABLED', False),
            ('inactive', False),
            ('INACTIVE', False),
            
            # Numeric inputs
            (1, True),
            (0, False),
            (42, True),
            (-1, True),
            (1.0, True),
            (0.0, False),
            (3.14, True),
            
            # Invalid inputs (should use default)
            ('invalid', False),  # Using default False
            ('maybe', False),     # Using default False
            (None, False),        # Using default False
            ([], False),          # Using default False
            ({}, False),          # Using default False
        ]
        
        for input_value, expected in test_cases:
            with self.subTest(input_value=input_value):
                result = self.manager.safe_bool_convert(input_value, default=False)
                self.assertEqual(result, expected, 
                               f"safe_bool_convert({input_value}) should return {expected}, got {result}")
    
    def test_safe_bool_convert_custom_default(self):
        """Test safe_bool_convert with custom default value"""
        result = self.manager.safe_bool_convert('invalid_input', default=True, param_name='test_param')
        self.assertTrue(result)
        
        result = self.manager.safe_bool_convert('invalid_input', default=False, param_name='test_param')
        self.assertFalse(result)
    
    def test_get_setting_with_type_conversion(self):
        """Test get_setting_with_type_conversion for various types"""
        # Test integer conversion
        result = self.manager.get_setting_with_type_conversion(
            'performance', 'threads', int, default=1
        )
        self.assertEqual(result, 4)
        self.assertIsInstance(result, int)
        
        # Test float conversion
        result = self.manager.get_setting_with_type_conversion(
            'performance', 'timeout', float, default=10.0
        )
        self.assertEqual(result, 30.0)
        self.assertIsInstance(result, float)
        
        # Test boolean conversion
        result = self.manager.get_setting_with_type_conversion(
            'performance', 'enabled', bool, default=False
        )
        self.assertTrue(result)
        self.assertIsInstance(result, bool)
        
        # Test string conversion
        result = self.manager.get_setting_with_type_conversion(
            'test_section', 'string_value', str, default='default'
        )
        self.assertEqual(result, 'test')
        self.assertIsInstance(result, str)
        
        # Test missing key uses default
        result = self.manager.get_setting_with_type_conversion(
            'missing_section', 'missing_key', int, default=999
        )
        self.assertEqual(result, 999)
    
    def test_get_nested_config_setting(self):
        """Test get_nested_config_setting with various paths"""
        # Test existing nested path
        result = self.manager.get_nested_config_setting(
            'nested.level1.level2.value'
        )
        self.assertEqual(result, 'deep_value')
        
        # Test missing path with default
        result = self.manager.get_nested_config_setting(
            'missing.path', default='fallback'
        )
        self.assertEqual(result, 'fallback')
        
        # Test fallback paths
        result = self.manager.get_nested_config_setting(
            'missing.path',
            default='final_fallback',
            fallback_paths=['also.missing', 'test_section.string_value']
        )
        self.assertEqual(result, 'test')  # Should find test_section.string_value
    
    def test_get_boolean_setting(self):
        """Test get_boolean_setting with environment overrides"""
        # Test normal boolean setting
        result = self.manager.get_boolean_setting('bool_value', default=False)
        # This will look for bool_value in config, but our mock doesn't have it at root level
        self.assertFalse(result)  # Should use default
        
        # Test environment override
        result = self.manager.get_boolean_setting('BOOL_TRUE', default=False, environment_override=True)
        self.assertTrue(result)  # Should get 'true' from env_vars
        
        result = self.manager.get_boolean_setting('BOOL_FALSE', default=True, environment_override=True)
        self.assertFalse(result)  # Should get 'false' from env_vars
        
        # Test no environment override
        result = self.manager.get_boolean_setting('BOOL_TRUE', default=False, environment_override=False)
        self.assertFalse(result)  # Should use default since not in config
    
    # ========================================================================
    # CONFIGURATION PROCESSING UTILITIES TESTS
    # ========================================================================
    
    def test_load_json_with_env_substitution(self):
        """Test load_json_with_env_substitution"""
        # Create temporary JSON file
        test_config = {
            'database': {
                'host': '${DB_HOST:localhost}',
                'port': '${DB_PORT:5432}',
                'name': 'test_db'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        try:
            # Test without environment variables (should use defaults)
            result = self.manager.load_json_with_env_substitution(temp_file, env_prefix='DB_')
            expected = {
                'database': {
                    'host': 'localhost',  # Default value
                    'port': '5432',       # Default value
                    'name': 'test_db'
                }
            }
            self.assertEqual(result, expected)
            
            # Test missing file (not required)
            result = self.manager.load_json_with_env_substitution('nonexistent.json', required=False)
            self.assertEqual(result, {})
            
            # Test missing file (required) - should raise error
            with self.assertRaises(ConfigurationError):
                self.manager.load_json_with_env_substitution('nonexistent.json', required=True)
                
        finally:
            os.unlink(temp_file)
    
    def test_get_config_section_safely(self):
        """Test get_config_section_safely"""
        # Test existing section
        result = self.manager.get_config_section_safely('test_section')
        expected = {
            'string_value': 'test',
            'int_value': 42,
            'float_value': 3.14,
            'bool_value': True
        }
        self.assertEqual(result, expected)
        
        # Test missing section with fallback
        fallback = {'fallback_key': 'fallback_value'}
        result = self.manager.get_config_section_safely('missing_section', fallback=fallback)
        self.assertEqual(result, fallback)
        
        # Test missing section without fallback
        result = self.manager.get_config_section_safely('missing_section')
        self.assertEqual(result, {})
    
    def test_apply_env_overrides(self):
        """Test apply_env_overrides"""
        base_config = {
            'section1': {'key1': 'original_value'},
            'section2': {'key2': 42}
        }
        
        # Mock environment variables
        with patch.dict(os.environ, {
            'TEST_SECTION1_KEY1': 'overridden_value',
            'TEST_SECTION2_KEY2': '999',
            'TEST_NEW_KEY': 'new_value'
        }):
            result = self.manager.apply_env_overrides(base_config, 'TEST_')
            
            # Check overrides applied
            self.assertEqual(result['section1']['key1'], 'overridden_value')
            self.assertEqual(result['section2']['key2'], '999')  # String from env
            self.assertEqual(result['new']['key'], 'new_value')  # New nested structure
    
    def test_get_with_fallback(self):
        """Test get_with_fallback"""
        # Test primary key exists
        result = self.manager.get_with_fallback(
            'test_section', 
            ['fallback1', 'fallback2'], 
            default='default_value'
        )
        # Should return the test_section dict
        self.assertIsInstance(result, dict)
        
        # Test fallback chain
        result = self.manager.get_with_fallback(
            'missing_primary',
            ['missing_fallback1', 'performance', 'missing_fallback2'],
            default='default_value'
        )
        # Should find 'performance' in fallback chain
        self.assertIsInstance(result, dict)
        self.assertIn('threads', result)
        
        # Test all keys missing
        result = self.manager.get_with_fallback(
            'missing_primary',
            ['missing_fallback1', 'missing_fallback2'],
            default='default_value'
        )
        self.assertEqual(result, 'default_value')
    
    def test_validate_config_structure(self):
        """Test validate_config_structure"""
        config_data = {
            'required_section1': {'key1': 'value1'},
            'required_section2': {'key2': 42},
            'optional_section': {'key3': True}
        }
        
        # Test valid configuration
        issues = self.manager.validate_config_structure(
            config_data,
            required_sections=['required_section1', 'required_section2']
        )
        self.assertEqual(issues, [])
        
        # Test missing required section
        issues = self.manager.validate_config_structure(
            config_data,
            required_sections=['required_section1', 'missing_section']
        )
        self.assertEqual(len(issues), 1)
        self.assertIn('Missing required section: missing_section', issues)
        
        # Test invalid section type
        invalid_config = {
            'required_section1': 'not_a_dict',  # Should be dict
            'required_section2': {'key2': 42}
        }
        issues = self.manager.validate_config_structure(
            invalid_config,
            required_sections=['required_section1', 'required_section2']
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("Section 'required_section1' must be a dictionary", issues)
        
        # Test with schema
        schema = {
            'required_section1': {'key1': str},
            'required_section2': {'key2': int}
        }
        issues = self.manager.validate_config_structure(
            config_data,
            required_sections=['required_section1', 'required_section2'],
            schema=schema
        )
        self.assertEqual(issues, [])  # Should pass validation
    
    # ========================================================================
    # TYPE CONVERSION UTILITIES TESTS
    # ========================================================================
    
    def test_safe_int_convert(self):
        """Test safe_int_convert with various inputs and range validation"""
        # Test valid conversions
        test_cases = [
            (42, 42),           # int
            (3.14, 3),          # float -> int
            ('123', 123),       # string -> int
            ('45.67', 45),      # string float -> int
            (True, 1),          # bool -> int
            (False, 0),         # bool -> int
        ]
        
        for input_value, expected in test_cases:
            with self.subTest(input_value=input_value):
                result = self.manager.safe_int_convert(input_value, default=0)
                self.assertEqual(result, expected)
        
        # Test invalid conversions use default
        invalid_inputs = ['not_a_number', None, [], {}]
        for invalid_input in invalid_inputs:
            with self.subTest(input_value=invalid_input):
                result = self.manager.safe_int_convert(invalid_input, default=999)
                self.assertEqual(result, 999)
        
        # Test range validation
        result = self.manager.safe_int_convert(5, default=0, min_val=10, max_val=20)
        self.assertEqual(result, 10)  # Should clamp to minimum
        
        result = self.manager.safe_int_convert(25, default=0, min_val=10, max_val=20)
        self.assertEqual(result, 20)  # Should clamp to maximum
        
        result = self.manager.safe_int_convert(15, default=0, min_val=10, max_val=20)
        self.assertEqual(result, 15)  # Should remain unchanged
    
    def test_safe_float_convert(self):
        """Test safe_float_convert with various inputs and range validation"""
        # Test valid conversions
        test_cases = [
            (42, 42.0),         # int -> float
            (3.14, 3.14),       # float
            ('123', 123.0),     # string -> float
            ('45.67', 45.67),   # string float
        ]
        
        for input_value, expected in test_cases:
            with self.subTest(input_value=input_value):
                result = self.manager.safe_float_convert(input_value, default=0.0)
                self.assertAlmostEqual(result, expected, places=2)
        
        # Test invalid conversions use default
        invalid_inputs = ['not_a_number', None, [], {}]
        for invalid_input in invalid_inputs:
            with self.subTest(input_value=invalid_input):
                result = self.manager.safe_float_convert(invalid_input, default=99.9)
                self.assertEqual(result, 99.9)
        
        # Test range validation
        result = self.manager.safe_float_convert(1.5, default=0.0, min_val=2.0, max_val=5.0)
        self.assertEqual(result, 2.0)  # Should clamp to minimum
        
        result = self.manager.safe_float_convert(6.5, default=0.0, min_val=2.0, max_val=5.0)
        self.assertEqual(result, 5.0)  # Should clamp to maximum
        
        result = self.manager.safe_float_convert(3.5, default=0.0, min_val=2.0, max_val=5.0)
        self.assertEqual(result, 3.5)  # Should remain unchanged
    
    # ========================================================================
    # VALIDATION UTILITIES TESTS
    # ========================================================================
    
    def test_validate_range(self):
        """Test validate_range"""
        # Test valid ranges
        self.assertTrue(self.manager.validate_range(5, 1, 10, 'test_param'))
        self.assertTrue(self.manager.validate_range(1, 1, 10, 'test_param'))  # At minimum
        self.assertTrue(self.manager.validate_range(10, 1, 10, 'test_param'))  # At maximum
        
        # Test invalid ranges
        self.assertFalse(self.manager.validate_range(0, 1, 10, 'test_param'))   # Below minimum
        self.assertFalse(self.manager.validate_range(11, 1, 10, 'test_param'))  # Above maximum
        
        # Test non-numeric values
        self.assertFalse(self.manager.validate_range('not_numeric', 1, 10, 'test_param'))
        self.assertFalse(self.manager.validate_range(None, 1, 10, 'test_param'))
        
        # Test with None bounds (None means no limit)
        self.assertTrue(self.manager.validate_range(100, None, None, 'test_param'))  # No limits
        self.assertTrue(self.manager.validate_range(-100, None, 10, 'test_param'))   # Only max limit
        self.assertTrue(self.manager.validate_range(100, 1, None, 'test_param'))     # Only min limit, value above min
    
    def test_validate_type(self):
        """Test validate_type"""
        # Test matching types
        self.assertTrue(self.manager.validate_type('test', str, 'string_param'))
        self.assertTrue(self.manager.validate_type(42, int, 'int_param'))
        self.assertTrue(self.manager.validate_type(3.14, float, 'float_param'))
        self.assertTrue(self.manager.validate_type(True, bool, 'bool_param'))
        
        # Test type mismatches
        self.assertFalse(self.manager.validate_type('test', int, 'mismatch_param'))
        self.assertFalse(self.manager.validate_type(42, str, 'mismatch_param'))  # int is not str
        
        # Test tuple of types
        self.assertTrue(self.manager.validate_type(42, (int, float), 'numeric_param'))
        self.assertTrue(self.manager.validate_type(3.14, (int, float), 'numeric_param'))
        self.assertFalse(self.manager.validate_type('test', (int, float), 'numeric_param'))
        
        # Test special cases - numeric types (cross-compatibility)
        self.assertTrue(self.manager.validate_type(42, float, 'int_as_float'))  # int can be float
        self.assertTrue(self.manager.validate_type(3.14, int, 'float_as_int'))  # float can be int
        
        # Test string type validation (strict)
        self.assertTrue(self.manager.validate_type('string', str, 'string_param'))
        self.assertFalse(self.manager.validate_type(42, str, 'int_as_string'))  # int is not automatically str
        self.assertFalse(self.manager.validate_type(None, str, 'none_as_string'))  # None is not str
    
    def test_validate_bounds(self):
        """Test validate_bounds"""
        # Test valid bounds dictionary
        bounds = {'min': 1, 'max': 10}
        self.assertTrue(self.manager.validate_bounds(5, bounds, 'test_param'))
        self.assertTrue(self.manager.validate_bounds(1, bounds, 'test_param'))  # At minimum
        self.assertTrue(self.manager.validate_bounds(10, bounds, 'test_param'))  # At maximum
        
        # Test invalid bounds
        self.assertFalse(self.manager.validate_bounds(0, bounds, 'test_param'))   # Below minimum
        self.assertFalse(self.manager.validate_bounds(11, bounds, 'test_param'))  # Above maximum
        
        # Test partial bounds
        min_only_bounds = {'min': 5}
        self.assertTrue(self.manager.validate_bounds(10, min_only_bounds, 'test_param'))
        self.assertFalse(self.manager.validate_bounds(3, min_only_bounds, 'test_param'))
        
        max_only_bounds = {'max': 15}
        self.assertTrue(self.manager.validate_bounds(10, max_only_bounds, 'test_param'))
        self.assertFalse(self.manager.validate_bounds(20, max_only_bounds, 'test_param'))
        
        # Test invalid inputs
        self.assertFalse(self.manager.validate_bounds('not_numeric', bounds, 'test_param'))
        self.assertFalse(self.manager.validate_bounds(5, 'not_dict', 'test_param'))
        self.assertFalse(self.manager.validate_bounds(5, None, 'test_param'))
    
    # ========================================================================
    # ERROR HANDLING UTILITIES TESTS
    # ========================================================================
    
    def test_handle_error_with_fallback(self):
        """Test handle_error_with_fallback"""
        test_error = ValueError("Test error message")
        fallback_value = "fallback_result"
        context = "test_context"
        operation = "test_operation"
        
        result = self.manager.handle_error_with_fallback(
            test_error, fallback_value, context, operation
        )
        
        # Should return fallback value
        self.assertEqual(result, fallback_value)
        
        # Should update operation status
        status = self.manager.get_last_operation_status()
        self.assertIn(operation, status)
        self.assertFalse(status[operation]['success'])
        self.assertEqual(status[operation]['error'], 'Test error message')
        self.assertEqual(status[operation]['context'], context)
        self.assertEqual(status[operation]['fallback_used'], fallback_value)
    
    # ========================================================================
    # UTILITY STATUS METHODS TESTS
    # ========================================================================
    
    def test_get_last_operation_status(self):
        """Test get_last_operation_status"""
        # Initially should be empty
        status = self.manager.get_last_operation_status()
        self.assertEqual(status, {})
        
        # Trigger an error to populate status
        test_error = RuntimeError("Test error")
        self.manager.handle_error_with_fallback(test_error, "fallback", "test_context", "test_op")
        
        status = self.manager.get_last_operation_status()
        self.assertIn('test_op', status)
        self.assertFalse(status['test_op']['success'])
    
    def test_validation_errors_management(self):
        """Test validation error collection and management"""
        # Initially should be empty
        errors = self.manager.get_validation_errors()
        self.assertEqual(errors, [])
        
        # Add some validation errors by calling methods that generate them
        self.manager.validate_range('not_numeric', 1, 10, 'test_param')
        self.manager.validate_type('test', int, 'mismatch_param')
        
        # Clear validation errors
        self.manager.clear_validation_errors()
        errors = self.manager.get_validation_errors()
        self.assertEqual(errors, [])
    
    def test_get_status(self):
        """Test get_status comprehensive status reporting"""
        status = self.manager.get_status()
        
        # Check required status fields
        self.assertEqual(status['manager_type'], 'SharedUtilitiesManager')
        self.assertIn('initialization_time', status)
        self.assertTrue(status['config_manager_available'])
        self.assertEqual(status['validation_errors_count'], 0)
        self.assertEqual(status['last_operations_count'], 0)
        self.assertEqual(status['utilities_available'], 15)
        self.assertEqual(status['status'], 'healthy')
    
    # ========================================================================
    # INTEGRATION TESTS WITH EXISTING MANAGERS
    # ========================================================================
    
    def test_integration_with_mock_managers(self):
        """Test SharedUtilitiesManager integration patterns"""
        # Simulate how other managers would use SharedUtilitiesManager
        
        # Mock a manager that needs validation utilities
        class MockAnalysisManager:
            def __init__(self, shared_utils):
                self.shared_utils = shared_utils
            
            def validate_parameter(self, value, param_type, param_name):
                """Example of using shared utilities for validation"""
                if param_type == int:
                    return self.shared_utils.safe_int_convert(value, default=0, param_name=param_name)
                elif param_type == float:
                    return self.shared_utils.safe_float_convert(value, default=0.0, param_name=param_name)
                elif param_type == bool:
                    return self.shared_utils.safe_bool_convert(value, default=False, param_name=param_name)
                else:
                    return value
        
        # Test integration
        mock_manager = MockAnalysisManager(self.manager)
        
        # Test parameter validation through shared utilities
        result = mock_manager.validate_parameter('123', int, 'test_int_param')
        self.assertEqual(result, 123)
        self.assertIsInstance(result, int)
        
        result = mock_manager.validate_parameter('45.67', float, 'test_float_param')
        self.assertAlmostEqual(result, 45.67, places=2)
        self.assertIsInstance(result, float)
        
        result = mock_manager.validate_parameter('true', bool, 'test_bool_param')
        self.assertTrue(result)
        self.assertIsInstance(result, bool)
    
    # ========================================================================
    # PERFORMANCE TESTS
    # ========================================================================
    
    def test_performance_impact(self):
        """Test SharedUtilitiesManager doesn't negatively impact performance"""
        # Test utility method call overhead
        start_time = time.perf_counter()
        
        # Perform 1000 utility operations
        for i in range(1000):
            self.manager.safe_bool_convert(True)
            self.manager.safe_int_convert(i)
            self.manager.validate_range(i, 0, 2000)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        # Should complete 3000 operations in reasonable time
        # Allowing 1 second for 3000 operations (very generous)
        self.assertLess(total_time, 1.0, "Performance impact too high")
        
        # Calculate average time per operation
        avg_time_per_op = (total_time / 3000) * 1000  # Convert to milliseconds
        
        # Should be well under 5ms per operation (target from design)
        self.assertLess(avg_time_per_op, 5.0, f"Average operation time {avg_time_per_op:.2f}ms exceeds 5ms target")
    
    def test_memory_usage_impact(self):
        """Test SharedUtilitiesManager memory efficiency"""
        import sys
        
        # Get initial memory usage
        initial_size = sys.getsizeof(self.manager)
        
        # Perform operations that might accumulate memory
        for i in range(100):
            self.manager.handle_error_with_fallback(
                ValueError(f"Test error {i}"),
                f"fallback_{i}",
                f"context_{i}",
                f"operation_{i}"
            )
        
        # Check memory usage didn't grow excessively
        final_size = sys.getsizeof(self.manager)
        growth = final_size - initial_size
        
        # Memory growth should be reasonable (allowing for operation status storage)
        self.assertLess(growth, 50000, f"Memory usage grew by {growth} bytes, which seems excessive")
    
    # ========================================================================
    # ERROR CONDITION TESTS
    # ========================================================================
    
    def test_constructor_error_conditions(self):
        """Test SharedUtilitiesManager constructor error handling"""
        # Test None config
        with self.assertRaises(ConfigurationError):
            SharedUtilitiesManager(None)
        
        # Test invalid config (missing required methods)
        invalid_config = Mock()
        del invalid_config.get_env_str  # Remove required method
        
        with self.assertRaises(ConfigurationError):
            SharedUtilitiesManager(invalid_config)
    
    def test_resilient_error_handling(self):
        """Test resilient error handling throughout the manager"""
        # Test with config manager that raises exceptions
        error_config = Mock()
        error_config.get_env_str.side_effect = Exception("Config error")
        error_config.get_env_dict.side_effect = Exception("Config error")
        
        # Manager should still be creatable and functional with fallbacks
        try:
            manager = SharedUtilitiesManager(error_config)
            
            # Operations should not crash, but use fallbacks
            result = manager.safe_bool_convert('true')
            self.assertTrue(result)  # Should still work
            
            result = manager.get_config_section_safely('any_section')
            self.assertEqual(result, {})  # Should return empty dict fallback
            
        except Exception as e:
            # If constructor fails due to config error, that's acceptable
            # The manager is resilient to config errors after construction
            self.assertIn("Config error", str(e))
    
    def test_json_file_error_conditions(self):
        """Test JSON file loading error conditions"""
        # Test invalid JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{ invalid json content }')  # Invalid JSON
            invalid_json_file = f.name
        
        try:
            # Required file with invalid JSON should raise error
            with self.assertRaises(ConfigurationError):
                self.manager.load_json_with_env_substitution(invalid_json_file, required=True)
            
            # Optional file with invalid JSON should return empty dict
            result = self.manager.load_json_with_env_substitution(invalid_json_file, required=False)
            self.assertEqual(result, {})
            
        finally:
            os.unlink(invalid_json_file)


# ============================================================================
# INTEGRATION TEST SUITE FOR CLEAN V3.1 COMPLIANCE
# ============================================================================

class TestCleanArchitectureCompliance(unittest.TestCase):
    """Test Clean v3.1 architecture compliance"""
    
    def test_factory_function_pattern(self):
        """Test factory function pattern compliance"""
        # Factory function should exist
        self.assertTrue(callable(create_shared_utilities_manager))
        
        # Factory should return correct type
        mock_config = MockUnifiedConfigManager()
        manager = create_shared_utilities_manager(mock_config)
        self.assertIsInstance(manager, SharedUtilitiesManager)
    
    def test_dependency_injection_pattern(self):
        """Test dependency injection pattern compliance"""
        mock_config = MockUnifiedConfigManager()
        manager = SharedUtilitiesManager(mock_config)
        
        # Manager should store injected dependency
        self.assertEqual(manager.config_manager, mock_config)
        
        # Manager should use dependency, not create its own
        # This is tested by using a mock and verifying calls
        mock_config.get_env_dict = Mock(return_value={})
        manager.get_config_section_safely('test_section')
        mock_config.get_env_dict.assert_called()
    
    def test_resilient_error_handling_compliance(self):
        """Test resilient error handling compliance"""
        mock_config = MockUnifiedConfigManager()
        manager = SharedUtilitiesManager(mock_config)
        
        # Operations should not crash on invalid inputs
        result = manager.safe_bool_convert('invalid_input')
        self.assertIsInstance(result, bool)  # Should return bool fallback
        
        result = manager.safe_int_convert('not_a_number')
        self.assertIsInstance(result, int)   # Should return int fallback
        
        result = manager.validate_range('not_numeric', 1, 10)
        self.assertIsInstance(result, bool)  # Should return bool validation result
    
    def test_file_versioning_compliance(self):
        """Test file versioning compliance"""
        # This test verifies the module has proper version documentation
        import managers.shared_utilities as module
        
        # Check module docstring contains version information
        docstring = module.__doc__
        self.assertIsNotNone(docstring)
        self.assertIn('FILE VERSION:', docstring)
        self.assertIn('v3.1-3e-2.2-1', docstring)
        self.assertIn('CLEAN ARCHITECTURE: v3.1 Compliant', docstring)


# ============================================================================
# TEST SUITE RUNNER
# ============================================================================

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases using the modern approach
    suite.addTest(loader.loadTestsFromTestCase(TestSharedUtilitiesManager))
    suite.addTest(loader.loadTestsFromTestCase(TestCleanArchitectureCompliance))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True,
        descriptions=True,
        failfast=False
    )
    
    print("🧪 Running SharedUtilitiesManager Integration Test Suite...")
    print("=" * 80)
    
    result = runner.run(suite)
    
    print("=" * 80)
    print(f"🎯 Tests Run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed! SharedUtilitiesManager ready for integration!")
    else:
        print("⚠️ Some tests failed. Review output above for details.")
    
    print("=" * 80)