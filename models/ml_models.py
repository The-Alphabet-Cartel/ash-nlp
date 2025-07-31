"""
Enhanced ML Model Management for Ash NLP Service - Three Model Architecture
Handles loading, caching, and access to ML models with DistilBERT emotional distress detection
"""

import logging
import os
import torch
from transformers import pipeline, AutoConfig
from typing import Optional, Dict, Any, Union, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedModelManager:
    """Enhanced centralized management of ML models with three-model ensemble support"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ModelManager with optional configuration
        
        Args:
            config: Optional configuration dictionary. If None, uses environment variables.
        """
        # Load configuration from environment or passed config
        self.config = self._load_config(config)
        
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
        
        logger.info(f"Enhanced ModelManager initialized with THREE-MODEL ensemble")
        logger.info(f"Device: {self.device}")
        logger.info(f"Model cache directory: {self.config['cache_dir']}")
    
    def _load_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Load configuration from environment variables or passed config"""
        
        if config:
            # Use passed configuration
            return config
        else:
            # Load from environment variables with defaults - ADD THIRD MODEL CONFIG
            return {
                'depression_model': os.getenv('NLP_DEPRESSION_MODEL', 'AnkitAI/deberta-v3-small-base-emotions-classifier'),
                'sentiment_model': os.getenv('NLP_SENTIMENT_MODEL', 'siebert/sentiment-roberta-large-english'),
                'emotional_distress_model': os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL', 'distilbert-base-uncased-finetuned-sst-2-english'),  # NEW
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
    
    def _get_model_kwargs(self) -> Dict[str, Any]:
        """Get arguments for model pipeline creation"""
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
        """Load all THREE models with enhanced configuration"""
        
        logger.info("=" * 70)
        logger.info("STARTING THREE-MODEL ENSEMBLE LOADING PROCESS")
        logger.info("=" * 70)
        
        logger.info(f"🔧 Configuration:")
        logger.info(f"   Device: {self.device}")
        logger.info(f"   Precision: {self.config['precision']}")
        logger.info(f"   Cache Dir: {self.config['cache_dir']}")
        logger.info(f"   Max Batch Size: {self.config['max_batch_size']}")
        logger.info(f"   Ensemble Mode: {self.config['ensemble_mode']}")
        
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
            logger.info("✅ THREE-MODEL ENSEMBLE LOADING COMPLETE")
            logger.info("=" * 70)
            
        except Exception as e:
            self._models_loaded = False
            logger.error(f"❌ Failed to load models: {e}")
            logger.exception("Full traceback:")
            raise
    
    async def _load_depression_model(self, model_kwargs, loading_kwargs):
        """Load the depression detection model"""
        logger.info("🧠 Loading Depression Detection model...")
        logger.info(f"   Model: {self.config['depression_model']}")
        
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
    
    async def _load_sentiment_model(self, model_kwargs, loading_kwargs):
        """Load the zero-shot sentiment analysis model"""
        logger.info("💭 Loading Zero-Shot Sentiment Analysis model...")
        logger.info(f"   Model: {self.config['sentiment_model']}")
        
        try:
            sent_config = AutoConfig.from_pretrained(
                self.config['sentiment_model'],
                **loading_kwargs
            )
            logger.info(f"   Architecture: {sent_config.model_type}")
            logger.info(f"   Labels: Zero-shot classification (dynamic)")
        except Exception as e:
            logger.warning(f"   Could not load model config: {e}")
        
        # CHANGE THIS LINE - use 'zero-shot-classification' not 'sentiment-analysis'
        self.sentiment_model = pipeline(
            "zero-shot-classification",  # ← CHANGED FROM "sentiment-analysis"
            model=self.config['sentiment_model'],
            **model_kwargs
        )
        logger.info("✅ Zero-shot sentiment model loaded successfully!")
    
    async def _load_emotional_distress_model(self, model_kwargs, loading_kwargs):
        """Load the emotional distress detection model (NEW)"""
        logger.info("😰 Loading Emotional Distress model...")
        logger.info(f"   Model: {self.config['emotional_distress_model']}")
        
        try:
            distress_config = AutoConfig.from_pretrained(
                self.config['emotional_distress_model'],
                **loading_kwargs
            )
            logger.info(f"   Architecture: {distress_config.model_type}")
            logger.info(f"   Labels: {getattr(distress_config, 'id2label', 'Not specified')}")
        except Exception as e:
            logger.warning(f"   Could not load model config: {e}")
        
        self.emotional_distress_model = pipeline(
            "sentiment-analysis",  # DistilBERT SST-2 uses sentiment-analysis pipeline
            model=self.config['emotional_distress_model'],
            top_k=None,
            **model_kwargs
        )
        logger.info("✅ Emotional distress model loaded successfully!")
    
    async def _test_all_models(self):
        """Test all three models with sample messages"""
        try:
            test_messages = [
                "I'm feeling really down and hopeless today",
                "Everything is falling apart and I can't handle it anymore",
                "I'm just having a rough day but I'll be okay"
            ]
            
            logger.info("🧪 Testing all three models...")
            
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
        """Analyze message with depression detection model"""
        try:
            return self.depression_model(message)
        except Exception as e:
            logger.error(f"Depression model analysis failed: {e}")
            return None
    
    def analyze_with_sentiment_model(self, message: str):
        """Analyze message with zero-shot sentiment model using crisis-optimized labels"""
        try:
            # CRISIS-OPTIMIZED LABELS - much more specific and distinct
            crisis_labels = [
                "person expressing severe mental health crisis, suicidal thoughts, or immediate danger",
                "person expressing significant emotional distress and needing support",
                "person having a difficult day or minor negative feelings",
                "person making neutral everyday conversation or factual statements", 
                "person expressing positive feelings, gratitude, or happiness",
                "person expressing excitement, joy, or very positive emotions"
            ]
            
            result = self.sentiment_model(message, crisis_labels)
            
            # Convert to format compatible with your existing code
            formatted_result = []
            for label, score in zip(result['labels'], result['scores']):
                # Map long labels to short ones for compatibility
                short_label = self._map_crisis_label_to_sentiment(label)
                formatted_result.append({
                    'label': short_label,
                    'score': score
                })
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Zero-shot sentiment analysis failed: {e}")
            return None
    
    def _map_crisis_label_to_sentiment(self, long_label: str) -> str:
        """Map crisis-specific labels back to sentiment categories"""
        
        # Look for key phrases in the label to determine mapping
        label_lower = long_label.lower()
        
        if "severe mental health crisis" in label_lower or "suicidal" in label_lower:
            return "Very Negative"
        elif "significant emotional distress" in label_lower or "needing support" in label_lower:
            return "Negative"
        elif "difficult day" in label_lower or "minor negative" in label_lower:
            return "Slightly Negative"
        elif "neutral everyday conversation" in label_lower or "factual statements" in label_lower:
            return "Neutral"
        elif "positive feelings" in label_lower or "gratitude" in label_lower:
            return "Positive"
        elif "excitement" in label_lower or "very positive" in label_lower:
            return "Very Positive"
        else:
            # Fallback mapping
            return "Neutral"

    def analyze_with_emotional_distress_model(self, message: str):  # NEW METHOD
        """Analyze message with emotional distress detection model"""
        try:
            return self.emotional_distress_model(message)
        except Exception as e:
            logger.error(f"Emotional distress model analysis failed: {e}")
            return None
    
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
        """Enhanced normalization for zero-shot crisis predictions"""
        pred_lower = prediction.lower()
        
        # Crisis indicators (updated for new labels)
        if pred_lower in ['very negative', 'severe']:
            return 'crisis'
        elif pred_lower in ['negative', 'slightly negative']:
            return 'crisis'  # Still treat as crisis for safety-first approach
        elif pred_lower in ['neutral']:
            return 'neutral'
        elif pred_lower in ['positive', 'very positive']:
            return 'safe'
        
        # Keep your existing mappings for other models
        elif pred_lower == 'label_0':  # ALBERT IMDB
            return 'crisis'
        elif pred_lower == 'label_1':  # ALBERT IMDB 
            return 'safe'
        elif pred_lower in ['sadness', 'fear', 'anger', 'disgust']:  # Emotion models
            return 'crisis'
        elif pred_lower in ['joy', 'love', 'surprise']:  # Emotion models
            return 'safe'
        
        return 'unknown'
    
    def _generate_consensus(self, processed: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consensus prediction from three models using NORMALIZED predictions"""
        if not processed['confidence_scores']:
            return None
        
        ensemble_mode = self.config['ensemble_mode']
        
        if ensemble_mode == 'consensus':
            # Check if NORMALIZED predictions agree (not raw predictions)
            normalized_predictions = set(processed['normalized_predictions'].values())
            
            if len(normalized_predictions) == 1:
                # All models agree on normalized prediction
                avg_confidence = sum(processed['confidence_scores'].values()) / len(processed['confidence_scores'])
                consensus_prediction = list(normalized_predictions)[0]  # Use normalized prediction
                
                return {
                    'prediction': consensus_prediction,  # 'crisis' or 'safe' instead of raw labels
                    'confidence': avg_confidence,
                    'method': 'unanimous_consensus'  # This will now trigger correctly!
                }
            else:
                # Models disagree on normalized predictions - use highest confidence but mark as uncertain
                best_model = max(processed['confidence_scores'], key=processed['confidence_scores'].get)
                return {
                    'prediction': processed['predictions'][best_model],  # Keep original prediction for debugging
                    'confidence': processed['confidence_scores'][best_model] * 0.7,  # Reduce confidence due to disagreement
                    'method': 'best_of_disagreeing'
                }
        
        elif ensemble_mode == 'majority':
            # Simple majority vote with confidence weighting on NORMALIZED predictions
            prediction_votes = {}
            for model, normalized_pred in processed['normalized_predictions'].items():
                confidence = processed['confidence_scores'][model]
                if normalized_pred not in prediction_votes:
                    prediction_votes[normalized_pred] = []
                prediction_votes[normalized_pred].append(confidence)
            
            # Find majority prediction
            majority_prediction = max(prediction_votes, key=lambda x: len(prediction_votes[x]))
            avg_confidence = sum(prediction_votes[majority_prediction]) / len(prediction_votes[majority_prediction])
            
            return {
                'prediction': majority_prediction,  # Use normalized prediction
                'confidence': avg_confidence,
                'method': 'majority_vote'
            }
        
        elif ensemble_mode == 'weighted':
            # Weight models differently using normalized predictions
            model_weights = {
                'depression': 0.5,      # Primary model gets highest weight
                'sentiment': 0.2,       # Secondary contextual model
                'emotional_distress': 0.3  # Third model for additional insight
            }
            
            weighted_scores = {}
            for model, normalized_pred in processed['normalized_predictions'].items():
                confidence = processed['confidence_scores'][model]
                weight = model_weights.get(model, 1.0)
                weighted_score = confidence * weight
                
                if normalized_pred not in weighted_scores:
                    weighted_scores[normalized_pred] = 0
                weighted_scores[normalized_pred] += weighted_score
            
            best_prediction = max(weighted_scores, key=weighted_scores.get)
            
            return {
                'prediction': best_prediction,  # Use normalized prediction
                'confidence': weighted_scores[best_prediction],
                'method': 'weighted_ensemble'
            }
        
        # Fallback to highest confidence (use raw prediction for compatibility)
        best_model = max(processed['confidence_scores'], key=processed['confidence_scores'].get)
        return {
            'prediction': processed['predictions'][best_model],
            'confidence': processed['confidence_scores'][best_model],
            'method': 'highest_confidence_fallback'
        }
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all models"""
        return {
            'models_loaded': self.models_loaded(),
            'device': self.device,
            'precision': self.config['precision'],
            'ensemble_mode': self.config['ensemble_mode'],
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