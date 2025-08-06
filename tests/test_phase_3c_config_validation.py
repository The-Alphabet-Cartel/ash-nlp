# ash-nlp/tests/test_phase_3c_config_validation.py
"""
Phase 3c: Configuration Validation Tests
Tests JSON schema validation, environment variable precedence, and configuration consistency

Clean v3.1 Architecture Configuration Test Suite
"""

import os
import pytest
import json
import tempfile
from unittest.mock import Mock, patch
from typing import Dict, Any

# Import the components we're testing
from managers.threshold_mapping_manager import ThresholdMappingManager
from managers.config_manager import ConfigManager


class TestThresholdConfigurationValidation:
    """Test configuration validation logic and error handling"""
    
    def get_valid_threshold_config(self) -> Dict[str, Any]:
        """Get a valid threshold configuration for testing"""
        return {
            "_metadata": {
                "configuration_version": "3c.1",
                "description": "Test threshold configuration"
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
                        "low": 0.13
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
            },
            "validation_rules": {
                "threshold_consistency": {
                    "crisis_to_high_minimum": 0.3,
                    "crisis_to_high_maximum": 0.8,
                    "high_greater_than_medium": True
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
        """Test validation of threshold ranges (0.0 to 1.0)"""
        # Test values outside valid range
        invalid_configs = [
            # Negative value
            ('crisis_to_high', -0.1),
            # Value greater than 1.0
            ('crisis_to_medium', 1.5),
            # Zero (edge case)
            ('mild_crisis_to_low', 0.0),
            # Exactly 1.0 (should be valid)
            ('negative_to_low', 1.0)
        ]
        
        for threshold_name, invalid_value in invalid_configs:
            config = self.get_valid_threshold_config()
            config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping'][threshold_name] = invalid_value
            mock_config_manager.load_config_file.return_value = config
            
            with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
                manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
                validation_summary = manager.get_validation_summary()
                
                if invalid_value < 0.0 or invalid_value > 1.0:
                    assert validation_summary['validation_errors'] > 0
                    assert any("not in valid range" in error for error in validation_summary['error_details'])
                else:
                    # Values 0.0 and 1.0 should be valid
                    pass  # No error expected
    
    def test_threshold_ordering_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of threshold ordering (high > medium > low)"""
        # Test crisis_to_high <= crisis_to_medium (invalid)
        invalid_config = self.get_valid_threshold_config()
        invalid_config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_high'] = 0.25
        invalid_config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_medium'] = 0.30
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be >" in error for error in validation_summary['error_details'])
    
    def test_ensemble_threshold_ordering_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of ensemble threshold ordering"""
        # Test high <= medium <= low (invalid)
        invalid_config = self.get_valid_threshold_config()
        invalid_config['threshold_mapping_by_mode']['consensus']['ensemble_thresholds'] = {
            'high': 0.20,   # Should be highest
            'medium': 0.25,
            'low': 0.30     # Should be lowest
        }
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be high > medium > low" in error for error in validation_summary['error_details'])
    
    def test_staff_review_threshold_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of staff review threshold ordering"""
        # Test low_confidence_threshold <= medium_confidence_threshold (invalid)
        invalid_config = self.get_valid_threshold_config()
        invalid_config['shared_configuration']['staff_review']['medium_confidence_threshold'] = 0.80
        invalid_config['shared_configuration']['staff_review']['low_confidence_threshold'] = 0.70
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be >" in error for error in validation_summary['error_details'])
    
    def test_learning_system_parameter_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of learning system parameters"""
        # Test feedback_weight outside valid range [0.0, 1.0]
        invalid_config = self.get_valid_threshold_config()
        invalid_config['shared_configuration']['learning_system']['feedback_weight'] = 1.5
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("must be in range [0.0, 1.0]" in error for error in validation_summary['error_details'])
    
    def test_safety_bias_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of safety bias parameters"""
        # Test safety bias outside reasonable range [0.0, 0.1]
        invalid_config = self.get_valid_threshold_config()
        invalid_config['shared_configuration']['safety_controls']['consensus_safety_bias'] = 0.15
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            validation_summary = manager.get_validation_summary()
            
            assert validation_summary['validation_errors'] > 0
            assert any("should be in range [0.0, 0.1]" in error for error in validation_summary['error_details'])
    
    def test_cross_mode_consistency_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test cross-mode consistency validation (warnings, not errors)"""
        # Create config where weighted mode has lower thresholds than consensus (should warn)
        config_with_warning = self.get_valid_threshold_config()
        config_with_warning['threshold_mapping_by_mode']['weighted']['crisis_level_mapping']['crisis_to_high'] = 0.45  # Lower than consensus (0.50)
        mock_config_manager.load_config_file.return_value = config_with_warning
        
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
            
            # Should fall back to defaults
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert crisis_mapping is not None
            assert 'crisis_to_high' in crisis_mapping
    
    def test_missing_mode_configurations(self, mock_config_manager, mock_model_ensemble_manager):
        """Test handling of missing ensemble mode configurations"""
        # Test with missing weighted mode configuration
        config_missing_mode = self.get_valid_threshold_config()
        del config_missing_mode['threshold_mapping_by_mode']['weighted']
        mock_config_manager.load_config_file.return_value = config_missing_mode
        
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Should fall back to defaults for missing mode
        weighted_mapping = manager.get_crisis_level_mapping_for_mode('weighted')
        assert weighted_mapping is not None
        assert 'crisis_to_high' in weighted_mapping
    
    def test_invalid_data_types(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation of invalid data types"""
        # Test string where float expected
        invalid_config = self.get_valid_threshold_config()
        invalid_config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_high'] = "invalid_string"
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Should handle gracefully and either convert or use defaults
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Should still provide valid mappings (using defaults or error handling)
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert isinstance(crisis_mapping.get('crisis_to_high'), (int, float))


class TestEnvironmentVariableOverrides:
    """Test environment variable override functionality"""
    
    @pytest.fixture
    def base_config(self):
        """Get base configuration for override testing"""
        return {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50,
                        "crisis_to_medium": 0.30
                    },
                    "ensemble_thresholds": {
                        "high": 0.45,
                        "medium": 0.25,
                        "low": 0.12
                    }
                },
                "weighted": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.55,
                        "crisis_to_medium": 0.32
                    },
                    "ensemble_thresholds": {
                        "high": 0.48,
                        "medium": 0.27,
                        "low": 0.13
                    }
                }
            },
            "shared_configuration": {
                "staff_review": {
                    "high_always": True,
                    "medium_confidence_threshold": 0.45
                },
                "learning_system": {
                    "feedback_weight": 0.1,
                    "enable_threshold_learning": True
                },
                "safety_controls": {
                    "consensus_safety_bias": 0.03
                }
            }
        }
    
    def test_crisis_level_mapping_overrides(self, base_config):
        """Test environment variable overrides for crisis level mappings"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = base_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        env_overrides = {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.60',
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM': '0.35',
            'NLP_THRESHOLD_WEIGHTED_CRISIS_TO_HIGH': '0.65'
        }
        
        with patch.dict(os.environ, env_overrides, clear=False):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            # Test consensus mode overrides
            consensus_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert consensus_mapping['crisis_to_high'] == 0.60  # Overridden
            assert consensus_mapping['crisis_to_medium'] == 0.35  # Overridden
            
            # Test weighted mode overrides
            weighted_mapping = manager.get_crisis_level_mapping_for_mode('weighted')
            assert weighted_mapping['crisis_to_high'] == 0.65  # Overridden
            assert weighted_mapping['crisis_to_medium'] == 0.32  # Not overridden, should be original
    
    def test_ensemble_threshold_overrides(self, base_config):
        """Test environment variable overrides for ensemble thresholds"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = base_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        env_overrides = {
            'NLP_THRESHOLD_CONSENSUS_ENSEMBLE_HIGH': '0.50',
            'NLP_THRESHOLD_WEIGHTED_ENSEMBLE_MEDIUM': '0.30'
        }
        
        with patch.dict(os.environ, env_overrides, clear=False):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            # Test consensus ensemble overrides
            consensus_thresholds = manager.get_ensemble_thresholds_for_mode('consensus')
            assert consensus_thresholds['high'] == 0.50  # Overridden
            assert consensus_thresholds['medium'] == 0.25  # Not overridden
            
            # Test weighted ensemble overrides
            weighted_thresholds = manager.get_ensemble_thresholds_for_mode('weighted')
            assert weighted_thresholds['medium'] == 0.30  # Overridden
            assert weighted_thresholds['high'] == 0.48  # Not overridden
    
    def test_shared_configuration_overrides(self, base_config):
        """Test environment variable overrides for shared configuration"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = base_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        env_overrides = {
            'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE': '0.50',
            'NLP_THRESHOLD_LEARNING_FEEDBACK_WEIGHT': '0.15',
            'NLP_THRESHOLD_SAFETY_BIAS': '0.05',
            'NLP_THRESHOLD_LEARNING_ENABLED': 'false'
        }
        
        with patch.dict(os.environ, env_overrides, clear=False):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            # Test staff review overrides
            staff_review_config = manager.get_staff_review_config()
            assert staff_review_config['medium_confidence_threshold'] == 0.50  # Overridden
            
            # Test learning system overrides
            learning_config = manager.get_learning_system_config()
            assert learning_config['feedback_weight'] == 0.15  # Overridden
            assert learning_config['enable_threshold_learning'] == False  # Overridden
            
            # Test safety controls overrides
            safety_config = manager.get_safety_controls_config()
            assert safety_config['consensus_safety_bias'] == 0.05  # Overridden
    
    def test_boolean_environment_variable_parsing(self, base_config):
        """Test parsing of boolean environment variables"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = base_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Test various boolean representations
        boolean_tests = [
            ('true', True),
            ('True', True),
            ('TRUE', True),
            ('1', True),
            ('yes', True),
            ('on', True),
            ('false', False),
            ('False', False),
            ('FALSE', False),
            ('0', False),
            ('no', False),
            ('off', False)
        ]
        
        for env_value, expected_bool in boolean_tests:
            env_overrides = {
                'NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS': env_value,
                'NLP_THRESHOLD_LEARNING_ENABLED': env_value,
                'NLP_THRESHOLD_ENABLE_SAFETY_OVERRIDE': env_value
            }
            
            with patch.dict(os.environ, env_overrides, clear=False):
                manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
                
                staff_review_config = manager.get_staff_review_config()
                learning_config = manager.get_learning_system_config()
                safety_config = manager.get_safety_controls_config()
                
                # All should parse to the expected boolean value
                assert staff_review_config['high_always'] == expected_bool
                assert learning_config['enable_threshold_learning'] == expected_bool
                assert safety_config['enable_safety_override'] == expected_bool
    
    def test_invalid_environment_variable_values(self, base_config):
        """Test handling of invalid environment variable values"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = base_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Test invalid float values
        env_overrides = {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': 'not_a_number',
            'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE': 'invalid_float'
        }
        
        with patch.dict(os.environ, env_overrides, clear=False):
            # Should handle gracefully and use defaults or raise appropriate errors
            try:
                manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
                
                # If it doesn't raise an error, verify it uses reasonable defaults
                consensus_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
                assert isinstance(consensus_mapping['crisis_to_high'], (int, float))
                
                staff_review_config = manager.get_staff_review_config()
                assert isinstance(staff_review_config['medium_confidence_threshold'], (int, float))
                
            except (ValueError, TypeError):
                # It's also acceptable to raise an error for invalid values
                pass
    
    def test_environment_variable_precedence(self, base_config):
        """Test that environment variables take precedence over JSON configuration"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = base_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # JSON has crisis_to_high = 0.50, override with environment variable
        env_overrides = {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.75'
        }
        
        with patch.dict(os.environ, env_overrides, clear=False):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            consensus_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert consensus_mapping['crisis_to_high'] == 0.75  # Environment variable wins
            assert consensus_mapping['crisis_to_medium'] == 0.30  # JSON default remains


class TestConfigurationFileHandling:
    """Test configuration file loading and error handling"""
    
    def test_missing_configuration_file(self):
        """Test handling of missing configuration file"""
        mock_config_manager = Mock()
        mock_config_manager.load_config_file.return_value = None
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        # Should handle gracefully and use defaults
        manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
        
        validation_summary = manager.get_validation_summary()
        assert validation_summary['configuration_loaded'] == False
        
        # Should still provide default mappings
        crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
        assert crisis_mapping is not None
        assert 'crisis_to_high' in crisis_mapping
    
    def test_corrupted_configuration_file(self):
        """Test handling of corrupted JSON configuration"""
        mock_config_manager = Mock()
        # Simulate corrupted JSON that can't be processed
        mock_config_manager.load_config_file.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        # Should handle JSON errors gracefully
        manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
        
        validation_summary = manager.get_validation_summary()
        assert len(validation_summary['error_details']) > 0
        
        # Should still provide fallback functionality
        crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
        assert crisis_mapping is not None
    
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
        """Test fail-fast behavior when enabled and errors present"""
        mock_config_manager = Mock()
        # Create invalid configuration
        invalid_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.20,  # Invalid: less than medium
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = invalid_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'true'}):
            with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
                ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
    
    def test_fail_fast_disabled_with_errors(self):
        """Test behavior when fail-fast is disabled but errors present"""
        mock_config_manager = Mock()
        # Create invalid configuration
        invalid_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.20,  # Invalid: less than medium
                        "crisis_to_medium": 0.30
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = invalid_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            # Should not raise exception
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            assert validation_summary['validation_errors'] > 0
            assert len(validation_summary['error_details']) > 0
    
    def test_fail_fast_default_behavior(self):
        """Test default fail-fast behavior (should be enabled)"""
        mock_config_manager = Mock()
        # Create invalid configuration
        invalid_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": -0.1  # Invalid: negative value
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = invalid_config
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Don't set environment variable - test default behavior
        with pytest.raises(ValueError):
            ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)


class TestConfigurationSchemaValidation:
    """Test JSON schema-like validation of configuration structure"""
    
    def test_required_sections_validation(self):
        """Test validation of required configuration sections"""
        mock_config_manager = Mock()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Test completely empty configuration
        mock_config_manager.load_config_file.return_value = {}
        
        manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
        
        # Should handle gracefully and provide defaults
        crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
        assert crisis_mapping is not None
        
        staff_review_config = manager.get_staff_review_config()
        assert staff_review_config is not None
    
    def test_partial_configuration_handling(self):
        """Test handling of partially complete configurations"""
        mock_config_manager = Mock()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'majority'
        
        # Configuration with some sections missing
        partial_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.50
                        # Missing other mappings
                    }
                    # Missing ensemble_thresholds
                }
                # Missing majority and weighted modes
            }
            # Missing shared_configuration
        }
        mock_config_manager.load_config_file.return_value = partial_config
        
        manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
        
        # Should fill in missing values with defaults
        consensus_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
        assert consensus_mapping['crisis_to_high'] == 0.50  # From config
        assert 'crisis_to_medium' in consensus_mapping  # Should have default
        
        majority_mapping = manager.get_crisis_level_mapping_for_mode('majority')
        assert majority_mapping is not None  # Should have defaults
        
        staff_review_config = manager.get_staff_review_config()
        assert staff_review_config is not None  # Should have defaults


class TestAdvancedValidationScenarios:
    """Test advanced validation scenarios and edge cases"""
    
    def test_mode_specific_validation_rules(self):
        """Test mode-specific validation rules"""
        # In the future, we might want different validation rules for different modes
        # For now, this is a placeholder for mode-specific validation
        pass
    
    def test_configuration_versioning(self):
        """Test configuration version compatibility"""
        mock_config_manager = Mock()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        # Test with different version metadata
        config_with_version = {
            "_metadata": {
                "configuration_version": "3c.2",  # Future version
                "description": "Test configuration"
            },
            "threshold_mapping_by_mode": {
                "weighted": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.55
                    }
                }
            }
        }
        mock_config_manager.load_config_file.return_value = config_with_version
        
        # Should handle version gracefully (for now)
        manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
        
        # Should still work with different versions
        validation_summary = manager.get_validation_summary()
        assert validation_summary['configuration_loaded'] == True
    
    def test_complex_validation_combinations(self):
        """Test combinations of validation errors"""
        mock_config_manager = Mock()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'consensus'
        
        # Configuration with multiple types of errors
        complex_invalid_config = {
            "threshold_mapping_by_mode": {
                "consensus": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 1.5,  # Out of range
                        "crisis_to_medium": 0.80  # Greater than crisis_to_high (after correction)
                    },
                    "ensemble_thresholds": {
                        "high": 0.10,  # Wrong ordering
                        "medium": 0.20,
                        "low": 0.30
                    }
                }
            },
            "shared_configuration": {
                "learning_system": {
                    "feedback_weight": 2.0  # Out of range
                },
                "safety_controls": {
                    "consensus_safety_bias": 0.5  # Too high
                }
            }
        }
        mock_config_manager.load_config_file.return_value = complex_invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
            
            validation_summary = manager.get_validation_summary()
            
            # Should detect multiple errors
            assert validation_summary['validation_errors'] > 3
            
            # Error details should contain information about different types of errors
            error_details = validation_summary['error_details']
            assert any("not in valid range" in error for error in error_details)
            assert any("must be" in error for error in error_details)


# Comprehensive test runner
class TestPhase3cConfigurationTestSuite:
    """Run comprehensive configuration validation test suite"""
    
    def test_run_all_validation_tests(self):
        """Meta-test to ensure all validation components work together"""
        # This could be used to run a subset of critical validation tests
        # for quick validation during development
        
        mock_config_manager = Mock()
        mock_ensemble_manager = Mock()
        mock_ensemble_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        # Use a valid configuration
        valid_config = {
            "threshold_mapping_by_mode": {
                "weighted": {
                    "crisis_level_mapping": {
                        "crisis_to_high": 0.55,
                        "crisis_to_medium": 0.32,
                        "mild_crisis_to_low": 0.42
                    },
                    "ensemble_thresholds": {
                        "high": 0.48,
                        "medium": 0.27,
                        "low": 0.13
                    }
                }
            },
            "shared_configuration": {
                "staff_review": {
                    "high_always": True,
                    "medium_confidence_threshold": 0.45
                }
            }
        }
        mock_config_manager.load_config_file.return_value = valid_config
        
        # Should initialize without errors
        manager = ThresholdMappingManager(mock_config_manager, mock_ensemble_manager)
        
        # Should pass all basic validation
        validation_summary = manager.get_validation_summary()
        assert validation_summary['validation_errors'] == 0
        assert validation_summary['configuration_loaded'] == True
        
        # Should provide all expected functionality
        assert manager.get_crisis_level_mapping_for_mode('weighted') is not None
        assert manager.get_staff_review_config() is not None
        assert manager.get_safety_controls_config() is not None


# Pytest configuration and test runners
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short', '--color=yes'])