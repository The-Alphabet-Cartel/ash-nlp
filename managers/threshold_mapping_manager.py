"""
ThresholdMappingManager - Mode-Aware Threshold Configuration Manager
Phase 3d Step 9: Updated for UnifiedConfigManager - NO MORE os.getenv() calls

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
        
        logger.info("ThresholdMappingManager v3.1d Step 9 initialized - UnifiedConfigManager integration complete")
    
    def _load_threshold_mapping_config(self):
        """Load threshold mapping configuration using UnifiedConfigManager"""
        try:
            # Load threshold mapping configuration through unified manager
            self.threshold_config = self.unified_config.load_config_file('threshold_mapping')
            
            if not self.threshold_config:
                logger.warning("⚠️ Threshold mapping configuration not found, using environment fallbacks")
                self.threshold_config = self._get_fallback_threshold_config()
            
            # Apply environment overrides using unified configuration
            self.threshold_config = self._apply_environment_overrides(self.threshold_config)
            
            # Validate threshold configuration
            self._validate_threshold_config()
            
            logger.info("✅ Threshold mapping configuration loaded and validated")
            
        except Exception as e:
            logger.error(f"❌ Error loading threshold mapping configuration: {e}")
            self._validation_errors.append(f"Configuration loading error: {str(e)}")
    
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
    # MODE-AWARE THRESHOLD ACCESS METHODS (PRESERVED)
    # ========================================================================
    
    def get_current_ensemble_mode(self) -> str:
        """Get current ensemble mode from ModelEnsembleManager or unified config"""
        if self.model_ensemble_manager:
            return self.model_ensemble_manager.get_current_ensemble_mode()
        else:
            # STEP 9 CHANGE: Use unified_config instead of os.getenv()
            mode = self.unified_config.get_env('NLP_ENSEMBLE_MODE', 'consensus')
            logger.debug(f"🔧 Ensemble mode from unified config: {mode}")
            return mode
    
    def get_ensemble_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get ensemble thresholds for specific mode - MISSING METHOD ADDED
        
        Args:
            mode: Ensemble mode ('consensus', 'majority', 'weighted')
            
        Returns:
            Dictionary with high, medium, low thresholds for the mode
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
            
            return ensemble_thresholds
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble thresholds for mode '{mode}': {e}")
            return {
                'high': 0.5,
                'medium': 0.3,
                'low': 0.15
            }

    def get_crisis_level_mapping_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """Get crisis level mapping thresholds for specific mode"""
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
            
            return mapping
            
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
        """Get staff review thresholds for specific mode"""
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            mode_config = self.threshold_config.get('threshold_mapping_by_mode', {}).get(mode, {})
            staff_thresholds = mode_config.get('staff_review_thresholds', {})
            
            if not staff_thresholds:
                logger.warning(f"⚠️ No staff review thresholds found for mode '{mode}', using global defaults")
                return self.get_global_staff_review_thresholds()
            
            return staff_thresholds
            
        except Exception as e:
            logger.error(f"❌ Error getting staff review thresholds for mode '{mode}': {e}")
            return self.get_global_staff_review_thresholds()
    
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
# FACTORY FUNCTION - Updated for Phase 3d Step 9
# ============================================================================

def create_threshold_mapping_manager(unified_config_manager, model_ensemble_manager=None) -> ThresholdMappingManager:
    """
    Factory function to create ThresholdMappingManager instance - Phase 3d Step 9
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (STEP 9 CHANGE)
        model_ensemble_manager: ModelEnsembleManager instance for mode detection
        
    Returns:
        ThresholdMappingManager instance
    """
    return ThresholdMappingManager(unified_config_manager, model_ensemble_manager)

# ============================================================================
# CLEAN ARCHITECTURE EXPORTS
# ============================================================================

__all__ = [
    'ThresholdMappingManager',
    'create_threshold_mapping_manager'
]

logger.info("✅ ThresholdMappingManager v3.1d Step 9 loaded - UnifiedConfigManager integration complete, direct os.getenv() calls eliminated")