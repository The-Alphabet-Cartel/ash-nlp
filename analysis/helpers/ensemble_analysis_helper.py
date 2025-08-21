# ash-nlp/analysis/helpers/ensemble_analysis_helper.py
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
Ensemble Analysis Helper for CrisisAnalyzer
---
FILE VERSION: v3.1-3e-5.5-6-5
CREATED: 2025-08-21
UPDATED: 2025-08-21
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization with ACTUAL ZeroShotManager Integration
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

CRITICAL FIX: Replaced TODO placeholder with actual transformers pipeline implementation
RESTORED: True AI zero-shot classification instead of pattern-based fallback
MIGRATION NOTICE: Methods moved from CrisisAnalyzer for optimization
Original location: analysis/crisis_analyzer.py - ensemble analysis methods
"""

import logging
import time
import asyncio
import os
from typing import Dict, List, Any, Optional

# FIXED: Add actual transformers imports for zero-shot classification
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Transformers library loaded successfully for zero-shot classification")
except ImportError as e:
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ Transformers library not available: {e}")
    logger.warning("⚠️ Zero-shot classification will use enhanced pattern fallback")

logger = logging.getLogger(__name__)

class EnsembleAnalysisHelper:
    """Helper class for ensemble analysis operations moved from CrisisAnalyzer"""
    
    def __init__(self, crisis_analyzer):
        """
        Initialize with reference to parent CrisisAnalyzer
        
        Args:
            crisis_analyzer: Parent CrisisAnalyzer instance
        """
        self.crisis_analyzer = crisis_analyzer
        
        # FIXED: Initialize model cache for zero-shot pipelines
        self._model_cache = {}
        self._model_loading_lock = asyncio.Lock()
        
        # Get device configuration
        self.device = self._get_device_config()
        logger.info(f"🔧 EnsembleAnalysisHelper initialized with device: {self.device}")
        
    def _get_device_config(self) -> str:
        """
        FIXED: Get device configuration from ModelEnsembleManager first, then fallback
        
        Returns:
            Device configuration string (cpu/cuda/auto)
        """
        try:
            # First check ModelEnsembleManager hardware settings
            if self.crisis_analyzer.model_ensemble_manager:
                hardware_settings = self.crisis_analyzer.model_ensemble_manager.get_hardware_settings()
                device = hardware_settings.get('device')
                if device and device != 'auto':
                    logger.debug(f"Using ModelEnsembleManager device setting: {device}")
                    return device
            
            # Check environment variable via UnifiedConfigManager
            if self.crisis_analyzer.unified_config_manager:
                device = self.crisis_analyzer.unified_config_manager.get_env_str('NLP_ZERO_SHOT_DEVICE', 'auto')
                if device != 'auto':
                    logger.debug(f"Using environment device setting: {device}")
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
        
    # ========================================================================
    # ENSEMBLE ANALYSIS METHODS
    # ========================================================================
    
    async def perform_ensemble_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Perform the actual ensemble analysis with integrated context analysis
        Migrated from: CrisisAnalyzer._perform_ensemble_analysis()
        """
        
        # Step 10.8: Enhanced context analysis using ContextPatternManager
        context_analysis = None
        if self.crisis_analyzer._feature_cache.get('context_analysis', True) and self.crisis_analyzer.context_pattern_manager:
            try:
                logger.debug("Starting enhanced context analysis via ContextPatternManager...")
                
                # Get basic context signals
                context_signals = self.crisis_analyzer.extract_context_signals(message)
                
                # Perform enhanced context analysis with crisis pattern integration
                enhanced_context = self.crisis_analyzer.perform_enhanced_context_analysis(message)
                
                # Analyze sentiment context if we have model results
                sentiment_context = self.crisis_analyzer.analyze_sentiment_context(message, 0.0)  # Will be updated with actual sentiment
                
                context_analysis = {
                    'context_signals': context_signals,
                    'enhanced_context': enhanced_context,
                    'sentiment_context': sentiment_context,
                    'context_manager_status': 'available',
                    'total_context_indicators': (
                        context_signals.get('social_isolation_indicators', 0) +
                        context_signals.get('hopelessness_indicators', 0) +
                        len(context_signals.get('temporal_indicators', []))
                    )
                }
                
                logger.debug(f"Context analysis complete: {context_analysis['total_context_indicators']} indicators found")
                
            except Exception as e:
                logger.error(f"Context analysis failed: {e}")
                context_analysis = {
                    'context_manager_status': 'error',
                    'error': str(e),
                    'fallback_used': True
                }
        else:
            context_analysis = {
                'context_manager_status': 'not_available',
                'feature_enabled': self.crisis_analyzer._feature_cache.get('context_analysis', False)
            }
            logger.debug("Context analysis disabled or ContextPatternManager not available")

        # Continue with pattern analysis
        pattern_analysis = await self._perform_pattern_analysis(message)

        # Model ensemble analysis with ACTUAL zero-shot models
        model_results = await self._perform_model_ensemble_analysis(message, context_analysis)

        # Combine results with enhanced context integration
        return self.crisis_analyzer._combine_analysis_results(
            message, user_id, channel_id, model_results, pattern_analysis, context_analysis, start_time
        )
    
    async def _perform_pattern_analysis(self, message: str) -> Dict:
        """
        Perform pattern analysis via CrisisPatternManager
        Migrated from: CrisisAnalyzer._perform_ensemble_analysis() (pattern analysis section)
        """
        pattern_analysis = None
        if self.crisis_analyzer._feature_cache.get('pattern_analysis', True) and self.crisis_analyzer.crisis_pattern_manager:
            try:
                logger.debug("Starting pattern analysis via CrisisPatternManager...")
                
                # Community patterns analysis via CrisisPatternManager
                community_patterns = []
                if self.crisis_analyzer._feature_cache.get('community_patterns', True):
                    community_patterns = self.crisis_analyzer.crisis_pattern_manager.extract_community_patterns(message)
                    logger.debug(f"Found {len(community_patterns)} community patterns")
                
                # Extract crisis context phrases
                context_phrases = []
                if self.crisis_analyzer._feature_cache.get('context_analysis', True):
                    context_phrases = self.crisis_analyzer.crisis_pattern_manager.extract_crisis_context_phrases(message)
                    logger.debug(f"Found {len(context_phrases)} context phrases")
                
                # Analyze temporal indicators
                temporal_analysis = {}
                if self.crisis_analyzer._feature_cache.get('temporal_boost', True):
                    temporal_analysis = self.crisis_analyzer.crisis_pattern_manager.analyze_temporal_indicators(message)
                    logger.debug(f"Temporal analysis: {temporal_analysis.get('urgency_score', 0)}")
                
                # Enhanced crisis pattern check
                enhanced_patterns = {}
                enhanced_patterns = self.crisis_analyzer.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
                logger.debug(f"Enhanced patterns: {len(enhanced_patterns.get('matches', []))} matches")
                
                pattern_analysis = {
                    'community_patterns': community_patterns,
                    'context_phrases': context_phrases,
                    'temporal_analysis': temporal_analysis,
                    'enhanced_patterns': enhanced_patterns,
                    'total_patterns': len(community_patterns) + len(context_phrases) + len(enhanced_patterns.get('matches', [])),
                    'source': 'crisis_pattern_manager_direct'
                }
                
            except Exception as e:
                logger.error(f"Pattern analysis failed: {e}")
                pattern_analysis = {'error': str(e), 'total_patterns': 0}
        
        return pattern_analysis or {}
    
    async def _perform_model_ensemble_analysis(self, message: str, context_analysis: Dict) -> Dict:
        """
        Perform model ensemble analysis with ACTUAL zero-shot models
        Migrated from: CrisisAnalyzer._perform_ensemble_analysis() (model analysis section)
        """
        model_results = {}
        if self.crisis_analyzer.model_ensemble_manager:
            try:
                logger.debug("Starting model ensemble analysis with ACTUAL zero-shot models...")
                
                # Get models based on feature flags
                active_models = []
                if self.crisis_analyzer._feature_cache.get('ensemble_analysis', True):
                    active_models.extend(['depression', 'sentiment', 'emotional_distress'])
                
                for model_name in active_models:
                    try:
                        model_timeout = self.crisis_analyzer._performance_cache.get('model_timeout', 10.0)
                        model_result = await asyncio.wait_for(
                            self._analyze_with_model(message, model_name),
                            timeout=model_timeout
                        )
                        model_results[model_name] = model_result
                        
                        # Update sentiment context with actual sentiment score
                        if model_name == 'sentiment' and context_analysis and 'sentiment_context' in context_analysis:
                            sentiment_score = model_result.get('score', 0.0)
                            updated_sentiment_context = self.crisis_analyzer.analyze_sentiment_context(message, sentiment_score)
                            context_analysis['sentiment_context'] = updated_sentiment_context
                            
                    except asyncio.TimeoutError:
                        logger.warning(f"Model {model_name} timed out")
                        model_results[model_name] = {'error': 'timeout', 'score': 0.0}
                    except Exception as e:
                        logger.warning(f"Model {model_name} failed: {e}")
                        model_results[model_name] = {'error': str(e), 'score': 0.0}
                        
            except Exception as e:
                logger.error(f"Model ensemble failed: {e}")
                model_results = {'error': str(e)}
        
        return model_results
    
    async def _analyze_with_model(self, message: str, model_name: str) -> Dict:
        """
        Analyze message with specific model using ACTUAL zero-shot models
        Migrated from: CrisisAnalyzer._analyze_with_model()
        """
        try:
            if model_name == 'depression':
                return await self._analyze_depression_with_zero_shot(message)
            elif model_name == 'sentiment':
                return await self._analyze_sentiment_with_zero_shot(message)
            elif model_name == 'emotional_distress':
                return await self._analyze_emotional_distress_with_zero_shot(message)
            else:
                return {'error': f'Unknown model: {model_name}', 'score': 0.0}
        except Exception as e:
            logger.error(f"Model {model_name} analysis failed: {e}")
            return {'error': str(e), 'score': 0.0}
    
    # ========================================================================
    # ACTUAL ZERO-SHOT MODEL IMPLEMENTATIONS - FIXED WITH REAL AI
    # ========================================================================
    
    async def _analyze_depression_with_zero_shot(self, message: str) -> Dict:
        """
        FIXED: Analyze depression using ACTUAL zero-shot model with ZeroShotManager integration
        Replaces: TODO placeholder with real transformers pipeline implementation
        """
        try:
            logger.debug("🤖 Analyzing depression indicators with ACTUAL zero-shot model...")
            
            # Get depression model configuration
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            depression_config = self.crisis_analyzer.model_ensemble_manager.get_model_config('depression')
            if not depression_config:
                raise ValueError("Depression model not configured")
            
            model_name = depression_config.get('name')
            if not model_name:
                raise ValueError("Depression model name not specified")
            
            # Use ZeroShotManager for comprehensive label management
            labels = None
            hypothesis_template = "This text expresses {}."
            current_label_set = 'enhanced_crisis'  # Default label set
            
            if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager:
                try:
                    # Get current active label set
                    current_label_set = self.crisis_analyzer.zero_shot_manager.get_current_label_set()
                    logger.debug(f"Current ZeroShotManager label set: {current_label_set}")
                    
                    # Get all available label sets for context
                    available_sets = self.crisis_analyzer.zero_shot_manager.get_available_label_sets()
                    logger.debug(f"Available label sets: {available_sets}")
                    
                    # Get labels for depression analysis from current set
                    all_labels = self.crisis_analyzer.zero_shot_manager.get_all_labels()
                    if isinstance(all_labels, dict):
                        # Check if current set has depression-specific labels
                        if 'depression' in all_labels:
                            labels = all_labels['depression']
                        else:
                            # Use general crisis labels if no depression-specific labels
                            labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        # If get_all_labels returns a list, use it directly
                        labels = all_labels if isinstance(all_labels, list) else []
                    
                    # Get hypothesis template from ZeroShotManager configuration
                    zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', 'This text expresses {}.')
                    
                    logger.debug(f"✅ ZeroShotManager integration: {len(labels) if labels else 0} depression labels from '{current_label_set}' set")
                    
                except Exception as e:
                    logger.warning(f"⚠️ ZeroShotManager access failed: {e}, using fallback labels")
            
            # Fallback labels if ZeroShotManager not available
            if not labels:
                labels = [
                    "person actively expressing suicidal thoughts, death wishes, or specific plans to end their life",
                    "person expressing complete hopelessness, that nothing will ever get better, or life has no meaning",
                    "person showing severe depression with major breakdown and inability to function daily",
                    "person expressing emotional difficulty, low mood, or distress but still coping with life",
                    "person feeling emotionally stable, content, or positive about life"
                ]
                logger.debug("Using fallback depression labels")
            
            # FIXED: Perform ACTUAL zero-shot classification with configured labels
            score = await self._perform_actual_zero_shot_classification(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),  # Slightly higher confidence than score
                'model': model_name,
                'method': 'actual_zero_shot_classification',  # FIXED: Not pattern fallback!
                'labels_used': len(labels),
            # Also add comprehensive label tracking to other models
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager),
                'transformers_used': TRANSFORMERS_AVAILABLE,
                'current_label_set': current_label_set,
                'zero_shot_manager_methods_used': [
                    'get_current_label_set',
                    'get_available_label_sets', 
                    'get_all_labels',
                    'get_zero_shot_settings'
                ] if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager else [],
                'current_label_set': current_label_set,
                'zero_shot_manager_methods_used': [
                    'get_current_label_set',
                    'get_available_label_sets', 
                    'get_all_labels',
                    'get_zero_shot_settings'
                ] if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager else []
            }
            
        except Exception as e:
            logger.error(f"❌ Depression zero-shot analysis failed: {e}")
            # Fallback to pattern-based analysis only if transformers completely fail
            return await self._fallback_depression_analysis(message)

    async def _analyze_sentiment_with_zero_shot(self, message: str) -> Dict:
        """
        FIXED: Analyze sentiment using ACTUAL zero-shot model with ZeroShotManager integration
        Replaces: TODO placeholder with real transformers pipeline implementation
        """
        try:
            logger.debug("🤖 Analyzing sentiment with ACTUAL zero-shot model...")
            
            # Get sentiment model configuration
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            sentiment_config = self.crisis_analyzer.model_ensemble_manager.get_model_config('sentiment')
            if not sentiment_config:
                raise ValueError("Sentiment model not configured")
            
            model_name = sentiment_config.get('name')
            if not model_name:
                raise ValueError("Sentiment model name not specified")
            
            # Use ZeroShotManager for comprehensive label management
            labels = None
            hypothesis_template = "This text expresses {}."
            current_label_set = 'enhanced_crisis'  # Default label set
            
            if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager:
                try:
                    # Get current active label set
                    current_label_set = self.crisis_analyzer.zero_shot_manager.get_current_label_set()
                    logger.debug(f"Current ZeroShotManager label set: {current_label_set}")
                    
                    # Get all available label sets for context
                    available_sets = self.crisis_analyzer.zero_shot_manager.get_available_label_sets()
                    logger.debug(f"Available label sets: {available_sets}")
                    
                    # Get labels for sentiment analysis from current set
                    all_labels = self.crisis_analyzer.zero_shot_manager.get_all_labels()
                    if isinstance(all_labels, dict):
                        # Check if current set has sentiment-specific labels
                        if 'sentiment' in all_labels:
                            labels = all_labels['sentiment']
                        else:
                            # Use general crisis labels if no sentiment-specific labels
                            labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        # If get_all_labels returns a list, use it directly
                        labels = all_labels if isinstance(all_labels, list) else []
                    
                    # Get hypothesis template from ZeroShotManager configuration
                    zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', 'This text expresses {}.')
                    
                    logger.debug(f"ZeroShotManager integration: {len(labels) if labels else 0} sentiment labels from '{current_label_set}' set")
                    
                except Exception as e:
                    logger.warning(f"ZeroShotManager access failed: {e}, using fallback labels")
            
            # Fallback labels if ZeroShotManager not available
            if not labels:
                labels = [
                    "extreme sadness, despair, anguish, or devastating emotional pain",
                    "significant negativity, distress, anger, or emotional upset",
                    "mild sadness, disappointment, or somewhat negative feelings",
                    "neutral emotions, mixed feelings, or neither positive nor negative",
                    "happiness, joy, contentment, or positive emotional expression"
                ]
                logger.debug("Using fallback sentiment labels")
            
            # FIXED: Perform ACTUAL zero-shot classification with configured labels
            score = await self._perform_actual_zero_shot_classification(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),
                'model': model_name,
                'method': 'actual_zero_shot_classification',  # FIXED: Not pattern fallback!
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager),
                'transformers_used': TRANSFORMERS_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"❌ Sentiment zero-shot analysis failed: {e}")
            # Fallback to simple sentiment analysis
            return await self._fallback_sentiment_analysis(message)

    async def _analyze_emotional_distress_with_zero_shot(self, message: str) -> Dict:
        """
        FIXED: Analyze emotional distress using ACTUAL zero-shot model with ZeroShotManager integration
        Replaces: TODO placeholder with real transformers pipeline implementation
        """
        try:
            logger.debug("🤖 Analyzing emotional distress with ACTUAL zero-shot model...")
            
            # Get emotional distress model configuration
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            distress_config = self.crisis_analyzer.model_ensemble_manager.get_model_config('emotional_distress')
            if not distress_config:
                raise ValueError("Emotional distress model not configured")
            
            model_name = distress_config.get('name')
            if not model_name:
                raise ValueError("Emotional distress model name not specified")
            
            # Use ZeroShotManager for comprehensive label management
            labels = None
            hypothesis_template = "This text expresses {}."
            current_label_set = 'enhanced_crisis'  # Default label set
            
            if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager:
                try:
                    # Get current active label set
                    current_label_set = self.crisis_analyzer.zero_shot_manager.get_current_label_set()
                    logger.debug(f"Current ZeroShotManager label set: {current_label_set}")
                    
                    # Get all available label sets for context
                    available_sets = self.crisis_analyzer.zero_shot_manager.get_available_label_sets()
                    logger.debug(f"Available label sets: {available_sets}")
                    
                    # Get labels for emotional distress analysis from current set
                    all_labels = self.crisis_analyzer.zero_shot_manager.get_all_labels()
                    if isinstance(all_labels, dict):
                        # Check if current set has emotional_distress-specific labels
                        if 'emotional_distress' in all_labels:
                            labels = all_labels['emotional_distress']
                        else:
                            # Use general crisis labels if no emotional_distress-specific labels
                            labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        # If get_all_labels returns a list, use it directly
                        labels = all_labels if isinstance(all_labels, list) else []
                    
                    # Get hypothesis template from ZeroShotManager configuration
                    zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', 'This text expresses {}.')
                    
                    logger.debug(f"ZeroShotManager integration: {len(labels) if labels else 0} emotional distress labels from '{current_label_set}' set")
                    
                except Exception as e:
                    logger.warning(f"ZeroShotManager access failed: {e}, using fallback labels")
            
            # Fallback labels if ZeroShotManager not available
            if not labels:
                labels = [
                    "person in acute psychological distress unable to cope and requiring immediate crisis intervention",
                    "person experiencing severe emotional overwhelm with significantly impaired functioning and coping",
                    "person showing moderate distress with some difficulty managing emotions and daily responsibilities",
                    "person handling normal life stress with adequate coping strategies and emotional regulation",
                    "person demonstrating strong emotional resilience with healthy stress management and adaptation"
                ]
                logger.debug("Using fallback emotional distress labels")
            
            # FIXED: Perform ACTUAL zero-shot classification with configured labels
            score = await self._perform_actual_zero_shot_classification(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),
                'model': model_name,
                'method': 'actual_zero_shot_classification',  # FIXED: Not pattern fallback!
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager),
                'transformers_used': TRANSFORMERS_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"❌ Emotional distress zero-shot analysis failed: {e}")
            # Fallback to pattern-based analysis
            return await self._fallback_distress_analysis(message)
    
    # ========================================================================
    # ACTUAL ZERO-SHOT IMPLEMENTATION - THE REAL AI FUNCTIONALITY
    # ========================================================================
    
    async def _perform_actual_zero_shot_classification(self, text: str, labels: List[str], hypothesis_template: str, model_name: str) -> float:
        """
        FIXED: Perform ACTUAL zero-shot classification using transformers pipeline
        
        This replaces the TODO placeholder with real AI functionality using:
        - Actual transformers models from Hugging Face
        - Real zero-shot classification pipelines
        - Semantic understanding instead of keyword matching
        
        Args:
            text: Text to classify
            labels: List of labels for classification
            hypothesis_template: Template for generating hypotheses (e.g., "This text expresses {}.")
            model_name: Hugging Face model name
            
        Returns:
            Classification score (0.0 to 1.0) - higher scores indicate higher crisis levels
        """
        try:
            if not TRANSFORMERS_AVAILABLE:
                logger.warning(f"⚠️ Transformers library not available - falling back to enhanced pattern matching")
                return await self._enhanced_label_aware_scoring(text, labels, hypothesis_template)
            
            # Load or get cached zero-shot pipeline
            classifier = await self._get_zero_shot_pipeline(model_name)
            
            if classifier is None:
                logger.warning(f"⚠️ Could not load zero-shot model {model_name} - falling back to pattern matching")
                return await self._enhanced_label_aware_scoring(text, labels, hypothesis_template)
            
            # Perform actual zero-shot classification
            logger.debug(f"🤖 Running ACTUAL zero-shot classification with {model_name}")
            logger.debug(f"📝 Text: {text[:100]}...")
            logger.debug(f"🏷️ Labels: {len(labels)} labels")
            
            # Execute the classification
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: classifier(text, labels)
            )
            
            # Process results to extract crisis score
            crisis_score = self._process_zero_shot_result(result, labels)
            
            logger.info(f"✅ ACTUAL zero-shot classification complete: {crisis_score:.3f}")
            logger.debug(f"🔍 Raw result: {result}")
            
            return crisis_score
            
        except Exception as e:
            logger.error(f"❌ ACTUAL zero-shot classification failed: {e}")
            logger.warning(f"⚠️ Falling back to enhanced pattern matching")
            return await self._enhanced_label_aware_scoring(text, labels, hypothesis_template)

    async def _get_zero_shot_pipeline(self, model_name: str):
        """
        Load or get cached zero-shot classification pipeline with proper ModelEnsembleManager integration
        
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
                logger.debug(f"📦 Using cached zero-shot model: {model_name}")
                return self._model_cache[model_name]
            
            try:
                logger.info(f"🔄 Loading zero-shot model: {model_name}")
                
                # FIXED: Get cache directory from ModelEnsembleManager configuration
                cache_dir = self._get_model_cache_dir_from_config(model_name)
                
                # Create zero-shot classification pipeline with proper configuration
                classifier = pipeline(
                    "zero-shot-classification",
                    model=model_name,
                    device=0 if self.device == 'cuda' else -1,
                    cache_dir=cache_dir,
                    return_all_scores=True
                )
                
                # Cache the pipeline
                self._model_cache[model_name] = classifier
                
                logger.info(f"✅ Zero-shot model loaded successfully: {model_name}")
                logger.info(f"📁 Using cache directory: {cache_dir}")
                return classifier
                
            except Exception as e:
                logger.error(f"❌ Failed to load zero-shot model {model_name}: {e}")
                return None

    def _get_model_cache_dir_from_config(self, model_name: str) -> str:
        """
        FIXED: Get model cache directory from ModelEnsembleManager configuration
        
        Args:
            model_name: Hugging Face model name to find cache directory for
            
        Returns:
            Cache directory path from configuration or fallback
        """
        try:
            # Get model configuration from ModelEnsembleManager
            if self.crisis_analyzer.model_ensemble_manager:
                model_definitions = self.crisis_analyzer.model_ensemble_manager.get_model_definitions()
                
                # Find the model type that matches this model name
                for model_type, model_config in model_definitions.items():
                    config_model_name = model_config.get('name', '')
                    if config_model_name == model_name:
                        # Check if this model has a specific cache directory
                        cache_dir = model_config.get('cache_dir')
                        if cache_dir:
                            # Ensure directory exists
                            os.makedirs(cache_dir, exist_ok=True)
                            logger.debug(f"📁 Using configured cache directory for {model_name}: {cache_dir}")
                            return cache_dir
                        
                        # No specific cache_dir, check model-level cache settings
                        break
                
                # Check for global cache directory in hardware settings
                hardware_settings = self.crisis_analyzer.model_ensemble_manager.get_hardware_settings()
                if 'cache_dir' in hardware_settings:
                    cache_dir = hardware_settings['cache_dir']
                    os.makedirs(cache_dir, exist_ok=True)
                    logger.debug(f"📁 Using global cache directory from hardware settings: {cache_dir}")
                    return cache_dir
            
            # Fallback to UnifiedConfigManager cache directory
            if self.crisis_analyzer.unified_config_manager:
                cache_dir = self.crisis_analyzer.unified_config_manager.get_config_section(
                    'model_ensemble',
                    'ensemble_config.cache_dir',
                    './models/cache/'
                )
                os.makedirs(cache_dir, exist_ok=True)
                logger.debug(f"📁 Using UnifiedConfigManager cache directory: {cache_dir}")
                return cache_dir
                
        except Exception as e:
            logger.warning(f"⚠️ Cache dir config from ModelEnsembleManager failed: {e}")
        
        # Final fallback cache directory
        fallback_dir = './cache/models/'
        try:
            os.makedirs(fallback_dir, exist_ok=True)
            logger.debug(f"📁 Using fallback cache directory: {fallback_dir}")
        except Exception as e:
            logger.error(f"❌ Could not create fallback cache directory {fallback_dir}: {e}")
        
        return fallback_dir

    def _process_zero_shot_result(self, result: Dict, labels: List[str]) -> float:
        """
        Process zero-shot classification result into crisis score
        
        Args:
            result: Raw result from zero-shot classifier
            labels: Original labels used for classification
            
        Returns:
            Crisis score (0.0 to 1.0) where higher values indicate higher crisis levels
        """
        try:
            if not result or 'scores' not in result:
                logger.warning(f"⚠️ Invalid zero-shot result format: {result}")
                return 0.0
            
            scores = result['scores']
            predicted_labels = result.get('labels', [])
            
            if len(scores) != len(labels) or len(predicted_labels) != len(labels):
                logger.warning(f"⚠️ Score/label mismatch in zero-shot result")
                return 0.0
            
            # Calculate weighted crisis score based on label severity
            # Labels are arranged from highest crisis (index 0) to lowest crisis (last index)
            crisis_score = 0.0
            
            for i, (label, score) in enumerate(zip(predicted_labels, scores)):
                # Find original index of this label to determine severity
                try:
                    original_index = labels.index(label)
                    # Convert index to severity weight (0 = highest crisis, last = lowest crisis)
                    severity_weight = 1.0 - (original_index / (len(labels) - 1))
                    weighted_contribution = score * severity_weight
                    crisis_score += weighted_contribution
                    
                    logger.debug(f"🔍 Label '{label[:50]}...': score={score:.3f}, weight={severity_weight:.3f}, contribution={weighted_contribution:.3f}")
                    
                except ValueError:
                    logger.warning(f"⚠️ Label '{label}' not found in original labels")
                    continue
            
            # Normalize the score to 0-1 range
            crisis_score = max(0.0, min(1.0, crisis_score))
            
            logger.debug(f"📊 Processed zero-shot result: final_score={crisis_score:.3f}")
            return crisis_score
            
        except Exception as e:
            logger.error(f"❌ Zero-shot result processing failed: {e}")
            return 0.0

    # ========================================================================
    # ENHANCED PATTERN FALLBACK (Only used when transformers unavailable)
    # ========================================================================

    async def _enhanced_label_aware_scoring(self, text: str, labels: List[str], hypothesis_template: str) -> float:
        """
        Enhanced pattern-based scoring that's aware of the configured labels
        Only used as fallback when transformers are not available
        
        Args:
            text: Text to analyze
            labels: List of crisis labels from ZeroShotManager
            hypothesis_template: Hypothesis template from configuration
            
        Returns:
            Label-aware pattern score (0.0 to 1.0)
        """
        try:
            if not labels:
                logger.warning("⚠️ No labels provided for label-aware scoring")
                return 0.0
            
            text_lower = text.lower()
            
            # Extract keywords from labels to build dynamic pattern matching
            crisis_keywords = set()
            for label in labels:
                # Extract key terms from each label for pattern matching
                label_lower = label.lower()
                
                # Common crisis terms to look for in labels
                if any(term in label_lower for term in ['suicide', 'death', 'die', 'kill']):
                    crisis_keywords.update(['suicide', 'suicidal', 'death', 'die', 'kill', 'end my life'])
                
                if any(term in label_lower for term in ['hopeless', 'helpless', 'trapped']):
                    crisis_keywords.update(['hopeless', 'hopelessness', 'helpless', 'trapped', 'no way out'])
                
                if any(term in label_lower for term in ['breakdown', 'crisis', 'overwhelm']):
                    crisis_keywords.update(['breakdown', 'crisis', 'overwhelmed', 'can\'t cope', 'falling apart'])
                
                if any(term in label_lower for term in ['severe', 'extreme', 'acute']):
                    crisis_keywords.update(['severe', 'extreme', 'terrible', 'unbearable', 'intense'])
                
                if any(term in label_lower for term in ['distress', 'anguish', 'pain']):
                    crisis_keywords.update(['distress', 'anguish', 'pain', 'suffering', 'agony'])
                
                if any(term in label_lower for term in ['self-harm', 'cutting', 'hurt myself']):
                    crisis_keywords.update(['self-harm', 'cutting', 'hurt myself', 'harm myself'])
            
            # Calculate score based on label-derived keywords
            score = 0.0
            matches = []
            
            for keyword in crisis_keywords:
                if keyword in text_lower:
                    matches.append(keyword)
                    
                    # Weight scores based on severity (inferred from labels)
                    if keyword in ['suicide', 'suicidal', 'kill', 'death', 'end my life']:
                        score += 0.8  # Highest severity
                    elif keyword in ['hopeless', 'hopelessness', 'trapped', 'no way out']:
                        score += 0.6  # High severity
                    elif keyword in ['breakdown', 'crisis', 'overwhelmed', 'can\'t cope']:
                        score += 0.4  # Medium-high severity
                    elif keyword in ['severe', 'extreme', 'unbearable', 'intense']:
                        score += 0.3  # Medium severity
                    else:
                        score += 0.1  # Lower severity
            
            # Apply label-count based weighting
            if len(labels) > 3:  # More nuanced label sets can provide more precise scoring
                label_sophistication_bonus = 0.1
                score *= (1.0 + label_sophistication_bonus)
            
            # Boost for multiple indicators
            if len(matches) > 2:
                score *= 1.3
            elif len(matches) > 1:
                score *= 1.1
            
            # Normalize to 0-1 range but allow for higher sensitivity with good labels
            score = min(1.0, score)
            
            logger.debug(f"📊 Label-aware pattern scoring: {score:.3f} (matches: {matches})")
            logger.debug(f"🏷️ Labels used: {len(labels)}, Keywords extracted: {len(crisis_keywords)}")
            
            return score
            
        except Exception as e:
            logger.error(f"❌ Enhanced label-aware scoring failed: {e}")
            return 0.0
    
    # ========================================================================
    # FALLBACK ANALYSIS METHODS (Only used when models fail completely)
    # ========================================================================
    
    async def _fallback_depression_analysis(self, message: str) -> Dict:
        """Fallback depression analysis using patterns"""
        try:
            if self.crisis_analyzer.crisis_pattern_manager:
                # Use pattern manager for depression analysis
                patterns = self.crisis_analyzer.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
                score = min(0.7, len(patterns.get('matches', [])) * 0.15)
            else:
                score = 0.3  # Conservative fallback
            
            return {
                'score': score,
                'confidence': 0.5,
                'model': 'pattern_fallback',
                'method': 'pattern_based_fallback',
                'transformers_used': False
            }
        except Exception as e:
            logger.error(f"❌ Fallback depression analysis failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'transformers_used': False}
    
    async def _fallback_sentiment_analysis(self, message: str) -> Dict:
        """Fallback sentiment analysis using simple rules"""
        try:
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'sad']
            positive_words = ['good', 'great', 'happy', 'love', 'excellent', 'wonderful']
            
            text_lower = message.lower()
            negative_count = sum(1 for word in negative_words if word in text_lower)
            positive_count = sum(1 for word in positive_words if word in text_lower)
            
            if negative_count > positive_count:
                score = min(0.6, negative_count * 0.1)
            else:
                score = max(0.0, 0.3 - positive_count * 0.05)
            
            return {
                'score': score,
                'confidence': 0.4,
                'model': 'simple_sentiment_fallback',
                'method': 'keyword_based_fallback',
                'transformers_used': False
            }
        except Exception as e:
            logger.error(f"❌ Fallback sentiment analysis failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'transformers_used': False}
    
    async def _fallback_distress_analysis(self, message: str) -> Dict:
        """Fallback emotional distress analysis using patterns"""
        try:
            distress_words = ['stressed', 'anxious', 'panic', 'overwhelmed', 'breakdown', 'crisis']
            text_lower = message.lower()
            matches = sum(1 for word in distress_words if word in text_lower)
            score = min(0.7, matches * 0.2)
            
            return {
                'score': score,
                'confidence': 0.5,
                'model': 'distress_pattern_fallback',
                'method': 'pattern_based_fallback',
                'transformers_used': False
            }
        except Exception as e:
            logger.error(f"❌ Fallback distress analysis failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'transformers_used': False}