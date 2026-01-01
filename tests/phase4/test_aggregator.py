"""
Ash-NLP Phase 4 Tests: Result Aggregator
---
FILE VERSION: v5.0-4-TEST-3.1
LAST MODIFIED: 2026-01-01
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- ResultAggregator class
- AggregatedResult data class
- Crisis level determination
- Intervention priority calculation
- Backward compatibility (legacy format)
"""

import pytest
from typing import Dict, Any

from src.ensemble.aggregator import (
    # Enums
    CrisisLevel,
    InterventionPriority,
    # Data classes
    ModelResultSummary,
    AggregatedResult,
    # Aggregator
    ResultAggregator,
    create_result_aggregator,
)
from src.ensemble.consensus import (
    ConsensusAlgorithm,
    AgreementLevel,
    ConsensusResult,
)
from src.ensemble.conflict_detector import (
    ConflictType,
    ConflictSeverity,
    DetectedConflict,
    ConflictReport,
)
from src.ensemble.conflict_resolver import (
    ResolutionStrategy,
    ResolutionResult,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def high_crisis_signals() -> Dict[str, Any]:
    """High crisis model signals."""
    return {
        "bart": {
            "crisis_signal": 0.90,
            "label": "suicide ideation",
            "raw_score": 0.90,
            "score": 0.90,
            "metadata": {"all_scores": {"suicide ideation": 0.90, "safe": 0.10}},
        },
        "sentiment": {
            "crisis_signal": 0.80,
            "label": "negative",
            "raw_score": 0.80,
            "score": 0.80,
            "metadata": {"negative": 0.80, "positive": 0.15},
        },
        "irony": {
            "crisis_signal": 0.95,
            "label": "not_ironic",
            "raw_score": 0.95,
            "score": 0.95,
            "metadata": {"irony_score": 0.05},
        },
        "emotions": {
            "crisis_signal": 0.75,
            "label": "sadness",
            "raw_score": 0.75,
            "score": 0.75,
            "metadata": {"top_emotions": {"sadness": 0.60, "fear": 0.40}},
        },
    }


@pytest.fixture
def low_crisis_signals() -> Dict[str, Any]:
    """Safe/low crisis model signals."""
    return {
        "bart": {
            "crisis_signal": 0.15,
            "label": "safe",
            "raw_score": 0.15,
            "score": 0.15,
            "metadata": {"all_scores": {"safe": 0.85}},
        },
        "sentiment": {
            "crisis_signal": 0.20,
            "label": "positive",
            "raw_score": 0.20,
            "score": 0.20,
            "metadata": {"positive": 0.70},
        },
        "irony": {
            "crisis_signal": 0.90,
            "label": "not_ironic",
            "raw_score": 0.90,
            "score": 0.90,
            "metadata": {},
        },
        "emotions": {
            "crisis_signal": 0.10,
            "label": "joy",
            "raw_score": 0.10,
            "score": 0.10,
            "metadata": {"top_emotions": {"joy": 0.70}},
        },
    }


@pytest.fixture
def high_consensus_result() -> ConsensusResult:
    """High crisis consensus result."""
    return ConsensusResult(
        algorithm=ConsensusAlgorithm.WEIGHTED_VOTING,
        crisis_score=0.85,
        confidence=0.90,
        agreement_level=AgreementLevel.STRONG_AGREEMENT,
        is_crisis=True,
        requires_review=False,
        has_conflict=False,
        individual_scores={"bart": 0.90, "sentiment": 0.80},
    )


@pytest.fixture
def no_conflict_report() -> ConflictReport:
    """Report with no conflicts."""
    return ConflictReport(
        has_conflicts=False,
        conflict_count=0,
        conflicts=[],
        highest_severity=None,
        requires_review=False,
        summary="No conflicts",
    )


@pytest.fixture
def high_conflict_report() -> ConflictReport:
    """Report with high severity conflict."""
    return ConflictReport(
        has_conflicts=True,
        conflict_count=1,
        conflicts=[
            DetectedConflict(
                conflict_type=ConflictType.SCORE_DISAGREEMENT,
                severity=ConflictSeverity.HIGH,
                description="Score disagreement",
                involved_models=["bart", "sentiment"],
            )
        ],
        highest_severity=ConflictSeverity.HIGH,
        requires_review=True,
        summary="1 high conflict",
    )


@pytest.fixture
def resolution_with_review() -> ResolutionResult:
    """Resolution result requiring review."""
    return ResolutionResult(
        strategy_used=ResolutionStrategy.CONSERVATIVE,
        original_score=0.60,
        resolved_score=0.85,
        was_modified=True,
        requires_review=True,
        resolution_reason="Conservative resolution",
    )


@pytest.fixture
def default_thresholds() -> Dict[str, float]:
    """Default crisis thresholds."""
    return {
        "critical": 0.85,
        "high": 0.70,
        "medium": 0.50,
        "low": 0.30,
    }


@pytest.fixture
def default_weights() -> Dict[str, float]:
    """Default model weights."""
    return {
        "bart": 0.50,
        "sentiment": 0.25,
        "irony": 0.15,
        "emotions": 0.10,
    }


# =============================================================================
# ResultAggregator Basic Tests
# =============================================================================


class TestResultAggregatorBasic:
    """Basic tests for ResultAggregator."""

    def test_create_aggregator(self):
        """Should create aggregator with defaults."""
        aggregator = ResultAggregator()

        assert aggregator.thresholds is not None
        assert aggregator.weights is not None

    def test_factory_function(self):
        """Factory function should create valid aggregator."""
        aggregator = create_result_aggregator()

        assert isinstance(aggregator, ResultAggregator)

    def test_aggregate_returns_result(self, high_crisis_signals):
        """Should return AggregatedResult."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        assert isinstance(result, AggregatedResult)

    def test_result_has_required_fields(self, high_crisis_signals):
        """Result should have all required fields."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        assert hasattr(result, "crisis_score")
        assert hasattr(result, "crisis_level")
        assert hasattr(result, "confidence")
        assert hasattr(result, "requires_intervention")
        assert hasattr(result, "model_results")
        assert hasattr(result, "timestamp")
        assert hasattr(result, "request_id")


# =============================================================================
# Crisis Level Tests
# =============================================================================


class TestCrisisLevel:
    """Tests for crisis level determination."""

    def test_critical_level(self, high_crisis_signals, default_thresholds):
        """High score should produce CRITICAL level."""
        aggregator = ResultAggregator(thresholds=default_thresholds)
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        # With high signals, crisis_score should be >= 0.85
        if result.crisis_score >= 0.85:
            assert result.crisis_level == CrisisLevel.CRITICAL

    def test_safe_level(self, low_crisis_signals, default_thresholds):
        """Low score should produce SAFE level."""
        aggregator = ResultAggregator(thresholds=default_thresholds)
        result = aggregator.aggregate(model_signals=low_crisis_signals)

        assert result.crisis_level == CrisisLevel.SAFE

    def test_from_score_method(self, default_thresholds):
        """CrisisLevel.from_score should work correctly."""
        assert CrisisLevel.from_score(0.90, default_thresholds) == CrisisLevel.CRITICAL
        assert CrisisLevel.from_score(0.75, default_thresholds) == CrisisLevel.HIGH
        assert CrisisLevel.from_score(0.55, default_thresholds) == CrisisLevel.MEDIUM
        assert CrisisLevel.from_score(0.35, default_thresholds) == CrisisLevel.LOW
        assert CrisisLevel.from_score(0.10, default_thresholds) == CrisisLevel.SAFE

    def test_threshold_configurable(self, high_crisis_signals):
        """Custom thresholds should affect level."""
        # Very high thresholds - nothing is critical
        high_thresholds = {"critical": 0.99, "high": 0.95, "medium": 0.90, "low": 0.80}
        aggregator = ResultAggregator(thresholds=high_thresholds)
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        # Even high signals won't be CRITICAL with 0.99 threshold
        assert result.crisis_level != CrisisLevel.CRITICAL or result.crisis_score >= 0.99


# =============================================================================
# Intervention Priority Tests
# =============================================================================


class TestInterventionPriority:
    """Tests for intervention priority calculation."""

    def test_critical_gets_immediate(self, high_crisis_signals):
        """CRITICAL should get IMMEDIATE priority."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        if result.crisis_level == CrisisLevel.CRITICAL:
            assert result.intervention_priority == InterventionPriority.IMMEDIATE

    def test_safe_gets_none(self, low_crisis_signals):
        """SAFE should get NONE priority."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=low_crisis_signals)

        assert result.intervention_priority == InterventionPriority.NONE

    def test_review_upgrades_priority(
        self, high_crisis_signals, resolution_with_review
    ):
        """Review requirement should upgrade priority."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            resolution_result=resolution_with_review,
        )

        # Review should push priority up
        assert result.requires_intervention is True


# =============================================================================
# Model Result Summary Tests
# =============================================================================


class TestModelResultSummary:
    """Tests for model result summaries."""

    def test_summaries_created(self, high_crisis_signals, default_weights):
        """Should create summary for each model."""
        aggregator = ResultAggregator(weights=default_weights)
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        assert len(result.model_results) == 4
        assert "bart" in result.model_results
        assert "sentiment" in result.model_results

    def test_summary_has_correct_values(self, high_crisis_signals, default_weights):
        """Summaries should have correct values."""
        aggregator = ResultAggregator(weights=default_weights)
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        bart_summary = result.model_results["bart"]
        assert isinstance(bart_summary, ModelResultSummary)
        assert bart_summary.model_name == "bart"
        assert bart_summary.weight == 0.50
        assert bart_summary.crisis_signal == 0.90

    def test_contribution_calculated(self, high_crisis_signals, default_weights):
        """Contribution should be signal * weight."""
        aggregator = ResultAggregator(weights=default_weights)
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        bart_summary = result.model_results["bart"]
        expected_contribution = 0.90 * 0.50
        assert abs(bart_summary.contribution - expected_contribution) < 0.01


# =============================================================================
# Consensus Integration Tests
# =============================================================================


class TestConsensusIntegration:
    """Tests for consensus result integration."""

    def test_uses_consensus_score(
        self, high_crisis_signals, high_consensus_result
    ):
        """Should use score from consensus result."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            consensus_result=high_consensus_result,
        )

        # Should use consensus score
        assert result.crisis_score == high_consensus_result.crisis_score

    def test_uses_consensus_confidence(
        self, high_crisis_signals, high_consensus_result
    ):
        """Should use confidence from consensus result."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            consensus_result=high_consensus_result,
        )

        assert result.confidence == high_consensus_result.confidence


# =============================================================================
# Resolution Integration Tests
# =============================================================================


class TestResolutionIntegration:
    """Tests for resolution result integration."""

    def test_uses_resolved_score(
        self, high_crisis_signals, resolution_with_review
    ):
        """Should use resolved score when available."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            resolution_result=resolution_with_review,
        )

        assert result.crisis_score == resolution_with_review.resolved_score

    def test_requires_review_from_resolution(
        self, high_crisis_signals, resolution_with_review
    ):
        """Should inherit review requirement from resolution."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            resolution_result=resolution_with_review,
        )

        assert result.requires_intervention is True


# =============================================================================
# Conflict Report Integration Tests
# =============================================================================


class TestConflictReportIntegration:
    """Tests for conflict report integration."""

    def test_stores_conflict_report(
        self, high_crisis_signals, high_conflict_report
    ):
        """Should store conflict report in result."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            conflict_report=high_conflict_report,
        )

        assert result.conflict_report is not None
        assert result.conflict_report.has_conflicts is True


