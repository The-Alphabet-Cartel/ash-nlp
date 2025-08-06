"""
Enhanced ML Model Management for Ash NLP Service v3.1 - Manager Architecture
Phase 2 Migration: models/ml_models.py → managers/models_manager.py

FIXED VERSION: Robust cache directory handling with multiple fallbacks
"""

import logging
logger = logging.getLogger(__name__)

import os
import torch

logger.info(f"🔍 About to import transformers - working directory: {os.getcwd()}")
logger.info(f"🔍 Temp directory permissions: {os.access('/tmp', os.W_OK)}")
logger.info(f"🔍 Current user: {os.getuid() if hasattr(os, 'getuid') else 'unknown'}")
from transformers import pipeline, AutoConfig
from typing import Optional, Dict, Any, Union, List, Tuple
from pathlib import Path


class ModelsManager:
    """
    Enhanced centralized management of ML models with Three Zero-Shot Model Ensemble support
    
    FIXED: Robust cache directory handling and configuration extraction
    """
    
    def __init__(self, config_manager, settings_manager=None, zero_shot_manager=None):
        """
        Initialize ModelsManager with clean architecture
        
        Args:
            config_manager: ConfigManager instance (required)
            settings_manager: SettingsManager instance (optional)
            zero_shot_manager: ZeroShotManager instance (optional)
        """
        logger.debug("🔧 Initializing ModelsManager with clean v3.1 architecture...")
        
        self.config_manager = config_manager
        self.settings_manager = settings_manager
        self.zero_shot_manager = zero_shot_manager
        
        # Extract configurations from managers
        try:
            self.model_config = self._extract_model_config_from_manager(config_manager)
            self.hardware_config = self._extract_hardware_config_from_manager(config_manager)
            
            logger.debug(f"ModelsManager model_config keys: {list(self.model_config.keys())}")
            logger.debug(f"ModelsManager hardware_config keys: {list(self.hardware_config.keys())}")
            
        except Exception as e:
            logger.error(f"Failed to extract configuration from managers: {e}")
            raise ValueError(f"ModelsManager initialization failed: {e}")
        
        # CRITICAL: Set up Hugging Face authentication IMMEDIATELY after config extraction
        self._setup_huggingface_auth()
        
        # Model instances - THREE MODELS
        self.depression_model = None
        self.sentiment_model = None
        self.emotional_distress_model = None
        self._models_loaded = False
        
        # Device configuration
        self.device = self._configure_device()
        
        # Set up model cache directory (with robust fallback handling)
        self._setup_cache_directory()
        
        logger.info("✅ ModelsManager initialized with Three Zero-Shot Model Ensemble")
        logger.debug(f"Device: {self.device}")
        logger.debug(f"Model cache directory: {self.model_config.get('cache_dir', 'not set')}")
        logger.debug(f"HuggingFace token available: {bool(self.model_config.get('huggingface_token'))}")
    
    def _extract_model_config_from_manager(self, config_manager) -> Dict[str, Any]:
        """Extract model configuration from existing ConfigManager (compatibility)"""
        logger.debug("🔍 Extracting model configuration from ConfigManager...")
        
        try:
            # Try to get configuration from the existing manager's methods
            full_model_config = config_manager.get_model_configuration()
            hardware_config = config_manager.get_hardware_configuration()
            
            logger.debug(f"🔍 Full model config structure: {list(full_model_config.keys())}")
            
            # Extract models from the nested structure
            models = full_model_config.get('models', {})
            logger.debug(f"🔍 Models found: {list(models.keys())}")
            
            # Get cache_dir from multiple possible locations
            cache_dir = (
                hardware_config.get('cache_dir') or 
                full_model_config.get('hardware_config', {}).get('cache_dir') or
                full_model_config.get('cache_dir') or 
                os.getenv('NLP_MODEL_CACHE_DIR') or
                os.getenv('NLP_HUGGINGFACE_CACHE_DIR') or
                './models/cache'
            )
            
            # Extract ensemble mode from nested structure
            ensemble_mode = (
                full_model_config.get('ensemble_config', {}).get('mode') or
                config_manager.get_ensemble_mode() or
                'majority'
            )
            
            # Extract gap detection settings
            gap_detection_config = full_model_config.get('ensemble_config', {}).get('gap_detection', {})
            
            # FIXED: Properly read HuggingFace token from file or environment
            hf_token = self._get_huggingface_token()
            
            config = {
                # Flatten the models structure
                'depression_model': models.get('depression', {}).get('name', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                'sentiment_model': models.get('sentiment', {}).get('name', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                'emotional_distress_model': models.get('emotional_distress', {}).get('name', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                'cache_dir': cache_dir,
                'huggingface_token': hf_token,
                'ensemble_mode': ensemble_mode,
                'depression_weight': models.get('depression', {}).get('weight', 0.5),
                'sentiment_weight': models.get('sentiment', {}).get('weight', 0.2),
                'emotional_distress_weight': models.get('emotional_distress', {}).get('weight', 0.3),
                'gap_detection_enabled': gap_detection_config.get('enabled', True),
                'disagreement_threshold': gap_detection_config.get('disagreement_threshold', 2)
            }
            
            logger.debug(f"✅ Extracted model config:")
            logger.debug(f"   depression_model: {config['depression_model']}")
            logger.debug(f"   sentiment_model: {config['sentiment_model']}")
            logger.debug(f"   emotional_distress_model: {config['emotional_distress_model']}")
            logger.debug(f"   cache_dir: {config['cache_dir']}")
            logger.debug(f"   ensemble_mode: {config['ensemble_mode']}")
            logger.debug(f"   huggingface_token: {'***PRESENT***' if hf_token else 'NOT FOUND'}")
            
            return config
            
        except Exception as e:
            logger.warning(f"Could not extract model config from manager: {e}")
            logger.debug("🔄 Falling back to environment variables")
            
            # Fallback to environment variables
            hf_token = self._get_huggingface_token()
            
            return {
                'depression_model': os.getenv('NLP_DEPRESSION_MODEL', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                'sentiment_model': os.getenv('NLP_SENTIMENT_MODEL', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                'emotional_distress_model': os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                'cache_dir': os.getenv('NLP_MODEL_CACHE_DIR') or os.getenv('NLP_HUGGINGFACE_CACHE_DIR') or './models/cache',
                'huggingface_token': hf_token,
                'ensemble_mode': os.getenv('NLP_ENSEMBLE_MODE', 'majority'),
                'depression_weight': float(os.getenv('NLP_DEPRESSION_MODEL_WEIGHT', '0.5')),
                'sentiment_weight': float(os.getenv('NLP_SENTIMENT_MODEL_WEIGHT', '0.2')),
                'emotional_distress_weight': float(os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', '0.3')),
                'gap_detection_enabled': os.getenv('NLP_GAP_DETECTION_ENABLED', 'true').lower() == 'true',
                'disagreement_threshold': int(os.getenv('NLP_DISAGREEMENT_THRESHOLD', '2'))
            }
    
    def _get_huggingface_token(self) -> Optional[str]:
        """
        Get HuggingFace token from environment variable or secret file
        
        Returns:
            str: The actual token content, or None if not found
        """
        # Check environment variable first
        token_path_or_value = os.getenv('GLOBAL_HUGGINGFACE_TOKEN')
        
        if not token_path_or_value:
            logger.debug("No GLOBAL_HUGGINGFACE_TOKEN environment variable found")
            return None
        
        # Check if it's a file path (Docker secret)
        if token_path_or_value.startswith('/') and os.path.isfile(token_path_or_value):
            logger.debug(f"Reading HuggingFace token from secret file: {token_path_or_value}")
            try:
                with open(token_path_or_value, 'r') as f:
                    token = f.read().strip()
                
                if token:
                    logger.debug(f"✅ Token loaded from file: {token[:10]}... (length: {len(token)})")
                    return token
                else:
                    logger.warning(f"⚠️ Secret file {token_path_or_value} is empty")
                    return None
                    
            except Exception as e:
                logger.error(f"❌ Failed to read token from secret file {token_path_or_value}: {e}")
                return None
        
        # Check if it looks like a token (starts with hf_)
        elif token_path_or_value.startswith('hf_'):
            logger.debug("Using HuggingFace token from environment variable")
            return token_path_or_value
        
        else:
            logger.warning(f"⚠️ GLOBAL_HUGGINGFACE_TOKEN doesn't look like a token or valid file path: {token_path_or_value[:20]}...")
            return None

    def _extract_hardware_config_from_manager(self, config_manager) -> Dict[str, Any]:
        """Extract hardware configuration from existing ConfigManager (compatibility)"""
        logger.debug("🔍 Extracting hardware configuration from ConfigManager...")
        
        try:
            # Try to get configuration from the existing manager's methods
            full_config = config_manager.get_hardware_configuration()
            
            logger.debug(f"🔍 Hardware config structure: {list(full_config.keys())}")
            
            # Handle nested hardware config structure
            hardware_config = full_config.get('hardware_config', full_config)
            
            config = {
                'device': hardware_config.get('device', 'auto'),
                'precision': hardware_config.get('precision', 'float16'),
                'max_batch_size': hardware_config.get('max_batch_size') or hardware_config.get('performance_settings', {}).get('max_batch_size', 32),
                'use_fast_tokenizer': hardware_config.get('use_fast_tokenizer', True),
                'trust_remote_code': hardware_config.get('trust_remote_code', False),
                'model_revision': hardware_config.get('model_revision', 'main')
            }
            
            logger.debug(f"✅ Extracted hardware config:")
            logger.debug(f"   device: {config['device']}")
            logger.debug(f"   precision: {config['precision']}")
            logger.debug(f"   max_batch_size: {config['max_batch_size']}")
            
            return config
            
        except Exception as e:
            logger.warning(f"Could not extract hardware config from manager: {e}")
            logger.debug("🔄 Falling back to environment variables")
            
            # Fallback to environment variables
            return {
                'device': os.getenv('NLP_DEVICE', 'auto'),
                'precision': os.getenv('NLP_MODEL_PRECISION', 'float16'),
                'max_batch_size': int(os.getenv('NLP_MAX_BATCH_SIZE', '32')),
                'use_fast_tokenizer': os.getenv('NLP_MODEL_USE_FAST_TOKENIZER', 'true').lower() == 'true',
                'trust_remote_code': os.getenv('NLP_MODEL_TRUST_REMOTE_CODE', 'false').lower() == 'true',
                'model_revision': os.getenv('NLP_MODEL_REVISION', 'main')
            }
    
    def _configure_device(self) -> str:
        """Configure the compute device based on hardware configuration"""
        device_config = self.hardware_config.get('device', 'auto')
        
        if device_config == 'auto':
            if torch.cuda.is_available():
                device = 'cuda'
                logger.info(f"🔥 GPU detected: {torch.cuda.get_device_name()}")
            else:
                device = 'cpu'
                logger.info("💻 Using CPU (CUDA not available)")
        else:
            device = device_config
            logger.info(f"🎯 Using specified device: {device}")
        
        return device
    
    def _setup_cache_directory(self):
        """Set up model cache directory with robust fallback handling"""
        logger.debug("🔧 Setting up model cache directory...")
        
        # Try multiple sources for cache_dir with comprehensive fallbacks
        cache_dir_str = (
            self.model_config.get('cache_dir') or 
            self.hardware_config.get('cache_dir') or 
            os.getenv('NLP_MODEL_CACHE_DIR') or 
            os.getenv('NLP_HUGGINGFACE_CACHE_DIR') or 
            './models/cache'
        )
        
        logger.debug(f"Using cache directory: {cache_dir_str}")
        
        cache_dir = Path(cache_dir_str)
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure the model_config has cache_dir for later use
        if 'cache_dir' not in self.model_config:
            self.model_config['cache_dir'] = str(cache_dir)
        
        logger.debug(f"✅ Model cache directory ready: {cache_dir}")
    
    def _setup_huggingface_auth(self):
        """Set up Hugging Face authentication with multiple environment variable names"""
        hf_token = self.model_config.get('huggingface_token')
        if hf_token:
            # Set multiple environment variable names that different libraries may check
            os.environ['HF_TOKEN'] = hf_token
            os.environ['HUGGING_FACE_HUB_TOKEN'] = hf_token  # Alternative name
            os.environ['HUGGINGFACE_HUB_TOKEN'] = hf_token   # Another alternative
            os.environ['HF_HOME'] = self.model_config.get('cache_dir', './models/cache')
            
            logger.info("🔑 Hugging Face authentication configured with multiple token variables")
            logger.debug(f"Token variables set: HF_TOKEN, HUGGING_FACE_HUB_TOKEN, HUGGINGFACE_HUB_TOKEN")
            logger.debug(f"HF_HOME set to: {os.environ['HF_HOME']}")
        else:
            logger.warning("⚠️ No Hugging Face token provided - this may cause authentication errors")
    
    def _get_model_kwargs(self) -> Dict[str, Any]:
        """Get arguments for pipeline creation"""
        return {
            'device': self.device,
            'torch_dtype': self._get_torch_dtype(),
            'return_all_scores': True,
            'batch_size': self.hardware_config.get('max_batch_size', 32),
        }
    
    def _get_model_loading_kwargs(self) -> Dict[str, Any]:
        """Get arguments for model/tokenizer loading with token authentication"""
        kwargs = {
            'cache_dir': self.model_config['cache_dir'],
            'use_fast': self.hardware_config.get('use_fast_tokenizer', True),
            'trust_remote_code': self.hardware_config.get('trust_remote_code', False),
            'revision': self.hardware_config.get('model_revision', 'main'),
        }
        
        # Add token directly to loading kwargs as fallback
        hf_token = self.model_config.get('huggingface_token')
        if hf_token:
            kwargs['token'] = hf_token
            logger.debug("🔑 Added HuggingFace token directly to model loading kwargs")
        
        return kwargs
    
    def _get_torch_dtype(self):
        """Get torch dtype based on precision setting"""
        precision = self.hardware_config.get('precision', 'float16').lower()
        
        if precision == 'float16':
            return torch.float16
        elif precision == 'bfloat16':
            return torch.bfloat16
        elif precision == 'float32':
            return torch.float32
        else:
            logger.warning(f"Unknown precision '{precision}', using float32")
            return torch.float32
    
    async def initialize(self):
        """
        Initialize the ModelsManager by loading all models
        
        This method loads all three models required for the ensemble analysis.
        """
        logger.info("🚀 Initializing ModelsManager - Loading Three Zero-Shot Model Ensemble...")
        
        try:
            await self.load_models()
            
            if self.models_loaded():
                logger.info("✅ ModelsManager initialization complete - All models loaded")
            else:
                logger.error("❌ ModelsManager initialization failed - Models not loaded")
                raise RuntimeError("ModelsManager initialization failed - models not loaded")
                
        except Exception as e:
            logger.error(f"❌ ModelsManager initialization failed: {e}")
            raise

    async def load_models(self):
        """
        Load all three models for the ensemble analysis
        
        This method loads all models using the proper arguments structure.
        """
        logger.info("📦 Loading Three Zero-Shot Model Ensemble...")
        
        try:
            # Get the arguments that the model loading methods expect
            model_kwargs = self._get_model_kwargs()
            loading_kwargs = self._get_model_loading_kwargs()
            
            # Load all three models with proper arguments
            await self._load_depression_model(model_kwargs, loading_kwargs)
            await self._load_sentiment_model(model_kwargs, loading_kwargs)  
            await self._load_emotional_distress_model(model_kwargs, loading_kwargs)
            
            self._models_loaded = True
            logger.info("✅ All three models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            self._models_loaded = False
            raise

    def get_ensemble_status(self) -> Dict[str, Any]:
        """Get ensemble status information"""
        return {
            'models_loaded': self.models_loaded(),
            'device': self.device,
            'precision': self.hardware_config.get('precision'),
            'ensemble_mode': self.model_config.get('ensemble_mode'),
            'model_count': 3,
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

    def get_configuration_status(self) -> Dict[str, Any]:
        """Get configuration status"""
        return {
            'models_initialized': self.models_loaded(),
            'status': 'operational' if self.models_loaded() else 'loading'
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'total_models': 3,
            'status': 'operational' if self.models_loaded() else 'loading'
        }

    async def _load_depression_model(self, model_kwargs: Dict, loading_kwargs: Dict):
        """Load the depression detection model"""
        model_name = self.model_config.get('depression_model', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0')
        logger.info(f"📦 Loading Depression Model: {model_name}")
        
        try:
            # Ensure authentication is set up before loading
            self._setup_huggingface_auth()
            
            self.depression_model = pipeline(
                "zero-shot-classification",
                model=model_name,
                **model_kwargs,
                **loading_kwargs
            )
            logger.info("✅ Depression model loaded successfully")
            logger.debug(f"   Model: {model_name}")
            logger.debug(f"   Purpose: Primary crisis classification")
            
        except Exception as e:
            logger.error(f"❌ Failed to load depression model: {e}")
            if "401" in str(e) or "Unauthorized" in str(e):
                logger.error("🔑 Authentication error - check HuggingFace token")
                logger.error(f"Token present: {bool(self.model_config.get('huggingface_token'))}")
            raise

    async def _load_sentiment_model(self, model_kwargs: Dict, loading_kwargs: Dict):
        """Load the sentiment analysis model"""
        model_name = self.model_config.get('sentiment_model', 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli')
        logger.info(f"📦 Loading Sentiment Model: {model_name}")
        
        try:
            # Ensure authentication is set up before loading
            self._setup_huggingface_auth()
            
            self.sentiment_model = pipeline(
                "zero-shot-classification",
                model=model_name,
                **model_kwargs,
                **loading_kwargs
            )
            logger.info("✅ Sentiment model loaded successfully")
            logger.debug(f"   Model: {model_name}")
            logger.debug(f"   Purpose: Contextual validation")
            
        except Exception as e:
            logger.error(f"❌ Failed to load sentiment model: {e}")
            if "401" in str(e) or "Unauthorized" in str(e):
                logger.error("🔑 Authentication error - check HuggingFace token")
                logger.error(f"Token present: {bool(self.model_config.get('huggingface_token'))}")
            raise

    async def _load_emotional_distress_model(self, model_kwargs: Dict, loading_kwargs: Dict):
        """Load the emotional distress detection model"""
        model_name = self.model_config.get('emotional_distress_model', 'Lowerated/lm6-deberta-v3-topic-sentiment')
        logger.info(f"📦 Loading Emotional Distress Model: {model_name}")
        
        try:
            # Ensure authentication is set up before loading
            self._setup_huggingface_auth()
            
            self.emotional_distress_model = pipeline(
                "zero-shot-classification",
                model=model_name,
                **model_kwargs,
                **loading_kwargs
            )
            logger.info("✅ Emotional distress model loaded successfully")
            logger.debug(f"   Model: {model_name}")
            logger.debug(f"   Purpose: Emotional distress detection")
            
        except Exception as e:
            logger.error(f"❌ Failed to load emotional distress model: {e}")
            if "401" in str(e) or "Unauthorized" in str(e):
                logger.error("🔑 Authentication error - check HuggingFace token")
                logger.error(f"Token present: {bool(self.model_config.get('huggingface_token'))}")
            raise
    
    def models_loaded(self) -> bool:
        """Check if all models are loaded"""
        return self._models_loaded and all([
            self.depression_model is not None,
            self.sentiment_model is not None,
            self.emotional_distress_model is not None
        ])
        
    # Model access methods
    def get_depression_model(self):
        """Get the depression detection model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.depression_model
    
    def get_sentiment_model(self):
        """Get the sentiment analysis model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.sentiment_model
    
    def get_emotional_distress_model(self):
        """Get the emotional distress detection model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.emotional_distress_model
    
    # Label mapping methods
    def get_depression_labels(self) -> List[str]:
        """Get depression model classification labels"""
        return ['crisis', 'mild_crisis', 'negative', 'neutral', 'positive']
    
    def get_sentiment_labels(self) -> List[str]:
        """Get sentiment model classification labels"""
        return ['very_negative', 'negative', 'neutral', 'positive', 'very_positive']
    
    def get_emotional_distress_labels(self) -> List[str]:
        """Get emotional distress model classification labels"""
        return ['high_distress', 'medium_distress', 'low_distress', 'minimal_distress']
    
    def _map_depression_zero_shot_label(self, label: str) -> str:
        """Map depression model labels to standardized format"""
        mapping = {
            'crisis': 'crisis',
            'mild_crisis': 'mild_crisis',
            'negative': 'negative',
            'neutral': 'neutral',
            'positive': 'positive'
        }
        return mapping.get(label.lower(), label)
    
    def _map_sentiment_zero_shot_label(self, label: str) -> str:
        """Map sentiment model labels to standardized format"""
        mapping = {
            'very_negative': 'very_negative',
            'negative': 'negative',
            'neutral': 'neutral',
            'positive': 'positive',
            'very_positive': 'very_positive'
        }
        return mapping.get(label.lower(), label)
    
    def _map_emotional_distress_zero_shot_label(self, label: str) -> str:
        """Map emotional distress model labels to standardized format"""
        mapping = {
            'high_distress': 'high_distress',
            'medium_distress': 'medium_distress',
            'low_distress': 'low_distress',
            'minimal_distress': 'minimal_distress'
        }
        return mapping.get(label.lower(), label)
    
    # Analysis methods
    def analyze_with_depression_model(self, message: str) -> List[Dict[str, Any]]:
        """Primary crisis detection using specialized depression model"""
        try:
            labels = self.get_depression_labels()
            result = self.depression_model(message, labels)
            
            formatted_result = []
            for label, score in zip(result['labels'], result['scores']):
                category = self._map_depression_zero_shot_label(label)
                formatted_result.append({
                    'label': category,
                    'score': score,
                    'model_type': 'depression_specialist',
                    'raw_label': label
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Depression model analysis failed: {e}")
            return []
    
    def analyze_with_sentiment_model(self, message: str) -> List[Dict[str, Any]]:
        """Contextual validation using sentiment analysis model"""
        try:
            labels = self.get_sentiment_labels()
            result = self.sentiment_model(message, labels)
            
            formatted_result = []
            for label, score in zip(result['labels'], result['scores']):
                category = self._map_sentiment_zero_shot_label(label)
                formatted_result.append({
                    'label': category,
                    'score': score,
                    'model_type': 'sentiment_validator',
                    'raw_label': label
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Sentiment model analysis failed: {e}")
            return []
    
    def analyze_with_emotional_distress_model(self, message: str) -> List[Dict[str, Any]]:
        """Emotional distress detection using specialized model"""
        try:
            labels = self.get_emotional_distress_labels()
            result = self.emotional_distress_model(message, labels)
            
            formatted_result = []
            for label, score in zip(result['labels'], result['scores']):
                category = self._map_emotional_distress_zero_shot_label(label)
                formatted_result.append({
                    'label': category,
                    'score': score,
                    'model_type': 'emotional_distress_detector',
                    'raw_label': label
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Emotional distress model analysis failed: {e}")
            return []
    
    async def analyze_message_ensemble(self, message: str, user_id: str, channel_id: str = None) -> Dict[str, Any]:
        """
        Three Zero-Shot Model Ensemble analysis with consensus building
        
        Returns:
            Dict containing individual model results, consensus prediction, and metadata
        """
        try:
            logger.debug(f"🎯 Starting Three Zero-Shot Model Ensemble analysis")
            
            # Run all three models
            depression_results = self.analyze_with_depression_model(message)
            sentiment_results = self.analyze_with_sentiment_model(message)
            emotional_distress_results = self.analyze_with_emotional_distress_model(message)
            
            # Extract top predictions
            depression_top = depression_results[0] if depression_results else {'label': 'unknown', 'score': 0.0}
            sentiment_top = sentiment_results[0] if sentiment_results else {'label': 'unknown', 'score': 0.0}
            emotional_distress_top = emotional_distress_results[0] if emotional_distress_results else {'label': 'unknown', 'score': 0.0}
            
            # Build consensus using configured ensemble mode
            consensus = self._build_ensemble_consensus(
                depression_top, sentiment_top, emotional_distress_top, message
            )
            
            # Detect model disagreements for gap detection
            gap_detected = self._detect_model_disagreement(
                depression_top, sentiment_top, emotional_distress_top
            )
            
            result = {
                'individual_results': {
                    'depression': depression_results,
                    'sentiment': sentiment_results,
                    'emotional_distress': emotional_distress_results
                },
                'top_predictions': {
                    'depression': depression_top,
                    'sentiment': sentiment_top,
                    'emotional_distress': emotional_distress_top
                },
                'consensus': consensus,
                'gap_detection': {
                    'gap_detected': gap_detected,
                    'requires_review': gap_detected and self.model_config.get('gap_detection_enabled', True)
                },
                'ensemble_metadata': {
                    'ensemble_mode': self.model_config.get('ensemble_mode', 'majority'),
                    'models_used': 3,
                    'all_models_responded': all([depression_results, sentiment_results, emotional_distress_results])
                }
            }
            
            logger.debug(f"✅ Ensemble analysis complete: {consensus['prediction']} ({consensus['confidence']:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ensemble analysis failed: {e}")
            logger.exception("Ensemble analysis error details:")
            return {
                'individual_results': {'depression': [], 'sentiment': [], 'emotional_distress': []},
                'consensus': {'prediction': 'error', 'confidence': 0.0, 'method': 'error_fallback'},
                'gap_detection': {'gap_detected': True, 'requires_review': True},
                'error': str(e)
            }
    
    def _build_ensemble_consensus(self, depression_pred: Dict, sentiment_pred: Dict, 
                                emotional_distress_pred: Dict, message: str) -> Dict[str, Any]:
        """Build consensus prediction from three model outputs"""
        
        ensemble_mode = self.model_config.get('ensemble_mode', 'majority')
        
        if ensemble_mode == 'weighted':
            return self._weighted_ensemble_consensus(depression_pred, sentiment_pred, emotional_distress_pred)
        elif ensemble_mode == 'consensus':
            return self._consensus_ensemble(depression_pred, sentiment_pred, emotional_distress_pred)
        else:  # Default to majority
            return self._majority_ensemble_consensus(depression_pred, sentiment_pred, emotional_distress_pred)
    
    def _majority_ensemble_consensus(self, depression_pred: Dict, sentiment_pred: Dict, 
                                   emotional_distress_pred: Dict) -> Dict[str, Any]:
        """Build majority vote consensus"""
        
        # Map predictions to crisis levels for consensus
        crisis_mappings = {
            'crisis': 'crisis',
            'mild_crisis': 'mild_crisis', 
            'high_distress': 'crisis',
            'medium_distress': 'mild_crisis',
            'very_negative': 'mild_crisis',
            'negative': 'low_risk',
            'low_distress': 'low_risk',
            'minimal_distress': 'no_risk',
            'neutral': 'no_risk',
            'positive': 'no_risk',
            'very_positive': 'no_risk'
        }
        
        # Get mapped predictions
        dep_mapped = crisis_mappings.get(depression_pred['label'], 'unknown')
        sent_mapped = crisis_mappings.get(sentiment_pred['label'], 'unknown')
        dist_mapped = crisis_mappings.get(emotional_distress_pred['label'], 'unknown')
        
        # Count votes
        votes = [dep_mapped, sent_mapped, dist_mapped]
        vote_counts = {}
        for vote in votes:
            vote_counts[vote] = vote_counts.get(vote, 0) + 1
        
        # Find majority
        max_votes = max(vote_counts.values())
        majority_predictions = [pred for pred, count in vote_counts.items() if count == max_votes]
        
        if len(majority_predictions) == 1:
            final_prediction = majority_predictions[0]
            confidence = max_votes / 3.0
        else:
            # Tie-breaker: use highest confidence prediction
            candidates = [
                (depression_pred['label'], depression_pred['score']),
                (sentiment_pred['label'], sentiment_pred['score']),
                (emotional_distress_pred['label'], emotional_distress_pred['score'])
            ]
            best_candidate = max(candidates, key=lambda x: x[1])
            final_prediction = crisis_mappings.get(best_candidate[0], 'unknown')
            confidence = best_candidate[1]
        
        return {
            'prediction': final_prediction,
            'confidence': confidence,
            'method': 'majority_vote',
            'vote_breakdown': vote_counts
        }
    
    def _weighted_ensemble_consensus(self, depression_pred: Dict, sentiment_pred: Dict, 
                                   emotional_distress_pred: Dict) -> Dict[str, Any]:
        """Build weighted ensemble consensus using model weights"""
        
        # Get model weights from configuration
        weights = {
            'depression': self.model_config.get('depression_weight', 0.5),
            'sentiment': self.model_config.get('sentiment_weight', 0.2),
            'emotional_distress': self.model_config.get('emotional_distress_weight', 0.3)
        }
        
        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v/total_weight for k, v in weights.items()}
        
        # Calculate weighted confidence scores for each outcome
        outcomes = {}
        
        # Add depression model contribution
        if depression_pred['label'] != 'unknown':
            outcomes[depression_pred['label']] = outcomes.get(depression_pred['label'], 0) + \
                                               (depression_pred['score'] * weights['depression'])
        
        # Add sentiment model contribution  
        if sentiment_pred['label'] != 'unknown':
            outcomes[sentiment_pred['label']] = outcomes.get(sentiment_pred['label'], 0) + \
                                              (sentiment_pred['score'] * weights['sentiment'])
        
        # Add emotional distress model contribution
        if emotional_distress_pred['label'] != 'unknown':
            outcomes[emotional_distress_pred['label']] = outcomes.get(emotional_distress_pred['label'], 0) + \
                                                       (emotional_distress_pred['score'] * weights['emotional_distress'])
        
        if outcomes:
            best_outcome = max(outcomes.items(), key=lambda x: x[1])
            final_prediction = best_outcome[0]
            final_confidence = min(1.0, best_outcome[1])  # Cap at 1.0
        else:
            final_prediction = 'unknown'
            final_confidence = 0.0
        
        return {
            'prediction': final_prediction,
            'confidence': final_confidence,
            'method': 'weighted_ensemble',
            'weights_used': weights,
            'outcome_scores': outcomes
        }
    
    def _consensus_ensemble(self, depression_pred: Dict, sentiment_pred: Dict, 
                          emotional_distress_pred: Dict) -> Dict[str, Any]:
        """Build consensus requiring agreement between models"""
        
        predictions = [depression_pred['label'], sentiment_pred['label'], emotional_distress_pred['label']]
        confidences = [depression_pred['score'], sentiment_pred['score'], emotional_distress_pred['score']]
        
        # Check for unanimous agreement
        if len(set(predictions)) == 1:
            final_prediction = predictions[0]
            final_confidence = sum(confidences) / len(confidences)
            agreement_level = 'unanimous'
        else:
            # Check for majority agreement (2/3)
            pred_counts = {}
            for pred, conf in zip(predictions, confidences):
                if pred not in pred_counts:
                    pred_counts[pred] = {'count': 0, 'total_confidence': 0}
                pred_counts[pred]['count'] += 1
                pred_counts[pred]['total_confidence'] += conf
            
            majority_pred = max(pred_counts.items(), key=lambda x: x[1]['count'])
            if majority_pred[1]['count'] >= 2:
                final_prediction = majority_pred[0]
                final_confidence = majority_pred[1]['total_confidence'] / majority_pred[1]['count']
                agreement_level = 'majority'
            else:
                # No consensus - use highest confidence
                best_idx = confidences.index(max(confidences))
                final_prediction = predictions[best_idx]
                final_confidence = confidences[best_idx]
                agreement_level = 'no_consensus'
        
        return {
            'prediction': final_prediction,
            'confidence': final_confidence,
            'method': 'consensus_ensemble',
            'agreement_level': agreement_level,
            'all_predictions': predictions
        }
    
    def _detect_model_disagreement(self, depression_pred: Dict, sentiment_pred: Dict, 
                                 emotional_distress_pred: Dict) -> bool:
        """Detect significant disagreement between models for gap detection"""
        
        # Map predictions to risk levels for comparison (0.0 to 1.0 scale)
        risk_levels = {
            'crisis': 1.0, 'mild_crisis': 0.75, 'high_distress': 1.0, 'medium_distress': 0.75,
            'very_negative': 0.75, 'negative': 0.5, 'low_distress': 0.25, 'minimal_distress': 0.0,
            'neutral': 0.25, 'positive': 0.0, 'very_positive': 0.0, 'unknown': 0.25
        }
        
        dep_risk = risk_levels.get(depression_pred['label'], 0.25)
        sent_risk = risk_levels.get(sentiment_pred['label'], 0.25)
        dist_risk = risk_levels.get(emotional_distress_pred['label'], 0.25)
        
        risks = [dep_risk, sent_risk, dist_risk]
        risk_range = max(risks) - min(risks)
        
        # Configure disagreement threshold (0.0-1.0 scale)
        disagreement_threshold = self.model_config.get('disagreement_threshold', 0.35)
        
        # Convert to float if it's a string (from environment variables)
        if isinstance(disagreement_threshold, str):
            try:
                disagreement_threshold = float(disagreement_threshold)
            except ValueError:
                logger.warning(f"⚠️ Invalid disagreement_threshold '{disagreement_threshold}', using default 0.35")
                disagreement_threshold = 0.35
        
        return risk_range >= disagreement_threshold
    
    def get_model_status(self) -> Dict[str, Any]:
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

# ============================================================================
# FACTORY FUNCTION FOR CLEAN ARCHITECTURE
# ============================================================================

def create_models_manager(config_manager, settings_manager=None, zero_shot_manager=None):
    """
    Factory function to create ModelsManager instance with clean architecture
    
    Args:
        config_manager: ConfigManager instance (required)
        settings_manager: SettingsManager instance (optional)
        zero_shot_manager: ZeroShotManager instance (optional)
        
    Returns:
        ModelsManager instance
    """
    return ModelsManager(config_manager, settings_manager, zero_shot_manager)

# Export for clean architecture
__all__ = [
    'ModelsManager',
    'create_models_manager'
]