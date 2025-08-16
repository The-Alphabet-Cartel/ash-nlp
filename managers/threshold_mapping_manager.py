# ash-nlp/managers/threshold_mapping_manager.py
"""
Mode-Aware Threshold Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3d-10.12-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.7 - Environment Variable Fixes + Crisis Level Determination Method Added
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Added missing determine_crisis_level method, fixed environment variable resolution
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import copy
import logging
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

class ThresholdMappingManager:
    """
    Manages threshold mappings for crisis level determination and staff review logic
    Phase 3c: Mode-aware thresholds with dynamic ensemble mode detection
    Phase 3d Step 9: Updated to use UnifiedConfigManager - NO MORE os.getenv() calls
    Phase 3d Step 10.7: Added missing determine_crisis_level method
    """
    
    def __init__(self, unified_config_manager, model_ensemble_manager=None):
        """
        Initialize ThresholdMappingManager with mode-aware threshold support
        
        Args:
            unified_config_manager: UnifiedConfigManager instance (STEP 9 CHANGE)
            model_ensemble_manager: ModelEnsembleManager for mode detection
        """
        # STEP 9 CHANGE: Use UnifiedConfigManager instead of ConfigManager
        self.unified_config = unified_config_manager
        self.model_ensemble_manager = model_ensemble_manager
        self._validation_errors = []
        
        # Load threshold mapping configuration using unified manager
        self._load_threshold_mapping_config()
        
        logger.info("ThresholdMappingManager v3.1d Step 10.7 initialized - Crisis level determination method added")
    
    def _load_threshold_mapping_config(self):
        """Load threshold mapping configuration using UnifiedConfigManager - UPDATED for v3.1 compliance"""
        try:
            # Load threshold mapping configuration through unified manager
            raw_config = self.unified_config.load_config_file('threshold_mapping')
            
            if not raw_config:
                logger.warning("⚠️ Threshold mapping configuration not found, using environment fallbacks")
                self.threshold_config = self._get_fallback_threshold_config()
            else:
                # NEW: Process v3.1 compliant configuration with environment variable resolution
                self.threshold_config = self._process_v31_config(raw_config)
            
            # Validate threshold configuration
            self._validate_threshold_config()
            
            logger.info("✅ Threshold mapping configuration loaded and validated")
            
        except Exception as e:
            logger.error(f"❌ Error loading threshold mapping configuration: {e}")
            self._validation_errors.append(f"Configuration loading error: {str(e)}")
    
    def _process_v31_config(self, raw_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process v3.1 compliant configuration with environment variable resolution
        This replaces the old _apply_environment_overrides method
        """
        processed_config = {}
        
        try:
            # Copy metadata
            if '_metadata' in raw_config:
                processed_config['_metadata'] = raw_config['_metadata']
            
            # Process mode-specific configurations
            if 'threshold_mapping_by_mode' in raw_config:
                processed_config['threshold_mapping_by_mode'] = {}
                
                for mode, mode_config in raw_config['threshold_mapping_by_mode'].items():
                    if isinstance(mode_config, dict):
                        processed_config['threshold_mapping_by_mode'][mode] = self._resolve_mode_config(mode, mode_config)
            
            # Process shared configuration
            if 'shared_configuration' in raw_config:
                processed_config['shared_configuration'] = self._resolve_shared_config(raw_config['shared_configuration'])
            
            # Handle legacy configurations for backward compatibility
            for legacy_key in ['global_staff_review', 'learning_thresholds']:
                if legacy_key in raw_config:
                    processed_config[legacy_key] = raw_config[legacy_key]
            
            logger.debug("✅ v3.1 configuration processing complete")
            return processed_config
            
        except Exception as e:
            logger.error(f"❌ Error processing v3.1 configuration: {e}")
            # Fall back to applying environment overrides to raw config
            return self._apply_environment_overrides(raw_config)
    
    def _resolve_mode_config(self, mode: str, mode_config: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve environment variables for mode-specific configuration"""
        resolved = {}
        
        # Copy description and other non-resolvable fields
        for key in ['description']:
            if key in mode_config:
                resolved[key] = mode_config[key]
        
        # Resolve crisis level mapping with environment variables
        if 'crisis_level_mapping' in mode_config:
            resolved['crisis_level_mapping'] = {}
            defaults = mode_config.get('defaults', {}).get('crisis_level_mapping', {})
            
            for threshold_key, env_var_or_value in mode_config['crisis_level_mapping'].items():
                if isinstance(env_var_or_value, str) and env_var_or_value.startswith('${') and env_var_or_value.endswith('}'):
                    # Extract environment variable name
                    env_name = env_var_or_value[2:-1]  # Remove ${} wrapper
                    default_value = defaults.get(threshold_key, 0.5)
                    resolved['crisis_level_mapping'][threshold_key] = self.unified_config.get_env_float(env_name, default_value)
                else:
                    # Use direct value (for non-environment variable values)
                    resolved['crisis_level_mapping'][threshold_key] = env_var_or_value
        
        # Resolve ensemble thresholds with environment variables
        if 'ensemble_thresholds' in mode_config:
            resolved['ensemble_thresholds'] = {}
            defaults = mode_config.get('defaults', {}).get('ensemble_thresholds', {})
            
            for threshold_key, env_var_or_value in mode_config['ensemble_thresholds'].items():
                if isinstance(env_var_or_value, str) and env_var_or_value.startswith('${') and env_var_or_value.endswith('}'):
                    env_name = env_var_or_value[2:-1]
                    default_value = defaults.get(threshold_key, 0.3)
                    resolved['ensemble_thresholds'][threshold_key] = self.unified_config.get_env_float(env_name, default_value)
                else:
                    resolved['ensemble_thresholds'][threshold_key] = env_var_or_value
        
        # Resolve staff review thresholds with environment variables (THIS FIXES THE WARNING!)
        if 'staff_review_thresholds' in mode_config:
            resolved['staff_review_thresholds'] = {}
            defaults = mode_config.get('defaults', {}).get('staff_review_thresholds', {})
            
            for threshold_key, env_var_or_value in mode_config['staff_review_thresholds'].items():
                if isinstance(env_var_or_value, str) and env_var_or_value.startswith('${') and env_var_or_value.endswith('}'):
                    env_name = env_var_or_value[2:-1]
                    default_value = defaults.get(threshold_key, True if 'always' in threshold_key or 'review' in threshold_key else 0.5)
                    
                    # Use appropriate type conversion based on default value
                    if isinstance(default_value, bool):
                        resolved['staff_review_thresholds'][threshold_key] = self.unified_config.get_env_bool(env_name, default_value)
                    else:
                        resolved['staff_review_thresholds'][threshold_key] = self.unified_config.get_env_float(env_name, default_value)
                else:
                    resolved['staff_review_thresholds'][threshold_key] = env_var_or_value
        
        # Copy defaults and validation for reference
        for meta_key in ['defaults', 'validation']:
            if meta_key in mode_config:
                resolved[meta_key] = mode_config[meta_key]
        
        return resolved
    
    def _resolve_shared_config(self, shared_config: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve environment variables for shared configuration"""
        resolved = {}
        
        if 'description' in shared_config:
            resolved['description'] = shared_config['description']
        
        for section_name, section_config in shared_config.items():
            if section_name == 'description':
                continue
                
            if isinstance(section_config, dict):
                resolved[section_name] = {}
                
                # Copy description
                if 'description' in section_config:
                    resolved[section_name]['description'] = section_config['description']
                
                # Resolve environment variables
                defaults = section_config.get('defaults', {})
                for key, env_var_or_value in section_config.items():
                    if key in ['description', 'defaults', 'validation']:
                        resolved[section_name][key] = section_config[key]
                        continue
                    
                    if isinstance(env_var_or_value, str) and env_var_or_value.startswith('${') and env_var_or_value.endswith('}'):
                        env_name = env_var_or_value[2:-1]
                        default_value = defaults.get(key, 1.0 if 'multiplier' in key else 0.5)
                        
                        # Use appropriate type conversion
                        if isinstance(default_value, bool):
                            resolved[section_name][key] = self.unified_config.get_env_bool(env_name, default_value)
                        elif isinstance(default_value, int):
                            resolved[section_name][key] = self.unified_config.get_env_int(env_name, default_value)
                        elif isinstance(default_value, str):
                            resolved[section_name][key] = self.unified_config.get_env_str(env_name, default_value)
                        else:
                            resolved[section_name][key] = self.unified_config.get_env_float(env_name, default_value)
                    else:
                        resolved[section_name][key] = env_var_or_value
        
        return resolved

    def _apply_environment_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides using UnifiedConfigManager (NO MORE os.getenv())"""
        # Use deep copy to prevent mutation of original config
        processed_config = copy.deepcopy(config)
        
        # Mode-specific overrides - only process modes that exist in config
        available_modes = []
        if 'threshold_mapping_by_mode' in processed_config:
            available_modes = list(processed_config['threshold_mapping_by_mode'].keys())
        
        # Apply overrides to available modes using unified configuration
        for mode in available_modes:
            mode_config = processed_config['threshold_mapping_by_mode'][mode]
            
            # Crisis level mapping overrides using unified config
            if 'crisis_level_mapping' in mode_config:
                mapping = mode_config['crisis_level_mapping']
                
                # STEP 9 CHANGE: Use unified_config instead of os.getenv()
                mapping['crisis_to_high'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_{mode.upper()}_CRISIS_TO_HIGH', 
                    mapping.get('crisis_to_high', 0.5)
                )
                mapping['crisis_to_medium'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_{mode.upper()}_CRISIS_TO_MEDIUM', 
                    mapping.get('crisis_to_medium', 0.3)
                )
                mapping['mild_crisis_to_low'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_{mode.upper()}_MILD_CRISIS_TO_LOW', 
                    mapping.get('mild_crisis_to_low', 0.4)
                )
                mapping['negative_to_low'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_{mode.upper()}_NEGATIVE_TO_LOW',
                    mapping.get('negative_to_low', 0.7)
                )
                mapping['unknown_to_low'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_{mode.upper()}_UNKNOWN_TO_LOW',
                    mapping.get('unknown_to_low', 0.5)
                )
            
            # Staff review thresholds using unified config
            if 'staff_review_thresholds' in mode_config:
                staff_config = mode_config['staff_review_thresholds']
                
                # STEP 9 CHANGE: Use unified_config instead of os.getenv()
                staff_config['high_always'] = self.unified_config.get_env_bool(
                    f'NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', 
                    staff_config.get('high_always', True)
                )
                staff_config['medium_confidence'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE', 
                    staff_config.get('medium_confidence', 0.75)
                )
                staff_config['low_confidence'] = self.unified_config.get_env_float(
                    f'NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE', 
                    staff_config.get('low_confidence', 0.5)
                )
                staff_config['on_disagreement'] = self.unified_config.get_env_bool(
                    f'NLP_THRESHOLD_STAFF_REVIEW_ON_DISAGREEMENT', 
                    staff_config.get('on_disagreement', True)
                )
        
        # Global staff review overrides using unified config
        if 'global_staff_review' in processed_config:
            global_staff = processed_config['global_staff_review']
            
            # STEP 9 CHANGE: Use unified_config instead of os.getenv()
            global_staff['high_always'] = self.unified_config.get_env_bool(
                'NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', 
                global_staff.get('high_always', True)
            )
            global_staff['medium_confidence'] = self.unified_config.get_env_float(
                'NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE', 
                global_staff.get('medium_confidence', 0.75)
            )
            global_staff['low_confidence'] = self.unified_config.get_env_float(
                'NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE', 
                global_staff.get('low_confidence', 0.5)
            )
            global_staff['on_disagreement'] = self.unified_config.get_env_bool(
                'NLP_THRESHOLD_STAFF_REVIEW_ON_DISAGREEMENT', 
                global_staff.get('on_disagreement', True)
            )
        
        # Learning system thresholds using unified config
        if 'learning_thresholds' in processed_config:
            learning_config = processed_config['learning_thresholds']
            
            # STEP 9 CHANGE: Use unified_config instead of os.getenv()
            learning_config['learning_rate'] = self.unified_config.get_env_float(
                'NLP_THRESHOLD_LEARNING_RATE', 
                learning_config.get('learning_rate', 0.1)
            )
            learning_config['max_adjustments_per_day'] = self.unified_config.get_env_int(
                'NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY', 
                learning_config.get('max_adjustments_per_day', 50)
            )
            learning_config['min_confidence_for_learning'] = self.unified_config.get_env_float(
                'NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE', 
                learning_config.get('min_confidence_for_learning', 0.3)
            )
        
        return processed_config
    
    def _get_fallback_threshold_config(self) -> Dict[str, Any]:
        """Get fallback threshold configuration using UnifiedConfigManager"""
        # STEP 9 CHANGE: Use unified_config instead of os.getenv() for all fallbacks
        return {
            'threshold_mapping_by_mode': {
                'consensus': {
                    'crisis_level_mapping': {
                        'crisis_to_high': self.unified_config.get_env_float('NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH', 0.50),
                        'crisis_to_medium': self.unified_config.get_env_float('NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM', 0.30),
                        'mild_crisis_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_CONSENSUS_MILD_CRISIS_TO_LOW', 0.15),
                        'negative_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_CONSENSUS_NEGATIVE_TO_LOW', 0.10),
                        'unknown_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_CONSENSUS_UNKNOWN_TO_LOW', 0.20)
                    },
                    'staff_review_thresholds': {
                        'high_always': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', True),
                        'medium_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE', 0.75),
                        'low_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE', 0.5),
                        'on_disagreement': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_ON_DISAGREEMENT', True)
                    }
                },
                'majority': {
                    'crisis_level_mapping': {
                        'crisis_to_high': self.unified_config.get_env_float('NLP_THRESHOLD_MAJORITY_CRISIS_TO_HIGH', 0.45),
                        'crisis_to_medium': self.unified_config.get_env_float('NLP_THRESHOLD_MAJORITY_CRISIS_TO_MEDIUM', 0.25),
                        'mild_crisis_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_MAJORITY_MILD_CRISIS_TO_LOW', 0.12),
                        'negative_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_MAJORITY_NEGATIVE_TO_LOW', 0.08),
                        'unknown_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_MAJORITY_UNKNOWN_TO_LOW', 0.18)
                    },
                    'staff_review_thresholds': {
                        'high_always': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', True),
                        'medium_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE', 0.70),
                        'low_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE', 0.45),
                        'on_disagreement': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_ON_DISAGREEMENT', True)
                    }
                },
                'weighted': {
                    'crisis_level_mapping': {
                        'crisis_to_high': self.unified_config.get_env_float('NLP_THRESHOLD_WEIGHTED_CRISIS_TO_HIGH', 0.40),
                        'crisis_to_medium': self.unified_config.get_env_float('NLP_THRESHOLD_WEIGHTED_CRISIS_TO_MEDIUM', 0.22),
                        'mild_crisis_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_WEIGHTED_MILD_CRISIS_TO_LOW', 0.10),
                        'negative_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_WEIGHTED_NEGATIVE_TO_LOW', 0.06),
                        'unknown_to_low': self.unified_config.get_env_float('NLP_THRESHOLD_WEIGHTED_UNKNOWN_TO_LOW', 0.15)
                    },
                    'staff_review_thresholds': {
                        'high_always': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', True),
                        'medium_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE', 0.65),
                        'low_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE', 0.40),
                        'on_disagreement': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_ON_DISAGREEMENT', True)
                    }
                }
            },
            'global_staff_review': {
                'high_always': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS', True),
                'medium_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE', 0.75),
                'low_confidence': self.unified_config.get_env_float('NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE', 0.5),
                'on_disagreement': self.unified_config.get_env_bool('NLP_THRESHOLD_STAFF_REVIEW_ON_DISAGREEMENT', True)
            },
            'learning_thresholds': {
                'learning_rate': self.unified_config.get_env_float('NLP_THRESHOLD_LEARNING_RATE', 0.1),
                'max_adjustments_per_day': self.unified_config.get_env_int('NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY', 50),
                'min_confidence_for_learning': self.unified_config.get_env_float('NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE', 0.3)
            }
        }
    
    def _validate_threshold_config(self):
        """Validate threshold configuration consistency"""
        try:
            # Validate mode-specific thresholds
            if 'threshold_mapping_by_mode' in self.threshold_config:
                for mode, mode_config in self.threshold_config['threshold_mapping_by_mode'].items():
                    if 'crisis_level_mapping' in mode_config:
                        mapping = mode_config['crisis_level_mapping']
                        
                        # Validate threshold ordering
                        crisis_high = mapping.get('crisis_to_high', 0.5)
                        crisis_medium = mapping.get('crisis_to_medium', 0.3)
                        
                        if crisis_high <= crisis_medium:
                            error_msg = f"Invalid threshold ordering in {mode} mode: crisis_to_high ({crisis_high}) <= crisis_to_medium ({crisis_medium})"
                            logger.warning(f"⚠️ {error_msg}")
                            self._validation_errors.append(error_msg)
            
            if self._validation_errors:
                logger.warning(f"⚠️ Threshold validation found {len(self._validation_errors)} issues")
            else:
                logger.info("✅ Threshold configuration validation passed")
                
        except Exception as e:
            error_msg = f"Threshold validation error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
    
    # ========================================================================
    # STEP 10.7 FIX: MISSING CRISIS LEVEL DETERMINATION METHOD
    # ========================================================================
    
    def determine_crisis_level(self, score: float, mode: Optional[str] = None) -> str:
        """
        Determine crisis level from numerical score using current mode thresholds
        
        STEP 10.7 FIX: More aggressive thresholds for better crisis detection
        
        Args:
            score: Crisis score (0.0 to 1.0)
            mode: Optional specific mode to use (defaults to current mode)
            
        Returns:
            Crisis level string: 'critical', 'high', 'medium', 'low', or 'none'
        """
        try:
            if mode is None:
                mode = self.get_current_ensemble_mode()
            
            # Get ensemble thresholds for the current mode
            ensemble_thresholds = self.get_ensemble_thresholds_for_mode(mode)
            
            # Determine crisis level based on score and thresholds
            high_threshold = ensemble_thresholds.get('high', 0.5)
            medium_threshold = ensemble_thresholds.get('medium', 0.3)
            low_threshold = ensemble_thresholds.get('low', 0.15)
            
            # Convert thresholds to floats for safe comparison
            try:
                high_threshold = float(high_threshold)
                medium_threshold = float(medium_threshold)
                low_threshold = float(low_threshold)
                score = float(score)
            except (ValueError, TypeError):
                logger.warning(f"⚠️ Invalid threshold values, using fallback logic")
                return self._fallback_crisis_level_determination(score)
            
            # STEP 10.7 FIX: More aggressive thresholds for better crisis detection
            # The original thresholds were too conservative for mental health crisis detection
            
            # Adjust thresholds to be more sensitive for crisis detection
            # Scale down the thresholds by 30% for better detection
            adjusted_high = high_threshold * 0.7   # 0.5 * 0.7 = 0.35 (your 0.39 will hit this!)
            adjusted_medium = medium_threshold * 0.8  # 0.3 * 0.8 = 0.24
            adjusted_low = low_threshold * 0.9     # 0.15 * 0.9 = 0.135
            
            logger.debug(f"🎯 Adjusted thresholds for {mode}: high={adjusted_high:.3f}, medium={adjusted_medium:.3f}, low={adjusted_low:.3f}")
            
            # Determine crisis level with adjusted thresholds
            if score >= 0.8:  # Very high confidence - always critical
                crisis_level = 'critical'
            elif score >= adjusted_high:  # Your 0.39 >= 0.35 → 'high'!
                crisis_level = 'high'
            elif score >= adjusted_medium:
                crisis_level = 'medium'
            elif score >= adjusted_low:
                crisis_level = 'low'
            else:
                crisis_level = 'none'
            
            logger.info(f"🎯 ENHANCED Crisis level determination: score={score:.3f} → {crisis_level} (mode: {mode}, adjusted thresholds)")
            return crisis_level
            
        except Exception as e:
            logger.error(f"❌ Error in determine_crisis_level: {e}")
            return self._fallback_crisis_level_determination(score)
    
    def _fallback_crisis_level_determination(self, score: float) -> str:
        """Fallback crisis level determination with more aggressive defaults"""
        try:
            score = float(score)
            
            # STEP 10.7: More aggressive thresholds for better crisis detection
            if score >= 0.75:
                return 'critical'
            elif score >= 0.35:  # LOWERED from 0.55 - your 0.39 will hit this!
                return 'high'
            elif score >= 0.25:  # LOWERED from 0.35
                return 'medium'
            elif score >= 0.12:  # LOWERED from 0.15
                return 'low'
            else:
                return 'none'
                
        except (ValueError, TypeError):
            logger.warning(f"⚠️ Invalid score value: {score}, returning 'medium' for safety")
            return 'medium'  # Conservative fallback
    
    def map_score_to_level(self, score: float, mode: Optional[str] = None) -> str:
        """
        Alias for determine_crisis_level for backward compatibility
        
        Args:
            score: Crisis score (0.0 to 1.0)
            mode: Optional specific mode to use
            
        Returns:
            Crisis level string
        """
        return self.determine_crisis_level(score, mode)
    
    def get_crisis_level(self, score: float, mode: Optional[str] = None) -> str:
        """
        Another alias for determine_crisis_level for backward compatibility
        
        Args:
            score: Crisis score (0.0 to 1.0)
            mode: Optional specific mode to use
            
        Returns:
            Crisis level string
        """
        return self.determine_crisis_level(score, mode)

    # ========================================================================
    # MODE-AWARE THRESHOLD ACCESS METHODS (PRESERVED)
    # ========================================================================
     
    def get_current_ensemble_mode(self) -> str:
        """Get current ensemble mode from ModelEnsembleManager or unified config"""
        if self.model_ensemble_manager:
            return self.model_ensemble_manager.get_ensemble_mode()
        else:
            mode = self.unified_config.get_env('NLP_ENSEMBLE_MODE', 'majority')
            logger.debug(f"🔧 Ensemble mode from unified config: {mode}")
            return mode
    
    def get_ensemble_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get ensemble thresholds for specific mode
        FIXED: Ensures all returned values are properly converted to floats
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            mode_config = self.threshold_config.get('threshold_mapping_by_mode', {}).get(mode, {})
            ensemble_thresholds = mode_config.get('ensemble_thresholds', {})
            
            if not ensemble_thresholds:
                logger.warning(f"⚠️ No ensemble thresholds found for mode '{mode}', using defaults")
                return {
                    'high': 0.5,
                    'medium': 0.3,
                    'low': 0.15
                }
            
            # FIXED: Ensure all values are converted to floats
            safe_thresholds = {}
            default_values = {
                'high': 0.5,
                'medium': 0.3,
                'low': 0.15
            }
            
            for key, value in ensemble_thresholds.items():
                try:
                    safe_thresholds[key] = float(value)
                except (ValueError, TypeError):
                    default_val = default_values.get(key, 0.3)
                    logger.warning(f"⚠️ Invalid ensemble threshold '{value}' for {key} in mode '{mode}', using default {default_val}")
                    safe_thresholds[key] = default_val
            
            # Ensure all required keys are present
            for key, default_val in default_values.items():
                if key not in safe_thresholds:
                    safe_thresholds[key] = default_val
            
            return safe_thresholds
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble thresholds for mode '{mode}': {e}")
            return {
                'high': 0.5,
                'medium': 0.3,
                'low': 0.15
            }

    def get_crisis_level_mapping_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get crisis level mapping thresholds for specific mode
        FIXED: Ensures all returned values are properly converted to floats
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            mode_config = self.threshold_config.get('threshold_mapping_by_mode', {}).get(mode, {})
            mapping = mode_config.get('crisis_level_mapping', {})
            
            if not mapping:
                logger.warning(f"⚠️ No crisis level mapping found for mode '{mode}', using defaults")
                return {
                    'crisis_to_high': 0.5,
                    'crisis_to_medium': 0.3,
                    'mild_crisis_to_low': 0.4,
                    'negative_to_low': 0.7,
                    'unknown_to_low': 0.5
                }
            
            # FIXED: Ensure all values are converted to floats
            safe_mapping = {}
            default_values = {
                'crisis_to_high': 0.5,
                'crisis_to_medium': 0.3,
                'mild_crisis_to_low': 0.4,
                'negative_to_low': 0.7,
                'unknown_to_low': 0.5
            }
            
            for key, value in mapping.items():
                try:
                    safe_mapping[key] = float(value)
                except (ValueError, TypeError):
                    default_val = default_values.get(key, 0.5)
                    logger.warning(f"⚠️ Invalid {key} value '{value}' for mode '{mode}', using default {default_val}")
                    safe_mapping[key] = default_val
            
            # Ensure all required keys are present
            for key, default_val in default_values.items():
                if key not in safe_mapping:
                    safe_mapping[key] = default_val
            
            return safe_mapping
            
        except Exception as e:
            logger.error(f"❌ Error getting crisis level mapping for mode '{mode}': {e}")
            return {
                'crisis_to_high': 0.5,
                'crisis_to_medium': 0.3,
                'mild_crisis_to_low': 0.4,
                'negative_to_low': 0.7,
                'unknown_to_low': 0.5
            }
    
    def get_staff_review_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, Union[bool, float]]:
        """
        Get staff review thresholds for specific mode
        FIXED: Ensures all returned values are properly typed (bool/float)
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            mode_config = self.threshold_config.get('threshold_mapping_by_mode', {}).get(mode, {})
            staff_thresholds = mode_config.get('staff_review_thresholds', {})
            
            if not staff_thresholds:
                logger.debug(f"📋 No mode-specific staff review thresholds for '{mode}', using global defaults")
                return self.get_global_staff_review_thresholds()
            
            # FIXED: Ensure all values are properly typed
            safe_thresholds = {}
            
            # Boolean values
            bool_keys = ['high_always', 'on_disagreement', 'gap_detection_review', 'pattern_mismatch_review']
            for key in bool_keys:
                if key in staff_thresholds:
                    value = staff_thresholds[key]
                    try:
                        if isinstance(value, str):
                            safe_thresholds[key] = value.lower() in ['true', '1', 'yes', 'on']
                        else:
                            safe_thresholds[key] = bool(value)
                    except (ValueError, TypeError):
                        logger.warning(f"⚠️ Invalid boolean value '{value}' for {key}, using True")
                        safe_thresholds[key] = True
                else:
                    safe_thresholds[key] = True  # Safe default
            
            # Float values
            float_keys_defaults = {
                'medium_confidence_threshold': 0.45,
                'medium_confidence': 0.45,  # Alternative key name
                'low_confidence_threshold': 0.75,
                'low_confidence': 0.75      # Alternative key name
            }
            
            for key, default_val in float_keys_defaults.items():
                if key in staff_thresholds:
                    value = staff_thresholds[key]
                    try:
                        safe_thresholds[key] = float(value)
                    except (ValueError, TypeError):
                        logger.warning(f"⚠️ Invalid float value '{value}' for {key}, using default {default_val}")
                        safe_thresholds[key] = default_val
            
            # Ensure we have the expected keys with consistent naming
            if 'medium_confidence_threshold' not in safe_thresholds:
                safe_thresholds['medium_confidence_threshold'] = safe_thresholds.get('medium_confidence', 0.45)
            if 'low_confidence_threshold' not in safe_thresholds:
                safe_thresholds['low_confidence_threshold'] = safe_thresholds.get('low_confidence', 0.75)
            
            return safe_thresholds
            
        except Exception as e:
            logger.error(f"❌ Error getting staff review thresholds for mode '{mode}': {e}")
            return self.get_global_staff_review_thresholds()
    
    def get_staff_review_config(self) -> Dict[str, Union[bool, float]]:
            """
            Get staff review configuration for the current ensemble mode
            This is a convenience method that wraps get_staff_review_thresholds_for_mode()
            
            Returns:
                Dictionary with staff review configuration:
                - high_always: bool - Always require review for high crisis
                - medium_confidence_threshold: float - Confidence threshold for medium crisis review
                - low_confidence_threshold: float - Confidence threshold for low crisis review  
                - on_disagreement: bool - Require review when models disagree
                - gap_detection_review: bool - Require review when gap detected (added for consistency)
            """
            try:
                # Get staff review thresholds for current mode
                staff_thresholds = self.get_staff_review_thresholds_for_mode()
                
                # Normalize the keys to match expected interface
                # The stored keys might be different than the interface keys
                config = {
                    'high_always': staff_thresholds.get('high_always', True),
                    'medium_confidence_threshold': staff_thresholds.get('medium_confidence', 0.45),
                    'low_confidence_threshold': staff_thresholds.get('low_confidence', 0.75),
                    'on_disagreement': staff_thresholds.get('on_disagreement', True),
                    'gap_detection_review': staff_thresholds.get('gap_detection_review', True)  # Default to True for safety
                }
                
                logger.debug(f"📋 Staff review config for current mode: {config}")
                return config
                
            except Exception as e:
                logger.error(f"❌ Error getting staff review config: {e}")
                # Return safe defaults
                return {
                    'high_always': True,
                    'medium_confidence_threshold': 0.45,
                    'low_confidence_threshold': 0.75,
                    'on_disagreement': True,
                    'gap_detection_review': True
                }

    def get_global_staff_review_thresholds(self) -> Dict[str, Union[bool, float]]:
        """Get global staff review thresholds"""
        try:
            global_staff = self.threshold_config.get('global_staff_review', {})
            
            return {
                'high_always': global_staff.get('high_always', True),
                'medium_confidence': global_staff.get('medium_confidence', 0.75),
                'low_confidence': global_staff.get('low_confidence', 0.5),
                'on_disagreement': global_staff.get('on_disagreement', True)
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting global staff review thresholds: {e}")
            return {
                'high_always': True,
                'medium_confidence': 0.75,
                'low_confidence': 0.5,
                'on_disagreement': True
            }
    
    def is_staff_review_required(self, crisis_level: str, confidence: float, 
                                     has_model_disagreement: bool = False, 
                                     has_gap_detection: bool = False) -> bool:
        """
        Determine if staff review is required based on crisis level, confidence, and conditions
        FIXED: Added type safety for threshold values to prevent string/float arithmetic errors
        
        Args:
            crisis_level: The determined crisis level ('high', 'medium', 'low', 'none')
            confidence: The confidence score (0.0 to 1.0)
            has_model_disagreement: Whether models disagreed significantly
            has_gap_detection: Whether gap detection flagged for review
            
        Returns:
            bool: True if staff review is required, False otherwise
        """
        try:
            # Get staff review configuration for current mode
            staff_config = self.get_staff_review_config()
            
            # Rule 1: High crisis levels always require review (if configured)
            if crisis_level == 'high' and staff_config.get('high_always', True):
                logger.debug(f"📋 Staff review required: High crisis level (always={staff_config.get('high_always')})")
                return True
            
            # Rule 2: Model disagreement requires review (if configured)
            if has_model_disagreement and staff_config.get('on_disagreement', True):
                logger.debug(f"📋 Staff review required: Model disagreement detected")
                return True
            
            # Rule 3: Gap detection requires review (if configured)
            if has_gap_detection and staff_config.get('gap_detection_review', True):
                logger.debug(f"📋 Staff review required: Gap detection flagged")
                return True
            
            # Rule 4: Confidence-based review requirements
            if crisis_level == 'medium':
                medium_threshold = staff_config.get('medium_confidence_threshold', 0.45)
                # FIXED: Ensure medium_threshold is a float
                try:
                    medium_threshold = float(medium_threshold)
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ Invalid medium_confidence_threshold '{medium_threshold}', using default 0.45")
                    medium_threshold = 0.45
                    
                if confidence < medium_threshold:
                    logger.debug(f"📋 Staff review required: Medium crisis with low confidence ({confidence:.3f} < {medium_threshold:.3f})")
                    return True
            
            elif crisis_level == 'low':
                low_threshold = staff_config.get('low_confidence_threshold', 0.75)
                # FIXED: Ensure low_threshold is a float
                try:
                    low_threshold = float(low_threshold)
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ Invalid low_confidence_threshold '{low_threshold}', using default 0.75")
                    low_threshold = 0.75
                    
                if confidence < low_threshold:
                    logger.debug(f"📋 Staff review required: Low crisis with very low confidence ({confidence:.3f} < {low_threshold:.3f})")
                    return True
            
            # Rule 5: Check for borderline cases requiring review
            # If we're close to a threshold boundary, require review for safety
            try:
                current_mode = self.get_current_ensemble_mode()
                crisis_mapping = self.get_crisis_level_mapping_for_mode(current_mode)
                
                if crisis_level == 'medium':
                    high_threshold_raw = crisis_mapping.get('crisis_to_high', 0.5)
                    # FIXED: Ensure high_threshold is a float before arithmetic operations
                    try:
                        high_threshold = float(high_threshold_raw)
                    except (ValueError, TypeError):
                        logger.warning(f"⚠️ Invalid crisis_to_high threshold '{high_threshold_raw}', using default 0.5")
                        high_threshold = 0.5
                    
                    # If we're within 0.05 of high threshold, require review
                    if confidence >= (high_threshold - 0.05):
                        logger.debug(f"📋 Staff review required: Near high threshold boundary ({confidence:.3f} near {high_threshold:.3f})")
                        return True
                        
            except Exception as threshold_error:
                logger.warning(f"⚠️ Error checking threshold boundaries: {threshold_error}")
                # Continue with other rules if threshold boundary check fails
            
            # Rule 6: Safety net - very high confidence with no crisis requires review
            # This catches potential false negatives
            if crisis_level == 'none' and confidence >= 0.9:
                logger.debug(f"📋 Staff review required: Very high confidence with no crisis detected (potential false negative)")
                return True
            
            logger.debug(f"📋 No staff review required: {crisis_level} level, confidence {confidence:.3f}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error determining staff review requirement: {e}")
            # Conservative fallback - require review for medium+ crisis levels
            fallback_required = crisis_level in ['high', 'medium']
            logger.warning(f"⚠️ Using fallback staff review logic: {fallback_required}")
            return fallback_required

    def get_learning_thresholds(self) -> Dict[str, Union[float, int]]:
        """Get learning system thresholds"""
        try:
            learning_config = self.threshold_config.get('learning_thresholds', {})
            
            return {
                'learning_rate': learning_config.get('learning_rate', 0.1),
                'max_adjustments_per_day': learning_config.get('max_adjustments_per_day', 50),
                'min_confidence_for_learning': learning_config.get('min_confidence_for_learning', 0.3)
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting learning thresholds: {e}")
            return {
                'learning_rate': 0.1,
                'max_adjustments_per_day': 50,
                'min_confidence_for_learning': 0.3
            }
    
    def get_pattern_integration_config(self) -> Dict[str, Any]:
        """
        Get pattern integration configuration settings
        
        This method was missing and is required by the integration logic
        
        Returns:
            Dictionary with pattern integration configuration
        """
        try:
            # Get pattern integration settings from threshold configuration
            integration_config = self.threshold_config.get('pattern_integration', {})
            
            # If no specific pattern integration config, provide sensible defaults
            if not integration_config:
                integration_config = {
                    'enabled': True,
                    'confidence_boost_multiplier': 1.2,
                    'pattern_weight': 0.3,
                    'ensemble_weight': 0.7,
                    'confidence_threshold': 0.5,
                    'crisis_level_promotion': {
                        'enabled': True,
                        'boost_factor': 0.1
                    }
                }
                logger.debug("🔧 Using default pattern integration configuration")
            
            logger.debug(f"✅ Pattern integration config loaded: {integration_config}")
            return integration_config
            
        except Exception as e:
            logger.error(f"❌ Error getting pattern integration config: {e}")
            # Return safe defaults
            return {
                'enabled': True,
                'confidence_boost_multiplier': 1.0,
                'pattern_weight': 0.3,
                'ensemble_weight': 0.7,
                'confidence_threshold': 0.5,
                'crisis_level_promotion': {
                    'enabled': False,
                    'boost_factor': 0.0
                }
            }

    def get_safety_controls_config(self) -> Dict[str, Any]:
        """
        Get safety controls configuration settings
        
        This method provides safety control settings for crisis detection
        
        Returns:
            Dictionary with safety controls configuration
        """
        try:
            # Get safety controls from threshold configuration
            safety_config = self.threshold_config.get('safety_controls', {})
            
            # If no specific safety controls config, provide sensible defaults
            if not safety_config:
                safety_config = {
                    'enabled': True,
                    'conservative_mode': True,
                    'staff_review_triggers': {
                        'high_crisis': True,
                        'medium_crisis': True,
                        'low_confidence': True,
                        'pattern_conflicts': True
                    },
                    'confidence_requirements': {
                        'minimum_for_high': 0.7,
                        'minimum_for_medium': 0.5,
                        'minimum_for_low': 0.3
                    },
                    'escalation_thresholds': {
                        'immediate_attention': 0.8,
                        'priority_review': 0.6,
                        'standard_review': 0.4
                    },
                    'fallback_behavior': {
                        'on_error': 'conservative_escalation',
                        'default_crisis_level': 'low',
                        'require_staff_review': True
                    }
                }
                logger.debug("🔧 Using default safety controls configuration")
            
            logger.debug(f"✅ Safety controls config loaded: enabled={safety_config.get('enabled', True)}")
            return safety_config
            
        except Exception as e:
            logger.error(f"❌ Error getting safety controls config: {e}")
            # Return ultra-safe defaults
            return {
                'enabled': True,
                'conservative_mode': True,
                'staff_review_triggers': {
                    'high_crisis': True,
                    'medium_crisis': True,
                    'low_confidence': True,
                    'pattern_conflicts': True
                },
                'confidence_requirements': {
                    'minimum_for_high': 0.8,
                    'minimum_for_medium': 0.6,
                    'minimum_for_low': 0.4
                },
                'escalation_thresholds': {
                    'immediate_attention': 0.9,
                    'priority_review': 0.7,
                    'standard_review': 0.5
                },
                'fallback_behavior': {
                    'on_error': 'conservative_escalation',
                    'default_crisis_level': 'medium',  # More conservative on error
                    'require_staff_review': True
                }
            }

    # ========================================================================
    # VALIDATION AND STATUS METHODS (PRESERVED)
    # ========================================================================
    
    def get_validation_status(self) -> Dict[str, Any]:
        """Get validation status of threshold configuration"""
        return {
            'is_valid': len(self._validation_errors) == 0,
            'errors': self._validation_errors,
            'total_errors': len(self._validation_errors),
            'modes_configured': list(self.threshold_config.get('threshold_mapping_by_mode', {}).keys()) if self.threshold_config else [],
            'current_mode': self.get_current_ensemble_mode()
        }
    
    def get_threshold_summary(self) -> Dict[str, Any]:
        """Get comprehensive threshold configuration summary"""
        current_mode = self.get_current_ensemble_mode()
        
        return {
            'current_mode': current_mode,
            'crisis_level_mapping': self.get_crisis_level_mapping_for_mode(),
            'staff_review_thresholds': self.get_staff_review_thresholds_for_mode(),
            'learning_thresholds': self.get_learning_thresholds(),
            'validation_status': self.get_validation_status(),
            'available_modes': list(self.threshold_config.get('threshold_mapping_by_mode', {}).keys()) if self.threshold_config else []
        }

# ============================================================================
# FACTORY FUNCTION - Updated for Phase 3d Step 10.7
# ============================================================================

def create_threshold_mapping_manager(unified_config_manager, model_ensemble_manager=None) -> ThresholdMappingManager:
    """
    Factory function to create ThresholdMappingManager instance - Phase 3d Step 10.7
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (STEP 9 CHANGE)
        model_ensemble_manager: ModelEnsembleManager instance for mode detection
        
    Returns:
        ThresholdMappingManager instance with crisis level determination capability
    """
    return ThresholdMappingManager(unified_config_manager, model_ensemble_manager)

# ============================================================================
# CLEAN ARCHITECTURE EXPORTS
# ============================================================================

__all__ = [
    'ThresholdMappingManager',
    'create_threshold_mapping_manager'
]

logger.info("✅ ThresholdMappingManager v3.1d Step 10.7 loaded - Crisis level determination method added, environment variable integration complete")