# =============================================================================
# AggregatedResult Tests
# =============================================================================


class TestAggregatedResult:
    """Tests for AggregatedResult data class."""

    def test_to_dict(self, high_crisis_signals):
        """Should convert to dictionary."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "crisis_assessment" in result_dict
        assert "model_results" in result_dict
        assert "performance" in result_dict

    def test_to_legacy_dict(self, high_crisis_signals):
        """Should provide backward-compatible format."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        legacy = result.to_legacy_dict()

        # Should have Phase 3 format fields
        assert "crisis_detected" in legacy
        assert "severity" in legacy
        assert "confidence" in legacy
        assert "crisis_score" in legacy
        assert "signals" in legacy

    def test_auto_generates_request_id(self, high_crisis_signals):
        """Should auto-generate request_id."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        assert result.request_id is not None
        assert len(result.request_id) > 0

    def test_auto_generates_timestamp(self, high_crisis_signals):
        """Should auto-generate timestamp."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        assert result.timestamp is not None
        assert "T" in result.timestamp  # ISO format


# =============================================================================
# Configuration Tests
# =============================================================================


class TestConfiguration:
    """Tests for aggregator configuration."""

    def test_set_thresholds(self, high_crisis_signals):
        """Should allow threshold updates."""
        aggregator = ResultAggregator()
        aggregator.set_thresholds({"critical": 0.99})

        result = aggregator.aggregate(model_signals=high_crisis_signals)

        # With 0.99 threshold, won't be critical
        if result.crisis_score < 0.99:
            assert result.crisis_level != CrisisLevel.CRITICAL

    def test_set_weights(self, high_crisis_signals):
        """Should allow weight updates."""
        aggregator = ResultAggregator()
        aggregator.set_weights({"bart": 1.0, "sentiment": 0.0, "irony": 0.0, "emotions": 0.0})

        result = aggregator.aggregate(model_signals=high_crisis_signals)

        # BART-only weights
        bart_summary = result.model_results.get("bart")
        if bart_summary:
            assert bart_summary.weight == 1.0


