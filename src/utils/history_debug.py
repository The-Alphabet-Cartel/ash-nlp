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
History Debug Utilities for Ash-NLP Service - Phase 6 Sprint 3
---
FILE VERSION: v5.0-6-3.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 3 (FE-007: History Passthrough Investigation)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Validate message history format and structure
- Log detailed history processing information
- Detect edge cases and anomalies in history data
- Provide debugging utilities for history passthrough issues
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Module version
__version__ = "v5.0-6-3.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class HistoryIssue(Enum):
    """Types of history validation issues."""
    EMPTY_HISTORY = "empty_history"
    MISSING_TIMESTAMP = "missing_timestamp"
    INVALID_TIMESTAMP = "invalid_timestamp"
    MISSING_MESSAGE = "missing_message"
    EMPTY_MESSAGE = "empty_message"
    MISSING_SCORE = "missing_score"
    INVALID_SCORE = "invalid_score"
    OUT_OF_ORDER = "out_of_order"
    DUPLICATE_TIMESTAMP = "duplicate_timestamp"
    FUTURE_TIMESTAMP = "future_timestamp"
    LARGE_TIME_GAP = "large_time_gap"
    SCORE_OUT_OF_RANGE = "score_out_of_range"
    UNKNOWN_FIELD = "unknown_field"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class HistoryValidationIssue:
    """Single validation issue found in history."""
    issue_type: HistoryIssue
    message_index: Optional[int] = None
    field_name: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    severity: str = "warning"  # warning, error
    
    def __str__(self) -> str:
        msg = f"[{self.severity.upper()}] {self.issue_type.value}"
        if self.message_index is not None:
            msg += f" at index {self.message_index}"
        if self.field_name:
            msg += f" (field: {self.field_name})"
        if self.expected and self.actual:
            msg += f" - expected {self.expected}, got {self.actual}"
        return msg


@dataclass
class HistoryValidationResult:
    """Result of history validation."""
    valid: bool = True
    issues: List[HistoryValidationIssue] = field(default_factory=list)
    message_count: int = 0
    time_span_hours: float = 0.0
    earliest_timestamp: Optional[datetime] = None
    latest_timestamp: Optional[datetime] = None
    score_range: Tuple[float, float] = (0.0, 0.0)
    
    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")
    
    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "valid": self.valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "message_count": self.message_count,
            "time_span_hours": round(self.time_span_hours, 2),
            "earliest_timestamp": self.earliest_timestamp.isoformat() if self.earliest_timestamp else None,
            "latest_timestamp": self.latest_timestamp.isoformat() if self.latest_timestamp else None,
            "score_range": {
                "min": round(self.score_range[0], 3),
                "max": round(self.score_range[1], 3),
            },
            "issues": [str(i) for i in self.issues],
        }


@dataclass
class HistoryDebugInfo:
    """Detailed debug information for history processing."""
    validation: HistoryValidationResult = field(default_factory=HistoryValidationResult)
    parsed_count: int = 0
    skipped_count: int = 0
    processing_time_ms: float = 0.0
    memory_estimate_kb: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "validation": self.validation.to_dict(),
            "parsed_count": self.parsed_count,
            "skipped_count": self.skipped_count,
            "processing_time_ms": round(self.processing_time_ms, 2),
            "memory_estimate_kb": round(self.memory_estimate_kb, 2),
        }


# =============================================================================
# History Validator
# =============================================================================

