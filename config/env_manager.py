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
            # Hugging Face Configuration
            'HUGGINGFACE_HUB_TOKEN': {'type': str, 'default': None, 'required': False},
            'HUGGINGFACE_CACHE_DIR': {'type': str, 'default': './models/cache'},
            
            # Learning System
            'ENABLE_LEARNING_SYSTEM': {'type': bool, 'default': True},
            'LEARNING_RATE': {'type': float, 'default': 0.1, 'min': 0.01, 'max': 1.0},
            'MAX_LEARNING_ADJUSTMENTS_PER_DAY': {'type': int, 'default': 50, 'min': 1},
            'LEARNING_PERSISTENCE_FILE': {'type': str, 'default': './learning_data/adjustments.json'},
            'MIN_CONFIDENCE_ADJUSTMENT': {'type': float, 'default': 0.05, 'min': 0.01, 'max': 0.5},
            'MAX_CONFIDENCE_ADJUSTMENT': {'type': float, 'default': 0.30, 'min': 0.1, 'max': 1.0},
            
            # Model Configuration
            'DEPRESSION_MODEL': {'type': str, 'default': 'rafalposwiata/deproberta-large-depression'},
            'SENTIMENT_MODEL': {'type': str, 'default': 'cardiffnlp/twitter-roberta-base-sentiment-latest'},
            'MODEL_CACHE_DIR': {'type': str, 'default': './models/cache'},
            
            # Hardware Configuration
            'DEVICE': {'type': str, 'default': 'auto', 'choices': ['auto', 'cpu', 'cuda']},
            'MODEL_PRECISION': {'type': str, 'default': 'float16', 'choices': ['float32', 'float16', 'bfloat16']},
            
            # Performance Tuning
            'MAX_BATCH_SIZE': {'type': int, 'default': 32, 'min': 1, 'max': 128},
            'INFERENCE_THREADS': {'type': int, 'default': 4, 'min': 1, 'max': 16},
            'MAX_CONCURRENT_REQUESTS': {'type': int, 'default': 10, 'min': 1, 'max': 100},
            'REQUEST_TIMEOUT': {'type': int, 'default': 30, 'min': 5, 'max': 300},
            
            # Server Configuration
            'NLP_SERVICE_HOST': {'type': str, 'default': '0.0.0.0'},
            'NLP_SERVICE_PORT': {'type': int, 'default': 8881, 'min': 1024, 'max': 65535},
            'UVICORN_WORKERS': {'type': int, 'default': 1, 'min': 1, 'max': 8},
            'RELOAD_ON_CHANGES': {'type': bool, 'default': False},
            
            # Logging Configuration
            'LOG_LEVEL': {'type': str, 'default': 'INFO', 'choices': ['DEBUG', 'INFO', 'WARNING', 'ERROR']},
            'LOG_FILE': {'type': str, 'default': 'nlp_service.log'},
            'PYTHONUNBUFFERED': {'type': str, 'default': '1'},
            'ENABLE_DEBUG_LOGGING': {'type': bool, 'default': False},
            
            # Storage Paths
            'DATA_DIR': {'type': str, 'default': './data'},
            'MODELS_DIR': {'type': str, 'default': './models'},
            'LOGS_DIR': {'type': str, 'default': './logs'},
            'LEARNING_DATA_DIR': {'type': str, 'default': './learning_data'},
            
            # Crisis Detection Thresholds
            'HIGH_CRISIS_THRESHOLD': {'type': float, 'default': 0.7, 'min': 0.1, 'max': 1.0},
            'MEDIUM_CRISIS_THRESHOLD': {'type': float, 'default': 0.4, 'min': 0.1, 'max': 1.0},
            'LOW_CRISIS_THRESHOLD': {'type': float, 'default': 0.2, 'min': 0.1, 'max': 1.0},
            
            # Rate Limiting
            'MAX_REQUESTS_PER_MINUTE': {'type': int, 'default': 60, 'min': 1},
            'MAX_REQUESTS_PER_HOUR': {'type': int, 'default': 1000, 'min': 1},
            
            # Security
            'ALLOWED_IPS': {'type': str, 'default': '10.20.30.0/24,127.0.0.1,::1'},
            'ENABLE_CORS': {'type': bool, 'default': True},
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
        """Validate configuration consistency"""
        # Validate threshold ordering
        if self.config['HIGH_CRISIS_THRESHOLD'] <= self.config['MEDIUM_CRISIS_THRESHOLD']:
            raise ValueError("HIGH_CRISIS_THRESHOLD must be > MEDIUM_CRISIS_THRESHOLD")
        
        if self.config['MEDIUM_CRISIS_THRESHOLD'] <= self.config['LOW_CRISIS_THRESHOLD']:
            raise ValueError("MEDIUM_CRISIS_THRESHOLD must be > LOW_CRISIS_THRESHOLD")
        
        # Validate learning system settings
        if self.config['MIN_CONFIDENCE_ADJUSTMENT'] >= self.config['MAX_CONFIDENCE_ADJUSTMENT']:
            raise ValueError("MIN_CONFIDENCE_ADJUSTMENT must be < MAX_CONFIDENCE_ADJUSTMENT")
        
        logger.info("Configuration validation passed")
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.config['DATA_DIR'],
            self.config['MODELS_DIR'],
            self.config['LOGS_DIR'],
            self.config['LEARNING_DATA_DIR'],
            os.path.dirname(self.config['MODEL_CACHE_DIR']),
            os.path.dirname(self.config['LEARNING_PERSISTENCE_FILE']),
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
        sensitive_keys = ['HUGGINGFACE_HUB_TOKEN']
        
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