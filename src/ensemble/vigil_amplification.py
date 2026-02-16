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
Vigil Amplification Logic for Ensemble Decision Engine

Standalone functions for Ash-Vigil risk amplification:
- load_vigil_config(): Load Vigil amplification settings from ConfigManager
- apply_vigil_amplification(): Async Vigil call + score boosting
- apply_vigil_amplification_sync(): Sync wrapper for above
- determine_requires_review(): CRT review flag logic
----------------------------------------------------------------------------
FILE VERSION: v5.1-6-6.4.3-1
LAST MODIFIED: 2026-02-15
PHASE: Phase 6 - Step 6.4.3 Decision Engine Decomposition
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import asyncio
import copy
import logging
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

from src.clients.vigil_client import VigilClient, VigilStatus, VigilResult
from .data_models import VigilResponse
from .scoring import CrisisSeverity, ModelSignal

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.1-6-6.4.3-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Default Vigil Amplification Configuration
# =============================================================================

DEFAULT_VIGIL_AMPLIFICATION = {
    "enabled": True,
    "score_cap": 1.0,
    "skip_threshold": 0.70,
    "amplify_medium": True,
    "confidence_skip": {
        "enabled": True,
        "crisis_threshold": 0.85,
        "safe_threshold": 0.90,
    },
    "vigil_thresholds": {
        "critical": 0.8,
        "high": 0.6,
        "moderate": 0.4,
    },
    "boosts": {
        "critical_boost": 0.35,
        "critical_minimum": 0.55,
        "high_multiplier": 0.3,
        "moderate_multiplier": 0.1,
    },
}


# =============================================================================
# Configuration Loading
# =============================================================================


