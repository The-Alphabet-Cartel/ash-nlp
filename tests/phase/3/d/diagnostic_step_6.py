#!/usr/bin/env python3
# tests/phase/3/d/diagnostic_step_6.py
"""
Diagnostic test to identify the exact issue with boolean returns
"""

import sys
import os

# Add /app to path
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

def main():
    print("🔬 Diagnostic Test for Step 6 Boolean Issues")
    print("=" * 60)
    
    try:
        from managers.config_manager import create_config_manager
        from managers.logging_config_manager import create_logging_config_manager
        
        # Create managers
        config_manager = create_config_manager('/app/config')
        logging_manager = create_logging_config_manager(config_manager)
        
        print("✅ Managers created successfully")
        
        # Test each method individually and show what it returns
        print("\n🔍 Testing individual methods:")
        
        # Test 1: get_global_logging_settings
        print("\n1. get_global_logging_settings():")
        global_settings = logging_manager.get_global_logging_settings()
        print(f"   Type: {type(global_settings)}")
        print(f"   Content: {global_settings}")
        
        # Test 2: get_detailed_logging_settings  
        print("\n2. get_detailed_logging_settings():")
        detailed_settings = logging_manager.get_detailed_logging_settings()
        print(f"   Type: {type(detailed_settings)}")
        print(f"   Content: {detailed_settings}")
        
        # Check each value in detailed_settings
        for key, value in detailed_settings.items():
            print(f"   {key}: {value} (type: {type(value)})")
        
        # Test 3: get_component_logging_settings
        print("\n3. get_component_logging_settings():")
        component_settings = logging_manager.get_component_logging_settings()
        print(f"   Type: {type(component_settings)}")
        
        # Check a few component values
        for key in ['threshold_changes', 'model_disagreements', 'staff_review_triggers']:
            if key in component_settings:
                value = component_settings[key]
                print(f"   {key}: {value} (type: {type(value)})")
        
        # Test 4: Convenience methods
        print("\n4. Convenience methods:")
        
        # Test get_log_level
        log_level = logging_manager.get_log_level()
        print(f"   get_log_level(): {log_level} (type: {type(log_level)})")
        
        # Test should_log_detailed - this is the one failing
        print("\n   Testing should_log_detailed() step by step:")
        try:
            detailed = logging_manager.get_detailed_logging_settings()
            print(f"   - detailed_settings: {detailed}")
            
            enable_detailed = detailed.get('enable_detailed', True)
            print(f"   - enable_detailed raw: {enable_detailed} (type: {type(enable_detailed)})")
            
            # Now call the actual method
            should_log = logging_manager.should_log_detailed()
            print(f"   - should_log_detailed(): {should_log} (type: {type(should_log)})")
            
            # Check if it's a boolean
            is_bool = isinstance(should_log, bool)
            print(f"   - isinstance(should_log, bool): {is_bool}")
            
            if not is_bool:
                print(f"   ❌ This is the problem! should_log_detailed() returned {type(should_log)}, not bool")
                print(f"   Raw value: {repr(should_log)}")
            else:
                print(f"   ✅ should_log_detailed() correctly returns a boolean")
            
        except Exception as e:
            print(f"   ❌ Error in should_log_detailed(): {e}")
            import traceback
            traceback.print_exc()
        
        # Test should_include_reasoning
        print("\n   Testing should_include_reasoning():")
        should_include = logging_manager.should_include_reasoning()
        print(f"   should_include_reasoning(): {should_include} (type: {type(should_include)})")
        print(f"   isinstance(should_include, bool): {isinstance(should_include, bool)}")
        
        # Test get_log_file_path
        print("\n   Testing get_log_file_path():")
        log_path = logging_manager.get_log_file_path()
        print(f"   get_log_file_path(): {log_path} (type: {type(log_path)})")
        print(f"   isinstance(log_path, str): {isinstance(log_path, str)}")
        
        # Test should_log_component
        print("\n   Testing should_log_component():")
        threshold_check = logging_manager.should_log_component('threshold_changes')
        print(f"   should_log_component('threshold_changes'): {threshold_check} (type: {type(threshold_check)})")
        print(f"   isinstance(threshold_check, bool): {isinstance(threshold_check, bool)}")
        
        # Final summary
        print("\n📊 Summary:")
        all_methods = [
            ('get_log_level', log_level, str),
            ('should_log_detailed', should_log, bool),
            ('should_include_reasoning', should_include, bool), 
            ('get_log_file_path', log_path, str),
            ('should_log_component', threshold_check, bool)
        ]
        
        all_good = True
        for method_name, value, expected_type in all_methods:
            is_correct = isinstance(value, expected_type)
            status = "✅" if is_correct else "❌"
            print(f"   {status} {method_name}: {type(value)} (expected {expected_type})")
            if not is_correct:
                all_good = False
        
        if all_good:
            print("\n🎉 All methods return correct types!")
        else:
            print("\n❌ Some methods return incorrect types - need fixes")
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🏁 Diagnostic complete: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(0 if success else 1)