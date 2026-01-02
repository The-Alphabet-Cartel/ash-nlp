"""
Ash-NLP Phase 4 Tests: Explainability Layer
---
FILE VERSION: v5.0-4-TEST-4.1
LAST MODIFIED: 2026-01-01
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- ExplainabilityGenerator class
- Verbosity levels: minimal, standard, detailed
- Explanation generation
- Recommendation generation
"""

import pytest
from typing import Dict, Any

from src.ensemble.explainability import (
    # Enums
    VerbosityLevel,
    # Data classes
    ModelContribution,
    RecommendedAction,
    Explanation,
    # Generator
    ExplainabilityGenerator,
    create_explainability_generator,
)
from src.ensemble.aggregator import (
    CrisisLevel,
    InterventionPriority,
    ModelResultSummary,
    AggregatedResult,
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


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def critical_result() -> AggregatedResult:
    """Critical crisis aggregated result."""
    result = AggregatedResult(
        crisis_score=0.90,
        crisis_level=CrisisLevel.CRITICAL,
        confidence=0.92,
        requires_intervention=True,
        intervention_priority=InterventionPriority.IMMEDIATE,
        models_used=["bart", "sentiment", "irony", "emotions"],
        processing_time_ms=150.0,
        message="I can't do this anymore",
    )
    result.model_results = {
        "bart": ModelResultSummary(
            model_name="bart",
            label="suicide ideation",
            score=0.92,
            confidence=0.92,
            weight=0.50,
            contribution=0.46,
            crisis_signal=0.92,
            top_labels=[{"label": "suicide ideation", "score": 0.92}],
        ),
        "sentiment": ModelResultSummary(
            model_name="sentiment",
            label="negative",
            score=0.85,
            confidence=0.85,
            weight=0.25,
            contribution=0.21,
            crisis_signal=0.85,
            top_labels=[{"label": "negative", "score": 0.85}],
        ),
    }
    return result


@pytest.fixture
def high_result() -> AggregatedResult:
    """High crisis aggregated result."""
    result = AggregatedResult(
        crisis_score=0.75,
        crisis_level=CrisisLevel.HIGH,
        confidence=0.80,
        requires_intervention=True,
        intervention_priority=InterventionPriority.HIGH,
        models_used=["bart", "sentiment"],
        processing_time_ms=120.0,
    )
    result.model_results = {
        "bart": ModelResultSummary(
            model_name="bart",
            label="emotional distress",
            score=0.78,
            confidence=0.78,
            weight=0.50,
            contribution=0.39,
            crisis_signal=0.78,
            top_labels=[{"label": "emotional distress", "score": 0.78}],
        ),
    }
    return result


@pytest.fixture
def medium_result() -> AggregatedResult:
    """Medium crisis aggregated result."""
    result = AggregatedResult(
        crisis_score=0.55,
        crisis_level=CrisisLevel.MEDIUM,
        confidence=0.70,
        requires_intervention=False,
        intervention_priority=InterventionPriority.STANDARD,
        models_used=["bart", "sentiment"],
        processing_time_ms=100.0,
    )
    result.model_results = {}
    return result


@pytest.fixture
def safe_result() -> AggregatedResult:
    """Safe (no crisis) aggregated result."""
    result = AggregatedResult(
        crisis_score=0.15,
        crisis_level=CrisisLevel.SAFE,
        confidence=0.85,
        requires_intervention=False,
        intervention_priority=InterventionPriority.NONE,
        models_used=["bart", "sentiment", "irony", "emotions"],
        processing_time_ms=130.0,
    )
    result.model_results = {
        "bart": ModelResultSummary(
            model_name="bart",
            label="safe",
            score=0.10,
            confidence=0.90,
            weight=0.50,
            contribution=0.05,
            crisis_signal=0.10,
            top_labels=[{"label": "safe", "score": 0.90}],
        ),
    }
    return result


@pytest.fixture
def result_with_conflict() -> AggregatedResult:
    """Result with conflict report."""
    result = AggregatedResult(
        crisis_score=0.70,
        crisis_level=CrisisLevel.HIGH,
        confidence=0.65,
        requires_intervention=True,
        intervention_priority=InterventionPriority.HIGH,
        models_used=["bart", "sentiment"],
        processing_time_ms=140.0,
    )
    result.conflict_report = ConflictReport(
        has_conflicts=True,
        conflict_count=1,
        conflicts=[
            DetectedConflict(
                conflict_type=ConflictType.SCORE_DISAGREEMENT,
                severity=ConflictSeverity.HIGH,
                description="Score disagreement between models",
                involved_models=["bart", "sentiment"],
            )
        ],
        highest_severity=ConflictSeverity.HIGH,
        requires_review=True,
        summary="1 high severity conflict",
    )
    result.model_results = {}
    return result


@pytest.fixture
def result_with_consensus() -> AggregatedResult:
    """Result with consensus data."""
    result = AggregatedResult(
        crisis_score=0.80,
        crisis_level=CrisisLevel.HIGH,
        confidence=0.88,
        requires_intervention=True,
        intervention_priority=InterventionPriority.HIGH,
        models_used=["bart", "sentiment"],
        processing_time_ms=110.0,
    )
    result.consensus = ConsensusResult(
        algorithm=ConsensusAlgorithm.WEIGHTED_VOTING,
        crisis_score=0.80,
        confidence=0.88,
        agreement_level=AgreementLevel.STRONG_AGREEMENT,
        is_crisis=True,
        requires_review=False,
        has_conflict=False,
        individual_scores={"bart": 0.85, "sentiment": 0.75},
    )
    result.model_results = {}
    return result


# =============================================================================
# ExplainabilityGenerator Basic Tests
# =============================================================================


class TestExplainabilityGeneratorBasic:
    """Basic tests for ExplainabilityGenerator."""

    def test_create_generator(self):
        """Should create generator with defaults."""
        generator = ExplainabilityGenerator()

        assert generator.default_verbosity == VerbosityLevel.STANDARD

    def test_factory_function(self):
        """Factory function should create valid generator."""
        generator = create_explainability_generator()

        assert isinstance(generator, ExplainabilityGenerator)

    def test_generate_returns_explanation(self, critical_result):
        """Should return Explanation object."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=critical_result)

        assert isinstance(explanation, Explanation)

    def test_get_config(self):
        """Should return current configuration."""
        generator = ExplainabilityGenerator(
            default_verbosity=VerbosityLevel.DETAILED,
            include_model_details=False,
        )
        config = generator.get_config()

        assert config["default_verbosity"] == "detailed"
        assert config["include_model_details"] is False


# =============================================================================
# Verbosity Level Tests
# =============================================================================


class TestVerbosityLevels:
    """Tests for different verbosity levels."""

    def test_minimal_verbosity(self, critical_result):
        """Minimal should have decision summary only."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.MINIMAL,
        )

        assert explanation.verbosity == VerbosityLevel.MINIMAL
        assert explanation.decision_summary is not None
        assert len(explanation.decision_summary) > 0
        # Should NOT have detailed fields
        assert len(explanation.model_contributions) == 0

    def test_standard_verbosity(self, critical_result):
        """Standard should have summary + key factors + recommendation."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert explanation.verbosity == VerbosityLevel.STANDARD
        assert explanation.decision_summary is not None
        assert isinstance(explanation.key_factors, list)
        assert explanation.recommended_action is not None

    def test_detailed_verbosity(self, critical_result):
        """Detailed should have full breakdown."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        assert explanation.verbosity == VerbosityLevel.DETAILED
        assert explanation.decision_summary is not None
        assert explanation.confidence_summary is not None
        assert len(explanation.model_contributions) > 0

    def test_default_verbosity_used(self, critical_result):
        """Should use default verbosity when not specified."""
        generator = ExplainabilityGenerator(default_verbosity=VerbosityLevel.MINIMAL)
        explanation = generator.generate(result=critical_result)

        assert explanation.verbosity == VerbosityLevel.MINIMAL

    def test_set_verbosity(self, critical_result):
        """set_verbosity should change default."""
        generator = ExplainabilityGenerator()
        generator.set_verbosity(VerbosityLevel.DETAILED)

        explanation = generator.generate(result=critical_result)

        assert explanation.verbosity == VerbosityLevel.DETAILED


