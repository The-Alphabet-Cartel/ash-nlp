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
Phase 6 Sprint 3 Tests - FE-005 (Per-Severity Thresholds) & FE-007 (History Debug)
---
FILE VERSION: v5.0-6-3.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 3
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

TEST COVERAGE:
- FE-005: Per-severity threshold configuration and usage
- FE-007: History validation and edge case detection
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# =============================================================================
# FE-005: Per-Severity Threshold Tests
# =============================================================================

class TestSeverityThresholds:
    """Tests for FE-005: Configurable Escalation Thresholds per Severity."""
    
    def test_severity_threshold_dataclass(self):
        """Test SeverityThreshold dataclass creation."""
        from src.managers import SeverityThreshold
        
        threshold = SeverityThreshold(
            score_increase_threshold=0.15,
            minimum_messages=2,
            rapid_threshold_hours=2,
        )
        
        assert threshold.score_increase_threshold == 0.15
        assert threshold.minimum_messages == 2
        assert threshold.rapid_threshold_hours == 2
    
    def test_threshold_preset_dataclass(self):
        """Test ThresholdPreset dataclass creation."""
        from src.managers import ThresholdPreset
        
        preset = ThresholdPreset(
            name="sensitive",
            description="High sensitivity",
            score_increase_threshold=0.2,
            minimum_messages=2,
            rapid_threshold_hours=6,
        )
        
        assert preset.name == "sensitive"
        assert preset.description == "High sensitivity"
        assert preset.score_increase_threshold == 0.2
    
    def test_config_get_threshold_for_severity(self):
        """Test getting threshold for specific severity level."""
        from src.managers import EscalationDetectionConfig, SeverityThreshold
        
        # Create config with per-severity thresholds
        config = EscalationDetectionConfig(
            score_increase_threshold=0.3,  # default
            minimum_messages=3,
            rapid_threshold_hours=4,
            per_severity_thresholds={
                "critical": SeverityThreshold(0.15, 2, 2),
                "high": SeverityThreshold(0.20, 2, 3),
            }
        )
        
        # Test getting critical threshold
        critical = config.get_threshold_for_severity("critical")
        assert critical.score_increase_threshold == 0.15
        assert critical.minimum_messages == 2
        
        # Test getting high threshold
        high = config.get_threshold_for_severity("high")
        assert high.score_increase_threshold == 0.20
        
        # Test fallback to default for unknown severity
        unknown = config.get_threshold_for_severity("unknown")
        assert unknown.score_increase_threshold == 0.3  # default
    
    def test_context_config_loads_per_severity(self, tmp_path):
        """Test that ContextConfigManager loads per-severity thresholds."""
        import json
        from src.managers import create_context_config_manager
        
        # Create test config
        config_data = {
            "_metadata": {"file_version": "test"},
            "context_analysis": {"defaults": {"enabled": True}},
            "escalation_detection": {
                "defaults": {
                    "enabled": True,
                    "score_increase_threshold": 0.3,
                    "minimum_messages": 3,
                    "rapid_threshold_hours": 4,
                    "gradual_threshold_hours": 24,
                },
                "per_severity_thresholds": {
                    "critical": {
                        "score_increase_threshold": 0.15,
                        "minimum_messages": 2,
                        "rapid_threshold_hours": 2,
                    },
                    "high": {
                        "score_increase_threshold": 0.20,
                        "minimum_messages": 2,
                        "rapid_threshold_hours": 3,
                    },
                },
                "threshold_presets": {
                    "sensitive": {
                        "description": "High sensitivity",
                        "score_increase_threshold": 0.20,
                        "minimum_messages": 2,
                        "rapid_threshold_hours": 6,
                    },
                },
            },
            "temporal_detection": {"defaults": {"enabled": True}},
            "trend_analysis": {"defaults": {"enabled": True}},
            "intervention": {},
            "known_patterns": {"patterns": {}},
        }
        
        config_file = tmp_path / "context_config.json"
        config_file.write_text(json.dumps(config_data))
        
        manager = create_context_config_manager(config_dir=tmp_path)
        escalation_config = manager.get_escalation_detection_config()
        
        # Check per-severity thresholds loaded
        assert "critical" in escalation_config.per_severity_thresholds
        assert "high" in escalation_config.per_severity_thresholds
        
        critical = escalation_config.get_threshold_for_severity("critical")
        assert critical.score_increase_threshold == 0.15
        
        # Check presets loaded
        assert "sensitive" in escalation_config.threshold_presets
        preset = escalation_config.get_preset("sensitive")
        assert preset is not None
        assert preset.score_increase_threshold == 0.20


