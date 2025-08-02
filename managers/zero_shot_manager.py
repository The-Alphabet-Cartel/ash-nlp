#!/usr/bin/env python3
"""
Zero-Shot Labels Configuration Loader for Ash NLP Service
Location: ash/ash-nlp/config/zero_shot_config.py

Loads label configurations from label_config.json following the same pattern as ash-thrash
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LabelSetInfo:
    """Information about a label set"""
    name: str
    description: str
    optimized_for: str
    sensitivity_level: str
    recommended: bool = False
    label_counts: Dict[str, int] = None

class ZeroShotLabelsConfig:
    """
    Configuration loader for zero-shot labels, following ash-thrash pattern.
    Loads from label_config.json file with fallback to hardcoded defaults.
    """
    
    def __init__(self, config_file: str = "label_config.json"):
        self.config_file = config_file
        self.config = None
        self.current_label_set_name = None
        self.current_labels = None
        self.current_mapping_rules = None
        
        # Load configuration
        self._load_config()
        
        # Set initial label set
        initial_set = self._get_initial_label_set()
        self.switch_label_set(initial_set)
        
    def _load_config(self):
        """Load configuration from JSON file with fallback"""
        try:
            # Try multiple possible paths for the JSON file (same pattern as ash-thrash)
            possible_paths = [
                Path(__file__).parent / self.config_file,                    # config/label_config.json
                Path(__file__).parent.parent / "config" / self.config_file,  # ../config/label_config.json from models/
                Path(self.config_file),                                      # label_config.json from cwd  
                Path("config") / self.config_file,                          # config/label_config.json from cwd
                Path.cwd() / "config" / self.config_file,                   # Absolute from current working directory
            ]
            
            config_file_path = None
            for path in possible_paths:
                if path.exists():
                    config_file_path = path
                    break
            
            if config_file_path:
                logger.info(f"✅ Loading label configuration from: {config_file_path}")
                with open(config_file_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    logger.info(f"📋 Loaded {len(self.config.get('label_sets', {}))} label sets")
            else:
                logger.warning(f"⚠️ Could not find {self.config_file} in any of these locations:")
                for path in possible_paths:
                    logger.warning(f"     - {path} (exists: {path.exists()})")
                logger.warning("⚠️ Using hardcoded fallback configuration")
                self.config = self._get_fallback_config()
                
        except Exception as e:
            logger.error(f"⚠️ Error loading {self.config_file}: {e}")
            logger.warning("⚠️ Using hardcoded fallback configuration")
            self.config = self._get_fallback_config()
    
    def _get_fallback_config(self) -> Dict[str, Any]:
        """Hardcoded fallback configuration if JSON file is unavailable"""
        return {
            "version": "1.0",
            "description": "Fallback configuration - JSON file not found",
            "default_label_set": "enhanced_crisis",
            "label_sets": {
                "enhanced_crisis": {
                    "name": "Enhanced Crisis Detection (Fallback)",
                    "description": "Crisis-optimized fallback labels",
                    "optimized_for": "high_crisis_detection",
                    "sensitivity_level": "high",
                    "labels": {
                        "depression": [
                            "person actively expressing suicidal thoughts or specific plans to end their life",
                            "person expressing complete hopelessness or being beyond help",
                            "person describing active self-harm or severe depression with breakdown",
                            "person experiencing moderate depression but maintaining some functioning",
                            "person showing stable mental health with normal emotional fluctuations"
                        ],
                        "sentiment": [
                            "person expressing devastating emotional pain or complete despair",
                            "person showing significant emotional pain or distressing emotions",
                            "person expressing neutral emotions or balanced feelings",
                            "person expressing contentment, gratitude, or positive emotions",
                            "person expressing intense joy, excitement, or overwhelming happiness"
                        ],
                        "emotional_distress": [
                            "person in acute psychological crisis, completely unable to cope",
                            "person experiencing severe emotional overwhelm with major difficulty",
                            "person experiencing moderate emotional distress with some difficulty",
                            "person handling typical life stress with adequate coping",
                            "person demonstrating excellent emotional resilience and wellbeing"
                        ]
                    },
                    "mapping_rules": {
                        "depression": {
                            "severe_patterns": ["suicidal thoughts", "end their life", "complete hopelessness", "beyond help"],
                            "moderate_patterns": ["active self-harm", "severe depression", "breakdown"],
                            "mild_patterns": ["moderate depression", "maintaining some functioning"],
                            "none_patterns": ["stable mental health", "normal emotional"]
                        },
                        "sentiment": {
                            "very_negative_patterns": ["devastating emotional pain", "complete despair"],
                            "negative_patterns": ["significant emotional pain", "distressing emotions"],
                            "neutral_patterns": ["neutral emotions", "balanced feelings"],
                            "positive_patterns": ["contentment", "gratitude", "positive emotions"],
                            "very_positive_patterns": ["intense joy", "overwhelming happiness"]
                        },
                        "emotional_distress": {
                            "high_patterns": ["acute psychological crisis", "unable to cope"],
                            "medium_patterns": ["moderate emotional distress", "some difficulty"],
                            "low_patterns": ["typical life stress", "adequate coping"],
                            "none_patterns": ["excellent emotional resilience"]
                        }
                    }
                }
            }
        }
    
    def _get_initial_label_set(self) -> str:
        """Get initial label set from environment or config default"""
        # Check environment variable first (same pattern as ash-thrash)
        env_label_set = os.getenv('NLP_ZERO_SHOT_LABEL_SET')
        if env_label_set and env_label_set in self.get_available_label_sets():
            return env_label_set
        
        # Use config default
        default_set = self.config.get('default_label_set', 'enhanced_crisis')
        if default_set in self.get_available_label_sets():
            return default_set
        
        # Fallback to first available
        available_sets = self.get_available_label_sets()
        if available_sets:
            return available_sets[0]
        
        # This should never happen with fallback config
        raise ValueError("No label sets available")
    
    # =============================================================================
    # PUBLIC API METHODS
    # =============================================================================
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label set names"""
        return list(self.config.get('label_sets', {}).keys())
    
    def get_label_set_info(self, label_set_name: str) -> Optional[LabelSetInfo]:
        """Get information about a specific label set"""
        label_sets = self.config.get('label_sets', {})
        if label_set_name not in label_sets:
            return None
        
        label_set = label_sets[label_set_name]
        labels = label_set.get('labels', {})
        
        return LabelSetInfo(
            name=label_set.get('name', label_set_name),
            description=label_set.get('description', ''),
            optimized_for=label_set.get('optimized_for', 'general'),
            sensitivity_level=label_set.get('sensitivity_level', 'medium'),
            recommended=label_set.get('recommended', False),
            label_counts={
                model: len(model_labels) 
                for model, model_labels in labels.items()
            }
        )
    
    def get_current_label_set_name(self) -> str:
        """Get currently active label set name"""
        return self.current_label_set_name
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """Switch to a different label set"""
        label_sets = self.config.get('label_sets', {})
        if label_set_name not in label_sets:
            logger.error(f"Unknown label set: {label_set_name}")
            return False
        
        label_set = label_sets[label_set_name]
        self.current_label_set_name = label_set_name
        self.current_labels = label_set.get('labels', {})
        self.current_mapping_rules = label_set.get('mapping_rules', {})
        
        logger.info(f"🔄 Switched to label set: {label_set_name}")
        return True
    
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
    
    # =============================================================================
    # MAPPING METHODS (using JSON configuration)
    # =============================================================================
    
    def map_depression_label(self, long_label: str) -> str:
        """Map depression specialist labels to crisis categories"""
        label_lower = long_label.lower()
        rules = self.current_mapping_rules.get('depression', {})
        
        # Check patterns in order of severity
        for severity, patterns in [
            ('severe', rules.get('severe_patterns', [])),
            ('moderate', rules.get('moderate_patterns', [])),
            ('mild', rules.get('mild_patterns', [])),
            ('none', rules.get('none_patterns', []))
        ]:
            if any(pattern.lower() in label_lower for pattern in patterns):
                if severity == "severe":
                    return "severe"
                elif severity == "moderate":
                    return "moderate"
                elif severity == "mild":
                    return "mild"
                else:
                    return "not depression"
        
        return "not depression"  # Default safe
    
    def map_sentiment_label(self, long_label: str) -> str:
        """Map sentiment specialist labels to emotional categories"""
        label_lower = long_label.lower()
        rules = self.current_mapping_rules.get('sentiment', {})
        
        # Check patterns in order
        for sentiment, patterns in [
            ('Very Negative', rules.get('very_negative_patterns', [])),
            ('Negative', rules.get('negative_patterns', [])),
            ('Neutral', rules.get('neutral_patterns', [])),
            ('Positive', rules.get('positive_patterns', [])),
            ('Very Positive', rules.get('very_positive_patterns', []))
        ]:
            if any(pattern.lower() in label_lower for pattern in patterns):
                return sentiment
        
        return "Neutral"  # Default neutral
    
    def map_distress_label(self, long_label: str) -> str:
        """Map distress specialist labels to stress categories"""
        label_lower = long_label.lower()
        rules = self.current_mapping_rules.get('emotional_distress', {})
        
        # Check patterns in order of severity
        for distress_level, patterns in [
            ('High Distress', rules.get('high_patterns', [])),
            ('Medium Distress', rules.get('medium_patterns', [])),
            ('Low Distress', rules.get('low_patterns', [])),
            ('No Distress', rules.get('none_patterns', []))
        ]:
            if any(pattern.lower() in label_lower for pattern in patterns):
                return distress_level
        
        return "Low Distress"  # Default safe
    
    # =============================================================================
    # CONFIGURATION INFO METHODS
    # =============================================================================
    
    def get_config_info(self) -> Dict[str, Any]:
        """Get comprehensive configuration information"""
        current_info = self.get_label_set_info(self.current_label_set_name)
        
        return {
            'version': self.config.get('version', '1.0'),
            'description': self.config.get('description', ''),
            'current_set': {
                'name': self.current_label_set_name,
                'info': current_info.__dict__ if current_info else None
            },
            'available_sets': [
                {
                    'name': name,
                    'info': self.get_label_set_info(name).__dict__
                }
                for name in self.get_available_label_sets()
            ],
            'total_label_sets': len(self.get_available_label_sets()),
            'configuration': self.config.get('configuration', {}),
            'metadata': self.config.get('metadata', {})
        }
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get statistics about current label set"""
        if not self.current_labels:
            return {}
        
        return {
            'label_set': self.current_label_set_name,
            'model_counts': {
                model: len(labels) 
                for model, labels in self.current_labels.items()
            },
            'total_labels': sum(len(labels) for labels in self.current_labels.values()),
            'has_mapping_rules': bool(self.current_mapping_rules)
        }

# =============================================================================
# GLOBAL INSTANCE AND CONVENIENCE FUNCTIONS
# =============================================================================

# Global instance (singleton pattern)
_global_config = None

def get_labels_config() -> ZeroShotLabelsConfig:
    """Get global labels configuration instance"""
    global _global_config
    if _global_config is None:
        _global_config = ZeroShotLabelsConfig()
    return _global_config

def reload_labels_config():
    """Reload labels configuration from file"""
    global _global_config
    _global_config = ZeroShotLabelsConfig()
    logger.info("♻️ Reloaded labels configuration from JSON file")

# Convenience functions for backward compatibility
def get_depression_labels() -> List[str]:
    """Get depression detection labels"""
    return get_labels_config().get_depression_labels()

def get_sentiment_labels() -> List[str]:
    """Get sentiment analysis labels"""
    return get_labels_config().get_sentiment_labels()

def get_emotional_distress_labels() -> List[str]:
    """Get emotional distress labels"""
    return get_labels_config().get_emotional_distress_labels()

def switch_label_set(label_set_name: str) -> bool:
    """Switch global configuration to different label set"""
    return get_labels_config().switch_label_set(label_set_name)

def get_current_label_set() -> str:
    """Get current label set name"""
    return get_labels_config().get_current_label_set_name()

# Mapping functions for models
def map_depression_zero_shot_label(long_label: str) -> str:
    """Map depression labels using current configuration"""
    return get_labels_config().map_depression_label(long_label)

def map_sentiment_zero_shot_label(long_label: str) -> str:
    """Map sentiment labels using current configuration"""
    return get_labels_config().map_sentiment_label(long_label)

def map_distress_zero_shot_label(long_label: str) -> str:
    """Map distress labels using current configuration"""
    return get_labels_config().map_distress_label(long_label)