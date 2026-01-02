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
Explainability Layer for Ash-NLP Ensemble Service
---
FILE VERSION: v5.0-4-4.1-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 Step 4 - Explainability Layer
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Generate human-readable explanations for crisis decisions
- Support verbosity levels: minimal, standard, detailed
- Include: decision_summary, model_contributions, key_factors, recommended_action
- Provide templates for consistent explanation formatting
- Enable moderators to quickly understand crisis assessments

DESIGN PHILOSOPHY:
Explanations should:
- Be immediately understandable by non-technical moderators
- Highlight the most important factors in the decision
- Provide actionable recommendations
- Support different verbosity levels for different contexts
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .aggregator import (
    AggregatedResult,
    CrisisLevel,
    InterventionPriority,
    ModelResultSummary,
)
from .consensus import AgreementLevel
from .conflict_detector import ConflictReport, ConflictSeverity

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-4-4.1-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Verbosity Levels
# =============================================================================


class VerbosityLevel(Enum):
    """Verbosity levels for explanations."""

    MINIMAL = "minimal"  # Just crisis level and score
    STANDARD = "standard"  # Summary + key factors + recommendation
    DETAILED = "detailed"  # Full breakdown with all model contributions


# =============================================================================
# Explanation Data Classes
# =============================================================================


@dataclass
class ModelContribution:
    """Explanation of a single model's contribution."""

    model_name: str
    display_name: str
    description: str
    confidence: float
    detected_labels: List[str] = field(default_factory=list)
    impact: str = ""  # "high", "medium", "low"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "model_name": self.model_name,
            "display_name": self.display_name,
            "description": self.description,
            "confidence": round(self.confidence, 2),
            "detected_labels": self.detected_labels,
            "impact": self.impact,
        }


@dataclass
class RecommendedAction:
    """Recommended action based on assessment."""

    priority: str
    action: str
    escalation: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "priority": self.priority,
            "action": self.action,
            "escalation": self.escalation,
            "rationale": self.rationale,
        }


@dataclass
class Explanation:
    """
    Complete explanation for a crisis assessment.

    Attributes:
        verbosity: Verbosity level used
        decision_summary: Plain-English summary of the decision
        confidence_summary: Explanation of confidence level
        model_contributions: Per-model contribution explanations
        key_factors: Primary factors driving the classification
        recommended_action: Suggested intervention
        conflict_summary: Summary of any model conflicts
        plain_text: Full plain-text explanation
    """

    verbosity: VerbosityLevel
    decision_summary: str
    confidence_summary: str = ""
    model_contributions: List[ModelContribution] = field(default_factory=list)
    key_factors: List[str] = field(default_factory=list)
    recommended_action: Optional[RecommendedAction] = None
    conflict_summary: str = ""
    plain_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "verbosity": self.verbosity.value,
            "decision_summary": self.decision_summary,
        }

        if self.verbosity in (VerbosityLevel.STANDARD, VerbosityLevel.DETAILED):
            result["key_factors"] = self.key_factors
            if self.recommended_action:
                result["recommended_action"] = self.recommended_action.to_dict()

        if self.verbosity == VerbosityLevel.DETAILED:
            result["confidence_summary"] = self.confidence_summary
            result["model_contributions"] = [
                mc.to_dict() for mc in self.model_contributions
            ]
            if self.conflict_summary:
                result["conflict_summary"] = self.conflict_summary

        result["plain_text"] = self.plain_text

        return result


# =============================================================================
# Explainability Generator
# =============================================================================


