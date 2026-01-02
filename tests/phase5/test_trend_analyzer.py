"""
Ash-NLP Phase 5 Tests: Trend Analyzer
---
FILE VERSION: v5.0-5-TEST-1.0
LAST MODIFIED: 2026-01-02
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- TrendAnalyzer class
- Trend direction detection (worsening, stable, improving, volatile)
- Trend velocity calculation
- Inflection point detection
- Score smoothing
"""

import pytest
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock

from src.context.trend_analyzer import (
    TrendDirection,
    TrendVelocity,
    TrendAnalysis,
    TrendAnalyzer,
    create_trend_analyzer,
)
from src.managers.context_config_manager import (
    ContextConfigManager,
    TrendAnalysisConfig,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_config_manager():
    """Create a mock ContextConfigManager with default settings."""
    manager = MagicMock(spec=ContextConfigManager)
    
    manager.get_trend_analysis_config.return_value = TrendAnalysisConfig(
        enabled=True,
        worsening_threshold=0.15,
        improving_threshold=-0.15,
        velocity_rapid_threshold=0.1,
        velocity_gradual_threshold=0.03,
    )
    
    return manager


@pytest.fixture
def disabled_config_manager():
    """Create a mock with trend analysis disabled."""
    manager = MagicMock(spec=ContextConfigManager)
    manager.get_trend_analysis_config.return_value = TrendAnalysisConfig(
        enabled=False,
    )
    return manager


@pytest.fixture
def trend_analyzer(mock_config_manager):
    """Create TrendAnalyzer with mock config."""
    return TrendAnalyzer(mock_config_manager)


@pytest.fixture
def base_timestamp():
    """Base timestamp for test sequences."""
    return datetime(2026, 1, 1, 14, 0, 0)


# =============================================================================
# Helper Functions
# =============================================================================


def generate_timestamps(
    base: datetime,
    count: int,
    interval_minutes: int = 60
) -> List[datetime]:
    """Generate evenly spaced timestamps."""
    return [base + timedelta(minutes=interval_minutes * i) for i in range(count)]


def generate_worsening_scores(count: int = 5) -> List[float]:
    """Generate worsening (increasing) crisis scores."""
    return [0.2 + (0.6 / (count - 1)) * i for i in range(count)]


def generate_improving_scores(count: int = 5) -> List[float]:
    """Generate improving (decreasing) crisis scores."""
    return [0.8 - (0.5 / (count - 1)) * i for i in range(count)]


def generate_stable_scores(value: float = 0.4, count: int = 5) -> List[float]:
    """Generate stable scores with tiny fluctuation."""
    return [value + 0.02 * (i % 2) for i in range(count)]


def generate_volatile_scores(count: int = 6) -> List[float]:
    """Generate volatile (oscillating) scores."""
    return [0.3, 0.6, 0.3, 0.7, 0.4, 0.5][:count]


# =============================================================================
# Test Cases: Basic Functionality
# =============================================================================


class TestTrendAnalyzerBasic:
    """Tests for basic trend analysis functionality."""
    
    def test_create_factory_function(self, mock_config_manager):
        """Test factory function creates analyzer."""
        analyzer = create_trend_analyzer(mock_config_manager)
        
        assert analyzer is not None
        assert isinstance(analyzer, TrendAnalyzer)
        assert analyzer.is_enabled()
    
    def test_disabled_analysis(self, disabled_config_manager):
        """Test that disabled analyzer returns empty result."""
        analyzer = TrendAnalyzer(disabled_config_manager)
        
        scores = generate_worsening_scores(5)
        result = analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.STABLE
        assert result.velocity == TrendVelocity.NONE
    
    def test_single_score(self, trend_analyzer):
        """Test handling of single score."""
        scores = [0.5]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.start_score == 0.5
        assert result.end_score == 0.5
        assert result.score_delta == 0.0
    
    def test_empty_scores(self, trend_analyzer):
        """Test handling of empty scores."""
        result = trend_analyzer.analyze([])
        
        assert result.direction == TrendDirection.STABLE
        assert result.velocity == TrendVelocity.NONE


class TestTrendDirection:
    """Tests for trend direction detection."""
    
    def test_worsening_trend(self, trend_analyzer):
        """Test worsening trend is detected."""
        scores = generate_worsening_scores(5)  # 0.2 → 0.8
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.WORSENING
        assert result.score_delta > 0.15  # Above threshold
    
    def test_improving_trend(self, trend_analyzer):
        """Test improving trend is detected."""
        scores = generate_improving_scores(5)  # 0.8 → 0.3
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.IMPROVING
        assert result.score_delta < -0.15  # Below threshold
    
    def test_stable_trend(self, trend_analyzer):
        """Test stable trend is detected."""
        scores = generate_stable_scores(0.4, 5)
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.STABLE
        assert abs(result.score_delta) < 0.15
    
    def test_volatile_trend(self, trend_analyzer):
        """Test volatile trend is detected."""
        scores = generate_volatile_scores(6)
        
        result = trend_analyzer.analyze(scores)
        
        # Volatile should have multiple inflection points and small net change
        assert result.direction == TrendDirection.VOLATILE or len(result.inflection_points) >= 2
    
    def test_mild_increase_stable(self, trend_analyzer):
        """Test mild increase stays stable."""
        # 0.3 → 0.4 = 0.1 increase (below 0.15 threshold)
        scores = [0.3, 0.32, 0.35, 0.38, 0.4]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.STABLE
    
    def test_mild_decrease_stable(self, trend_analyzer):
        """Test mild decrease stays stable."""
        # 0.5 → 0.4 = -0.1 decrease (above -0.15 threshold)
        scores = [0.5, 0.48, 0.45, 0.42, 0.4]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.STABLE


class TestTrendVelocity:
    """Tests for trend velocity calculation."""
    
    def test_rapid_velocity(self, trend_analyzer, base_timestamp):
        """Test rapid velocity detection."""
        scores = generate_worsening_scores(5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=30)
        
        result = trend_analyzer.analyze(scores, timestamps)
        
        # 0.6 change over 2 hours = 0.3/hour (above 0.1 threshold)
        assert result.velocity == TrendVelocity.RAPID
    
    def test_moderate_velocity(self, trend_analyzer, base_timestamp):
        """Test moderate velocity detection."""
        scores = [0.3, 0.35, 0.4, 0.45, 0.5]  # 0.2 change
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=60)
        
        result = trend_analyzer.analyze(scores, timestamps)
        
        # 0.2 change over 4 hours = 0.05/hour
        assert result.velocity in [TrendVelocity.MODERATE, TrendVelocity.GRADUAL]
    
    def test_gradual_velocity(self, trend_analyzer, base_timestamp):
        """Test gradual velocity detection."""
        scores = [0.3, 0.32, 0.34, 0.36, 0.38]  # 0.08 change
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=120)
        
        result = trend_analyzer.analyze(scores, timestamps)
        
        # Small change over long time
        assert result.velocity in [TrendVelocity.GRADUAL, TrendVelocity.NONE]
    
    def test_no_velocity_stable(self, trend_analyzer, base_timestamp):
        """Test no velocity for stable scores."""
        scores = [0.4, 0.4, 0.4, 0.4, 0.4]
        timestamps = generate_timestamps(base_timestamp, 5)
        
        result = trend_analyzer.analyze(scores, timestamps)
        
        assert result.velocity == TrendVelocity.NONE


