"""
Ash-NLP Ensemble Tests
---
FILE VERSION: v5.0-3-5.4-5
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for ensemble system components: ModelLoader, WeightedScorer,
FallbackStrategy, and EnsembleDecisionEngine.
"""

import pytest


class TestCrisisSeverity:
    """Tests for CrisisSeverity enum."""

    def test_severity_levels_exist(self):
        """Test all severity levels exist."""
        from src.ensemble import CrisisSeverity

        assert hasattr(CrisisSeverity, "CRITICAL")
        assert hasattr(CrisisSeverity, "HIGH")
        assert hasattr(CrisisSeverity, "MEDIUM")
        assert hasattr(CrisisSeverity, "LOW")
        assert hasattr(CrisisSeverity, "SAFE")

    def test_severity_from_score(self):
        """Test score to severity mapping."""
        from src.ensemble import CrisisSeverity

        thresholds = {
            "critical": 0.85,
            "high": 0.70,
            "medium": 0.50,
            "low": 0.30,
        }

        assert CrisisSeverity.from_score(0.90, thresholds) == CrisisSeverity.CRITICAL
        assert CrisisSeverity.from_score(0.75, thresholds) == CrisisSeverity.HIGH
        assert CrisisSeverity.from_score(0.60, thresholds) == CrisisSeverity.MEDIUM
        assert CrisisSeverity.from_score(0.35, thresholds) == CrisisSeverity.LOW
        assert CrisisSeverity.from_score(0.20, thresholds) == CrisisSeverity.SAFE


class TestWeightedScorer:
    """Tests for WeightedScorer class."""

    def test_scorer_import(self):
        """Test scorer can be imported."""
        from src.ensemble import WeightedScorer, create_weighted_scorer

        assert WeightedScorer is not None
        assert create_weighted_scorer is not None

    def test_scorer_factory(self, config_manager):
        """Test scorer factory function."""
        from src.ensemble import create_weighted_scorer

        scorer = create_weighted_scorer(config_manager=config_manager)

        assert scorer is not None
        assert scorer.weights is not None
        assert scorer.thresholds is not None

    def test_scorer_default_weights(self):
        """Test scorer has correct default weights."""
        from src.ensemble import create_weighted_scorer

        scorer = create_weighted_scorer()
        weights = scorer.get_weights()

        assert weights["bart"] == 0.50
        assert weights["sentiment"] == 0.25
        assert weights["irony"] == 0.15
        assert weights["emotions"] == 0.10

    def test_calculate_score_with_mocks(
        self,
        mock_bart_result,
        mock_sentiment_result,
        mock_irony_result,
        mock_emotions_result,
    ):
        """Test score calculation with mock results."""
        from src.ensemble import create_weighted_scorer

        scorer = create_weighted_scorer()

        result = scorer.calculate_score(
            bart_result=mock_bart_result,
            sentiment_result=mock_sentiment_result,
            irony_result=mock_irony_result,
            emotions_result=mock_emotions_result,
        )

        assert result is not None
        assert 0.0 <= result.crisis_score <= 1.0
        assert 0.0 <= result.confidence <= 1.0
        assert result.severity is not None

    def test_calculate_score_partial(self, mock_bart_result):
        """Test score calculation with only BART result."""
        from src.ensemble import create_weighted_scorer

        scorer = create_weighted_scorer()

        result = scorer.calculate_score(bart_result=mock_bart_result)

        assert result is not None
        assert result.crisis_score >= 0.0

    def test_extract_bart_signal(self, mock_bart_result):
        """Test BART signal extraction."""
        from src.ensemble import create_weighted_scorer

        scorer = create_weighted_scorer()
        signal = scorer.extract_bart_signal(mock_bart_result)

        assert signal.model_name == "bart"
        assert signal.weight == 0.50
        assert signal.crisis_signal >= 0.0

    def test_extract_irony_signal_dampening(self):
        """Test irony dampening factor calculation."""
        from src.ensemble import create_weighted_scorer
        from src.models import ModelResult, ModelRole

        scorer = create_weighted_scorer()

        # High irony = low dampening
        ironic_result = ModelResult(
            label="irony",
            score=0.95,
            all_scores={"irony": 0.95, "non_irony": 0.05},
            latency_ms=50.0,
            model_name="irony",
            model_role=ModelRole.TERTIARY,
            success=True,
            error=None,
        )

        signal = scorer.extract_irony_signal(ironic_result)

        # Irony signal should be dampening factor (low for high irony)
        assert signal.crisis_signal < 0.5  # High irony = low dampening


