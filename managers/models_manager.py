# ash/ash-nlp/managers/models_manager.py
"""
ModelsManager v3.1 - Advanced Model Ensemble Management
Phase 3d Step 9: Updated for UnifiedConfigManager integration - NO MORE os.getenv() calls

Advanced manager for handling three zero-shot model ensemble with GPU optimization,
model caching, and comprehensive validation.

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import torch
from typing import Dict, Any, List, Optional, Union
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class ModelsManager:
    """
    Manages Three Zero-Shot Model Ensemble for Crisis Detection
    Phase 3d Step 9: Updated to use UnifiedConfigManager instead of direct os.getenv() calls
    
    Supports: Depression Detection, Sentiment Analysis, Emotional Distress Detection
    Features: GPU optimization, model caching, weight validation, health monitoring
    """
    
    def __init__(self, unified_config_manager, settings_manager=None, zero_shot_manager=None):
        """
        Initialize ModelsManager with UnifiedConfigManager
        
        Args:
            unified_config_manager: UnifiedConfigManager instance (required)
            settings_manager: SettingsManager instance (optional)
            zero_shot_manager: ZeroShotManager instance (optional)
        """
        if unified_config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ModelsManager")
        
        self.unified_config = unified_config_manager
        self.settings_manager = settings_manager
        self.zero_shot_manager = zero_shot_manager
        
        # Initialize model storage
        self.depression_model = None
        self.sentiment_model = None
        self.emotional_distress_model = None
        self.depression_tokenizer = None
        self.sentiment_tokenizer = None
        self.emotional_distress_tokenizer = None
        
        # Extract configuration from unified config manager
        self.model_config = self._extract_model_config_from_unified_manager()
        self.hardware_config = self._extract_hardware_config_from_unified_manager()
        
        logger.info("🤖 Initializing ModelsManager v3.1 with Three Zero-Shot Model Ensemble...")
        
        # Device configuration
        self.device = self._configure_device()
        
        # Set up model cache directory (with robust fallback handling)
        self._setup_cache_directory()
        
        logger.info("✅ ModelsManager initialized with Three Zero-Shot Model Ensemble")
        logger.debug(f"Device: {self.device}")
        logger.debug(f"Model cache directory: {self.model_config.get('cache_dir', 'not set')}")
        logger.debug(f"HuggingFace token available: {bool(self.model_config.get('huggingface_token'))}")
    
    def _extract_model_config_from_unified_manager(self) -> Dict[str, Any]:
        """Extract model configuration from UnifiedConfigManager (Phase 3d Step 9)"""
        logger.debug("🔍 Extracting model configuration from UnifiedConfigManager...")
        
        try:
            # Get configuration using unified config manager methods
            full_model_config = self.unified_config.get_model_configuration()
            
            logger.debug(f"🔍 Full model config structure: {list(full_model_config.keys())}")
            
            # Extract models from the nested structure
            models = full_model_config.get('models', {})
            logger.debug(f"🔍 Models found: {list(models.keys())}")
            
            # Get cache_dir using unified config (NO MORE os.getenv calls)
            cache_dir = (
                self.unified_config.get_env('NLP_STORAGE_MODELS_DIR') or
                self.unified_config.get_env('NLP_MODEL_CACHE_DIR') or
                self.unified_config.get_env('NLP_HUGGINGFACE_CACHE_DIR') or
                './models/cache'
            )
            
            # Extract ensemble mode from nested structure or unified config
            ensemble_mode = (
                full_model_config.get('ensemble_config', {}).get('mode') or
                self.unified_config.get_env('NLP_ENSEMBLE_MODE', 'majority')
            )
            
            # Extract gap detection settings
            gap_detection_config = full_model_config.get('ensemble_config', {}).get('gap_detection', {})
            
            # Read HuggingFace token using unified config
            hf_token = self.unified_config.get_env('GLOBAL_HUGGINGFACE_TOKEN')
            if hf_token and hf_token.startswith('/run/secrets/'):
                try:
                    with open(hf_token, 'r') as f:
                        hf_token = f.read().strip()
                    logger.debug("✅ HuggingFace token read from secrets file")
                except Exception as e:
                    logger.warning(f"⚠️ Could not read HuggingFace token from {hf_token}: {e}")
                    hf_token = None
            
            # Build standardized configuration structure
            config = {
                # Model names (Phase 3d standardized variables)
                'depression_model': models.get('depression', {}).get('name') or self.unified_config.get_env('NLP_MODEL_DEPRESSION_NAME'),
                'sentiment_model': models.get('sentiment', {}).get('name') or self.unified_config.get_env('NLP_MODEL_SENTIMENT_NAME'),
                'emotional_distress_model': models.get('emotional_distress', {}).get('name') or self.unified_config.get_env('NLP_MODEL_DISTRESS_NAME'),
                
                # Model weights (Phase 3d standardized variables)
                'depression_weight': models.get('depression', {}).get('weight', self.unified_config.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4)),
                'sentiment_weight': models.get('sentiment', {}).get('weight', self.unified_config.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3)),
                'emotional_distress_weight': models.get('emotional_distress', {}).get('weight', self.unified_config.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3)),
                
                # Storage and authentication
                'cache_dir': cache_dir,
                'huggingface_token': hf_token,
                
                # Ensemble configuration
                'ensemble_mode': ensemble_mode,
                'gap_detection_enabled': gap_detection_config.get('enabled', self.unified_config.get_env_bool('NLP_ENSEMBLE_GAP_DETECTION_ENABLED', True)),
                'disagreement_threshold': gap_detection_config.get('disagreement_threshold', self.unified_config.get_env_int('NLP_ENSEMBLE_DISAGREEMENT_THRESHOLD', 2))
            }
            
            logger.info("✅ Model configuration extracted from UnifiedConfigManager")
            return config
            
        except Exception as e:
            logger.error(f"❌ Error extracting model configuration: {e}")
            return self._get_fallback_model_config()
    
    def _extract_hardware_config_from_unified_manager(self) -> Dict[str, Any]:
        """Extract hardware configuration from UnifiedConfigManager (Phase 3d Step 9)"""
        logger.debug("🔍 Extracting hardware configuration from UnifiedConfigManager...")
        
        try:
            # Get hardware configuration using unified config
            hardware_config = self.unified_config.get_hardware_configuration()
            
            # Extract with fallbacks using unified config (NO MORE os.getenv calls)
            config = {
                'device': hardware_config.get('device') or self.unified_config.get_env('NLP_MODEL_DEVICE', 'auto'),
                'precision': hardware_config.get('precision') or self.unified_config.get_env('NLP_MODEL_PRECISION', 'float16'),
                'max_batch_size': hardware_config.get('max_batch_size') or self.unified_config.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
                'inference_threads': hardware_config.get('inference_threads') or self.unified_config.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16)
            }
            
            logger.info("✅ Hardware configuration extracted from UnifiedConfigManager")
            return config
            
        except Exception as e:
            logger.error(f"❌ Error extracting hardware configuration: {e}")
            return self._get_fallback_hardware_config()
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Fallback model configuration using UnifiedConfigManager (Phase 3d Step 9)"""
        logger.warning("⚠️ Using fallback model configuration with UnifiedConfigManager")
        
        return {
            # Use Phase 3d standardized variable names
            'depression_model': self.unified_config.get_env('NLP_MODEL_DEPRESSION_NAME', 'martin-ha/toxic-comment-model'),
            'sentiment_model': self.unified_config.get_env('NLP_MODEL_SENTIMENT_NAME', 'cardiffnlp/twitter-roberta-base-sentiment-latest'),
            'emotional_distress_model': self.unified_config.get_env('NLP_MODEL_DISTRESS_NAME', 'j-hartmann/emotion-english-distilroberta-base'),
            
            'depression_weight': self.unified_config.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
            'sentiment_weight': self.unified_config.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
            'emotional_distress_weight': self.unified_config.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
            
            'cache_dir': self.unified_config.get_env('NLP_STORAGE_MODELS_DIR', './models/cache'),
            'huggingface_token': self.unified_config.get_env('GLOBAL_HUGGINGFACE_TOKEN'),
            'ensemble_mode': self.unified_config.get_env('NLP_ENSEMBLE_MODE', 'majority'),
            'gap_detection_enabled': self.unified_config.get_env_bool('NLP_ENSEMBLE_GAP_DETECTION_ENABLED', True),
            'disagreement_threshold': self.unified_config.get_env_int('NLP_ENSEMBLE_DISAGREEMENT_THRESHOLD', 2)
        }
    
    def _get_fallback_hardware_config(self) -> Dict[str, Any]:
        """Fallback hardware configuration using UnifiedConfigManager (Phase 3d Step 9)"""
        logger.warning("⚠️ Using fallback hardware configuration with UnifiedConfigManager")
        
        return {
            'device': self.unified_config.get_env('NLP_MODEL_DEVICE', 'auto'),
            'precision': self.unified_config.get_env('NLP_MODEL_PRECISION', 'float16'),
            'max_batch_size': self.unified_config.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
            'inference_threads': self.unified_config.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16)
        }
    
    def _configure_device(self) -> str:
        """Configure device for model inference"""
        device_config = self.hardware_config.get('device', 'auto')
        
        if device_config == 'auto':
            if torch.cuda.is_available():
                device = 'cuda'
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"🎮 Using GPU: {gpu_name}")
            else:
                device = 'cpu'
                logger.info("💻 Using CPU (CUDA not available)")
        else:
            device = device_config
            logger.info(f"🔧 Using configured device: {device}")
        
        return device
    
    def _setup_cache_directory(self):
        """Set up model cache directory"""
        cache_dir = self.model_config.get('cache_dir', './models/cache')
        cache_path = Path(cache_dir)
        
        try:
            cache_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Model cache directory ready: {cache_path}")
        except Exception as e:
            logger.warning(f"⚠️ Could not create cache directory {cache_path}: {e}")
    
    # ========================================================================
    # MODEL LOADING METHODS
    # ========================================================================
    
    async def load_models(self):
        """Load all three models in the ensemble"""
        logger.info("🔄 Loading three zero-shot model ensemble...")
        
        try:
            # Load models
            await self._load_depression_model()
            await self._load_sentiment_model()
            await self._load_emotional_distress_model()
            
            if self.models_loaded():
                logger.info("✅ All three models loaded successfully")
                return True
            else:
                logger.error("❌ Failed to load all models")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            return False
    
    async def _load_depression_model(self):
        """Load depression detection model"""
        model_name = self.model_config.get('depression_model')
        if not model_name:
            logger.error("❌ Depression model name not configured")
            return
        
        try:
            logger.info(f"🔄 Loading depression model: {model_name}")
            
            cache_dir = self.model_config.get('cache_dir')
            token = self.model_config.get('huggingface_token')
            
            self.depression_tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                use_auth_token=token
            )
            
            self.depression_model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                use_auth_token=token,
                torch_dtype=torch.float16 if self.hardware_config.get('precision') == 'float16' else torch.float32
            ).to(self.device)
            
            logger.info("✅ Depression model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load depression model: {e}")
    
    async def _load_sentiment_model(self):
        """Load sentiment analysis model"""
        model_name = self.model_config.get('sentiment_model')
        if not model_name:
            logger.error("❌ Sentiment model name not configured")
            return
        
        try:
            logger.info(f"🔄 Loading sentiment model: {model_name}")
            
            cache_dir = self.model_config.get('cache_dir')
            token = self.model_config.get('huggingface_token')
            
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                use_auth_token=token
            )
            
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                use_auth_token=token,
                torch_dtype=torch.float16 if self.hardware_config.get('precision') == 'float16' else torch.float32
            ).to(self.device)
            
            logger.info("✅ Sentiment model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load sentiment model: {e}")
    
    async def _load_emotional_distress_model(self):
        """Load emotional distress detection model"""
        model_name = self.model_config.get('emotional_distress_model')
        if not model_name:
            logger.error("❌ Emotional distress model name not configured")
            return
        
        try:
            logger.info(f"🔄 Loading emotional distress model: {model_name}")
            
            cache_dir = self.model_config.get('cache_dir')
            token = self.model_config.get('huggingface_token')
            
            self.emotional_distress_tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                use_auth_token=token
            )
            
            self.emotional_distress_model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                use_auth_token=token,
                torch_dtype=torch.float16 if self.hardware_config.get('precision') == 'float16' else torch.float32
            ).to(self.device)
            
            logger.info("✅ Emotional distress model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load emotional distress model: {e}")
    
    # ========================================================================
    # MODEL ACCESS METHODS
    # ========================================================================
    
    def models_loaded(self) -> bool:
        """Check if all models are loaded"""
        return (
            self.depression_model is not None and
            self.sentiment_model is not None and
            self.emotional_distress_model is not None
        )
    
    def get_depression_model(self):
        """Get depression detection model"""
        return self.depression_model, self.depression_tokenizer
    
    def get_sentiment_model(self):
        """Get sentiment analysis model"""
        return self.sentiment_model, self.sentiment_tokenizer
    
    def get_emotional_distress_model(self):
        """Get emotional distress detection model"""
        return self.emotional_distress_model, self.emotional_distress_tokenizer
    
    def get_all_models(self) -> Dict[str, Any]:
        """Get all models and tokenizers"""
        return {
            'depression': {
                'model': self.depression_model,
                'tokenizer': self.depression_tokenizer,
                'weight': self.model_config.get('depression_weight', 0.4)
            },
            'sentiment': {
                'model': self.sentiment_model,
                'tokenizer': self.sentiment_tokenizer,
                'weight': self.model_config.get('sentiment_weight', 0.3)
            },
            'emotional_distress': {
                'model': self.emotional_distress_model,
                'tokenizer': self.emotional_distress_tokenizer,
                'weight': self.model_config.get('emotional_distress_weight', 0.3)
            }
        }
    
    def get_ensemble_mode(self) -> str:
        """Get current ensemble mode"""
        return self.model_config.get('ensemble_mode', 'majority')
    
    def get_model_weights(self) -> Dict[str, float]:
        """Get model weights for ensemble calculation"""
        return {
            'depression': self.model_config.get('depression_weight', 0.4),
            'sentiment': self.model_config.get('sentiment_weight', 0.3),
            'emotional_distress': self.model_config.get('emotional_distress_weight', 0.3)
        }
    
    def validate_model_weights(self) -> Dict[str, Any]:
        """Validate that model weights sum to approximately 1.0"""
        weights = self.get_model_weights()
        total_weight = sum(weights.values())
        tolerance = 0.1  # Allow 10% tolerance
        
        is_valid = abs(total_weight - 1.0) <= tolerance
        
        return {
            'valid': is_valid,
            'total_weight': total_weight,
            'tolerance': tolerance,
            'weights': weights,
            'message': 'Valid' if is_valid else f'Weights sum to {total_weight}, expected ~1.0'
        }
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all models"""
        return {
            'models_loaded': self.models_loaded(),
            'device': self.device,
            'precision': self.hardware_config.get('precision'),
            'ensemble_mode': self.model_config.get('ensemble_mode'),
            'models': {
                'depression': {
                    'name': self.model_config.get('depression_model', 'Unknown'),
                    'loaded': self.depression_model is not None,
                    'purpose': 'Primary crisis classification',
                    'weight': self.model_config.get('depression_weight', 0.5)
                },
                'sentiment': {
                    'name': self.model_config.get('sentiment_model', 'Unknown'),
                    'loaded': self.sentiment_model is not None,
                    'purpose': 'Contextual validation',
                    'weight': self.model_config.get('sentiment_weight', 0.2)
                },
                'emotional_distress': {
                    'name': self.model_config.get('emotional_distress_model', 'Unknown'),
                    'loaded': self.emotional_distress_model is not None,
                    'purpose': 'Emotional distress detection',
                    'weight': self.model_config.get('emotional_distress_weight', 0.3)
                }
            },
            'gap_detection': {
                'enabled': self.model_config.get('gap_detection_enabled', True),
                'disagreement_threshold': self.model_config.get('disagreement_threshold', 2)
            }
        }

    def get_model_status(self) -> Dict[str, Any]:
        """Get model status information - NOT async"""
        return {
            'models_loaded': self.models_loaded(),
            'device': self.device,
            'precision': self.hardware_config.get('precision'),
            'ensemble_mode': self.model_config.get('ensemble_mode'),
            'models': {
                'depression': {
                    'name': self.model_config.get('depression_model', 'Unknown'),
                    'loaded': self.depression_model is not None,
                    'purpose': 'Primary crisis classification',
                    'weight': self.model_config.get('depression_weight', 0.5)
                },
                'sentiment': {
                    'name': self.model_config.get('sentiment_model', 'Unknown'),
                    'loaded': self.sentiment_model is not None,
                    'purpose': 'Contextual validation',
                    'weight': self.model_config.get('sentiment_weight', 0.2)
                },
                'emotional_distress': {
                    'name': self.model_config.get('emotional_distress_model', 'Unknown'),
                    'loaded': self.emotional_distress_model is not None,
                    'purpose': 'Emotional distress detection',
                    'weight': self.model_config.get('emotional_distress_weight', 0.3)
                }
            },
            'gap_detection': {
                'enabled': self.model_config.get('gap_detection_enabled', True),
                'disagreement_threshold': self.model_config.get('disagreement_threshold', 2)
            }
        }

# ============================================================================
# FACTORY FUNCTION FOR CLEAN ARCHITECTURE
# ============================================================================

def create_models_manager(unified_config_manager, settings_manager=None, zero_shot_manager=None):
    """
    Factory function to create ModelsManager instance with clean architecture
    Phase 3d Step 9: Updated to use UnifiedConfigManager
    
    Args:
        unified_config_manager: UnifiedConfigManager instance (required)
        settings_manager: SettingsManager instance (optional)
        zero_shot_manager: ZeroShotManager instance (optional)
        
    Returns:
        ModelsManager instance
    """
    return ModelsManager(unified_config_manager, settings_manager, zero_shot_manager)

# Export for clean architecture
__all__ = [
    'ModelsManager',
    'create_models_manager'
]