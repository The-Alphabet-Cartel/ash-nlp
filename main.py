#!/usr/bin/env python3
"""
Debug version of main.py to identify startup issues
"""

import sys
import logging
import traceback
import time

# Set up basic logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug.log')
    ]
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test all imports step by step"""
    logger.info("🔍 Testing imports...")
    
    try:
        logger.info("Testing FastAPI...")
        from fastapi import FastAPI
        logger.info("✅ FastAPI OK")
        
        logger.info("Testing managers...")
        import managers
        logger.info("✅ Managers OK")
        
        logger.info("Testing managers functions...")
        from managers import get_managers_status
        status = get_managers_status()
        logger.info(f"📊 Manager status: {status}")
        
        logger.info("Testing models...")
        from models.pydantic_models import MessageRequest, CrisisResponse, HealthResponse
        logger.info("✅ Pydantic models OK")
        
        logger.info("Testing ML models...")
        from models.ml_models import EnhancedModelManager
        logger.info("✅ ML models OK")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_configuration():
    """Test configuration loading"""
    logger.info("🔧 Testing configuration...")
    
    try:
        from managers import (
            get_model_ensemble_manager,
            get_env_config,
            get_nlp_config,
            MANAGERS_STATUS
        )
        
        logger.info(f"Manager status: {MANAGERS_STATUS}")
        
        # Test env config
        config = get_env_config()
        logger.info(f"Environment config keys: {list(config.keys()) if config else 'None'}")
        
        # Test NLP config
        nlp_config = get_nlp_config()
        logger.info(f"NLP config available: {nlp_config is not None}")
        
        # Test ensemble manager
        try:
            ensemble_manager = get_model_ensemble_manager()
            summary = ensemble_manager.get_summary()
            logger.info(f"Ensemble manager summary: {summary}")
        except Exception as e:
            logger.warning(f"Ensemble manager not available: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Configuration test failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_fastapi_creation():
    """Test FastAPI app creation"""
    logger.info("🚀 Testing FastAPI app creation...")
    
    try:
        from fastapi import FastAPI
        
        app = FastAPI(
            title="Debug Ash NLP Service",
            version="debug",
            description="Debug version to test startup"
        )
        
        @app.get("/health")
        def health():
            return {"status": "ok", "message": "Debug version running"}
        
        logger.info("✅ FastAPI app created successfully")
        return app
        
    except Exception as e:
        logger.error(f"❌ FastAPI creation failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

def main():
    """Main debug function"""
    logger.info("🚀 Starting debug main.py...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {sys.path[0]}")
    
    try:
        # Test imports
        if not test_imports():
            logger.error("❌ Import tests failed")
            return 1
        
        # Test configuration
        if not test_configuration():
            logger.error("❌ Configuration tests failed")
            return 1
        
        # Test FastAPI
        app = test_fastapi_creation()
        if not app:
            logger.error("❌ FastAPI creation failed")
            return 1
        
        # Test server startup
        logger.info("🌐 Testing server startup...")
        import uvicorn
        
        logger.info("✅ All tests passed! Starting server...")
        logger.info("🌐 Server should start on http://0.0.0.0:8881")
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8881,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown requested")
        return 0
    except Exception as e:
        logger.error(f"❌ Main execution failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        logger.info(f"🏁 Exiting with code: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)