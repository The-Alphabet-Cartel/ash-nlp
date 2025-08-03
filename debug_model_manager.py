#!/usr/bin/env python3
"""
Debug ModelManager import and initialization specifically
"""

import os
import sys
import logging
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_model_dependencies():
    """Test ModelManager dependencies step by step"""
    logger.info("🔍 Testing ModelManager dependencies...")
    
    dependencies = [
        ('torch', 'PyTorch'),
        ('transformers', 'Hugging Face Transformers'),
        ('numpy', 'NumPy'),
        ('asyncio', 'AsyncIO'),
        ('concurrent.futures', 'Threading'),
        ('pathlib', 'Path utilities'),
        ('typing', 'Type hints'),
    ]
    
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            logger.info(f"   ✅ {module_name}: {description}")
        except ImportError as e:
            logger.error(f"   ❌ {module_name}: FAILED - {e}")
            return False
    
    return True

def test_models_directory():
    """Test if models directory structure exists"""
    logger.info("📁 Testing models directory structure...")
    
    try:
        import models
        logger.info("✅ models package importable")
        
        # Check for specific files
        models_dir = "/app/models"
        if os.path.exists(models_dir):
            logger.info(f"✅ Models directory exists: {models_dir}")
            files = os.listdir(models_dir)
            logger.info(f"   Files: {files}")
        else:
            logger.error(f"❌ Models directory missing: {models_dir}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Models directory test failed: {e}")
        return False

def test_ml_models_import():
    """Test ml_models.py import step by step"""
    logger.info("🧠 Testing ml_models.py import step by step...")
    
    try:
        # Test if the file exists
        ml_models_path = "/app/models/ml_models.py"
        if os.path.exists(ml_models_path):
            logger.info(f"✅ ml_models.py file exists: {ml_models_path}")
        else:
            logger.error(f"❌ ml_models.py file missing: {ml_models_path}")
            return False
        
        # Test syntax compilation
        logger.info("🔍 Testing ml_models.py syntax...")
        with open(ml_models_path, 'r') as f:
            source = f.read()
        
        compile(source, ml_models_path, 'exec')
        logger.info("✅ ml_models.py syntax is valid")
        
        # Try importing step by step
        logger.info("📦 Attempting import of models.ml_models...")
        
        # Import with detailed error reporting
        try:
            import models.ml_models
            logger.info("✅ models.ml_models imported successfully")
            
            # Check if ModelManager class exists
            if hasattr(models.ml_models, 'ModelManager'):
                logger.info("✅ ModelManager class found")
            else:
                logger.error("❌ ModelManager class not found in models.ml_models")
                return False
                
        except ImportError as e:
            logger.error(f"❌ Import error in models.ml_models: {e}")
            traceback.print_exc()
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error importing models.ml_models: {e}")
            traceback.print_exc()
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ml_models import test failed: {e}")
        traceback.print_exc()
        return False

def test_model_manager_class():
    """Test ModelManager class instantiation"""
    logger.info("🏗️ Testing ModelManager class instantiation...")
    
    try:
        from models.ml_models import ModelManager
        logger.info("✅ ModelManager imported successfully")
        
        # Test basic instantiation (no config)
        logger.info("🔧 Testing basic ModelManager instantiation...")
        try:
            model_manager = ModelManager()
            logger.info("✅ ModelManager basic instantiation successful")
        except Exception as e:
            logger.error(f"❌ ModelManager basic instantiation failed: {e}")
            traceback.print_exc()
            return False
        
        # Test with config manager
        logger.info("🔧 Testing ModelManager with config...")
        try:
            from managers.config_manager import ConfigManager
            config_manager = ConfigManager("/app/config")
            model_config = config_manager.get_model_configuration()
            hardware_config = config_manager.get_hardware_configuration()
            
            model_manager_with_config = ModelManager(
                config_manager=config_manager,
                model_config=model_config,
                hardware_config=hardware_config
            )
            logger.info("✅ ModelManager with config instantiation successful")
            
        except Exception as e:
            logger.error(f"❌ ModelManager with config failed: {e}")
            traceback.print_exc()
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ModelManager class test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    logger.info("🔍 Debugging ModelManager Import Issue")
    logger.info("=" * 50)
    
    # Test dependencies
    if not test_model_dependencies():
        logger.error("❌ ModelManager dependencies failed")
        return False
    
    # Test models directory
    if not test_models_directory():
        logger.error("❌ Models directory test failed")
        return False
    
    # Test ml_models.py import
    if not test_ml_models_import():
        logger.error("❌ ml_models.py import failed")
        return False
    
    # Test ModelManager class
    if not test_model_manager_class():
        logger.error("❌ ModelManager class test failed")
        return False
    
    logger.info("✅ All ModelManager debug tests passed!")
    logger.info("🎯 ModelManager should work correctly")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        logger.error("❌ ModelManager debug failed")
        sys.exit(1)
    else:
        logger.info("✅ ModelManager debug successful")
        sys.exit(0)