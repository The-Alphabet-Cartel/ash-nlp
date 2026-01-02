"""
Ash-NLP Phase 4 Tests: Conflict Detection
---
FILE VERSION: v5.0-4-TEST-2.1
LAST MODIFIED: 2026-01-01
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- ConflictDetector class
- Score disagreement detection
- Irony-sentiment conflict detection
- Emotion-crisis mismatch detection
- Label disagreement detection
"""

import pytest
from typing import Dict

from src.ensemble.conflict_detector import (
    # Enums
    ConflictType,
    ConflictSeverity,
    # Data classes
    DetectedConflict,
    ConflictReport,
    ModelSignals,
    # Detector
    ConflictDetector,
    create_conflict_detector,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def agreeing_signals() -> ModelSignals:
    """Model signals that agree (no conflicts)."""
    return ModelSignals(
        bart_score=0.80,
        bart_label="emotional distress",
        bart_all_scores={"emotional distress": 0.80, "safe": 0.15},
        sentiment_score=0.75,
        sentiment_label="negative",
        sentiment_all_scores={"negative": 0.75, "positive": 0.15, "neutral": 0.10},
        irony_score=0.95,  # High = no irony (dampening factor)
        irony_detected=False,
        irony_confidence=0.10,
        emotions_score=0.70,
        emotions_top={"sadness": 0.60, "fear": 0.40},
        emotions_all_scores={"sadness": 0.60, "fear": 0.40},
    )


@pytest.fixture
def agreeing_scores() -> Dict[str, float]:
    """Crisis scores that agree."""
    return {
        "bart": 0.80,
        "sentiment": 0.75,
        "irony": 0.95,
        "emotions": 0.70,
    }


@pytest.fixture
def disagreeing_signals() -> ModelSignals:
    """Model signals with score disagreement."""
    return ModelSignals(
        bart_score=0.90,
        bart_label="suicide ideation",
        bart_all_scores={"suicide ideation": 0.90},
        sentiment_score=0.20,
        sentiment_label="positive",
        sentiment_all_scores={"positive": 0.70, "negative": 0.20},
        irony_score=0.50,
        irony_detected=False,
        irony_confidence=0.40,
        emotions_score=0.30,
        emotions_top={"joy": 0.50},
        emotions_all_scores={"joy": 0.50},
    )


@pytest.fixture
def disagreeing_scores() -> Dict[str, float]:
    """Crisis scores with significant disagreement."""
    return {
        "bart": 0.90,
        "sentiment": 0.20,
        "irony": 0.50,
        "emotions": 0.30,
    }


@pytest.fixture
def irony_conflict_signals() -> ModelSignals:
    """Model signals with irony-sentiment conflict."""
    return ModelSignals(
        bart_score=0.60,
        bart_label="emotional distress",
        sentiment_score=0.30,  # Low crisis signal
        sentiment_label="positive",
        sentiment_all_scores={"positive": 0.70, "negative": 0.20},
        irony_score=0.40,  # Low = irony detected
        irony_detected=True,
        irony_confidence=0.75,  # High confidence irony
        emotions_score=0.50,
        emotions_top={"sadness": 0.40},
    )


@pytest.fixture
def emotion_mismatch_signals() -> ModelSignals:
    """Model signals with emotion-crisis mismatch."""
    return ModelSignals(
        bart_score=0.85,
        bart_label="severe depression",
        bart_all_scores={"severe depression": 0.85},
        sentiment_score=0.70,
        sentiment_label="negative",
        sentiment_all_scores={"negative": 0.70},
        irony_score=0.90,
        irony_detected=False,
        irony_confidence=0.10,
        emotions_score=0.20,  # Low emotion crisis signal
        emotions_top={"joy": 0.60, "surprise": 0.30},  # No crisis emotions
        emotions_all_scores={"joy": 0.60, "surprise": 0.30},
    )


@pytest.fixture
def label_conflict_signals() -> ModelSignals:
    """Model signals with label disagreement."""
    return ModelSignals(
        bart_score=0.85,
        bart_label="suicide ideation",  # Crisis label
        bart_all_scores={"suicide ideation": 0.85},
        sentiment_score=0.25,
        sentiment_label="positive",
        sentiment_all_scores={"positive": 0.80, "negative": 0.15},  # Very positive
        irony_score=0.95,  # No irony
        irony_detected=False,
        irony_confidence=0.10,
        emotions_score=0.40,
        emotions_top={"joy": 0.50},
    )


# =============================================================================
# ConflictDetector Basic Tests
# =============================================================================


class TestConflictDetectorBasic:
    """Basic tests for ConflictDetector."""

    def test_create_detector(self):
        """Should create detector with defaults."""
        detector = ConflictDetector()

        assert detector.score_disagreement_threshold == 0.4
        assert detector.irony_detection_threshold == 0.5

    def test_factory_function(self):
        """Factory function should create valid detector."""
        detector = create_conflict_detector()

        assert isinstance(detector, ConflictDetector)

    def test_no_conflicts_returns_clean_report(self, agreeing_signals, agreeing_scores):
        """Should return clean report when no conflicts."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=agreeing_signals,
            crisis_scores=agreeing_scores,
        )

        assert isinstance(report, ConflictReport)
        assert report.has_conflicts is False
        assert report.conflict_count == 0
        assert len(report.conflicts) == 0
        assert report.requires_review is False

    def test_get_config(self):
        """Should return current configuration."""
        detector = ConflictDetector(
            score_disagreement_threshold=0.5,
            irony_detection_threshold=0.6,
        )
        config = detector.get_config()

        assert config["score_disagreement_threshold"] == 0.5
        assert config["irony_detection_threshold"] == 0.6


# =============================================================================
# Score Disagreement Tests
# =============================================================================


class TestScoreDisagreement:
    """Tests for score disagreement detection."""

    def test_detects_score_disagreement(self, disagreeing_signals, disagreeing_scores):
        """Should detect significant score disagreement."""
        detector = ConflictDetector(score_disagreement_threshold=0.4)
        report = detector.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        assert report.has_conflicts is True
        
        # Find the score disagreement conflict
        score_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]
        assert len(score_conflicts) >= 1
        
        conflict = score_conflicts[0]
        assert conflict.severity == ConflictSeverity.HIGH
        assert "bart" in conflict.involved_models or "sentiment" in conflict.involved_models

    def test_no_detection_below_threshold(self, agreeing_signals, agreeing_scores):
        """Should not detect when variance below threshold."""
        detector = ConflictDetector(score_disagreement_threshold=0.4)
        report = detector.detect_conflicts(
            model_signals=agreeing_signals,
            crisis_scores=agreeing_scores,
        )

        score_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]
        assert len(score_conflicts) == 0

    def test_threshold_configurable(self, disagreeing_scores, disagreeing_signals):
        """Threshold should be configurable."""
        # High threshold - won't detect
        detector1 = ConflictDetector(score_disagreement_threshold=0.9)
        report1 = detector1.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        # Low threshold - will detect
        detector2 = ConflictDetector(score_disagreement_threshold=0.1)
        report2 = detector2.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        score_conflicts1 = [
            c for c in report1.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]
        score_conflicts2 = [
            c for c in report2.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]

        assert len(score_conflicts1) == 0
        assert len(score_conflicts2) >= 1


# =============================================================================
# Irony-Sentiment Conflict Tests
# =============================================================================


class TestIronySentimentConflict:
    """Tests for irony-sentiment conflict detection."""

    def test_detects_irony_sentiment_conflict(self, irony_conflict_signals):
        """Should detect irony + positive sentiment conflict."""
        detector = ConflictDetector(irony_detection_threshold=0.5)
        
        # Need scores that won't trigger score disagreement
        scores = {"bart": 0.60, "sentiment": 0.55, "irony": 0.55, "emotions": 0.50}
        
        report = detector.detect_conflicts(
            model_signals=irony_conflict_signals,
            crisis_scores=scores,
        )

        irony_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.IRONY_SENTIMENT_CONFLICT
        ]
        
        assert len(irony_conflicts) >= 1
        
        conflict = irony_conflicts[0]
        assert conflict.severity == ConflictSeverity.MEDIUM
        assert "sentiment" in conflict.involved_models
        assert "irony" in conflict.involved_models

    def test_no_conflict_when_no_irony(self, agreeing_signals, agreeing_scores):
        """Should not detect when no irony present."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=agreeing_signals,
            crisis_scores=agreeing_scores,
        )

        irony_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.IRONY_SENTIMENT_CONFLICT
        ]
        assert len(irony_conflicts) == 0


