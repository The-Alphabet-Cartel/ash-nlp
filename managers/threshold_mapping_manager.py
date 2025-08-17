# ash-nlp/managers/threshold_mapping_manager.py
"""
Mode-Aware Threshold Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3e-3.3-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 3.3 - Learning Integration Points Added
CLEAN ARCHITECTURE: v3.1 Compliant
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
    
    Phase 3e Step 3.3: Learning integration points added for LearningSystemManager compatibility
    Phase 3d Step 10.7: Added missing determine_crisis_level method
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
        self.config = None
        self._validation_errors = []
        
        # Load threshold mapping configuration using unified manager
        self._load_threshold_mapping_config()
        
        logger.info("ThresholdMappingManager v3.1e Step 3.3 initialized - Learning integration points added")
    
    def _load_threshold_mapping_config(self):
        """Load threshold mapping configuration using UnifiedConfigManager correctly"""
        try:
            # Load threshold mapping configuration through unified manager
            raw_config = self.unified_config.load_config_file('threshold_mapping')
            
            if not raw_config:
                logger.warning("⚠️ Threshold mapping configuration not found, using environment fallbacks")
                self.threshold_config = self._get_fallback_threshold_config()
            else:
                # FIXED: Use UCM's substitute_environment_variables() method like other managers
                self.threshold_config = self.unified_config.substitute_environment_variables(raw_config)
                logger.debug("✅ Environment variable substitution complete via UnifiedConfigManager")
            
            # Validate threshold configuration
            self._validate_threshold_config()
            
            logger.info("✅ Threshold mapping configuration loaded and validated")
            
        except Exception as e:
            logger.error(f"❌ Error loading threshold mapping configuration: {e}")
            self._validation_errors.append(f"Configuration loading error: {str(e)}")
    
    
    # NOTE: Custom v3.1 config processing methods removed - now using UCM.substitute_environment_variables()
    # This eliminates ~200 lines of duplicate environment variable resolution code
    # and ensures consistent behavior with other managers like AnalysisParametersManager
    

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
            # managers/threshold_mapping_manager.py
"""
Threshold Mapping Manager for Ash-NLP Service v3.1
FILE VERSION: v3.1-3e-3.3-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 3.3 - Learning Integration Points Updated
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from managers.unified_config_manager import UnifiedConfigManager

# Configure logging
logger = logging.getLogger(__name__)


