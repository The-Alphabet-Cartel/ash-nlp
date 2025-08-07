# Create a simple test file to verify validation is working
# Save this as test_simple_validation.py in your tests/ directory

#!/usr/bin/env python3
"""
Simple validation test to verify threshold validation is working
"""

import os
import sys
import logging
from unittest.mock import Mock

# Add the app directory to the path
sys.path.insert(0, '/app')

from managers.threshold_mapping_manager import ThresholdMappingManager

# Set up logging to see what's happening
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def test_simple_validation():
    """Test validation with obviously invalid values"""
    print("🧪 Testing simple validation...")
    
    # Create mock config manager
    mock_config = Mock()
    
    # Create config with obviously invalid values
    invalid_config = {
        'threshold_mapping_by_mode': {
            'consensus': {
                'crisis_level_mapping': {
                    'crisis_to_high': -0.1,  # Invalid: negative
                    'crisis_to_medium': 1.5,  # Invalid: > 1.0
                    'mild_crisis_to_low': 0.4  # Valid
                }
            }
        }
    }
    
    mock_config.load_config_file.return_value = invalid_config
    
    # Create mock ensemble manager
    mock_ensemble = Mock()
    mock_ensemble.get_current_ensemble_mode.return_value = 'consensus'
    
    # Set fail_fast to false so we can see the errors
    os.environ['NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID'] = 'false'
    
    try:
        print("🔍 Creating ThresholdMappingManager...")
        manager = ThresholdMappingManager(mock_config, mock_ensemble)
        
        print("🔍 Getting validation summary...")
        summary = manager.get_validation_summary()
        
        print(f"📊 Validation results:")
        print(f"   - Configuration loaded: {summary.get('configuration_loaded')}")
        print(f"   - Validation errors: {summary.get('validation_errors')}")
        print(f"   - Error details: {summary.get('error_details')}")
        print(f"   - Fail fast enabled: {summary.get('fail_fast_enabled')}")
        
        # Check if validation is working
        if summary.get('validation_errors', 0) > 0:
            print("✅ Validation IS working - errors detected!")
            for error in summary.get('error_details', []):
                print(f"   ❌ {error}")
        else:
            print("❌ Validation NOT working - no errors detected for invalid values!")
            
            # Check if the validation methods exist
            print("🔍 Checking validation methods...")
            print(f"   - _validate_configuration method exists: {hasattr(manager, '_validate_configuration')}")
            print(f"   - _validate_mode_thresholds method exists: {hasattr(manager, '_validate_mode_thresholds')}")
            print(f"   - _processed_config exists: {manager._processed_config is not None}")
            
            if manager._processed_config:
                print(f"   - Processed config keys: {list(manager._processed_config.keys())}")
                if 'threshold_mapping_by_mode' in manager._processed_config:
                    modes = manager._processed_config['threshold_mapping_by_mode']
                    print(f"   - Available modes: {list(modes.keys())}")
                    if 'consensus' in modes:
                        consensus_config = modes['consensus']
                        print(f"   - Consensus config keys: {list(consensus_config.keys())}")
                        if 'crisis_level_mapping' in consensus_config:
                            crisis_mapping = consensus_config['crisis_level_mapping']
                            print(f"   - Crisis mapping: {crisis_mapping}")
        
        return summary.get('validation_errors', 0) > 0
        
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_validation()
    print(f"\n🎯 Test result: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1)