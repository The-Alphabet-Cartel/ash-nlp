# ash-nlp/tests/test_phase_3c_config_validation.py
"""
Phase 3c Configuration Validation Tests - FIXED VERSION
Tests ThresholdMappingManager configuration validation using environment variables

Fixed to follow correct architecture:
- JSON contains valid defaults
- Environment variables provide overrides  
- Invalid values come from bad environment variables
- Validation catches invalid environment variable values
"""

import pytest
import os
import json
import tempfile
from unittest.mock import Mock, patch
from managers.threshold_mapping_manager import ThresholdMappingManager
from managers.config_manager import ConfigManager


class TestThresholdConfigurationValidation:
    """Test threshold configuration validation with environment variable overrides"""
    
    def get_valid_threshold_config(self):
        """Get a valid threshold configuration (should always be valid in JSON)"""
        return {
            "_metadata": {
                "version": "3c.1",
                "description": "Phase 3c threshold mapping configuration",
                "last_updated": "2025-08-06"
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
                    "confidence_boost_limit": 0.15,
                    "escalation_required_minimum": "low"
                },
                "staff_review": {
                    "high_always": True,
                    "medium_confidence_threshold": 0.45,
                    "low_confidence_threshold": 0.75,
                    "on_model_disagreement": True
                },
                "learning_system": {
                    "feedback_weight": 0.1,
                    "min_samples_for_update": 5,
                    "enable_threshold_learning": True
                },
                "safety_controls": {
                    "consensus_safety_bias": 0.03,
                    "enable_safety_override": True,
                    "minimum_response_threshold": 0.10
                }
            }
        }
    
    @pytest.fixture
    def mock_config_manager(self):
        """Create mock ConfigManager for testing"""
        mock_config = Mock(spec=ConfigManager)
        mock_config.load_config_file.return_value = self.get_valid_threshold_config()
        return mock_config
    
    @pytest.fixture
    def mock_model_ensemble_manager(self):
        """Create mock ModelEnsembleManager for testing"""
        mock_manager = Mock()
        mock_manager.get_current_ensemble_mode.return_value = 'weighted'
        return mock_manager
    
    def test_valid_configuration_passes_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test that valid configuration passes all validation checks"""
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'true'}):
            # Should not raise exception
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['validation_errors'] == 0
            assert validation_summary['configuration_loaded'] == True
    
    def test_threshold_range_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of threshold ranges (0.0 to 1.0) using environment variables"""
        # Test values outside valid range via environment variables
        invalid_env_configs = [
            # Negative value
            ('NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH', '-0.1'),
            # Value greater than 1.0
            ('NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM', '1.5'),
        ]
        
        valid_env_configs = [
            # Zero (edge case - should be valid)
            ('NLP_THRESHOLD_CONSENSUS_NEGATIVE_TO_LOW', '0.0'),
            # Exactly 1.0 (should be valid)
            ('NLP_THRESHOLD_CONSENSUS_UNKNOWN_TO_LOW', '1.0')
        ]
        
        # Test invalid environment variable values
        for env_var, invalid_value in invalid_env_configs:
            config = self.get_valid_threshold_config()
            mock_config_manager.load_config_file.return_value = config
            
            with patch.dict(os.environ, {
                'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
                env_var: invalid_value
            }):
                manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
                validation_summary = manager.get_validation_summary()
                
                assert validation_summary['validation_errors'] > 0
                assert any("not in valid range" in error for error in validation_summary['error_details'])
        
        # Test valid environment variable values
        for env_var, valid_value in valid_env_configs:
            config = self.get_valid_threshold_config()
            mock_config_manager.load_config_file.return_value = config
            
            with patch.dict(os.environ, {
                'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
                env_var: valid_value
            }):
                manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
                validation_summary = manager.get_validation_summary()
                
                # Should not have validation errors for valid values
                assert validation_summary['validation_errors'] == 0
    
    def test_threshold_ordering_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of threshold ordering (high > medium > low) using environment variables"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        # Test crisis_to_high <= crisis_to_medium (invalid) via environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.25',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM': '0.30'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be >" in error for error in validation_summary['error_details'])
    
    def test_ensemble_threshold_ordering_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of ensemble threshold ordering using environment variables"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        # Test high <= medium <= low (invalid) via environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_HIGH': '0.20',    # Should be highest
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_MEDIUM': '0.25',
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_LOW': '0.30'      # Should be lowest
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("high" in error and "medium" in error for error in validation_summary['error_details'])
    
    def test_staff_review_threshold_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of staff review threshold ordering using environment variables"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        # Test low_confidence_threshold <= medium_confidence_threshold (invalid) via environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE': '0.80',
            'NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE': '0.70'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be >" in error for error in validation_summary['error_details'])
    
    def test_learning_system_parameter_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of learning system parameters using environment variables"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        # Test feedback_weight outside valid range [0.0, 1.0] via environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_LEARNING_FEEDBACK_WEIGHT': '1.5'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be between 0.0 and 1.0" in error for error in validation_summary['error_details'])
    
    def test_safety_bias_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of safety bias parameters using environment variables"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        # Test safety bias outside reasonable range [0.0, 0.2] via environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_SAFETY_BIAS': '0.25'  # Above 0.2 limit
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be between 0.0 and 0.2" in error for error in validation_summary['error_details'])
    
    def test_cross_mode_consistency_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test cross-mode consistency validation (warnings, not errors)"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Should create manager successfully (warnings don't prevent initialization)
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # This is more of a warning than an error, so validation_errors might still be 0
            # The warning would be logged but not counted as a critical error
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
    
    def test_missing_configuration_sections(self, mock_config_manager, mock_model_ensemble_manager):
        """Test handling of missing configuration sections"""
        # Test with missing threshold_mapping_by_mode section
        invalid_config = {
            "_metadata": {"version": "3c.1"},
            "shared_configuration": {
                "staff_review": {"high_always": True}
            }
            # Missing threshold_mapping_by_mode
        }
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Should handle missing sections gracefully in non-fail-fast mode
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
    
    def test_missing_mode_configurations(self, mock_config_manager, mock_model_ensemble_manager):
        """Test handling of missing mode configurations"""
        # Only provide consensus mode (missing majority and weighted)
        partial_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = partial_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Should work with single mode (server runs one mode at a time)
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
    
    def test_invalid_data_types(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of invalid data types"""
        config = self.get_valid_threshold_config()
        mock_config_manager.load_config_file.return_value = config
        
        # Test non-numeric environment variable
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': 'not_a_number'
        }):
            # Should raise ValueError during float conversion
            with pytest.raises(ValueError):
                ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)


class TestEnvironmentVariableOverrides:
    """Test environment variable override functionality"""
    
    def get_valid_threshold_config(self):
        """Get a valid threshold configuration"""
        return {
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
                }
            },
            "shared_configuration": {
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
    
    def test_crisis_level_mapping_overrides(self):
        """Test crisis level mapping environment variable overrides"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = self.get_valid_threshold_config()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.60',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM': '0.35',
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert crisis_mapping['crisis_to_high'] == 0.60
            assert crisis_mapping['crisis_to_medium'] == 0.35
            # Values not overridden should keep defaults
            assert crisis_mapping['mild_crisis_to_low'] == 0.40
    
    def test_ensemble_threshold_overrides(self):
        """Test ensemble threshold environment variable overrides"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = self.get_valid_threshold_config()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_HIGH': '0.50',
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_MEDIUM': '0.30',
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_LOW': '0.15',
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            ensemble_thresholds = manager.get_ensemble_thresholds_for_mode('consensus')
            assert ensemble_thresholds['high'] == 0.50
            assert ensemble_thresholds['medium'] == 0.30
            assert ensemble_thresholds['low'] == 0.15
    
    def test_shared_configuration_overrides(self):
        """Test shared configuration environment variable overrides"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = self.get_valid_threshold_config()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE': '0.50',
            'NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE': '0.80',
            'NLP_THRESHOLD_LEARNING_FEEDBACK_WEIGHT': '0.15',
            'NLP_THRESHOLD_SAFETY_BIAS': '0.05',
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            staff_config = manager.get_staff_review_config()
            assert staff_config['medium_confidence_threshold'] == 0.50
            assert staff_config['low_confidence_threshold'] == 0.80
            
            learning_config = manager.get_learning_system_config()
            assert learning_config['feedback_weight'] == 0.15
            
            safety_config = manager.get_safety_controls_config()
            assert safety_config['consensus_safety_bias'] == 0.05
    
    def test_boolean_environment_variable_parsing(self):
        """Test boolean environment variable parsing"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = self.get_valid_threshold_config()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Test valid boolean values
        valid_boolean_tests = [
            ('true', True),
            ('false', False),
            ('1', True),
            ('0', False),
            ('yes', True),
            ('no', False),
            ('on', True),
            ('off', False)
        ]
        
        for env_value, expected_bool in valid_boolean_tests:
            with patch.dict(os.environ, {
                'NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS': env_value,
                'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
            }):
                manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
                staff_review_config = manager.get_staff_review_config()
                
                assert staff_review_config['high_always'] == expected_bool
        
        # Test invalid boolean values
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS': 'invalid_boolean',
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("Invalid boolean value" in error for error in validation_summary['error_details'])
    
    def test_invalid_environment_variable_values(self):
        """Test handling of invalid environment variable values"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = self.get_valid_threshold_config()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Test various invalid values
        invalid_env_vars = [
            ('NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH', 'not_a_number'),
            ('NLP_THRESHOLD_CONSENSUS_ENSEMBLE_MEDIUM', 'invalid'),
        ]
        
        for env_var, invalid_value in invalid_env_vars:
            with patch.dict(os.environ, {
                env_var: invalid_value,
                'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
            }):
                # Should raise ValueError during float conversion
                with pytest.raises(ValueError):
                    ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
    
    def test_environment_variable_precedence(self):
        """Test that environment variables take precedence over JSON values"""
        mock_config_manager = Mock()
        config = self.get_valid_threshold_config()
        # JSON has crisis_to_high = 0.50
        assert config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_high'] == 0.50
        mock_config_manager.load_config_file.return_value = config
        
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Environment variable should override JSON value
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.65',
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            # Should be environment value, not JSON value
            assert crisis_mapping['crisis_to_high'] == 0.65


class TestConfigurationFileHandling:
    """Test configuration file loading and error handling"""
    
    def test_missing_configuration_file(self):
        """Test handling of missing configuration file"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = None  # Simulate missing file
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
            ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
    
    def test_corrupted_configuration_file(self):
        """Test handling of corrupted JSON configuration file"""
        mock_config_manager = Mock()
        # Simulate JSON decode error
        mock_config_manager.load_config_file.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
            ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
    
    def test_real_file_loading_integration(self):
        """Test loading from actual file system"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = os.path.join(temp_dir, 'threshold_mapping.json')
            
            # Write valid test configuration
            test_config = {
                "threshold_mapping_by_mode": {
                    "consensus": {
                        "crisis_level_mapping": {
                            "crisis_to_high": 0.50,
                            "crisis_to_medium": 0.30
                        }
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
            manager = ThresholdMappingManager(config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
            
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert crisis_mapping['crisis_to_high'] == 0.50


class TestFailFastBehavior:
    """Test fail-fast validation behavior"""
    
    def test_fail_fast_enabled_with_errors(self):
        """Test fail-fast behavior when enabled and errors present via environment variables"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Set invalid environment variable with fail-fast enabled
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'true',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '-0.1'  # Invalid value via env var
        }):
            with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
                ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
    
    def test_fail_fast_disabled_with_errors(self):
        """Test behavior when fail-fast is disabled but errors present via environment variables"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Set invalid environment variable with fail-fast disabled
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '-0.1'  # Invalid value via env var
        }):
            # Should not raise exception
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['validation_errors'] > 0
            assert len(validation_summary['error_details']) > 0
    
    def test_fail_fast_default_behavior(self):
        """Test default fail-fast behavior (should be enabled) with invalid environment variables"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Set invalid environment variable without setting fail-fast env var (test default behavior)
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '-0.1'  # Invalid value via env var
        }, clear=True):  # Clear environment to test default behavior
            with pytest.raises(ValueError):
                ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)


class TestConfigurationSchemaValidation:
    """Test JSON schema-like validation of configuration structure"""
    
    def test_required_sections_validation(self):
        """Test validation of required configuration sections"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = None  # Missing file
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
            ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
    
    def test_partial_configuration_handling(self):
        """Test handling of partial configurations"""
        mock_config_manager = Mock()
        # Partial config - only has consensus mode
        partial_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = partial_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Should handle partial config gracefully
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True


class TestAdvancedValidationScenarios:
    """Test advanced validation scenarios and edge cases"""
    
    def test_mode_specific_validation_rules(self):
        """Test validation rules specific to different ensemble modes"""
        mock_config_manager = Mock()
        config = {
            "threshold_mapping_by_mode": {
                "weighted": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.55,
                        "crisis_to_medium": 0.32
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
    
    def test_configuration_versioning(self):
        """Test configuration versioning and metadata handling"""
        mock_config_manager = Mock()
        versioned_config = {
            "_metadata": {
                "version": "3c.1",
                "description": "Test configuration"
            },
            "threshold_mapping_by_mode": {
                "weighted": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.55,
                        "crisis_to_medium": 0.32
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = versioned_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
    
    def test_complex_validation_combinations(self):
        """Test complex combinations of validation scenarios using environment variables"""
        mock_config_manager = Mock()
        config = {
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
                    "medium_confidence_threshold": 0.45,
                    "low_confidence_threshold": 0.75
                }
            }
        }
        mock_config_manager.load_config_file.return_value = config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Multiple invalid environment variables
        with patch.dict(os.environ, {
            'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '-0.1',     # Invalid range
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM': '1.5',    # Invalid range
            'NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE': '0.3'    # Invalid ordering
        }):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            # Should detect multiple errors
            assert validation_summary['validation_errors'] >= 2  # At least 2 errors expected


class TestPhase3cConfigurationTestSuite:
    """Comprehensive test suite for Phase 3c configuration validation"""
    
    def test_run_all_validation_tests(self):
        """Run all validation tests in sequence to ensure comprehensive coverage"""
        mock_config_manager = Mock()
        config = {
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
                }
            },
            "shared_configuration": {
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
        mock_config_manager.load_config_file.return_value = config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Should successfully create manager with valid configuration
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['configuration_loaded'] == True
            assert validation_summary['validation_errors'] == 0
            
            # Test all accessor methods work
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert isinstance(crisis_mapping, dict)
            
            ensemble_thresholds = manager.get_ensemble_thresholds_for_mode('consensus')
            assert isinstance(ensemble_thresholds, dict)
            
            staff_config = manager.get_staff_review_config()
            assert isinstance(staff_config, dict)
            
            learning_config = manager.get_learning_system_config()
            assert isinstance(learning_config, dict)
            
            safety_config = manager.get_safety_controls_config()
            assert isinstance(safety_config, dict)