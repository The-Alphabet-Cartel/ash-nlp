#!/usr/bin/env python3
"""
Debug startup script to identify import issues
"""

import sys
import traceback

def test_import(module_name, description):
    """Test importing a module and report results"""
    try:
        __import__(module_name)
        print(f"✅ {description}: OK")
        return True
    except Exception as e:
        print(f"❌ {description}: FAILED")
        print(f"   Error: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def main():
    print("🔍 Debugging Ash NLP startup...")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path}")
    
    success = True
    
    # Test core imports
    success &= test_import("logging", "Basic logging")
    success &= test_import("os", "Basic os")
    success &= test_import("pathlib", "Basic pathlib")
    
    # Test framework imports
    success &= test_import("fastapi", "FastAPI framework")
    success &= test_import("uvicorn", "Uvicorn server")
    success &= test_import("torch", "PyTorch")
    success &= test_import("transformers", "Transformers")
    
    # Test our managers
    success &= test_import("managers", "Managers package")
    
    if success:
        print("\n✅ All basic imports successful, testing managers components...")
        
        try:
            from managers import get_managers_status, MANAGERS_STATUS
            print(f"📊 Manager status: {get_managers_status()}")
        except Exception as e:
            print(f"❌ Manager status check failed: {e}")
            success = False
    
    # Test main.py import
    success &= test_import("main", "Main application")
    
    if success:
        print("\n🎉 All imports successful! The issue might be in runtime execution.")
    else:
        print("\n💥 Import failures detected. Check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())