class TestScoreMetrics:
    """Tests for score metrics calculation."""
    
    def test_start_end_scores(self, trend_analyzer):
        """Test start and end scores are captured."""
        scores = [0.2, 0.4, 0.6, 0.8]
        
        result = trend_analyzer.analyze(scores)
        
        # Note: scores may be smoothed, so compare approximately
        # 3-point smoothing affects edge values
        assert abs(result.start_score - 0.3) < 0.15  # Smoothed from 0.2
        assert abs(result.end_score - 0.7) < 0.15   # Smoothed from 0.8
    
    def test_min_max_scores(self, trend_analyzer):
        """Test min and max scores are found."""
        scores = [0.3, 0.5, 0.2, 0.8, 0.6]
        
        result = trend_analyzer.analyze(scores)
        
        # After smoothing, values may shift but min/max should be reasonable
        assert result.min_score <= 0.35  # Around 0.2-0.3
        assert result.max_score >= 0.65  # Around 0.7-0.8
    
    def test_score_delta_calculation(self, trend_analyzer):
        """Test score delta is calculated correctly."""
        scores = [0.2, 0.4, 0.6, 0.8]
        
        result = trend_analyzer.analyze(scores)
        
        # Delta based on smoothed start/end scores
        # Smoothing shifts edge values inward, reducing delta
        assert result.score_delta >= 0.35  # Positive direction
        assert result.score_delta <= 0.7   # Upper bound


