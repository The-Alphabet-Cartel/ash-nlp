# ash-nlp/tests/phase/3/e/test_performance_config_manager_integration.py
"""
Integration Test for Optimized PerformanceConfigManager
FILE VERSION: v3.1-3e-5.5-1
LAST MODIFIED: 2025-08-19
PHASE: 3e Step 5.5 - PerformanceConfigManager Optimization Integration Test
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

# Import the optimized manager
from managers.performance_config_manager import PerformanceConfigManager, create_performance_config_manager
from managers.unified_config_manager import UnifiedConfigManager

class TestPerformanceConfigManagerIntegration(unittest.TestCase):
    """
    Integration tests for optimized PerformanceConfigManager
    
    These tests verify that the optimization maintains 100% functionality while
    properly consolidating utility methods and updating configuration access patterns.
    """
    
    def setUp(self):
        """Set up test environment with temporary config directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        
        # Create sample configuration files for testing
        self._create_test_config_files()
        
        # Create UnifiedConfigManager and PerformanceConfigManager
        self.config_manager = UnifiedConfigManager(str(self.config_dir))
        self.manager = PerformanceConfigManager(self.config_manager)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_test_config_files(self):
        """Create sample configuration files for testing"""
        # Create performance_settings.json
        performance_config = {
            "performance_settings": {
                "analysis_performance": {
                    "timeout_seconds": "${NLP_ANALYSIS_TIMEOUT}",
                    "retry_attempts": "${NLP_ANALYSIS_RETRY_ATTEMPTS}",
                    "enable_timeout": "${NLP_ANALYSIS_TIMEOUT_ENABLED}",
                    "batch_size": "${NLP_ANALYSIS_BATCH_SIZE}",
                    "defaults": {
                        "timeout_seconds": 30.0,
                        "retry_attempts": 3,
                        "enable_timeout": True,
                        "batch_size": 10
                    }
                },
                "server_performance": {
                    "max_workers": "${NLP_SERVER_MAX_WORKERS}",
                    "worker_timeout": "${NLP_SERVER_WORKER_TIMEOUT}",
                    "max_concurrent_requests": "${NLP_SERVER_MAX_CONCURRENT}",
                    "workers": "${NLP_SERVER_WORKERS}",
                    "defaults": {
                        "max_workers": 4,
                        "worker_timeout": 60,
                        "max_concurrent_requests": 20,
                        "workers": 1
                    }
                },
                "model_performance": {
                    "device": "${NLP_MODEL_DEVICE}",
                    "device_map": "${NLP_MODEL_DEVICE_MAP}",
                    "load_in_8bit": "${NLP_MODEL_LOAD_8BIT}",
                    "load_in_4bit": "${NLP_MODEL_LOAD_4BIT}",
                    "max_memory": "${NLP_MODEL_MAX_MEMORY}",
                    "offload_folder": "${NLP_MODEL_OFFLOAD_FOLDER}",
                    "defaults": {
                        "device": "auto",
                        "device_map": "auto",
                        "load_in_8bit": False,
                        "load_in_4bit": False,
                        "max_memory": None,
                        "offload_folder": None
                    }
                },
                "rate_limiting_performance": {
                    "rate_limit_per_minute": "${NLP_RATE_LIMIT_PER_MINUTE}",
                    "rate_limit_per_hour": "${NLP_RATE_LIMIT_PER_HOUR}",
                    "rate_limit_burst": "${NLP_RATE_LIMIT_BURST}",
                    "defaults": {
                        "rate_limit_per_minute": 120,
                        "rate_limit_per_hour": 2000,
                        "rate_limit_burst": 150
                    }
                },
                "cache_performance": {
                    "model_cache_size_limit": "${NLP_CACHE_MODEL_SIZE_LIMIT}",
                    "analysis_cache_size_limit": "${NLP_CACHE_ANALYSIS_SIZE_LIMIT}",
                    "cache_expiry_hours": "${NLP_CACHE_EXPIRY_HOURS}",
                    "defaults": {
                        "model_cache_size_limit": "10GB",
                        "analysis_cache_size_limit": "2GB",
                        "cache_expiry_hours": 24
                    }
                }
            },
            "performance_profiles": {
                "balanced": {
                    "description": "Balanced settings for general production use",
                    "analysis_timeout": 30.0,
                    "max_workers": 4,
                    "device": "auto"
                },
                "high_performance": {
                    "description": "High performance settings for maximum throughput",
                    "analysis_timeout": 60.0,
                    "max_workers": 8,
                    "device": "cuda"
                }
            },
            "performance_monitoring": {
                "cpu_threshold": 80.0,
                "memory_threshold": 85.0,
                "response_time_threshold": 5.0
            }
        }
        
        with open(self.config_dir / 'performance_settings.json', 'w') as f:
            json.dump(performance_config, f)
    
    # ========================================================================
    # CORE FUNCTIONALITY TESTS
    # ========================================================================
    
    def test_manager_initialization_with_config(self):
        """Test that manager initializes correctly with configuration"""
        self.assertIsNotNone(self.manager.config_cache)
        self.assertIsInstance(self.manager.config_cache, dict)
        
        # Should have loaded performance settings
        self.assertIn('performance_settings', self.manager.config_cache)
        self.assertIn('performance_profiles', self.manager.config_cache)
    
    def test_factory_function_creates_optimized_manager(self):
        """Test that factory function creates properly optimized manager"""
        manager = create_performance_config_manager(self.config_manager)
        
        self.assertIsInstance(manager, PerformanceConfigManager)
        self.assertIsNotNone(manager.config_cache)
        self.assertEqual(len(manager.get_validation_errors()), 0)
    
    def test_configuration_access_updated(self):
        """Test that configuration access uses enhanced patterns"""
        # Manager should use get_config_section approach
        # This is tested indirectly by verifying the config is loaded correctly
        settings = self.manager.get_all_performance_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn('analysis_performance', settings)
        self.assertIn('server_performance', settings)
    
    def test_fallback_configuration_with_safe_defaults(self):
        """Test that fallback configuration works with safe defaults"""
        # Create manager without performance_settings.json
        temp_dir_no_config = tempfile.mkdtemp()
        config_manager_no_config = UnifiedConfigManager(temp_dir_no_config)
        
        manager_fallback = PerformanceConfigManager(config_manager_no_config)
        
        # Should fall back to safe defaults
        analysis_settings = manager_fallback.get_analysis_performance_settings()
        self.assertEqual(analysis_settings['timeout_seconds'], 30.0)
        self.assertEqual(analysis_settings['retry_attempts'], 3)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir_no_config)
    
    # ========================================================================
    # MIGRATION REFERENCE TESTS
    # ========================================================================
    
    def test_utility_method_migration_references(self):
        """Test that utility methods provide proper fallback functionality"""
        # Test _get_performance_setting fallback
        result = self.manager._get_performance_setting('analysis_performance', 'timeout_seconds', 25.0, float)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
        
        # Test _parse_memory_string fallback
        result = self.manager._parse_memory_string('5GB')
        self.assertEqual(result, 5 * 1024 ** 3)
        
        result = self.manager._parse_memory_string('1024MB')
        self.assertEqual(result, 1024 * 1024 ** 2)
        
        # Test invalid memory string
        result = self.manager._parse_memory_string('invalid')
        self.assertEqual(result, 0)
    
    def test_migration_error_handling(self):
        """Test migration error handling when utility methods encounter errors"""
        # Test with invalid type conversion
        result = self.manager._get_performance_setting('nonexistent', 'setting', 'default', str)
        self.assertEqual(result, 'default')
        
        # Test with invalid memory format
        result = self.manager._parse_memory_string('')
        self.assertEqual(result, 0)
    
    # ========================================================================
    # PERFORMANCE SETTINGS ACCESS TESTS
    # ========================================================================
    
    def test_analysis_performance_settings(self):
        """Test analysis performance settings access"""
        settings = self.manager.get_analysis_performance_settings()
        
        self.assertIsInstance(settings, dict)
        self.assertIn('timeout_seconds', settings)
        self.assertIn('retry_attempts', settings)
        self.assertIn('enable_timeout', settings)
        self.assertIn('batch_size', settings)
        
        # Test individual getters
        self.assertEqual(self.manager.get_analysis_timeout(), settings['timeout_seconds'])
        self.assertEqual(self.manager.get_analysis_retry_attempts(), settings['retry_attempts'])
        self.assertEqual(self.manager.is_analysis_timeout_enabled(), settings['enable_timeout'])
    
    def test_server_performance_settings(self):
        """Test server performance settings access"""
        settings = self.manager.get_server_performance_settings()
        
        self.assertIsInstance(settings, dict)
        self.assertIn('max_workers', settings)
        self.assertIn('worker_timeout', settings)
        self.assertIn('request_timeout', settings)
        self.assertIn('max_concurrent_requests', settings)
        self.assertIn('workers', settings)
        
        # Test individual getters
        self.assertEqual(self.manager.get_max_workers(), settings['max_workers'])
        self.assertEqual(self.manager.get_max_concurrent_requests(), settings['max_concurrent_requests'])
    
    def test_model_performance_settings(self):
        """Test model performance settings access"""
        settings = self.manager.get_model_performance_settings()
        
        self.assertIsInstance(settings, dict)
        self.assertIn('device', settings)
        self.assertIn('device_map', settings)
        self.assertIn('load_in_8bit', settings)
        self.assertIn('load_in_4bit', settings)
        self.assertIn('max_memory', settings)
        self.assertIn('offload_folder', settings)
        
        # Test individual getters
        self.assertEqual(self.manager.get_device(), settings['device'])
        self.assertEqual(self.manager.is_load_in_8bit_enabled(), settings['load_in_8bit'])
    
    def test_rate_limiting_performance_settings(self):
        """Test rate limiting performance settings access"""
        settings = self.manager.get_rate_limiting_performance_settings()
        
        self.assertIsInstance(settings, dict)
        self.assertIn('rate_limit_per_minute', settings)
        self.assertIn('rate_limit_per_hour', settings)
        self.assertIn('rate_limit_burst', settings)
        
        # Test individual getter
        self.assertEqual(self.manager.get_rate_limit_requests_per_minute(), settings['rate_limit_per_minute'])
    
    def test_cache_performance_settings(self):
        """Test cache performance settings access"""
        settings = self.manager.get_cache_performance_settings()
        
        self.assertIsInstance(settings, dict)
        self.assertIn('model_cache_size_limit', settings)
        self.assertIn('analysis_cache_size_limit', settings)
        self.assertIn('cache_expiry_hours', settings)
        
        # Test individual getter
        self.assertEqual(self.manager.get_model_cache_size_limit(), settings['model_cache_size_limit'])
    
    def test_environment_variable_override(self):
        """Test environment variable override functionality"""
        with patch.dict(os.environ, {
            'NLP_ANALYSIS_TIMEOUT': '45.0',
            'NLP_SERVER_MAX_WORKERS': '8',
            'NLP_MODEL_DEVICE': 'cuda'
        }):
            # Create new manager with environment overrides
            manager_env = PerformanceConfigManager(self.config_manager)
            
            # Should use environment values
            self.assertEqual(manager_env.get_analysis_timeout(), 45.0)
            self.assertEqual(manager_env.get_max_workers(), 8)
            self.assertEqual(manager_env.get_device(), 'cuda')
    
    # ========================================================================
    # COMPREHENSIVE SETTINGS TESTS
    # ========================================================================
    
    def test_all_performance_settings(self):
        """Test comprehensive performance settings access"""
        all_settings = self.manager.get_all_performance_settings()
        
        self.assertIsInstance(all_settings, dict)
        self.assertIn('analysis_performance', all_settings)
        self.assertIn('server_performance', all_settings)
        self.assertIn('model_performance', all_settings)
        self.assertIn('rate_limiting_performance', all_settings)
        self.assertIn('cache_performance', all_settings)
        
        # Each category should be a dictionary
        for category, settings in all_settings.items():
            self.assertIsInstance(settings, dict)
            self.assertGreater(len(settings), 0)
    
    def test_cache_settings_comprehensive(self):
        """Test comprehensive cache settings"""
        cache_settings = self.manager.get_cache_settings()
        
        self.assertIsInstance(cache_settings, dict)
        self.assertIn('enabled', cache_settings)
        self.assertIn('ttl', cache_settings)
        self.assertIn('model_cache_limit', cache_settings)
        self.assertIn('analysis_cache_limit', cache_settings)
        self.assertIn('expiry_hours', cache_settings)
        
        # TTL should be hours converted to seconds
        self.assertTrue(cache_settings['enabled'])
        self.assertIsInstance(cache_settings['ttl'], int)
    
    def test_optimization_settings(self):
        """Test optimization settings"""
        opt_settings = self.manager.get_optimization_settings()
        
        self.assertIsInstance(opt_settings, dict)
        self.assertIn('batch_processing', opt_settings)
        self.assertIn('parallel_models', opt_settings)
        self.assertIn('gpu_optimization', opt_settings)
        self.assertIn('memory_optimization', opt_settings)
        self.assertIn('cache_optimization', opt_settings)
        self.assertIn('quantization_enabled', opt_settings)
        
        # Should be boolean values
        for key, value in opt_settings.items():
            self.assertIsInstance(value, bool)
    
    # ========================================================================
    # PERFORMANCE PROFILES TESTS
    # ========================================================================
    
    def test_performance_profiles_access(self):
        """Test performance profiles functionality"""
        # Test available profiles
        profiles = self.manager.get_available_profiles()
        self.assertIsInstance(profiles, list)
        self.assertIn('balanced', profiles)
        self.assertIn('high_performance', profiles)
        
        # Test profile settings access
        balanced_settings = self.manager.get_profile_settings('balanced')
        self.assertIsInstance(balanced_settings, dict)
        self.assertIn('description', balanced_settings)
        self.assertIn('analysis_timeout', balanced_settings)
        
        # Test nonexistent profile
        invalid_settings = self.manager.get_profile_settings('nonexistent')
        self.assertEqual(invalid_settings, {})
    
    def test_profile_activation(self):
        """Test performance profile activation"""
        # Test valid profile activation
        result = self.manager.activate_profile('balanced')
        self.assertTrue(result)
        
        # Test invalid profile activation
        result = self.manager.activate_profile('nonexistent')
        self.assertFalse(result)
    
    # ========================================================================
    # VALIDATION TESTS
    # ========================================================================
    
    def test_settings_validation(self):
        """Test performance settings validation"""
        validation_errors = self.manager.get_validation_errors()
        self.assertIsInstance(validation_errors, list)
        
        # With valid settings, should have no errors
        self.assertEqual(len(validation_errors), 0)
    
    def test_validation_with_invalid_settings(self):
        """Test validation with invalid settings"""
        # Create manager with invalid settings
        manager_invalid = PerformanceConfigManager(self.config_manager)
        
        # Manually inject invalid settings for testing
        manager_invalid.config_cache['performance_settings']['analysis_performance']['defaults']['timeout_seconds'] = 1.0  # Too low
        manager_invalid.config_cache['performance_settings']['server_performance']['defaults']['max_concurrent_requests'] = 0  # Too low
        manager_invalid.config_cache['performance_settings']['model_performance']['defaults']['device'] = 'invalid_device'
        
        # Re-run validation
        manager_invalid._validate_performance_settings()
        
        validation_errors = manager_invalid.get_validation_errors()
        self.assertGreater(len(validation_errors), 0)
    
    def test_performance_monitoring_thresholds(self):
        """Test performance monitoring thresholds access"""
        thresholds = self.manager.get_performance_monitoring_thresholds()
        
        self.assertIsInstance(thresholds, dict)
        # Should match what's in the test config
        self.assertIn('cpu_threshold', thresholds)
        self.assertIn('memory_threshold', thresholds)
        self.assertIn('response_time_threshold', thresholds)
    
    # ========================================================================
    # LEGACY COMPATIBILITY TESTS
    # ========================================================================
    
    def test_legacy_method_compatibility(self):
        """Test that legacy methods still work correctly"""
        # Test legacy request timeout method
        request_timeout = self.manager.get_request_timeout()
        analysis_timeout = self.manager.get_analysis_timeout()
        self.assertEqual(request_timeout, analysis_timeout)
        
        # Test other legacy methods maintain functionality
        self.assertIsInstance(self.manager.is_analysis_timeout_enabled(), bool)
        self.assertIsInstance(self.manager.is_load_in_8bit_enabled(), bool)
    
    # ========================================================================
    # ERROR HANDLING TESTS
    # ========================================================================
    
    def test_configuration_loading_error_handling(self):
        """Test error handling in configuration loading"""
        # Test with corrupted config manager
        with patch.object(self.config_manager, 'get_config_section', side_effect=Exception("Config error")):
            manager_error = PerformanceConfigManager(self.config_manager)
            
            # Should fall back to safe defaults
            settings = manager_error.get_analysis_performance_settings()
            self.assertIsInstance(settings, dict)
            self.assertEqual(settings['timeout_seconds'], 30.0)  # Safe default
    
    def test_validation_error_handling(self):
        """Test error handling in validation"""
        # Create manager with corrupted config cache
        manager_corrupt = PerformanceConfigManager(self.config_manager)
        manager_corrupt.config_cache = None
        
        # Should handle validation gracefully
        manager_corrupt._validate_performance_settings()
        
        # Should still return empty validation errors list
        validation_errors = manager_corrupt.get_validation_errors()
        self.assertIsInstance(validation_errors, list)

if __name__ == '__main__':
    unittest.main()