"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Phase 6 Sprint 2 Tests - FE-001 (Timezone) and FE-003 (Truncation)
---
FILE VERSION: v5.0-6-2.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 2
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

TEST COVERAGE:
- FE-001: User timezone support for late night detection
- FE-003: Smart text truncation for long inputs
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

# Module version
__version__ = "v5.0-6-2.0-1"


# =============================================================================
# FE-001: Timezone Support Tests
# =============================================================================

class TestTimezoneSupport:
    """Tests for FE-001: User Timezone Support."""
    
    def test_convert_utc_to_eastern(self):
        """Test UTC to America/New_York conversion."""
        from src.context.temporal_detector import TemporalDetector
        from src.managers import ContextConfigManager
        
        # Create mock config manager
        config_manager = MagicMock(spec=ContextConfigManager)
        config_manager.get_temporal_detection_config.return_value = MagicMock(
            enabled=True,
            late_night_start_hour=22,
            late_night_end_hour=4,
            late_night_risk_modifier=1.2,
            rapid_posting_threshold_minutes=30,
            rapid_posting_message_count=5,
            weekend_risk_modifier=1.1,
        )
        
        detector = TemporalDetector(config_manager)
        
        # 3 AM UTC = 10 PM EST (previous day) in winter
        utc_time = datetime(2026, 1, 1, 3, 0, tzinfo=timezone.utc)
        local_time = detector._convert_to_local_time(utc_time, "America/New_York")
        
        assert local_time is not None
        # In January, EST is UTC-5, so 3 AM UTC = 10 PM EST
        assert local_time.hour == 22
    
    def test_convert_utc_to_tokyo(self):
        """Test UTC to Asia/Tokyo conversion."""
        from src.context.temporal_detector import TemporalDetector
        from src.managers import ContextConfigManager
        
        config_manager = MagicMock(spec=ContextConfigManager)
        config_manager.get_temporal_detection_config.return_value = MagicMock(
            enabled=True,
            late_night_start_hour=22,
            late_night_end_hour=4,
            late_night_risk_modifier=1.2,
            rapid_posting_threshold_minutes=30,
            rapid_posting_message_count=5,
            weekend_risk_modifier=1.1,
        )
        
        detector = TemporalDetector(config_manager)
        
        # 15:00 UTC = 00:00 JST (next day)
        utc_time = datetime(2026, 1, 1, 15, 0, tzinfo=timezone.utc)
        local_time = detector._convert_to_local_time(utc_time, "Asia/Tokyo")
        
        assert local_time is not None
        # JST is UTC+9
        assert local_time.hour == 0
    
    def test_invalid_timezone_returns_none(self):
        """Test that invalid timezone returns None."""
        from src.context.temporal_detector import TemporalDetector
        from src.managers import ContextConfigManager
        
        config_manager = MagicMock(spec=ContextConfigManager)
        config_manager.get_temporal_detection_config.return_value = MagicMock(
            enabled=True,
            late_night_start_hour=22,
            late_night_end_hour=4,
            late_night_risk_modifier=1.2,
            rapid_posting_threshold_minutes=30,
            rapid_posting_message_count=5,
            weekend_risk_modifier=1.1,
        )
        
        detector = TemporalDetector(config_manager)
        
        utc_time = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
        local_time = detector._convert_to_local_time(utc_time, "Invalid/Timezone")
        
        assert local_time is None
    
    def test_is_valid_timezone(self):
        """Test timezone validation helper."""
        from src.context.temporal_detector import TemporalDetector
        from src.managers import ContextConfigManager
        
        config_manager = MagicMock(spec=ContextConfigManager)
        config_manager.get_temporal_detection_config.return_value = MagicMock(
            enabled=True,
            late_night_start_hour=22,
            late_night_end_hour=4,
            late_night_risk_modifier=1.2,
            rapid_posting_threshold_minutes=30,
            rapid_posting_message_count=5,
            weekend_risk_modifier=1.1,
        )
        
        detector = TemporalDetector(config_manager)
        
        assert detector.is_valid_timezone("America/New_York") is True
        assert detector.is_valid_timezone("Europe/London") is True
        assert detector.is_valid_timezone("UTC") is True
        assert detector.is_valid_timezone("Invalid/Timezone") is False
        assert detector.is_valid_timezone("NotATimezone") is False
    
    def test_late_night_detection_with_timezone(self):
        """Test late night detection uses user's local time."""
        from src.context.temporal_detector import TemporalDetector, TimeOfDayRisk
        from src.managers import ContextConfigManager
        
        config_manager = MagicMock(spec=ContextConfigManager)
        config_manager.get_temporal_detection_config.return_value = MagicMock(
            enabled=True,
            late_night_start_hour=22,  # 10 PM
            late_night_end_hour=4,      # 4 AM
            late_night_risk_modifier=1.2,
            rapid_posting_threshold_minutes=30,
            rapid_posting_message_count=5,
            weekend_risk_modifier=1.1,
        )
        
        detector = TemporalDetector(config_manager)
        
        # 3 AM UTC would be:
        # - 10 PM EST (late night) in New York
        # - 3 AM UTC (late night) without timezone
        utc_time = datetime(2026, 1, 1, 3, 0, tzinfo=timezone.utc)
        
        # Without timezone: 3 AM UTC is late night
        result_utc = detector.analyze([utc_time], utc_time, user_timezone=None)
        assert result_utc.late_night_detected is True
        assert result_utc.hour_of_day == 3
        
        # With NY timezone: 10 PM EST is late night
        result_ny = detector.analyze([utc_time], utc_time, user_timezone="America/New_York")
        assert result_ny.late_night_detected is True
        assert result_ny.user_timezone == "America/New_York"
        assert result_ny.local_hour == 22  # 10 PM EST
    
    def test_analyze_returns_timezone_info(self):
        """Test that analyze result includes timezone metadata."""
        from src.context.temporal_detector import TemporalDetector
        from src.managers import ContextConfigManager
        
        config_manager = MagicMock(spec=ContextConfigManager)
        config_manager.get_temporal_detection_config.return_value = MagicMock(
            enabled=True,
            late_night_start_hour=22,
            late_night_end_hour=4,
            late_night_risk_modifier=1.2,
            rapid_posting_threshold_minutes=30,
            rapid_posting_message_count=5,
            weekend_risk_modifier=1.1,
        )
        
        detector = TemporalDetector(config_manager)
        
        utc_time = datetime(2026, 1, 1, 14, 0, tzinfo=timezone.utc)  # 2 PM UTC
        
        result = detector.analyze(
            [utc_time], 
            utc_time, 
            user_timezone="Europe/London"
        )
        
        assert result.user_timezone == "Europe/London"
        assert result.local_hour == 14  # 2 PM GMT (same as UTC in winter)


