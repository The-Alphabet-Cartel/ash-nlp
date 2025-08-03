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
        self.emotional_distress_model = None  # NEW: Third model
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
        
        # Log model configurations
        self._log_model_configurations()
    
    def _load_unified_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON (if available) and environment variables
        JSON takes precedence for ensemble settings, environment for operational settings
        """
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
        if self.config_manager and hasattr(self.config_manager, '_config'):
            # Use config manager if available
            env_config = self.config_manager._config
        else:
            # Direct environment variable access
            env_config = {}
        
        return {
            # Model names (can be overridden by JSON)
            'depression_model': env_config.get('NLP_DEPRESSION_MODEL', os.getenv('NLP_DEPRESSION_MODEL', 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0')),
            'sentiment_model': env_config.get('NLP_SENTIMENT_MODEL', os.getenv('NLP_SENTIMENT_MODEL', 'Lowerated/lm6-deberta-v3-topic-sentiment')),
            'emotional_distress_model': env_config.get('NLP_EMOTIONAL_DISTRESS_MODEL', os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL', 'facebook/bart-large-mnli')),
            
            # Operational settings (typically not in JSON)
            'cache_dir': env_config.get('NLP_MODEL_CACHE_DIR', os.getenv('NLP_MODEL_CACHE_DIR', './models/cache')),
            'device': env_config.get('NLP_DEVICE', os.getenv('NLP_DEVICE', 'auto')),
            'precision': env_config.get('NLP_MODEL_PRECISION', os.getenv('NLP_MODEL_PRECISION', 'float16')),
            'max_batch_size': int(env_config.get('NLP_MAX_BATCH_SIZE', os.getenv('NLP_MAX_BATCH_SIZE', '32'))),
            'huggingface_token': env_config.get('GLOBAL_HUGGINGFACE_TOKEN', os.getenv('GLOBAL_HUGGINGFACE_TOKEN')),
            
            # Ensemble settings (can be overridden by JSON)
            'depression_weight': float(env_config.get('NLP_DEPRESSION_MODEL_WEIGHT', os.getenv('NLP_DEPRESSION_MODEL_WEIGHT', '0.6'))),
            'sentiment_weight': float(env_config.get('NLP_SENTIMENT_MODEL_WEIGHT', os.getenv('NLP_SENTIMENT_MODEL_WEIGHT', '0.15'))),
            'emotional_distress_weight': float(env_config.get('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', os.getenv('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT', '0.25'))),
            'ensemble_mode': env_config.get('NLP_ENSEMBLE_MODE', os.getenv('NLP_ENSEMBLE_MODE', 'weighted')),
            'gap_detection_threshold': float(env_config.get('NLP_GAP_DETECTION_THRESHOLD', os.getenv('NLP_GAP_DETECTION_THRESHOLD', '0.25'))),
            'disagreement_threshold': float(env_config.get('NLP_DISAGREEMENT_THRESHOLD', os.getenv('NLP_DISAGREEMENT_THRESHOLD', '0.35')))
        }
    
    def _load_json_config(self) -> Dict[str, Any]:
        """Load configuration from JSON ensemble manager in managers/ directory"""
        json_config = {}
        
        # Get model definitions from JSON
        model_definitions = self.ensemble_manager.get_model_definitions()
        
        # Extract model names and configurations
        for model_key, model_config in model_definitions.items():
            if model_key == 'depression':
                json_config['depression_model'] = model_config['name']
                json_config['depression_weight'] = model_config.get('weight', model_config.get('default_weight', 0.6))
                json_config['depression_pipeline_kwargs'] = model_config.get('pipeline_kwargs', {})
                json_config['depression_model_kwargs'] = model_config.get('model_kwargs', {})
            elif model_key == 'sentiment':
                json_config['sentiment_model'] = model_config['name']
                json_config['sentiment_weight'] = model_config.get('weight', model_config.get('default_weight', 0.15))
                json_config['sentiment_pipeline_kwargs'] = model_config.get('pipeline_kwargs', {})
                json_config['sentiment_model_kwargs'] = model_config.get('model_kwargs', {})
            elif model_key == 'emotional_distress':
                json_config['emotional_distress_model'] = model_config['name']
                json_config['emotional_distress_weight'] = model_config.get('weight', model_config.get('default_weight', 0.25))
                json_config['emotional_distress_pipeline_kwargs'] = model_config.get('pipeline_kwargs', {})
                json_config['emotional_distress_model_kwargs'] = model_config.get('model_kwargs', {})
        
        # Get ensemble configuration
        ensemble_config = self.ensemble_manager.get_ensemble_configuration()
        json_config['ensemble_mode'] = ensemble_config.get('default_mode', 'weighted')
        
        # Get gap detection settings
        gap_detection = ensemble_config.get('gap_detection', {})
        json_config['gap_detection_threshold'] = gap_detection.get('threshold', gap_detection.get('default_threshold', 0.25))
        json_config['disagreement_threshold'] = gap_detection.get('disagreement_threshold', gap_detection.get('default_disagreement_threshold', 0.35))
        
        # Get hardware optimization settings
        hardware_config = self.ensemble_manager.get_hardware_optimization()
        json_config['device'] = hardware_config.get('device', hardware_config.get('default_device', 'auto'))
        json_config['precision'] = hardware_config.get('precision', hardware_config.get('default_precision', 'float16'))
        
        # Get performance settings
        perf_settings = hardware_config.get('performance_settings', {})
        json_config['max_batch_size'] = perf_settings.get('max_batch_size', perf_settings.get('default_batch_size', 32))
        
        # Get memory optimization settings
        memory_settings = hardware_config.get('memory_optimization', {})
        json_config['cache_dir'] = memory_settings.get('cache_dir', memory_settings.get('default_cache_dir', './models/cache'))
        
        return json_config
    
    def _log_model_configurations(self):
        """Log the model configurations for debugging"""
        logger.info("🤖 Model Configuration Summary:")
        logger.info(f"   Depression Model: {self.config['depression_model']} (weight: {self.config['depression_weight']})")
        logger.info(f"   Sentiment Model: {self.config['sentiment_model']} (weight: {self.config['sentiment_weight']})")
        logger.info(f"   Emotional Distress Model: {self.config['emotional_distress_model']} (weight: {self.config['emotional_distress_weight']})")
        logger.info(f"   Ensemble Mode: {self.config['ensemble_mode']}")
        logger.info(f"   Gap Detection Threshold: {self.config['gap_detection_threshold']}")
        logger.info(f"   Disagreement Threshold: {self.config['disagreement_threshold']}")
        
        # Validate weights
        total_weight = self.config['depression_weight'] + self.config['sentiment_weight'] + self.config['emotional_distress_weight']
        if abs(total_weight - 1.0) > 0.01:
            logger.warning(f"⚠️ Model weights sum to {total_weight}, expected ~1.0")
        else:
            logger.info(f"✅ Model weights validation passed: {total_weight}")
    
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
    
    def _get_model_kwargs(self, model_key: str) -> Dict[str, Any]:
        """Get model-specific kwargs from configuration"""
        # Check if JSON config provides model-specific kwargs
        model_kwargs_key = f"{model_key}_model_kwargs"
        if model_kwargs_key in self.config:
            kwargs = self.config[model_kwargs_key].copy()
        else:
            kwargs = {}
        
        # Set device and torch_dtype if not specified
        if 'device_map' not in kwargs:
            kwargs['device_map'] = 'auto' if self.device.startswith('cuda') else None
        
        if 'torch_dtype' not in kwargs or kwargs['torch_dtype'] == 'auto':
            kwargs['torch_dtype'] = self._get_torch_dtype()
        
        return kwargs
    
    def _get_pipeline_kwargs(self, model_key: str) -> Dict[str, Any]:
        """Get pipeline-specific kwargs from configuration"""
        # Check if JSON config provides pipeline-specific kwargs
        pipeline_kwargs_key = f"{model_key}_pipeline_kwargs"
        if pipeline_kwargs_key in self.config:
            kwargs = self.config[pipeline_kwargs_key].copy()
        else:
            kwargs = {}
        
        # Set device if not specified
        if 'device' not in kwargs:
            kwargs['device'] = self.device
        
        # Set default pipeline arguments
        kwargs.setdefault('return_all_scores', True)
        kwargs.setdefault('multi_label', False)
        
        return kwargs
    
    async def load_models(self):
        """Load all three models with JSON configuration support"""
        try:
            logger.info("🚀 Starting model loading with enhanced configuration...")
            
            # Load depression model
            logger.info(f"📦 Loading depression model: {self.config['depression_model']}")
            model_kwargs = self._get_model_kwargs('depression')
            pipeline_kwargs = self._get_pipeline_kwargs('depression')
            
            self.depression_model = pipeline(
                "zero-shot-classification",
                model=self.config['depression_model'],
                model_kwargs=model_kwargs,
                **pipeline_kwargs
            )
            logger.info("✅ Depression model loaded successfully")
            
            # Load sentiment model
            logger.info(f"📦 Loading sentiment model: {self.config['sentiment_model']}")
            model_kwargs = self._get_model_kwargs('sentiment')
            pipeline_kwargs = self._get_pipeline_kwargs('sentiment')
            
            self.sentiment_model = pipeline(
                "zero-shot-classification",
                model=self.config['sentiment_model'],
                model_kwargs=model_kwargs,
                **pipeline_kwargs
            )
            logger.info("✅ Sentiment model loaded successfully")
            
            # Load emotional distress model
            logger.info(f"📦 Loading emotional distress model: {self.config['emotional_distress_model']}")
            model_kwargs = self._get_model_kwargs('emotional_distress')
            pipeline_kwargs = self._get_pipeline_kwargs('emotional_distress')
            
            self.emotional_distress_model = pipeline(
                "zero-shot-classification",
                model=self.config['emotional_distress_model'],
                model_kwargs=model_kwargs,
                **pipeline_kwargs
            )
            logger.info("✅ Emotional distress model loaded successfully")
            
            self._models_loaded = True
            logger.info("🎯 All three models loaded successfully with JSON-configured ensemble")
            
            # Log memory usage if on GPU
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated() / 1024**3  # GB
                memory_reserved = torch.cuda.memory_reserved() / 1024**3   # GB
                logger.info(f"🔥 GPU Memory - Allocated: {memory_allocated:.2f}GB, Reserved: {memory_reserved:.2f}GB")
            
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
        """Get detailed status of all models with JSON config info"""
        status = {
            "models_loaded": self.models_loaded(),
            "device": self.device,
            "precision": self.config['precision'],
            "ensemble_mode": self.config['ensemble_mode'],
            "gap_detection": True,
            "configuration_source": "JSON + Environment (managers/)" if self.ensemble_manager else "Environment Only",
            "models": {
                "depression": {
                    "name": self.config['depression_model'],
                    "loaded": self.depression_model is not None,
                    "weight": self.config['depression_weight'],
                    "type": "DeBERTa-based classification"
                },
                "sentiment": {
                    "name": self.config['sentiment_model'],
                    "loaded": self.sentiment_model is not None,
                    "weight": self.config['sentiment_weight'],
                    "type": "DeBERTa-based sentiment analysis"
                },
                "emotional_distress": {
                    "name": self.config['emotional_distress_model'],
                    "loaded": self.emotional_distress_model is not None,
                    "weight": self.config['emotional_distress_weight'],
                    "type": "BART-based emotional classification"
                }
            }
        }
        
        # Add JSON-specific information if available from managers/
        if self.ensemble_manager:
            try:
                json_summary = self.ensemble_manager.get_summary()
                status["json_config"] = json_summary
                status["config_file"] = self.ensemble_manager.config_file
                status["config_modified"] = self.ensemble_manager.is_config_modified()
                status["managers_directory"] = "managers/"
            except Exception as e:
                logger.warning(f"Could not get JSON config summary from managers/: {e}")
        
        return status
    
    def get_zero_shot_labels(self, label_set: str = "enhanced_crisis") -> List[str]:
        """Get zero-shot labels for classification (this should be moved to JSON config later)"""
        # TODO: Move to JSON configuration in next iteration
        if label_set == "enhanced_crisis":
            return [
                "person in acute crisis requiring immediate intervention with severe depression or suicidal thoughts",
                "person experiencing significant mental health crisis with moderate depression and distress", 
                "person showing mild signs of emotional distress or mental health concerns",
                "person expressing normal emotional range without crisis indicators",
                "person demonstrating positive mental wellness and emotional stability",
                "person showing exceptional emotional resilience and mental health"
            ]
        else:
            # Fallback labels
            return [
                "crisis", "mild_crisis", "negative", "neutral", "positive", "very_positive"
            ]
    
    def get_depression_labels(self):
        """Depression-specific labels for the primary model"""
        return [
            "person experiencing severe depression with crisis-level symptoms requiring immediate intervention",
            "person showing significant depressive symptoms with substantial impairment in daily functioning",
            "person displaying moderate depressive symptoms that interfere with normal daily activities", 
            "person experiencing mild depressive symptoms or temporary sadness within normal emotional range",
            "person demonstrating stable mental health with normal emotional fluctuations and no depression signs",
            "person exhibiting positive mental wellness, emotional resilience, and psychological stability"
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
    
    async def analyze_with_ensemble(self, message: str, user_id: str = None, channel_id: str = None) -> Dict[str, Any]:
        """
        Perform ensemble analysis using all three models with JSON-configured weights and thresholds
        """
        if not self.models_loaded():
            raise RuntimeError("Models not loaded")
        
        try:
            start_time = time.time()
            
            # Get labels for each model
            depression_labels = self.get_depression_labels()
            sentiment_labels = self.get_sentiment_labels()
            distress_labels = self.get_emotional_distress_labels()
            
            # Run all three models
            depression_result = self.depression_model(message, depression_labels)
            sentiment_result = self.sentiment_model(message, sentiment_labels)
            distress_result = self.emotional_distress_model(message, distress_labels)
            
            # Process results with JSON-configured weights
            ensemble_result = self._process_ensemble_results(
                depression_result, sentiment_result, distress_result, message
            )
            
            processing_time = (time.time() - start_time) * 1000
            ensemble_result['processing_time_ms'] = processing_time
            ensemble_result['user_id'] = user_id
            ensemble_result['channel_id'] = channel_id
            ensemble_result['timestamp'] = time.time()
            ensemble_result['configuration_source'] = "JSON + Environment (managers/)" if self.ensemble_manager else "Environment Only"
            
            return ensemble_result
            
        except Exception as e:
            logger.error(f"Ensemble analysis failed: {e}")
            raise
    
    def _process_ensemble_results(self, depression_result, sentiment_result, distress_result, message: str) -> Dict[str, Any]:
        """Process ensemble results using JSON-configured weights and consensus rules"""
        
        # Extract predictions and confidences
        dep_prediction, dep_confidence = self._extract_top_prediction(depression_result)
        sent_prediction, sent_confidence = self._extract_top_prediction(sentiment_result)
        dist_prediction, dist_confidence = self._extract_top_prediction(distress_result)
        
        # Store individual results
        individual_results = {
            "depression": {"prediction": dep_prediction, "confidence": dep_confidence},
            "sentiment": {"prediction": sent_prediction, "confidence": sent_confidence},
            "emotional_distress": {"prediction": dist_prediction, "confidence": dist_confidence}
        }
        
        # Apply ensemble logic based on JSON configuration
        ensemble_mode = self.config['ensemble_mode']
        
        if ensemble_mode == 'weighted':
            final_result = self._weighted_ensemble(individual_results)
        elif ensemble_mode == 'consensus':
            final_result = self._consensus_ensemble(individual_results)
        elif ensemble_mode == 'majority':
            final_result = self._majority_ensemble(individual_results)
        else:
            logger.warning(f"Unknown ensemble mode '{ensemble_mode}', using weighted")
            final_result = self._weighted_ensemble(individual_results)
        
        # Detect gaps/disagreements using JSON thresholds
        gap_info = self._detect_model_gaps(individual_results)
        
        return {
            "needs_response": final_result['needs_response'],
            "crisis_level": final_result['crisis_level'],
            "confidence_score": final_result['confidence_score'],
            "method": f"three_model_ensemble_{ensemble_mode}",
            "individual_results": individual_results,
            "ensemble_analysis": {
                "consensus": final_result,
                "predictions": {k: v["prediction"] for k, v in individual_results.items()},
                "confidence_scores": {k: v["confidence"] for k, v in individual_results.items()}
            },
            "gaps_detected": gap_info['gaps_detected'],
            "gap_details": gap_info['gap_details'],
            "requires_staff_review": gap_info['requires_staff_review'] or final_result.get('requires_staff_review', False),
            "model_info": "json_configured_three_model_ensemble",
            "detected_categories": final_result.get('detected_categories', [])
        }
    
    def _extract_top_prediction(self, result) -> Tuple[str, float]:
        """Extract top prediction and confidence from model result"""
        if isinstance(result, dict) and 'labels' in result and 'scores' in result:
            return result['labels'][0], result['scores'][0]
        return "unknown", 0.0
    
    def _weighted_ensemble(self, individual_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Weighted ensemble using JSON-configured weights"""
        weights = {
            'depression': self.config['depression_weight'],
            'sentiment': self.config['sentiment_weight'],
            'emotional_distress': self.config['emotional_distress_weight']
        }
        
        # Calculate weighted confidence score
        weighted_score = 0.0
        for model, weight in weights.items():
            confidence = individual_results[model]['confidence']
            weighted_score += confidence * weight
        
        # Map to crisis level using JSON thresholds (if available)
        crisis_level = self._map_confidence_to_crisis_level(weighted_score)
        
        return {
            "confidence_score": weighted_score,
            "crisis_level": crisis_level,
            "needs_response": crisis_level != "none",
            "method": "weighted_average",
            "detected_categories": [crisis_level] if crisis_level != "none" else []
        }
    
    def _consensus_ensemble(self, individual_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Consensus ensemble - all models must agree"""
        predictions = [result['prediction'] for result in individual_results.values()]
        confidences = [result['confidence'] for result in individual_results.values()]
        
        # Simple consensus: use average confidence if predictions are similar
        avg_confidence = sum(confidences) / len(confidences)
        crisis_level = self._map_confidence_to_crisis_level(avg_confidence)
        
        return {
            "confidence_score": avg_confidence,
            "crisis_level": crisis_level,
            "needs_response": crisis_level != "none",
            "method": "consensus",
            "detected_categories": [crisis_level] if crisis_level != "none" else []
        }
    
    def _majority_ensemble(self, individual_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Majority ensemble - democratic voting"""
        confidences = [result['confidence'] for result in individual_results.values()]
        
        # Use median confidence for majority decision
        confidences.sort()
        median_confidence = confidences[len(confidences) // 2]
        crisis_level = self._map_confidence_to_crisis_level(median_confidence)
        
        return {
            "confidence_score": median_confidence,
            "crisis_level": crisis_level,
            "needs_response": crisis_level != "none",
            "method": "majority",
            "detected_categories": [crisis_level] if crisis_level != "none" else []
        }
    
    def _map_confidence_to_crisis_level(self, confidence: float) -> str:
        """Map confidence score to crisis level using JSON thresholds from managers/ if available"""
        # Try to get thresholds from managers/ JSON config
        if self.ensemble_manager:
            try:
                threshold_config = self.ensemble_manager.get_threshold_configuration()
                ensemble_thresholds = threshold_config.get('ensemble_thresholds', {})
                
                high_threshold = ensemble_thresholds.get('high', 0.45)
                medium_threshold = ensemble_thresholds.get('medium', 0.25)
                low_threshold = ensemble_thresholds.get('low', 0.12)
            except Exception as e:
                logger.warning(f"Could not get JSON thresholds from managers/, using defaults: {e}")
                high_threshold, medium_threshold, low_threshold = 0.45, 0.25, 0.12
        else:
            # Fallback to environment variables or defaults
            high_threshold = float(os.getenv('NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD', '0.45'))
            medium_threshold = float(os.getenv('NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD', '0.25'))
            low_threshold = float(os.getenv('NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD', '0.12'))
        
        if confidence >= high_threshold:
            return "high"
        elif confidence >= medium_threshold:
            return "medium"
        elif confidence >= low_threshold:
            return "low"
        else:
            return "none"
    
    def _detect_model_gaps(self, individual_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Detect disagreements between models using JSON-configured thresholds from managers/"""
        confidences = [result['confidence'] for result in individual_results.values()]
        max_conf = max(confidences)
        min_conf = min(confidences)
        confidence_spread = max_conf - min_conf
        
        # Get thresholds from JSON config
        gap_threshold = self.config['gap_detection_threshold']
        disagreement_threshold = self.config['disagreement_threshold']
        
        gaps_detected = confidence_spread >= gap_threshold
        significant_disagreement = confidence_spread >= disagreement_threshold
        
        gap_details = []
        if gaps_detected:
            gap_details.append({
                "type": "confidence_spread",
                "value": confidence_spread,
                "threshold": gap_threshold,
                "significant": significant_disagreement
            })
        
        return {
            "gaps_detected": gaps_detected,
            "requires_staff_review": significant_disagreement,
            "gap_details": gap_details,
            "confidence_spread": confidence_spread
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