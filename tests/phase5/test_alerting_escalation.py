"""
Ash-NLP Phase 5 Tests: Discord Escalation Alerting
---
FILE VERSION: v5.0-6-TEST-1.1
LAST MODIFIED: 2026-01-02
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for:
- DiscordAlerter.send_escalation_alert() async method
- DiscordAlerter.send_escalation_alert_sync() sync method
- Escalation cooldown tracking
- Urgency-based severity mapping
- Alert field formatting
"""

import pytest
import time
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch

from src.utils.alerting import (
    DiscordAlerter,
    Alert,
    AlertSeverity,
    ThrottleConfig,
    create_discord_alerter,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def alerter_with_webhook():
    """Create alerter with test webhook URL."""
    return DiscordAlerter(
        webhook_url="https://discord.com/api/webhooks/test/token",
        enabled=True,
        escalation_cooldown_seconds=60.0,
        testing_mode=False,  # Explicitly disable to test real webhook flow with mocks
    )


@pytest.fixture
def alerter_disabled():
    """Create disabled alerter."""
    return DiscordAlerter(
        webhook_url=None,
        enabled=False,
    )


@pytest.fixture
def alerter_short_cooldown():
    """Create alerter with very short cooldown for testing."""
    return DiscordAlerter(
        webhook_url="https://discord.com/api/webhooks/test/token",
        enabled=True,
        escalation_cooldown_seconds=0.1,  # 100ms
        testing_mode=False,  # Explicitly disable to test real webhook flow with mocks
    )


# =============================================================================
# Test Cases: AlertSeverity Enum
# =============================================================================


class TestAlertSeverityEscalation:
    """Tests for ESCALATION severity level."""
    
    def test_escalation_severity_exists(self):
        """Test ESCALATION severity is defined."""
        assert hasattr(AlertSeverity, 'ESCALATION')
    
    def test_escalation_color(self):
        """Test ESCALATION has correct color (dark red)."""
        assert AlertSeverity.ESCALATION.color == 0xE74C3C
    
    def test_escalation_emoji(self):
        """Test ESCALATION has trending up emoji."""
        assert AlertSeverity.ESCALATION.emoji == "📈"


# =============================================================================
# Test Cases: Async Escalation Alerts
# =============================================================================


class TestSendEscalationAlertAsync:
    """Tests for async send_escalation_alert method."""
    
    @pytest.mark.asyncio
    async def test_disabled_alerter_returns_false(self, alerter_disabled):
        """Test disabled alerter returns False."""
        result = await alerter_disabled.send_escalation_alert(
            escalation_rate="rapid",
            pattern_name="evening_deterioration",
            pattern_confidence=0.85,
            crisis_score=0.9,
            score_delta=0.6,
            time_span_hours=3.0,
            intervention_urgency="immediate",
            message_preview="I can't do this anymore",
        )
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_send_escalation_alert_immediate(self, alerter_with_webhook):
        """Test escalation alert with immediate urgency."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            result = await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name="evening_deterioration",
                pattern_confidence=0.85,
                crisis_score=0.9,
                score_delta=0.6,
                time_span_hours=3.0,
                intervention_urgency="immediate",
                message_preview="I can't do this anymore",
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Check the alert passed to send_alert
            alert = mock_send.call_args[0][0]
            assert alert.severity == AlertSeverity.CRITICAL
            assert "IMMEDIATE" in alert.description.upper()
    
    @pytest.mark.asyncio
    async def test_send_escalation_alert_high(self, alerter_with_webhook):
        """Test escalation alert with high urgency."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            result = await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.75,
                score_delta=0.45,
                time_span_hours=4.0,
                intervention_urgency="high",
                message_preview="Things are getting bad",
            )
            
            assert result is True
            
            alert = mock_send.call_args[0][0]
            assert alert.severity == AlertSeverity.ESCALATION
    
    @pytest.mark.asyncio
    async def test_send_escalation_alert_standard(self, alerter_with_webhook):
        """Test escalation alert with standard urgency."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            result = await alerter_with_webhook.send_escalation_alert(
                escalation_rate="gradual",
                pattern_name="gradual_decline",
                pattern_confidence=0.7,
                crisis_score=0.55,
                score_delta=0.35,
                time_span_hours=12.0,
                intervention_urgency="standard",
                message_preview="Not feeling great",
            )
            
            assert result is True
            
            alert = mock_send.call_args[0][0]
            assert alert.severity == AlertSeverity.WARNING
    
    @pytest.mark.asyncio
    async def test_send_escalation_alert_low(self, alerter_with_webhook):
        """Test escalation alert with low urgency."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            result = await alerter_with_webhook.send_escalation_alert(
                escalation_rate="gradual",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.4,
                score_delta=0.2,
                time_span_hours=24.0,
                intervention_urgency="low",
                message_preview="A bit down today",
            )
            
            assert result is True
            
            alert = mock_send.call_args[0][0]
            assert alert.severity == AlertSeverity.INFO
    
    @pytest.mark.asyncio
    async def test_escalation_alert_fields(self, alerter_with_webhook):
        """Test escalation alert contains correct fields."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name="evening_deterioration",
                pattern_confidence=0.87,
                crisis_score=0.85,
                score_delta=0.55,
                time_span_hours=4.5,
                intervention_urgency="high",
                message_preview="Test message preview",
                user_id="user_123",
                channel_id="channel_456",
            )
            
            alert = mock_send.call_args[0][0]
            
            assert "Escalation Rate" in alert.fields
            assert "Crisis Score" in alert.fields
            assert "Score Change" in alert.fields
            assert "Time Span" in alert.fields
            assert "Urgency" in alert.fields
            assert "Pattern" in alert.fields
            assert "Confidence" in alert.fields
            assert "User ID" in alert.fields
            assert "Channel" in alert.fields
    
    @pytest.mark.asyncio
    async def test_message_preview_truncation(self, alerter_with_webhook):
        """Test long message preview is truncated."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            long_message = "A" * 150  # 150 chars
            
            await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.8,
                score_delta=0.5,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview=long_message,
            )
            
            alert = mock_send.call_args[0][0]
            
            # Message field should be present and contain truncated content
            assert "Message" in alert.fields
            assert len(alert.fields["Message"]) < 150