# =============================================================================
# FE-003: Text Truncation Tests
# =============================================================================

class TestTextTruncation:
    """Tests for FE-003: Smart Text Truncation."""
    
    def test_no_truncation_needed(self):
        """Test that short text is not truncated."""
        from src.utils.text_truncation import create_text_truncator
        
        truncator = create_text_truncator(max_tokens=512)
        
        short_text = "This is a short message."
        result = truncator.truncate(short_text)
        
        assert result.was_truncated is False
        assert result.text == short_text
        assert result.original_tokens == result.final_tokens
    
    def test_simple_truncation(self):
        """Test simple head truncation."""
        from src.utils.text_truncation import create_text_truncator
        
        truncator = create_text_truncator(max_tokens=10, strategy="head")
        
        # 10 tokens * 4 chars = ~40 chars max
        long_text = "A" * 100  # Much longer than 40 chars
        result = truncator.truncate(long_text)
        
        assert result.was_truncated is True
        assert len(result.text) < len(long_text)
        assert result.text.endswith("...")
    
    def test_smart_truncation_preserves_sentences(self):
        """Test smart truncation preserves complete sentences."""
        from src.utils.text_truncation import create_text_truncator
        
        truncator = create_text_truncator(max_tokens=20, strategy="smart")
        
        # ~80 chars max (20 * 4)
        long_text = (
            "First sentence here. Second sentence follows. "
            "Third sentence is here. Fourth sentence now. "
            "Fifth sentence added. Sixth sentence too."
        )
        result = truncator.truncate(long_text)
        
        assert result.was_truncated is True
        # Should preserve sentence boundaries
        assert result.text.endswith(".") or result.text.startswith("...")
    
    def test_tail_truncation(self):
        """Test tail truncation keeps end of text."""
        from src.utils.text_truncation import create_text_truncator
        
        truncator = create_text_truncator(max_tokens=10, strategy="tail")
        
        long_text = "Beginning text here. " + "Middle text. " * 10 + "End text here."
        result = truncator.truncate(long_text)
        
        assert result.was_truncated is True
        assert result.text.startswith("...")
        assert "End text here" in result.text
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        from src.utils.text_truncation import estimate_tokens
        
        # 4 chars per token estimate
        text = "A" * 40
        tokens = estimate_tokens(text)
        assert tokens == 10  # 40 / 4
        
        empty = estimate_tokens("")
        assert empty == 0
    
    def test_truncation_result_metadata(self):
        """Test that truncation result includes correct metadata."""
        from src.utils.text_truncation import create_text_truncator, TruncationStrategy
        
        truncator = create_text_truncator(max_tokens=10, strategy="smart")
        
        long_text = "A" * 200
        result = truncator.truncate(long_text)
        
        assert result.was_truncated is True
        assert result.original_tokens > result.final_tokens
        assert result.strategy_used == TruncationStrategy.SMART
    
    def test_convenience_function(self):
        """Test truncate_text convenience function."""
        from src.utils.text_truncation import truncate_text
        
        short_text = "Short message."
        assert truncate_text(short_text) == short_text
        
        long_text = "A" * 5000
        truncated = truncate_text(long_text, max_tokens=100)
        assert len(truncated) < len(long_text)
    
    def test_needs_truncation(self):
        """Test needs_truncation check."""
        from src.utils.text_truncation import create_text_truncator
        
        truncator = create_text_truncator(max_tokens=10)
        
        assert truncator.needs_truncation("Short.") is False
        assert truncator.needs_truncation("A" * 200) is True
    
    def test_get_stats(self):
        """Test get_stats method."""
        from src.utils.text_truncation import create_text_truncator
        
        truncator = create_text_truncator(max_tokens=100, strategy="smart")
        
        stats = truncator.get_stats("Test message here.")
        
        assert "characters" in stats
        assert "estimated_tokens" in stats
        assert "max_tokens" in stats
        assert "needs_truncation" in stats
        assert "strategy" in stats
        assert stats["strategy"] == "smart"