class HistoryValidator:
    """
    Validates message history data structure and content (FE-007).
    
    Checks for:
    - Required fields (message, timestamp)
    - Valid data types
    - Chronological ordering
    - Score validity
    - Edge cases (gaps, duplicates, future timestamps)
    """
    
    # Expected fields in a history item
    REQUIRED_FIELDS = {"message", "timestamp"}
    OPTIONAL_FIELDS = {"crisis_score", "user_id", "message_id"}
    KNOWN_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS
    
    # Thresholds for warnings
    LARGE_GAP_HOURS = 24  # Gap larger than this triggers warning
    MAX_HISTORY_AGE_DAYS = 30  # History older than this triggers warning
    
    def __init__(self, strict: bool = False):
        """
        Initialize HistoryValidator.
        
        Args:
            strict: If True, warnings become errors
        """
        self.strict = strict
    
    def validate(
        self,
        history: List[Dict[str, Any]],
        current_timestamp: Optional[datetime] = None,
    ) -> HistoryValidationResult:
        """
        Validate message history list.
        
        Args:
            history: List of history item dictionaries
            current_timestamp: Current time for comparison (default: now)
            
        Returns:
            HistoryValidationResult with validation details
        """
        result = HistoryValidationResult()
        
        if current_timestamp is None:
            current_timestamp = datetime.utcnow()
        
        # Check for empty history
        if not history:
            result.issues.append(HistoryValidationIssue(
                issue_type=HistoryIssue.EMPTY_HISTORY,
                severity="warning",
            ))
            logger.debug("FE-007: Empty history received")
            return result
        
        result.message_count = len(history)
        timestamps: List[datetime] = []
        scores: List[float] = []
        
        # Validate each item
        for idx, item in enumerate(history):
            self._validate_item(item, idx, result, current_timestamp)
            
            # Collect valid timestamps and scores
            if "timestamp" in item:
                ts = self._parse_timestamp(item["timestamp"])
                if ts:
                    timestamps.append(ts)
            
            if "crisis_score" in item:
                score = item["crisis_score"]
                if isinstance(score, (int, float)) and 0.0 <= score <= 1.0:
                    scores.append(float(score))
        
        # Check chronological order
        self._check_order(timestamps, result)
        
        # Calculate statistics
        if timestamps:
            result.earliest_timestamp = min(timestamps)
            result.latest_timestamp = max(timestamps)
            result.time_span_hours = (
                result.latest_timestamp - result.earliest_timestamp
            ).total_seconds() / 3600.0
        
        if scores:
            result.score_range = (min(scores), max(scores))
        
        # Check for large gaps
        self._check_gaps(timestamps, result)
        
        # Set overall validity
        result.valid = result.error_count == 0
        
        # Log summary
        logger.debug(
            f"FE-007: Validated {result.message_count} history items - "
            f"{result.error_count} errors, {result.warning_count} warnings"
        )
        
        return result
    
    def _validate_item(
        self,
        item: Dict[str, Any],
        idx: int,
        result: HistoryValidationResult,
        current_timestamp: datetime,
    ) -> None:
        """Validate a single history item."""
        severity = "error" if self.strict else "warning"
        
        # Check for required fields
        for field in self.REQUIRED_FIELDS:
            if field not in item:
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.MISSING_TIMESTAMP if field == "timestamp" else HistoryIssue.MISSING_MESSAGE,
                    message_index=idx,
                    field_name=field,
                    severity="error",
                ))
        
        # Validate message field
        if "message" in item:
            msg = item["message"]
            if not isinstance(msg, str):
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.EMPTY_MESSAGE,
                    message_index=idx,
                    field_name="message",
                    expected="string",
                    actual=type(msg).__name__,
                    severity="error",
                ))
            elif not msg.strip():
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.EMPTY_MESSAGE,
                    message_index=idx,
                    severity=severity,
                ))
        
        # Validate timestamp field
        if "timestamp" in item:
            ts = self._parse_timestamp(item["timestamp"])
            if ts is None:
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.INVALID_TIMESTAMP,
                    message_index=idx,
                    field_name="timestamp",
                    actual=str(item["timestamp"]),
                    severity="error",
                ))
            elif ts > current_timestamp + timedelta(minutes=5):
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.FUTURE_TIMESTAMP,
                    message_index=idx,
                    severity=severity,
                ))
        
        # Validate crisis_score field (optional)
        if "crisis_score" in item:
            score = item["crisis_score"]
            if score is None:
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.MISSING_SCORE,
                    message_index=idx,
                    severity="warning",
                ))
            elif not isinstance(score, (int, float)):
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.INVALID_SCORE,
                    message_index=idx,
                    expected="number",
                    actual=type(score).__name__,
                    severity="error",
                ))
            elif not (0.0 <= score <= 1.0):
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.SCORE_OUT_OF_RANGE,
                    message_index=idx,
                    expected="0.0-1.0",
                    actual=str(score),
                    severity=severity,
                ))
        
        # Check for unknown fields
        unknown_fields = set(item.keys()) - self.KNOWN_FIELDS
        for field in unknown_fields:
            result.issues.append(HistoryValidationIssue(
                issue_type=HistoryIssue.UNKNOWN_FIELD,
                message_index=idx,
                field_name=field,
                severity="warning",
            ))
    
    def _parse_timestamp(self, value: Any) -> Optional[datetime]:
        """Parse timestamp from various formats."""
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            try:
                # Handle ISO format with Z suffix
                clean = value.replace("Z", "+00:00")
                dt = datetime.fromisoformat(clean)
                # Convert to naive UTC
                if dt.tzinfo is not None:
                    from datetime import timezone
                    dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
                return dt
            except (ValueError, AttributeError):
                pass
        
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(value)
            except (ValueError, OSError):
                pass
        
        return None
    
    def _check_order(
        self,
        timestamps: List[datetime],
        result: HistoryValidationResult,
    ) -> None:
        """Check if timestamps are in chronological order."""
        for i in range(1, len(timestamps)):
            if timestamps[i] < timestamps[i-1]:
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.OUT_OF_ORDER,
                    message_index=i,
                    severity="warning",
                ))
            elif timestamps[i] == timestamps[i-1]:
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.DUPLICATE_TIMESTAMP,
                    message_index=i,
                    severity="warning",
                ))
    
    def _check_gaps(
        self,
        timestamps: List[datetime],
        result: HistoryValidationResult,
    ) -> None:
        """Check for large time gaps in history."""
        for i in range(1, len(timestamps)):
            gap_hours = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600.0
            if gap_hours > self.LARGE_GAP_HOURS:
                result.issues.append(HistoryValidationIssue(
                    issue_type=HistoryIssue.LARGE_TIME_GAP,
                    message_index=i,
                    expected=f"<{self.LARGE_GAP_HOURS}h",
                    actual=f"{gap_hours:.1f}h",
                    severity="warning",
                ))


