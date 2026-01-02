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
Context Configuration Manager for Ash-NLP Service - Phase 5
---
FILE VERSION: v5.0-6-3.0-1
LAST MODIFIED: 2026-01-02
PHASE: Phase 6 - Sprint 3 (FE-005: Per-Severity Thresholds)
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Load context analysis configuration from context_config.json
- Apply environment variable overrides
- Provide typed getters for all context analysis settings
- Support runtime configuration updates
- Validate configuration values against schemas

CONFIGURATION SECTIONS:
- context_analysis: Master toggle and history limits
- escalation_detection: Escalation pattern detection settings
- temporal_detection: Time-based pattern detection settings
- trend_analysis: Trend direction and velocity settings
- intervention: Urgency levels and recommendations
- known_patterns: Named escalation pattern definitions
"""

import json
import os
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field

# Module version
__version__ = "v5.0-6-3.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Configuration Data Classes
# =============================================================================

@dataclass
class ContextAnalysisConfig:
    """Master context analysis configuration."""
    enabled: bool = True
    max_history_size: int = 20


@dataclass
class SeverityThreshold:
    """
    Per-severity escalation threshold (FE-005).
    
    Lower thresholds = more sensitive detection for that severity.
    """
    score_increase_threshold: float = 0.3
    minimum_messages: int = 3
    rapid_threshold_hours: int = 4


@dataclass
class ThresholdPreset:
    """
    Preset configuration for escalation detection sensitivity (FE-005).
    """
    name: str = "balanced"
    description: str = ""
    score_increase_threshold: float = 0.3
    minimum_messages: int = 3
    rapid_threshold_hours: int = 4


@dataclass
class EscalationDetectionConfig:
    """Escalation detection configuration with FE-005 per-severity thresholds."""
    enabled: bool = True
    rapid_threshold_hours: int = 4
    gradual_threshold_hours: int = 24
    score_increase_threshold: float = 0.3
    minimum_messages: int = 3
    alert_on_detection: bool = True
    alert_cooldown_seconds: int = 300
    # FE-005: Per-severity thresholds
    threshold_preset: str = "balanced"
    per_severity_thresholds: Dict[str, SeverityThreshold] = field(default_factory=dict)
    threshold_presets: Dict[str, ThresholdPreset] = field(default_factory=dict)
    
    def get_threshold_for_severity(self, severity: str) -> SeverityThreshold:
        """
        Get escalation threshold for a specific severity level (FE-005).
        
        Args:
            severity: Severity level (critical, high, medium, low, safe)
            
        Returns:
            SeverityThreshold for that level, or default if not found
        """
        return self.per_severity_thresholds.get(
            severity.lower(),
            SeverityThreshold(
                score_increase_threshold=self.score_increase_threshold,
                minimum_messages=self.minimum_messages,
                rapid_threshold_hours=self.rapid_threshold_hours,
            )
        )
    
    def get_preset(self, preset_name: str) -> Optional[ThresholdPreset]:
        """
        Get a threshold preset by name (FE-005).
        
        Args:
            preset_name: Preset name (conservative, balanced, sensitive)
            
        Returns:
            ThresholdPreset if found, None otherwise
        """
        return self.threshold_presets.get(preset_name.lower())


@dataclass
class TemporalDetectionConfig:
    """Temporal pattern detection configuration."""
    enabled: bool = True
    late_night_start_hour: int = 22
    late_night_end_hour: int = 4
    late_night_risk_modifier: float = 1.2
    rapid_posting_threshold_minutes: int = 30
    rapid_posting_message_count: int = 5
    weekend_risk_modifier: float = 1.1


@dataclass
class TrendAnalysisConfig:
    """Trend analysis configuration."""
    enabled: bool = True
    worsening_threshold: float = 0.15
    improving_threshold: float = -0.15
    velocity_rapid_threshold: float = 0.1
    velocity_gradual_threshold: float = 0.03


@dataclass
class InterventionConfig:
    """Intervention urgency configuration."""
    escalation_urgency_boost: bool = True
    late_night_urgency_boost: bool = True
    urgency_levels: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class KnownPattern:
    """Single known escalation pattern definition."""
    name: str
    description: str
    typical_duration_hours: int
    escalation_type: str  # rapid, gradual, sudden
    risk_level: str  # critical, high, medium, low


# =============================================================================
# Context Configuration Manager
# =============================================================================

class ContextConfigManager:
    """
    Configuration Manager for Phase 5 Context Analysis Features.
    
    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_context_config_manager)
    - JSON configuration with environment variable overrides
    - Resilient validation with safe fallbacks
    - Typed configuration dataclasses
    
    Attributes:
        config_dir: Path to configuration directory
        _raw_config: Raw JSON configuration
        _context_analysis: Resolved context analysis settings
        _escalation_detection: Resolved escalation detection settings
        _temporal_detection: Resolved temporal detection settings
        _trend_analysis: Resolved trend analysis settings
        _intervention: Resolved intervention settings
        _known_patterns: Dictionary of known escalation patterns
    """
    
    CONFIG_FILE = "context_config.json"
    
    def __init__(
        self,
        config_dir: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize ContextConfigManager.
        
        Args:
            config_dir: Path to configuration directory (default: ./config)
            
        Note:
            Use create_context_config_manager() factory function instead.
        """
        # Set configuration directory
        if config_dir is None:
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        # Initialize configuration storage
        self._raw_config: Dict[str, Any] = {}
        self._validation_errors: List[str] = []
        
        # Initialize typed configuration objects
        self._context_analysis = ContextAnalysisConfig()
        self._escalation_detection = EscalationDetectionConfig()
        self._temporal_detection = TemporalDetectionConfig()
        self._trend_analysis = TrendAnalysisConfig()
        self._intervention = InterventionConfig()
        self._known_patterns: Dict[str, KnownPattern] = {}
        
        # Load configuration
        self._load_configuration()
        
        logger.info(
            f"✅ ContextConfigManager v{__version__} initialized "
            f"(context_analysis: {'enabled' if self._context_analysis.enabled else 'disabled'})"
        )
    
    def _load_configuration(self) -> None:
        """
        Load context configuration from JSON and apply environment overrides.
        """
        config_path = self.config_dir / self.CONFIG_FILE
        
        logger.info(f"📂 Loading context configuration from: {config_path}")
        
        if config_path.exists():
            self._raw_config = self._load_json_file(config_path)
            if self._raw_config:
                self._resolve_configuration()
                logger.info("📝 Loaded Phase 5 context configuration")
            else:
                logger.warning("⚠️ Failed to parse context_config.json, using defaults")
                self._use_defaults()
        else:
            logger.warning(f"⚠️ Context config not found: {config_path}, using defaults")
            self._use_defaults()
    
    def _load_json_file(self, path: Path) -> Dict[str, Any]:
        """
        Load JSON file with error handling.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Parsed JSON as dictionary, empty dict on failure
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"📄 Loaded: {path}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in {path}: {e}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error loading {path}: {e}")
            return {}
    
    def _resolve_env_value(
        self, 
        value: Any, 
        default: Any,
        value_type: type = str
    ) -> Any:
        """
        Resolve a value that may be an environment variable reference.
        
        Args:
            value: The value to resolve (may be ${ENV_VAR} string)
            default: Default value if env var not set
            value_type: Expected type for conversion
            
        Returns:
            Resolved and type-converted value
        """
        # If not an env var reference, return as-is
        if not isinstance(value, str) or not value.startswith("${") or not value.endswith("}"):
            return value
        
        # Extract env var name
        env_var = value[2:-1]
        env_value = os.environ.get(env_var)
        
        if env_value is None:
            return default
        
        # Type conversion
        try:
            if value_type == bool:
                return env_value.lower() in ("true", "1", "yes", "on")
            elif value_type == int:
                return int(env_value)
            elif value_type == float:
                return float(env_value)
            else:
                return env_value
        except (ValueError, TypeError):
            logger.warning(f"⚠️ Failed to convert {env_var}='{env_value}' to {value_type.__name__}, using default")
            return default
    
    def _resolve_configuration(self) -> None:
        """
        Resolve all configuration sections with environment overrides.
        """
        # Resolve context_analysis section
        self._resolve_context_analysis()
        
        # Resolve escalation_detection section
        self._resolve_escalation_detection()
        
        # Resolve temporal_detection section
        self._resolve_temporal_detection()
        
        # Resolve trend_analysis section
        self._resolve_trend_analysis()
        
        # Resolve intervention section
        self._resolve_intervention()
        
        # Load known patterns
        self._load_known_patterns()
        
        # Log validation errors
        if self._validation_errors:
            logger.warning(f"⚠️ {len(self._validation_errors)} context config validation issues:")
            for error in self._validation_errors:
                logger.warning(f"  - {error}")
    
    def _resolve_context_analysis(self) -> None:
        """Resolve context_analysis configuration section."""
        section = self._raw_config.get("context_analysis", {})
        defaults = section.get("defaults", {})
        
        self._context_analysis = ContextAnalysisConfig(
            enabled=self._resolve_env_value(
                section.get("enabled", defaults.get("enabled", True)),
                defaults.get("enabled", True),
                bool
            ),
            max_history_size=self._resolve_env_value(
                section.get("max_history_size", defaults.get("max_history_size", 20)),
                defaults.get("max_history_size", 20),
                int
            ),
        )
        
        # Validate range
        if not (3 <= self._context_analysis.max_history_size <= 50):
            self._validation_errors.append(
                f"max_history_size={self._context_analysis.max_history_size} out of range [3, 50], clamping"
            )
            self._context_analysis.max_history_size = max(3, min(50, self._context_analysis.max_history_size))
    
    def _resolve_escalation_detection(self) -> None:
        """Resolve escalation_detection configuration section with FE-005 enhancements."""
        section = self._raw_config.get("escalation_detection", {})
        defaults = section.get("defaults", {})
        
        # Load per-severity thresholds (FE-005)
        per_severity_thresholds: Dict[str, SeverityThreshold] = {}
        per_severity_data = section.get("per_severity_thresholds", {})
        for severity, threshold_data in per_severity_data.items():
            if severity.startswith("_"):  # Skip metadata keys like _description
                continue
            if isinstance(threshold_data, dict):
                per_severity_thresholds[severity] = SeverityThreshold(
                    score_increase_threshold=threshold_data.get("score_increase_threshold", 0.3),
                    minimum_messages=threshold_data.get("minimum_messages", 3),
                    rapid_threshold_hours=threshold_data.get("rapid_threshold_hours", 4),
                )
        
        # Load threshold presets (FE-005)
        threshold_presets: Dict[str, ThresholdPreset] = {}
        presets_data = section.get("threshold_presets", {})
        for preset_name, preset_data in presets_data.items():
            if preset_name.startswith("_"):  # Skip metadata keys
                continue
            if isinstance(preset_data, dict):
                threshold_presets[preset_name] = ThresholdPreset(
                    name=preset_name,
                    description=preset_data.get("description", ""),
                    score_increase_threshold=preset_data.get("score_increase_threshold", 0.3),
                    minimum_messages=preset_data.get("minimum_messages", 3),
                    rapid_threshold_hours=preset_data.get("rapid_threshold_hours", 4),
                )
        
        self._escalation_detection = EscalationDetectionConfig(
            enabled=self._resolve_env_value(
                section.get("enabled"), defaults.get("enabled", True), bool
            ),
            rapid_threshold_hours=self._resolve_env_value(
                section.get("rapid_threshold_hours"), defaults.get("rapid_threshold_hours", 4), int
            ),
            gradual_threshold_hours=self._resolve_env_value(
                section.get("gradual_threshold_hours"), defaults.get("gradual_threshold_hours", 24), int
            ),
            score_increase_threshold=self._resolve_env_value(
                section.get("score_increase_threshold"), defaults.get("score_increase_threshold", 0.3), float
            ),
            minimum_messages=self._resolve_env_value(
                section.get("minimum_messages"), defaults.get("minimum_messages", 3), int
            ),
            alert_on_detection=self._resolve_env_value(
                section.get("alert_on_detection"), defaults.get("alert_on_detection", True), bool
            ),
            alert_cooldown_seconds=self._resolve_env_value(
                section.get("alert_cooldown_seconds"), defaults.get("alert_cooldown_seconds", 300), int
            ),
            # FE-005: Per-severity thresholds and presets
            threshold_preset=self._resolve_env_value(
                section.get("threshold_preset"), defaults.get("threshold_preset", "balanced"), str
            ),
            per_severity_thresholds=per_severity_thresholds,
            threshold_presets=threshold_presets,
        )
        
        # Log FE-005 config if any thresholds loaded
        if per_severity_thresholds:
            logger.debug(
                f"📊 Loaded {len(per_severity_thresholds)} per-severity thresholds (FE-005)"
            )
        if threshold_presets:
            logger.debug(
                f"📊 Loaded {len(threshold_presets)} threshold presets (FE-005): "
                f"{list(threshold_presets.keys())}"
            )
    
    def _resolve_temporal_detection(self) -> None:
        """Resolve temporal_detection configuration section."""
        section = self._raw_config.get("temporal_detection", {})
        defaults = section.get("defaults", {})
        
        self._temporal_detection = TemporalDetectionConfig(
            enabled=self._resolve_env_value(
                section.get("enabled"), defaults.get("enabled", True), bool
            ),
            late_night_start_hour=self._resolve_env_value(
                section.get("late_night_start_hour"), defaults.get("late_night_start_hour", 22), int
            ),
            late_night_end_hour=self._resolve_env_value(
                section.get("late_night_end_hour"), defaults.get("late_night_end_hour", 4), int
            ),
            late_night_risk_modifier=self._resolve_env_value(
                section.get("late_night_risk_modifier"), defaults.get("late_night_risk_modifier", 1.2), float
            ),
            rapid_posting_threshold_minutes=self._resolve_env_value(
                section.get("rapid_posting_threshold_minutes"), defaults.get("rapid_posting_threshold_minutes", 30), int
            ),
            rapid_posting_message_count=self._resolve_env_value(
                section.get("rapid_posting_message_count"), defaults.get("rapid_posting_message_count", 5), int
            ),
            weekend_risk_modifier=self._resolve_env_value(
                section.get("weekend_risk_modifier"), defaults.get("weekend_risk_modifier", 1.1), float
            ),
        )
    
    def _resolve_trend_analysis(self) -> None:
        """Resolve trend_analysis configuration section."""
        section = self._raw_config.get("trend_analysis", {})
        defaults = section.get("defaults", {})
        
        self._trend_analysis = TrendAnalysisConfig(
            enabled=self._resolve_env_value(
                section.get("enabled"), defaults.get("enabled", True), bool
            ),
            worsening_threshold=self._resolve_env_value(
                section.get("worsening_threshold"), defaults.get("worsening_threshold", 0.15), float
            ),
            improving_threshold=self._resolve_env_value(
                section.get("improving_threshold"), defaults.get("improving_threshold", -0.15), float
            ),
            velocity_rapid_threshold=self._resolve_env_value(
                section.get("velocity_rapid_threshold"), defaults.get("velocity_rapid_threshold", 0.1), float
            ),
            velocity_gradual_threshold=self._resolve_env_value(
                section.get("velocity_gradual_threshold"), defaults.get("velocity_gradual_threshold", 0.03), float
            ),
        )
    
    def _resolve_intervention(self) -> None:
        """Resolve intervention configuration section."""
        section = self._raw_config.get("intervention", {})
        defaults = section.get("defaults", {})
        
        self._intervention = InterventionConfig(
            escalation_urgency_boost=self._resolve_env_value(
                section.get("escalation_urgency_boost"), defaults.get("escalation_urgency_boost", True), bool
            ),
            late_night_urgency_boost=self._resolve_env_value(
                section.get("late_night_urgency_boost"), defaults.get("late_night_urgency_boost", True), bool
            ),
            urgency_levels=section.get("urgency_levels", {}),
        )
    
    def _load_known_patterns(self) -> None:
        """Load known escalation patterns from configuration."""
        patterns_section = self._raw_config.get("known_patterns", {})
        patterns = patterns_section.get("patterns", {})
        
        for name, pattern_data in patterns.items():
            try:
                self._known_patterns[name] = KnownPattern(
                    name=name,
                    description=pattern_data.get("description", ""),
                    typical_duration_hours=pattern_data.get("typical_duration_hours", 0),
                    escalation_type=pattern_data.get("escalation_type", "unknown"),
                    risk_level=pattern_data.get("risk_level", "medium"),
                )
            except Exception as e:
                logger.warning(f"⚠️ Failed to load pattern '{name}': {e}")
        
        logger.debug(f"📊 Loaded {len(self._known_patterns)} known escalation patterns")
    
    def _use_defaults(self) -> None:
        """Use default configuration values when config file not found."""
        self._context_analysis = ContextAnalysisConfig()
        self._escalation_detection = EscalationDetectionConfig()
        self._temporal_detection = TemporalDetectionConfig()
        self._trend_analysis = TrendAnalysisConfig()
        self._intervention = InterventionConfig()
        self._known_patterns = {}
    
    # =========================================================================
    # PUBLIC API - Typed Getters
    # =========================================================================
    
    def get_context_analysis_config(self) -> ContextAnalysisConfig:
        """
        Get context analysis master configuration.
        
        Returns:
            ContextAnalysisConfig with enabled flag and max_history_size
        """
        return self._context_analysis
    
    def get_escalation_detection_config(self) -> EscalationDetectionConfig:
        """
        Get escalation detection configuration.
        
        Returns:
            EscalationDetectionConfig with all escalation detection settings
        """
        return self._escalation_detection
    
    def get_temporal_detection_config(self) -> TemporalDetectionConfig:
        """
        Get temporal pattern detection configuration.
        
        Returns:
            TemporalDetectionConfig with late night, rapid posting settings
        """
        return self._temporal_detection
    
    def get_trend_analysis_config(self) -> TrendAnalysisConfig:
        """
        Get trend analysis configuration.
        
        Returns:
            TrendAnalysisConfig with threshold and velocity settings
        """
        return self._trend_analysis
    
    def get_intervention_config(self) -> InterventionConfig:
        """
        Get intervention urgency configuration.
        
        Returns:
            InterventionConfig with urgency boosts and level definitions
        """
        return self._intervention
    
    def get_known_patterns(self) -> Dict[str, KnownPattern]:
        """
        Get dictionary of known escalation patterns.
        
        Returns:
            Dictionary mapping pattern name to KnownPattern dataclass
        """
        return self._known_patterns.copy()
    
    def get_pattern(self, pattern_name: str) -> Optional[KnownPattern]:
        """
        Get a specific known escalation pattern by name.
        
        Args:
            pattern_name: Name of the pattern (e.g., "evening_deterioration")
            
        Returns:
            KnownPattern if found, None otherwise
        """
        return self._known_patterns.get(pattern_name)
    
    def get_pattern_names(self) -> List[str]:
        """
        Get list of all known pattern names.
        
        Returns:
            List of pattern name strings
        """
        return list(self._known_patterns.keys())
    
    # =========================================================================
    # Convenience Properties
    # =========================================================================
    
    @property
    def is_enabled(self) -> bool:
        """Check if context analysis is enabled."""
        return self._context_analysis.enabled
    
    @property
    def max_history_size(self) -> int:
        """Get maximum message history size."""
        return self._context_analysis.max_history_size
    
    @property
    def escalation_enabled(self) -> bool:
        """Check if escalation detection is enabled."""
        return self._escalation_detection.enabled
    
    @property
    def temporal_enabled(self) -> bool:
        """Check if temporal detection is enabled."""
        return self._temporal_detection.enabled
    
    @property
    def trend_enabled(self) -> bool:
        """Check if trend analysis is enabled."""
        return self._trend_analysis.enabled
    
    @property
    def alert_cooldown_seconds(self) -> int:
        """Get escalation alert cooldown in seconds."""
        return self._escalation_detection.alert_cooldown_seconds
    
    # =========================================================================
    # Dictionary Export for API
    # =========================================================================
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export configuration as dictionary for API responses.
        
        Returns:
            Dictionary representation of all context configuration
        """
        return {
            "context_analysis": {
                "enabled": self._context_analysis.enabled,
                "max_history_size": self._context_analysis.max_history_size,
            },
            "escalation_detection": {
                "enabled": self._escalation_detection.enabled,
                "rapid_threshold_hours": self._escalation_detection.rapid_threshold_hours,
                "gradual_threshold_hours": self._escalation_detection.gradual_threshold_hours,
                "score_increase_threshold": self._escalation_detection.score_increase_threshold,
                "minimum_messages": self._escalation_detection.minimum_messages,
                "alert_on_detection": self._escalation_detection.alert_on_detection,
                "alert_cooldown_seconds": self._escalation_detection.alert_cooldown_seconds,
            },
            "temporal_detection": {
                "enabled": self._temporal_detection.enabled,
                "late_night_start_hour": self._temporal_detection.late_night_start_hour,
                "late_night_end_hour": self._temporal_detection.late_night_end_hour,
                "late_night_risk_modifier": self._temporal_detection.late_night_risk_modifier,
                "rapid_posting_threshold_minutes": self._temporal_detection.rapid_posting_threshold_minutes,
                "rapid_posting_message_count": self._temporal_detection.rapid_posting_message_count,
                "weekend_risk_modifier": self._temporal_detection.weekend_risk_modifier,
            },
            "trend_analysis": {
                "enabled": self._trend_analysis.enabled,
                "worsening_threshold": self._trend_analysis.worsening_threshold,
                "improving_threshold": self._trend_analysis.improving_threshold,
                "velocity_rapid_threshold": self._trend_analysis.velocity_rapid_threshold,
                "velocity_gradual_threshold": self._trend_analysis.velocity_gradual_threshold,
            },
            "intervention": {
                "escalation_urgency_boost": self._intervention.escalation_urgency_boost,
                "late_night_urgency_boost": self._intervention.late_night_urgency_boost,
            },
            "known_pattern_count": len(self._known_patterns),
        }
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors encountered during loading."""
        return self._validation_errors.copy()
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ContextConfigManager("
            f"enabled={self.is_enabled}, "
            f"max_history={self.max_history_size}, "
            f"patterns={len(self._known_patterns)})"
        )


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================

def create_context_config_manager(
    config_dir: Optional[Union[str, Path]] = None,
) -> ContextConfigManager:
    """
    Factory function for ContextConfigManager (Clean Architecture v5.1 Pattern).
    
    This is the ONLY way to create a ContextConfigManager instance.
    Direct instantiation should be avoided in production code.
    
    Args:
        config_dir: Path to configuration directory (default: auto-detect)
        
    Returns:
        Configured ContextConfigManager instance
        
    Example:
        >>> context_config = create_context_config_manager()
        >>> context_config = create_context_config_manager(config_dir="/custom/path")
        >>> 
        >>> # Check if context analysis is enabled
        >>> if context_config.is_enabled:
        ...     escalation_config = context_config.get_escalation_detection_config()
    """
    logger.info("🏭 Creating ContextConfigManager")
    
    return ContextConfigManager(config_dir=config_dir)


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    # Manager
    "ContextConfigManager",
    "create_context_config_manager",
    # Config dataclasses
    "ContextAnalysisConfig",
    "EscalationDetectionConfig",
    "TemporalDetectionConfig",
    "TrendAnalysisConfig",
    "InterventionConfig",
    "KnownPattern",
    # FE-005: Per-severity thresholds
    "SeverityThreshold",
    "ThresholdPreset",
]
