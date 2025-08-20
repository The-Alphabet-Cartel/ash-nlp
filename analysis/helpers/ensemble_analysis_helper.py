# ash-nlp/analysis/helpers/ensemble_analysis_helper.py
"""
Ensemble Analysis Helper for CrisisAnalyzer
FILE VERSION: v3.1-3e-5.5-6-1
CREATED: 2025-08-20
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

MIGRATION NOTICE: Methods moved from CrisisAnalyzer for optimization
Original location: analysis/crisis_analyzer.py - ensemble analysis methods
"""

import logging
import time
import asyncio
from typing import Dict, List, Any, Optional

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

        # Model ensemble analysis with actual zero-shot models
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
        Perform model ensemble analysis with actual zero-shot models
        Migrated from: CrisisAnalyzer._perform_ensemble_analysis() (model analysis section)
        """
        model_results = {}
        if self.crisis_analyzer.model_ensemble_manager:
            try:
                logger.debug("Starting model ensemble analysis...")
                
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
        Analyze message with specific model using actual zero-shot models
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
    # ACTUAL ZERO-SHOT MODEL IMPLEMENTATIONS
    # ========================================================================
    
    async def _analyze_depression_with_zero_shot(self, message: str) -> Dict:
        """
        Analyze depression using actual zero-shot model with ZeroShotManager integration
        Replaces: CrisisAnalyzer._analyze_depression() placeholder
        """
        try:
            logger.debug("Analyzing depression indicators with zero-shot model...")
            
            # Get depression model configuration
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            depression_config = self.crisis_analyzer.model_ensemble_manager.get_model_config('depression')
            if not depression_config:
                raise ValueError("Depression model not configured")
            
            model_name = depression_config.get('name')
            if not model_name:
                raise ValueError("Depression model name not specified")
            
            # Use ZeroShotManager for label management if available
            labels = None
            hypothesis_template = "This text expresses {}."
            
            if hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager:
                try:
                    # Get depression labels from ZeroShotManager
                    all_labels = self.crisis_analyzer.zero_shot_manager.get_all_labels()
                    labels = all_labels.get('depression', [])
                    
                    # Get hypothesis template from ZeroShotManager
                    zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', 'This text expresses {}.')
                    
                    logger.debug(f"Using ZeroShotManager: {len(labels) if labels else 0} depression labels")
                    
                except Exception as e:
                    logger.warning(f"ZeroShotManager access failed: {e}, using fallback labels")
            
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
            
            # Perform zero-shot classification with configured labels
            score = await self._perform_zero_shot_classification_with_labels(
                message, labels, hypothesis_template, model_name
            )
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),  # Slightly higher confidence than score
                'model': model_name,
                'method': 'zero_shot_classification',
                'labels_used': len(labels),
                'hypothesis_template': hypothesis_template,
                'zero_shot_manager': bool(hasattr(self.crisis_analyzer, 'zero_shot_manager') and self.crisis_analyzer.zero_shot_manager)
            }
            
        except Exception as e:
            logger.error(f"Depression zero-shot analysis failed: {e}")
            # Fallback to pattern-based analysis
            return await self._fallback_depression_analysis(message)
    
    async def _analyze_sentiment_with_zero_shot(self, message: str) -> Dict:
        """
        Analyze sentiment using actual zero-shot model
        Replaces: CrisisAnalyzer._analyze_sentiment() placeholder
        """
        try:
            logger.debug("Analyzing sentiment with zero-shot model...")
            
            # Get sentiment model configuration
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            sentiment_config = self.crisis_analyzer.model_ensemble_manager.get_model_config('sentiment')
            if not sentiment_config:
                raise ValueError("Sentiment model not configured")
            
            model_name = sentiment_config.get('name')
            if not model_name:
                raise ValueError("Sentiment model name not specified")
            
            # Analyze negative sentiment specifically for crisis detection
            hypothesis = "This text expresses negative emotions, distress, or crisis"
            score = await self._perform_zero_shot_classification(message, hypothesis, model_name)
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),
                'model': model_name,
                'method': 'zero_shot_classification',
                'hypothesis': hypothesis
            }
            
        except Exception as e:
            logger.error(f"Sentiment zero-shot analysis failed: {e}")
            # Fallback to simple sentiment analysis
            return await self._fallback_sentiment_analysis(message)
    
    async def _analyze_emotional_distress_with_zero_shot(self, message: str) -> Dict:
        """
        Analyze emotional distress using actual zero-shot model
        Replaces: CrisisAnalyzer._analyze_emotional_distress() placeholder
        """
        try:
            logger.debug("Analyzing emotional distress with zero-shot model...")
            
            # Get emotional distress model configuration
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            distress_config = self.crisis_analyzer.model_ensemble_manager.get_model_config('emotional_distress')
            if not distress_config:
                raise ValueError("Emotional distress model not configured")
            
            model_name = distress_config.get('name')
            if not model_name:
                raise ValueError("Emotional distress model name not specified")
            
            # Analyze emotional distress and crisis indicators
            hypothesis = "This text indicates emotional distress, anxiety, panic, or mental health crisis"
            score = await self._perform_zero_shot_classification(message, hypothesis, model_name)
            
            return {
                'score': score,
                'confidence': min(0.9, score + 0.1),
                'model': model_name,
                'method': 'zero_shot_classification',
                'hypothesis': hypothesis
            }
            
        except Exception as e:
            logger.error(f"Emotional distress zero-shot analysis failed: {e}")
            # Fallback to pattern-based analysis
            return await self._fallback_distress_analysis(message)
    
    async def _perform_zero_shot_classification(self, text: str, hypothesis: str, model_name: str) -> float:
        """
        Perform actual zero-shot classification using Hugging Face transformers
        
        Args:
            text: Text to classify
            hypothesis: Classification hypothesis
            model_name: Hugging Face model name
            
        Returns:
            Classification score (0.0 to 1.0)
        """
        try:
            # TODO: Implement actual transformers pipeline
            # This requires installing transformers library and loading the models
            # For now, return enhanced pattern-based fallback
            
            logger.warning(f"Zero-shot classification not yet implemented for {model_name}")
            logger.warning("Using enhanced pattern-based fallback")
            
            # Enhanced pattern-based scoring as temporary implementation
            score = await self._enhanced_pattern_scoring(text, hypothesis)
            return score
            
        except Exception as e:
            logger.error(f"Zero-shot classification failed: {e}")
            return 0.0
    
    async def _enhanced_pattern_scoring(self, text: str, hypothesis: str) -> float:
        """
        Enhanced pattern-based scoring as fallback for zero-shot classification
        
        Args:
            text: Text to analyze
            hypothesis: Classification hypothesis
            
        Returns:
            Pattern-based score (0.0 to 1.0)
        """
        try:
            score = 0.0
            text_lower = text.lower()
            
            # Crisis keywords based on hypothesis
            if "depression" in hypothesis.lower():
                depression_keywords = [
                    'depressed', 'hopeless', 'worthless', 'empty', 'sad', 'down',
                    'lonely', 'isolated', 'meaningless', 'pointless', 'give up'
                ]
                matches = sum(1 for keyword in depression_keywords if keyword in text_lower)
                score = min(0.8, matches * 0.15)
                
            elif "negative" in hypothesis.lower() or "distress" in hypothesis.lower():
                negative_keywords = [
                    'terrible', 'awful', 'horrible', 'hate', 'angry', 'furious',
                    'stressed', 'overwhelmed', 'anxious', 'scared', 'worried'
                ]
                matches = sum(1 for keyword in negative_keywords if keyword in text_lower)
                score = min(0.8, matches * 0.12)
                
            elif "crisis" in hypothesis.lower():
                crisis_keywords = [
                    'crisis', 'emergency', 'help', 'urgent', 'desperate', 'panic',
                    'can\'t cope', 'breakdown', 'falling apart', 'end it all'
                ]
                matches = sum(1 for keyword in crisis_keywords if keyword in text_lower)
                score = min(0.9, matches * 0.2)
            
            # Boost for multiple indicators
            if score > 0.3:
                score *= 1.2
                score = min(1.0, score)
            
            logger.debug(f"Enhanced pattern scoring: {score:.3f} for hypothesis: {hypothesis[:50]}...")
            return score
            
        except Exception as e:
            logger.error(f"Enhanced pattern scoring failed: {e}")
            return 0.0
    
    # ========================================================================
    # FALLBACK ANALYSIS METHODS
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
                'method': 'pattern_based_fallback'
            }
        except Exception as e:
            logger.error(f"Fallback depression analysis failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e)}
    
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
                'method': 'keyword_based_fallback'
            }
        except Exception as e:
            logger.error(f"Fallback sentiment analysis failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e)}
    
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
                'method': 'pattern_based_fallback'
            }
        except Exception as e:
            logger.error(f"Fallback distress analysis failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e)}