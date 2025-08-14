# ash-nlp/managers/unified_config_manager.py
"""
Unified Configuration Manager for Ash NLP Service
FILE VERSION: v3.1-3d-10.9-1
LAST MODIFIED: 2025-08-14
PHASE: 3d Step 10.9 - ENHANCED ENVIRONMENT VARIABLE RESOLUTION
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class VariableSchema:
    """Schema definition for environment variable validation"""
    var_type: str  # 'str', 'int', 'float', 'bool', 'list'
    default: Any
    choices: Optional[List[Any]] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    required: bool = False
    description: str = ""

class UnifiedConfigManager:
    """
    Unified Configuration Manager for Ash-NLP v3.1d with Enhanced Environment Variable Resolution
    
    STEP 10.9 ENHANCEMENT:
    Enhanced substitute_environment_variables method to properly resolve placeholders using:
    1. Environment variables (first priority)
    2. JSON defaults block (second priority) 
    3. Schema defaults (third priority)
    4. Only leave placeholders if no resolution possible
    
    FOLLOWS ESTABLISHED PATTERN WITH ENHANCED DEFAULTS RESOLUTION:
    1. JSON files have main configuration with ${VAR_NAME} placeholders
    2. JSON files have separate "defaults" block with actual default values
    3. Environment variables substitute ${VAR_NAME} placeholders when present
    4. ENHANCED: Remaining placeholders immediately check JSON defaults block
    5. ENHANCED: Still unresolved placeholders fall back to schema defaults
    6. ENHANCED: Type conversion applied consistently across all resolution paths
    
    Example JSON structure:
    {
      "crisis_amplification_patterns": {
        "crisis_amplifier_weight": "${NLP_HOPELESSNESS_CONTEXT_CRISIS_BOOST}",
        "defaults": {
          "crisis_amplifier_weight": 1.2  // Used when env var doesn't exist
        }
      }
    }
    
    This manager consolidates:
    - UnifiedConfigManager: JSON loading with ${VAR} substitution (ENHANCED)
    - EnvConfigManager: Schema validation and type conversion (INTEGRATED)  
    - Direct os.getenv(): Centralized environment access (REPLACED)
    
    Clean v3.1 Architecture:
    - Factory function pattern  
    - Dependency injection support
    - Fail-fast validation
    - JSON placeholders + defaults block pattern (ENHANCED)
    
    v3.1 Pattern File Consolidation Support:
    - Supports consolidated context_patterns.json (crisis + positive + weights)
    - Supports consolidated community_vocabulary_patterns.json
    - Backward compatibility with legacy pattern files
    """
    
    def __init__(self, config_dir: str = "/app/config"):
        """
        Initialize Unified Configuration Manager
        
        Args:
            config_dir: Directory containing JSON configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.env_override_pattern = re.compile(r'\$\{([^}]+)\}')
        
        # Initialize schema definitions for validation
        self.variable_schemas = self._initialize_schemas()
        
        # Configuration file mappings - UPDATED for v3.1 consolidation
        self.config_files = {
            # Core algorithm configuration
            'analysis_parameters': 'analysis_parameters.json',
            'threshold_mapping': 'threshold_mapping.json',
            
            # v3.1 compliant pattern files (consolidated and individual)
            'community_vocabulary_patterns': 'community_vocabulary_patterns.json',  # ✅ Consolidated
            'context_patterns': 'context_patterns.json',                           # ✅ Consolidated (NEW)
            'temporal_indicators_patterns': 'temporal_indicators_patterns.json',   # ✅ v3.1 compliant
            'enhanced_crisis_patterns': 'enhanced_crisis_patterns.json',           # ✅ v3.1 compliant
            'crisis_idiom_patterns': 'crisis_idiom_patterns.json',                 # ✅ v3.1 compliant
            'crisis_burden_patterns': 'crisis_burden_patterns.json',               # ✅ v3.1 compliant
            
            # Core system configuration
            'feature_flags': 'feature_flags.json',
            'label_config': 'label_config.json',
            'learning_parameters': 'learning_parameters.json',
            'learning_settings': 'learning_settings.json',
            'logging_settings': 'logging_settings.json',
            'model_ensemble': 'model_ensemble.json',
            'performance_settings': 'performance_settings.json',
            'server_settings': 'server_settings.json',
            'storage_settings': 'storage_settings.json',
            
            # ELIMINATED FILES - Removed from config_files mapping
            # ❌ 'context_weight_patterns': 'context_weight_patterns.json',        # Merged into context_patterns.json
            # ❌ 'crisis_community_vocabulary': 'crisis_community_vocabulary.json', # Merged into community_vocabulary_patterns.json
            # ❌ 'crisis_context_patterns': 'crisis_context_patterns.json',        # Merged into context_patterns.json
            # ❌ 'crisis_lgbtqia_patterns': 'crisis_lgbtqia_patterns.json',        # Merged into community_vocabulary_patterns.json
            # ❌ 'positive_context_patterns': 'positive_context_patterns.json',    # Merged into context_patterns.json
        }
        
        # Load and validate all environment variables
        self.env_config = self._load_all_environment_variables()
        
        logger.info("UnifiedConfigManager v3.1d Step 10.9 initialized - Enhanced environment variable resolution with JSON defaults integration")
    
    def _initialize_schemas(self) -> Dict[str, VariableSchema]:
        """Initialize comprehensive schema definitions for all 150+ environment variables"""
        schemas = {}
        
        # Models & Thresholds (Critical Priority)
        schemas.update({
            'NLP_MODEL_DEPRESSION_NAME': VariableSchema('str',
                'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
            'NLP_MODEL_SENTIMENT_NAME': VariableSchema('str',
                'Lowerated/lm6-deberta-v3-topic-sentiment'),
            'NLP_MODEL_DISTRESS_NAME': VariableSchema('str',
                'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
            'NLP_MODEL_DEPRESSION_WEIGHT': VariableSchema('float', 0.4,
                min_value=0.0, max_value=1.0),
            'NLP_MODEL_SENTIMENT_WEIGHT': VariableSchema('float', 0.3,
                min_value=0.0, max_value=1.0),
            'NLP_MODEL_DISTRESS_WEIGHT': VariableSchema('float', 0.3,
                min_value=0.0, max_value=1.0),
            'NLP_MODEL_CACHE_DIR': VariableSchema('str',
                './models/cache'),
            'NLP_MODEL_DEVICE': VariableSchema('str', 'auto',
                choices=['auto', 'cpu', 'cuda']),
            'NLP_MODEL_MAX_MEMORY_MB': VariableSchema('int', 8192,
                min_value=1024, max_value=32768),
            'NLP_MODEL_ENSEMBLE_MODE': VariableSchema('str', 'consensus',
                choices=['consensus', 'majority', 'weighted']),
            
            # Analysis Parameters (High Priority)
            'NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH': VariableSchema('float', 0.55,
                min_value=0.0, max_value=1.0, 
                description='High crisis threshold for analysis'),
            'NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM': VariableSchema('float',
                0.28, min_value=0.0, max_value=1.0, 
                description='Medium crisis threshold for analysis'),
            'NLP_ANALYSIS_CRISIS_THRESHOLD_LOW': VariableSchema('float', 0.16,
                min_value=0.0, max_value=1.0, 
                description='Low crisis threshold for analysis'),
            'NLP_ANALYSIS_DEPRESSION_THRESHOLD': VariableSchema('float', 0.6,
                min_value=0.0, max_value=1.0),
            'NLP_ANALYSIS_SENTIMENT_THRESHOLD': VariableSchema('float', 0.5,
                min_value=0.0, max_value=1.0),
            'NLP_ANALYSIS_EMOTIONAL_DISTRESS_THRESHOLD': VariableSchema('float',
                0.6, min_value=0.0, max_value=1.0),
            'NLP_ANALYSIS_MINIMUM_TEXT_LENGTH': VariableSchema('int', 10,
                min_value=1, max_value=1000),
            'NLP_ANALYSIS_MAXIMUM_TEXT_LENGTH': VariableSchema('int', 512,
                min_value=100, max_value=2048),
            
            # Server & Infrastructure (Medium Priority)
            'NLP_SERVER_HOST': VariableSchema('str', '0.0.0.0'),
            'NLP_SERVER_PORT': VariableSchema('int', 8881, min_value=1024,
                max_value=65535),
            'NLP_SERVER_WORKERS': VariableSchema('int', 1, min_value=1,
                max_value=16),
            'NLP_SERVER_TIMEOUT': VariableSchema('int', 60, min_value=10,
                max_value=300),
            'NLP_SERVER_RELOAD': VariableSchema('bool', False),
            
            # Storage & Logging (Medium Priority)
            'NLP_STORAGE_DATA_DIR': VariableSchema('str', './data'),
            'NLP_STORAGE_CACHE_DIR': VariableSchema('str', './cache'),
            'NLP_STORAGE_LOG_DIR': VariableSchema('str', './logs'),
            'NLP_LOGGING_LEVEL': VariableSchema('str', 'INFO',
                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
            'NLP_LOGGING_FORMAT': VariableSchema('str', 'detailed',
                choices=['simple', 'detailed', 'json']),
            
            # Feature Flags (Low Priority)
            'NLP_FEATURE_ENABLE_CRISIS_DETECTION': VariableSchema('bool', True),
            'NLP_FEATURE_ENABLE_PATTERN_MATCHING': VariableSchema('bool', True),
            'NLP_FEATURE_ENABLE_STAFF_REVIEW': VariableSchema('bool', True),
            'NLP_FEATURE_ENABLE_ENHANCED_PATTERNS': VariableSchema('bool',
                False,
                description='Enable enhanced pattern matching features'),
            'NLP_FEATURE_ENSEMBLE_ANALYSIS': VariableSchema('bool', True,
                description='Enable ensemble analysis functionality'),

            # Performance Settings (Low Priority)
            'NLP_PERFORMANCE_BATCH_SIZE': VariableSchema('int', 32,
                min_value=1, max_value=256),
            'NLP_PERFORMANCE_CACHE_SIZE': VariableSchema('int', 1000,
                min_value=100, max_value=10000),
            'NLP_PERFORMANCE_ENABLE_OPTIMIZATION': VariableSchema('bool', True),
            
            # Zero-Shot Label Configuration (NEW - Missing schemas causing warnings)
            'NLP_ZERO_SHOT_LABEL_SET': VariableSchema('str', 'enhanced_crisis', 
                choices=['enhanced_crisis', 'clinical_focused', 'conversational', 'safety_first'],
                description='Zero-shot model label set selection'),
            'NLP_ZERO_SHOT_ENABLE_RUNTIME_SWITCHING': VariableSchema('bool', True, 
                description='Enable runtime switching of label sets'),
            'NLP_ZERO_SHOT_CACHE_LABELS': VariableSchema('bool', True, 
                description='Enable caching of label configurations'),
            'NLP_ZERO_SHOT_VALIDATE_ON_LOAD': VariableSchema('bool', True, 
                description='Validate label configuration on load'),
            'NLP_ZERO_SHOT_FALLBACK_LABEL_SET': VariableSchema('str',
                'enhanced_crisis',
                choices=['enhanced_crisis', 'clinical_focused', 'conversational', 'safety_first'],
                description='Fallback label set if primary fails'),

            # STEP 10.9: Add schema for context pattern variables (from .env.template and JSON configs)
            'NLP_CONFIG_ENHANCED_CRISIS_WEIGHT': VariableSchema('float', 1.2,
                min_value=0.1, max_value=5.0,
                description='Enhanced crisis pattern weight multiplier'),
            'NLP_HOPELESSNESS_CONTEXT_CRISIS_BOOST': VariableSchema('float', 1.2,
                min_value=0.1, max_value=5.0,
                description='Hopelessness context crisis boost factor'),
            'NLP_HOPELESSNESS_CONTEXT_BOOST_FACTOR': VariableSchema('float', 1.2,
                min_value=0.1, max_value=5.0,
                description='Hopelessness context boost factor for pattern analysis'),

            # Preserve GLOBAL_* variables (Ecosystem Compatibility)
            'GLOBAL_LOG_LEVEL': VariableSchema('str', 'INFO',
                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
            'GLOBAL_DEBUG': VariableSchema('bool', False),
            'GLOBAL_ENABLE_LOGGING': VariableSchema('bool', True),
            'GLOBAL_NLP_API_PORT': VariableSchema('int', 8881,
                min_value=1024, max_value=65535),
            'GLOBAL_ENABLE_CORS': VariableSchema('bool', True),
            'GLOBAL_ALLOWED_IPS': VariableSchema('str',
                '10.20.30.0/24,127.0.0.1,::1'),
            'GLOBAL_HUGGINGFACE_TOKEN': VariableSchema('str', ''),
            'GLOBAL_FEATURE_ENABLE_LEARNING_SYSTEM': VariableSchema('bool',
                True),
        })
        
        # Add additional schemas for learning, thresholds, etc.
        schemas.update(self._get_learning_schemas())
        schemas.update(self._get_threshold_schemas())
        schemas.update(self._get_extended_schemas())
        
        logger.info(f"✅ Initialized {len(schemas)} environment variable schemas")
        return schemas
    
    def _get_learning_schemas(self) -> Dict[str, VariableSchema]:
        """Get learning system variable schemas"""
        return {
            'NLP_LEARNING_ENABLE_ADJUSTMENTS': VariableSchema('bool', True),
            'NLP_LEARNING_ADJUSTMENT_RATE': VariableSchema('float', 0.1,
                min_value=0.01, max_value=1.0),
            'NLP_LEARNING_PERSISTENCE_FILE': VariableSchema('str',
                './learning_data/adjustments.json'),
            'NLP_LEARNING_MAXIMUM_ADJUSTMENTS': VariableSchema('int', 100,
                min_value=10, max_value=1000),
            'NLP_ANALYSIS_LEARNING_PERSISTENCE_FILE': VariableSchema('str',
                './learning_data/enhanced_learning_adjustments.json'),
            'NLP_ANALYSIS_LEARNING_RATE': VariableSchema('float', 0.1,
                min_value=0.01, max_value=1.0),
            'NLP_ANALYSIS_LEARNING_ENABLE_ADJUSTMENTS': VariableSchema('bool',
                True),
            'NLP_ANALYSIS_LEARNING_MAXIMUM_ADJUSTMENTS': VariableSchema('int',
                100, min_value=10, max_value=1000),
            'NLP_ANALYSIS_LEARNING_MIN_CONFIDENCE_ADJUSTMENT': VariableSchema('float',
                0.05, min_value=0.01, max_value=0.5),
            'NLP_ANALYSIS_LEARNING_MAX_CONFIDENCE_ADJUSTMENT': VariableSchema('float',
                0.30, min_value=0.1, max_value=1.0),
            'NLP_ANALYSIS_LEARNING_MAX_ADJUSTMENTS_PER_DAY': VariableSchema('int',
                50, min_value=1, max_value=500),

            # NEW - Missing schemas causing warnings
            'NLP_ANALYSIS_LEARNING_FALSE_POSITIVE_FACTOR': VariableSchema('float',
                -0.1, min_value=-1.0, max_value=0.0,
                description='Factor for adjusting false positive learning (negative value reduces sensitivity)'),
            'NLP_ANALYSIS_LEARNING_FALSE_NEGATIVE_FACTOR': VariableSchema('float',
                0.1, min_value=0.0, max_value=1.0,
                description='Factor for adjusting false negative learning (positive value increases sensitivity)'),
        }
    
    def _get_threshold_schemas(self) -> Dict[str, VariableSchema]:
        """Get threshold mapping variable schemas"""
        schemas = {}
        
        # Basic threshold configuration
        schemas.update({
            'NLP_THRESHOLD_ENSEMBLE_MODE': VariableSchema('str', 'consensus',
                choices=['consensus', 'majority', 'weighted']),
            'NLP_THRESHOLD_CRISIS_MAPPING_HIGH': VariableSchema('float', 0.8,
                min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CRISIS_MAPPING_MEDIUM': VariableSchema('float', 0.6,
                min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CRISIS_MAPPING_LOW': VariableSchema('float', 0.4,
                min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_STAFF_REVIEW_REQUIRED': VariableSchema('float', 0.7,
                min_value=0.0, max_value=1.0)
        })
        
        # Mode-specific threshold mappings (Phase 3c)
        # Consensus mode thresholds
        schemas.update({
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH': VariableSchema('float',
                0.50, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM': VariableSchema('float',
                0.30, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CONSENSUS_MILD_CRISIS_TO_LOW': VariableSchema('float',
                0.40, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CONSENSUS_NEGATIVE_TO_LOW': VariableSchema('float',
                0.70, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_CONSENSUS_UNKNOWN_TO_LOW': VariableSchema('float',
                0.50, min_value=0.0, max_value=1.0)
        })
        
        # Majority mode thresholds
        schemas.update({
            'NLP_THRESHOLD_MAJORITY_CRISIS_TO_HIGH': VariableSchema('float',
                0.45, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_MAJORITY_CRISIS_TO_MEDIUM': VariableSchema('float',
                0.28, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_MAJORITY_MILD_CRISIS_TO_LOW': VariableSchema('float',
                0.35, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_MAJORITY_NEGATIVE_TO_LOW': VariableSchema('float',
                0.65, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_MAJORITY_UNKNOWN_TO_LOW': VariableSchema('float',
                0.45, min_value=0.0, max_value=1.0)
        })
        
        # Weighted mode thresholds
        schemas.update({
            'NLP_THRESHOLD_WEIGHTED_CRISIS_TO_HIGH': VariableSchema('float',
                0.55, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_WEIGHTED_CRISIS_TO_MEDIUM': VariableSchema('float',
                0.32, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_WEIGHTED_MILD_CRISIS_TO_LOW': VariableSchema('float',
                0.42, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_WEIGHTED_NEGATIVE_TO_LOW': VariableSchema('float',
                0.72, min_value=0.0, max_value=1.0),
            'NLP_THRESHOLD_WEIGHTED_UNKNOWN_TO_LOW': VariableSchema('float',
                0.52, min_value=0.0, max_value=1.0)
        })
        
        return schemas
    
    def _get_extended_schemas(self) -> Dict[str, VariableSchema]:
        """Get extended variable schemas for complete system coverage"""
        schemas = {}
        
        # Additional model configurations
        schemas.update({
            'NLP_MODEL_PRECISION_MODE': VariableSchema('str', 'balanced',
                choices=['speed', 'balanced', 'accuracy']),
        })
        
        # Extended analysis parameters
        schemas.update({
            'NLP_ANALYSIS_ENABLE_PREPROCESSING': VariableSchema('bool', True),
            'NLP_ANALYSIS_ENABLE_POSTPROCESSING': VariableSchema('bool', True),
            'NLP_ANALYSIS_CONTEXT_WINDOW': VariableSchema('int', 512,
                min_value=64, max_value=2048),
        })
        
        # Extended server configurations  
        schemas.update({
            'NLP_SERVER_ENABLE_CORS': VariableSchema('bool', True),
            'NLP_SERVER_ENABLE_COMPRESSION': VariableSchema('bool', True),
            'NLP_SERVER_MAX_REQUEST_SIZE': VariableSchema('int', 10485760,
                min_value=1048576, max_value=104857600),
        })
        
        # Extended storage configurations
        schemas.update({
            'NLP_STORAGE_ENABLE_COMPRESSION': VariableSchema('bool', False),
            'NLP_STORAGE_BACKUP_DIR': VariableSchema('str', './backups'),
            'NLP_STORAGE_RETENTION_DAYS': VariableSchema('int', 30, min_value=1,
                max_value=365),
            'NLP_STORAGE_MODELS_DIR': VariableSchema('str', './models/cache'),
            'NLP_STORAGE_LOGS_DIR': VariableSchema('str', './logs'),
            'NLP_STORAGE_LOG_FILE': VariableSchema('str', 'nlp_service.log'),
        })
        
        # Ensemble configuration
        schemas.update({
            'NLP_ENSEMBLE_MODE': VariableSchema('str', 'majority',
                choices=['consensus', 'majority', 'weighted']),
            'NLP_ENSEMBLE_GAP_DETECTION_ENABLED': VariableSchema('bool', True),
            'NLP_ENSEMBLE_DISAGREEMENT_THRESHOLD': VariableSchema('int', 2,
                min_value=1, max_value=5),
        })
        
        # Hardware configuration
        schemas.update({
            'NLP_HARDWARE_DEVICE': VariableSchema('str', 'auto',
                choices=['auto', 'cpu', 'cuda']),
            'NLP_HARDWARE_PRECISION': VariableSchema('str', 'float16',
                choices=['float16', 'float32']),
            'NLP_HARDWARE_MAX_BATCH_SIZE': VariableSchema('int', 32,
                min_value=1, max_value=256),
            'NLP_HARDWARE_INFERENCE_THREADS': VariableSchema('int', 16,
                min_value=1, max_value=64),
        })
        
        # Logging configuration
        schemas.update({
            'NLP_LOGGING_ENABLE_DETAILED': VariableSchema('bool', True),
            'NLP_LOGGING_ANALYSIS_STEPS': VariableSchema('bool', False),
            'NLP_LOGGING_THRESHOLD_CHANGES': VariableSchema('bool', True),
            'NLP_LOGGING_MODEL_DISAGREEMENTS': VariableSchema('bool', True),
            'NLP_LOGGING_STAFF_REVIEW_TRIGGERS': VariableSchema('bool', True),
            'NLP_LOGGING_PATTERN_ADJUSTMENTS': VariableSchema('bool', True),
            'NLP_LOGGING_LEARNING_UPDATES': VariableSchema('bool', True),
            'NLP_LOGGING_LABEL_MAPPINGS': VariableSchema('bool', False),
        })
        
        return schemas
    
    # ========================================================================
    # GET HARDWARE CONFIGURATION FIX
    # ========================================================================

    def get_hardware_configuration(self) -> Dict[str, Any]:
        """
        Get hardware configuration for models - MISSING METHOD FOR MODELSMANAGER
        
        Returns:
            Dictionary containing hardware configuration settings
        """
        try:
            return {
                'device': self.get_env('NLP_MODEL_DEVICE', 'auto'),
                'precision': self.get_env('NLP_MODEL_PRECISION', 'float16'),
                'max_batch_size': self.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
                'inference_threads': self.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16),
                'max_memory': self.get_env('NLP_MODEL_MAX_MEMORY', None),
                'offload_folder': self.get_env('NLP_MODEL_OFFLOAD_FOLDER', './models/offload'),
                'cache_directory': self.get_env('NLP_MODEL_CACHE_DIR', './models/cache')
            }
        except Exception as e:
            logger.error(f"❌ Error getting hardware configuration: {e}")
            # Return safe defaults
            return {
                'device': 'auto',
                'precision': 'float16',
                'max_batch_size': 32,
                'inference_threads': 16,
                'max_memory': None,
                'offload_folder': './models/offload',
                'cache_directory': './models/cache'
            }

    def get_model_configuration(self) -> Dict[str, Any]:
        """
        Get model configuration settings - ADDITIONAL METHOD FOR MODELSMANAGER
        
        Returns:
            Dictionary containing model configuration
        """
        try:
            return {
                'depression_model': self.get_env('NLP_MODEL_DEPRESSION_NAME', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                'depression_weight': self.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
                'sentiment_model': self.get_env('NLP_MODEL_SENTIMENT_NAME', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                'sentiment_weight': self.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
                'emotional_distress_model': self.get_env('NLP_MODEL_DISTRESS_NAME', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                'emotional_distress_weight': self.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
                'ensemble_mode': self.get_env('NLP_ENSEMBLE_MODE', 'consensus'),
                'gap_detection_enabled': self.get_env_bool('NLP_ENSEMBLE_GAP_DETECTION_ENABLED', True),
                'disagreement_threshold': self.get_env_int('NLP_ENSEMBLE_DISAGREEMENT_THRESHOLD', 2),
                'cache_directory': self.get_env('NLP_MODEL_CACHE_DIR', './models/cache'),
                'huggingface_token': self.get_env('GLOBAL_HUGGINGFACE_TOKEN', None)
            }
        except Exception as e:
            logger.error(f"❌ Error getting model configuration: {e}")
            # Return safe defaults
            return {
                'depression_model': 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0',
                'depression_weight': 0.4,
                'sentiment_model': 'Lowerated/lm6-deberta-v3-topic-sentiment',
                'sentiment_weight': 0.3,
                'emotional_distress_model': 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli',
                'emotional_distress_weight': 0.3,
                'ensemble_mode': 'consensus',
                'gap_detection_enabled': True,
                'disagreement_threshold': 2,
                'cache_directory': './models/cache',
                'huggingface_token': None
            }

    def get_performance_configuration(self) -> Dict[str, Any]:
        """
        Get performance configuration settings - ADDITIONAL METHOD FOR MODELSMANAGER
        
        Returns:
            Dictionary containing performance settings
        """
        try:
            return {
                'max_concurrent_requests': self.get_env_int('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', 20),
                'request_timeout': self.get_env_int('NLP_PERFORMANCE_REQUEST_TIMEOUT', 40),
                'worker_timeout': self.get_env_int('NLP_PERFORMANCE_WORKER_TIMEOUT', 60),
                'analysis_timeout_ms': self.get_env_int('NLP_PERFORMANCE_ANALYSIS_TIMEOUT_MS', 5000),
                'analysis_cache_ttl': self.get_env_int('NLP_PERFORMANCE_ANALYSIS_CACHE_TTL', 300),
                'enable_optimization': self.get_env_bool('NLP_PERFORMANCE_ENABLE_OPTIMIZATION', True),
                'batch_size': self.get_env_int('NLP_PERFORMANCE_BATCH_SIZE', 32),
                'cache_size': self.get_env_int('NLP_PERFORMANCE_CACHE_SIZE', 1000)
            }
        except Exception as e:
            logger.error(f"❌ Error getting performance configuration: {e}")
            # Return safe defaults
            return {
                'max_concurrent_requests': 20,
                'request_timeout': 40,
                'worker_timeout': 60,
                'analysis_timeout_ms': 5000,
                'analysis_cache_ttl': 300,
                'enable_optimization': True,
                'batch_size': 32,
                'cache_size': 1000
            }

    def get_storage_configuration(self) -> Dict[str, Any]:
        """
        Get storage configuration settings - ADDITIONAL METHOD FOR MODELSMANAGER
        
        Returns:
            Dictionary containing storage settings
        """
        try:
            return {
                'data_directory': self.get_env('NLP_STORAGE_DATA_DIR', './data'),
                'cache_directory': self.get_env('NLP_STORAGE_CACHE_DIR', './cache'),
                'log_directory': self.get_env('NLP_STORAGE_LOG_DIR', './logs'),
                'backup_directory': self.get_env('NLP_STORAGE_BACKUP_DIR', './backups'),
                'models_directory': self.get_env('NLP_STORAGE_MODELS_DIR', './models/cache'),
                'enable_compression': self.get_env_bool('NLP_STORAGE_ENABLE_COMPRESSION', False),
                'retention_days': self.get_env_int('NLP_STORAGE_RETENTION_DAYS', 30),
                'log_file': self.get_env('NLP_STORAGE_LOG_FILE', 'nlp_service.log')
            }
        except Exception as e:
            logger.error(f"❌ Error getting storage configuration: {e}")
            # Return safe defaults
            return {
                'data_directory': './data',
                'cache_directory': './cache',
                'log_directory': './logs',
                'backup_directory': './backups',
                'models_directory': './models/cache',
                'enable_compression': False,
                'retention_days': 30,
                'log_file': 'nlp_service.log'
            }
            
    # ========================================================================
    # UNIFIED ENVIRONMENT VARIABLE ACCESS (FOR MANAGERS WITHOUT JSON CONFIG)
    # ========================================================================
    
    def _load_all_environment_variables(self) -> Dict[str, Any]:
        """Load and validate all environment variables using schemas"""
        env_config = {}
        validation_errors = []
        
        logger.info("🔍 Loading and validating all environment variables...")
        
        for var_name, schema in self.variable_schemas.items():
            try:
                # Get environment value or use default
                env_value = os.getenv(var_name)
                
                if env_value is None:
                    if schema.required:
                        validation_errors.append(f"Required variable {var_name} not found")
                        continue
                    else:
                        env_config[var_name] = schema.default
                        logger.debug(f"✅ {var_name}: Using default '{schema.default}'")
                        continue
                
                # Validate and convert the environment value
                validated_value = self._validate_and_convert(var_name, env_value)
                env_config[var_name] = validated_value
                
                logger.debug(f"✅ {var_name}: '{env_value}' → {validated_value}")
                
            except Exception as e:
                validation_errors.append(f"Validation error for {var_name}: {e}")
                logger.error(f"❌ {var_name}: {e}")
        
        # Fail-fast on validation errors
        if validation_errors:
            error_msg = f"Environment variable validation failed:\n" + "\n".join(validation_errors)
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        logger.info(f"✅ Successfully loaded and validated {len(env_config)} environment variables")
        return env_config
    
    # ========================================================================
    # UNIFIED ENVIRONMENT VARIABLE ACCESS (CRITICAL METHODS)
    # ========================================================================
    
    def get_env(self, var_name: str, default: Any = None) -> Any:
        """
        Get environment variable with schema validation and type conversion
        CRITICAL METHOD - Used by all managers
        """
        # Get raw environment value
        env_value = os.getenv(var_name)
        
        # If no environment value, use schema default or provided default
        if env_value is None:
            if var_name in self.variable_schemas:
                result = self.variable_schemas[var_name].default
                logger.debug(f"🔧 Using schema default for {var_name}: {result}")
                return result
            else:
                logger.debug(f"🔧 Using provided default for {var_name}: {default}")
                return default
        
        # Validate and convert using schema
        if var_name in self.variable_schemas:
            return self._validate_and_convert(var_name, env_value)
        else:
            logger.warning(f"⚠️ No schema found for {var_name}, returning raw value: {env_value}")
            return env_value
    
    def get_env_str(self, var_name: str, default: str = '') -> str:
        """Get environment variable as string"""
        result = self.get_env(var_name, default)
        return str(result) if result is not None else default
    
    def get_env_int(self, var_name: str, default: int = 0) -> int:
        """Get environment variable as integer"""
        result = self.get_env(var_name, default)
        try:
            return int(result) if result is not None else default
        except (ValueError, TypeError):
            logger.warning(f"⚠️ Cannot convert {var_name}={result} to int, using default: {default}")
            return default
    
    def get_env_float(self, var_name: str, default: float = 0.0) -> float:
        """Get environment variable as float"""
        result = self.get_env(var_name, default)
        try:
            return float(result) if result is not None else default
        except (ValueError, TypeError):
            logger.warning(f"⚠️ Cannot convert {var_name}={result} to float, using default: {default}")
            return default
    
    def get_env_bool(self, var_name: str, default: bool = False) -> bool:
        """Get environment variable as boolean"""
        result = self.get_env(var_name, default)
        if isinstance(result, bool):
            return result
        if isinstance(result, str):
            return result.lower() in ('true', '1', 'yes', 'on', 'enabled')
        return bool(result) if result is not None else default
    
    def get_env_list(self, var_name: str, default: List[str] = None) -> List[str]:
        """Get environment variable as list (comma-separated)"""
        if default is None:
            default = []
        result = self.get_env(var_name, ','.join(default) if default else '')
        if isinstance(result, str) and result:
            return [item.strip() for item in result.split(',')]
        return default

    def _validate_and_convert(self, var_name: str, value: str) -> Any:
        """Validate and convert environment variable using schema"""
        schema = self.variable_schemas[var_name]
        
        try:
            # Type conversion
            if schema.var_type == 'bool':
                converted = value.lower() in ('true', '1', 'yes', 'on', 'enabled')
            elif schema.var_type == 'int':
                converted = int(value)
            elif schema.var_type == 'float':
                converted = float(value)
            elif schema.var_type == 'list':
                converted = [item.strip() for item in value.split(',')]
            else:  # str
                converted = value
            
            # Validation
            if schema.choices and converted not in schema.choices:
                logger.error(f"❌ Invalid choice for {var_name}: {converted} not in {schema.choices}")
                return schema.default
                
            if schema.min_value is not None and isinstance(converted, (int, float)):
                if converted < schema.min_value:
                    logger.error(f"❌ Value too low for {var_name}: {converted} < {schema.min_value}")
                    return schema.default
                    
            if schema.max_value is not None and isinstance(converted, (int, float)):
                if converted > schema.max_value:
                    logger.error(f"❌ Value too high for {var_name}: {converted} > {schema.max_value}")
                    return schema.default
            
            logger.debug(f"✅ Validated {var_name}: {converted}")
            return converted
            
        except (ValueError, TypeError) as e:
            logger.error(f"❌ Conversion error for {var_name}: {e}")
            return schema.default
    
    # ========================================================================
    # JSON CONFIGURATION METHODS - STEP 10.9 ENHANCED
    # ========================================================================
    
    def substitute_environment_variables(self, value: Any, defaults_context: Dict[str, Any] = None) -> Any:
        """
        STEP 10.9 ENHANCED: Substitute environment variables with immediate defaults fallback
        
        ENHANCED RESOLUTION ORDER:
        1. Environment variables (os.getenv())
        2. JSON defaults block (when available)
        3. Schema defaults (when available)
        4. Original placeholder (only if no resolution possible)
        
        Args:
            value: Value to process (can be string, dict, list, or primitive)
            defaults_context: Current defaults context for this configuration section
            
        Returns:
            Processed value with placeholders resolved
        """
        if isinstance(value, str):
            def replace_env_var(match):
                env_var = match.group(1)
                logger.debug(f"🔄 Step 10.9: Processing ${{{env_var}}}")
                
                # Step 1: Try environment variable first
                env_value = os.getenv(env_var)
                if env_value is not None:
                    logger.debug(f"   ✅ Environment: ${{{env_var}}} = {env_value}")
                    return self._convert_value_type(env_value)
                
                # Step 2: Try JSON defaults context (new in Step 10.9)
                if defaults_context:
                    defaults_value = self._find_default_value(env_var, defaults_context)
                    if defaults_value is not None:
                        logger.debug(f"   ✅ JSON defaults: ${{{env_var}}} = {defaults_value}")
                        return str(defaults_value)  # Convert to string for substitution
                
                # Step 3: Try schema defaults (existing fallback)
                if env_var in self.variable_schemas:
                    schema_default = self.variable_schemas[env_var].default
                    logger.debug(f"   ✅ Schema default: ${{{env_var}}} = {schema_default}")
                    return str(schema_default)
                
                # Step 4: No resolution possible - warn and keep placeholder
                logger.warning(f"   ⚠️ No resolution found for ${{{env_var}}} - keeping placeholder")
                return match.group(0)  # Return original placeholder
            
            # Apply substitution with enhanced resolution
            result = self.env_override_pattern.sub(replace_env_var, value)
            logger.debug(f"🔄 Step 10.9: '{value}' → '{result}'")
            return result
            
        elif isinstance(value, dict):
            # Process dictionaries recursively, passing defaults context
            # STEP 10.9 FIX: Skip _metadata blocks to avoid processing documentation examples
            result = {}
            current_defaults = defaults_context or value.get('defaults', {})
            
            for k, v in value.items():
                if k.startswith('_'):
                    # Skip metadata blocks (they contain documentation and examples, not real config)
                    logger.debug(f"🔄 Step 10.9: Skipping metadata block: {k}")
                    result[k] = v  # Keep metadata as-is without processing
                elif k == 'defaults':
                    # Keep defaults block as-is for reference
                    result[k] = v
                else:
                    # Get defaults for this key if available
                    key_defaults = current_defaults.get(k, {}) if isinstance(current_defaults, dict) else {}
                    result[k] = self.substitute_environment_variables(v, key_defaults)
            return result
            
        elif isinstance(value, list):
            # Process lists recursively
            return [self.substitute_environment_variables(item, defaults_context) for item in value]
            
        else:
            # Return primitive values as-is
            return value
    
    def _find_default_value(self, env_var: str, defaults_context: Dict[str, Any]) -> Any:
        """
        STEP 10.9 NEW: Find default value for environment variable in JSON defaults context
        
        This method searches through the defaults context to find a matching default value
        for the given environment variable.
        
        Args:
            env_var: Environment variable name (e.g., 'NLP_HOPELESSNESS_CONTEXT_CRISIS_BOOST')
            defaults_context: Current defaults context dictionary
            
        Returns:
            Default value if found, None otherwise
        """
        if not isinstance(defaults_context, dict):
            return None
        
        # Direct key lookup (most common case)
        if env_var in defaults_context:
            logger.debug(f"   🎯 Direct match for {env_var} in defaults")
            return defaults_context[env_var]
        
        # Search through nested structures
        for key, value in defaults_context.items():
            # Skip metadata and other non-data keys
            if key.startswith('_') or key == 'defaults':
                continue
                
            if isinstance(value, dict):
                # Recursive search in nested dictionaries
                found = self._find_default_value(env_var, value)
                if found is not None:
                    logger.debug(f"   🎯 Nested match for {env_var} in defaults.{key}")
                    return found
            
            # Pattern matching for common variable patterns
            # Convert env var name to potential JSON key patterns
            simplified_key = self._env_var_to_json_key(env_var)
            if key == simplified_key:
                logger.debug(f"   🎯 Pattern match for {env_var} → {key}")
                return value
        
        return None
    
    def _env_var_to_json_key(self, env_var: str) -> str:
        """
        STEP 10.9 NEW: Convert environment variable name to potential JSON key
        
        Examples:
        - NLP_HOPELESSNESS_CONTEXT_CRISIS_BOOST → crisis_amplifier_weight
        - NLP_CONFIG_ENHANCED_CRISIS_WEIGHT → enhanced_crisis_weight
        
        Args:
            env_var: Environment variable name
            
        Returns:
            Potential JSON key name
        """
        # Remove common prefixes
        key = env_var.replace('NLP_', '').replace('CONFIG_', '').replace('GLOBAL_', '')
        
        # Convert to lowercase with underscores
        key = key.lower()
        
        # Common pattern mappings
        pattern_mappings = {
            'hopelessness_context_crisis_boost': 'crisis_amplifier_weight',
            'hopelessness_context_boost_factor': 'crisis_amplifier_weight',
            'enhanced_crisis_weight': 'enhanced_crisis_weight',
            'crisis_context_boost_multiplier': 'crisis_amplifier_weight',
            'lgbtqia_weight_multiplier': 'lgbtqia_weight_multiplier',
            'burden_weight_multiplier': 'burden_weight_multiplier'
        }
        
        return pattern_mappings.get(key, key)
    
    def _convert_value_type(self, value: str) -> str:
        """
        STEP 10.9 ENHANCED: Convert string value to appropriate type for substitution
        
        Args:
            value: String value to convert
            
        Returns:
            String representation of converted value
        """
        # Boolean conversion
        if value.lower() in ('true', 'false'):
            result = str(value.lower() == 'true')
            logger.debug(f"   → Boolean conversion: {value} → {result}")
            return result
        
        # Numeric conversion
        if value.replace('.', '').replace('-', '').isdigit():
            try:
                if '.' in value:
                    result = str(float(value))
                    logger.debug(f"   → Float conversion: {value} → {result}")
                    return result
                else:
                    result = str(int(value))
                    logger.debug(f"   → Int conversion: {value} → {result}")
                    return result
            except ValueError:
                logger.debug(f"   → String (conversion failed): {value}")
                return value
        
        # String (no conversion)
        logger.debug(f"   → String (no conversion): {value}")
        return value
    
    def _apply_defaults_fallback(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        STEP 10.9 UPDATED: Legacy defaults fallback - now mostly redundant
        
        This method is kept for backward compatibility but most placeholder resolution
        now happens in substitute_environment_variables() with immediate defaults lookup.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Configuration with any remaining placeholders resolved
        """
        defaults = config.get('defaults', {})
        if not defaults:
            logger.debug("🔍 No defaults block found for legacy fallback")
            return config
        
        logger.debug("🔧 Step 10.9: Running legacy defaults fallback for any remaining placeholders...")
        
        def apply_legacy_defaults_recursive(main_value: Any, defaults_value: Any) -> Any:
            if isinstance(main_value, str) and main_value.startswith('${') and main_value.endswith('}'):
                # This is still an unresolved placeholder - use the default
                logger.debug(f"🔄 Legacy fallback: {main_value} → {defaults_value}")
                return self._apply_type_conversion(defaults_value)
            elif isinstance(main_value, dict) and isinstance(defaults_value, dict):
                # Recursively apply defaults to nested dictionaries
                result = {}
                for key in main_value:
                    if key in defaults_value:
                        result[key] = apply_legacy_defaults_recursive(main_value[key], defaults_value[key])
                    else:
                        result[key] = main_value[key]
                # Add any defaults that aren't in main config
                for key in defaults_value:
                    if key not in result:
                        result[key] = self._apply_type_conversion(defaults_value[key])
                return result
            elif isinstance(main_value, list) and isinstance(defaults_value, list):
                # For lists, prefer main_value if it exists, otherwise use defaults
                return main_value if main_value else defaults_value
            else:
                # Use main value if it's not a placeholder
                return main_value
        
        # Apply legacy defaults to the main configuration sections
        result = {}
        for key, value in config.items():
            if key == 'defaults':
                # Keep the defaults block for reference
                result[key] = value
            elif key in defaults:
                # Apply defaults to this section
                result[key] = apply_legacy_defaults_recursive(value, defaults[key])
            else:
                # No defaults for this section, keep as-is
                result[key] = value
        
        logger.debug("✅ Legacy defaults fallback completed")
        return result
    
    def _apply_type_conversion(self, value: Any) -> Any:
        """
        STEP 10.9 NEW: Apply type conversion to default values
        
        Args:
            value: Value to convert
            
        Returns:
            Type-converted value
        """
        if isinstance(value, str):
            # Try to convert string defaults to appropriate types
            if value.lower() in ('true', 'false'):
                return value.lower() == 'true'
            elif value.replace('.', '').replace('-', '').isdigit():
                try:
                    if '.' in value:
                        return float(value)
                    else:
                        return int(value)
                except ValueError:
                    return value
            else:
                return value
        else:
            # Return non-string values as-is
            return value
    
    def load_config_file(self, config_name: str) -> Dict[str, Any]:
        """
        STEP 10.9 ENHANCED: Load and parse configuration file with enhanced placeholder resolution
        
        Args:
            config_name: Name of configuration to load
            
        Returns:
            Processed configuration dictionary
        """
        if config_name in self.config_cache:
            logger.debug(f"📋 Using cached config for {config_name}")
            return self.config_cache[config_name]
        
        config_file = self.config_files.get(config_name)
        if not config_file:
            logger.error(f"❌ Unknown configuration: {config_name}")
            logger.debug(f"🔍 Available configurations: {list(self.config_files.keys())}")
            return {}
        
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            logger.warning(f"⚠️ Configuration file not found: {config_path}")
            logger.debug(f"🔍 Config directory contents: {list(self.config_dir.glob('*.json')) if self.config_dir.exists() else 'Directory does not exist'}")
            return {}
        
        try:
            logger.debug(f"🔍 Step 10.9: Loading config file: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.debug(f"✅ JSON loaded successfully")
            
            # STEP 10.9 ENHANCED: Single-pass resolution with immediate defaults lookup
            logger.debug("🔄 Step 10.9: Starting enhanced environment variable substitution with immediate defaults resolution...")
            processed_config = self.substitute_environment_variables(raw_config)
            
            # STEP 10.9: Legacy fallback for any remaining placeholders (should be minimal now)
            processed_config = self._apply_defaults_fallback(processed_config)
            
            # Cache the processed configuration
            self.config_cache[config_name] = processed_config
            
            logger.info(f"✅ Step 10.9: Successfully loaded configuration: {config_name} from {config_file}")
            return processed_config
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error in {config_file}: {e}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error loading {config_file}: {e}")
            return {}
    
    # ========================================================================
    # BACKWARD COMPATIBILITY METHODS (PRESERVED FROM PREVIOUS PHASES)
    # ========================================================================
    
    def get_crisis_patterns(self, pattern_type: str) -> Dict[str, Any]:
        """
        Get crisis pattern configuration by type - UPDATED for consolidation support
        
        This method now handles both consolidated and individual pattern files:
        - For consolidated files: Loads the new consolidated JSON structure
        - For individual files: Loads individual pattern files as before
        - For eliminated files: Returns empty dict with info message
        """
        logger.debug(f"🔍 Getting crisis patterns: {pattern_type}")
        
        # Handle requests for eliminated files
        eliminated_files = {
            'crisis_context_patterns': 'context_patterns',
            'positive_context_patterns': 'context_patterns', 
            'context_weights_patterns': 'context_patterns',
            'crisis_lgbtqia_patterns': 'community_vocabulary_patterns',
            'crisis_community_vocabulary': 'community_vocabulary_patterns'
        }
        
        if pattern_type in eliminated_files:
            target_file = eliminated_files[pattern_type]
            logger.info(f"ℹ️ {pattern_type}.json was consolidated into {target_file}.json")
            
            # Load the consolidated file instead
            consolidated_config = self.get_crisis_patterns(target_file)
            if not consolidated_config:
                logger.warning(f"⚠️ Consolidated file {target_file}.json not found")
                return {}
            
            # Extract the relevant section based on pattern type
            if pattern_type == 'crisis_context_patterns':
                return consolidated_config.get('crisis_amplification_patterns', {})
            elif pattern_type == 'positive_context_patterns':
                return consolidated_config.get('positive_reduction_patterns', {})
            elif pattern_type == 'context_weights_patterns':
                # Reconstruct the weights structure from consolidated file
                weights = {}
                crisis_amp = consolidated_config.get('crisis_amplification_patterns', {})
                if 'crisis_amplifier_words' in crisis_amp:
                    weights['crisis_context_words'] = crisis_amp['crisis_amplifier_words']
                positive_red = consolidated_config.get('positive_reduction_patterns', {})
                if 'positive_reducer_words' in positive_red:
                    weights['positive_context_words'] = positive_red['positive_reducer_words']
                return weights
            elif pattern_type in ['crisis_lgbtqia_patterns', 'crisis_community_vocabulary']:
                # Return the full consolidated community vocabulary
                return consolidated_config
        
        try:
            # Check if we have a cached version first
            cache_key = f"crisis_patterns_{pattern_type}"
            if cache_key in self.config_cache:
                logger.debug(f"📋 Using cached config for {pattern_type}")
                return self.config_cache[cache_key]
            
            # Load the specific pattern configuration file (follows established pattern)
            config_file_path = self.config_dir / f"{pattern_type}.json"
            
            if not config_file_path.exists():
                logger.warning(f"⚠️ Crisis pattern file not found: {config_file_path}")
                return {}
            
            logger.debug(f"🔍 Loading config file: {config_file_path}")
            
            with open(config_file_path, 'r', encoding='utf-8') as f:
                raw_config = json.load(f)
            
            logger.debug("✅ JSON loaded successfully")
            
            # STEP 10.9 ENHANCED: Apply enhanced environment variable substitutions
            processed_config = self.substitute_environment_variables(raw_config)
            
            # Apply legacy defaults fallback if present
            processed_config = self._apply_defaults_fallback(processed_config)
            
            # Cache the processed configuration
            self.config_cache[cache_key] = processed_config
            
            logger.debug(f"✅ Loaded crisis patterns: {pattern_type}")
            
            return processed_config
            
        except Exception as e:
            logger.error(f"❌ Failed to load crisis patterns {pattern_type}: {e}")
            return {}
    
    def get_model_configuration(self) -> Dict[str, Any]:
        """Get model ensemble configuration - PRESERVED from Phase 3d"""
        logger.debug("🔍 Getting model configuration...")
        
        config = self.load_config_file('model_ensemble')
        
        if not config:
            logger.warning("⚠️ Model ensemble configuration not found, using environment fallback")
            return self._get_fallback_model_config()
        
        # Extract model definitions from the nested structure
        model_defs = config.get('model_ensemble', {}).get('model_definitions', {})
        ensemble_config = config.get('model_ensemble', {}).get('ensemble_config', {})
        
        # Return in the format expected by ModelEnsembleManager
        result = {
            'models': model_defs,  # ModelEnsembleManager expects 'models' key
            'ensemble_mode': ensemble_config.get('mode', 'consensus'),
            'validation': config.get('model_ensemble', {}).get('validation', {}),
            'performance': config.get('model_ensemble', {}).get('performance', {})
        }
        
        logger.debug(f"✅ Model configuration loaded successfully: {len(model_defs)} models found")
        return result
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Get fallback model configuration using schema defaults and environment overrides"""
        logger.info("🔧 Using schema defaults with environment overrides for model configuration")
        
        return {
            'models': {  # ModelEnsembleManager expects 'models' key
                'depression': {
                    'name': self.get_env_str('NLP_MODEL_DEPRESSION_NAME', 'cardiffnlp/twitter-roberta-base-sentiment'),
                    'weight': self.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
                    'cache_dir': self.get_env_str('NLP_MODEL_CACHE_DIR', './model_cache'),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                },
                'sentiment': {
                    'name': self.get_env_str('NLP_MODEL_SENTIMENT_NAME', 'cardiffnlp/twitter-roberta-base-sentiment-latest'),
                    'weight': self.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
                    'cache_dir': self.get_env_str('NLP_MODEL_CACHE_DIR', './model_cache'),
                    'type': 'sentiment-analysis',
                    'pipeline_task': 'zero-shot-classification'
                },
                'emotional_distress': {
                    'name': self.get_env_str('NLP_MODEL_EMOTIONAL_DISTRESS_NAME', 'j-hartmann/emotion-english-distilroberta-base'),
                    'weight': self.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
                    'cache_dir': self.get_env_str('NLP_MODEL_CACHE_DIR', './model_cache'),
                    'type': 'natural-language-inference',
                    'pipeline_task': 'zero-shot-classification'
                }
            },
            'ensemble_mode': self.get_env_str('NLP_MODEL_ENSEMBLE_MODE', 'consensus'),
            'validation': {
                'ensure_weights_sum_to_one': True,
                'fail_on_invalid_weights': True
            },
            'performance': {
                'device': self.get_env_str('NLP_MODEL_DEVICE', 'auto'),
                'max_memory_mb': self.get_env_int('NLP_MODEL_MAX_MEMORY_MB', 8192)
            }
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get status of UnifiedConfigManager with consolidation info
        
        Returns:
            Dictionary containing manager status and operational info
        """
        return {
            'status': 'operational',
            'version': 'v3.1d_step_10.9',
            'enhancement': 'Enhanced Environment Variable Resolution',
            'config_files': len(self.config_files),
            'variables_managed': len([k for k in os.environ.keys() if k.startswith('NLP_') or k.startswith('GLOBAL_')]),
            'cache_size': len(self.config_cache),
            'config_directory': str(self.config_dir),
            'architecture': 'Clean v3.1 with Enhanced Configuration Resolution',
            'consolidation_status': {
                'context_patterns_consolidated': 'context_patterns' in self.config_files,
                'community_patterns_consolidated': 'community_vocabulary_patterns' in self.config_files,
                'eliminated_files': [
                    'crisis_context_patterns', 'positive_context_patterns', 'context_weights_patterns',
                    'crisis_lgbtqia_patterns', 'crisis_community_vocabulary'
                ],
                'consolidated_files': ['context_patterns', 'community_vocabulary_patterns']
            },
            'step_10_9_enhancements': {
                'immediate_defaults_resolution': True,
                'enhanced_placeholder_processing': True,
                'json_defaults_integration': True,
                'schema_fallback_support': True,
                'type_conversion_consistency': True
            }
        }

# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_unified_config_manager(config_dir: str = "/app/config") -> UnifiedConfigManager:
    """
    Factory function to create UnifiedConfigManager instance
    
    Args:
        config_dir: Directory containing JSON configuration files
        
    Returns:
        UnifiedConfigManager instance with Step 10.9 enhancements
    """
    return UnifiedConfigManager(config_dir)

__all__ = ['UnifiedConfigManager', 'create_unified_config_manager']

logger.info("✅ UnifiedConfigManager v3.1d Step 10.9 loaded - Enhanced environment variable resolution with immediate JSON defaults integration")