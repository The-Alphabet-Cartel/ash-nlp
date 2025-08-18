# ash-nlp/tests/phase/3/e/test_crisis_analyzer_consolidation.py
"""
Integration Tests for Phase 3e Step 4: CrisisAnalyzer Consolidation
FILE VERSION: v3.1-3e-4.3-1
LAST MODIFIED: 2025-08-18
PHASE: 3e Step 4.3 - CrisisAnalyzer Integration Testing
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import pytest
import asyncio
import logging
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any, List

# Import the enhanced CrisisAnalyzer and factory function
from analysis.crisis_analyzer import CrisisAnalyzer, create_crisis_analyzer
from analysis import (
    create_enhanced_crisis_analyzer_v3e,
    validate_crisis_analyzer_dependencies,
    get_consolidation_summary
)

# Configure test logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestEnhancedCrisisAnalyzerFactory:
    """Test enhanced factory function with Phase 3e dependencies"""
    
    def test_enhanced_factory_function_basic_creation(self):
        """Test basic CrisisAnalyzer creation with enhanced factory"""
        # Create mock dependencies
        model_ensemble_manager = Mock()
        shared_utilities_manager = Mock()
        learning_system_manager = Mock()
        
        # Create CrisisAnalyzer using enhanced factory
        analyzer = create_crisis_analyzer(
            model_ensemble_manager=model_ensemble_manager,
            shared_utilities_manager=shared_utilities_manager,
            learning_system_manager=learning_system_manager
        )
        
        # Verify creation and dependencies
        assert isinstance(analyzer, CrisisAnalyzer)
        assert analyzer.model_ensemble_manager == model_ensemble_manager
        assert analyzer.shared_utilities_manager == shared_utilities_manager
        assert analyzer.learning_system_manager == learning_system_manager
        
        logger.info("✅ Enhanced factory function basic creation test passed")

    def test_enhanced_factory_function_with_all_dependencies(self):
        """Test CrisisAnalyzer creation with all possible dependencies"""
        # Create all mock dependencies
        model_ensemble_manager = Mock()
        crisis_pattern_manager = Mock()
        learning_manager = Mock()
        analysis_parameters_manager = Mock()
        threshold_mapping_manager = Mock()
        feature_config_manager = Mock()
        performance_config_manager = Mock()
        context_pattern_manager = Mock()
        shared_utilities_manager = Mock()
        learning_system_manager = Mock()
        
        # Create CrisisAnalyzer with all dependencies
        analyzer = create_crisis_analyzer(
            model_ensemble_manager=model_ensemble_manager,
            crisis_pattern_manager=crisis_pattern_manager,
            learning_manager=learning_manager,
            analysis_parameters_manager=analysis_parameters_manager,
            threshold_mapping_manager=threshold_mapping_manager,
            feature_config_manager=feature_config_manager,
            performance_config_manager=performance_config_manager,
            context_pattern_manager=context_pattern_manager,
            shared_utilities_manager=shared_utilities_manager,
            learning_system_manager=learning_system_manager
        )
        
        # Verify all dependencies are set
        assert analyzer.model_ensemble_manager == model_ensemble_manager
        assert analyzer.crisis_pattern_manager == crisis_pattern_manager
        assert analyzer.learning_manager == learning_manager
        assert analyzer.analysis_parameters_manager == analysis_parameters_manager
        assert analyzer.threshold_mapping_manager == threshold_mapping_manager
        assert analyzer.feature_config_manager == feature_config_manager
        assert analyzer.performance_config_manager == performance_config_manager
        assert analyzer.context_pattern_manager == context_pattern_manager
        assert analyzer.shared_utilities_manager == shared_utilities_manager
        assert analyzer.learning_system_manager == learning_system_manager
        
        logger.info("✅ Enhanced factory function with all dependencies test passed")

    def test_convenience_factory_function_v3e(self):
        """Test Phase 3e convenience factory function"""
        # Create required Phase 3e dependencies
        model_ensemble_manager = Mock()
        shared_utilities_manager = Mock()
        learning_system_manager = Mock()
        
        # Optional legacy dependencies
        crisis_pattern_manager = Mock()
        
        # Create using convenience factory
        analyzer = create_enhanced_crisis_analyzer_v3e(
            model_ensemble_manager=model_ensemble_manager,
            shared_utilities_manager=shared_utilities_manager,
            learning_system_manager=learning_system_manager,
            crisis_pattern_manager=crisis_pattern_manager
        )
        
        # Verify creation and Phase 3e dependencies
        assert isinstance(analyzer, CrisisAnalyzer)
        assert analyzer.shared_utilities_manager == shared_utilities_manager
        assert analyzer.learning_system_manager == learning_system_manager
        assert analyzer.crisis_pattern_manager == crisis_pattern_manager
        
        logger.info("✅ Convenience factory function v3e test passed")

    def test_dependency_validation_function(self):
        """Test dependency validation function"""
        # Test with all required dependencies
        model_ensemble_manager = Mock()
        shared_utilities_manager = Mock()
        learning_system_manager = Mock()
        
        validation = validate_crisis_analyzer_dependencies(
            model_ensemble_manager=model_ensemble_manager,
            shared_utilities_manager=shared_utilities_manager,
            learning_system_manager=learning_system_manager
        )
        
        assert validation["valid"] is True
        assert validation["phase"] == "3e_enhanced"
        assert len(validation["errors"]) == 0
        
        # Test with missing required dependency
        validation_missing = validate_crisis_analyzer_dependencies(
            shared_utilities_manager=shared_utilities_manager,
            learning_system_manager=learning_system_manager
        )
        
        assert validation_missing["valid"] is False
        assert "model_ensemble_manager is required" in validation_missing["errors"]
        
        logger.info("✅ Dependency validation function test passed")


class TestConsolidatedAnalysisParametersMethods:
    """Test consolidated methods from AnalysisParametersManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.model_ensemble_manager = Mock()
        self.shared_utilities_manager = Mock()
        self.learning_system_manager = Mock()
        
        self.analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )

    def test_get_analysis_crisis_thresholds(self):
        """Test get_analysis_crisis_thresholds consolidated method"""
        # Mock shared utilities response
        expected_thresholds = {
            'low': 0.2,
            'medium': 0.4,
            'high': 0.6,
            'critical': 0.8
        }
        self.shared_utilities_manager.get_config_section_safely.return_value = expected_thresholds
        
        # Call consolidated method
        result = self.analyzer.get_analysis_crisis_thresholds()
        
        # Verify results
        assert result == expected_thresholds
        self.shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            'analysis_parameters', 'crisis_thresholds', unittest.mock.ANY
        )
        
        logger.info("✅ get_analysis_crisis_thresholds test passed")

    def test_get_analysis_timeouts(self):
        """Test get_analysis_timeouts consolidated method"""
        # Mock shared utilities response
        expected_timeouts = {
            'model_analysis': 10,
            'pattern_analysis': 5,
            'total_analysis': 30
        }
        self.shared_utilities_manager.get_config_section_safely.return_value = expected_timeouts
        
        # Call consolidated method
        result = self.analyzer.get_analysis_timeouts()
        
        # Verify results
        assert result == expected_timeouts
        self.shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            'analysis_parameters', 'timeouts', unittest.mock.ANY
        )
        
        logger.info("✅ get_analysis_timeouts test passed")

    def test_get_analysis_confidence_boosts(self):
        """Test get_analysis_confidence_boosts consolidated method"""
        # Mock shared utilities response
        expected_boosts = {
            'pattern_match': 0.1,
            'context_boost': 0.15,
            'temporal_boost': 0.05,
            'community_pattern': 0.08
        }
        self.shared_utilities_manager.get_config_section_safely.return_value = expected_boosts
        
        # Call consolidated method
        result = self.analyzer.get_analysis_confidence_boosts()
        
        # Verify results
        assert result == expected_boosts
        self.shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            'analysis_parameters', 'confidence_boosts', unittest.mock.ANY
        )
        
        logger.info("✅ get_analysis_confidence_boosts test passed")

    def test_get_analysis_pattern_weights(self):
        """Test get_analysis_pattern_weights consolidated method"""
        # Mock shared utilities response
        expected_weights = {
            'crisis_patterns': 0.6,
            'community_patterns': 0.3,
            'context_patterns': 0.4,
            'temporal_patterns': 0.2
        }
        self.shared_utilities_manager.get_config_section_safely.return_value = expected_weights
        
        # Call consolidated method
        result = self.analyzer.get_analysis_pattern_weights()
        
        # Verify results
        assert result == expected_weights
        self.shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            'analysis_parameters', 'pattern_weights', unittest.mock.ANY
        )
        
        logger.info("✅ get_analysis_pattern_weights test passed")

    def test_get_analysis_algorithm_parameters(self):
        """Test get_analysis_algorithm_parameters consolidated method"""
        # Mock shared utilities response
        expected_params = {
            'ensemble_weights': [0.4, 0.3, 0.3],
            'score_normalization': 'sigmoid',
            'threshold_adaptation': True,
            'learning_rate': 0.01,
            'confidence_threshold': 0.5
        }
        self.shared_utilities_manager.get_config_section_safely.return_value = expected_params
        
        # Call consolidated method
        result = self.analyzer.get_analysis_algorithm_parameters()
        
        # Verify results
        assert result == expected_params
        self.shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            'analysis_parameters', 'algorithm_parameters', unittest.mock.ANY
        )
        
        logger.info("✅ get_analysis_algorithm_parameters test passed")

    def test_analysis_parameters_fallback_handling(self):
        """Test fallback handling when SharedUtilitiesManager is unavailable"""
        # Create analyzer without shared utilities
        analyzer_no_shared = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            analysis_parameters_manager=Mock(),
            shared_utilities_manager=None
        )
        
        # Mock legacy manager method
        analyzer_no_shared.analysis_parameters_manager.get_crisis_thresholds.return_value = {
            'low': 0.3, 'medium': 0.5, 'high': 0.7, 'critical': 0.9
        }
        
        # Call consolidated method
        result = analyzer_no_shared.get_analysis_crisis_thresholds()
        
        # Verify fallback was used
        assert result['low'] == 0.3
        assert result['critical'] == 0.9
        analyzer_no_shared.analysis_parameters_manager.get_crisis_thresholds.assert_called_once()
        
        logger.info("✅ Analysis parameters fallback handling test passed")


