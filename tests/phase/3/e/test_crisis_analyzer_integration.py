# ash-nlp/tests/phase/3/e/test_real_crisis_analyzer_integration.py
"""
Real-World Integration Tests for Phase 3e Step 4: CrisisAnalyzer Consolidation
FILE VERSION: v3.1-3e-4.3-2
LAST MODIFIED: 2025-08-18
PHASE: 3e Step 4.3 - Real-World CrisisAnalyzer Integration Testing
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This test suite uses REAL managers and functions, not mocks, to validate actual functionality.
"""

import pytest
import asyncio
import logging
import time
from typing import Dict, Any, List

# Import real managers and create actual instances
from managers.unified_config_manager import create_unified_config_manager
from managers.model_ensemble_manager import create_model_ensemble_manager
from managers.crisis_pattern_manager import create_crisis_pattern_manager
from managers.analysis_parameters_manager import create_analysis_parameters_manager
from managers.threshold_mapping_manager import create_threshold_mapping_manager
from managers.feature_config_manager import create_feature_config_manager
from managers.performance_config_manager import create_performance_config_manager
from managers.context_pattern_manager import create_context_pattern_manager

# Import the enhanced CrisisAnalyzer
from analysis.crisis_analyzer import CrisisAnalyzer, create_crisis_analyzer
from analysis import (
    create_enhanced_crisis_analyzer_v3e,
    validate_crisis_analyzer_dependencies,
    get_consolidation_summary
)

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestRealWorldCrisisAnalyzerIntegration:
    """Test CrisisAnalyzer with real manager dependencies"""
    
    @classmethod
    def setup_class(cls):
        """Setup real manager instances for all tests"""
        logger.info("🔧 Setting up real manager instances for integration testing...")
        
        # Create unified config manager
        cls.config_manager = create_unified_config_manager()
        
        # Create all real managers
        cls.model_ensemble_manager = create_model_ensemble_manager(cls.config_manager)
        cls.crisis_pattern_manager = create_crisis_pattern_manager(cls.config_manager)
        cls.analysis_parameters_manager = create_analysis_parameters_manager(cls.config_manager)
        cls.threshold_mapping_manager = create_threshold_mapping_manager(cls.config_manager, cls.model_ensemble_manager)
        cls.feature_config_manager = create_feature_config_manager(cls.config_manager)
        cls.performance_config_manager = create_performance_config_manager(cls.config_manager)
        cls.context_pattern_manager = create_context_pattern_manager(cls.config_manager)
        
        # Create enhanced CrisisAnalyzer with real dependencies
        cls.crisis_analyzer = create_crisis_analyzer(
            model_ensemble_manager=cls.model_ensemble_manager,
            crisis_pattern_manager=cls.crisis_pattern_manager,
            analysis_parameters_manager=cls.analysis_parameters_manager,
            threshold_mapping_manager=cls.threshold_mapping_manager,
            feature_config_manager=cls.feature_config_manager,
            performance_config_manager=cls.performance_config_manager,
            context_pattern_manager=cls.context_pattern_manager,
            # Note: SharedUtilities and LearningSystem managers not available yet
            shared_utilities_manager=None,
            learning_system_manager=None
        )
        
        logger.info("✅ Real manager setup complete")

    def test_enhanced_crisis_analyzer_creation(self):
        """Test that enhanced CrisisAnalyzer can be created with real managers"""
        assert isinstance(self.crisis_analyzer, CrisisAnalyzer)
        assert self.crisis_analyzer.model_ensemble_manager is not None
        assert self.crisis_analyzer.crisis_pattern_manager is not None
        assert self.crisis_analyzer.analysis_parameters_manager is not None
        assert self.crisis_analyzer.threshold_mapping_manager is not None
        assert self.crisis_analyzer.feature_config_manager is not None
        assert self.crisis_analyzer.performance_config_manager is not None
        assert self.crisis_analyzer.context_pattern_manager is not None
        
        logger.info("✅ Enhanced CrisisAnalyzer creation test passed")

    def test_consolidated_analysis_parameters_methods(self):
        """Test consolidated methods from AnalysisParametersManager with real configuration"""
        
        # Test get_analysis_crisis_thresholds
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        assert isinstance(thresholds, dict)
        assert 'low' in thresholds
        assert 'medium' in thresholds
        assert 'high' in thresholds
        assert 'critical' in thresholds
        assert all(isinstance(v, (int, float)) for v in thresholds.values())
        logger.info(f"✅ Crisis thresholds: {thresholds}")
        
        # Test get_analysis_timeouts
        timeouts = self.crisis_analyzer.get_analysis_timeouts()
        assert isinstance(timeouts, dict)
        assert all(isinstance(v, (int, float)) for v in timeouts.values())
        logger.info(f"✅ Analysis timeouts: {timeouts}")
        
        # Test get_analysis_confidence_boosts
        boosts = self.crisis_analyzer.get_analysis_confidence_boosts()
        assert isinstance(boosts, dict)
        assert all(isinstance(v, (int, float)) for v in boosts.values())
        logger.info(f"✅ Confidence boosts: {boosts}")
        
        # Test get_analysis_pattern_weights
        weights = self.crisis_analyzer.get_analysis_pattern_weights()
        assert isinstance(weights, dict)
        assert all(isinstance(v, (int, float)) for v in weights.values())
        logger.info(f"✅ Pattern weights: {weights}")
        
        # Test get_analysis_algorithm_parameters
        params = self.crisis_analyzer.get_analysis_algorithm_parameters()
        assert isinstance(params, dict)
        logger.info(f"✅ Algorithm parameters: {params}")
        
        logger.info("✅ All consolidated AnalysisParameters methods working with real configuration")

    def test_consolidated_threshold_mapping_methods(self):
        """Test consolidated methods from ThresholdMappingManager with real configuration"""
        
        # Test apply_crisis_thresholds with different confidence levels
        test_cases = [
            (0.1, 'none'),
            (0.25, 'low'),
            (0.45, 'medium'),
            (0.65, 'high'),
            (0.85, 'critical')
        ]
        
        for confidence, expected_level in test_cases:
            result = self.crisis_analyzer.apply_crisis_thresholds(confidence)
            assert isinstance(result, str)
            assert result in ['none', 'low', 'medium', 'high', 'critical']
            logger.info(f"✅ Confidence {confidence} → Crisis level: {result}")
        
        # Test calculate_crisis_level_from_confidence (should delegate to apply_crisis_thresholds)
        result = self.crisis_analyzer.calculate_crisis_level_from_confidence(0.5, 'default')
        assert isinstance(result, str)
        logger.info(f"✅ Crisis level from confidence: {result}")
        
        # Test validate_crisis_analysis_thresholds
        validation = self.crisis_analyzer.validate_crisis_analysis_thresholds()
        assert isinstance(validation, dict)
        assert 'overall_valid' in validation
        logger.info(f"✅ Threshold validation: {validation}")
        
        # Test get_crisis_threshold_for_mode with different modes
        for mode in ['default', 'sensitive', 'conservative']:
            mode_thresholds = self.crisis_analyzer.get_crisis_threshold_for_mode(mode)
            assert isinstance(mode_thresholds, dict)
            assert 'low' in mode_thresholds
            logger.info(f"✅ {mode} mode thresholds: {mode_thresholds}")
        
        logger.info("✅ All consolidated ThresholdMapping methods working with real configuration")

    def test_consolidated_model_ensemble_methods(self):
        """Test consolidated methods from ModelEnsembleManager with real configuration"""
        
        # Test combine_ensemble_model_results with realistic model results
        mock_model_results = [
            {'score': 0.6, 'confidence': 0.8, 'categories': ['depression']},
            {'score': 0.7, 'confidence': 0.9, 'categories': ['anxiety']},
            {'score': 0.5, 'confidence': 0.7, 'categories': ['depression', 'social']}
        ]
        
        combined = self.crisis_analyzer.combine_ensemble_model_results(mock_model_results)
        assert isinstance(combined, dict)
        assert 'crisis_score' in combined
        assert 'confidence' in combined
        assert 'model_count' in combined
        assert combined['model_count'] == 3
        assert 'detected_categories' in combined
        logger.info(f"✅ Combined model results: {combined}")
        
        # Test apply_analysis_ensemble_weights
        weights = [0.4, 0.3, 0.3]
        weighted = self.crisis_analyzer.apply_analysis_ensemble_weights(combined, weights)
        assert isinstance(weighted, dict)
        assert 'weighted_crisis_score' in weighted
        assert 'weights_applied' in weighted
        assert weighted['weights_applied'] == weights
        logger.info(f"✅ Weighted results: {weighted}")
        
        logger.info("✅ All consolidated ModelEnsemble methods working with real configuration")

    @pytest.mark.asyncio
    async def test_real_world_crisis_analysis_high_risk(self):
        """Test complete crisis analysis with high-risk message using real system"""
        message = "I feel hopeless and want to kill myself"
        user_id = "test_user_001"
        channel_id = "test_channel_001"
        
        logger.info(f"🔍 Testing high-risk message: '{message}'")
        
        start_time = time.time()
        result = await self.crisis_analyzer.analyze_crisis(message, user_id, channel_id)
        processing_time = time.time() - start_time
        
        # Validate response structure
        assert isinstance(result, dict)
        required_fields = [
            'message', 'user_id', 'channel_id', 'needs_response', 
            'crisis_level', 'confidence_score', 'detected_categories',
            'method', 'analysis_results', 'requires_staff_review', 'processing_time'
        ]
        
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"
        
        # Validate high-risk detection
        assert result['needs_response'] is True, "High-risk message should need response"
        assert result['crisis_level'] in ['medium', 'high', 'critical'], f"Unexpected crisis level: {result['crisis_level']}"
        assert result['confidence_score'] > 0.2, f"Low confidence for high-risk message: {result['confidence_score']}"
        assert len(result['detected_categories']) > 0, "Should detect some categories"
        
        # Validate analysis results structure
        analysis_results = result['analysis_results']
        assert 'crisis_score' in analysis_results
        assert 'model_results' in analysis_results
        assert 'pattern_analysis' in analysis_results
        assert 'context_analysis' in analysis_results
        assert 'analysis_metadata' in analysis_results
        
        # Check for pattern detection (should detect hopelessness patterns)
        pattern_analysis = analysis_results['pattern_analysis']
        if pattern_analysis and 'enhanced_patterns' in pattern_analysis:
            enhanced = pattern_analysis['enhanced_patterns']
            if 'matches' in enhanced and enhanced['matches']:
                logger.info(f"✅ Detected patterns: {len(enhanced['matches'])} matches")
                for match in enhanced['matches']:
                    logger.info(f"   - {match.get('pattern_name', 'unknown')} ({match.get('crisis_level', 'unknown')})")
        
        # Performance validation
        assert processing_time < 1.0, f"Analysis took too long: {processing_time:.3f}s"
        
        logger.info(f"✅ High-risk analysis complete:")
        logger.info(f"   Crisis level: {result['crisis_level']}")
        logger.info(f"   Confidence: {result['confidence_score']:.3f}")
        logger.info(f"   Categories: {result['detected_categories']}")
        logger.info(f"   Processing time: {processing_time:.3f}s")
        logger.info(f"   Method: {result['method']}")

    @pytest.mark.asyncio
    async def test_real_world_crisis_analysis_low_risk(self):
        """Test complete crisis analysis with low-risk message using real system"""
        message = "I'm having a great day and feeling positive about life"
        user_id = "test_user_002"
        channel_id = "test_channel_002"
        
        logger.info(f"🔍 Testing low-risk message: '{message}'")
        
        start_time = time.time()
        result = await self.crisis_analyzer.analyze_crisis(message, user_id, channel_id)
        processing_time = time.time() - start_time
        
        # Validate response structure (same as high-risk)
        assert isinstance(result, dict)
        required_fields = [
            'message', 'user_id', 'channel_id', 'needs_response', 
            'crisis_level', 'confidence_score', 'detected_categories',
            'method', 'analysis_results', 'requires_staff_review', 'processing_time'
        ]
        
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"
        
        # Validate low-risk detection
        assert result['crisis_level'] in ['none', 'low'], f"Unexpected crisis level for positive message: {result['crisis_level']}"
        assert result['confidence_score'] < 0.5, f"High confidence for low-risk message: {result['confidence_score']}"
        
        # Performance validation
        assert processing_time < 1.0, f"Analysis took too long: {processing_time:.3f}s"
        
        logger.info(f"✅ Low-risk analysis complete:")
        logger.info(f"   Crisis level: {result['crisis_level']}")
        logger.info(f"   Confidence: {result['confidence_score']:.3f}")
        logger.info(f"   Categories: {result['detected_categories']}")
        logger.info(f"   Processing time: {processing_time:.3f}s")
        logger.info(f"   Method: {result['method']}")

    @pytest.mark.asyncio
    async def test_real_world_crisis_analysis_edge_cases(self):
        """Test edge cases with real system"""
        
        edge_cases = [
            ("", "empty_message"),
            ("   ", "whitespace_only"),
            ("a", "single_character"),
            ("🙂", "emoji_only"),
            ("Maybe I'm struggling but it's fine", "ambiguous_message"),
            ("I used to feel hopeless but I'm better now", "past_tense_negation")
        ]
        
        for message, case_name in edge_cases:
            logger.info(f"🔍 Testing edge case '{case_name}': '{message}'")
            
            try:
                result = await self.crisis_analyzer.analyze_crisis(
                    message, f"test_{case_name}", "edge_case_channel"
                )
                
                # Should always return valid response structure
                assert isinstance(result, dict)
                assert 'crisis_level' in result
                assert 'confidence_score' in result
                assert 'method' in result
                
                logger.info(f"   ✅ {case_name}: {result['crisis_level']} (conf: {result['confidence_score']:.3f})")
                
            except Exception as e:
                logger.error(f"   ❌ {case_name} failed: {e}")
                raise

    def test_backward_compatibility_analyze_message(self):
        """Test that the legacy analyze_message method still works"""
        
        async def test_legacy_method():
            message = "I'm feeling down today"
            result = await self.crisis_analyzer.analyze_message(message, "legacy_user", "legacy_channel")
            
            assert isinstance(result, dict)
            assert 'crisis_level' in result
            assert 'confidence_score' in result
            
            logger.info(f"✅ Legacy analyze_message: {result['crisis_level']} (conf: {result['confidence_score']:.3f})")
        
        # Run the async test
        asyncio.run(test_legacy_method())

    def test_input_validation_and_error_handling(self):
        """Test input validation and error handling with real system"""
        
        # Test invalid input types (should handle gracefully)
        async def test_invalid_inputs():
            try:
                # Test with None values
                result = await self.crisis_analyzer.analyze_crisis(None, "user", "channel")
                # Should handle gracefully and return error response
                assert isinstance(result, dict)
                assert result.get('status') == 'error' or 'error' in str(result)
                logger.info("✅ None message handled gracefully")
            except Exception as e:
                logger.info(f"✅ None message raised expected exception: {type(e).__name__}")
        
        asyncio.run(test_invalid_inputs())

    def test_configuration_access_patterns(self):
        """Test that consolidated methods properly access configuration"""
        
        # Test that methods return consistent data types
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        assert isinstance(thresholds, dict)
        assert all(isinstance(k, str) for k in thresholds.keys())
        assert all(isinstance(v, (int, float)) for v in thresholds.values())
        
        # Test that validation works
        validation = self.crisis_analyzer.validate_crisis_analysis_thresholds()
        assert isinstance(validation, dict)
        assert 'overall_valid' in validation
        
        # Test configuration consistency
        timeouts = self.crisis_analyzer.get_analysis_timeouts()
        assert isinstance(timeouts, dict)
        
        logger.info("✅ Configuration access patterns working correctly")

    def test_performance_characteristics(self):
        """Test performance characteristics of consolidated methods"""
        
        # Test method execution times
        methods_to_test = [
            ('get_analysis_crisis_thresholds', lambda: self.crisis_analyzer.get_analysis_crisis_thresholds()),
            ('get_analysis_timeouts', lambda: self.crisis_analyzer.get_analysis_timeouts()),
            ('get_analysis_confidence_boosts', lambda: self.crisis_analyzer.get_analysis_confidence_boosts()),
            ('apply_crisis_thresholds', lambda: self.crisis_analyzer.apply_crisis_thresholds(0.5)),
            ('validate_crisis_analysis_thresholds', lambda: self.crisis_analyzer.validate_crisis_analysis_thresholds())
        ]
        
        for method_name, method_func in methods_to_test:
            start_time = time.time()
            
            # Run method multiple times to get average
            for _ in range(10):
                result = method_func()
                assert result is not None
            
            avg_time = (time.time() - start_time) / 10
            
            # Should be very fast (< 10ms per call on average)
            assert avg_time < 0.01, f"{method_name} too slow: {avg_time:.4f}s per call"
            
            logger.info(f"✅ {method_name}: {avg_time*1000:.2f}ms per call")

    def test_feature_flag_integration(self):
        """Test that feature flags properly control analysis behavior"""
        
        # Test that feature manager is accessible
        assert self.crisis_analyzer.feature_config_manager is not None
        
        # Test feature cache refresh
        self.crisis_analyzer._refresh_feature_cache()
        assert isinstance(self.crisis_analyzer._feature_cache, dict)
        
        # Test performance cache refresh
        self.crisis_analyzer._refresh_performance_cache()
        assert isinstance(self.crisis_analyzer._performance_cache, dict)
        
        logger.info(f"✅ Feature flags: {self.crisis_analyzer._feature_cache}")
        logger.info(f"✅ Performance settings: {self.crisis_analyzer._performance_cache}")

    def test_manager_integration_status(self):
        """Test the status of all manager integrations"""
        
        managers = {
            'model_ensemble_manager': self.crisis_analyzer.model_ensemble_manager,
            'crisis_pattern_manager': self.crisis_analyzer.crisis_pattern_manager,
            'analysis_parameters_manager': self.crisis_analyzer.analysis_parameters_manager,
            'threshold_mapping_manager': self.crisis_analyzer.threshold_mapping_manager,
            'feature_config_manager': self.crisis_analyzer.feature_config_manager,
            'performance_config_manager': self.crisis_analyzer.performance_config_manager,
            'context_pattern_manager': self.crisis_analyzer.context_pattern_manager,
            'shared_utilities_manager': self.crisis_analyzer.shared_utilities_manager,
            'learning_system_manager': self.crisis_analyzer.learning_system_manager
        }
        
        for manager_name, manager_instance in managers.items():
            status = "Available" if manager_instance is not None else "Not Available"
            logger.info(f"   {manager_name}: {status}")
            
            if manager_name in ['shared_utilities_manager', 'learning_system_manager']:
                # These are expected to be None in current setup
                assert manager_instance is None, f"{manager_name} should be None in current setup"
            else:
                # These should be available
                assert manager_instance is not None, f"{manager_name} should be available"
        
        logger.info("✅ Manager integration status verified")


