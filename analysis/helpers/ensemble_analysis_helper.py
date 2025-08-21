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
Ensemble Analysis Helper for CrisisAnalyzer - PHASE 3 IMPLEMENTATION COMPLETE
---
FILE VERSION: v3.1-3e-5.5-7-3
CREATED: 2025-08-21
UPDATED: 2025-08-21
PHASE: 3e Sub-step 5.5-7 - PHASE 3: Manager Integration Implementation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PHASE 3 COMPLETE: Proper manager integration implemented
- EnsembleAnalysisHelper now calls ModelEnsembleManager.classify_with_zero_shot()
- Removed direct transformers pipeline creation (architectural fix)
- Proper integration with ZeroShotManager for label management
- Correct flow: EnsembleAnalysisHelper → ModelEnsembleManager → transformers
- All AI classification now goes through proper manager architecture
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
        
        logger.info("EnsembleAnalysisHelper v3.1e-5.5-7-3 Phase 3 initialized with manager integration")
        
    # ========================================================================
    # ENSEMBLE ANALYSIS METHODS
    # ========================================================================
    
    async def perform_ensemble_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        PHASE 3: AI-FIRST ensemble analysis with pattern enhancement
        ARCHITECTURE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
        
        Migrated from: CrisisAnalyzer._perform_ensemble_analysis()
        PHASE 3 CHANGE: Uses ModelEnsembleManager for all AI classification
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

        # Step 2: PRIMARY AI ensemble analysis using ModelEnsembleManager
        logger.info("PHASE 3: Starting PRIMARY AI semantic classification via ModelEnsembleManager...")
        model_results = await self.analyze_crisis_with_manager_ensemble(message, context_analysis)

        # Step 3: SECONDARY pattern enhancement of AI results
        logger.info("PHASE 3: Enhancing AI results with pattern analysis...")
        pattern_analysis = await self.enhance_ai_with_pattern_analysis(message, model_results)

        # Step 4: Combine AI results with pattern enhancements
        logger.info("PHASE 3: Combining AI results with pattern enhancements...")
        return self.crisis_analyzer._combine_analysis_results(
            message, user_id, channel_id, model_results, pattern_analysis, context_analysis, start_time
        )
    
    async def enhance_ai_with_pattern_analysis(self, message: str, ai_results: Dict) -> Dict:
        """
        PHASE 3: SECONDARY pattern enhancement of AI results (was _perform_pattern_analysis)
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
                logger.debug("PHASE 3: Analyzing patterns to enhance AI results...")
                
                # Extract AI confidence for pattern enhancement decisions
                ai_confidence = 0.0
                ai_score = 0.0
                if ai_results:
                    # Calculate average AI confidence and score
                    valid_results = [r for r in ai_results.values() if isinstance(r, dict) and 'score' in r]
                    if valid_results:
                        ai_score = sum(r.get('score', 0.0) for r in valid_results) / len(valid_results)
                        ai_confidence = sum(r.get('confidence', 0.0) for r in valid_results) / len(valid_results)
                
                logger.debug(f"PHASE 3: AI baseline - score: {ai_score:.3f}, confidence: {ai_confidence:.3f}")
                
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
                
                logger.info(f"PHASE 3: Pattern enhancement analysis complete - boost factor: {pattern_boost_factor:.3f}")
                
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
    
    async def analyze_crisis_with_manager_ensemble(self, message: str, context_analysis: Dict) -> Dict:
        """
        PHASE 3: PRIMARY AI ensemble analysis using ModelEnsembleManager
        RENAMED: (was analyze_crisis_with_ensemble_ai)
        ARCHITECTURE FIX: Uses ModelEnsembleManager instead of direct transformers
        """
        model_results = {}
        if self.crisis_analyzer.model_ensemble_manager:
            try:
                logger.debug("PHASE 3: Starting AI ensemble analysis via ModelEnsembleManager...")
                
                # PHASE 3 CRITICAL FIX: Use ModelEnsembleManager.classify_with_ensemble()
                # Instead of calling individual models directly
                ensemble_result = await self.crisis_analyzer.model_ensemble_manager.classify_with_ensemble(
                    message, 
                    self.crisis_analyzer.zero_shot_manager
                )
                
                if ensemble_result and 'individual_results' in ensemble_result:
                    model_results = ensemble_result['individual_results']
                    
                    # Add ensemble information to model_results
                    model_results['ensemble_meta'] = {
                        'ensemble_score': ensemble_result.get('ensemble_score', 0.0),
                        'ensemble_confidence': ensemble_result.get('ensemble_confidence', 0.0),
                        'ensemble_mode': ensemble_result.get('ensemble_mode', 'unknown'),
                        'models_used': ensemble_result.get('models_used', 0),
                        'zero_shot_manager_used': ensemble_result.get('zero_shot_manager_used', False),
                        'method': 'model_ensemble_manager_classification'
                    }
                    
                    logger.info(f"PHASE 3: ModelEnsembleManager classification complete - ensemble score: {ensemble_result.get('ensemble_score', 0.0):.3f}")
                    
                    # Update sentiment context with actual sentiment score if available
                    if 'sentiment' in model_results and context_analysis and 'sentiment_context' in context_analysis:
                        sentiment_score = model_results['sentiment'].get('score', 0.0)
                        updated_sentiment_context = self.crisis_analyzer.analyze_sentiment_context(message, sentiment_score)
                        context_analysis['sentiment_context'] = updated_sentiment_context
                else:
                    logger.warning("ModelEnsembleManager returned unexpected result format")
                    model_results = {'error': 'unexpected_ensemble_result_format'}
                        
            except Exception as e:
                logger.error(f"ModelEnsembleManager ensemble classification failed: {e}")
                model_results = {'error': str(e)}
        else:
            logger.error("ModelEnsembleManager not available")
            model_results = {'error': 'model_ensemble_manager_not_available'}
        
        return model_results
    
    async def classify_crisis_with_manager_model(self, message: str, model_name: str) -> Dict:
        """
        PHASE 3: Classify crisis using specific AI model via ModelEnsembleManager
        RENAMED: (was classify_crisis_with_ai_model)
        ARCHITECTURE FIX: Uses ModelEnsembleManager instead of direct classification
        """
        try:
            if not self.crisis_analyzer.model_ensemble_manager:
                raise ValueError("ModelEnsembleManager not available")
            
            # Get labels from ZeroShotManager if available
            labels = []
            hypothesis_template = "This text expresses {}."
            
            if self.crisis_analyzer.zero_shot_manager:
                try:
                    all_labels = self.crisis_analyzer.zero_shot_manager.get_all_labels()
                    zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', hypothesis_template)
                    
                    # Get labels for this model type
                    if isinstance(all_labels, dict) and model_name in all_labels:
                        labels = all_labels[model_name]
                    elif isinstance(all_labels, dict):
                        # Use general labels if model-specific not available
                        labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        labels = all_labels if isinstance(all_labels, list) else []
                        
                    logger.debug(f"PHASE 3: ZeroShotManager provided {len(labels)} labels for {model_name}")
                    
                except Exception as e:
                    logger.warning(f"ZeroShotManager access failed: {e}, using fallback labels")
            
            # Fallback labels if ZeroShotManager not available
            if not labels:
                labels = self._get_fallback_labels(model_name)
                logger.debug(f"PHASE 3: Using fallback labels for {model_name}")
            
            # PHASE 3 CRITICAL FIX: Use ModelEnsembleManager.classify_with_zero_shot()
            # Instead of direct transformers pipeline creation
            result = await self.crisis_analyzer.model_ensemble_manager.classify_with_zero_shot(
                message, labels, model_name, hypothesis_template
            )
            
            logger.debug(f"PHASE 3: ModelEnsembleManager classification for {model_name}: {result.get('score', 0.0):.3f}")
            return result
            
        except Exception as e:
            logger.error(f"ModelEnsembleManager model {model_name} analysis failed: {e}")
            return {'error': str(e), 'score': 0.0}
    
    def _get_fallback_labels(self, model_name: str) -> List[str]:
        """Get fallback labels for a model type"""
        fallback_labels = {
            'depression': [
                "person actively expressing suicidal thoughts, death wishes, or specific plans to end their life",
                "person expressing complete hopelessness, that nothing will ever get better, or life has no meaning",
                "person showing severe depression with major breakdown and inability to function daily",
                "person expressing emotional difficulty, low mood, or distress but still coping with life",
                "person feeling emotionally stable, content, or positive about life"
            ],
            'sentiment': [
                "extreme sadness, despair, anguish, or devastating emotional pain",
                "significant negativity, distress, anger, or emotional upset",
                "mild sadness, disappointment, or somewhat negative feelings",
                "neutral emotions, mixed feelings, or neither positive nor negative",
                "happiness, joy, contentment, or positive emotional expression"
            ],
            'emotional_distress': [
                "person in acute psychological distress unable to cope and requiring immediate crisis intervention",
                "person experiencing severe emotional overwhelm with significantly impaired functioning and coping",
                "person showing moderate distress with some difficulty managing emotions and daily responsibilities",
                "person handling normal life stress with adequate coping strategies and emotional regulation",
                "person demonstrating strong emotional resilience with healthy stress management and adaptation"
            ]
        }
        
        return fallback_labels.get(model_name, [
            "high crisis level",
            "medium crisis level", 
            "low crisis level"
        ])
    
    # ========================================================================
    # PRIMARY AI SEMANTIC DETECTION METHODS - PHASE 3 MANAGER INTEGRATION
    # ========================================================================
    
    async def detect_depression_semantically(self, message: str) -> Dict:
        """
        PHASE 3: AI-FIRST semantic depression detection via ModelEnsembleManager
        RENAMED: (was _analyze_depression_with_zero_shot)
        ARCHITECTURE FIX: Uses ModelEnsembleManager instead of direct transformers
        """
        try:
            logger.debug("PHASE 3: Detecting depression via ModelEnsembleManager...")
            
            # PHASE 3 CRITICAL FIX: Use ModelEnsembleManager instead of direct classification
            result = await self.classify_crisis_with_manager_model(message, 'depression')
            
            # Add method identification for Phase 3 tracking
            if isinstance(result, dict):
                result['method'] = 'manager_semantic_classification'
                result['architecture'] = 'phase_3_manager_integration'
                result['direct_transformers'] = False
                
            logger.debug(f"PHASE 3: Depression detection via manager complete: {result.get('score', 0.0):.3f}")
            return result
            
        except Exception as e:
            logger.error(f"PHASE 3: Depression semantic detection failed: {e}")
            return await self.emergency_depression_classification(message)

    async def detect_sentiment_semantically(self, message: str) -> Dict:
        """
        PHASE 3: AI-FIRST semantic sentiment detection via ModelEnsembleManager
        RENAMED: (was _analyze_sentiment_with_zero_shot)
        ARCHITECTURE FIX: Uses ModelEnsembleManager instead of direct transformers
        """
        try:
            logger.debug("PHASE 3: Detecting sentiment via ModelEnsembleManager...")
            
            # PHASE 3 CRITICAL FIX: Use ModelEnsembleManager instead of direct classification
            result = await self.classify_crisis_with_manager_model(message, 'sentiment')
            
            # Add method identification for Phase 3 tracking
            if isinstance(result, dict):
                result['method'] = 'manager_semantic_classification'
                result['architecture'] = 'phase_3_manager_integration'
                result['direct_transformers'] = False
                
            logger.debug(f"PHASE 3: Sentiment detection via manager complete: {result.get('score', 0.0):.3f}")
            return result
            
        except Exception as e:
            logger.error(f"PHASE 3: Sentiment semantic detection failed: {e}")
            return await self.emergency_sentiment_classification(message)

    async def detect_distress_semantically(self, message: str) -> Dict:
        """
        PHASE 3: AI-FIRST semantic distress detection via ModelEnsembleManager
        RENAMED: (was _analyze_emotional_distress_with_zero_shot)
        ARCHITECTURE FIX: Uses ModelEnsembleManager instead of direct transformers
        """
        try:
            logger.debug("PHASE 3: Detecting emotional distress via ModelEnsembleManager...")
            
            # PHASE 3 CRITICAL FIX: Use ModelEnsembleManager instead of direct classification
            result = await self.classify_crisis_with_manager_model(message, 'emotional_distress')
            
            # Add method identification for Phase 3 tracking
            if isinstance(result, dict):
                result['method'] = 'manager_semantic_classification'
                result['architecture'] = 'phase_3_manager_integration'
                result['direct_transformers'] = False
                
            logger.debug(f"PHASE 3: Distress detection via manager complete: {result.get('score', 0.0):.3f}")
            return result
            
        except Exception as e:
            logger.error(f"PHASE 3: Distress semantic detection failed: {e}")
            return await self.emergency_distress_classification(message)
    
    # ========================================================================
    # EMERGENCY CLASSIFICATION METHODS (Only used when AI fails completely)
    # ========================================================================
    
    async def emergency_depression_classification(self, message: str) -> Dict:
        """
        EMERGENCY: Emergency depression classification when ModelEnsembleManager fails
        """
        try:
            if self.crisis_analyzer.crisis_pattern_manager:
                patterns = self.crisis_analyzer.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
                score = min(0.7, len(patterns.get('matches', [])) * 0.15)
            else:
                score = 0.3  # Conservative fallback
            
            return {
                'score': score,
                'confidence': 0.5,
                'model': 'emergency_pattern_fallback',
                'method': 'emergency_pattern_classification',
                'architecture': 'emergency_fallback',
                'manager_used': False
            }
        except Exception as e:
            logger.error(f"Emergency depression classification failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'manager_used': False}
    
    async def emergency_sentiment_classification(self, message: str) -> Dict:
        """
        EMERGENCY: Emergency sentiment classification when ModelEnsembleManager fails
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
                'architecture': 'emergency_fallback',
                'manager_used': False
            }
        except Exception as e:
            logger.error(f"Emergency sentiment classification failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'manager_used': False}
    
    async def emergency_distress_classification(self, message: str) -> Dict:
        """
        EMERGENCY: Emergency distress classification when ModelEnsembleManager fails
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
                'architecture': 'emergency_fallback',
                'manager_used': False
            }
        except Exception as e:
            logger.error(f"Emergency distress classification failed: {e}")
            return {'score': 0.0, 'confidence': 0.0, 'error': str(e), 'manager_used': False}