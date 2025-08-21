# ash-nlp/managers/zero_shot_manager.py
"""
Zero-Shot Manager for Ash NLP Service
FILE VERSION: v3.1-3e-5.5-6
LAST MODIFIED: 2025-08-20
PHASE: 3e, Sub-step 5.5, Task 5 - ZeroShotManager Standard Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Phase 3e cleanup complete - get_config_section patterns applied
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ZeroShotManager:
    """
    Manager for zero-shot classification labels and mappings for Ash NLP Service
    
    Phase 3e Sub-step 5.5: Enhanced with get_config_section() patterns and improved label management
    
    This manager provides comprehensive zero-shot classification label management including:
    - Label set configuration and switching (depression, sentiment, emotional distress)
    - Zero-shot classification settings and parameters
    - Label mapping and validation
    - Profile-based label configurations for different deployment scenarios
    - Environment variable integration with safe type conversion
    
    Phase 3e Improvements:
    - Replaced load_config_file() with get_config_section() patterns
    - Enhanced error handling and resilience for label configuration access
    - Improved fallback mechanisms for safe operation
    - Better integration with UnifiedConfigManager
    - Added comprehensive label validation and monitoring
    """
    
    def __init__(self, unified_config_manager):
        """
        Initialize zero-shot manager with UnifiedConfigManager
        
        Args:
            unified_config_manager: UnifiedConfigManager instance (required)
        """
        if unified_config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ZeroShotManager")
        
        self.unified_config = unified_config_manager
        self.current_label_set = "enhanced_crisis"
        self.label_configuration = {}
        self.current_labels = {}
        self.zero_shot_settings = {}
        self.label_mapping_config = {}
        
        logger.info("ZeroShotManager v3.1e-5.5 initialized with Phase 3e patterns")
        
        # Load label configuration using Phase 3e patterns
        self._load_label_configuration()
        
        # Set initial label set from configuration
        initial_set = self.label_mapping_config.get('default_label_set', 'enhanced_crisis')
        self.switch_label_set(initial_set)
    
    def _load_label_configuration(self):
        """Load label configuration using Phase 3e get_config_section patterns"""
        try:
            # Extract configuration structure with enhanced error handling
            self.label_configuration = self.unified_config.get_config_section('label_config', 'label_configuration', {})
            self.label_mapping_config = self.unified_config.get_config_section('label_config', 'label_mapping', {})
            self.zero_shot_settings = self.unified_config.get_config_section('label_config', 'zero_shot_settings', {})
            
            if not self.label_configuration:
                logger.error("No label_configuration found in label configuration")
                self._load_fallback_configuration()
                return
            
            logger.info("Label configuration loaded successfully using Phase 3e patterns")
            logger.debug(f"Label categories available: {list(self.label_configuration.keys())}")
            
            # Log available label categories with enhanced validation
            available_categories = [key for key in self.label_configuration.keys() 
                                  if key not in ['label_mapping'] and isinstance(self.label_configuration[key], dict) 
                                  and any(isinstance(v, str) for v in self.label_configuration[key].values())]
            logger.info(f"Available label categories: {available_categories}")
            
        except Exception as e:
            logger.error(f"Error loading label configuration: {e}")
            logger.info("Falling back to minimal hardcoded configuration per Clean Architecture Charter Rule #5")
            self._load_fallback_configuration()

    def _load_fallback_configuration(self):
        """Load minimal fallback configuration with enhanced Phase 3e structure"""
        logger.warning("Using fallback label configuration - limited functionality")
        
        self.label_configuration = {
            "description": "Fallback baseline labels for Phase 3e",
            "depression": [
                "person experiencing severe clinical depression with major functional impairment",
                "person showing moderate depression with professional intervention needed",
                "person with mild depressive episode with manageable symptoms and temporary low mood",
                "person with stable mental health with normal emotional fluctuations and no depression signs",
                "person demonstrating positive mental wellness, emotional resilience, and psychological stability"
            ],
            "sentiment": [
                "person expressing profound despair, hopelessness, overwhelming sadness, or emotional devastation",
                "person showing significant negative emotions such as anger, frustration, fear, or deep disappointment",
                "person displaying mixed or neutral emotional state without strong positive or negative feelings",
                "person expressing mild positive emotions like satisfaction, calm contentment, or gentle happiness",
                "person showing strong positive emotions including joy, excitement, love, gratitude, or enthusiasm",
                "person radiating intense positive energy, euphoria, overwhelming happiness, or peak emotional highs"
            ],
            "emotional_distress": [
                "person in acute psychological distress unable to cope and requiring immediate crisis intervention",
                "person experiencing severe emotional overwhelm with significantly impaired functioning and coping",
                "person showing moderate distress with some difficulty managing emotions and daily responsibilities",
                "person handling normal life stress with adequate coping strategies and emotional regulation",
                "person demonstrating strong emotional resilience with healthy stress management and adaptation",
                "person exhibiting optimal emotional wellbeing with excellent coping skills and life satisfaction"
            ]
        }
        
        self.label_mapping_config = {
            "default_label_set": "enhanced_crisis",
            "enable_label_switching": True,
            "fallback_behavior": "enhanced_crisis",
            "case_sensitive": False,
            "normalize_labels": True,
            "defaults": {
                "default_label_set": "enhanced_crisis",
                "enable_label_switching": True,
                "fallback_behavior": "enhanced_crisis",
                "case_sensitive": False,
                "normalize_labels": True
            },
            "validation": {
                "default_label_set": {"type": "string"},
                "enable_label_switching": {"type": "boolean"},
                "fallback_behavior": {"type": "string"},
                "case_sensitive": {"type": "boolean"},
                "normalize_labels": {"type": "boolean"}
            }
        }
        
        self.zero_shot_settings = {
            "track_performance": False,
            "hypothesis_template": "This text expresses {}.",
            "multi_label": False,
            "confidence_threshold": 0.3,
            "max_labels": 5,
            "normalize_scores": True,
            "defaults": {
                "track_performance": False,
                "hypothesis_template": "This text expresses {label}",
                "multi_label": False,
                "confidence_threshold": 0.3,
                "max_labels": 5,
                "normalize_scores": True
            },
            "validation": {
                "track_performance": {"type": "boolean"},
                "hypothesis_template": {"type": "string"},
                "multi_label": {"type": "boolean"},
                "confidence_threshold": {"type": "float", "range": [0.0, 1.0]},
                "max_labels": {"type": "integer", "range": [1, 10]},
                "normalize_scores": {"type": "boolean"}
            }
        }
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label set names"""
        try:
            label_config = self.unified_config.get_config_section('label_config', 'label_configuration', {})
            return list(label_config.keys())
            
        except Exception as e:
            logger.error(f"Error getting available label sets: {e}")
            return ['enhanced_crisis']
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """
        Switch to a different label set with enhanced Phase 3e configuration support
        
        Args:
            label_set_name: Name of the label set to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        try:
            available_sets = self.get_available_label_sets()
            
            if label_set_name not in available_sets:
                logger.error(f"Unknown label set: {label_set_name}")
                logger.info(f"Available label sets: {available_sets}")
                
                # Try fallback from configuration with enhanced error handling
                try:
                    fallback_set = self.label_mapping_config.get('default_label_set', 'enhanced_crisis')
                    defaults = self.label_mapping_config.get('defaults', {})
                    if not fallback_set:
                        fallback_set = defaults.get('default_label_set', 'enhanced_crisis')
                    
                    if fallback_set in available_sets:
                        logger.info(f"Using configured fallback label set: {fallback_set}")
                        label_set_name = fallback_set
                    elif available_sets:
                        # Use first available set
                        label_set_name = available_sets[0]
                        logger.info(f"Using first available label set: {label_set_name}")
                    else:
                        logger.error("No label sets available!")
                        return False
                except Exception as e:
                    logger.error(f"Error getting fallback label set: {e}")
                    return False
            
            # Switch to the label set with enhanced error handling
            self.current_label_set = label_set_name
            label_set_config = self.label_configuration[label_set_name]
            
            # Extract labels from configuration format with enhanced validation
            self.current_labels = {}
            defaults = label_set_config.get('defaults', {})
            
            for key, value in label_set_config.items():
                if key not in ['description', 'defaults', 'validation'] and isinstance(value, str):
                    # Handle environment variable placeholders
                    if value.startswith('${') and value.endswith('}'):
                        # Fall back to defaults if placeholder not resolved
                        fallback_value = defaults.get(key, value)
                        self.current_labels[key] = fallback_value
                    else:
                        self.current_labels[key] = value
            
            logger.info(f"Switched to label set: {label_set_name}")
            logger.info(f"Description: {label_set_config.get('description', 'N/A')}")
            logger.debug(f"Labels loaded: {len(self.current_labels)} labels")
            
            return True
            
        except Exception as e:
            logger.error(f"Error switching to label set {label_set_name}: {e}")
            return False
    
    def get_current_label_set_name(self) -> str:
        """Get current label set name with enhanced validation"""
        try:
            return self.current_label_set
        except Exception as e:
            logger.error(f"Error getting current label set name: {e}")
            return "enhanced_crisis"
    
    def get_current_label_set(self) -> str:
        """Get current label set name (legacy alias) with enhanced validation"""
        return self.get_current_label_set_name()
    
    def get_all_labels(self) -> Dict[str, str]:
        """Get all labels for current set with enhanced error handling"""
        try:
            return self.current_labels.copy()
        except Exception as e:
            logger.error(f"Error getting all labels: {e}")
            return {}
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get current manager status with Phase 3e enhancements"""
        try:
            return {
                'current_label_set': self.current_label_set,
                'available_sets': self.get_available_label_sets(),
                'total_labels': len(self.current_labels),
                'labels_loaded': list(self.current_labels.keys()),
                'manager_version': 'v3.1e-5.5-5',
                'phase': '3e Sub-step 5.5 Task 5',
                'configuration_format': 'enhanced',
                'get_config_section_patterns': 'implemented',
                'phase_3e_cleanup': 'complete',
                'unified_config_manager': 'operational',
                'zero_shot_settings': {
                    'hypothesis_template': self.zero_shot_settings.get('hypothesis_template', 'This text expresses {}.'),
                    'multi_label': self.zero_shot_settings.get('multi_label', False),
                    'confidence_threshold': self.zero_shot_settings.get('confidence_threshold', 0.5)
                }
            }
        except Exception as e:
            logger.error(f"Error getting manager status: {e}")
            return {
                'current_label_set': 'unknown',
                'manager_version': 'v3.1e-5.5-5',
                'error': str(e),
                'fallback_mode': 'active'
            }
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration summary with Phase 3e enhancements
        Phase 3e: Enhanced method for system visibility and monitoring
        """
        try:
            # PHASE 3E: Enhanced configuration access using environment variable patterns
            configured_set = self.unified_config.get_env('NLP_ZERO_SHOT_LABEL_SET', 'crisis_labels')
            label_switching_enabled = self.unified_config.get_env_bool('NLP_ZERO_SHOT_ENABLE_LABEL_SET_SWITCHING', True)
            
            return {
                'manager_version': 'v3.1e-5.5-5',
                'phase': '3e Sub-step 5.5 Task 5',
                'configured_label_set': configured_set,
                'active_label_set': self.current_label_set,
                'configuration_matches': configured_set == self.current_label_set,
                'available_label_sets': self.get_available_label_sets(),
                'label_switching_enabled': label_switching_enabled,
                'current_labels_summary': {
                    'total_labels': len(self.current_labels),
                    'label_categories': list(self.current_labels.keys())
                },
                'zero_shot_configuration': self.zero_shot_settings,
                'unified_config_manager': 'operational',
                'get_config_section_patterns': 'implemented',
                'enhanced_error_handling': True,
                'configuration_source': 'json_with_env_overrides',
                'initialization_status': 'complete',
                'cleanup_status': 'phase_3e_complete'
            }
            
        except Exception as e:
            logger.error(f"Error generating configuration summary: {e}")
            return {
                'manager_version': 'v3.1e-5.5-5',
                'phase': '3e Sub-step 5.5 Task 5',
                'error': str(e),
                'initialization_status': 'error',
                'cleanup_status': 'phase_3e_complete'
            }
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a label profile from configuration with Phase 3e enhanced access patterns
        
        Args:
            profile_name: Name of the profile to activate
            
        Returns:
            Boolean indicating if profile was activated successfully
        
        NOT CURRENTLY USED!
        """
