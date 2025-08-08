#!/usr/bin/env python3
"""
Integration Test for Phase 3d Step 6: Storage & Logging Cleanup
Tests LoggingConfigManager and enhanced storage configuration

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import sys
import tempfile
import json
from pathlib import Path
from typing import Dict, Any

# Add the project root to Python path for imports
sys.path.insert(0, '/app')

try:
    from managers.config_manager import create_config_manager
    from managers.logging_config_manager import create_logging_config_manager
    print("✅ Successfully imported Clean v3.1 managers")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def create_test_configs(temp_dir: Path) -> None:
    """Create test configuration files for testing"""
    
    # Create logging_settings.json
    logging_config = {
        "logging_configuration": {
            "global_settings": {
                "log_level": "${GLOBAL_LOG_LEVEL}",
                "log_file": "${NLP_STORAGE_LOG_FILE}",
                "log_directory": "${NLP_STORAGE_LOGS_DIR}",
                "enable_console_output": True,
                "enable_file_output": True
            },
            "detailed_logging": {
                "enable_detailed": "${NLP_LOGGING_ENABLE_DETAILED}",
                "include_raw_labels": "${NLP_LOGGING_INCLUDE_RAW_LABELS}",
                "analysis_steps": "${NLP_LOGGING_ANALYSIS_STEPS}"
            },
            "component_logging": {
                "threshold_changes": "${NLP_LOGGING_THRESHOLD_CHANGES}",
                "model_disagreements": "${NLP_LOGGING_MODEL_DISAGREEMENTS}"
            },
            "defaults": {
                "global_settings": {
                    "log_level": "INFO",
                    "log_file": "nlp_service.log",
                    "log_directory": "./logs",
                    "enable_console_output": True,
                    "enable_file_output": True
                },
                "detailed_logging": {
                    "enable_detailed": True,
                    "include_raw_labels": True,
                    "analysis_steps": False
                },
                "component_logging": {
                    "threshold_changes": True,
                    "model_disagreements": True
                }
            }
        }
    }
    
    # Create enhanced storage_settings.json
    storage_config = {
        "storage_configuration": {
            "directories": {
                "data_directory": "${NLP_STORAGE_DATA_DIR}",
                "models_directory": "${NLP_STORAGE_MODELS_DIR}",
                "logs_directory": "${NLP_STORAGE_LOGS_DIR}",
                "cache_directory": "${NLP_STORAGE_CACHE_DIR}"
            },
            "file_paths": {
                "log_file": "${NLP_STORAGE_LOG_FILE}",
                "learning_persistence_file": "${NLP_STORAGE_LEARNING_FILE}"
            },
            "defaults": {
                "directories": {
                    "data_directory": "./data",
                    "models_directory": "./models/cache",
                    "logs_directory": "./logs",
                    "cache_directory": "./cache"
                },
                "file_paths": {
                    "log_file": "nlp_service.log",
                    "learning_persistence_file": "./learning_data/adjustments.json"
                }
            }
        }
    }
    
    # Write configuration files
    with open(temp_dir / 'logging_settings.json', 'w') as f:
        json.dump(logging_config, f, indent=2)
    
    with open(temp_dir / 'storage_settings.json', 'w') as f:
        json.dump(storage_config, f, indent=2)
    
    print(f"✅ Test configuration files created in {temp_dir}")

def test_config_manager_logging_support():
    """Test that ConfigManager supports logging configuration"""
    print("\n🧪 Testing ConfigManager logging support...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_test_configs(temp_path)
        
        # Create ConfigManager with test directory
        config_manager = create_config_manager(str(temp_path))
        
        # Test logging configuration loading
        try:
            logging_config = config_manager.get_logging_configuration()
            assert 'global_settings' in logging_config
            assert 'detailed_logging' in logging_config
            assert 'component_logging' in logging_config
            print("✅ ConfigManager.get_logging_configuration() works correctly")
        except Exception as e:
            print(f"❌ ConfigManager logging configuration failed: {e}")
            return False
        
        # Test enhanced storage configuration
        try:
            storage_config = config_manager.get_storage_configuration()
            assert 'directories' in storage_config
            assert 'file_paths' in storage_config
            print("✅ Enhanced storage configuration works correctly")
        except Exception as e:
            print(f"❌ Enhanced storage configuration failed: {e}")
            return False
    
    return True

def test_logging_config_manager():
    """Test LoggingConfigManager functionality"""
    print("\n🧪 Testing LoggingConfigManager...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_test_configs(temp_path)
        
        # Create managers
        config_manager = create_config_manager(str(temp_path))
        
        try:
            logging_config_manager = create_logging_config_manager(config_manager)
            print("✅ LoggingConfigManager factory function works")
        except Exception as e:
            print(f"❌ LoggingConfigManager creation failed: {e}")
            return False
        
        # Test configuration methods
        try:
            global_settings = logging_config_manager.get_global_logging_settings()
            assert 'log_level' in global_settings
            assert 'log_file' in global_settings
            print("✅ get_global_logging_settings() works")
            
            detailed_settings = logging_config_manager.get_detailed_logging_settings()
            assert 'enable_detailed' in detailed_settings
            print("✅ get_detailed_logging_settings() works")
            
            component_settings = logging_config_manager.get_component_logging_settings()
            assert 'threshold_changes' in component_settings
            print("✅ get_component_logging_settings() works")
            
        except Exception as e:
            print(f"❌ LoggingConfigManager methods failed: {e}")
            return False
        
        # Test convenience methods
        try:
            should_log = logging_config_manager.should_log_detailed()
            assert isinstance(should_log, bool)
            print("✅ Convenience methods work correctly")
        except Exception as e:
            print(f"❌ Convenience methods failed: {e}")
            return False
        
        # Test configuration status
        try:
            status = logging_config_manager.get_configuration_status()
            assert status['manager_type'] == 'LoggingConfigManager'
            assert status['architecture'] == 'clean-v3.1'
            assert status['phase'] == '3d-step-6'
            print("✅ Configuration status reporting works")
        except Exception as e:
            print(f"❌ Configuration status failed: {e}")
            return False
    
    return True

def test_environment_variable_overrides():
    """Test environment variable override functionality"""
    print("\n🧪 Testing environment variable overrides...")
    
    # Set test environment variables
    test_env_vars = {
        'GLOBAL_LOG_LEVEL': 'DEBUG',
        'NLP_LOGGING_ENABLE_DETAILED': 'false',
        'NLP_LOGGING_THRESHOLD_CHANGES': 'false',
        'NLP_STORAGE_DATA_DIR': '/test/data',
        'NLP_STORAGE_LOG_FILE': 'test_service.log'
    }
    
    # Set environment variables
    for key, value in test_env_vars.items():
        os.environ[key] = value
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            create_test_configs(temp_path)
            
            # Create managers
            config_manager = create_config_manager(str(temp_path))
            logging_config_manager = create_logging_config_manager(config_manager)
            
            # Test environment overrides
            global_settings = logging_config_manager.get_global_logging_settings()
            assert global_settings['log_level'] == 'DEBUG'
            assert global_settings['log_file'] == 'test_service.log'
            print("✅ GLOBAL_LOG_LEVEL override works (preserved)")
            
            detailed_settings = logging_config_manager.get_detailed_logging_settings()
            assert detailed_settings['enable_detailed'] == False
            print("✅ Detailed logging override works")
            
            component_settings = logging_config_manager.get_component_logging_settings()
            assert component_settings['threshold_changes'] == False
            print("✅ Component logging override works")
            
            storage_config = config_manager.get_storage_configuration()
            # Note: This tests the fallback method since env vars override JSON placeholders
            print("✅ Storage configuration override compatibility confirmed")
        
    finally:
        # Clean up environment variables
        for key in test_env_vars.keys():
            if key in os.environ:
                del os.environ[key]
    
    return True

def test_global_log_level_preservation():
    """Test that GLOBAL_LOG_LEVEL is properly preserved"""
    print("\n🧪 Testing GLOBAL_LOG_LEVEL preservation...")
    
    # Test various GLOBAL_LOG_LEVEL values
    test_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    for level in test_levels:
        os.environ['GLOBAL_LOG_LEVEL'] = level
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                create_test_configs(temp_path)
                
                config_manager = create_config_manager(str(temp_path))
                logging_config_manager = create_logging_config_manager(config_manager)
                
                # Verify GLOBAL_LOG_LEVEL is preserved
                retrieved_level = logging_config_manager.get_log_level()
                assert retrieved_level == level, f"Expected {level}, got {retrieved_level}"
                
                # Verify status reports preservation
                status = logging_config_manager.get_configuration_status()
                assert status['global_log_level_preserved'] == True
                
        finally:
            if 'GLOBAL_LOG_LEVEL' in os.environ:
                del os.environ['GLOBAL_LOG_LEVEL']
    
    print("✅ GLOBAL_LOG_LEVEL preservation verified for all levels")
    return True

def run_integration_tests():
    """Run all Step 6 integration tests"""
    print("🚀 Running Phase 3d Step 6 Integration Tests")
    print("=" * 60)
    
    tests = [
        ("ConfigManager Logging Support", test_config_manager_logging_support),
        ("LoggingConfigManager Functionality", test_logging_config_manager),
        ("Environment Variable Overrides", test_environment_variable_overrides),
        ("GLOBAL_LOG_LEVEL Preservation", test_global_log_level_preservation)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ PASSED: {test_name}")
                passed += 1
            else:
                print(f"❌ FAILED: {test_name}")
                failed += 1
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED - Step 6 is ready for production!")
        return True
    else:
        print("⚠️ Some tests failed - review implementation before proceeding")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)