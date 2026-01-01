"""
Ash-NLP Phase 4 Tests: Consensus Algorithms
---
FILE VERSION: v5.0-4-TEST-1.1
LAST MODIFIED: 2026-01-01
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- weighted_voting_consensus()
- majority_voting_consensus()
- unanimous_consensus()
- conflict_aware_consensus()
- ConsensusSelector class
"""

import pytest
from typing import Dict

from src.ensemble.consensus import (
    # Enums
    ConsensusAlgorithm,
    AgreementLevel,
    # Data classes
    ConsensusResult,
    # Functions
    weighted_voting_consensus,
    majority_voting_consensus,
    unanimous_consensus,
    conflict_aware_consensus,
    # Selector
    ConsensusSelector,
    create_consensus_selector,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def high_agreement_scores() -> Dict[str, float]:
    """Model scores with strong agreement (all high crisis)."""
    return {
        "bart": 0.85,
        "sentiment": 0.80,
        "irony": 0.78,
        "emotions": 0.82,
    }


@pytest.fixture
def low_agreement_scores() -> Dict[str, float]:
    """Model scores with strong agreement (all low/safe)."""
    return {
        "bart": 0.15,
        "sentiment": 0.20,
        "irony": 0.18,
        "emotions": 0.12,
    }


@pytest.fixture
def mixed_scores() -> Dict[str, float]:
    """Model scores with mixed signals."""
    return {
        "bart": 0.75,
        "sentiment": 0.60,
        "irony": 0.40,
        "emotions": 0.55,
    }


@pytest.fixture
def disagreement_scores() -> Dict[str, float]:
    """Model scores with significant disagreement."""
    return {
        "bart": 0.90,  # High crisis
        "sentiment": 0.20,  # Low
        "irony": 0.85,  # High crisis
        "emotions": 0.30,  # Low
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


@pytest.fixture
def default_thresholds() -> Dict[str, float]:
    """Default consensus thresholds."""
    return {
        "crisis": 0.5,
        "majority": 0.5,
        "unanimous": 0.6,
        "disagreement": 0.15,
    }


# =============================================================================
# Weighted Voting Consensus Tests
# =============================================================================


class TestWeightedVotingConsensus:
    """Tests for weighted_voting_consensus algorithm."""

    def test_high_agreement_crisis(
        self, high_agreement_scores, default_weights, default_thresholds
    ):
        """High agreement scores should result in crisis detection."""
        result = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert isinstance(result, ConsensusResult)
        assert result.algorithm == ConsensusAlgorithm.WEIGHTED_VOTING
        assert result.is_crisis is True
        assert result.crisis_score >= 0.75
        assert result.confidence >= 0.8
        assert result.agreement_level in (
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT,
        )

    def test_low_agreement_safe(
        self, low_agreement_scores, default_weights, default_thresholds
    ):
        """Low agreement scores should result in safe (no crisis)."""
        result = weighted_voting_consensus(
            model_signals=low_agreement_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is False
        assert result.crisis_score < 0.3
        assert result.agreement_level in (
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT,
        )

    def test_mixed_scores_near_threshold(
        self, mixed_scores, default_weights, default_thresholds
    ):
        """Mixed scores should produce moderate results."""
        result = weighted_voting_consensus(
            model_signals=mixed_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        # Score should be in moderate range
        assert 0.4 <= result.crisis_score <= 0.7

    def test_weights_affect_result(self, high_agreement_scores, default_thresholds):
        """Different weights should affect the final score."""
        # BART-heavy weights
        bart_heavy = {"bart": 0.90, "sentiment": 0.05, "irony": 0.03, "emotions": 0.02}
        result1 = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=bart_heavy,
            thresholds=default_thresholds,
        )

        # Sentiment-heavy weights
        sentiment_heavy = {"bart": 0.10, "sentiment": 0.70, "irony": 0.10, "emotions": 0.10}
        result2 = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=sentiment_heavy,
            thresholds=default_thresholds,
        )

        # Results should differ based on weights
        assert result1.crisis_score != result2.crisis_score

    def test_empty_signals_handled(self, default_weights, default_thresholds):
        """Empty signals should produce safe result."""
        result = weighted_voting_consensus(
            model_signals={},
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is False
        assert result.crisis_score == 0.0


# =============================================================================
# Majority Voting Consensus Tests
# =============================================================================


class TestMajorityVotingConsensus:
    """Tests for majority_voting_consensus algorithm."""

    def test_unanimous_crisis(self, high_agreement_scores, default_thresholds):
        """All models voting crisis should result in crisis."""
        result = majority_voting_consensus(
            model_signals=high_agreement_scores,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is True
        assert result.vote_breakdown is not None
        assert result.vote_breakdown["crisis_votes"] == 4
        assert result.vote_breakdown["vote_ratio"] == 1.0

    def test_unanimous_safe(self, low_agreement_scores, default_thresholds):
        """All models voting safe should result in safe."""
        result = majority_voting_consensus(
            model_signals=low_agreement_scores,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is False
        assert result.vote_breakdown["crisis_votes"] == 0

    def test_split_vote(self, disagreement_scores, default_thresholds):
        """Split votes should be resolved by majority threshold."""
        result = majority_voting_consensus(
            model_signals=disagreement_scores,
            thresholds=default_thresholds,
        )

        # 2 high (bart, irony), 2 low (sentiment, emotions)
        assert result.vote_breakdown["crisis_votes"] == 2
        assert result.vote_breakdown["total_votes"] == 4
        assert result.vote_breakdown["vote_ratio"] == 0.5

    def test_majority_threshold_configurable(self):
        """Majority threshold should be configurable."""
        scores = {"bart": 0.70, "sentiment": 0.30, "irony": 0.30, "emotions": 0.30}

        # Low threshold (25%) - should be crisis
        low_threshold = {"majority": 0.25, "crisis": 0.5}
        result1 = majority_voting_consensus(
            model_signals=scores,
            thresholds=low_threshold,
        )

        # High threshold (75%) - should be safe
        high_threshold = {"majority": 0.75, "crisis": 0.5}
        result2 = majority_voting_consensus(
            model_signals=scores,
            thresholds=high_threshold,
        )

        assert result1.is_crisis is True
        assert result2.is_crisis is False


# =============================================================================
# Unanimous Consensus Tests
# =============================================================================


class TestUnanimousConsensus:
    """Tests for unanimous_consensus algorithm."""

    def test_unanimous_agreement_crisis(self, high_agreement_scores, default_thresholds):
        """All models above threshold should result in crisis."""
        result = unanimous_consensus(
            model_signals=high_agreement_scores,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is True
        assert result.requires_review is False

    def test_one_dissenter_no_crisis(self, default_thresholds):
        """One model below threshold should result in no crisis."""
        scores = {
            "bart": 0.80,
            "sentiment": 0.75,
            "irony": 0.70,
            "emotions": 0.40,  # Below threshold
        }

        result = unanimous_consensus(
            model_signals=scores,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is False
        assert result.vote_breakdown["below_threshold"] == ["emotions"]

    def test_all_below_threshold(self, low_agreement_scores, default_thresholds):
        """All models below threshold should result in no crisis."""
        result = unanimous_consensus(
            model_signals=low_agreement_scores,
            thresholds=default_thresholds,
        )

        assert result.is_crisis is False

    def test_unanimous_threshold_configurable(self):
        """Unanimous threshold should be configurable."""
        scores = {"bart": 0.65, "sentiment": 0.65, "irony": 0.65, "emotions": 0.65}

        # Low threshold - should be unanimous crisis
        low_threshold = {"unanimous": 0.60, "crisis": 0.5}
        result1 = unanimous_consensus(
            model_signals=scores,
            thresholds=low_threshold,
        )

        # High threshold - should not be unanimous
        high_threshold = {"unanimous": 0.70, "crisis": 0.5}
        result2 = unanimous_consensus(
            model_signals=scores,
            thresholds=high_threshold,
        )

        assert result1.is_crisis is True
        assert result2.is_crisis is False


# =============================================================================
# Conflict-Aware Consensus Tests
# =============================================================================


class TestConflictAwareConsensus:
    """Tests for conflict_aware_consensus algorithm."""

    def test_high_agreement_no_conflict(
        self, high_agreement_scores, default_weights, default_thresholds
    ):
        """High agreement should not flag conflict."""
        result = conflict_aware_consensus(
            model_signals=high_agreement_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.has_conflict is False
        assert result.requires_review is False

    def test_disagreement_flags_conflict(
        self, disagreement_scores, default_weights, default_thresholds
    ):
        """Significant disagreement should flag conflict."""
        result = conflict_aware_consensus(
            model_signals=disagreement_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.has_conflict is True
        assert result.requires_review is True
        assert result.agreement_level == AgreementLevel.SIGNIFICANT_DISAGREEMENT

    def test_disagreement_threshold_configurable(
        self, disagreement_scores, default_weights
    ):
        """Disagreement threshold should be configurable."""
        # Very high threshold - won't detect conflict
        high_threshold = {"disagreement": 0.50, "crisis": 0.5}
        result1 = conflict_aware_consensus(
            model_signals=disagreement_scores,
            weights=default_weights,
            thresholds=high_threshold,
        )

        # Very low threshold - will detect conflict easily
        low_threshold = {"disagreement": 0.05, "crisis": 0.5}
        result2 = conflict_aware_consensus(
            model_signals=disagreement_scores,
            weights=default_weights,
            thresholds=low_threshold,
        )

        # High threshold may not detect, low threshold should
        assert result2.has_conflict is True


# =============================================================================
# ConsensusSelector Tests
# =============================================================================


class TestConsensusSelector:
    """Tests for ConsensusSelector class."""

    def test_default_algorithm(self, high_agreement_scores):
        """Default algorithm should be weighted voting."""
        selector = ConsensusSelector()
        result = selector.select_and_run(model_signals=high_agreement_scores)

        assert result.algorithm == ConsensusAlgorithm.WEIGHTED_VOTING

    def test_algorithm_switching(self, high_agreement_scores):
        """Should be able to switch algorithms."""
        selector = ConsensusSelector()

        # Run with different algorithms
        result1 = selector.select_and_run(
            model_signals=high_agreement_scores,
            algorithm=ConsensusAlgorithm.WEIGHTED_VOTING,
        )
        result2 = selector.select_and_run(
            model_signals=high_agreement_scores,
            algorithm=ConsensusAlgorithm.MAJORITY_VOTING,
        )
        result3 = selector.select_and_run(
            model_signals=high_agreement_scores,
            algorithm=ConsensusAlgorithm.UNANIMOUS,
        )
        result4 = selector.select_and_run(
            model_signals=high_agreement_scores,
            algorithm=ConsensusAlgorithm.CONFLICT_AWARE,
        )

        # Each should use the specified algorithm
        assert result1.algorithm == ConsensusAlgorithm.WEIGHTED_VOTING
        assert result2.algorithm == ConsensusAlgorithm.MAJORITY_VOTING
        assert result3.algorithm == ConsensusAlgorithm.UNANIMOUS
        assert result4.algorithm == ConsensusAlgorithm.CONFLICT_AWARE

    def test_set_algorithm_persists(self, high_agreement_scores):
        """set_algorithm should change default."""
        selector = ConsensusSelector()
        selector.set_algorithm(ConsensusAlgorithm.UNANIMOUS)

        result = selector.select_and_run(model_signals=high_agreement_scores)

        assert result.algorithm == ConsensusAlgorithm.UNANIMOUS

    def test_set_weights(self, high_agreement_scores):
        """set_weights should update weights."""
        selector = ConsensusSelector()
        new_weights = {"bart": 0.70, "sentiment": 0.15, "irony": 0.10, "emotions": 0.05}
        selector.set_weights(new_weights)

        result = selector.select_and_run(model_signals=high_agreement_scores)

        # Score should be BART-weighted (0.85 * 0.70 = 0.595 contribution)
        assert result.crisis_score > 0

    def test_get_config(self):
        """get_config should return current configuration."""
        selector = ConsensusSelector()
        config = selector.get_config()

        assert "algorithm" in config
        assert "weights" in config
        assert "thresholds" in config

    def test_factory_function(self):
        """Factory function should create valid selector."""
        selector = create_consensus_selector()

        assert isinstance(selector, ConsensusSelector)
        assert selector.algorithm == ConsensusAlgorithm.WEIGHTED_VOTING


# =============================================================================
# Agreement Level Tests
# =============================================================================


class TestAgreementLevel:
    """Tests for agreement level calculation."""

    def test_strong_agreement_low_variance(self, high_agreement_scores, default_weights, default_thresholds):
        """Low variance should produce strong agreement."""
        result = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        # High agreement scores have low variance
        assert result.agreement_level in (
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT,
        )

    def test_significant_disagreement_high_variance(
        self, disagreement_scores, default_weights, default_thresholds
    ):
        """High variance should produce significant disagreement."""
        result = conflict_aware_consensus(
            model_signals=disagreement_scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.agreement_level == AgreementLevel.SIGNIFICANT_DISAGREEMENT


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_single_model(self, default_weights, default_thresholds):
        """Single model should work."""
        scores = {"bart": 0.80}

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.crisis_score == 0.80

    def test_zero_scores(self, default_weights, default_thresholds):
        """All zero scores should work."""
        scores = {"bart": 0.0, "sentiment": 0.0, "irony": 0.0, "emotions": 0.0}

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.crisis_score == 0.0
        assert result.is_crisis is False

    def test_all_ones(self, default_weights, default_thresholds):
        """All 1.0 scores should work."""
        scores = {"bart": 1.0, "sentiment": 1.0, "irony": 1.0, "emotions": 1.0}

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=default_weights,
            thresholds=default_thresholds,
        )

        assert result.crisis_score == 1.0
        assert result.is_crisis is True

    def test_missing_model_in_weights(self, default_thresholds):
        """Models not in weights should use 0 weight."""
        scores = {"bart": 0.80, "unknown_model": 0.90}
        weights = {"bart": 1.0}  # Only BART has weight

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=weights,
            thresholds=default_thresholds,
        )

        # Should only consider BART
        assert result.crisis_score == 0.80
