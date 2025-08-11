# managers/debug_manager_availability.py
"""
Debug script to check manager availability
Run this to diagnose the missing managers warning
"""

import logging
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_manager_availability():
    """Check which managers are available and which are missing"""
    logger.info("🔍 Checking manager availability...")
    
    # List of all expected managers
    expected_managers = [
        ('AnalysisParametersManager', 'managers.analysis_parameters_manager'),
        ('CrisisPatternManager', 'managers.crisis_pattern_manager'),
        ('ThresholdMappingManager', 'managers.threshold_mapping_manager'),
        ('ServerConfigManager', 'managers.server_config_manager'),
        ('LoggingConfigManager', 'managers.logging_config_manager'),
        ('FeatureConfigManager', 'managers.feature_config_manager'),
        ('PerformanceConfigManager', 'managers.performance_config_manager'),
        ('StorageConfigManager', 'managers.storage_config_manager'),
        ('UnifiedConfigManager', 'managers.unified_config_manager'),
        ('SettingsManager', 'managers.settings_manager')
    ]
    
    available_managers = []
    missing_managers = []
    
    for manager_name, module_path in expected_managers:
        try:
            # Try to import the manager
            module = __import__(module_path, fromlist=[manager_name])
            manager_class = getattr(module, manager_name)
            
            # Try to get the factory function
            factory_name = f"create_{manager_name.replace('Manager', '').lower()}_manager"
            # Handle special cases
            if manager_name == 'AnalysisParametersManager':
                factory_name = 'create_analysis_parameters_manager'
            elif manager_name == 'CrisisPatternManager':
                factory_name = 'create_crisis_pattern_manager'
            elif manager_name == 'FeatureConfigManager':
                factory_name = 'create_feature_config_manager'
            elif manager_name == 'LoggingConfigManager':
                factory_name = 'create_logging_config_manager'
            elif manager_name == 'ModelEnsembleManager':
                factory_name = 'create_model_ensemble_manager'
            elif manager_name == 'ModelsManager':
                factory_name = 'create_models_manager'
            elif manager_name == 'PerformanceConfigManager':
                factory_name = 'create_performance_config_manager'
            elif manager_name == 'PydanticManager':
                factory_name = 'create_pydantic_manager'
            elif manager_name == 'ServerConfigManager':
                factory_name = 'create_server_config_manager'
            elif manager_name == 'SettingsManager':
                factory_name = 'create_settings_manager'
            elif manager_name == 'StorageConfigManager':
                factory_name = 'create_storage_config_manager'
            elif manager_name == 'ThresholdMappingManager':
                factory_name = 'create_threshold_mapping_manager'
            elif manager_name == 'UnifiedConfigManager':
                factory_name = 'create_unified_config_manager'
            elif manager_name == 'ZeroShotManager':
                factory_name = 'create_zero_shot_manager'
            
            factory_func = getattr(module, factory_name, None)
            
            if factory_func:
                logger.info(f"✅ {manager_name}: Available with factory function {factory_name}")
                available_managers.append(manager_name)
            else:
                logger.warning(f"⚠️ {manager_name}: Class available but missing factory function {factory_name}")
                missing_managers.append(f"{manager_name} (no factory)")
                
        except ImportError as e:
            logger.error(f"❌ {manager_name}: Import failed - {e}")
            missing_managers.append(manager_name)
        except AttributeError as e:
            logger.error(f"❌ {manager_name}: Attribute error - {e}")
            missing_managers.append(manager_name)
        except Exception as e:
            logger.error(f"❌ {manager_name}: Unexpected error - {e}")
            missing_managers.append(manager_name)
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 MANAGER AVAILABILITY SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Available managers: {available_managers}")
    logger.info(f"❌ Missing managers: {missing_managers}")
    logger.info(f"📈 Success rate: {len(available_managers)}/{len(expected_managers)} ({len(available_managers)/len(expected_managers)*100:.1f}%)")
    
    return len(missing_managers) == 0

def check_managers_init_file():
    """Check the managers/__init__.py file for proper exports"""
    logger.info("\n🔍 Checking managers/__init__.py exports...")
    
    try:
        import managers
        
        # Check __all__ exports
        if hasattr(managers, '__all__'):
            logger.info(f"✅ __all__ exports found: {len(managers.__all__)} items")
            for item in managers.__all__:
                logger.info(f"   📋 {item}")
        else:
            logger.warning("⚠️ No __all__ exports found in managers/__init__.py")
        
        # Check get_manager_status function
        if hasattr(managers, 'get_manager_status'):
            status = managers.get_manager_status()
            logger.info(f"✅ get_manager_status() function available")
            logger.info(f"📊 Manager status: {status}")
        else:
            logger.warning("⚠️ get_manager_status() function not found")
            
    except Exception as e:
        logger.error(f"❌ Error checking managers/__init__.py: {e}")

if __name__ == "__main__":
    logger.info("🚀 Starting manager availability diagnosis...")
    
    # Check individual manager availability
    all_available = check_manager_availability()
    
    # Check managers init file
    check_managers_init_file()
    
    # Final recommendation
    logger.info("\n" + "="*60)
    logger.info("🎯 RECOMMENDATIONS")
    logger.info("="*60)
    
    if all_available:
        logger.info("🎉 All managers available! The warning may be from test logic.")
        logger.info("💡 Recommendation: Run the comprehensive test to see specific issues.")
    else:
        logger.info("🔧 Some managers are missing or have issues.")
        logger.info("💡 Recommendation: Fix missing imports and factory functions first.")
    
    logger.info("✅ Diagnosis complete!")