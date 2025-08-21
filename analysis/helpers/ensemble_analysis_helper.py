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
Ensemble Analysis Helper for CrisisAnalyzer - PHASE 1 RENAME COMPLETE
---
FILE VERSION: v3.1-3e-5.5-6-7-PHASE2
CREATED: 2025-08-21
UPDATED: 2025-08-21
PHASE: 3e Sub-step 5.5-6 - PHASE 2: Flow Reordering to AI-First Architecture
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PHASE 1 COMPLETE: Method names updated to follow AI-first architectural conventions
PHASE 2 COMPLETE: Analysis flow reordered to run AI-first with pattern enhancement
- Primary AI analysis runs first using zero-shot semantic classification
- Pattern analysis now enhances AI results instead of running independently  
- Pattern boost factors calculated based on AI confidence levels
- Clear logging indicates AI-first, pattern-enhancement flow
- Emergency fallbacks only trigger when AI completely fails
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
        PHASE 2: AI-FIRST ensemble analysis with pattern enhancement
        ARCHITECTURE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
        
        Migrated from: CrisisAnalyzer._perform_ensemble_analysis()
        PHASE 2 CHANGE: Reordered to run AI analysis first, then enhance with patterns
        """
        
        # Step 1: Enhanced context analysis using ContextPatternManager (unchanged)
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

        # Step 2: PRIMARY AI ensemble analysis with ACTUAL zero-shot models
        logger.info("PHASE 2: Starting PRIMARY AI semantic classification...")
        model_results = await self.analyze_crisis_with_ensemble_ai(message, context_analysis)

        # Step 3: SECONDARY pattern enhancement of AI results
        logger.info("PHASE 2: Enhancing AI results with pattern analysis...")
        pattern_analysis = await self.enhance_ai_with_pattern_analysis(message, model_results)

        # Step 4: Combine AI results with pattern enhancements
        logger.info("PHASE 2: Combining AI results with pattern enhancements...")
        return self.crisis_analyzer._combine_analysis_results(
            message, user_id, channel_id, model_results, pattern_analysis, context_analysis, start_time
        )
    
    async def enhance_ai_with_pattern_analysis(self, message: str, ai_results: Dict) -> Dict:
        """
        PHASE 2: SECONDARY pattern enhancement of AI results (was _perform_pattern_analysis)
        ENHANCEMENT: Analyzes patterns to boost/refine AI classification scores
        
        Args:
            message: Original message text
            ai_results: Results from AI ensemble analysis to be enhanced
            
        Returns:
            Enhanced pattern analysis that can boost AI confidence scores
        """
        pattern_analysis = None
        if self.crisis_analyzer._feature_cache.get('pattern_analysis', True) and self.crisis_analyzer.crisis_pattern_manager:
            try:
                logger.debug("PHASE 2: Analyzing patterns to enhance AI results...")
                
                # Extract AI confidence for pattern enhancement decisions
                ai_confidence = 0.0
                ai_score = 0.0
                if ai_results:
                    # Calculate average AI confidence and score
                    valid_results = [r for r in ai_results.values() if isinstance(r, dict) and 'score' in r]
                    if valid_results:
                        ai_score = sum(r.get('score', 0.0) for r in valid_results) / len(valid_results)
                        ai_confidence = sum(r.get('confidence', 0.0) for r in valid_results) / len(valid_results)
                
                logger.debug(f"PHASE 2: AI baseline - score: {ai_score:.3f}, confidence: {ai_confidence:.3f}")
                
                # Community patterns analysis for AI enhancement
                community_patterns = []
                if self.crisis_analyzer._feature_cache.get('community_patterns', True):
                    community_patterns = self.crisis_analyzer.crisis_pattern_manager.extract_community_patterns(message)
                    logger.debug(f"Found {len(community_patterns)} community patterns for AI enhancement")
                
                # Extract crisis context phrases for AI enhancement
                context_phrases = []
                if self.crisis_analyzer._feature_cache.get('context_analysis', True):
                    context_phrases = self.crisis_analyzer.crisis_pattern_manager.extract_crisis_context_phrases(message)
                    logger.debug(f"Found {len(context_phrases)} context phrases for AI enhancement")
                
                # Analyze temporal indicators for AI enhancement
                temporal_analysis = {}
                if self.crisis_analyzer._feature_cache.get('temporal_boost', True):
                    temporal_analysis = self.crisis_analyzer.crisis_pattern_manager.analyze_temporal_indicators(message)
                    logger.debug(f"Temporal analysis for AI enhancement: {temporal_analysis.get('urgency_score', 0)}")
                
                # Enhanced crisis pattern check for AI enhancement
                enhanced_patterns = {}
                enhanced_patterns = self.crisis_analyzer.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
                logger.debug(f"Enhanced patterns for AI enhancement: {len(enhanced_patterns.get('matches', []))} matches")
                
                # Calculate pattern enhancement factors
                pattern_boost_factor = self._calculate_pattern_boost_factor(
                    community_patterns, context_phrases, temporal_analysis, enhanced_patterns, ai_confidence
                )
                
                pattern_analysis = {
                    'community_patterns': community_patterns,
                    'context_phrases': context_phrases,
                    'temporal_analysis': temporal_analysis,
                    'enhanced_patterns': enhanced_patterns,
                    'total_patterns': len(community_patterns) + len(context_phrases) + len(enhanced_patterns.get('matches', [])),
                    'source': 'crisis_pattern_manager_enhancement',
                    'ai_enhancement_role': True,
                    'ai_baseline_score': ai_score,
                    'ai_baseline_confidence': ai_confidence,
                    'pattern_boost_factor': pattern_boost_factor,
                    'enhancement_mode': 'ai_first_pattern_enhancement'
                }
                
                logger.info(f"PHASE 2: Pattern enhancement analysis complete - boost factor: {pattern_boost_factor:.3f}")
                
            except Exception as e:
                logger.error(f"Pattern enhancement analysis failed: {e}")
                pattern_analysis = {
                    'error': str(e), 
                    'total_patterns': 0,
                    'ai_enhancement_role': True,
                    'enhancement_mode': 'error_fallback'
                }
        else:
            logger.debug("Pattern enhancement disabled or CrisisPatternManager not available")
            pattern_analysis = {
                'ai_enhancement_role': True,
                'enhancement_mode': 'disabled',
                'total_patterns': 0
            }
        
        return pattern_analysis or {}
    
    def _calculate_pattern_boost_factor(self, community_patterns: List, context_phrases: List, 
                                       temporal_analysis: Dict, enhanced_patterns: Dict, ai_confidence: float) -> float:
        """
        Calculate how much patterns should boost AI confidence scores
        
        Args:
            community_patterns: Community-specific patterns found
            context_phrases: Crisis context phrases found  
            temporal_analysis: Temporal urgency indicators
            enhanced_patterns: Enhanced crisis patterns
            ai_confidence: Baseline AI confidence to determine boost amount
            
        Returns:
            Pattern boost factor (0.0 to 1.5) to multiply AI scores
        """
        try:
            base_boost = 1.0  # No boost by default
            
            # Community pattern boost (max +0.2)
            if community_patterns:
                community_boost = min(0.2, len(community_patterns) * 0.05)
                base_boost += community_boost
                logger.debug(f"Community pattern boost: +{community_boost:.3f}")
            
            # Context phrase boost (max +0.15)  
            if context_phrases:
                context_boost = min(0.15, len(context_phrases) * 0.03)
                base_boost += context_boost
                logger.debug(f"Context phrase boost: +{context_boost:.3f}")
            
            # Temporal urgency boost (max +0.1)
            temporal_score = temporal_analysis.get('urgency_score', 0.0)
            if temporal_score > 0:
                temporal_boost = min(0.1, temporal_score * 0.1)
                base_boost += temporal_boost
                logger.debug(f"Temporal urgency boost: +{temporal_boost:.3f}")
            
            # Enhanced pattern boost (max +0.15)
            enhanced_matches = enhanced_patterns.get('matches', [])
            if enhanced_matches:
                enhanced_boost = min(0.15, len(enhanced_matches) * 0.05)
                base_boost += enhanced_boost
                logger.debug(f"Enhanced pattern boost: +{enhanced_boost:.3f}")
            
            # Limit total boost based on AI confidence
            # High AI confidence = less pattern boost needed
            # Low AI confidence = more pattern boost helpful
            confidence_modifier = 1.0 + (1.0 - ai_confidence) * 0.3
            final_boost = min(1.5, base_boost * confidence_modifier)
            
            logger.debug(f"Pattern boost calculation: base={base_boost:.3f}, confidence_mod={confidence_modifier:.3f}, final={final_boost:.3f}")
            return final_boost
            
        except Exception as e:
            logger.error(f"Pattern boost calculation failed: {e}")
            return 1.0  # No boost on error
    
    async def analyze_crisis_with_ensemble_ai(self, message: str, context_analysis: Dict) -> Dict:
        """
        RENAMED: Primary AI ensemble analysis method (was _perform_model_ensemble_analysis)
        AI-FIRST: This method performs the primary semantic classification using zero-shot models
        """
        model_results = {}
        if self.crisis_analyzer.model_ensemble_manager:
            try:
                logger.debug("Starting AI ensemble analysis with ACTUAL zero-shot models...")
                
                # Get models based on feature flags
                active_models = []
                if self.crisis_analyzer._feature_cache.get('ensemble_analysis', True):
                    active_models.extend(['depression', 'sentiment', 'emotional_distress'])
                
                for model_name in active_models:
                    try:
                        model_timeout = self.crisis_analyzer._performance_cache.get('model_timeout', 10.0)
                        model_result = await asyncio.wait_for(
                            self.classify_crisis_with_ai_model(message, model_name),
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
    
    async def classify_crisis_with_ai_model(self, message: str, model_name: str) -> Dict:
        """
        RENAMED: Classify crisis using specific AI model (was _analyze_with_model)
        AI-FIRST: Primary method for individual model classification
        """
        try:
            if model_name == 'depression':
                return await self.detect_depression_semantically(message)
            elif model_name == 'sentiment':
                return await self.detect_sentiment_semantically(message)
            elif model_name == 'emotional_distress':
                return await self.detect_distress_semantically(message)
            else:
                return {'error': f'Unknown model: {model_name}', 'score': 0.0}
        except Exception as e:
            logger.error(f"Model {model_name} analysis failed: {e}")
            return {'error': str(e), 'score': 0.0}
    
    # ========================================================================
    # PRIMARY AI SEMANTIC DETECTION METHODS - AI-FIRST NAMING
    # ========================================================================
    
    async def detect_depression_semantically(self, message: str) -> Dict:
        """
        RENAMED: AI-FIRST semantic depression detection (was _analyze_depression_with_zero_shot)
        PRIMARY: Uses zero-shot AI models for semantic classification
        """
        try:
            logger.debug("🤖 Detecting depression indicators with ACTUAL zero-shot AI model...")
            
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
            
            # AI-FIRST: Perform ACTUAL zero-shot classification with configured labels
            score = await self.analyze_crisis_with_zero_shot_classification(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),  # Slightly higher confidence than score
                'model': model_name,
                'method': 'ai_semantic_classification',  # AI-FIRST: Clear AI method indication
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager),
                'transformers_used': TRANSFORMERS_AVAILABLE,
                'current_label_set': current_label_set,
                'zero_shot_manager_methods_used': [
                    'get_current_label_set',
                    'get_available_label_sets', 
                    'get_all_labels',
                    'get_zero_shot_settings'
                ] if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager else []
            }
            
        except Exception as e:
            logger.error(f"❌ Depression semantic detection failed: {e}")
            # Emergency fallback only when transformers completely fail
            return await self.emergency_depression_classification(message)

    async def detect_sentiment_semantically(self, message: str) -> Dict:
        """
        RENAMED: AI-FIRST semantic sentiment detection (was _analyze_sentiment_with_zero_shot)
        PRIMARY: Uses zero-shot AI models for semantic classification
        """
        try:
            logger.debug("🤖 Detecting sentiment with ACTUAL zero-shot AI model...")
            
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
            
            # AI-FIRST: Perform ACTUAL zero-shot classification with configured labels
            score = await self.analyze_crisis_with_zero_shot_classification(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),
                'model': model_name,
                'method': 'ai_semantic_classification',  # AI-FIRST: Clear AI method indication
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager),
                'transformers_used': TRANSFORMERS_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"❌ Sentiment semantic detection failed: {e}")
            # Emergency fallback to simple sentiment analysis
            return await self.emergency_sentiment_classification(message)

    async def detect_distress_semantically(self, message: str) -> Dict:
        """
        RENAMED: AI-FIRST semantic distress detection (was _analyze_emotional_distress_with_zero_shot)
        PRIMARY: Uses zero-shot AI models for semantic classification
        """
        try:
            logger.debug("🤖 Detecting emotional distress with ACTUAL zero-shot AI model...")
            
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
            
            # AI-FIRST: Perform ACTUAL zero-shot classification with configured labels
            score = await self.analyze_crisis_with_zero_shot_classification(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),
                'model': model_name,
                'method': 'ai_semantic_classification',  # AI-FIRST: Clear AI method indication
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager),
                'transformers_used': TRANSFORMERS_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"❌ Distress semantic detection failed: {e}")
            # Emergency fallback to pattern-based analysis
            return await self.emergency_distress_classification(message)
    
    # ========================================================================
    # CORE AI CLASSIFICATION IMPLEMENTATION - THE REAL AI FUNCTIONALITY
    # ========================================================================
    
    async def analyze_crisis_with_zero_shot_classification(self, text: str, labels: List[str], hypothesis_template: str, model_name: str) -> float:
        """
        RENAMED: Core AI classification method (was _perform_actual_zero_shot_classification)
        AI-FIRST: This is the primary semantic classification using transformers
        
        This performs the ACTUAL AI functionality using:
        - Real transformers models from Hugging Face
        - Semantic understanding instead of keyword matching
        - Zero-shot classification pipelines
        
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
                logger.warning(f"⚠️ Transformers library not available - using pattern enhancement fallback")
                return await self.enhance_ai_with_pattern_fallback(text, labels, hypothesis_template)
            
            # Load or get cached zero-shot pipeline
            classifier = await self._get_zero_shot_pipeline(model_name)
            
            if classifier is None:
                logger.warning(f"⚠️ Could not load zero-shot model {model_name} - using pattern enhancement fallback")
                return await self.enhance_ai_with_pattern_fallback(text, labels, hypothesis_template)
            
            # Perform actual zero-shot classification
            logger.debug(f"🤖 Running PRIMARY AI zero-shot classification with {model_name}")
            logger.debug(f"📝 Text: {text[:100]}...")
            logger.debug(f"🏷️ Labels: {len(labels)} labels")
            
            # Execute the classification
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: classifier(text, labels)
            )
            
            # Process results to extract crisis score
            crisis_score = self._process_zero_shot_result(result, labels)
            
            logger.info(f"✅ PRIMARY AI zero-shot classification complete: {crisis_score:.3f}")
            logger.debug(f"📊 Raw result: {result}")
            
            return crisis_score
            
        except Exception as e:
            logger.error(f"❌ PRIMARY AI zero-shot classification failed: {e}")
            logger.warning(f"⚠️ Using pattern enhancement fallback")
            return await self.enhance_ai_with_pattern_fallback(text, labels, hypothesis_template)

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
                logger.info(f"📥 Loading zero-shot model: {model_name}")
                
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
                logger.info(f"📂 Using cache directory: {cache_dir}")
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
                            logger.debug(f"📂 Using configured cache directory for {model_name}: {cache_dir}")
                            return cache_dir
                        
                        # No specific cache_dir, check model-level cache settings
                        break
                
                # Check for global cache directory in hardware settings
                hardware_settings = self.crisis_analyzer.model_ensemble_manager.get_hardware_settings()
                if 'cache_dir' in hardware_settings:
                    cache_dir = hardware_settings['cache_dir']
                    os.makedirs(cache_dir, exist_ok=True)
                    logger.debug(f"📂 Using global cache directory from hardware settings: {cache_dir}")
                    return cache_dir
            
            # Fallback to UnifiedConfigManager cache directory
            if self.crisis_analyzer.unified_config_manager:
                cache_dir = self.crisis_analyzer.unified_config_manager.get_config_section(
                    'model_ensemble',
                    'ensemble_config.cache_dir',
                    './models/cache/'
                )
                os.makedirs(cache_dir, exist_ok=True)
                logger.debug(f"📂 Using UnifiedConfigManager cache directory: {cache_dir}")
                return cache_dir
                
        except Exception as e:
            logger.warning(f"⚠️ Cache dir config from ModelEnsembleManager failed: {e}")
        
        # Final fallback cache directory
        fallback_dir = './cache/models/'
        try:
            os.makedirs(fallback_dir, exist_ok=True)
            logger.debug(f"📂 Using fallback cache directory: {fallback_dir}")
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
                    
                    logger.debug(f"📊 Label '{label[:50]}...': score={score:.3f}, weight={severity_weight:.3f}, contribution={weighted_contribution:.3f}")
                    
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
    # PATTERN ENHANCEMENT FALLBACK (Only used when transformers unavailable)
    # ========================================================================

    async def enhance_ai_with_pattern_fallback(self, text: str, labels: List[str], hypothesis_template: str) -> float:
        """
        RENAMED: Pattern enhancement for AI (was _enhanced_label_aware_scoring)
        ENHANCEMENT: Only used when transformers are not available, not as primary method
        
        Args:
            text: Text to analyze
            labels: List of crisis labels from ZeroShotManager
            hypothesis_template: Hypothesis template from configuration
            
        Returns:
            Label-aware pattern score (0.0 to 1.0)
        """
        try:
            if not labels:
                logger.warning("⚠️ No labels provided for pattern enhancement")
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
            
            logger.debug(f"📊 Pattern enhancement scoring: {score:.3f} (matches: {matches})")
            logger.debug(f"🏷️ Labels used: {len(labels)}, Keywords extracted: {len(crisis_keywords)}")
            
            return score
            
        except Exception as e:
            logger.error(f"❌ Pattern enhancement failed: {e}")
            return 0.0
    
    # ========================================================================
    # EMERGENCY CLASSIFICATION METHODS (Only used when AI fails completely)
    # ========================================================================
    
    async def emergency_depression_classification(self, message: str) -> Dict:
        """
        RENAMED: Emergency depression classification (was _fallback_depression_analysis)
        EMERGENCY: Only used when AI models fail completely
        """
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
                'model': 'emergency_pattern_fallback',
                'method': 'emergency_pattern_classification',
                'transformers_used': False
            }
        except Exception as e:
            logger.error(f"❌ Emergency depression classification failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'transformers_used': False}
    
    async def emergency_sentiment_classification(self, message: str) -> Dict:
        """
        RENAMED: Emergency sentiment classification (was _fallback_sentiment_analysis)
        EMERGENCY: Only used when AI models fail completely
        """
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
                'model': 'emergency_sentiment_fallback',
                'method': 'emergency_keyword_classification',
                'transformers_used': False
            }
        except Exception as e:
            logger.error(f"❌ Emergency sentiment classification failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'transformers_used': False}
    
    async def emergency_distress_classification(self, message: str) -> Dict:
        """
        RENAMED: Emergency distress classification (was _fallback_distress_analysis)
        EMERGENCY: Only used when AI models fail completely
        """
        try:
            distress_words = ['stressed', 'anxious', 'panic', 'overwhelmed', 'breakdown', 'crisis']
            text_lower = message.lower()
            matches = sum(1 for word in distress_words if word in text_lower)
            score = min(0.7, matches * 0.2)
            
            return {
                'score': score,
                'confidence': 0.5,
                'model': 'emergency_distress_fallback',
                'method': 'emergency_pattern_classification',
                'transformers_used': False
            }
        except Exception as e:
            logger.error(f"❌ Emergency distress classification failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'transformers_used': False}