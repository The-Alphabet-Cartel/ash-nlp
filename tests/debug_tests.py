#!/usr/bin/env python3
"""
Debug script for Phase 3e Step 7 test issues
Helps identify and fix import and structural issues

FILE: tests/debug_test_issues.py
VERSION: v3.1-3e-7-debug-1
"""

import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='[DEBUG] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test all imports to identify issues"""
    logger.info("🔍 Testing imports...")
    
    # Test basic manager imports
    try:
        from managers.unified_config import create_unified_config_manager
        logger.info("✅ unified_config import: OK")
    except ImportError as e:
        logger.error(f"❌ unified_config import failed: {e}")
        
    try:
        from managers.learning_system import create_learning_system_manager
        logger.info("✅ learning_system import: OK")
    except ImportError as e:
        logger.error(f"❌ learning_system import failed: {e}")
        
    try:
        from managers.shared_utilities import create_shared_utilities_manager
        logger.info("✅ shared_utilities import: OK")
    except ImportError as e:
        logger.error(f"❌ shared_utilities import failed: {e}")
        
    try:
        from analysis.crisis_analyzer import create_crisis_analyzer
        logger.info("✅ crisis_analyzer import: OK")
    except ImportError as e:
        logger.error(f"❌ crisis_analyzer import failed: {e}")
        
    try:
        from main import initialize_unified_managers
        logger.info("✅ main.initialize_unified_managers import: OK")
    except ImportError as e:
        logger.error(f"❌ main.initialize_unified_managers import failed: {e}")

def test_manager_creation():
    """Test basic manager creation"""
    logger.info("🔧 Testing manager creation...")
    
    try:
        from managers.unified_config import create_unified_config_manager
        unified_config = create_unified_config_manager()
        logger.info(f"✅ UnifiedConfigManager created: {type(unified_config)}")
        
        # Test shared utilities manager
        from managers.shared_utilities import create_shared_utilities_manager
        shared_utils = create_shared_utilities_manager(unified_config)
        logger.info(f"✅ SharedUtilitiesManager created: {type(shared_utils)}")
        
        # Test learning system manager
        from managers.learning_system import create_learning_system_manager
        learning_system = create_learning_system_manager(unified_config, shared_utils=shared_utils)
        logger.info(f"✅ LearningSystemManager created: {type(learning_system)}")
        
        # Check learning system attributes
        if hasattr(learning_system, 'shared_utils'):
            logger.info("✅ LearningSystemManager has shared_utils attribute")
        else:
            logger.warning("⚠️ LearningSystemManager missing shared_utils attribute")
            logger.info(f"Available attributes: {[attr for attr in dir(learning_system) if not attr.startswith('_')]}")
            
        # Test crisis analyzer creation
        from analysis.crisis_analyzer import create_crisis_analyzer
        from managers.model_coordination import create_model_coordination_manager
        
        model_coordination = create_model_coordination_manager(unified_config)
        logger.info(f"✅ ModelCoordinationManager created: {type(model_coordination)}")
        
        crisis_analyzer = create_crisis_analyzer(
            unified_config,
            model_coordination_manager=model_coordination,
            shared_utilities_manager=shared_utils,
            learning_system_manager=learning_system
        )
        logger.info(f"✅ CrisisAnalyzer created: {type(crisis_analyzer)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Manager creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_initialization():
    """Test main system initialization"""
    logger.info("🚀 Testing main system initialization...")
    
    try:
        from main import initialize_unified_managers
        managers = initialize_unified_managers()
        
        logger.info(f"✅ System initialized with {len(managers)} managers")
        logger.info(f"Manager keys: {list(managers.keys())}")
        
        # Test specific managers
        crisis_analyzer = managers.get('crisis_analyzer')
        if crisis_analyzer:
            logger.info("✅ CrisisAnalyzer available in managers")
            
            # Check for analysis methods
            analysis_methods = ['analyze_message', 'analyze']
            available_methods = [method for method in analysis_methods if hasattr(crisis_analyzer, method)]
            logger.info(f"Analysis methods available: {available_methods}")
        else:
            logger.error("❌ CrisisAnalyzer not found in managers")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Main initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all debug tests"""
    logger.info("🌈 Starting Phase 3e Step 7 Debug Tests")
    logger.info("=" * 50)
    
    results = {}
    
    # Test 1: Imports
    logger.info("\n1. Testing Imports")
    logger.info("-" * 20)
    test_imports()
    
    # Test 2: Manager Creation
    logger.info("\n2. Testing Manager Creation")
    logger.info("-" * 30)
    results['manager_creation'] = test_manager_creation()
    
    # Test 3: Main Initialization
    logger.info("\n3. Testing Main Initialization")
    logger.info("-" * 35)
    results['main_initialization'] = test_main_initialization()
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("🎯 DEBUG TEST SUMMARY")
    logger.info("=" * 50)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    overall_success = all(results.values())
    if overall_success:
        logger.info("\n🚀 All debug tests passed! Ready for integration testing.")
        return 0
    else:
        logger.error("\n❌ Some debug tests failed. Fix issues before running full tests.")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)