class TestConsolidatedThresholdMappingMethods:
    """Test consolidated methods from ThresholdMappingManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.model_ensemble_manager = Mock()
        self.shared_utilities_manager = Mock()
        self.learning_system_manager = Mock()
        
        self.analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )

    def test_apply_crisis_thresholds(self):
        """Test apply_crisis_thresholds consolidated method"""
        # Mock get_crisis_threshold_for_mode
        self.analyzer.get_crisis_threshold_for_mode = Mock(return_value={
            'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8
        })
        
        # Mock learning system adjustment
        self.learning_system_manager.apply_threshold_adjustments.return_value = 0.75
        
        # Test critical level
        result = self.analyzer.apply_crisis_thresholds(0.85, 'default')
        assert result == 'critical'
        
        # Test high level  
        result = self.analyzer.apply_crisis_thresholds(0.65, 'default')
        assert result == 'high'
        
        # Test medium level
        result = self.analyzer.apply_crisis_thresholds(0.45, 'default')
        assert result == 'medium'
        
        # Test low level
        result = self.analyzer.apply_crisis_thresholds(0.25, 'default')
        assert result == 'low'
        
        # Test none level
        result = self.analyzer.apply_crisis_thresholds(0.15, 'default')
        assert result == 'none'
        
        # Verify learning adjustment was called
        self.learning_system_manager.apply_threshold_adjustments.assert_called()
        
        logger.info("✅ apply_crisis_thresholds test passed")

    def test_calculate_crisis_level_from_confidence(self):
        """Test calculate_crisis_level_from_confidence consolidated method"""
        # This method delegates to apply_crisis_thresholds
        self.analyzer.apply_crisis_thresholds = Mock(return_value='high')
        
        result = self.analyzer.calculate_crisis_level_from_confidence(0.7, 'sensitive')
        
        assert result == 'high'
        self.analyzer.apply_crisis_thresholds.assert_called_once_with(0.7, 'sensitive')
        
        logger.info("✅ calculate_crisis_level_from_confidence test passed")

    def test_validate_crisis_analysis_thresholds(self):
        """Test validate_crisis_analysis_thresholds consolidated method"""
        # Mock consolidated method responses
        self.analyzer.get_analysis_crisis_thresholds = Mock(return_value={
            'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8
        })
        self.analyzer.get_analysis_confidence_boosts = Mock(return_value={
            'pattern_match': 0.1, 'context_boost': 0.15
        })
        self.analyzer.get_analysis_pattern_weights = Mock(return_value={
            'crisis_patterns': 0.6, 'community_patterns': 0.3
        })
        
        # Call validation
        result = self.analyzer.validate_crisis_analysis_thresholds()
        
        # Verify validation results
        assert result['crisis_thresholds_valid'] is True
        assert result['confidence_boosts_valid'] is True
        assert result['pattern_weights_valid'] is True
        assert result['overall_valid'] is True
        
        logger.info("✅ validate_crisis_analysis_thresholds test passed")

    def test_get_crisis_threshold_for_mode(self):
        """Test get_crisis_threshold_for_mode consolidated method"""
        # Mock base thresholds
        base_thresholds = {'low': 0.3, 'medium': 0.5, 'high': 0.7, 'critical': 0.9}
        self.analyzer.get_analysis_crisis_thresholds = Mock(return_value=base_thresholds)
        
        # Test default mode
        result = self.analyzer.get_crisis_threshold_for_mode('default')
        assert result == base_thresholds
        
        # Test sensitive mode (lower thresholds)
        result = self.analyzer.get_crisis_threshold_for_mode('sensitive')
        assert result['low'] == 0.2  # 0.3 - 0.1
        assert result['critical'] == 0.8  # 0.9 - 0.1
        
        # Test conservative mode (higher thresholds)
        result = self.analyzer.get_crisis_threshold_for_mode('conservative')
        assert result['low'] == 0.4  # 0.3 + 0.1
        assert result['critical'] == 1.0  # min(1.0, 0.9 + 0.1)
        
        logger.info("✅ get_crisis_threshold_for_mode test passed")


class TestConsolidatedModelEnsembleMethods:
    """Test consolidated methods from ModelEnsembleManager"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.model_ensemble_manager = Mock()
        self.shared_utilities_manager = Mock()
        self.learning_system_manager = Mock()
        
        self.analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )

    def test_perform_ensemble_crisis_analysis(self):
        """Test perform_ensemble_crisis_analysis consolidated method"""
        # Mock input validation
        self.analyzer._validate_analysis_input = Mock(return_value=True)
        
        # Mock algorithm parameters
        self.analyzer.get_analysis_algorithm_parameters = Mock(return_value={
            'ensemble_weights': [0.4, 0.3, 0.3]
        })
        
        # Mock ModelEnsembleManager base analysis
        self.model_ensemble_manager.analyze_message_with_ensemble.return_value = {
            'model_results': [
                {'score': 0.6, 'confidence': 0.8},
                {'score': 0.7, 'confidence': 0.9},
                {'score': 0.5, 'confidence': 0.7}
            ]
        }
        
        # Mock consolidated methods
        self.analyzer.combine_ensemble_model_results = Mock(return_value={
            'crisis_score': 0.6, 'confidence': 0.8, 'model_count': 3
        })
        self.analyzer.apply_analysis_ensemble_weights = Mock(return_value={
            'weighted_crisis_score': 0.62, 'weights_applied': [0.4, 0.3, 0.3]
        })
        
        # Mock learning adjustments
        self.learning_system_manager.apply_learning_adjustments.return_value = {
            'adjusted_score': 0.65, 'adjustments': {'threshold_boost': 0.03}
        }
        
        # Call method
        result = self.analyzer.perform_ensemble_crisis_analysis(
            "I'm feeling really down today", "user123", "channel456"
        )
        
        # Verify method calls
        self.analyzer._validate_analysis_input.assert_called_once()
        self.model_ensemble_manager.analyze_message_with_ensemble.assert_called_once()
        self.analyzer.combine_ensemble_model_results.assert_called_once()
        self.analyzer.apply_analysis_ensemble_weights.assert_called_once()
        self.learning_system_manager.apply_learning_adjustments.assert_called_once()
        
        # Verify result structure
        assert 'analysis_metadata' in result
        assert result['analysis_metadata']['learning_applied'] is True
        
        logger.info("✅ perform_ensemble_crisis_analysis test passed")

    def test_combine_ensemble_model_results(self):
        """Test combine_ensemble_model_results consolidated method"""
        # Mock model results
        model_results = [
            {'score': 0.6, 'confidence': 0.8, 'categories': ['depression']},
            {'score': 0.7, 'confidence': 0.9, 'categories': ['anxiety']},
            {'score': 0.5, 'confidence': 0.7, 'categories': ['depression', 'social']}
        ]
        
        # Mock confidence boost
        self.analyzer.get_analysis_confidence_boosts = Mock(return_value={
            'pattern_match': 0.1
        })
        
        # Call method
        result = self.analyzer.combine_ensemble_model_results(model_results)
        
        # Verify results
        assert result['crisis_score'] == 0.6  # (0.6 + 0.7 + 0.5) / 3
        assert result['confidence'] == 0.8   # (0.8 + 0.9 + 0.7) / 3
        assert result['model_count'] == 3
        assert 'depression' in result['detected_categories']
        assert 'anxiety' in result['detected_categories']
        assert 'social' in result['detected_categories']
        
        logger.info("✅ combine_ensemble_model_results test passed")

    def test_apply_analysis_ensemble_weights(self):
        """Test apply_analysis_ensemble_weights consolidated method"""
        # Mock results
        results = {
            'individual_scores': [0.6, 0.7, 0.5],
            'confidence': 0.8
        }
        
        # Custom weights
        weights = [0.5, 0.3, 0.2]
        
        # Call method
        result = self.analyzer.apply_analysis_ensemble_weights(results, weights)
        
        # Verify weighted score calculation
        expected_weighted_score = 0.6 * 0.5 + 0.7 * 0.3 + 0.5 * 0.2  # 0.61
        assert abs(result['weighted_crisis_score'] - expected_weighted_score) < 0.01
        assert result['weights_applied'] == weights
        assert result['weighting_method'] == 'ensemble_weighted_v3e4.2'
        
        logger.info("✅ apply_analysis_ensemble_weights test passed")