class TestEscalationDetectorSeverity:
    """Tests for EscalationDetector severity-aware analysis."""
    
    @pytest.fixture
    def mock_context_config(self):
        """Create mock context config manager with per-severity thresholds."""
        from src.managers import (
            ContextConfigManager,
            EscalationDetectionConfig,
            SeverityThreshold,
        )
        
        mock = MagicMock(spec=ContextConfigManager)
        
        # Create config with per-severity thresholds
        config = EscalationDetectionConfig(
            enabled=True,
            score_increase_threshold=0.3,
            minimum_messages=3,
            rapid_threshold_hours=4,
            gradual_threshold_hours=24,
            per_severity_thresholds={
                "critical": SeverityThreshold(0.15, 2, 2),
                "high": SeverityThreshold(0.20, 2, 3),
                "medium": SeverityThreshold(0.30, 3, 4),
                "low": SeverityThreshold(0.40, 4, 6),
            }
        )
        mock.get_escalation_detection_config.return_value = config
        mock.get_known_patterns.return_value = {}
        
        return mock
    
    def test_analyze_with_severity_critical(self, mock_context_config):
        """Test severity-aware analysis with critical threshold."""
        from src.context.escalation_detector import create_escalation_detector
        
        detector = create_escalation_detector(mock_context_config)
        
        now = datetime.utcnow()
        # Small escalation that meets critical threshold (0.15) but not medium (0.30)
        scores = [0.5, 0.55, 0.67]  # delta = 0.17
        timestamps = [now - timedelta(hours=1), now - timedelta(minutes=30), now]
        
        # With critical threshold (0.15), should detect
        result_critical = detector.analyze_with_severity(
            scores=scores,
            timestamps=timestamps,
            current_severity="critical",
        )
        
        assert result_critical.severity_used == "critical"
        assert result_critical.detected is True
        assert result_critical.threshold_used["score_increase_threshold"] == 0.15
    
    def test_analyze_with_severity_returns_threshold_info(self, mock_context_config):
        """Test that severity analysis returns threshold information."""
        from src.context.escalation_detector import create_escalation_detector
        
        detector = create_escalation_detector(mock_context_config)
        
        now = datetime.utcnow()
        scores = [0.3, 0.5, 0.7, 0.9]
        timestamps = [
            now - timedelta(hours=3),
            now - timedelta(hours=2),
            now - timedelta(hours=1),
            now,
        ]
        
        result = detector.analyze_with_severity(
            scores=scores,
            timestamps=timestamps,
            current_severity="high",
        )
        
        # Check metadata is populated
        assert result.severity_used == "high"
        assert result.threshold_used is not None
        assert "score_increase_threshold" in result.threshold_used
        assert "minimum_messages" in result.threshold_used
        assert "rapid_threshold_hours" in result.threshold_used
    
    def test_get_available_severities(self, mock_context_config):
        """Test getting list of available severity levels."""
        from src.context.escalation_detector import create_escalation_detector
        
        detector = create_escalation_detector(mock_context_config)
        
        severities = detector.get_available_severities()
        
        assert "critical" in severities
        assert "high" in severities
        assert "medium" in severities
        assert "low" in severities
    
    def test_get_threshold_for_severity_method(self, mock_context_config):
        """Test detector method to get threshold for severity."""
        from src.context.escalation_detector import create_escalation_detector
        
        detector = create_escalation_detector(mock_context_config)
        
        critical_threshold = detector.get_threshold_for_severity("critical")
        
        assert critical_threshold.score_increase_threshold == 0.15
        assert critical_threshold.minimum_messages == 2
        assert critical_threshold.rapid_threshold_hours == 2


# =============================================================================
# FE-007: History Validation Tests
# =============================================================================