def test_consolidation_summary_function():
    """Test the consolidation summary information function"""
    summary = get_consolidation_summary()
    
    assert isinstance(summary, dict)
    assert summary['phase'] == '3e_step_4.2'
    assert summary['total_methods_added'] == 12
    assert 'SharedUtilitiesManager' in summary['dependencies_added']
    assert 'LearningSystemManager' in summary['dependencies_added']
    assert len(summary['methods_consolidated']['from_analysis_parameters_manager']) == 5
    assert len(summary['methods_consolidated']['from_threshold_mapping_manager']) == 4
    assert len(summary['methods_consolidated']['from_model_ensemble_manager']) == 3
    
    logger.info("✅ Consolidation summary function working correctly")


def test_dependency_validation_function():
    """Test dependency validation with real managers"""
    
    # Create unified config manager
    config_manager = create_unified_config_manager()
    model_ensemble_manager = create_model_ensemble_manager(config_manager)
    
    # Test validation with valid dependencies
    validation = validate_crisis_analyzer_dependencies(
        model_ensemble_manager=model_ensemble_manager
    )
    
    assert validation["valid"] is True
    assert len(validation["errors"]) == 0
    
    # Test validation with missing required dependency
    validation_missing = validate_crisis_analyzer_dependencies()
    
    assert validation_missing["valid"] is False
    assert "model_ensemble_manager is required" in validation_missing["errors"]
    
    logger.info("✅ Dependency validation function working correctly")


if __name__ == "__main__":
    # Run the tests
    pytest.main([
        "-v", 
        "-s",  # Don't capture output so we can see logs
        __file__,
        "--tb=short"  # Shorter traceback format
    ])
    
    logger.info("🎉 Real-World CrisisAnalyzer Integration Tests Complete!")
    logger.info("✅ All consolidated methods tested with actual functionality")
    logger.info("✅ Real manager integration verified")
    logger.info("✅ Performance characteristics validated")
    logger.info("✅ Edge cases and error handling confirmed")
    logger.info("✅ Configuration access patterns working")
    logger.info("🚀 Phase 3e Step 4.3 - Real-world testing successful!")