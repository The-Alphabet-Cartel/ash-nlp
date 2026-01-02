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
Trend Analyzer for Ash-NLP Service - Phase 5
---
FILE VERSION: v5.0-5-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Analyze trend direction (worsening, stable, improving)
- Calculate trend velocity (how fast things are changing)
- Provide trajectory information for visualization
- Detect trend reversals and inflection points
"""

import logging
from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from src.managers import (
    ContextConfigManager,
    TrendAnalysisConfig,
)

# Module version
__version__ = "v5.0-5-1.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class TrendDirection(Enum):
    """Direction of crisis score trend."""
    IMPROVING = "improving"
    STABLE = "stable"
    WORSENING = "worsening"
    VOLATILE = "volatile"


class TrendVelocity(Enum):
    """Velocity/speed of trend change."""
    NONE = "none"
    GRADUAL = "gradual"
    MODERATE = "moderate"
    RAPID = "rapid"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TrendAnalysis:
    """
    Result of trend analysis.
    
    Attributes:
        direction: Overall trend direction
        velocity: Speed of change
        score_delta: Total score change (end - start)
        rate_per_hour: Score change rate per hour
        start_score: First score in sequence
        end_score: Last score in sequence
        min_score: Minimum score in sequence
        max_score: Maximum score in sequence
        inflection_points: Indices where trend direction changed
        smoothed_scores: Scores after noise smoothing
        confidence: Confidence in trend detection (0.0-1.0)
        time_span_hours: Total time span analyzed
    """
    direction: TrendDirection = TrendDirection.STABLE
    velocity: TrendVelocity = TrendVelocity.NONE
    score_delta: float = 0.0
    rate_per_hour: float = 0.0
    start_score: float = 0.0
    end_score: float = 0.0
    min_score: float = 0.0
    max_score: float = 0.0
    inflection_points: List[int] = field(default_factory=list)
    smoothed_scores: List[float] = field(default_factory=list)
    confidence: float = 0.0
    time_span_hours: float = 0.0


# =============================================================================
# Trend Analyzer
# =============================================================================

class TrendAnalyzer:
    """
    Analyzes trends in crisis score sequences.
    
    Examines score history to determine:
    - Whether situation is worsening, stable, or improving
    - How quickly things are changing
    - Where inflection points occurred
    
    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_trend_analyzer)
    - Configuration via ContextConfigManager
    - Resilient analysis with safe defaults
    """
    
    def __init__(self, context_config_manager: ContextConfigManager):
        """
        Initialize TrendAnalyzer.
        
        Args:
            context_config_manager: Context configuration manager
            
        Note:
            Use create_trend_analyzer() factory function instead.
        """
        self._config_manager = context_config_manager
        self._config = context_config_manager.get_trend_analysis_config()
        
        logger.debug(
            f"TrendAnalyzer initialized "
            f"(worsening_threshold={self._config.worsening_threshold}, "
            f"improving_threshold={self._config.improving_threshold})"
        )
    
    def analyze(
        self,
        scores: List[float],
        timestamps: Optional[List[datetime]] = None,
    ) -> TrendAnalysis:
        """
        Analyze a sequence of crisis scores for trends.
        
        Args:
            scores: List of crisis scores (0.0-1.0) in chronological order
            timestamps: Optional list of timestamps for velocity calculation
            
        Returns:
            TrendAnalysis with detection results
        """
        if not self._config.enabled:
            logger.debug("Trend analysis disabled")
            return TrendAnalysis()
        
        if len(scores) < 2:
            logger.debug("Insufficient scores for trend analysis")
            if scores:
                return TrendAnalysis(
                    start_score=scores[0],
                    end_score=scores[0],
                    min_score=scores[0],
                    max_score=scores[0],
                    smoothed_scores=scores.copy(),
                )
            return TrendAnalysis()
        
        # Calculate time span if timestamps provided
        time_span_hours = 0.0
        if timestamps and len(timestamps) >= 2:
            delta = timestamps[-1] - timestamps[0]
            time_span_hours = max(delta.total_seconds() / 3600.0, 0.0167)
        
        # Smooth scores to reduce noise
        smoothed_scores = self._smooth_scores(scores)
        
        # Calculate basic metrics
        start_score = smoothed_scores[0]
        end_score = smoothed_scores[-1]
        score_delta = end_score - start_score
        min_score = min(smoothed_scores)
        max_score = max(smoothed_scores)
        
        # Calculate rate per hour
        rate_per_hour = 0.0
        if time_span_hours > 0:
            rate_per_hour = score_delta / time_span_hours
        
        # Determine direction and velocity
        direction = self._determine_direction(score_delta, smoothed_scores)
        velocity = self._determine_velocity(rate_per_hour)
        
        # Find inflection points
        inflection_points = self._find_inflection_points(smoothed_scores)
        
        # Adjust direction for volatile patterns
        if len(inflection_points) >= 2 and abs(score_delta) < self._config.worsening_threshold:
            direction = TrendDirection.VOLATILE
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            scores=smoothed_scores,
            direction=direction,
            score_delta=score_delta,
        )
        
        return TrendAnalysis(
            direction=direction,
            velocity=velocity,
            score_delta=score_delta,
            rate_per_hour=rate_per_hour,
            start_score=start_score,
            end_score=end_score,
            min_score=min_score,
            max_score=max_score,
            inflection_points=inflection_points,
            smoothed_scores=smoothed_scores,
            confidence=confidence,
            time_span_hours=time_span_hours,
        )
    
    def _smooth_scores(self, scores: List[float]) -> List[float]:
        """
        Apply simple moving average smoothing to reduce noise.
        
        Uses a window size of 3 for minimal smoothing that
        preserves the overall trend while reducing jitter.
        
        Args:
            scores: Raw score list
            
        Returns:
            Smoothed score list (same length)
        """
        if len(scores) <= 2:
            return scores.copy()
        
        smoothed = []
        window_size = min(3, len(scores))
        
        for i in range(len(scores)):
            # Calculate window bounds
            start = max(0, i - window_size // 2)
            end = min(len(scores), i + window_size // 2 + 1)
            
            # Calculate average in window
            window = scores[start:end]
            avg = sum(window) / len(window)
            smoothed.append(avg)
        
        return smoothed
    
    def _determine_direction(
        self, 
        score_delta: float,
        scores: List[float],
    ) -> TrendDirection:
        """
        Determine overall trend direction.
        
        Args:
            score_delta: Total score change
            scores: Score list for consistency check
            
        Returns:
            TrendDirection classification
        """
        # Check against thresholds
        if score_delta >= self._config.worsening_threshold:
            # Verify consistent upward movement
            if self._is_consistent_trend(scores, increasing=True):
                return TrendDirection.WORSENING
            else:
                return TrendDirection.VOLATILE
        
        elif score_delta <= self._config.improving_threshold:
            # Verify consistent downward movement
            if self._is_consistent_trend(scores, increasing=False):
                return TrendDirection.IMPROVING
            else:
                return TrendDirection.VOLATILE
        
        else:
            return TrendDirection.STABLE
    
    def _is_consistent_trend(
        self, 
        scores: List[float], 
        increasing: bool
    ) -> bool:
        """
        Check if scores show a consistent trend.
        
        Allows minor fluctuations but requires overall consistency.
        
        Args:
            scores: Score list
            increasing: True to check for upward trend
            
        Returns:
            True if trend is consistent
        """
        if len(scores) < 2:
            return True
        
        # Count transitions in expected vs opposite direction
        expected = 0
        opposite = 0
        
        for i in range(1, len(scores)):
            delta = scores[i] - scores[i-1]
            
            if increasing:
                if delta > 0.02:  # Small tolerance
                    expected += 1
                elif delta < -0.02:
                    opposite += 1
            else:
                if delta < -0.02:
                    expected += 1
                elif delta > 0.02:
                    opposite += 1
        
        # Consider consistent if majority moves in expected direction
        total = expected + opposite
        if total == 0:
            return True
        
        return expected >= opposite
    
    def _determine_velocity(self, rate_per_hour: float) -> TrendVelocity:
        """
        Determine velocity classification based on rate of change.
        
        Args:
            rate_per_hour: Score change per hour
            
        Returns:
            TrendVelocity classification
        """
        abs_rate = abs(rate_per_hour)
        
        if abs_rate >= self._config.velocity_rapid_threshold:
            return TrendVelocity.RAPID
        elif abs_rate >= self._config.velocity_gradual_threshold:
            return TrendVelocity.MODERATE
        elif abs_rate > 0.01:
            return TrendVelocity.GRADUAL
        else:
            return TrendVelocity.NONE
    
    def _find_inflection_points(self, scores: List[float]) -> List[int]:
        """
        Find indices where trend direction changes.
        
        An inflection point is where the score changes from
        increasing to decreasing or vice versa.
        
        Args:
            scores: Score list
            
        Returns:
            List of indices where direction changed
        """
        if len(scores) < 3:
            return []
        
        inflection_points = []
        tolerance = 0.03  # Ignore tiny fluctuations
        
        # Track current direction
        prev_direction = None  # True=up, False=down, None=flat
        
        for i in range(1, len(scores)):
            delta = scores[i] - scores[i-1]
            
            if delta > tolerance:
                current_direction = True
            elif delta < -tolerance:
                current_direction = False
            else:
                continue  # Flat, no direction change
            
            # Check for direction reversal
            if prev_direction is not None and current_direction != prev_direction:
                inflection_points.append(i - 1)
            
            prev_direction = current_direction
        
        return inflection_points
    
    def _calculate_confidence(
        self,
        scores: List[float],
        direction: TrendDirection,
        score_delta: float,
    ) -> float:
        """
        Calculate confidence in trend detection.
        
        Factors:
        - Consistency of direction
        - Magnitude of change
        - Number of data points
        
        Args:
            scores: Score list
            direction: Detected direction
            score_delta: Total score change
            
        Returns:
            Confidence score 0.0-1.0
        """
        # Factor 1: Data points (more = higher confidence, up to 0.3)
        data_factor = min(len(scores) / 10.0, 0.3)
        
        # Factor 2: Magnitude of change (larger = higher confidence, up to 0.4)
        if direction in (TrendDirection.WORSENING, TrendDirection.IMPROVING):
            threshold = self._config.worsening_threshold
            magnitude_ratio = abs(score_delta) / threshold
            magnitude_factor = min(magnitude_ratio * 0.2, 0.4)
        else:
            magnitude_factor = 0.2  # Stable/volatile get moderate confidence
        
        # Factor 3: Consistency (up to 0.3)
        if direction == TrendDirection.VOLATILE:
            consistency_factor = 0.1
        else:
            increasing = direction == TrendDirection.WORSENING
            is_consistent = self._is_consistent_trend(scores, increasing)
            consistency_factor = 0.3 if is_consistent else 0.15
        
        confidence = data_factor + magnitude_factor + consistency_factor
        return min(confidence, 1.0)
    
    def get_trajectory_summary(self, analysis: TrendAnalysis) -> str:
        """
        Generate a human-readable trajectory summary.
        
        Args:
            analysis: TrendAnalysis result
            
        Returns:
            Summary string
        """
        direction_text = {
            TrendDirection.IMPROVING: "improving",
            TrendDirection.STABLE: "stable",
            TrendDirection.WORSENING: "worsening",
            TrendDirection.VOLATILE: "volatile",
        }
        
        velocity_text = {
            TrendVelocity.NONE: "",
            TrendVelocity.GRADUAL: "gradually",
            TrendVelocity.MODERATE: "moderately",
            TrendVelocity.RAPID: "rapidly",
        }
        
        vel = velocity_text.get(analysis.velocity, "")
        dir_text = direction_text.get(analysis.direction, "unknown")
        
        if vel:
            return f"Situation is {vel} {dir_text}"
        else:
            return f"Situation is {dir_text}"
    
    def is_enabled(self) -> bool:
        """Check if trend analysis is enabled."""
        return self._config.enabled
    
    def get_config(self) -> TrendAnalysisConfig:
        """Get current trend analysis configuration."""
        return self._config


# =============================================================================
# Factory Function
# =============================================================================

def create_trend_analyzer(
    context_config_manager: ContextConfigManager,
) -> TrendAnalyzer:
    """
    Factory function for TrendAnalyzer (Clean Architecture v5.1 Pattern).
    
    Args:
        context_config_manager: Context configuration manager
        
    Returns:
        Configured TrendAnalyzer instance
        
    Example:
        >>> analyzer = create_trend_analyzer(context_config)
        >>> result = analyzer.analyze(scores=[0.3, 0.4, 0.6, 0.8])
        >>> print(f"Trend: {result.direction.value} ({result.velocity.value})")
    """
    logger.info("🏭 Creating TrendAnalyzer")
    return TrendAnalyzer(context_config_manager=context_config_manager)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "TrendDirection",
    "TrendVelocity",
    "TrendAnalysis",
    "TrendAnalyzer",
    "create_trend_analyzer",
]