# =============================================================================
# Emotion-Crisis Mismatch Tests
# =============================================================================


class TestEmotionCrisisMismatch:
    """Tests for emotion-crisis mismatch detection."""

    def test_detects_emotion_mismatch(self, emotion_mismatch_signals):
        """Should detect high crisis but no crisis emotions."""
        detector = ConflictDetector()
        
        # High crisis scores
        scores = {"bart": 0.85, "sentiment": 0.70, "irony": 0.90, "emotions": 0.20}
        
        report = detector.detect_conflicts(
            model_signals=emotion_mismatch_signals,
            crisis_scores=scores,
        )

        mismatch_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.EMOTION_CRISIS_MISMATCH
        ]
        
        assert len(mismatch_conflicts) >= 1
        
        conflict = mismatch_conflicts[0]
        assert conflict.severity == ConflictSeverity.MEDIUM

    def test_no_mismatch_with_crisis_emotions(self, agreeing_signals, agreeing_scores):
        """Should not detect when crisis emotions present."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=agreeing_signals,
            crisis_scores=agreeing_scores,
        )

        mismatch_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.EMOTION_CRISIS_MISMATCH
        ]
        assert len(mismatch_conflicts) == 0


# =============================================================================
# Label Disagreement Tests
# =============================================================================


class TestLabelDisagreement:
    """Tests for label disagreement detection."""

    def test_detects_label_disagreement(self, label_conflict_signals):
        """Should detect crisis label with positive sentiment (no irony)."""
        detector = ConflictDetector()
        
        scores = {"bart": 0.85, "sentiment": 0.25, "irony": 0.95, "emotions": 0.40}
        
        report = detector.detect_conflicts(
            model_signals=label_conflict_signals,
            crisis_scores=scores,
        )

        label_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.LABEL_DISAGREEMENT
        ]
        
        assert len(label_conflicts) >= 1

    def test_no_label_conflict_when_consistent(self, agreeing_signals, agreeing_scores):
        """Should not detect when labels consistent."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=agreeing_signals,
            crisis_scores=agreeing_scores,
        )

        label_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.LABEL_DISAGREEMENT
        ]
        assert len(label_conflicts) == 0


