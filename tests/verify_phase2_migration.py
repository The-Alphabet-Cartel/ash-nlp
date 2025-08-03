#!/usr/bin/env python3
"""
Phase 2 Migration Verification Script
Tests the new ModelsManager integration to ensure everything works correctly
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging for verification
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verify_file_structure():
    """Verify all required files exist for Phase 2"""
    logger.info("🔍 Verifying Phase 2 file structure...")
    
    required_files = [
        'managers/models_manager.py',
        'config/models_configuration.json',
        'managers/config_manager.py',  # From Phase 1
        'managers/settings_manager.py',  # From Phase 1
        'managers/__init__.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
            logger.error(f"❌ Missing: {file_path}")
        else:
            logger.info(f"✅ Found: {file_path}")
    
    if missing_files:
        logger.error(f"❌ {len(missing_files)} required files missing for Phase 2")
        return False
    else:
        logger.info("✅ All Phase 2 files present")
        return True

def verify_imports():
    """Verify new manager imports work correctly"""
    logger.info("🔍 Verifying Phase 2 imports...")
    
    try:
        # Test ConfigManager import (from Phase 1)
        from managers.config_manager import ConfigManager
        logger.info("✅ ConfigManager import successful")
        
        # Test new ModelsManager import
        from managers.models_manager import ModelsManager
        logger.info("✅ ModelsManager import successful")
        
        # Test backward compatibility aliases
        from managers.models_manager import ModelManager, EnhancedModelManager
        logger.info("✅ Backward compatibility aliases working")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def verify_configuration_loading():
    """Verify JSON configuration loading works"""
    logger.info("🔍 Verifying configuration loading...")
    
    try:
        # This would normally be done by the existing ConfigManager
        import json
        
        # Check if models_configuration.json can be loaded
        config_file = Path('config/models_configuration.json')
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info("✅ models_configuration.json loads successfully")
            logger.debug(f"Configuration keys: {list(config.keys())}")
            return True
        else:
            logger.error("❌ config/models_configuration.json not found")
            return False
            
    except Exception as e:
        logger.error(f"❌ Configuration loading failed: {e}")
        return False

async def verify_models_manager_initialization():
    """Verify ModelsManager can be initialized with mock configuration"""
    logger.info("🔍 Verifying ModelsManager initialization...")
    
    try:
        from managers.models_manager import ModelsManager
        
        # Mock configuration for testing
        mock_config_manager = MockConfigManager()
        mock_model_config = {
            'depression_model': 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0',
            'sentiment_model': 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli',
            'emotional_distress_model': 'Lowerated/lm6-deberta-v3-topic-sentiment',
            'cache_dir': './models/cache',
            'ensemble_mode': 'majority',
            'depression_weight': 0.5,
            'sentiment_weight': 0.2,
            'emotional_distress_weight': 0.3,
            'gap_detection_enabled': True,
            'disagreement_threshold': 2
        }
        mock_hardware_config = {
            'device': 'cpu',  # Use CPU for testing
            'precision': 'float32',
            'max_batch_size': 8,
            'use_fast_tokenizer': True,
            'trust_remote_code': False,
            'model_revision': 'main'
        }
        
        # Initialize ModelsManager
        models_manager = ModelsManager(
            config_manager=mock_config_manager,
            model_config=mock_model_config,
            hardware_config=mock_hardware_config
        )
        
        logger.info("✅ ModelsManager initialized successfully")
        
        # Test status method
        status = models_manager.get_model_status()
        logger.info(f"✅ ModelsManager status: {status['models_loaded']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ModelsManager initialization failed: {e}")
        logger.exception("Initialization error details:")
        return False

class MockConfigManager:
    """Mock ConfigManager for testing"""
    
    def __init__(self):
        self.config = {}
    
    def get_config(self, key):
        return {}
    
    def get(self, key, default=None):
        return default

def verify_backward_compatibility():
    """Verify backward compatibility during migration period"""
    logger.info("🔍 Verifying backward compatibility...")
    
    try:
        # Test that old import patterns still work with aliases
        from managers.models_manager import ModelManager
        from managers.models_manager import EnhancedModelManager
        
        # Verify they're aliases to the same class
        from managers.models_manager import ModelsManager
        
        if ModelManager is ModelsManager and EnhancedModelManager is ModelsManager:
            logger.info("✅ Backward compatibility aliases working correctly")
            return True
        else:
            logger.error("❌ Backward compatibility aliases not set up correctly")
            return False
            
    except Exception as e:
        logger.error(f"❌ Backward compatibility verification failed: {e}")
        return False

async def run_verification():
    """Run all Phase 2 verification tests"""
    logger.info("🚀 Starting Phase 2 Migration Verification")
    logger.info("=" * 50)
    
    verification_results = {
        'file_structure': verify_file_structure(),
        'imports': verify_imports(),
        'configuration_loading': verify_configuration_loading(),
        'models_manager_init': await verify_models_manager_initialization(),
        'backward_compatibility': verify_backward_compatibility()
    }
    
    # Summary
    logger.info("=" * 50)
    logger.info("📊 Phase 2 Verification Results:")
    
    all_passed = True
    for test_name, result in verification_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("🎉 Phase 2 Migration Verification: ALL TESTS PASSED")
        logger.info("✅ Ready to implement Phase 2 migration")
        return 0
    else:
        logger.error("❌ Phase 2 Migration Verification: SOME TESTS FAILED")
        logger.error("🔴 Fix issues before implementing Phase 2 migration")
        return 1

if __name__ == "__main__":
    """Run verification script"""
    exit_code = asyncio.run(run_verification())
    sys.exit(exit_code)