class TestFallbackStrategy:
    """Tests for FallbackStrategy class."""

    def test_fallback_import(self):
        """Test fallback can be imported."""
        from src.ensemble import FallbackStrategy, create_fallback_strategy

        assert FallbackStrategy is not None
        assert create_fallback_strategy is not None

    def test_fallback_factory(self):
        """Test fallback factory function."""
        from src.ensemble import create_fallback_strategy

        fallback = create_fallback_strategy()

        assert fallback is not None
        assert fallback.is_operational()

    def test_fallback_initial_state(self):
        """Test fallback initial state."""
        from src.ensemble import create_fallback_strategy

        fallback = create_fallback_strategy()

        assert not fallback.is_degraded()
        assert fallback.is_operational()
        assert len(fallback.failed_models) == 0

    def test_handle_secondary_model_failure(self):
        """Test handling non-critical model failure."""
        from src.ensemble import create_fallback_strategy

        fallback = create_fallback_strategy()

        # Fail a secondary model
        fallback.handle_model_failure("sentiment", "Test error")

        # Should be degraded but still operational
        assert fallback.is_degraded()
        assert fallback.is_operational()
        assert "sentiment" in fallback.failed_models

    def test_handle_primary_model_failure(self):
        """Test handling critical (BART) model failure."""
        from src.ensemble import create_fallback_strategy, CriticalModelFailure

        fallback = create_fallback_strategy()

        # Fail BART (primary) - should raise exception
        with pytest.raises(CriticalModelFailure):
            fallback.handle_model_failure("bart", "Test error")

    def test_weight_redistribution(self):
        """Test weight redistribution on model failure."""
        from src.ensemble import create_fallback_strategy

        fallback = create_fallback_strategy()
        original_weights = fallback.get_current_weights()

        # Fail sentiment model
        fallback.handle_model_failure("sentiment", "Test error")
        new_weights = fallback.get_current_weights()

        # Sentiment weight should be 0
        assert new_weights["sentiment"] == 0.0

        # Other models should have increased weights
        # (redistributed from sentiment)

    def test_circuit_breaker(self):
        """Test circuit breaker functionality."""
        from src.ensemble import create_fallback_strategy

        fallback = create_fallback_strategy(failure_threshold=2)

        # Should be able to call initially
        assert fallback.can_call_model("sentiment")

        # Fail multiple times
        fallback.handle_model_failure("sentiment", "Error 1")
        fallback.handle_model_failure("sentiment", "Error 2")

        # Circuit should be open now
        assert not fallback.can_call_model("sentiment")

    def test_reset(self):
        """Test fallback reset functionality."""
        from src.ensemble import create_fallback_strategy

        fallback = create_fallback_strategy()

        # Create some failures
        fallback.handle_model_failure("sentiment", "Test error")
        assert fallback.is_degraded()

        # Reset
        fallback.reset()

        # Should be back to initial state
        assert not fallback.is_degraded()
        assert len(fallback.failed_models) == 0


