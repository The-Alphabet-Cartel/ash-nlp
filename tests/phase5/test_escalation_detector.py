"""
Ash-NLP Phase 5 Tests: Escalation Detector
---
FILE VERSION: v5.0-5-TEST-1.0
LAST MODIFIED: 2026-01-02
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- EscalationDetector class
- Escalation type classification (rapid, gradual, sudden, none)
- Pattern matching
- Intervention point detection
- Confidence calculation
"""

import pytest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock, patch

from src.context.escalation_detector import (
    EscalationType,
    EscalationAnalysis,
    EscalationDetector,
    create_escalation_detector,
)
from src.managers.context_config_manager import (
    ContextConfigManager,
    EscalationDetectionConfig,
    KnownPattern,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_config_manager():
    """Create a mock ContextConfigManager with default settings."""
    manager = MagicMock(spec=ContextConfigManager)
    
    # Default escalation detection config
    manager.get_escalation_detection_config.return_value = EscalationDetectionConfig(
        enabled=True,
        rapid_threshold_hours=4,
        gradual_threshold_hours=24,
        score_increase_threshold=0.3,
        minimum_messages=3,
        alert_on_detection=True,
        alert_cooldown_seconds=300,
    )
    
    # Default known patterns
    manager.get_known_patterns.return_value = {
        "evening_deterioration": KnownPattern(
            name="evening_deterioration",
            description="Rapid decline during evening hours",
            typical_duration_hours=4,
            escalation_type="rapid",
            risk_level="high",
        ),
        "gradual_decline": KnownPattern(
            name="gradual_decline",
            description="Slow decline over 24 hours",
            typical_duration_hours=24,
            escalation_type="gradual",
            risk_level="medium",
        ),
        "sudden_crisis": KnownPattern(
            name="sudden_crisis",
            description="Very rapid escalation",
            typical_duration_hours=1,
            escalation_type="sudden",
            risk_level="critical",
        ),
    }
    
    return manager


@pytest.fixture
def disabled_config_manager():
    """Create a mock with escalation detection disabled."""
    manager = MagicMock(spec=ContextConfigManager)
    manager.get_escalation_detection_config.return_value = EscalationDetectionConfig(
        enabled=False,
    )
    manager.get_known_patterns.return_value = {}
    return manager


@pytest.fixture
def escalation_detector(mock_config_manager):
    """Create EscalationDetector with mock config."""
    return EscalationDetector(mock_config_manager)


@pytest.fixture
def base_timestamp():
    """Base timestamp for test sequences."""
    return datetime(2026, 1, 1, 14, 0, 0)  # 2:00 PM


# =============================================================================
# Score and Timestamp Generators
# =============================================================================


def generate_timestamps(
    base: datetime, 
    count: int, 
    interval_minutes: int = 60
) -> List[datetime]:
    """Generate evenly spaced timestamps."""
    return [base + timedelta(minutes=interval_minutes * i) for i in range(count)]


def generate_escalating_scores(
    start: float = 0.2, 
    end: float = 0.9, 
    count: int = 5
) -> List[float]:
    """Generate smoothly escalating scores."""
    if count == 1:
        return [start]
    step = (end - start) / (count - 1)
    return [start + step * i for i in range(count)]


def generate_stable_scores(value: float = 0.3, count: int = 5) -> List[float]:
    """Generate stable scores with minor fluctuation."""
    import random
    random.seed(42)
    return [value + random.uniform(-0.05, 0.05) for _ in range(count)]


def generate_improving_scores(
    start: float = 0.8, 
    end: float = 0.3, 
    count: int = 5
) -> List[float]:
    """Generate improving (decreasing) scores."""
    return generate_escalating_scores(start, end, count)


# =============================================================================
# Test Cases: Basic Detection
# =============================================================================


class TestEscalationDetectorBasic:
    """Tests for basic escalation detection functionality."""
    
    def test_create_factory_function(self, mock_config_manager):
        """Test factory function creates detector."""
        detector = create_escalation_detector(mock_config_manager)
        
        assert detector is not None
        assert isinstance(detector, EscalationDetector)
        assert detector.is_enabled()
    
    def test_disabled_detection(self, disabled_config_manager, base_timestamp):
        """Test that disabled detector returns empty result."""
        detector = EscalationDetector(disabled_config_manager)
        
        scores = generate_escalating_scores(0.2, 0.9, 5)
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.escalation_type == EscalationType.NONE
        assert result.scores == scores
    
    def test_insufficient_messages(self, escalation_detector, base_timestamp):
        """Test detection with insufficient messages."""
        scores = [0.2, 0.5]  # Only 2 messages, need 3
        timestamps = generate_timestamps(base_timestamp, 2)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.scores == scores
    
    def test_mismatched_lists(self, escalation_detector, base_timestamp):
        """Test with mismatched score/timestamp list lengths."""
        scores = [0.2, 0.4, 0.6, 0.8]
        timestamps = generate_timestamps(base_timestamp, 3)  # Mismatch!
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected


class TestEscalationDetection:
    """Tests for escalation detection logic."""
    
    def test_clear_escalation_detected(self, escalation_detector, base_timestamp):
        """Test that clear escalation pattern is detected."""
        scores = generate_escalating_scores(0.2, 0.85, 5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=60)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.detected
        assert result.escalation_type in [
            EscalationType.RAPID, 
            EscalationType.SUDDEN
        ]
        assert result.score_delta >= 0.3
        assert result.confidence > 0.0
    
    def test_no_escalation_stable(self, escalation_detector, base_timestamp):
        """Test that stable scores don't trigger escalation."""
        scores = generate_stable_scores(0.3, 5)
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.escalation_type == EscalationType.NONE
    
    def test_no_escalation_improving(self, escalation_detector, base_timestamp):
        """Test that improving scores don't trigger escalation."""
        scores = generate_improving_scores(0.8, 0.3, 5)
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.score_delta < 0  # Negative delta = improving
    
    def test_small_increase_below_threshold(self, escalation_detector, base_timestamp):
        """Test that small increases below threshold don't trigger."""
        scores = generate_escalating_scores(0.3, 0.5, 5)  # Only 0.2 increase
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.score_delta < 0.3


class TestEscalationTypeClassification:
    """Tests for escalation type classification."""
    
    def test_sudden_escalation(self, escalation_detector, base_timestamp):
        """Test sudden escalation (within 1 hour)."""
        scores = generate_escalating_scores(0.2, 0.9, 4)
        timestamps = generate_timestamps(base_timestamp, 4, interval_minutes=15)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.detected
        assert result.escalation_type == EscalationType.SUDDEN
        assert result.time_span_hours < 1.0
    
    def test_rapid_escalation(self, escalation_detector, base_timestamp):
        """Test rapid escalation (1-4 hours)."""
        scores = generate_escalating_scores(0.2, 0.85, 5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=45)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.detected
        assert result.escalation_type == EscalationType.RAPID
        assert 1.0 <= result.time_span_hours <= 4.0
    
    def test_gradual_escalation(self, escalation_detector, base_timestamp):
        """Test gradual escalation (4-24 hours)."""
        scores = generate_escalating_scores(0.2, 0.8, 5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=180)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.detected
        assert result.escalation_type == EscalationType.GRADUAL
        assert result.time_span_hours > 4.0


class TestInterventionPoint:
    """Tests for intervention point detection."""
    
    def test_intervention_point_found(self, escalation_detector, base_timestamp):
        """Test intervention point is correctly identified."""
        # Scores that cross 0.5 threshold at index 2
        scores = [0.2, 0.35, 0.55, 0.75, 0.9]
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.intervention_point == 2
    
    def test_no_intervention_point_low_scores(self, escalation_detector, base_timestamp):
        """Test no intervention point when scores stay low."""
        scores = [0.2, 0.25, 0.3, 0.35, 0.4]
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.intervention_point is None
    
    def test_immediate_intervention_high_start(self, escalation_detector, base_timestamp):
        """Test intervention point at 0 when starting high."""
        scores = [0.6, 0.7, 0.8, 0.85, 0.9]
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.intervention_point == 0


class TestPatternMatching:
    """Tests for known pattern matching."""
    
    def test_rapid_pattern_match(self, escalation_detector, base_timestamp):
        """Test matching rapid escalation pattern."""
        scores = generate_escalating_scores(0.2, 0.85, 5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=45)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.matched_pattern is not None
        assert result.pattern_confidence > 0.0
    
    def test_no_pattern_when_no_escalation(self, escalation_detector, base_timestamp):
        """Test no pattern match when not escalating."""
        scores = generate_stable_scores(0.3, 5)
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.matched_pattern is None
        assert result.pattern_confidence == 0.0


class TestConfidence:
    """Tests for confidence calculation."""
    
    def test_high_confidence_clear_escalation(self, escalation_detector, base_timestamp):
        """Test high confidence for clear escalation."""
        scores = generate_escalating_scores(0.1, 0.95, 6)
        timestamps = generate_timestamps(base_timestamp, 6, interval_minutes=30)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.detected
        assert result.confidence >= 0.5
    
    def test_lower_confidence_noisy_escalation(self, escalation_detector, base_timestamp):
        """Test lower confidence for noisy escalation."""
        # Escalating but with dips
        scores = [0.2, 0.4, 0.35, 0.55, 0.5, 0.75, 0.85]
        timestamps = generate_timestamps(base_timestamp, 7, interval_minutes=30)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        # May or may not detect depending on consistency check
        if result.detected:
            assert result.confidence < 0.8


class TestRateCalculation:
    """Tests for rate per hour calculation."""
    
    def test_rate_per_hour_calculation(self, escalation_detector, base_timestamp):
        """Test rate per hour is calculated correctly."""
        scores = [0.2, 0.4, 0.6, 0.8]
        timestamps = generate_timestamps(base_timestamp, 4, interval_minutes=60)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        # 0.6 increase over 3 hours = 0.2 per hour
        assert abs(result.rate_per_hour - 0.2) < 0.01
    
    def test_time_span_calculation(self, escalation_detector, base_timestamp):
        """Test time span is calculated correctly."""
        scores = [0.2, 0.4, 0.6, 0.8, 0.9]
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=60)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        # 5 messages at 60 min intervals = 4 hours span
        assert abs(result.time_span_hours - 4.0) < 0.1


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_single_message(self, escalation_detector, base_timestamp):
        """Test handling of single message."""
        scores = [0.5]
        timestamps = [base_timestamp]
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.scores == scores
    
    def test_empty_lists(self, escalation_detector):
        """Test handling of empty lists."""
        result = escalation_detector.analyze([], [])
        
        assert not result.detected
        assert result.scores == []
    
    def test_all_same_scores(self, escalation_detector, base_timestamp):
        """Test with all identical scores."""
        scores = [0.5, 0.5, 0.5, 0.5, 0.5]
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert not result.detected
        assert result.score_delta == 0.0
    
    def test_max_scores(self, escalation_detector, base_timestamp):
        """Test with maximum crisis scores."""
        scores = [0.7, 0.85, 0.95, 0.99, 1.0]
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = escalation_detector.analyze(scores, timestamps)
        
        assert result.detected
        assert result.end_score == scores[-1]
    
    def test_very_long_time_span(self, escalation_detector, base_timestamp):
        """Test with very long time span (>24 hours)."""
        scores = generate_escalating_scores(0.2, 0.8, 5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=720)  # 12 hours each
        
        result = escalation_detector.analyze(scores, timestamps)
        
        # Should still detect but classify as gradual
        if result.detected:
            assert result.escalation_type == EscalationType.GRADUAL


class TestConfigAccess:
    """Tests for configuration access."""
    
    def test_is_enabled(self, escalation_detector):
        """Test is_enabled returns correct value."""
        assert escalation_detector.is_enabled() is True
    
    def test_get_config(self, escalation_detector):
        """Test get_config returns config object."""
        config = escalation_detector.get_config()
        
        assert isinstance(config, EscalationDetectionConfig)
        assert config.enabled is True
        assert config.rapid_threshold_hours == 4


# =============================================================================
# Export
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
