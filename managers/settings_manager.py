# ash/ash-nlp/managers/settings_manager.py
"""
Settings Manager for Ash NLP Service v3.1 - Phase 3a Complete
Handles runtime settings and configuration overrides

Phase 3a: Crisis patterns migrated to CrisisPatternManager and JSON configuration
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# CORE CONFIGURATION CONSTANTS (Not migrated - still needed)
# ============================================================================

# Server configuration - Core system info, not migrated
SERVER_CONFIG = {
    "version": "4.1",
    "architecture": "modular_v3.1_phase_3a_complete",
    "hardware_info": {
        "cpu": "Ryzen 7 7700x",
        "gpu": "RTX 3060 (12GB VRAM)",
        "ram": "64GB",
        "inference_device": "GPU",
        "models_loaded": 3
    },
    "capabilities": {
        "crisis_analysis": "Enhanced ensemble + pattern analysis",
        "phrase_extraction": "Extract crisis keywords using model scoring",
        "pattern_learning": "Learn distinctive crisis patterns from community messages", 
        "semantic_analysis": "Enhanced crisis detection with community context",
        "community_awareness": "LGBTQIA+ specific pattern recognition via CrisisPatternManager",
        "json_configuration": "Crisis patterns managed via JSON configuration files"
    }
}

# Crisis level mapping thresholds - Core algorithm config, not migrated
CRISIS_THRESHOLDS = {
    "high": 0.55,    # Reduced from 0.50 - matches new systematic approach
    "medium": 0.28,  # Reduced from 0.22 - more selective for medium alerts
    "low": 0.16      # Reduced from 0.12 - avoids very mild expressions
}

# Default parameters for analysis - Core algorithm config, not migrated
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

# ============================================================================
# SETTINGS MANAGER CLASS - v3.1 Clean Architecture
# ============================================================================

class SettingsManager:
    """
    Manages runtime settings and configuration overrides
    Phase 3a: Crisis patterns now managed by CrisisPatternManager
    """
    
    def __init__(self, config_manager):
        """Initialize SettingsManager with ConfigManager dependency injection"""
        self.config_manager = config_manager
        self.setting_overrides = {}
        self.runtime_settings = {}
        
        # Load runtime settings
        self._load_runtime_settings()
        
        logger.info("SettingsManager v3.1 initialized (Phase 3a - Crisis patterns externalized)")
    
    def _load_runtime_settings(self):
        """Load runtime settings from environment variables and config"""
        try:
            # Load basic runtime settings
            self.runtime_settings = {
                'server': SERVER_CONFIG,
                'crisis_thresholds': CRISIS_THRESHOLDS,
                'default_params': DEFAULT_PARAMS,
                'phase_status': {
                    'phase_2a': 'complete',
                    'phase_2b': 'complete', 
                    'phase_2c': 'complete',
                    'phase_3a': 'complete',
                    'crisis_patterns': 'externalized_to_json'
                }
            }
            
            # Load environment overrides
            self._load_environment_overrides()
            
        except Exception as e:
            logger.error(f"Error loading runtime settings: {e}")
    
    def _load_environment_overrides(self):
        """Load setting overrides from environment variables"""
        try:
            # Load threshold overrides
            if os.getenv('NLP_CRISIS_THRESHOLD_HIGH'):
                self.setting_overrides['crisis_threshold_high'] = float(os.getenv('NLP_CRISIS_THRESHOLD_HIGH'))
            if os.getenv('NLP_CRISIS_THRESHOLD_MEDIUM'):
                self.setting_overrides['crisis_threshold_medium'] = float(os.getenv('NLP_CRISIS_THRESHOLD_MEDIUM'))
            if os.getenv('NLP_CRISIS_THRESHOLD_LOW'):
                self.setting_overrides['crisis_threshold_low'] = float(os.getenv('NLP_CRISIS_THRESHOLD_LOW'))
            
            # Load analysis parameter overrides
            if os.getenv('NLP_MIN_PHRASE_LENGTH'):
                self.setting_overrides['min_phrase_length'] = int(os.getenv('NLP_MIN_PHRASE_LENGTH'))
            if os.getenv('NLP_MAX_PHRASE_LENGTH'):
                self.setting_overrides['max_phrase_length'] = int(os.getenv('NLP_MAX_PHRASE_LENGTH'))
            
        except Exception as e:
            logger.error(f"Error loading environment overrides: {e}")
    
    # ========================================================================
    # DEVICE AND PERFORMANCE SETTINGS
    # ========================================================================
    
    def get_device_setting(self) -> str:
        """Get device setting (cpu/cuda/auto)"""
        return os.getenv('NLP_DEVICE', 'auto')
    
    def get_precision_setting(self) -> str:
        """Get precision setting (float16/float32/auto)"""
        return os.getenv('NLP_PRECISION', 'auto')
    
    def get_cache_dir_setting(self) -> str:
        """Get model cache directory setting"""
        return os.getenv('NLP_CACHE_DIR', '/app/models/cache')
    
    def get_max_memory_setting(self) -> Optional[str]:
        """Get maximum memory setting"""
        return os.getenv('NLP_MAX_MEMORY')
    
    def get_offload_folder_setting(self) -> Optional[str]:
        """Get model offload folder setting"""
        return os.getenv('NLP_OFFLOAD_FOLDER')
    
    # ========================================================================
    # ANALYSIS SETTINGS
    # ========================================================================
    
    def get_ensemble_analysis_enabled_setting(self) -> bool:
        """Get ensemble analysis enabled setting"""
        return os.getenv('NLP_ENSEMBLE_ANALYSIS_ENABLED', 'true').lower() == 'true'
    
    def get_crisis_threshold_settings(self) -> Dict[str, float]:
        """Get crisis threshold settings with environment overrides"""
        thresholds = CRISIS_THRESHOLDS.copy()
        
        # Apply environment overrides
        if 'crisis_threshold_high' in self.setting_overrides:
            thresholds['high'] = self.setting_overrides['crisis_threshold_high']
        if 'crisis_threshold_medium' in self.setting_overrides:
            thresholds['medium'] = self.setting_overrides['crisis_threshold_medium']
        if 'crisis_threshold_low' in self.setting_overrides:
            thresholds['low'] = self.setting_overrides['crisis_threshold_low']
        
        return thresholds
    
    def get_phrase_extraction_settings(self) -> Dict[str, Any]:
        """Get phrase extraction settings with environment overrides"""
        settings = DEFAULT_PARAMS['phrase_extraction'].copy()
        
        # Apply environment overrides
        if 'min_phrase_length' in self.setting_overrides:
            settings['min_phrase_length'] = self.setting_overrides['min_phrase_length']
        if 'max_phrase_length' in self.setting_overrides:
            settings['max_phrase_length'] = self.setting_overrides['max_phrase_length']
        
        return settings
    
    def get_pattern_learning_settings(self) -> Dict[str, Any]:
        """Get pattern learning settings"""
        return DEFAULT_PARAMS['pattern_learning'].copy()
    
    def get_semantic_analysis_settings(self) -> Dict[str, Any]:
        """Get semantic analysis settings"""
        return DEFAULT_PARAMS['semantic_analysis'].copy()
    
    # ========================================================================
    # MIGRATION NOTIFICATION METHODS (Phase 3a)
    # ========================================================================
    
    def get_crisis_patterns_migration_notice(self) -> Dict[str, str]:
        """
        Get migration notice for crisis patterns (Phase 3a)
        
        Returns:
            Dictionary with migration information
        """
        return {
            'status': 'migrated_to_json_configuration',
            'phase': '3a_complete',
            'new_location': 'CrisisPatternManager with JSON configuration files',
            'config_directory': '/app/config/',
            'manager_class': 'CrisisPatternManager',
            'access_method': 'Use create_crisis_pattern_manager(config_manager)',
            'migration_date': '2025-08-04',
            'note': 'Crisis patterns are no longer available from SettingsManager. Use CrisisPatternManager for pattern access.'
        }
    
    # Legacy method stubs for backward compatibility warnings
    def get_lgbtqia_patterns(self):
        """DEPRECATED: Crisis patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_lgbtqia_patterns() is deprecated. Use CrisisPatternManager.get_lgbtqia_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_crisis_contexts(self):
        """DEPRECATED: Crisis contexts migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_crisis_contexts() is deprecated. Use CrisisPatternManager.get_crisis_context_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    def get_positive_context_patterns(self):
        """DEPRECATED: Positive context patterns migrated to CrisisPatternManager in Phase 3a"""
        logger.warning("get_positive_context_patterns() is deprecated. Use CrisisPatternManager.get_positive_context_patterns() instead.")
        return self.get_crisis_patterns_migration_notice()
    
    # ========================================================================
    # STATUS AND VALIDATION METHODS
    # ========================================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get SettingsManager status"""
        return {
            'manager': 'SettingsManager',
            'version': '3.1.0',
            'architecture': 'v3.1_clean_phase_3a_complete',
            'config_manager_available': self.config_manager is not None,
            'crisis_patterns_status': 'migrated_to_crisis_pattern_manager',
            'ensemble_analysis_enabled': self.get_ensemble_analysis_enabled_setting(),
            'active_overrides': len(self.setting_overrides),
            'total_settings_categories': len(self.runtime_settings),
            'phase_3a_status': 'complete'
        }
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate current settings"""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'phase_3a_status': 'complete'
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
            
            # Validate crisis thresholds
            thresholds = self.get_crisis_threshold_settings()
            if thresholds['high'] <= thresholds['medium'] or thresholds['medium'] <= thresholds['low']:
                validation_result['errors'].append("Crisis thresholds must be: high > medium > low")
                validation_result['valid'] = False
            
        except Exception as e:
            validation_result['errors'].append(f"Settings validation error: {e}")
            validation_result['valid'] = False
        
        return validation_result


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_settings_manager(config_manager) -> SettingsManager:
    """
    Factory function to create SettingsManager instance
    
    Args:
        config_manager: ConfigManager instance for dependency injection
        
    Returns:
        SettingsManager instance
    """
    return SettingsManager(config_manager)


# ============================================================================
# CLEAN ARCHITECTURE EXPORTS (Phase 3a Complete)
# ============================================================================

__all__ = [
    'SettingsManager',
    'create_settings_manager',
    # Core constants (not migrated - still needed for algorithm configuration)
    'SERVER_CONFIG',
    'CRISIS_THRESHOLDS', 
    'DEFAULT_PARAMS'
    # NOTE: Crisis pattern constants removed in Phase 3a - now available via CrisisPatternManager
    # To access crisis patterns, use: create_crisis_pattern_manager(config_manager)
]

# ============================================================================
# PHASE 3A MIGRATION COMPLETE
# ============================================================================

logger.info("✅ SettingsManager v3.1 - Phase 3a Migration Complete")
logger.info("🔄 Crisis patterns migrated to CrisisPatternManager with JSON configuration")
logger.debug("📋 Remaining constants: SERVER_CONFIG, CRISIS_THRESHOLDS, DEFAULT_PARAMS")
logger.debug("🎯 For crisis patterns, use CrisisPatternManager instead of SettingsManager")