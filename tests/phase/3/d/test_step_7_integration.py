# tests/phase/3/d/test_step_7_integration.py
"""
Phase 3d Step 7 Integration Tests - Feature Flags & Performance Cleanup
Tests the FeatureConfigManager and PerformanceConfigManager integration

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging for tests
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all Clean v3.1 managers can be imported successfully"""
    try:
        from managers.config_manager import ConfigManager
        from managers.feature_config_manager import FeatureConfigManager, create_feature_config_manager
        from managers.performance_config_manager import PerformanceConfigManager, create_performance_config_manager
        
        logger.info("✅ Successfully imported Clean v3.1 managers")
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_feature_config_manager():
    """Test FeatureConfigManager functionality"""
    try:
        from managers.config_manager import ConfigManager
        from managers.feature_config_manager import create_feature_config_manager
        
        # Initialize managers using Clean v3.1 factory pattern
        config_manager = ConfigManager()
        feature_manager = create_feature_config_manager(config_manager)
        
        # Test core system features
        ensemble_enabled = feature_manager.is_ensemble_analysis_enabled()
        assert isinstance(ensemble_enabled, bool), "Ensemble analysis setting should be boolean"
        
        pattern_integration = feature_manager.is_pattern_integration_enabled()
        assert isinstance(pattern_integration, bool), "Pattern integration setting should be boolean"
        
        # Test analysis component features
        pattern_analysis = feature_manager.is_pattern_analysis_enabled()
        assert isinstance(pattern_analysis, bool), "Pattern analysis setting should be boolean"
        
        semantic_analysis = feature_manager.is_semantic_analysis_enabled()
        assert isinstance(semantic_analysis, bool), "Semantic analysis setting should be boolean"
        
        # Test experimental features
        experimental_features = feature_manager.get_experimental_features()
        assert isinstance(experimental_features, dict), "Experimental features should be dict"
        assert 'advanced_context' in experimental_features, "Should have advanced_context feature"
        
        # Test development features
        dev_features = feature_manager.get_development_debug_features()
        assert isinstance(dev_features, dict), "Development features should be dict"
        assert 'detailed_logging' in dev_features, "Should have detailed_logging feature"
        
        # Test all features getter
        all_features = feature_manager.get_all_features()
        assert isinstance(all_features, dict), "All features should be dict"
        assert 'core_system_features' in all_features, "Should have core system features"
        assert 'analysis_component_features' in all_features, "Should have analysis component features"
        
        # Test feature categories
        categories = feature_manager.get_feature_categories()
        assert isinstance(categories, dict), "Feature categories should be dict"
        
        logger.info("✅ FeatureConfigManager functionality test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ FeatureConfigManager test failed: {e}")
        return False

def test_performance_config_manager():
    """Test PerformanceConfigManager functionality"""
    try:
        from managers.config_manager import ConfigManager
        from managers.performance_config_manager import create_performance_config_manager
        
        # Initialize managers using Clean v3.1 factory pattern
        config_manager = ConfigManager()
        performance_manager = create_performance_config_manager(config_manager)
        
        # Test analysis performance settings
        analysis_timeout = performance_manager.get_analysis_timeout_ms()
        assert isinstance(analysis_timeout, int), "Analysis timeout should be integer"
        assert analysis_timeout > 0, "Analysis timeout should be positive"
        
        max_concurrent = performance_manager.get_analysis_max_concurrent()
        assert isinstance(max_concurrent, int), "Max concurrent should be integer"
        assert max_concurrent > 0, "Max concurrent should be positive"
        
        # Test server performance settings
        server_settings = performance_manager.get_server_performance_settings()
        assert isinstance(server_settings, dict), "Server settings should be dict"
        assert 'max_concurrent_requests' in server_settings, "Should have max concurrent requests"
        assert 'workers' in server_settings, "Should have workers setting"
        
        # Test model performance settings
        batch_size = performance_manager.get_max_batch_size()
        assert isinstance(batch_size, int), "Batch size should be integer"
        assert batch_size > 0, "Batch size should be positive"
        
        device = performance_manager.get_device()
        assert isinstance(device, str), "Device should be string"
        assert device in ['auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1'], f"Invalid device: {device}"
        
        precision = performance_manager.get_model_precision()
        assert isinstance(precision, str), "Precision should be string"
        assert precision in ['float32', 'float16', 'bfloat16', 'auto'], f"Invalid precision: {precision}"
        
        # Test rate limiting settings
        rate_settings = performance_manager.get_rate_limiting_performance_settings()
        assert isinstance(rate_settings, dict), "Rate settings should be dict"
        assert 'rate_limit_per_minute' in rate_settings, "Should have per-minute limit"
        assert 'rate_limit_per_hour' in rate_settings, "Should have per-hour limit"
        
        # Test cache performance settings
        cache_settings = performance_manager.get_cache_performance_settings()
        assert isinstance(cache_settings, dict), "Cache settings should be dict"
        assert 'model_cache_size_limit' in cache_settings, "Should have model cache limit"
        
        # Test all performance settings
        all_settings = performance_manager.get_all_performance_settings()
        assert isinstance(all_settings, dict), "All settings should be dict"
        assert 'analysis_performance' in all_settings, "Should have analysis performance"
        assert 'server_performance' in all_settings, "Should have server performance"
        
        # Test performance profiles
        profiles = performance_manager.get_available_profiles()
        assert isinstance(profiles, list), "Profiles should be list"
        assert len(profiles) > 0, "Should have at least one profile"
        
        logger.info("✅ PerformanceConfigManager functionality test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ PerformanceConfigManager test failed: {e}")
        return False

