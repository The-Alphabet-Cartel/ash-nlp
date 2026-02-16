"""
============================================================================
Ash-NLP: Crisis Detection NLP Server
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Analyze  → Process messages through multi-model ensemble classification
    Detect   → Identify crisis signals with weighted consensus algorithms
    Explain  → Provide human-readable explanations for all decisions
    Protect  → Safeguard our LGBTQIA+ community through accurate detection

============================================================================
Consensus Disagreement Escalation (Step 6.4.3)

Safety net that catches implicit/euphemistic crisis language where BART
misses signals that contextual models (sentiment, emotions) detect.

When the consensus score significantly exceeds the pipeline score, a
severity floor is applied — preventing the final classification from
dropping too far below the consensus assessment.

Key principles:
- Pipeline remains authoritative (consensus never overrides, only floors)
- Floor can only RAISE scores, never lower
- Dual threshold guard (disagreement AND consensus minimum)
- DROP_LEVELS provides "err one level toward caution" logic
- Escalated messages are flagged for CRT review
----------------------------------------------------------------------------
FILE VERSION: v5.1-6-6.4.3-1
LAST MODIFIED: 2026-02-15
PHASE: Phase 6 - Step 6.4.3 Consensus Disagreement Escalation
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, TYPE_CHECKING

from .scoring import CrisisSeverity

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.1-6-6.4.3-1"

# Initialize logger
logger = logging.getLogger(__name__)

# Severity ordering for drop_levels calculation (highest to lowest)
SEVERITY_ORDER = [
    CrisisSeverity.CRITICAL,
    CrisisSeverity.HIGH,
    CrisisSeverity.MEDIUM,
    CrisisSeverity.LOW,
    CrisisSeverity.SAFE,
]

# Minimum score required to reach each severity level (default thresholds)
DEFAULT_SEVERITY_THRESHOLDS = {
    CrisisSeverity.CRITICAL: 0.85,
    CrisisSeverity.HIGH: 0.70,
    CrisisSeverity.MEDIUM: 0.50,
    CrisisSeverity.LOW: 0.30,
    CrisisSeverity.SAFE: 0.0,
}


# =============================================================================
# Consensus Escalation Result Dataclass
# =============================================================================


@dataclass
class ConsensusEscalationResult:
    """
    Result of consensus disagreement escalation check.

    Attributes:
        triggered: Whether the escalation floor was applied
        pipeline_score: Original pipeline score (ensemble → Vigil → irony gate)
        pipeline_severity: Original pipeline severity
        consensus_score: Consensus algorithm score
        consensus_severity: Mapped severity of consensus score
        disagreement: Gap between consensus and pipeline (consensus - pipeline)
        floor_severity: Severity floor applied (consensus - drop_levels)
        floor_score: Minimum score from floor severity threshold
        final_score: Result score after floor application
        final_severity: Result severity after floor application
        escalation_reason: Human-readable reason if triggered
    """

    triggered: bool
    pipeline_score: float
    pipeline_severity: CrisisSeverity
    consensus_score: float
    consensus_severity: CrisisSeverity
    disagreement: float
    floor_severity: Optional[CrisisSeverity] = None
    floor_score: Optional[float] = None
    final_score: Optional[float] = None
    final_severity: Optional[CrisisSeverity] = None
    escalation_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        result = {
            "triggered": self.triggered,
            "pipeline_score": round(self.pipeline_score, 4),
            "pipeline_severity": self.pipeline_severity.value,
            "consensus_score": round(self.consensus_score, 4),
            "consensus_severity": self.consensus_severity.value,
            "disagreement": round(self.disagreement, 4),
        }

        if self.triggered:
            result["floor_severity"] = self.floor_severity.value if self.floor_severity else None
            result["floor_score"] = round(self.floor_score, 4) if self.floor_score is not None else None
            result["final_score"] = round(self.final_score, 4) if self.final_score is not None else None
            result["final_severity"] = self.final_severity.value if self.final_severity else None
            result["escalation_reason"] = self.escalation_reason

        return result


# =============================================================================
# Consensus Escalation Engine
# =============================================================================


class ConsensusEscalation:
    """
    Consensus Disagreement Escalation - Safety Net for Implicit Crisis.

    When the consensus algorithm (independent model voting) scores
    significantly higher than the pipeline (ensemble → Vigil → irony gate),
    this indicates contextual models detected crisis signals that BART
    missed — common with euphemistic/implicit crisis language.

    The escalation applies a SEVERITY FLOOR:
    - Consensus severity is calculated from consensus_score
    - Floor severity = consensus_severity - drop_levels
    - Floor score = minimum threshold for floor_severity
    - Final score = max(pipeline_score, floor_score)

    The floor can only RAISE scores, never lower them. This preserves
    pipeline authority while adding a safety net.

    Configuration: classification_config.json → consensus_escalation
    Environment: NLP_CONSENSUS_ESCALATION_* variables

    Clean Architecture v5.2.3 Compliance:
    - Factory function: create_consensus_escalation()
    - Configuration via ConfigManager
    - Resilient error handling (Rule #5)
    """

    def __init__(
        self,
        enabled: bool = True,
        disagreement_threshold: float = 0.15,
        consensus_minimum_score: float = 0.40,
        drop_levels: int = 1,
        set_requires_review: bool = True,
        severity_thresholds: Optional[Dict[CrisisSeverity, float]] = None,
    ):
        """
        Initialize ConsensusEscalation.

        Args:
            enabled: Master toggle
            disagreement_threshold: Min gap to trigger (consensus - pipeline)
            consensus_minimum_score: Consensus must be at least this
            drop_levels: Severity levels below consensus for floor
            set_requires_review: Flag escalated messages for CRT
            severity_thresholds: Score thresholds per severity level
        """
        self.enabled = enabled
        self.disagreement_threshold = max(0.1, min(0.9, disagreement_threshold))
        self.consensus_minimum_score = max(0.3, min(0.95, consensus_minimum_score))
        self.drop_levels = max(0, min(3, drop_levels))
        self.set_requires_review = set_requires_review
        self.severity_thresholds = severity_thresholds or dict(DEFAULT_SEVERITY_THRESHOLDS)

        logger.info(
            f"🛡️ ConsensusEscalation initialized "
            f"(enabled={enabled}, "
            f"disagreement_threshold={self.disagreement_threshold}, "
            f"consensus_minimum={self.consensus_minimum_score}, "
            f"drop_levels={self.drop_levels})"
        )

    def _severity_index(self, severity: CrisisSeverity) -> int:
        """Get index of severity in ordered list (0=CRITICAL, 4=SAFE)."""
        try:
            return SEVERITY_ORDER.index(severity)
        except ValueError:
            return len(SEVERITY_ORDER) - 1  # Default to SAFE

    def _drop_severity(self, severity: CrisisSeverity, levels: int) -> CrisisSeverity:
        """
        Drop severity by N levels toward SAFE.

        CRITICAL -1 → HIGH, HIGH -1 → MEDIUM, etc.

        Args:
            severity: Starting severity
            levels: Number of levels to drop

        Returns:
            Dropped severity (clamped to SAFE)
        """
        idx = self._severity_index(severity)
        new_idx = min(idx + levels, len(SEVERITY_ORDER) - 1)
        return SEVERITY_ORDER[new_idx]

    def _score_for_severity(self, severity: CrisisSeverity) -> float:
        """Get minimum score threshold for a severity level."""
        return self.severity_thresholds.get(severity, 0.0)

    def apply_floor(
        self,
        pipeline_score: float,
        pipeline_severity: CrisisSeverity,
        consensus_score: float,
        thresholds: Optional[Dict[str, float]] = None,
    ) -> ConsensusEscalationResult:
        """
        Apply consensus disagreement severity floor.

        This is the core escalation logic. When consensus significantly
        exceeds the pipeline, a floor prevents final classification from
        dropping too far below the consensus assessment.

        Args:
            pipeline_score: Score from ensemble → Vigil → irony gate
            pipeline_severity: Severity from pipeline score
            consensus_score: Independent consensus algorithm score
            thresholds: Optional score thresholds dict (keys: critical,
                        high, medium, low) for severity mapping

        Returns:
            ConsensusEscalationResult with floor application details
        """
        # Update severity thresholds if provided
        if thresholds:
            self.severity_thresholds = {
                CrisisSeverity.CRITICAL: thresholds.get("critical", 0.85),
                CrisisSeverity.HIGH: thresholds.get("high", 0.70),
                CrisisSeverity.MEDIUM: thresholds.get("medium", 0.50),
                CrisisSeverity.LOW: thresholds.get("low", 0.30),
                CrisisSeverity.SAFE: 0.0,
            }

        # Map consensus score to severity
        consensus_severity = CrisisSeverity.from_score(
            consensus_score,
            {
                "critical": self.severity_thresholds[CrisisSeverity.CRITICAL],
                "high": self.severity_thresholds[CrisisSeverity.HIGH],
                "medium": self.severity_thresholds[CrisisSeverity.MEDIUM],
                "low": self.severity_thresholds[CrisisSeverity.LOW],
            },
        )

        # Calculate disagreement
        disagreement = consensus_score - pipeline_score

        # =====================================================================
        # Gate 1: Is escalation enabled?
        # =====================================================================
        if not self.enabled:
            logger.debug("🛡️ Consensus escalation disabled")
            return ConsensusEscalationResult(
                triggered=False,
                pipeline_score=pipeline_score,
                pipeline_severity=pipeline_severity,
                consensus_score=consensus_score,
                consensus_severity=consensus_severity,
                disagreement=disagreement,
            )

        # =====================================================================
        # Gate 2: Is disagreement large enough?
        # =====================================================================
        if disagreement < self.disagreement_threshold:
            logger.debug(
                f"🛡️ Consensus escalation pass-through: "
                f"disagreement {disagreement:.3f} < "
                f"threshold {self.disagreement_threshold}"
            )
            return ConsensusEscalationResult(
                triggered=False,
                pipeline_score=pipeline_score,
                pipeline_severity=pipeline_severity,
                consensus_score=consensus_score,
                consensus_severity=consensus_severity,
                disagreement=disagreement,
            )

        # =====================================================================
        # Gate 3: Is consensus score high enough?
        # =====================================================================
        if consensus_score < self.consensus_minimum_score:
            logger.debug(
                f"🛡️ Consensus escalation pass-through: "
                f"consensus {consensus_score:.3f} < "
                f"minimum {self.consensus_minimum_score}"
            )
            return ConsensusEscalationResult(
                triggered=False,
                pipeline_score=pipeline_score,
                pipeline_severity=pipeline_severity,
                consensus_score=consensus_score,
                consensus_severity=consensus_severity,
                disagreement=disagreement,
            )

        # =====================================================================
        # Apply severity floor
        # =====================================================================

        # Calculate floor severity (consensus - drop_levels)
        floor_severity = self._drop_severity(consensus_severity, self.drop_levels)

        # Get minimum score for floor severity
        floor_score = self._score_for_severity(floor_severity)

        # Floor can only RAISE, never lower
        final_score = max(pipeline_score, floor_score)
        final_severity = CrisisSeverity.from_score(
            final_score,
            {
                "critical": self.severity_thresholds[CrisisSeverity.CRITICAL],
                "high": self.severity_thresholds[CrisisSeverity.HIGH],
                "medium": self.severity_thresholds[CrisisSeverity.MEDIUM],
                "low": self.severity_thresholds[CrisisSeverity.LOW],
            },
        )

        # Build escalation reason
        escalation_reason = (
            f"consensus_disagreement: consensus={consensus_score:.3f} "
            f"({consensus_severity.value}) vs pipeline={pipeline_score:.3f} "
            f"({pipeline_severity.value}), "
            f"floor={floor_severity.value} (score={floor_score:.3f})"
        )

        logger.info(
            f"🛡️ ConsensusEscalation TRIGGERED: "
            f"pipeline={pipeline_score:.3f}→{final_score:.3f} "
            f"({pipeline_severity.value}→{final_severity.value}), "
            f"consensus={consensus_score:.3f} ({consensus_severity.value}), "
            f"disagreement={disagreement:.3f}, "
            f"floor={floor_severity.value}"
        )

        return ConsensusEscalationResult(
            triggered=True,
            pipeline_score=pipeline_score,
            pipeline_severity=pipeline_severity,
            consensus_score=consensus_score,
            consensus_severity=consensus_severity,
            disagreement=disagreement,
            floor_severity=floor_severity,
            floor_score=floor_score,
            final_score=final_score,
            final_severity=final_severity,
            escalation_reason=escalation_reason,
        )


# =============================================================================
# Factory Function - Clean Architecture v5.2.3 Compliance (Rule #1)
# =============================================================================


def create_consensus_escalation(
    config_manager: Optional["ConfigManager"] = None,
    enabled: Optional[bool] = None,
    disagreement_threshold: Optional[float] = None,
    consensus_minimum_score: Optional[float] = None,
    drop_levels: Optional[int] = None,
    set_requires_review: Optional[bool] = None,
) -> ConsensusEscalation:
    """
    Factory function for ConsensusEscalation.

    Creates a configured ConsensusEscalation using ConfigManager settings,
    with optional explicit overrides.

    Args:
        config_manager: Configuration manager instance
        enabled: Override enabled flag
        disagreement_threshold: Override disagreement threshold
        consensus_minimum_score: Override consensus minimum
        drop_levels: Override drop levels
        set_requires_review: Override review flag

    Returns:
        Configured ConsensusEscalation instance

    Example:
        >>> escalation = create_consensus_escalation(config_manager=config)
        >>> result = escalation.apply_floor(
        ...     pipeline_score=0.19,
        ...     pipeline_severity=CrisisSeverity.SAFE,
        ...     consensus_score=0.84,
        ... )
    """
    ce_enabled = True
    ce_disagreement = 0.15
    ce_minimum = 0.40
    ce_drop = 1
    ce_review = True

    # Load from config manager
    if config_manager is not None:
        try:
            ce_config = config_manager.get_consensus_escalation_config()
            if ce_config:
                ce_enabled = ce_config.get("enabled", True)
                ce_disagreement = ce_config.get("disagreement_threshold", 0.15)
                ce_minimum = ce_config.get("consensus_minimum_score", 0.40)
                ce_drop = ce_config.get("drop_levels", 1)
                ce_review = ce_config.get("set_requires_review", True)
        except Exception as e:
            logger.warning(
                f"⚠️ Error loading consensus escalation config, "
                f"using defaults: {e}"
            )

    # Apply explicit overrides
    if enabled is not None:
        ce_enabled = enabled
    if disagreement_threshold is not None:
        ce_disagreement = disagreement_threshold
    if consensus_minimum_score is not None:
        ce_minimum = consensus_minimum_score
    if drop_levels is not None:
        ce_drop = drop_levels
    if set_requires_review is not None:
        ce_review = set_requires_review

    return ConsensusEscalation(
        enabled=ce_enabled,
        disagreement_threshold=ce_disagreement,
        consensus_minimum_score=ce_minimum,
        drop_levels=ce_drop,
        set_requires_review=ce_review,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "ConsensusEscalationResult",
    "ConsensusEscalation",
    "create_consensus_escalation",
    "SEVERITY_ORDER",
    "DEFAULT_SEVERITY_THRESHOLDS",
]