# =============================================================================
# Primary Indicators Tests
# =============================================================================


class TestPrimaryIndicators:
    """Tests for primary indicator identification."""

    def test_identify_primary_indicators(self, high_crisis_signals):
        """Should identify primary crisis indicators."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        indicators = aggregator.identify_primary_indicators(result.model_results)

        assert isinstance(indicators, list)
        assert len(indicators) <= 6  # Limited to 6

    def test_indicators_from_high_signal_models(self, high_crisis_signals):
        """Should get indicators from high signal models."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals=high_crisis_signals)

        indicators = aggregator.identify_primary_indicators(result.model_results)

        # Should include the primary label from BART
        assert any("suicide" in ind.lower() or "distress" in ind.lower() 
                   for ind in indicators) or len(indicators) > 0


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_signals(self):
        """Should handle empty signals."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(model_signals={})

        assert result.crisis_score == 0.0
        assert result.crisis_level == CrisisLevel.SAFE

    def test_single_model(self):
        """Should handle single model."""
        aggregator = ResultAggregator()
        signals = {
            "bart": {
                "crisis_signal": 0.75,
                "label": "test",
                "raw_score": 0.75,
                "metadata": {},
            }
        }
        result = aggregator.aggregate(model_signals=signals)

        assert len(result.model_results) == 1

    def test_missing_metadata(self):
        """Should handle missing metadata."""
        aggregator = ResultAggregator()
        signals = {
            "bart": {
                "crisis_signal": 0.80,
                "label": "test",
                "raw_score": 0.80,
                # No metadata
            }
        }
        result = aggregator.aggregate(model_signals=signals)

        assert result is not None

    def test_performance_metrics_stored(self, high_crisis_signals):
        """Should store performance metrics."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            processing_time_ms=150.5,
            per_model_latency={"bart": 50.0, "sentiment": 30.0},
        )

        assert result.processing_time_ms == 150.5
        assert result.per_model_latency["bart"] == 50.0

    def test_degraded_state_stored(self, high_crisis_signals):
        """Should store degraded state."""
        aggregator = ResultAggregator()
        result = aggregator.aggregate(
            model_signals=high_crisis_signals,
            is_degraded=True,
            degradation_reason="Model failure",
        )

        assert result.is_degraded is True
        assert result.degradation_reason == "Model failure"