class ExplainabilityGenerator:
    """
    Explainability Generator for Crisis Assessments.

    Creates human-readable explanations for crisis decisions,
    supporting multiple verbosity levels.

    Verbosity Levels:
    - MINIMAL: Crisis level and score only
    - STANDARD: Summary + key factors + recommendation
    - DETAILED: Full model breakdown + confidence analysis

    Clean Architecture v5.1 Compliance:
    - Factory function: create_explainability_generator()
    - Configuration via ConfigManager
    """

    # Display names for models
    MODEL_DISPLAY_NAMES = {
        "bart": "Crisis Classifier",
        "sentiment": "Sentiment Analyzer",
        "irony": "Irony Detector",
        "emotions": "Emotion Detector",
    }

    # Crisis level descriptions
    CRISIS_LEVEL_DESCRIPTIONS = {
        CrisisLevel.CRITICAL: "CRITICAL",
        CrisisLevel.HIGH: "HIGH CONCERN",
        CrisisLevel.MEDIUM: "MODERATE CONCERN",
        CrisisLevel.LOW: "LOW CONCERN",
        CrisisLevel.SAFE: "NO CONCERN",
    }

    def __init__(
        self,
        default_verbosity: VerbosityLevel = VerbosityLevel.STANDARD,
        include_model_details: bool = True,
        include_recommendations: bool = True,
    ):
        """
        Initialize ExplainabilityGenerator.

        Args:
            default_verbosity: Default verbosity level
            include_model_details: Include per-model details
            include_recommendations: Include action recommendations
        """
        self.default_verbosity = default_verbosity
        self.include_model_details = include_model_details
        self.include_recommendations = include_recommendations

        logger.info(
            f"📝 ExplainabilityGenerator initialized "
            f"(verbosity: {default_verbosity.value})"
        )

    def generate(
        self,
        result: AggregatedResult,
        verbosity: Optional[VerbosityLevel] = None,
    ) -> Explanation:
        """
        Generate explanation for an aggregated result.

        Args:
            result: AggregatedResult from ResultAggregator
            verbosity: Override verbosity level

        Returns:
            Explanation with human-readable content
        """
        active_verbosity = verbosity or self.default_verbosity

        # Generate decision summary
        decision_summary = self._generate_decision_summary(result)

        # Initialize explanation
        explanation = Explanation(
            verbosity=active_verbosity,
            decision_summary=decision_summary,
        )

        # Add components based on verbosity
        if active_verbosity in (VerbosityLevel.STANDARD, VerbosityLevel.DETAILED):
            # Key factors
            explanation.key_factors = self._identify_key_factors(result)

            # Recommended action
            if self.include_recommendations:
                explanation.recommended_action = self._generate_recommendation(result)

        if active_verbosity == VerbosityLevel.DETAILED:
            # Confidence summary
            explanation.confidence_summary = self._generate_confidence_summary(result)

            # Model contributions
            if self.include_model_details:
                explanation.model_contributions = self._generate_model_contributions(
                    result
                )

            # Conflict summary
            if result.conflict_report and result.conflict_report.has_conflicts:
                explanation.conflict_summary = self._generate_conflict_summary(
                    result.conflict_report
                )

        # Generate full plain text
        explanation.plain_text = self._generate_plain_text(explanation, result)

        return explanation

    # =========================================================================
    # Decision Summary Generation
    # =========================================================================

    def _generate_decision_summary(self, result: AggregatedResult) -> str:
        """Generate plain-English decision summary."""
        level_desc = self.CRISIS_LEVEL_DESCRIPTIONS.get(
            result.crisis_level, "UNKNOWN"
        )
        confidence_pct = int(result.confidence * 100)

        if result.crisis_level == CrisisLevel.CRITICAL:
            return (
                f"{level_desc}: Significant crisis indicators detected "
                f"with {confidence_pct}% confidence. Immediate attention required."
            )
        elif result.crisis_level == CrisisLevel.HIGH:
            return (
                f"{level_desc}: Crisis indicators detected "
                f"with {confidence_pct}% confidence. Priority response recommended."
            )
        elif result.crisis_level == CrisisLevel.MEDIUM:
            return (
                f"{level_desc}: Some crisis indicators present "
                f"with {confidence_pct}% confidence. Monitoring recommended."
            )
        elif result.crisis_level == CrisisLevel.LOW:
            return (
                f"{level_desc}: Minor indicators detected "
                f"with {confidence_pct}% confidence. Passive monitoring suggested."
            )
        else:  # SAFE
            return (
                f"{level_desc}: No significant crisis indicators detected. "
                f"Message appears safe ({confidence_pct}% confidence)."
            )

    # =========================================================================
    # Key Factors Identification
    # =========================================================================

    def _identify_key_factors(self, result: AggregatedResult) -> List[str]:
        """Identify key factors driving the classification."""
        factors = []

        for model_name, model_result in result.model_results.items():
            if model_result.crisis_signal < 0.3:
                continue  # Skip low-signal models

            # Add primary label if significant
            if model_result.label and model_result.crisis_signal > 0.5:
                # Clean up label for display
                label = model_result.label.replace("_", " ").lower()
                if label not in factors:
                    factors.append(label)

            # Add top labels with high scores
            for label_info in model_result.top_labels[:2]:
                if label_info.get("score", 0) > 0.5:
                    label = label_info.get("label", "").replace("_", " ").lower()
                    if label and label not in factors:
                        factors.append(label)

        # Add sentiment info if negative
        if "sentiment" in result.model_results:
            sentiment = result.model_results["sentiment"]
            if sentiment.crisis_signal > 0.6:
                if "negative sentiment" not in factors:
                    factors.append("negative sentiment")

        return factors[:6]  # Limit to 6 factors

    # =========================================================================
    # Recommendation Generation
    # =========================================================================

    def _generate_recommendation(self, result: AggregatedResult) -> RecommendedAction:
        """Generate action recommendation based on assessment."""
        priority = result.intervention_priority.value.upper()

        # Generate action based on crisis level
        if result.crisis_level == CrisisLevel.CRITICAL:
            action = "Immediate outreach to community member"
            escalation = "Alert senior moderators immediately"
            rationale = "Critical crisis indicators require immediate human intervention"

        elif result.crisis_level == CrisisLevel.HIGH:
            action = "Check user history and consider direct outreach"
            escalation = "Moderator review recommended"
            rationale = "High-severity indicators warrant prompt attention"

        elif result.crisis_level == CrisisLevel.MEDIUM:
            action = "Monitor user activity and be prepared to engage"
            escalation = "Flag for follow-up if pattern continues"
            rationale = "Moderate indicators suggest watching for escalation"

        elif result.crisis_level == CrisisLevel.LOW:
            action = "Note and continue passive monitoring"
            escalation = "No immediate escalation needed"
            rationale = "Minor indicators do not require active intervention"

        else:  # SAFE
            action = "No action required"
            escalation = "None"
            rationale = "No concerning indicators detected"

        # Adjust if review is required due to conflict
        if result.resolution and result.resolution.requires_review:
            escalation = "Human review recommended due to model disagreement"

        return RecommendedAction(
            priority=priority,
            action=action,
            escalation=escalation,
            rationale=rationale,
        )

    # =========================================================================
    # Confidence Summary
    # =========================================================================

    def _generate_confidence_summary(self, result: AggregatedResult) -> str:
        """Generate explanation of confidence level."""
        confidence_pct = int(result.confidence * 100)

        # Get agreement level from consensus
        agreement = None
        if result.consensus:
            agreement = result.consensus.agreement_level

        if confidence_pct >= 85:
            agreement_text = "strong agreement"
        elif confidence_pct >= 70:
            agreement_text = "good agreement"
        elif confidence_pct >= 50:
            agreement_text = "moderate agreement"
        else:
            agreement_text = "limited agreement"

        # Check for conflicts
        conflict_note = ""
        if result.conflict_report and result.conflict_report.has_conflicts:
            conflict_note = (
                f" Note: {result.conflict_report.conflict_count} model "
                f"conflict(s) detected which may affect reliability."
            )

        return (
            f"Assessment confidence is {confidence_pct}% based on {agreement_text} "
            f"between {len(result.models_used)} models.{conflict_note}"
        )

    # =========================================================================
    # Model Contributions
    # =========================================================================

    def _generate_model_contributions(
        self, result: AggregatedResult
    ) -> List[ModelContribution]:
        """Generate explanation of each model's contribution."""
        contributions = []

        for model_name, model_result in result.model_results.items():
            display_name = self.MODEL_DISPLAY_NAMES.get(model_name, model_name)

            # Determine impact level
            if model_result.crisis_signal > 0.7:
                impact = "high"
            elif model_result.crisis_signal > 0.4:
                impact = "medium"
            else:
                impact = "low"

            # Build description
            description = self._build_model_description(model_name, model_result)

            # Extract detected labels
            detected_labels = [model_result.label] if model_result.label else []
            for label_info in model_result.top_labels[:3]:
                label = label_info.get("label", "")
                if label and label not in detected_labels:
                    detected_labels.append(label)

            contributions.append(
                ModelContribution(
                    model_name=model_name,
                    display_name=display_name,
                    description=description,
                    confidence=model_result.confidence,
                    detected_labels=detected_labels,
                    impact=impact,
                )
            )

        # Sort by impact (high first)
        impact_order = {"high": 0, "medium": 1, "low": 2}
        contributions.sort(key=lambda c: impact_order.get(c.impact, 3))

        return contributions

    def _build_model_description(
        self, model_name: str, model_result: ModelResultSummary
    ) -> str:
        """Build description for a model's contribution."""
        confidence_pct = int(model_result.confidence * 100)

        if model_name == "bart":
            if model_result.crisis_signal > 0.5:
                return (
                    f"Detected \"{model_result.label}\" ({confidence_pct}%)"
                )
            else:
                return f"No significant crisis labels detected ({confidence_pct}%)"

        elif model_name == "sentiment":
            if model_result.crisis_signal > 0.6:
                return f"Highly negative sentiment detected ({confidence_pct}%)"
            elif model_result.crisis_signal > 0.3:
                return f"Moderately negative sentiment ({confidence_pct}%)"
            else:
                return f"Neutral or positive sentiment ({confidence_pct}%)"

        elif model_name == "irony":
            # Irony score is inverted (high = no irony)
            irony_detected = model_result.crisis_signal < 0.5
            if irony_detected:
                return "Sarcasm/irony detected - may be masking true feelings"
            else:
                return "No sarcasm detected - message appears sincere"

        elif model_name == "emotions":
            # Get top emotions from labels
            top_emotions = model_result.detected_labels[:3] if hasattr(model_result, 'detected_labels') else []
            if not top_emotions and model_result.top_labels:
                top_emotions = [l.get("label", "") for l in model_result.top_labels[:3]]

            if model_result.crisis_signal > 0.5 and top_emotions:
                emotions_str = ", ".join(top_emotions[:3])
                return f"Crisis emotions detected: {emotions_str}"
            else:
                return "No significant crisis emotions detected"

        return f"{model_name}: {model_result.label} ({confidence_pct}%)"

    # =========================================================================
    # Conflict Summary
    # =========================================================================

    def _generate_conflict_summary(self, conflict_report: ConflictReport) -> str:
        """Generate summary of model conflicts."""
        if not conflict_report.has_conflicts:
            return ""

        conflict_types = [c.conflict_type.value for c in conflict_report.conflicts]
        severity = conflict_report.highest_severity

        severity_text = {
            ConflictSeverity.HIGH: "significant",
            ConflictSeverity.MEDIUM: "moderate",
            ConflictSeverity.LOW: "minor",
        }.get(severity, "")

        return (
            f"Models showed {severity_text} disagreement "
            f"({', '.join(conflict_types)}). "
            f"Human review may be beneficial to verify assessment."
        )

    # =========================================================================
    # Plain Text Generation
    # =========================================================================

    def _generate_plain_text(
        self, explanation: Explanation, result: AggregatedResult
    ) -> str:
        """Generate full plain-text explanation."""
        lines = []

        # Decision summary (always included)
        lines.append("DECISION SUMMARY:")
        lines.append(explanation.decision_summary)
        lines.append("")

        # Standard and detailed
        if explanation.verbosity in (VerbosityLevel.STANDARD, VerbosityLevel.DETAILED):
            # Key factors
            if explanation.key_factors:
                lines.append("KEY FACTORS:")
                for factor in explanation.key_factors:
                    lines.append(f"• {factor}")
                lines.append("")

            # Recommendation
            if explanation.recommended_action:
                rec = explanation.recommended_action
                lines.append("RECOMMENDED ACTION:")
                lines.append(f"Priority: {rec.priority}")
                lines.append(f"Action: {rec.action}")
                lines.append(f"Escalation: {rec.escalation}")
                lines.append("")

        # Detailed only
        if explanation.verbosity == VerbosityLevel.DETAILED:
            # Model contributions
            if explanation.model_contributions:
                lines.append("MODEL CONTRIBUTIONS:")
                for mc in explanation.model_contributions:
                    lines.append(f"• {mc.display_name}: {mc.description}")
                lines.append("")

            # Confidence
            if explanation.confidence_summary:
                lines.append("CONFIDENCE:")
                lines.append(explanation.confidence_summary)
                lines.append("")

            # Conflicts
            if explanation.conflict_summary:
                lines.append("CONFLICTS:")
                lines.append(explanation.conflict_summary)
                lines.append("")

        return "\n".join(lines).strip()

    # =========================================================================
    # Configuration Methods
    # =========================================================================

    def set_verbosity(self, verbosity: VerbosityLevel) -> None:
        """Set default verbosity level."""
        self.default_verbosity = verbosity
        logger.info(f"Verbosity set to: {verbosity.value}")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "default_verbosity": self.default_verbosity.value,
            "include_model_details": self.include_model_details,
            "include_recommendations": self.include_recommendations,
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_explainability_generator(
    config_manager: Optional["ConfigManager"] = None,
    default_verbosity: Optional[str] = None,
) -> ExplainabilityGenerator:
    """
    Factory function for ExplainabilityGenerator.

    Creates a configured explainability generator.

    Args:
        config_manager: Configuration manager instance
        default_verbosity: Override verbosity level name

    Returns:
        Configured ExplainabilityGenerator instance

    Example:
        >>> generator = create_explainability_generator(config_manager=config)
        >>> explanation = generator.generate(aggregated_result)
    """
    # Default values
    final_verbosity = VerbosityLevel.STANDARD
    include_details = True
    include_recommendations = True

    # Load from config manager
    if config_manager is not None:
        explain_config = config_manager.get_explainability_config()
        if explain_config:
            verbosity_name = explain_config.get("verbosity")
            if verbosity_name:
                try:
                    final_verbosity = VerbosityLevel(verbosity_name)
                except ValueError:
                    logger.warning(
                        f"Invalid verbosity '{verbosity_name}', using standard"
                    )

            include_details = explain_config.get("include_model_details", include_details)
            include_recommendations = explain_config.get(
                "include_recommendations", include_recommendations
            )

    # Apply explicit override
    if default_verbosity:
        try:
            final_verbosity = VerbosityLevel(default_verbosity)
        except ValueError:
            logger.warning(
                f"Invalid verbosity '{default_verbosity}', using standard"
            )

    return ExplainabilityGenerator(
        default_verbosity=final_verbosity,
        include_model_details=include_details,
        include_recommendations=include_recommendations,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "VerbosityLevel",
    # Data classes
    "ModelContribution",
    "RecommendedAction",
    "Explanation",
    # Generator class
    "ExplainabilityGenerator",
    "create_explainability_generator",
]
