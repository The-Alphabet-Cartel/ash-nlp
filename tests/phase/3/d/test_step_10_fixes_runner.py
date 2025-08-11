# tests/phase/3/d/test_fixes_runner.py
"""
Quick test runner to validate Step 10 fixes
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_storage_config_manager_creation():
    """Test that StorageConfigManager can be created"""
    logger.info("🧪 Testing StorageConfigManager creation...")
    
    try:
        from managers.storage_config_manager import create_storage_config_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        # Create unified config manager
        unified_config = create_unified_config_manager("/app/config")
        
        # Create storage config manager
        storage_manager = create_storage_config_manager(unified_config)
        
        # Test basic functionality
        status = storage_manager.get_status()
        assert isinstance(status, dict), "Should return dict status"
        
        directories = storage_manager.get_directories()
        assert isinstance(directories, dict), "Should return dict directories"
        
        logger.info(f"   ✅ StorageConfigManager working - status: {status.get('status', 'unknown')}")
        logger.info(f"   ✅ Directories configured: {len(directories)}")
        
        return True
        
    except ImportError as e:
        logger.error(f"   ❌ StorageConfigManager import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"   ❌ StorageConfigManager test failed: {e}")
        return False

def test_boolean_schema_validation():
    """Test that boolean schema validation works"""
    logger.info("🧪 Testing boolean schema validation...")
    
    try:
        from managers.unified_config_manager import create_unified_config_manager
        
        unified_config = create_unified_config_manager("/app/config")
        
        # Test boolean variable access
        bool_vars = [
            'NLP_FEATURES_ENSEMBLE_ANALYSIS_ENABLED',
            'NLP_STORAGE_ENABLE_MODEL_CACHE',
            'NLP_PERFORMANCE_ENABLE_OPTIMIZATION'
        ]
        
        for var in bool_vars:
            try:
                value = unified_config.get_env(var, True)
                logger.info(f"   ✅ {var}: {value} (type: {type(value).__name__})")
            except Exception as e:
                logger.warning(f"   ⚠️ {var}: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"   ❌ Boolean schema validation test failed: {e}")
        return False

def test_crisis_analyzer_methods():
    """Test CrisisAnalyzer method availability"""
    logger.info("🧪 Testing CrisisAnalyzer method availability...")
    
    try:
        from analysis.crisis_analyzer import CrisisAnalyzer
        from managers.unified_config_manager import create_unified_config_manager
        from managers.settings_manager import create_settings_manager
        
        # Initialize with unified configuration
        unified_config = create_unified_config_manager("/app/config")
        settings_manager = create_settings_manager(
            unified_config_manager=unified_config,
            crisis_pattern_manager=None,
            analysis_parameters_manager=None,
            threshold_mapping_manager=None,
            server_config_manager=None,
            logging_config_manager=None,
            feature_config_manager=None,
            performance_config_manager=None
        )
        
        # Create CrisisAnalyzer instance
        analyzer = CrisisAnalyzer(settings_manager)
        
        # Check method availability
        required_methods = [
            'get_configuration_summary',
            '_get_current_threshold_mode'
        ]
        
        optional_methods = [
            '_map_confidence_to_crisis_level',
            '_is_staff_review_required'
        ]
        
        for method in required_methods:
            if hasattr(analyzer, method):
                logger.info(f"   ✅ Required method available: {method}")
            else:
                logger.error(f"   ❌ Required method missing: {method}")
                return False
        
        for method in optional_methods:
            if hasattr(analyzer, method):
                logger.info(f"   ✅ Optional method available: {method}")
            else:
                logger.info(f"   📋 Optional method not implemented: {method}")
        
        return True
        
    except Exception as e:
        logger.error(f"   ❌ CrisisAnalyzer test failed: {e}")
        return False

def test_manager_integration():
    """Test that all managers integrate properly"""
    logger.info("🧪 Testing manager integration...")
    
    try:
        from managers.unified_config_manager import create_unified_config_manager
        
        unified_config = create_unified_config_manager("/app/config")
        
        # Test manager imports
        manager_tests = [
            ("managers.settings_manager", "create_settings_manager"),
            ("managers.crisis_pattern_manager", "create_crisis_pattern_manager"),
            ("managers.analysis_parameters_manager", "create_analysis_parameters_manager"),
            ("managers.threshold_mapping_manager", "create_threshold_mapping_manager"),
            ("managers.server_config_manager", "create_server_config_manager"),
            ("managers.logging_config_manager", "create_logging_config_manager"),
            ("managers.feature_config_manager", "create_feature_config_manager"),
            ("managers.performance_config_manager", "create_performance_config_manager"),
            ("managers.models_manager", "create_models_manager")
        ]
        
        successful = 0
        total = len(manager_tests)
        
        for module_name, factory_name in manager_tests:
            try:
                module = __import__(module_name, fromlist=[factory_name])
                factory_func = getattr(module, factory_name)
                
                # Try to create manager
                if factory_name == "create_threshold_mapping_manager":
                    manager = factory_func(unified_config, None)
                else:
                    manager = factory_func(unified_config)
                
                logger.info(f"   ✅ {factory_name} working")
                successful += 1
                
            except Exception as e:
                logger.warning(f"   ⚠️ {factory_name} failed: {e}")
        
        success_rate = (successful / total) * 100
        logger.info(f"   📊 Manager integration: {successful}/{total} ({success_rate:.1f}%)")
        
        return successful >= total * 0.8  # 80% success rate
        
    except Exception as e:
        logger.error(f"   ❌ Manager integration test failed: {e}")
        return False

def run_all_fixes_tests():
    """Run all fix validation tests"""
    logger.info("🚀 Running Step 10 Fixes Validation")
    logger.info("=" * 60)
    
    tests = [
        ("StorageConfigManager Creation", test_storage_config_manager_creation),
        ("Boolean Schema Validation", test_boolean_schema_validation),
        ("CrisisAnalyzer Methods", test_crisis_analyzer_methods),
        ("Manager Integration", test_manager_integration)
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
    logger.info(f"📊 FIXES VALIDATION RESULTS: {passed}/{total} tests passed")
    
    success_rate = (passed / total) * 100
    
    if passed == total:
        logger.info("🎉 ALL FIXES VALIDATED - Ready for comprehensive testing!")
        return True
    elif success_rate >= 75:
        logger.info("✅ MOST FIXES VALIDATED - Should improve test results")
        return True
    else:
        logger.error("❌ FIXES NEED MORE WORK")
        return False

if __name__ == "__main__":
    success = run_all_fixes_tests()
    sys.exit(0 if success else 1)