def load_vigil_config(
    config_manager: Optional["ConfigManager"],
    vigil_config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Load Vigil amplification configuration from ConfigManager.

    The resolved config from ConfigManager contains the final resolved values
    with environment variable overrides applied. Nested dicts like
    vigil_thresholds and boosts are fully resolved.

    Args:
        config_manager: Configuration manager instance
        vigil_config: Mutable config dict to update in-place

    Returns:
        Updated vigil_config dictionary
    """
    if config_manager is None:
        logger.debug("No config_manager provided, using Vigil defaults")
        return vigil_config

    try:
        # Get the section - ensure we have a dict
        vigil_amp_config = config_manager.get_section("vigil_amplification")
        logger.debug(f"Raw vigil_amplification section: {vigil_amp_config}")

        if vigil_amp_config is None:
            logger.debug("vigil_amplification section is None, using defaults")
            return vigil_config

        if not isinstance(vigil_amp_config, dict):
            logger.warning(f"vigil_amplification is not a dict: {type(vigil_amp_config)}")
            return vigil_config

        if not vigil_amp_config:
            logger.debug("No vigil_amplification section found (empty), using defaults")
            return vigil_config

        # Load top-level settings from resolved config
        if "enabled" in vigil_amp_config:
            val = vigil_amp_config.get("enabled")
            if val is not None:
                vigil_config["enabled"] = bool(val)

        if "score_cap" in vigil_amp_config:
            val = vigil_amp_config.get("score_cap")
            if val is not None:
                vigil_config["score_cap"] = float(val)

        if "skip_threshold" in vigil_amp_config:
            val = vigil_amp_config.get("skip_threshold")
            if val is not None:
                vigil_config["skip_threshold"] = float(val)

        if "amplify_medium" in vigil_amp_config:
            val = vigil_amp_config.get("amplify_medium")
            if val is not None:
                vigil_config["amplify_medium"] = bool(val)

        # Load confidence_skip config - ConfigManager resolves env var overrides
        confidence_skip = vigil_amp_config.get("confidence_skip")
        logger.debug(f"confidence_skip from config: {confidence_skip}")
        if confidence_skip is not None and isinstance(confidence_skip, dict):
            vigil_config["confidence_skip"] = {
                "enabled": bool(confidence_skip.get("enabled", True)),
                "crisis_threshold": float(confidence_skip.get("crisis_threshold") or 0.85),
                "safe_threshold": float(confidence_skip.get("safe_threshold") or 0.90),
            }

        # Load nested thresholds - ConfigManager resolves these with env var overrides
        thresholds = vigil_amp_config.get("vigil_thresholds")
        logger.debug(f"vigil_thresholds from config: {thresholds}")
        if thresholds is not None and isinstance(thresholds, dict):
            vigil_config["vigil_thresholds"] = {
                "critical": float(thresholds.get("critical") or 0.8),
                "high": float(thresholds.get("high") or 0.6),
                "moderate": float(thresholds.get("moderate") or 0.4),
            }

        # Load nested boosts - ConfigManager resolves these with env var overrides
        boosts = vigil_amp_config.get("boosts")
        logger.debug(f"boosts from config: {boosts}")
        if boosts is not None and isinstance(boosts, dict):
            vigil_config["boosts"] = {
                "critical_boost": float(boosts.get("critical_boost") or 0.35),
                "critical_minimum": float(boosts.get("critical_minimum") or 0.55),
                "high_multiplier": float(boosts.get("high_multiplier") or 0.3),
                "moderate_multiplier": float(boosts.get("moderate_multiplier") or 0.1),
            }

        logger.info(
            f"✅ Loaded Vigil amplification config: "
            f"skip_threshold={vigil_config['skip_threshold']}, "
            f"amplify_medium={vigil_config['amplify_medium']}, "
            f"confidence_skip={vigil_config['confidence_skip']}"
        )

    except Exception as e:
        import traceback
        import sys
        error_tb = traceback.format_exc()
        logger.warning(f"Error loading Vigil config, using defaults: {e}")
        # Force print to stderr to ensure we see it
        print(f"VIGIL CONFIG ERROR TRACEBACK:\n{error_tb}", file=sys.stderr, flush=True)

    return vigil_config


# =============================================================================
# Phase 3 Vigil: Amplification Logic
# =============================================================================


async def apply_vigil_amplification(
    base_score: float,
    base_severity: CrisisSeverity,
    text: str,
    config: Dict[str, Any],
    vigil_client: Optional[VigilClient],
    bart_signal: Optional[ModelSignal] = None,
) -> Tuple[float, VigilResponse, bool, bool, bool]:
    """
    Apply Ash-Vigil risk amplification to base ensemble score.

    Vigil acts as a SOFT amplifier:
    - Only called when base score is below skip_threshold
    - Skipped when BART is highly confident (crisis or safe)
    - Boosts scores when Vigil detects risk that base models missed
    - Respects amplify_medium toggle for MEDIUM severity
    - Hard caps at score_cap (1.0)
    - Does NOT apply irony dampening (that comes after)

    Args:
        base_score: Pre-irony-dampening ensemble score
        base_severity: Preliminary severity from base score
        text: Original message text
        config: Vigil amplification config dictionary
        vigil_client: Vigil client instance (may be None)
        bart_signal: BART model signal for confidence-based skip (optional)

    Returns:
        Tuple of (amplified_score, VigilResponse, was_called: bool, was_amplified: bool,
                  was_confidence_skip: bool)
        was_called, was_amplified, and was_confidence_skip are for stats tracking
        by the caller.
    """
    was_called = False
    was_amplified = False
    was_confidence_skip = False

    # =========================================================================
    # Gate 1: Is amplification enabled?
    # =========================================================================
    if not config["enabled"]:
        logger.debug("Vigil amplification disabled in config")
        return base_score, VigilResponse(
            status=VigilStatus.DISABLED,
            base_score=base_score,
        ), was_called, was_amplified, was_confidence_skip

    # =========================================================================
    # Gate 2: Is base score already above skip threshold?
    # =========================================================================
    if base_score >= config["skip_threshold"]:
        logger.debug(
            f"Skipping Vigil: base score {base_score:.3f} >= "
            f"skip threshold {config['skip_threshold']}"
        )
        return base_score, VigilResponse(
            status=VigilStatus.SKIPPED,
            base_score=base_score,
        ), was_called, was_amplified, was_confidence_skip

    # =========================================================================
    # Gate 3: BART confidence-based skip (Phase 6.4)
    # =========================================================================
    cs_config = config["confidence_skip"]
    if cs_config["enabled"] and bart_signal is not None:
        crisis_signal = bart_signal.crisis_signal
        crisis_threshold = cs_config["crisis_threshold"]
        safe_threshold = cs_config["safe_threshold"]

        # Confident crisis: BART crisis_signal is very high
        if crisis_signal >= crisis_threshold:
            was_confidence_skip = True
            logger.debug(
                f"Skipping Vigil: BART confident crisis "
                f"(crisis_signal={crisis_signal:.3f} >= {crisis_threshold}, "
                f"label={bart_signal.label})"
            )
            return base_score, VigilResponse(
                status=VigilStatus.SKIPPED,
                base_score=base_score,
            ), was_called, was_amplified, was_confidence_skip

        # Confident safe: BART crisis_signal is very low
        safe_cutoff = 1.0 - safe_threshold
        if crisis_signal <= safe_cutoff:
            was_confidence_skip = True
            logger.debug(
                f"Skipping Vigil: BART confident safe "
                f"(crisis_signal={crisis_signal:.3f} <= {safe_cutoff:.3f}, "
                f"label={bart_signal.label})"
            )

            return base_score, VigilResponse(
                status=VigilStatus.SKIPPED,
                base_score=base_score,
            ), was_called, was_amplified, was_confidence_skip

    # =========================================================================
    # Gate 4: Is this MEDIUM severity and amplify_medium is disabled?
    # =========================================================================
    if base_severity == CrisisSeverity.MEDIUM and not config["amplify_medium"]:
        logger.debug("Skipping Vigil: MEDIUM severity and amplify_medium=false")
        return base_score, VigilResponse(
            status=VigilStatus.SKIPPED,
            base_score=base_score,
        ), was_called, was_amplified, was_confidence_skip

    # =========================================================================
    # Gate 5: Is Vigil client available?
    # =========================================================================
    if not vigil_client or not vigil_client.enabled:
        logger.debug("Vigil client not available or disabled")
        return base_score, VigilResponse(
            status=VigilStatus.DISABLED,
            base_score=base_score,
        ), was_called, was_amplified, was_confidence_skip

    # =========================================================================
    # Call Vigil
    # =========================================================================
    was_called = True
    vigil_result = await vigil_client.analyze(text)

    if vigil_result is None:
        # Vigil unavailable - return base score with appropriate status
        status = vigil_client.status
        logger.warning(f"Vigil call failed: {status.value}")
        return base_score, VigilResponse(
            status=status,
            base_score=base_score,
        ), was_called, was_amplified, was_confidence_skip

    # =========================================================================
    # Apply amplification based on Vigil risk level
    # =========================================================================
    risk_signal = vigil_result.risk_score
    risk_label = vigil_result.risk_label
    thresholds = config["vigil_thresholds"]
    boosts = config["boosts"]

    amplification_applied = False

    if risk_signal >= thresholds["critical"]:
        # Critical risk Vigil caught that base models missed
        amplified = max(
            base_score + boosts["critical_boost"], boosts["critical_minimum"]
        )
        amplification_applied = True
        was_amplified = True
        logger.info(
            f"🚨 Vigil CRITICAL amplification: {base_score:.3f} → {amplified:.3f} "
            f"(vigil_risk={risk_signal:.3f}, label={risk_label})"
        )

    elif risk_signal >= thresholds["high"]:
        # Significant risk, boost with multiplier
        boost = risk_signal * boosts["high_multiplier"]
        amplified = base_score + boost
        amplification_applied = True
        was_amplified = True
        logger.info(
            f"⚠️ Vigil HIGH amplification: {base_score:.3f} → {amplified:.3f} "
            f"(vigil_risk={risk_signal:.3f}, boost={boost:.3f})"
        )

    elif risk_signal >= thresholds["moderate"]:
        # Modest risk signal
        boost = risk_signal * boosts["moderate_multiplier"]
        amplified = base_score + boost
        if boost > 0.01:  # Only count meaningful amplifications
            amplification_applied = True
            was_amplified = True
        logger.debug(
            f"ℹ️ Vigil MODERATE amplification: {base_score:.3f} → {amplified:.3f} "
            f"(vigil_risk={risk_signal:.3f}, boost={boost:.3f})"
        )

    else:
        # Vigil didn't detect significant risk
        amplified = base_score
        logger.debug(
            f"Vigil detected low risk ({risk_signal:.3f}), no amplification"
        )

    # =========================================================================
    # HARD CAP - Never exceed score_cap
    # =========================================================================
    if amplified > config["score_cap"]:
        logger.debug(f"Applying hard cap: {amplified:.3f} → {config['score_cap']}")
        amplified = config["score_cap"]

    return amplified, VigilResponse(
        status=VigilStatus.USED,
        risk_score=risk_signal,
        risk_label=risk_label,
        amplification_applied=amplification_applied,
        base_score=base_score,
        amplified_score=amplified,
    ), was_called, was_amplified, was_confidence_skip


def apply_vigil_amplification_sync(
    base_score: float,
    base_severity: CrisisSeverity,
    text: str,
    config: Dict[str, Any],
    vigil_client: Optional[VigilClient],
    bart_signal: Optional[ModelSignal] = None,
) -> Tuple[float, VigilResponse, bool, bool, bool]:
    """
    Synchronous wrapper for Vigil amplification.

    Used by the sync analyze() method.

    Args:
        base_score: Pre-irony-dampening ensemble score
        base_severity: Preliminary severity from base score
        text: Original message text
        config: Vigil amplification config dictionary
        vigil_client: Vigil client instance (may be None)
        bart_signal: BART model signal for confidence-based skip (optional)

    Returns:
        Tuple of (amplified_score, VigilResponse, was_called, was_amplified, was_confidence_skip)
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(
                    asyncio.run,
                    apply_vigil_amplification(
                        base_score, base_severity, text, config,
                        vigil_client, bart_signal,
                    ),
                )
                return future.result(timeout=2.0)
        else:
            return loop.run_until_complete(
                apply_vigil_amplification(
                    base_score, base_severity, text, config,
                    vigil_client, bart_signal,
                )
            )
    except Exception as e:
        logger.warning(f"Sync Vigil amplification failed: {e}")
        return base_score, VigilResponse(
            status=VigilStatus.UNAVAILABLE,
            base_score=base_score,
        ), False, False, False


# =============================================================================
# Review Determination
# =============================================================================


def determine_requires_review(
    final_severity: CrisisSeverity,
    vigil_response: VigilResponse,
) -> bool:
    """
    Determine if CRT review is required.

    Rules:
    - HIGH or CRITICAL severity → always requires review
    - Vigil unavailable/timeout/circuit_open → requires review (safety net)

    Args:
        final_severity: Final severity after all processing
        vigil_response: Vigil response with status

    Returns:
        True if CRT review is recommended
    """
    # HIGH and CRITICAL always need review
    if final_severity in (CrisisSeverity.HIGH, CrisisSeverity.CRITICAL):
        return True

    # If Vigil was supposed to run but couldn't, flag for review
    if vigil_response.status in (
        VigilStatus.UNAVAILABLE,
        VigilStatus.TIMEOUT,
        VigilStatus.CIRCUIT_OPEN,
    ):
        return True

    return False


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "DEFAULT_VIGIL_AMPLIFICATION",
    "load_vigil_config",
    "apply_vigil_amplification",
    "apply_vigil_amplification_sync",
    "determine_requires_review",
]
