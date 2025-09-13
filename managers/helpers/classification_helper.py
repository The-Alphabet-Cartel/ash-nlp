# ash-nlp/managers/helpers/classification_helper.py
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
AI Classification and Result Processing Helper for Ash-NLP Service
---
FILE VERSION: v3.1-3e-7-1
LAST MODIFIED: 2025-09-09
PHASE: 3e Step 7 - Model Coordination Refactoring
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Handle AI classification methods and result processing
"""

import asyncio
import logging
from typing import Dict, Any, List, Tuple

# Import transformers for AI classification
try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Transformers library loaded in ClassificationHelper")
except ImportError as e:
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Transformers library not available in ClassificationHelper: {e}")

logger = logging.getLogger(__name__)

class ClassificationHelper:
    """
    AI Classification and Result Processing Helper
    
    Handles:
    - Zero-shot classification methods
    - Synchronous ensemble classification
    - Classification result processing
    - Score normalization
    - Pattern-based fallback classification
    """
    
    def __init__(self, config_manager, model_coordination_manager, pipeline_helper):
        """
        Initialize Classification Helper
        
        Args:
            config_manager: UnifiedConfigManager instance
            model_coordination_manager: Parent ModelCoordinationManager instance
            pipeline_helper: ModelPipelineHelper instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ClassificationHelper")
        if model_coordination_manager is None:
            raise ValueError("ModelCoordinationManager is required for ClassificationHelper")
        if pipeline_helper is None:
            raise ValueError("ModelPipelineHelper is required for ClassificationHelper")
        
        self.config_manager = config_manager
        self.model_manager = model_coordination_manager
        self.pipeline_helper = pipeline_helper
        
        logger.info("ClassificationHelper initialized for AI classification")

    async def classify_with_zero_shot(self, text: str, labels: List[str], model_type: str, hypothesis_template: str = "This text expresses {}.") -> Dict[str, Any]:
        """
        PRIMARY AI classification method for EnsembleAnalysisHelper
        
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
            model_config = self.model_manager.get_model_config(model_type)
            if not model_config:
                raise ValueError(f"No configuration found for model type: {model_type}")
            
            model_name = model_config.get('name')
            if not model_name:
                raise ValueError(f"No model name configured for type: {model_type}")
            
            # Load or get cached pipeline
            classifier = await self.pipeline_helper.get_or_load_pipeline(model_name)
            if classifier is None:
                logger.warning(f"⚠️ Could not load model {model_name}, using pattern fallback")
                return await self._pattern_fallback_classification(text, labels, model_type)
            
            # Generate actual hypotheses from labels
            actual_hypotheses = []
            for label in labels:
                if "{}" in hypothesis_template:
                    hypothesis = hypothesis_template.replace("{}", label)
                elif "{label}" in hypothesis_template:
                    hypothesis = hypothesis_template.replace("{label}", label)
                else:
                    hypothesis = f"{hypothesis_template} {label}"
                actual_hypotheses.append(hypothesis)

            # Perform zero-shot classification
            logger.debug(f"🤖 Running zero-shot classification: {model_type} with {model_name}")
            
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: classifier(text, labels)
            )
            
            # Process result and capture transformer details
            crisis_score, transformer_details = self._process_classification_result(result, labels)
            
            return {
                'score': crisis_score,
                'confidence': min(0.9, crisis_score + 0.1),
                'model': model_name,
                'model_type': model_type,
                'method': 'zero_shot_classification',
                'labels_used': len(labels),
                'labels': labels,
                'hypothesis_template': hypothesis_template,
                'transformers_used': True,
                'device': self.pipeline_helper.device,
                'ensemble_manager': True,
                'transformer_details': transformer_details
            }

        except Exception as e:
            logger.error(f"❌ Zero-shot classification failed for {model_type}: {e}")
            return await self._pattern_fallback_classification(text, labels, model_type)

    def classify_sync_ensemble(self, text: str, zero_shot_manager=None, override_weights: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Synchronous ensemble classification for performance optimization
        
        Args:
            text: Text to classify
            zero_shot_manager: ZeroShotManager instance for label management
            override_weights: Optional dynamic weights to use instead of configuration
            
        Returns:
            Synchronous ensemble classification results
        """
        try:
            model_results = {}
            models = self.model_manager.get_model_definitions()
            
            # Use provided weights or try to detect dynamic weights
            dynamic_weights = override_weights or self.model_manager._get_dynamic_weights_if_available()
            
            if dynamic_weights:
                logger.debug(f"🎯 SYNC ENSEMBLE: Using dynamic weights: {dynamic_weights}")
            else:
                logger.debug(f"🎯 SYNC ENSEMBLE: Using configuration weights")
            
            # Get labels from ZeroShotManager if available
            if zero_shot_manager:
                try:
                    all_labels = zero_shot_manager.get_all_labels()
                    zero_shot_settings = zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', "This text expresses {}.")
                    logger.debug("Using ZeroShotManager for synchronous label management")
                except Exception as e:
                    logger.warning(f"ZeroShotManager access failed in sync mode: {e}")
                    all_labels = {}
                    hypothesis_template = "This text expresses {}."
            else:
                all_labels = {}
                hypothesis_template = "This text expresses {}."
            
            # Classify with each model (synchronous)
            for model_type in models.keys():
                try:
                    # Get labels for this model type
                    if isinstance(all_labels, dict) and model_type in all_labels:
                        model_labels = all_labels[model_type]
                    elif isinstance(all_labels, dict):
                        model_labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        model_labels = self._get_fallback_labels(model_type)
                    
                    if not model_labels:
                        model_labels = self._get_fallback_labels(model_type)
                    
                    # Synchronous classification (no async)
                    result = self._classify_sync_direct(text, model_labels, model_type, hypothesis_template)
                    model_results[model_type] = result
                    
                except Exception as e:
                    logger.error(f"Model {model_type} sync classification failed: {e}")
                    model_results[model_type] = {
                        'score': 0.0,
                        'confidence': 0.0,
                        'error': str(e),
                        'model_type': model_type,
                        'method': 'sync_error'
                    }
            
            return {
                'individual_results': model_results,
                'models_used': len(model_results),
                'zero_shot_manager_used': zero_shot_manager is not None,
                'method': 'sync_ensemble_classification',
                'performance_optimized': True,
                'dynamic_weights_used': dynamic_weights is not None,
                'weights_source': 'dynamic' if dynamic_weights else 'configuration'
            }
            
        except Exception as e:
            logger.error(f"Synchronous ensemble classification failed: {e}")
            return {
                'error': str(e),
                'method': 'sync_ensemble_error'
            }

    def _classify_sync_direct(self, text: str, labels: List[str], model_type: str, hypothesis_template: str) -> Dict[str, Any]:
        """
        Direct synchronous classification
        
        Eliminates async overhead by using synchronous model inference.
        Falls back to pattern matching if transformers unavailable.
        
        Args:
            text: Text to classify
            labels: Classification labels
            model_type: Model type (depression, sentiment, emotional_distress) 
            hypothesis_template: Template for hypothesis generation
            
        Returns:
            Synchronous classification result
        """
        try:
            if not TRANSFORMERS_AVAILABLE:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            # Get model configuration
            model_config = self.model_manager.get_model_config(model_type)
            if not model_config:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            model_name = model_config.get('name')
            if not model_name:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            # Get cached pipeline (synchronous)
            classifier = self.pipeline_helper.get_cached_pipeline_sync(model_name)
            if classifier is None:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            # Perform synchronous zero-shot classification
            logger.debug(f"Running sync zero-shot classification: {model_type} with {model_name}")
            
            # Direct synchronous call (no async executor)
            result = classifier(text, labels)
            
            # Process result and capture transformer details
            crisis_score, transformer_details = self._process_classification_result(result, labels)
            
            return {
                'score': crisis_score,
                'confidence': min(0.9, crisis_score + 0.1),
                'model': model_name,
                'model_type': model_type,
                'method': 'sync_zero_shot_classification',
                'labels_used': len(labels),
                'transformers_used': True,
                'device': self.pipeline_helper.device,
                'sync_optimized': True,
                'transformer_details': transformer_details
            }

        except Exception as e:
            logger.error(f"Sync zero-shot classification failed for {model_type}: {e}")
            return self._sync_pattern_fallback(text, labels, model_type)

    def _sync_pattern_fallback(self, text: str, labels: List[str], model_type: str) -> Dict[str, Any]:
        """
        Synchronous pattern-based fallback classification
        
        Args:
            text: Text to classify
            labels: Classification labels (unused in pattern matching)
            model_type: Model type for context
            
        Returns:
            Pattern-based classification result
        """
        try:
            text_lower = text.lower()
            
            # Model-specific keyword sets
            if model_type == 'depression':
                keywords = ['suicide', 'suicidal', 'hopeless', 'worthless', 'depression', 'kill myself']
            elif model_type == 'sentiment':
                keywords = ['hate', 'angry', 'furious', 'terrible', 'awful', 'worst']
            elif model_type == 'emotional_distress':
                keywords = ['crisis', 'breakdown', 'panic', 'overwhelmed', 'distress', 'emergency']
            else:
                keywords = ['crisis', 'help', 'emergency', 'urgent', 'desperate']
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            # Calculate score based on matches
            base_score = min(0.8, matches * 0.2)
            
            # Boost score for multiple matches
            if matches >= 3:
                base_score = min(0.9, base_score + 0.1)
            
            return {
                'score': base_score,
                'confidence': min(0.7, base_score + 0.1),
                'model': f'sync_pattern_{model_type}',
                'model_type': model_type,
                'method': 'sync_pattern_fallback',
                'keywords_matched': matches,
                'transformers_used': False,
                'sync_optimized': True
            }
            
        except Exception as e:
            logger.error(f"Sync pattern fallback failed for {model_type}: {e}")
            return {
                'score': 0.0,
                'confidence': 0.0,
                'error': str(e),
                'model_type': model_type,
                'method': 'sync_pattern_error'
            }

    def _process_classification_result(self, result: Dict, labels: List[str]) -> Tuple[float, Dict[str, Any]]:
        """
        Process zero-shot classification result into crisis score WITH raw transformer details
        that respect the NLP_ZERO_SHOT_MAX_LABELS configuration setting
        
        Args:
            result: Raw result from zero-shot classifier
            labels: Original labels used for classification
            
        Returns:
            Tuple of (crisis_score, transformer_details) where transformer_details contains
            filtered raw information respecting MAX_LABELS configuration
        """
        try:
            if not result or 'scores' not in result:
                logger.warning(f"⚠️ Invalid classification result format")
                return 0.0, self._get_empty_transformer_details()
            
            scores = result['scores']
            predicted_labels = result.get('labels', [])
            
            if len(scores) != len(labels):
                logger.warning(f"⚠️ Score/label mismatch in classification result")
                return 0.0, self._get_empty_transformer_details()
            
            # Get MAX_LABELS configuration setting
            max_labels = self._get_zero_shot_max_labels_setting()
            
            # Apply MAX_LABELS filtering to the results for API output
            filtered_predicted_labels = predicted_labels[:max_labels] if predicted_labels else []
            filtered_scores = scores[:max_labels] if scores else []
            
            # Capture RAW transformer details for API response (with MAX_LABELS filtering)
            raw_transformer_details = {
                'raw_transformers_result': {
                    'predicted_labels': filtered_predicted_labels.copy(),
                    'confidence_scores': [float(s) for s in filtered_scores],
                    'original_input_labels': labels.copy() if labels else [],
                    'top_prediction': {
                        'label': predicted_labels[0] if predicted_labels else None,
                        'confidence': float(scores[0]) if scores else 0.0
                    },
                    'all_predictions': [
                        {
                            'label': label,
                            'confidence': float(score),
                            'rank': idx + 1
                        }
                        for idx, (label, score) in enumerate(zip(filtered_predicted_labels, filtered_scores))
                    ],
                    'model_response_metadata': {
                        'total_labels_processed': len(labels),
                        'predictions_returned': len(predicted_labels) if predicted_labels else 0,
                        'max_labels_configured': max_labels,
                        'predictions_shown': len(filtered_predicted_labels),
                        'predictions_filtered': max(0, len(predicted_labels) - max_labels),
                        'score_distribution': {
                            'highest': float(max(scores)) if scores else 0.0,
                            'lowest': float(min(scores)) if scores else 0.0,
                            'average': float(sum(scores) / len(scores)) if scores else 0.0,
                            'top_n_average': float(sum(filtered_scores) / len(filtered_scores)) if filtered_scores else 0.0
                        }
                    }
                },
                'configuration_applied': {
                    'max_labels_setting': max_labels,
                    'max_labels_source': self._get_max_labels_config_source(),
                    'filtering_applied': len(predicted_labels) > max_labels if predicted_labels else False
                },
                'normalization_applied': False,
                'base_score_before_normalization': 0.0,
                'final_score_after_normalization': 0.0
            }
            
            # DEBUG: Log the transformers result structure for verification
            logger.debug(f"🔍 Transformers result - labels: {predicted_labels}")
            logger.debug(f"🔍 Transformers result - scores: {[f'{s:.3f}' for s in scores]}")
            logger.debug(f"🔍 Original input labels: {labels}")
            logger.debug(f"🔍 MAX_LABELS configuration: {max_labels}")
            logger.debug(f"🔍 Filtered to top {len(filtered_predicted_labels)} predictions for API response")

            # Continue with full internal processing using ALL results (not filtered)
            if not predicted_labels or not scores:
                logger.warning("⚠️ No predictions returned from transformers")
                return 0.0, raw_transformer_details
                
            top_label = predicted_labels[0]  # Use full results for crisis calculation
            top_score = scores[0]
            
            # Find where this label was positioned in our original severity-ordered labels
            try:
                original_index = labels.index(top_label)
                # Convert index to severity weight (0 = highest crisis, last = lowest crisis)
                severity_weight = 1.0 - (original_index / (len(labels) - 1)) if len(labels) > 1 else 1.0
                
                # Calculate base crisis score based on confidence and severity position
                base_crisis_score = top_score * severity_weight
                
                # Update transformer details with severity analysis
                raw_transformer_details['severity_analysis'] = {
                    'top_predicted_label': top_label,
                    'original_severity_index': original_index,
                    'total_severity_levels': len(labels),
                    'severity_weight': severity_weight,
                    'severity_percentile': original_index / (len(labels) - 1) if len(labels) > 1 else 0.0,
                    'note': f'Crisis calculation uses full transformer results, API shows top {max_labels}'
                }
                
                logger.debug(f"📊 Top prediction: {top_label} (score={top_score:.3f})")
                logger.debug(f"📊 Original severity index: {original_index}/{len(labels)-1}")
                logger.debug(f"📊 Severity weight: {severity_weight:.3f}")
                logger.debug(f"📊 Crisis score: {base_crisis_score:.3f}")
                
            except ValueError:
                logger.warning(f"⚠️ Top predicted label '{top_label}' not found in original labels")
                # Fallback: use raw confidence score
                base_crisis_score = top_score
                severity_weight = 1.0
                original_index = 0
                
                raw_transformer_details['severity_analysis'] = {
                    'top_predicted_label': top_label,
                    'original_severity_index': None,
                    'error': 'predicted_label_not_in_original_labels',
                    'fallback_applied': True
                }
                
                logger.debug(f"📊 Using fallback score: {base_crisis_score:.3f}")
            
            # Store base score before normalization
            raw_transformer_details['base_score_before_normalization'] = base_crisis_score
            
            # Apply score normalization if enabled and capture details
            final_crisis_score, normalization_details = self._apply_score_normalization_with_details(
                base_crisis_score, 
                severity_weight, 
                original_index, 
                len(labels)
            )
            
            # Update transformer details with normalization information
            raw_transformer_details.update(normalization_details)
            raw_transformer_details['final_score_after_normalization'] = final_crisis_score
            
            # Ensure final score is within valid range
            final_crisis_score = max(0.0, min(1.0, final_crisis_score))
            
            logger.debug(f"📊 Final crisis score: {final_crisis_score:.3f}")
            return final_crisis_score, raw_transformer_details
            
        except Exception as e:
            logger.error(f"❌ Classification result processing failed: {e}")
            error_details = self._get_empty_transformer_details()
            error_details['processing_error'] = str(e)
            return 0.0, error_details

    def _apply_score_normalization_with_details(self, base_score: float, severity_weight: float, severity_index: int, total_labels: int) -> Tuple[float, Dict[str, Any]]:
        """
        Enhanced normalization that returns both the normalized score AND detailed information
        about the normalization process for inclusion in API responses
        """
        try:
            # Check if score normalization is enabled
            normalize_enabled = self._get_zero_shot_normalize_setting()
            
            normalization_details = {
                'normalization_applied': normalize_enabled,
                'normalization_settings': {
                    'enabled': normalize_enabled,
                    'source': 'NLP_ZERO_SHOT_NORMALIZE_SCORES'
                }
            }
            
            if not normalize_enabled:
                logger.debug(f"📊 Score normalization disabled, using raw score: {base_score:.3f}")
                normalization_details['reason'] = 'normalization_disabled'
                return base_score, normalization_details
            
            # Apply normalization scaling based on severity tier
            severity_percentile = severity_index / (total_labels - 1) if total_labels > 1 else 0.0
            
            if severity_percentile <= 0.25:  # High-severity tier
                min_scaled_score = 0.400
                max_scaled_score = 0.800
                amplification = 2.0
                tier = "high_severity"
                
            elif severity_percentile <= 0.75:  # Medium-severity tier
                min_scaled_score = 0.200
                max_scaled_score = 0.600
                amplification = 1.5
                tier = "medium_severity"
                
            else:  # Low-severity tier
                min_scaled_score = 0.001
                max_scaled_score = 0.400
                amplification = 1.0
                tier = "low_severity"
            
            # Apply amplification to base score
            amplified_score = min(1.0, base_score * amplification)
            
            # Scale to the appropriate range for this severity tier
            range_span = max_scaled_score - min_scaled_score
            normalized_score = min_scaled_score + (amplified_score * range_span)
            
            # Additional boost for very high confidence on high-severity labels
            confidence_boost = 0.0
            if severity_percentile <= 0.25 and base_score >= 0.6:
                confidence_boost = (base_score - 0.6) * 0.5
                normalized_score = min(1.0, normalized_score + confidence_boost)
            
            # Capture detailed normalization information
            normalization_details.update({
                'normalization_tier': tier,
                'severity_percentile': severity_percentile,
                'amplification_factor': amplification,
                'target_range': {
                    'minimum': min_scaled_score,
                    'maximum': max_scaled_score,
                    'span': range_span
                },
                'score_progression': {
                    'base_score': base_score,
                    'amplified_score': amplified_score,
                    'range_normalized_score': min_scaled_score + (amplified_score * range_span),
                    'confidence_boost': confidence_boost,
                    'final_normalized_score': normalized_score
                },
                'normalization_impact': {
                    'original_to_final_ratio': normalized_score / base_score if base_score > 0 else 0,
                    'absolute_change': normalized_score - base_score,
                    'percentage_change': ((normalized_score - base_score) / base_score * 100) if base_score > 0 else 0
                }
            })
            
            logger.debug(f"📊 Score normalization applied:")
            logger.debug(f"   Severity percentile: {severity_percentile:.2f}")
            logger.debug(f"   Base score: {base_score:.3f}")
            logger.debug(f"   Amplification: {amplification:.1f}")
            logger.debug(f"   Amplified score: {amplified_score:.3f}")
            logger.debug(f"   Target range: {min_scaled_score:.3f}-{max_scaled_score:.3f}")
            logger.debug(f"   Normalized score: {normalized_score:.3f}")
            
            return normalized_score, normalization_details
            
        except Exception as e:
            logger.error(f"❌ Score normalization failed: {e}")
            error_details = {
                'normalization_applied': False,
                'error': str(e),
                'fallback_used': True
            }
            return base_score, error_details

    def _get_zero_shot_max_labels_setting(self) -> int:
        """
        Get the NLP_ZERO_SHOT_MAX_LABELS setting from configuration
        
        Returns:
            Maximum number of labels to show in API responses (default: 5)
        """
        try:
            # Check zero-shot settings in configuration
            zero_shot_settings = self.config_manager.get_config_section('label_config', 'zero_shot_settings')
            if zero_shot_settings:
                max_labels = zero_shot_settings.get('max_labels', 5)
                # Validate and convert to int
                max_labels = int(max_labels)
                # Ensure reasonable bounds (1-10 as per validation rules)
                max_labels = max(1, min(10, max_labels))
                logger.debug(f"🔧 Zero-shot max_labels setting: {max_labels}")
                return max_labels
            
            # Fallback: check environment variable directly
            import os
            env_setting = os.getenv('NLP_ZERO_SHOT_MAX_LABELS', '5')
            try:
                max_labels = int(env_setting)
                max_labels = max(1, min(10, max_labels))  # Bounds check
                logger.debug(f"🔧 Zero-shot max_labels from ENV: {max_labels}")
                return max_labels
            except ValueError:
                logger.warning(f"⚠️ Invalid NLP_ZERO_SHOT_MAX_LABELS value '{env_setting}', using default 5")
                return 5
                
        except Exception as e:
            logger.warning(f"⚠️ Could not get max_labels setting: {e}")
            return 5  # Safe default

    def _get_max_labels_config_source(self) -> str:
        """
        Determine where the max_labels setting came from for debugging
        
        Returns:
            Source description for the max_labels setting
        """
        try:
            # Check if it's from config file
            zero_shot_settings = self.config_manager.get_config_section('label_config', 'zero_shot_settings')
            if zero_shot_settings and 'max_labels' in zero_shot_settings:
                return 'config_file_label_config.json'
            
            # Check if it's from environment variable
            import os
            if 'NLP_ZERO_SHOT_MAX_LABELS' in os.environ:
                return 'environment_variable'
            
            return 'default_fallback'
            
        except Exception:
            return 'unknown'

    def _get_empty_transformer_details(self) -> Dict[str, Any]:
        """Return empty transformer details structure for error cases with MAX_LABELS awareness"""
        max_labels = self._get_zero_shot_max_labels_setting()
        
        return {
            'raw_transformers_result': {
                'predicted_labels': [],
                'confidence_scores': [],
                'original_input_labels': [],
                'top_prediction': {'label': None, 'confidence': 0.0},
                'all_predictions': [],
                'model_response_metadata': {
                    'total_labels_processed': 0,
                    'predictions_returned': 0,
                    'max_labels_configured': max_labels,
                    'predictions_shown': 0,
                    'predictions_filtered': 0,
                    'score_distribution': {'highest': 0.0, 'lowest': 0.0, 'average': 0.0, 'top_n_average': 0.0}
                }
            },
            'configuration_applied': {
                'max_labels_setting': max_labels,
                'max_labels_source': self._get_max_labels_config_source(),
                'filtering_applied': False
            },
            'severity_analysis': {},
            'normalization_applied': False,
            'base_score_before_normalization': 0.0,
            'final_score_after_normalization': 0.0,
            'error': 'no_valid_results'
        }

    def _get_zero_shot_normalize_setting(self) -> bool:
        """
        Get the NLP_ZERO_SHOT_NORMALIZE_SCORES setting from configuration
        
        Returns:
            True if score normalization is enabled, False otherwise
        """
        try:
            # Check if we have access to the ZeroShotManager configuration through config_manager
            zero_shot_settings = self.config_manager.get_config_section('label_config', 'zero_shot_settings')
            if zero_shot_settings:
                normalize_setting = zero_shot_settings.get('normalize_scores', True)
                logger.debug(f"🔧 Zero-shot normalize_scores setting: {normalize_setting}")
                return bool(normalize_setting)
            
            # Fallback: check environment variable directly
            import os
            env_setting = os.getenv('NLP_ZERO_SHOT_NORMALIZE_SCORES', 'true').lower()
            normalize_enabled = env_setting in ['true', '1', 'yes', 'on']
            logger.debug(f"🔧 Zero-shot normalize_scores from ENV: {normalize_enabled}")
            return normalize_enabled
            
        except Exception as e:
            logger.warning(f"⚠️ Could not get normalize_scores setting: {e}")
            # Default to enabled for better crisis detection
            return True

    async def _pattern_fallback_classification(self, text: str, labels: List[str], model_type: str) -> Dict[str, Any]:
        """
        Pattern-based fallback when transformers unavailable
        
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

# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_classification_helper(config_manager, model_coordination_manager, pipeline_helper) -> ClassificationHelper:
    """
    Factory function to create ClassificationHelper instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        model_coordination_manager: ModelCoordinationManager instance
        pipeline_helper: ModelPipelineHelper instance
        
    Returns:
        ClassificationHelper instance
    """
    return ClassificationHelper(config_manager, model_coordination_manager, pipeline_helper)
# ============================================================================

__all__ = [
    'ClassificationHelper',
    'create_classification_helper'
]

logger.info("ClassificationHelper v3.1-3e-7-1 loaded - AI classification and result processing functionality")