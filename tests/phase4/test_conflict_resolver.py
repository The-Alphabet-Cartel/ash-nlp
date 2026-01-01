"""
Ash-NLP Phase 4 Tests: Conflict Resolution
---
FILE VERSION: v5.0-4-TEST-2.6
LAST MODIFIED: 2026-01-01
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- ConflictResolver class
- Resolution strategies: conservative, optimistic, mean, review_flag
- Alerting integration
"""

import pytest
from typing import Dict
from unittest.mock import AsyncMock, MagicMock

from src.ensemble.conflict_resolver import (
    # Enums
    ResolutionStrategy,
    # Data classes
    ResolutionResult,
    # Resolver
    ConflictResolver,
    create_conflict_resolver,
)
from src.ensemble.conflict_detector import (
    ConflictType,
    ConflictSeverity,
    DetectedConflict,
    ConflictReport,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def conflict_scores() -> Dict[str, float]:
    """Crisis scores with disagreement."""
    return {
        "bart": 0.90,
        "sentiment": 0.30,
        "irony": 0.80,
        "emotions": 0.40,
    }


@pytest.fixture
def agreeing_scores() -> Dict[str, float]:
    """Crisis scores with agreement."""
    return {
        "bart": 0.75,
        "sentiment": 0.72,
        "irony": 0.78,
        "emotions": 0.70,
    }


@pytest.fixture
def no_conflict_report() -> ConflictReport:
    """Report with no conflicts."""
    return ConflictReport(
        has_conflicts=False,
        conflict_count=0,
        conflicts=[],
        highest_severity=None,
        requires_review=False,
        summary="No conflicts detected",
    )


@pytest.fixture
def high_conflict_report() -> ConflictReport:
    """Report with high severity conflict."""
    conflict = DetectedConflict(
        conflict_type=ConflictType.SCORE_DISAGREEMENT,
        severity=ConflictSeverity.HIGH,
        description="Significant score disagreement",
        involved_models=["bart", "sentiment"],
        details={"score_range": 0.60},
    )
    return ConflictReport(
        has_conflicts=True,
        conflict_count=1,
        conflicts=[conflict],
        highest_severity=ConflictSeverity.HIGH,
        requires_review=True,
        summary="1 conflict: score_disagreement",
    )


@pytest.fixture
def medium_conflict_report() -> ConflictReport:
    """Report with medium severity conflict."""
    conflict = DetectedConflict(
        conflict_type=ConflictType.IRONY_SENTIMENT_CONFLICT,
        severity=ConflictSeverity.MEDIUM,
        description="Irony-sentiment conflict",
        involved_models=["sentiment", "irony"],
    )
    return ConflictReport(
        has_conflicts=True,
        conflict_count=1,
        conflicts=[conflict],
        highest_severity=ConflictSeverity.MEDIUM,
        requires_review=False,
        summary="1 conflict: irony_sentiment_conflict",
    )


# =============================================================================
# ConflictResolver Basic Tests
# =============================================================================


class TestConflictResolverBasic:
    """Basic tests for ConflictResolver."""

    def test_create_resolver(self):
        """Should create resolver with defaults."""
        resolver = ConflictResolver()

        assert resolver.default_strategy == ResolutionStrategy.CONSERVATIVE

    def test_factory_function(self):
        """Factory function should create valid resolver."""
        resolver = create_conflict_resolver()

        assert isinstance(resolver, ConflictResolver)
        assert resolver.default_strategy == ResolutionStrategy.CONSERVATIVE

    def test_no_conflict_returns_original(
        self, agreeing_scores, no_conflict_report
    ):
        """Should return original score when no conflicts."""
        resolver = ConflictResolver()
        result = resolver.resolve(
            crisis_scores=agreeing_scores,
            conflict_report=no_conflict_report,
        )

        assert isinstance(result, ResolutionResult)
        assert result.was_modified is False
        assert result.requires_review is False

    def test_get_config(self):
        """Should return current configuration."""
        resolver = ConflictResolver(
            default_strategy=ResolutionStrategy.OPTIMISTIC,
            alert_on_high_severity=False,
        )
        config = resolver.get_config()

        assert config["default_strategy"] == "optimistic"
        assert config["alert_on_high_severity"] is False


# =============================================================================
# Conservative Strategy Tests
# =============================================================================


class TestConservativeStrategy:
    """Tests for conservative resolution strategy."""

    def test_uses_highest_score(self, conflict_scores, high_conflict_report):
        """Conservative should use highest crisis score."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.CONSERVATIVE)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        # Highest score is bart at 0.90
        assert result.resolved_score == 0.90
        assert result.strategy_used == ResolutionStrategy.CONSERVATIVE

    def test_identifies_max_model(self, conflict_scores, high_conflict_report):
        """Should identify which model provided max score."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.CONSERVATIVE)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        assert result.metadata.get("max_model") == "bart"
        assert result.metadata.get("max_score") == 0.90


# =============================================================================
# Optimistic Strategy Tests
# =============================================================================


class TestOptimisticStrategy:
    """Tests for optimistic resolution strategy."""

    def test_uses_lowest_score(self, conflict_scores, high_conflict_report):
        """Optimistic should use lowest crisis score."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.OPTIMISTIC)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        # Lowest score is sentiment at 0.30
        assert result.resolved_score == 0.30
        assert result.strategy_used == ResolutionStrategy.OPTIMISTIC

    def test_always_requires_review(self, conflict_scores, high_conflict_report):
        """Optimistic should always require review."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.OPTIMISTIC)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        assert result.requires_review is True


# =============================================================================
# Mean Strategy Tests
# =============================================================================


class TestMeanStrategy:
    """Tests for mean resolution strategy."""

    def test_uses_average_score(self, conflict_scores, high_conflict_report):
        """Mean should use average of all scores."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.MEAN)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        # Average: (0.90 + 0.30 + 0.80 + 0.40) / 4 = 0.60
        expected_mean = (0.90 + 0.30 + 0.80 + 0.40) / 4
        assert abs(result.resolved_score - expected_mean) < 0.01
        assert result.strategy_used == ResolutionStrategy.MEAN

    def test_not_modified_flag(self, agreeing_scores, high_conflict_report):
        """Mean shouldn't change score if already average."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.MEAN)
        result = resolver.resolve(
            crisis_scores=agreeing_scores,
            conflict_report=high_conflict_report,
        )

        # Original score is already the mean
        assert result.was_modified is False


# =============================================================================
# Review Flag Strategy Tests
# =============================================================================


class TestReviewFlagStrategy:
    """Tests for review flag resolution strategy."""

    def test_uses_conservative_interim(self, conflict_scores, high_conflict_report):
        """Review flag should use conservative as interim."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.REVIEW_FLAG)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        # Uses highest (conservative) as interim
        assert result.resolved_score == 0.90
        assert result.strategy_used == ResolutionStrategy.REVIEW_FLAG

    def test_always_requires_review(self, conflict_scores, high_conflict_report):
        """Review flag should always require review."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.REVIEW_FLAG)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        assert result.requires_review is True


# =============================================================================
# Strategy Override Tests
# =============================================================================


class TestStrategyOverride:
    """Tests for strategy override in resolve()."""

    def test_override_strategy(self, conflict_scores, high_conflict_report):
        """Should allow strategy override per call."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.CONSERVATIVE)

        # Override to optimistic
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
            strategy=ResolutionStrategy.OPTIMISTIC,
        )

        assert result.strategy_used == ResolutionStrategy.OPTIMISTIC
        assert result.resolved_score == 0.30  # Lowest score

    def test_default_used_when_no_override(self, conflict_scores, high_conflict_report):
        """Should use default when no override."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.MEAN)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        assert result.strategy_used == ResolutionStrategy.MEAN


# =============================================================================
# Strategy Setting Tests
# =============================================================================


class TestStrategySettings:
    """Tests for strategy configuration."""

    def test_set_strategy(self, conflict_scores, high_conflict_report):
        """set_strategy should change default."""
        resolver = ConflictResolver(default_strategy=ResolutionStrategy.CONSERVATIVE)
        resolver.set_strategy(ResolutionStrategy.OPTIMISTIC)

        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        assert result.strategy_used == ResolutionStrategy.OPTIMISTIC


# =============================================================================
# Alerting Tests
# =============================================================================


class TestAlerting:
    """Tests for Discord alerting integration."""

    def test_no_alert_without_alerter(self, conflict_scores, high_conflict_report):
        """Should not alert when no alerter configured."""
        resolver = ConflictResolver(alerter=None)
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        assert result.alert_sent is False

    def test_alert_config_in_result(self, conflict_scores, high_conflict_report):
        """Alert configuration should be accessible."""
        resolver = ConflictResolver(
            alert_on_high_severity=True,
            alert_on_review_flag=False,
        )
        config = resolver.get_config()

        assert config["alert_on_high_severity"] is True
        assert config["alert_on_review_flag"] is False


# =============================================================================
# Resolution Result Tests
# =============================================================================


class TestResolutionResult:
    """Tests for ResolutionResult data class."""

    def test_to_dict(self, conflict_scores, high_conflict_report):
        """Should convert to dictionary."""
        resolver = ConflictResolver()
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "strategy_used" in result_dict
        assert "original_score" in result_dict
        assert "resolved_score" in result_dict
        assert "was_modified" in result_dict
        assert "requires_review" in result_dict

    def test_scores_rounded(self, conflict_scores, high_conflict_report):
        """Scores should be rounded in dict."""
        resolver = ConflictResolver()
        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
        )

        result_dict = result.to_dict()

        # Should be rounded to 4 decimal places
        assert len(str(result_dict["original_score"]).split(".")[-1]) <= 4


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_single_model_score(self, high_conflict_report):
        """Should handle single model score."""
        scores = {"bart": 0.75}
        resolver = ConflictResolver()
        result = resolver.resolve(
            crisis_scores=scores,
            conflict_report=high_conflict_report,
        )

        assert result.resolved_score == 0.75

    def test_empty_scores(self, high_conflict_report):
        """Should handle empty scores gracefully."""
        resolver = ConflictResolver()
        
        # Empty scores with conflict report
        result = resolver.resolve(
            crisis_scores={},
            conflict_report=high_conflict_report,
        )

        # Should return 0.0 for empty
        assert result.original_score == 0.0

    def test_all_same_scores(self, high_conflict_report):
        """Should handle all identical scores."""
        scores = {"bart": 0.50, "sentiment": 0.50, "irony": 0.50, "emotions": 0.50}
        resolver = ConflictResolver()
        result = resolver.resolve(
            crisis_scores=scores,
            conflict_report=high_conflict_report,
        )

        # All strategies should produce 0.50
        assert result.resolved_score == 0.50

    def test_message_preview_truncation(self, conflict_scores, high_conflict_report):
        """Should handle long message preview."""
        resolver = ConflictResolver()
        long_message = "A" * 200

        result = resolver.resolve(
            crisis_scores=conflict_scores,
            conflict_report=high_conflict_report,
            message_preview=long_message,
        )

        # Should complete without error
        assert result is not None


# =============================================================================
# Statistics Tests
# =============================================================================


class TestStatistics:
    """Tests for resolution statistics."""

    def test_get_stats(self):
        """Should return stats dictionary."""
        resolver = ConflictResolver()
        stats = resolver.get_stats()

        assert "total_alerts_sent" in stats
        assert stats["total_alerts_sent"] == 0

    def test_alerter_configured_in_stats(self):
        """Should indicate alerter status in stats."""
        resolver = ConflictResolver(alerter=None)
        stats = resolver.get_stats()

        assert stats["alerter_configured"] is False