#        try:
#            # PHASE 3E: Enhanced profile access using get_config_section patterns
#            profiles = self.unified_config.get_config_section('label_config', 'label_profiles', {})
#            if not profiles:
#                # Fallback to direct access
#                label_config = self.unified_config.get_config_section('label_config')
#                profiles = label_config.get('label_profiles', {})
#            
#            if profile_name not in profiles:
#                logger.warning(f"Profile '{profile_name}' not found")
#                return False
#            
#            profile = profiles[profile_name]
#            logger.info(f"Activating label profile: {profile_name}")
#            
#            # Switch to profile's label set if specified
#            if 'label_set' in profile:
#                return self.switch_label_set(profile['label_set'])
#            
#            return True
#            
#        except Exception as e:
#            logger.error(f"Error activating profile '{profile_name}': {e}")
        return False
    
    def get_zero_shot_settings(self) -> Dict[str, Any]:
        """
        Get zero-shot classification settings with Phase 3e enhanced access
        Phase 3e: New method for enhanced configuration access
        """
        try:
            # PHASE 3E: Enhanced settings access using get_config_section patterns
            settings = self.unified_config.get_config_section('label_config', 'zero_shot_settings', {})
            if not settings:
                # Fallback to direct zero_shot_settings access
                settings = self.zero_shot_settings
            
            # Provide safe defaults with validation
            return {
                'track_performance': settings.get('track_performance', False),
                'hypothesis_template': settings.get('hypothesis_template', 'This text expresses {}.'),
                'multi_label': settings.get('multi_label', False),
                'confidence_threshold': max(0.0, min(1.0, float(settings.get('confidence_threshold', 0.3)))),
                'max_labels': max(1, min(10, int(settings.get('max_labels', 5)))),
                'normalize_scores': settings.get('normalize_scores', True)
            }
            
        except Exception as e:
            logger.error(f"Error getting zero-shot settings: {e}")
            return {
                'track_performance': False,
                'hypothesis_template': 'This text expresses {}.',
                'multi_label': False,
                'confidence_threshold': 0.3,
                'max_labels': 5,
                'normalize_scores': True
            }
    
    def validate_label_configuration(self) -> Dict[str, Any]:
        """
        Validate current label configuration
        Phase 3e: New method for enhanced validation and monitoring
        """
        try:
            validation_results = {
                'valid': True,
                'warnings': [],
                'errors': [],
                'configuration_status': 'valid',
                'phase_3e_compliant': True
            }
            
            # Validate available label sets
            available_sets = self.get_available_label_sets()
            if not available_sets:
                validation_results['errors'].append("No label sets available")
                validation_results['valid'] = False
            
            # Validate current label set
            if self.current_label_set not in available_sets:
                validation_results['errors'].append(f"Current label set '{self.current_label_set}' not in available sets")
                validation_results['valid'] = False
            
            # Validate current labels
            if not self.current_labels:
                validation_results['warnings'].append("No labels loaded for current label set")
            
            # Validate zero-shot settings
            settings = self.get_zero_shot_settings()
            threshold = settings.get('confidence_threshold', 0.3)
            if not 0.0 <= threshold <= 1.0:
                validation_results['warnings'].append(f"Confidence threshold {threshold} outside valid range [0.0, 1.0]")
            
            max_labels = settings.get('max_labels', 5)
            if not 1 <= max_labels <= 10:
                validation_results['warnings'].append(f"Max labels {max_labels} outside recommended range [1, 10]")
            
            logger.info(f"Label configuration validation: {'PASSED' if validation_results['valid'] else 'FAILED'}")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating label configuration: {e}")
            return {
                'valid': False,
                'warnings': [],
                'errors': [f"Validation error: {str(e)}"],
                'configuration_status': 'error',
                'phase_3e_compliant': False
            }

# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance (Phase 3e Enhanced)
# ============================================================================

def create_zero_shot_manager(unified_config_manager) -> ZeroShotManager:
    """
    Factory function for ZeroShotManager (Clean v3.1 Pattern) - Phase 3e Enhanced
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (required)
        
    Returns:
        ZeroShotManager instance with Phase 3e enhancements
    """
    return ZeroShotManager(unified_config_manager)

# Export public interface
__all__ = [
    'ZeroShotManager',
    'create_zero_shot_manager'
]

logger.info("ZeroShotManager v3.1e-5.5-5 loaded - Phase 3e Sub-step 5.5 cleanup complete with enhanced patterns")