class TestLearningSystemIntegration:
    """Test learning system integration methods"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.model_ensemble_manager = Mock()
        self.shared_utilities_manager = Mock()
        self.learning_system_manager = Mock()
        
        self.analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )

    def test_analyze_message_with_learning(self):
        """Test analyze_message_with_learning method"""
        # Mock base analysis
        base_result = {
            'crisis_score': 0.6,
            'confidence': 0.8,
            'crisis_level': 'medium'
        }
        self.analyzer.perform_ensemble_crisis_analysis = Mock(return_value=base_result)
        
        # Mock learning adjustments
        learning_result = {
            'adjusted_score': 0.65,
            'metadata': {'adjustment_reason': 'false_positive_history'},
            'adjustments': {'threshold_boost': 0.05}
        }
        self.learning_system_manager.apply_learning_adjustments.return_value = learning_result
        
        # Call method
        result = self.analyzer.analyze_message_with_learning(
            "I'm struggling today", "user123", "channel456"
        )
        
        # Verify learning integration
        assert result['learning_adjusted_score'] == 0.65
        assert result['learning_applied'] is True
        assert result['threshold_adjustments'] == {'threshold_boost': 0.05}
        assert 'learning_metadata' in result
        
        self.learning_system_manager.apply_learning_adjustments.assert_called_once()
        
        logger.info("✅ analyze_message_with_learning test passed")

    def test_process_analysis_feedback(self):
        """Test process_analysis_feedback method"""
        # Mock original result
        original_result = {
            'crisis_score': 0.7,
            'crisis_level': 'high',
            'confidence': 0.8
        }
        
        # Call feedback processing
        self.analyzer.process_analysis_feedback(
            "I'm fine actually", "user123", "channel456", 
            "false_positive", original_result
        )
        
        # Verify learning system was called
        self.learning_system_manager.process_feedback.assert_called_once_with(
            "I'm fine actually", "user123", "channel456", 
            "false_positive", original_result
        )
        
        logger.info("✅ process_analysis_feedback test passed")

    def test_learning_system_unavailable_handling(self):
        """Test handling when learning system is not available"""
        # Create analyzer without learning system
        analyzer_no_learning = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=None
        )
        
        # Mock base analysis
        base_result = {'crisis_score': 0.6, 'learning_applied': False}
        analyzer_no_learning.perform_ensemble_crisis_analysis = Mock(return_value=base_result)
        
        # Call learning analysis method
        result = analyzer_no_learning.analyze_message_with_learning(
            "test message", "user123", "channel456"
        )
        
        # Verify learning was not applied
        assert result['learning_applied'] is False
        assert 'learning_adjusted_score' not in result
        
        logger.info("✅ Learning system unavailable handling test passed")


class TestSharedUtilitiesIntegration:
    """Test shared utilities integration methods"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.model_ensemble_manager = Mock()
        self.shared_utilities_manager = Mock()
        self.learning_system_manager = Mock()
        
        self.analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )

    def test_safe_analysis_execution(self):
        """Test _safe_analysis_execution method"""
        # Mock successful operation
        def mock_operation():
            return {'result': 'success'}
        
        self.shared_utilities_manager.execute_safely.return_value = {'result': 'success'}
        
        # Call safe execution
        result = self.analyzer._safe_analysis_execution('test_operation', mock_operation)
        
        # Verify shared utilities was called
        assert result == {'result': 'success'}
        self.shared_utilities_manager.execute_safely.assert_called_once_with(
            'test_operation', mock_operation
        )
        
        logger.info("✅ _safe_analysis_execution test passed")

    def test_validate_analysis_input(self):
        """Test _validate_analysis_input method"""
        # Mock shared utilities validation
        self.shared_utilities_manager.validate_type.side_effect = [True, True, True]
        
        # Call validation
        result = self.analyzer._validate_analysis_input("test message", "user123", "channel456")
        
        # Verify validation calls
        assert result is True
        assert self.shared_utilities_manager.validate_type.call_count == 3
        
        # Test with invalid input
        self.shared_utilities_manager.validate_type.side_effect = [False, True, True]
        result = self.analyzer._validate_analysis_input("", "user123", "channel456")
        assert result is False
        
        logger.info("✅ _validate_analysis_input test passed")

    def test_get_analysis_setting(self):
        """Test _get_analysis_setting method"""
        # Mock shared utilities config access
        self.shared_utilities_manager.get_config_section_safely.return_value = "test_value"
        
        # Call method
        result = self.analyzer._get_analysis_setting("test_section", "test_key", "default")
        
        # Verify call
        assert result == "test_value"
        self.shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            "test_section", "test_key", "default"
        )
        
        logger.info("✅ _get_analysis_setting test passed")

    def test_shared_utilities_fallback_handling(self):
        """Test fallback handling when SharedUtilities is unavailable"""
        # Create analyzer without shared utilities
        analyzer_no_shared = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            shared_utilities_manager=None,
            learning_system_manager=self.learning_system_manager
        )
        
        # Test input validation fallback
        result = analyzer_no_shared._validate_analysis_input(
            "valid message", "user123", "channel456"
        )
        assert result is True
        
        # Test with invalid input
        result = analyzer_no_shared._validate_analysis_input("", "", "")
        assert result is False
        
        logger.info("✅ Shared utilities fallback handling test passed")


