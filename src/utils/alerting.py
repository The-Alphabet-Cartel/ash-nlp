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
FILE VERSION: v5.0-6-4.0-3
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 4 (FE-002, FE-008: Enhanced Conflict Alerts)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Send alerts to Discord webhook for critical failures
- Throttle alerts to prevent spam
- Format alerts with severity and context
- Support async and sync operations
- Phase 4: Send conflict alerts for ensemble disagreements
- Phase 5: Send escalation alerts for crisis pattern detection

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
- ESCALATION: Phase 5 - Crisis pattern escalation alerts
"""

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

# Module version
__version__ = "v5.0-6-4.0-3"

# Initialize logger
logger = logging.getLogger(__name__)

# User-Agent for Discord webhook requests
USER_AGENT = "Ash-NLP/5.0 (Discord Webhook; +https://github.com/the-alphabet-cartel/ash-nlp)"


# =============================================================================
# FE-002: Discord Message Length Limits
# =============================================================================

# Discord API limits (https://discord.com/developers/docs/resources/message)
DISCORD_LIMITS = {
    "message_content": 2000,      # Message content (non-embed)
    "embed_title": 256,            # Embed title
    "embed_description": 4096,     # Embed description
    "embed_field_name": 256,       # Field name
    "embed_field_value": 1024,     # Field value
    "embed_footer_text": 2048,     # Footer text
    "embed_author_name": 256,      # Author name
    "embed_total": 6000,           # Total characters in embed
    "embeds_per_message": 10,      # Max embeds per message
}


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to max length with suffix (FE-002).
    
    Args:
        text: Text to truncate
        max_length: Maximum allowed length
        suffix: Suffix to append when truncated (default: "...")
        
    Returns:
        Truncated text with suffix if needed
    """
    if not text or len(text) <= max_length:
        return text
    
    # Leave room for suffix
    truncate_at = max_length - len(suffix)
    if truncate_at <= 0:
        return suffix[:max_length]
    
    return text[:truncate_at] + suffix


