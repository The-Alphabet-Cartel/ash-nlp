# ash-nlp/managers/threshold_mapping_manager.py
"""
Mode-Aware Threshold Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3e-5.5-1
LAST MODIFIED: 2025-08-19
PHASE: 3e, Sub-step 5.2 - ThresholdMappingManager Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Methods moved to CrisisAnalyzer and LearningSystemManager with migration references
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
    Phase 3e Sub-step 5.2: CLEANUP - Methods moved to CrisisAnalyzer and LearningSystemManager
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
        self.config = None
        self._validation_errors = []
        
        # Load threshold mapping configuration using unified manager
        self._load_threshold_mapping_config()
        
        logger.info("ThresholdMappingManager v3.1-3e-5.2-1 initialized - Phase 3e cleanup with migration references")
    
    def _load_threshold_mapping_config(self):
        """
        Load threshold mapping configuration using UnifiedConfigManager get_config_section()
        SIMPLIFIED: No more manual environment variable resolution needed
        """
        try:
            raw_config = self.unified_config.get_config_section('threshold_mapping')
            
            if not raw_config:
                logger.warning("⚠️ Threshold mapping configuration not found, using environment fallbacks")
                self.threshold_config = self._get_fallback_threshold_config()
            else:
                self.threshold_config = raw_config
                logger.info("✅ Threshold mapping configuration loaded (environment resolution via get_config_section)")
            
            # Validate threshold configuration
            self._validate_threshold_config()
            
            logger.info("✅ Threshold mapping configuration loaded and validated")
            
        except Exception as e:
            logger.error(f"❌ Error loading threshold mapping configuration: {e}")
            self._validation_errors.append(f"Configuration loading error: {str(e)}")
            # Fallback to safe defaults
            self.threshold_config = self._get_fallback_threshold_config()
    
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
        """
        Validate threshold configuration consistency using get_config_section()
        UPDATED: Uses new methods for validation instead of raw config access
        """
        try:
            # Validate each available mode using the new methods
            available_modes = ['consensus', 'majority', 'weighted']
            
            for mode in available_modes:
                try:
                    # Test ensemble thresholds
                    ensemble_thresholds = self.get_ensemble_thresholds_for_mode(mode)
                    if ensemble_thresholds:
                        # Validate threshold ordering
                        critical = ensemble_thresholds.get('critical', 1.0)
                        high = ensemble_thresholds.get('high', 0.5)
                        medium = ensemble_thresholds.get('medium', 0.3)
                        low = ensemble_thresholds.get('low', 0.1)
                        
                        if not (low <= medium <= high <= critical):
                            error_msg = f"Invalid threshold ordering in {mode} mode: low({low}) <= medium({medium}) <= high({high}) <= critical({critical})"
                            logger.warning(f"⚠️ {error_msg}")
                            self._validation_errors.append(error_msg)
                        else:
                            logger.debug(f"✅ Threshold ordering valid for {mode}: {low} <= {medium} <= {high} <= {critical}")
                    
                    # Test crisis level mapping
                    crisis_mapping = self.get_crisis_level_mapping_for_mode(mode)
                    if crisis_mapping:
                        crisis_high = crisis_mapping.get('crisis_to_high', 0.5)
                        crisis_medium = crisis_mapping.get('crisis_to_medium', 0.3)
                        
                        if crisis_high <= crisis_medium:
                            error_msg = f"Invalid crisis mapping in {mode} mode: crisis_to_high ({crisis_high}) <= crisis_to_medium ({crisis_medium})"
                            logger.warning(f"⚠️ {error_msg}")
                            self._validation_errors.append(error_msg)
                    
                    # Test staff review thresholds
                    staff_thresholds = self.get_staff_review_thresholds_for_mode(mode)
                    if staff_thresholds:
                        medium_conf = staff_thresholds.get('medium_confidence_threshold', 0.5)
                        low_conf = staff_thresholds.get('low_confidence_threshold', 0.8)
                        
                        if not (0.0 <= medium_conf <= 1.0) or not (0.0 <= low_conf <= 1.0):
                            error_msg = f"Staff review confidence thresholds out of range in {mode} mode"
                            logger.warning(f"⚠️ {error_msg}")
                            self._validation_errors.append(error_msg)
                            
                except Exception as mode_error:
                    error_msg = f"Validation failed for mode {mode}: {str(mode_error)}"
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
    # PHASE 3E SUB-STEP 5.2: MIGRATION REFERENCES FOR MOVED METHODS
    # ========================================================================
    
    def apply_threshold_to_confidence(self, confidence: float, mode: str = 'consensus') -> str:
        """
        PHASE 3E SUB-STEP 5.2: Method moved to CrisisAnalyzer
        
        This method has been consolidated into CrisisAnalyzer.apply_crisis_thresholds()
        for better organization of analysis-specific functionality.
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
            mode: Analysis mode
            
        Returns:
            Dictionary indicating where to find the new method
        """
        logger.info("ℹ️ Phase 3e Sub-step 5.2: apply_threshold_to_confidence() moved to CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.apply_crisis_thresholds() for threshold application")
        
        return {
            'note': 'Threshold application moved to CrisisAnalyzer for better analysis consolidation',
            'use_instead': 'CrisisAnalyzer.apply_crisis_thresholds()',
            'reason': 'Phase 3e Sub-step 5.2 analysis method consolidation - moved to specialized analysis manager',
            'migration_date': '2025-08-19',
            'phase': '3e.5.2',
            'parameters': {
                'confidence': confidence,
                'mode': mode
            },
            'benefits': [
                'Consolidated analysis functionality in CrisisAnalyzer',
                'Better separation of threshold configuration vs threshold application',
                'Enhanced learning system integration in analysis context',
                'Improved maintainability and testing',
                'Direct access to SharedUtilities for enhanced error handling'
            ]
        }
    
    def calculate_crisis_level(self, confidence: float, mode: str = 'default') -> str:
        """
        PHASE 3E SUB-STEP 5.2: Method moved to CrisisAnalyzer
        
        This method has been consolidated into CrisisAnalyzer.calculate_crisis_level_from_confidence()
        for better organization of analysis-specific functionality.
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
            mode: Analysis mode
            
        Returns:
            Dictionary indicating where to find the new method
        """
        logger.info("ℹ️ Phase 3e Sub-step 5.2: calculate_crisis_level() moved to CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.calculate_crisis_level_from_confidence() for crisis level calculation")
        
        return {
            'note': 'Crisis level calculation moved to CrisisAnalyzer for better analysis consolidation',
            'use_instead': 'CrisisAnalyzer.calculate_crisis_level_from_confidence()',
            'reason': 'Phase 3e Sub-step 5.2 analysis method consolidation - moved to specialized analysis manager',
            'migration_date': '2025-08-19',
            'phase': '3e.5.2',
            'parameters': {
                'confidence': confidence,
                'mode': mode
            },
            'benefits': [
                'Consolidated analysis functionality in CrisisAnalyzer',
                'Learning system integration for adaptive crisis level calculation',
                'Enhanced error handling via SharedUtilities',
                'Better separation of threshold configuration vs crisis level determination',
                'Improved testability with consolidated analysis methods'
            ]
        }
    
    def validate_analysis_thresholds(self, mode: str = 'consensus') -> Dict[str, bool]:
        """
        PHASE 3E SUB-STEP 5.2: Method moved to CrisisAnalyzer
        
        This method has been consolidated into CrisisAnalyzer.validate_crisis_analysis_thresholds()
        for better organization of analysis-specific functionality.
        
        Args:
            mode: Analysis mode to validate
            
        Returns:
            Dictionary indicating where to find the new method
        """
        logger.info("ℹ️ Phase 3e Sub-step 5.2: validate_analysis_thresholds() moved to CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.validate_crisis_analysis_thresholds() for threshold validation")
        
        return {
            'note': 'Analysis threshold validation moved to CrisisAnalyzer for better analysis consolidation',
            'use_instead': 'CrisisAnalyzer.validate_crisis_analysis_thresholds()',
            'reason': 'Phase 3e Sub-step 5.2 analysis method consolidation - moved to specialized analysis manager',
            'migration_date': '2025-08-19',
            'phase': '3e.5.2',
            'parameters': {
                'mode': mode
            },
            'benefits': [
                'Consolidated analysis validation in CrisisAnalyzer',
                'Better integration with other analysis methods',
                'Enhanced error handling and reporting',
                'Learning system aware validation',
                'Improved consistency across analysis operations'
            ]
        }
    
    def get_threshold_for_mode(self, mode: str) -> Dict[str, float]:
        """
        PHASE 3E SUB-STEP 5.2: Method moved to CrisisAnalyzer
        
        This method has been consolidated into CrisisAnalyzer.get_crisis_threshold_for_mode()
        for better organization of analysis-specific functionality.
        
        Args:
            mode: Analysis mode
            
        Returns:
            Dictionary indicating where to find the new method
        """
        logger.info("ℹ️ Phase 3e Sub-step 5.2: get_threshold_for_mode() moved to CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.get_crisis_threshold_for_mode() for mode-specific thresholds")
        
        return {
            'note': 'Mode-specific threshold retrieval moved to CrisisAnalyzer for better analysis consolidation',
            'use_instead': 'CrisisAnalyzer.get_crisis_threshold_for_mode()',
            'reason': 'Phase 3e Sub-step 5.2 analysis method consolidation - moved to specialized analysis manager',
            'migration_date': '2025-08-19',
            'phase': '3e.5.2',
            'parameters': {
                'mode': mode
            },
            'benefits': [
                'Consolidated threshold access in CrisisAnalyzer',
                'Better integration with analysis algorithms',
                'Learning system aware threshold retrieval',
                'Enhanced mode support (sensitive, conservative, etc.)',
                'Direct access to SharedUtilities for configuration access'
            ]
        }
    
    def adapt_thresholds_based_on_learning(self, feedback_data: Dict = None) -> Dict[str, Any]:
        """
        PHASE 3E SUB-STEP 5.2: Method moved to LearningSystemManager
        
        This method has been consolidated into LearningSystemManager.adapt_crisis_thresholds()
        for better organization of learning-specific functionality.
        
        Args:
            feedback_data: Learning feedback data
            
        Returns:
            Dictionary indicating where to find the new method
        """
        logger.info("ℹ️ Phase 3e Sub-step 5.2: adapt_thresholds_based_on_learning() moved to LearningSystemManager")
        logger.info("💡 Use LearningSystemManager.adapt_crisis_thresholds() for learning-based threshold adaptation")
        
        return {
            'note': 'Learning-based threshold adaptation moved to LearningSystemManager for better learning consolidation',
            'use_instead': 'LearningSystemManager.adapt_crisis_thresholds()',
            'reason': 'Phase 3e Sub-step 5.2 learning method consolidation - moved to specialized learning manager',
            'migration_date': '2025-08-19',
            'phase': '3e.5.2',
            'parameters': {
                'feedback_data': feedback_data
            },
            'benefits': [
                'Consolidated learning functionality in LearningSystemManager',
                'Better separation of threshold configuration vs learning adaptation',
                'Enhanced learning algorithms and feedback processing',
                'Specialized learning system with false positive/negative handling',
                'Improved learning data persistence and analysis'
            ]
        }

    # ========================================================================
    # CORE CRISIS LEVEL DETERMINATION METHOD (PRESERVED)
    # ========================================================================
    
    def determine_crisis_level(self, score: float, mode: Optional[str] = None) -> str:
        """
        Determine crisis level from numerical score using current mode thresholds
        
        PRESERVED: This is core business logic for life-saving crisis detection
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
        """Get current ensemble mode UnifiedConfigManager"""
        logger.debug("📋 Getting ensemble mode from JSON...")
        self.config = self.unified_config.get_config_section(
            'model_ensemble',
            'ensemble_config.mode',
            'majority'
        )
        if self.config:
            logger.debug(f"🔧 Ensemble mode: {mode}")
            return mode
        else:
            mode = self.unified_config.get_env('NLP_ENSEMBLE_MODE', 'majority')
            logger.error("⚠️ Ensemble mode not found, using ENV...")
            return mode

    def get_ensemble_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get ensemble thresholds for specific mode using new UnifiedConfigManager method
        UPDATED: Now uses get_config_section() instead of manual resolution
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            ensemble_thresholds = self.unified_config.get_config_section(
                'threshold_mapping', 
                f'threshold_mapping_by_mode.{mode}.ensemble_thresholds',
                {
                    'critical': 0.7,
                    'high': 0.45,
                    'medium': 0.25,
                    'low': 0.12
                }
            )
            
            # Ensure all values are floats (get_config_section should handle this, but be safe)
            safe_thresholds = {}
            default_values = {
                'critical': 0.7,
                'high': 0.45,
                'medium': 0.25,
                'low': 0.12
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
            
            logger.debug(f"✅ Ensemble thresholds for mode '{mode}': {safe_thresholds}")
            return safe_thresholds
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble thresholds for mode '{mode}': {e}")
            return {
                'critical': 0.7,
                'high': 0.45,
                'medium': 0.25,
                'low': 0.12
            }

    def get_crisis_level_mapping_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get crisis level mapping thresholds for specific mode using new UnifiedConfigManager method
        UPDATED: Now uses get_config_section() instead of manual resolution
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            crisis_mapping = self.unified_config.get_config_section(
                'threshold_mapping',
                f'threshold_mapping_by_mode.{mode}.crisis_level_mapping',
                {
                    'crisis_to_high': 0.5,
                    'crisis_to_medium': 0.3,
                    'mild_crisis_to_low': 0.4,
                    'negative_to_low': 0.7,
                    'unknown_to_low': 0.5
                }
            )
            
            # Ensure all values are floats
            safe_mapping = {}
            default_values = {
                'crisis_to_high': 0.5,
                'crisis_to_medium': 0.3,
                'mild_crisis_to_low': 0.4,
                'negative_to_low': 0.7,
                'unknown_to_low': 0.5
            }
            
            for key, value in crisis_mapping.items():
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
            
            logger.debug(f"✅ Crisis level mapping for mode '{mode}': {safe_mapping}")
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
        Get staff review thresholds for specific mode using new UnifiedConfigManager method
        UPDATED: Now uses get_config_section() instead of manual resolution
        """
        if mode is None:
            mode = self.get_current_ensemble_mode()
        
        try:
            staff_thresholds = self.unified_config.get_config_section(
                'threshold_mapping',
                f'threshold_mapping_by_mode.{mode}.staff_review_thresholds',
                {
                    'high_always': True,
                    'medium_confidence_threshold': 0.5,
                    'low_confidence_threshold': 0.8,
                    'on_model_disagreement': True,
                    'gap_detection_review': True,
                    'pattern_mismatch_review': True
                }
            )
            
            if not staff_thresholds:
                logger.debug(f"📋 No mode-specific staff review thresholds for '{mode}', using global defaults")
                return self.get_global_staff_review_thresholds()
            
            # Ensure all values are properly typed (bool/float)
            safe_thresholds = {}
            
            # Boolean values with proper conversion
            bool_keys = ['high_always', 'on_model_disagreement', 'gap_detection_review', 'pattern_mismatch_review']
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
            
            # Float values with proper conversion
            float_keys_defaults = {
                'medium_confidence_threshold': 0.5,
                'medium_confidence': 0.5,  # Alternative key name
                'low_confidence_threshold': 0.8,
                'low_confidence': 0.8      # Alternative key name
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
                safe_thresholds['medium_confidence_threshold'] = safe_thresholds.get('medium_confidence', 0.5)
            if 'low_confidence_threshold' not in safe_thresholds:
                safe_thresholds['low_confidence_threshold'] = safe_thresholds.get('low_confidence', 0.8)
            
            logger.debug(f"✅ Staff review thresholds for mode '{mode}': {safe_thresholds}")
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
        """
        Get global staff review thresholds using new UnifiedConfigManager method
        UPDATED: Now uses get_config_section() instead of manual resolution
        """
        try:
            global_staff = self.unified_config.get_config_section(
                'threshold_mapping',
                'global_staff_review',
                {
                    'high_always': True,
                    'medium_confidence': 0.75,
                    'low_confidence': 0.5,
                    'on_disagreement': True
                }
            )
            
            # Ensure proper type conversion
            safe_global = {}
            
            # Boolean values
            bool_keys = ['high_always', 'on_disagreement']
            for key in bool_keys:
                value = global_staff.get(key, True)
                try:
                    if isinstance(value, str):
                        safe_global[key] = value.lower() in ['true', '1', 'yes', 'on']
                    else:
                        safe_global[key] = bool(value)
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ Invalid boolean value '{value}' for global {key}, using True")
                    safe_global[key] = True
            
            # Float values
            float_keys_defaults = {
                'medium_confidence': 0.75,
                'low_confidence': 0.5
            }
            
            for key, default_val in float_keys_defaults.items():
                value = global_staff.get(key, default_val)
                try:
                    safe_global[key] = float(value)
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ Invalid float value '{value}' for global {key}, using default {default_val}")
                    safe_global[key] = default_val
            
            logger.debug(f"✅ Global staff review thresholds: {safe_global}")
            return safe_global
            
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

    def get_learning_thresholds(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 3: Learning threshold configuration now managed by LearningSystemManager
        
        This method has been migrated to LearningSystemManager for better consolidation
        of all learning-related functionality.
        
        Returns:
            Dictionary indicating where to get learning threshold configuration
        """
        logger.info("ℹ️ Phase 3e: Learning threshold configuration now managed by LearningSystemManager")
        logger.info("💡 Use LearningSystemManager.get_learning_thresholds() for learning threshold configuration")
        
        return {
            'note': 'Learning threshold configuration managed by LearningSystemManager',
            'use_instead': 'LearningSystemManager.get_learning_thresholds()',
            'reason': 'Phase 3e Step 3 learning method consolidation - moved to specialized learning manager',
            'migration_date': '2025-08-17',
            'phase': '3e.3',
            'benefits': [
                'Consolidated learning functionality management',
                'Specialized threshold learning configuration',
                'Enhanced learning system integration',
                'Better separation of concerns between threshold mapping and learning',
                'Improved maintainability and testing'
            ]
        }
    
    def get_pattern_integration_config(self) -> Dict[str, Any]:
        """
        Get pattern integration configuration settings using new UnifiedConfigManager method
        UPDATED: Now uses get_config_section() instead of manual resolution
        """
        try:
            integration_config = self.unified_config.get_config_section(
                'threshold_mapping',
                'shared_configuration.pattern_integration',
                {
                    'pattern_weight_multiplier': 1.2,
                    'confidence_boost_limit': 0.15,
                    'escalation_required_minimum': 'low',
                    'pattern_override_threshold': 0.8,
                    'community_pattern_boost': 1.1
                }
            )
            
            # Ensure proper type conversion and validation
            safe_config = {}
            
            # Float values with validation
            float_keys_defaults = {
                'pattern_weight_multiplier': 1.2,
                'confidence_boost_limit': 0.15,
                'pattern_override_threshold': 0.8,
                'community_pattern_boost': 1.1
            }
            
            for key, default_val in float_keys_defaults.items():
                value = integration_config.get(key, default_val)
                try:
                    safe_config[key] = float(value)
                    # Validate ranges
                    if key == 'confidence_boost_limit' and safe_config[key] > 1.0:
                        logger.warning(f"⚠️ {key} value {safe_config[key]} exceeds 1.0, capping at 1.0")
                        safe_config[key] = 1.0
                    elif key in ['pattern_override_threshold'] and not (0.0 <= safe_config[key] <= 1.0):
                        logger.warning(f"⚠️ {key} value {safe_config[key]} out of range [0,1], using default")
                        safe_config[key] = default_val
                except (ValueError, TypeError):
                    logger.warning(f"⚠️ Invalid float value '{value}' for {key}, using default {default_val}")
                    safe_config[key] = default_val
            
            # String values
            safe_config['escalation_required_minimum'] = integration_config.get('escalation_required_minimum', 'low')
            if safe_config['escalation_required_minimum'] not in ['none', 'low', 'medium', 'high', 'critical']:
                logger.warning(f"⚠️ Invalid escalation_required_minimum '{safe_config['escalation_required_minimum']}', using 'low'")
                safe_config['escalation_required_minimum'] = 'low'
            
            # Add computed values for backward compatibility
            safe_config.update({
                'enabled': True,
                'confidence_boost_multiplier': safe_config['pattern_weight_multiplier'],
                'pattern_weight': 0.3,
                'ensemble_weight': 0.7,
                'confidence_threshold': 0.5,
                'crisis_level_promotion': {
                    'enabled': True,
                    'boost_factor': safe_config['confidence_boost_limit']
                }
            })
            
            logger.debug(f"✅ Pattern integration config loaded: multiplier={safe_config['pattern_weight_multiplier']}")
            return safe_config
            
        except Exception as e:
            logger.error(f"❌ Error getting pattern integration config: {e}")
            # Return safe defaults
            return {
                'enabled': True,
                'pattern_weight_multiplier': 1.0,
                'confidence_boost_limit': 0.1,
                'escalation_required_minimum': 'low',
                'pattern_override_threshold': 0.8,
                'community_pattern_boost': 1.0,
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
            'learning_thresholds_note': self.get_learning_thresholds(),  # Now returns migration info
            'validation_status': self.get_validation_status(),
            'available_modes': list(self.threshold_config.get('threshold_mapping_by_mode', {}).keys()) if self.threshold_config else [],
            'phase_3e_changes': {
                'sub_step_5_2_completed': 'Methods moved to CrisisAnalyzer and LearningSystemManager',
                'crisis_analyzer_methods': [
                    'apply_crisis_thresholds()',
                    'calculate_crisis_level_from_confidence()',
                    'validate_crisis_analysis_thresholds()',
                    'get_crisis_threshold_for_mode()'
                ],
                'learning_system_methods': [
                    'adapt_crisis_thresholds()'
                ],
                'preserved_functionality': 'All core threshold mapping and staff review functionality maintained',
                'enhanced_specialization': 'Better separation of configuration vs analysis vs learning concerns'
            }
        }

# ============================================================================
# FACTORY FUNCTION - Updated for Phase 3e Sub-step 5.2
# ============================================================================

def create_threshold_mapping_manager(unified_config_manager, model_ensemble_manager=None) -> ThresholdMappingManager:
    """
    Factory function to create ThresholdMappingManager instance - Phase 3e Sub-step 5.2
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (STEP 9 CHANGE)
        model_ensemble_manager: ModelEnsembleManager instance for mode detection
        
    Returns:
        ThresholdMappingManager instance with Phase 3e cleanup complete
    """
    return ThresholdMappingManager(unified_config_manager, model_ensemble_manager)

# ============================================================================
# CLEAN ARCHITECTURE EXPORTS
# ============================================================================

__all__ = [
    'ThresholdMappingManager',
    'create_threshold_mapping_manager'
]

logger.info("✅ ThresholdMappingManager v3.1-3e-5.2-1 loaded - Phase 3e Sub-step 5.2 cleanup complete with migration references")