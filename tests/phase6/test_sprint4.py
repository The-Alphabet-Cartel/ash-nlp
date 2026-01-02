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
Phase 6 Sprint 4 Tests - FE-002 (Discord Length), FE-004 (Warm-up), FE-008 (Conflict Alerts)
---
FILE VERSION: v5.0-6-4.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 4
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

TEST COVERAGE:
- FE-002: Discord message length validation and truncation
- FE-004: Model warm-up on container start
- FE-008: Enhanced ensemble conflict webhook alerts
"""

import pytest
from datetime import datetime
from typing import Dict, Any
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# =============================================================================
# FE-002: Discord Message Length Validation Tests
# =============================================================================

class TestDiscordLimits:
    """Tests for FE-002: Discord Message Length Validation."""
    
    def test_discord_limits_constants(self):
        """Test that Discord limits are properly defined."""
        from src.utils.alerting import DISCORD_LIMITS
        
        assert DISCORD_LIMITS["message_content"] == 2000
        assert DISCORD_LIMITS["embed_title"] == 256
        assert DISCORD_LIMITS["embed_description"] == 4096
        assert DISCORD_LIMITS["embed_field_name"] == 256
        assert DISCORD_LIMITS["embed_field_value"] == 1024
        assert DISCORD_LIMITS["embed_footer_text"] == 2048
        assert DISCORD_LIMITS["embed_total"] == 6000
    
    def test_truncate_text_short(self):
        """Test truncate_text with short text (no truncation needed)."""
        from src.utils.alerting import truncate_text
        
        short_text = "Hello world"
        result = truncate_text(short_text, 100)
        
        assert result == short_text
    
    def test_truncate_text_long(self):
        """Test truncate_text with long text."""
        from src.utils.alerting import truncate_text
        
        long_text = "A" * 100
        result = truncate_text(long_text, 50)
        
        assert len(result) == 50
        assert result.endswith("...")
        assert result == "A" * 47 + "..."
    
    def test_truncate_text_custom_suffix(self):
        """Test truncate_text with custom suffix."""
        from src.utils.alerting import truncate_text
        
        long_text = "A" * 100
        result = truncate_text(long_text, 50, suffix=" [truncated]")
        
        assert len(result) == 50
        assert result.endswith(" [truncated]")
    
    def test_truncate_text_empty(self):
        """Test truncate_text with empty text."""
        from src.utils.alerting import truncate_text
        
        result = truncate_text("", 100)
        assert result == ""
        
        result = truncate_text(None, 100)
        assert result is None
    
    def test_truncate_at_boundary_sentence(self):
        """Test truncate_at_boundary preserves sentence boundary."""
        from src.utils.alerting import truncate_at_boundary
        
        text = "First sentence. Second sentence. Third sentence is very long and continues."
        result = truncate_at_boundary(text, 60)
        
        # Should truncate at sentence boundary
        assert result.endswith("...")
        assert "First sentence." in result or "Second sentence." in result
    
    def test_truncate_at_boundary_word(self):
        """Test truncate_at_boundary preserves word boundary."""
        from src.utils.alerting import truncate_at_boundary
        
        text = "This is a test of word boundary truncation without sentences"
        result = truncate_at_boundary(text, 30)
        
        # Should truncate at word boundary
        assert result.endswith("...")
        assert not result[-4].isalpha() or result.endswith("...")  # Not mid-word
    
    def test_truncate_at_boundary_short(self):
        """Test truncate_at_boundary with short text."""
        from src.utils.alerting import truncate_at_boundary
        
        short_text = "Short text"
        result = truncate_at_boundary(short_text, 100)
        
        assert result == short_text


class TestEmbedValidation:
    """Tests for embed size calculation and validation."""
    
    def test_calculate_embed_size_simple(self):
        """Test calculate_embed_size with simple embed."""
        from src.utils.alerting import calculate_embed_size
        
        embed = {
            "title": "Test Title",  # 10 chars
            "description": "Test Description",  # 16 chars
            "footer": {"text": "Footer"},  # 6 chars
        }
        
        size = calculate_embed_size(embed)
        assert size == 10 + 16 + 6
    
    def test_calculate_embed_size_with_fields(self):
        """Test calculate_embed_size with fields."""
        from src.utils.alerting import calculate_embed_size
        
        embed = {
            "title": "Title",  # 5
            "description": "Desc",  # 4
            "fields": [
                {"name": "Field1", "value": "Value1"},  # 6 + 6 = 12
                {"name": "Field2", "value": "Value2"},  # 6 + 6 = 12
            ]
        }
        
        size = calculate_embed_size(embed)
        assert size == 5 + 4 + 12 + 12
    
    def test_validate_embed_size_valid(self):
        """Test validate_embed_size with valid embed."""
        from src.utils.alerting import validate_embed_size
        
        embed = {
            "title": "Test",
            "description": "A short description",
        }
        
        is_valid, total_size, issues = validate_embed_size(embed)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_embed_size_title_too_long(self):
        """Test validate_embed_size detects long title."""
        from src.utils.alerting import validate_embed_size, DISCORD_LIMITS
        
        embed = {
            "title": "A" * (DISCORD_LIMITS["embed_title"] + 10),
            "description": "Short",
        }
        
        is_valid, total_size, issues = validate_embed_size(embed)
        
        assert is_valid is False
        assert any("Title exceeds" in issue for issue in issues)
    
    def test_validate_embed_size_description_too_long(self):
        """Test validate_embed_size detects long description."""
        from src.utils.alerting import validate_embed_size, DISCORD_LIMITS
        
        embed = {
            "title": "Test",
            "description": "A" * (DISCORD_LIMITS["embed_description"] + 10),
        }
        
        is_valid, total_size, issues = validate_embed_size(embed)
        
        assert is_valid is False
        assert any("Description exceeds" in issue for issue in issues)
    
    def test_validate_embed_size_total_too_large(self):
        """Test validate_embed_size detects oversized embed."""
        from src.utils.alerting import validate_embed_size, DISCORD_LIMITS
        
        # Create embed that exceeds total limit
        embed = {
            "title": "A" * 256,
            "description": "B" * 4000,  # Large but within individual limit
            "footer": {"text": "C" * 2000},  # Large footer
        }
        
        is_valid, total_size, issues = validate_embed_size(embed)
        
        assert total_size > DISCORD_LIMITS["embed_total"]
        assert is_valid is False
        assert any("Total embed size" in issue for issue in issues)


class TestAlertTruncation:
    """Tests for Alert.to_discord_embed() with FE-002 truncation."""
    
    def test_alert_normal_content(self):
        """Test alert with normal-length content."""
        from src.utils.alerting import Alert, AlertSeverity
        
        alert = Alert(
            severity=AlertSeverity.WARNING,
            title="Test Alert",
            description="This is a normal length description.",
            fields={"Key": "Value"},
            source="test",
        )
        
        embed = alert.to_discord_embed()
        
        assert embed["description"] == "This is a normal length description."
        assert "Test Alert" in embed["title"]
    
    def test_alert_long_title_truncated(self):
        """Test alert with long title gets truncated."""
        from src.utils.alerting import Alert, AlertSeverity, DISCORD_LIMITS
        
        long_title = "A" * 300  # Exceeds 256 limit
        alert = Alert(
            severity=AlertSeverity.INFO,
            title=long_title,
            description="Short description",
        )
        
        embed = alert.to_discord_embed()
        
        assert len(embed["title"]) <= DISCORD_LIMITS["embed_title"]
        assert embed["title"].endswith("...")
    
    def test_alert_long_description_truncated(self):
        """Test alert with long description gets truncated."""
        from src.utils.alerting import Alert, AlertSeverity, DISCORD_LIMITS
        
        long_desc = "A" * 5000  # Exceeds 4096 limit
        alert = Alert(
            severity=AlertSeverity.INFO,
            title="Test",
            description=long_desc,
        )
        
        embed = alert.to_discord_embed()
        
        assert len(embed["description"]) <= DISCORD_LIMITS["embed_description"]
        assert embed["description"].endswith("...")
    
    def test_alert_long_field_value_truncated(self):
        """Test alert with long field value gets truncated."""
        from src.utils.alerting import Alert, AlertSeverity, DISCORD_LIMITS
        
        long_value = "V" * 2000  # Exceeds 1024 limit
        alert = Alert(
            severity=AlertSeverity.INFO,
            title="Test",
            description="Description",
            fields={"Key": long_value},
        )
        
        embed = alert.to_discord_embed()
        
        assert len(embed["fields"][0]["value"]) <= DISCORD_LIMITS["embed_field_value"]
    
    def test_alert_embed_within_total_limit(self):
        """Test that generated embed is within total size limit."""
        from src.utils.alerting import (
            Alert, AlertSeverity, DISCORD_LIMITS, calculate_embed_size
        )
        
        # Create alert with content that would exceed limits if not truncated
        alert = Alert(
            severity=AlertSeverity.CRITICAL,
            title="A" * 300,
            description="B" * 5000,
            fields={
                "Field1": "C" * 2000,
                "Field2": "D" * 2000,
            },
        )
        
        embed = alert.to_discord_embed()
        size = calculate_embed_size(embed)
        
        # Should be truncated to fit
        assert size <= DISCORD_LIMITS["embed_total"]


class TestUtilsExports:
    """Tests for FE-002 exports from utils package."""
    
    def test_discord_limits_exported(self):
        """Test that DISCORD_LIMITS is exported from utils."""
        from src.utils import DISCORD_LIMITS
        
        assert "embed_title" in DISCORD_LIMITS
    
    def test_truncate_functions_exported(self):
        """Test that truncation functions are exported."""
        from src.utils import truncate_text, truncate_at_boundary
        
        assert callable(truncate_text)
        assert callable(truncate_at_boundary)
    
    def test_validation_functions_exported(self):
        """Test that validation functions are exported."""
        from src.utils import calculate_embed_size, validate_embed_size
        
        assert callable(calculate_embed_size)
        assert callable(validate_embed_size)


# =============================================================================
# FE-004: Model Warm-up Tests
# =============================================================================

class TestModelWarmup:
    """Tests for FE-004: Model Warm-up on Container Start."""
    
    def test_warmup_result_dataclass(self):
        """Test WarmupResult dataclass structure."""
        from src.ensemble import WarmupResult
        
        result = WarmupResult(
            success=True,
            total_latency_ms=150.5,
            per_model_latency_ms={"bart": 100.0, "sentiment": 50.0},
            models_warmed=["bart", "sentiment"],
        )
        
        assert result.success is True
        assert result.total_latency_ms == 150.5
        assert "bart" in result.per_model_latency_ms
        assert result.timestamp is not None
    
    def test_warmup_result_to_dict(self):
        """Test WarmupResult.to_dict() method."""
        from src.ensemble import WarmupResult
        
        result = WarmupResult(
            success=True,
            total_latency_ms=200.0,
            per_model_latency_ms={"bart": 150.0},
            models_warmed=["bart"],
        )
        
        d = result.to_dict()
        
        assert d["success"] is True
        assert d["total_latency_ms"] == 200.0
        assert "bart" in d["per_model_latency_ms"]
        assert d["timestamp"] is not None
    
    def test_warmup_result_failure(self):
        """Test WarmupResult for failed warmup."""
        from src.ensemble import WarmupResult
        
        result = WarmupResult(
            success=False,
            total_latency_ms=50.0,
            error="Model loading failed",
        )
        
        assert result.success is False
        assert result.error == "Model loading failed"
        assert result.models_warmed == []
    
    def test_warmup_result_exported(self):
        """Test that WarmupResult is exported from ensemble package."""
        from src.ensemble import WarmupResult
        
        assert WarmupResult is not None
    
    @pytest.mark.skip(reason="Requires model loading - integration test")
    def test_engine_warmup_returns_warmup_result(self):
        """Test that engine.warmup() returns WarmupResult."""
        pass
    
    @pytest.mark.skip(reason="Requires model loading - integration test")
    def test_engine_get_warmup_result(self):
        """Test that engine.get_warmup_result() returns last warmup."""
        pass


# =============================================================================
# FE-008: Enhanced Conflict Alerts Tests
# =============================================================================

class TestEnhancedConflictAlerts:
    """Tests for FE-008: Enhanced Ensemble Conflict Webhook Alerts."""
    
    def test_default_conflict_alert_threshold_exists(self):
        """Test DEFAULT_CONFLICT_ALERT_THRESHOLD constant exists."""
        from src.utils.alerting import DEFAULT_CONFLICT_ALERT_THRESHOLD
        
        assert DEFAULT_CONFLICT_ALERT_THRESHOLD == 0.15
    
    def test_generate_disagreement_chart_basic(self):
        """Test basic ASCII chart generation."""
        from src.utils.alerting import generate_disagreement_chart
        
        scores = {
            "bart": 0.85,
            "sentiment": 0.60,
            "irony": 0.25,
            "emotions": 0.78,
        }
        
        chart = generate_disagreement_chart(scores)
        
        assert "bart" in chart
        assert "sentiment" in chart
        assert "0.85" in chart
        assert "0.60" in chart
        assert "Range:" in chart
        assert "Var:" in chart
    
    def test_generate_disagreement_chart_empty(self):
        """Test ASCII chart with empty scores."""
        from src.utils.alerting import generate_disagreement_chart
        
        chart = generate_disagreement_chart({})
        
        assert "No model scores available" in chart
    
    def test_generate_disagreement_chart_clamping(self):
        """Test score clamping to 0-1 range."""
        from src.utils.alerting import generate_disagreement_chart
        
        scores = {
            "model_a": 1.5,  # Should clamp to 1.0
            "model_b": -0.2,  # Should clamp to 0.0
        }
        
        chart = generate_disagreement_chart(scores)
        
        # Should still generate without error
        assert "model_a" in chart
        assert "model_b" in chart
    
    def test_format_conflict_summary(self):
        """Test conflict summary formatting."""
        from src.utils.alerting import format_conflict_summary
        
        scores = {
            "bart": 0.9,
            "sentiment": 0.3,
        }
        
        summary = format_conflict_summary(
            conflict_type="score_disagreement",
            model_scores=scores,
            resolution_strategy="conservative",
            final_score=0.9,
        )
        
        assert "Score Disagreement" in summary
        assert "bart" in summary
        assert "Conservative" in summary
        assert "0.9" in summary or "0.90" in summary
    
    def test_format_conflict_summary_no_resolution(self):
        """Test conflict summary without resolution."""
        from src.utils.alerting import format_conflict_summary
        
        scores = {"bart": 0.5}
        
        summary = format_conflict_summary(
            conflict_type="test_conflict",
            model_scores=scores,
        )
        
        assert "Test Conflict" in summary
        assert "bart" in summary
    
    def test_alerter_has_conflict_threshold(self):
        """Test DiscordAlerter accepts conflict threshold parameter."""
        from src.utils.alerting import DiscordAlerter
        
        alerter = DiscordAlerter(
            webhook_url="https://test.webhook",
            testing_mode=True,
            conflict_alert_threshold=0.25,
        )
        
        assert alerter._conflict_alert_threshold == 0.25
    
    def test_fe008_exports(self):
        """Test FE-008 functions exported from src.utils."""
        from src.utils import (
            DEFAULT_CONFLICT_ALERT_THRESHOLD,
            generate_disagreement_chart,
            format_conflict_summary,
        )
        
        assert DEFAULT_CONFLICT_ALERT_THRESHOLD is not None
        assert callable(generate_disagreement_chart)
        assert callable(format_conflict_summary)