def test_environment_variable_overrides():
    """Test that environment variables properly override JSON defaults"""
    try:
        from managers.config_manager import ConfigManager
        from managers.feature_config_manager import create_feature_config_manager
        from managers.performance_config_manager import create_performance_config_manager
        
        # Test environment variable override for feature flags
        original_value = os.environ.get('NLP_FEATURE_ENSEMBLE_ANALYSIS')
        os.environ['NLP_FEATURE_ENSEMBLE_ANALYSIS'] = 'false'
        
        try:
            config_manager = ConfigManager()
            feature_manager = create_feature_config_manager(config_manager)
            
            ensemble_enabled = feature_manager.is_ensemble_analysis_enabled()
            assert ensemble_enabled == False, "Environment variable should override default"
            
        finally:
            # Clean up environment
            if original_value is not None:
                os.environ['NLP_FEATURE_ENSEMBLE_ANALYSIS'] = original_value
            else:
                os.environ.pop('NLP_FEATURE_ENSEMBLE_ANALYSIS', None)
        
        # Test environment variable override for performance settings
        original_timeout = os.environ.get('NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS')
        os.environ['NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS'] = '8000'
        
        try:
            config_manager = ConfigManager()
            performance_manager = create_performance_config_manager(config_manager)
            
            timeout = performance_manager.get_analysis_timeout_ms()
            assert timeout == 8000, "Environment variable should override default timeout"
            
        finally:
            # Clean up environment
            if original_timeout is not None:
                os.environ['NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS'] = original_timeout
            else:
                os.environ.pop('NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS', None)
        
        logger.info("✅ Environment variable overrides test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment variable overrides test failed: {e}")
        return False

def test_config_manager_integration():
    """Test ConfigManager integration with new feature and performance methods"""
    try:
        from managers.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        
        # Test feature configuration access
        feature_config = config_manager.get_feature_configuration()
        assert isinstance(feature_config, dict), "Feature config should be dict"
        assert 'core_system_features' in feature_config, "Should have core system features"
        assert 'experimental_features' in feature_config, "Should have experimental features"
        
        # Test performance configuration access
        performance_config = config_manager.get_performance_configuration()
        assert isinstance(performance_config, dict), "Performance config should be dict"
        assert 'analysis_performance' in performance_config, "Should have analysis performance"
        assert 'model_performance' in performance_config, "Should have model performance"
        
        logger.info("✅ ConfigManager integration test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ ConfigManager integration test failed: {e}")
        return False

def test_backward_compatibility():
    """Test that Step 7 changes don't break existing functionality"""
    try:
        from managers.config_manager import ConfigManager
        from managers.settings_manager import create_settings_manager
        
        # Test that existing managers still work
        config_manager = ConfigManager()
        settings_manager = create_settings_manager(config_manager)
        
        # Test that existing methods still work
        device_setting = settings_manager.get_device_setting()
        assert isinstance(device_setting, str), "Device setting should be string"
        
        precision_setting = settings_manager.get_precision_setting()
        assert isinstance(precision_setting, str), "Precision setting should be string"
        
        logger.info("✅ Backward compatibility test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Backward compatibility test failed: {e}")
        return False

def main():
    """Run all Phase 3d Step 7 integration tests"""
    logger.info("🚀 Running Phase 3d Step 7 Integration Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("FeatureConfigManager Functionality", test_feature_config_manager),
        ("PerformanceConfigManager Functionality", test_performance_config_manager),
        ("Environment Variable Overrides", test_environment_variable_overrides),
        ("ConfigManager Integration", test_config_manager_integration),
        ("Backward Compatibility", test_backward_compatibility)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"🧪 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            failed += 1
        logger.info("-" * 60)
    
    logger.info("=" * 60)
    logger.info(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 All Step 7 integration tests PASSED!")
        return True
    else:
        logger.error("❌ Some Step 7 integration tests FAILED!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)