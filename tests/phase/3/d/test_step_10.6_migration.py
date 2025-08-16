# ash-nlp/tests/test_step_10_6_migration.py
"""
Phase 3d, Step 10.6 Testing Suite for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-13
PHASE: 3d, Step 10.11-3
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import pytest
import asyncio
import logging
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Test the migrated functions in CrisisAnalyzer
from analysis.crisis_analyzer import CrisisAnalyzer
from managers.crisis_pattern_manager import create_crisis_pattern_manager
from managers.unified_config_manager import create_unified_config_manager

logger = logging.getLogger(__name__)

class TestStep106Migration:
    """Test the migration of scoring functions from utils/scoring_helpers.py to CrisisAnalyzer"""
    
    @pytest.fixture
    def sample_config_manager(self):
        """Create a mock unified config manager for testing"""
        config_manager = Mock()
        config_manager.get_config_value.return_value = "/app/config"
        config_manager.substitute_environment_variables.return_value = {}
        return config_manager
    
    @pytest.fixture
    def sample_model_ensemble_manager(self):
        """Create a mock models manager for testing"""
        model_ensemble_manager = Mock()
        
        # Mock depression model
        depression_model = Mock()
        depression_model.return_value = [
            {'label': 'depression', 'score': 0.75},
            {'label': 'normal', 'score': 0.25}
        ]
        
        # Mock sentiment model
        sentiment_model = Mock()
        sentiment_model.return_value = [
            {'label': 'NEGATIVE', 'score': 0.85},
            {'label': 'POSITIVE', 'score': 0.15}
        ]
        
        # Mock crisis model
        crisis_model = Mock()
        crisis_model.return_value = [
            {'label': 'crisis', 'score': 0.60},
            {'label': 'no_crisis', 'score': 0.40}
        ]
        
        model_ensemble_manager.get_model.side_effect = lambda model_type: {
            'depression': depression_model,
            'sentiment': sentiment_model,
            'crisis': crisis_model
        }.get(model_type)
        
        return model_ensemble_manager
    
    @pytest.fixture
    def sample_crisis_analyzer(self, sample_model_ensemble_manager, sample_config_manager):
        """Create a CrisisAnalyzer instance for testing"""
        # Create mock managers
        crisis_pattern_manager = Mock()
        crisis_pattern_manager.get_patterns.return_value = {'idiom_patterns': []}
        crisis_pattern_manager.apply_context_weights.return_value = (0.5, {})
        
        analysis_parameters_manager = Mock()
        analysis_parameters_manager.get_phrase_extraction_parameters.return_value = {
            'min_confidence': 0.3,
            'max_results': 20
        }
        
        threshold_mapping_manager = Mock()
        threshold_mapping_manager.get_current_ensemble_mode.return_value = 'balanced'
        threshold_mapping_manager.get_ensemble_thresholds.return_value = {
            'crisis_levels': {'high': 0.55, 'medium': 0.28, 'low': 0.16}
        }
        
        feature_config_manager = Mock()
        feature_config_manager.get_core_system_features.return_value = {
            'ensemble_analysis': True,
            'pattern_integration': True
        }
        
        performance_config_manager = Mock()
        performance_config_manager.get_analysis_performance_settings.return_value = {
            'analysis_timeout_seconds': 30.0
        }
        
        return CrisisAnalyzer(
            model_ensemble_manager=sample_model_ensemble_manager,
            crisis_pattern_manager=crisis_pattern_manager,
            analysis_parameters_manager=analysis_parameters_manager,
            threshold_mapping_manager=threshold_mapping_manager,
            feature_config_manager=feature_config_manager,
            performance_config_manager=performance_config_manager
        )

    def test_extract_depression_score_migration(self, sample_crisis_analyzer, sample_model_ensemble_manager):
        """Test that extract_depression_score works as CrisisAnalyzer instance method"""
        
        # Get the depression model
        depression_model = sample_model_ensemble_manager.get_model('depression')
        
        # Test the migrated method
        score = sample_crisis_analyzer.extract_depression_score(
            message="I feel really sad and hopeless",
            depression_model=depression_model
        )
        
        # Validate score
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert score == 0.75  # Should match the mocked return value
        
        logger.info(f"✅ extract_depression_score migration test passed: score={score}")

    def test_enhanced_depression_analysis_migration(self, sample_crisis_analyzer, sample_model_ensemble_manager):
        """Test that enhanced_depression_analysis works as CrisisAnalyzer instance method"""
        
        # Get models
        depression_model = sample_model_ensemble_manager.get_model('depression')
        sentiment_model = sample_model_ensemble_manager.get_model('sentiment')
        
        # Test the migrated method
        result = sample_crisis_analyzer.enhanced_depression_analysis(
            message="I feel really sad and hopeless",
            base_score=0.6,
            depression_model=depression_model,
            sentiment_model=sentiment_model,
            context={'social_isolation_indicators': 3}
        )
        
        # Validate result structure
        assert isinstance(result, dict)
        assert 'final_score' in result
        assert 'base_score' in result
        assert 'total_adjustment' in result
        assert 'reasoning' in result
        assert 'detected_categories' in result
        
        # Validate score adjustments
        assert result['base_score'] == 0.6
        assert isinstance(result['final_score'], float)
        assert 0.0 <= result['final_score'] <= 1.0
        
        logger.info(f"✅ enhanced_depression_analysis migration test passed: final_score={result['final_score']}")

    def test_enhanced_crisis_level_mapping_migration(self, sample_crisis_analyzer):
        """Test that enhanced_crisis_level_mapping works as CrisisAnalyzer instance method"""
        
        # Test different score levels
        test_cases = [
            (0.8, 'high'),
            (0.4, 'medium'),
            (0.2, 'low'),
            (0.1, 'none')
        ]
        
        for score, expected_level in test_cases:
            level = sample_crisis_analyzer.enhanced_crisis_level_mapping(score)
            assert level == expected_level
            logger.info(f"✅ Crisis level mapping: {score} → {level}")

    def test_advanced_idiom_detection_migration(self, sample_crisis_analyzer):
        """Test that advanced_idiom_detection works as CrisisAnalyzer instance method"""
        
        # Test with patterns
        test_patterns = [
            {'pattern': r'\bfeeling down\b', 'boost': 0.1}
        ]
        
        adjusted_score = sample_crisis_analyzer.advanced_idiom_detection(
            message="I'm feeling down today",
            base_score=0.3,
            patterns=test_patterns
        )
        
        # Validate adjustment
        assert isinstance(adjusted_score, float)
        assert adjusted_score >= 0.3  # Should be boosted
        
        logger.info(f"✅ advanced_idiom_detection migration test passed: {0.3} → {adjusted_score}")

    @pytest.mark.asyncio
    async def test_score_phrases_with_models_migration(self, sample_crisis_analyzer):
        """Test that score_phrases_with_models works as CrisisAnalyzer instance method"""
        
        # Test phrase scoring
        phrases = ["I feel hopeless", "Everything is terrible", "I can't go on"]
        
        scored_phrases = await sample_crisis_analyzer.score_phrases_with_models(
            phrases=phrases,
            original_message="I feel hopeless. Everything is terrible. I can't go on."
        )
        
        # Validate results
        assert isinstance(scored_phrases, list)
        assert len(scored_phrases) <= len(phrases)
        
        for phrase_data in scored_phrases:
            assert isinstance(phrase_data, dict)
            assert 'text' in phrase_data
            assert 'score' in phrase_data
            assert isinstance(phrase_data['score'], float)
            assert 0.0 <= phrase_data['score'] <= 1.0
        
        logger.info(f"✅ score_phrases_with_models migration test passed: {len(scored_phrases)} phrases scored")

    def test_filter_and_rank_phrases_migration(self, sample_crisis_analyzer):
        """Test that filter_and_rank_phrases works as CrisisAnalyzer instance method"""
        
        # Create sample phrases with scores
        phrases = [
            {'text': 'High score phrase', 'score': 0.8},
            {'text': 'Medium score phrase', 'score': 0.5},
            {'text': 'Low score phrase', 'score': 0.2},
            {'text': 'Very low score phrase', 'score': 0.1}
        ]
        
        # Test filtering and ranking
        filtered_phrases = sample_crisis_analyzer.filter_and_rank_phrases(
            phrases=phrases,
            parameters={'min_confidence': 0.3, 'max_results': 3}
        )
        
        # Validate filtering
        assert isinstance(filtered_phrases, list)
        assert len(filtered_phrases) <= 3
        
        # Should be ranked by score (descending)
        scores = [p['score'] for p in filtered_phrases]
        assert scores == sorted(scores, reverse=True)
        
        # All scores should be >= min_confidence
        for phrase in filtered_phrases:
            assert phrase['score'] >= 0.3
        
        logger.info(f"✅ filter_and_rank_phrases migration test passed: {len(filtered_phrases)} phrases filtered")

    def test_process_sentiment_result_migration(self, sample_crisis_analyzer):
        """Test that _process_sentiment_result works as CrisisAnalyzer instance method"""
        
        # Test sentiment processing
        sentiment_result = [
            {'label': 'NEGATIVE', 'score': 0.85},
            {'label': 'POSITIVE', 'score': 0.15}
        ]
        
        processed = sample_crisis_analyzer._process_sentiment_result(sentiment_result)
        
        # Validate processing
        assert isinstance(processed, dict)
        assert 'negative' in processed
        assert 'positive' in processed
        assert processed['negative'] == 0.85
        assert processed['positive'] == 0.15
        
        logger.info(f"✅ _process_sentiment_result migration test passed: {processed}")

    def test_utils_scoring_helpers_eliminated(self):
        """Test that utils/scoring_helpers.py functions are no longer accessible via utils import"""
        
        try:
            # This should fail because we've removed the imports
            from utils import extract_depression_score
            pytest.fail("utils.extract_depression_score should not be accessible after migration")
        except ImportError:
            logger.info("✅ utils.extract_depression_score correctly eliminated")
        
        try:
            from utils import enhanced_depression_analysis  
            pytest.fail("utils.enhanced_depression_analysis should not be accessible after migration")
        except ImportError:
            logger.info("✅ utils.enhanced_depression_analysis correctly eliminated")

    def test_migration_status_metadata(self):
        """Test that utils package correctly reports migration status"""
        
        from utils import get_migration_status, get_scoring_capabilities
        
        # Check migration status
        migration_status = get_migration_status()
        assert migration_status['current_step'] == '10.6_complete'
        assert 'scoring_helpers_consolidation' in migration_status['completed']
        
        # Check scoring capabilities
        scoring_capabilities = get_scoring_capabilities()
        assert scoring_capabilities['status'] == 'MIGRATED_TO_CRISIS_ANALYZER'
        assert scoring_capabilities['phase'] == '3d_step_10_6_complete'
        
        logger.info("✅ Migration status metadata test passed")

    @pytest.mark.asyncio
    async def test_full_analysis_with_consolidated_functions(self, sample_crisis_analyzer):
        """Test that full analysis workflow works with consolidated scoring functions"""
        
        # Test full message analysis
        test_message = "I feel hopeless and can't see a way out of this darkness"
        
        result = await sample_crisis_analyzer.analyze_message(
            message=test_message,
            context={'user_id': 'test_user'}
        )
        
        # Validate analysis result
        assert isinstance(result, dict)
        assert 'crisis_level' in result
        assert 'confidence' in result
        assert 'ensemble_scores' in result
        assert 'reasoning' in result
        assert 'processing_time' in result
        
        # Validate crisis level
        assert result['crisis_level'] in ['none', 'low', 'medium', 'high']
        assert isinstance(result['confidence'], float)
        assert 0.0 <= result['confidence'] <= 1.0
        
        logger.info(f"✅ Full analysis test passed: {result['crisis_level']} (confidence: {result['confidence']:.3f})")

# Comprehensive test runner
@pytest.mark.asyncio
async def test_step_10_6_comprehensive_validation():
    """Comprehensive validation that Step 10.6 migration is successful"""
    
    logger.info("🚀 Starting Step 10.6 Comprehensive Migration Validation")
    
    # Create test instance
    test_instance = TestStep106Migration()
    
    # Create fixtures
    config_manager = test_instance.sample_config_manager()
    model_ensemble_manager = test_instance.sample_model_ensemble_manager()
    crisis_analyzer = test_instance.sample_crisis_analyzer(model_ensemble_manager, config_manager)
    
    # Run all tests
    test_methods = [
        'test_extract_depression_score_migration',
        'test_enhanced_depression_analysis_migration', 
        'test_enhanced_crisis_level_mapping_migration',
        'test_advanced_idiom_detection_migration',
        'test_filter_and_rank_phrases_migration',
        'test_process_sentiment_result_migration',
        'test_utils_scoring_helpers_eliminated',
        'test_migration_status_metadata'
    ]
    
    # Run async tests
    await test_instance.test_score_phrases_with_models_migration(crisis_analyzer)
    await test_instance.test_full_analysis_with_consolidated_functions(crisis_analyzer)
    
    # Run sync tests
    for method_name in test_methods:
        method = getattr(test_instance, method_name)
        if 'crisis_analyzer' in method.__code__.co_varnames:
            method(crisis_analyzer)
        elif 'model_ensemble_manager' in method.__code__.co_varnames:
            method(crisis_analyzer, model_ensemble_manager)
        else:
            method()
    
    logger.info("✅ Step 10.6 Comprehensive Migration Validation PASSED")
    return True

if __name__ == "__main__":
    # Run the comprehensive test
    result = asyncio.run(test_step_10_6_comprehensive_validation())
    print(f"✅ Step 10.6 Migration Test Result: {'PASSED' if result else 'FAILED'}")