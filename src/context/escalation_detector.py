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
Escalation Detector for Ash-NLP Service - Phase 5
---
FILE VERSION: v5.0-5-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Detect escalation patterns across message score sequences
- Classify escalation rate (rapid, gradual, sudden, none)
- Calculate escalation confidence scores
- Identify intervention points in the sequence
- Match against known escalation patterns
"""

import logging
from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from src.managers import (
    ContextConfigManager,
    EscalationDetectionConfig,
    KnownPattern,
)

# Module version
__version__ = "v5.0-5-1.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class EscalationType(Enum):
    """Classification of escalation rate."""
    NONE = "none"
    GRADUAL = "gradual"
    RAPID = "rapid"
    SUDDEN = "sudden"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EscalationAnalysis:
    """
    Result of escalation detection analysis.
    
    Attributes:
        detected: Whether escalation was detected
        escalation_type: Classification of escalation rate
        confidence: Confidence score for the detection (0.0-1.0)
        score_delta: Total change in crisis score (end - start)
        time_span_hours: Time span of the message sequence
        intervention_point: Index where intervention should have occurred
        matched_pattern: Name of matched known pattern (if any)
        pattern_confidence: Confidence of pattern match (0.0-1.0)
        scores: List of crisis scores in sequence
        rate_per_hour: Score change rate per hour
    """
    detected: bool = False
    escalation_type: EscalationType = EscalationType.NONE
    confidence: float = 0.0
    score_delta: float = 0.0
    time_span_hours: float = 0.0
    intervention_point: Optional[int] = None
    matched_pattern: Optional[str] = None
    pattern_confidence: float = 0.0
    scores: List[float] = field(default_factory=list)
    rate_per_hour: float = 0.0


# =============================================================================
# Escalation Detector
# =============================================================================

class EscalationDetector:
    """
    Detects escalation patterns in crisis score sequences.
    
    Analyzes message history to identify:
    - Whether crisis scores are escalating
    - The rate of escalation (rapid, gradual, sudden)
    - Where intervention should have occurred
    - Matches to known escalation patterns
    
    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_escalation_detector)
    - Configuration via ContextConfigManager
    - Resilient analysis with safe defaults
    """
    
    def __init__(self, context_config_manager: ContextConfigManager):
        """
        Initialize EscalationDetector.
        
        Args:
            context_config_manager: Context configuration manager
            
        Note:
            Use create_escalation_detector() factory function instead.
        """
        self._config_manager = context_config_manager
        self._config = context_config_manager.get_escalation_detection_config()
        self._known_patterns = context_config_manager.get_known_patterns()
        
        logger.debug(
            f"EscalationDetector initialized "
            f"(rapid_threshold={self._config.rapid_threshold_hours}h, "
            f"score_threshold={self._config.score_increase_threshold})"
        )
    
    def analyze(
        self,
        scores: List[float],
        timestamps: List[datetime],
    ) -> EscalationAnalysis:
        """
        Analyze a sequence of crisis scores for escalation patterns.
        
        Args:
            scores: List of crisis scores (0.0-1.0) in chronological order
            timestamps: List of timestamps corresponding to each score
            
        Returns:
            EscalationAnalysis with detection results
        """
        # Validate inputs
        if not self._config.enabled:
            logger.debug("Escalation detection disabled")
            return EscalationAnalysis(scores=scores)
        
        if len(scores) < self._config.minimum_messages:
            logger.debug(
                f"Insufficient messages for escalation analysis: "
                f"{len(scores)} < {self._config.minimum_messages}"
            )
            return EscalationAnalysis(scores=scores)
        
        if len(scores) != len(timestamps):
            logger.warning("Score and timestamp lists must be same length")
            return EscalationAnalysis(scores=scores)
        
        # Calculate basic metrics
        time_span = self._calculate_time_span(timestamps)
        score_delta = scores[-1] - scores[0]
        rate_per_hour = self._calculate_rate_per_hour(score_delta, time_span)
        
        # Detect escalation
        detected, escalation_type, confidence = self._detect_escalation(
            scores=scores,
            time_span_hours=time_span,
            score_delta=score_delta,
        )
        
        # Find intervention point
        intervention_point = self._find_intervention_point(scores)
        
        # Match against known patterns
        matched_pattern, pattern_confidence = self._match_pattern(
            escalation_type=escalation_type,
            time_span_hours=time_span,
            score_delta=score_delta,
        )
        
        return EscalationAnalysis(
            detected=detected,
            escalation_type=escalation_type,
            confidence=confidence,
            score_delta=score_delta,
            time_span_hours=time_span,
            intervention_point=intervention_point,
            matched_pattern=matched_pattern,
            pattern_confidence=pattern_confidence,
            scores=scores,
            rate_per_hour=rate_per_hour,
        )
    
    def _calculate_time_span(self, timestamps: List[datetime]) -> float:
        """
        Calculate time span in hours between first and last timestamp.
        
        Args:
            timestamps: List of timestamps
            
        Returns:
            Time span in hours (minimum 0.0167 = 1 minute)
        """
        if len(timestamps) < 2:
            return 0.0
        
        delta = timestamps[-1] - timestamps[0]
        hours = delta.total_seconds() / 3600.0
        
        # Minimum 1 minute to avoid division by zero
        return max(hours, 0.0167)
    
    def _calculate_rate_per_hour(
        self, 
        score_delta: float, 
        time_span_hours: float
    ) -> float:
        """
        Calculate score change rate per hour.
        
        Args:
            score_delta: Total score change
            time_span_hours: Time span in hours
            
        Returns:
            Rate of change per hour
        """
        if time_span_hours <= 0:
            return 0.0
        return score_delta / time_span_hours
    
    def _detect_escalation(
        self,
        scores: List[float],
        time_span_hours: float,
        score_delta: float,
    ) -> Tuple[bool, EscalationType, float]:
        """
        Detect if escalation occurred and classify its type.
        
        Args:
            scores: List of crisis scores
            time_span_hours: Time span in hours
            score_delta: Total score change
            
        Returns:
            Tuple of (detected, escalation_type, confidence)
        """
        # Check if score increased enough to be escalation
        if score_delta < self._config.score_increase_threshold:
            return False, EscalationType.NONE, 0.0
        
        # Check for consistent upward trend
        if not self._is_upward_trend(scores):
            return False, EscalationType.NONE, 0.0
        
        # Classify escalation type based on time span
        escalation_type = self._classify_escalation_type(time_span_hours)
        
        # Calculate confidence based on multiple factors
        confidence = self._calculate_confidence(
            scores=scores,
            score_delta=score_delta,
            time_span_hours=time_span_hours,
            escalation_type=escalation_type,
        )
        
        return True, escalation_type, confidence
    
    def _is_upward_trend(self, scores: List[float]) -> bool:
        """
        Check if scores show a predominantly upward trend.
        
        Allows for minor fluctuations but requires overall increase.
        
        Args:
            scores: List of crisis scores
            
        Returns:
            True if upward trend detected
        """
        if len(scores) < 2:
            return False
        
        # Count increasing vs decreasing transitions
        increases = 0
        decreases = 0
        
        for i in range(1, len(scores)):
            delta = scores[i] - scores[i-1]
            if delta > 0.01:  # Small tolerance for noise
                increases += 1
            elif delta < -0.01:
                decreases += 1
        
        # Need more increases than decreases
        # and final score higher than initial
        return increases > decreases and scores[-1] > scores[0]
    
    def _classify_escalation_type(self, time_span_hours: float) -> EscalationType:
        """
        Classify escalation type based on time span.
        
        Args:
            time_span_hours: Time span in hours
            
        Returns:
            EscalationType classification
        """
        if time_span_hours <= 1:
            return EscalationType.SUDDEN
        elif time_span_hours <= self._config.rapid_threshold_hours:
            return EscalationType.RAPID
        elif time_span_hours <= self._config.gradual_threshold_hours:
            return EscalationType.GRADUAL
        else:
            # Very slow escalation over long period
            return EscalationType.GRADUAL
    
    def _calculate_confidence(
        self,
        scores: List[float],
        score_delta: float,
        time_span_hours: float,
        escalation_type: EscalationType,
    ) -> float:
        """
        Calculate confidence score for escalation detection.
        
        Factors:
        - Score delta magnitude (larger = higher confidence)
        - Trend consistency (smoother = higher confidence)
        - Final score severity (higher = higher confidence)
        
        Args:
            scores: List of crisis scores
            score_delta: Total score change
            time_span_hours: Time span in hours
            escalation_type: Classified escalation type
            
        Returns:
            Confidence score 0.0-1.0
        """
        # Factor 1: Score delta relative to threshold (0-0.4)
        delta_factor = min(
            score_delta / (self._config.score_increase_threshold * 2),
            0.4
        )
        
        # Factor 2: Trend consistency (0-0.3)
        consistency = self._calculate_trend_consistency(scores)
        consistency_factor = consistency * 0.3
        
        # Factor 3: Final score severity (0-0.3)
        final_score = scores[-1] if scores else 0.0
        severity_factor = min(final_score, 1.0) * 0.3
        
        # Combine factors
        confidence = delta_factor + consistency_factor + severity_factor
        
        return min(confidence, 1.0)
    
    def _calculate_trend_consistency(self, scores: List[float]) -> float:
        """
        Calculate how consistent the upward trend is.
        
        Args:
            scores: List of crisis scores
            
        Returns:
            Consistency score 0.0-1.0
        """
        if len(scores) < 2:
            return 0.0
        
        # Count transitions that go in expected direction
        expected_increases = len(scores) - 1
        actual_increases = sum(
            1 for i in range(1, len(scores))
            if scores[i] >= scores[i-1] - 0.05  # Allow small dips
        )
        
        return actual_increases / expected_increases
    
    def _find_intervention_point(self, scores: List[float]) -> Optional[int]:
        """
        Find the index where intervention should have occurred.
        
        The intervention point is where the score first crosses
        a significant threshold (medium severity = 0.5).
        
        Args:
            scores: List of crisis scores
            
        Returns:
            Index of intervention point, or None if not reached
        """
        intervention_threshold = 0.5  # Medium severity
        
        for i, score in enumerate(scores):
            if score >= intervention_threshold:
                return i
        
        return None
    
    def _match_pattern(
        self,
        escalation_type: EscalationType,
        time_span_hours: float,
        score_delta: float,
    ) -> Tuple[Optional[str], float]:
        """
        Match against known escalation patterns.
        
        Args:
            escalation_type: Detected escalation type
            time_span_hours: Time span in hours
            score_delta: Total score change
            
        Returns:
            Tuple of (pattern_name, confidence) or (None, 0.0)
        """
        if escalation_type == EscalationType.NONE:
            return None, 0.0
        
        best_match: Optional[str] = None
        best_confidence: float = 0.0
        
        for pattern_name, pattern in self._known_patterns.items():
            # Check escalation type match
            type_matches = self._type_matches_pattern(
                escalation_type, 
                pattern.escalation_type
            )
            if not type_matches:
                continue
            
            # Calculate duration similarity
            duration_similarity = self._calculate_duration_similarity(
                time_span_hours,
                pattern.typical_duration_hours,
            )
            
            # Calculate overall match confidence
            confidence = duration_similarity * 0.7 + (score_delta * 0.3)
            confidence = min(confidence, 1.0)
            
            if confidence > best_confidence:
                best_match = pattern_name
                best_confidence = confidence
        
        return best_match, best_confidence
    
    def _type_matches_pattern(
        self, 
        detected: EscalationType, 
        pattern_type: str
    ) -> bool:
        """
        Check if detected escalation type matches pattern type.
        
        Args:
            detected: Detected EscalationType
            pattern_type: Pattern's escalation_type string
            
        Returns:
            True if types match
        """
        type_map = {
            EscalationType.RAPID: "rapid",
            EscalationType.GRADUAL: "gradual",
            EscalationType.SUDDEN: "sudden",
        }
        return type_map.get(detected) == pattern_type
    
    def _calculate_duration_similarity(
        self, 
        actual_hours: float, 
        typical_hours: int
    ) -> float:
        """
        Calculate similarity between actual and typical duration.
        
        Args:
            actual_hours: Actual time span
            typical_hours: Pattern's typical duration
            
        Returns:
            Similarity score 0.0-1.0
        """
        if typical_hours <= 0:
            return 0.5
        
        ratio = actual_hours / typical_hours
        
        # Perfect match at 1.0, decreasing as ratio diverges
        # Use a bell curve centered at 1.0
        if ratio < 0.5:
            return ratio * 2 * 0.7  # Scale up small ratios
        elif ratio > 2.0:
            return max(0.0, 1.0 - (ratio - 2.0) * 0.5)  # Penalize very long
        else:
            # Between 0.5 and 2.0, use inverse distance from 1.0
            distance = abs(1.0 - ratio)
            return 1.0 - distance
    
    def is_enabled(self) -> bool:
        """Check if escalation detection is enabled."""
        return self._config.enabled
    
    def get_config(self) -> EscalationDetectionConfig:
        """Get current escalation detection configuration."""
        return self._config


# =============================================================================
# Factory Function
# =============================================================================

def create_escalation_detector(
    context_config_manager: ContextConfigManager,
) -> EscalationDetector:
    """
    Factory function for EscalationDetector (Clean Architecture v5.1 Pattern).
    
    Args:
        context_config_manager: Context configuration manager
        
    Returns:
        Configured EscalationDetector instance
        
    Example:
        >>> detector = create_escalation_detector(context_config)
        >>> result = detector.analyze(scores=[0.2, 0.4, 0.7, 0.9], timestamps=[...])
        >>> if result.detected:
        ...     print(f"Escalation: {result.escalation_type.value}")
    """
    logger.info("🏭 Creating EscalationDetector")
    return EscalationDetector(context_config_manager=context_config_manager)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "EscalationType",
    "EscalationAnalysis",
    "EscalationDetector",
    "create_escalation_detector",
]
