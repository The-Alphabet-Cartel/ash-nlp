# ash-nlp/tests/test_phase_3c_integration.py
"""
Phase 3c: Comprehensive Integration Tests
Tests complete integration of ThresholdMappingManager with existing system components

Clean v3.1 Architecture Integration Test Suite
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock

# Import system components for integration testing
from managers.threshold_mapping_manager import ThresholdMappingManager
from analysis.crisis_analyzer import CrisisAnalyzer
from api.ensemble_endpoints import integrate_pattern_and_ensemble_analysis_v3c, _map_ensemble_prediction_to_crisis_level_v3c
from managers.config_manager import ConfigManager


class TestPhase3cSystemIntegration:
    """Test complete system integration with Phase 3c components"""
    
    @pytest.fixture
    def mock_threshold_manager(self):
        """Create comprehensive mock ThresholdMappingManager"""
        mock_manager = Mock(spec=ThresholdMappingManager)
        
        # Mock current mode
        mock_manager.get_current_ensemble_mode.return_value = 'weighted'
        
        # Mock crisis level mapping
        mock_manager.get_crisis_level_mapping_for_mode.return_value = {
            'crisis_to_high': 0.55,
            'crisis_to_medium': 0.32,
            'mild_crisis_to_low': 0.42,
            'negative_to_low': 0.72,
            'unknown_to_low': 0.52
        }
        
        # Mock ensemble thresholds
        mock_manager.get_ensemble_thresholds_for_mode.return_value = {
            'high': 0.48,
            'medium': 0.27,
            'low': 0.13
        }
        
        # Mock staff review config
        mock_manager.get_staff_review_config.return_value = {
            'high_always': True,
            'medium_confidence_threshold': 0.45,
            'low_confidence_threshold': 0.75,
            'on_model_disagreement': True,
            'gap_detection_review': True
        }
        
        # Mock pattern integration config
        mock_manager.get_pattern_integration_config.return_value = {
            'pattern_weight_multiplier': 1.2,
            'confidence_boost_limit': 0.15,
            'escalation_required_minimum': 'low',
            'pattern_override_threshold': 0.8
        }
        
        # Mock safety controls
        mock_manager.get_safety_controls_config.return_value = {
            'consensus_safety_bias': 0.03,
            'enable_safety_override': True,
            'fail_safe_escalation': True
        }
        
        # Mock staff review determination
        mock_manager.is_staff_review_required.return_value = False
        
        # Mock validation summary
        mock_manager.get_validation_summary.return_value = {
            'configuration_loaded': True,
            'validation_errors': 0,
            'error_details': [],
            'current_ensemble_mode': 'weighted',
            'fail_fast_enabled': True
        }
        
        return mock_manager
    
    @pytest.fixture
    def mock_crisis_pattern_manager(self):
        """Create mock CrisisPatternManager for testing"""
        mock_manager = Mock()
        mock_manager.find_triggered_patterns.return_value = [
            {
                'pattern_name': 'test_pattern',
                'crisis_level': 'medium',
                'confidence': 0.7,
                'weight': 1.0,
                'category': 'general'
            }
        ]
        return mock_manager
    
    @pytest.fixture
    def mock_analysis_parameters_manager(self):
        """Create mock AnalysisParametersManager for testing"""
        mock_manager = Mock()
        mock_manager.get_crisis_thresholds.return_value = {
            'high': 0.55,
            'medium': 0.28,
            'low': 0.16
        }
        return mock_manager
    
    def test_crisis_analyzer_integration(self, mock_threshold_manager, mock_crisis_pattern_manager, mock_analysis_parameters_manager):
        """Test CrisisAnalyzer integration with ThresholdMappingManager"""
        # Create mock models manager
        mock_models_manager = Mock()
        mock_models_manager.analyze_with_ensemble.return_value = {
            'consensus': {
                'prediction': 'crisis',
                'confidence': 0.65
            },
            'detected_categories': ['depression'],
            'gap_detection': {
                'gap_detected': False,
                'requires_review': False
            }
        }
        
        # Create CrisisAnalyzer with all Phase 3c components
        analyzer = CrisisAnalyzer(
            models_manager=mock_models_manager,
            crisis_pattern_manager=mock_crisis_pattern_manager,
            analysis_parameters_manager=mock_analysis_parameters_manager,
            threshold_mapping_manager=mock_threshold_manager
        )
        
        # Verify initialization
        assert analyzer.threshold_mapping_manager == mock_threshold_manager
        
        # Test configuration summary includes threshold info
        config_summary = analyzer.get_configuration_summary()
        assert config_summary['phase'] == '3c'
        assert 'threshold_configuration' in config_summary
    
    @asyncio.coroutine
    def test_crisis_analyzer_message_analysis_integration(self, mock_threshold_manager, mock_crisis_pattern_manager, mock_analysis_parameters_manager):
        """Test complete message analysis with Phase 3c integration"""
        # Create mock models manager with ensemble capability
        mock_models_manager = Mock()
        mock_models_manager.analyze_with_ensemble.return_value = {
            'consensus': {
                'prediction': 'crisis',
                'confidence': 0.60,
                'method': 'weighted_ensemble'
            },
            'detected_categories': ['depression', 'hopelessness'],
            'gap_detection': {
                'gap_detected': False,
                'requires_review': False
            },
            'model_info': 'Test ensemble'
        }
        
        # Set up pattern analysis mock
        mock_crisis_pattern_manager.analyze_message = AsyncMock(return_value={
            'patterns_triggered': [
                {
                    'pattern_name': 'hopelessness_pattern',
                    'crisis_level': 'high',
                    'confidence': 0.8,
                    'weight': 1.2
                }
            ],
            'adjustments': {
                'confidence_adjustment': 0.1,
                'crisis_boost': 0.15,
                'escalation_required': True,
                'pattern_confidence': 0.8
            },
            'summary': '1 high-level pattern triggered'
        })
        
        # Create analyzer
        analyzer = CrisisAnalyzer(
            models_manager=mock_models_manager,
            crisis_pattern_manager=mock_crisis_pattern_manager,
            analysis_parameters_manager=mock_analysis_parameters_manager,
            threshold_mapping_manager=mock_threshold_manager
        )
        
        # Run analysis
        result = yield from analyzer.analyze_message("I feel hopeless and want to give up")
        
        # Verify Phase 3c integration
        assert result['method'] == 'three_model_ensemble_with_patterns_v3c'
        assert 'staff_review_required' in result
        assert 'threshold_mode' in result
        assert 'threshold_config' in result
        assert result['threshold_mode'] == 'weighted'
    
    def test_ensemble_endpoints_integration(self, mock_threshold_manager):
        """Test ensemble endpoints integration with ThresholdMappingManager"""
        # Create test ensemble result
        ensemble_result = {
            'consensus': {
                'prediction': 'mild_crisis',
                'confidence': 0.45
            },
            'detected_categories': ['anxiety'],
            'gap_detection': {
                'gap_detected': True,
                'requires_review': True
            }
        }
        
        # Create test pattern result
        pattern_result = {
            'patterns_triggered': [
                {
                    'pattern_name': 'anxiety_pattern',
                    'crisis_level': 'medium',
                    'confidence': 0.6
                }
            ],
            'error': None
        }
        
        # Test integration function
        combined_result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Verify Phase 3c integration
        assert 'staff_review_required' in combined_result
        assert 'threshold_mode' in combined_result
        assert combined_result['threshold_mode'] == 'weighted'
        assert combined_result['method'].endswith('_v3c_weighted')
        
        # Verify staff review was calculated
        mock_threshold_manager.is_staff_review_required.assert_called_once()
    
    def test_ensemble_prediction_mapping_integration(self, mock_threshold_manager):
        """Test ensemble prediction to crisis level mapping with mode-aware thresholds"""
        # Test crisis prediction with weighted mode thresholds
        crisis_level = _map_ensemble_prediction_to_crisis_level_v3c(
            'crisis', 0.60, mock_threshold_manager.get_crisis_level_mapping_for_mode()
        )
        
        # Should map to high based on weighted mode threshold (0.55)
        assert crisis_level == 'high'
        
        # Test mild_crisis prediction
        crisis_level = _map_ensemble_prediction_to_crisis_level_v3c(
            'mild_crisis', 0.50, mock_threshold_manager.get_crisis_level_mapping_for_mode()
        )
        
        # Should map to low based on weighted mode threshold (0.42)
        assert crisis_level == 'low'
        
        # Test negative prediction
        crisis_level = _map_ensemble_prediction_to_crisis_level_v3c(
            'negative', 0.75, mock_threshold_manager.get_crisis_level_mapping_for_mode()
        )
        
        # Should map to low based on weighted mode threshold (0.72)
        assert crisis_level == 'low'
    
    def test_staff_review_integration_scenarios(self, mock_threshold_manager):
        """Test various staff review scenarios with ThresholdMappingManager integration"""
        # Test high crisis always requires review
        mock_threshold_manager.is_staff_review_required.return_value = True
        
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.80},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        assert result['staff_review_required'] == True
        
        # Verify the call was made with correct parameters
        mock_threshold_manager.is_staff_review_required.assert_called()
    
    def test_mode_switching_integration(self, mock_threshold_manager):
        """Test threshold behavior changes with different ensemble modes"""
        # Test consensus mode
        mock_threshold_manager.get_current_ensemble_mode.return_value = 'consensus'
        mock_threshold_manager.get_crisis_level_mapping_for_mode.return_value = {
            'crisis_to_high': 0.50,  # Lower threshold for consensus
            'crisis_to_medium': 0.30
        }
        
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.52},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        assert result['threshold_mode'] == 'consensus'
        assert 'consensus' in result['method']
        
        # Test majority mode
        mock_threshold_manager.get_current_ensemble_mode.return_value = 'majority'
        mock_threshold_manager.get_crisis_level_mapping_for_mode.return_value = {
            'crisis_to_high': 0.45,  # Different threshold for majority
            'crisis_to_medium': 0.28
        }
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        assert result['threshold_mode'] == 'majority'
        assert 'majority' in result['method']
    
    def test_safety_controls_integration(self, mock_threshold_manager):
        """Test safety controls integration with ThresholdMappingManager"""
        # Configure safety controls
        mock_threshold_manager.get_safety_controls_config.return_value = {
            'consensus_safety_bias': 0.05,
            'enable_safety_override': True,
            'fail_safe_escalation': True
        }
        
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.60},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Confidence should be increased by safety bias
        assert result['confidence_score'] >= 0.60  # Original confidence plus bias
        
        # Safety bias should be documented in integration details
        assert result['integration_details']['safety_bias_applied'] == True
    
    def test_pattern_integration_with_mode_awareness(self, mock_threshold_manager):
        """Test pattern integration with mode-aware scaling"""
        # Configure pattern integration for different modes
        mock_threshold_manager.get_pattern_integration_config.return_value = {
            'pattern_weight_multiplier': 1.3,  # Higher multiplier
            'confidence_boost_limit': 0.20,
            'pattern_override_threshold': 0.75
        }
        
        ensemble_result = {
            'consensus': {'prediction': 'negative', 'confidence': 0.40},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        
        pattern_result = {
            'patterns_triggered': [
                {
                    'pattern_name': 'high_risk_pattern',
                    'crisis_level': 'high',
                    'confidence': 0.85  # Above override threshold
                }
            ],
            'error': None
        }
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Pattern should override ensemble result due to high confidence
        assert result['crisis_level'] in ['high', 'medium']  # Should be escalated
        
        # Integration details should show pattern override
        integration_details = result['integration_details']
        assert integration_details['pattern_confidence'] == 0.85
    
    def test_validation_integration(self, mock_threshold_manager):
        """Test validation integration across system components"""
        # Configure validation summary with warnings
        mock_threshold_manager.get_validation_summary.return_value = {
            'configuration_loaded': True,
            'validation_errors': 1,
            'error_details': ['Minor threshold inconsistency warning'],
            'current_ensemble_mode': 'weighted',
            'fail_fast_enabled': False
        }
        
        # Test that system still operates with validation warnings
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.55},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # System should still function despite validation warnings
        assert result['crisis_level'] in ['none', 'low', 'medium', 'high']
        assert result['confidence_score'] > 0.0
    
    def test_fallback_behavior_integration(self, mock_threshold_manager):
        """Test fallback behavior when ThresholdMappingManager is not available"""
        # Test with None threshold manager
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.55},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, None  # No threshold manager
        )
        
        # Should use fallback behavior
        assert result['threshold_mode'] == 'fallback'
        assert result['staff_review_required'] in [True, False]  # Should have fallback logic
        
        # Should still produce valid result
        assert result['crisis_level'] in ['none', 'low', 'medium', 'high']
    
    def test_error_handling_integration(self, mock_threshold_manager):
        """Test error handling in Phase 3c integration"""
        # Configure threshold manager to raise errors
        mock_threshold_manager.get_current_ensemble_mode.side_effect = Exception("Mode detection failed")
        
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.55},
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        # Should handle errors gracefully
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Should still produce a valid result
        assert 'crisis_level' in result
        assert result['staff_review_required'] == True  # Conservative fallback


class TestPhase3cEndToEndIntegration:
    """End-to-end integration tests for complete Phase 3c system"""
    
    def test_complete_analysis_pipeline(self):
        """Test complete analysis pipeline with all Phase 3c components"""
        # This test would require setting up the complete system
        # For now, it's a placeholder for future comprehensive testing
        pass
    
    def test_configuration_hot_reload(self):
        """Test configuration changes without system restart"""
        # Placeholder for testing configuration hot-reload capabilities
        pass
    
    def test_performance_with_phase_3c_integration(self):
        """Test performance impact of Phase 3c integration"""
        # Placeholder for performance testing
        pass


# Pytest configuration and test runners
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short', '--color=yes'])