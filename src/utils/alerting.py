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
Discord Alerting Service for Ash-NLP
---
FILE VERSION: v5.0-4-5.6-3
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 - Ensemble Coordinator Enhancement
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Send alerts to Discord webhook for critical failures
- Throttle alerts to prevent spam
- Format alerts with severity and context
- Support async and sync operations
- Phase 4: Send conflict alerts for ensemble disagreements

WEBHOOK SETUP:
1. Create webhook in Discord server (Server Settings > Integrations > Webhooks)
2. Copy webhook URL
3. Add to secrets:
   - Docker: echo "https://discord.com/api/webhooks/..." > secrets/discord_alert_webhook
   - Env: NLP_SECRET_DISCORD_ALERT_WEBHOOK=https://...

ALERT TYPES:
- CRITICAL: Primary model (BART) failure - immediate attention required
- ERROR: Secondary model failure - degraded operation
- WARNING: Performance degradation - monitoring needed
- INFO: System events - startup, recovery, etc.
- CONFLICT: Phase 4 - Model ensemble disagreement alerts
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Module version
__version__ = "v5.0-4-5.6-3"

# Initialize logger
logger = logging.getLogger(__name__)

# User-Agent for Discord webhook requests
USER_AGENT = "Ash-NLP/5.0 (Discord Webhook; +https://github.com/the-alphabet-cartel/ash-nlp)"


# =============================================================================
# Alert Severity Levels
# =============================================================================


class AlertSeverity(Enum):
    """Alert severity levels with Discord embed colors."""

    CRITICAL = ("critical", 0xFF0000)  # Red
    ERROR = ("error", 0xFF6B6B)  # Light Red
    WARNING = ("warning", 0xFFAA00)  # Orange
    INFO = ("info", 0x00AA00)  # Green
    RECOVERY = ("recovery", 0x00FF00)  # Bright Green
    CONFLICT = ("conflict", 0x9B59B6)  # Purple - Phase 4

    def __init__(self, name: str, color: int):
        self._name = name
        self.color = color

    @property
    def emoji(self) -> str:
        """Get emoji for severity level."""
        emojis = {
            "critical": "🚨",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "recovery": "✅",
            "conflict": "⚔️",  # Phase 4
        }
        return emojis.get(self._name, "📢")


# =============================================================================
# Alert Data Structure
# =============================================================================


@dataclass
class Alert:
    """
    Alert data structure.

    Attributes:
        severity: Alert severity level
        title: Short title for the alert
        description: Detailed description
        fields: Additional fields (key-value pairs)
        timestamp: When the alert was created
        source: Source component (e.g., "ensemble", "bart_model")
    """

    severity: AlertSeverity
    title: str
    description: str
    fields: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = "ash-nlp"

    def to_discord_embed(self) -> Dict[str, Any]:
        """
        Convert to Discord embed format.

        Returns:
            Discord embed dictionary
        """
        embed = {
            "title": f"{self.severity.emoji} {self.title}",
            "description": self.description,
            "color": self.severity.color,
            "timestamp": self.timestamp.isoformat() + "Z",
            "footer": {
                "text": f"Ash-NLP | {self.source}",
            },
        }

        if self.fields:
            embed["fields"] = [
                {"name": k, "value": str(v)[:1024], "inline": True}  # Discord limit
                for k, v in self.fields.items()
            ]

        return embed


# =============================================================================
# Throttle Configuration
# =============================================================================


@dataclass
class ThrottleConfig:
    """
    Configuration for alert throttling.

    Prevents flooding Discord with repeated alerts.

    Attributes:
        window_seconds: Time window for throttling
        max_alerts: Maximum alerts per window
        cooldown_seconds: Cooldown after hitting limit
    """

    window_seconds: float = 300.0  # 5 minutes
    max_alerts: int = 5
    cooldown_seconds: float = 600.0  # 10 minute cooldown


# =============================================================================
# Discord Alerter
# =============================================================================


