# ash/ash-nlp/models/ml_models.py (Clean Manager-Only Architecture)
"""
Enhanced ModelManager with clean manager-only architecture for Ash NLP Service v3.1
No backward compatibility - requires ConfigManager integration
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import logging
import torch
from typing import Dict, Any, Optional, List
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import asyncio

logger = logging.getLogger(__name__)

class ModelManager:
    """Clean ModelManager with manager-only architecture"""
    
    def __init__(self, config_manager, model_config: Dict[str, Any], hardware_config: Dict[str, Any]):
        """
        Initialize ModelManager with clean manager architecture
        
        Args:
            config_manager: ConfigManager instance for dynamic configuration access
            model_config: Model configuration dictionary from ConfigManager
            hardware_config: Hardware configuration dictionary from ConfigManager
        """
        if config_manager is None:
            raise ValueError("ConfigManager is required - no backward compatibility support")
        
        self.config_manager = config_manager
        self.model_config = model_config
        self.hardware_config = hardware_config
        
        # Model storage
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        
        # Configuration extraction
        self.models_config = self.model_config.get('models', {})
        self.ensemble_config = self.model_config.get('ensemble_config', {})
        
        # Hardware settings
        self.device = self._determine_device()
        self.model_cache_dir = self._get_cache_directory()
        self.precision = self._get_model_precision()
        
        # Performance settings
        perf_settings = self.hardware_config.get('performance_settings', {})
        self.max_batch_size = perf_settings.get('max_batch_size', 32)
        self.max_concurrent_requests = perf_settings.get('max_concurrent_requests', 20)
        self.inference_threads = perf_settings.get('inference_threads', 16)
        self.request_timeout = perf_settings.get('request_timeout', 40)
        
        logger.info("✅ Enhanced ModelManager initialized with clean manager architecture")
        logger.info(f"Device: {self.device}")
        logger.info(f"Model cache directory: {self.model_cache_dir}")
        logger.info(f"Model precision: {self.precision}")
        logger.info(f"Performance settings: batch_size={self.max_batch_size}, threads={self.inference_threads}")
        
        # Validate configuration
        self._validate_configuration()
    
    def _determine_device(self) -> str:
        """Determine the device to use for models with manager integration"""
        device_config = self.hardware_config.get('device', 'auto')
        
        if device_config == 'auto':
            if torch.cuda.is_available():
                device = 'cuda'
                logger.info("💻 Auto-detected CUDA GPU")
            else:
                device = 'cpu'
                logger.info("💻 Auto-detected CPU (CUDA not available)")
        else:
            device = device_config
            logger.info(f"💻 Using configured device: {device}")
        
        return device
    
    def _get_cache_directory(self) -> str:
        """Get model cache directory from configuration"""
        cache_config = self.hardware_config.get('memory_optimization', {})
        cache_dir = cache_config.get('cache_dir', './models/cache')
        
        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)
        logger.info(f"📁 Model cache directory configured: {cache_dir}")
        
        return cache_dir
    
    def _get_model_precision(self) -> str:
        """Get model precision from configuration"""
        precision = self.hardware_config.get('precision', 'float16')
        logger.info(f"🔢 Model precision: {precision}")
        return precision
    
    def _validate_configuration(self):
        """Validate model configuration with manager integration"""
        logger.info("🔍 Validating model configuration...")
        
        # Use ConfigManager for validation
        validation_result = self.config_manager.validate_configuration()
        
        if not validation_result['valid']:
            error_msg = f"Model configuration validation failed: {validation_result['errors']}"
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        # Log warnings
        for warning in validation_result['warnings']:
            logger.warning(f"⚠️ Configuration warning: {warning}")
        
        # Additional ModelManager-specific validation
        required_models = ['depression', 'sentiment', 'emotional_distress']
        
        for model_type in required_models:
            if model_type not in self.models_config:
                error_msg = f"Missing required model configuration: {model_type}"
                logger.error(f"❌ {error_msg}")
                raise ValueError(error_msg)
            
            model_info = self.models_config[model_type]
            if not model_info.get('name'):
                error_msg = f"No model name specified for {model_type}"
                logger.error(f"❌ {error_msg}")
                raise ValueError(error_msg)
        
        logger.info("✅ Model configuration validation passed")
    
    def _get_huggingface_token(self) -> Optional[str]:
        """Get Hugging Face token from secrets or environment"""
        hf_token = os.getenv('GLOBAL_HUGGINGFACE_TOKEN')
        
        if hf_token and hf_token.startswith('/run/secrets/'):
            try:
                with open(hf_token, 'r') as f:
                    token = f.read().strip()
                logger.info("🔑 Hugging Face token loaded from secrets")
                return token
            except Exception as e:
                logger.warning(f"⚠️ Could not read HF token from secrets: {e}")
                return None
        elif hf_token:
            logger.info("🔑 Hugging Face token loaded from environment")
            return hf_token
        else:
            logger.warning("⚠️ No Hugging Face token found")
            return None
    
    async def load_models(self):
        """Load all models with clean manager architecture"""
        logger.info("🚀 Starting model loading with manager configuration...")
        
        hf_token = self._get_huggingface_token()
        
        # Get torch dtype based on precision setting
        if self.precision == 'float16' and self.device == 'cuda':
            torch_dtype = torch.float16
            logger.info("🔢 Using float16 precision for CUDA")
        elif self.precision == 'float32' or self.device == 'cpu':
            torch_dtype = torch.float32
            logger.info("🔢 Using float32 precision")
        else:
            torch_dtype = 'auto'
            logger.info("🔢 Using auto precision")
        
        # Load each model based on processed configuration
        for model_type, model_config in self.models_config.items():
            model_name = model_config['name']
            model_weight = model_config['weight']
            
            logger.info(f"📦 Loading {model_type} model: {model_name} (weight: {model_weight})")
            
            try:
                # Load tokenizer
                tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    cache_dir=self.model_cache_dir,
                    token=hf_token,
                    trust_remote_code=False
                )
                
                # Load model
                model = AutoModelForSequenceClassification.from_pretrained(
                    model_name,
                    cache_dir=self.model_cache_dir,
                    token=hf_token,
                    torch_dtype=torch_dtype,
                    trust_remote_code=False
                )
                
                # Move model to device
                if self.device == 'cuda' and torch.cuda.is_available():
                    model = model.to('cuda')
                    device_id = 0
                    logger.info(f"Device set to use {self.device}")
                else:
                    device_id = -1
                    logger.info(f"Device set to use cpu")
                
                # Create pipeline with configuration
                pipeline_task = model_config.get('pipeline_task', 'zero-shot-classification')
                pipeline_kwargs = model_config.get('pipeline_kwargs', {})
                
                # Set device in pipeline kwargs
                pipeline_kwargs['device'] = device_id
                pipeline_kwargs['return_all_scores'] = True
                
                pipe = pipeline(
                    pipeline_task,
                    model=model,
                    tokenizer=tokenizer,
                    **pipeline_kwargs
                )
                
                # Store components
                self.models[model_type] = model
                self.tokenizers[model_type] = tokenizer
                self.pipelines[model_type] = pipe
                
                logger.info(f"✅ {model_type.title()} model loaded successfully")
                
            except Exception as e:
                error_msg = f"Failed to load {model_type} model ({model_name}): {e}"
                logger.error(f"❌ {error_msg}")
                raise RuntimeError(error_msg)
        
        logger.info("🎯 All three models loaded successfully with manager configuration")
        
        # Log final model summary
        self._log_model_summary()
    
    def _log_model_summary(self):
        """Log summary of loaded models"""
        logger.info("📊 Model Loading Summary:")
        
        total_weight = 0.0
        for model_type, model_config in self.models_config.items():
            weight = model_config['weight']
            total_weight += weight
            
            loaded_status = "✅" if model_type in self.pipelines else "❌"
            logger.info(f"   {model_type.title()}: {loaded_status}")
            logger.info(f"     Model: {model_config['name']}")
            logger.info(f"     Weight: {weight}")
            logger.info(f"     Type: {model_config.get('type', 'Unknown')}")
        
        logger.info(f"   Total Weight: {total_weight}")
        logger.info(f"   Ensemble Mode: {self.ensemble_config.get('default_mode', 'majority')}")
        logger.info(f"   Models Loaded: {len(self.pipelines)}/3")
    
    def models_loaded(self) -> bool:
        """Check if all required models are loaded"""
        required_models = ['depression', 'sentiment', 'emotional_distress']
        loaded = all(model_type in self.pipelines for model_type in required_models)
        
        if loaded:
            logger.debug("✅ All required models are loaded")
        else:
            missing = [m for m in required_models if m not in self.pipelines]
            logger.warning(f"⚠️ Missing models: {missing}")
        
        return loaded
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive information about loaded models"""
        ensemble_mode = self.config_manager.get_ensemble_mode()
        feature_flags = self.config_manager.get_feature_flags()
        
        return {
            'models_loaded': self.models_loaded(),
            'model_count': len(self.pipelines),
            'models': {
                model_type: {
                    'name': self.models_config[model_type]['name'],
                    'weight': self.models_config[model_type]['weight'],
                    'type': self.models_config[model_type].get('type', 'Unknown'),
                    'loaded': model_type in self.pipelines,
                    'purpose': self.models_config[model_type].get('purpose', '')
                }
                for model_type in self.models_config.keys()
            },
            'ensemble_configuration': {
                'mode': ensemble_mode,
                'gap_detection_enabled': feature_flags.get('experimental_features', {}).get('enable_gap_detection', True),
                'confidence_spreading_enabled': feature_flags.get('experimental_features', {}).get('enable_confidence_spreading', True)
            },
            'hardware_configuration': {
                'device': self.device,
                'precision': self.precision,
                'cache_dir': self.model_cache_dir,
                'max_batch_size': self.max_batch_size,
                'max_concurrent_requests': self.max_concurrent_requests
            },
            'manager_architecture': 'clean_v3.1'
        }
    
    async def analyze_with_ensemble(self, text: str, labels: List[str]) -> Dict[str, Any]:
        """
        Analyze text with all models in ensemble using manager configuration
        
        Args:
            text: Text to analyze
            labels: List of labels for zero-shot classification
            
        Returns:
            Dictionary with individual model results and ensemble analysis
        """
        if not self.models_loaded():
            raise RuntimeError("Models not loaded - cannot perform analysis")
        
        logger.debug(f"🔍 Analyzing text with {len(self.pipelines)} models")
        
        results = {}
        
        # Run each model
        for model_type, pipeline in self.pipelines.items():
            try:
                logger.debug(f"Running {model_type} model analysis...")
                
                # Get model result
                result = pipeline(text, labels)
                
                # Process result consistently
                processed_result = self._process_model_result(result, model_type)
                
                results[model_type] = {
                    'model_name': self.models_config[model_type]['name'],
                    'weight': self.models_config[model_type]['weight'],
                    'type': self.models_config[model_type].get('type', 'Unknown'),
                    'result': processed_result
                }
                
                logger.debug(f"✅ {model_type} analysis complete: {processed_result.get('prediction')} ({processed_result.get('confidence', 0):.3f})")
                
            except Exception as e:
                logger.error(f"❌ Error in {model_type} model analysis: {e}")
                results[model_type] = {
                    'model_name': self.models_config[model_type]['name'],
                    'weight': self.models_config[model_type]['weight'],
                    'type': self.models_config[model_type].get('type', 'Unknown'),
                    'result': {
                        'labels': [],
                        'scores': [],
                        'prediction': None,
                        'confidence': 0.0,
                        'error': str(e)
                    }
                }
        
        # Calculate ensemble consensus using manager configuration
        ensemble_result = self._calculate_ensemble_consensus(results)
        
        # Get gap detection analysis
        gap_analysis = self._analyze_model_gaps(results)
        
        return {
            'individual_results': results,
            'ensemble_result': ensemble_result,
            'gap_analysis': gap_analysis,
            'ensemble_mode': self.config_manager.get_ensemble_mode(),
            'model_info': self.get_model_info(),
            'analysis_metadata': {
                'text_length': len(text),
                'labels_count': len(labels),
                'timestamp': int(torch.tensor(0).item()),  # Simple timestamp
                'manager_version': 'clean_v3.1'
            }
        }
    
    def _process_model_result(self, result: Any, model_type: str) -> Dict[str, Any]:
        """Process model result into consistent format"""
        try:
            if isinstance(result, dict):
                return {
                    'labels': result.get('labels', []),
                    'scores': result.get('scores', []),
                    'prediction': result.get('labels', [None])[0] if result.get('labels') else None,
                    'confidence': max(result.get('scores', [0])) if result.get('scores') else 0.0
                }
            elif isinstance(result, list) and len(result) > 0:
                best_result = result[0] if result else {}
                return {
                    'labels': [item.get('label', '') for item in result],
                    'scores': [item.get('score', 0.0) for item in result],
                    'prediction': best_result.get('label'),
                    'confidence': best_result.get('score', 0.0)
                }
            else:
                logger.warning(f"⚠️ Unexpected result format from {model_type}: {type(result)}")
                return {
                    'labels': [],
                    'scores': [],
                    'prediction': None,
                    'confidence': 0.0,
                    'error': f'Unexpected result format: {type(result)}'
                }
        except Exception as e:
            logger.error(f"❌ Error processing {model_type} result: {e}")
            return {
                'labels': [],
                'scores': [],
                'prediction': None,
                'confidence': 0.0,
                'error': f'Result processing error: {e}'
            }
    
    def _calculate_ensemble_consensus(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ensemble consensus using manager configuration"""
        ensemble_mode = self.config_manager.get_ensemble_mode()
        
        logger.debug(f"🔄 Calculating ensemble consensus using {ensemble_mode} mode")
        
        if ensemble_mode == 'weighted':
            return self._weighted_consensus(results)
        elif ensemble_mode == 'consensus':
            return self._unanimous_consensus(results)
        else:  # majority (default)
            return self._majority_consensus(results)
    
    def _majority_consensus(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate majority voting consensus"""
        predictions = {}
        total_confidence = 0.0
        valid_results = 0
        
        for model_type, model_result in results.items():
            prediction = model_result['result'].get('prediction')
            confidence = model_result['result'].get('confidence', 0.0)
            
            if prediction and not model_result['result'].get('error'):
                predictions[prediction] = predictions.get(prediction, 0) + 1
                total_confidence += confidence
                valid_results += 1
        
        if not predictions:
            return {
                'consensus_prediction': 'unknown',
                'consensus_confidence': 0.0,
                'agreement_level': 'no_valid_results',
                'method': 'majority',
                'requires_review': True
            }
        
        # Get majority prediction
        consensus_prediction = max(predictions, key=predictions.get)
        agreement_count = predictions[consensus_prediction]
        agreement_level = agreement_count / len(results) if results else 0.0
        
        return {
            'consensus_prediction': consensus_prediction,
            'consensus_confidence': total_confidence / valid_results if valid_results > 0 else 0.0,
            'agreement_level': agreement_level,
            'agreement_count': f"{agreement_count}/{len(results)}",
            'method': 'majority',
            'prediction_counts': predictions,
            'requires_review': agreement_level < 0.67  # Less than 2/3 agreement
        }
    
    def _weighted_consensus(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate weighted consensus based on model weights"""
        weighted_scores = {}
        total_weight = 0.0
        
        for model_type, model_result in results.items():
            if model_result['result'].get('error'):
                continue
                
            weight = model_result['weight']
            prediction = model_result['result'].get('prediction')
            confidence = model_result['result'].get('confidence', 0.0)
            
            if prediction:
                weighted_score = weight * confidence
                weighted_scores[prediction] = weighted_scores.get(prediction, 0.0) + weighted_score
                total_weight += weight
        
        if not weighted_scores:
            return {
                'consensus_prediction': 'unknown',
                'consensus_confidence': 0.0,
                'agreement_level': 'no_valid_results',
                'method': 'weighted',
                'requires_review': True
            }
        
        # Get highest weighted prediction
        consensus_prediction = max(weighted_scores, key=weighted_scores.get)
        consensus_confidence = weighted_scores[consensus_prediction] / total_weight if total_weight > 0 else 0.0
        
        return {
            'consensus_prediction': consensus_prediction,
            'consensus_confidence': consensus_confidence,
            'agreement_level': weighted_scores[consensus_prediction] / sum(weighted_scores.values()) if weighted_scores else 0.0,
            'method': 'weighted',
            'weighted_scores': weighted_scores,
            'total_weight': total_weight,
            'requires_review': consensus_confidence < 0.5
        }
    
    def _unanimous_consensus(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate unanimous consensus (all models must agree)"""
        predictions = set()
        confidences = []
        
        for model_type, model_result in results.items():
            if model_result['result'].get('error'):
                continue
                
            prediction = model_result['result'].get('prediction')
            confidence = model_result['result'].get('confidence', 0.0)
            
            if prediction:
                predictions.add(prediction)
                confidences.append(confidence)
        
        if len(predictions) == 1:
            # Unanimous agreement
            consensus_prediction = list(predictions)[0]
            consensus_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            agreement_level = 1.0
            requires_review = False
        else:
            # No unanimous agreement
            consensus_prediction = 'disagreement'
            consensus_confidence = 0.0
            agreement_level = 0.0
            requires_review = True
        
        return {
            'consensus_prediction': consensus_prediction,
            'consensus_confidence': consensus_confidence,
            'agreement_level': agreement_level,
            'method': 'consensus',
            'unique_predictions': len(predictions),
            'requires_review': requires_review
        }
    
    def _analyze_model_gaps(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze gaps and disagreements between models"""
        feature_flags = self.config_manager.get_feature_flags()
        gap_detection_enabled = feature_flags.get('experimental_features', {}).get('enable_gap_detection', True)
        
        if not gap_detection_enabled:
            return {'gap_detection': 'disabled'}
        
        predictions = []
        confidences = []
        
        for model_type, model_result in results.items():
            if not model_result['result'].get('error'):
                prediction = model_result['result'].get('prediction')
                confidence = model_result['result'].get('confidence', 0.0)
                if prediction:
                    predictions.append(prediction)
                    confidences.append(confidence)
        
        unique_predictions = len(set(predictions))
        confidence_spread = max(confidences) - min(confidences) if confidences else 0.0
        
        # Get gap detection threshold from configuration
        threshold_config = self.config_manager.get_threshold_configuration()
        gap_threshold = 0.25  # Default fallback
        
        if isinstance(threshold_config, dict):
            ensemble_config = threshold_config.get('ensemble_configuration', {})
            if isinstance(ensemble_config, dict):
                gap_detection = ensemble_config.get('gap_detection', {})
                if isinstance(gap_detection, dict):
                    gap_threshold = float(gap_detection.get('threshold', gap_threshold))
        
        gap_detected = unique_predictions > 1 or confidence_spread > gap_threshold
        
        return {
            'gap_detection_enabled': True,
            'gap_detected': gap_detected,
            'unique_predictions': unique_predictions,
            'confidence_spread': confidence_spread,
            'gap_threshold': gap_threshold,
            'requires_manual_review': gap_detected,
            'analysis_detail': {
                'predictions': predictions,
                'confidences': confidences,
                'disagreement_level': 'high' if unique_predictions > 2 else 'medium' if unique_predictions > 1 else 'none'
            }
        }