# =============================================================================
# Integration Tests
# =============================================================================

class TestSprint2Integration:
    """Integration tests for Sprint 2 features."""
    
    def test_api_schema_has_timezone_field(self):
        """Test that AnalyzeRequest includes user_timezone field."""
        from src.api.schemas import AnalyzeRequest
        
        request = AnalyzeRequest(
            message="Test message",
            user_timezone="America/Los_Angeles",
        )
        
        assert request.user_timezone == "America/Los_Angeles"
    
    def test_temporal_factors_response_has_timezone_fields(self):
        """Test that TemporalFactorsResponse includes timezone fields."""
        from src.api.schemas import TemporalFactorsResponse
        
        response = TemporalFactorsResponse(
            late_night_risk=True,
            rapid_posting=False,
            time_risk_modifier=1.2,
            hour_of_day=22,
            is_weekend=False,
            user_timezone="America/New_York",
            local_hour=22,
        )
        
        assert response.user_timezone == "America/New_York"
        assert response.local_hour == 22
    
    def test_config_has_truncation_settings(self):
        """Test that default config includes truncation settings."""
        import json
        import os
        
        # Try multiple possible config paths
        config_paths = [
            "/app/config/default.json",
            "/app/src/config/default.json",
            "src/config/default.json",
            "config/default.json",
        ]
        
        config = None
        for path in config_paths:
            if os.path.exists(path):
                with open(path) as f:
                    config = json.load(f)
                break
        
        if config is None:
            pytest.skip("Config file not found in expected locations")
        
        assert "models" in config
        models_config = config["models"]
        
        # Check defaults include truncation settings
        assert "defaults" in models_config
        defaults = models_config["defaults"]
        assert "max_input_tokens" in defaults
        assert "truncation_strategy" in defaults
        assert defaults["max_input_tokens"] == 512
        assert defaults["truncation_strategy"] == "smart"


# =============================================================================
# Export test classes
# =============================================================================

__all__ = [
    "TestTimezoneSupport",
    "TestTextTruncation", 
    "TestSprint2Integration",
]
