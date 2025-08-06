# ash-nlp/tests/test_threshold_mapping_manager.py
"""
Phase 3c: Comprehensive Unit Tests for ThresholdMappingManager
Tests mode-aware threshold loading, validation, and environment variable overrides

Clean v3.1 Architecture Test Suite
"""

import os
import pytest
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Import the components we're testing
from managers.threshold_mapping_manager import ThresholdMappingManager, create_threshold_mapping_manager
from managers.config_manager import ConfigManager

class TestThresholdMappingManager:
    """Comprehensive unit tests for ThresholdMappingManager"""
    
    @pytest.fixture
    def mock_config_manager(self):
        """Create mock ConfigManager for testing"""
        mock_config = Mock(spec=ConfigManager)
        mock_config.load_config_file.return_value = self.get_test_threshold_config()
        return mock_config
    
    @pytest.fixture
    def mock_model_ensemble_manager(self):
        """Create mock ModelEnsembleManager for testing"""
        mock_manager = Mock()
        mock_manager.get_current_ensemble_mode.return_value = 'weighted'
        return mock_manager
    
    def get_test_threshold_config(self):
        """Get test threshold configuration"""
        return {
            "_metadata": {
                "configuration_version": "3c.1",
                "description": "Test threshold configuration",
                "ensemble_modes_supported": ["consensus", "majority", "weighted"]
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
            }
        }
    
    def test_initialization_success(self, mock_config_manager, mock_model_ensemble_manager):
        """Test successful ThresholdMappingManager initialization"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        assert manager.config_manager == mock_config_manager
        assert manager.model_ensemble_manager == mock_model_ensemble_manager
        assert manager._processed_config is not None
        assert len(manager._validation_errors) == 0
    
    def test_initialization_with_validation_errors(self, mock_config_manager, mock_model_ensemble_manager):
        """Test initialization with validation errors and fail-fast disabled"""
        # Create config with validation errors
        invalid_config = self.get_test_threshold_config()
        invalid_config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_high'] = 0.20  # Lower than medium
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            assert len(manager._validation_errors) > 0
            assert "crisis_to_high" in str(manager._validation_errors)
    
    def test_initialization_fail_fast(self, mock_config_manager, mock_model_ensemble_manager):
        """Test initialization with fail-fast validation enabled"""
        # Create config with validation errors
        invalid_config = self.get_test_threshold_config()
        invalid_config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_high'] = 0.20
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'true'}):
            with pytest.raises(ValueError, match="Invalid threshold mapping configuration"):
                ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
    
    def test_crisis_level_mapping_for_mode(self, mock_config_manager, mock_model_ensemble_manager):
        """Test getting crisis level mapping for specific modes"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Test consensus mode
        consensus_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
        assert consensus_mapping['crisis_to_high'] == 0.50
        assert consensus_mapping['crisis_to_medium'] == 0.30
        
        # Test majority mode
        majority_mapping = manager.get_crisis_level_mapping_for_mode('majority')
        assert majority_mapping['crisis_to_high'] == 0.45
        assert majority_mapping['crisis_to_medium'] == 0.28
        
        # Test weighted mode
        weighted_mapping = manager.get_crisis_level_mapping_for_mode('weighted')
        assert weighted_mapping['crisis_to_high'] == 0.55
        assert weighted_mapping['crisis_to_medium'] == 0.32
    
    def test_ensemble_thresholds_for_mode(self, mock_config_manager, mock_model_ensemble_manager):
        """Test getting ensemble thresholds for specific modes"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Test consensus mode
        consensus_thresholds = manager.get_ensemble_thresholds_for_mode('consensus')
        assert consensus_thresholds['high'] == 0.45
        assert consensus_thresholds['medium'] == 0.25
        assert consensus_thresholds['low'] == 0.12
        
        # Test weighted mode
        weighted_thresholds = manager.get_ensemble_thresholds_for_mode('weighted')
        assert weighted_thresholds['high'] == 0.48
        assert weighted_thresholds['medium'] == 0.27
        assert weighted_thresholds['low'] == 0.13
    
    def test_current_ensemble_mode_detection(self, mock_config_manager, mock_model_ensemble_manager):
        """Test current ensemble mode detection"""
        mock_model_ensemble_manager.get_current_ensemble_mode.return_value = 'majority'
        
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        current_mode = manager.get_current_ensemble_mode()
        assert current_mode == 'majority'
        
        # Test automatic mode-based threshold loading
        current_mapping = manager.get_crisis_level_mapping_for_mode()  # No mode specified
        majority_mapping = manager.get_crisis_level_mapping_for_mode('majority')
        assert current_mapping == majority_mapping
    
    def test_environment_variable_overrides(self, mock_config_manager, mock_model_ensemble_manager):
        """Test environment variable overrides for thresholds"""
        env_overrides = {
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': '0.60',
            'NLP_THRESHOLD_WEIGHTED_CRISIS_TO_MEDIUM': '0.35',
            'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE': '0.50'
        }
        
        with patch.dict(os.environ, env_overrides):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            # Test consensus mode override
            consensus_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert consensus_mapping['crisis_to_high'] == 0.60  # Overridden from 0.50
            
            # Test weighted mode override
            weighted_mapping = manager.get_crisis_level_mapping_for_mode('weighted')
            assert weighted_mapping['crisis_to_medium'] == 0.35  # Overridden from 0.32
            
            # Test staff review override
            staff_review_config = manager.get_staff_review_config()
            assert staff_review_config['medium_confidence_threshold'] == 0.50  # Overridden from 0.45
    
    def test_staff_review_determination(self, mock_config_manager, mock_model_ensemble_manager):
        """Test staff review requirement determination"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Test high crisis always requires review
        assert manager.is_staff_review_required('high', 0.5) == True
        
        # Test medium crisis with high confidence
        assert manager.is_staff_review_required('medium', 0.50) == True  # Above threshold
        assert manager.is_staff_review_required('medium', 0.40) == False  # Below threshold
        
        # Test low crisis with very high confidence
        assert manager.is_staff_review_required('low', 0.80) == True  # Above threshold
        assert manager.is_staff_review_required('low', 0.70) == False  # Below threshold
        
        # Test model disagreement triggers review
        assert manager.is_staff_review_required('low', 0.30, has_model_disagreement=True) == True
        
        # Test gap detection triggers review
        assert manager.is_staff_review_required('low', 0.30, has_gap_detection=True) == True
    
    def test_validation_cross_mode_consistency(self, mock_config_manager, mock_model_ensemble_manager):
        """Test cross-mode threshold consistency validation"""
        # Create config where weighted mode has lower thresholds than consensus (should warn)
        config_with_inconsistency = self.get_test_threshold_config()
        config_with_inconsistency['threshold_mapping_by_mode']['weighted']['crisis_level_mapping']['crisis_to_high'] = 0.45  # Lower than consensus
        
        mock_config_manager.load_config_file.return_value = config_with_inconsistency
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            # Should create manager but log warnings (not tested here, but validation occurs)
    
    def test_learning_system_integration(self, mock_config_manager, mock_model_ensemble_manager):
        """Test learning system integration for threshold adjustment"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Test threshold adjustment
        adjustment_applied = manager.adjust_threshold_with_learning(
            'crisis_to_high', 'weighted', 0.05
        )
        
        assert adjustment_applied == True  # Should accept adjustment
        
        # Test with learning disabled
        with patch.dict(os.environ, {'NLP_THRESHOLD_LEARNING_ENABLED': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            adjustment_applied = manager.adjust_threshold_with_learning(
                'crisis_to_high', 'weighted', 0.05
            )
            assert adjustment_applied == False  # Should reject adjustment
    
    def test_fallback_behavior(self, mock_config_manager, mock_model_ensemble_manager):
        """Test fallback behavior when configuration is missing"""
        # Test with no configuration
        mock_config_manager.load_config_file.return_value = None
        
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Should use default values
        crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
        assert crisis_mapping['crisis_to_high'] == 0.50  # Default value
        
        ensemble_thresholds = manager.get_ensemble_thresholds_for_mode('consensus')
        assert ensemble_thresholds['high'] == 0.45  # Default value
    
    def test_validation_summary(self, mock_config_manager, mock_model_ensemble_manager):
        """Test validation summary generation"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        summary = manager.get_validation_summary()
        
        assert 'configuration_loaded' in summary
        assert 'validation_errors' in summary
        assert 'current_ensemble_mode' in summary
        assert 'fail_fast_enabled' in summary
        
        assert summary['configuration_loaded'] == True
        assert summary['validation_errors'] == 0  # No errors with valid config
        assert summary['current_ensemble_mode'] == 'weighted'  # From mock
    
    def test_factory_function(self, mock_config_manager, mock_model_ensemble_manager):
        """Test factory function for creating ThresholdMappingManager"""
        manager = create_threshold_mapping_manager(mock_config_manager, mock_model_ensemble_manager)
        
        assert isinstance(manager, ThresholdMappingManager)
        assert manager.config_manager == mock_config_manager
        assert manager.model_ensemble_manager == mock_model_ensemble_manager
    
    def test_shared_configuration_access(self, mock_config_manager, mock_model_ensemble_manager):
        """Test access to shared configuration components"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Test pattern integration config
        pattern_config = manager.get_pattern_integration_config()
        assert pattern_config['pattern_weight_multiplier'] == 1.2
        assert pattern_config['confidence_boost_limit'] == 0.15
        
        # Test safety controls config
        safety_config = manager.get_safety_controls_config()
        assert safety_config['consensus_safety_bias'] == 0.03
        assert safety_config['enable_safety_override'] == True
        
        # Test learning system config
        learning_config = manager.get_learning_system_config()
        assert learning_config['feedback_weight'] == 0.1
        assert learning_config['enable_threshold_learning'] == True
    
    def test_invalid_mode_handling(self, mock_config_manager, mock_model_ensemble_manager):
        """Test handling of invalid ensemble modes"""
        manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
        
        # Test with invalid mode - should fallback to defaults
        invalid_mode_mapping = manager.get_crisis_level_mapping_for_mode('invalid_mode')
        default_mapping = manager._get_default_crisis_mapping()
        assert invalid_mode_mapping == default_mapping
    
    def test_threshold_range_validation(self, mock_config_manager, mock_model_ensemble_manager):
        """Test threshold range validation (0.0 to 1.0)"""
        # Create config with out-of-range values
        invalid_config = self.get_test_threshold_config()
        invalid_config['threshold_mapping_by_mode']['consensus']['crisis_level_mapping']['crisis_to_high'] = 1.5  # Invalid range
        mock_config_manager.load_config_file.return_value = invalid_config
        
        with patch.dict(os.environ, {'NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID': 'false'}):
            manager = ThresholdMappingManager(mock_config_manager, mock_model_ensemble_manager)
            
            assert len(manager._validation_errors) > 0
            assert "not in valid range" in str(manager._validation_errors)


class TestThresholdMappingManagerIntegration:
    """Integration tests for ThresholdMappingManager with real config files"""
    
    def test_real_config_file_loading(self):
        """Test loading with actual config file structure"""
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
            manager = ThresholdMappingManager(config_manager, mock_ensemble_manager)
            
            crisis_mapping = manager.get_crisis_level_mapping_for_mode('consensus')
            assert crisis_mapping['crisis_to_high'] == 0.50


# Pytest configuration and test runners
if __name__ == '__main__':
    # Run tests with comprehensive output
    pytest.main([__file__, '-v', '--tb=short', '--color=yes'])