# ash/ash-nlp/managers/zero_shot_manager.py
"""
Zero-Shot Manager for Ash NLP Service v3.1 - Clean Architecture
Manages zero-shot classification labels and mappings
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ZeroShotManager:
    """Manager for zero-shot classification labels and mappings"""
    
    def __init__(self, config_manager):
        """
        Initialize zero-shot manager
        
        Args:
            config_manager: ConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("ConfigManager is required for ZeroShotManager")
        
        self.config_manager = config_manager
        self.current_label_set = "safety_first"  # Default from .env
        self.label_sets = {}
        self.current_labels = {}
        
        logger.info("✅ ZeroShotManager initialized with ConfigManager integration")
        
        # Load label sets
        self._load_label_sets()
        
        # Set initial label set from environment
        initial_set = os.getenv('NLP_ZERO_SHOT_LABEL_SET', 'safety_first')
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
                        'person showing moderate depression symptoms',
                        'person experiencing mild sadness or temporary low mood',
                        'person showing stable mental health and emotional wellbeing'
                    ],
                    'sentiment': [
                        'devastating emotional pain and complete despair',
                        'significant emotional distress and negative feelings',
                        'neutral emotional state with balanced feelings',
                        'positive emotions and general contentment',
                        'intense joy and overwhelming happiness'
                    ],
                    'emotional_distress': [
                        'person in acute psychological crisis unable to cope',
                        'person experiencing severe emotional overwhelm',
                        'person handling moderate stress with some difficulty',
                        'person managing typical life challenges adequately',
                        'person demonstrating excellent emotional resilience'
                    ]
                }
            },
            'enhanced_crisis': {
                'name': 'Enhanced Crisis Detection',
                'description': 'Enhanced labels for comprehensive crisis detection',
                'labels': {
                    'depression': [
                        'person expressing active suicidal ideation or plans',
                        'person in severe depressive crisis requiring immediate intervention',
                        'person experiencing moderate depression affecting functioning',
                        'person with mild depressive symptoms manageable daily',
                        'person with healthy emotional regulation and stability'
                    ],
                    'sentiment': [
                        'extreme negative emotions with crisis-level distress',
                        'strong negative emotions causing significant impact',
                        'balanced emotional state without distress',
                        'positive emotional state with satisfaction',
                        'exceptionally positive emotions and euphoria'
                    ],
                    'emotional_distress': [
                        'person completely overwhelmed unable to function',
                        'person experiencing high distress impacting function',
                        'person with moderate distress but maintaining function',
                        'person with minimal distress handling challenges',
                        'person with optimal emotional functioning'
                    ]
                }
            }
        }
        
        logger.info(f"✅ Loaded {len(self.label_sets)} label sets")
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label set names"""
        return list(self.label_sets.keys())
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """
        Switch to a different label set
        
        Args:
            label_set_name: Name of the label set to switch to
            
        Returns:
            True if successful, False if label set not found
        """
        if label_set_name not in self.label_sets:
            logger.error(f"❌ Unknown label set: {label_set_name}")
            return False
        
        self.current_label_set = label_set_name
        self.current_labels = self.label_sets[label_set_name]['labels']
        
        logger.info(f"🔄 Switched to label set: {label_set_name}")
        return True
    
    def get_current_label_set(self) -> str:
        """Get currently active label set name"""
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
            'models_supported': list(self.current_labels.keys()) if self.current_labels else []
        }


# Factory function 
def create_zero_shot_manager(config_manager) -> ZeroShotManager:
    """Create and return a ZeroShotManager instance"""
    return ZeroShotManager(config_manager)

# Export for clean architecture
__all__ = [
    'ZeroShotManager',
    'create_zero_shot_manager'
]