# =============================================================================
# Test Cases: Sync Escalation Alerts
# =============================================================================


class TestSendEscalationAlertSync:
    """Tests for sync send_escalation_alert_sync method."""
    
    def test_disabled_alerter_returns_false(self, alerter_disabled):
        """Test disabled alerter returns False."""
        result = alerter_disabled.send_escalation_alert_sync(
            escalation_rate="rapid",
            pattern_name=None,
            pattern_confidence=0.0,
            crisis_score=0.8,
            score_delta=0.5,
            time_span_hours=3.0,
            intervention_urgency="high",
            message_preview="Test",
        )
        
        assert result is False
    
    def test_sync_immediate_urgency(self, alerter_with_webhook):
        """Test sync method with immediate urgency."""
        with patch.object(alerter_with_webhook, 'send_alert_sync') as mock_send:
            mock_send.return_value = True
            
            result = alerter_with_webhook.send_escalation_alert_sync(
                escalation_rate="sudden",
                pattern_name="sudden_crisis",
                pattern_confidence=0.9,
                crisis_score=0.95,
                score_delta=0.7,
                time_span_hours=1.0,
                intervention_urgency="immediate",
                message_preview="Emergency",
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            alert = mock_send.call_args[0][0]
            assert alert.severity == AlertSeverity.CRITICAL
    
    def test_sync_high_urgency(self, alerter_with_webhook):
        """Test sync method with high urgency."""
        with patch.object(alerter_with_webhook, 'send_alert_sync') as mock_send:
            mock_send.return_value = True
            
            result = alerter_with_webhook.send_escalation_alert_sync(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.75,
                score_delta=0.45,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview="Concerning",
            )
            
            assert result is True
            
            alert = mock_send.call_args[0][0]
            assert alert.severity == AlertSeverity.ESCALATION


# =============================================================================
# Test Cases: Cooldown Tracking
# =============================================================================


class TestEscalationCooldown:
    """Tests for escalation-specific cooldown."""
    
    @pytest.mark.asyncio
    async def test_cooldown_blocks_second_alert(self, alerter_with_webhook):
        """Test second alert is blocked during cooldown."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            # First alert should succeed
            result1 = await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.8,
                score_delta=0.5,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview="First",
            )
            
            assert result1 is True
            
            # Second alert should be throttled (within 60s cooldown)
            result2 = await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.85,
                score_delta=0.55,
                time_span_hours=3.5,
                intervention_urgency="high",
                message_preview="Second",
            )
            
            assert result2 is False
            
            # send_alert should only be called once
            assert mock_send.call_count == 1
    
    @pytest.mark.asyncio
    async def test_cooldown_expires(self, alerter_short_cooldown):
        """Test alerts allowed after cooldown expires."""
        with patch.object(alerter_short_cooldown, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            # First alert
            result1 = await alerter_short_cooldown.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.8,
                score_delta=0.5,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview="First",
            )
            
            assert result1 is True
            
            # Wait for cooldown (100ms + buffer)
            time.sleep(0.15)
            
            # Second alert should succeed after cooldown
            result2 = await alerter_short_cooldown.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.85,
                score_delta=0.55,
                time_span_hours=3.5,
                intervention_urgency="high",
                message_preview="Second",
            )
            
            assert result2 is True
            assert mock_send.call_count == 2
    
    def test_sync_cooldown(self, alerter_with_webhook):
        """Test cooldown works for sync method too."""
        with patch.object(alerter_with_webhook, 'send_alert_sync') as mock_send:
            mock_send.return_value = True
            
            # First alert
            result1 = alerter_with_webhook.send_escalation_alert_sync(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.8,
                score_delta=0.5,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview="First",
            )
            
            assert result1 is True
            
            # Second should be throttled
            result2 = alerter_with_webhook.send_escalation_alert_sync(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.85,
                score_delta=0.55,
                time_span_hours=3.5,
                intervention_urgency="high",
                message_preview="Second",
            )
            
            assert result2 is False


# =============================================================================
# Test Cases: Factory Function
# =============================================================================


class TestFactoryFunction:
    """Tests for create_discord_alerter factory."""
    
    def test_factory_default_escalation_cooldown(self):
        """Test factory creates alerter with default escalation cooldown."""
        alerter = create_discord_alerter(
            webhook_url="https://discord.com/api/webhooks/test/token",
        )
        
        assert alerter._escalation_cooldown_seconds == 300.0
    
    def test_factory_custom_escalation_cooldown(self):
        """Test factory accepts custom escalation cooldown."""
        alerter = create_discord_alerter(
            webhook_url="https://discord.com/api/webhooks/test/token",
            escalation_cooldown_seconds=120.0,
        )
        
        assert alerter._escalation_cooldown_seconds == 120.0


# =============================================================================
# Test Cases: Status Reporting
# =============================================================================


class TestStatusReporting:
    """Tests for status reporting with escalation info."""
    
    def test_status_includes_escalation_cooldown(self, alerter_with_webhook):
        """Test status includes escalation cooldown remaining."""
        status = alerter_with_webhook.get_status()
        
        assert "escalation_cooldown_remaining" in status
        assert status["escalation_cooldown_remaining"] >= 0
    
    def test_status_includes_escalation_config(self, alerter_with_webhook):
        """Test status includes escalation cooldown in config."""
        status = alerter_with_webhook.get_status()
        
        assert "escalation_cooldown_seconds" in status["throttle_config"]
        assert status["throttle_config"]["escalation_cooldown_seconds"] == 60.0
    
    @pytest.mark.asyncio
    async def test_cooldown_remaining_after_alert(self, alerter_with_webhook):
        """Test cooldown remaining is updated after alert."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            # Send alert
            await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.8,
                score_delta=0.5,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview="Test",
            )
            
            status = alerter_with_webhook.get_status()
            
            # Should have cooldown remaining (close to 60s)
            assert status["escalation_cooldown_remaining"] > 50


