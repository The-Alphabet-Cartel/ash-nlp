"""
Enhanced Configuration Manager for NLP Server with Secrets Support
Located in: config/nlp_config_manager.py
Integrates with existing nlp_settings.py
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Import existing settings for defaults
from .nlp_settings import CRISIS_THRESHOLDS, SERVER_CONFIG

logger = logging.getLogger(__name__)

class NLPConfigManager:
    """Configuration manager for NLP server with secrets support"""
    
    def __init__(self, env_file: Optional[str] = None):
        self._config = {}
        self._load_environment(env_file)
        self._load_and_validate_config()
    
    def _load_environment(self, env_file: Optional[str] = None):
        """Load environment file if specified"""
        if env_file and Path(env_file).exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_file)
                logger.info(f"📁 Loaded environment from {env_file}")
            except ImportError:
                logger.warning("python-dotenv not available, using system environment only")
    
    def _read_secret_file(self, secret_path: str, suppress_warnings: bool = False) -> Optional[str]:
        """Read secret from file"""
        try:
            if Path(secret_path).exists():
                with open(secret_path, 'r', encoding='utf-8') as f:
                    secret = f.read().strip()
                logger.info(f"🔐 Successfully read secret from {secret_path}")
                return secret
            else:
                if not suppress_warnings:
                    logger.debug(f"🔍 Secret file not found: {secret_path}")
                return None
        except Exception as e:
            logger.error(f"❌ Failed to read secret from {secret_path}: {e}")
            return None
    
    def _get_config_value(self, key: str, default: Any = None, secret_file_suffix: str = None) -> Any:
        """
        Get configuration value with secrets support
        
        Priority order:
        1. Secret file (if secret_file_suffix provided)
        2. Environment variable
        3. Default value
        """
        # Check for secret file first
        if secret_file_suffix:
            secret_file_env = f"{key}_FILE"
            secret_file_path = os.getenv(secret_file_env)
            
            # If explicit secret file path is provided, use it
            if secret_file_path:
                secret_value = self._read_secret_file(secret_file_path)
                if secret_value:
                    return secret_value
                logger.warning(f"⚠️ Secret file specified but couldn't read: {secret_file_path}")
            else:
                # Try common secret file locations
                secret_paths = [
                    f"./secrets/{secret_file_suffix}",  # Windows/Local development
                    f"/run/secrets/{secret_file_suffix}",  # Docker container
                    f"./{secret_file_suffix}.txt",  # Alternative local location
                ]
                
                for i, path in enumerate(secret_paths):
                    # Only suppress warnings for the fallback paths
                    suppress_warnings = i > 0
                    secret_value = self._read_secret_file(path, suppress_warnings)
                    if secret_value:
                        logger.info(f"🔐 Found secret in path: {path}")
                        return secret_value
        
        # Fall back to environment variable
        env_value = os.getenv(key)
        if env_value:
            return env_value
        
        # Use default
        return default
    
    def _load_and_validate_config(self):
        """Load and validate all NLP server configuration"""
        logger.info("📋 Loading NLP server configuration with secrets support...")
        
        # Create directories if they don't exist
        directories = [
            './data', './models', './logs', './learning_data', 
            './models/cache', './learning_data'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # API Keys (sensitive - use secrets)
        self._config['GLOBAL_CLAUDE_API_KEY'] = self._get_config_value(
            'GLOBAL_CLAUDE_API_KEY',
            secret_file_suffix='claude_api_key'
        )
        
        self._config['GLOBAL_HUGGINGFACE_TOKEN'] = self._get_config_value(
            'GLOBAL_HUGGINGFACE_TOKEN',
            secret_file_suffix='huggingface_token'
        )
        
        self._config['OPENAI_API_KEY'] = self._get_config_value(
            'OPENAI_API_KEY',
            secret_file_suffix='openai_api_key'
        )
        
        # Hugging Face Configuration
        self._config['NLP_HUGGINGFACE_CACHE_DIR'] = self._get_config_value(
            'NLP_HUGGINGFACE_CACHE_DIR', './models/cache'
        )
        
        # Learning System Configuration
        self._config['GLOBAL_ENABLE_LEARNING_SYSTEM'] = self._get_config_value(
            'GLOBAL_ENABLE_LEARNING_SYSTEM', 'true'
        ).lower() in ('true', '1', 'yes')
        
        self._config['NLP_LEARNING_RATE'] = float(self._get_config_value(
            'NLP_LEARNING_RATE', '0.1'
        ))
        
        self._config['NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY'] = int(self._get_config_value(
            'NLP_MAX_LEARNING_ADJUSTMENTS_PER_DAY', '50'
        ))
        
        self._config['NLP_LEARNING_PERSISTENCE_FILE'] = self._get_config_value(
            'NLP_LEARNING_PERSISTENCE_FILE', './learning_data/adjustments.json'
        )
        
        self._config['NLP_MIN_CONFIDENCE_ADJUSTMENT'] = float(self._get_config_value(
            'NLP_MIN_CONFIDENCE_ADJUSTMENT', '0.05'
        ))
        
        self._config['NLP_MAX_CONFIDENCE_ADJUSTMENT'] = float(self._get_config_value(
            'NLP_MAX_CONFIDENCE_ADJUSTMENT', '0.30'
        ))
        
        # Model Configuration
        self._config['NLP_DEPRESSION_MODEL'] = self._get_config_value(
            'NLP_DEPRESSION_MODEL', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'
        )
        
        self._config['NLP_SENTIMENT_MODEL'] = self._get_config_value(
            'NLP_SENTIMENT_MODEL', 'Lowerated/lm6-deberta-v3-topic-sentiment'
        )
        
        self._config['NLP_MODEL_CACHE_DIR'] = self._get_config_value(
            'NLP_MODEL_CACHE_DIR', './models/cache'
        )
        
        # Hardware Configuration (optimized for RTX 3050 + Ryzen 7 7700x)
        self._config['NLP_DEVICE'] = self._get_config_value('NLP_DEVICE', 'auto')
        self._config['NLP_MODEL_PRECISION'] = self._get_config_value('NLP_MODEL_PRECISION', 'float16')
        
        # Performance Tuning (use SERVER_CONFIG hardware info as basis)
        hardware_info = SERVER_CONFIG.get('hardware_info', {})
        cpu_cores = 8 if 'Ryzen 7 7700x' in hardware_info.get('cpu', '') else 4
        
        self._config['NLP_MAX_BATCH_SIZE'] = int(self._get_config_value('NLP_MAX_BATCH_SIZE', '32'))
        self._config['NLP_INFERENCE_THREADS'] = int(self._get_config_value('NLP_INFERENCE_THREADS', str(cpu_cores)))
        self._config['NLP_MAX_CONCURRENT_REQUESTS'] = int(self._get_config_value('NLP_MAX_CONCURRENT_REQUESTS', '12'))
        self._config['NLP_REQUEST_TIMEOUT'] = int(self._get_config_value('NLP_REQUEST_TIMEOUT', '30'))
        
        # Server Configuration
        self._config['NLP_SERVICE_HOST'] = self._get_config_value('NLP_SERVICE_HOST', '0.0.0.0')
        self._config['NLP_SERVICE_PORT'] = int(self._get_config_value('NLP_SERVICE_PORT', '8881'))
        self._config['NLP_UVICORN_WORKERS'] = int(self._get_config_value('NLP_UVICORN_WORKERS', '1'))
        self._config['NLP_RELOAD_ON_CHANGES'] = self._get_config_value('NLP_RELOAD_ON_CHANGES', 'false').lower() in ('true', '1', 'yes')
        
        # Logging Configuration
        self._config['GLOBAL_LOG_LEVEL'] = self._get_config_value('GLOBAL_LOG_LEVEL', 'INFO').upper()
        self._config['NLP_LOG_FILE'] = self._get_config_value('NLP_LOG_FILE', 'nlp_service.log')
        self._config['GLOBAL_ENABLE_DEBUG_MODE'] = self._get_config_value('GLOBAL_ENABLE_DEBUG_MODE', 'false').lower() in ('true', '1', 'yes')
        
        # Storage Paths
        self._config['NLP_DATA_DIR'] = self._get_config_value('NLP_DATA_DIR', './data')
        self._config['NLP_MODELS_DIR'] = self._get_config_value('NLP_MODELS_DIR', './models/cache')
        self._config['NLP_LOGS_DIR'] = self._get_config_value('NLP_LOGS_DIR', './logs')
        self._config['NLP_LEARNING_DATA_DIR'] = self._get_config_value('NLP_LEARNING_DATA_DIR', './learning_data')
        
        # Crisis Detection Thresholds (use existing nlp_settings as defaults)
        self._config['NLP_HIGH_CRISIS_THRESHOLD'] = float(self._get_config_value(
            'NLP_HIGH_CRISIS_THRESHOLD', str(CRISIS_THRESHOLDS.get('high', 0.55))
        ))
        self._config['NLP_MEDIUM_CRISIS_THRESHOLD'] = float(self._get_config_value(
            'NLP_MEDIUM_CRISIS_THRESHOLD', str(CRISIS_THRESHOLDS.get('medium', 0.28))
        ))
        self._config['NLP_LOW_CRISIS_THRESHOLD'] = float(self._get_config_value(
            'NLP_LOW_CRISIS_THRESHOLD', str(CRISIS_THRESHOLDS.get('low', 0.16))
        ))
        
        # Rate Limiting
        self._config['NLP_MAX_REQUESTS_PER_MINUTE'] = int(self._get_config_value('NLP_MAX_REQUESTS_PER_MINUTE', '60'))
        self._config['NLP_MAX_REQUESTS_PER_HOUR'] = int(self._get_config_value('NLP_MAX_REQUESTS_PER_HOUR', '1000'))
        
        # Security
        self._config['GLOBAL_ALLOWED_IPS'] = self._get_config_value('GLOBAL_ALLOWED_IPS', '10.20.30.0/24,127.0.0.1,::1')
        self._config['GLOBAL_ENABLE_CORS'] = self._get_config_value('GLOBAL_ENABLE_CORS', 'true').lower() in ('true', '1', 'yes')
        
        # Health Check Configuration
        self._config['NLP_HEALTH_CHECK_INTERVAL'] = int(self._get_config_value('NLP_HEALTH_CHECK_INTERVAL', '60'))
        self._config['NLP_HEALTH_CHECK_INTERVAL'] = int(self._get_config_value('NLP_HEALTH_CHECK_INTERVAL', '30'))
        self._config['NLP_HEALTH_CHECK_START_PERIOD'] = int(self._get_config_value('NLP_HEALTH_CHECK_START_PERIOD', '300'))
        
        # Log configuration summary
        using_secrets = bool(
            os.getenv('CLAUDE_API_KEY_FILE') or 
            os.getenv('HUGGINGFACE_TOKEN_FILE') or
            Path("./secrets/claude_api_key").exists() or
            Path("./secrets/huggingface_token").exists()
        )
        
        logger.info("📊 NLP Server Configuration Summary:")
        logger.info(f"   🔐 Using secrets: {using_secrets}")
        logger.info(f"   🖥️ Device: {self._config['NLP_DEVICE']}")
        logger.info(f"   🧠 Model precision: {self._config['NLP_MODEL_PRECISION']}")
        logger.info(f"   ⚡ Max batch size: {self._config['NLP_MAX_BATCH_SIZE']}")
        logger.info(f"   🧵 Inference threads: {self._config['NLP_INFERENCE_THREADS']}")
        logger.info(f"   🌐 Server: {self._config['NLP_SERVICE_HOST']}:{self._config['NLP_SERVICE_PORT']}")
        logger.info(f"   📚 Learning system: {self._config['GLOBAL_ENABLE_LEARNING_SYSTEM']}")
        logger.info(f"   📝 Log level: {self._config['GLOBAL_LOG_LEVEL']}")
        
        # Validate critical settings
        if not self._config['GLOBAL_CLAUDE_API_KEY'] and self._config['GLOBAL_ENABLE_LEARNING_SYSTEM']:
            logger.warning("⚠️ Claude API key not found - learning system may be limited")
        
        if not self._config['GLOBAL_HUGGINGFACE_TOKEN']:
            logger.warning("⚠️ HuggingFace token not found - model downloads may be limited")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        value = self._config.get(key, default)
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            logger.warning(f"Invalid integer value for {key}: {value}, using default: {default}")
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get float configuration value"""
        value = self._config.get(key, default)
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            logger.warning(f"Invalid float value for {key}: {value}, using default: {default}")
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        value = self._config.get(key, default)
        if isinstance(value, bool):
            return value
        return str(value).lower() in ['true', '1', 'yes', 'on']
    
    def get_crisis_thresholds(self) -> Dict[str, float]:
        """Get crisis thresholds in the format expected by existing code"""
        return {
            'high': self._config['NLP_HIGH_CRISIS_THRESHOLD'],
            'medium': self._config['NLP_MEDIUM_CRISIS_THRESHOLD'], 
            'low': self._config['NLP_LOW_CRISIS_THRESHOLD']
        }
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server config compatible with existing nlp_settings.SERVER_CONFIG"""
        base_config = SERVER_CONFIG.copy()
        
        # Update with current configuration
        base_config['hardware_info'].update({
            'inference_threads': self._config['NLP_INFERENCE_THREADS'],
            'max_batch_size': self._config['NLP_MAX_BATCH_SIZE'],
            'max_concurrent_requests': self._config['NLP_MAX_CONCURRENT_REQUESTS']
        })
        
        # Update capabilities based on available API keys
        if self._config.get('GLOBAL_CLAUDE_API_KEY'):
            base_config['capabilities']['claude_integration'] = "Available with secrets"
        
        if self._config.get('GLOBAL_HUGGINGFACE_TOKEN'):
            base_config['capabilities']['model_downloads'] = "Enhanced with HF token"
        
        return base_config
    
    def get_all_safe(self) -> Dict[str, Any]:
        """Get all configuration (excluding sensitive values)"""
        safe_config = self._config.copy()
        # Mask sensitive values
        sensitive_keys = ['GLOBAL_HUGGINGFACE_TOKEN']
        for key in sensitive_keys:
            if key in safe_config and safe_config[key]:
                safe_config[key] = f"{safe_config[key][:10]}..."
        return safe_config

# Global config instance
_nlp_config = None

def get_nlp_config() -> NLPConfigManager:
    """Get the global NLP configuration instance"""
    global _nlp_config
    if _nlp_config is None:
        _nlp_config = NLPConfigManager()
    return _nlp_config

# For backward compatibility with existing code
def get_env_config() -> Dict[str, Any]:
    """Get configuration as dictionary (backward compatibility)"""
    config = get_nlp_config()
    return config._config

# Enhanced compatibility functions for existing nlp_settings.py usage
def get_crisis_thresholds() -> Dict[str, float]:
    """Get crisis thresholds (replaces nlp_settings.CRISIS_THRESHOLDS)"""
    config = get_nlp_config()
    return config.get_crisis_thresholds()

def get_server_config() -> Dict[str, Any]:
    """Get server config (replaces nlp_settings.SERVER_CONFIG)"""
    config = get_nlp_config()
    return config.get_server_config()