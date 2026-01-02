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
Context Analyzer for Ash-NLP Service - Phase 5 (Main Orchestrator)
---
FILE VERSION: v5.0-5-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Orchestrate all context analysis components
- Coordinate EscalationDetector, TemporalDetector, TrendAnalyzer
- Calculate intervention urgency
- Produce unified ContextAnalysisResult
- Manage message history processing

KEY ARCHITECTURAL DECISION:
Ash-NLP remains STATELESS. Message history is provided by Ash-Bot in each request.
"""

import logging
from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from src.managers import (
    ContextConfigManager,
    create_context_config_manager,
    InterventionConfig,
)

from .escalation_detector import (
    EscalationDetector,
    create_escalation_detector,
    EscalationType,
    EscalationAnalysis,
)
from .temporal_detector import (
    TemporalDetector,
    create_temporal_detector,
    TimeOfDayRisk,
    PostingFrequency,
    TemporalAnalysis,
)
from .trend_analyzer import (
    TrendAnalyzer,
    create_trend_analyzer,
    TrendDirection,
    TrendVelocity,
    TrendAnalysis,
)

# Module version
__version__ = "v5.0-5-1.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Intervention Urgency Enum
# =============================================================================

class InterventionUrgency(Enum):
    """Urgency level for intervention."""
    NONE = "none"
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    IMMEDIATE = "immediate"


# =============================================================================
# Input Data Classes
# =============================================================================

@dataclass
class MessageHistoryItem:
    """
    Single message in history provided by Ash-Bot.
    
    Attributes:
        message: The message text content
        timestamp: When the message was sent (ISO format or datetime)
        crisis_score: Pre-calculated crisis score (optional, will be calculated if not provided)
        user_id: User identifier (optional)
    """
    message: str
    timestamp: datetime
    crisis_score: Optional[float] = None
    user_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageHistoryItem":
        """Create MessageHistoryItem from dictionary."""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        
        return cls(
            message=data.get("message", ""),
            timestamp=timestamp,
            crisis_score=data.get("crisis_score"),
            user_id=data.get("user_id"),
        )


@dataclass
class MessageSequence:
    """
    Complete message sequence for analysis.
    
    Includes current message and history.
    """
    current_message: str
    current_timestamp: datetime
    current_score: float
    history: List[MessageHistoryItem] = field(default_factory=list)
    user_id: Optional[str] = None


# =============================================================================
# Output Data Classes
# =============================================================================

@dataclass
class EscalationResult:
    """Escalation detection results for API response."""
    detected: bool = False
    rate: str = "none"  # none, gradual, rapid, sudden
    pattern: Optional[str] = None
    confidence: float = 0.0


@dataclass
class TemporalResult:
    """Temporal detection results for API response."""
    late_night_risk: bool = False
    rapid_posting: bool = False
    time_risk_modifier: float = 1.0
    hour_of_day: int = 12
    is_weekend: bool = False


@dataclass
class TrendResult:
    """Trend analysis results for API response."""
    direction: str = "stable"  # improving, stable, worsening, volatile
    velocity: str = "none"  # none, gradual, moderate, rapid
    score_delta: float = 0.0
    time_span_hours: float = 0.0


@dataclass
class TrajectoryInfo:
    """Score trajectory information."""
    start_score: float = 0.0
    end_score: float = 0.0
    scores: List[float] = field(default_factory=list)
    min_score: float = 0.0
    max_score: float = 0.0


@dataclass
class InterventionInfo:
    """Intervention recommendations."""
    urgency: str = "none"  # none, low, standard, high, immediate
    recommended_point: Optional[int] = None
    intervention_delayed: bool = False
    reason: str = ""


@dataclass 
class HistoryMetadata:
    """Metadata about the analyzed history."""
    message_count: int = 0
    time_span_hours: float = 0.0
    analysis_timestamp: Optional[datetime] = None


@dataclass
class ContextAnalysisResult:
    """
    Complete context analysis result for API response.
    
    This is the main output structure that gets returned to the API layer.
    """
    # Feature flags
    context_analysis_enabled: bool = True
    
    # Sub-results
    escalation: EscalationResult = field(default_factory=EscalationResult)
    temporal: TemporalResult = field(default_factory=TemporalResult)
    trend: TrendResult = field(default_factory=TrendResult)
    trajectory: TrajectoryInfo = field(default_factory=TrajectoryInfo)
    intervention: InterventionInfo = field(default_factory=InterventionInfo)
    metadata: HistoryMetadata = field(default_factory=HistoryMetadata)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "escalation_detected": self.escalation.detected,
            "escalation_rate": self.escalation.rate,
            "escalation_pattern": self.escalation.pattern,
            "pattern_confidence": self.escalation.confidence,
            
            "trend": {
                "direction": self.trend.direction,
                "velocity": self.trend.velocity,
                "score_delta": self.trend.score_delta,
                "time_span_hours": self.trend.time_span_hours,
            },
            
            "temporal_factors": {
                "late_night_risk": self.temporal.late_night_risk,
                "rapid_posting": self.temporal.rapid_posting,
                "time_risk_modifier": self.temporal.time_risk_modifier,
            },
            
            "trajectory": {
                "start_score": self.trajectory.start_score,
                "end_score": self.trajectory.end_score,
                "scores": self.trajectory.scores,
            },
            
            "intervention": {
                "urgency": self.intervention.urgency,
                "recommended_point": self.intervention.recommended_point,
                "intervention_delayed": self.intervention.intervention_delayed,
            },
        }


# =============================================================================
# Context Analyzer (Main Orchestrator)
# =============================================================================

class ContextAnalyzer:
    """
    Main orchestrator for context-aware crisis analysis.
    
    Coordinates:
    - EscalationDetector: Detects escalation patterns
    - TemporalDetector: Detects time-based patterns
    - TrendAnalyzer: Analyzes trend direction/velocity
    
    Produces unified ContextAnalysisResult for API responses.
    
    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_context_analyzer)
    - Dependency injection for all components
    - Resilient analysis with safe defaults
    """
    
    def __init__(
        self,
        context_config_manager: ContextConfigManager,
        escalation_detector: Optional[EscalationDetector] = None,
        temporal_detector: Optional[TemporalDetector] = None,
        trend_analyzer: Optional[TrendAnalyzer] = None,
    ):
        """
        Initialize ContextAnalyzer.
        
        Args:
            context_config_manager: Context configuration manager
            escalation_detector: Optional injected escalation detector
            temporal_detector: Optional injected temporal detector
            trend_analyzer: Optional injected trend analyzer
            
        Note:
            Use create_context_analyzer() factory function instead.
        """
        self._config_manager = context_config_manager
        self._config = context_config_manager.get_context_analysis_config()
        self._intervention_config = context_config_manager.get_intervention_config()
        
        # Initialize or use injected components
        self._escalation_detector = escalation_detector or create_escalation_detector(
            context_config_manager
        )
        self._temporal_detector = temporal_detector or create_temporal_detector(
            context_config_manager
        )
        self._trend_analyzer = trend_analyzer or create_trend_analyzer(
            context_config_manager
        )
        
        logger.info(
            f"✅ ContextAnalyzer v{__version__} initialized "
            f"(enabled={self._config.enabled}, max_history={self._config.max_history_size})"
        )
    
    def analyze(
        self,
        current_message: str,
        current_score: float,
        message_history: Optional[List[MessageHistoryItem]] = None,
        current_timestamp: Optional[datetime] = None,
    ) -> ContextAnalysisResult:
        """
        Perform complete context analysis.
        
        Args:
            current_message: The current message being analyzed
            current_score: Crisis score for the current message
            message_history: List of previous messages with scores
            current_timestamp: Timestamp of current message (default: now)
            
        Returns:
            ContextAnalysisResult with all analysis results
        """
        # Check if enabled
        if not self._config.enabled:
            logger.debug("Context analysis disabled")
            return ContextAnalysisResult(context_analysis_enabled=False)
        
        # Set default timestamp
        if current_timestamp is None:
            current_timestamp = datetime.utcnow()
        
        # Ensure history list exists
        if message_history is None:
            message_history = []
        
        # Limit history size
        if len(message_history) > self._config.max_history_size:
            message_history = message_history[-self._config.max_history_size:]
            logger.debug(f"Trimmed history to {self._config.max_history_size} messages")
        
        # Build score and timestamp sequences (history + current)
        scores, timestamps = self._build_sequences(
            message_history, current_score, current_timestamp
        )
        
        # Run individual analyzers
        escalation_analysis = self._run_escalation_analysis(scores, timestamps)
        temporal_analysis = self._run_temporal_analysis(timestamps, current_timestamp)
        trend_analysis = self._run_trend_analysis(scores, timestamps)
        
        # Build unified result
        result = self._build_result(
            escalation_analysis=escalation_analysis,
            temporal_analysis=temporal_analysis,
            trend_analysis=trend_analysis,
            scores=scores,
            timestamps=timestamps,
            current_score=current_score,
        )
        
        logger.debug(
            f"Context analysis complete: "
            f"escalation={result.escalation.detected}, "
            f"trend={result.trend.direction}, "
            f"urgency={result.intervention.urgency}"
        )
        
        return result
    
    def analyze_from_sequence(self, sequence: MessageSequence) -> ContextAnalysisResult:
        """
        Analyze a complete message sequence.
        
        Convenience method that accepts MessageSequence dataclass.
        
        Args:
            sequence: MessageSequence with current message and history
            
        Returns:
            ContextAnalysisResult
        """
        return self.analyze(
            current_message=sequence.current_message,
            current_score=sequence.current_score,
            message_history=sequence.history,
            current_timestamp=sequence.current_timestamp,
        )
    
    def _build_sequences(
        self,
        history: List[MessageHistoryItem],
        current_score: float,
        current_timestamp: datetime,
    ) -> tuple[List[float], List[datetime]]:
        """
        Build score and timestamp sequences from history + current.
        
        Args:
            history: Message history items
            current_score: Current message score
            current_timestamp: Current message timestamp
            
        Returns:
            Tuple of (scores, timestamps) lists
        """
        scores = []
        timestamps = []
        
        # Add history items (filter out items without scores)
        for item in history:
            if item.crisis_score is not None:
                scores.append(item.crisis_score)
                timestamps.append(item.timestamp)
        
        # Add current message
        scores.append(current_score)
        timestamps.append(current_timestamp)
        
        return scores, timestamps
    
    def _run_escalation_analysis(
        self,
        scores: List[float],
        timestamps: List[datetime],
    ) -> EscalationAnalysis:
        """
        Run escalation detection.
        
        Args:
            scores: Score sequence
            timestamps: Timestamp sequence
            
        Returns:
            EscalationAnalysis result
        """
        try:
            return self._escalation_detector.analyze(scores, timestamps)
        except Exception as e:
            logger.error(f"Escalation analysis failed: {e}")
            return EscalationAnalysis(scores=scores)
    
    def _run_temporal_analysis(
        self,
        timestamps: List[datetime],
        current_timestamp: datetime,
    ) -> TemporalAnalysis:
        """
        Run temporal pattern detection.
        
        Args:
            timestamps: Timestamp sequence
            current_timestamp: Current message timestamp
            
        Returns:
            TemporalAnalysis result
        """
        try:
            return self._temporal_detector.analyze(timestamps, current_timestamp)
        except Exception as e:
            logger.error(f"Temporal analysis failed: {e}")
            return TemporalAnalysis()
    
    def _run_trend_analysis(
        self,
        scores: List[float],
        timestamps: List[datetime],
    ) -> TrendAnalysis:
        """
        Run trend analysis.
        
        Args:
            scores: Score sequence
            timestamps: Timestamp sequence
            
        Returns:
            TrendAnalysis result
        """
        try:
            return self._trend_analyzer.analyze(scores, timestamps)
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return TrendAnalysis()
    
    def _build_result(
        self,
        escalation_analysis: EscalationAnalysis,
        temporal_analysis: TemporalAnalysis,
        trend_analysis: TrendAnalysis,
        scores: List[float],
        timestamps: List[datetime],
        current_score: float,
    ) -> ContextAnalysisResult:
        """
        Build unified ContextAnalysisResult from individual analyses.
        
        Args:
            escalation_analysis: Escalation detection results
            temporal_analysis: Temporal detection results
            trend_analysis: Trend analysis results
            scores: Score sequence
            timestamps: Timestamp sequence
            current_score: Current message score
            
        Returns:
            Unified ContextAnalysisResult
        """
        # Build escalation result
        escalation = EscalationResult(
            detected=escalation_analysis.detected,
            rate=escalation_analysis.escalation_type.value,
            pattern=escalation_analysis.matched_pattern,
            confidence=escalation_analysis.confidence,
        )
        
        # Build temporal result
        temporal = TemporalResult(
            late_night_risk=temporal_analysis.late_night_detected,
            rapid_posting=temporal_analysis.rapid_posting_detected,
            time_risk_modifier=temporal_analysis.risk_modifier,
            hour_of_day=temporal_analysis.hour_of_day,
            is_weekend=temporal_analysis.is_weekend,
        )
        
        # Build trend result
        trend = TrendResult(
            direction=trend_analysis.direction.value,
            velocity=trend_analysis.velocity.value,
            score_delta=trend_analysis.score_delta,
            time_span_hours=trend_analysis.time_span_hours,
        )
        
        # Build trajectory info
        trajectory = TrajectoryInfo(
            start_score=trend_analysis.start_score,
            end_score=trend_analysis.end_score,
            scores=scores.copy(),
            min_score=trend_analysis.min_score,
            max_score=trend_analysis.max_score,
        )
        
        # Calculate intervention info
        intervention = self._calculate_intervention(
            escalation_analysis=escalation_analysis,
            temporal_analysis=temporal_analysis,
            trend_analysis=trend_analysis,
            current_score=current_score,
        )
        
        # Build metadata
        time_span = 0.0
        if len(timestamps) >= 2:
            delta = timestamps[-1] - timestamps[0]
            time_span = delta.total_seconds() / 3600.0
        
        metadata = HistoryMetadata(
            message_count=len(scores),
            time_span_hours=time_span,
            analysis_timestamp=datetime.utcnow(),
        )
        
        return ContextAnalysisResult(
            context_analysis_enabled=True,
            escalation=escalation,
            temporal=temporal,
            trend=trend,
            trajectory=trajectory,
            intervention=intervention,
            metadata=metadata,
        )
    
    def _calculate_intervention(
        self,
        escalation_analysis: EscalationAnalysis,
        temporal_analysis: TemporalAnalysis,
        trend_analysis: TrendAnalysis,
        current_score: float,
    ) -> InterventionInfo:
        """
        Calculate intervention urgency and recommendations.
        
        Args:
            escalation_analysis: Escalation detection results
            temporal_analysis: Temporal detection results
            trend_analysis: Trend analysis results
            current_score: Current crisis score
            
        Returns:
            InterventionInfo with urgency and recommendations
        """
        # Start with score-based urgency
        urgency = self._score_to_urgency(current_score)
        reason_parts = []
        
        # Boost for escalation
        if (self._intervention_config.escalation_urgency_boost and 
            escalation_analysis.detected):
            urgency = self._boost_urgency(urgency)
            reason_parts.append("escalation detected")
        
        # Boost for late night
        if (self._intervention_config.late_night_urgency_boost and 
            temporal_analysis.late_night_detected):
            urgency = self._boost_urgency(urgency)
            reason_parts.append("late night hours")
        
        # Boost for rapid escalation
        if escalation_analysis.escalation_type == EscalationType.RAPID:
            urgency = self._boost_urgency(urgency)
            reason_parts.append("rapid escalation")
        
        # Check if intervention was delayed
        intervention_delayed = False
        recommended_point = escalation_analysis.intervention_point
        
        if recommended_point is not None:
            # Intervention should have happened earlier
            intervention_delayed = True
            reason_parts.append("intervention point passed")
        
        reason = "; ".join(reason_parts) if reason_parts else "score-based assessment"
        
        return InterventionInfo(
            urgency=urgency.value,
            recommended_point=recommended_point,
            intervention_delayed=intervention_delayed,
            reason=reason,
        )
    
    def _score_to_urgency(self, score: float) -> InterventionUrgency:
        """
        Convert crisis score to base urgency level.
        
        Args:
            score: Crisis score (0.0-1.0)
            
        Returns:
            InterventionUrgency level
        """
        if score >= 0.85:
            return InterventionUrgency.IMMEDIATE
        elif score >= 0.70:
            return InterventionUrgency.HIGH
        elif score >= 0.50:
            return InterventionUrgency.STANDARD
        elif score >= 0.30:
            return InterventionUrgency.LOW
        else:
            return InterventionUrgency.NONE
    
    def _boost_urgency(self, urgency: InterventionUrgency) -> InterventionUrgency:
        """
        Boost urgency level by one step.
        
        Args:
            urgency: Current urgency level
            
        Returns:
            Boosted urgency level (capped at IMMEDIATE)
        """
        boost_map = {
            InterventionUrgency.NONE: InterventionUrgency.LOW,
            InterventionUrgency.LOW: InterventionUrgency.STANDARD,
            InterventionUrgency.STANDARD: InterventionUrgency.HIGH,
            InterventionUrgency.HIGH: InterventionUrgency.IMMEDIATE,
            InterventionUrgency.IMMEDIATE: InterventionUrgency.IMMEDIATE,
        }
        return boost_map.get(urgency, InterventionUrgency.IMMEDIATE)
    
    def is_enabled(self) -> bool:
        """Check if context analysis is enabled."""
        return self._config.enabled
    
    def get_max_history_size(self) -> int:
        """Get maximum history size setting."""
        return self._config.max_history_size


# =============================================================================
# Factory Function
# =============================================================================

def create_context_analyzer(
    context_config_manager: Optional[ContextConfigManager] = None,
    escalation_detector: Optional[EscalationDetector] = None,
    temporal_detector: Optional[TemporalDetector] = None,
    trend_analyzer: Optional[TrendAnalyzer] = None,
) -> ContextAnalyzer:
    """
    Factory function for ContextAnalyzer (Clean Architecture v5.1 Pattern).
    
    Args:
        context_config_manager: Context configuration manager (default: create new)
        escalation_detector: Optional injected escalation detector
        temporal_detector: Optional injected temporal detector
        trend_analyzer: Optional injected trend analyzer
        
    Returns:
        Configured ContextAnalyzer instance
        
    Example:
        >>> analyzer = create_context_analyzer()
        >>> result = analyzer.analyze(
        ...     current_message="I can't do this anymore",
        ...     current_score=0.85,
        ...     message_history=[
        ...         MessageHistoryItem(message="Not feeling great", timestamp=..., crisis_score=0.3),
        ...         MessageHistoryItem(message="Things are harder", timestamp=..., crisis_score=0.5),
        ...     ],
        ... )
        >>> if result.escalation.detected:
        ...     print(f"Escalation: {result.escalation.rate}")
        ...     print(f"Urgency: {result.intervention.urgency}")
    """
    logger.info("🏭 Creating ContextAnalyzer")
    
    # Create config manager if not provided
    if context_config_manager is None:
        context_config_manager = create_context_config_manager()
    
    return ContextAnalyzer(
        context_config_manager=context_config_manager,
        escalation_detector=escalation_detector,
        temporal_detector=temporal_detector,
        trend_analyzer=trend_analyzer,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Urgency enum
    "InterventionUrgency",
    # Input data classes
    "MessageHistoryItem",
    "MessageSequence",
    # Output data classes
    "EscalationResult",
    "TemporalResult",
    "TrendResult",
    "TrajectoryInfo",
    "InterventionInfo",
    "HistoryMetadata",
    "ContextAnalysisResult",
    # Main analyzer
    "ContextAnalyzer",
    "create_context_analyzer",
]
