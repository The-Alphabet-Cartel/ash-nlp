# ash-nlp/managers/helpers/model_pipeline_helper.py
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
Model Pipeline Management Helper for Ash-NLP Service
---
FILE VERSION: v3.1-3e-7-1
LAST MODIFIED: 2025-09-09
PHASE: 3e Step 7 - Model Coordination Refactoring
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Handle model loading, caching, preloading, and pipeline management
"""

import os
import logging
import time
import asyncio
from typing import Dict, Any, Optional

# Import transformers for AI classification
try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Transformers library loaded in ModelPipelineHelper")
except ImportError as e:
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Transformers library not available in ModelPipelineHelper: {e}")

logger = logging.getLogger(__name__)

class ModelPipelineHelper:
    """
    Model Pipeline Management Helper
    
    Handles:
    - Model preloading and warmup
    - Pipeline caching and loading
    - Model cache directory management
    - Container startup optimization
    """
    
    def __init__(self, config_manager, model_coordination_manager):
        """
        Initialize Model Pipeline Helper
        
        Args:
            config_manager: UnifiedConfigManager instance
            model_coordination_manager: Parent ModelCoordinationManager instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ModelPipelineHelper")
        if model_coordination_manager is None:
            raise ValueError("ModelCoordinationManager is required for ModelPipelineHelper")
        
        self.config_manager = config_manager
        self.model_manager = model_coordination_manager
        
        # Model pipeline cache and loading management
        self._model_cache = {}
        self._model_loading_lock = asyncio.Lock()
        
        # Get device configuration for AI models
        self.device = self._get_device_config()
        
        logger.info(f"🔧 ModelPipelineHelper initialized with device: {self.device}")
    
    def _get_device_config(self) -> str:
        """Get device configuration for AI models"""
        try:
            # Get device from hardware settings via model manager
            hardware_settings = self.model_manager.get_hardware_settings()
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
    
    async def preload_models(self):
        """
        Preload all configured models during container startup
        This prevents timeout issues during actual crisis analysis
        """
        try:
            logger.info("Starting model preloading during container startup...")
            
            models = self.model_manager.get_model_definitions()
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
                    pipeline_obj = await self.get_or_load_pipeline(model_name)
                    
                    if pipeline_obj:
                        logger.info(f"Successfully preloaded: {model_type}")
                    else:
                        logger.warning(f"Failed to preload: {model_type}")
                        
                except Exception as e:
                    logger.error(f"Error preloading {model_type}: {e}")
                    
            logger.info(f"Model preloading complete. Cached models: {len(self._model_cache)}")
            
            # Warmup the complete analysis pipeline to eliminate cold start penalty
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
                    model_coordination_manager=self.model_manager,
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
            models = self.model_manager.get_model_definitions()
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
            models = self.model_manager.get_model_definitions()
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

    async def get_or_load_pipeline(self, model_name: str):
        """
        Load or get cached zero-shot classification pipeline
        
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
                cache_dir = self.get_model_cache_dir()
                
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

    def get_cached_pipeline_sync(self, model_name: str):
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

    def get_model_cache_dir(self) -> str:
        """Get model cache directory from configuration"""
        try:
            # First check individual model cache directories
            models = self.model_manager.get_model_definitions()
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

    def get_cached_models(self) -> Dict[str, Any]:
        """Get information about cached models"""
        return {
            'cached_count': len(self._model_cache),
            'cached_models': list(self._model_cache.keys()),
            'cache_available': bool(self._model_cache)
        }

# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_model_pipeline_helper(config_manager, model_coordination_manager) -> ModelPipelineHelper:
    """
    Factory function to create ModelPipelineHelper instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        model_coordination_manager: ModelCoordinationManager instance
        
    Returns:
        ModelPipelineHelper instance
    """
    return ModelPipelineHelper(config_manager, model_coordination_manager)
# ============================================================================

__all__ = [
    'ModelPipelineHelper',
    'create_model_pipeline_helper'
]

logger.info("ModelPipelineHelper v3.1-3e-7-1 loaded - Model pipeline management functionality")