# =============================================================================
# Test Cases: Score Delta Formatting
# =============================================================================


class TestScoreDeltaFormatting:
    """Tests for score delta field formatting."""
    
    @pytest.mark.asyncio
    async def test_positive_delta_formatting(self, alerter_with_webhook):
        """Test positive score delta shows + prefix."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            await alerter_with_webhook.send_escalation_alert(
                escalation_rate="rapid",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.8,
                score_delta=0.5,
                time_span_hours=3.0,
                intervention_urgency="high",
                message_preview="Test",
            )
            
            alert = mock_send.call_args[0][0]
            
            assert alert.fields["Score Change"].startswith("+")
    
    @pytest.mark.asyncio
    async def test_negative_delta_formatting(self, alerter_with_webhook):
        """Test negative score delta shows - prefix."""
        with patch.object(alerter_with_webhook, 'send_alert', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            
            await alerter_with_webhook.send_escalation_alert(
                escalation_rate="gradual",
                pattern_name=None,
                pattern_confidence=0.0,
                crisis_score=0.4,
                score_delta=-0.3,  # Negative = improving
                time_span_hours=6.0,
                intervention_urgency="low",
                message_preview="Test",
            )
            
            alert = mock_send.call_args[0][0]
            
            assert alert.fields["Score Change"].startswith("-")


# =============================================================================
# Export
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
