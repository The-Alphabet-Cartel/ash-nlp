# ash/ash-nlp/managers/zero_shot_manager.py
"""
Zero-Shot Manager for Ash NLP Service v3.1 - Clean Architecture
Phase 3d Step 9: Updated for UnifiedConfigManager integration - NO MORE os.getenv() calls

Manages zero-shot classification labels and mappings
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ZeroShotManager:
    """
    Manager for zero-shot classification labels and mappings
    Phase 3d Step 9: Updated to use UnifiedConfigManager instead of direct os.getenv() calls
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
        self.current_label_set = "safety_first"  # Default from .env
        self.label_sets = {}
        self.current_labels = {}
        
        logger.info("✅ ZeroShotManager initialized with UnifiedConfigManager integration")
        
        # Load label sets
        self._load_label_sets()
        
        # Set initial label set from unified config (NO MORE os.getenv calls)
        initial_set = self.unified_config.get_env('NLP_ZERO_SHOT_LABEL_SET', 'safety_first')
        self.switch_label_set(initial_set)
    
    def _load_label_sets(self):
        """Load available label sets from JSON configuration file"""
        try:
            # Load label configuration using unified config manager
            label_config = self.unified_config.load_config_file('label_config')
            
            if not label_config:
                logger.error("❌ Could not load label_config.json, falling back to minimal defaults")
                self._load_fallback_label_sets()
                return
            
            # Extract label sets from JSON configuration
            label_sets_config = label_config.get('label_sets', {})
            
            if not label_sets_config:
                logger.error("❌ No label_sets found in label_config.json")
                self._load_fallback_label_sets()
                return
            
            # Load all label sets from configuration
            self.label_sets = {}
            for set_name, set_config in label_sets_config.items():
                self.label_sets[set_name] = {
                    'name': set_config.get('name', set_name),
                    'description': set_config.get('description', f'Label set: {set_name}'),
                    'labels': set_config.get('labels', {}),
                    'optimized_for': set_config.get('optimized_for', 'general'),
                    'sensitivity_level': set_config.get('sensitivity_level', 'medium'),
                    'recommended': set_config.get('recommended', False)
                }
            
            logger.info(f"✅ Loaded {len(self.label_sets)} label sets from label_config.json: {list(self.label_sets.keys())}")
            
            # Log recommended sets
            recommended_sets = [name for name, config in self.label_sets.items() if config.get('recommended', False)]
            if recommended_sets:
                logger.info(f"📋 Recommended label sets: {recommended_sets}")
            
        except Exception as e:
            logger.error(f"❌ Error loading label sets from JSON: {e}")
            logger.info("🔧 Falling back to minimal hardcoded label sets")
            self._load_fallback_label_sets()

    def _load_fallback_label_sets(self):
        """Load minimal fallback label sets if JSON loading fails"""
        logger.warning("⚠️ Using fallback label sets - limited functionality")
        
        self.label_sets = {
            'safety_first': {
                'name': 'Safety First (Fallback)',
                'description': 'Minimal fallback label set for emergency use',
                'labels': {
                    'depression': [
                        'person expressing crisis thoughts',
                        'person with severe symptoms', 
                        'person with moderate symptoms',
                        'person with mild symptoms',
                        'person with stable mental health'
                    ],
                    'sentiment': [
                        'extremely negative',
                        'negative',
                        'neutral',
                        'positive', 
                        'extremely positive'
                    ],
                    'emotional_distress': [
                        'severe crisis',
                        'high distress',
                        'moderate distress',
                        'low distress',
                        'stable'
                    ]
                },
                'optimized_for': 'fallback',
                'sensitivity_level': 'high',
                'recommended': False
            }
        }
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """
        Switch to a different label set with JSON configuration support
        
        Args:
            label_set_name: Name of the label set to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        if label_set_name not in self.label_sets:
            logger.error(f"❌ Unknown label set: {label_set_name}")
            logger.info(f"🔄 Available label sets: {list(self.label_sets.keys())}")
            
            # Try to get fallback from JSON config
            try:
                label_config = self.unified_config.load_config_file('label_config')
                fallback_set = label_config.get('configuration', {}).get('fallback_label_set', 'enhanced_crisis')
                
                if fallback_set in self.label_sets:
                    logger.info(f"🔧 Using configured fallback label set: {fallback_set}")
                    label_set_name = fallback_set
                else:
                    # Use first available set
                    available_sets = list(self.label_sets.keys())
                    if available_sets:
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
            self.current_labels = self.label_sets[label_set_name]['labels'].copy()
            
            # Get additional info from the label set
            set_info = self.label_sets[label_set_name]
            logger.info(f"✅ Switched to label set: {label_set_name}")
            logger.info(f"   📝 Description: {set_info.get('description', 'N/A')}")
            logger.info(f"   🎯 Optimized for: {set_info.get('optimized_for', 'N/A')}")
            logger.info(f"   📊 Sensitivity: {set_info.get('sensitivity_level', 'N/A')}")
            logger.debug(f"   📊 Labels loaded: {sum(len(labels) for labels in self.current_labels.values())} total")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error switching to label set {label_set_name}: {e}")
            return False
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label set names"""
        return list(self.label_sets.keys())
    
    def get_label_set_info(self, label_set_name: str = None) -> Dict[str, Any]:
        """
        Get detailed information about a label set
        
        Args:
            label_set_name: Name of label set (uses current if None)
            
        Returns:
            Dictionary with label set information
        """
        if label_set_name is None:
            label_set_name = self.current_label_set
        
        if label_set_name not in self.label_sets:
            return {'error': f'Label set {label_set_name} not found'}
        
        set_config = self.label_sets[label_set_name]
        
        return {
            'name': set_config.get('name', label_set_name),
            'description': set_config.get('description', ''),
            'optimized_for': set_config.get('optimized_for', 'general'),
            'sensitivity_level': set_config.get('sensitivity_level', 'medium'),
            'recommended': set_config.get('recommended', False),
            'total_labels': sum(len(labels) for labels in set_config.get('labels', {}).values()),
            'model_types': list(set_config.get('labels', {}).keys()),
            'is_current': label_set_name == self.current_label_set
        }
    
    def get_current_label_set_name(self) -> str:
        """Get current label set name"""
        return self.current_label_set
    
    def get_depression_labels(self) -> List[str]:
        """Get depression detection labels for current set"""
        return self.current_labels.get('depression', [])
    
    def get_sentiment_labels(self) -> List[str]:
        """Get sentiment analysis labels for current set"""
        return self.current_labels.get('sentiment', [])
    
    def get_emotional_distress_labels(self) -> List[str]:
        """Get emotional distress labels for current set"""
        return self.current_labels.get('emotional_distress', [])
    
    def get_all_labels(self) -> Dict[str, List[str]]:
        """Get all labels for current set"""
        return self.current_labels.copy()
    
    def get_labels_for_model(self, model_type: str) -> List[str]:
        """
        Get labels for a specific model type
        
        Args:
            model_type: Type of model ('depression', 'sentiment', 'emotional_distress')
            
        Returns:
            List of labels for the model type
        """
        return self.current_labels.get(model_type, [])
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get current manager status"""
        return {
            'current_label_set': self.current_label_set,
            'available_sets': self.get_available_label_sets(),
            'total_labels': sum(len(labels) for labels in self.current_labels.values()) if self.current_labels else 0,
            'models_supported': list(self.current_labels.keys()) if self.current_labels else [],
            'phase_3d_step_9': 'unified_config_manager_integrated'
        }
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get summary of configuration and current state"""
        # Get configuration from unified config manager
        label_set_from_config = self.unified_config.get_env('NLP_ZERO_SHOT_LABEL_SET', 'safety_first')
        
        return {
            'configured_label_set': label_set_from_config,
            'active_label_set': self.current_label_set,
            'configuration_matches': label_set_from_config == self.current_label_set,
            'available_label_sets': self.get_available_label_sets(),
            'current_labels_summary': {
                model_type: len(labels) 
                for model_type, labels in self.current_labels.items()
            } if self.current_labels else {},
            'unified_config_manager': 'operational'
        }
    
    def validate_label_set_configuration(self) -> Dict[str, Any]:
        """Validate that the configured label set is available and properly loaded"""
        configured_set = self.unified_config.get_env('NLP_ZERO_SHOT_LABEL_SET', 'safety_first')
        
        validation_result = {
            'valid': True,
            'configured_set': configured_set,
            'active_set': self.current_label_set,
            'issues': []
        }
        
        # Check if configured set exists
        if configured_set not in self.label_sets:
            validation_result['valid'] = False
            validation_result['issues'].append(f"Configured label set '{configured_set}' not found")
        
        # Check if current set matches configuration
        if configured_set != self.current_label_set:
            validation_result['issues'].append(f"Active set '{self.current_label_set}' differs from configured '{configured_set}'")
        
        # Check if current labels are loaded
        if not self.current_labels:
            validation_result['valid'] = False
            validation_result['issues'].append("No labels currently loaded")
        
        # Check that all expected model types have labels
        expected_models = ['depression', 'sentiment', 'emotional_distress']
        for model_type in expected_models:
            if model_type not in self.current_labels or not self.current_labels[model_type]:
                validation_result['valid'] = False
                validation_result['issues'].append(f"No labels found for model type '{model_type}'")
        
        return validation_result


# Factory function for Clean v3.1 Architecture
def create_zero_shot_manager(unified_config_manager) -> ZeroShotManager:
    """
    Create and return a ZeroShotManager instance
    Phase 3d Step 9: Updated to use UnifiedConfigManager
    
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