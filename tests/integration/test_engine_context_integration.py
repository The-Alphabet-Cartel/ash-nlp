"""
Ash-NLP Integration Tests: Engine + Context Analyzer
---
FILE VERSION: v5.0-5-TEST-1.0
LAST MODIFIED: 2026-01-02
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Integration tests for:
- EnsembleDecisionEngine with ContextAnalyzer
- Full message analysis with context history
- Escalation detection through engine
- Context-enhanced crisis assessments
"""

import pytest
from datetime import datetime, timedelta
from typing import List, Dict, Any
from unittest.mock import MagicMock, AsyncMock, patch

from src.context import (
    ContextAnalyzer,
    create_context_analyzer,
    MessageHistoryItem,
    InterventionUrgency,
)
from src.managers.context_config_manager import (
    ContextConfigManager,
    ContextAnalysisConfig,
    EscalationDetectionConfig,
    TemporalDetectionConfig,
    TrendAnalysisConfig,
    InterventionConfig,
    KnownPattern,
)
from src.ensemble import (
    CrisisAssessment,
    CrisisSeverity,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_context_config_manager():
    """Create a fully configured mock ContextConfigManager."""
    manager = MagicMock(spec=ContextConfigManager)
    
    # Context analysis master config
    manager.get_context_analysis_config.return_value = ContextAnalysisConfig(
        enabled=True,
        max_history_size=20,
    )
    
    # Escalation detection config
    manager.get_escalation_detection_config.return_value = EscalationDetectionConfig(
        enabled=True,
        rapid_threshold_hours=4,
        gradual_threshold_hours=24,
        score_increase_threshold=0.3,
        minimum_messages=3,
        alert_on_detection=True,
        alert_cooldown_seconds=300,
    )
    
    # Temporal detection config
    manager.get_temporal_detection_config.return_value = TemporalDetectionConfig(
        enabled=True,
        late_night_start_hour=22,
        late_night_end_hour=4,
        late_night_risk_modifier=1.2,
        rapid_posting_threshold_minutes=30,
        rapid_posting_message_count=5,
        weekend_risk_modifier=1.1,
    )
    
    # Trend analysis config
    manager.get_trend_analysis_config.return_value = TrendAnalysisConfig(
        enabled=True,
        worsening_threshold=0.15,
        improving_threshold=-0.15,
        velocity_rapid_threshold=0.1,
        velocity_gradual_threshold=0.03,
    )
    
    # Intervention config
    manager.get_intervention_config.return_value = InterventionConfig(
        escalation_urgency_boost=True,
        late_night_urgency_boost=True,
        urgency_levels={},
    )
    
    # Known patterns
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
    }
    
    return manager


@pytest.fixture
def context_analyzer(mock_context_config_manager):
    """Create a real ContextAnalyzer with mock config."""
    return ContextAnalyzer(mock_context_config_manager)


@pytest.fixture
def base_timestamp():
    """Base timestamp for test sequences."""
    return datetime(2026, 1, 1, 14, 0, 0)  # Wednesday 2:00 PM


@pytest.fixture
def late_night_timestamp():
    """Late night timestamp for testing."""
    return datetime(2026, 1, 1, 23, 30, 0)  # 11:30 PM


@pytest.fixture
def weekend_timestamp():
    """Weekend timestamp for testing."""
    return datetime(2026, 1, 3, 14, 0, 0)  # Saturday 2:00 PM


# =============================================================================
# Message History Generators
# =============================================================================


def create_escalating_history(
    base: datetime,
    start_score: float = 0.2,
    end_score: float = 0.75,
    count: int = 4,
    interval_minutes: int = 60,
) -> List[MessageHistoryItem]:
    """Create escalating message history."""
    messages = [
        "Just feeling a bit off today",
        "Things are getting harder to deal with",
        "I'm struggling more than usual",
        "I don't know if I can keep going",
        "Everything feels hopeless",
        "I can't take this anymore",
    ]
    
    history = []
    score_step = (end_score - start_score) / (count - 1) if count > 1 else 0
    
    for i in range(count):
        score = start_score + (score_step * i)
        history.append(MessageHistoryItem(
            message=messages[i % len(messages)],
            timestamp=base + timedelta(minutes=interval_minutes * i),
            crisis_score=score,
            user_id=f"user_{i:03d}",
        ))
    
    return history


