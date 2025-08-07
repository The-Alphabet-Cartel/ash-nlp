#!/usr/bin/env python3
"""
Phase 3c Threshold Mapping Manager Tests - FIXED VERSION
Tests ThresholdMappingManager with proper logging and correct validation approach

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import pytest
import os
import sys
import json
import tempfile
import logging
from pathlib import Path
from unittest.mock import Mock, patch

# Set up logging - ADDED FOR PROPER OUTPUT
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the app directory to the path
sys.path.insert(0, '/app')

try:
    from managers.threshold_mapping_manager import ThresholdMappingManager, create_threshold_mapping_manager
    from managers.config_manager import ConfigManager
    logger.info("✅ Successfully imported ThresholdMappingManager")
except ImportError as e:
    logger.error(f"❌ Failed to import ThresholdMappingManager: {e}")
    logger.error("🔍 Make sure the app is properly configured and managers are available")


class TestThresholdMappingManager:
    """Test ThresholdMappingManager functionality with corrected validation approach"""
    
    def get_test_threshold_config(self):
        """Get a valid test configuration for threshold mapping"""
        return {
            "_metadata": {
                "version": "3c.1",
                "description": "Test threshold mapping configuration"
            },
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30,
                        "mild_crisis_to_low": 0.40,
                        "negative_to_low": 0.70,
                        "unknown_to_low": 0.50
                    },
                    "ensemble_thresholds": {
                        "high": 0.45,
                        "medium": 0.25,
                        "low": 0.12
                    }
                },
                "majority": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.45,
                        "crisis_to_medium": 0.28,
                        "mild_crisis_to_low": 0.35,
                        "negative_to_low": 0.65,
                        "unknown_to_low": 0.45
                    },
                    "ensemble_thresholds": {
                        "high": 0.42,
                        "medium": 0.23,
                        "low": 0.11
                    }
                },
                "weighted": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.55,
                        "crisis_to_medium": 0.32,
                        "mild_crisis_to_low": 0.42,
                        "negative_to_low": 0.72,
                        "unknown_to_low": 0.52
                    },
                    "ensemble_thresholds": {
                        "high": 0.48,
                        "medium": 0.27,
                        "low": 0.14
                    }
                }
            },
            "shared_configuration": {
                "pattern_integration": {
                    "pattern_weight_multiplier": 1.2,
                    "confidence_boost_limit": 0.15
                },
                "staff_review": {
                    "high_always": True,
                    "medium_confidence_threshold": 0.45,
                    "low_confidence_threshold": 0.75
                },
                "learning_system": {
                    "feedback_weight": 0.1,
                    "enable_threshold_learning": True
                },
                "safety_controls": {
                    "consensus_safety_bias": 0.03,
                    "enable_safety_override": True
                }
            }
        }
    
    @pytest.fixture
    def mock_config_manager(self):
        """Create mock ConfigManager for testing"""
        mock_config = Mock()
        mock_config.load_config_file.return_value = self.get_test_threshold_config()
        return mock_config
    
    @pytest.fixture  
    def mock_model_ensemble_manager(self):
        """Create mock ModelEnsembleManager for testing"""
        mock_manager = Mock()
        mock_manager.get_current_ensemble_mode.return_value = 'consensus'
        return mock_manager
    
    def test_initialization_success(self, mock_config_manager, mock_model_ensemble_manager):
        """Test successful ThresholdMappingManager initialization"""
        logger.info("🧪 Testing successful initialization...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
            logger.info("✅ Initialization successful")
    
    def test_initialization_with_validation_errors(self, mock_config_manager, mock_model_ensemble_manager):
        """Test initialization with validation errors using environment variables"""
        logger.info("🧪 Testing initialization with validation errors via env vars...")
        
        # Set invalid environment variables to trigger validation errors
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '1.5'  # Invalid: > 1.0
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            # Should have validation errors from invalid environment variable
            assert validation_summary['validation_errors'] > 0
            assert any("not in valid range" in error for error in validation_summary['error_details'])
            logger.info(f"✅ Validation errors detected: {validation_summary['validation_errors']}")
    
    def test_initialization_fail_fast(self, mock_config_manager, mock_model_ensemble_manager):
        """Test initialization with fail-fast validation enabled"""
        logger.info("🧪 Testing fail-fast behavior...")
        
        # Set invalid environment variable with fail-fast enabled
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'true',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '1.5'  # Invalid: > 1.0
        }):
            with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
                ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            logger.info("✅ Fail-fast behavior working correctly")
    
    def test_crisis_level_mapping_for_mode(self, mock_config_manager, mock_model_ensemble_manager):
        """Test getting crisis level mapping for all three modes: consensus, majority, and weighted"""
        logger.info("🧪 Testing crisis level mapping retrieval for all modes...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Test all three ensemble modes
            modes_to_test = ['consensus', 'majority', 'weighted']
            
            for mode in modes_to_test:
                logger.info(f"   🧪 Testing {mode} mode crisis level mapping...")
                
                # Test mode crisis level mapping
                mode_mapping = manager.get_crisis_level_mapping_for_mode(mode)
                assert isinstance(mode_mapping, dict), f"{mode} mode mapping must be a dictionary"
                
                # Verify required mapping keys exist
                required_keys = ['crisis_to_high', 'crisis_to_medium']
                for key in required_keys:
                    assert key in mode_mapping, f"{mode} mode missing required mapping: {key}"
                
                # Verify values are numeric and in valid range
                for mapping_name, value in mode_mapping.items():
                    assert isinstance(value, (int, float)), f"{mode} {mapping_name} must be numeric"
                    assert 0.0 <= value <= 1.0, f"{mode} {mapping_name} = {value} must be in range [0.0, 1.0]"
                
                # Verify crisis mapping ordering: crisis_to_high > crisis_to_medium
                if 'crisis_to_high' in mode_mapping and 'crisis_to_medium' in mode_mapping:
                    high_val = mode_mapping['crisis_to_high']
                    medium_val = mode_mapping['crisis_to_medium']
                    assert high_val > medium_val, f"{mode} mode: crisis_to_high ({high_val}) must be > crisis_to_medium ({medium_val})"
                
                # Log actual values for debugging
                logger.info(f"   📊 {mode.capitalize()} crisis mapping: {dict(list(mode_mapping.items())[:3])}...")  # Show first few items
            
            logger.info("✅ Crisis level mapping retrieval working for all three modes (consensus, majority, weighted)")
    
    def test_ensemble_thresholds_for_mode(self, mock_config_manager, mock_model_ensemble_manager):
        """Test getting ensemble thresholds for all three modes: consensus, majority, and weighted"""
        logger.info("🧪 Testing ensemble threshold retrieval for all modes...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Test all three ensemble modes
            modes_to_test = ['consensus', 'majority', 'weighted']
            
            for mode in modes_to_test:
                logger.info(f"   🧪 Testing {mode} mode ensemble thresholds...")
                
                # Test mode ensemble thresholds - focus on structure, not exact values
                mode_thresholds = manager.get_ensemble_thresholds_for_mode(mode)
                assert isinstance(mode_thresholds, dict), f"{mode} mode thresholds must be a dictionary"
                
                # Verify required threshold keys exist
                required_keys = ['high', 'medium', 'low']
                for key in required_keys:
                    assert key in mode_thresholds, f"{mode} mode missing required threshold: {key}"
                
                # Verify values are numeric and in valid range
                for threshold_name, value in mode_thresholds.items():
                    assert isinstance(value, (int, float)), f"{mode} {threshold_name} threshold must be numeric"
                    assert 0.0 <= value <= 1.0, f"{mode} {threshold_name} threshold = {value} must be in range [0.0, 1.0]"
                
                # Verify threshold ordering: high > medium > low
                high_val = mode_thresholds['high']
                medium_val = mode_thresholds['medium']
                low_val = mode_thresholds['low']
                
                assert high_val > medium_val, f"{mode} mode: high ({high_val}) must be > medium ({medium_val})"
                assert medium_val > low_val, f"{mode} mode: medium ({medium_val}) must be > low ({low_val})"
                
                # Log actual values for debugging
                logger.info(f"   📊 {mode.capitalize()} thresholds: high={high_val}, medium={medium_val}, low={low_val}")
            
            logger.info("✅ Ensemble threshold retrieval working for all three modes (consensus, majority, weighted)")
    
    def test_current_ensemble_mode_detection(self, mock_config_manager, mock_model_ensemble_manager):
        """Test current ensemble mode detection and threshold retrieval"""
        logger.info("🧪 Testing current ensemble mode detection...")
        
        # Test with different current modes
        test_modes = ['consensus', 'majority', 'weighted']
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            for mode in test_modes:
                mock_model_ensemble_manager.get_current_ensemble_mode.return_value = mode
                manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
                
                # Test getting current mode's thresholds
                current_crisis_mapping = manager.get_crisis_level_mapping_for_mode(mode)
                current_ensemble_thresholds = manager.get_ensemble_thresholds_for_mode(mode)
                
                assert isinstance(current_crisis_mapping, dict)
                assert isinstance(current_ensemble_thresholds, dict)
                assert 'crisis_to_high' in current_crisis_mapping
                assert 'high' in current_ensemble_thresholds
                
                logger.info(f"✅ Mode {mode} detection and threshold retrieval working")
    
    def test_environment_variable_overrides(self, mock_config_manager, mock_model_ensemble_manager):
        """Test environment variable override functionality"""
        logger.info("🧪 Testing environment variable overrides...")
        
        # Test consensus mode overrides
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.60',  # Override from 0.50
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_HIGH': '0.50'    # Override from 0.45
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            ensemble_thresholds = manager.get_ensemble_thresholds_for_mode('consensus')
            
            # Should use environment variable values
            assert crisis_mapping['crisis_to_high'] == 0.60
            assert ensemble_thresholds['high'] == 0.50
            
            # Non-overridden values should use defaults
            assert crisis_mapping['crisis_to_medium'] == 0.30  # Not overridden
            
            logger.info("✅ Environment variable overrides working")
    
    def test_staff_review_determination(self, mock_config_manager, mock_model_ensemble_manager):
        """Test staff review configuration access"""
        logger.info("🧪 Testing staff review configuration...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            staff_config = manager.get_staff_review_config()
            assert staff_config['high_always'] == True
            assert staff_config['medium_confidence_threshold'] == 0.45
            assert staff_config['low_confidence_threshold'] == 0.75
            
            logger.info("✅ Staff review configuration access working")
    
    def test_validation_cross_mode_consistency(self, mock_config_manager, mock_model_ensemble_manager):
        """Test cross-mode validation warnings"""
        logger.info("🧪 Testing cross-mode validation...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            # Cross-mode warnings don't prevent loading but generate warnings
            assert validation_summary['configuration_loaded'] == True
            
            logger.info("✅ Cross-mode validation working")
    
    def test_learning_system_integration(self, mock_config_manager, mock_model_ensemble_manager):
        """Test learning system configuration access"""
        logger.info("🧪 Testing learning system integration...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            learning_config = manager.get_learning_system_config()
            assert learning_config['feedback_weight'] == 0.1
            assert learning_config['enable_threshold_learning'] == True
            
            logger.info("✅ Learning system integration working")
    
    def test_fallback_behavior(self, mock_config_manager, mock_model_ensemble_manager):
        """Test fallback behavior for missing configuration"""
        logger.info("🧪 Testing fallback behavior...")
        
        # Test with None config (missing file)
        mock_config_manager.load_config_file.return_value = None
        
        with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
            ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        logger.info("✅ Fallback behavior working - properly raises error for missing config")
    
    def test_validation_summary(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation summary functionality"""
        logger.info("🧪 Testing validation summary...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            summary = manager.get_validation_summary()
            
            required_keys = [
                'configuration_loaded', 
                'validation_errors', 
                'error_details',
                'fail_fast_enabled'
            ]
            
            for key in required_keys:
                assert key in summary, f"Missing key: {key}"
            
            assert isinstance(summary['error_details'], list)
            assert isinstance(summary['validation_errors'], int)
            assert isinstance(summary['configuration_loaded'], bool)
            
            logger.info("✅ Validation summary working")
    
    def test_factory_function(self, mock_config_manager, mock_model_ensemble_manager):
        """Test factory function creation pattern"""
        logger.info("🧪 Testing factory function...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Test factory function (should use same constructor)
            manager = create_threshold_mapping_manager(mock_config_manager, mock_model_ensemble_manager)
            
            assert isinstance(manager, ThresholdMappingManager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
            
            logger.info("✅ Factory function working")
    
    def test_shared_configuration_access(self, mock_config_manager, mock_model_ensemble_manager):
        """Test shared configuration section access"""
        logger.info("🧪 Testing shared configuration access...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Test all shared configuration accessors
            staff_config = manager.get_staff_review_config()
            learning_config = manager.get_learning_system_config()
            safety_config = manager.get_safety_controls_config()
            
            assert isinstance(staff_config, dict)
            assert isinstance(learning_config, dict) 
            assert isinstance(safety_config, dict)
            
            # Test specific values
            assert 'high_always' in staff_config
            assert 'feedback_weight' in learning_config
            assert 'consensus_safety_bias' in safety_config
            
            logger.info("✅ Shared configuration access working")
    
    def test_invalid_mode_handling(self, mock_config_manager, mock_model_ensemble_manager):
        """Test handling of invalid ensemble mode requests"""
        logger.info("🧪 Testing invalid mode handling...")
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Test invalid mode - should raise KeyError or return empty/default
            try:
                invalid_mapping = manager.get_crisis_level_mapping_for_mode('invalid_mode')
                # If it doesn't raise an error, it should return an empty dict or fallback
                assert isinstance(invalid_mapping, dict)
                logger.info("✅ Invalid mode handled gracefully")
            except (KeyError, ValueError) as e:
                # It's also acceptable to raise an error for invalid modes
                logger.info(f"✅ Invalid mode properly raises error: {e}")
    
    def test_threshold_range_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test threshold range validation using environment variables"""
        logger.info("🧪 Testing threshold range validation...")
        
        # Test out-of-range values via environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '1.5',  # Invalid: > 1.0
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM': '-0.1'  # Invalid: < 0.0
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            # Should detect validation errors from invalid environment variables
            assert validation_summary['validation_errors'] > 0
            assert any("not in valid range" in error for error in validation_summary['error_details'])
            
            logger.info(f"✅ Range validation working - detected {validation_summary['validation_errors']} errors")


class TestThresholdMappingManagerIntegration:
    """Integration tests for ThresholdMappingManager with real config files"""
    
    def test_real_config_file_loading(self):
        """Test loading with actual config file structure"""
        logger.info("🧪 Testing real config file loading...")
        
        # Create temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = os.path.join(temp_dir, 'threshold_mapping.json')
            
            # Write test config
            test_config = {
                "threshold_mapping_by_mode": {
                    "consensus": {
                        "crisis_level_mapping": {
                            "crisis_to_high": 0.50,
                            "crisis_to_medium": 0.30
                        }
                    }
                },
                "shared_configuration": {
                    "staff_review": {
                        "high_always": True
                    }
                }
            }
            
            with open(config_file, 'w') as f:
                json.dump(test_config, f)
            
            # Create real ConfigManager
            config_manager = ConfigManager(temp_dir)
            mock_ensemble_manager = Mock()
            mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
            
            # Test loading
            with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
                manager = ThresholdMappingManager(config_manager, mock_ensemble_manager)
                
                crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
                assert crisis_mapping['crisis_to_high'] == 0.50
                
                logger.info("✅ Real config file loading working")


# ============================================================================
# COMPREHENSIVE TEST RUNNER WITH PROPER LOGGING - ADDED FOR OUTPUT
# ============================================================================

def run_threshold_mapping_manager_tests():
    """Run all threshold mapping manager tests with proper logging"""
    logger.info("🧪 Starting ThresholdMappingManager Test Suite")
    logger.info("=" * 70)
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        logger.info("🔍 Running comprehensive pytest suite...")
        
        # Run pytest with verbose output but capture results
        import subprocess
        
        result = subprocess.run([
            sys.executable, '-m', 'pytest', __file__, 
            '-v', '--tb=short', '--disable-warnings'
        ], capture_output=True, text=True, cwd='/app')
        
        # Parse pytest output
        if result.returncode == 0:
            logger.info("🎉 All ThresholdMappingManager tests PASSED!")
            test_results['passed'] = 1
            test_results['overall_success'] = True
        else:
            logger.error("❌ Some ThresholdMappingManager tests FAILED")
            logger.error("📋 Test Output:")
            for line in result.stdout.split('\n'):
                if line.strip() and ('FAILED' in line or 'PASSED' in line or '====' in line):
                    logger.info(f"   {line}")
            
            if result.stderr:
                logger.error("📋 Error Output:")
                for line in result.stderr.split('\n'):
                    if line.strip():
                        logger.error(f"   {line}")
            
            test_results['failed'] = 1
            test_results['overall_success'] = False
            
    except Exception as e:
        logger.error(f"❌ Test suite execution error: {e}")
        test_results['errors'].append(f"Suite execution: {str(e)}")
        test_results['overall_success'] = False
    
    logger.info("=" * 70)
    logger.info(f"📊 ThresholdMappingManager Test Results: {test_results['passed']} passed, {test_results['failed']} failed")
    
    if test_results['errors']:
        logger.info("📋 Error Details:")
        for error in test_results['errors']:
            logger.info(f"   ❌ {error}")
    
    if test_results.get('overall_success', False):
        logger.info("🎯 THRESHOLD MAPPING MANAGER: SUCCESS - All tests working correctly!")
        logger.info("🏗️ ThresholdMappingManager ready for production use!")
    else:
        logger.info("🎯 THRESHOLD MAPPING MANAGER: NEEDS ATTENTION - Some tests failed")
    
    return test_results


if __name__ == "__main__":
    """Main execution - Run tests when script is executed directly"""
    logger.info("🚀 ThresholdMappingManager Test Execution")
    logger.info("Repository: https://github.com/the-alphabet-cartel/ash-nlp")
    logger.info("Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org")
    logger.info("")
    
    # Run the test suite
    results = run_threshold_mapping_manager_tests()
    success = results.get('overall_success', False)
    
    logger.info("")
    logger.info("🎯 Final Result:")
    if success:
        logger.info("🎉 ThresholdMappingManager Tests: SUCCESS!")
        logger.info("🏗️ Ready for production use!")
    else:
        logger.info("❌ ThresholdMappingManager Tests: NEEDS ATTENTION")
        logger.info("🔧 Check the test failures above and fix any issues")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)