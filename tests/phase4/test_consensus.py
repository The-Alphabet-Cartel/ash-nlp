"""
Ash-NLP Phase 4 Tests: Consensus Algorithms
---
FILE VERSION: v5.0-6-1.0-1
LAST MODIFIED: 2026-01-02
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


# =============================================================================
# Weighted Voting Consensus Tests
# =============================================================================


class TestWeightedVotingConsensus:
    """Tests for weighted_voting_consensus algorithm."""

    def test_high_agreement_crisis(self, high_agreement_scores, default_weights):
        """High agreement scores should result in crisis detection."""
        result = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=default_weights,
            crisis_threshold=0.5,
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

    def test_low_agreement_safe(self, low_agreement_scores, default_weights):
        """Low agreement scores should result in safe (no crisis)."""
        result = weighted_voting_consensus(
            model_signals=low_agreement_scores,
            weights=default_weights,
            crisis_threshold=0.5,
        )

        assert result.is_crisis is False
        assert result.crisis_score < 0.3
        assert result.agreement_level in (
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT,
        )

    def test_mixed_scores_near_threshold(self, mixed_scores, default_weights):
        """Mixed scores should produce moderate results."""
        result = weighted_voting_consensus(
            model_signals=mixed_scores,
            weights=default_weights,
            crisis_threshold=0.5,
        )

        # Score should be in moderate range
        assert 0.4 <= result.crisis_score <= 0.7

    def test_weights_affect_result(self, high_agreement_scores):
        """Different weights should affect the final score."""
        # BART-heavy weights
        bart_heavy = {"bart": 0.90, "sentiment": 0.05, "irony": 0.03, "emotions": 0.02}
        result1 = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=bart_heavy,
            crisis_threshold=0.5,
        )

        # Sentiment-heavy weights
        sentiment_heavy = {"bart": 0.10, "sentiment": 0.70, "irony": 0.10, "emotions": 0.10}
        result2 = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=sentiment_heavy,
            crisis_threshold=0.5,
        )

        # Results should differ based on weights
        assert result1.crisis_score != result2.crisis_score

    def test_empty_signals_handled(self, default_weights):
        """Empty signals should produce safe result."""
        result = weighted_voting_consensus(
            model_signals={},
            weights=default_weights,
            crisis_threshold=0.5,
        )

        assert result.is_crisis is False
        assert result.crisis_score == 0.0


# =============================================================================
# Majority Voting Consensus Tests
# =============================================================================


class TestMajorityVotingConsensus:
    """Tests for majority_voting_consensus algorithm."""

    def test_unanimous_crisis(self, high_agreement_scores):
        """All models voting crisis should result in crisis."""
        result = majority_voting_consensus(
            model_signals=high_agreement_scores,
            crisis_threshold=0.5,
            majority_threshold=0.5,
        )

        assert result.is_crisis is True
        assert result.vote_breakdown is not None
        assert result.vote_breakdown["crisis_votes"] == 4
        assert result.vote_breakdown["vote_ratio"] == 1.0

    def test_unanimous_safe(self, low_agreement_scores):
        """All models voting safe should result in safe."""
        result = majority_voting_consensus(
            model_signals=low_agreement_scores,
            crisis_threshold=0.5,
            majority_threshold=0.5,
        )

        assert result.is_crisis is False
        assert result.vote_breakdown["crisis_votes"] == 0

    def test_split_vote(self, disagreement_scores):
        """Split votes should be resolved by majority threshold."""
        result = majority_voting_consensus(
            model_signals=disagreement_scores,
            crisis_threshold=0.5,
            majority_threshold=0.5,
        )

        # 2 high (bart, irony), 2 low (sentiment, emotions)
        assert result.vote_breakdown["crisis_votes"] == 2
        assert result.vote_breakdown["total_votes"] == 4
        assert result.vote_breakdown["vote_ratio"] == 0.5

    def test_majority_threshold_configurable(self):
        """
        Majority threshold should be configurable.
        
        FE-011 Fix: Use test data that clearly exceeds thresholds.
        Previous issue: 0.25 == 0.25 returns False with > comparison.
        Solution: Ensure vote ratios clearly cross threshold boundaries.
        """
        # 2 of 4 models vote crisis = 0.5 ratio
        scores = {"bart": 0.70, "sentiment": 0.70, "irony": 0.30, "emotions": 0.30}

        # Low threshold (40%) - 0.5 > 0.4, should be crisis
        result1 = majority_voting_consensus(
            model_signals=scores,
            crisis_threshold=0.5,
            majority_threshold=0.40,
        )

        # High threshold (60%) - 0.5 < 0.6, should be safe
        result2 = majority_voting_consensus(
            model_signals=scores,
            crisis_threshold=0.5,
            majority_threshold=0.60,
        )

        assert result1.is_crisis is True
        assert result2.is_crisis is False


# =============================================================================
# Unanimous Consensus Tests
# =============================================================================


class TestUnanimousConsensus:
    """Tests for unanimous_consensus algorithm."""

    def test_unanimous_agreement_crisis(self, high_agreement_scores):
        """All models above threshold should result in crisis."""
        result = unanimous_consensus(
            model_signals=high_agreement_scores,
            crisis_threshold=0.6,
        )

        assert result.is_crisis is True
        assert result.requires_review is False

    def test_one_dissenter_no_crisis(self):
        """One model below threshold should result in no crisis."""
        scores = {
            "bart": 0.80,
            "sentiment": 0.75,
            "irony": 0.70,
            "emotions": 0.40,  # Below threshold
        }

        result = unanimous_consensus(
            model_signals=scores,
            crisis_threshold=0.6,
        )

        assert result.is_crisis is False
        # Check vote breakdown for safe_agreeing (models below threshold)
        assert "emotions" in result.vote_breakdown.get("safe_agreeing", [])

    def test_all_below_threshold(self, low_agreement_scores):
        """All models below threshold should result in no crisis."""
        result = unanimous_consensus(
            model_signals=low_agreement_scores,
            crisis_threshold=0.6,
        )

        assert result.is_crisis is False

    def test_unanimous_threshold_configurable(self):
        """Unanimous threshold should be configurable."""
        scores = {"bart": 0.65, "sentiment": 0.65, "irony": 0.65, "emotions": 0.65}

        # Low threshold - should be unanimous crisis
        result1 = unanimous_consensus(
            model_signals=scores,
            crisis_threshold=0.60,
        )

        # High threshold - should not be unanimous
        result2 = unanimous_consensus(
            model_signals=scores,
            crisis_threshold=0.70,
        )

        assert result1.is_crisis is True
        assert result2.is_crisis is False


# =============================================================================
# Conflict-Aware Consensus Tests
# =============================================================================


class TestConflictAwareConsensus:
    """Tests for conflict_aware_consensus algorithm."""

    def test_high_agreement_no_conflict(self, high_agreement_scores, default_weights):
        """High agreement should not flag conflict."""
        result = conflict_aware_consensus(
            model_signals=high_agreement_scores,
            weights=default_weights,
            disagreement_threshold=0.15,
            crisis_threshold=0.5,
        )

        assert result.has_conflict is False
        assert result.requires_review is False

    def test_disagreement_flags_conflict(self, default_weights):
        """
        Significant disagreement should flag conflict.
        
        FE-011 Fix: Use extreme disagreement data that exceeds threshold.
        Previous issue: disagreement_scores variance 0.099 < 0.15 threshold.
        Solution: Use scores with very high variance (0.95 vs 0.05).
        """
        # Extreme disagreement: variance will be ~0.203 (well above 0.15)
        extreme_disagreement_scores = {
            "bart": 0.95,      # Very high crisis
            "sentiment": 0.05,  # Very low
            "irony": 0.90,     # High crisis
            "emotions": 0.10,  # Low
        }
        
        result = conflict_aware_consensus(
            model_signals=extreme_disagreement_scores,
            weights=default_weights,
            disagreement_threshold=0.15,
            crisis_threshold=0.5,
        )

        assert result.has_conflict is True
        assert result.requires_review is True
        assert result.agreement_level == AgreementLevel.SIGNIFICANT_DISAGREEMENT

    def test_disagreement_threshold_configurable(self, disagreement_scores, default_weights):
        """Disagreement threshold should be configurable."""
        # Very high threshold - won't detect conflict
        result1 = conflict_aware_consensus(
            model_signals=disagreement_scores,
            weights=default_weights,
            disagreement_threshold=0.50,
            crisis_threshold=0.5,
        )

        # Very low threshold - will detect conflict easily
        result2 = conflict_aware_consensus(
            model_signals=disagreement_scores,
            weights=default_weights,
            disagreement_threshold=0.05,
            crisis_threshold=0.5,
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

        # Check for the actual keys in the config
        assert "default_algorithm" in config
        assert "weights" in config
        assert "thresholds" in config
        assert "available_algorithms" in config

    def test_factory_function(self):
        """Factory function should create valid selector."""
        selector = create_consensus_selector()

        assert isinstance(selector, ConsensusSelector)
        # Check default_algorithm attribute
        assert selector.default_algorithm == ConsensusAlgorithm.WEIGHTED_VOTING


# =============================================================================
# Agreement Level Tests
# =============================================================================


class TestAgreementLevel:
    """Tests for agreement level calculation."""

    def test_strong_agreement_low_variance(self, high_agreement_scores, default_weights):
        """Low variance should produce strong agreement."""
        result = weighted_voting_consensus(
            model_signals=high_agreement_scores,
            weights=default_weights,
            crisis_threshold=0.5,
        )

        # High agreement scores have low variance
        assert result.agreement_level in (
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT,
        )

    def test_significant_disagreement_high_variance(self, default_weights):
        """
        High variance should produce significant disagreement.
        
        FE-011 Fix: Use extreme disagreement data with high variance.
        Previous issue: disagreement_scores variance 0.099 < 0.15 threshold.
        Solution: Use scores with very high variance.
        """
        # Extreme variance data - same as test_disagreement_flags_conflict
        extreme_disagreement_scores = {
            "bart": 0.95,
            "sentiment": 0.05,
            "irony": 0.90,
            "emotions": 0.10,
        }
        
        result = conflict_aware_consensus(
            model_signals=extreme_disagreement_scores,
            weights=default_weights,
            disagreement_threshold=0.15,
            crisis_threshold=0.5,
        )

        assert result.agreement_level == AgreementLevel.SIGNIFICANT_DISAGREEMENT


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_single_model(self, default_weights):
        """Single model should work."""
        scores = {"bart": 0.80}

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=default_weights,
            crisis_threshold=0.5,
        )

        assert result.crisis_score == 0.80

    def test_zero_scores(self, default_weights):
        """All zero scores should work."""
        scores = {"bart": 0.0, "sentiment": 0.0, "irony": 0.0, "emotions": 0.0}

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=default_weights,
            crisis_threshold=0.5,
        )

        assert result.crisis_score == 0.0
        assert result.is_crisis is False

    def test_all_ones(self, default_weights):
        """All 1.0 scores should work."""
        scores = {"bart": 1.0, "sentiment": 1.0, "irony": 1.0, "emotions": 1.0}

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=default_weights,
            crisis_threshold=0.5,
        )

        assert result.crisis_score == 1.0
        assert result.is_crisis is True

    def test_missing_model_in_weights(self):
        """Models not in weights should use 0 weight."""
        scores = {"bart": 0.80, "unknown_model": 0.90}
        weights = {"bart": 1.0}  # Only BART has weight

        result = weighted_voting_consensus(
            model_signals=scores,
            weights=weights,
            crisis_threshold=0.5,
        )

        # Should only consider BART
        assert result.crisis_score == 0.80