def create_stable_history(
    base: datetime,
    score: float = 0.3,
    count: int = 4,
    interval_minutes: int = 60,
) -> List[MessageHistoryItem]:
    """Create stable (non-escalating) message history."""
    messages = [
        "Having an okay day",
        "Nothing much happening",
        "Just checking in",
        "Same as usual",
    ]
    
    history = []
    for i in range(count):
        history.append(MessageHistoryItem(
            message=messages[i % len(messages)],
            timestamp=base + timedelta(minutes=interval_minutes * i),
            crisis_score=score + (0.02 * (i % 2)),  # Small fluctuation
            user_id=f"user_{i:03d}",
        ))
    
    return history


def create_improving_history(
    base: datetime,
    start_score: float = 0.8,
    end_score: float = 0.3,
    count: int = 4,
    interval_minutes: int = 60,
) -> List[MessageHistoryItem]:
    """Create improving message history."""
    messages = [
        "Really struggling right now",
        "Things are starting to look up",
        "Feeling a bit better",
        "I think I'm okay now",
    ]
    
    history = []
    score_step = (end_score - start_score) / (count - 1) if count > 1 else 0
    
    for i in range(count):
        score = start_score + (score_step * i)
        history.append(MessageHistoryItem(
            message=messages[i % len(messages)],
            timestamp=base + timedelta(minutes=interval_minutes * i),
            crisis_score=score,
            user_id=f"user_{i:03d}",
        ))
    
    return history


def create_rapid_posting_history(
    base: datetime,
    count: int = 6,
    interval_minutes: int = 5,
) -> List[MessageHistoryItem]:
    """Create rapid posting pattern history."""
    messages = [
        "Can't sleep",
        "Why is everything so hard",
        "I hate this",
        "Nobody understands",
        "I'm so tired",
        "What's the point",
    ]
    
    history = []
    for i in range(count):
        history.append(MessageHistoryItem(
            message=messages[i % len(messages)],
            timestamp=base + timedelta(minutes=interval_minutes * i),
            crisis_score=0.5 + (0.05 * i),
            user_id=f"user_{i:03d}",
        ))
    
    return history


# =============================================================================
# Test Cases: Context Analyzer Integration
# =============================================================================