class DiscordAlerter:
    """
    Discord webhook alerter for system notifications.

    Sends formatted alerts to a Discord webhook with:
    - Severity-based colors
    - Throttling to prevent spam
    - Async and sync support

    Attributes:
        webhook_url: Discord webhook URL
        enabled: Whether alerting is enabled
        throttle: Throttle configuration
        service_name: Name of the service (for footer)

    Example:
        alerter = DiscordAlerter(webhook_url="https://discord.com/api/webhooks/...")

        # Send a critical alert
        await alerter.send_critical(
            title="BART Model Failure",
            description="Primary crisis detection model is unavailable",
            fields={"Error": "CUDA OOM", "Action": "Restarting..."}
        )
    """

    def __init__(
        self,
        webhook_url: Optional[str] = None,
        enabled: bool = True,
        throttle: Optional[ThrottleConfig] = None,
        service_name: str = "Ash-NLP",
        conflict_cooldown_seconds: float = 60.0,  # Phase 4
    ):
        """
        Initialize the Discord alerter.

        Args:
            webhook_url: Discord webhook URL (or None to disable)
            enabled: Whether alerting is enabled
            throttle: Throttle configuration
            service_name: Name for the footer
            conflict_cooldown_seconds: Cooldown between conflict alerts (Phase 4)
        """
        self.webhook_url = webhook_url
        self.enabled = enabled and webhook_url is not None
        self.throttle = throttle or ThrottleConfig()
        self.service_name = service_name

        # Throttling state
        self._alert_history: List[float] = []
        self._in_cooldown = False
        self._cooldown_until = 0.0

        # Phase 4: Conflict alert cooldown
        self._conflict_cooldown_seconds = conflict_cooldown_seconds
        self._last_conflict_alert = 0.0

        # HTTP session (lazy init)
        self._session = None

        if self.enabled:
            logger.info(f"🔔 Discord alerter initialized for {service_name}")
        else:
            logger.info("🔕 Discord alerter disabled (no webhook URL)")

    async def _get_session(self):
        """Get or create aiohttp session."""
        if self._session is None:
            import aiohttp

            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        """Close the HTTP session."""
        if self._session:
            await self._session.close()
            self._session = None

    # =========================================================================
    # Throttling
    # =========================================================================

    def _should_throttle(self) -> bool:
        """Check if alert should be throttled."""
        now = time.time()

        # Check cooldown
        if self._in_cooldown:
            if now < self._cooldown_until:
                return True
            else:
                self._in_cooldown = False
                self._alert_history.clear()
                logger.info("🔔 Alert cooldown ended")

        # Clean old entries
        window_start = now - self.throttle.window_seconds
        self._alert_history = [t for t in self._alert_history if t > window_start]

        # Check if over limit
        if len(self._alert_history) >= self.throttle.max_alerts:
            self._in_cooldown = True
            self._cooldown_until = now + self.throttle.cooldown_seconds
            logger.warning(
                f"🔕 Alert throttle activated, cooldown for "
                f"{self.throttle.cooldown_seconds}s"
            )
            return True

        return False

    def _record_alert(self):
        """Record an alert for throttling."""
        self._alert_history.append(time.time())

    def _should_throttle_conflict(self) -> bool:
        """Check if conflict alert should be throttled (Phase 4)."""
        now = time.time()
        return now - self._last_conflict_alert < self._conflict_cooldown_seconds

    def _record_conflict_alert(self):
        """Record a conflict alert timestamp (Phase 4)."""
        self._last_conflict_alert = time.time()

    # =========================================================================
    # Send Methods
    # =========================================================================

    async def send_alert(self, alert: Alert) -> bool:
        """
        Send an alert to Discord.

        Args:
            alert: Alert to send

        Returns:
            True if sent successfully
        """
        if not self.enabled:
            logger.debug(f"Alert skipped (disabled): {alert.title}")
            return False

        if self._should_throttle():
            logger.warning(f"Alert throttled: {alert.title}")
            return False

        try:
            session = await self._get_session()

            payload = {
                "embeds": [alert.to_discord_embed()],
            }

            async with session.post(
                self.webhook_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": USER_AGENT,
                },
            ) as response:
                if response.status == 204:
                    self._record_alert()
                    logger.info(f"🔔 Alert sent: {alert.title}")
                    return True
                else:
                    body = await response.text()
                    logger.error(f"Discord webhook failed: {response.status} - {body}")
                    return False

        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False

    def send_alert_sync(self, alert: Alert) -> bool:
        """
        Send an alert synchronously.

        Args:
            alert: Alert to send

        Returns:
            True if sent successfully
        """
        if not self.enabled:
            return False

        if self._should_throttle():
            logger.warning(f"Alert throttled: {alert.title}")
            return False

        try:
            import urllib.request

            payload = json.dumps({"embeds": [alert.to_discord_embed()]}).encode()

            req = urllib.request.Request(
                self.webhook_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": USER_AGENT,
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 204:
                    self._record_alert()
                    logger.info(f"🔔 Alert sent (sync): {alert.title}")
                    return True

        except Exception as e:
            logger.error(f"Failed to send alert (sync): {e}")

        return False

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    async def send_critical(
        self,
        title: str,
        description: str,
        fields: Optional[Dict[str, str]] = None,
        source: str = "system",
    ) -> bool:
        """Send a critical alert."""
        alert = Alert(
            severity=AlertSeverity.CRITICAL,
            title=title,
            description=description,
            fields=fields or {},
            source=source,
        )
        return await self.send_alert(alert)

    async def send_error(
        self,
        title: str,
        description: str,
        fields: Optional[Dict[str, str]] = None,
        source: str = "system",
    ) -> bool:
        """Send an error alert."""
        alert = Alert(
            severity=AlertSeverity.ERROR,
            title=title,
            description=description,
            fields=fields or {},
            source=source,
        )
        return await self.send_alert(alert)

    async def send_warning(
        self,
        title: str,
        description: str,
        fields: Optional[Dict[str, str]] = None,
        source: str = "system",
    ) -> bool:
        """Send a warning alert."""
        alert = Alert(
            severity=AlertSeverity.WARNING,
            title=title,
            description=description,
            fields=fields or {},
            source=source,
        )
        return await self.send_alert(alert)

    async def send_info(
        self,
        title: str,
        description: str,
        fields: Optional[Dict[str, str]] = None,
        source: str = "system",
    ) -> bool:
        """Send an info alert."""
        alert = Alert(
            severity=AlertSeverity.INFO,
            title=title,
            description=description,
            fields=fields or {},
            source=source,
        )
        return await self.send_alert(alert)

    async def send_recovery(
        self,
        title: str,
        description: str,
        fields: Optional[Dict[str, str]] = None,
        source: str = "system",
    ) -> bool:
        """Send a recovery alert."""
        alert = Alert(
            severity=AlertSeverity.RECOVERY,
            title=title,
            description=description,
            fields=fields or {},
            source=source,
        )
        return await self.send_alert(alert)

    # =========================================================================
    # Phase 4: Conflict Alert Method
    # =========================================================================

    async def send_conflict_alert(
        self,
        conflict_type: str,
        severity: str,
        details: Dict[str, Any],
        resolution: Optional[Dict[str, Any]] = None,
        source: str = "ensemble",
    ) -> bool:
        """
        Send an alert for ensemble model conflicts (Phase 4).

        Args:
            conflict_type: Type of conflict (e.g., "score_disagreement", "irony_sentiment")
            severity: Conflict severity level (e.g., "high", "medium", "low")
            details: Conflict details dictionary
            resolution: Resolution information (if resolved)
            source: Source component

        Returns:
            True if alert sent successfully
        """
        if not self.enabled:
            logger.debug(f"Conflict alert skipped (disabled): {conflict_type}")
            return False

        # Check conflict-specific cooldown
        if self._should_throttle_conflict():
            logger.debug(f"Conflict alert on cooldown: {conflict_type}")
            return False

        # Build fields from details
        fields = {
            "Conflict Type": conflict_type.replace("_", " ").title(),
            "Severity": severity.upper(),
        }

        # Add key details
        if "max_score" in details:
            fields["Max Score"] = f"{details['max_score']:.3f}"
        if "min_score" in details:
            fields["Min Score"] = f"{details['min_score']:.3f}"
        if "range" in details:
            fields["Score Range"] = f"{details['range']:.3f}"
        if "variance" in details:
            fields["Variance"] = f"{details['variance']:.4f}"

        # Add resolution info if available
        if resolution:
            fields["Resolution"] = resolution.get("strategy", "unknown").title()
            if "final_score" in resolution:
                fields["Final Score"] = f"{resolution['final_score']:.3f}"
            if "flagged_for_review" in resolution and resolution["flagged_for_review"]:
                fields["Review Required"] = "Yes"

        # Determine alert severity based on conflict severity
        if severity.lower() == "high":
            alert_severity = AlertSeverity.WARNING
            description = (
                "**Significant model disagreement detected.**\n"
                "The ensemble models have conflicting opinions on this analysis. "
                "Review may be required for accurate crisis assessment."
            )
        elif severity.lower() == "medium":
            alert_severity = AlertSeverity.CONFLICT
            description = (
                "**Model conflict detected.**\n"
                "Some models disagree on the analysis. "
                "The system has applied conflict resolution."
            )
        else:
            alert_severity = AlertSeverity.INFO
            description = (
                "**Minor model disagreement.**\n"
                "A small conflict was detected and resolved automatically."
            )

        alert = Alert(
            severity=alert_severity,
            title=f"Ensemble Conflict: {conflict_type.replace('_', ' ').title()}",
            description=description,
            fields=fields,
            source=source,
        )

        result = await self.send_alert(alert)
        if result:
            self._record_conflict_alert()
        return result

    def send_conflict_alert_sync(
        self,
        conflict_type: str,
        severity: str,
        details: Dict[str, Any],
        resolution: Optional[Dict[str, Any]] = None,
        source: str = "ensemble",
    ) -> bool:
        """
        Send a conflict alert synchronously (Phase 4).

        Args:
            conflict_type: Type of conflict
            severity: Conflict severity level
            details: Conflict details dictionary
            resolution: Resolution information
            source: Source component

        Returns:
            True if alert sent successfully
        """
        if not self.enabled:
            return False

        if self._should_throttle_conflict():
            logger.debug(f"Conflict alert on cooldown: {conflict_type}")
            return False

        # Build fields
        fields = {
            "Conflict Type": conflict_type.replace("_", " ").title(),
            "Severity": severity.upper(),
        }

        if "max_score" in details:
            fields["Max Score"] = f"{details['max_score']:.3f}"
        if "min_score" in details:
            fields["Min Score"] = f"{details['min_score']:.3f}"

        if resolution:
            fields["Resolution"] = resolution.get("strategy", "unknown").title()

        if severity.lower() == "high":
            alert_severity = AlertSeverity.WARNING
        elif severity.lower() == "medium":
            alert_severity = AlertSeverity.CONFLICT
        else:
            alert_severity = AlertSeverity.INFO

        alert = Alert(
            severity=alert_severity,
            title=f"Ensemble Conflict: {conflict_type.replace('_', ' ').title()}",
            description="Model conflict detected in ensemble analysis.",
            fields=fields,
            source=source,
        )

        result = self.send_alert_sync(alert)
        if result:
            self._record_conflict_alert()
        return result

    # =========================================================================
    # Model-Specific Alerts
    # =========================================================================

    async def alert_model_failure(
        self,
        model_name: str,
        error: str,
        is_critical: bool = False,
    ) -> bool:
        """
        Send alert for model failure.

        Args:
            model_name: Name of the failed model
            error: Error message
            is_critical: Whether this is the primary model

        Returns:
            True if alert sent
        """
        if is_critical:
            return await self.send_critical(
                title=f"Critical: {model_name} Model Failure",
                description=(
                    "**The primary crisis detection model has failed.**\n"
                    "Crisis detection may be impaired until resolved."
                ),
                fields={
                    "Model": model_name,
                    "Error": error[:200],  # Truncate long errors
                    "Impact": "Crisis detection unavailable",
                },
                source=model_name,
            )
        else:
            return await self.send_error(
                title=f"Model Failure: {model_name}",
                description=(
                    "A supporting model has failed. "
                    "System is operating in degraded mode."
                ),
                fields={
                    "Model": model_name,
                    "Error": error[:200],
                    "Impact": "Reduced accuracy",
                },
                source=model_name,
            )

    async def alert_model_recovery(self, model_name: str) -> bool:
        """
        Send alert for model recovery.

        Args:
            model_name: Name of the recovered model

        Returns:
            True if alert sent
        """
        return await self.send_recovery(
            title=f"Model Recovered: {model_name}",
            description=f"The {model_name} model has recovered and is operational.",
            fields={"Model": model_name, "Status": "Operational"},
            source=model_name,
        )

    async def alert_system_startup(
        self,
        models_loaded: int,
        total_models: int,
    ) -> bool:
        """
        Send alert for system startup.

        Args:
            models_loaded: Number of models loaded
            total_models: Total number of models

        Returns:
            True if alert sent
        """
        if models_loaded == total_models:
            return await self.send_info(
                title="Ash-NLP Started",
                description="All models loaded successfully. System is ready.",
                fields={
                    "Models": f"{models_loaded}/{total_models}",
                    "Status": "Ready",
                },
                source="startup",
            )
        else:
            return await self.send_warning(
                title="Ash-NLP Started (Degraded)",
                description="System started but some models failed to load.",
                fields={
                    "Models": f"{models_loaded}/{total_models}",
                    "Status": "Degraded",
                },
                source="startup",
            )

    async def alert_high_latency(
        self,
        model_name: str,
        latency_ms: float,
        threshold_ms: float,
    ) -> bool:
        """
        Send alert for high latency.

        Args:
            model_name: Name of the slow model
            latency_ms: Observed latency in milliseconds
            threshold_ms: Threshold that was exceeded

        Returns:
            True if alert sent
        """
        return await self.send_warning(
            title=f"High Latency: {model_name}",
            description="Model inference is taking longer than expected.",
            fields={
                "Model": model_name,
                "Latency": f"{latency_ms:.0f}ms",
                "Threshold": f"{threshold_ms:.0f}ms",
            },
            source=model_name,
        )

    # =========================================================================
    # Status
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get alerter status."""
        return {
            "enabled": self.enabled,
            "webhook_configured": self.webhook_url is not None,
            "in_cooldown": self._in_cooldown,
            "alerts_in_window": len(self._alert_history),
            "conflict_cooldown_remaining": max(
                0,
                self._conflict_cooldown_seconds
                - (time.time() - self._last_conflict_alert),
            ),
            "throttle_config": {
                "window_seconds": self.throttle.window_seconds,
                "max_alerts": self.throttle.max_alerts,
                "cooldown_seconds": self.throttle.cooldown_seconds,
                "conflict_cooldown_seconds": self._conflict_cooldown_seconds,
            },
        }


# =============================================================================
# Factory Function
# =============================================================================


def create_discord_alerter(
    webhook_url: Optional[str] = None,
    secrets_manager=None,
    enabled: bool = True,
    conflict_cooldown_seconds: float = 60.0,
) -> DiscordAlerter:
    """
    Factory function to create a Discord alerter.

    Args:
        webhook_url: Explicit webhook URL (optional)
        secrets_manager: SecretsManager instance for loading URL
        enabled: Whether alerting is enabled
        conflict_cooldown_seconds: Cooldown between conflict alerts (Phase 4)

    Returns:
        Configured DiscordAlerter instance
    """
    # Get webhook URL from secrets if not provided
    if webhook_url is None and secrets_manager is not None:
        webhook_url = secrets_manager.get("discord_alert_webhook")

    # Also check environment variable
    if webhook_url is None:
        import os

        webhook_url = os.environ.get("NLP_DISCORD_ALERT_WEBHOOK")

    return DiscordAlerter(
        webhook_url=webhook_url,
        enabled=enabled,
        conflict_cooldown_seconds=conflict_cooldown_seconds,
    )


# =============================================================================
# Global Instance
# =============================================================================

_global_alerter: Optional[DiscordAlerter] = None


def get_alerter() -> Optional[DiscordAlerter]:
    """Get the global alerter instance."""
    return _global_alerter


def set_alerter(alerter: DiscordAlerter) -> None:
    """Set the global alerter instance."""
    global _global_alerter
    _global_alerter = alerter


async def send_alert(alert: Alert) -> bool:
    """Send alert using global alerter."""
    if _global_alerter:
        return await _global_alerter.send_alert(alert)
    return False


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Classes
    "DiscordAlerter",
    "Alert",
    "AlertSeverity",
    "ThrottleConfig",
    # Factory
    "create_discord_alerter",
    # Global
    "get_alerter",
    "set_alerter",
    "send_alert",
]
