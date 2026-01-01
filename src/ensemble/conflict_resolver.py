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
Conflict Resolution for Ash-NLP Ensemble Service
---
FILE VERSION: v5.0-4-2.6-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 Step 2 - Conflict Resolution
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Resolve conflicts between ensemble models
- Apply resolution strategies:
  - Conservative: Use highest crisis score (safety-first) - DEFAULT
  - Optimistic: Use lowest crisis score (reduce false positives)
  - Mean: Use average score (balanced)
  - Review Flag: Flag for human review (defer decision)
- Support Discord alerting for conflicts requiring review

DESIGN PHILOSOPHY:
For a LIFE-SAVING crisis detection system:
- DEFAULT to conservative (safety-first)
- Better to over-alert than miss a crisis
- Human review when models significantly disagree
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from .conflict_detector import ConflictReport, ConflictSeverity

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager
    from src.utils.alerting import DiscordAlerter

# Module version
__version__ = "v5.0-4-2.6-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Resolution Strategies
# =============================================================================


class ResolutionStrategy(Enum):
    """Available conflict resolution strategies."""

    CONSERVATIVE = "conservative"  # Use highest crisis score (safety-first)
    OPTIMISTIC = "optimistic"  # Use lowest crisis score (reduce false positives)
    MEAN = "mean"  # Use average score (balanced)
    REVIEW_FLAG = "review_flag"  # Flag for human review


# =============================================================================
# Resolution Result Data Class
# =============================================================================


@dataclass
class ResolutionResult:
    """
    Result from conflict resolution.

    Attributes:
        strategy_used: Which strategy was applied
        original_score: Score before resolution
        resolved_score: Score after resolution
        was_modified: Whether the score was changed
        requires_review: Whether human review is needed
        resolution_reason: Explanation of the resolution
        alert_sent: Whether Discord alert was sent
        metadata: Additional resolution details
    """

    strategy_used: ResolutionStrategy
    original_score: float
    resolved_score: float
    was_modified: bool
    requires_review: bool
    resolution_reason: str
    alert_sent: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "strategy_used": self.strategy_used.value,
            "original_score": round(self.original_score, 4),
            "resolved_score": round(self.resolved_score, 4),
            "was_modified": self.was_modified,
            "requires_review": self.requires_review,
            "resolution_reason": self.resolution_reason,
            "alert_sent": self.alert_sent,
            "metadata": self.metadata,
        }


# =============================================================================
# Conflict Resolver
# =============================================================================