# =============================================================================
# Debug Logger
# =============================================================================

class HistoryDebugLogger:
    """
    Detailed logging for history processing (FE-007).
    
    Provides structured logging at various stages of history processing
    to help diagnose passthrough issues.
    """
    
    def __init__(self, logger_name: str = "ash_nlp.history"):
        """Initialize with custom logger."""
        self._logger = logging.getLogger(logger_name)
    
    def log_receive(
        self,
        history: List[Dict[str, Any]],
        request_id: Optional[str] = None,
    ) -> None:
        """Log when history is received."""
        self._logger.debug(
            f"FE-007 [RECEIVE] History received: "
            f"{len(history)} items"
            f"{f' (request_id={request_id})' if request_id else ''}"
        )
        if history:
            self._logger.debug(f"  First item keys: {list(history[0].keys())}")
    
    def log_parse(
        self,
        parsed_count: int,
        skipped_count: int,
        errors: List[str],
    ) -> None:
        """Log parsing results."""
        self._logger.debug(
            f"FE-007 [PARSE] Parsed: {parsed_count}, Skipped: {skipped_count}"
        )
        for error in errors[:5]:  # Limit to first 5 errors
            self._logger.warning(f"  Parse error: {error}")
    
    def log_transform(
        self,
        input_count: int,
        output_count: int,
        transform_name: str,
    ) -> None:
        """Log transformation results."""
        self._logger.debug(
            f"FE-007 [TRANSFORM:{transform_name}] "
            f"{input_count} -> {output_count} items"
        )
    
    def log_analysis(
        self,
        component: str,
        input_count: int,
        result_summary: str,
    ) -> None:
        """Log analysis component results."""
        self._logger.debug(
            f"FE-007 [ANALYSIS:{component}] "
            f"{input_count} items -> {result_summary}"
        )
    
    def log_complete(
        self,
        total_items: int,
        processing_time_ms: float,
        success: bool,
    ) -> None:
        """Log completion of history processing."""
        status = "SUCCESS" if success else "FAILED"
        self._logger.debug(
            f"FE-007 [COMPLETE:{status}] "
            f"Processed {total_items} items in {processing_time_ms:.2f}ms"
        )


# =============================================================================
# Factory Functions
# =============================================================================

def create_history_validator(strict: bool = False) -> HistoryValidator:
    """
    Factory function for HistoryValidator (Clean Architecture v5.1 Pattern).
    
    Args:
        strict: If True, warnings become errors
        
    Returns:
        Configured HistoryValidator instance
    """
    logger.info("🏭 Creating HistoryValidator (FE-007)")
    return HistoryValidator(strict=strict)


def create_history_debug_logger(logger_name: str = "ash_nlp.history") -> HistoryDebugLogger:
    """
    Factory function for HistoryDebugLogger (Clean Architecture v5.1 Pattern).
    
    Args:
        logger_name: Name for the debug logger
        
    Returns:
        Configured HistoryDebugLogger instance
    """
    return HistoryDebugLogger(logger_name=logger_name)


def validate_history(
    history: List[Dict[str, Any]],
    strict: bool = False,
) -> HistoryValidationResult:
    """
    Convenience function to validate history data (FE-007).
    
    Args:
        history: List of history item dictionaries
        strict: If True, warnings become errors
        
    Returns:
        HistoryValidationResult with validation details
    """
    validator = HistoryValidator(strict=strict)
    return validator.validate(history)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Enums
    "HistoryIssue",
    # Data classes
    "HistoryValidationIssue",
    "HistoryValidationResult",
    "HistoryDebugInfo",
    # Classes
    "HistoryValidator",
    "HistoryDebugLogger",
    # Factory functions
    "create_history_validator",
    "create_history_debug_logger",
    "validate_history",
]
