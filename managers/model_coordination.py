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
from typing import Dict, Any, List, Optional, Tuple

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
    # ========================================================================
            
    # ========================================================================
    # LOAD THE SYSTEM
    # ========================================================================
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
    
    # ========================================================================
    # AI CLASSIFICATION METHODS - CORE IMPLEMENTATION
    # ========================================================================
    async def classify_with_zero_shot(self, text: str, labels: List[str], model_type: str, hypothesis_template: str = "This text expresses {}.") -> Dict[str, Any]:
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
            
            # ENHANCED: Process result and capture transformer details
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
                'device': self.device,
                'ensemble_manager': True,
                'transformer_details': transformer_details  # NEW: Include raw transformer info
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
        from analysis.crisis_analyzer import create_crisis_analyzer
        from analysis.performance_optimizations import integrate_performance_optimizations

        crisis_analyzer = create_crisis_analyzer(config_manager)
        performance_optimizer = integrate_performance_optimizations(crisis_analyzer)

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
            override_weights = None
            if (hasattr(performance_optimizer, '_cached_model_weights')):
                override_weights = performance_optimizer._cached_model_weights
                logger.info(f"Passing dynamic weights to ModelCoordinationManager: {override_weights}")

            ensemble_result = self._perform_ensemble_voting(model_results, override_weights)
            
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
    
    def _classify_sync_direct(self, text: str, labels: List[str], model_type: str, hypothesis_template: str) -> Dict[str, Any]:
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
            
            # ENHANCED: Process result and capture transformer details
            crisis_score, transformer_details = self._process_classification_result(result, labels)
            
            return {
                'score': crisis_score,
                'confidence': min(0.9, crisis_score + 0.1),
                'model': model_name,
                'model_type': model_type,
                'method': 'sync_zero_shot_classification',
                'labels_used': len(labels),
                'transformers_used': True,
                'device': self.device,
                'sync_optimized': True,
                'transformer_details': transformer_details  # NEW: Include raw transformer info
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
    # ========================================================================
    
    # ========================================================================
    # PROCESS CLASSIFICATION METHODS
    # ========================================================================
    def _process_classification_result(self, result: Dict, labels: List[str]) -> Tuple[float, Dict[str, Any]]:
        """
        ENHANCED: Process zero-shot classification result into crisis score WITH raw transformer details
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
            # Keep full internal processing but limit API response
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
            # This ensures crisis detection accuracy isn't affected by API display limits
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
                max_scaled_score = 1.000
                amplification = 1.8
                tier = "high_severity"
                
            elif severity_percentile <= 0.75:  # Medium-severity tier
                min_scaled_score = 0.200
                max_scaled_score = 0.700
                amplification = 1.4
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
    
    def _apply_score_normalization(self, base_score: float, severity_weight: float, severity_index: int, total_labels: int) -> float:
        """
        Apply score normalization to utilize the full 0.001-1.000 crisis detection scale
        
        This method addresses the issue where transformer models naturally output
        conservative confidence scores (typically max ~0.65) but the crisis detection
        system expects a full 0.001-1.000 scale for proper threshold classification.
        
        Args:
            base_score: Raw crisis score from transformer confidence * severity weight
            severity_weight: Severity positioning weight (1.0 = highest crisis, 0.0 = lowest)
            severity_index: Index position in severity-ordered labels (0 = most severe)
            total_labels: Total number of labels in the classification set
            
        Returns:
            Normalized crisis score utilizing the full detection scale
        """
        try:
            # Check if score normalization is enabled
            normalize_enabled = self._get_zero_shot_normalize_setting()
            
            if not normalize_enabled:
                logger.debug(f"📊 Score normalization disabled, using raw score: {base_score:.3f}")
                return base_score
            
            # Apply normalization scaling based on severity tier
            # High-severity labels (top 25% of label positions) get aggressive scaling
            # Medium-severity labels (middle 50%) get moderate scaling  
            # Low-severity labels (bottom 25%) get conservative scaling
            
            severity_percentile = severity_index / (total_labels - 1) if total_labels > 1 else 0.0
            
            if severity_percentile <= 0.25:  # High-severity tier (most critical labels)
                # Scale to utilize 0.400-1.000 range for high-severity classifications
                # Minimum boost ensures crisis detection even for lower transformer confidence
                min_scaled_score = 0.400
                max_scaled_score = 1.000
                # Amplification factor for high-severity labels
                amplification = 1.8
                
            elif severity_percentile <= 0.75:  # Medium-severity tier
                # Scale to utilize 0.200-0.700 range for medium-severity classifications
                min_scaled_score = 0.200
                max_scaled_score = 0.700
                amplification = 1.4
                
            else:  # Low-severity tier (least critical labels)
                # Scale to utilize 0.001-0.400 range for low-severity classifications
                min_scaled_score = 0.001
                max_scaled_score = 0.400
                amplification = 1.0
            
            # Apply amplification to base score
            amplified_score = min(1.0, base_score * amplification)
            
            # Scale to the appropriate range for this severity tier
            range_span = max_scaled_score - min_scaled_score
            normalized_score = min_scaled_score + (amplified_score * range_span)
            
            # Additional boost for very high confidence on high-severity labels
            if severity_percentile <= 0.25 and base_score >= 0.6:
                # Extra boost for high-confidence crisis classifications
                confidence_boost = (base_score - 0.6) * 0.5
                normalized_score = min(1.0, normalized_score + confidence_boost)
            
            logger.debug(f"📊 Score normalization applied:")
            logger.debug(f"   Severity percentile: {severity_percentile:.2f}")
            logger.debug(f"   Base score: {base_score:.3f}")
            logger.debug(f"   Amplification: {amplification:.1f}")
            logger.debug(f"   Amplified score: {amplified_score:.3f}")
            logger.debug(f"   Target range: {min_scaled_score:.3f}-{max_scaled_score:.3f}")
            logger.debug(f"   Normalized score: {normalized_score:.3f}")
            
            return normalized_score
            
        except Exception as e:
            logger.error(f"❌ Score normalization failed: {e}")
            return base_score  # Fallback to base score if normalization fails
    
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
    # ========================================================================
    
    # ========================================================================
    # ENSEMBLE VOTING METHODS
    # ========================================================================
    def _perform_ensemble_voting(self, model_results: Dict[str, Dict], override_weights: Dict[str, float] = None) -> Dict[str, float]:
        """
        PHASE 3: Perform ensemble voting on multiple model results
        
        Args:
            model_results: Dictionary of model results
            
        Returns:
            Ensemble score and confidence
        """
        logger.info("WEIGHT DEBUG: ModelCoordinationManager voting called!")
        import traceback
        logger.info("CALL TRACE: ModelCoordinationManager._perform_ensemble_voting called from:")
        for line in traceback.format_stack()[-3:-1]:
            logger.info(f"  {line.strip()}")

        try:
            ensemble_mode = self.get_ensemble_mode()
            valid_results = []
            
            logger.info(f"🎯 ENSEMBLE VOTING: mode={ensemble_mode}")
            if override_weights:
                logger.info(f"🎯 ENSEMBLE VOTING: Using override weights: {override_weights}")
            else:
                logger.info(f"🎯 ENSEMBLE VOTING: Using configuration weights")
            
            # Extract valid results
            for model_type, result in model_results.items():
                if isinstance(result, dict) and 'score' in result:
                    score = result.get('score', 0.0)
                    confidence = result.get('confidence', 0.0)
#                    weight = self.get_model_weight(model_type)
#                    logger.info(f"WEIGHT DEBUG: {model_type} using weight {weight}")
                # ENHANCEMENT: Use override weights if provided
                    if override_weights and model_type in override_weights:
                        weight = override_weights[model_type]
                        logger.info(f"🎯 WEIGHT DEBUG: {model_type} using OVERRIDE weight {weight}")
                    else:
                        weight = self.get_model_weight(model_type)
                        logger.info(f"🎯 WEIGHT DEBUG: {model_type} using CONFIG weight {weight}")
                            
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
    
    # ========================================================================
    # GET METHODS
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

    def get_validation_settings(self) -> Dict[str, Any]:
        """Get validation settings"""
        return self.config.get('validation', {})
    # ========================================================================
    
    # ========================================================================
    # MODEL INFO
    # ========================================================================
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
    
    def is_weights_validation_enabled(self) -> bool:
        """Check if weight validation is enabled"""
        return self.get_validation_settings().get('ensure_weights_sum_to_one', True)
    # ========================================================================
    # MANAGER STATUS
    # ========================================================================
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

# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
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

__all__ = [
    'ModelCoordinationManager', 
    'create_model_coordination_manager'#,
]

logger.info("ModelCoordinationManager v3.1e-5.5-7-3 Phase 3 loaded - AI classification methods implemented")