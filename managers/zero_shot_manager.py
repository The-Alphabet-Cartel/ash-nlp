# ash-nlp/managers/zero_shot_manager.py
"""
Zero-Shot Manager for Ash NLP Service
FILE VERSION: v3.1-3d-10.12-3
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ZeroShotManager:
    """
    Manager for zero-shot classification labels and mappings
    Updated for v3.1 configuration format with comprehensive label categories and validation
    Phase 3d Step 9: Updated to use UnifiedConfigManager with v3.1 label_config.json format
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
        
        logger.info("✅ ZeroShotManager v3.1 initialized with UnifiedConfigManager integration")
        
        # Load v3.1 label configuration
        self._load_label_configuration()
        
        # Set initial label set from unified config
        initial_set = self.label_mapping_config.get('default_label_set', 'enhanced_crisis')
        self.switch_label_set(initial_set)
    
    def _load_label_configuration(self):
        """Load v3.1 label configuration from JSON with environment overrides"""
        try:
            # Load label configuration using unified config manager
            label_config = self.unified_config.load_config_file('label_config')
            
            if not label_config:
                logger.error("❌ Could not load label_config.json, falling back to minimal defaults")
                self._load_fallback_configuration()
                return
            
            # Extract v3.1 configuration structure
            self.label_configuration = label_config.get('label_configuration', {})
            self.label_mapping_config = label_config.get('label_mapping', {})
            self.zero_shot_settings = label_config.get('zero_shot_settings', {})
            
            if not self.label_configuration:
                logger.error("❌ No label_configuration found in v3.1 label_config.json")
                self._load_fallback_configuration()
                return
            
            logger.info("✅ v3.1 label configuration loaded successfully")
            logger.debug(f"🔍 Label categories available: {list(self.label_configuration.keys())}")
            
            # Log available label categories
            available_categories = [key for key in self.label_configuration.keys() 
                                  if key not in ['label_mapping'] and isinstance(self.label_configuration[key], dict) 
                                  and any(isinstance(v, str) for v in self.label_configuration[key].values())]
            logger.info(f"📋 Available label categories: {available_categories}")
            
        except Exception as e:
            logger.error(f"❌ Error loading v3.1 label configuration: {e}")
            logger.info("🔧 Falling back to minimal hardcoded configuration")
            self._load_fallback_configuration()

    def _load_fallback_configuration(self):
        """Load minimal fallback configuration if v3.1 JSON loading fails"""
        logger.warning("⚠️ Using fallback label configuration - limited functionality")
        
        self.label_configuration = {
            "description": "Fallback baseline labels",
            "depression": "fallback_depression_labels",
            "sentiment": "fallback_sentiment_labels", 
            "emotional_distress": "fallback_distress_labels",
            "defaults": {
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
            },
            "validation": {
                "depression": {
                    "type": "list"
                },
                "sentiment": {
                    "type": "list"
                },
                "emotional_distress": {
                    "type": "list"
                }
            }
        }
        
        self.label_mapping_config = {
            "default_label_set": "enhanced_crisis",
            "enable_label_switching": true,
            "fallback_behavior": "enhanced_crisis",
            "case_sensitive": false,
            "normalize_labels": true,
            "defaults": {
                "default_label_set": "enhanced_crisis",
                "enable_label_switching": true,
                "fallback_behavior": "enhanced_crisis",
                "case_sensitive": false,
                "normalize_labels": true
            },
            "validation": {
                "default_label_set": {
                    "type": "string"
                },
                "enable_label_switching": {
                    "type": "boolean"
                },
                "fallback_behavior": {
                    "type": "string"
                },
                "case_sensitive": {
                    "type": "boolean"
                },
                "normalize_labels": {
                    "type": "boolean"
                }
            }
        }
        
        self.zero_shot_settings = {
            "track_performance": false,
            "hypothesis_template": "This text expresses {}.",
            "multi_label": false,
            "confidence_threshold": 0.3,
            "max_labels": 5,
            "normalize_scores": true,
            "defaults": {
                "track_performance": false,
                "hypothesis_template": "This text expresses {label}",
                "multi_label": false,
                "confidence_threshold": 0.3,
                "max_labels": 5,
                "normalize_scores": true
            },
            "validation": {
                "track_performance": {
                    "type": "boolean"
                },
                "hypothesis_template": {
                    "type": "string"
                },
                "multi_label": {
                    "type": "boolean"
                },
                "confidence_threshold": {
                    "type": "float",
                    "range": [0.0, 1.0]
                },
                "max_labels": {
                    "type": "integer",
                    "range": [1, 10]
                },
                "normalize_scores": {
                    "type": "boolean"
                }
            }
        }
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label set names from v3.1 configuration"""
        available_sets = []
        for key, value in self.label_configuration.items():
            # Skip label_mapping and other non-label categories
            if key != 'label_mapping' and isinstance(value, dict):
                # Check if it contains label definitions (string values that aren't 'description')
                has_labels = any(isinstance(v, str) and k != 'description' 
                               for k, v in value.items() 
                               if k not in ['defaults', 'validation'])
                if has_labels:
                    available_sets.append(key)
        
        return available_sets
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """
        Switch to a different label set with v3.1 configuration support
        
        Args:
            label_set_name: Name of the label set to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        available_sets = self.get_available_label_sets()
        
        if label_set_name not in available_sets:
            logger.error(f"❌ Unknown label set: {label_set_name}")
            logger.info(f"📄 Available label sets: {available_sets}")
            
            # Try fallback from configuration
            try:
                fallback_set = self.label_mapping_config.get('default_label_set', 'enhanced_crisis')
                defaults = self.label_mapping_config.get('defaults', {})
                if not fallback_set:
                    fallback_set = defaults.get('default_label_set', 'enhanced_crisis')
                
                if fallback_set in available_sets:
                    logger.info(f"🔧 Using configured fallback label set: {fallback_set}")
                    label_set_name = fallback_set
                elif available_sets:
                    # Use first available set
                    label_set_name = available_sets[0]
                    logger.info(f"🔧 Using first available label set: {label_set_name}")
                else:
                    logger.error("❌ No label sets available!")
                    return False
            except Exception as e:
                logger.error(f"❌ Error getting fallback label set: {e}")
                return False
        
        try:
            # Switch to the label set
            self.current_label_set = label_set_name
            label_set_config = self.label_configuration[label_set_name]
            
            # Extract labels from v3.1 configuration format
            self.current_labels = {}
            defaults = label_set_config.get('defaults', {})
            
            for key, value in label_set_config.items():
                if key not in ['description', 'defaults', 'validation'] and isinstance(value, str):
                    # Handle environment variable placeholders
                    if value.startswith('${') and value.endswith('}'):
                        # Fall back to defaults if placeholder not resolved
                        self.current_labels[key] = defaults.get(key, value)
                    else:
                        self.current_labels[key] = value
            
            logger.info(f"✅ Switched to label set: {label_set_name}")
            logger.info(f"   📋 Description: {label_set_config.get('description', 'N/A')}")
            logger.debug(f"   📊 Labels loaded: {len(self.current_labels)} labels")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error switching to label set {label_set_name}: {e}")
            return False
    
    def get_current_label_set_name(self) -> str:
        """Get current label set name"""
        return self.current_label_set
    
    def get_current_label_set(self) -> str:
        """Get current label set name (legacy alias)"""
        return self.get_current_label_set_name()
    
    def get_all_labels(self) -> Dict[str, str]:
        """Get all labels for current set"""
        return self.current_labels.copy()
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get current manager status"""
        return {
            'current_label_set': self.current_label_set,
            'available_sets': self.get_available_label_sets(),
            'total_labels': len(self.current_labels),
            'labels_loaded': list(self.current_labels.keys()),
            'v31_configuration': True,
            'phase_3d_step_9': 'unified_config_manager_integrated',
            'zero_shot_settings': {
                'hypothesis_template': self.zero_shot_settings.get('hypothesis_template', 'This text expresses {}.'),
                'multi_label': self.zero_shot_settings.get('multi_label', False),
                'confidence_threshold': self.zero_shot_settings.get('confidence_threshold', 0.5)
            }
        }
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get summary of configuration and current state"""
        # Get configuration from unified config manager
        configured_set = self.unified_config.get_env('NLP_ZERO_SHOT_LABEL_SET', 'crisis_labels')
        label_switching_enabled = self.unified_config.get_env('NLP_ZERO_SHOT_ENABLE_LABEL_SET_SWITCHING', True)
        
        return {
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
            'v31_format': True
        }
    
    def activate_profile(self, profile_name: str) -> bool:
        """
        Activate a label profile from configuration
        
        Args:
            profile_name: Name of the profile to activate
            
        Returns:
            Boolean indicating if profile was activated successfully
        """
        try:
            # Load profile configuration if available
            label_config = self.unified_config.load_config_file('label_config')
            profiles = label_config.get('label_profiles', {})
            
            if profile_name not in profiles:
                logger.warning(f"⚠️ Profile '{profile_name}' not found")
                return False
            
            profile = profiles[profile_name]
            logger.info(f"🔄 Activating label profile: {profile_name}")
            
            # Switch to profile's label set if specified
            if 'label_set' in profile:
                return self.switch_label_set(profile['label_set'])
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error activating profile '{profile_name}': {e}")
            return False


# Factory function for Clean v3.1 Architecture
def create_zero_shot_manager(unified_config_manager) -> ZeroShotManager:
    """
    Create and return a ZeroShotManager instance
    Updated for v3.1 configuration format
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (required)
        
    Returns:
        ZeroShotManager instance
    """
    return ZeroShotManager(unified_config_manager)

# Export for clean architecture
__all__ = [
    'ZeroShotManager',
    'create_zero_shot_manager'
]