class ConflictResolver:
    """
    Conflict Resolver for Ensemble Model Disagreements.

    Applies resolution strategies when models disagree.
    Default: Conservative (safety-first for crisis detection).

    Strategies:
    1. Conservative: Use highest crisis score
       - Rationale: Better to over-alert than miss a crisis
    2. Optimistic: Use lowest crisis score
       - Rationale: Reduce false positives when appropriate
    3. Mean: Use average of scores
       - Rationale: Balanced approach
    4. Review Flag: Flag for human review
       - Rationale: Defer decision to humans for ambiguous cases

    Clean Architecture v5.1 Compliance:
    - Factory function: create_conflict_resolver()
    - Configuration via ConfigManager
    """

    def __init__(
        self,
        default_strategy: ResolutionStrategy = ResolutionStrategy.CONSERVATIVE,
        alerter: Optional["DiscordAlerter"] = None,
        alert_on_high_severity: bool = True,
        alert_on_review_flag: bool = True,
        alert_cooldown_seconds: float = 60.0,
    ):
        """
        Initialize ConflictResolver.

        Args:
            default_strategy: Default resolution strategy
            alerter: Discord alerter for notifications
            alert_on_high_severity: Alert on high severity conflicts
            alert_on_review_flag: Alert when review is flagged
            alert_cooldown_seconds: Minimum time between alerts
        """
        self.default_strategy = default_strategy
        self._alerter = alerter
        self.alert_on_high_severity = alert_on_high_severity
        self.alert_on_review_flag = alert_on_review_flag
        self.alert_cooldown_seconds = alert_cooldown_seconds

        # Alert rate limiting
        self._last_alert_time: float = 0.0
        self._alert_count: int = 0

        # Strategy implementations
        self._strategies: Dict[ResolutionStrategy, Callable] = {
            ResolutionStrategy.CONSERVATIVE: self._apply_conservative,
            ResolutionStrategy.OPTIMISTIC: self._apply_optimistic,
            ResolutionStrategy.MEAN: self._apply_mean,
            ResolutionStrategy.REVIEW_FLAG: self._apply_review_flag,
        }

        logger.info(
            f"⚖️ ConflictResolver initialized "
            f"(default: {default_strategy.value}, "
            f"alert_high={alert_on_high_severity}, "
            f"alert_review={alert_on_review_flag})"
        )

    def resolve(
        self,
        crisis_scores: Dict[str, float],
        conflict_report: ConflictReport,
        strategy: Optional[ResolutionStrategy] = None,
        message_preview: str = "",
    ) -> ResolutionResult:
        """
        Resolve model conflicts and determine final score.

        Args:
            crisis_scores: Dict of model_name -> crisis_signal
            conflict_report: Report from ConflictDetector
            strategy: Override strategy (None = default)
            message_preview: First 100 chars of message for alerts

        Returns:
            ResolutionResult with resolved score
        """
        active_strategy = strategy or self.default_strategy

        # Calculate original score (simple average)
        scores = list(crisis_scores.values())
        original_score = sum(scores) / len(scores) if scores else 0.0

        # If no conflicts, return original
        if not conflict_report.has_conflicts:
            return ResolutionResult(
                strategy_used=active_strategy,
                original_score=original_score,
                resolved_score=original_score,
                was_modified=False,
                requires_review=False,
                resolution_reason="No conflicts detected - using original score",
                metadata={"scores": crisis_scores},
            )

        # Apply resolution strategy
        result = self._strategies[active_strategy](
            crisis_scores=crisis_scores,
            conflict_report=conflict_report,
            original_score=original_score,
        )

        # Check if we should send alert
        alert_sent = False
        if self._should_alert(conflict_report, result):
            alert_sent = self._send_conflict_alert(
                conflict_report=conflict_report,
                result=result,
                message_preview=message_preview,
            )
            result.alert_sent = alert_sent

        return result

    async def resolve_async(
        self,
        crisis_scores: Dict[str, float],
        conflict_report: ConflictReport,
        strategy: Optional[ResolutionStrategy] = None,
        message_preview: str = "",
    ) -> ResolutionResult:
        """
        Async version of resolve with async alerting.

        Args:
            crisis_scores: Dict of model_name -> crisis_signal
            conflict_report: Report from ConflictDetector
            strategy: Override strategy (None = default)
            message_preview: First 100 chars of message for alerts

        Returns:
            ResolutionResult with resolved score
        """
        active_strategy = strategy or self.default_strategy

        # Calculate original score
        scores = list(crisis_scores.values())
        original_score = sum(scores) / len(scores) if scores else 0.0

        # If no conflicts, return original
        if not conflict_report.has_conflicts:
            return ResolutionResult(
                strategy_used=active_strategy,
                original_score=original_score,
                resolved_score=original_score,
                was_modified=False,
                requires_review=False,
                resolution_reason="No conflicts detected - using original score",
                metadata={"scores": crisis_scores},
            )

        # Apply resolution strategy
        result = self._strategies[active_strategy](
            crisis_scores=crisis_scores,
            conflict_report=conflict_report,
            original_score=original_score,
        )

        # Check if we should send alert (async)
        alert_sent = False
        if self._should_alert(conflict_report, result):
            alert_sent = await self._send_conflict_alert_async(
                conflict_report=conflict_report,
                result=result,
                message_preview=message_preview,
            )
            result.alert_sent = alert_sent

        return result

    # =========================================================================
    # Strategy Implementations
    # =========================================================================

    def _apply_conservative(
        self,
        crisis_scores: Dict[str, float],
        conflict_report: ConflictReport,
        original_score: float,
    ) -> ResolutionResult:
        """
        Conservative strategy: Use highest crisis score.

        Rationale: For life-saving service, better to over-alert.
        """
        max_score = max(crisis_scores.values())
        max_model = max(crisis_scores, key=crisis_scores.get)

        was_modified = abs(max_score - original_score) > 0.01

        return ResolutionResult(
            strategy_used=ResolutionStrategy.CONSERVATIVE,
            original_score=original_score,
            resolved_score=max_score,
            was_modified=was_modified,
            requires_review=conflict_report.requires_review,
            resolution_reason=(
                f"Conservative: Using highest score from {max_model} ({max_score:.2f}) "
                f"due to {conflict_report.conflict_count} conflict(s)"
            ),
            metadata={
                "max_model": max_model,
                "max_score": max_score,
                "conflict_count": conflict_report.conflict_count,
            },
        )

    def _apply_optimistic(
        self,
        crisis_scores: Dict[str, float],
        conflict_report: ConflictReport,
        original_score: float,
    ) -> ResolutionResult:
        """
        Optimistic strategy: Use lowest crisis score.

        Rationale: Reduce false positives when human review is available.
        """
        min_score = min(crisis_scores.values())
        min_model = min(crisis_scores, key=crisis_scores.get)

        was_modified = abs(min_score - original_score) > 0.01

        return ResolutionResult(
            strategy_used=ResolutionStrategy.OPTIMISTIC,
            original_score=original_score,
            resolved_score=min_score,
            was_modified=was_modified,
            requires_review=True,  # Always recommend review for optimistic
            resolution_reason=(
                f"Optimistic: Using lowest score from {min_model} ({min_score:.2f}) "
                f"- human review recommended"
            ),
            metadata={
                "min_model": min_model,
                "min_score": min_score,
                "conflict_count": conflict_report.conflict_count,
            },
        )

    def _apply_mean(
        self,
        crisis_scores: Dict[str, float],
        conflict_report: ConflictReport,
        original_score: float,
    ) -> ResolutionResult:
        """
        Mean strategy: Use average of scores.

        Rationale: Balanced approach that considers all models equally.
        """
        # Mean is already the original_score
        mean_score = original_score

        return ResolutionResult(
            strategy_used=ResolutionStrategy.MEAN,
            original_score=original_score,
            resolved_score=mean_score,
            was_modified=False,
            requires_review=conflict_report.requires_review,
            resolution_reason=(
                f"Mean: Using average score ({mean_score:.2f}) "
                f"across {len(crisis_scores)} models"
            ),
            metadata={
                "model_count": len(crisis_scores),
                "all_scores": crisis_scores,
                "conflict_count": conflict_report.conflict_count,
            },
        )

    def _apply_review_flag(
        self,
        crisis_scores: Dict[str, float],
        conflict_report: ConflictReport,
        original_score: float,
    ) -> ResolutionResult:
        """
        Review Flag strategy: Use conservative score but always flag for review.

        Rationale: Let humans decide on ambiguous cases.
        """
        # Use conservative (highest) as interim score
        max_score = max(crisis_scores.values())
        max_model = max(crisis_scores, key=crisis_scores.get)

        was_modified = abs(max_score - original_score) > 0.01

        return ResolutionResult(
            strategy_used=ResolutionStrategy.REVIEW_FLAG,
            original_score=original_score,
            resolved_score=max_score,  # Conservative interim
            was_modified=was_modified,
            requires_review=True,  # Always requires review
            resolution_reason=(
                f"Review Flag: Using conservative interim score ({max_score:.2f}) "
                f"but flagging for human review due to {conflict_report.conflict_count} conflict(s)"
            ),
            metadata={
                "interim_score": max_score,
                "interim_model": max_model,
                "conflict_types": [c.conflict_type.value for c in conflict_report.conflicts],
                "highest_severity": conflict_report.highest_severity.value if conflict_report.highest_severity else None,
            },
        )

    # =========================================================================
    # Alerting Methods
    # =========================================================================

    def _should_alert(
        self, conflict_report: ConflictReport, result: ResolutionResult
    ) -> bool:
        """Determine if we should send a Discord alert."""
        if self._alerter is None:
            return False

        # Check cooldown
        now = time.time()
        if now - self._last_alert_time < self.alert_cooldown_seconds:
            return False

        # Check conditions
        if self.alert_on_high_severity:
            if conflict_report.highest_severity == ConflictSeverity.HIGH:
                return True

        if self.alert_on_review_flag:
            if result.requires_review:
                return True

        return False

    def _send_conflict_alert(
        self,
        conflict_report: ConflictReport,
        result: ResolutionResult,
        message_preview: str,
    ) -> bool:
        """
        Send Discord alert for conflict (sync version).

        Args:
            conflict_report: Conflict analysis
            result: Resolution result
            message_preview: First 100 chars of message

        Returns:
            True if alert was sent
        """
        if self._alerter is None:
            return False

        try:
            # Build alert message
            alert_content = self._build_alert_content(
                conflict_report, result, message_preview
            )

            # Send via alerter (fire and forget for sync)
            asyncio.create_task(
                self._alerter.send_conflict_alert(
                    content=alert_content,
                    severity=conflict_report.highest_severity.value if conflict_report.highest_severity else "unknown",
                )
            )

            self._last_alert_time = time.time()
            self._alert_count += 1
            logger.info(f"📢 Conflict alert queued (total: {self._alert_count})")
            return True

        except Exception as e:
            logger.error(f"Failed to send conflict alert: {e}")
            return False

    async def _send_conflict_alert_async(
        self,
        conflict_report: ConflictReport,
        result: ResolutionResult,
        message_preview: str,
    ) -> bool:
        """
        Send Discord alert for conflict (async version).

        Args:
            conflict_report: Conflict analysis
            result: Resolution result
            message_preview: First 100 chars of message

        Returns:
            True if alert was sent
        """
        if self._alerter is None:
            return False

        try:
            # Build alert message
            alert_content = self._build_alert_content(
                conflict_report, result, message_preview
            )

            # Send via alerter
            await self._alerter.send_conflict_alert(
                content=alert_content,
                severity=conflict_report.highest_severity.value if conflict_report.highest_severity else "unknown",
            )

            self._last_alert_time = time.time()
            self._alert_count += 1
            logger.info(f"📢 Conflict alert sent (total: {self._alert_count})")
            return True

        except Exception as e:
            logger.error(f"Failed to send conflict alert: {e}")
            return False

    def _build_alert_content(
        self,
        conflict_report: ConflictReport,
        result: ResolutionResult,
        message_preview: str,
    ) -> Dict[str, Any]:
        """Build structured alert content."""
        # Truncate message preview safely
        safe_preview = message_preview[:100] + "..." if len(message_preview) > 100 else message_preview

        return {
            "title": "⚠️ Model Conflict Detected",
            "severity": conflict_report.highest_severity.value if conflict_report.highest_severity else "unknown",
            "conflict_count": conflict_report.conflict_count,
            "conflicts": [c.to_dict() for c in conflict_report.conflicts],
            "resolution": {
                "strategy": result.strategy_used.value,
                "original_score": result.original_score,
                "resolved_score": result.resolved_score,
                "requires_review": result.requires_review,
            },
            "message_preview": safe_preview,
            "summary": conflict_report.summary,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        }

    # =========================================================================
    # Configuration Methods
    # =========================================================================

    def set_strategy(self, strategy: ResolutionStrategy) -> None:
        """Set the default resolution strategy."""
        self.default_strategy = strategy
        logger.info(f"Default strategy set to: {strategy.value}")

    def set_alerter(self, alerter: "DiscordAlerter") -> None:
        """Set the Discord alerter."""
        self._alerter = alerter
        logger.info("Discord alerter configured for conflict resolution")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "default_strategy": self.default_strategy.value,
            "alert_on_high_severity": self.alert_on_high_severity,
            "alert_on_review_flag": self.alert_on_review_flag,
            "alert_cooldown_seconds": self.alert_cooldown_seconds,
            "alerter_configured": self._alerter is not None,
            "total_alerts_sent": self._alert_count,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get resolution statistics."""
        return {
            "total_alerts_sent": self._alert_count,
            "last_alert_time": self._last_alert_time,
            "alerter_configured": self._alerter is not None,
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_conflict_resolver(
    config_manager: Optional["ConfigManager"] = None,
    alerter: Optional["DiscordAlerter"] = None,
    default_strategy: Optional[str] = None,
) -> ConflictResolver:
    """
    Factory function for ConflictResolver.

    Creates a configured conflict resolver.

    Args:
        config_manager: Configuration manager instance
        alerter: Discord alerter for notifications
        default_strategy: Strategy name string (optional)

    Returns:
        Configured ConflictResolver instance

    Example:
        >>> resolver = create_conflict_resolver(config_manager=config)
        >>> result = resolver.resolve(scores, conflict_report)
    """
    # Default values
    final_strategy = ResolutionStrategy.CONSERVATIVE
    alert_high = True
    alert_review = True
    cooldown = 60.0

    # Load from config manager
    if config_manager is not None:
        resolution_config = config_manager.get_conflict_resolution_config()
        if resolution_config:
            strategy_name = resolution_config.get("default_strategy")
            if strategy_name:
                try:
                    final_strategy = ResolutionStrategy(strategy_name)
                except ValueError:
                    logger.warning(
                        f"Invalid strategy '{strategy_name}', using conservative"
                    )

        alert_config = config_manager.get_conflict_alerting_config()
        if alert_config:
            alert_high = alert_config.get("alert_on_high_severity", alert_high)
            alert_review = alert_config.get("alert_on_review_flag", alert_review)
            cooldown = alert_config.get("cooldown_seconds", cooldown)

    # Apply explicit override
    if default_strategy:
        try:
            final_strategy = ResolutionStrategy(default_strategy)
        except ValueError:
            logger.warning(
                f"Invalid strategy '{default_strategy}', using conservative"
            )

    return ConflictResolver(
        default_strategy=final_strategy,
        alerter=alerter,
        alert_on_high_severity=alert_high,
        alert_on_review_flag=alert_review,
        alert_cooldown_seconds=cooldown,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "ResolutionStrategy",
    # Data classes
    "ResolutionResult",
    # Resolver class
    "ConflictResolver",
    "create_conflict_resolver",
]