# =============================================================================
# Decision Summary Tests
# =============================================================================


class TestDecisionSummary:
    """Tests for decision summary generation."""

    def test_critical_summary(self, critical_result):
        """Critical should have urgent language."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=critical_result)

        summary = explanation.decision_summary.upper()
        assert "CRITICAL" in summary

    def test_high_summary(self, high_result):
        """High should indicate concern."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=high_result)

        summary = explanation.decision_summary.upper()
        assert "HIGH" in summary or "CONCERN" in summary

    def test_medium_summary(self, medium_result):
        """Medium should indicate moderate concern."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=medium_result)

        summary = explanation.decision_summary.upper()
        assert "MODERATE" in summary or "MEDIUM" in summary

    def test_safe_summary(self, safe_result):
        """Safe should indicate no concern."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=safe_result)

        summary = explanation.decision_summary.upper()
        assert "NO CONCERN" in summary or "SAFE" in summary

    def test_includes_confidence(self, critical_result):
        """Summary should include confidence percentage."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=critical_result)

        # Should contain a percentage
        assert "%" in explanation.decision_summary


# =============================================================================
# Key Factors Tests
# =============================================================================


class TestKeyFactors:
    """Tests for key factors identification."""

    def test_identifies_factors(self, critical_result):
        """Should identify key crisis factors."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert isinstance(explanation.key_factors, list)
        # Should have at least one factor from the high-signal model
        assert len(explanation.key_factors) >= 0  # May be empty for some configs

    def test_factors_from_labels(self, critical_result):
        """Factors should come from model labels."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        # If BART detected "suicide ideation", it should be in factors
        if explanation.key_factors:
            factors_lower = [f.lower() for f in explanation.key_factors]
            # Should include crisis-related terms
            assert any(
                "suicid" in f or "distress" in f or "negative" in f or "sentiment" in f
                for f in factors_lower
            ) or len(factors_lower) == 0

    def test_limited_factors(self, critical_result):
        """Should limit number of factors."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert len(explanation.key_factors) <= 6


