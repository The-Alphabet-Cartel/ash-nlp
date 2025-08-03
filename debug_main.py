#!/usr/bin/env python3
"""
Debug main.py execution step by step to find silent failure point
"""

import os
import sys
import logging
import traceback

# Set up logging exactly like main.py would
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_main_py_imports():
    """Test the imports from main.py step by step"""
    logger.info("🔍 Testing main.py imports step by step...")
    
    try:
        # Test basic imports
        logger.info("📦 Testing basic imports...")
        import os
        import time
        import logging
        from contextlib import asynccontextmanager
        from fastapi import FastAPI
        from pydantic import BaseModel
        logger.info("✅ Basic imports successful")
        
        # Test manager imports (these worked in debug)
        logger.info("🔧 Testing manager imports...")
        from managers.config_manager import ConfigManager
        from managers.settings_manager import SettingsManager
        from managers.zero_shot_manager import ZeroShotManager
        logger.info("✅ Manager imports successful")
        
        # Test model imports
        logger.info("🧠 Testing model imports...")
        from models.ml_models import ModelManager
        logger.info("✅ Model imports successful")
        
        # Test API imports (these also worked in debug)
        logger.info("🌐 Testing API imports...")
        from api.ensemble_endpoints import add_ensemble_endpoints
        from api.learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
        logger.info("✅ API imports successful")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import error in main.py sequence: {e}")
        traceback.print_exc()
        return False

def test_main_py_initialization():
    """Test the initialization sequence from main.py"""
    logger.info("🚀 Testing main.py initialization sequence...")
    
    try:
        # Import what we need
        from managers.config_manager import ConfigManager
        from managers.settings_manager import SettingsManager
        from managers.zero_shot_manager import ZeroShotManager
        from models.ml_models import ModelManager
        
        # Test Step 1: Initialize managers (like main.py does)
        logger.info("📋 Step 1: Initialize core configuration managers...")
        config_manager = ConfigManager("/app/config")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        logger.info("✅ Core managers initialized")
        
        # Test Step 2: Validate configuration
        logger.info("🔍 Step 2: Validate configuration...")
        validation_result = config_manager.validate_configuration()
        if not validation_result['valid']:
            logger.error(f"❌ Configuration validation failed: {validation_result['errors']}")
            return False
        logger.info("✅ Configuration validation passed")
        
        # Test Step 3: Extract configuration
        logger.info("📊 Step 3: Extract processed configuration...")
        model_config = config_manager.get_model_configuration()
        hardware_config = config_manager.get_hardware_configuration()
        threshold_config = config_manager.get_threshold_configuration()
        feature_flags = config_manager.get_feature_flags()
        ensemble_mode = config_manager.get_ensemble_mode()
        logger.info("✅ Configuration extracted successfully")
        
        # Test Step 4: Initialize ModelManager with config
        logger.info("🧠 Step 4: Initialize ModelManager with configuration...")
        model_manager = ModelManager(
            config_manager=config_manager,
            model_config=model_config,
            hardware_config=hardware_config
        )
        logger.info("✅ ModelManager initialized with config")
        
        # Test Step 5: Try to load models (this might be where it fails)
        logger.info("📦 Step 5: Test model loading (this might fail silently)...")
        try:
            # Don't actually load models, just test if the method exists
            if hasattr(model_manager, 'load_models'):
                logger.info("✅ ModelManager has load_models method")
            else:
                logger.error("❌ ModelManager missing load_models method")
                return False
        except Exception as e:
            logger.error(f"❌ Model loading test failed: {e}")
            traceback.print_exc()
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Initialization error: {e}")
        traceback.print_exc()
        return False

def test_fastapi_creation():
    """Test FastAPI app creation like main.py does"""
    logger.info("🌐 Testing FastAPI app creation...")
    
    try:
        from fastapi import FastAPI
        from contextlib import asynccontextmanager
        
        # Create a minimal lifespan like main.py
        @asynccontextmanager
        async def test_lifespan(app: FastAPI):
            logger.info("🚀 Test lifespan startup")
            yield
            logger.info("🛑 Test lifespan shutdown")
        
        # Create FastAPI app like main.py does
        app = FastAPI(
            title="Debug Test App",
            version="3.1.0",
            description="Debug test for main.py",
            lifespan=test_lifespan
        )
        
        logger.info("✅ FastAPI app created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ FastAPI creation failed: {e}")
        traceback.print_exc()
        return False

def test_uvicorn_startup():
    """Test if uvicorn would be able to start the app"""
    logger.info("🔄 Testing uvicorn startup capability...")
    
    try:
        import uvicorn
        logger.info("✅ uvicorn import successful")
        
        # Don't actually start uvicorn, just test if it would work
        logger.info("✅ uvicorn startup test would succeed")
        return True
        
    except Exception as e:
        logger.error(f"❌ uvicorn test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    logger.info("🔍 Debugging main.py Silent Failure")
    logger.info("=" * 50)
    
    # Test imports
    if not test_main_py_imports():
        logger.error("❌ main.py imports failed")
        return False
    
    # Test initialization sequence
    if not test_main_py_initialization():
        logger.error("❌ main.py initialization failed")
        return False
    
    # Test FastAPI creation
    if not test_fastapi_creation():
        logger.error("❌ FastAPI creation failed")
        return False
    
    # Test uvicorn capability
    if not test_uvicorn_startup():
        logger.error("❌ uvicorn startup test failed")
        return False
    
    logger.info("✅ All main.py debug tests passed!")
    logger.info("🤔 The silent failure might be:")
    logger.info("   1. Model loading taking too long and timing out")
    logger.info("   2. uvicorn not starting properly")
    logger.info("   3. Docker container issue")
    logger.info("   4. FastAPI lifespan context manager issue")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        logger.error("❌ main.py debug failed")
        sys.exit(1)
    else:
        logger.info("✅ main.py debug successful")
        sys.exit(0)