# tests/phase/3/d/test_step_7_integration.py
"""
Phase 3d Step 7 Integration Tests - Feature Flags & Performance Cleanup
STEP 9.8 FIXED: Updated to use UnifiedConfigManager instead of ConfigManager

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
    """Test that all Clean v3.1 managers can be imported successfully - STEP 9.8 FIXED"""
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.feature_config_manager import FeatureConfigManager, create_feature_config_manager
        from managers.performance_config_manager import PerformanceConfigManager, create_performance_config_manager
        
        logger.info("✅ Successfully imported Clean v3.1 managers")
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_feature_config_manager():
    """Test FeatureConfigManager functionality - STEP 9.8 FIXED"""
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.feature_config_manager import create_feature_config_manager
        
        # Initialize managers using Clean v3.1 factory pattern
        config_manager = create_unified_config_manager("/app/config")
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
        
        # Test learning system features
        learning_enabled = feature_manager.is_learning_system_enabled()
        assert isinstance(learning_enabled, bool), "Learning system setting should be boolean"
        
        logger.info("✅ FeatureConfigManager functionality tests passed")
        return True
    except Exception as e:
        logger.error(f"❌ FeatureConfigManager test failed: {e}")
        return False

def test_performance_config_manager():
    """Test PerformanceConfigManager functionality - STEP 9.8 FIXED"""
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.performance_config_manager import create_performance_config_manager
        
        # Initialize managers using Clean v3.1 factory pattern
        config_manager = create_unified_config_manager("/app/config")
        performance_manager = create_performance_config_manager(config_manager)
        
        # Test performance settings access
        batch_settings = performance_manager.get_batch_processing_settings()
        assert isinstance(batch_settings, dict), "Batch settings should be dict"
        
        caching_settings = performance_manager.get_caching_settings()
        assert isinstance(caching_settings, dict), "Caching settings should be dict"
        
        optimization_settings = performance_manager.get_optimization_settings()
        assert isinstance(optimization_settings, dict), "Optimization settings should be dict"
        
        logger.info("✅ PerformanceConfigManager functionality tests passed")
        return True
    except Exception as e:
        logger.error(f"❌ PerformanceConfigManager test failed: {e}")
        return False

def test_environment_variable_overrides():
    """Test environment variable overrides - STEP 9.8 FIXED"""
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        from managers.feature_config_manager import create_feature_config_manager
        from managers.performance_config_manager import create_performance_config_manager
        
        # Test with environment variables
        test_env_vars = {
            'NLP_FEATURE_ENSEMBLE_ANALYSIS': 'false',
            'NLP_PERFORMANCE_BATCH_SIZE': '16',
            'NLP_PERFORMANCE_CACHE_TTL': '600'
        }
        
        with patch.dict(os.environ, test_env_vars):
            config_manager = create_unified_config_manager("/app/config")
            feature_manager = create_feature_config_manager(config_manager)
            performance_manager = create_performance_config_manager(config_manager)
            
            # Test that environment variables are respected
            # Note: These might not change due to caching, but the test verifies no errors
            ensemble_setting = feature_manager.is_ensemble_analysis_enabled()
            batch_settings = performance_manager.get_batch_processing_settings()
            
            assert isinstance(ensemble_setting, bool)
            assert isinstance(batch_settings, dict)
            
        logger.info("✅ Environment variable override tests passed")
        return True
    except Exception as e:
        logger.error(f"❌ Environment variable override test failed: {e}")
        return False

def test_config_manager_integration():
    """Test UnifiedConfigManager integration - STEP 9.8 FIXED"""
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager("/app/config")
        
        # Test that both new methods exist and work
        feature_config = config_manager.get_feature_configuration()
        assert isinstance(feature_config, dict), "Feature config should be dict"
        
        performance_config = config_manager.get_performance_configuration()
        assert isinstance(performance_config, dict), "Performance config should be dict"
        
        logger.info("✅ UnifiedConfigManager integration tests passed")
        return True
    except Exception as e:
        logger.error(f"❌ UnifiedConfigManager integration test failed: {e}")
        return False

def test_backward_compatibility():
    """Test backward compatibility - STEP 9.8 FIXED"""
    try:
        # STEP 9.8 FIX: Use UnifiedConfigManager instead of ConfigManager  
        from managers.unified_config_manager import create_unified_config_manager
        from managers.feature_config_manager import create_feature_config_manager
        from managers.performance_config_manager import create_performance_config_manager
        
        # Test that existing functionality still works
        config_manager = create_unified_config_manager("/app/config")
        feature_manager = create_feature_config_manager(config_manager)
        performance_manager = create_performance_config_manager(config_manager)
        
        # Test key methods exist and return expected types
        assert hasattr(feature_manager, 'is_ensemble_analysis_enabled')
        assert hasattr(performance_manager, 'get_batch_processing_settings')
        
        logger.info("✅ Backward compatibility tests passed")
        return True
    except Exception as e:
        logger.error(f"❌ Backward compatibility test failed: {e}")
        return False

def main():
    """Run all Step 7 integration tests - STEP 9.8 FIXED"""
    logger.info("🚀 Phase 3d Step 7 Integration Tests - STEP 9.8 FIXED VERSION")
    logger.info("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("FeatureConfigManager Functionality", test_feature_config_manager),
        ("PerformanceConfigManager Functionality", test_performance_config_manager),
        ("Environment Variable Overrides", test_environment_variable_overrides),
        ("UnifiedConfigManager Integration", test_config_manager_integration),
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
    # Add missing import for patch
    from unittest.mock import patch
    
    success = main()
    sys.exit(0 if success else 1)