#!/usr/bin/env python3
"""
Environment Configuration Manager for ash-nlp
UPDATED: Centralized threshold management with comprehensive validation
"""

import os
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class EnvConfigManager:
    """Centralized environment variable management with threshold validation"""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize configuration manager"""
        self.env_file = env_file
        self.config = {}
        self.load_environment()
        self.validate_config()
        self.create_directories()
    
    def load_environment(self):
        """Load environment variables from .env file and system"""
        # Load from .env file if it exists (development mode)
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            logger.info(f"✅ Loaded environment from {self.env_file}")
        else:
            # Check if we're in Docker (environment variables should be present)
            if os.getenv('NLP_DEPRESSION_MODEL'):
                logger.info(f"🐳 Running in Docker mode - using system environment variables")
            else:
                logger.warning(f"⚠️ No {self.env_file} file found and no environment variables detected")

        # Define configuration with defaults and types
        config_schema = {
            # =================================================================
            # HUGGING FACE CONFIGURATION
            # =================================================================
            'GLOBAL_HUGGINGFACE_TOKEN': {'type': str, 'default': None, 'required': False},
            'NLP_HUGGINGFACE_CACHE_DIR': {'type': str, 'default': './models/cache'},
            
            # =================================================================
            # LEARNING SYSTEM CONFIGURATION
            # =================================================================
            'GLOBAL_ENABLE_LEARNING_SYSTEM': {'type': bool, 'default': True},
            'NLP_LEARNING_RATE': {'type': float, 'default': 0.1, 'min': 0.01, 'max': 1.0},
            'NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY': {'type': int, 'default': 50, 'min': 1},
            'NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE': {'type': str, 'default': './learning_data/adjustments.json'},
            'NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE_ADJUSTMENT': {'type': float, 'default': 0.05, 'min': 0.01, 'max': 0.5},
            'NLP_THRESHOLD_LEARNING_MAX_CONFIDENCE_ADJUSTMENT': {'type': float, 'default': 0.30, 'min': 0.05, 'max': 1.0},
            
            # =================================================================
            # THREE-MODEL CONFIGURATION
            # =================================================================
            'NLP_DEPRESSION_MODEL': {'type': str, 'default': 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'},
            'NLP_SENTIMENT_MODEL': {'type': str, 'default': 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'},
            'NLP_EMOTIONAL_DISTRESS_MODEL': {'type': str, 'default': 'Lowerated/lm6-deberta-v3-topic-sentiment'},
            'NLP_MODEL_CACHE_DIR': {'type': str, 'default': './models/cache'},
            
            # =================================================================
            # ENSEMBLE CONFIGURATION
            # =================================================================
            'NLP_ENSEMBLE_MODE': {'type': str, 'default': 'weighted', 'choices': ['consensus', 'majority', 'weighted']},
            'NLP_GAP_DETECTION_THRESHOLD': {'type': float, 'default': 0.25, 'min': 0.1, 'max': 1.0},
            'NLP_DISAGREEMENT_THRESHOLD': {'type': float, 'default': 0.35, 'min': 0.1, 'max': 1.0},
            'NLP_AUTO_FLAG_DISAGREEMENTS': {'type': bool, 'default': True},
            
            # Model confidence weighting (for weighted ensemble mode)
            'NLP_DEPRESSION_MODEL_WEIGHT': {'type': float, 'default': 0.6, 'min': 0.0, 'max': 1.0},
            'NLP_SENTIMENT_MODEL_WEIGHT': {'type': float, 'default': 0.15, 'min': 0.0, 'max': 1.0},
            'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': {'type': float, 'default': 0.25, 'min': 0.0, 'max': 1.0},
            
            # =================================================================
            # CENTRALIZED CONSENSUS PREDICTION MAPPING THRESHOLDS
            # =================================================================
            # CRISIS prediction thresholds (PRIMARY - used by ensemble_endpoints.py)
            'NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD': {'type': float, 'default': 0.50, 'min': 0.1, 'max': 1.0},
            'NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD': {'type': float, 'default': 0.30, 'min': 0.1, 'max': 1.0},
            
            # MILD_CRISIS prediction thresholds
            'NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD': {'type': float, 'default': 0.40, 'min': 0.1, 'max': 1.0},
            
            # NEGATIVE sentiment thresholds
            'NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD': {'type': float, 'default': 0.70, 'min': 0.1, 'max': 1.0},
            
            # UNKNOWN prediction fallback
            'NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD': {'type': float, 'default': 0.50, 'min': 0.1, 'max': 1.0},
            
            # =================================================================
            # STAFF REVIEW THRESHOLDS
            # =================================================================
            'NLP_STAFF_REVIEW_HIGH_ALWAYS': {'type': bool, 'default': True},
            'NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD': {'type': float, 'default': 0.45, 'min': 0.1, 'max': 1.0},
            'NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD': {'type': float, 'default': 0.75, 'min': 0.1, 'max': 1.0},
            'NLP_STAFF_REVIEW_ON_MODEL_DISAGREEMENT': {'type': bool, 'default': True},
            
            # =================================================================
            # SAFETY AND BIAS CONTROLS
            # =================================================================
            'NLP_CONSENSUS_SAFETY_BIAS': {'type': float, 'default': 0.03, 'min': 0.0, 'max': 0.1},
            'NLP_ENABLE_SAFETY_OVERRIDE': {'type': bool, 'default': True},
            
            # =================================================================
            # LEGACY ENSEMBLE THRESHOLDS (for backward compatibility)
            # =================================================================
            'NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.45, 'min': 0.1, 'max': 1.0},
            'NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.25, 'min': 0.1, 'max': 1.0},
            'NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.12, 'min': 0.1, 'max': 1.0},
            
            # =================================================================
            # INDIVIDUAL MODEL THRESHOLDS (for backward compatibility)
            # =================================================================
            'NLP_HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.45, 'min': 0.1, 'max': 1.0},
            'NLP_MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.25, 'min': 0.1, 'max': 1.0},
            'NLP_LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.15, 'min': 0.1, 'max': 1.0},
            
            # =================================================================
            # HARDWARE CONFIGURATION
            # =================================================================
            'NLP_DEVICE': {'type': str, 'default': 'auto', 'choices': ['auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1']},
            'NLP_MODEL_PRECISION': {'type': str, 'default': 'float16', 'choices': ['float32', 'float16', 'bfloat16']},
            
            # =================================================================
            # PERFORMANCE TUNING
            # =================================================================
            'NLP_MAX_BATCH_SIZE': {'type': int, 'default': 32, 'min': 1, 'max': 128},
            'NLP_INFERENCE_THREADS': {'type': int, 'default': 16, 'min': 1, 'max': 32},
            'NLP_MAX_CONCURRENT_REQUESTS': {'type': int, 'default': 20, 'min': 1, 'max': 100},
            'NLP_REQUEST_TIMEOUT': {'type': int, 'default': 40, 'min': 5, 'max': 300},
            
            # =================================================================
            # SERVER CONFIGURATION
            # =================================================================
            'NLP_SERVICE_HOST': {'type': str, 'default': '0.0.0.0'},
            'NLP_SERVICE_PORT': {'type': int, 'default': 8881, 'min': 1024, 'max': 65535},
            'NLP_UVICORN_WORKERS': {'type': int, 'default': 1, 'min': 1, 'max': 8},
            'NLP_RELOAD_ON_CHANGES': {'type': bool, 'default': False},
            
            # =================================================================
            # LOGGING CONFIGURATION
            # =================================================================
            'GLOBAL_LOG_LEVEL': {'type': str, 'default': 'INFO', 'choices': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']},
            'NLP_LOG_FILE': {'type': str, 'default': 'nlp_service.log'},
            'NLP_FLIP_SENTIMENT_LOGIC': {'type': bool, 'default': False},
            
            # =================================================================
            # STORAGE PATHS
            # =================================================================
            'NLP_DATA_DIR': {'type': str, 'default': './data'},
            'NLP_MODELS_DIR': {'type': str, 'default': './models/cache'},
            'NLP_LOGS_DIR': {'type': str, 'default': './logs'},
            'NLP_LEARNING_DATA_DIR': {'type': str, 'default': './learning_data'},
            
            # =================================================================
            # RATE LIMITING
            # =================================================================
            'NLP_MAX_REQUESTS_PER_MINUTE': {'type': int, 'default': 120, 'min': 1},
            'NLP_MAX_REQUESTS_PER_HOUR': {'type': int, 'default': 2000, 'min': 1},
            
            # =================================================================
            # SECURITY
            # =================================================================
            'GLOBAL_ALLOWED_IPS': {'type': str, 'default': '10.20.30.0/24,127.0.0.1,::1'},
            'GLOBAL_ENABLE_CORS': {'type': bool, 'default': True},
            
            # =================================================================
            # EXPERIMENTAL FEATURES
            # =================================================================
            'NLP_ENABLE_ENSEMBLE_ANALYSIS': {'type': bool, 'default': True},
            'NLP_ENABLE_GAP_DETECTION': {'type': bool, 'default': True},
            'NLP_ENABLE_CONFIDENCE_SPREADING': {'type': bool, 'default': True},
            'NLP_LOG_MODEL_DISAGREEMENTS': {'type': bool, 'default': True},
        }
        
        # Process each configuration item
        for key, schema in config_schema.items():
            raw_value = os.getenv(key, schema['default'])
            self.config[key] = self._parse_value(key, raw_value, schema)
    
    def _parse_value(self, key: str, raw_value: Any, schema: Dict) -> Any:
        """Parse and validate a configuration value"""
        if raw_value is None:
            if schema.get('required', False):
                raise ValueError(f"Required environment variable {key} is not set")
            return schema['default']
        
        try:
            # Type conversion
            if schema['type'] == bool:
                if isinstance(raw_value, str):
                    return raw_value.lower() in ('true', '1', 'yes', 'on')
                return bool(raw_value)
            elif schema['type'] == int:
                value = int(raw_value)
            elif schema['type'] == float:
                value = float(raw_value)
            else:
                value = str(raw_value)
            
            # Validation
            if 'choices' in schema and value not in schema['choices']:
                raise ValueError(f"{key} must be one of {schema['choices']}, got {value}")
            
            if 'min' in schema and value < schema['min']:
                raise ValueError(f"{key} must be >= {schema['min']}, got {value}")
            
            if 'max' in schema and value > schema['max']:
                raise ValueError(f"{key} must be <= {schema['max']}, got {value}")
            
            return value
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid value for {key}: {raw_value} - {e}")
    
    def validate_config(self):
        """Validate configuration consistency for centralized thresholds"""
        
        # Validate consensus prediction mapping thresholds are properly ordered
        crisis_high = self.config['NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD']
        crisis_medium = self.config['NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD']
        
        if crisis_high <= crisis_medium:
            raise ValueError(
                f"NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD ({crisis_high}) must be > "
                f"NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD ({crisis_medium})"
            )
        
        # Validate staff review thresholds are reasonable
        medium_review = self.config['NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD']
        low_review = self.config['NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD']
        
        if medium_review >= low_review:
            logger.warning(
                f"Staff review thresholds: MEDIUM ({medium_review}) should typically be < LOW ({low_review})"
            )
        
        # Validate model weights sum to 1.0 (for weighted ensemble mode)
        if self.config['NLP_ENSEMBLE_MODE'] == 'weighted':
            total_weight = (
                self.config['NLP_DEPRESSION_MODEL_WEIGHT'] + 
                self.config['NLP_SENTIMENT_MODEL_WEIGHT'] + 
                self.config['NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT']
            )
            
            if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
                raise ValueError(f"Model weights must sum to 1.0, got {total_weight}")
        
        # Validate gap detection thresholds make sense
        gap_threshold = self.config['NLP_GAP_DETECTION_THRESHOLD']
        disagreement_threshold = self.config['NLP_DISAGREEMENT_THRESHOLD']
        
        if gap_threshold >= disagreement_threshold:
            raise ValueError(
                f"NLP_GAP_DETECTION_THRESHOLD ({gap_threshold}) should be < "
                f"NLP_DISAGREEMENT_THRESHOLD ({disagreement_threshold})"
            )
        
        # Validate safety bias is reasonable
        safety_bias = self.config['NLP_CONSENSUS_SAFETY_BIAS']
        if safety_bias > 0.1:
            logger.warning(f"NLP_CONSENSUS_SAFETY_BIAS ({safety_bias}) is quite high, consider <0.1")
        
        logger.info("✅ Centralized threshold configuration validation passed")
        self._log_threshold_summary()
    
    def _log_threshold_summary(self):
        """Log a summary of the centralized threshold configuration"""
        logger.debug("🎯 Centralized Threshold Configuration:")
        logger.debug(f"   Ensemble mode: {self.config['NLP_ENSEMBLE_MODE']}")
        
        # Consensus mapping thresholds (PRIMARY)
        logger.debug("   Consensus Mapping Thresholds:")
        logger.debug(f"     CRISIS → HIGH: {self.config['NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD']}")
        logger.debug(f"     CRISIS → MEDIUM: {self.config['NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD']}")
        logger.debug(f"     MILD_CRISIS → LOW: {self.config['NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD']}")
        logger.debug(f"     NEGATIVE → LOW: {self.config['NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD']}")
        
        # Model weights
        logger.debug("   Model Weights:")
        logger.debug(f"     Depression: {self.config['NLP_DEPRESSION_MODEL_WEIGHT']}")
        logger.debug(f"     Sentiment: {self.config['NLP_SENTIMENT_MODEL_WEIGHT']}")
        logger.debug(f"     Emotional Distress: {self.config['NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT']}")
        
        # Staff review thresholds
        logger.debug("   Staff Review Thresholds:")
        logger.debug(f"     MEDIUM confidence: {self.config['NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD']}")
        logger.debug(f"     LOW confidence: {self.config['NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD']}")
        
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.config['NLP_DATA_DIR'],
            self.config['NLP_MODELS_DIR'],
            self.config['NLP_LOGS_DIR'],
            self.config['NLP_LEARNING_DATA_DIR'],
            os.path.dirname(self.config['NLP_MODEL_CACHE_DIR']),
            os.path.dirname(self.config['NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE']),
        ]
        
        for directory in directories:
            if directory and directory != '.':
                Path(directory).mkdir(parents=True, exist_ok=True)
                logger.debug(f"Ensured directory exists: {directory}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()
    
    def get_consensus_thresholds(self) -> Dict[str, float]:
        """Get consensus prediction mapping thresholds (PRIMARY thresholds)"""
        return {
            'crisis_to_high': self.config['NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD'],
            'crisis_to_medium': self.config['NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD'],
            'mild_crisis_to_low': self.config['NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD'],
            'negative_to_low': self.config['NLP_CONSENSUS_NEGATIVE_TO_LOW_THRESHOLD'],
            'unknown_to_low': self.config['NLP_CONSENSUS_UNKNOWN_TO_LOW_THRESHOLD'],
        }
    
    def get_staff_review_thresholds(self) -> Dict[str, Union[bool, float]]:
        """Get staff review thresholds"""
        return {
            'high_always': self.config['NLP_STAFF_REVIEW_HIGH_ALWAYS'],
            'medium_confidence': self.config['NLP_STAFF_REVIEW_MEDIUM_CONFIDENCE_THRESHOLD'],
            'low_confidence': self.config['NLP_STAFF_REVIEW_LOW_CONFIDENCE_THRESHOLD'],
            'on_disagreement': self.config['NLP_STAFF_REVIEW_ON_MODEL_DISAGREEMENT'],
        }
    
    def print_config(self):
        """Print configuration for debugging (hiding sensitive values)"""
        sensitive_keys = ['GLOBAL_HUGGINGFACE_TOKEN']
        
        logger.info("=== Centralized NLP Service Configuration ===")
        for key, value in sorted(self.config.items()):
            if key in sensitive_keys and value:
                display_value = f"{str(value)[:8]}..."
            else:
                display_value = value
            logger.info(f"{key}: {display_value}")
        logger.info("=== End Configuration ===")

# Global configuration instance
config_manager = None

def get_config() -> EnvConfigManager:
    """Get global configuration manager instance"""
    global config_manager
    if config_manager is None:
        config_manager = EnvConfigManager()
    return config_manager

def get_config_value(key: str, default: Any = None) -> Any:
    """Convenience function to get a configuration value"""
    return get_config().get(key, default)