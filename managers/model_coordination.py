# ash-nlp/managers/model_coordination.py
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
FILE VERSION: v3.1-3e-6-1
LAST MODIFIED: 2025-08-22
PHASE: 3e Step 5.5-7 - Phase 3: AI Classification Methods Implementation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PHASE 3 IMPLEMENTATION:
- Added actual AI classification methods that EnsembleAnalysisHelper should call
- Implemented classify_with_zero_shot() for semantic classification
- Added model pipeline management and caching
- Proper integration with ZeroShotManager for label management
- Correct architectural flow: EnsembleAnalysisHelper → ModelCoordinationManager → transformers
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
    logger.info("✅ Transformers library loaded in ModelCoordinationManager for AI classification")
except ImportError as e:
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Transformers library not available in ModelCoordinationManager: {e}")

logger = logging.getLogger(__name__)

class ModelCoordinationManager:
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
    EnsembleAnalysisHelper calls ModelCoordinationManager.classify_with_zero_shot()
    Instead of EnsembleAnalysisHelper directly creating transformers pipelines
    """
    
    def __init__(self, config_manager):
        """
        Initialize Model Ensemble Manager
        
        Args:
            config_manager: UnifiedConfigManager instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ModelCoordinationManager")
        
        self.config_manager = config_manager
        
        # PHASE 3: Add model pipeline cache and loading management
        self._model_cache = {}
        self._model_loading_lock = asyncio.Lock()
        
        logger.info("ModelCoordinationManager v3.1e-5.5-7-3 Phase 3 initialized with AI classification")
        
        # Load and validate configuration
        self._load_and_validate_configuration()
        
        # Get device configuration for AI models
        self.device = self._get_device_config()
        logger.info(f"🔧 ModelCoordinationManager device configuration: {self.device}")
    
    # ========================================================================
    # PRELOAD THOSE BIG-ASS MODELS!
    # ========================================================================
    
    async def preload_models(self):
        """
        Preload all configured models during container startup
        This prevents timeout issues during actual crisis analysis
        """
        try:
            logger.info("Starting model preloading during container startup...")
            
            models = self.get_model_definitions()
            if not models:
                logger.warning("No models configured for preloading")
                return
            
            for model_type, model_config in models.items():
                model_name = model_config.get('name')
                enabled = model_config.get('enabled', True)
                
                if not model_name or not enabled:
                    logger.info(f"Skipping model {model_type}: {'no name' if not model_name else 'disabled'}")
                    continue
                
                try:
                    logger.info(f"Preloading model: {model_type} ({model_name})")
                    pipeline_obj = await self._get_or_load_pipeline(model_name)
                    
                    if pipeline_obj:
                        logger.info(f"Successfully preloaded: {model_type}")
                    else:
                        logger.warning(f"Failed to preload: {model_type}")
                        
                except Exception as e:
                    logger.error(f"Error preloading {model_type}: {e}")
                    
            logger.info(f"Model preloading complete. Cached models: {len(self._model_cache)}")
            
            # NEW: Warmup the complete analysis pipeline to eliminate cold start penalty
            warmup_success = await self._warmup_analysis_pipeline()
            if warmup_success:
                logger.info("🔥 Analysis pipeline warmup successful - cold start penalty eliminated")
            else:
                logger.warning("⚠️ Analysis pipeline warmup had issues - may experience cold start penalty")
            
        except Exception as e:
            logger.error(f"Model preloading failed: {e}")

    async def _warmup_analysis_pipeline(self):
        """
        Warmup the complete analysis pipeline to eliminate cold start penalty
        
        This method creates a temporary CrisisAnalyzer and runs a complete analysis
        to ensure all components are initialized and cached properly.
        """
        try:
            logger.info("🔥 Starting analysis pipeline warmup...")
            warmup_start_time = time.time()
            
            # Import here to avoid circular imports
            try:
                from analysis import create_crisis_analyzer
            except ImportError as e:
                logger.warning(f"Cannot import CrisisAnalyzer for warmup: {e}")
                return False
            
            # Get other managers from config if available
            shared_utilities_manager = None
            learning_system_manager = None
            pattern_detection_manager = None
            
            # Try to get additional managers for complete warmup
            try:
                # These may not be available in all configurations
                if hasattr(self.config_manager, 'get_manager'):
                    shared_utilities_manager = self.config_manager.get_manager('shared_utilities')
                    learning_system_manager = self.config_manager.get_manager('learning_system')
                    pattern_detection_manager = self.config_manager.get_manager('pattern_detection')
            except Exception as e:
                logger.debug(f"Additional managers not available for warmup: {e}")
            
            # Create a temporary CrisisAnalyzer for warmup
            logger.debug("Creating temporary CrisisAnalyzer for warmup...")
            try:
                warmup_analyzer = create_crisis_analyzer(
                    unified_config=self.config_manager,
                    model_coordination_manager=self,
                    shared_utilities_manager=shared_utilities_manager,
                    learning_system_manager=learning_system_manager,
                    pattern_detection_manager=pattern_detection_manager
                )
            except Exception as e:
                logger.warning(f"Failed to create CrisisAnalyzer for warmup: {e}")
                return False
            
            # Warmup test message - realistic but generic to exercise key paths
            warmup_message = "This is a warmup test to initialize the analysis pipeline and cache components."
            
            # Run a complete analysis to warm up all components
            logger.debug("Running warmup analysis to initialize all components...")
            analysis_start_time = time.time()
            
            try:
                # Check if analyze_message is async or sync
                import inspect
                if hasattr(warmup_analyzer, 'analyze_message'):
                    if inspect.iscoroutinefunction(warmup_analyzer.analyze_message):
                        warmup_result = await warmup_analyzer.analyze_message(
                            message=warmup_message,
                            user_id="warmup_user",
                            channel_id="warmup_channel"
                        )
                    else:
                        warmup_result = warmup_analyzer.analyze_message(
                            message=warmup_message,
                            user_id="warmup_user", 
                            channel_id="warmup_channel"
                        )
                elif hasattr(warmup_analyzer, 'analyze'):
                    warmup_result = warmup_analyzer.analyze(warmup_message)
                else:
                    logger.warning("No suitable analysis method found on CrisisAnalyzer")
                    return False
                    
            except Exception as e:
                logger.warning(f"Warmup analysis execution failed: {e}")
                # Still consider partial success if we got this far
                warmup_result = {'status': 'partial_warmup', 'error': str(e)}
            
            analysis_time = (time.time() - analysis_start_time) * 1000
            total_warmup_time = (time.time() - warmup_start_time) * 1000
            
            # Evaluate warmup success
            if warmup_result and (
                warmup_result.get('status') == 'success' or 
                'score' in warmup_result or 
                'crisis_level' in warmup_result
            ):
                logger.info(f"✅ Analysis pipeline warmup successful!")
                logger.info(f"   Warmup analysis time: {analysis_time:.1f}ms")
                logger.info(f"   Total warmup time: {total_warmup_time:.1f}ms")
                
                # Store warmup metadata for health checks
                self._pipeline_warmed = True
                self._warmup_time_ms = total_warmup_time
                self._warmup_analysis_time_ms = analysis_time
                self._warmup_success = True
                
                return True
            else:
                logger.warning(f"⚠️ Analysis pipeline warmup completed with issues")
                logger.warning(f"   Warmup analysis time: {analysis_time:.1f}ms")
                logger.warning(f"   Total warmup time: {total_warmup_time:.1f}ms")
                logger.warning(f"   Result: {warmup_result}")
                
                # Store partial warmup metadata
                self._pipeline_warmed = True
                self._warmup_time_ms = total_warmup_time  
                self._warmup_analysis_time_ms = analysis_time
                self._warmup_success = False
                
                return False
                
        except Exception as e:
            logger.error(f"❌ Analysis pipeline warmup failed: {e}")
            
            # Store failure metadata
            self._pipeline_warmed = False
            self._warmup_time_ms = None
            self._warmup_analysis_time_ms = None 
            self._warmup_success = False
            
            return False

    def get_warmup_status(self) -> Dict[str, Any]:
        """
        Get warmup status for health checks and diagnostics
        
        Returns:
            Dictionary with warmup status information
        """
        try:
            models = self.get_model_definitions()
            preload_status = self.get_preload_status()
            
            return {
                'pipeline_warmed': getattr(self, '_pipeline_warmed', False),
                'warmup_success': getattr(self, '_warmup_success', None),
                'total_warmup_time_ms': getattr(self, '_warmup_time_ms', None),
                'warmup_analysis_time_ms': getattr(self, '_warmup_analysis_time_ms', None),
                'models_preloaded': preload_status.get('preload_complete', False),
                'models_cached': len(self._model_cache),
                'total_models_configured': len(models),
                'transformers_available': TRANSFORMERS_AVAILABLE,
                'cold_start_eliminated': (
                    getattr(self, '_pipeline_warmed', False) and 
                    getattr(self, '_warmup_success', False)
                ),
                'ready_for_production': (
                    preload_status.get('preload_complete', False) and
                    getattr(self, '_pipeline_warmed', False)
                )
            }
        except Exception as e:
            return {
                'error': str(e), 
                'pipeline_warmed': False,
                'ready_for_production': False
            }

    def get_preload_status(self) -> Dict[str, Any]:
        """Get status of model preloading for health checks"""
        try:
            models = self.get_model_definitions()
            total_models = len(models)
            loaded_models = len(self._model_cache)
            
            return {
                'total_models_configured': total_models,
                'models_loaded': loaded_models,
                'preload_complete': loaded_models == total_models,
                'cached_model_names': list(self._model_cache.keys()),
                'transformers_available': TRANSFORMERS_AVAILABLE
            }
        except Exception as e:
            return {'error': str(e), 'preload_complete': False}
            
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
            model_config = self.config_manager.get_config_section('model_coordination')
            
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
            logger.warning(f"Error loading model configuration: {e}")
            return
    
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
            
            # Process result into crisis score
            crisis_score = self._process_classification_result(result, labels)
            
            return {
                'score': crisis_score,
                'confidence': min(0.9, crisis_score + 0.1),
                'model': model_name,
                'model_type': model_type,
                'method': 'zero_shot_classification',
                'labels_used': len(labels),
                'labels': labels,  # Add the actual labels
                'hypothesis_template': hypothesis_template,  # Keep the template
                'actual_hypotheses': actual_hypotheses,  # Add resolved hypotheses
                'transformers_used': True,
                'device': self.device,
                'ensemble_manager': True
            }

        except Exception as e:
            logger.error(f"❌ Zero-shot classification failed for {model_type}: {e}")
            return await self._pattern_fallback_classification(text, labels, model_type)
    
    def classify_sync_ensemble(self, text: str, zero_shot_manager=None) -> Dict[str, Any]:
        """
        PHASE 3E STEP 7: Synchronous ensemble classification for performance optimization
        
        This method provides synchronous model coordination to eliminate async/sync
        conversion overhead in the performance-optimized analysis path.
        
        Args:
            text: Text to classify
            zero_shot_manager: ZeroShotManager instance for label management
            
        Returns:
            Synchronous ensemble classification results
        """
        try:
            model_results = {}
            models = self.get_model_definitions()
            
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
            
            # Perform ensemble voting (synchronous)
            ensemble_result = self._perform_ensemble_voting(model_results)
            
            return {
                'ensemble_score': ensemble_result['score'],
                'ensemble_confidence': ensemble_result['confidence'], 
                'ensemble_mode': self.get_ensemble_mode(),
                'individual_results': model_results,
                'models_used': len(model_results),
                'zero_shot_manager_used': zero_shot_manager is not None,
                'method': 'sync_ensemble_classification',
                'performance_optimized': True
            }
            
        except Exception as e:
            logger.error(f"Synchronous ensemble classification failed: {e}")
            return {
                'ensemble_score': 0.0,
                'ensemble_confidence': 0.0,
                'error': str(e),
                'method': 'sync_ensemble_error'
            }
    
    def _classify_sync_direct(self, text: str, labels: List[str], model_type: str, 
                            hypothesis_template: str) -> Dict[str, Any]:
        """
        PHASE 3E STEP 7: Direct synchronous classification
        
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
            model_config = self.get_model_config(model_type)
            if not model_config:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            model_name = model_config.get('name')
            if not model_name:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            # Get cached pipeline (synchronous)
            classifier = self._get_cached_pipeline_sync(model_name)
            if classifier is None:
                return self._sync_pattern_fallback(text, labels, model_type)
            
            # Perform synchronous zero-shot classification
            logger.debug(f"Running sync zero-shot classification: {model_type} with {model_name}")
            
            # Direct synchronous call (no async executor)
            result = classifier(text, labels)
            
            # Process result into crisis score
            crisis_score = self._process_classification_result(result, labels)
            
            return {
                'score': crisis_score,
                'confidence': min(0.9, crisis_score + 0.1),
                'model': model_name,
                'model_type': model_type,
                'method': 'sync_zero_shot_classification',
                'labels_used': len(labels),
                'transformers_used': True,
                'device': self.device,
                'sync_optimized': True
            }

        except Exception as e:
            logger.error(f"Sync zero-shot classification failed for {model_type}: {e}")
            return self._sync_pattern_fallback(text, labels, model_type)
    
    def _get_cached_pipeline_sync(self, model_name: str):
        """
        Get cached pipeline synchronously (no async lock)
        Returns cached pipeline or None if not available
        """
        if not TRANSFORMERS_AVAILABLE:
            return None
            
        # Check cache first (no async lock for performance)
        if model_name in self._model_cache:
            logger.debug(f"Using cached model synchronously: {model_name}")
            return self._model_cache[model_name]
        
        # If not cached, return None to fall back to pattern matching
        # This avoids loading models during performance-critical analysis
        logger.debug(f"Model {model_name} not cached, using pattern fallback")
        return None
    
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
                cache_dir = self.config_manager.get_config_section('model_coordination', 'ensemble_config.cache_dir')
                if cache_dir and cache_dir.strip():
                    os.makedirs(cache_dir, exist_ok=True)
                    logger.debug(f"Using ensemble config cache directory: {cache_dir}")
                    return cache_dir
            except Exception as e:
                logger.debug(f"Ensemble config cache dir access failed: {e}")
            
            # Check hardware_settings cache_dir
            cache_dir = self.config_manager.get_config_section('model_coordination', 'hardware_settings.cache_dir')
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

def create_model_coordination_manager(config_manager) -> ModelCoordinationManager:
    """
    Factory function to create ModelCoordinationManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        ModelCoordinationManager instance
    """
    return ModelCoordinationManager(config_manager)

# ============================================================================
# BACKWARD COMPATIBILITY - Global Instance Management
# ============================================================================

_model_coordination_manager = None

def get_model_coordination_manager(config_manager=None) -> ModelCoordinationManager:
    """
    Get the global model ensemble manager instance - LEGACY COMPATIBILITY
    
    Args:
        config_manager: UnifiedConfigManager instance (optional for compatibility)
        
    Returns:
        ModelCoordinationManager instance
    """
    global _model_coordination_manager
    
    if _model_coordination_manager is None:
        if config_manager is None:
            logger.info("Creating UnifiedConfigManager for ModelCoordinationManager compatibility")
            from managers.unified_config import create_unified_config_manager
            config_manager = create_unified_config_manager()
        
        _model_coordination_manager = ModelCoordinationManager(config_manager)
    
    return _model_coordination_manager

def reset_model_coordination_manager():
    """Reset the global manager instance - for testing"""
    global _model_coordination_manager
    _model_coordination_manager = None

__all__ = [
    'ModelCoordinationManager', 
    'create_model_coordination_manager',
    'get_model_coordination_manager', 
    'reset_model_coordination_manager'
]

logger.info("ModelCoordinationManager v3.1e-5.5-7-3 Phase 3 loaded - AI classification methods implemented")