"""
Enhanced ML Model Management for Ash NLP Service
Handles loading, caching, and access to ML models with full environment variable support
"""

import logging
import os
import torch
from transformers import pipeline, AutoConfig
from typing import Optional, Dict, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedModelManager:
    """Enhanced centralized management of ML models with environment variable configuration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ModelManager with optional configuration
        
        Args:
            config: Optional configuration dictionary. If None, uses environment variables.
        """
        # Load configuration from environment or passed config
        self.config = self._load_config(config)
        
        # Model instances
        self.depression_model = None
        self.sentiment_model = None
        self._models_loaded = False
        
        # Device configuration
        self.device = self._configure_device()
        
        # Set up model cache directory
        self._setup_cache_directory()
        
        # Set up Hugging Face authentication if token provided
        self._setup_huggingface_auth()
        
        logger.info(f"ModelManager initialized with device: {self.device}")
        logger.info(f"Model cache directory: {self.config['cache_dir']}")
    
    def _load_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Load configuration from environment variables or passed config"""
        
        if config:
            # Use passed configuration
            return config
        else:
            # Load from environment variables with defaults
            return {
                'depression_model': os.getenv('NLP_DEPRESSION_MODEL', 'rafalposwiata/deproberta-large-depression'),
                'sentiment_model': os.getenv('NLP_SENTIMENT_MODEL', 'cardiffnlp/twitter-roberta-base-sentiment-latest'),
                'cache_dir': os.getenv('NLP_MODEL_CACHE_DIR', './models/cache'),
                'device': os.getenv('NLP_DEVICE', 'auto'),
                'precision': os.getenv('NLP_MODEL_PRECISION', 'float16'),
                'max_batch_size': int(os.getenv('NLP_MAX_BATCH_SIZE', '32')),
                'huggingface_token': os.getenv('HUGGINGFACE_TOKEN'),
                'use_fast_tokenizer': os.getenv('USE_FAST_TOKENIZER', 'true').lower() in ('true', '1', 'yes'),
                'trust_remote_code': os.getenv('TRUST_REMOTE_CODE', 'false').lower() in ('true', '1', 'yes'),
                'model_revision': os.getenv('MODEL_REVISION', 'main'),
                'local_files_only': os.getenv('LOCAL_FILES_ONLY', 'false').lower() in ('true', '1', 'yes'),
            }
    
    def _configure_device(self) -> Union[int, str]:
        """Configure device based on environment and hardware availability"""
        
        device_config = self.config['device'].lower()
        
        if device_config == 'auto':
            # Auto-detect best available device
            if torch.cuda.is_available():
                device = 0  # Use first GPU
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"🔥 GPU detected: {gpu_name}")
                logger.info(f"CUDA version: {torch.version.cuda}")
                logger.info(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            else:
                device = -1  # Use CPU
                logger.info("💻 Using CPU for inference")
        elif device_config == 'cpu':
            device = -1
            logger.info("💻 Forced CPU usage")
        elif device_config.startswith('cuda'):
            if torch.cuda.is_available():
                if device_config == 'cuda':
                    device = 0
                else:
                    # Extract device number from 'cuda:0', 'cuda:1', etc.
                    device = int(device_config.split(':')[1])
                gpu_name = torch.cuda.get_device_name(device)
                logger.info(f"🔥 Using specified GPU {device}: {gpu_name}")
            else:
                logger.warning("⚠️ CUDA requested but not available, falling back to CPU")
                device = -1
        else:
            logger.warning(f"⚠️ Unknown device config '{device_config}', using CPU")
            device = -1
        
        return device
    
    def _setup_cache_directory(self):
        """Create model cache directory if it doesn't exist"""
        cache_path = Path(self.config['cache_dir'])
        cache_path.mkdir(parents=True, exist_ok=True)
        
        # Set environment variable for transformers cache
        os.environ['TRANSFORMERS_CACHE'] = str(cache_path)
        os.environ['HF_HOME'] = str(cache_path.parent)
        
        logger.info(f"📁 Model cache directory: {cache_path}")
    
    def _setup_huggingface_auth(self):
        """Set up Hugging Face authentication if token is provided"""
        if self.config['huggingface_token']:
            os.environ['HUGGINGFACE_TOKEN'] = self.config['huggingface_token']
            logger.info("🔑 Hugging Face authentication configured")
        else:
            logger.info("ℹ️ No Hugging Face token provided (some models may be inaccessible)")
    
    def _get_model_kwargs(self) -> Dict[str, Any]:
        """Get common model loading arguments for pipeline creation"""
        return {
            'device': self.device,
            'torch_dtype': self._get_torch_dtype(),
            # Note: Only include parameters that are valid for pipeline()
            # Other parameters like cache_dir, trust_remote_code are handled separately
        }
    
    def _get_model_loading_kwargs(self) -> Dict[str, Any]:
        """Get arguments for model/tokenizer loading (not for pipeline)"""
        return {
            'cache_dir': self.config['cache_dir'],
            'use_fast': self.config['use_fast_tokenizer'],
            'trust_remote_code': self.config['trust_remote_code'],
            'revision': self.config['model_revision'],
        }
    
    def _get_torch_dtype(self):
        """Get torch dtype based on precision setting"""
        precision = self.config['precision'].lower()
        
        if precision == 'float16':
            return torch.float16
        elif precision == 'bfloat16':
            return torch.bfloat16
        elif precision == 'float32':
            return torch.float32
        else:
            logger.warning(f"Unknown precision '{precision}', using float32")
            return torch.float32
    
    async def load_models(self):
        """Load both depression and sentiment analysis models with enhanced configuration"""
        
        logger.info("=" * 60)
        logger.info("STARTING ENHANCED MODEL LOADING PROCESS")
        logger.info("=" * 60)
        
        logger.info(f"🔧 Configuration:")
        logger.info(f"   Device: {self.device}")
        logger.info(f"   Precision: {self.config['precision']}")
        logger.info(f"   Cache Dir: {self.config['cache_dir']}")
        logger.info(f"   Max Batch Size: {self.config['max_batch_size']}")
        
        try:
            # Get model loading arguments
            model_kwargs = self._get_model_kwargs()
            loading_kwargs = self._get_model_loading_kwargs()
            
            # Load Depression Detection Model
            logger.info("🧠 Loading Depression Detection model...")
            logger.info(f"   Model: {self.config['depression_model']}")
            
            # Check if model config is accessible before loading
            try:
                dep_config = AutoConfig.from_pretrained(
                    self.config['depression_model'],
                    **loading_kwargs
                )
                logger.info(f"   Architecture: {dep_config.model_type}")
                logger.info(f"   Labels: {getattr(dep_config, 'id2label', 'Not specified')}")
            except Exception as e:
                logger.warning(f"   Could not load model config: {e}")
            
            self.depression_model = pipeline(
                "text-classification",
                model=self.config['depression_model'],
                top_k=None,
                **model_kwargs
            )
            logger.info("✅ Depression model loaded successfully!")
            
            # Load Sentiment Analysis Model  
            logger.info("💭 Loading Sentiment Analysis model...")
            logger.info(f"   Model: {self.config['sentiment_model']}")
            
            # Check sentiment model config
            try:
                sent_config = AutoConfig.from_pretrained(
                    self.config['sentiment_model'],
                    **loading_kwargs
                )
                logger.info(f"   Architecture: {sent_config.model_type}")
                logger.info(f"   Labels: {getattr(sent_config, 'id2label', 'Not specified')}")
            except Exception as e:
                logger.warning(f"   Could not load model config: {e}")
            
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model=self.config['sentiment_model'],
                top_k=None,
                **model_kwargs
            )
            logger.info("✅ Sentiment model loaded successfully!")
            
            self._models_loaded = True
            
            # Memory usage info
            if self.device != -1:  # GPU
                logger.info(f"🔥 GPU Memory Usage:")
                logger.info(f"   Allocated: {torch.cuda.memory_allocated(self.device) / 1024**3:.2f} GB")
                logger.info(f"   Cached: {torch.cuda.memory_reserved(self.device) / 1024**3:.2f} GB")
            
            # Quick functionality test
            await self._test_models()
            
            logger.info("=" * 60)
            logger.info("✅ ENHANCED MODEL LOADING COMPLETE")
            logger.info("=" * 60)
            
        except Exception as e:
            self._models_loaded = False
            logger.error(f"❌ Failed to load models: {e}")
            logger.exception("Full traceback:")
            raise
    
    async def _test_models(self):
        """Test both models with a sample message"""
        try:
            test_message = "I'm feeling really down and hopeless today"
            
            logger.info("🧪 Testing models with sample message...")
            
            # Test depression model
            dep_result = self.analyze_with_depression_model(test_message)
            if dep_result:
                # Handle different result formats - extract predictions
                predictions_to_process = []
                if isinstance(dep_result, list):
                    if len(dep_result) > 0 and isinstance(dep_result[0], list):
                        # Nested list format [[{...}, {...}]]
                        predictions_to_process = dep_result[0]
                    elif len(dep_result) > 0 and isinstance(dep_result[0], dict):
                        # Flat list format [{...}, {...}]
                        predictions_to_process = dep_result
                elif isinstance(dep_result, dict):
                    # Single result format {...}
                    predictions_to_process = [dep_result]
                
                if predictions_to_process:
                    top_dep = max(predictions_to_process, key=lambda x: x.get('score', 0))
                    logger.info(f"   Depression: {top_dep.get('label', 'unknown')} ({top_dep.get('score', 0):.3f})")
                else:
                    logger.warning("   Depression: No valid predictions found")
            
            # Test sentiment model
            sent_result = self.analyze_with_sentiment_model(test_message)
            if sent_result:
                # Handle different result formats - extract predictions
                predictions_to_process = []
                if isinstance(sent_result, list):
                    if len(sent_result) > 0 and isinstance(sent_result[0], list):
                        # Nested list format [[{...}, {...}]]
                        predictions_to_process = sent_result[0]
                    elif len(sent_result) > 0 and isinstance(sent_result[0], dict):
                        # Flat list format [{...}, {...}]
                        predictions_to_process = sent_result
                elif isinstance(sent_result, dict):
                    # Single result format {...}
                    predictions_to_process = [sent_result]
                
                if predictions_to_process:
                    top_sent = max(predictions_to_process, key=lambda x: x.get('score', 0))
                    logger.info(f"   Sentiment: {top_sent.get('label', 'unknown')} ({top_sent.get('score', 0):.3f})")
                else:
                    logger.warning("   Sentiment: No valid predictions found")
            
            logger.info("✅ Model testing completed successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Model testing failed: {e}")
            logger.exception("Full model testing traceback:")

    def models_loaded(self) -> bool:
        """Check if all models are loaded"""
        return (self._models_loaded and 
                self.depression_model is not None and 
                self.sentiment_model is not None)
    
    def get_depression_model(self):
        """Get the depression detection model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        return self.depression_model
    
    def get_sentiment_model(self):
        """Get the sentiment analysis model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        return self.sentiment_model
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get detailed status of all models"""
        status = {
            "models_loaded": self.models_loaded(),
            "depression_model": {
                "loaded": self.depression_model is not None,
                "name": self.config['depression_model'],
                "device": str(self.device),
            },
            "sentiment_model": {
                "loaded": self.sentiment_model is not None,
                "name": self.config['sentiment_model'],
                "device": str(self.device),
            },
            "configuration": {
                "device": str(self.device),
                "precision": self.config['precision'],
                "cache_dir": self.config['cache_dir'],
                "max_batch_size": self.config['max_batch_size'],
            }
        }
        
        # Add GPU info if available
        if self.device != -1 and torch.cuda.is_available():
            status["gpu_info"] = {
                "name": torch.cuda.get_device_name(self.device),
                "memory_allocated_gb": torch.cuda.memory_allocated(self.device) / 1024**3,
                "memory_cached_gb": torch.cuda.memory_reserved(self.device) / 1024**3,
                "memory_total_gb": torch.cuda.get_device_properties(self.device).total_memory / 1024**3,
            }
        
        return status
    
    def analyze_with_depression_model(self, text: str, **kwargs) -> Optional[Any]:
        """
        Analyze text with depression model
        
        Args:
            text: Text to analyze
            **kwargs: Additional arguments for the pipeline
        """
        if not self.depression_model:
            return None
        try:
            # Use configured batch size if analyzing multiple texts
            if isinstance(text, list) and len(text) > self.config['max_batch_size']:
                # Process in batches
                results = []
                for i in range(0, len(text), self.config['max_batch_size']):
                    batch = text[i:i + self.config['max_batch_size']]
                    batch_results = self.depression_model(batch, **kwargs)
                    results.extend(batch_results)
                return results
            else:
                return self.depression_model(text, **kwargs)
        except Exception as e:
            logger.error(f"Error in depression model analysis: {e}")
            return None
    
    def analyze_with_sentiment_model(self, text: str, **kwargs) -> Optional[Any]:
        """
        Analyze text with sentiment model
        
        Args:
            text: Text to analyze
            **kwargs: Additional arguments for the pipeline
        """
        if not self.sentiment_model:
            return None
        try:
            # Use configured batch size if analyzing multiple texts
            if isinstance(text, list) and len(text) > self.config['max_batch_size']:
                # Process in batches
                results = []
                for i in range(0, len(text), self.config['max_batch_size']):
                    batch = text[i:i + self.config['max_batch_size']]
                    batch_results = self.sentiment_model(batch, **kwargs)
                    results.extend(batch_results)
                return results
            else:
                return self.sentiment_model(text, **kwargs)
        except Exception as e:
            logger.error(f"Error in sentiment model analysis: {e}")
            return None
    
    def analyze_batch(self, texts: list, include_sentiment: bool = True) -> Dict[str, Any]:
        """
        Analyze a batch of texts with both models
        
        Args:
            texts: List of texts to analyze
            include_sentiment: Whether to include sentiment analysis
            
        Returns:
            Dictionary with depression and sentiment results
        """
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        
        results = {
            "depression_results": [],
            "sentiment_results": [],
            "processing_info": {
                "batch_size": len(texts),
                "max_batch_size": self.config['max_batch_size'],
                "device": str(self.device)
            }
        }
        
        try:
            # Depression analysis
            dep_results = self.analyze_with_depression_model(texts)
            if dep_results:
                results["depression_results"] = dep_results
            
            # Sentiment analysis (if requested)
            if include_sentiment:
                sent_results = self.analyze_with_sentiment_model(texts)
                if sent_results:
                    results["sentiment_results"] = sent_results
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]):
        """
        Update configuration (requires model reload)
        
        Args:
            new_config: New configuration values
        """
        self.config.update(new_config)
        logger.info("Configuration updated - models need to be reloaded")
        self._models_loaded = False
        self.depression_model = None
        self.sentiment_model = None
    
    def clear_cache(self):
        """Clear model cache to free memory"""
        if torch.cuda.is_available() and self.device != -1:
            torch.cuda.empty_cache()
            logger.info("🧹 GPU cache cleared")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage information"""
        memory_info = {}
        
        if torch.cuda.is_available() and self.device != -1:
            memory_info["gpu"] = {
                "allocated_gb": torch.cuda.memory_allocated(self.device) / 1024**3,
                "cached_gb": torch.cuda.memory_reserved(self.device) / 1024**3,
                "total_gb": torch.cuda.get_device_properties(self.device).total_memory / 1024**3,
            }
            memory_info["gpu"]["usage_percent"] = (
                memory_info["gpu"]["allocated_gb"] / memory_info["gpu"]["total_gb"] * 100
            )
        
        # Could add CPU memory info here too if needed
        import psutil
        memory_info["system"] = {
            "used_gb": psutil.virtual_memory().used / 1024**3,
            "total_gb": psutil.virtual_memory().total / 1024**3,
            "usage_percent": psutil.virtual_memory().percent
        }
        
        return memory_info


# Backward compatibility alias
ModelManager = EnhancedModelManager