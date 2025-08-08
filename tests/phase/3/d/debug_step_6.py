# tests/phase/3/d/debug_step_6.py
"""
Debug script for Step 6 test failures
Run this to identify why the test is silently failing
"""

import sys
import os
import traceback

def debug_imports():
    """Debug import issues step by step"""
    print("🔍 Starting Step 6 Debug Session")
    print("=" * 60)
    
    # Test 1: Basic Python execution
    print("🧪 Test 1: Basic Python execution")
    try:
        print("✅ Python execution working")
    except Exception as e:
        print(f"❌ Python execution failed: {e}")
        return False
    
    # Test 2: System path
    print(f"\n🧪 Test 2: Python path")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   Python path entries:")
    for i, path in enumerate(sys.path):
        print(f"     {i}: {path}")
    
    # Test 3: Basic logging
    print(f"\n🧪 Test 3: Basic logging import")
    try:
        import logging
        print("✅ logging module imported successfully")
    except Exception as e:
        print(f"❌ logging import failed: {e}")
        return False
    
    # Test 4: tempfile and pathlib
    print(f"\n🧪 Test 4: Standard library imports")
    try:
        import tempfile
        import json
        from pathlib import Path
        from unittest.mock import patch, mock_open
        print("✅ Standard library imports successful")
    except Exception as e:
        print(f"❌ Standard library import failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 5: Manager imports (the likely culprit)
    print(f"\n🧪 Test 5: ConfigManager import")
    try:
        # Add /app to path if not already there
        if '/app' not in sys.path:
            sys.path.insert(0, '/app')
            print("   Added /app to Python path")
        
        from managers.config_manager import ConfigManager, create_config_manager
        print("✅ ConfigManager imported successfully")
    except Exception as e:
        print(f"❌ ConfigManager import failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 6: LoggingConfigManager import
    print(f"\n🧪 Test 6: LoggingConfigManager import")
    try:
        from managers.logging_config_manager import LoggingConfigManager, create_logging_config_manager
        print("✅ LoggingConfigManager imported successfully")
    except Exception as e:
        print(f"❌ LoggingConfigManager import failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 7: Check if files exist
    print(f"\n🧪 Test 7: File existence check")
    files_to_check = [
        '/app/managers/config_manager.py',
        '/app/managers/logging_config_manager.py',
        '/app/config/logging_settings.json',
        '/app/tests/phase/3/d/test_step_6_integration.py'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} NOT FOUND")
    
    # Test 8: Try running a basic ConfigManager test
    print(f"\n🧪 Test 8: Basic ConfigManager functionality")
    try:
        config_manager = create_config_manager('/app/config')
        print("✅ ConfigManager factory function works")
        
        # Try to get logging configuration
        logging_config = config_manager.get_logging_configuration()
        print(f"✅ get_logging_configuration() works: {type(logging_config)}")
        
    except Exception as e:
        print(f"❌ ConfigManager functionality failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 9: Try creating LoggingConfigManager
    print(f"\n🧪 Test 9: LoggingConfigManager creation")
    try:
        logging_manager = create_logging_config_manager(config_manager)
        print("✅ LoggingConfigManager factory function works")
        
        # Try convenience methods
        log_level = logging_manager.get_log_level()
        print(f"✅ get_log_level() works: {log_level}")
        
        should_log = logging_manager.should_log_detailed()
        print(f"✅ should_log_detailed() works: {should_log}")
        
    except Exception as e:
        print(f"❌ LoggingConfigManager creation failed: {e}")
        traceback.print_exc()
        return False
    
    print(f"\n🎉 All debug tests passed!")
    print("The components are working - the issue is likely in the test file itself")
    return True

def check_test_file():
    """Check the actual test file for syntax errors"""
    print(f"\n🧪 Test 10: Check test file syntax")
    
    test_file_path = '/app/tests/phase/3/d/test_step_6_integration.py'
    
    if not os.path.exists(test_file_path):
        print(f"❌ Test file not found: {test_file_path}")
        return False
    
    try:
        # Try to compile the test file
        with open(test_file_path, 'r') as f:
            test_content = f.read()
        
        compile(test_content, test_file_path, 'exec')
        print("✅ Test file syntax is valid")
        
        # Try to execute it in a safe way
        print("🔍 Attempting to import test file...")
        
        # Add the test directory to path
        test_dir = os.path.dirname(test_file_path)
        if test_dir not in sys.path:
            sys.path.insert(0, test_dir)
        
        # Try importing as module
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_step_6_integration", test_file_path)
        test_module = importlib.util.module_from_spec(spec)
        
        # Execute the module to check for runtime errors
        spec.loader.exec_module(test_module)
        print("✅ Test file imported successfully")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in test file: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Runtime error in test file: {e}")
        traceback.print_exc()
        return False

def run_minimal_test():
    """Run a minimal version of the Step 6 test"""
    print(f"\n🧪 Test 11: Minimal Step 6 test")
    
    try:
        # Import required modules
        if '/app' not in sys.path:
            sys.path.insert(0, '/app')
        
        from managers.config_manager import create_config_manager
        from managers.logging_config_manager import create_logging_config_manager
        import tempfile
        import json
        from pathlib import Path
        
        # Test 1: ConfigManager Logging Support
        print("   🧪 Testing ConfigManager logging support...")
        config_manager = create_config_manager('/app/config')
        logging_config = config_manager.get_logging_configuration()
        assert isinstance(logging_config, dict)
        print("   ✅ ConfigManager.get_logging_configuration() works correctly")
        
        # Test 2: LoggingConfigManager basic functionality
        print("   🧪 Testing LoggingConfigManager...")
        logging_manager = create_logging_config_manager(config_manager)
        
        # Test basic methods
        global_settings = logging_manager.get_global_logging_settings()
        detailed_settings = logging_manager.get_detailed_logging_settings() 
        component_settings = logging_manager.get_component_logging_settings()
        
        assert isinstance(global_settings, dict)
        assert isinstance(detailed_settings, dict)
        assert isinstance(component_settings, dict)
        print("   ✅ Basic LoggingConfigManager methods work")
        
        # Test convenience methods
        log_level = logging_manager.get_log_level()
        should_log = logging_manager.should_log_detailed()
        should_include = logging_manager.should_include_reasoning()
        log_path = logging_manager.get_log_file_path()
        
        assert isinstance(log_level, str)
        assert isinstance(should_log, bool)
        assert isinstance(should_include, bool)
        assert isinstance(log_path, str)
        print("   ✅ Convenience methods work correctly")
        
        # Test component checks
        threshold_check = logging_manager.should_log_component('threshold_changes')
        model_check = logging_manager.should_log_component('model_disagreements')
        
        assert isinstance(threshold_check, bool)
        assert isinstance(model_check, bool)
        print("   ✅ Component logging checks work")
        
        print("🎉 Minimal Step 6 test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Minimal test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Running Step 6 Debug Session")
    
    # Run all debug tests
    imports_ok = debug_imports()
    
    if imports_ok:
        file_ok = check_test_file()
        
        if file_ok:
            minimal_ok = run_minimal_test()
            
            if minimal_ok:
                print("\n✅ All debug tests passed - the core functionality works!")
                print("🔍 The issue is likely in the specific test implementation")
                print("💡 Try running the test with more verbose output:")
                print("   docker compose exec ash-nlp python -v tests/phase/3/d/test_step_6_integration.py")
            else:
                print("\n❌ Minimal test failed - there are issues with the core functionality")
        else:
            print("\n❌ Test file has issues")
    else:
        print("\n❌ Import issues detected")
    
    print("\n🏁 Debug session complete")