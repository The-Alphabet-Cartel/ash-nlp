# ash-nlp/managers/model_ensemble_manager.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Model Ensemble Manager for Ash NLP Service
---
FILE VERSION: v3.1-3e-5.5-7-3
LAST MODIFIED: 2025-08-21
PHASE: 3e Step 5.5-7 - Phase 3: AI Classification Methods Implementation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PHASE 3 IMPLEMENTATION:
- Added actual AI classification methods that EnsembleAnalysisHelper should call
- Implemented classify_with_zero_shot() for semantic classification
- Added model pipeline management and caching
- Proper integration with ZeroShotManager for label management
- Correct architectural flow: EnsembleAnalysisHelper → ModelEnsembleManager → transformers
"""

import os
import logging
import time
import asyncio
from typing import Dict, Any, List, Optional

# PHASE 3: Add transformers imports for actual AI classification
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Transformers library loaded in ModelEnsembleManager for AI classification")
except ImportError as e:
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Transformers library not available in ModelEnsembleManager: {e}")

logger = logging.getLogger(__name__)

class ModelEnsembleManager:
    """
    Model Ensemble Manager - PHASE 3: AI Classification Implementation
    
    This manager now provides:
    - Model configuration management
    - ACTUAL AI classification methods for EnsembleAnalysisHelper
    - Model pipeline loading and caching
    - Ensemble voting and score aggregation
    - Integration with ZeroShotManager for label management
    - Hardware configuration and optimization
    
    PHASE 3 ARCHITECTURE FIX:
    EnsembleAnalysisHelper calls ModelEnsembleManager.classify_with_zero_shot()
    Instead of EnsembleAnalysisHelper directly creating transformers pipelines
    """
    
    def __init__(self, config_manager):
        """
        Initialize Model Ensemble Manager
        
        Args:
            config_manager: UnifiedConfigManager instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ModelEnsembleManager")
        
        self.config_manager = config_manager
        
        # PHASE 3: Add model pipeline cache and loading management
        self._model_cache = {}
        self._model_loading_lock = asyncio.Lock()
        
        logger.info("ModelEnsembleManager v3.1e-5.5-7-3 Phase 3 initialized with AI classification")
        
        # Load and validate configuration
        self._load_and_validate_configuration()
        
        # Get device configuration for AI models
        self.device = self._get_device_config()
        logger.info(f"🔧 ModelEnsembleManager device configuration: {self.device}")
    
    def _load_and_validate_configuration(self):
        """Load and validate model ensemble configuration using enhanced patterns"""
        try:
            # Use enhanced configuration access patterns
            self.config = self._load_model_configuration()
            
            if not self.config:
                raise ValueError("Model configuration could not be loaded")
            
            logger.info(f"Model ensemble configuration loaded successfully")
            
            # Validate configuration
            self._validate_configuration()
            
        except Exception as e:
            logger.error(f"Failed to load model configuration: {e}")
            raise
    
    def _load_model_configuration(self) -> Dict[str, Any]:
        """Load model configuration using enhanced UnifiedConfigManager patterns"""
        try:
            # Use get_config_section instead of get_model_configuration
            model_config = self.config_manager.get_config_section('model_ensemble')
            
            if not model_config:
                logger.warning("No model_ensemble.json found, using environment fallback")
                return self._get_fallback_model_config()
            
            # Extract model definitions from configuration
            ensemble_models = model_config.get('ensemble_models', {})
            model_definitions = ensemble_models.get('model_definitions', {})
            
            # Transform to expected format
            result = {
                'models': model_definitions,
                'ensemble_mode': model_config.get('ensemble_config', {}).get('mode', 'majority'),
                'hardware_settings': model_config.get('hardware_settings', {}),
                'validation': model_config.get('validation', {})
            }
            
            logger.debug(f"Loaded {len(model_definitions)} model definitions")
            return result
            
        except Exception as e:
            logger.warning(f"Error loading model configuration: {e}, using fallback")
            return self._get_fallback_model_config()
    
    def _get_fallback_model_config(self) -> Dict[str, Any]:
        """Get fallback model configuration using environment variables"""
        logger.info("Using environment variable fallback for model configuration")
        
        return {
            'models': {
                'depression': {
                    'name': self.config_manager.get_env_str('NLP_MODEL_DEPRESSION_NAME', 
                                                          'MoritzLaurer/deberta-v3-base-zeroshot-v2.0'),
                    'weight': self.config_manager.get_env_float('NLP_MODEL_DEPRESSION_WEIGHT', 0.4),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                },
                'sentiment': {
                    'name': self.config_manager.get_env_str('NLP_MODEL_SENTIMENT_NAME', 
                                                          'Lowerated/lm6-deberta-v3-topic-sentiment'),
                    'weight': self.config_manager.get_env_float('NLP_MODEL_SENTIMENT_WEIGHT', 0.3),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                },
                'emotional_distress': {
                    'name': self.config_manager.get_env_str('NLP_MODEL_DISTRESS_NAME', 
                                                          'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'),
                    'weight': self.config_manager.get_env_float('NLP_MODEL_DISTRESS_WEIGHT', 0.3),
                    'type': 'zero-shot-classification',
                    'pipeline_task': 'zero-shot-classification'
                }
            },
            'ensemble_mode': self.config_manager.get_env_str('NLP_ENSEMBLE_MODE', 'majority'),
            'hardware_settings': self._get_hardware_settings_from_env(),
            'validation': {
                'ensure_weights_sum_to_one': True,
                'fail_on_invalid_weights': True
            }
        }
    
    def _get_hardware_settings_from_env(self) -> Dict[str, Any]:
        """Get hardware settings from environment variables"""
        return {
            'device': self.config_manager.get_env_str('NLP_MODEL_DEVICE', 'auto'),
            'precision': self.config_manager.get_env_str('NLP_MODEL_PRECISION', 'float16'),
            'max_batch_size': self.config_manager.get_env_int('NLP_MODEL_MAX_BATCH_SIZE', 32),
            'inference_threads': self.config_manager.get_env_int('NLP_MODEL_INFERENCE_THREADS', 16),
            'max_memory': self.config_manager.get_env_str('NLP_MODEL_MAX_MEMORY', ''),
            'offload_folder': self.config_manager.get_env_str('NLP_MODEL_OFFLOAD_FOLDER', './models/offload')
        }
    
    def _get_device_config(self) -> str:
        """Get device configuration for AI models"""
        try:
            # Get device from hardware settings
            hardware_settings = self.get_hardware_settings()
            device = hardware_settings.get('device', 'auto')
            
            if device != 'auto':
                logger.debug(f"Using configured device: {device}")
                return device
            
            # Auto-detect best available device
            if TRANSFORMERS_AVAILABLE and torch.cuda.is_available():
                logger.debug("Auto-detected device: cuda")
                return 'cuda'
            else:
                logger.debug("Auto-detected device: cpu")
                return 'cpu'
                
        except Exception as e:
            logger.warning(f"Device config detection failed: {e}, using CPU")
            return 'cpu'
    
    def _validate_configuration(self) -> bool:
        """Validate model ensemble configuration"""
        try:
            if not self.config:
                logger.error("No configuration loaded")
                return False
            
            models = self.config.get('models', {})
            if not models:
                logger.warning("No models configured")
                return False
            
            # Validate individual models
            valid_models = 0
            total_weight = 0.0
            
            for model_type, model_config in models.items():
                try:
                    # Check model name
                    model_name = model_config.get('name', '').strip()
                    if not model_name:
                        logger.warning(f"{model_type}: No model name configured")
                        continue
                    
                    # Check and convert weight
                    weight = model_config.get('weight')
                    if weight is not None:
                        try:
                            weight = float(weight)
                            model_config['weight'] = weight  # Update with converted value
                            total_weight += weight
                        except (ValueError, TypeError) as e:
                            logger.warning(f"{model_type}: Invalid weight '{weight}': {e}")
                            continue
                    else:
                        logger.warning(f"{model_type}: No weight configured")
                        continue
                    
                    valid_models += 1
                    logger.debug(f"{model_type}: {model_name} (weight: {weight})")
                    
                except Exception as e:
                    logger.warning(f"{model_type}: Validation error: {e}")
                    continue
            
            # Overall validation
            if valid_models == 0:
                logger.error("No valid models found")
                return False
            
            # Weight validation (lenient)
            if total_weight <= 0:
                logger.warning(f"Invalid total weight: {total_weight}")
                return False
            
            weight_deviation = abs(total_weight - 1.0)
            if weight_deviation > 0.5:
                logger.warning(f"Weights sum to {total_weight:.3f}, ideally should be ~1.0, but continuing...")
            
            logger.info(f"Configuration validation passed: {valid_models}/{len(models)} models valid")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    # ========================================================================
    # PHASE 3: AI CLASSIFICATION METHODS - CORE IMPLEMENTATION
    # ========================================================================
    
    async def classify_with_zero_shot(self, text: str, labels: List[str], model_type: str, 
                                    hypothesis_template: str = "This text expresses {}.") -> Dict[str, Any]:
        """
        PHASE 3: PRIMARY AI classification method for EnsembleAnalysisHelper
        
        This method performs actual zero-shot classification using transformers models.
        EnsembleAnalysisHelper should call this instead of creating pipelines directly.
        
        Args:
            text: Text to classify
            labels: List of classification labels
            model_type: Model type (depression, sentiment, emotional_distress)
            hypothesis_template: Template for hypothesis generation
            
        Returns:
            Classification result with score, confidence, and metadata
        """
        try:
            if not TRANSFORMERS_AVAILABLE:
                logger.warning(f"⚠️ Transformers not available for {model_type} classification")
                return await self._pattern_fallback_classification(text, labels, model_type)
            
            # Get model configuration
            model_config = self.get_model_config(model_type)
            if not model_config:
                raise ValueError(f"No configuration found for model type: {model_type}")
            
            model_name = model_config.get('name')
            if not model_name:
                raise ValueError(f"No model name configured for type: {model_type}")
            
            # Load or get cached pipeline
            classifier = await self._get_or_load_pipeline(model_name)
            if classifier is None:
                logger.warning(f"⚠️ Could not load model {model_name}, using pattern fallback")
                return await self._pattern_fallback_classification(text, labels, model_type)
            
            # Perform zero-shot classification
            logger.debug(f"🤖 Running zero-shot classification: {model_type} with {model_name}")
            
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: classifier(text, labels)
            )
            
            # Process result into crisis score
            crisis_score = self._process_classification_result(result, labels)
            
            return {
                'score': crisis_score,
                'confidence': min(0.9, crisis_score + 0.1),
                'model': model_name,
                'model_type': model_type,
                'method': 'zero_shot_classification',
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'transformers_used': True,
                'device': self.device,
                'ensemble_manager': True
            }
            
        except Exception as e:
            logger.error(f"❌ Zero-shot classification failed for {model_type}: {e}")
            return await self._pattern_fallback_classification(text, labels, model_type)
    
    async def classify_with_ensemble(self, text: str, zero_shot_manager=None) -> Dict[str, Any]:
        """
        PHASE 3: Ensemble classification using multiple models
        
        Args:
            text: Text to classify
            zero_shot_manager: ZeroShotManager instance for label management
            
        Returns:
            Ensemble classification results
        """
        try:
            model_results = {}
            models = self.get_model_definitions()
            
            # Get labels from ZeroShotManager if available
            labels = None
            hypothesis_template = "This text expresses {}."
            
            if zero_shot_manager:
                try:
                    all_labels = zero_shot_manager.get_all_labels()
                    zero_shot_settings = zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', hypothesis_template)
                    logger.debug(f"✅ Using ZeroShotManager for label management")
                except Exception as e:
                    logger.warning(f"⚠️ ZeroShotManager access failed: {e}")
                    all_labels = {}
            else:
                all_labels = {}
            
            # Classify with each model
            for model_type in models.keys():
                try:
                    # Get labels for this model type
                    if isinstance(all_labels, dict) and model_type in all_labels:
                        model_labels = all_labels[model_type]
                    elif isinstance(all_labels, dict):
                        # Use general labels if model-specific not available
                        model_labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        model_labels = self._get_fallback_labels(model_type)
                    
                    if not model_labels:
                        model_labels = self._get_fallback_labels(model_type)
                    
                    # Perform classification
                    result = await self.classify_with_zero_shot(
                        text, model_labels, model_type, hypothesis_template
                    )
                    model_results[model_type] = result
                    
                except Exception as e:
                    logger.error(f"❌ Model {model_type} classification failed: {e}")
                    model_results[model_type] = {
                        'score': 0.0,
                        'confidence': 0.0,
                        'error': str(e),
                        'model_type': model_type
                    }
            
            # Perform ensemble voting
            ensemble_result = self._perform_ensemble_voting(model_results)
            
            return {
                'ensemble_score': ensemble_result['score'],
                'ensemble_confidence': ensemble_result['confidence'],
                'ensemble_mode': self.get_ensemble_mode(),
                'individual_results': model_results,
                'models_used': len(model_results),
                'zero_shot_manager_used': zero_shot_manager is not None,
                'method': 'ensemble_classification'
            }
            
        except Exception as e:
            logger.error(f"❌ Ensemble classification failed: {e}")
            return {
                'ensemble_score': 0.0,
                'ensemble_confidence': 0.0,
                'error': str(e),
                'method': 'ensemble_classification_error'
            }
    
    async def _get_or_load_pipeline(self, model_name: str):
        """
        PHASE 3: Load or get cached zero-shot classification pipeline
        
        Args:
            model_name: Hugging Face model name
            
        Returns:
            Zero-shot classification pipeline or None if loading fails
        """
        if not TRANSFORMERS_AVAILABLE:
            return None
            
        async with self._model_loading_lock:
            # Check cache first
            if model_name in self._model_cache:
                logger.debug(f"📦 Using cached model: {model_name}")
                return self._model_cache[model_name]
            
            try:
                logger.info(f"🔥 Loading zero-shot model: {model_name}")
                
                # Get cache directory
                cache_dir = self._get_model_cache_dir()
                
                # Create pipeline with proper configuration
                classifier = pipeline(
                    "zero-shot-classification",
                    model=model_name,
                    device=0 if self.device == 'cuda' else -1,
                    cache_dir=cache_dir,
                    return_all_scores=True
                )
                
                # Cache the pipeline
                self._model_cache[model_name] = classifier
                
                logger.info(f"✅ Model loaded successfully: {model_name}")
                return classifier
                
            except Exception as e:
                logger.error(f"❌ Failed to load model {model_name}: {e}")
                return None
    
    def _get_model_cache_dir(self) -> str:
        """Get model cache directory from configuration"""
        try:
            # First check individual model cache directories
            models = self.get_model_definitions()
            if models:
                # Use cache_dir from any model (they should all be the same)
                for model_type, model_config in models.items():
                    cache_dir = model_config.get('cache_dir')
                    if cache_dir and cache_dir.strip():
                        os.makedirs(cache_dir, exist_ok=True)
                        logger.debug(f"Using model cache directory: {cache_dir}")
                        return cache_dir
            
            # Check ensemble_config cache_dir
            try:
                cache_dir = self.config_manager.get_config_section('model_ensemble', 'ensemble_config.cache_dir')
                if cache_dir and cache_dir.strip():
                    os.makedirs(cache_dir, exist_ok=True)
                    logger.debug(f"Using ensemble config cache directory: {cache_dir}")
                    return cache_dir
            except Exception as e:
                logger.debug(f"Ensemble config cache dir access failed: {e}")
            
            # Check hardware_settings cache_dir
            cache_dir = self.config_manager.get_config_section('model_ensemble', 'hardware_settings.cache_dir')
            if cache_dir and cache_dir.strip():
                os.makedirs(cache_dir, exist_ok=True)
                logger.debug(f"Using hardware settings cache directory: {cache_dir}")
                return cache_dir
            
            # Final fallback
            fallback_dir = './models/cache/'
            os.makedirs(fallback_dir, exist_ok=True)
            logger.warning(f"Using fallback cache directory: {fallback_dir}")
            return fallback_dir
            
        except Exception as e:
            logger.warning(f"Cache dir config failed: {e}")
            fallback_dir = './models/cache/'
            try:
                os.makedirs(fallback_dir, exist_ok=True)
            except Exception as e2:
                logger.error(f"Could not create fallback cache directory {fallback_dir}: {e2}")
            return fallback_dir
    
    def _process_classification_result(self, result: Dict, labels: List[str]) -> float:
        """
        PHASE 3: Process zero-shot classification result into crisis score
        
        Args:
            result: Raw result from zero-shot classifier
            labels: Original labels used for classification
            
        Returns:
            Crisis score (0.0 to 1.0) where higher values indicate higher crisis levels
        """
        try:
            if not result or 'scores' not in result:
                logger.warning(f"⚠️ Invalid classification result format")
                return 0.0
            
            scores = result['scores']
            predicted_labels = result.get('labels', [])
            
            if len(scores) != len(labels):
                logger.warning(f"⚠️ Score/label mismatch in classification result")
                return 0.0
            
            # Calculate weighted crisis score based on label severity
            # Labels are arranged from highest crisis (index 0) to lowest crisis (last index)
            crisis_score = 0.0
            
            for i, (label, score) in enumerate(zip(predicted_labels, scores)):
                try:
                    original_index = labels.index(label)
                    # Convert index to severity weight (0 = highest crisis, last = lowest crisis)
                    severity_weight = 1.0 - (original_index / (len(labels) - 1))
                    weighted_contribution = score * severity_weight
                    crisis_score += weighted_contribution
                    
                    logger.debug(f"📊 Label: score={score:.3f}, weight={severity_weight:.3f}")
                    
                except ValueError:
                    logger.warning(f"⚠️ Label '{label}' not found in original labels")
                    continue
            
            # Normalize the score to 0-1 range
            crisis_score = max(0.0, min(1.0, crisis_score))
            
            logger.debug(f"📊 Final crisis score: {crisis_score:.3f}")
            return crisis_score
            
        except Exception as e:
            logger.error(f"❌ Classification result processing failed: {e}")
            return 0.0
    
    def _perform_ensemble_voting(self, model_results: Dict[str, Dict]) -> Dict[str, float]:
        """
        PHASE 3: Perform ensemble voting on multiple model results
        
        Args:
            model_results: Dictionary of model results
            
        Returns:
            Ensemble score and confidence
        """
        try:
            ensemble_mode = self.get_ensemble_mode()
            valid_results = []
            
            # Extract valid results
            for model_type, result in model_results.items():
                if isinstance(result, dict) and 'score' in result:
                    score = result.get('score', 0.0)
                    confidence = result.get('confidence', 0.0)
                    weight = self.get_model_weight(model_type)
                    
                    valid_results.append({
                        'score': score,
                        'confidence': confidence,
                        'weight': weight,
                        'model_type': model_type
                    })
            
            if not valid_results:
                return {'score': 0.0, 'confidence': 0.0}
            
            # Perform voting based on ensemble mode
            if ensemble_mode == 'weighted':
                return self._weighted_ensemble_voting(valid_results)
            elif ensemble_mode == 'majority':
                return self._majority_ensemble_voting(valid_results)
            elif ensemble_mode == 'consensus':
                return self._consensus_ensemble_voting(valid_results)
            else:
                # Default to weighted
                return self._weighted_ensemble_voting(valid_results)
                
        except Exception as e:
            logger.error(f"❌ Ensemble voting failed: {e}")
            return {'score': 0.0, 'confidence': 0.0}
    
    def _weighted_ensemble_voting(self, results: List[Dict]) -> Dict[str, float]:
        """Weighted ensemble voting"""
        total_weight = sum(r['weight'] for r in results)
        if total_weight == 0:
            return {'score': 0.0, 'confidence': 0.0}
        
        weighted_score = sum(r['score'] * r['weight'] for r in results) / total_weight
        weighted_confidence = sum(r['confidence'] * r['weight'] for r in results) / total_weight
        
        return {'score': weighted_score, 'confidence': weighted_confidence}
    
    def _majority_ensemble_voting(self, results: List[Dict]) -> Dict[str, float]:
        """Majority ensemble voting"""
        if not results:
            return {'score': 0.0, 'confidence': 0.0}
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        return {'score': avg_score, 'confidence': avg_confidence}
    
    def _consensus_ensemble_voting(self, results: List[Dict]) -> Dict[str, float]:
        """Consensus ensemble voting"""
        if not results:
            return {'score': 0.0, 'confidence': 0.0}
        
        # For consensus, require agreement (similar scores)
        scores = [r['score'] for r in results]
        score_std = (sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores))**0.5
        
        if score_std > 0.3:  # High disagreement
            consensus_confidence = 0.3
        else:
            consensus_confidence = 0.8
        
        avg_score = sum(scores) / len(scores)
        return {'score': avg_score, 'confidence': consensus_confidence}
    
    async def _pattern_fallback_classification(self, text: str, labels: List[str], model_type: str) -> Dict[str, Any]:
        """
        PHASE 3: Pattern-based fallback when transformers unavailable
        
        Args:
            text: Text to classify
            labels: Classification labels
            model_type: Model type for context
            
        Returns:
            Pattern-based classification result
        """
        try:
            # Simple pattern-based classification
            text_lower = text.lower()
            crisis_keywords = ['suicide', 'suicidal', 'hopeless', 'helpless', 'crisis', 'breakdown']
            
            matches = sum(1 for keyword in crisis_keywords if keyword in text_lower)
            score = min(0.7, matches * 0.15)
            
            return {
                'score': score,
                'confidence': 0.5,
                'model': f'pattern_fallback_{model_type}',
                'model_type': model_type,
                'method': 'pattern_fallback',
                'labels_used': len(labels),
                'transformers_used': False,
                'ensemble_manager': True
            }
            
        except Exception as e:
            logger.error(f"❌ Pattern fallback failed: {e}")
            return {
                'score': 0.0,
                'confidence': 0.0,
                'error': str(e),
                'model_type': model_type,
                'method': 'pattern_fallback_error'
            }
    
    def _get_fallback_labels(self, model_type: str) -> List[str]:
        """Get fallback labels for a model type"""
        fallback_labels = {
            'depression': [
                "person expressing suicidal thoughts or plans",
                "person showing severe depression",
                "person feeling emotionally stable"
            ],
            'sentiment': [
                "extreme sadness or despair",
                "neutral emotions",
                "happiness or joy"
            ],
            'emotional_distress': [
                "person in acute psychological distress",
                "person showing moderate distress",
                "person demonstrating emotional resilience"
            ]
        }
        
        return fallback_labels.get(model_type, [
            "high crisis level",
            "medium crisis level", 
            "low crisis level"
        ])
    
    # ========================================================================
    # EXISTING CONFIGURATION METHODS (Keep unchanged)
    # ========================================================================
    
    def get_model_definitions(self) -> Dict[str, Any]:
        """Get all model definitions"""
        return self.config.get('models', {})
    
    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get configuration for specific model type"""
        return self.get_model_definitions().get(model_type, {})
    
    def get_model_name(self, model_type: str) -> str:
        """Get model name for specific model type"""
        return self.get_model_config(model_type).get('name', '')
    
    def get_model_weight(self, model_type: str) -> float:
        """Get model weight for specific model type"""
        return self.get_model_config(model_type).get('weight', 0.0)
    
    def get_model_weights(self) -> Dict[str, float]:
        """Get all model weights as dictionary"""
        models = self.get_model_definitions()
        return {model_type: model.get('weight', 0.0) for model_type, model in models.items()}
    
    def get_normalized_weights(self) -> Dict[str, float]:
        """Get normalized model weights (sum to 1.0)"""
        weights = self.get_model_weights()
        total_weight = sum(weights.values())
        
        if total_weight <= 0:
            equal_weight = 1.0 / len(weights) if weights else 0.0
            return {model_type: equal_weight for model_type in weights.keys()}
        
        return {model_type: weight / total_weight for model_type, weight in weights.items()}
    
    def get_model_names(self) -> List[str]:
        """Get list of configured model names"""
        return list(self.get_model_definitions().keys())
    
    def get_ensemble_mode(self) -> str:
        """Get current ensemble mode"""
        return self.config.get('ensemble_mode', 'majority')
    
    def get_ensemble_settings(self) -> Dict[str, Any]:
        """Get ensemble settings including validation"""
        return {
            'mode': self.get_ensemble_mode(),
            'validation': self.config.get('validation', {})
        }
    
    def validate_ensemble_mode(self, mode: str) -> bool:
        """Validate if an ensemble mode is supported"""
        available_modes = ['consensus', 'majority', 'weighted']
        return mode in available_modes
    
    def get_hardware_settings(self) -> Dict[str, Any]:
        """Get hardware configuration settings"""
        return self.config.get('hardware_settings', {})
    
    def get_device_setting(self) -> str:
        """Get device setting (auto/cpu/cuda)"""
        return self.get_hardware_settings().get('device', 'auto')
    
    def get_precision_setting(self) -> str:
        """Get precision setting (float16/float32)"""
        return self.get_hardware_settings().get('precision', 'float16')
    
    def get_max_batch_size(self) -> int:
        """Get maximum batch size"""
        return self.get_hardware_settings().get('max_batch_size', 32)
    
    def get_inference_threads(self) -> int:
        """Get inference thread count"""
        return self.get_hardware_settings().get('inference_threads', 16)
    
    def models_loaded(self) -> bool:
        """Check if models are configured and ready for analysis"""
        try:
            models = self.get_model_definitions()
            if not models:
                logger.warning("No models configured")
                return False
            
            if len(models) < 2:
                logger.warning(f"Only {len(models)} models configured, need at least 2")
                return False
            
            models_with_names = 0
            for model_type, model_config in models.items():
                model_name = model_config.get('name', '').strip()
                if model_name:
                    models_with_names += 1
            
            if models_with_names == 0:
                logger.warning("No models have valid names configured")
                return False
            
            weights = self.get_model_weights()
            total_weight = sum(weights.values())
            
            if total_weight <= 0:
                logger.warning(f"Invalid total weight: {total_weight}")
                return False
            
            logger.debug(f"Models validation passed: {models_with_names}/{len(models)} models with valid names")
            return True
            
        except Exception as e:
            logger.error(f"Error checking models_loaded status: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information for API responses"""
        try:
            models = self.get_model_definitions()
            
            model_info = {
                'total_models': len(models),
                'models_configured': len(models) > 0,
                'architecture_version': '3.1e-5.5-7-3-phase3',
                'configuration_source': 'unified_config_manager',
                'ensemble_mode': self.get_ensemble_mode(),
                'device_setting': self.get_device_setting(),
                'precision_setting': self.get_precision_setting(),
                'model_details': {},
                'phase_3_ai_methods': True,
                'transformers_available': TRANSFORMERS_AVAILABLE
            }
            
            try:
                weights = self.get_model_weights()
                model_info['total_weight'] = sum(weights.values())
                model_info['weights_valid'] = abs(sum(weights.values()) - 1.0) < 0.5
            except Exception as e:
                logger.warning(f"Could not get model weights: {e}")
                model_info['total_weight'] = 0.0
                model_info['weights_valid'] = False
            
            for model_type, model_config in models.items():
                try:
                    model_info['model_details'][model_type] = {
                        'name': model_config.get('name', ''),
                        'weight': model_config.get('weight', 0.0),
                        'type': model_config.get('type', ''),
                        'pipeline_task': model_config.get('pipeline_task', 'text-classification'),
                        'configured': bool(model_config.get('name', '').strip())
                    }
                except Exception as e:
                    logger.warning(f"Error processing model {model_type}: {e}")
                    model_info['model_details'][model_type] = {
                        'error': str(e),
                        'configured': False
                    }
            
            model_info['status'] = {
                'models_loaded': self.models_loaded(),
                'ready_for_analysis': len(models) >= 2,
                'ai_classification_available': TRANSFORMERS_AVAILABLE
            }
            
            logger.debug(f"Model info generated successfully: {len(models)} models")
            return model_info
            
        except Exception as e:
            logger.error(f"Error generating model info: {e}")
            return {
                'total_models': 0,
                'models_configured': False,
                'status': 'error',
                'error': str(e),
                'architecture_version': '3.1e-5.5-7-3-phase3',
                'ready_for_analysis': False
            }
    
    def get_validation_settings(self) -> Dict[str, Any]:
        """Get validation settings"""
        return self.config.get('validation', {})
    
    def is_weights_validation_enabled(self) -> bool:
        """Check if weight validation is enabled"""
        return self.get_validation_settings().get('ensure_weights_sum_to_one', True)
    
    def get_zero_shot_capabilities(self) -> Dict[str, Any]:
        """Get information about zero-shot classification capabilities"""
        try:
            zero_shot_model = self._get_best_zero_shot_model()
            
            capabilities = {
                'zero_shot_available': zero_shot_model is not None,
                'zero_shot_model': zero_shot_model,
                'semantic_pattern_matching': zero_shot_model is not None,
                'classification_method': 'transformers_pipeline' if zero_shot_model else 'keyword_fallback',
                'transformers_available': TRANSFORMERS_AVAILABLE,
                'phase_3_implementation': True
            }
            
            if zero_shot_model:
                model_config = self.get_model_config(zero_shot_model)
                capabilities['model_details'] = {
                    'name': model_config.get('name', ''),
                    'type': model_config.get('type', ''),
                    'pipeline_task': model_config.get('pipeline_task', '')
                }
            
            return capabilities
            
        except Exception as e:
            logger.error(f"Error getting zero-shot capabilities: {e}")
            return {'zero_shot_available': False, 'error': str(e)}
    
    def _get_best_zero_shot_model(self) -> Optional[str]:
        """Find the best available zero-shot classification model"""
        try:
            models = self.get_model_definitions()
            
            for model_type, model_config in models.items():
                pipeline_task = model_config.get('pipeline_task', '')
                if pipeline_task == 'zero-shot-classification':
                    return model_type
            
            for model_type, model_config in models.items():
                model_name = model_config.get('name', '').lower()
                if 'nli' in model_name or 'mnli' in model_name:
                    return model_type
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding zero-shot model: {e}")
            return None
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status"""
        try:
            models = self.get_model_definitions()
            weights = self.get_model_weights()
            
            return {
                'version': '3.1e-5.5-7-3-phase3',
                'architecture': 'clean-v3.1-unified',
                'phase_3_implementation': True,
                'ai_classification_methods': True,
                'config_source': 'enhanced_config_manager',
                'ensemble_mode': self.get_ensemble_mode(),
                'models_configured': len(models),
                'model_types': list(models.keys()),
                'total_weight': sum(weights.values()),
                'weights_normalized': abs(sum(weights.values()) - 1.0) < 0.01,
                'hardware_device': self.get_device_setting(),
                'validation_enabled': self.is_weights_validation_enabled(),
                'transformers_available': TRANSFORMERS_AVAILABLE,
                'cache_initialized': hasattr(self, '_model_cache'),
                'methods_available': [
                    'classify_with_zero_shot',
                    'classify_with_ensemble',
                    '_get_or_load_pipeline',
                    '_process_classification_result',
                    '_perform_ensemble_voting'
                ]
            }
        except Exception as e:
            logger.error(f"Error getting manager status: {e}")
            return {
                'version': '3.1e-5.5-7-3-phase3',
                'status': 'error',
                'error': str(e)
            }


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_model_ensemble_manager(config_manager) -> ModelEnsembleManager:
    """
    Factory function to create ModelEnsembleManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        ModelEnsembleManager instance
    """
    return ModelEnsembleManager(config_manager)

# ============================================================================
# BACKWARD COMPATIBILITY - Global Instance Management
# ============================================================================

_model_ensemble_manager = None

def get_model_ensemble_manager(config_manager=None) -> ModelEnsembleManager:
    """
    Get the global model ensemble manager instance - LEGACY COMPATIBILITY
    
    Args:
        config_manager: UnifiedConfigManager instance (optional for compatibility)
        
    Returns:
        ModelEnsembleManager instance
    """
    global _model_ensemble_manager
    
    if _model_ensemble_manager is None:
        if config_manager is None:
            logger.info("Creating UnifiedConfigManager for ModelEnsembleManager compatibility")
            from managers.unified_config_manager import create_unified_config_manager
            config_manager = create_unified_config_manager()
        
        _model_ensemble_manager = ModelEnsembleManager(config_manager)
    
    return _model_ensemble_manager

def reset_model_ensemble_manager():
    """Reset the global manager instance - for testing"""
    global _model_ensemble_manager
    _model_ensemble_manager = None

__all__ = [
    'ModelEnsembleManager', 
    'create_model_ensemble_manager',
    'get_model_ensemble_manager', 
    'reset_model_ensemble_manager'
]

logger.info("ModelEnsembleManager v3.1e-5.5-7-3 Phase 3 loaded - AI classification methods implemented")