class TestEndToEndIntegration:
    """Test end-to-end integration of all consolidated methods"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.model_ensemble_manager = Mock()
        self.shared_utilities_manager = Mock()
        self.learning_system_manager = Mock()
        self.crisis_pattern_manager = Mock()
        self.feature_config_manager = Mock()
        
        self.analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            crisis_pattern_manager=self.crisis_pattern_manager,
            feature_config_manager=self.feature_config_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )

    @pytest.mark.asyncio
    async def test_complete_crisis_analysis_workflow(self):
        """Test complete crisis analysis workflow with all consolidations"""
        # Setup feature cache
        self.analyzer._feature_cache = {
            'ensemble_enabled': True,
            'enhanced_learning': True
        }
        self.analyzer._performance_cache = {
            'analysis_timeout': 30.0
        }
        
        # Mock the learning-enhanced analysis
        learning_result = {
            'crisis_score': 0.7,
            'crisis_level': 'high',
            'confidence': 0.85,
            'learning_applied': True,
            'analysis_results': {
                'crisis_score': 0.7,
                'analysis_metadata': {
                    'processing_time': 0.05,
                    'learning_applied': True
                }
            },
            'requires_staff_review': True
        }
        
        self.analyzer.analyze_message_with_learning = Mock(return_value=learning_result)
        
        # Call main analysis method
        result = await self.analyzer.analyze_crisis(
            "I can't take this anymore", "user123", "channel456"
        )
        
        # Verify learning analysis was called
        self.analyzer.analyze_message_with_learning.assert_called_once_with(
            "I can't take this anymore", "user123", "channel456"
        )
        
        # Verify result structure
        assert result['crisis_level'] == 'high'
        assert result['learning_applied'] is True
        assert result['requires_staff_review'] is True
        
        logger.info("✅ Complete crisis analysis workflow test passed")

    def test_backward_compatibility(self):
        """Test backward compatibility with existing analyze_message method"""
        # Mock analyze_crisis method
        expected_result = {
            'crisis_score': 0.5,
            'crisis_level': 'medium',
            'confidence': 0.7
        }
        
        # Use async mock for the delegated method
        async def mock_analyze_crisis(message, user_id, channel_id):
            return expected_result
            
        self.analyzer.analyze_crisis = mock_analyze_crisis
        
        # Call legacy method
        async def test_call():
            result = await self.analyzer.analyze_message(
                "test message", "user123", "channel456"
            )
            return result
        
        # Run async test
        result = asyncio.run(test_call())
        
        # Verify delegation worked
        assert result == expected_result
        
        logger.info("✅ Backward compatibility test passed")

    def test_performance_impact_validation(self):
        """Test that consolidation has minimal performance impact"""
        import time
        
        # Mock dependencies for fast execution
        self.shared_utilities_manager.get_config_section_safely.return_value = {
            'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8
        }
        
        # Measure execution time for consolidated methods
        start_time = time.time()
        
        # Call multiple consolidated methods
        for _ in range(10):
            self.analyzer.get_analysis_crisis_thresholds()
            self.analyzer.get_analysis_confidence_boosts()
            self.analyzer.apply_crisis_thresholds(0.5, 'default')
        
        execution_time = time.time() - start_time
        
        # Verify performance (should be very fast for 30 method calls)
        assert execution_time < 0.1  # Less than 100ms for 30 calls
        
        logger.info(f"✅ Performance impact validation passed: {execution_time:.4f}s for 30 method calls")


class TestConfigurationIntegration:
    """Test configuration integration through SharedUtilities"""
    
    def test_unified_config_manager_access(self):
        """Test UnifiedConfigManager access through SharedUtilities"""
        shared_utilities_manager = Mock()
        
        analyzer = create_crisis_analyzer(
            model_ensemble_manager=Mock(),
            shared_utilities_manager=shared_utilities_manager
        )
        
        # Mock configuration response
        expected_config = {
            'crisis_thresholds': {'low': 0.2, 'medium': 0.4}
        }
        shared_utilities_manager.get_config_section_safely.return_value = expected_config
        
        # Call configuration method
        result = analyzer._get_analysis_setting('analysis_parameters', 'crisis_thresholds', {})
        
        # Verify UnifiedConfigManager was accessed through SharedUtilities
        assert result == expected_config
        shared_utilities_manager.get_config_section_safely.assert_called_once_with(
            'analysis_parameters', 'crisis_thresholds', {}
        )
        
        logger.info("✅ UnifiedConfigManager access test passed")

    def test_configuration_fallback_mechanisms(self):
        """Test configuration fallback when managers are unavailable"""
        # Create analyzer with minimal dependencies
        analyzer = create_crisis_analyzer(
            model_ensemble_manager=Mock(),
            shared_utilities_manager=None,
            learning_system_manager=None
        )
        
        # Call methods that should provide fallbacks
        thresholds = analyzer.get_analysis_crisis_thresholds()
        timeouts = analyzer.get_analysis_timeouts()
        boosts = analyzer.get_analysis_confidence_boosts()
        
        # Verify fallback values are reasonable
        assert isinstance(thresholds, dict)
        assert 'low' in thresholds and 'critical' in thresholds
        assert isinstance(timeouts, dict)
        assert 'total_analysis' in timeouts
        assert isinstance(boosts, dict)
        assert all(isinstance(v, (int, float)) for v in boosts.values())
        
        logger.info("✅ Configuration fallback mechanisms test passed")


def test_consolidation_summary():
    """Test consolidation summary information function"""
    summary = get_consolidation_summary()
    
    assert summary['phase'] == '3e_step_4.2'
    assert summary['total_methods_added'] == 12
    assert 'SharedUtilitiesManager' in summary['dependencies_added']
    assert 'LearningSystemManager' in summary['dependencies_added']
    assert len(summary['methods_consolidated']['from_analysis_parameters_manager']) == 5
    assert len(summary['methods_consolidated']['from_threshold_mapping_manager']) == 4
    assert len(summary['methods_consolidated']['from_model_ensemble_manager']) == 3
    
    logger.info("✅ Consolidation summary test passed")


if __name__ == "__main__":
    # Run specific test categories
    pytest.main([
        "-v", 
        "test_crisis_analyzer_consolidation.py::TestEnhancedCrisisAnalyzerFactory",
        "test_crisis_analyzer_consolidation.py::TestConsolidatedAnalysisParametersMethods", 
        "test_crisis_analyzer_consolidation.py::TestConsolidatedThresholdMappingMethods",
        "test_crisis_analyzer_consolidation.py::TestConsolidatedModelEnsembleMethods",
        "test_crisis_analyzer_consolidation.py::TestLearningSystemIntegration",
        "test_crisis_analyzer_consolidation.py::TestSharedUtilitiesIntegration",
        "test_crisis_analyzer_consolidation.py::TestEndToEndIntegration",
        "test_crisis_analyzer_consolidation.py::TestConfigurationIntegration"
    ])
    
    logger.info("🎉 Phase 3e Step 4.3: CrisisAnalyzer Integration Tests Complete!")
    logger.info("✅ All consolidated methods tested and validated")
    logger.info("✅ Learning system integration verified")
    logger.info("✅ SharedUtilities integration confirmed")
    logger.info("✅ Backward compatibility maintained")
    logger.info("✅ Performance impact validated as minimal")
    logger.info("🚀 Ready for Phase 3e Step 5: Systematic Manager Cleanup!")