class TestTimeMetrics:
    """Tests for time-based metrics."""
    
    def test_time_span_calculation(self, trend_analyzer, base_timestamp):
        """Test time span is calculated correctly."""
        scores = [0.3, 0.4, 0.5, 0.6]
        timestamps = generate_timestamps(base_timestamp, 4, interval_minutes=60)
        
        result = trend_analyzer.analyze(scores, timestamps)
        
        # 4 timestamps, 60 min apart = 3 hours
        assert abs(result.time_span_hours - 3.0) < 0.1
    
    def test_rate_per_hour(self, trend_analyzer, base_timestamp):
        """Test rate per hour calculation."""
        scores = [0.2, 0.4, 0.6, 0.8]
        timestamps = generate_timestamps(base_timestamp, 4, interval_minutes=60)
        
        result = trend_analyzer.analyze(scores, timestamps)
        
        # 0.6 change over 3 hours = 0.2/hour
        assert abs(result.rate_per_hour - 0.2) < 0.1
    
    def test_no_timestamps(self, trend_analyzer):
        """Test analysis without timestamps."""
        scores = [0.2, 0.4, 0.6, 0.8]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.time_span_hours == 0.0
        assert result.rate_per_hour == 0.0


class TestInflectionPoints:
    """Tests for inflection point detection."""
    
    def test_no_inflection_monotonic(self, trend_analyzer):
        """Test no inflection points for monotonic sequence."""
        scores = [0.2, 0.3, 0.4, 0.5, 0.6]
        
        result = trend_analyzer.analyze(scores)
        
        assert len(result.inflection_points) == 0
    
    def test_single_inflection(self, trend_analyzer):
        """Test single inflection point detection."""
        scores = [0.2, 0.4, 0.6, 0.5, 0.4]  # Up then down
        
        result = trend_analyzer.analyze(scores)
        
        # Should detect the peak around index 2
        assert len(result.inflection_points) >= 1
    
    def test_multiple_inflections(self, trend_analyzer):
        """Test multiple inflection points detection."""
        scores = [0.2, 0.5, 0.3, 0.6, 0.4, 0.7]  # Oscillating
        
        result = trend_analyzer.analyze(scores)
        
        # Should detect multiple direction changes
        assert len(result.inflection_points) >= 2


class TestSmoothing:
    """Tests for score smoothing."""
    
    def test_smoothed_scores_returned(self, trend_analyzer):
        """Test smoothed scores are in result."""
        scores = [0.2, 0.4, 0.3, 0.5, 0.6]
        
        result = trend_analyzer.analyze(scores)
        
        assert len(result.smoothed_scores) == len(scores)
    
    def test_smoothing_reduces_noise(self, trend_analyzer):
        """Test smoothing reduces noise."""
        noisy_scores = [0.3, 0.8, 0.2, 0.7, 0.4, 0.6]
        
        result = trend_analyzer.analyze(noisy_scores)
        
        # Smoothed scores should have less extreme range
        smoothed_range = max(result.smoothed_scores) - min(result.smoothed_scores)
        raw_range = max(noisy_scores) - min(noisy_scores)
        
        assert smoothed_range <= raw_range