# =============================================================================
# Conflict Report Tests
# =============================================================================


class TestConflictReport:
    """Tests for ConflictReport generation."""

    def test_highest_severity_calculated(self, disagreeing_signals, disagreeing_scores):
        """Should identify highest severity conflict."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        if report.has_conflicts:
            assert report.highest_severity is not None
            # Score disagreement is HIGH severity
            assert report.highest_severity == ConflictSeverity.HIGH

    def test_requires_review_for_high_severity(self, disagreeing_signals, disagreeing_scores):
        """Should require review for high severity conflicts."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        if report.highest_severity == ConflictSeverity.HIGH:
            assert report.requires_review is True

    def test_summary_generated(self, agreeing_signals, agreeing_scores):
        """Should generate summary string."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=agreeing_signals,
            crisis_scores=agreeing_scores,
        )

        assert isinstance(report.summary, str)
        assert len(report.summary) > 0

    def test_to_dict_works(self, disagreeing_signals, disagreeing_scores):
        """Should convert to dictionary."""
        detector = ConflictDetector()
        report = detector.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        report_dict = report.to_dict()

        assert isinstance(report_dict, dict)
        assert "has_conflicts" in report_dict
        assert "conflict_count" in report_dict
        assert "conflicts" in report_dict


# =============================================================================
# ModelSignals Tests
# =============================================================================


class TestModelSignals:
    """Tests for ModelSignals data class."""

    def test_from_ensemble_signals(self):
        """Should create from ensemble signal dictionary."""
        signals_dict = {
            "bart": {
                "crisis_signal": 0.80,
                "label": "emotional distress",
                "metadata": {"all_scores": {"emotional distress": 0.80}},
            },
            "sentiment": {
                "crisis_signal": 0.70,
                "label": "negative",
                "metadata": {"negative": 0.70},
            },
            "irony": {
                "crisis_signal": 0.95,
                "metadata": {"irony_score": 0.10},
            },
            "emotions": {
                "crisis_signal": 0.60,
                "metadata": {"top_emotions": {"sadness": 0.50}},
            },
        }

        signals = ModelSignals.from_ensemble_signals(signals_dict)

        assert signals.bart_score == 0.80
        assert signals.bart_label == "emotional distress"
        assert signals.sentiment_score == 0.70
        assert signals.irony_score == 0.95

    def test_default_values(self):
        """Should have sensible defaults."""
        signals = ModelSignals()

        assert signals.bart_score == 0.0
        assert signals.irony_score == 1.0  # No irony by default
        assert signals.irony_detected is False


# =============================================================================
# Conflict Type Enable/Disable Tests
# =============================================================================


class TestConflictTypeToggle:
    """Tests for enabling/disabling conflict types."""

    def test_disable_conflict_type(self, disagreeing_signals, disagreeing_scores):
        """Should not detect disabled conflict types."""
        detector = ConflictDetector()
        detector.disable_conflict_type(ConflictType.SCORE_DISAGREEMENT)

        report = detector.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        score_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]
        assert len(score_conflicts) == 0

    def test_enable_conflict_type(self, disagreeing_signals, disagreeing_scores):
        """Should re-enable disabled conflict type."""
        detector = ConflictDetector()
        detector.disable_conflict_type(ConflictType.SCORE_DISAGREEMENT)
        detector.enable_conflict_type(ConflictType.SCORE_DISAGREEMENT)

        report = detector.detect_conflicts(
            model_signals=disagreeing_signals,
            crisis_scores=disagreeing_scores,
        )

        # Should now detect again
        score_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]
        assert len(score_conflicts) >= 1


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_scores(self):
        """Should handle empty scores."""
        detector = ConflictDetector()
        signals = ModelSignals()

        report = detector.detect_conflicts(
            model_signals=signals,
            crisis_scores={},
        )

        assert report.has_conflicts is False

    def test_single_model_score(self):
        """Should handle single model score."""
        detector = ConflictDetector()
        signals = ModelSignals(bart_score=0.80, bart_label="test")

        report = detector.detect_conflicts(
            model_signals=signals,
            crisis_scores={"bart": 0.80},
        )

        # Can't have score disagreement with one model
        score_conflicts = [
            c for c in report.conflicts
            if c.conflict_type == ConflictType.SCORE_DISAGREEMENT
        ]
        assert len(score_conflicts) == 0
