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
        """Get current ensemble mode from ModelEnsembleManager"""
        try:
            if self.model_ensemble_manager:
                return self.model_ensemble_manager.get_current_ensemble_mode()
            else:
                # Fallback to environment variable
                return self.unified_config.get_env_str('NLP_ENSEMBLE_MODE', 'consensus')
                
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
        """Validate threshold configuration consistency"""
        try:
            self._validation_errors = []
            
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
                        
                        # Validate threshold ranges
                        for threshold_name, threshold_value in mapping.items():
                            if not 0.0 <= threshold_value <= 1.0:
                                error_msg = f"Threshold {threshold_name} in {mode} mode outside valid range [0.0, 1.0]: {threshold_value}"
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