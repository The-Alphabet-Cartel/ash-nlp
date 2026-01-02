"""
Ash-NLP Phase 5 Tests: Temporal Detector
---
FILE VERSION: v5.0-5-TEST-1.0
LAST MODIFIED: 2026-01-02
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- TemporalDetector class
- Late night detection
- Rapid posting detection
- Risk modifier calculation
- Weekend detection
"""

import pytest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock

from src.context.temporal_detector import (
    TimeOfDayRisk,
    PostingFrequency,
    TemporalAnalysis,
    TemporalDetector,
    create_temporal_detector,
)
from src.managers.context_config_manager import (
    ContextConfigManager,
    TemporalDetectionConfig,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_config_manager():
    """Create a mock ContextConfigManager with default settings."""
    manager = MagicMock(spec=ContextConfigManager)
    
    manager.get_temporal_detection_config.return_value = TemporalDetectionConfig(
        enabled=True,
        late_night_start_hour=22,  # 10 PM
        late_night_end_hour=4,     # 4 AM
        late_night_risk_modifier=1.2,
        rapid_posting_threshold_minutes=30,
        rapid_posting_message_count=5,
        weekend_risk_modifier=1.1,
    )
    
    return manager


@pytest.fixture
def disabled_config_manager():
    """Create a mock with temporal detection disabled."""
    manager = MagicMock(spec=ContextConfigManager)
    manager.get_temporal_detection_config.return_value = TemporalDetectionConfig(
        enabled=False,
    )
    return manager


@pytest.fixture
def temporal_detector(mock_config_manager):
    """Create TemporalDetector with mock config."""
    return TemporalDetector(mock_config_manager)


# =============================================================================
# Time Generation Helpers
# =============================================================================


def generate_timestamps(
    base: datetime,
    count: int,
    interval_minutes: int = 10
) -> List[datetime]:
    """Generate evenly spaced timestamps."""
    return [base + timedelta(minutes=interval_minutes * i) for i in range(count)]


def generate_rapid_timestamps(
    base: datetime,
    count: int,
    interval_minutes: int = 5
) -> List[datetime]:
    """Generate rapid posting timestamps."""
    return generate_timestamps(base, count, interval_minutes)


# =============================================================================
# Test Cases: Basic Functionality
# =============================================================================


class TestTemporalDetectorBasic:
    """Tests for basic temporal detection functionality."""
    
    def test_create_factory_function(self, mock_config_manager):
        """Test factory function creates detector."""
        detector = create_temporal_detector(mock_config_manager)
        
        assert detector is not None
        assert isinstance(detector, TemporalDetector)
        assert detector.is_enabled()
    
    def test_disabled_detection(self, disabled_config_manager):
        """Test that disabled detector returns empty result."""
        detector = TemporalDetector(disabled_config_manager)
        
        base = datetime(2026, 1, 1, 23, 0, 0)  # 11 PM - late night
        timestamps = generate_timestamps(base, 5)
        
        result = detector.analyze(timestamps)
        
        # Disabled should return defaults
        assert not result.late_night_detected
        assert result.risk_modifier == 1.0
    
    def test_empty_timestamps(self, temporal_detector):
        """Test handling of empty timestamps."""
        result = temporal_detector.analyze([])
        
        assert not result.late_night_detected
        assert not result.rapid_posting_detected
        assert result.risk_modifier == 1.0


class TestLateNightDetection:
    """Tests for late night posting detection."""
    
    def test_late_night_detected_11pm(self, temporal_detector):
        """Test late night detection at 11 PM."""
        base = datetime(2026, 1, 1, 23, 0, 0)  # 11 PM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.late_night_detected
        assert result.time_of_day_risk == TimeOfDayRisk.LATE_NIGHT
        assert result.hour_of_day == 23
    
    def test_late_night_detected_2am(self, temporal_detector):
        """Test late night detection at 2 AM."""
        base = datetime(2026, 1, 2, 2, 0, 0)  # 2 AM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.late_night_detected
        assert result.time_of_day_risk == TimeOfDayRisk.LATE_NIGHT
        assert result.hour_of_day == 2
    
    def test_not_late_night_afternoon(self, temporal_detector):
        """Test not late night at 2 PM."""
        base = datetime(2026, 1, 1, 14, 0, 0)  # 2 PM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert not result.late_night_detected
        assert result.time_of_day_risk == TimeOfDayRisk.NORMAL
        assert result.hour_of_day == 14
    
    def test_not_late_night_9pm(self, temporal_detector):
        """Test not late night at 9 PM (before 10 PM threshold)."""
        base = datetime(2026, 1, 1, 21, 0, 0)  # 9 PM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert not result.late_night_detected
        assert result.time_of_day_risk == TimeOfDayRisk.NORMAL
    
    def test_not_late_night_5am(self, temporal_detector):
        """Test not late night at 5 AM (after 4 AM threshold)."""
        base = datetime(2026, 1, 1, 5, 0, 0)  # 5 AM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert not result.late_night_detected
        # Early morning has its own classification
        assert result.time_of_day_risk == TimeOfDayRisk.EARLY_MORNING
    
    def test_late_night_count(self, temporal_detector):
        """Test counting of late night messages in history."""
        timestamps = [
            datetime(2026, 1, 1, 14, 0, 0),   # 2 PM - not late
            datetime(2026, 1, 1, 23, 0, 0),   # 11 PM - late
            datetime(2026, 1, 2, 1, 0, 0),    # 1 AM - late
            datetime(2026, 1, 2, 2, 0, 0),    # 2 AM - late (current)
        ]
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.late_night_count == 3


class TestRapidPostingDetection:
    """Tests for rapid posting detection."""
    
    def test_rapid_posting_detected(self, temporal_detector):
        """Test rapid posting is detected."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        # 6 messages in 25 minutes (threshold is 5 in 30 min)
        timestamps = generate_rapid_timestamps(base, 6, interval_minutes=5)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.rapid_posting_detected
        assert result.posting_frequency == PostingFrequency.RAPID
        assert result.messages_in_window >= 5
    
    def test_not_rapid_normal_pace(self, temporal_detector):
        """Test normal posting pace not flagged."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        # 3 messages in 2 hours - normal pace
        timestamps = generate_timestamps(base, 3, interval_minutes=60)
        
        result = temporal_detector.analyze(timestamps)
        
        assert not result.rapid_posting_detected
        assert result.posting_frequency == PostingFrequency.NORMAL
    
    def test_elevated_posting(self, temporal_detector):
        """Test elevated but not rapid posting."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        # 3 messages in 30 minutes (60% of threshold)
        timestamps = generate_timestamps(base, 3, interval_minutes=10)
        
        result = temporal_detector.analyze(timestamps)
        
        assert not result.rapid_posting_detected
        assert result.posting_frequency == PostingFrequency.ELEVATED
    
    def test_messages_in_window_count(self, temporal_detector):
        """Test accurate counting of messages in window."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        # Messages spread over time, some within window
        timestamps = [
            base,
            base + timedelta(minutes=10),
            base + timedelta(minutes=20),
            base + timedelta(minutes=25),
            base + timedelta(minutes=28),
        ]
        
        result = temporal_detector.analyze(timestamps)
        
        # All should be within 30 min window from last
        assert result.messages_in_window == 5


class TestWeekendDetection:
    """Tests for weekend detection."""
    
    def test_saturday_detected(self, temporal_detector):
        """Test Saturday is detected as weekend."""
        saturday = datetime(2026, 1, 3, 14, 0, 0)  # Saturday
        timestamps = generate_timestamps(saturday, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.is_weekend
    
    def test_sunday_detected(self, temporal_detector):
        """Test Sunday is detected as weekend."""
        sunday = datetime(2026, 1, 4, 14, 0, 0)  # Sunday
        timestamps = generate_timestamps(sunday, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.is_weekend
    
    def test_weekday_not_weekend(self, temporal_detector):
        """Test weekday is not weekend."""
        wednesday = datetime(2026, 1, 1, 14, 0, 0)  # Wednesday
        timestamps = generate_timestamps(wednesday, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert not result.is_weekend


class TestRiskModifier:
    """Tests for risk modifier calculation."""
    
    def test_no_risk_normal_day(self, temporal_detector):
        """Test no risk modifier for normal day."""
        base = datetime(2026, 1, 1, 14, 0, 0)  # Wednesday 2 PM
        timestamps = generate_timestamps(base, 3, interval_minutes=60)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.risk_modifier == 1.0
    
    def test_late_night_risk_modifier(self, temporal_detector):
        """Test late night adds risk modifier."""
        base = datetime(2026, 1, 1, 23, 0, 0)  # 11 PM
        timestamps = generate_timestamps(base, 3, interval_minutes=60)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.risk_modifier >= 1.2  # Late night modifier
    
    def test_rapid_posting_risk_modifier(self, temporal_detector):
        """Test rapid posting adds risk modifier."""
        base = datetime(2026, 1, 1, 14, 0, 0)  # Normal time
        timestamps = generate_rapid_timestamps(base, 6, interval_minutes=5)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.risk_modifier >= 1.15  # Rapid posting modifier
    
    def test_weekend_risk_modifier(self, temporal_detector):
        """Test weekend adds risk modifier."""
        saturday = datetime(2026, 1, 3, 14, 0, 0)  # Saturday 2 PM
        timestamps = generate_timestamps(saturday, 3, interval_minutes=60)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.risk_modifier >= 1.1  # Weekend modifier
    
    def test_combined_risk_modifiers(self, temporal_detector):
        """Test multiple risk modifiers combine."""
        # Late night + weekend + rapid posting
        saturday_night = datetime(2026, 1, 3, 23, 0, 0)  # Saturday 11 PM
        timestamps = generate_rapid_timestamps(saturday_night, 6, interval_minutes=5)
        
        result = temporal_detector.analyze(timestamps)
        
        # All three modifiers should stack: 1.2 * 1.15 * 1.1 ≈ 1.518
        assert result.risk_modifier > 1.4
        assert result.late_night_detected
        assert result.rapid_posting_detected
        assert result.is_weekend


class TestAverageGap:
    """Tests for average gap calculation."""
    
    def test_average_gap_calculation(self, temporal_detector):
        """Test average gap is calculated correctly."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        # 4 messages, 30 minutes apart
        timestamps = generate_timestamps(base, 4, interval_minutes=30)
        
        result = temporal_detector.analyze(timestamps)
        
        # 3 gaps of 30 minutes each = 30 min average
        assert abs(result.average_gap_minutes - 30.0) < 0.1
    
    def test_average_gap_variable_spacing(self, temporal_detector):
        """Test average gap with variable spacing."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        timestamps = [
            base,
            base + timedelta(minutes=10),   # 10 min gap
            base + timedelta(minutes=30),   # 20 min gap
            base + timedelta(minutes=90),   # 60 min gap
        ]
        
        result = temporal_detector.analyze(timestamps)
        
        # (10 + 20 + 60) / 3 = 30 min average
        assert abs(result.average_gap_minutes - 30.0) < 0.1
    
    def test_average_gap_single_message(self, temporal_detector):
        """Test average gap with single message."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        timestamps = [base]
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.average_gap_minutes == 0.0


class TestCurrentTimestamp:
    """Tests for current timestamp handling."""
    
    def test_explicit_current_timestamp(self, temporal_detector):
        """Test explicit current timestamp is used."""
        base = datetime(2026, 1, 1, 14, 0, 0)
        timestamps = generate_timestamps(base, 3)
        
        # Explicit late night current
        current = datetime(2026, 1, 1, 23, 30, 0)
        
        result = temporal_detector.analyze(timestamps, current_timestamp=current)
        
        assert result.late_night_detected
        assert result.hour_of_day == 23
    
    def test_default_current_is_last(self, temporal_detector):
        """Test default current timestamp is last in list."""
        timestamps = [
            datetime(2026, 1, 1, 14, 0, 0),
            datetime(2026, 1, 1, 15, 0, 0),
            datetime(2026, 1, 1, 23, 0, 0),  # Last = late night
        ]
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.late_night_detected
        assert result.hour_of_day == 23


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_exactly_at_threshold_start(self, temporal_detector):
        """Test exactly at late night start (10 PM)."""
        base = datetime(2026, 1, 1, 22, 0, 0)  # Exactly 10 PM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.late_night_detected
        assert result.hour_of_day == 22
    
    def test_exactly_at_threshold_end(self, temporal_detector):
        """Test exactly at late night end (4 AM)."""
        base = datetime(2026, 1, 1, 4, 0, 0)  # Exactly 4 AM
        timestamps = generate_timestamps(base, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        # 4 AM should NOT be late night (end hour is exclusive)
        assert not result.late_night_detected
    
    def test_midnight(self, temporal_detector):
        """Test midnight is late night."""
        midnight = datetime(2026, 1, 1, 0, 0, 0)
        timestamps = generate_timestamps(midnight, 3)
        
        result = temporal_detector.analyze(timestamps)
        
        assert result.late_night_detected
        assert result.hour_of_day == 0


class TestConfigAccess:
    """Tests for configuration access."""
    
    def test_is_enabled(self, temporal_detector):
        """Test is_enabled returns correct value."""
        assert temporal_detector.is_enabled() is True
    
    def test_get_config(self, temporal_detector):
        """Test get_config returns config object."""
        config = temporal_detector.get_config()
        
        assert isinstance(config, TemporalDetectionConfig)
        assert config.enabled is True
        assert config.late_night_start_hour == 22
        assert config.late_night_end_hour == 4


# =============================================================================
# Export
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