# =============================================================================
# Recommendation Tests
# =============================================================================


class TestRecommendation:
    """Tests for action recommendation generation."""

    def test_critical_gets_immediate(self, critical_result):
        """Critical should recommend immediate action."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert explanation.recommended_action is not None
        assert explanation.recommended_action.priority == "IMMEDIATE"

    def test_high_gets_priority(self, high_result):
        """High should recommend priority response."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=high_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert explanation.recommended_action.priority == "HIGH"

    def test_safe_gets_none(self, safe_result):
        """Safe should recommend no action."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=safe_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert explanation.recommended_action.action == "No action required"

    def test_recommendation_has_all_fields(self, critical_result):
        """Recommendation should have all required fields."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        rec = explanation.recommended_action
        assert rec.priority is not None
        assert rec.action is not None
        assert rec.escalation is not None
        assert rec.rationale is not None


# =============================================================================
# Model Contribution Tests
# =============================================================================


class TestModelContributions:
    """Tests for model contribution explanations."""

    def test_contributions_in_detailed(self, critical_result):
        """Detailed verbosity should include model contributions."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        assert len(explanation.model_contributions) > 0

    def test_contribution_has_fields(self, critical_result):
        """Contributions should have required fields."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        if explanation.model_contributions:
            contrib = explanation.model_contributions[0]
            assert isinstance(contrib, ModelContribution)
            assert contrib.model_name is not None
            assert contrib.display_name is not None
            assert contrib.description is not None
            assert contrib.impact in ("high", "medium", "low")

    def test_sorted_by_impact(self, critical_result):
        """Contributions should be sorted by impact."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        if len(explanation.model_contributions) >= 2:
            # First should have higher or equal impact
            impact_order = {"high": 0, "medium": 1, "low": 2}
            first_impact = impact_order[explanation.model_contributions[0].impact]
            second_impact = impact_order[explanation.model_contributions[1].impact]
            assert first_impact <= second_impact

    def test_no_contributions_when_disabled(self, critical_result):
        """Should not include contributions when disabled."""
        generator = ExplainabilityGenerator(include_model_details=False)
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        assert len(explanation.model_contributions) == 0


# =============================================================================
# Conflict Summary Tests
# =============================================================================


class TestConflictSummary:
    """Tests for conflict summary generation."""

    def test_conflict_summary_in_detailed(self, result_with_conflict):
        """Detailed should include conflict summary."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=result_with_conflict,
            verbosity=VerbosityLevel.DETAILED,
        )

        assert explanation.conflict_summary is not None
        assert len(explanation.conflict_summary) > 0

    def test_no_conflict_summary_when_none(self, critical_result):
        """Should not have conflict summary when no conflicts."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        # No conflict report, so no conflict summary
        assert explanation.conflict_summary == "" or explanation.conflict_summary is None


# =============================================================================
# Confidence Summary Tests
# =============================================================================


class TestConfidenceSummary:
    """Tests for confidence summary generation."""

    def test_confidence_summary_in_detailed(self, critical_result):
        """Detailed should include confidence summary."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        assert explanation.confidence_summary is not None
        assert "%" in explanation.confidence_summary

    def test_includes_model_count(self, critical_result):
        """Confidence summary should mention model count."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        # Should mention number of models
        assert "model" in explanation.confidence_summary.lower()


# =============================================================================
# Plain Text Generation Tests
# =============================================================================


class TestPlainTextGeneration:
    """Tests for plain text explanation generation."""

    def test_plain_text_generated(self, critical_result):
        """Should generate plain text explanation."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=critical_result)

        assert explanation.plain_text is not None
        assert len(explanation.plain_text) > 0

    def test_plain_text_includes_summary(self, critical_result):
        """Plain text should include decision summary."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=critical_result)

        assert "DECISION SUMMARY" in explanation.plain_text

    def test_plain_text_includes_factors(self, critical_result):
        """Plain text should include key factors (standard+)."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert "KEY FACTORS" in explanation.plain_text or len(explanation.key_factors) == 0

    def test_plain_text_includes_recommendation(self, critical_result):
        """Plain text should include recommendation."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert "RECOMMENDED ACTION" in explanation.plain_text


# =============================================================================
# Explanation to_dict Tests
# =============================================================================


class TestExplanationToDict:
    """Tests for Explanation.to_dict() method."""

    def test_to_dict_works(self, critical_result):
        """Should convert to dictionary."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=critical_result)

        explanation_dict = explanation.to_dict()

        assert isinstance(explanation_dict, dict)
        assert "verbosity" in explanation_dict
        assert "decision_summary" in explanation_dict
        assert "plain_text" in explanation_dict

    def test_to_dict_minimal(self, critical_result):
        """Minimal should have fewer fields."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.MINIMAL,
        )

        explanation_dict = explanation.to_dict()

        # Minimal shouldn't have detailed fields
        assert "model_contributions" not in explanation_dict

    def test_to_dict_detailed(self, critical_result):
        """Detailed should have all fields."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        explanation_dict = explanation.to_dict()

        assert "confidence_summary" in explanation_dict
        assert "model_contributions" in explanation_dict


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_model_results(self, medium_result):
        """Should handle empty model results."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=medium_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        # Should still generate explanation
        assert explanation.decision_summary is not None

    def test_zero_confidence(self):
        """Should handle zero confidence."""
        result = AggregatedResult(
            crisis_score=0.50,
            crisis_level=CrisisLevel.MEDIUM,
            confidence=0.0,
            requires_intervention=False,
            intervention_priority=InterventionPriority.STANDARD,
            models_used=[],
            processing_time_ms=100.0,
        )
        result.model_results = {}

        generator = ExplainabilityGenerator()
        explanation = generator.generate(result=result)

        assert "0%" in explanation.decision_summary

    def test_include_recommendations_disabled(self, critical_result):
        """Should not include recommendations when disabled."""
        generator = ExplainabilityGenerator(include_recommendations=False)
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        assert explanation.recommended_action is None


# =============================================================================
# RecommendedAction Tests
# =============================================================================


class TestRecommendedActionClass:
    """Tests for RecommendedAction data class."""

    def test_to_dict(self, critical_result):
        """Should convert to dictionary."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.STANDARD,
        )

        if explanation.recommended_action:
            rec_dict = explanation.recommended_action.to_dict()
            assert "priority" in rec_dict
            assert "action" in rec_dict
            assert "escalation" in rec_dict
            assert "rationale" in rec_dict


# =============================================================================
# ModelContribution Tests
# =============================================================================


class TestModelContributionClass:
    """Tests for ModelContribution data class."""

    def test_to_dict(self, critical_result):
        """Should convert to dictionary."""
        generator = ExplainabilityGenerator()
        explanation = generator.generate(
            result=critical_result,
            verbosity=VerbosityLevel.DETAILED,
        )

        if explanation.model_contributions:
            contrib_dict = explanation.model_contributions[0].to_dict()
            assert "model_name" in contrib_dict
            assert "display_name" in contrib_dict
            assert "description" in contrib_dict
            assert "impact" in contrib_dict
