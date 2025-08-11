#!/usr/bin/env python3
"""
Step 9.8 Progress Test - Check what we've fixed so far

This test checks:
1. If syntax error is fixed (CrisisPatternManager startup)
2. If managers/__init__.py can import correctly
3. What ConfigManager references remain
"""

import sys
import traceback

def test_crisis_pattern_manager():
    """Test that CrisisPatternManager starts without syntax errors"""
    print("🧪 Testing CrisisPatternManager startup...")
    try:
        from managers.unified_config_manager import create_unified_config_manager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        
        config_manager = create_unified_config_manager("/app/config")
        crisis_manager = create_crisis_pattern_manager(config_manager)
        
        status = crisis_manager.get_status()
        print(f"✅ CrisisPatternManager status: {status['status']}")
        print(f"✅ Config manager type: {status['config_manager']}")
        print(f"✅ Version: {status['version']}")
        return True
    except Exception as e:
        print(f"❌ CrisisPatternManager test failed: {e}")
        traceback.print_exc()
        return False

def test_managers_init():
    """Test that managers.__init__.py imports correctly"""
    print("\n🧪 Testing managers.__init__.py imports...")
    try:
        import managers
        
        print(f"✅ Managers module imported")
        
        # Check what's available
        if hasattr(managers, 'UnifiedConfigManager'):
            print("✅ UnifiedConfigManager available")
        else:
            print("❌ UnifiedConfigManager NOT available")
            
        if hasattr(managers, 'ConfigManager'):
            print("⚠️ ConfigManager still available (needs removal)")
        else:
            print("✅ ConfigManager properly removed")
            
        # Test manager status
        if hasattr(managers, 'get_manager_status'):
            status = managers.get_manager_status()
            print(f"✅ Manager status: {status}")
        else:
            print("❌ get_manager_status not available")
            
        return True
    except Exception as e:
        print(f"❌ Managers init test failed: {e}")
        traceback.print_exc()
        return False

def test_unified_config_manager():
    """Test UnifiedConfigManager functionality"""
    print("\n🧪 Testing UnifiedConfigManager functionality...")
    try:
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager("/app/config")
        status = config_manager.get_status()
        
        print(f"✅ UnifiedConfigManager status: {status['status']}")
        print(f"✅ Config files: {status['config_files']}")  # This is already a count
        print(f"✅ Variables managed: {status['variables_managed']}")
        
        return True
    except Exception as e:
        print(f"❌ UnifiedConfigManager test failed: {e}")
        traceback.print_exc()
        return False

def check_remaining_config_manager_imports():
    """Check for remaining ConfigManager imports that need fixing"""
    print("\n🔍 Checking for remaining ConfigManager imports...")
    
    # List of files that might still have ConfigManager imports
    files_to_check = [
        "managers/__init__.py",
        "tests/phase/3/a/test_crisis_patterns.py",
        "tests/phase/3/d/test_step_6_integration.py",
        "tests/phase/3/d/test_step_7_integration.py",
        "__init__.py"
    ]
    
    remaining_imports = []
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if 'from managers.config_manager import' in content or 'import config_manager' in content:
                    remaining_imports.append(file_path)
                    print(f"⚠️ {file_path} still has ConfigManager imports")
                else:
                    print(f"✅ {file_path} clean (or file not found)")
        except FileNotFoundError:
            print(f"ℹ️ {file_path} not found (may not exist)")
        except Exception as e:
            print(f"❌ Error checking {file_path}: {e}")
    
    if remaining_imports:
        print(f"\n⚠️ Found {len(remaining_imports)} files with remaining ConfigManager imports:")
        for file_path in remaining_imports:
            print(f"   - {file_path}")
    else:
        print("\n✅ No ConfigManager imports found in checked files!")
    
    return len(remaining_imports) == 0

def main():
    """Run all Step 9.8 progress tests"""
    print("🚀 Step 9.8 Progress Test - ConfigManager Elimination Check")
    print("=" * 60)
    
    tests = [
        ("CrisisPatternManager Startup", test_crisis_pattern_manager),
        ("Managers Init Import", test_managers_init),
        ("UnifiedConfigManager Functionality", test_unified_config_manager),
        ("Remaining ConfigManager Imports", check_remaining_config_manager_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 STEP 9.8 PROGRESS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 STEP 9.8 PROGRESS: All tests passed!")
        print("✅ Ready to proceed with remaining ConfigManager eliminations")
    else:
        print(f"⚠️ STEP 9.8 PROGRESS: {total - passed} issues remain")
        print("🔧 Additional work needed to complete ConfigManager elimination")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)