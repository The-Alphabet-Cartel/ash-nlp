#!/usr/bin/env python3
"""
Minimal startup test to isolate silent failure
This strips down main.py to the absolute minimum
"""

import os
import sys
import logging

# Set up basic logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_basic_startup():
    """Test the most basic startup sequence"""
    try:
        logger.info("🔄 Starting minimal startup test...")
        
        # Test 1: Basic imports
        logger.info("📦 Testing basic imports...")
        from fastapi import FastAPI
        from contextlib import asynccontextmanager
        logger.info("✅ Basic FastAPI imports successful")
        
        # Test 2: Manager imports
        logger.info("🔧 Testing manager imports...")
        from managers.config_manager import ConfigManager
        from managers.settings_manager import SettingsManager
        from managers.zero_shot_manager import ZeroShotManager
        logger.info("✅ Manager imports successful")
        
        # Test 3: Initialize config manager
        logger.info("📋 Testing config manager initialization...")
        config_manager = ConfigManager("/app/config")
        logger.info("✅ ConfigManager initialized")
        
        # Test 4: Initialize other managers
        logger.info("⚙️ Testing other manager initialization...")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        logger.info("✅ All managers initialized")
        
        # Test 5: Validate configuration
        logger.info("🔍 Testing configuration validation...")
        validation_result = config_manager.validate_configuration()
        logger.info(f"✅ Configuration validation: {validation_result}")
        
        # Test 6: Try to create FastAPI app
        logger.info("🌐 Testing FastAPI app creation...")
        
        @asynccontextmanager
        async def minimal_lifespan(app: FastAPI):
            logger.info("🚀 Minimal lifespan startup")
            yield
            logger.info("🛑 Minimal lifespan shutdown")
        
        app = FastAPI(
            title="Minimal Test App",
            lifespan=minimal_lifespan
        )
        logger.info("✅ FastAPI app created successfully")
        
        @app.get("/test")
        async def test_endpoint():
            return {"status": "ok", "message": "Minimal test successful"}
        
        logger.info("✅ All minimal startup tests passed!")
        logger.info("🎯 The issue is likely in a specific component, not basic setup")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_manager():
    """Test ModelManager specifically"""
    try:
        logger.info("🧠 Testing ModelManager import...")
        from models.ml_models import ModelManager
        logger.info("✅ ModelManager import successful")
        
        logger.info("🔧 Testing ModelManager initialization...")
        # Try without config first
        model_manager = ModelManager()
        logger.info("✅ ModelManager basic initialization successful")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ModelManager error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_imports():
    """Test API imports specifically"""
    try:
        logger.info("🌐 Testing API imports...")
        
        from api.ensemble_endpoints import add_ensemble_endpoints
        logger.info("✅ ensemble_endpoints import successful")
        
        from api.learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints  
        logger.info("✅ enhanced_learning_endpoints import successful")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    logger.info("🔍 Starting Minimal Startup Test")
    logger.info("=" * 50)
    
    # Test basic startup
    if not test_basic_startup():
        logger.error("❌ Basic startup test failed")
        return False
    
    # Test model manager
    if not test_model_manager():
        logger.error("❌ ModelManager test failed")
        return False
    
    # Test API imports
    if not test_api_imports():
        logger.error("❌ API imports test failed")
        return False
    
    logger.info("✅ All minimal tests passed!")
    logger.info("🎯 Ready to test full main.py")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        logger.error("❌ Minimal startup test failed")
        sys.exit(1)
    else:
        logger.info("✅ Minimal startup test successful")
        sys.exit(0)