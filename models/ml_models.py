"""
Enhanced ML Model Management for Ash NLP Service - Three Model Architecture
Handles loading, caching, and access to ML models with DistilBERT emotional distress detection
"""

import logging
import os
import torch
from transformers import pipeline, AutoConfig
from typing import Optional, Dict, Any, Union, List, Tuple  # ← Make sure List is included
from pathlib import Path
from config.env_manager import get_config

logger = logging.getLogger(__name__)

class EnhancedModelManager:
    """Enhanced centralized management of ML models with Three Zero-Shot Model Ensemble support"""
    
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
        
        logger.info(f"Enhanced ModelManager initialized with Three Zero-Shot Model Ensemble")
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
    
    def get_depression_labels(self):
        """Ultra-specific crisis detection labels for primary model"""
        return [
            "person actively expressing suicidal ideation, plans for self-harm, or immediate danger to themselves",
            "person showing severe clinical depression with major functional impairment and crisis indicators",
            "person experiencing moderate depression with significant distress requiring professional intervention",
            "person having mild depressive episode or temporary low mood with manageable symptoms",
            "person in stable mental health with normal emotional fluctuations and no depression signs",
            "person demonstrating positive mental wellness, emotional resilience, and psychological stability"
        ]

    def get_sentiment_labels(self):
        """Emotional tone and affect labels for contextual analysis"""
        return [
            "person expressing profound despair, hopelessness, overwhelming sadness, or emotional devastation",
            "person showing significant negative emotions such as anger, frustration, fear, or deep disappointment", 
            "person displaying mixed or neutral emotional state without strong positive or negative feelings",
            "person expressing mild positive emotions like satisfaction, calm contentment, or gentle happiness",
            "person showing strong positive emotions including joy, excitement, love, gratitude, or enthusiasm",
            "person radiating intense positive energy, euphoria, overwhelming happiness, or peak emotional highs"
        ]

    def get_emotional_distress_labels(self):
        """Stress and coping capacity labels for validation"""
        return [
            "person in acute psychological distress unable to cope and requiring immediate crisis intervention",
            "person experiencing severe emotional overwhelm with significantly impaired functioning and coping",
            "person showing moderate distress with some difficulty managing emotions and daily responsibilities", 
            "person handling normal life stress with adequate coping strategies and emotional regulation",
            "person demonstrating strong emotional resilience with healthy stress management and adaptation",
            "person exhibiting optimal emotional wellbeing with excellent coping skills and life satisfaction"
        ]

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
        logger.info("STARTING Three Zero-Shot Model Ensemble LOADING PROCESS")
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

    def _map_depression_zero_shot_label(self, long_label: str) -> str:
        """Map depression specialist labels to crisis categories"""
        label_lower = long_label.lower()
        
        if "actively expressing suicidal ideation" in label_lower or "immediate danger" in label_lower:
            return "severe"
        elif "severe clinical depression" in label_lower or "major functional impairment" in label_lower:
            return "severe"
        elif "moderate depression" in label_lower or "professional intervention" in label_lower:
            return "moderate"
        elif "mild depressive episode" in label_lower or "manageable symptoms" in label_lower:
            return "mild"
        elif "stable mental health" in label_lower or "no depression signs" in label_lower:
            return "not depression"
        elif "positive mental wellness" in label_lower or "psychological stability" in label_lower:
            return "not depression"
        else:
            return "not depression"

    def _map_sentiment_zero_shot_label(self, long_label: str) -> str:
        """Map sentiment specialist labels to emotional categories"""
        label_lower = long_label.lower()
        
        if "profound despair" in label_lower or "overwhelming sadness" in label_lower or "emotional devastation" in label_lower:
            return "Very Negative"
        elif "significant negative emotions" in label_lower or "anger" in label_lower or "deep disappointment" in label_lower:
            return "Negative"
        elif "mixed or neutral emotional state" in label_lower:
            return "Neutral"
        elif "mild positive emotions" in label_lower or "calm contentment" in label_lower:
            return "Positive"
        elif "strong positive emotions" in label_lower or "joy" in label_lower or "enthusiasm" in label_lower:
            return "Very Positive"
        elif "intense positive energy" in label_lower or "euphoria" in label_lower or "peak emotional highs" in label_lower:
            return "Very Positive"
        else:
            return "Neutral"

    def _map_distress_zero_shot_label(self, long_label: str) -> str:
        """Map distress specialist labels to stress categories"""
        label_lower = long_label.lower()
        
        if "acute psychological distress" in label_lower or "immediate crisis intervention" in label_lower:
            return "High Distress"
        elif "severe emotional overwhelm" in label_lower or "significantly impaired functioning" in label_lower:
            return "High Distress"
        elif "moderate distress" in label_lower or "difficulty managing emotions" in label_lower:
            return "Medium Distress"
        elif "normal life stress" in label_lower or "adequate coping strategies" in label_lower:
            return "Low Distress"
        elif "strong emotional resilience" in label_lower or "healthy stress management" in label_lower:
            return "No Distress"
        elif "optimal emotional wellbeing" in label_lower or "excellent coping skills" in label_lower:
            return "No Distress"
        else:
            return "Low Distress"

    def _map_to_depression_category(self, zero_shot_label: str) -> str:
        """Map zero-shot labels to depression categories"""
        label_lower = zero_shot_label.lower()
        
        if "severe depression" in label_lower or "suicidal ideation" in label_lower:
            return "severe"
        elif "moderate depression" in label_lower or "significant functional impairment" in label_lower:
            return "moderate"
        elif "mild depression" in label_lower or "temporary low mood" in label_lower:
            return "mild"
        elif "normal emotional state" in label_lower:
            return "not depression"
        elif "positive mental health" in label_lower:
            return "not depression"
        else:
            return "not depression"  # Default to safe
    
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