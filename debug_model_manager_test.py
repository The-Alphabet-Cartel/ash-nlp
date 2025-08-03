#!/usr/bin/env python3
"""
Test ModelManager with proper configuration parameters
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_modelmanager_with_proper_config():
    """Test ModelManager with all required parameters"""
    logger.info("🔧 Testing ModelManager with proper configuration...")
    
    try:
        # Step 1: Initialize managers like main.py does
        logger.info("📋 Step 1: Initialize configuration managers...")
        from managers.config_manager import ConfigManager
        from managers.settings_manager import SettingsManager
        from managers.zero_shot_manager import ZeroShotManager
        
        config_manager = ConfigManager("/app/config")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        logger.info("✅ Managers initialized")
        
        # Step 2: Get configuration like main.py does
        logger.info("📊 Step 2: Extract configuration...")
        model_config = config_manager.get_model_configuration()
        hardware_config = config_manager.get_hardware_configuration()
        threshold_config = config_manager.get_threshold_configuration()
        feature_flags = config_manager.get_feature_flags()
        ensemble_mode = config_manager.get_ensemble_mode()
        
        logger.info("✅ Configuration extracted")
        logger.info(f"   Ensemble mode: {ensemble_mode}")
        logger.info(f"   Models in config: {list(model_config.get('models', {}).keys())}")
        
        # Step 3: Initialize ModelManager with proper parameters
        logger.info("🧠 Step 3: Initialize ModelManager with configuration...")
        from models.ml_models import ModelManager
        
        model_manager = ModelManager(
            config_manager=config_manager,
            model_config=model_config,
            hardware_config=hardware_config
        )
        
        logger.info("✅ ModelManager initialized with clean manager architecture!")
        
        # Step 4: Test ModelManager methods
        logger.info("🔍 Step 4: Test ModelManager methods...")
        
        # Test models_loaded (should be False before loading)
        loaded = model_manager.models_loaded()
        logger.info(f"   Models loaded: {loaded}")
        
        # Test get_model_info
        model_info = model_manager.get_model_info()
        logger.info(f"   Model info: {model_info['model_count']} models configured")
        logger.info(f"   Device: {model_info['hardware_configuration']['device']}")
        
        logger.info("✅ All ModelManager tests passed!")
        logger.info("🎯 ModelManager is working correctly with clean architecture")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ModelManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_py_flow():
    """Test the exact flow that main.py should use"""
    logger.info("🚀 Testing main.py initialization flow...")
    
    try:
        # This mirrors the main.py flow exactly
        logger.info("🔄 Following main.py initialization sequence...")
        
        # Import what main.py imports
        from managers.config_manager import ConfigManager
        from managers.settings_manager import SettingsManager
        from managers.zero_shot_manager import ZeroShotManager
        from models.ml_models import ModelManager
        
        # Initialize like main.py
        logger.info("📋 Initializing core configuration managers...")
        config_manager = ConfigManager("/app/config")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        
        # Validate configuration
        logger.info("🔍 Validating configuration...")
        validation_result = config_manager.validate_configuration()
        if not validation_result['valid']:
            logger.error(f"❌ Configuration validation failed: {validation_result['errors']}")
            return False
        
        # Extract configuration
        logger.info("📊 Extracting processed configuration...")
        model_config = config_manager.get_model_configuration()
        hardware_config = config_manager.get_hardware_configuration()
        
        # Initialize ModelManager
        logger.info("🧠 Initializing Enhanced ModelManager with processed configuration...")
        model_manager = ModelManager(
            config_manager=config_manager,
            model_config=model_config,
            hardware_config=hardware_config
        )
        
        logger.info("✅ All main.py initialization steps completed successfully!")
        logger.info("🎯 main.py should work with this exact flow")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ main.py flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    logger.info("🔍 Testing ModelManager with Clean Manager Architecture")
    logger.info("=" * 60)
    
    # Test ModelManager with proper config
    if not test_modelmanager_with_proper_config():
        logger.error("❌ ModelManager config test failed")
        return False
    
    logger.info("\n" + "=" * 60)
    
    # Test main.py flow
    if not test_main_py_flow():
        logger.error("❌ main.py flow test failed")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ All tests passed!")
    logger.info("💡 The issue in your main.py is likely:")
    logger.info("   1. ModelManager being called without required parameters")
    logger.info("   2. Missing proper configuration extraction before ModelManager init")
    logger.info("   3. Import error in API endpoints preventing proper startup")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)