class TestHistoryValidator:
    """Tests for FE-007: History Validation."""
    
    def test_validate_empty_history(self):
        """Test validation of empty history."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        result = validate_history([])
        
        assert result.message_count == 0
        assert len(result.issues) == 1
        assert result.issues[0].issue_type == HistoryIssue.EMPTY_HISTORY
    
    def test_validate_valid_history(self):
        """Test validation of properly formatted history."""
        from src.utils.history_debug import validate_history
        
        now = datetime.utcnow()
        history = [
            {
                "message": "I'm feeling down today",
                "timestamp": (now - timedelta(hours=2)).isoformat() + "Z",
                "crisis_score": 0.3,
            },
            {
                "message": "Things are getting worse",
                "timestamp": (now - timedelta(hours=1)).isoformat() + "Z",
                "crisis_score": 0.5,
            },
            {
                "message": "I don't know what to do",
                "timestamp": now.isoformat() + "Z",
                "crisis_score": 0.7,
            },
        ]
        
        result = validate_history(history)
        
        assert result.valid is True
        assert result.message_count == 3
        assert result.error_count == 0
    
    def test_validate_missing_timestamp(self):
        """Test detection of missing timestamp."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        history = [
            {"message": "Test message"},  # Missing timestamp
        ]
        
        result = validate_history(history)
        
        assert result.valid is False
        assert any(i.issue_type == HistoryIssue.MISSING_TIMESTAMP for i in result.issues)
    
    def test_validate_missing_message(self):
        """Test detection of missing message."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        history = [
            {"timestamp": datetime.utcnow().isoformat() + "Z"},  # Missing message
        ]
        
        result = validate_history(history)
        
        assert result.valid is False
        assert any(i.issue_type == HistoryIssue.MISSING_MESSAGE for i in result.issues)
    
    def test_validate_invalid_score(self):
        """Test detection of invalid crisis score."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        now = datetime.utcnow()
        history = [
            {
                "message": "Test",
                "timestamp": now.isoformat() + "Z",
                "crisis_score": 1.5,  # Out of range
            },
        ]
        
        result = validate_history(history)
        
        assert any(i.issue_type == HistoryIssue.SCORE_OUT_OF_RANGE for i in result.issues)
    
    def test_validate_out_of_order_timestamps(self):
        """Test detection of non-chronological timestamps."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        now = datetime.utcnow()
        history = [
            {
                "message": "Second message",
                "timestamp": now.isoformat() + "Z",
            },
            {
                "message": "First message",  # Out of order
                "timestamp": (now - timedelta(hours=1)).isoformat() + "Z",
            },
        ]
        
        result = validate_history(history)
        
        assert any(i.issue_type == HistoryIssue.OUT_OF_ORDER for i in result.issues)
    
    def test_validate_future_timestamp(self):
        """Test detection of future timestamps."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        future = datetime.utcnow() + timedelta(hours=1)
        history = [
            {
                "message": "Future message",
                "timestamp": future.isoformat() + "Z",
            },
        ]
        
        result = validate_history(history)
        
        assert any(i.issue_type == HistoryIssue.FUTURE_TIMESTAMP for i in result.issues)
    
    def test_validate_large_time_gap(self):
        """Test detection of large time gaps."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        now = datetime.utcnow()
        history = [
            {
                "message": "Old message",
                "timestamp": (now - timedelta(days=2)).isoformat() + "Z",
            },
            {
                "message": "Recent message",
                "timestamp": now.isoformat() + "Z",
            },
        ]
        
        result = validate_history(history)
        
        assert any(i.issue_type == HistoryIssue.LARGE_TIME_GAP for i in result.issues)
    
    def test_validate_unknown_field_warning(self):
        """Test warning for unknown fields."""
        from src.utils.history_debug import validate_history, HistoryIssue
        
        now = datetime.utcnow()
        history = [
            {
                "message": "Test",
                "timestamp": now.isoformat() + "Z",
                "unknown_field": "value",  # Unknown field
            },
        ]
        
        result = validate_history(history)
        
        assert any(i.issue_type == HistoryIssue.UNKNOWN_FIELD for i in result.issues)


class TestHistoryValidationResult:
    """Tests for HistoryValidationResult dataclass."""
    
    def test_to_dict_conversion(self):
        """Test conversion to dictionary."""
        from src.utils.history_debug import (
            HistoryValidationResult,
            HistoryValidationIssue,
            HistoryIssue,
        )
        
        now = datetime.utcnow()
        result = HistoryValidationResult(
            valid=True,
            issues=[
                HistoryValidationIssue(
                    issue_type=HistoryIssue.LARGE_TIME_GAP,
                    severity="warning",
                )
            ],
            message_count=5,
            time_span_hours=2.5,
            earliest_timestamp=now - timedelta(hours=2),
            latest_timestamp=now,
            score_range=(0.2, 0.8),
        )
        
        d = result.to_dict()
        
        assert d["valid"] is True
        assert d["message_count"] == 5
        assert d["time_span_hours"] == 2.5
        assert d["score_range"]["min"] == 0.2
        assert d["score_range"]["max"] == 0.8
        assert len(d["issues"]) == 1
    
    def test_error_and_warning_counts(self):
        """Test counting errors vs warnings."""
        from src.utils.history_debug import (
            HistoryValidationResult,
            HistoryValidationIssue,
            HistoryIssue,
        )
        
        result = HistoryValidationResult(
            issues=[
                HistoryValidationIssue(HistoryIssue.MISSING_TIMESTAMP, severity="error"),
                HistoryValidationIssue(HistoryIssue.MISSING_MESSAGE, severity="error"),
                HistoryValidationIssue(HistoryIssue.LARGE_TIME_GAP, severity="warning"),
            ]
        )
        
        assert result.error_count == 2
        assert result.warning_count == 1


class TestHistoryDebugLogger:
    """Tests for HistoryDebugLogger."""
    
    def test_log_receive(self, caplog):
        """Test logging of history receive."""
        import logging
        from src.utils.history_debug import create_history_debug_logger
        
        caplog.set_level(logging.DEBUG)
        debug_logger = create_history_debug_logger()
        
        history = [{"message": "test", "timestamp": "2026-01-01T00:00:00Z"}]
        debug_logger.log_receive(history, request_id="test-123")
        
        assert "FE-007 [RECEIVE]" in caplog.text
        assert "1 items" in caplog.text
    
    def test_log_complete(self, caplog):
        """Test logging of completion."""
        import logging
        from src.utils.history_debug import create_history_debug_logger
        
        caplog.set_level(logging.DEBUG)
        debug_logger = create_history_debug_logger()
        
        debug_logger.log_complete(
            total_items=10,
            processing_time_ms=15.5,
            success=True,
        )
        
        assert "FE-007 [COMPLETE:SUCCESS]" in caplog.text


# =============================================================================
# Integration Tests
# =============================================================================

class TestSprint3Integration:
    """Integration tests for Sprint 3 features."""
    
    def test_config_has_per_severity_section(self, tmp_path):
        """Test that context_config.json has per_severity_thresholds section."""
        import json
        from pathlib import Path
        
        # Read actual config file
        config_path = Path(__file__).parent.parent.parent / "src" / "config" / "context_config.json"
        
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            
            assert "escalation_detection" in config
            assert "per_severity_thresholds" in config["escalation_detection"]
            assert "threshold_presets" in config["escalation_detection"]
            
            # Check severity levels exist
            thresholds = config["escalation_detection"]["per_severity_thresholds"]
            assert "critical" in thresholds
            assert "high" in thresholds
    
    def test_escalation_analysis_includes_fe005_fields(self):
        """Test that EscalationAnalysis includes FE-005 fields."""
        from src.context.escalation_detector import EscalationAnalysis
        
        analysis = EscalationAnalysis()
        
        # Check FE-005 fields exist
        assert hasattr(analysis, "severity_used")
        assert hasattr(analysis, "threshold_used")
    
    def test_utils_exports_history_debug(self):
        """Test that utils package exports history debug utilities."""
        from src.utils import (
            HistoryIssue,
            HistoryValidationResult,
            HistoryValidator,
            validate_history,
        )
        
        # Verify imports work
        assert HistoryIssue is not None
        assert HistoryValidationResult is not None
        assert HistoryValidator is not None
        assert validate_history is not None
    
    def test_managers_exports_fe005_classes(self):
        """Test that managers package exports FE-005 classes."""
        from src.managers import (
            SeverityThreshold,
            ThresholdPreset,
        )
        
        # Verify imports work
        assert SeverityThreshold is not None
        assert ThresholdPreset is not None
