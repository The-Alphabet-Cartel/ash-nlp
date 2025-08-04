# ash/ash-nlp/managers/settings_manager.py (Phase 3a Updated)
"""
Settings Manager for Ash NLP Service v3.1 - Phase 3a Crisis Patterns Integration
Handles runtime settings and configuration overrides with crisis patterns from ConfigManager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# PATTERN CONSTANTS FOR COMPONENT COMPATIBILITY (FALLBACK ONLY)
# Phase 3a: These are now fallbacks - primary source is ConfigManager JSON
# ============================================================================

# Server configuration - PRESERVED (not part of crisis patterns migration)
SERVER_CONFIG = {
    "version": "4.1",
    "architecture": "modular",
    "hardware_info": {
        "cpu": "Ryzen 7 7700x",
        "gpu": "RTX 3050 (8GB VRAM)",
        "ram": "64GB",
        "inference_device": "GPU",
        "models_loaded": 3
    },
    "capabilities": {
        "crisis_analysis": "Original depression + sentiment analysis",
        "phrase_extraction": "Extract crisis keywords using model scoring",
        "pattern_learning": "Learn distinctive crisis patterns from community messages", 
        "semantic_analysis": "Enhanced crisis detection with community context",
        "community_awareness": "LGBTQIA+ specific pattern recognition"
    }
}

# Crisis level mapping thresholds - PRESERVED (not part of crisis patterns migration)
CRISIS_THRESHOLDS = {
    "high": 0.55,    # Reduced from 0.50 - matches new systematic approach
    "medium": 0.28,  # Reduced from 0.22 - more selective for medium alerts
    "low": 0.16      # Reduced from 0.12 - avoids very mild expressions
}

# Default parameters for analysis - PRESERVED (not part of crisis patterns migration)
DEFAULT_PARAMS = {
    'phrase_extraction': {
        'min_phrase_length': 2,
        'max_phrase_length': 6,
        'crisis_focus': True,
        'community_specific': True,
        'min_confidence': 0.3,
        'max_results': 20
    },
    'pattern_learning': {
        'min_crisis_messages': 10,
        'max_phrases_to_analyze': 200,
        'min_distinctiveness_ratio': 2.0,
        'min_frequency': 3,
        'confidence_thresholds': {
            'high_confidence': 0.7,
            'medium_confidence': 0.4,
            'low_confidence': 0.1
        }
    },
    'semantic_analysis': {
        'context_window': 3,  # Words around community terms
        'boost_weights': {
            'high_relevance': 0.1,
            'medium_relevance': 0.05,
            'family_rejection': 0.15,
            'discrimination_fear': 0.15,
            'support_seeking': -0.05  # Reduces crisis level (positive)
        }
    }
}

# Phase 3a: CRISIS PATTERNS NOW LOADED FROM CONFIGMANAGER JSON FILES
# These constants are kept as FALLBACKS ONLY for backward compatibility

# Context patterns for detection (FALLBACK - Primary: ConfigManager JSON)
POSITIVE_CONTEXT_PATTERNS = {
    'humor': ['joke', 'funny', 'hilarious', 'laugh', 'comedy', 'lol', 'haha'],
    'entertainment': ['movie', 'show', 'game', 'book', 'story', 'video'],
    'work_success': ['work', 'job', 'project', 'performance', 'success', 'achievement'],
    'food': ['hungry', 'eat', 'food', 'burger', 'pizza', 'meal'],
    'fatigue': ['tired', 'exhausted', 'sleepy', 'worn out'],
    'frustration': ['traffic', 'homework', 'test', 'exam', 'assignment']
}

IDIOM_PATTERNS = [
    (r'\b(dead|dying) (tired|exhausted)\b', 'fatigue'),
    (r'\bjoke (killed|murdered) me\b', 'humor'),
    (r'\b(that|it) (killed|murdered) me\b', 'humor'),
    (r'\bdying of laughter\b', 'humor'),
    (r'\b(killing|slaying) it\b', 'success'),
    (r'\bmurder (a|some) \w+\b', 'desire'),
    (r'\bdriving me (crazy|insane|nuts)\b', 'frustration'),
    (r'\b(brutal|killer) (test|exam|workout)\b', 'difficulty')
]

# LGBTQIA+ community patterns (FALLBACK - Primary: ConfigManager JSON)
LGBTQIA_PATTERNS = {
    # Family rejection patterns (HIGH crisis)
    'family_rejection': {
        'patterns': [
            r'family (rejected|disowned|kicked out|threw out) me',
            r'parents (don\'t|won\'t) (accept|love|support) me',
            r'(mom|dad|mother|father) (rejected|disowned) me',
            r'family (doesn\'t|won\'t) accept (my|me being)',
            r'(religious|conservative) family'
        ],
        'crisis_level': 'high',
        'category': 'family_rejection'
    },
    
    # Identity crisis patterns (MEDIUM)
    'identity_crisis': {
        'patterns': [
            r'(gender|trans|gay|lesbian|bi) (panic|crisis|confusion)',
            r'questioning (my|myself|everything)',
            r'(internalized|religious) (homophobia|shame|guilt)',
            r'(coming out|pride) (anxiety|stress|fear)',
            r'(closet|hiding) (suffocating|exhausting|killing me)'
        ],
        'crisis_level': 'medium',
        'category': 'identity_crisis'
    },
    
    # Dysphoria and transition patterns (MEDIUM)
    'dysphoria_transition': {
        'patterns': [
            r'(gender|body) dysphoria',
            r'(transition|dysphoria) (regret|doubt|scared|anxiety)',
            r'(deadnamed|misgendered) (me|today|again|constantly)',
            r'(passing|voice|body) (anxiety|dysphoria|stress)',
            r'(hormone|surgery) (regret|doubt|scared)'
        ],
        'crisis_level': 'medium',
        'category': 'dysphoria_transition'
    },
    
    # Discrimination and safety patterns (HIGH)
    'discrimination_safety': {
        'patterns': [
            r'(hate crime|discrimination|harassment)',
            r'(conversion therapy|pray away|religious trauma)',
            r'(unsafe|scared) (to be|being) (myself|gay|trans)',
            r'(workplace|school) (discrimination|harassment)',
            r'(violent|aggressive) (homophobia|transphobia)'
        ],
        'crisis_level': 'high',
        'category': 'discrimination_safety'
    },
    
    # Community support patterns (LOW - positive but worth tracking)
    'community_support': {
        'patterns': [
            r'(chosen|found) family',
            r'(pride|community) (support|family|love)',
            r'(lgbtq|queer) (community|support|friends)',
            r'(ally|allies) (support|help|love)'
        ],
        'crisis_level': 'low',
        'category': 'community_support'
    }
}

CRISIS_CONTEXTS = {
    'temporal_urgency': {
        'indicators': ['right now', 'tonight', 'today', 'immediately', 'urgent'],
        'context_type': 'temporal_urgency',
        'crisis_boost': 'high'
    },
    'intensity_amplifier': {
        'indicators': ['extremely', 'incredibly', 'absolutely', 'completely', 'totally'],
        'context_type': 'intensity_amplifier', 
        'crisis_boost': 'medium'
    },
    'social_isolation': {
        'indicators': ['no one', 'nobody', 'alone', 'isolated', 'abandoned'],
        'context_type': 'social_isolation',
        'crisis_boost': 'medium'
    },
    'capability_loss': {
        'indicators': ['can\'t', 'unable', 'impossible', 'won\'t be able'],
        'context_type': 'capability_loss',
        'crisis_boost': 'medium'
    }
}

COMMUNITY_VOCABULARY = {
    'identity_terms': [
        'trans', 'transgender', 'gay', 'lesbian', 'bisexual', 'pansexual', 
        'asexual', 'queer', 'enby', 'nonbinary', 'genderfluid'
    ],
    'experience_terms': [
        'coming out', 'dysphoria', 'euphoria', 'transition', 'deadname', 
        'chosen name', 'passing', 'binding', 'misgendered'
    ],
    'community_terms': [
        'chosen family', 'found family', 'pride', 'ally', 'safe space', 
        'visibility', 'representation'
    ],
    'struggle_terms': [
        'closeted', 'discrimination', 'homophobia', 'transphobia', 
        'religious trauma', 'internalized shame'
    ]
}

TEMPORAL_INDICATORS = {
    'immediate': ['right now', 'immediately', 'urgent', 'asap', 'tonight'],
    'recent': ['today', 'yesterday', 'lately', 'recently', 'this week'],
    'ongoing': ['always', 'constantly', 'every day', 'all the time', 'never stops'],
    'future_fear': ['never get better', 'will never', 'hopeless', 'pointless', 'no future']
}

CONTEXT_WEIGHTS = {
    'crisis_context_words': [
        'struggling', 'difficult', 'hard', 'painful', 'scared', 'worried', 
        'anxious', 'depressed', 'rejected', 'alone', 'isolated', 'hate', 'hurt'
    ],
    'positive_context_words': [
        'proud', 'happy', 'celebrating', 'love', 'support', 'accepted', 
        'supported', 'community', 'friends', 'family'
    ]
}

ENHANCED_IDIOM_PATTERNS = [
    {
        'patterns': [r'\b(dead|dying) (tired|exhausted|beat)\b'],
        'required_context': lambda msg: not any(word in msg.lower() for word in ['depressed', 'sad', 'hopeless', 'hate', 'kill myself']),
        'reduction_factor': 0.15,
        'max_score_after': 0.10,
        'name': 'fatigue_idiom'
    },
    {
        'patterns': [r'\b(joke|that|it) (killed|murdered) me\b', r'\bdying of laughter\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['funny', 'hilarious', 'laugh', 'lol', 'haha']),
        'reduction_factor': 0.05,
        'max_score_after': 0.08,
        'name': 'humor_idiom'
    },
    {
        'patterns': [r'\b(killing|slaying|crushing) it\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['work', 'job', 'performance', 'success']),
        'reduction_factor': 0.10,
        'max_score_after': 0.05,
        'name': 'success_idiom'
    },
    {
        'patterns': [r'\bmurder (a|some) \w+\b', r'\bcould kill for\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['food', 'hungry', 'eat', 'burger', 'pizza']),
        'reduction_factor': 0.08,
        'max_score_after': 0.05,
        'name': 'food_craving_idiom'
    },
    {
        'patterns': [r'\bdriving me (crazy|insane|nuts)\b', r'\b(brutal|killer) (test|exam|homework)\b'],
        'required_context': lambda msg: any(word in msg.lower() for word in ['traffic', 'homework', 'test', 'exam', 'work']),
        'reduction_factor': 0.12,
        'max_score_after': 0.08,
        'name': 'frustration_idiom'
    }
]

BURDEN_PATTERNS = [
    'better off without me', 'everyone would be better without me',
    'better off if i was gone', 'better off if i wasn\'t here',
    'nobody would miss me', 'wouldn\'t be missed'
]

HOPELESSNESS_PATTERNS = [
    'everything feels pointless', 'life feels pointless',
    'i hate my life', 'hate my life',
    'wish i could disappear', 'want to disappear'
]

STRUGGLE_PATTERNS = [
    'really struggling', 'struggling so much',
    'can\'t take it anymore', 'can\'t go on'
]

NEGATION_PATTERNS = [
    r'\bnot (really|actually|that|very|going to|planning to|trying to)\b',
    r'\bdoesn\'t (really|actually|mean|want to)\b',
    r'\bisn\'t (really|actually|that)\b',
    r'\bwon\'t (really|actually|ever)\b',
    r'\bdon\'t (want to|plan to|intend to)\b'
]

# ============================================================================
# SETTINGS MANAGER CLASS - PHASE 3A UPDATED
# ============================================================================

class SettingsManager:
    """Settings manager for runtime configuration and overrides - Phase 3a Enhanced"""
    
    def __init__(self, config_manager):
        """
        Initialize settings manager with ConfigManager integration
        
        Args:
            config_manager: ConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("ConfigManager is required for SettingsManager")
        
        self.config_manager = config_manager
        self.runtime_settings = {}
        self.setting_overrides = {}
        
        # Phase 3a: Crisis patterns from ConfigManager (not hardcoded constants)
        self.crisis_patterns_cache = {}
        self.crisis_patterns_loaded = False
        
        logger.info("✅ SettingsManager initialized with ConfigManager integration (Phase 3a)")
        
        # Load initial settings
        self._load_initial_settings()
        
        # Phase 3a: Load crisis patterns from ConfigManager
        self._load_crisis_patterns_from_config()
    
    def _load_initial_settings(self):
        """Load initial settings from configuration"""
        try:
            # Get hardware settings
            hardware_config = self.config_manager.get_hardware_configuration()
            self.runtime_settings['hardware'] = hardware_config
            
            # Get feature flags
            feature_flags = self.config_manager.get_feature_flags()
            self.runtime_settings['features'] = feature_flags
            
            # Get threshold settings
            threshold_config = self.config_manager.get_threshold_configuration()
            self.runtime_settings['thresholds'] = threshold_config
            
            logger.info("✅ Initial settings loaded from ConfigManager")
            
        except Exception as e:
            logger.error(f"❌ Failed to load initial settings: {e}")
            self.runtime_settings = {}
    
    def _load_crisis_patterns_from_config(self):
        """Phase 3a: Load crisis patterns from ConfigManager JSON files"""
        try:
            logger.info("🔍 Loading crisis patterns from ConfigManager JSON files...")
            
            # Get all crisis patterns from ConfigManager
            all_patterns = self.config_manager.get_crisis_patterns()
            
            if all_patterns:
                self.crisis_patterns_cache = all_patterns
                self.crisis_patterns_loaded = True
                
                # Log summary
                pattern_count = len(all_patterns)
                enabled_count = sum(1 for p in all_patterns.values() 
                                   if p.get('configuration', {}).get('enabled', True))
                
                logger.info(f"✅ Loaded {pattern_count} crisis pattern types from JSON ({enabled_count} enabled)")
                
                # Log details for each pattern type
                for pattern_type, pattern_data in all_patterns.items():
                    config = pattern_data.get('configuration', {})
                    metadata = pattern_data.get('metadata', {})
                    enabled = config.get('enabled', True)
                    total_patterns = metadata.get('total_patterns', 'unknown')
                    source = metadata.get('source', 'JSON')
                    
                    status = "✅ enabled" if enabled else "❌ disabled"
                    logger.debug(f"   📋 {pattern_type}: {total_patterns} patterns from {source} ({status})")
            else:
                logger.warning("⚠️ No crisis patterns loaded from ConfigManager, using fallback constants")
                self.crisis_patterns_loaded = False
                
        except Exception as e:
            logger.error(f"❌ Failed to load crisis patterns from ConfigManager: {e}")
            logger.warning("⚠️ Falling back to hardcoded pattern constants")
            self.crisis_patterns_loaded = False
    
    # ========================================================================
    # PHASE 3A: CRISIS PATTERN ACCESS METHODS (NEW)
    # ========================================================================
    
    def get_crisis_patterns(self, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get crisis patterns from ConfigManager JSON (Phase 3a)
        
        Args:
            pattern_type: Specific pattern type or None for all
            
        Returns:
            Crisis patterns dictionary
        """
        if not self.crisis_patterns_loaded:
            logger.debug("🔄 Crisis patterns not loaded from JSON, using fallback constants")
            return self._get_fallback_crisis_patterns(pattern_type)
        
        if pattern_type:
            pattern_data = self.crisis_patterns_cache.get(pattern_type, {})
            if pattern_data:
                # Check if enabled
                enabled = pattern_data.get('configuration', {}).get('enabled', True)
                if enabled:
                    return pattern_data.get('patterns', {})
                else:
                    logger.debug(f"🚫 Pattern type {pattern_type} is disabled")
                    return {}
            else:
                logger.warning(f"⚠️ Pattern type {pattern_type} not found in ConfigManager")
                return self._get_fallback_crisis_patterns(pattern_type)
        
        # Return all enabled patterns
        result = {}
        for ptype, pdata in self.crisis_patterns_cache.items():
            enabled = pdata.get('configuration', {}).get('enabled', True)
            if enabled:
                result[ptype] = pdata.get('patterns', {})
        
        return result
    
    def _get_fallback_crisis_patterns(self, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """Get fallback crisis patterns from hardcoded constants"""
        fallback_patterns = {
            'lgbtqia_patterns': LGBTQIA_PATTERNS,
            'burden_patterns': BURDEN_PATTERNS,
            'hopelessness_patterns': HOPELESSNESS_PATTERNS,
            'struggle_patterns': STRUGGLE_PATTERNS,
            'idiom_patterns': ENHANCED_IDIOM_PATTERNS,
            'positive_context_patterns': POSITIVE_CONTEXT_PATTERNS,
            'context_patterns': CRISIS_CONTEXTS,
            'community_vocabulary': COMMUNITY_VOCABULARY,
            'temporal_patterns': TEMPORAL_INDICATORS,
            'context_weights': CONTEXT_WEIGHTS,
            'negation_patterns': NEGATION_PATTERNS,
            'basic_idiom_patterns': IDIOM_PATTERNS
        }
        
        if pattern_type:
            return fallback_patterns.get(pattern_type, {})
        
        return fallback_patterns
    
    def get_lgbtqia_patterns(self) -> Dict[str, Any]:
        """Get LGBTQIA+ patterns from ConfigManager JSON or fallback"""
        return self.get_crisis_patterns('lgbtqia_patterns')
    
    def get_burden_patterns(self) -> List[str]:
        """Get burden patterns from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('burden_patterns')
        
        # Extract pattern list from JSON structure or use fallback
        if isinstance(patterns, dict) and 'burden_expressions' in patterns:
            # JSON structure
            burden_data = patterns['burden_expressions']
            if isinstance(burden_data, dict) and 'patterns' in burden_data:
                return [p.get('pattern', p) if isinstance(p, dict) else p 
                       for p in burden_data['patterns']]
        
        # Fallback to constant
        return BURDEN_PATTERNS
    
    def get_hopelessness_patterns(self) -> List[str]:
        """Get hopelessness patterns from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('hopelessness_patterns')
        
        # If JSON structure, extract patterns; otherwise use fallback
        if isinstance(patterns, dict):
            # Try to extract from JSON structure
            for key, value in patterns.items():
                if isinstance(value, dict) and 'patterns' in value:
                    return [p.get('pattern', p) if isinstance(p, dict) else p 
                           for p in value['patterns']]
        
        # Fallback to constant
        return HOPELESSNESS_PATTERNS
    
    def get_struggle_patterns(self) -> List[str]:
        """Get struggle patterns from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('struggle_patterns')
        
        # If JSON structure, extract patterns; otherwise use fallback
        if isinstance(patterns, dict):
            # Try to extract from JSON structure
            for key, value in patterns.items():
                if isinstance(value, dict) and 'patterns' in value:
                    return [p.get('pattern', p) if isinstance(p, dict) else p 
                           for p in value['patterns']]
        
        # Fallback to constant
        return STRUGGLE_PATTERNS
    
    def get_enhanced_idiom_patterns(self) -> List[Dict[str, Any]]:
        """Get enhanced idiom patterns from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('idiom_patterns')
        
        # If JSON structure, convert to expected format; otherwise use fallback
        if isinstance(patterns, dict):
            # Try to convert JSON structure to expected format
            result = []
            for pattern_name, pattern_data in patterns.items():
                if isinstance(pattern_data, dict):
                    # Convert JSON format to expected dict format
                    converted_pattern = {
                        'name': pattern_data.get('name', pattern_name),
                        'patterns': [p.get('pattern', p) if isinstance(p, dict) else p 
                                   for p in pattern_data.get('patterns', [])],
                        'reduction_factor': pattern_data.get('reduction_factor', 0.1),
                        'max_score_after': pattern_data.get('max_score_after', 0.1),
                        'required_context': pattern_data.get('context_validation'),
                    }
                    result.append(converted_pattern)
            if result:
                return result
        
        # Fallback to constant
        return ENHANCED_IDIOM_PATTERNS
    
    def get_community_vocabulary(self) -> Dict[str, List[str]]:
        """Get community vocabulary from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('community_vocabulary')
        
        # If JSON structure, extract vocabulary; otherwise use fallback
        if isinstance(patterns, dict) and 'vocabulary' in patterns:
            vocab_data = patterns['vocabulary']
            result = {}
            
            for category, category_data in vocab_data.items():
                if isinstance(category_data, dict) and 'terms' in category_data:
                    # Extract terms from JSON structure
                    result[category] = [
                        term.get('term', term) if isinstance(term, dict) else term
                        for term in category_data['terms']
                    ]
                else:
                    result[category] = category_data
            
            return result
        
        # Fallback to constant
        return COMMUNITY_VOCABULARY
    
    def get_temporal_indicators(self) -> Dict[str, List[str]]:
        """Get temporal indicators from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('temporal_patterns')
        
        # If JSON structure, extract indicators; otherwise use fallback
        if isinstance(patterns, dict):
            return patterns
        
        # Fallback to constant
        return TEMPORAL_INDICATORS
    
    def get_context_weights(self) -> Dict[str, List[str]]:
        """Get context weights from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('context_weights')
        
        # If JSON structure, extract weights; otherwise use fallback
        if isinstance(patterns, dict):
            return patterns
        
        # Fallback to constant
        return CONTEXT_WEIGHTS
    
    def get_negation_patterns(self) -> List[str]:
        """Get negation patterns from ConfigManager JSON or fallback"""
        patterns = self.get_crisis_patterns('negation_patterns')
        
        # If JSON structure, extract patterns; otherwise use fallback
        if isinstance(patterns, dict):
            # Try to extract from JSON structure
            for key, value in patterns.items():
                if isinstance(value, dict) and 'patterns' in value:
                    return [p.get('pattern', p) if isinstance(p, dict) else p 
                           for p in value['patterns']]
                elif isinstance(value, list):
                    return value
        
        # Fallback to constant
        return NEGATION_PATTERNS
    
    def get_crisis_patterns_summary(self) -> Dict[str, Any]:
        """Get summary of crisis patterns loading status"""
        if self.crisis_patterns_loaded:
            return self.config_manager.get_crisis_pattern_summary()
        else:
            return {
                'source': 'fallback_constants',
                'total_pattern_types': 12,
                'note': 'Using hardcoded constants from settings_manager.py'
            }
    
    # ========================================================================
    # EXISTING METHODS (PRESERVED)
    # ========================================================================
    
    def get_setting(self, setting_path: str, default: Any = None) -> Any:
        """
        Get a setting value using dot notation
        
        Args:
            setting_path: Dot-separated path to setting (e.g., 'hardware.device')
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
        try:
            # Check for runtime overrides first
            if setting_path in self.setting_overrides:
                return self.setting_overrides[setting_path]
            
            # Navigate through nested settings
            current = self.runtime_settings
            for part in setting_path.split('.'):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            
            return current
            
        except Exception as e:
            logger.warning(f"⚠️ Error accessing setting {setting_path}: {e}")
            return default
    
    def set_setting_override(self, setting_path: str, value: Any):
        """
        Set a runtime override for a setting
        
        Args:
            setting_path: Dot-separated path to setting
            value: New value to set
        """
        self.setting_overrides[setting_path] = value
        logger.info(f"🔄 Setting override: {setting_path} = {value}")
    
    def clear_setting_override(self, setting_path: str):
        """Clear a runtime setting override"""
        if setting_path in self.setting_overrides:
            del self.setting_overrides[setting_path]
            logger.info(f"🔄 Cleared setting override: {setting_path}")
    
    def get_hardware_settings(self) -> Dict[str, Any]:
        """Get hardware configuration settings"""
        return self.runtime_settings.get('hardware', {})
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance configuration settings"""
        hardware = self.get_hardware_settings()
        return hardware.get('performance_settings', {})
    
    def get_feature_settings(self) -> Dict[str, Any]:
        """Get feature flag settings"""
        return self.runtime_settings.get('features', {})
    
    def get_threshold_settings(self) -> Dict[str, Any]:
        """Get threshold configuration settings"""
        return self.runtime_settings.get('thresholds', {})
    
    def get_device_setting(self) -> str:
        """Get device setting"""
        return self.get_setting('hardware.device', 'auto')
    
    def get_precision_setting(self) -> str:
        """Get model precision setting"""
        return self.get_setting('hardware.precision', 'float16')
    
    def get_cache_dir_setting(self) -> str:
        """Get model cache directory setting"""
        return self.get_setting('hardware.memory_optimization.cache_dir', './models/cache')
    
    def get_learning_enabled_setting(self) -> bool:
        """Get learning system enabled setting"""
        return self.get_setting('features.learning_system.enabled', True)
    
    def get_gap_detection_enabled_setting(self) -> bool:
        """Get gap detection enabled setting"""
        return self.get_setting('features.experimental_features.enable_gap_detection', True)
    
    def get_ensemble_analysis_enabled_setting(self) -> bool:
        """Get ensemble analysis enabled setting"""
        return self.get_setting('features.experimental_features.enable_ensemble_analysis', True)
    
    def reload_settings(self):
        """Reload settings from ConfigManager"""
        logger.info("🔄 Reloading settings from ConfigManager...")
        self._load_initial_settings()
        
        # Phase 3a: Reload crisis patterns
        self._load_crisis_patterns_from_config()
        
        logger.info("✅ Settings reloaded")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings including overrides"""
        result = self.runtime_settings.copy()
        
        # Apply overrides
        for path, value in self.setting_overrides.items():
            # Simple override application (doesn't handle nested paths)
            result[f"override_{path}"] = value
        
        # Phase 3a: Add crisis patterns summary
        result['crisis_patterns'] = self.get_crisis_patterns_summary()
        
        return result
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings"""
        summary = {
            'device': self.get_device_setting(),
            'precision': self.get_precision_setting(),
            'cache_dir': self.get_cache_dir_setting(),
            'learning_enabled': self.get_learning_enabled_setting(),
            'gap_detection_enabled': self.get_gap_detection_enabled_setting(),
            'ensemble_analysis_enabled': self.get_ensemble_analysis_enabled_setting(),
            'active_overrides': len(self.setting_overrides),
            'total_settings_categories': len(self.runtime_settings),
            # Phase 3a: Crisis patterns status
            'crisis_patterns_loaded': self.crisis_patterns_loaded,
            'crisis_patterns_source': 'JSON' if self.crisis_patterns_loaded else 'fallback'
        }
        
        return summary
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate current settings"""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Validate device setting
            device = self.get_device_setting()
            if device not in ['auto', 'cpu', 'cuda']:
                validation_result['warnings'].append(f"Unusual device setting: {device}")
            
            # Validate precision setting
            precision = self.get_precision_setting()
            if precision not in ['float16', 'float32', 'auto']:
                validation_result['warnings'].append(f"Unusual precision setting: {precision}")
            
            # Validate cache directory exists
            cache_dir = self.get_cache_dir_setting()
            if not Path(cache_dir).exists():
                validation_result['warnings'].append(f"Cache directory does not exist: {cache_dir}")
            
            # Phase 3a: Validate crisis patterns
            if self.crisis_patterns_loaded:
                pattern_validation = self.config_manager.validate_crisis_patterns()
                if not pattern_validation['valid']:
                    validation_result['errors'].extend(pattern_validation['errors'])
                    validation_result['valid'] = False
                validation_result['warnings'].extend(pattern_validation['warnings'])
            else:
                validation_result['warnings'].append("Crisis patterns using fallback constants instead of JSON")
            
        except Exception as e:
            validation_result['errors'].append(f"Settings validation error: {e}")
            validation_result['valid'] = False
        
        return validation_result


# Export for clean architecture - PHASE 3A UPDATED
__all__ = [
    'SettingsManager',
    'create_settings_manager',
    # Pattern constants for component compatibility (FALLBACK ONLY - Primary: ConfigManager JSON)
    'SERVER_CONFIG',
    'CRISIS_THRESHOLDS', 
    'DEFAULT_PARAMS',
    'POSITIVE_CONTEXT_PATTERNS',
    'IDIOM_PATTERNS', 
    'LGBTQIA_PATTERNS',
    'CRISIS_CONTEXTS',
    'COMMUNITY_VOCABULARY',
    'TEMPORAL_INDICATORS',
    'CONTEXT_WEIGHTS',
    'ENHANCED_IDIOM_PATTERNS',
    'BURDEN_PATTERNS',
    'HOPELESSNESS_PATTERNS',
    'STRUGGLE_PATTERNS',
    'NEGATION_PATTERNS'
]