class TestConfidence:
    """Tests for confidence calculation."""
    
    def test_high_confidence_clear_trend(self, trend_analyzer):
        """Test high confidence for clear monotonic trend."""
        scores = [0.1, 0.25, 0.4, 0.55, 0.7, 0.85]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.confidence >= 0.4
    
    def test_lower_confidence_noisy(self, trend_analyzer):
        """Test lower confidence for noisy data."""
        scores = [0.3, 0.5, 0.35, 0.55, 0.4, 0.6]
        
        result = trend_analyzer.analyze(scores)
        
        # Volatile data should have lower confidence
        # or be marked as volatile direction
        if result.direction != TrendDirection.VOLATILE:
            assert result.confidence <= 0.7
    
    def test_confidence_stable(self, trend_analyzer):
        """Test moderate confidence for stable trend."""
        scores = [0.4, 0.41, 0.39, 0.4, 0.42]
        
        result = trend_analyzer.analyze(scores)
        
        # Stable trends get moderate confidence
        assert 0.2 <= result.confidence <= 0.8


class TestTrajectorySummary:
    """Tests for trajectory summary generation."""
    
    def test_worsening_summary(self, trend_analyzer, base_timestamp):
        """Test worsening trajectory summary."""
        scores = generate_worsening_scores(5)
        timestamps = generate_timestamps(base_timestamp, 5, interval_minutes=30)
        
        result = trend_analyzer.analyze(scores, timestamps)
        summary = trend_analyzer.get_trajectory_summary(result)
        
        assert "worsening" in summary.lower()
        if result.velocity == TrendVelocity.RAPID:
            assert "rapidly" in summary.lower()
    
    def test_improving_summary(self, trend_analyzer):
        """Test improving trajectory summary."""
        scores = generate_improving_scores(5)
        
        result = trend_analyzer.analyze(scores)
        summary = trend_analyzer.get_trajectory_summary(result)
        
        assert "improving" in summary.lower()
    
    def test_stable_summary(self, trend_analyzer):
        """Test stable trajectory summary."""
        scores = generate_stable_scores(0.4, 5)
        
        result = trend_analyzer.analyze(scores)
        summary = trend_analyzer.get_trajectory_summary(result)
        
        assert "stable" in summary.lower()


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_two_scores(self, trend_analyzer):
        """Test with minimum two scores."""
        scores = [0.2, 0.8]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.WORSENING
        assert result.score_delta > 0.5
    
    def test_identical_scores(self, trend_analyzer):
        """Test with all identical scores."""
        scores = [0.5, 0.5, 0.5, 0.5]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.STABLE
        assert result.score_delta == 0.0
    
    def test_extreme_scores(self, trend_analyzer):
        """Test with extreme score values."""
        scores = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        result = trend_analyzer.analyze(scores)
        
        assert result.direction == TrendDirection.WORSENING
        # Smoothing reduces delta from edges
        assert result.score_delta >= 0.6  # Still significant
        assert result.score_delta <= 1.0  # Bounded


class TestConfigAccess:
    """Tests for configuration access."""
    
    def test_is_enabled(self, trend_analyzer):
        """Test is_enabled returns correct value."""
        assert trend_analyzer.is_enabled() is True
    
    def test_get_config(self, trend_analyzer):
        """Test get_config returns config object."""
        config = trend_analyzer.get_config()
        
        assert isinstance(config, TrendAnalysisConfig)
        assert config.enabled is True
        assert config.worsening_threshold == 0.15
        assert config.improving_threshold == -0.15


# =============================================================================
# Export
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
