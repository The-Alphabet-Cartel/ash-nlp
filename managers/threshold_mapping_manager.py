# ash-nlp/managers/threshold_mapping_manager.py
"""
Phase 3c: Threshold Mapping Configuration Manager
Mode-aware threshold management with fail-fast validation and learning system integration

Clean v3.1 Architecture - NO backward compatibility
"""

import os
import json
import logging
import copy
from typing import Dict, Any, Optional, List
from managers.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class ThresholdMappingManager:
    """
    Mode-Aware Threshold Mapping Manager - Phase 3c
    
    Manages crisis level mapping thresholds with support for multiple ensemble modes.
    Provides fail-fast validation and learning system integration.
    
    Architecture: Clean v3.1 with mode-aware threshold loading
    """
    
    def __init__(self, config_manager: ConfigManager, model_ensemble_manager=None):
        """
        Initialize ThresholdMappingManager with mode awareness
        
        Args:
            config_manager: ConfigManager instance for loading JSON configuration
            model_ensemble_manager: ModelEnsembleManager for current ensemble mode detection
        """
        self.config_manager = config_manager
        self.model_ensemble_manager = model_ensemble_manager
        self._processed_config = None
        self._validation_errors = []
        
        # Load and validate configuration
        self._load_configuration()
        
        if self._validation_errors and self._should_fail_fast():
            error_summary = "; ".join(self._validation_errors)
            logger.critical(f"🚨 FAIL-FAST: Invalid threshold configuration: {error_summary}")
            raise ValueError(f"Invalid threshold mapping configuration: {error_summary}")
        
        logger.info("✅ ThresholdMappingManager initialized successfully with mode-aware thresholds")
    
    def _load_configuration(self) -> None:
        """Load and process threshold mapping configuration with environment overrides"""
        try:
            # Load base configuration
            base_config = self.config_manager.load_config_file('threshold_mapping')
            
            if not base_config:
                logger.error("❌ No threshold_mapping.json configuration found")
                self._validation_errors.append("Missing threshold_mapping.json file")
                return
            
            # Apply environment variable overrides
            self._processed_config = self._apply_environment_overrides(base_config)
            
            # Validate configuration
            self._validate_configuration()
            
            logger.info("✅ Threshold mapping configuration loaded and validated")
            
        except Exception as e:
            logger.error(f"❌ Error loading threshold mapping configuration: {e}")
            self._validation_errors.append(f"Configuration loading error: {str(e)}")
    
    def _apply_environment_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration"""
        # Use deep copy to prevent mutation of original config
        processed_config = copy.deepcopy(config)
        
        # Mode-specific overrides - only process modes that exist in config
        available_modes = []
        if 'threshold_mapping_by_mode' in processed_config:
            available_modes = list(processed_config['threshold_mapping_by_mode'].keys())
        
        # Apply overrides to available modes (don't create new modes)
        for mode in available_modes:
            mode_config = processed_config['threshold_mapping_by_mode'][mode]
            
            # Crisis level mapping overrides
            if 'crisis_level_mapping' in mode_config:
                mapping = mode_config['crisis_level_mapping']
                mapping['crisis_to_high'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_CRISIS_TO_HIGH', 
                    mapping.get('crisis_to_high', 0.5)
                ))
                mapping['crisis_to_medium'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_CRISIS_TO_MEDIUM', 
                    mapping.get('crisis_to_medium', 0.3)
                ))
                mapping['mild_crisis_to_low'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_MILD_CRISIS_TO_LOW', 
                    mapping.get('mild_crisis_to_low', 0.4)
                ))
                mapping['negative_to_low'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_NEGATIVE_TO_LOW', 
                    mapping.get('negative_to_low', 0.7)
                ))
                mapping['unknown_to_low'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_UNKNOWN_TO_LOW', 
                    mapping.get('unknown_to_low', 0.5)
                ))
            
            # Ensemble threshold overrides
            if 'ensemble_thresholds' in mode_config:
                thresholds = mode_config['ensemble_thresholds']
                thresholds['high'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_ENSEMBLE_HIGH', 
                    thresholds.get('high', 0.45)
                ))
                thresholds['medium'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_ENSEMBLE_MEDIUM', 
                    thresholds.get('medium', 0.25)
                ))
                thresholds['low'] = float(os.getenv(
                    f'NLP_THRESHOLD_{mode.upper()}_ENSEMBLE_LOW', 
                    thresholds.get('low', 0.12)
                ))
        
        # Shared configuration overrides (same as before)
        if 'shared_configuration' in processed_config:
            shared = processed_config['shared_configuration']
            
            # Staff review overrides
            if 'staff_review' in shared:
                staff_review = shared['staff_review']
                staff_review['medium_confidence_threshold'] = float(os.getenv(
                    'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE',
                    staff_review.get('medium_confidence_threshold', 0.45)
                ))
                staff_review['low_confidence_threshold'] = float(os.getenv(
                    'NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE',
                    staff_review.get('low_confidence_threshold', 0.75)
                ))
                staff_review['high_always'] = self._parse_boolean_env_var(
                    'NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', 
                    staff_review.get('high_always', True)
                )
            
            # Learning system overrides
            if 'learning_system' in shared:
                learning = shared['learning_system']
                learning['feedback_weight'] = float(os.getenv(
                    'NLP_THRESHOLD_LEARNING_FEEDBACK_WEIGHT',
                    learning.get('feedback_weight', 0.1)
                ))
                learning['enable_threshold_learning'] = self._parse_boolean_env_var(
                    'NLP_THRESHOLD_LEARNING_ENABLED',
                    learning.get('enable_threshold_learning', True)
                )
            
            # Safety controls overrides
            if 'safety_controls' in shared:
                safety = shared['safety_controls']
                safety['consensus_safety_bias'] = float(os.getenv(
                    'NLP_THRESHOLD_SAFETY_BIAS',
                    safety.get('consensus_safety_bias', 0.03)
                ))
                safety['enable_safety_override'] = self._parse_boolean_env_var(
                    'NLP_THRESHOLD_ENABLE_SAFETY_OVERRIDE',
                    safety.get('enable_safety_override', True)
                )
        
        return processed_config
    
    def _parse_boolean_env_var(self, env_var: str, default_value: bool) -> bool:
        """Parse boolean environment variable with proper validation"""
        env_value = os.getenv(env_var)
        if env_value is None:
            return default_value
        
        # Handle various boolean representations
        env_lower = env_value.lower().strip()
        if env_lower in ('true', '1', 'yes', 'on', 'enabled'):
            return True
        elif env_lower in ('false', '0', 'no', 'off', 'disabled'):
            return False
        else:
            # Invalid boolean value should cause validation error
            self._validation_errors.append(f"Invalid boolean value for {env_var}: '{env_value}' (expected true/false)")
            return default_value

    def _validate_configuration(self) -> None:
        """Validate threshold configuration with fail-fast checking - DIAGNOSTIC VERSION"""
        logger.debug(f"🔍 Starting validation. Processed config exists: {self._processed_config is not None}")
        
        if not self._processed_config:
            self._validation_errors.append("No configuration to validate")
            return
        
        logger.debug(f"🔍 Processed config keys: {list(self._processed_config.keys())}")
        
        # Validate mode-specific thresholds
        if 'threshold_mapping_by_mode' in self._processed_config:
            modes = self._processed_config['threshold_mapping_by_mode']
            logger.debug(f"🔍 Found modes: {list(modes.keys())}")
            
            for mode, mode_config in modes.items():
                logger.debug(f"🔍 Validating mode {mode}")
                self._validate_mode_thresholds(mode, mode_config)
        else:
            logger.debug("🔍 No threshold_mapping_by_mode found")
        
        # Validate shared configuration
        if 'shared_configuration' in self._processed_config:
            logger.debug(f"🔍 Validating shared configuration")
            self._validate_shared_configuration(self._processed_config['shared_configuration'])
        else:
            logger.debug("🔍 No shared_configuration found")
        
        # Cross-mode validation
        self._validate_cross_mode_consistency()
        
        total_errors = len(self._validation_errors)
        logger.debug(f"🔍 Validation complete. Total errors: {total_errors}")
        logger.debug(f"🔍 Error details: {self._validation_errors}")
        
        if self._validation_errors:
            logger.warning(f"⚠️ Threshold validation found {total_errors} issues")
        else:
            logger.info("✅ All threshold validation checks passed")
    
    def _validate_mode_thresholds(self, mode: str, mode_config: Dict[str, Any]) -> None:
        """Validate thresholds for a specific ensemble mode with strict checking - DIAGNOSTIC VERSION"""
        mode_name = mode.upper()
        logger.debug(f"🔍 Validating mode: {mode_name}, config: {mode_config}")
        
        # Validate crisis level mapping
        if 'crisis_level_mapping' in mode_config:
            mapping = mode_config['crisis_level_mapping']
            logger.debug(f"🔍 Validating crisis mapping: {mapping}")
            
            # Validate each threshold individually
            for threshold_name, value in mapping.items():
                logger.debug(f"🔍 Checking {threshold_name} = {value} (type: {type(value)})")
                
                # Type validation
                if not isinstance(value, (int, float)):
                    error_msg = f"{mode_name} {threshold_name}: must be numeric, got {type(value).__name__}"
                    logger.debug(f"❌ Type error: {error_msg}")
                    self._validation_errors.append(error_msg)
                    continue
                
                # Range validation
                if value < 0.0 or value > 1.0:
                    error_msg = f"{mode_name} {threshold_name}: {value} not in valid range [0.0, 1.0]"
                    logger.debug(f"❌ Range error: {error_msg}")
                    self._validation_errors.append(error_msg)
            
            # Ordering validation for crisis thresholds
            crisis_high = mapping.get('crisis_to_high')
            crisis_medium = mapping.get('crisis_to_medium')
            
            logger.debug(f"🔍 Checking ordering: high={crisis_high}, medium={crisis_medium}")
            
            if (isinstance(crisis_high, (int, float)) and isinstance(crisis_medium, (int, float)) and 
                crisis_high <= crisis_medium):
                error_msg = f"{mode_name} crisis_to_high ({crisis_high}) must be > crisis_to_medium ({crisis_medium})"
                logger.debug(f"❌ Ordering error: {error_msg}")
                self._validation_errors.append(error_msg)
        
        # Validate ensemble thresholds
        if 'ensemble_thresholds' in mode_config:
            thresholds = mode_config['ensemble_thresholds']
            logger.debug(f"🔍 Validating ensemble thresholds: {thresholds}")
            
            high = thresholds.get('high')
            medium = thresholds.get('medium')
            low = thresholds.get('low')
            
            # Type and range validation
            for name, value in [('high', high), ('medium', medium), ('low', low)]:
                if value is not None:
                    logger.debug(f"🔍 Checking ensemble {name} = {value} (type: {type(value)})")
                    
                    if not isinstance(value, (int, float)):
                        error_msg = f"{mode_name} ensemble {name}: must be numeric, got {type(value).__name__}"
                        logger.debug(f"❌ Ensemble type error: {error_msg}")
                        self._validation_errors.append(error_msg)
                        continue
                    if value < 0.0 or value > 1.0:
                        error_msg = f"{mode_name} ensemble {name}: {value} not in valid range [0.0, 1.0]"
                        logger.debug(f"❌ Ensemble range error: {error_msg}")
                        self._validation_errors.append(error_msg)
            
            # Ordering validation: high > medium > low
            if (isinstance(high, (int, float)) and isinstance(medium, (int, float)) and isinstance(low, (int, float))):
                logger.debug(f"🔍 Checking ensemble ordering: high={high}, medium={medium}, low={low}")
                
                if high <= medium:
                    error_msg = f"{mode_name} ensemble: high ({high}) must be > medium ({medium})"
                    logger.debug(f"❌ Ensemble ordering error: {error_msg}")
                    self._validation_errors.append(error_msg)
                if medium <= low:
                    error_msg = f"{mode_name} ensemble: medium ({medium}) must be > low ({low})"
                    logger.debug(f"❌ Ensemble ordering error: {error_msg}")
                    self._validation_errors.append(error_msg)
        
        logger.debug(f"🔍 Mode validation complete. Current errors: {len(self._validation_errors)}")
    
    def _validate_shared_configuration(self, shared_config: Dict[str, Any]) -> None:
        """Validate shared configuration parameters with strict checking - DIAGNOSTIC VERSION"""
        logger.debug(f"🔍 Validating shared config: {shared_config}")
        
        # Validate staff review thresholds
        if 'staff_review' in shared_config:
            staff = shared_config['staff_review']
            logger.debug(f"🔍 Validating staff review: {staff}")
            
            medium_threshold = staff.get('medium_confidence_threshold')
            low_threshold = staff.get('low_confidence_threshold')
            high_always = staff.get('high_always')
            
            # Type and range validation
            if medium_threshold is not None:
                logger.debug(f"🔍 Checking medium_threshold = {medium_threshold} (type: {type(medium_threshold)})")
                if not isinstance(medium_threshold, (int, float)):
                    error_msg = f"Staff review medium_confidence_threshold must be numeric, got {type(medium_threshold).__name__}"
                    logger.debug(f"❌ Staff review type error: {error_msg}")
                    self._validation_errors.append(error_msg)
                elif medium_threshold < 0.0 or medium_threshold > 1.0:
                    error_msg = f"Staff review medium_confidence_threshold ({medium_threshold}) must be between 0.0 and 1.0"
                    logger.debug(f"❌ Staff review range error: {error_msg}")
                    self._validation_errors.append(error_msg)
            
            if low_threshold is not None:
                logger.debug(f"🔍 Checking low_threshold = {low_threshold} (type: {type(low_threshold)})")
                if not isinstance(low_threshold, (int, float)):
                    error_msg = f"Staff review low_confidence_threshold must be numeric, got {type(low_threshold).__name__}"
                    logger.debug(f"❌ Staff review type error: {error_msg}")
                    self._validation_errors.append(error_msg)
                elif low_threshold < 0.0 or low_threshold > 1.0:
                    error_msg = f"Staff review low_confidence_threshold ({low_threshold}) must be between 0.0 and 1.0"
                    logger.debug(f"❌ Staff review range error: {error_msg}")
                    self._validation_errors.append(error_msg)
            
            # Ordering validation
            if (isinstance(medium_threshold, (int, float)) and isinstance(low_threshold, (int, float)) and 
                low_threshold <= medium_threshold):
                error_msg = f"Staff review: low_confidence_threshold ({low_threshold}) must be > medium_confidence_threshold ({medium_threshold})"
                logger.debug(f"❌ Staff review ordering error: {error_msg}")
                self._validation_errors.append(error_msg)
        
        # Validate learning system parameters
        if 'learning_system' in shared_config:
            learning = shared_config['learning_system']
            logger.debug(f"🔍 Validating learning system: {learning}")
            
            feedback_weight = learning.get('feedback_weight')
            
            if feedback_weight is not None:
                logger.debug(f"🔍 Checking feedback_weight = {feedback_weight} (type: {type(feedback_weight)})")
                if not isinstance(feedback_weight, (int, float)) or feedback_weight < 0.0 or feedback_weight > 1.0:
                    error_msg = f"Learning system feedback_weight ({feedback_weight}) must be between 0.0 and 1.0"
                    logger.debug(f"❌ Learning system error: {error_msg}")
                    self._validation_errors.append(error_msg)
        
        # Validate safety controls
        if 'safety_controls' in shared_config:
            safety = shared_config['safety_controls']
            logger.debug(f"🔍 Validating safety controls: {safety}")
            
            safety_bias = safety.get('consensus_safety_bias')
            
            if safety_bias is not None:
                logger.debug(f"🔍 Checking safety_bias = {safety_bias} (type: {type(safety_bias)})")
                if not isinstance(safety_bias, (int, float)) or safety_bias < 0.0 or safety_bias > 0.2:
                    error_msg = f"Safety controls consensus_safety_bias ({safety_bias}) must be between 0.0 and 0.2"
                    logger.debug(f"❌ Safety controls error: {error_msg}")
                    self._validation_errors.append(error_msg)
        
        logger.debug(f"🔍 Shared config validation complete. Current errors: {len(self._validation_errors)}")
    
    def _validate_cross_mode_consistency(self) -> None:
        """Validate consistency across ensemble modes (only validates modes that are present)"""
        if not self._processed_config or 'threshold_mapping_by_mode' not in self._processed_config:
            return
        
        modes = self._processed_config['threshold_mapping_by_mode']
        
        # DO NOT require all modes - server runs single mode at startup
        # Only validate whatever modes are actually present in the configuration
        
        # Get the current/expected mode
        current_mode = self.get_current_ensemble_mode()
        
        # Validate that the current mode has configuration (if we can determine it)
        if current_mode and current_mode not in modes:
            logger.warning(f"⚠️ Current ensemble mode '{current_mode}' not found in configuration, will use defaults")
        
        # Only validate consistency between modes if multiple modes are present
        # This is for deployments that have multiple mode configurations
        if len(modes) >= 2:
            crisis_high_values = []
            crisis_medium_values = []
            
            for mode, config in modes.items():
                if 'crisis_level_mapping' in config:
                    crisis_mapping = config['crisis_level_mapping']
                    high_val = crisis_mapping.get('crisis_to_high')
                    medium_val = crisis_mapping.get('crisis_to_medium')
                    
                    if isinstance(high_val, (int, float)):
                        crisis_high_values.append(high_val)
                    if isinstance(medium_val, (int, float)):
                        crisis_medium_values.append(medium_val)
            
            # Warn (don't error) if there's too much variation between modes
            # This is informational for multi-mode deployments
            if len(crisis_high_values) >= 2:
                high_range = max(crisis_high_values) - min(crisis_high_values)
                if high_range > 0.3:
                    logger.warning(
                        f"⚠️ Crisis high thresholds vary significantly across modes: range = {high_range:.3f} "
                        f"(this may be intentional for different ensemble strategies)"
                    )
            
            if len(crisis_medium_values) >= 2:
                medium_range = max(crisis_medium_values) - min(crisis_medium_values)
                if medium_range > 0.3:
                    logger.warning(
                        f"⚠️ Crisis medium thresholds vary significantly across modes: range = {medium_range:.3f} "
                        f"(this may be intentional for different ensemble strategies)"
                    )
    
    def _should_fail_fast(self) -> bool:
        """Determine if configuration errors should cause startup failure"""
        fail_fast_env = os.getenv('NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID')
        if fail_fast_env is not None:
            # Use proper boolean parsing
            env_lower = fail_fast_env.lower().strip()
            if env_lower in ('true', '1', 'yes', 'on', 'enabled'):
                return True
            elif env_lower in ('false', '0', 'no', 'off', 'disabled'):
                return False
        
        # Default to True (fail-fast enabled by default)
        return True
    
    def get_current_ensemble_mode(self) -> str:
        """Get the current ensemble mode from ModelEnsembleManager"""
        if self.model_ensemble_manager:
            try:
                return self.model_ensemble_manager.get_current_ensemble_mode()
            except Exception as e:
                logger.warning(f"⚠️ Could not get current ensemble mode: {e}")
        
        # Fallback to environment variable or default
        return os.getenv('NLP_ENSEMBLE_MODE', 'weighted')
    
    def get_crisis_level_mapping_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get crisis level mapping thresholds for specified or current ensemble mode
        
        Args:
            mode: Specific ensemble mode ('consensus', 'majority', 'weighted') or None for current
            
        Returns:
            Dictionary of crisis level mapping thresholds
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        if not self._processed_config or 'threshold_mapping_by_mode' not in self._processed_config:
            logger.warning("⚠️ No threshold configuration available, using defaults")
            return self._get_default_crisis_mapping()
        
        mode_config = self._processed_config['threshold_mapping_by_mode'].get(mode, {})
        crisis_mapping = mode_config.get('crisis_level_mapping', {})
        
        if not crisis_mapping:
            logger.warning(f"⚠️ No crisis mapping for mode '{mode}', using defaults")
            return self._get_default_crisis_mapping()
        
        return crisis_mapping
    
    def get_ensemble_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get ensemble thresholds for specified or current ensemble mode
        
        Args:
            mode: Specific ensemble mode or None for current
            
        Returns:
            Dictionary of ensemble thresholds (high, medium, low)
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        if not self._processed_config or 'threshold_mapping_by_mode' not in self._processed_config:
            logger.warning("⚠️ No threshold configuration available, using defaults")
            return self._get_default_ensemble_thresholds()
        
        mode_config = self._processed_config['threshold_mapping_by_mode'].get(mode, {})
        ensemble_thresholds = mode_config.get('ensemble_thresholds', {})
        
        if not ensemble_thresholds:
            logger.warning(f"⚠️ No ensemble thresholds for mode '{mode}', using defaults")
            return self._get_default_ensemble_thresholds()
        
        return ensemble_thresholds
    
    def get_staff_review_config(self) -> Dict[str, Any]:
        """Get staff review configuration"""
        if not self._processed_config or 'shared_configuration' not in self._processed_config:
            return self._get_default_staff_review_config()
        
        shared = self._processed_config['shared_configuration']
        return shared.get('staff_review', self._get_default_staff_review_config())
    
    def get_learning_system_config(self) -> Dict[str, Any]:
        """Get learning system configuration"""
        if not self._processed_config or 'shared_configuration' not in self._processed_config:
            return self._get_default_learning_config()
        
        shared = self._processed_config['shared_configuration']
        return shared.get('learning_system', self._get_default_learning_config())
    
    def get_safety_controls_config(self) -> Dict[str, Any]:
        """Get safety controls configuration"""
        if not self._processed_config or 'shared_configuration' not in self._processed_config:
            return self._get_default_safety_config()
        
        shared = self._processed_config['shared_configuration']
        return shared.get('safety_controls', self._get_default_safety_config())
    
    def get_pattern_integration_config(self) -> Dict[str, Any]:
        """Get pattern integration configuration"""
        if not self._processed_config or 'shared_configuration' not in self._processed_config:
            return self._get_default_pattern_integration_config()
        
        shared = self._processed_config['shared_configuration']
        return shared.get('pattern_integration', self._get_default_pattern_integration_config())
    
    def get_gap_detection_config(self) -> Dict[str, Any]:
        """Get gap detection configuration"""
        if not self._processed_config or 'shared_configuration' not in self._processed_config:
            return self._get_default_gap_detection_config()
        
        shared = self._processed_config['shared_configuration']
        return shared.get('gap_detection', self._get_default_gap_detection_config())
    
    def is_staff_review_required(self, crisis_level: str, confidence: float, 
                                has_model_disagreement: bool = False, 
                                has_gap_detection: bool = False) -> bool:
        """
        Determine if a case requires staff review based on configuration
        
        Args:
            crisis_level: Detected crisis level ('high', 'medium', 'low', 'none')
            confidence: Confidence score (0.0 to 1.0)
            has_model_disagreement: Whether models disagreed
            has_gap_detection: Whether gap was detected
            
        Returns:
            True if staff review is required
        """
        staff_config = self.get_staff_review_config()
        
        # High crisis always requires review
        if crisis_level == 'high' and staff_config.get('high_always', True):
            return True
        
        # Medium crisis with high confidence
        if (crisis_level == 'medium' and 
            confidence >= staff_config.get('medium_confidence_threshold', 0.45)):
            return True
        
        # Low crisis with very high confidence
        if (crisis_level == 'low' and 
            confidence >= staff_config.get('low_confidence_threshold', 0.75)):
            return True
        
        # Model disagreement requires review
        if has_model_disagreement and staff_config.get('on_model_disagreement', True):
            return True
        
        # Gap detection requires review
        if has_gap_detection and staff_config.get('gap_detection_review', True):
            return True
        
        return False
    
    def adjust_threshold_with_learning(self, threshold_name: str, mode: str, 
                                     adjustment: float) -> bool:
        """
        Adjust threshold based on learning system feedback
        
        Args:
            threshold_name: Name of threshold to adjust
            mode: Ensemble mode
            adjustment: Adjustment amount (-1.0 to 1.0)
            
        Returns:
            True if adjustment was applied
        """
        learning_config = self.get_learning_system_config()
        
        if not learning_config.get('enable_threshold_learning', True):
            return False
        
        # Apply learning rate and limits
        learning_rate = learning_config.get('learning_rate', 0.01)
        max_adjustment = learning_config.get('confidence_adjustment_limit', 0.05)
        
        # Scale adjustment by learning rate and clamp to max
        scaled_adjustment = adjustment * learning_rate
        scaled_adjustment = max(-max_adjustment, min(max_adjustment, scaled_adjustment))
        
        logger.info(f"🎓 Learning adjustment: {threshold_name} in {mode} mode by {scaled_adjustment:.4f}")
        
        # In a real implementation, this would update the configuration
        # For now, just log the learning action
        return True
    
    def _get_default_crisis_mapping(self) -> Dict[str, float]:
        """Get default crisis level mapping"""
        return {
            'crisis_to_high': 0.50,
            'crisis_to_medium': 0.30,
            'mild_crisis_to_low': 0.40,
            'negative_to_low': 0.70,
            'unknown_to_low': 0.50
        }
    
    def _get_default_ensemble_thresholds(self) -> Dict[str, float]:
        """Get default ensemble thresholds"""
        return {
            'high': 0.45,
            'medium': 0.25,
            'low': 0.12
        }
    
    def _get_default_staff_review_config(self) -> Dict[str, Any]:
        """Get default staff review configuration"""
        return {
            'high_always': True,
            'medium_confidence_threshold': 0.45,
            'low_confidence_threshold': 0.75,
            'on_model_disagreement': True,
            'gap_detection_review': True
        }
    
    def _get_default_learning_config(self) -> Dict[str, Any]:
        """Get default learning system configuration"""
        return {
            'feedback_weight': 0.1,
            'min_samples_for_update': 5,
            'confidence_adjustment_limit': 0.05,
            'enable_threshold_learning': True,
            'learning_rate': 0.01
        }
    
    def _get_default_safety_config(self) -> Dict[str, Any]:
        """Get default safety controls configuration"""
        return {
            'consensus_safety_bias': 0.03,
            'enable_safety_override': True,
            'minimum_response_threshold': 0.10,
            'fail_safe_escalation': True
        }
    
    def _get_default_pattern_integration_config(self) -> Dict[str, Any]:
        """Get default pattern integration configuration"""
        return {
            'pattern_weight_multiplier': 1.2,
            'confidence_boost_limit': 0.15,
            'escalation_required_minimum': 'low',
            'pattern_override_threshold': 0.8
        }
    
    def _get_default_gap_detection_config(self) -> Dict[str, Any]:
        """Get default gap detection configuration"""
        return {
            'threshold': 0.25,
            'disagreement_threshold': 0.30,
            'enable_automatic_escalation': True
        }
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary for debugging"""
        return {
            'configuration_loaded': self._processed_config is not None,
            'validation_errors': len(self._validation_errors),
            'error_details': self._validation_errors,
            'current_ensemble_mode': self.get_current_ensemble_mode(),
            'fail_fast_enabled': self._should_fail_fast()
        }

# Factory function for clean v3.1 architecture
def create_threshold_mapping_manager(config_manager: ConfigManager, 
                                   model_ensemble_manager=None) -> ThresholdMappingManager:
    """
    Create ThresholdMappingManager instance following v3.1 clean architecture
    
    Args:
        config_manager: ConfigManager instance
        model_ensemble_manager: Optional ModelEnsembleManager for mode detection
        
    Returns:
        Configured ThresholdMappingManager instance
    """
    return ThresholdMappingManager(config_manager, model_ensemble_manager)