def truncate_at_boundary(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text at word/sentence boundary (FE-002).
    
    Prefers to break at sentence end, then word boundary.
    
    Args:
        text: Text to truncate
        max_length: Maximum allowed length
        suffix: Suffix to append when truncated
        
    Returns:
        Truncated text at natural boundary
    """
    if not text or len(text) <= max_length:
        return text
    
    truncate_at = max_length - len(suffix)
    if truncate_at <= 0:
        return suffix[:max_length]
    
    # Get the truncated portion
    truncated = text[:truncate_at]
    
    # Try to find last sentence boundary
    for delimiter in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
        last_pos = truncated.rfind(delimiter)
        if last_pos > truncate_at // 2:  # Only if in latter half
            return truncated[:last_pos + 1] + suffix
    
    # Try to find last word boundary
    last_space = truncated.rfind(' ')
    if last_space > truncate_at // 2:
        return truncated[:last_space] + suffix
    
    # Fall back to hard truncation
    return truncated + suffix


def calculate_embed_size(embed: Dict[str, Any]) -> int:
    """
    Calculate total character count of a Discord embed (FE-002).
    
    Args:
        embed: Discord embed dictionary
        
    Returns:
        Total character count
    """
    total = 0
    
    total += len(embed.get("title", ""))
    total += len(embed.get("description", ""))
    
    if "footer" in embed:
        total += len(embed["footer"].get("text", ""))
    
    if "author" in embed:
        total += len(embed["author"].get("name", ""))
    
    for field in embed.get("fields", []):
        total += len(field.get("name", ""))
        total += len(field.get("value", ""))
    
    return total


def validate_embed_size(embed: Dict[str, Any]) -> tuple:
    """
    Validate embed against Discord limits (FE-002).
    
    Args:
        embed: Discord embed dictionary
        
    Returns:
        Tuple of (is_valid, total_size, issues)
    """
    issues = []
    
    # Check individual field limits
    if len(embed.get("title", "")) > DISCORD_LIMITS["embed_title"]:
        issues.append(f"Title exceeds {DISCORD_LIMITS['embed_title']} chars")
    
    if len(embed.get("description", "")) > DISCORD_LIMITS["embed_description"]:
        issues.append(f"Description exceeds {DISCORD_LIMITS['embed_description']} chars")
    
    if "footer" in embed:
        if len(embed["footer"].get("text", "")) > DISCORD_LIMITS["embed_footer_text"]:
            issues.append(f"Footer exceeds {DISCORD_LIMITS['embed_footer_text']} chars")
    
    for i, field in enumerate(embed.get("fields", [])):
        if len(field.get("name", "")) > DISCORD_LIMITS["embed_field_name"]:
            issues.append(f"Field {i} name exceeds {DISCORD_LIMITS['embed_field_name']} chars")
        if len(field.get("value", "")) > DISCORD_LIMITS["embed_field_value"]:
            issues.append(f"Field {i} value exceeds {DISCORD_LIMITS['embed_field_value']} chars")
    
    # Check total size
    total_size = calculate_embed_size(embed)
    if total_size > DISCORD_LIMITS["embed_total"]:
        issues.append(f"Total embed size {total_size} exceeds {DISCORD_LIMITS['embed_total']} chars")
    
    return len(issues) == 0, total_size, issues


# =============================================================================
# FE-008: ASCII Disagreement Chart for Conflict Alerts
# =============================================================================

# Default conflict alert threshold (variance above this triggers alert)
DEFAULT_CONFLICT_ALERT_THRESHOLD = 0.15


def generate_disagreement_chart(
    model_scores: Dict[str, float],
    bar_width: int = 20,
    show_labels: bool = True,
) -> str:
    """
    Generate ASCII bar chart showing model score disagreement (FE-008).
    
    Creates a visual representation of how models disagree on crisis scores.
    
    Args:
        model_scores: Dict mapping model name to crisis score (0.0-1.0)
        bar_width: Width of the bar chart in characters
        show_labels: Whether to show score labels on bars
        
    Returns:
        ASCII chart string for Discord embed
        
    Example output:
        ```
        Model Scores:
        bart      ████████████████████ 0.85
        sentiment ████████████░░░░░░░░ 0.60
        irony     ██████░░░░░░░░░░░░░░ 0.25
        emotions  ████████████████░░░░ 0.78
        Range: 0.60 | Variance: 0.048
        ```
    """
    if not model_scores:
        return "No model scores available"
    
    lines = ["```"]
    lines.append("Model Scores:")
    
    # Find the longest model name for alignment
    max_name_len = max(len(name) for name in model_scores.keys())
    
    for model, score in model_scores.items():
        # Clamp score to 0-1 range
        score = max(0.0, min(1.0, score))
        
        # Calculate filled/empty portions
        filled = int(score * bar_width)
        empty = bar_width - filled
        
        # Build the bar
        bar = "█" * filled + "░" * empty
        
        # Format the line
        model_padded = model.ljust(max_name_len)
        if show_labels:
            line = f"{model_padded} {bar} {score:.2f}"
        else:
            line = f"{model_padded} {bar}"
        
        lines.append(line)
    
    # Calculate statistics
    scores = list(model_scores.values())
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score
    mean_score = sum(scores) / len(scores)
    variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
    
    # Add summary line
    lines.append(f"Range: {score_range:.2f} | Var: {variance:.3f}")
    lines.append("```")
    
    return "\n".join(lines)


def format_conflict_summary(
    conflict_type: str,
    model_scores: Dict[str, float],
    resolution_strategy: Optional[str] = None,
    final_score: Optional[float] = None,
) -> str:
    """
    Format a conflict summary with ASCII chart for Discord (FE-008).
    
    Args:
        conflict_type: Type of conflict detected
        model_scores: Dict mapping model name to crisis score
        resolution_strategy: Strategy used to resolve (optional)
        final_score: Final resolved score (optional)
        
    Returns:
        Formatted summary string with ASCII chart
    """
    parts = []
    
    # Add header
    parts.append(f"**Conflict Type:** {conflict_type.replace('_', ' ').title()}")
    parts.append("")
    
    # Add ASCII chart
    chart = generate_disagreement_chart(model_scores)
    parts.append(chart)
    
    # Add resolution info if available
    if resolution_strategy or final_score is not None:
        parts.append("")
        if resolution_strategy:
            parts.append(f"**Resolution:** {resolution_strategy.title()}")
        if final_score is not None:
            parts.append(f"**Final Score:** {final_score:.3f}")
    
    return "\n".join(parts)


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
    ESCALATION = ("escalation", 0xE74C3C)  # Dark Red - Phase 5

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
            "escalation": "📈",  # Phase 5 - trending up
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
        Convert to Discord embed format with FE-002 length validation.

        Returns:
            Discord embed dictionary with all fields properly truncated
        """
        # FE-002: Truncate title to Discord limit
        title = f"{self.severity.emoji} {self.title}"
        title = truncate_text(title, DISCORD_LIMITS["embed_title"])
        
        # FE-002: Truncate description at natural boundary
        description = truncate_at_boundary(
            self.description, 
            DISCORD_LIMITS["embed_description"]
        )
        
        embed = {
            "title": title,
            "description": description,
            "color": self.severity.color,
            "timestamp": self.timestamp.isoformat() + "Z",
            "footer": {
                "text": truncate_text(
                    f"Ash-NLP | {self.source}",
                    DISCORD_LIMITS["embed_footer_text"]
                ),
            },
        }

        if self.fields:
            embed["fields"] = [
                {
                    "name": truncate_text(k, DISCORD_LIMITS["embed_field_name"]),
                    "value": truncate_text(str(v), DISCORD_LIMITS["embed_field_value"]),
                    "inline": True,
                }
                for k, v in self.fields.items()
            ]
        
        # FE-002: Validate total embed size and log if issues found
        is_valid, total_size, issues = validate_embed_size(embed)
        if not is_valid:
            logger.warning(
                f"FE-002: Embed validation issues: {issues}. "
                f"Total size: {total_size}/{DISCORD_LIMITS['embed_total']}"
            )
            # If still too large, aggressively truncate description
            if total_size > DISCORD_LIMITS["embed_total"]:
                overage = total_size - DISCORD_LIMITS["embed_total"] + 100  # buffer
                new_max = len(description) - overage
                if new_max > 100:
                    embed["description"] = truncate_at_boundary(description, new_max)
                    logger.debug(f"FE-002: Description truncated to fit embed limit")

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
    - Testing mode for suppressing real webhooks (FE-009)

    Attributes:
        webhook_url: Discord webhook URL
        enabled: Whether alerting is enabled
        throttle: Throttle configuration
        service_name: Name of the service (for footer)
        testing_mode: Whether to suppress real webhook calls

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
        escalation_cooldown_seconds: float = 300.0,  # Phase 5
        testing_mode: Optional[bool] = None,  # Phase 6 FE-009
        conflict_alert_threshold: float = DEFAULT_CONFLICT_ALERT_THRESHOLD,  # Phase 6 FE-008
    ):
        """
        Initialize the Discord alerter.

        Args:
            webhook_url: Discord webhook URL (or None to disable)
            enabled: Whether alerting is enabled
            throttle: Throttle configuration
            service_name: Name for the footer
            conflict_cooldown_seconds: Cooldown between conflict alerts (Phase 4)
            escalation_cooldown_seconds: Cooldown between escalation alerts (Phase 5)
            testing_mode: Suppress real webhook calls (auto-detects from NLP_ENVIRONMENT)
            conflict_alert_threshold: Variance threshold to trigger conflict alerts (FE-008)
        """
        self.webhook_url = webhook_url
        self.throttle = throttle or ThrottleConfig()
        self.service_name = service_name

        # Phase 6 FE-009: Testing mode detection
        # Auto-detect from environment if not explicitly set
        if testing_mode is None:
            env = os.environ.get("NLP_ENVIRONMENT", "production")
            self._testing_mode = env.lower() == "testing"
        else:
            self._testing_mode = testing_mode

        # When in testing mode, suppress real webhook calls but track them
        self.enabled = enabled and webhook_url is not None and not self._testing_mode

        # Phase 6 FE-009: Track suppressed alerts for test assertions
        self._suppressed_alerts: List[Alert] = []
        self._alert_callback: Optional[Callable[[Alert], None]] = None

        # Throttling state
        self._alert_history: List[float] = []
        self._in_cooldown = False
        self._cooldown_until = 0.0

        # Phase 4: Conflict alert cooldown
        self._conflict_cooldown_seconds = conflict_cooldown_seconds
        self._last_conflict_alert = 0.0
        self._conflict_alert_threshold = conflict_alert_threshold  # FE-008

        # Phase 5: Escalation alert cooldown
        self._escalation_cooldown_seconds = escalation_cooldown_seconds
        self._last_escalation_alert = 0.0

        # HTTP session (lazy init)
        self._session = None

        if self._testing_mode:
            logger.info(f"🧪 Discord alerter in TESTING MODE for {service_name} (webhooks suppressed)")
        elif self.enabled:
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

    def _should_throttle_escalation(self) -> bool:
        """Check if escalation alert should be throttled (Phase 5)."""
        now = time.time()
        return now - self._last_escalation_alert < self._escalation_cooldown_seconds

    def _record_escalation_alert(self):
        """Record an escalation alert timestamp (Phase 5)."""
        self._last_escalation_alert = time.time()

    # =========================================================================
    # Send Methods
    # =========================================================================

    # =========================================================================
    # Phase 6 FE-009: Testing Mode Methods
    # =========================================================================

    def is_testing_mode(self) -> bool:
        """Check if alerter is in testing mode."""
        return self._testing_mode

    def get_suppressed_alerts(self) -> List[Alert]:
        """
        Get list of alerts that were suppressed in testing mode.

        Returns:
            List of Alert objects that would have been sent
        """
        return self._suppressed_alerts.copy()

    def clear_suppressed_alerts(self) -> None:
        """Clear the list of suppressed alerts."""
        self._suppressed_alerts.clear()

    def set_alert_callback(self, callback: Optional[Callable[[Alert], None]]) -> None:
        """
        Set a callback function to be called for each alert (useful for testing).

        Args:
            callback: Function that receives Alert objects, or None to remove
        """
        self._alert_callback = callback

    def get_last_suppressed_alert(self) -> Optional[Alert]:
        """
        Get the most recent suppressed alert.

        Returns:
            Most recent Alert or None if no alerts suppressed
        """
        return self._suppressed_alerts[-1] if self._suppressed_alerts else None

    def _handle_testing_mode_alert(self, alert: Alert) -> bool:
        """
        Handle an alert in testing mode (suppress but track).

        Args:
            alert: Alert that would be sent

        Returns:
            True (simulating successful send)
        """
        self._suppressed_alerts.append(alert)
        self._record_alert()  # Still track for throttling behavior

        if self._alert_callback:
            self._alert_callback(alert)

        logger.debug(f"🧪 Alert suppressed (testing mode): {alert.title}")
        return True

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
        # Phase 6 FE-009: Handle testing mode
        if self._testing_mode:
            return self._handle_testing_mode_alert(alert)

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
        # Phase 6 FE-009: Handle testing mode
        if self._testing_mode:
            return self._handle_testing_mode_alert(alert)

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
        # Phase 6 FE-009: Check testing mode first (before enabled check)
        if not self._testing_mode and not self.enabled:
            logger.debug(f"Conflict alert skipped (disabled): {conflict_type}")
            return False

        # Check conflict-specific cooldown (applies in both modes)
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
        # Phase 6 FE-009: Check testing mode first (before enabled check)
        if not self._testing_mode and not self.enabled:
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
    # Phase 5: Escalation Alert Methods
    # =========================================================================

    async def send_escalation_alert(
        self,
        escalation_rate: str,
        pattern_name: Optional[str],
        pattern_confidence: float,
        crisis_score: float,
        score_delta: float,
        time_span_hours: float,
        intervention_urgency: str,
        message_preview: str,
        user_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        source: str = "context_analyzer",
    ) -> bool:
        """
        Send an alert for crisis escalation detection (Phase 5).

        Args:
            escalation_rate: Rate of escalation (none, gradual, rapid, sudden)
            pattern_name: Name of matched escalation pattern
            pattern_confidence: Confidence in pattern match (0-1)
            crisis_score: Current crisis score
            score_delta: Score change during escalation
            time_span_hours: Time span of the escalation
            intervention_urgency: Urgency level (none, low, standard, high, immediate)
            message_preview: First 100 chars of current message
            user_id: Optional user identifier
            channel_id: Optional channel identifier
            source: Source component

        Returns:
            True if alert sent successfully
        """
        # Phase 6 FE-009: Check testing mode first (before enabled check)
        # In testing mode, enabled is False but we still want to track alerts
        if not self._testing_mode and not self.enabled:
            logger.debug(f"Escalation alert skipped (disabled): {escalation_rate}")
            return False

        # Check escalation-specific cooldown (applies in both modes)
        if self._should_throttle_escalation():
            logger.debug(f"Escalation alert on cooldown: {escalation_rate}")
            return False

        # Build fields
        fields = {
            "Escalation Rate": escalation_rate.replace("_", " ").title(),
            "Crisis Score": f"{crisis_score:.2f}",
            "Score Change": f"+{score_delta:.2f}" if score_delta >= 0 else f"{score_delta:.2f}",
            "Time Span": f"{time_span_hours:.1f} hours",
            "Urgency": intervention_urgency.replace("_", " ").title(),
        }

        if pattern_name:
            fields["Pattern"] = pattern_name.replace("_", " ").title()
            fields["Confidence"] = f"{pattern_confidence:.0%}"

        if user_id:
            fields["User ID"] = user_id[:20]
        if channel_id:
            fields["Channel"] = channel_id[:20]

        # Truncate message preview
        preview = message_preview[:97] + "..." if len(message_preview) > 100 else message_preview
        fields["Message"] = f"\"...{preview[-50:]}\"" if len(preview) > 50 else f"\"{preview}\""

        # Determine alert severity based on intervention urgency
        urgency_lower = intervention_urgency.lower()
        if urgency_lower == "immediate":
            alert_severity = AlertSeverity.CRITICAL
            description = (
                "**IMMEDIATE INTERVENTION REQUIRED**\n"
                "A rapid crisis escalation pattern has been detected. "
                "The user's distress level has increased significantly in a short time."
            )
        elif urgency_lower == "high":
            alert_severity = AlertSeverity.ESCALATION
            description = (
                "**High Priority: Crisis Escalation Detected**\n"
                "The user's messages show a worsening trend that may require prompt attention."
            )
        elif urgency_lower == "standard":
            alert_severity = AlertSeverity.WARNING
            description = (
                "**Crisis Escalation Pattern Detected**\n"
                "A gradual increase in crisis indicators has been observed over recent messages."
            )
        else:
            alert_severity = AlertSeverity.INFO
            description = (
                "**Monitoring: Escalation Pattern**\n"
                "A minor escalation pattern was detected. Continued monitoring recommended."
            )

        alert = Alert(
            severity=alert_severity,
            title=f"Escalation: {escalation_rate.replace('_', ' ').title()}",
            description=description,
            fields=fields,
            source=source,
        )

        result = await self.send_alert(alert)
        if result:
            self._record_escalation_alert()
        return result

    def send_escalation_alert_sync(
        self,
        escalation_rate: str,
        pattern_name: Optional[str],
        pattern_confidence: float,
        crisis_score: float,
        score_delta: float,
        time_span_hours: float,
        intervention_urgency: str,
        message_preview: str,
        user_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        source: str = "context_analyzer",
    ) -> bool:
        """
        Send an escalation alert synchronously (Phase 5).

        Args:
            escalation_rate: Rate of escalation
            pattern_name: Name of matched escalation pattern
            pattern_confidence: Confidence in pattern match (0-1)
            crisis_score: Current crisis score
            score_delta: Score change during escalation
            time_span_hours: Time span of the escalation
            intervention_urgency: Urgency level
            message_preview: First 100 chars of current message
            user_id: Optional user identifier
            channel_id: Optional channel identifier
            source: Source component

        Returns:
            True if alert sent successfully
        """
        # Phase 6 FE-009: Check testing mode first (before enabled check)
        if not self._testing_mode and not self.enabled:
            return False

        if self._should_throttle_escalation():
            logger.debug(f"Escalation alert on cooldown: {escalation_rate}")
            return False

        # Build fields
        fields = {
            "Escalation Rate": escalation_rate.replace("_", " ").title(),
            "Crisis Score": f"{crisis_score:.2f}",
            "Score Change": f"+{score_delta:.2f}" if score_delta >= 0 else f"{score_delta:.2f}",
            "Time Span": f"{time_span_hours:.1f} hours",
            "Urgency": intervention_urgency.replace("_", " ").title(),
        }

        if pattern_name:
            fields["Pattern"] = pattern_name.replace("_", " ").title()

        # Determine alert severity
        urgency_lower = intervention_urgency.lower()
        if urgency_lower == "immediate":
            alert_severity = AlertSeverity.CRITICAL
        elif urgency_lower == "high":
            alert_severity = AlertSeverity.ESCALATION
        elif urgency_lower == "standard":
            alert_severity = AlertSeverity.WARNING
        else:
            alert_severity = AlertSeverity.INFO

        alert = Alert(
            severity=alert_severity,
            title=f"Escalation: {escalation_rate.replace('_', ' ').title()}",
            description="Crisis escalation pattern detected in user messages.",
            fields=fields,
            source=source,
        )

        result = self.send_alert_sync(alert)
        if result:
            self._record_escalation_alert()
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
            "testing_mode": self._testing_mode,  # Phase 6 FE-009
            "suppressed_alert_count": len(self._suppressed_alerts),  # Phase 6 FE-009
            "in_cooldown": self._in_cooldown,
            "alerts_in_window": len(self._alert_history),
            "conflict_cooldown_remaining": max(
                0,
                self._conflict_cooldown_seconds
                - (time.time() - self._last_conflict_alert),
            ),
            "escalation_cooldown_remaining": max(
                0,
                self._escalation_cooldown_seconds
                - (time.time() - self._last_escalation_alert),
            ),
            "throttle_config": {
                "window_seconds": self.throttle.window_seconds,
                "max_alerts": self.throttle.max_alerts,
                "cooldown_seconds": self.throttle.cooldown_seconds,
                "conflict_cooldown_seconds": self._conflict_cooldown_seconds,
                "escalation_cooldown_seconds": self._escalation_cooldown_seconds,
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
    escalation_cooldown_seconds: float = 300.0,
    testing_mode: Optional[bool] = None,
) -> DiscordAlerter:
    """
    Factory function to create a Discord alerter.

    Args:
        webhook_url: Explicit webhook URL (optional)
        secrets_manager: SecretsManager instance for loading URL
        enabled: Whether alerting is enabled
        conflict_cooldown_seconds: Cooldown between conflict alerts (Phase 4)
        escalation_cooldown_seconds: Cooldown between escalation alerts (Phase 5)
        testing_mode: Suppress real webhooks (auto-detects from NLP_ENVIRONMENT)

    Returns:
        Configured DiscordAlerter instance

    Note (Phase 6 FE-009):
        When NLP_ENVIRONMENT="testing" or testing_mode=True, webhook calls are
        suppressed but tracked. Use get_suppressed_alerts() to inspect them.
    """
    # Get webhook URL from secrets if not provided
    if webhook_url is None and secrets_manager is not None:
        webhook_url = secrets_manager.get("discord_alert_webhook")

    # Also check environment variable
    if webhook_url is None:
        webhook_url = os.environ.get("NLP_DISCORD_ALERT_WEBHOOK")

    return DiscordAlerter(
        webhook_url=webhook_url,
        enabled=enabled,
        conflict_cooldown_seconds=conflict_cooldown_seconds,
        escalation_cooldown_seconds=escalation_cooldown_seconds,
        testing_mode=testing_mode,
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
    # FE-002: Discord limits and truncation
    "DISCORD_LIMITS",
    "truncate_text",
    "truncate_at_boundary",
    "calculate_embed_size",
    "validate_embed_size",
    # FE-008: Conflict alert enhancements
    "DEFAULT_CONFLICT_ALERT_THRESHOLD",
    "generate_disagreement_chart",
    "format_conflict_summary",
]
