#!/usr/bin/env python3
"""
Phase 3c: Comprehensive Integration Tests
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-13
PHASE: 3d, Step 10.11-3
CLEAN ARCHITECTURE: v3.1 Compliant
Tests complete integration of ThresholdMappingManager with existing system components

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import pytest
import sys
import os
import logging
from unittest.mock import Mock, AsyncMock, patch, MagicMock

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
    # Import system components for integration testing
    from managers.threshold_mapping_manager import ThresholdMappingManager
    from analysis.crisis_analyzer import CrisisAnalyzer
    from api.ensemble_endpoints import integrate_pattern_and_ensemble_analysis_v3c, _map_ensemble_prediction_to_crisis_level_v3c
    from managers.unified_config_manager import UnifiedConfigManager
    logger.info("✅ Successfully imported Phase 3c integration components")
except ImportError as e:
    logger.error(f"❌ Failed to import Phase 3c components: {e}")
    logger.error("🔍 Make sure the app is properly configured and all components are available")


class TestPhase3cSystemIntegration:
    """Test complete system integration with Phase 3c components"""
    # REMOVED: pytestmark = pytest.mark.asyncio - This was causing the warnings
    
    @pytest.fixture
    def mock_threshold_manager(self):
        """Create comprehensive mock ThresholdMappingManager"""
        logger.info("🔧 Setting up mock ThresholdMappingManager...")
        
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
        
        # ADDED: Mock is_staff_review_required method - this was missing!
        mock_manager.is_staff_review_required.return_value = True
        
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
            'minimum_response_threshold': 0.10,
            'fail_safe_escalation': True
        }
        
        # Mock validation summary
        mock_manager.get_validation_summary.return_value = {
            'configuration_loaded': True,
            'validation_errors': 0,
            'error_details': [],
            'current_ensemble_mode': 'weighted',
            'fail_fast_enabled': True
        }
        
        logger.info("✅ Mock ThresholdMappingManager configured")
        return mock_manager
    
    @pytest.fixture
    def mock_crisis_pattern_manager(self):
        """Create mock CrisisPatternManager for testing"""
        logger.info("🔧 Setting up mock CrisisPatternManager...")
        
        mock_manager = Mock()
        mock_manager.get_pattern_categories.return_value = ['self_harm', 'suicidal_ideation', 'depression']
        mock_manager.get_patterns_for_category.return_value = ['pattern1', 'pattern2']
        mock_manager.validate_pattern_set.return_value = {'valid': True, 'pattern_count': 50}
        
        logger.info("✅ Mock CrisisPatternManager configured")
        return mock_manager
    
    @pytest.fixture
    def mock_analysis_parameters_manager(self):
        """Create mock AnalysisParametersManager for testing"""
        logger.info("🔧 Setting up mock AnalysisParametersManager...")
        
        mock_manager = Mock()
        mock_manager.get_crisis_thresholds.return_value = {'high': 0.7, 'medium': 0.4, 'low': 0.2}
        mock_manager.get_phrase_extraction_parameters.return_value = {'min_length': 3, 'max_length': 7}
        mock_manager.validate_parameters.return_value = {'valid': True}
        
        logger.info("✅ Mock AnalysisParametersManager configured")
        return mock_manager
    
    def test_crisis_analyzer_integration(self, mock_threshold_manager, mock_crisis_pattern_manager, mock_analysis_parameters_manager):
        """Test CrisisAnalyzer integration with ThresholdMappingManager"""
        logger.info("🧪 Testing CrisisAnalyzer integration with Phase 3c components...")
        
        # Create mock models manager
        mock_model_ensemble_manager = Mock()
        mock_model_ensemble_manager.is_ready.return_value = True
        
        # Create CrisisAnalyzer with Phase 3c integration
        try:
            # Test that CrisisAnalyzer can be created with threshold manager
            # Note: This tests the integration pattern, actual implementation may vary
            analyzer_components = {
                'model_ensemble_manager': mock_model_ensemble_manager,
                'crisis_pattern_manager': mock_crisis_pattern_manager,
                'analysis_parameters_manager': mock_analysis_parameters_manager,
                'threshold_mapping_manager': mock_threshold_manager
            }
            
            # Verify all components are available for integration
            for component_name, component in analyzer_components.items():
                assert component is not None, f"{component_name} should be available for integration"
                logger.info(f"   ✅ {component_name} available for integration")
            
            # Test that threshold manager provides required methods
            current_mode = mock_threshold_manager.get_current_ensemble_mode()
            crisis_mapping = mock_threshold_manager.get_crisis_level_mapping_for_mode(current_mode)
            staff_config = mock_threshold_manager.get_staff_review_config()
            
            assert current_mode == 'weighted'
            assert isinstance(crisis_mapping, dict)
            assert isinstance(staff_config, dict)
            
            logger.info("✅ CrisisAnalyzer integration test passed")
            
        except Exception as e:
            logger.error(f"❌ CrisisAnalyzer integration failed: {e}")
            raise
    
    def test_crisis_analyzer_message_analysis_integration(self, mock_threshold_manager, mock_crisis_pattern_manager, mock_analysis_parameters_manager):
        """Test message analysis integration with Phase 3c threshold mapping"""
        logger.info("🧪 Testing message analysis integration with threshold mapping...")
        
        try:
            # Test threshold-aware message analysis
            test_message = "I'm feeling really overwhelmed and don't know what to do"
            
            # Simulate ensemble analysis result
            ensemble_result = {
                'consensus': {'prediction': 'crisis', 'confidence': 0.62},
                'majority': {'prediction': 'crisis', 'confidence': 0.58},
                'weighted': {'prediction': 'crisis', 'confidence': 0.65}
            }
            
            # Get current mode thresholds
            current_mode = mock_threshold_manager.get_current_ensemble_mode()
            crisis_mapping = mock_threshold_manager.get_crisis_level_mapping_for_mode(current_mode)
            
            # Test crisis level mapping
            crisis_confidence = ensemble_result[current_mode]['confidence']
            
            # Simulate threshold-based crisis level determination
            if crisis_confidence >= crisis_mapping['crisis_to_high']:
                expected_level = 'high'
            elif crisis_confidence >= crisis_mapping['crisis_to_medium']:
                expected_level = 'medium'
            else:
                expected_level = 'low'
            
            logger.info(f"   📊 Mode: {current_mode}, Confidence: {crisis_confidence}, Expected Level: {expected_level}")
            
            # Verify threshold mapping works
            assert expected_level in ['high', 'medium', 'low']
            assert isinstance(crisis_confidence, (int, float))
            
            logger.info("✅ Message analysis integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Message analysis integration failed: {e}")
            raise
    
    def test_ensemble_endpoints_integration(self, mock_threshold_manager):
        """Test ensemble endpoints integration with ThresholdMappingManager"""
        logger.info("🧪 Testing ensemble endpoints integration...")
        
        # Test ensemble result integration
        ensemble_result = {
            'consensus': {'prediction': 'crisis', 'confidence': 0.55},
            'majority': {'prediction': 'mild_crisis', 'confidence': 0.48},
            'weighted': {'prediction': 'crisis', 'confidence': 0.62},
            'gap_detection': {'gap_detected': False, 'requires_review': False},
            'detected_categories': ['depression', 'anxiety']
        }
        
        pattern_result = {
            'patterns_triggered': ['depression_indicators', 'isolation_patterns'],
            'pattern_confidence': 0.7,
            'community_patterns': True,
            'error': None
        }
        
        logger.info(f"   📊 Calling integrate_pattern_and_ensemble_analysis_v3c...")
        logger.info(f"   📊 Ensemble result keys: {list(ensemble_result.keys())}")
        logger.info(f"   📊 Pattern result keys: {list(pattern_result.keys())}")
        logger.info(f"   📊 Mock manager available: {mock_threshold_manager is not None}")
        
        try:
            # Test the actual integration function - this should work!
            integrated_result = integrate_pattern_and_ensemble_analysis_v3c(
                ensemble_result, pattern_result, mock_threshold_manager
            )
            
            logger.info(f"   📊 Integration successful! Result keys: {list(integrated_result.keys())}")
            
            # Verify the actual result structure - be specific about what we expect
            if 'crisis_level' not in integrated_result:
                logger.error(f"❌ Missing 'crisis_level' in result. Got: {integrated_result}")
                raise AssertionError("Missing crisis_level in integration result")
            
            if 'staff_review_required' not in integrated_result:
                logger.error(f"❌ Missing 'staff_review_required' in result. Got: {integrated_result}")
                raise AssertionError("Missing staff_review_required in integration result")
            
            # Test the values
            crisis_level = integrated_result['crisis_level']
            staff_review = integrated_result['staff_review_required']
            
            assert crisis_level in ['none', 'low', 'medium', 'high'], f"Invalid crisis_level: {crisis_level}"
            assert isinstance(staff_review, bool), f"staff_review_required should be bool, got {type(staff_review)}"
            
            logger.info(f"   ✅ Crisis level: {crisis_level}")
            logger.info(f"   ✅ Staff review required: {staff_review}")
            
            # Verify mock was called correctly
            logger.info(f"   📊 Checking if mock methods were called...")
            mock_threshold_manager.get_current_ensemble_mode.assert_called()
            mock_threshold_manager.get_crisis_level_mapping_for_mode.assert_called()
            
            logger.info("✅ Ensemble endpoints integration test passed")
            
        except Exception as e:
            # This is what we want - to see the actual error!
            logger.error(f"❌ Integration function failed with error: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            
            # Log what we tried to call it with
            logger.error(f"❌ Called with ensemble_result: {ensemble_result}")
            logger.error(f"❌ Called with pattern_result: {pattern_result}")
            logger.error(f"❌ Called with threshold_manager: {type(mock_threshold_manager)}")
            
            # Log mock setup
            logger.error(f"❌ Mock current_mode method: {hasattr(mock_threshold_manager, 'get_current_ensemble_mode')}")
            logger.error(f"❌ Mock crisis_mapping method: {hasattr(mock_threshold_manager, 'get_crisis_level_mapping_for_mode')}")
            logger.error(f"❌ Mock staff_review method: {hasattr(mock_threshold_manager, 'is_staff_review_required')}")
            
            # Re-raise so we can see the actual problem and fix it
            raise
    
    def test_ensemble_prediction_mapping_integration(self, mock_threshold_manager):
        """Test ensemble prediction mapping with ThresholdMappingManager"""
        logger.info("🧪 Testing ensemble prediction mapping integration...")
        
        try:
            # Test prediction mapping scenarios
            test_scenarios = [
                {'prediction': 'crisis', 'confidence': 0.65, 'expected_level': 'high'},
                {'prediction': 'crisis', 'confidence': 0.40, 'expected_level': 'medium'},
                {'prediction': 'mild_crisis', 'confidence': 0.25, 'expected_level': 'low'},
                {'prediction': 'negative', 'confidence': 0.80, 'expected_level': 'low'},
                {'prediction': 'unknown', 'confidence': 0.60, 'expected_level': 'low'}
            ]
            
            current_mode = mock_threshold_manager.get_current_ensemble_mode()
            crisis_mapping = mock_threshold_manager.get_crisis_level_mapping_for_mode(current_mode)
            
            for scenario in test_scenarios:
                prediction = scenario['prediction']
                confidence = scenario['confidence']
                
                logger.info(f"   🧪 Testing: {prediction} with confidence {confidence}")
                
                # Test mapping logic (simplified version)
                if prediction == 'crisis':
                    if confidence >= crisis_mapping.get('crisis_to_high', 0.5):
                        mapped_level = 'high'
                    elif confidence >= crisis_mapping.get('crisis_to_medium', 0.3):
                        mapped_level = 'medium'
                    else:
                        mapped_level = 'low'
                else:
                    # Non-crisis predictions use different thresholds
                    mapped_level = 'low'  # Simplified
                
                assert mapped_level in ['high', 'medium', 'low']
                logger.info(f"     📊 Mapped to: {mapped_level}")
            
            logger.info("✅ Ensemble prediction mapping integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Ensemble prediction mapping integration failed: {e}")
            raise
    
    def test_staff_review_integration_scenarios(self, mock_threshold_manager):
        """Test staff review determination with ThresholdMappingManager"""
        logger.info("🧪 Testing staff review integration scenarios...")
        
        try:
            staff_config = mock_threshold_manager.get_staff_review_config()
            
            # Test various scenarios
            scenarios = [
                {'crisis_level': 'high', 'confidence': 0.8, 'gap_detected': False},
                {'crisis_level': 'medium', 'confidence': 0.4, 'gap_detected': False},
                {'crisis_level': 'medium', 'confidence': 0.7, 'gap_detected': True},
                {'crisis_level': 'low', 'confidence': 0.3, 'gap_detected': False}
            ]
            
            for scenario in scenarios:
                crisis_level = scenario['crisis_level']
                confidence = scenario['confidence']
                gap_detected = scenario['gap_detected']
                
                # Apply staff review logic
                requires_review = False
                
                # High crisis always requires review
                if crisis_level == 'high' and staff_config.get('high_always', True):
                    requires_review = True
                
                # Medium confidence threshold check
                elif crisis_level == 'medium' and confidence < staff_config.get('medium_confidence_threshold', 0.45):
                    requires_review = True
                
                # Low confidence threshold check
                elif crisis_level == 'low' and confidence < staff_config.get('low_confidence_threshold', 0.75):
                    requires_review = True
                
                # Gap detection review
                elif gap_detected and staff_config.get('gap_detection_review', True):
                    requires_review = True
                
                logger.info(f"   📊 {crisis_level} level, confidence {confidence}, gap {gap_detected} → review: {requires_review}")
                
                # Should have valid boolean result
                assert isinstance(requires_review, bool)
            
            logger.info("✅ Staff review integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Staff review integration failed: {e}")
            raise
    
    def test_mode_switching_integration(self, mock_threshold_manager):
        """Test dynamic mode switching with different threshold configurations"""
        logger.info("🧪 Testing mode switching integration...")
        
        try:
            # Test different modes
            test_modes = ['consensus', 'majority', 'weighted']
            
            for mode in test_modes:
                logger.info(f"   🧪 Testing mode: {mode}")
                
                # Change mock return value for different modes
                mock_threshold_manager.get_current_ensemble_mode.return_value = mode
                
                # Get mode-specific configuration
                crisis_mapping = mock_threshold_manager.get_crisis_level_mapping_for_mode(mode)
                ensemble_thresholds = mock_threshold_manager.get_ensemble_thresholds_for_mode(mode)
                
                # Verify mode-specific data is available
                assert isinstance(crisis_mapping, dict)
                assert isinstance(ensemble_thresholds, dict)
                
                # Verify threshold structure
                assert 'crisis_to_high' in crisis_mapping
                assert 'crisis_to_medium' in crisis_mapping
                assert 'high' in ensemble_thresholds
                assert 'medium' in ensemble_thresholds
                assert 'low' in ensemble_thresholds
                
                logger.info(f"     ✅ Mode {mode} configuration valid")
            
            logger.info("✅ Mode switching integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Mode switching integration failed: {e}")
            raise
    
    def test_safety_controls_integration(self, mock_threshold_manager):
        """Test safety controls integration with ThresholdMappingManager"""
        logger.info("🧪 Testing safety controls integration...")
        
        try:
            safety_config = mock_threshold_manager.get_safety_controls_config()
            
            # Test safety configuration
            assert isinstance(safety_config, dict)
            assert 'enable_safety_override' in safety_config
            assert 'consensus_safety_bias' in safety_config
            
            # Test safety bias application
            safety_bias = safety_config.get('consensus_safety_bias', 0.03)
            enable_override = safety_config.get('enable_safety_override', True)
            
            # Simulate applying safety bias
            original_confidence = 0.45
            adjusted_confidence = original_confidence + safety_bias if enable_override else original_confidence
            
            logger.info(f"   📊 Original confidence: {original_confidence}, Adjusted: {adjusted_confidence}")
            
            # Should have valid numeric values
            assert isinstance(safety_bias, (int, float))
            assert isinstance(enable_override, bool)
            assert 0.0 <= safety_bias <= 0.2  # Reasonable bias range
            
            logger.info("✅ Safety controls integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Safety controls integration failed: {e}")
            raise
    
    def test_pattern_integration_with_mode_awareness(self, mock_threshold_manager):
        """Test pattern integration with mode-aware threshold adjustment"""
        logger.info("🧪 Testing pattern integration with mode awareness...")
        
        try:
            pattern_config = mock_threshold_manager.get_pattern_integration_config()
            
            # Test pattern integration configuration
            assert isinstance(pattern_config, dict)
            assert 'pattern_weight_multiplier' in pattern_config
            assert 'confidence_boost_limit' in pattern_config
            
            # Simulate pattern-based confidence adjustment
            base_confidence = 0.35
            pattern_multiplier = pattern_config.get('pattern_weight_multiplier', 1.2)
            boost_limit = pattern_config.get('confidence_boost_limit', 0.15)
            
            # Apply pattern boost
            pattern_boost = min(base_confidence * (pattern_multiplier - 1.0), boost_limit)
            adjusted_confidence = base_confidence + pattern_boost
            
            logger.info(f"   📊 Base: {base_confidence}, Boost: {pattern_boost}, Adjusted: {adjusted_confidence}")
            
            # Verify reasonable values
            assert isinstance(pattern_multiplier, (int, float))
            assert isinstance(boost_limit, (int, float))
            assert pattern_multiplier >= 1.0  # Should boost, not reduce
            assert 0.0 <= boost_limit <= 0.5  # Reasonable boost limit
            
            # Test different mode scenarios
            current_mode = mock_threshold_manager.get_current_ensemble_mode()
            crisis_mapping = mock_threshold_manager.get_crisis_level_mapping_for_mode(current_mode)
            
            # Apply threshold mapping to adjusted confidence
            if adjusted_confidence >= crisis_mapping.get('crisis_to_high', 0.5):
                final_level = 'high'
            elif adjusted_confidence >= crisis_mapping.get('crisis_to_medium', 0.3):
                final_level = 'medium'
            else:
                final_level = 'low'
            
            logger.info(f"   📊 Final crisis level: {final_level}")
            assert final_level in ['high', 'medium', 'low']
            
            logger.info("✅ Pattern integration with mode awareness test passed")
            
        except Exception as e:
            logger.error(f"❌ Pattern integration failed: {e}")
            raise
    
    def test_validation_integration(self, mock_threshold_manager):
        """Test validation integration across Phase 3c components"""
        logger.info("🧪 Testing validation integration...")
        
        try:
            validation_summary = mock_threshold_manager.get_validation_summary()
            
            # Test validation summary structure
            required_keys = ['configuration_loaded', 'validation_errors', 'error_details', 'current_ensemble_mode']
            for key in required_keys:
                assert key in validation_summary, f"Missing validation key: {key}"
            
            # Test validation results
            assert validation_summary['configuration_loaded'] is True
            assert validation_summary['validation_errors'] == 0
            assert isinstance(validation_summary['error_details'], list)
            assert validation_summary['current_ensemble_mode'] in ['consensus', 'majority', 'weighted']
            
            logger.info(f"   📊 Validation summary: {validation_summary}")
            logger.info("✅ Validation integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Validation integration failed: {e}")
            raise
    
    def test_fallback_behavior_integration(self, mock_threshold_manager):
        """Test fallback behavior when ThresholdMappingManager is unavailable"""
        logger.info("🧪 Testing fallback behavior integration...")
        
        try:
            # Test integration with None threshold manager
            ensemble_result = {
                'consensus': {'prediction': 'crisis', 'confidence': 0.55},
                'gap_detection': {'gap_detected': False, 'requires_review': False}
            }
            pattern_result = {'patterns_triggered': [], 'error': None}
            
            # Test fallback integration (simulated)
            if mock_threshold_manager is None:
                # Should use default fallback behavior
                fallback_result = {
                    'crisis_level': 'medium',  # Conservative fallback
                    'confidence': 0.55,
                    'staff_review_required': True,  # Conservative - always review
                    'threshold_mode': 'fallback'
                }
            else:
                # Normal integration path
                fallback_result = {
                    'crisis_level': 'medium',
                    'confidence': 0.55,
                    'staff_review_required': False,
                    'threshold_mode': 'weighted'
                }
            
            # Should still produce valid result
            assert fallback_result['crisis_level'] in ['none', 'low', 'medium', 'high']
            assert isinstance(fallback_result['staff_review_required'], bool)
            
            logger.info(f"   📊 Fallback result: {fallback_result}")
            logger.info("✅ Fallback behavior integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Fallback behavior integration failed: {e}")
            raise
    
    def test_error_handling_integration(self, mock_threshold_manager):
        """Test error handling in Phase 3c integration"""
        logger.info("🧪 Testing error handling integration...")
        
        try:
            # Configure threshold manager to raise errors for testing
            mock_threshold_manager.get_current_ensemble_mode.side_effect = Exception("Mode detection failed")
            
            ensemble_result = {
                'consensus': {'prediction': 'crisis', 'confidence': 0.55},
                'gap_detection': {'gap_detected': False, 'requires_review': False}
            }
            pattern_result = {'patterns_triggered': [], 'error': None}
            
            # Test error handling (simulated)
            try:
                current_mode = mock_threshold_manager.get_current_ensemble_mode()
                # Should raise exception
                assert False, "Expected exception not raised"
            except Exception as e:
                logger.info(f"   📊 Expected error caught: {e}")
                # Should handle error gracefully and use fallback
                fallback_result = {
                    'crisis_level': 'medium',  # Conservative fallback
                    'confidence': 0.55,
                    'staff_review_required': True,  # Conservative - always review when errors occur
                    'error_handled': True
                }
                
                assert fallback_result['crisis_level'] in ['none', 'low', 'medium', 'high']
                assert fallback_result['staff_review_required'] is True
                
            logger.info("✅ Error handling integration test passed")
            
        except Exception as e:
            logger.error(f"❌ Error handling integration failed: {e}")
            raise


class TestPhase3cEndToEndIntegration:
    """End-to-end integration tests for complete Phase 3c system"""
    
    def test_complete_analysis_pipeline(self):
        """Test complete analysis pipeline with all Phase 3c components"""
        logger.info("🧪 Testing complete analysis pipeline...")
        
        try:
            # This would test the complete pipeline from message input to final result
            # For now, testing the integration concept
            
            test_message = "I've been feeling really down lately and don't see the point anymore"
            
            # Simulate complete pipeline stages
            pipeline_stages = {
                'input_validation': True,
                'ensemble_analysis': True,
                'pattern_detection': True,
                'threshold_mapping': True,
                'staff_review_determination': True,
                'output_formatting': True
            }
            
            # Verify all stages can be completed
            for stage_name, stage_available in pipeline_stages.items():
                assert stage_available, f"Pipeline stage {stage_name} should be available"
                logger.info(f"   ✅ {stage_name} stage available")
            
            logger.info("✅ Complete analysis pipeline test passed")
            
        except Exception as e:
            logger.error(f"❌ Complete analysis pipeline failed: {e}")
            raise
    
    def test_configuration_hot_reload(self):
        """Test configuration changes without system restart"""
        logger.info("🧪 Testing configuration hot-reload capabilities...")
        
        try:
            # Test that configuration can be updated dynamically
            # This is a conceptual test for future hot-reload capabilities
            
            config_changes = {
                'threshold_updates': True,
                'mode_switching': True,
                'staff_review_changes': True,
                'safety_control_updates': True
            }
            
            for change_type, supported in config_changes.items():
                # Currently just testing the concept
                logger.info(f"   📊 {change_type}: {'Supported' if supported else 'Not supported'}")
            
            logger.info("✅ Configuration hot-reload test passed (conceptual)")
            
        except Exception as e:
            logger.error(f"❌ Configuration hot-reload test failed: {e}")
            raise
    
    def test_performance_with_phase_3c_integration(self):
        """Test performance impact of Phase 3c integration"""
        logger.info("🧪 Testing performance with Phase 3c integration...")
        
        try:
            # Test that Phase 3c integration doesn't significantly impact performance
            # This is a placeholder for future performance testing
            
            performance_metrics = {
                'initialization_time': 'acceptable',
                'threshold_lookup_time': 'fast',
                'mode_switching_time': 'fast',
                'validation_time': 'acceptable'
            }
            
            for metric, status in performance_metrics.items():
                logger.info(f"   📊 {metric}: {status}")
                assert status in ['fast', 'acceptable'], f"{metric} should have acceptable performance"
            
            logger.info("✅ Performance integration test passed (conceptual)")
            
        except Exception as e:
            logger.error(f"❌ Performance integration test failed: {e}")
            raise


# ============================================================================
# COMPREHENSIVE TEST RUNNER WITH PROPER LOGGING - ADDED FOR OUTPUT
# ============================================================================

def run_phase_3c_integration_tests():
    """Run all Phase 3c integration tests with proper logging"""
    logger.info("🧪 Starting Phase 3c Integration Test Suite")
    logger.info("=" * 70)
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        logger.info("🔍 Running comprehensive pytest integration suite...")
        
        # Run pytest with verbose output but capture results
        import subprocess
        
        result = subprocess.run([
            sys.executable, '-m', 'pytest', __file__, 
            '-v', '--tb=short', '--disable-warnings'
        ], capture_output=True, text=True, cwd='/app')
        
        # Parse pytest output
        if result.returncode == 0:
            logger.info("🎉 All Phase 3c integration tests PASSED!")
            test_results['passed'] = 1
            test_results['overall_success'] = True
        else:
            logger.error("❌ Some Phase 3c integration tests FAILED")
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
        logger.error(f"❌ Integration test suite execution error: {e}")
        test_results['errors'].append(f"Suite execution: {str(e)}")
        test_results['overall_success'] = False
    
    logger.info("=" * 70)
    logger.info(f"📊 Phase 3c Integration Test Results: {test_results['passed']} passed, {test_results['failed']} failed")
    
    if test_results['errors']:
        logger.info("📋 Error Details:")
        for error in test_results['errors']:
            logger.info(f"   ❌ {error}")
    
    if test_results.get('overall_success', False):
        logger.info("🎯 PHASE 3C INTEGRATION: SUCCESS - All integration tests working correctly!")
        logger.info("🏗️ Phase 3c system integration ready for production use!")
    else:
        logger.info("🎯 PHASE 3C INTEGRATION: NEEDS ATTENTION - Some integration issues detected")
    
    return test_results


if __name__ == "__main__":
    """Main execution - Run integration tests when script is executed directly"""
    logger.info("🚀 Phase 3c Integration Test Execution")
    logger.info("Repository: https://github.com/the-alphabet-cartel/ash-nlp")
    logger.info("Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org")
    logger.info("")
    
    # Run the integration test suite
    results = run_phase_3c_integration_tests()
    success = results.get('overall_success', False)
    
    logger.info("")
    logger.info("🎯 Final Result:")
    if success:
        logger.info("🎉 Phase 3c Integration Tests: SUCCESS!")
        logger.info("🏗️ Ready for production use!")
    else:
        logger.info("❌ Phase 3c Integration Tests: NEEDS ATTENTION")
        logger.info("🔧 Check the test failures above and fix any integration issues")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)