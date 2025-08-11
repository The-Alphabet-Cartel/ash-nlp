#!/usr/bin/env python3
# tests/phase/3/d/test_step_6_integration_fixed.py
"""
Phase 3d Step 6 Integration Tests - STEP 9.8 FIXED VERSION
Tests LoggingConfigManager integration and functionality

STEP 9.8 FIX: Updated to use UnifiedConfigManager instead of ConfigManager
"""

import os
import sys
import tempfile
import json
import logging
from pathlib import Path
from unittest.mock import patch, mock_open, Mock

# Add /app to path
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

# Set up logging for test output
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def test_unified_config_manager_logging_support():
    """Test UnifiedConfigManager logging support - STEP 9.8 FIXED"""
    logger.info("🧪 Testing UnifiedConfigManager logging support...")
    
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        
        # Create UnifiedConfigManager
        config_manager = create_unified_config_manager('/app/config')
        
        # Test get_logging_configuration method  
        logging_config = config_manager.get_logging_configuration()
        
        # Verify it returns a dictionary
        assert isinstance(logging_config, dict), f"Expected dict, got {type(logging_config)}"
        
        # Verify it has expected structure
        expected_keys = ['global_settings', 'detailed_logging', 'component_logging', 'development_logging']
        for key in expected_keys:
            assert key in logging_config, f"Missing key: {key}"
        
        logger.info("✅ UnifiedConfigManager.get_logging_configuration() works correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ UnifiedConfigManager logging support failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logging_config_manager_functionality():
    """Test LoggingConfigManager functionality - STEP 9.8 FIXED"""
    logger.info("🧪 Testing LoggingConfigManager...")
    
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.logging_config_manager import create_logging_config_manager
        
        # Create test configuration
        test_config = {
            "logging_configuration": {
                "global_settings": {
                    "log_level": "DEBUG",
                    "log_file": "test_service.log", 
                    "log_directory": "/tmp/test_logs",
                    "enable_console_output": True,
                    "enable_file_output": True
                },
                "detailed_logging": {
                    "enable_detailed": True,
                    "include_raw_labels": True,
                    "analysis_steps": False,
                    "performance_metrics": True,
                    "include_reasoning": True
                },
                "component_logging": {
                    "threshold_changes": True,
                    "model_disagreements": True,
                    "staff_review_triggers": True,
                    "pattern_adjustments": True,
                    "learning_updates": True,
                    "label_mappings": True,
                    "ensemble_decisions": True,
                    "crisis_detection": True
                }
            }
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test configuration file
            config_file = temp_path / "logging_settings.json"
            with open(config_file, 'w') as f:
                json.dump(test_config, f)
            
            logger.info(f"✅ Test configuration files created in {temp_dir}")
            
            # STEP 9.8 FIX: Mock UnifiedConfigManager instead of ConfigManager
            with patch('managers.unified_config_manager.UnifiedConfigManager') as MockUnifiedConfigManager:
                mock_config_manager = MockUnifiedConfigManager.return_value
                mock_config_manager.load_config_file.return_value = test_config
                
                # Test LoggingConfigManager factory function
                logging_manager = create_logging_config_manager(mock_config_manager)
                logger.info("✅ LoggingConfigManager factory function works")
                
                # Test main configuration access methods
                global_settings = logging_manager.get_global_logging_settings()
                assert isinstance(global_settings, dict)
                assert global_settings['log_level'] == 'DEBUG'
                logger.info("✅ get_global_logging_settings() works")
                
                detailed_settings = logging_manager.get_detailed_logging_settings()
                assert isinstance(detailed_settings, dict)
                assert detailed_settings['enable_detailed'] == True
                logger.info("✅ get_detailed_logging_settings() works")
                
                component_settings = logging_manager.get_component_logging_settings()
                assert isinstance(component_settings, dict)
                assert component_settings['crisis_detection'] == True
                logger.info("✅ get_component_logging_settings() works")
                
                return True
        
    except Exception as e:
        logger.error(f"❌ LoggingConfigManager functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_variable_overrides():
    """Test environment variable overrides - STEP 9.8 FIXED"""
    logger.info("🧪 Testing environment variable overrides...")
    
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.logging_config_manager import create_logging_config_manager
        
        # Create base configuration with placeholders
        base_config = {
            "logging_configuration": {
                "global_settings": {
                    "log_level": "${GLOBAL_LOG_LEVEL}",
                    "log_file": "${NLP_STORAGE_LOG_FILE}",
                    "log_directory": "${NLP_STORAGE_LOGS_DIR}"
                },
                "detailed_logging": {
                    "enable_detailed": "${NLP_LOGGING_ENABLE_DETAILED}",
                    "analysis_steps": "${NLP_LOGGING_ANALYSIS_STEPS}"
                },
                "component_logging": {
                    "threshold_changes": "${NLP_LOGGING_THRESHOLD_CHANGES}"
                }
            }
        }
        
        # Set test environment variables
        test_env_vars = {
            'GLOBAL_LOG_LEVEL': 'WARNING',
            'NLP_STORAGE_LOG_FILE': 'override_test.log',
            'NLP_STORAGE_LOGS_DIR': '/tmp/override_logs',
            'NLP_LOGGING_ENABLE_DETAILED': 'false',
            'NLP_LOGGING_ANALYSIS_STEPS': 'true',
            'NLP_LOGGING_THRESHOLD_CHANGES': 'false'
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create configuration file with placeholders
            config_file = temp_path / "logging_settings.json"
            with open(config_file, 'w') as f:
                json.dump(base_config, f)
            
            logger.info(f"✅ Test configuration files created in {temp_dir}")
            
            # Test with environment variables set
            with patch.dict(os.environ, test_env_vars):
                # STEP 9.8 FIX: Create actual UnifiedConfigManager (not mocked) to test env var substitution
                config_manager = create_unified_config_manager(str(temp_path))
                
                # Load the configuration and check if substitution worked
                logging_config = config_manager.load_config_file('logging_settings')
                
                # Verify environment variables were substituted
                global_settings = logging_config.get('logging_configuration', {}).get('global_settings', {})
                assert global_settings.get('log_level') == 'WARNING'
                assert global_settings.get('log_file') == 'override_test.log'
                assert global_settings.get('log_directory') == '/tmp/override_logs'
                
                logger.info("✅ Environment variable overrides working correctly")
                return True
        
    except Exception as e:
        logger.error(f"❌ Environment variable overrides test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test backward compatibility - STEP 9.8 FIXED"""
    logger.info("🧪 Testing backward compatibility...")
    
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.logging_config_manager import create_logging_config_manager
        
        # Use real config directory
        config_manager = create_unified_config_manager('/app/config')
        logging_manager = create_logging_config_manager(config_manager)
        
        # Test that all expected methods exist and return reasonable values
        methods_to_test = [
            'get_global_logging_settings',
            'get_detailed_logging_settings', 
            'get_component_logging_settings',
            'get_development_logging_settings'
        ]
        
        for method_name in methods_to_test:
            method = getattr(logging_manager, method_name)
            result = method()
            assert isinstance(result, dict), f"{method_name} should return dict"
            logger.info(f"✅ {method_name}() works correctly")
        
        logger.info("✅ Backward compatibility maintained")
        return True
        
    except Exception as e:
        logger.error(f"❌ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# STEP 9.8 FIX: Main test execution with UnifiedConfigManager
def main():
    """Main test execution - STEP 9.8 FIXED"""
    logger.info("🚀 Phase 3d Step 6 Integration Tests - STEP 9.8 FIXED VERSION")
    logger.info("=" * 60)
    
    tests = [
        ("UnifiedConfigManager Logging Support", test_unified_config_manager_logging_support),
        ("LoggingConfigManager Functionality", test_logging_config_manager_functionality),
        ("Environment Variable Overrides", test_environment_variable_overrides),
        ("Backward Compatibility", test_backward_compatibility)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running: {test_name}")
        logger.info("-" * 40)
        
        try:
            if test_func():
                logger.info(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 STEP 9.8 FIXED TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED - Step 9.8 fixes successful!")
        return True
    else:
        logger.error(f"⚠️ {total - passed} tests failed - Step 9.8 fixes incomplete")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)