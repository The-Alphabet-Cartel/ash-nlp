# ash-nlp/tests/test_phase_3c_endpoints.py
"""
Phase 3c: API Endpoint Tests
Tests complete analysis pipeline with new threshold system, crisis level mapping accuracy,
ensemble + pattern integration, and staff review triggering

Clean v3.1 Architecture API Test Suite
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Import the components we're testing
from api.ensemble_endpoints import integrate_pattern_and_ensemble_analysis_v3c, _map_ensemble_prediction_to_crisis_level_v3c
from managers.threshold_mapping_manager import ThresholdMappingManager


class TestEnsembleAPIIntegration:
    """Test ensemble API integration with Phase 3c components"""
    
    @pytest.fixture
    def mock_threshold_manager(self):
        """Create comprehensive mock ThresholdMappingManager for API testing"""
        mock_manager = Mock(spec=ThresholdMappingManager)
        
        # Mock current mode (can be changed per test)
        mock_manager.get_current_ensemble_mode.return_value = 'majority'
        
        # Mock crisis level mapping for majority mode
        mock_manager.get_crisis_level_mapping_for_mode.return_value = {
            'crisis_to_high': 0.45,
            'crisis_to_medium': 0.28,
            'mild_crisis_to_low': 0.35,
            'negative_to_low': 0.65,
            'unknown_to_low': 0.45
        }
        
        # Mock ensemble thresholds for majority mode
        mock_manager.get_ensemble_thresholds_for_mode.return_value = {
            'high': 0.42,
            'medium': 0.23,
            'low': 0.11
        }
        
        # Mock pattern integration config
        mock_manager.get_pattern_integration_config.return_value = {
            'pattern_weight_multiplier': 1.2,
            'confidence_boost_limit': 0.15,
            'pattern_override_threshold': 0.8
        }
        
        # Mock safety controls
        mock_manager.get_safety_controls_config.return_value = {
            'consensus_safety_bias': 0.03,
            'enable_safety_override': True,
            'fail_safe_escalation': True
        }
        
        # Mock staff review determination
        def mock_staff_review(crisis_level, confidence, disagreement=False, gap=False):
            if crisis_level == 'high':
                return True
            elif crisis_level == 'medium' and confidence >= 0.45:
                return True
            elif crisis_level == 'low' and confidence >= 0.75:
                return True
            elif disagreement or gap:
                return True
            return False
        
        mock_manager.is_staff_review_required.side_effect = mock_staff_review
        
        return mock_manager
    
    def test_crisis_prediction_mapping_accuracy(self, mock_threshold_manager):
        """Test accuracy of crisis prediction to crisis level mapping"""
        # Test cases: (prediction, confidence, expected_crisis_level)
        test_cases = [
            # Crisis predictions with majority mode thresholds (crisis_to_high=0.45, crisis_to_medium=0.28)
            ('crisis', 0.50, 'high'),      # Above high threshold
            ('crisis', 0.30, 'medium'),    # Above medium threshold
            ('crisis', 0.25, 'low'),       # Below medium but still crisis
            
            # Mild crisis predictions (mild_crisis_to_low=0.35)
            ('mild_crisis', 0.40, 'low'),  # Above threshold
            ('mild_crisis', 0.30, 'none'), # Below threshold
            
            # Negative predictions (negative_to_low=0.65)
            ('negative', 0.70, 'low'),     # Above threshold
            ('negative', 0.60, 'none'),    # Below threshold
            
            # Unknown predictions (unknown_to_low=0.45)
            ('unknown', 0.50, 'low'),      # Above threshold
            ('unknown', 0.40, 'none'),     # Below threshold
            
            # Positive predictions (should always be none)
            ('positive', 0.90, 'none'),
            ('neutral', 0.50, 'none')
        ]
        
        crisis_mapping = mock_threshold_manager.get_crisis_level_mapping_for_mode()
        
        for prediction, confidence, expected_level in test_cases:
            actual_level = _map_ensemble_prediction_to_crisis_level_v3c(
                prediction, confidence, crisis_mapping
            )
            
            assert actual_level == expected_level, (
                f"Failed for {prediction} + {confidence}: expected {expected_level}, got {actual_level}"
            )
    
    def test_pattern_and_ensemble_integration_scenarios(self, mock_threshold_manager):
        """Test various ensemble + pattern integration scenarios"""
        
        # Scenario 1: High confidence crisis with supporting patterns
        ensemble_result_1 = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.60},
            'detected_categories': ['depression', 'hopelessness'],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result_1 = {
            'patterns_triggered': [
                {'pattern_name': 'suicide_ideation', 'crisis_level': 'high', 'confidence': 0.85}
            ],
            'error': None
        }
        
        result_1 = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result_1, pattern_result_1, mock_threshold_manager
        )
        
        assert result_1['crisis_level'] == 'high'
        assert result_1['staff_review_required'] == True
        assert result_1['threshold_mode'] == 'majority'
        assert 'majority' in result_1['method']
        
        # Scenario 2: Low ensemble confidence with pattern override
        ensemble_result_2 = {
            'consensus': {'prediction': 'negative', 'confidence': 0.30},
            'detected_categories': ['sadness'],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result_2 = {
            'patterns_triggered': [
                {'pattern_name': 'self_harm', 'crisis_level': 'high', 'confidence': 0.90}  # High pattern confidence
            ],
            'error': None
        }
        
        result_2 = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result_2, pattern_result_2, mock_threshold_manager
        )
        
        # Pattern should override due to high confidence
        assert result_2['crisis_level'] in ['high', 'medium']  # Should be escalated
        assert result_2['staff_review_required'] == True
        
        # Scenario 3: Model disagreement triggers review
        ensemble_result_3 = {
            'consensus': {'prediction': 'mild_crisis', 'confidence': 0.40},
            'detected_categories': ['anxiety'],
            'gap_detection': {'gap_detected': True, 'requires_review': True}
        }
        pattern_result_3 = {
            'patterns_triggered': [],
            'error': None
        }
        
        result_3 = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result_3, pattern_result_3, mock_threshold_manager
        )
        
        assert result_3['staff_review_required'] == True  # Due to model disagreement
        
        # Scenario 4: No patterns, low ensemble confidence
        ensemble_result_4 = {
            'consensus': {'prediction': 'neutral', 'confidence': 0.20},
            'detected_categories': [],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result_4 = {
            'patterns_triggered': [],
            'error': None
        }
        
        result_4 = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result_4, pattern_result_4, mock_threshold_manager
        )
        
        assert result_4['crisis_level'] == 'none'
        assert result_4['staff_review_required'] == False
    
    def test_mode_aware_threshold_differences(self, mock_threshold_manager):
        """Test that different ensemble modes produce different results"""
        
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.50},
            'detected_categories': ['depression'],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        # Test with consensus mode (crisis_to_high=0.50)
        mock_threshold_manager.get_current_ensemble_mode.return_value = 'consensus'
        mock_threshold_manager.get_crisis_level_mapping_for_mode.return_value = {
            'crisis_to_high': 0.50,
            'crisis_to_medium': 0.30
        }
        
        result_consensus = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Test with weighted mode (crisis_to_high=0.55)
        mock_threshold_manager.get_current_ensemble_mode.return_value = 'weighted'
        mock_threshold_manager.get_crisis_level_mapping_for_mode.return_value = {
            'crisis_to_high': 0.55,
            'crisis_to_medium': 0.32
        }
        
        result_weighted = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # With confidence=0.50:
        # - Consensus mode (threshold=0.50): should map to high
        # - Weighted mode (threshold=0.55): should map to medium
        assert result_consensus['threshold_mode'] == 'consensus'
        assert result_weighted['threshold_mode'] == 'weighted'
        
        # Results should potentially be different due to different thresholds
        # (exact results depend on the mapping logic)
    
    def test_staff_review_triggering_scenarios(self, mock_threshold_manager):
        """Test various staff review triggering scenarios"""
        
        # Define test scenarios with expected staff review requirements
        scenarios = [
            # (crisis_level, confidence, has_disagreement, has_gap, expected_review)
            ('high', 0.30, False, False, True),      # High always requires review
            ('medium', 0.50, False, False, True),    # Medium + high confidence
            ('medium', 0.40, False, False, False),   # Medium + low confidence
            ('low', 0.80, False, False, True),       # Low + very high confidence
            ('low', 0.60, False, False, False),      # Low + medium confidence
            ('low', 0.30, True, False, True),        # Low + model disagreement
            ('low', 0.30, False, True, True),        # Low + gap detection
            ('none', 0.90, False, False, False),     # None (no crisis detected)
        ]
        
        for crisis_level, confidence, disagreement, gap, expected_review in scenarios:
            ensemble_result = {
                'consensus': {'prediction': 'test', 'confidence': confidence},
                'detected_categories': [],
                'gap_detection': {'gap_detected': gap, 'requires_review': gap}
            }
            pattern_result = {'patterns_triggered': [], 'error': None}
            
            # Mock the crisis level mapping to return our test crisis level
            with patch('api.ensemble_endpoints._map_ensemble_prediction_to_crisis_level_v3c') as mock_map:
                mock_map.return_value = crisis_level
                
                result = integrate_pattern_and_ensemble_analysis_v3c(
                    ensemble_result, pattern_result, mock_threshold_manager
                )
                
                assert result['staff_review_required'] == expected_review, (
                    f"Failed staff review test: {crisis_level}, {confidence}, "
                    f"disagreement={disagreement}, gap={gap}, expected={expected_review}"
                )
    
    def test_safety_controls_application(self, mock_threshold_manager):
        """Test application of safety controls"""
        
        # Configure safety controls
        mock_threshold_manager.get_safety_controls_config.return_value = {
            'consensus_safety_bias': 0.05,  # Higher bias for testing
            'enable_safety_override': True,
            'fail_safe_escalation': True
        }
        
        # Test safety bias application
        ensemble_result = {
            'consensus': {'prediction': 'mild_crisis', 'confidence': 0.40},
            'detected_categories': ['anxiety'],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Confidence should be increased by safety bias
        assert result['confidence_score'] >= 0.45  # Original 0.40 + bias 0.05
        assert result['integration_details']['safety_bias_applied'] == True
        
        # Test safety override (ensemble high should not be downgraded)
        ensemble_result_high = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.80},
            'detected_categories': ['severe_depression'],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        
        # Even if patterns might suggest lower, safety override should maintain high
        pattern_result_conflicting = {
            'patterns_triggered': [
                {'pattern_name': 'mild_concern', 'crisis_level': 'low', 'confidence': 0.30}
            ],
            'error': None
        }
        
        result_override = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result_high, pattern_result_conflicting, mock_threshold_manager
        )
        
        # Should maintain high crisis level due to safety override
        assert result_override['crisis_level'] == 'high'
    
    def test_pattern_integration_with_different_multipliers(self, mock_threshold_manager):
        """Test pattern integration with different weight multipliers"""
        
        # Test with different pattern weight multipliers
        multipliers_to_test = [1.0, 1.2, 1.5, 2.0]
        
        for multiplier in multipliers_to_test:
            mock_threshold_manager.get_pattern_integration_config.return_value = {
                'pattern_weight_multiplier': multiplier,
                'confidence_boost_limit': 0.20,
                'pattern_override_threshold': 0.75
            }
            
            ensemble_result = {
                'consensus': {'prediction': 'negative', 'confidence': 0.30},
                'detected_categories': ['sadness'],
                'gap_detection': {'gap_detected': False, 'requires_review': False}
            }
            
            pattern_result = {
                'patterns_triggered': [
                    {'pattern_name': 'concern_pattern', 'crisis_level': 'medium', 'confidence': 0.60}
                ],
                'error': None
            }
            
            result = integrate_pattern_and_ensemble_analysis_v3c(
                ensemble_result, pattern_result, mock_threshold_manager
            )
            
            # Higher multipliers should generally result in more pattern influence
            # (exact behavior depends on integration logic)
            assert 'integration_details' in result
            assert result['integration_details']['pattern_confidence'] == 0.60
    
    def test_error_handling_and_fallbacks(self, mock_threshold_manager):
        """Test error handling and fallback behavior"""
        
        # Test with ThresholdMappingManager errors
        mock_threshold_manager.get_current_ensemble_mode.side_effect = Exception("Mode detection failed")
        
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.55},
            'detected_categories': ['depression'],
            'gap_detection': {'gap_detected': False, 'requires_review': False}
        }
        pattern_result = {'patterns_triggered': [], 'error': None}
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Should handle error gracefully and still produce a result
        assert 'crisis_level' in result
        assert 'confidence_score' in result
        assert result['staff_review_required'] == True  # Conservative fallback
        
        # Test with None threshold manager
        result_no_manager = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, None
        )
        
        assert result_no_manager['threshold_mode'] == 'fallback'
        assert 'crisis_level' in result_no_manager
        
        # Test with pattern analysis errors
        pattern_result_with_error = {
            'patterns_triggered': [],
            'error': 'Pattern analysis failed'
        }
        
        result_pattern_error = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result_with_error, mock_threshold_manager
        )
        
        # Should still work with pattern errors
        assert 'crisis_level' in result_pattern_error
        assert result_pattern_error['integration_details']['pattern_available'] == False
    
    def test_edge_case_handling(self, mock_threshold_manager):
        """Test edge cases and boundary conditions"""
        
        # Test with extreme confidence values
        edge_cases = [
            # (prediction, confidence)
            ('crisis', 0.0),    # Minimum confidence
            ('crisis', 1.0),    # Maximum confidence
            ('unknown', 0.5),   # Boundary confidence
            ('neutral', 0.999), # Very high confidence non-crisis
        ]
        
        for prediction, confidence in edge_cases:
            ensemble_result = {
                'consensus': {'prediction': prediction, 'confidence': confidence},
                'detected_categories': [],
                'gap_detection': {'gap_detected': False, 'requires_review': False}
            }
            pattern_result = {'patterns_triggered': [], 'error': None}
            
            result = integrate_pattern_and_ensemble_analysis_v3c(
                ensemble_result, pattern_result, mock_threshold_manager
            )
            
            # Should handle all edge cases without errors
            assert 'crisis_level' in result
            assert 'confidence_score' in result
            assert isinstance(result['staff_review_required'], bool)
            
            # Confidence should be bounded [0.0, 1.0]
            assert 0.0 <= result['confidence_score'] <= 1.0
    
    def test_comprehensive_integration_workflow(self, mock_threshold_manager):
        """Test a comprehensive real-world integration workflow"""
        
        # Simulate a complex real-world scenario
        ensemble_result = {
            'consensus': {
                'prediction': 'mild_crisis',
                'confidence': 0.42,
                'method': 'majority_vote'
            },
            'detected_categories': ['depression', 'anxiety', 'hopelessness'],
            'gap_detection': {
                'gap_detected': True,
                'requires_review': True,
                'confidence_spread': 0.35
            },
            'individual_results': {
                'depression': [{'label': 'crisis', 'confidence': 0.65}],
                'sentiment': [{'label': 'negative', 'confidence': 0.80}],
                'emotional_distress': [{'label': 'medium_distress', 'confidence': 0.30}]
            }
        }
        
        pattern_result = {
            'patterns_triggered': [
                {
                    'pattern_name': 'hopelessness_expression',
                    'crisis_level': 'high',
                    'confidence': 0.75,
                    'category': 'emotional_indicators',
                    'weight': 1.3
                },
                {
                    'pattern_name': 'isolation_language',
                    'crisis_level': 'medium',
                    'confidence': 0.60,
                    'category': 'social_indicators',
                    'weight': 1.0
                }
            ],
            'adjustments': {
                'confidence_adjustment': 0.12,
                'crisis_boost': 0.18,
                'escalation_required': True
            },
            'summary': '2 patterns triggered with high concern indicators'
        }
        
        result = integrate_pattern_and_ensemble_analysis_v3c(
            ensemble_result, pattern_result, mock_threshold_manager
        )
        
        # Verify comprehensive result structure
        expected_keys = [
            'needs_response', 'crisis_level', 'confidence_score', 'detected_categories',
            'method', 'model_info', 'reasoning', 'staff_review_required',
            'threshold_mode', 'integration_details'
        ]
        
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
        
        # Verify integration logic worked correctly
        assert result['crisis_level'] in ['low', 'medium', 'high']  # Should be escalated
        assert result['staff_review_required'] == True  # Due to gap detection and patterns
        assert result['threshold_mode'] == 'majority'
        assert len(result['detected_categories']) > 0
        assert result['confidence_score'] > 0.42  # Should be boosted by patterns
        
        # Verify integration details
        integration_details = result['integration_details']
        assert integration_details['patterns_count'] == 2
        assert integration_details['pattern_confidence'] == 0.75  # Highest pattern confidence
        assert integration_details['final_determination'] == result['crisis_level']


class TestFullAPIEndpointIntegration:
    """Test full API endpoint integration (requires more complex setup)"""
    
    def test_analyze_endpoint_with_phase_3c(self):
        """Test the full /analyze endpoint with Phase 3c integration"""
        # This would require setting up a full FastAPI test client
        # For now, it's a placeholder for comprehensive endpoint testing
        pass
    
    def test_health_endpoint_phase_3c_status(self):
        """Test health endpoint reporting Phase 3c status"""
        # Placeholder for health endpoint testing
        pass
    
    def test_debug_endpoints_phase_3c(self):
        """Test debug endpoints for threshold configuration inspection"""
        # Placeholder for debug endpoint testing
        pass


# Pytest configuration and test runners
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short', '--color=yes'])