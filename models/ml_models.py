"""
Enhanced ML Model Management for Ash NLP Service - Three Model Architecture
UPDATED: Now supports JSON configuration from managers/ directory with environment variable substitution
Handles loading, caching, and access to ML models with DistilBERT emotional distress detection
"""

import logging
import os
import torch
import time
from transformers import pipeline, AutoConfig
from typing import Optional, Dict, Any, Union, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedModelManager:
    """Enhanced centralized management of ML models with JSON Configuration from managers/ + Three Zero-Shot Model Ensemble support"""
    
    def __init__(self, config_manager: Optional[Any] = None, ensemble_manager: Optional[Any] = None):
        """
        Initialize ModelManager with optional configuration managers
        
        Args:
            config_manager: Optional configuration manager for secrets/environment
            ensemble_manager: Optional JSON configuration manager from managers/ directory
        """
        self.config_manager = config_manager
        self.ensemble_manager = ensemble_manager
        
        # Load configuration from multiple sources
        self.config = self._load_unified_config()
        
        # Model instances - THREE MODELS NOW
        self.depression_model = None
        self.sentiment_model = None
        self.emotional_distress_model = None
        self._models_loaded = False
        
        # Device configuration
        self.device = self._configure_device()
        
        # Set up model cache directory
        self._setup_cache_directory()
        
        # Set up Hugging Face authentication if token provided
        self._setup_huggingface_auth()
        
        config_source = "JSON + Environment (managers/)" if self.ensemble_manager else "Environment Only"
        logger.info(f"Enhanced ModelManager initialized with {config_source} configuration")
        logger.info(f"Device: {self.device}")
        logger.info(f"Model cache directory: {self.config['cache_dir']}")
    
    def _load_unified_config(self) -> Dict[str, Any]:
        """Load configuration from JSON (if available) and environment variables"""
        config = {}
        
        # Start with environment variable defaults
        config.update(self._load_env_config())
        
        # Override with JSON configuration if available
        if self.ensemble_manager:
            try:
                json_config = self._load_json_config()
                config.update(json_config)
                logger.info("✅ JSON configuration integrated with environment settings from managers/")
            except Exception as e:
                logger.warning(f"⚠️ Could not load JSON config from managers/, using environment only: {e}")
        
        return config
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables (fallback/operational config)"""
        # Use direct environment variable access since config_manager might not be available
        return {
            # Model names (can be overridden by JSON)
            'depression_model': os.getenv('NLP_DEPRESSION_MODEL', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
            'sentiment_model': os.getenv('NLP_SENTIMENT_MODEL', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
            'emotional_distress_model': os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL', 'facebook/bart-large-mnli'),
            
            # Operational settings
            'cache_dir': os.getenv('NLP_MODEL_CACHE_DIR', './models/cache'),
            'device': os.getenv('NLP_DEVICE', 'auto'),
            'precision': os.getenv('NLP_MODEL_PRECISION', 'float16'),
            'max_batch_size': int(os.getenv('NLP_MAX_BATCH_SIZE', '32')),
            'huggingface_token': os.getenv('GLOBAL_HUGGINGFACE_TOKEN'),
            
            # Ensemble settings
            'depression_weight': float(os.getenv('NLP_DEPRESSION_MODEL_WEIGHT', '0.6')),
            'sentiment_weight': float(os.getenv('NLP_SENTIMENT_MODEL_WEIGHT', '0.15')),
            'emotional_distress_weight': float(os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', '0.25')),
            'ensemble_mode': os.getenv('NLP_ENSEMBLE_MODE', 'weighted'),
            'gap_detection_threshold': float(os.getenv('NLP_GAP_DETECTION_THRESHOLD', '0.25')),
            'disagreement_threshold': float(os.getenv('NLP_DISAGREEMENT_THRESHOLD', '0.35'))
        }
    
    def _load_json_config(self) -> Dict[str, Any]:
        """Load configuration from JSON ensemble manager in managers/ directory"""
        json_config = {}
        
        # Get model definitions from JSON
        model_definitions = self.ensemble_manager.get_model_definitions()
        
        # Extract model configurations
        for model_key, model_config in model_definitions.items():
            if model_key == 'depression':
                json_config['depression_model'] = model_config['name']
                json_config['depression_weight'] = model_config.get('weight', model_config.get('default_weight', 0.6))
            elif model_key == 'sentiment':
                json_config['sentiment_model'] = model_config['name']
                json_config['sentiment_weight'] = model_config.get('weight', model_config.get('default_weight', 0.15))
            elif model_key == 'emotional_distress':
                json_config['emotional_distress_model'] = model_config['name']
                json_config['emotional_distress_weight'] = model_config.get('weight', model_config.get('default_weight', 0.25))
        
        # Get ensemble configuration
        ensemble_config = self.ensemble_manager.get_ensemble_configuration()
        json_config['ensemble_mode'] = ensemble_config.get('default_mode', 'weighted')
        
        # Get hardware optimization settings
        hardware_config = self.ensemble_manager.get_hardware_optimization()
        json_config['device'] = hardware_config.get('device', 'auto')
        json_config['precision'] = hardware_config.get('precision', 'float16')
        
        return json_config
    
    def _configure_device(self) -> str:
        """Configure device based on configuration and availability"""
        device_config = self.config['device']
        
        if device_config == 'auto':
            if torch.cuda.is_available():
                device = f"cuda:{torch.cuda.current_device()}"
                gpu_name = torch.cuda.get_device_name()
                logger.info(f"🔥 Using GPU: {gpu_name}")
            else:
                device = "cpu"
                logger.info("💻 Using CPU (CUDA not available)")
        else:
            device = device_config
            logger.info(f"🎯 Using configured device: {device}")
        
        return device
    
    def _setup_cache_directory(self):
        """Set up model cache directory"""
        cache_dir = Path(self.config['cache_dir'])
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Set environment variables for transformers
        os.environ['HF_HOME'] = str(cache_dir)
        os.environ['TRANSFORMERS_CACHE'] = str(cache_dir)
        os.environ['HF_DATASETS_CACHE'] = str(cache_dir)
        
        logger.info(f"📁 Model cache directory configured: {cache_dir}")
    
    def _setup_huggingface_auth(self):
        """Set up Hugging Face authentication"""
        hf_token = self.config.get('huggingface_token')
        if hf_token:
            os.environ['HF_TOKEN'] = hf_token
            logger.info("🔑 Hugging Face authentication configured")
        else:
            logger.info("ℹ️ No Hugging Face token provided")
    
    def _get_torch_dtype(self):
        """Get torch dtype based on precision configuration"""
        precision = self.config['precision']
        if precision == 'float16':
            return torch.float16
        elif precision == 'bfloat16':
            return torch.bfloat16
        elif precision == 'float32':
            return torch.float32
        else:
            logger.warning(f"Unknown precision '{precision}', using float16")
            return torch.float16
    
    async def load_models(self):
        """Load all three models with simplified configuration"""
        try:
            logger.info("🚀 Starting model loading...")
            
            # Load depression model
            logger.info(f"📦 Loading depression model: {self.config['depression_model']}")
            self.depression_model = pipeline(
                "zero-shot-classification",
                model=self.config['depression_model'],
                device=self.device,
                torch_dtype=self._get_torch_dtype()
            )
            logger.info("✅ Depression model loaded")
            
            # Load sentiment model
            logger.info(f"📦 Loading sentiment model: {self.config['sentiment_model']}")
            self.sentiment_model = pipeline(
                "zero-shot-classification",
                model=self.config['sentiment_model'],
                device=self.device,
                torch_dtype=self._get_torch_dtype()
            )
            logger.info("✅ Sentiment model loaded")
            
            # Load emotional distress model
            logger.info(f"📦 Loading emotional distress model: {self.config['emotional_distress_model']}")
            self.emotional_distress_model = pipeline(
                "zero-shot-classification",
                model=self.config['emotional_distress_model'],
                device=self.device,
                torch_dtype=self._get_torch_dtype()
            )
            logger.info("✅ Emotional distress model loaded")
            
            self._models_loaded = True
            logger.info("🎯 All three models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
            self._models_loaded = False
            raise
    
    def models_loaded(self) -> bool:
        """Check if all models are loaded"""
        return (self._models_loaded and 
                self.depression_model is not None and 
                self.sentiment_model is not None and 
                self.emotional_distress_model is not None)
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get detailed status of all models"""
        return {
            "models_loaded": self.models_loaded(),
            "device": self.device,
            "precision": self.config['precision'],
            "ensemble_mode": self.config['ensemble_mode'],
            "configuration_source": "JSON + Environment (managers/)" if self.ensemble_manager else "Environment Only",
            "models": {
                "depression": {
                    "name": self.config['depression_model'],
                    "loaded": self.depression_model is not None,
                    "weight": self.config['depression_weight']
                },
                "sentiment": {
                    "name": self.config['sentiment_model'],
                    "loaded": self.sentiment_model is not None,
                    "weight": self.config['sentiment_weight']
                },
                "emotional_distress": {
                    "name": self.config['emotional_distress_model'],
                    "loaded": self.emotional_distress_model is not None,
                    "weight": self.config['emotional_distress_weight']
                }
            }
        }

# Global model manager instance
_global_model_manager = None

def set_model_manager(manager: EnhancedModelManager):
    """Set the global model manager instance"""
    global _global_model_manager
    _global_model_manager = manager

def get_model_manager() -> Optional[EnhancedModelManager]:
    """Get the global model manager instance"""
    return _global_model_manager

# Backward compatibility
ModelManager = EnhancedModelManager