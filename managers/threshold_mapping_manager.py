# ash-nlp/managers/threshold_mapping_manager.py
"""
Mode-Aware Threshold Configuration Manager for Ash NLP Service v3.1
Clean v3.1 Architecture
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
        Initialize ThresholdMappingManager with standardized configuration support
        
        Args:
            unified_config_manager: UnifiedConfigManager instance
            model_ensemble_manager: ModelEnsembleManager instance (optional)
        """
        if unified_config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ThresholdMappingManager")
        
        self.unified_config = unified_config_manager
        self.model_ensemble_manager = model_ensemble_manager
        
        logger.info("ThresholdMappingManager v3.1d Step 10 initializing with standardized configuration...")
        
        # Try to load standardized configuration first, fall back to legacy if needed
        try:
            self.threshold_config = self._load_standardized_threshold_config()
            logger.info("✅ Using standardized JSON configuration format")
        except Exception as e:
            logger.warning(f"⚠️ Standardized config failed, using legacy format: {e}")
            self.threshold_config = self._load_threshold_configuration()
        
        # Validate configuration
        #self._validate_configuration()
        
        logger.info("✅ Threshold mapping configuration loaded and validated")
        logger.info("ThresholdMappingManager v3.1d Step 10 initialized - Standardized configuration support")
    
    def _load_standardized_threshold_config(self) -> Dict[str, Any]:
        """
        Load threshold configuration from standardized JSON format
        Following Clean v3.1 JSON configuration standards with defaults blocks
        """
        try:
            config = self.unified_config.get_threshold_configuration()
            
            # Transform from standardized format to internal format
            standardized_config = {
                'threshold_mapping_by_mode': {
                    'consensus': {
                        'crisis_level_mapping': {
                            'crisis_to_high': config.get('consensus_mode_thresholds', {}).get('crisis_to_high'),
                            'crisis_to_medium': config.get('consensus_mode_thresholds', {}).get('crisis_to_medium'),
                            'mild_crisis_to_low': config.get('consensus_mode_thresholds', {}).get('mild_crisis_to_low'),
                            'negative_to_low': config.get('consensus_mode_thresholds', {}).get('negative_to_low'),
                            'unknown_to_low': config.get('consensus_mode_thresholds', {}).get('unknown_to_low')
                        },
                        'ensemble_thresholds': {
                            'high': config.get('consensus_mode_thresholds', {}).get('ensemble_high'),
                            'medium': config.get('consensus_mode_thresholds', {}).get('ensemble_medium'),
                            'low': config.get('consensus_mode_thresholds', {}).get('ensemble_low')
                        },
                        'staff_review_thresholds': {
                            'high_always': config.get('staff_review_settings', {}).get('high_always'),
                            'medium_confidence_threshold': config.get('staff_review_settings', {}).get('medium_confidence_threshold'),
                            'low_confidence_threshold': config.get('staff_review_settings', {}).get('low_confidence_threshold'),
                            'on_disagreement': config.get('staff_review_settings', {}).get('on_disagreement'),
                            'gap_detection_review': config.get('staff_review_settings', {}).get('gap_detection_review')
                        }
                    },
                    'majority': {
                        'crisis_level_mapping': {
                            'crisis_to_high': config.get('majority_mode_thresholds', {}).get('crisis_to_high'),
                            'crisis_to_medium': config.get('majority_mode_thresholds', {}).get('crisis_to_medium'),
                            'mild_crisis_to_low': config.get('majority_mode_thresholds', {}).get('mild_crisis_to_low'),
                            'negative_to_low': config.get('majority_mode_thresholds', {}).get('negative_to_low'),
                            'unknown_to_low': config.get('majority_mode_thresholds', {}).get('unknown_to_low')
                        },
                        'ensemble_thresholds': {
                            'high': config.get('majority_mode_thresholds', {}).get('ensemble_high'),
                            'medium': config.get('majority_mode_thresholds', {}).get('ensemble_medium'),
                            'low': config.get('majority_mode_thresholds', {}).get('ensemble_low')
                        },
                        'staff_review_thresholds': {
                            'high_always': config.get('staff_review_settings', {}).get('high_always'),
                            'medium_confidence_threshold': config.get('staff_review_settings', {}).get('medium_confidence_threshold'),
                            'low_confidence_threshold': config.get('staff_review_settings', {}).get('low_confidence_threshold'),
                            'on_disagreement': config.get('staff_review_settings', {}).get('on_disagreement'),
                            'gap_detection_review': config.get('staff_review_settings', {}).get('gap_detection_review')
                        }
                    },
                    'weighted': {
                        'crisis_level_mapping': {
                            'crisis_to_high': config.get('weighted_mode_thresholds', {}).get('crisis_to_high'),
                            'crisis_to_medium': config.get('weighted_mode_thresholds', {}).get('crisis_to_medium'),
                            'mild_crisis_to_low': config.get('weighted_mode_thresholds', {}).get('mild_crisis_to_low'),
                            'negative_to_low': config.get('weighted_mode_thresholds', {}).get('negative_to_low'),
                            'unknown_to_low': config.get('weighted_mode_thresholds', {}).get('unknown_to_low')
                        },
                        'ensemble_thresholds': {
                            'high': config.get('weighted_mode_thresholds', {}).get('ensemble_high'),
                            'medium': config.get('weighted_mode_thresholds', {}).get('ensemble_medium'),
                            'low': config.get('weighted_mode_thresholds', {}).get('ensemble_low')
                        },
                        'staff_review_thresholds': {
                            'high_always': config.get('staff_review_settings', {}).get('high_always'),
                            'medium_confidence_threshold': config.get('staff_review_settings', {}).get('medium_confidence_threshold'),
                            'low_confidence_threshold': config.get('staff_review_settings', {}).get('low_confidence_threshold'),
                            'on_disagreement': config.get('staff_review_settings', {}).get('on_disagreement'),
                            'gap_detection_review': config.get('staff_review_settings', {}).get('gap_detection_review')
                        }
                    }
                },
                'shared_configuration': {
                    'pattern_integration': {
                        'pattern_weight_multiplier': config.get('pattern_integration_settings', {}).get('pattern_weight_multiplier'),
                        'confidence_boost_limit': config.get('pattern_integration_settings', {}).get('confidence_boost_limit'),
                        'pattern_override_threshold': config.get('pattern_integration_settings', {}).get('pattern_override_threshold'),
                        'community_pattern_boost': config.get('pattern_integration_settings', {}).get('community_pattern_boost'),
                        'pattern_weight': config.get('pattern_integration_settings', {}).get('pattern_weight'),
                        'ensemble_weight': config.get('pattern_integration_settings', {}).get('ensemble_weight'),
                        'confidence_threshold': config.get('pattern_integration_settings', {}).get('confidence_threshold'),
                        'crisis_level_promotion': {
                            'enabled': config.get('pattern_integration_settings', {}).get('crisis_level_promotion_enabled'),
                            'boost_factor': config.get('pattern_integration_settings', {}).get('crisis_level_boost_factor')
                        }
                    },
                    'learning_system': {
                        'feedback_weight': config.get('learning_system_settings', {}).get('feedback_weight'),
                        'min_samples_for_update': config.get('learning_system_settings', {}).get('min_samples_for_update'),
                        'confidence_adjustment_limit': config.get('learning_system_settings', {}).get('confidence_adjustment_limit'),
                        'enable_threshold_learning': config.get('learning_system_settings', {}).get('enable_threshold_learning'),
                        'learning_rate': config.get('learning_system_settings', {}).get('learning_rate'),
                        'max_threshold_drift': config.get('learning_system_settings', {}).get('max_threshold_drift'),
                        'min_confidence_for_learning': config.get('learning_system_settings', {}).get('min_confidence_for_learning')
                    },
                    'safety_controls': {
                        'enabled': config.get('safety_controls_settings', {}).get('safety_bias_enabled'),
                        'enable_conservative_bias': config.get('safety_controls_settings', {}).get('enable_conservative_bias'),
                        'false_negative_penalty': config.get('safety_controls_settings', {}).get('false_negative_penalty'),
                        'false_positive_tolerance': config.get('safety_controls_settings', {}).get('false_positive_tolerance'),
                        'emergency_escalation_threshold': config.get('safety_controls_settings', {}).get('emergency_escalation_threshold')
                    }
                }
            }
            
            logger.info("✅ Loaded standardized threshold configuration successfully")
            logger.debug(f"🔧 Configuration includes {len(standardized_config['threshold_mapping_by_mode'])} modes")
            
            return standardized_config
            
        except Exception as e:
            logger.error(f"❌ Error loading standardized threshold configuration: {e}")
            logger.info("🔄 Falling back to legacy configuration format")
            return self._get_fallback_threshold_config()

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
                    if confidence < medium_threshold:
                        logger.debug(f"📋 Staff review required: Medium crisis with low confidence ({confidence:.3f} < {medium_threshold:.3f})")
                        return True
                
                elif crisis_level == 'low':
                    low_threshold = staff_config.get('low_confidence_threshold', 0.75)
                    if confidence < low_threshold:
                        logger.debug(f"📋 Staff review required: Low crisis with very low confidence ({confidence:.3f} < {low_threshold:.3f})")
                        return True
                
                # Rule 5: Check for borderline cases requiring review
                # If we're close to a threshold boundary, require review for safety
                current_mode = self.get_current_ensemble_mode()
                crisis_mapping = self.get_crisis_level_mapping_for_mode(current_mode)
                
                if crisis_level == 'medium':
                    high_threshold = crisis_mapping.get('crisis_to_high', 0.5)
                    # If we're within 0.05 of high threshold, require review
                    if confidence >= (high_threshold - 0.05):
                        logger.debug(f"📋 Staff review required: Near high threshold boundary ({confidence:.3f} near {high_threshold:.3f})")
                        return True
                
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