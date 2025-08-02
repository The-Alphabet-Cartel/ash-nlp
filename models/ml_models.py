"""
Enhanced ML Model Management for Ash NLP Service - Three Model Architecture
Handles loading, caching, and access to ML models with JSON-based zero-shot label configuration
"""

import logging
import os
import torch
from transformers import pipeline, AutoConfig
from typing import Optional, Dict, Any, Union, List, Tuple
from pathlib import Path
from datetime import datetime
from config.env_manager import get_config

# Import JSON-based label configuration
from config.zero_shot_config import (
    get_labels_config,
    map_depression_zero_shot_label,
    map_sentiment_zero_shot_label, 
    map_distress_zero_shot_label,
    switch_label_set,
    get_current_label_set,
    reload_labels_config
)

logger = logging.getLogger(__name__)

class EnhancedModelManager:
    """Enhanced centralized management of ML models with JSON-configured Three Zero-Shot Model Ensemble"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ModelManager with optional configuration
        
        Args:
            config: Optional configuration dictionary. If None, uses environment variables.
        """
        # Load configuration from env_manager
        self.env_config = get_config()
        
        # Load configuration from environment or passed config
        self.config = self._load_config(config)
        
        # Initialize JSON-based labels configuration
        self.labels_config = get_labels_config()
        
        # Model instances - THREE MODELS NOW
        self.depression_model = None
        self.sentiment_model = None
        self.emotional_distress_model = None  # NEW: Third model
        self._models_loaded = False
        
        # Device configuration
        self.device = self._configure_device()
        
        # Set up model cache directory
        self._setup_cache_directory()
        
        # Set up Hugging Face authentication if token provided
        self._setup_huggingface_auth()
        
        logger.info(f"Enhanced ModelManager initialized with JSON-configured Three Zero-Shot Model Ensemble")
        logger.info(f"Device: {self.device}")
        logger.info(f"Model cache directory: {self.config['cache_dir']}")
        logger.info(f"Labels configuration: {self.labels_config.get_current_stats()}")
    
    def _load_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Load configuration from environment variables or passed config"""
        
        if config:
            # Use passed configuration
            return config
        else:
            # Load from environment variables with defaults - ADD THIRD MODEL CONFIG
            return {
                'depression_model': os.getenv('NLP_DEPRESSION_MODEL', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                'sentiment_model': os.getenv('NLP_SENTIMENT_MODEL', 'Lowerated/lm6-deberta-v3-topic-sentiment'),
                'emotional_distress_model': os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL', 'facebook/bart-large-mnli'),  # NEW
                'cache_dir': os.getenv('NLP_MODEL_CACHE_DIR', './models/cache'),
                'device': os.getenv('NLP_DEVICE', 'auto'),
                'precision': os.getenv('NLP_MODEL_PRECISION', 'float16'),
                'max_batch_size': int(os.getenv('NLP_MAX_BATCH_SIZE', '32')),
                'huggingface_token': os.getenv('GLOBAL_HUGGINGFACE_TOKEN'),
                'use_fast_tokenizer': os.getenv('USE_FAST_TOKENIZER', 'true').lower() in ('true', '1', 'yes'),
                'trust_remote_code': os.getenv('TRUST_REMOTE_CODE', 'false').lower() in ('true', '1', 'yes'),
                'model_revision': os.getenv('MODEL_REVISION', 'main'),
                'local_files_only': os.getenv('LOCAL_FILES_ONLY', 'false').lower() in ('true', '1', 'yes'),
                # NEW: Ensemble configuration
                'ensemble_mode': os.getenv('NLP_ENSEMBLE_MODE', 'consensus'),  # consensus, majority, weighted
                'gap_detection_threshold': float(os.getenv('NLP_GAP_DETECTION_THRESHOLD', '0.4')),
                'disagreement_threshold': float(os.getenv('NLP_DISAGREEMENT_THRESHOLD', '0.5')),
            }
    
    def _configure_device(self) -> Union[int, str]:
        """Configure device based on availability and configuration"""
        device_config = self.config['device'].lower()
        
        if device_config == 'auto':
            if torch.cuda.is_available():
                device = 0  # Use first GPU
                logger.info(f"Auto-detected device: CUDA GPU 0")
            else:
                device = -1  # Use CPU
                logger.info(f"Auto-detected device: CPU (no CUDA available)")
        elif device_config == 'cpu':
            device = -1
            logger.info(f"Configured device: CPU (forced)")
        elif device_config.startswith('cuda'):
            if torch.cuda.is_available():
                if ':' in device_config:
                    device = int(device_config.split(':')[1])
                else:
                    device = 0
                logger.info(f"Configured device: {device_config}")
            else:
                logger.warning(f"CUDA requested but not available, falling back to CPU")
                device = -1
        else:
            logger.warning(f"Unknown device config '{device_config}', using auto-detection")
            device = 0 if torch.cuda.is_available() else -1
        
        return device
    
    def _setup_cache_directory(self):
        """Ensure model cache directory exists"""
        cache_path = Path(self.config['cache_dir'])
        cache_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Model cache directory ready: {cache_path}")
    
    def _setup_huggingface_auth(self):
        """Set up Hugging Face authentication if token provided"""
        hf_token = self.config.get('huggingface_token')
        
        if hf_token and hf_token != 'None':
            # Handle Docker secrets path
            if hf_token.startswith('/run/secrets'):
                try:
                    with open(hf_token, 'r') as f:
                        actual_token = f.read().strip()
                    if actual_token:
                        os.environ['HUGGINGFACE_HUB_TOKEN'] = actual_token
                        logger.info("🔐 Hugging Face authentication configured (from secrets)")
                    else:
                        logger.warning("🔓 Hugging Face token file is empty")
                except Exception as e:
                    logger.warning(f"🔓 Could not read Hugging Face token from {hf_token}: {e}")
            else:
                # Direct token value
                os.environ['HUGGINGFACE_HUB_TOKEN'] = hf_token
                logger.info("🔐 Hugging Face authentication configured (direct token)")
        else:
            logger.info("🔓 No Hugging Face token provided (using public models only)")
    
    # =============================================================================
    # JSON-BASED LABEL METHODS - Now use centralized JSON configuration
    # =============================================================================
    
    def get_depression_labels(self) -> List[str]:
        """Get depression detection labels from JSON configuration"""
        return self.labels_config.get_depression_labels()

    def get_sentiment_labels(self) -> List[str]:
        """Get sentiment analysis labels from JSON configuration"""
        return self.labels_config.get_sentiment_labels()

    def get_emotional_distress_labels(self) -> List[str]:
        """Get emotional distress labels from JSON configuration"""
        return self.labels_config.get_emotional_distress_labels()

    # =============================================================================
    # JSON-BASED MAPPING METHODS - Now use centralized mapping functions
    # =============================================================================
    
    def _map_depression_zero_shot_label(self, long_label: str) -> str:
        """Map depression specialist labels using JSON configuration"""
        return self.labels_config.map_depression_label(long_label)

    def _map_sentiment_zero_shot_label(self, long_label: str) -> str:
        """Map sentiment specialist labels using JSON configuration"""
        return self.labels_config.map_sentiment_label(long_label)

    def _map_distress_zero_shot_label(self, long_label: str) -> str:
        """Map distress specialist labels using JSON configuration"""
        return self.labels_config.map_distress_label(long_label)

    # =============================================================================
    # JSON CONFIGURATION MANAGEMENT METHODS
    # =============================================================================
    
    def switch_label_set(self, label_set_name: str) -> bool:
        """Switch to a different label set from JSON configuration"""
        success = self.labels_config.switch_label_set(label_set_name)
        if success:
            logger.info(f"♻️ Switched labels to: {label_set_name}")
            logger.info(f"📊 New label stats: {self.labels_config.get_current_stats()}")
        return success
    
    def get_available_label_sets(self) -> List[str]:
        """Get list of available label sets from JSON configuration"""
        return self.labels_config.get_available_label_sets()
    
    def get_current_label_set_name(self) -> str:
        """Get current label set name"""
        return self.labels_config.get_current_label_set_name()
    
    def get_label_set_info(self, label_set_name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a label set (current if none specified)"""
        if label_set_name is None:
            label_set_name = self.get_current_label_set_name()
        
        info = self.labels_config.get_label_set_info(label_set_name)
        if info:
            return {
                'name': info.name,
                'description': info.description,
                'optimized_for': info.optimized_for,
                'sensitivity_level': info.sensitivity_level,
                'recommended': info.recommended,
                'label_counts': info.label_counts,
                'total_labels': sum(info.label_counts.values()) if info.label_counts else 0
            }
        return {}
    
    def get_labels_config_info(self) -> Dict[str, Any]:
        """Get comprehensive configuration information"""
        return self.labels_config.get_config_info()
    
    def reload_labels_from_json(self) -> bool:
        """Reload labels configuration from JSON file"""
        try:
            reload_labels_config()
            
            # Update our reference
            self.labels_config = get_labels_config()
            logger.info(f"♻️ Reloaded labels from JSON: {self.labels_config.get_current_stats()}")
            return True
        except Exception as e:
            logger.error(f"Failed to reload labels from JSON: {e}")
            return False
    
    def validate_current_labels(self) -> Dict[str, Any]:
        """Validate current label configuration"""
        stats = self.labels_config.get_current_stats()
        
        validation = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'stats': stats
        }
        
        # Check if we have labels for all models
        required_models = ['depression', 'sentiment', 'emotional_distress']
        current_labels = self.labels_config.get_all_labels()
        
        for model in required_models:
            if model not in current_labels:
                validation['valid'] = False
                validation['issues'].append(f"Missing labels for {model} model")
            elif len(current_labels[model]) == 0:
                validation['valid'] = False
                validation['issues'].append(f"No labels defined for {model} model")
            elif len(current_labels[model]) < 3:
                validation['warnings'].append(f"Only {len(current_labels[model])} labels for {model} model (recommend 5+)")
        
        # Check total label count
        total_labels = stats.get('total_labels', 0)
        if total_labels < 10:
            validation['warnings'].append(f"Only {total_labels} total labels (recommend 15+)")
        
        return validation
    
    def export_current_labels(self) -> Dict[str, Any]:
        """Export current label configuration for backup/sharing"""
        return {
            'exported_at': datetime.utcnow().isoformat(),
            'label_set': self.get_current_label_set_name(),
            'info': self.get_label_set_info(),
            'labels': self.labels_config.get_all_labels(),
            'stats': self.labels_config.get_current_stats(),
            'config_info': self.labels_config.get_config_info()
        }

    # =============================================================================
    # MODEL LOADING METHODS (unchanged)
    # =============================================================================
    
    def _get_model_kwargs(self) -> Dict[str, Any]:
        """Get arguments for model pipeline creation"""
        return {
            'device': self.device,
            'torch_dtype': self._get_torch_dtype(),
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
        """Load all THREE models with enhanced configuration"""
        
        logger.info("=" * 70)
        logger.info("STARTING Three Zero-Shot Model Ensemble LOADING PROCESS")
        logger.info("=" * 70)
        
        logger.info(f"🔧 Configuration:")
        logger.info(f"   Device: {self.device}")
        logger.info(f"   Precision: {self.config['precision']}")
        logger.info(f"   Cache Dir: {self.config['cache_dir']}")
        logger.info(f"   Max Batch Size: {self.config['max_batch_size']}")
        logger.info(f"   Ensemble Mode: {self.config['ensemble_mode']}")
        logger.info(f"   Current Label Set: {self.get_current_label_set_name()}")
        
        try:
            # Get model loading arguments
            model_kwargs = self._get_model_kwargs()
            loading_kwargs = self._get_model_loading_kwargs()
            
            # Load Model 1: Depression Detection
            await self._load_depression_model(model_kwargs, loading_kwargs)
            
            # Load Model 2: Sentiment Analysis  
            await self._load_sentiment_model(model_kwargs, loading_kwargs)
            
            # Load Model 3: Emotional Distress (NEW)
            await self._load_emotional_distress_model(model_kwargs, loading_kwargs)
            
            self._models_loaded = True
            
            # Memory usage info
            if self.device != -1:  # GPU
                logger.info(f"🔥 GPU Memory Usage:")
                logger.info(f"   Allocated: {torch.cuda.memory_allocated(self.device) / 1024**3:.2f} GB")
                logger.info(f"   Cached: {torch.cuda.memory_reserved(self.device) / 1024**3:.2f} GB")
            
            # Quick functionality test
            await self._test_all_models()
            
            logger.info("=" * 70)
            logger.info("✅ Three Zero-Shot Model Ensemble LOADING COMPLETE")
            logger.info("=" * 70)
            
        except Exception as e:
            self._models_loaded = False
            logger.error(f"❌ Failed to load models: {e}")
            logger.exception("Full traceback:")
            raise
    
    async def _load_depression_model(self, model_kwargs, loading_kwargs):
        """Load specialized zero-shot model for depression detection"""
        logger.info("🧠 Loading Depression-Specialized Zero-Shot model...")
        logger.info(f"   Model: {self.config['depression_model']}")
        
        try:
            dep_config = AutoConfig.from_pretrained(
                self.config['depression_model'],
                **loading_kwargs
            )
            logger.info(f"   Architecture: {dep_config.model_type}")
            logger.info(f"   Task: Mental health crisis detection")
        except Exception as e:
            logger.warning(f"   Could not load model config: {e}")
        
        self.depression_model = pipeline(
            "zero-shot-classification",
            model=self.config['depression_model'],
            **model_kwargs
        )
        logger.info("✅ Depression zero-shot model loaded successfully!")

    async def _load_sentiment_model(self, model_kwargs, loading_kwargs):
        """Load specialized zero-shot model for sentiment analysis"""
        logger.info("💭 Loading Sentiment-Specialized Zero-Shot model...")
        logger.info(f"   Model: {self.config['sentiment_model']}")
        
        try:
            sent_config = AutoConfig.from_pretrained(
                self.config['sentiment_model'],
                **loading_kwargs
            )
            logger.info(f"   Architecture: {sent_config.model_type}")
            logger.info(f"   Task: Emotional context analysis")
        except Exception as e:
            logger.warning(f"   Could not load model config: {e}")
        
        self.sentiment_model = pipeline(
            "zero-shot-classification",
            model=self.config['sentiment_model'],
            **model_kwargs
        )
        logger.info("✅ Sentiment zero-shot model loaded successfully!")

    async def _load_emotional_distress_model(self, model_kwargs, loading_kwargs):
        """Load specialized zero-shot model for emotional distress"""
        logger.info("😰 Loading Distress-Specialized Zero-Shot model...")
        logger.info(f"   Model: {self.config['emotional_distress_model']}")
        
        try:
            distress_config = AutoConfig.from_pretrained(
                self.config['emotional_distress_model'],
                **loading_kwargs
            )
            logger.info(f"   Architecture: {distress_config.model_type}")
            logger.info(f"   Task: Emotional distress validation")
        except Exception as e:
            logger.warning(f"   Could not load model config: {e}")
        
        self.emotional_distress_model = pipeline(
            "zero-shot-classification",
            model=self.config['emotional_distress_model'],
            **model_kwargs
        )
        logger.info("✅ Emotional distress zero-shot model loaded successfully!")
    
    async def _test_all_models(self):
        """Test all three models with sample messages"""
        try:
            test_messages = [
                "I'm feeling really down and hopeless today",
                "Everything is falling apart and I can't handle it anymore",
                "I'm just having a rough day but I'll be okay"
            ]
            
            logger.info("🧪 Testing all three models...")
            logger.info(f"   Using label set: {self.get_current_label_set_name()}")
            
            for i, test_message in enumerate(test_messages):
                logger.info(f"   Test {i+1}: '{test_message[:30]}...'")
                
                # Test depression model
                dep_result = self.analyze_with_depression_model(test_message)
                if dep_result:
                    predictions = self._extract_predictions(dep_result)
                    if predictions:
                        top_dep = max(predictions, key=lambda x: x.get('score', 0))
                        logger.info(f"     Depression: {top_dep.get('label', 'unknown')} ({top_dep.get('score', 0):.3f})")
                
                # Test sentiment model
                sent_result = self.analyze_with_sentiment_model(test_message)
                if sent_result:
                    predictions = self._extract_predictions(sent_result)
                    if predictions:
                        top_sent = max(predictions, key=lambda x: x.get('score', 0))
                        logger.info(f"     Sentiment: {top_sent.get('label', 'unknown')} ({top_sent.get('score', 0):.3f})")
                
                # Test emotional distress model (NEW)
                distress_result = self.analyze_with_emotional_distress_model(test_message)
                if distress_result:
                    predictions = self._extract_predictions(distress_result)
                    if predictions:
                        top_distress = max(predictions, key=lambda x: x.get('score', 0))
                        logger.info(f"     Distress: {top_distress.get('label', 'unknown')} ({top_distress.get('score', 0):.3f})")
                
                logger.info("")
            
            logger.info("✅ Three-model testing completed successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Model testing failed: {e}")
            logger.exception("Full model testing traceback:")
    
    def _extract_predictions(self, result) -> List[Dict]:
        """Helper method to extract predictions from various result formats"""
        predictions = []
        
        if isinstance(result, list):
            if len(result) > 0 and isinstance(result[0], list):
                # Nested list format [[{...}, {...}]]
                predictions = result[0]
            elif len(result) > 0 and isinstance(result[0], dict):
                # Flat list format [{...}, {...}]
                predictions = result
        elif isinstance(result, dict):
            # Single result format {...}
            predictions = [result]
        
        return predictions
    
    def models_loaded(self) -> bool:
        """Check if ALL THREE models are loaded"""
        return (self._models_loaded and 
                self.depression_model is not None and 
                self.sentiment_model is not None and 
                self.emotional_distress_model is not None)  # NEW CHECK
    
    # Model access methods
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
    
    def get_emotional_distress_model(self):  # NEW METHOD
        """Get the emotional distress detection model"""
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        return self.emotional_distress_model
    
    # Analysis methods
    def analyze_with_depression_model(self, message: str):
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
                    'raw_label': label  # Keep for debugging
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Depression specialist zero-shot failed: {e}")
            return None

    def analyze_with_sentiment_model(self, message: str):
        """Emotional context analysis using specialized sentiment model"""
        try:
            labels = self.get_sentiment_labels()
            result = self.sentiment_model(message, labels)
            
            formatted_result = []
            for label, score in zip(result['labels'], result['scores']):
                category = self._map_sentiment_zero_shot_label(label)
                formatted_result.append({
                    'label': category,
                    'score': score,
                    'model_type': 'sentiment_specialist',
                    'raw_label': label  # Keep for debugging
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Sentiment specialist zero-shot failed: {e}")
            return None

    def analyze_with_emotional_distress_model(self, message: str):
        """Distress validation using specialized distress model"""
        try:
            labels = self.get_emotional_distress_labels()
            result = self.emotional_distress_model(message, labels)
            
            formatted_result = []
            for label, score in zip(result['labels'], result['scores']):
                category = self._map_distress_zero_shot_label(label)
                formatted_result.append({
                    'label': category,
                    'score': score,
                    'model_type': 'distress_specialist',
                    'raw_label': label  # Keep for debugging
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Distress specialist zero-shot failed: {e}")
            return None

    # =============================================================================
    # ENHANCED ANALYSIS WITH LABEL CONTEXT
    # =============================================================================
    
    def analyze_with_label_context(self, message: str) -> Dict[str, Any]:
        """
        Analyze message with enhanced context about label configuration
        Useful for debugging and understanding model decisions
        """
        try:
            # Standard ensemble analysis
            ensemble_result = self.analyze_with_ensemble(message)
            
            # Add label context
            label_context = {
                'label_set_used': self.get_current_label_set_name(),
                'label_set_info': self.get_label_set_info(),
                'labels_per_model': {
                    'depression': len(self.get_depression_labels()),
                    'sentiment': len(self.get_sentiment_labels()),
                    'emotional_distress': len(self.get_emotional_distress_labels())
                }
            }
            
            # Combine results
            enhanced_result = {
                **ensemble_result,
                'label_context': label_context
            }
            
            return enhanced_result
            
        except Exception as e:
            logger.error(f"Enhanced analysis with label context failed: {e}")
            # Fallback to standard analysis
            return self.analyze_with_ensemble(message)

    def analyze_with_ensemble(self, message: str) -> Dict[str, Any]:  # NEW ENSEMBLE METHOD
        """
        Analyze message with all three models and provide ensemble results
        Returns comprehensive analysis with gap detection
        """
        try:
            results = {
                'depression': self.analyze_with_depression_model(message),
                'sentiment': self.analyze_with_sentiment_model(message),
                'emotional_distress': self.analyze_with_emotional_distress_model(message)
            }
            
            # Process results and detect gaps
            ensemble_analysis = self._process_ensemble_results(results)
            
            return ensemble_analysis
            
        except Exception as e:
            logger.error(f"Ensemble analysis failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'individual_results': {},
                'consensus': None,
                'gaps_detected': False
            }
    
    def _process_ensemble_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process results from all three models and detect gaps"""
        processed = {
            'individual_results': {},
            'confidence_scores': {},
            'predictions': {},
            'normalized_predictions': {},  # NEW: Normalized for gap detection
            'gaps_detected': False,
            'gap_details': [],
            'consensus': None,
            'ensemble_mode': self.config['ensemble_mode']
        }
        
        # Process each model's results
        for model_name, result in results.items():
            if result:
                predictions = self._extract_predictions(result)
                if predictions:
                    top_prediction = max(predictions, key=lambda x: x.get('score', 0))
                    processed['individual_results'][model_name] = predictions
                    processed['confidence_scores'][model_name] = top_prediction.get('score', 0)
                    processed['predictions'][model_name] = top_prediction.get('label', 'unknown')
                    
                    # Normalize predictions for gap detection
                    processed['normalized_predictions'][model_name] = self._normalize_prediction(
                        top_prediction.get('label', 'unknown')
                    )
        
        # Detect gaps and disagreements using normalized predictions
        if len(processed['confidence_scores']) >= 2:
            confidence_values = list(processed['confidence_scores'].values())
            confidence_spread = max(confidence_values) - min(confidence_values)
            
            # Gap detection logic with normalized predictions
            if confidence_spread > self.config['disagreement_threshold']:
                processed['gaps_detected'] = True
                processed['gap_details'].append({
                    'type': 'confidence_disagreement',
                    'spread': confidence_spread,
                    'threshold': self.config['disagreement_threshold']
                })
            
            # Check for meaningful prediction disagreements using normalized predictions
            normalized_set = set(processed['normalized_predictions'].values())
            if len(normalized_set) > 1:
                # Only flag as disagreement if it's actually meaningful
                crisis_predictions = {pred for pred in normalized_set if pred in ['crisis', 'negative']}
                safe_predictions = {pred for pred in normalized_set if pred in ['safe', 'positive']}
                
                if crisis_predictions and safe_predictions:
                    # Real disagreement: some models see crisis, others see safe
                    processed['gaps_detected'] = True
                    processed['gap_details'].append({
                        'type': 'meaningful_disagreement',
                        'crisis_models': [model for model, pred in processed['normalized_predictions'].items() 
                                        if pred in crisis_predictions],
                        'safe_models': [model for model, pred in processed['normalized_predictions'].items() 
                                      if pred in safe_predictions]
                    })
        
        # Generate consensus based on ensemble mode
        processed['consensus'] = self._generate_consensus(processed)
        
        return processed
    
    def _normalize_prediction(self, prediction: str) -> str:
        """Enhanced normalization for multi zero-shot specialist predictions"""
        pred_lower = prediction.lower()
        
        # Depression specialist predictions (highest priority for crisis)
        if pred_lower in ['severe']:
            return 'crisis'
        elif pred_lower in ['moderate']:
            return 'crisis'
        elif pred_lower in ['mild']:
            return 'mild_crisis'
        elif pred_lower in ['not depression']:
            return 'safe'
        
        # Sentiment specialist predictions (emotional context)
        elif pred_lower in ['very negative']:
            return 'crisis'
        elif pred_lower in ['negative']:
            return 'mild_crisis'  # Less severe than depression model
        elif pred_lower in ['neutral']:
            return 'neutral'
        elif pred_lower in ['positive', 'very positive']:
            return 'safe'
        
        # Distress specialist predictions (validation context)
        elif pred_lower in ['high distress']:
            return 'crisis'
        elif pred_lower in ['medium distress']:
            return 'mild_crisis'
        elif pred_lower in ['low distress']:
            return 'neutral'
        elif pred_lower in ['no distress']:
            return 'safe'
        
        return 'unknown'

    def _generate_consensus(self, processed: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consensus prediction using CONFIGURABLE model weights from env_manager"""
        if not processed['confidence_scores']:
            return None
        
        ensemble_mode = self.config['ensemble_mode']
        
        if ensemble_mode == 'consensus':
            # FIXED: Use normalized predictions instead of raw labels
            normalized_predictions = set(processed['normalized_predictions'].values())
            
            if len(normalized_predictions) == 1:
                avg_confidence = sum(processed['confidence_scores'].values()) / len(processed['confidence_scores'])
                consensus_prediction = list(normalized_predictions)[0]  # ← Use normalized
                
                return {
                    'prediction': consensus_prediction,  # ← This will be 'crisis', not 'severe'
                    'confidence': avg_confidence,
                    'method': 'unanimous_consensus'
                }
            else:
                # FIXED: When disagreeing, pick the most severe normalized prediction
                severity_order = ['safe', 'neutral', 'mild_crisis', 'crisis']
                most_severe = max(processed['normalized_predictions'].values(), 
                                key=lambda x: severity_order.index(x) if x in severity_order else 0)
                
                # Get confidence of the model that predicted the most severe
                best_model = None
                for model, pred in processed['normalized_predictions'].items():
                    if pred == most_severe:
                        best_model = model
                        break
                
                return {
                    'prediction': most_severe,  # ← Use normalized prediction
                    'confidence': processed['confidence_scores'][best_model] * 0.8,  # Reduced confidence for disagreement
                    'method': 'most_severe_normalized'
                }
        
        elif ensemble_mode == 'majority':
            # Use normalized predictions for majority vote
            prediction_votes = {}
            for model, normalized_pred in processed['normalized_predictions'].items():
                confidence = processed['confidence_scores'][model]
                if normalized_pred not in prediction_votes:
                    prediction_votes[normalized_pred] = []
                prediction_votes[normalized_pred].append(confidence)
            
            majority_prediction = max(prediction_votes, key=lambda x: len(prediction_votes[x]))
            avg_confidence = sum(prediction_votes[majority_prediction]) / len(prediction_votes[majority_prediction])
            
            return {
                'prediction': majority_prediction,
                'confidence': avg_confidence,
                'method': 'majority_vote_normalized'
            }
        
        elif ensemble_mode == 'weighted':
            # UPDATED: Load model weights from env_manager
            model_weights = {
                'depression': self.env_config.get('NLP_DEPRESSION_MODEL_WEIGHT'),
                'sentiment': self.env_config.get('NLP_SENTIMENT_MODEL_WEIGHT'),
                'emotional_distress': self.env_config.get('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT')
            }
            
            # Validate weights sum to 1.0
            total_weight = sum(model_weights.values())
            if abs(total_weight - 1.0) > 0.01:
                logger.warning(f"Model weights don't sum to 1.0 ({total_weight}), normalizing...")
                model_weights = {k: v/total_weight for k, v in model_weights.items()}
            
            logger.info(f"🎯 Using env-configured model weights: {model_weights}")
            
            # FIXED: Use normalized predictions for weighted voting
            weighted_scores = {}
            for model, normalized_pred in processed['normalized_predictions'].items():
                confidence = processed['confidence_scores'][model]
                weight = model_weights.get(model, 1.0)
                weighted_score = confidence * weight
                
                if normalized_pred not in weighted_scores:
                    weighted_scores[normalized_pred] = 0
                weighted_scores[normalized_pred] += weighted_score
            
            best_prediction = max(weighted_scores, key=weighted_scores.get)
            final_confidence = weighted_scores[best_prediction]
            
            # Apply safety bias if configured
            safety_bias = self.env_config.get('NLP_CONSENSUS_SAFETY_BIAS', 0.0)
            if safety_bias > 0 and best_prediction in ['crisis', 'mild_crisis']:
                final_confidence = min(1.0, final_confidence + safety_bias)
                logger.info(f"🛡️ Applied safety bias: +{safety_bias:.3f}")
            
            return {
                'prediction': best_prediction,  # ← Normalized prediction like 'crisis'
                'confidence': final_confidence,
                'method': 'weighted_ensemble_normalized'
            }
        
        # Fallback to highest confidence with normalized prediction
        best_model = max(processed['confidence_scores'], key=processed['confidence_scores'].get)
        return {
            'prediction': processed['normalized_predictions'][best_model],  # ← Use normalized
            'confidence': processed['confidence_scores'][best_model],
            'method': 'highest_confidence_normalized_fallback'
        }

    def get_model_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all models"""
        return {
            'models_loaded': self.models_loaded(),
            'device': self.device,
            'precision': self.config['precision'],
            'ensemble_mode': self.config['ensemble_mode'],
            'current_label_set': self.get_current_label_set_name(),
            'label_stats': self.labels_config.get_current_stats(),
            'models': {
                'depression': {
                    'name': self.config['depression_model'],
                    'loaded': self.depression_model is not None,
                    'purpose': 'Primary crisis classification'
                },
                'sentiment': {
                    'name': self.config['sentiment_model'],
                    'loaded': self.sentiment_model is not None,
                    'purpose': 'Contextual validation'
                },
                'emotional_distress': {  # NEW
                    'name': self.config['emotional_distress_model'],
                    'loaded': self.emotional_distress_model is not None,
                    'purpose': 'Emotional distress detection'
                }
            },
            'gap_detection': {
                'enabled': True,
                'disagreement_threshold': self.config['disagreement_threshold'],
                'gap_detection_threshold': self.config['gap_detection_threshold']
            }
        }

# For backwards compatibility, create alias
ModelManager = EnhancedModelManager

# Global model manager instance
_global_model_manager = None

def get_model_manager() -> EnhancedModelManager:
    """Get global model manager instance"""
    global _global_model_manager
    return _global_model_manager

def set_model_manager(manager: EnhancedModelManager):
    """Set global model manager instance"""
    global _global_model_manager
    _global_model_manager = manager