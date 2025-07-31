#!/usr/bin/env python3
"""
Environment Configuration Manager for ash-nlp
Centralized management of all environment variables with validation
"""

import os
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class EnvConfigManager:
    """Centralized environment variable management with validation"""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize configuration manager"""
        self.env_file = env_file
        self.config = {}
        self.load_environment()
        self.validate_config()
        self.create_directories()
    
    def load_environment(self):
        """Load environment variables from .env file and system"""
        # Load from .env file if it exists
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            logger.info(f"Loaded environment from {self.env_file}")
        else:
            logger.warning(f"No {self.env_file} file found, using system environment only")
        
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
            'NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY': {'type': int, 'default': 50, 'min': 1},
            'NLP_LEARNING_PERSISTENCE_FILE': {'type': str, 'default': './learning_data/adjustments.json'},
            'NLP_MIN_CONFIDENCE_ADJUSTMENT': {'type': float, 'default': 0.05, 'min': 0.01, 'max': 0.5},
            'NLP_MAX_CONFIDENCE_ADJUSTMENT': {'type': float, 'default': 0.30, 'min': 0.05, 'max': 1.0},
            
            # =================================================================
            # THREE-MODEL CONFIGURATION
            # =================================================================
            # Model 1: Primary crisis detection (DeBERTa-based depression analysis)
            'NLP_DEPRESSION_MODEL': {'type': str, 'default': 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'},
            
            # Model 2: Contextual sentiment analysis (RoBERTa-based sentiment)
            'NLP_SENTIMENT_MODEL': {'type': str, 'default': 'Lowerated/lm6-deberta-v3-topic-sentiment'},
            
            # Model 3: Emotional distress detection (BART-based emotional analysis)
            'NLP_EMOTIONAL_DISTRESS_MODEL': {'type': str, 'default': 'facebook/bart-large-mnli'},
            
            # Model storage configuration
            'NLP_MODEL_CACHE_DIR': {'type': str, 'default': './models/cache'},
            
            # =================================================================
            # ENSEMBLE CONFIGURATION
            # =================================================================
            # Ensemble modes: consensus, majority, weighted
            'NLP_ENSEMBLE_MODE': {'type': str, 'default': 'consensus', 'choices': ['consensus', 'majority', 'weighted']},
            
            # Gap detection settings
            'NLP_GAP_DETECTION_THRESHOLD': {'type': float, 'default': 0.4, 'min': 0.1, 'max': 1.0},
            'NLP_DISAGREEMENT_THRESHOLD': {'type': float, 'default': 0.5, 'min': 0.1, 'max': 1.0},
            'NLP_AUTO_FLAG_DISAGREEMENTS': {'type': bool, 'default': True},
            
            # Model confidence weighting (for weighted ensemble mode)
            'NLP_DEPRESSION_MODEL_WEIGHT': {'type': float, 'default': 0.5, 'min': 0.0, 'max': 1.0},
            'NLP_SENTIMENT_MODEL_WEIGHT': {'type': float, 'default': 0.2, 'min': 0.0, 'max': 1.0},
            'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': {'type': float, 'default': 0.3, 'min': 0.0, 'max': 1.0},
            
            # =================================================================
            # HARDWARE CONFIGURATION
            # =================================================================
            'NLP_DEVICE': {'type': str, 'default': 'auto', 'choices': ['auto', 'cpu', 'cuda', 'cuda:0', 'cuda:1']},
            'NLP_MODEL_PRECISION': {'type': str, 'default': 'float16', 'choices': ['float32', 'float16', 'bfloat16']},
            
            # =================================================================
            # PERFORMANCE TUNING - THREE MODEL OPTIMIZATION
            # =================================================================
            # Optimized for RTX 3060 (12GB VRAM) + Ryzen 7 5800X + 64GB RAM
            'NLP_MAX_BATCH_SIZE': {'type': int, 'default': 48, 'min': 1, 'max': 128},  # Much larger batches with 12GB VRAM
            'NLP_INFERENCE_THREADS': {'type': int, 'default': 16, 'min': 1, 'max': 32},  # Ryzen 7 5800X has 8 cores/16 threads
            'NLP_MAX_CONCURRENT_REQUESTS': {'type': int, 'default': 20, 'min': 1, 'max': 100},  # Higher with abundant VRAM and RAM
            'NLP_REQUEST_TIMEOUT': {'type': int, 'default': 35, 'min': 5, 'max': 300},  # Faster with more VRAM for batch processing
            
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
            'GLOBAL_PYTHONUNBUFFERED': {'type': bool, 'default': True},
            'GLOBAL_ENABLE_DEBUG_MODE': {'type': bool, 'default': False},
            'NLP_FLIP_SENTIMENT_LOGIC': {'type': bool, 'default': False},
            
            # =================================================================
            # STORAGE PATHS
            # =================================================================
            'NLP_DATA_DIR': {'type': str, 'default': './data'},
            'NLP_MODELS_DIR': {'type': str, 'default': './models/cache'},
            'NLP_LOGS_DIR': {'type': str, 'default': './logs'},
            'NLP_LEARNING_DATA_DIR': {'type': str, 'default': './learning_data'},
            
            # =================================================================
            # CRISIS DETECTION THRESHOLDS
            # =================================================================
            # Individual model thresholds
            'NLP_HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.55, 'min': 0.1, 'max': 1.0},
            'NLP_MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.28, 'min': 0.1, 'max': 1.0},
            'NLP_LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.16, 'min': 0.1, 'max': 1.0},
            
            # Ensemble-specific thresholds
            'NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.60, 'min': 0.1, 'max': 1.0},
            'NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.35, 'min': 0.1, 'max': 1.0},
            'NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.20, 'min': 0.1, 'max': 1.0},
            
            # =================================================================
            # ENHANCED CRISIS DETECTION THRESHOLDS
            # =================================================================
            # Individual model thresholds
            'NLP_HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.55, 'min': 0.1, 'max': 1.0},
            'NLP_MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.28, 'min': 0.1, 'max': 1.0},
            'NLP_LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.16, 'min': 0.1, 'max': 1.0},

            # Ensemble-specific thresholds (existing - keep these)
            'NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.60, 'min': 0.1, 'max': 1.0},
            'NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.35, 'min': 0.1, 'max': 1.0},
            'NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.20, 'min': 0.1, 'max': 1.0},

            # ADDITIONAL THRESHOLD CONTROLS - Add these new ones:
            'NLP_MILD_CRISIS_THRESHOLD': {'type': float, 'default': 0.30, 'min': 0.1, 'max': 1.0},
            'NLP_NEGATIVE_RESPONSE_THRESHOLD': {'type': float, 'default': 0.70, 'min': 0.1, 'max': 1.0},
            'NLP_UNKNOWN_RESPONSE_THRESHOLD': {'type': float, 'default': 0.50, 'min': 0.1, 'max': 1.0},

            # CONSENSUS SENSITIVITY CONTROLS - Add these new ones:
            'NLP_CONSENSUS_SAFETY_BIAS': {'type': float, 'default': 0.1, 'min': 0.0, 'max': 0.5},  # Bias toward higher crisis levels
            'NLP_ENABLE_SAFETY_OVERRIDE': {'type': bool, 'default': True},  # Allow individual severe model results to override consensus

            # =================================================================
            # RATE LIMITING
            # =================================================================
            'NLP_MAX_REQUESTS_PER_MINUTE': {'type': int, 'default': 120, 'min': 1},  # Much higher with 12GB VRAM + excellent hardware
            'NLP_MAX_REQUESTS_PER_HOUR': {'type': int, 'default': 2000, 'min': 1},   # Significantly increased for abundant VRAM
            
            # =================================================================
            # SECURITY
            # =================================================================
            'GLOBAL_ALLOWED_IPS': {'type': str, 'default': '10.20.30.0/24,127.0.0.1,::1'},
            'GLOBAL_ENABLE_CORS': {'type': bool, 'default': True},
            
            # =================================================================
            # EXPERIMENTAL FEATURES
            # =================================================================
            # Enable experimental three-model features
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
        """Validate configuration consistency for 3-model ensemble"""
        
        # Validate individual model threshold ordering
        if self.config['NLP_HIGH_CRISIS_THRESHOLD'] <= self.config['NLP_MEDIUM_CRISIS_THRESHOLD']:
            raise ValueError("NLP_HIGH_CRISIS_THRESHOLD must be > NLP_MEDIUM_CRISIS_THRESHOLD")
        
        if self.config['NLP_MEDIUM_CRISIS_THRESHOLD'] <= self.config['NLP_LOW_CRISIS_THRESHOLD']:
            raise ValueError("NLP_MEDIUM_CRISIS_THRESHOLD must be > NLP_LOW_CRISIS_THRESHOLD")
        
        # Validate ensemble threshold ordering
        if self.config['NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD'] <= self.config['NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD']:
            raise ValueError("NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD must be > NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD")
        
        if self.config['NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD'] <= self.config['NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD']:
            raise ValueError("NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD must be > NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD")
        
        # Validate learning system settings
        if self.config['NLP_MIN_CONFIDENCE_ADJUSTMENT'] >= self.config['NLP_MAX_CONFIDENCE_ADJUSTMENT']:
            raise ValueError("NLP_MIN_CONFIDENCE_ADJUSTMENT must be < NLP_MAX_CONFIDENCE_ADJUSTMENT")
        
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
        if self.config['NLP_GAP_DETECTION_THRESHOLD'] >= self.config['NLP_DISAGREEMENT_THRESHOLD']:
            raise ValueError("NLP_GAP_DETECTION_THRESHOLD should be < NLP_DISAGREEMENT_THRESHOLD")
        
        logger.info("3-Model ensemble configuration validation passed")
        logger.info(f"Ensemble mode: {self.config['NLP_ENSEMBLE_MODE']}")
        logger.info(f"Model weights: Depression={self.config['NLP_DEPRESSION_MODEL_WEIGHT']}, "
                    f"Sentiment={self.config['NLP_SENTIMENT_MODEL_WEIGHT']}, "
                    f"Emotional={self.config['NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT']}")
        
        # Log hardware optimization
        logger.info(f"Hardware optimization: Batch size={self.config['NLP_MAX_BATCH_SIZE']}, "
                    f"Threads={self.config['NLP_INFERENCE_THREADS']}, "
                    f"Concurrent requests={self.config['NLP_MAX_CONCURRENT_REQUESTS']}")
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.config['NLP_DATA_DIR'],
            self.config['NLP_MODELS_DIR'],
            self.config['NLP_LOGS_DIR'],
            self.config['NLP_LEARNING_DATA_DIR'],
            os.path.dirname(self.config['NLP_MODEL_CACHE_DIR']),
            os.path.dirname(self.config['NLP_LEARNING_PERSISTENCE_FILE']),
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
    
    def print_config(self):
        """Print configuration for debugging (hiding sensitive values)"""
        sensitive_keys = ['GLOBAL_HUGGINGFACE_TOKEN']
        
        logger.info("=== NLP Service Configuration ===")
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