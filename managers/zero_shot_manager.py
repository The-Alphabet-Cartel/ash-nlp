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
        """Load available label sets"""
        # For now, use hardcoded label sets that match your .env configuration
        self.label_sets = {
            'safety_first': {
                'name': 'Safety First Labels',
                'description': 'Optimized for safety-first crisis detection',
                'labels': {
                    'depression': [
                        'person actively planning or considering suicide',
                        'person experiencing severe depression with crisis thoughts',
                        'person expressing hopelessness and despair',
                        'person feeling overwhelmed and unable to cope',
                        'person showing signs of crisis mental health state'
                    ],
                    'sentiment': [
                        'extremely negative and distressing',
                        'concerning and potentially harmful',
                        'sad and distressing',
                        'neutral or mixed sentiment',
                        'positive and hopeful'
                    ],
                    'emotional_distress': [
                        'severe emotional crisis requiring immediate attention',
                        'moderate emotional distress needing support',
                        'mild emotional concern',
                        'emotionally stable',
                        'positive emotional state'
                    ]
                }
            },
            'balanced': {
                'name': 'Balanced Detection Labels',
                'description': 'Balanced approach between safety and precision',
                'labels': {
                    'depression': [
                        'person expressing suicidal ideation',
                        'person with severe depression symptoms',
                        'person showing moderate depression signs',
                        'person with mild mood concerns',
                        'person with stable mood'
                    ],
                    'sentiment': [
                        'very negative',
                        'negative',
                        'neutral',
                        'positive',
                        'very positive'
                    ],
                    'emotional_distress': [
                        'high emotional distress',
                        'moderate emotional distress',
                        'low emotional distress',
                        'stable emotional state',
                        'positive emotional state'
                    ]
                }
            },
            'precise': {
                'name': 'High Precision Labels',
                'description': 'Optimized for precise classification with lower false positives',
                'labels': {
                    'depression': [
                        'explicit suicidal intent with plan',
                        'severe clinical depression with crisis features',
                        'moderate depression requiring professional help',
                        'mild depressive symptoms',
                        'no depression indicators'
                    ],
                    'sentiment': [
                        'extremely negative with crisis indicators',
                        'significantly negative',
                        'mildly negative',
                        'neutral',
                        'positive'
                    ],
                    'emotional_distress': [
                        'acute emotional crisis',
                        'significant emotional distress',
                        'moderate emotional concern',
                        'minor emotional fluctuation',
                        'emotional stability'
                    ]
                }
            }
        }
        
        logger.info(f"✅ Loaded {len(self.label_sets)} label sets: {list(self.label_sets.keys())}")
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """
        Switch to a different label set
        
        Args:
            label_set_name: Name of the label set to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        if label_set_name not in self.label_sets:
            logger.error(f"❌ Unknown label set: {label_set_name}")
            logger.info(f"Available sets: {list(self.label_sets.keys())}")
            return False
        
        self.current_label_set = label_set_name
        self.current_labels = self.label_sets[label_set_name]['labels']
        
        logger.info(f"✅ Switched to label set: {label_set_name}")
        logger.debug(f"Labels available: {list(self.current_labels.keys())}")
        
        return True
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label set names"""
        return list(self.label_sets.keys())
    
    def get_label_set_info(self, label_set_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific label set
        
        Args:
            label_set_name: Name of the label set
            
        Returns:
            Dictionary with label set information or None if not found
        """
        if label_set_name not in self.label_sets:
            return None
        
        set_info = self.label_sets[label_set_name].copy()
        set_info['total_labels'] = sum(len(labels) for labels in set_info['labels'].values())
        set_info['model_types'] = list(set_info['labels'].keys())
        
        return set_info
    
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