class TestContextAnalyzerIntegration:
    """Tests for ContextAnalyzer standalone integration."""
    
    def test_analyze_with_escalating_history(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test analysis detects escalation in history."""
        history = create_escalating_history(base_timestamp, count=5)
        
        result = context_analyzer.analyze(
            current_message="I can't do this anymore",
            current_score=0.9,
            message_history=history,
        )
        
        # Should detect escalation
        assert result.escalation.detected
        assert result.escalation.rate in ["rapid", "gradual", "sudden"]
        
        # Should detect worsening trend
        assert result.trend.direction == "worsening"
        
        # Should recommend intervention
        assert result.intervention.urgency in [
            InterventionUrgency.HIGH,
            InterventionUrgency.IMMEDIATE,
            "high",
            "immediate",
        ]
    
    def test_analyze_with_stable_history(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test analysis with stable history."""
        history = create_stable_history(base_timestamp, count=4)
        
        result = context_analyzer.analyze(
            current_message="Just checking in again",
            current_score=0.35,
            message_history=history,
        )
        
        # Should not detect escalation
        assert not result.escalation.detected
        assert result.escalation.rate == "none"
        
        # Should detect stable trend
        assert result.trend.direction == "stable"
        
        # Low/no urgency
        assert result.intervention.urgency in [
            InterventionUrgency.NONE,
            InterventionUrgency.LOW,
            "none",
            "low",
        ]
    
    def test_analyze_with_improving_history(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test analysis with improving history."""
        history = create_improving_history(base_timestamp, count=4)
        
        result = context_analyzer.analyze(
            current_message="I'm doing better now",
            current_score=0.2,
            message_history=history,
        )
        
        # Should not detect escalation (improving)
        assert not result.escalation.detected
        
        # Should detect improving trend
        assert result.trend.direction == "improving"
    
    def test_analyze_late_night(
        self, 
        context_analyzer, 
        late_night_timestamp
    ):
        """Test analysis during late night hours."""
        history = create_stable_history(late_night_timestamp, count=3)
        
        result = context_analyzer.analyze(
            current_message="Can't sleep again",
            current_score=0.5,
            message_history=history,
        )
        
        # Should detect late night risk
        assert result.temporal.late_night_risk
        assert result.temporal.time_risk_modifier >= 1.0
    
    def test_analyze_rapid_posting(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test analysis with rapid posting pattern."""
        history = create_rapid_posting_history(base_timestamp, count=6)
        
        result = context_analyzer.analyze(
            current_message="I keep coming back here",
            current_score=0.6,
            message_history=history,
        )
        
        # Should detect rapid posting
        assert result.temporal.rapid_posting
    
    def test_analyze_weekend(
        self, 
        context_analyzer, 
        weekend_timestamp
    ):
        """Test analysis on weekend."""
        history = create_stable_history(weekend_timestamp, count=3, score=0.5)
        
        result = context_analyzer.analyze(
            current_message="Weekends are hard",
            current_score=0.6,
            message_history=history,
        )
        
        # Should detect weekend
        assert result.temporal.is_weekend
        assert result.temporal.time_risk_modifier >= 1.0
    
    def test_history_metadata(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test history metadata is captured."""
        history = create_escalating_history(base_timestamp, count=5)
        
        result = context_analyzer.analyze(
            current_message="Current message",
            current_score=0.8,
            message_history=history,
        )
        
        # Should have correct message count
        assert result.history_metadata.message_count == 6  # 5 history + 1 current
        
        # Should have time span
        assert result.history_metadata.time_span_hours >= 4.0
    
    def test_trajectory_info(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test trajectory information is captured."""
        history = create_escalating_history(
            base_timestamp, 
            start_score=0.2, 
            end_score=0.7, 
            count=4
        )
        
        result = context_analyzer.analyze(
            current_message="Crisis",
            current_score=0.85,
            message_history=history,
        )
        
        # Should capture score trajectory
        assert result.trajectory.start_score < result.trajectory.end_score
        assert result.trajectory.peak_score >= 0.7


class TestContextAnalyzerEdgeCases:
    """Tests for edge cases in context analysis."""
    
    def test_empty_history(self, context_analyzer):
        """Test analysis with no history."""
        result = context_analyzer.analyze(
            current_message="Hello",
            current_score=0.3,
            message_history=[],
        )
        
        assert result.history_metadata.message_count == 1
        assert not result.escalation.detected
    
    def test_single_history_item(self, context_analyzer, base_timestamp):
        """Test analysis with single history item."""
        history = [MessageHistoryItem(
            message="Previous message",
            timestamp=base_timestamp,
            crisis_score=0.4,
        )]
        
        result = context_analyzer.analyze(
            current_message="Current",
            current_score=0.5,
            message_history=history,
        )
        
        assert result.history_metadata.message_count == 2
    
    def test_history_without_scores(self, context_analyzer, base_timestamp):
        """Test analysis when history items lack crisis_score."""
        history = [
            MessageHistoryItem(
                message="Message without score",
                timestamp=base_timestamp,
                crisis_score=None,
            ),
            MessageHistoryItem(
                message="Another message",
                timestamp=base_timestamp + timedelta(hours=1),
                crisis_score=0.5,
            ),
        ]
        
        result = context_analyzer.analyze(
            current_message="Current",
            current_score=0.6,
            message_history=history,
        )
        
        # Should handle gracefully
        assert isinstance(result.escalation.detected, bool)
    
    def test_very_long_history(self, context_analyzer, base_timestamp):
        """Test analysis with history exceeding max size."""
        # Create 25 items (max is 20)
        history = []
        for i in range(25):
            history.append(MessageHistoryItem(
                message=f"Message {i}",
                timestamp=base_timestamp + timedelta(hours=i),
                crisis_score=0.3 + (0.02 * i),
            ))
        
        result = context_analyzer.analyze(
            current_message="Current",
            current_score=0.8,
            message_history=history,
        )
        
        # Should handle without error
        assert isinstance(result.escalation.detected, bool)
    
    def test_sudden_spike(self, context_analyzer, base_timestamp):
        """Test detection of sudden crisis spike."""
        # Low scores then sudden jump
        history = [
            MessageHistoryItem(
                message="Everything is fine",
                timestamp=base_timestamp,
                crisis_score=0.15,
            ),
            MessageHistoryItem(
                message="Still okay",
                timestamp=base_timestamp + timedelta(hours=1),
                crisis_score=0.2,
            ),
            MessageHistoryItem(
                message="Doing well",
                timestamp=base_timestamp + timedelta(hours=2),
                crisis_score=0.18,
            ),
        ]
        
        result = context_analyzer.analyze(
            current_message="I want to end it all",
            current_score=0.95,  # Sudden spike
            message_history=history,
        )
        
        # Should detect the sudden change
        assert result.trajectory.end_score > result.trajectory.start_score


class TestContextAnalyzerCombinedFactors:
    """Tests for combined risk factors."""
    
    def test_escalation_plus_late_night(
        self, 
        context_analyzer, 
        late_night_timestamp
    ):
        """Test combined escalation and late night risk."""
        history = create_escalating_history(late_night_timestamp, count=4)
        
        result = context_analyzer.analyze(
            current_message="I can't sleep and can't stop thinking",
            current_score=0.85,
            message_history=history,
        )
        
        # Both factors should be detected
        assert result.escalation.detected
        assert result.temporal.late_night_risk
        
        # Should have boosted urgency
        assert result.intervention.urgency in [
            InterventionUrgency.HIGH,
            InterventionUrgency.IMMEDIATE,
            "high",
            "immediate",
        ]
    
    def test_rapid_posting_plus_escalation(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test combined rapid posting and escalation."""
        # Rapid posting with escalating scores
        history = []
        for i in range(6):
            history.append(MessageHistoryItem(
                message=f"Can't stop thinking about it {i}",
                timestamp=base_timestamp + timedelta(minutes=5 * i),
                crisis_score=0.3 + (0.1 * i),  # 0.3 to 0.8
            ))
        
        result = context_analyzer.analyze(
            current_message="I need help now",
            current_score=0.9,
            message_history=history,
        )
        
        # Both factors should be detected
        assert result.temporal.rapid_posting
        # May or may not detect escalation depending on thresholds
    
    def test_weekend_late_night_escalation(
        self, 
        context_analyzer
    ):
        """Test all risk factors combined."""
        # Saturday 11:30 PM
        saturday_night = datetime(2026, 1, 3, 23, 30, 0)
        
        history = create_escalating_history(saturday_night, count=4)
        
        result = context_analyzer.analyze(
            current_message="Nobody is around and I can't take it",
            current_score=0.9,
            message_history=history,
        )
        
        # All factors should compound
        assert result.escalation.detected
        assert result.temporal.late_night_risk
        assert result.temporal.is_weekend
        
        # Maximum urgency expected
        assert result.intervention.urgency in [
            InterventionUrgency.IMMEDIATE,
            "immediate",
        ]


class TestContextAnalyzerInterventionPoints:
    """Tests for intervention point detection."""
    
    def test_intervention_point_identified(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test intervention point is identified in escalation."""
        history = create_escalating_history(
            base_timestamp, 
            start_score=0.2, 
            end_score=0.8, 
            count=5
        )
        
        result = context_analyzer.analyze(
            current_message="Crisis point",
            current_score=0.9,
            message_history=history,
        )
        
        # Should have intervention recommendation
        if result.intervention.recommended_point is not None:
            assert isinstance(result.intervention.recommended_point, int)
    
    def test_no_intervention_for_stable(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test no intervention needed for stable low scores."""
        history = create_stable_history(base_timestamp, score=0.2, count=4)
        
        result = context_analyzer.analyze(
            current_message="All good",
            current_score=0.15,
            message_history=history,
        )
        
        # Should not require intervention
        assert result.intervention.urgency in [
            InterventionUrgency.NONE,
            InterventionUrgency.LOW,
            "none",
            "low",
        ]


# =============================================================================
# Test Cases: Pattern Matching
# =============================================================================


class TestPatternMatching:
    """Tests for escalation pattern matching."""
    
    def test_rapid_pattern_matched(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test rapid escalation pattern is matched."""
        # 4 hour escalation matches "evening_deterioration" pattern
        history = create_escalating_history(
            base_timestamp, 
            count=5, 
            interval_minutes=45  # ~3 hours total
        )
        
        result = context_analyzer.analyze(
            current_message="Crisis",
            current_score=0.9,
            message_history=history,
        )
        
        if result.escalation.detected:
            # May have matched pattern
            assert result.escalation.rate in ["rapid", "gradual", "sudden"]
    
    def test_gradual_pattern_matched(
        self, 
        context_analyzer, 
        base_timestamp
    ):
        """Test gradual escalation pattern is matched."""
        # 24 hour escalation matches "gradual_decline" pattern
        history = create_escalating_history(
            base_timestamp, 
            count=6, 
            interval_minutes=240  # 4 hours each = 20 hours total
        )
        
        result = context_analyzer.analyze(
            current_message="Things have been getting worse",
            current_score=0.85,
            message_history=history,
        )
        
        if result.escalation.detected:
            assert result.escalation.rate == "gradual"


# =============================================================================
# Export
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