class ThresholdMappingManager:
    """
    Threshold Mapping Manager for mode-aware crisis level determination
    
    Phase 3e Step 3.3: Learning adjustment functionality now references LearningSystemManager
    
    Responsibilities (Post-Phase 3e):
    - Load threshold configurations from JSON
    - Provide mode-specific threshold mappings (consensus, majority, weighted)
    - Determine crisis levels based on confidence scores
    - Provide learning threshold configuration (static)
    - Reference LearningSystemManager for dynamic threshold adjustments
    
    Clean v3.1 Architecture:
    - Factory function pattern for object creation
    - Dependency injection (UnifiedConfigManager, ModelEnsembleManager)
    - Mode-aware threshold determination
    """
    
    def __init__(self, unified_config: UnifiedConfigManager, model_ensemble_manager=None):
        """
        Initialize ThresholdMappingManager with dependency injection
        
        Args:
            unified_config: UnifiedConfigManager instance for configuration
            model_ensemble_manager: ModelEnsembleManager for mode detection
        """
        self.unified_config = unified_config
        self.model_ensemble_manager = model_ensemble_manager
        self.config_dir = Path("config")
        self.threshold_config = {}
        self._validation_errors = []
        
        # Load threshold configuration
        self._load_threshold_configuration()
        
        logger.info("✅ ThresholdMappingManager initialized successfully")
    
    def _load_threshold_configuration(self):
        """Load threshold configuration from JSON with environment overrides"""
        try:
            config_file = self.config_dir / "threshold_mapping.json"
            
            if not config_file.exists():
                logger.warning(f"⚠️ Threshold configuration file not found: {config_file}")
                self.threshold_config = self._get_default_threshold_config()
                return
            
            with open(config_file, 'r') as f:
                raw_config = json.load(f)
            
            # Apply environment variable substitution
            self.threshold_config = self.unified_config.substitute_environment_variables(raw_config)
            
            # Validate configuration
            self._validate_threshold_config()
            
            logger.info(f"✅ Threshold configuration loaded from {config_file}")
            
        except Exception as e:
            logger.error(f"❌ Error loading threshold configuration: {e}")
            self.threshold_config = self._get_default_threshold_config()
    
    def _get_default_threshold_config(self) -> Dict[str, Any]:
        """Get default threshold configuration as fallback"""
        return {
            'threshold_mapping_by_mode': {
                'consensus': {
                    'crisis_level_mapping': {
                        'crisis_to_high': 0.50,
                        'crisis_to_medium': 0.30,
                        'mild_crisis_to_low': 0.40,
                        'negative_to_low': 0.70,
                        'unknown_to_low': 0.50
                    }
                },
                'majority': {
                    'crisis_level_mapping': {
                        'crisis_to_high': 0.45,
                        'crisis_to_medium': 0.25,
                        'mild_crisis_to_low': 0.35,
                        'negative_to_low': 0.65,
                        'unknown_to_low': 0.45
                    }
                },
                'weighted': {
                    'crisis_level_mapping': {
                        'crisis_to_high': 0.40,
                        'crisis_to_medium': 0.20,
                        'mild_crisis_to_low': 0.30,
                        'negative_to_low': 0.60,
                        'unknown_to_low': 0.40
                    }
                }
            },
            'staff_review_thresholds': {
                'high_confidence': 0.85,
                'medium_confidence': 0.75,
                'low_confidence': 0.5,
                'on_disagreement': True
            },
            'learning_thresholds': {
                'learning_rate': 0.1,
                'max_adjustments_per_day': 50,
                'min_confidence_for_learning': 0.3
            }
        }
    
    # ========================================================================
    # CORE THRESHOLD MAPPING METHODS
    # ========================================================================
    
    def get_current_ensemble_mode(self) -> str:
        """Get current ensemble mode from UnifiedConfdigManager"""
        try:
            config = self.unified_config.get_config('model_ensemble')
            mode = config.get('ensemble_config', {}).get('mode', 'majority')
                
        except Exception as e:
            logger.warning(f"⚠️ Error getting ensemble mode: {e}, using default")
            return 'consensus'
    
    def determine_crisis_level(self, confidence: float, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Determine crisis level based on confidence score and mode-specific thresholds
        
        Args:
            confidence: Confidence score from analysis (0.0 to 1.0)
            context: Optional context for threshold adjustments
            
        Returns:
            Crisis level: 'high', 'medium', 'low', or 'none'
        """
        try:
            current_mode = self.get_current_ensemble_mode()
            mapping = self.get_crisis_level_mapping_for_mode(current_mode)
            
            # Apply thresholds in order from highest to lowest
            if confidence >= mapping['crisis_to_high']:
                return 'high'
            elif confidence >= mapping['crisis_to_medium']:
                return 'medium'
            elif confidence >= mapping['mild_crisis_to_low']:
                return 'low'
            else:
                return 'none'
                
        except Exception as e:
            logger.error(f"❌ Error determining crisis level: {e}")
            # Safe fallback
            if confidence >= 0.7:
                return 'high'
            elif confidence >= 0.5:
                return 'medium'
            elif confidence >= 0.3:
                return 'low'
            else:
                return 'none'
    
    def get_crisis_level_mapping_for_mode(self, mode: Optional[str] = None) -> Dict[str, float]:
        """
        Get crisis level mapping for specific ensemble mode
        
        Args:
            mode: Ensemble mode ('consensus', 'majority', 'weighted')
            
        Returns:
            Dictionary with crisis level thresholds
        """
        try:
            if mode is None:
                mode = self.get_current_ensemble_mode()
            
            mode_config = self.threshold_config.get('threshold_mapping_by_mode', {})
            mapping = mode_config.get(mode, {}).get('crisis_level_mapping', {})
            
            return {
                'crisis_to_high': float(mapping.get('crisis_to_high', 0.50)),
                'crisis_to_medium': float(mapping.get('crisis_to_medium', 0.30)),
                'mild_crisis_to_low': float(mapping.get('mild_crisis_to_low', 0.40)),
                'negative_to_low': float(mapping.get('negative_to_low', 0.70)),
                'unknown_to_low': float(mapping.get('unknown_to_low', 0.50))
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting crisis level mapping for mode {mode}: {e}")
            return {
                'crisis_to_high': 0.50,
                'crisis_to_medium': 0.30,
                'mild_crisis_to_low': 0.40,
                'negative_to_low': 0.70,
                'unknown_to_low': 0.50
            }
    
    def get_staff_review_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, Any]:
        """
        Get staff review thresholds for specific mode
        
        Args:
            mode: Ensemble mode (currently mode-independent)
            
        Returns:
            Dictionary with staff review configuration
        """
        try:
            review_config = self.threshold_config.get('staff_review_thresholds', {})
            
            return {
                'high_confidence': float(review_config.get('high_confidence', 0.85)),
                'medium_confidence': float(review_config.get('medium_confidence', 0.75)),
                'low_confidence': float(review_config.get('low_confidence', 0.5)),
                'on_disagreement': bool(review_config.get('on_disagreement', True)),
                'require_staff_review': True
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting staff review thresholds: {e}")
            return {
                'high_confidence': 0.85,
                'medium_confidence': 0.75,
                'low_confidence': 0.5,
                'on_disagreement': True,
                'require_staff_review': True
            }
    
    # ========================================================================
    # LEARNING THRESHOLD CONFIGURATION (STATIC) - PHASE 3E STEP 3.3
    # ========================================================================
    
    def get_learning_thresholds(self) -> Dict[str, Any]:
        """
        Get learning system threshold configuration (static configuration only)
        
        Phase 3e Step 3.3: For dynamic learning adjustments, use LearningSystemManager
        
        Returns:
            Dictionary with learning threshold configuration
        """
        try:
            learning_config = self.threshold_config.get('learning_thresholds', {})
            
            result = {
                'learning_rate': float(learning_config.get('learning_rate', 0.1)),
                'max_adjustments_per_day': int(learning_config.get('max_adjustments_per_day', 50)),
                'min_confidence_for_learning': float(learning_config.get('min_confidence_for_learning', 0.3)),
                'note': 'For dynamic threshold adjustments, use LearningSystemManager',
                'learning_manager_methods': [
                    'adjust_threshold_false_positive()',
                    'adjust_threshold_false_negative()',
                    'process_feedback()'
                ]
            }
            
            logger.info("ℹ️ Static learning thresholds provided. Use LearningSystemManager for dynamic adjustments.")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting learning thresholds: {e}")
            return {
                'learning_rate': 0.1,
                'max_adjustments_per_day': 50,
                'min_confidence_for_learning': 0.3,
                'note': 'For dynamic threshold adjustments, use LearningSystemManager'
            }
    
    # ========================================================================
    # LEARNING INTEGRATION METHODS - PHASE 3E STEP 3.3
    # ========================================================================
    
    def get_adaptive_threshold_info(self) -> Dict[str, Any]:
        """
        Get information about adaptive threshold adjustment capabilities
        
        Phase 3e Step 3.3: Adaptive threshold adjustment now managed by LearningSystemManager
        
        Returns:
            Information about where to find adaptive threshold functionality
        """
        logger.info("ℹ️ Phase 3e: Adaptive threshold adjustment now managed by LearningSystemManager")
        
        return {
            'note': 'Adaptive threshold adjustment managed by LearningSystemManager',
            'static_thresholds': 'Available via get_crisis_level_mapping_for_mode()',
            'dynamic_adjustments': 'Use LearningSystemManager.adjust_threshold_false_positive/negative()',
            'integration_point': 'LearningSystemManager should be used alongside ThresholdMappingManager',
            'workflow': [
                '1. Get base thresholds from ThresholdMappingManager',
                '2. Apply dynamic adjustments via LearningSystemManager',
                '3. Use adjusted thresholds for crisis level determination'
            ]
        }
    
    def supports_learning_adjustment(self) -> bool:
        """
        Check if learning-based threshold adjustment is conceptually supported
        
        Returns:
            True - this manager provides base thresholds for learning adjustment
        """
        return True
    
    # ========================================================================
    # COMPREHENSIVE THRESHOLD ACCESS
    # ========================================================================
    
    def get_ensemble_thresholds_for_mode(self, mode: Optional[str] = None) -> Dict[str, Any]:
        """
        Get complete threshold configuration for ensemble mode
        
        Args:
            mode: Ensemble mode ('consensus', 'majority', 'weighted')
            
        Returns:
            Complete threshold configuration
        """
        try:
            if mode is None:
                mode = self.get_current_ensemble_mode()
            
            return {
                'mode': mode,
                'crisis_level_mapping': self.get_crisis_level_mapping_for_mode(mode),
                'staff_review_thresholds': self.get_staff_review_thresholds_for_mode(mode),
                'learning_thresholds': self.get_learning_thresholds(),
                'adaptive_threshold_info': self.get_adaptive_threshold_info()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting ensemble thresholds for mode {mode}: {e}")
            return {
                'mode': mode or 'consensus',
                'crisis_level_mapping': self.get_crisis_level_mapping_for_mode(),
                'staff_review_thresholds': self.get_staff_review_thresholds_for_mode(),
                'learning_thresholds': self.get_learning_thresholds(),
                'error': str(e)
            }
    
    # ========================================================================
    # VALIDATION AND STATUS METHODS
    # ========================================================================
    
    def _validate_threshold_config(self):
        """
        Validate threshold configuration consistency with proper type conversion
        
        FIXED: Ensures all threshold values are converted to floats before comparison
        to prevent "TypeError: '<=' not supported between instances of 'float' and 'str'"
        """
        try:
            self._validation_errors = []
            
            # Validate mode-specific thresholds
            if 'threshold_mapping_by_mode' in self.threshold_config:
                for mode, mode_config in self.threshold_config['threshold_mapping_by_mode'].items():
                    if 'crisis_level_mapping' in mode_config:
                        mapping = mode_config['crisis_level_mapping']
                        
                        # FIXED: Safely convert threshold values to floats before comparison
                        try:
                            crisis_high = float(mapping.get('crisis_to_high', 0.5))
                        except (ValueError, TypeError):
                            logger.warning(f"⚠️ Invalid crisis_to_high value in {mode} mode: {mapping.get('crisis_to_high')}, using default 0.5")
                            crisis_high = 0.5
                        
                        try:
                            crisis_medium = float(mapping.get('crisis_to_medium', 0.3))
                        except (ValueError, TypeError):
                            logger.warning(f"⚠️ Invalid crisis_to_medium value in {mode} mode: {mapping.get('crisis_to_medium')}, using default 0.3")
                            crisis_medium = 0.3
                        
                        # Now we can safely compare floats
                        if crisis_high <= crisis_medium:
                            error_msg = f"Invalid threshold ordering in {mode} mode: crisis_to_high ({crisis_high}) <= crisis_to_medium ({crisis_medium})"
                            logger.warning(f"⚠️ {error_msg}")
                            self._validation_errors.append(error_msg)
                        
                        # Validate all threshold values are within valid range [0.0, 1.0]
                        for threshold_name, threshold_value in mapping.items():
                            try:
                                threshold_float = float(threshold_value)
                                if not 0.0 <= threshold_float <= 1.0:
                                    error_msg = f"Threshold {threshold_name} in {mode} mode outside valid range [0.0, 1.0]: {threshold_float}"
                                    logger.warning(f"⚠️ {error_msg}")
                                    self._validation_errors.append(error_msg)
                            except (ValueError, TypeError):
                                error_msg = f"Invalid threshold value for {threshold_name} in {mode} mode: {threshold_value} (not convertible to float)"
                                logger.warning(f"⚠️ {error_msg}")
                                self._validation_errors.append(error_msg)
            
            # Validate ensemble thresholds if present
            if 'threshold_mapping_by_mode' in self.threshold_config:
                for mode, mode_config in self.threshold_config['threshold_mapping_by_mode'].items():
                    if 'ensemble_thresholds' in mode_config:
                        ensemble_thresholds = mode_config['ensemble_thresholds']
                        
                        # Validate ensemble threshold ordering (high > medium > low)
                        try:
                            high_thresh = float(ensemble_thresholds.get('high', 0.5))
                            medium_thresh = float(ensemble_thresholds.get('medium', 0.3))
                            low_thresh = float(ensemble_thresholds.get('low', 0.15))
                            
                            if not (high_thresh > medium_thresh > low_thresh):
                                error_msg = f"Invalid ensemble threshold ordering in {mode} mode: high ({high_thresh}) should be > medium ({medium_thresh}) should be > low ({low_thresh})"
                                logger.warning(f"⚠️ {error_msg}")
                                self._validation_errors.append(error_msg)
                                
                        except (ValueError, TypeError) as e:
                            error_msg = f"Invalid ensemble threshold values in {mode} mode: {e}"
                            logger.warning(f"⚠️ {error_msg}")
                            self._validation_errors.append(error_msg)
            
            # Report validation results
            if self._validation_errors:
                logger.warning(f"⚠️ Threshold validation found {len(self._validation_errors)} issues")
                for error in self._validation_errors:
                    logger.debug(f"   - {error}")
            else:
                logger.info("✅ Threshold configuration validation passed")
                
        except Exception as e:
            error_msg = f"Threshold validation error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            self._validation_errors.append(error_msg)
            
            # Log the problematic configuration for debugging
            logger.debug(f"Problematic threshold config: {self.threshold_config}")
    
    
    def get_validation_status(self) -> Dict[str, Any]:
        """Get validation status of threshold configuration"""
        return {
            'is_valid': len(self._validation_errors) == 0,
            'errors': self._validation_errors,
            'total_errors': len(self._validation_errors),
            'modes_configured': list(self.threshold_config.get('threshold_mapping_by_mode', {}).keys()) if self.threshold_config else [],
            'current_mode': self.get_current_ensemble_mode(),
            'learning_integration': 'LearningSystemManager provides dynamic threshold adjustments'
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
            'available_modes': list(self.threshold_config.get('threshold_mapping_by_mode', {}).keys()) if self.threshold_config else [],
            'adaptive_threshold_note': 'Use LearningSystemManager for dynamic threshold adjustments'
        }
    
    def reload_configuration(self) -> bool:
        """Reload threshold configuration from files"""
        try:
            self._load_threshold_configuration()
            logger.info("✅ Threshold configuration reloaded successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error reloading threshold configuration: {e}")
            return False


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_threshold_mapping_manager(unified_config_manager: UnifiedConfigManager, 
                                    model_ensemble_manager=None) -> ThresholdMappingManager:
    """
    Factory function to create ThresholdMappingManager with dependency injection
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for configuration
        model_ensemble_manager: Optional ModelEnsembleManager for mode detection
        
    Returns:
        ThresholdMappingManager instance ready for crisis level determination
        
    Raises:
        RuntimeError: If initialization fails
    """
    try:
        if not unified_config_manager:
            raise ValueError("unified_config_manager is required")
        
        manager = ThresholdMappingManager(unified_config_manager, model_ensemble_manager)
        
        # Verify initialization
        status = manager.get_validation_status()
        if not status['is_valid']:
            logger.warning(f"⚠️ ThresholdMappingManager has {status['total_errors']} validation issues")
        
        logger.info("✅ ThresholdMappingManager created successfully via factory function")
        return manager
        
    except Exception as e:
        logger.error(f"❌ Failed to create ThresholdMappingManager: {e}")
        raise RuntimeError(f"ThresholdMappingManager factory function failed: {e}")


# ============================================================================
# EXPORT FOR CLEAN ARCHITECTURE
# ============================================================================

__all__ = [
    'ThresholdMappingManager',
    'create_threshold_mapping_manager'
]