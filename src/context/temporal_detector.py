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
Temporal Detector for Ash-NLP Service - Phase 5
---
FILE VERSION: v5.0-5-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Detect late night posting patterns (10PM-4AM by default)
- Detect rapid posting frequency patterns
- Calculate time-based risk modifiers
- Identify weekend patterns
- Provide temporal context for crisis assessment
"""

import logging
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.managers import (
    ContextConfigManager,
    TemporalDetectionConfig,
)

# Module version
__version__ = "v5.0-5-1.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class TimeOfDayRisk(Enum):
    """Time of day risk classification."""
    NORMAL = "normal"
    LATE_NIGHT = "late_night"
    EARLY_MORNING = "early_morning"


class PostingFrequency(Enum):
    """Posting frequency classification."""
    NORMAL = "normal"
    ELEVATED = "elevated"
    RAPID = "rapid"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TemporalAnalysis:
    """
    Result of temporal pattern detection.
    
    Attributes:
        late_night_detected: Whether current message is during late night hours
        late_night_count: Number of messages in late night hours
        rapid_posting_detected: Whether rapid posting pattern detected
        messages_in_window: Number of messages in rapid posting window
        time_of_day_risk: Classification of time-based risk
        posting_frequency: Classification of posting frequency
        risk_modifier: Combined risk modifier to apply (1.0 = no change)
        is_weekend: Whether current message is on weekend
        hour_of_day: Hour of the current message (0-23)
        average_gap_minutes: Average time between messages
    """
    late_night_detected: bool = False
    late_night_count: int = 0
    rapid_posting_detected: bool = False
    messages_in_window: int = 0
    time_of_day_risk: TimeOfDayRisk = TimeOfDayRisk.NORMAL
    posting_frequency: PostingFrequency = PostingFrequency.NORMAL
    risk_modifier: float = 1.0
    is_weekend: bool = False
    hour_of_day: int = 12
    average_gap_minutes: float = 0.0


# =============================================================================
# Temporal Detector
# =============================================================================

class TemporalDetector:
    """
    Detects time-based patterns in message history.
    
    Analyzes timestamps to identify:
    - Late night posting (isolation risk)
    - Rapid posting frequency (crisis indicator)
    - Weekend patterns (reduced support availability)
    
    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_temporal_detector)
    - Configuration via ContextConfigManager
    - Resilient analysis with safe defaults
    """
    
    def __init__(self, context_config_manager: ContextConfigManager):
        """
        Initialize TemporalDetector.
        
        Args:
            context_config_manager: Context configuration manager
            
        Note:
            Use create_temporal_detector() factory function instead.
        """
        self._config_manager = context_config_manager
        self._config = context_config_manager.get_temporal_detection_config()
        
        logger.debug(
            f"TemporalDetector initialized "
            f"(late_night={self._config.late_night_start_hour}-{self._config.late_night_end_hour}, "
            f"rapid_threshold={self._config.rapid_posting_threshold_minutes}min)"
        )
    
    def analyze(
        self,
        timestamps: List[datetime],
        current_timestamp: Optional[datetime] = None,
    ) -> TemporalAnalysis:
        """
        Analyze timestamps for temporal patterns.
        
        Args:
            timestamps: List of message timestamps in chronological order
            current_timestamp: Timestamp of current message (default: last in list)
            
        Returns:
            TemporalAnalysis with detection results
        """
        if not self._config.enabled:
            logger.debug("Temporal detection disabled")
            return TemporalAnalysis()
        
        if not timestamps:
            logger.debug("No timestamps provided for temporal analysis")
            return TemporalAnalysis()
        
        # Use last timestamp as current if not provided
        if current_timestamp is None:
            current_timestamp = timestamps[-1]
        
        # Analyze late night patterns
        late_night_detected, late_night_count = self._analyze_late_night(
            timestamps, current_timestamp
        )
        
        # Analyze posting frequency
        rapid_posting_detected, messages_in_window = self._analyze_posting_frequency(
            timestamps
        )
        
        # Classify time of day risk
        time_of_day_risk = self._classify_time_of_day(current_timestamp)
        
        # Classify posting frequency
        posting_frequency = self._classify_posting_frequency(
            messages_in_window, 
            rapid_posting_detected
        )
        
        # Check weekend
        is_weekend = self._is_weekend(current_timestamp)
        
        # Calculate average gap
        average_gap = self._calculate_average_gap(timestamps)
        
        # Calculate combined risk modifier
        risk_modifier = self._calculate_risk_modifier(
            late_night_detected=late_night_detected,
            rapid_posting_detected=rapid_posting_detected,
            is_weekend=is_weekend,
        )
        
        return TemporalAnalysis(
            late_night_detected=late_night_detected,
            late_night_count=late_night_count,
            rapid_posting_detected=rapid_posting_detected,
            messages_in_window=messages_in_window,
            time_of_day_risk=time_of_day_risk,
            posting_frequency=posting_frequency,
            risk_modifier=risk_modifier,
            is_weekend=is_weekend,
            hour_of_day=current_timestamp.hour,
            average_gap_minutes=average_gap,
        )
    
    def _analyze_late_night(
        self,
        timestamps: List[datetime],
        current_timestamp: datetime,
    ) -> tuple[bool, int]:
        """
        Analyze for late night posting patterns.
        
        Args:
            timestamps: List of message timestamps
            current_timestamp: Current message timestamp
            
        Returns:
            Tuple of (is_late_night, late_night_message_count)
        """
        # Check if current message is late night
        is_late_night = self._is_late_night_hour(current_timestamp.hour)
        
        # Count how many messages in history are late night
        late_night_count = sum(
            1 for ts in timestamps 
            if self._is_late_night_hour(ts.hour)
        )
        
        return is_late_night, late_night_count
    
    def _is_late_night_hour(self, hour: int) -> bool:
        """
        Check if an hour falls within late night window.
        
        Handles wraparound (e.g., 22-4 spans midnight).
        
        Args:
            hour: Hour of day (0-23)
            
        Returns:
            True if hour is in late night window
        """
        start = self._config.late_night_start_hour
        end = self._config.late_night_end_hour
        
        if start > end:
            # Wraps around midnight (e.g., 22-4)
            return hour >= start or hour < end
        else:
            # Same day range (e.g., 1-5)
            return start <= hour < end
    
    def _analyze_posting_frequency(
        self,
        timestamps: List[datetime],
    ) -> tuple[bool, int]:
        """
        Analyze posting frequency for rapid posting detection.
        
        Args:
            timestamps: List of message timestamps
            
        Returns:
            Tuple of (is_rapid_posting, messages_in_window)
        """
        if len(timestamps) < 2:
            return False, len(timestamps)
        
        # Look at the window from the most recent message
        window_minutes = self._config.rapid_posting_threshold_minutes
        threshold_count = self._config.rapid_posting_message_count
        
        # Get the most recent timestamp as reference
        latest = timestamps[-1]
        window_start = latest - timedelta(minutes=window_minutes)
        
        # Count messages within the window
        messages_in_window = sum(
            1 for ts in timestamps
            if ts >= window_start
        )
        
        # Check if exceeds rapid posting threshold
        is_rapid = messages_in_window >= threshold_count
        
        return is_rapid, messages_in_window
    
    def _classify_time_of_day(self, timestamp: datetime) -> TimeOfDayRisk:
        """
        Classify time of day risk level.
        
        Args:
            timestamp: Message timestamp
            
        Returns:
            TimeOfDayRisk classification
        """
        hour = timestamp.hour
        
        if self._is_late_night_hour(hour):
            # Late night: 10PM - 4AM (default)
            return TimeOfDayRisk.LATE_NIGHT
        elif 4 <= hour < 7:
            # Early morning: 4AM - 7AM
            return TimeOfDayRisk.EARLY_MORNING
        else:
            return TimeOfDayRisk.NORMAL
    
    def _classify_posting_frequency(
        self, 
        messages_in_window: int,
        rapid_detected: bool,
    ) -> PostingFrequency:
        """
        Classify posting frequency level.
        
        Args:
            messages_in_window: Number of messages in time window
            rapid_detected: Whether rapid posting was detected
            
        Returns:
            PostingFrequency classification
        """
        if rapid_detected:
            return PostingFrequency.RAPID
        
        threshold = self._config.rapid_posting_message_count
        
        if messages_in_window >= threshold * 0.6:
            return PostingFrequency.ELEVATED
        else:
            return PostingFrequency.NORMAL
    
    def _is_weekend(self, timestamp: datetime) -> bool:
        """
        Check if timestamp falls on weekend.
        
        Args:
            timestamp: Message timestamp
            
        Returns:
            True if Saturday (5) or Sunday (6)
        """
        return timestamp.weekday() >= 5
    
    def _calculate_average_gap(self, timestamps: List[datetime]) -> float:
        """
        Calculate average time gap between messages in minutes.
        
        Args:
            timestamps: List of message timestamps
            
        Returns:
            Average gap in minutes
        """
        if len(timestamps) < 2:
            return 0.0
        
        total_gap = timedelta()
        
        for i in range(1, len(timestamps)):
            gap = timestamps[i] - timestamps[i-1]
            total_gap += gap
        
        avg_gap = total_gap / (len(timestamps) - 1)
        return avg_gap.total_seconds() / 60.0
    
    def _calculate_risk_modifier(
        self,
        late_night_detected: bool,
        rapid_posting_detected: bool,
        is_weekend: bool,
    ) -> float:
        """
        Calculate combined risk modifier based on temporal factors.
        
        Risk modifiers are multiplicative:
        - Late night: 1.2x (20% increase)
        - Rapid posting: 1.15x (15% increase) 
        - Weekend: 1.1x (10% increase)
        
        Args:
            late_night_detected: Whether late night posting detected
            rapid_posting_detected: Whether rapid posting detected
            is_weekend: Whether current message is on weekend
            
        Returns:
            Combined risk modifier (1.0 = no change)
        """
        modifier = 1.0
        
        if late_night_detected:
            modifier *= self._config.late_night_risk_modifier
        
        if rapid_posting_detected:
            # Rapid posting adds 15% risk
            modifier *= 1.15
        
        if is_weekend:
            modifier *= self._config.weekend_risk_modifier
        
        return modifier
    
    def is_enabled(self) -> bool:
        """Check if temporal detection is enabled."""
        return self._config.enabled
    
    def get_config(self) -> TemporalDetectionConfig:
        """Get current temporal detection configuration."""
        return self._config


# =============================================================================
# Factory Function
# =============================================================================

def create_temporal_detector(
    context_config_manager: ContextConfigManager,
) -> TemporalDetector:
    """
    Factory function for TemporalDetector (Clean Architecture v5.1 Pattern).
    
    Args:
        context_config_manager: Context configuration manager
        
    Returns:
        Configured TemporalDetector instance
        
    Example:
        >>> detector = create_temporal_detector(context_config)
        >>> result = detector.analyze(timestamps=[...])
        >>> if result.late_night_detected:
        ...     print(f"Late night risk modifier: {result.risk_modifier}")
    """
    logger.info("🏭 Creating TemporalDetector")
    return TemporalDetector(context_config_manager=context_config_manager)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "TimeOfDayRisk",
    "PostingFrequency",
    "TemporalAnalysis",
    "TemporalDetector",
    "create_temporal_detector",
]
