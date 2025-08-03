#!/usr/bin/env python3
"""
Debug startup script to identify silent failures
Run this BEFORE running main.py to catch import errors
"""

import sys
import os
import traceback

def debug_python_environment():
    """Debug Python environment and path"""
    print("🐍 Python Environment Debug")
    print(f"   Python version: {sys.version}")
    print(f"   Python executable: {sys.executable}")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
    print(f"   Python path: {sys.path}")

def debug_critical_imports():
    """Test critical imports that could cause silent failure"""
    print("\n📦 Testing Critical Imports...")
    
    imports_to_test = [
        ('os', 'Built-in module'),
        ('logging', 'Built-in logging'),
        ('fastapi', 'FastAPI framework'),
        ('uvicorn', 'ASGI server'),
        ('pathlib', 'Path handling'),
        ('contextlib', 'Context managers'),
        ('pydantic', 'Data validation'),
    ]
    
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {module_name}: {description}")
        except ImportError as e:
            print(f"   ❌ {module_name}: FAILED - {e}")
            return False
    
    return True

def test_manager_imports():
    """Test manager imports specifically"""
    print("\n🔧 Testing Manager Imports...")
    
    manager_imports = [
        'managers.config_manager',
        'managers.settings_manager', 
        'managers.zero_shot_manager'
    ]
    
    for manager in manager_imports:
        try:
            __import__(manager)
            print(f"   ✅ {manager}")
        except ImportError as e:
            print(f"   ❌ {manager}: {e}")
            traceback.print_exc()
            return False
    
    return True

def test_api_imports():
    """Test API imports"""
    print("\n🌐 Testing API Imports...")
    
    try:
        from api.ensemble_endpoints import add_ensemble_endpoints
        print("   ✅ api.ensemble_endpoints")
    except ImportError as e:
        print(f"   ❌ api.ensemble_endpoints: {e}")
        traceback.print_exc()
        return False
    
    try:
        from api.learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
        print("   ✅ api.learning_endpoints")
    except ImportError as e:
        print(f"   ❌ api.learning_endpoints: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_model_imports():
    """Test model imports"""
    print("\n🧠 Testing Model Imports...")
    
    try:
        from models.ml_models import ModelManager
        print("   ✅ models.ml_models")
    except ImportError as e:
        print(f"   ❌ models.ml_models: {e}")
        traceback.print_exc()
        return False
    
    try:
        from models.pydantic_models import MessageRequest, CrisisResponse, HealthResponse
        print("   ✅ models.pydantic_models")
    except ImportError as e:
        print(f"   ❌ models.pydantic_models: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_config_directory():
    """Test config directory and files"""
    print("\n📁 Testing Configuration Directory...")
    
    config_dir = "/app/config"
    if not os.path.exists(config_dir):
        print(f"   ❌ Config directory missing: {config_dir}")
        return False
    
    required_files = [
        'model_ensemble.json',
    ]
    
    for file_name in required_files:
        file_path = os.path.join(config_dir, file_name)
        if os.path.exists(file_path):
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ Missing: {file_name}")
            return False
    
    return True

def test_environment_variables():
    """Test critical environment variables"""
    print("\n🌍 Testing Environment Variables...")
    
    critical_env_vars = [
        'GLOBAL_LOG_LEVEL',
        'NLP_LOG_FILE',
        'GLOBAL_ENABLE_DEBUG_MODE',
        'GLOBAL_ENABLE_LEARNING_SYSTEM',
    ]
    
    for var in critical_env_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️ {var}: Not set (using defaults)")
    
    return True

def main():
    """Main debug function"""
    print("🔍 Ash NLP Service Startup Debug")
    print("=" * 50)
    
    try:
        # Test Python environment
        debug_python_environment()
        
        # Test critical imports
        if not debug_critical_imports():
            print("\n❌ Critical import failure detected!")
            return False
        
        # Test environment variables
        test_environment_variables()
        
        # Test config directory
        if not test_config_directory():
            print("\n❌ Configuration directory issues detected!")
            return False
        
        # Test manager imports
        if not test_manager_imports():
            print("\n❌ Manager import failure detected!")
            return False
        
        # Test API imports
        if not test_api_imports():
            print("\n❌ API import failure detected!")
            return False
        
        # Test model imports
        if not test_model_imports():
            print("\n❌ Model import failure detected!")
            return False
        
        print("\n✅ All debug checks passed!")
        print("🚀 You can now try running main.py")
        return True
        
    except Exception as e:
        print(f"\n💥 Unexpected error during debug: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)