class TestModelLoader:
    """Tests for ModelLoader class."""

    def test_loader_import(self):
        """Test loader can be imported."""
        from src.ensemble import ModelLoader, create_model_loader

        assert ModelLoader is not None
        assert create_model_loader is not None

    def test_loader_factory(self):
        """Test loader factory function."""
        from src.ensemble import create_model_loader

        loader = create_model_loader(lazy_load=True, warmup_on_load=False)

        assert loader is not None
        assert loader.lazy_load is True

    def test_loader_initial_state(self):
        """Test loader initial state."""
        from src.ensemble import create_model_loader

        loader = create_model_loader(lazy_load=True)

        assert loader._models_loaded == 0
        assert not loader._is_initialized

    def test_loader_model_names(self):
        """Test MODEL_NAMES constant."""
        from src.ensemble import MODEL_NAMES

        assert "bart" in MODEL_NAMES
        assert "sentiment" in MODEL_NAMES
        assert "irony" in MODEL_NAMES
        assert "emotions" in MODEL_NAMES


class TestDecisionEngine:
    """Tests for EnsembleDecisionEngine class."""

    def test_engine_import(self):
        """Test engine can be imported."""
        from src.ensemble import EnsembleDecisionEngine, create_decision_engine

        assert EnsembleDecisionEngine is not None
        assert create_decision_engine is not None

    def test_engine_factory(self, config_manager):
        """Test engine factory function."""
        from src.ensemble import create_decision_engine

        engine = create_decision_engine(
            config_manager=config_manager,
            auto_initialize=False,
        )

        assert engine is not None
        assert engine.model_loader is not None
        assert engine.scorer is not None
        assert engine.fallback is not None

    def test_engine_not_ready_without_init(self):
        """Test engine is not ready without initialization."""
        from src.ensemble import create_decision_engine

        engine = create_decision_engine(auto_initialize=False)

        # Should not be ready (models not loaded)
        assert not engine.is_ready()


class TestCrisisAssessment:
    """Tests for CrisisAssessment dataclass."""

    def test_assessment_creation(self):
        """Test CrisisAssessment can be created."""
        from src.ensemble import CrisisAssessment, CrisisSeverity

        assessment = CrisisAssessment(
            crisis_detected=True,
            severity=CrisisSeverity.HIGH,
            confidence=0.85,
            crisis_score=0.78,
            requires_intervention=True,
            recommended_action="priority_response",
            signals={},
            processing_time_ms=100.0,
            models_used=["bart"],
        )

        assert assessment.crisis_detected is True
        assert assessment.severity == CrisisSeverity.HIGH

    def test_assessment_to_dict(self):
        """Test CrisisAssessment to_dict method."""
        from src.ensemble import CrisisAssessment, CrisisSeverity

        assessment = CrisisAssessment(
            crisis_detected=True,
            severity=CrisisSeverity.HIGH,
            confidence=0.85,
            crisis_score=0.78,
            requires_intervention=True,
            recommended_action="priority_response",
            signals={},
            processing_time_ms=100.0,
            models_used=["bart"],
        )

        result = assessment.to_dict()

        assert isinstance(result, dict)
        assert result["crisis_detected"] is True
        assert result["severity"] == "high"

    def test_assessment_error_factory(self):
        """Test CrisisAssessment.create_error factory."""
        from src.ensemble import CrisisAssessment, CrisisSeverity

        assessment = CrisisAssessment.create_error(
            error="Test error",
            message="Test message",
        )

        assert assessment.crisis_detected is False
        assert assessment.severity == CrisisSeverity.SAFE
        assert assessment.is_degraded is True


class TestEnsemblePackage:
    """Tests for ensemble package exports."""

    def test_all_exports(self):
        """Test all expected exports are available."""
        from src.ensemble import (
            EnsembleDecisionEngine,
            create_decision_engine,
            CrisisAssessment,
            RecommendedAction,
            ModelLoader,
            create_model_loader,
            WeightedScorer,
            create_weighted_scorer,
            CrisisSeverity,
            ModelSignal,
            EnsembleScore,
            FallbackStrategy,
            create_fallback_strategy,
            CircuitBreaker,
            CriticalModelFailure,
        )

        # All imports should succeed
        assert EnsembleDecisionEngine is not None
        assert CrisisSeverity is not None
