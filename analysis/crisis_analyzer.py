# ash-nlp/analysis/crisis_analyzer.py
"""
Crisis Analyzer for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-10.8-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.7 - Community Pattern Consolidation + Manager Method Fixes
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Fixed manager method calls and environment variable handling
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
import re
import asyncio
from typing import Dict, List, Tuple, Any, Optional
from utils.context_helpers import extract_context_signals, analyze_sentiment_context, process_sentiment_with_flip
# PHASE 3D STEP 10.6: Scoring functions consolidated as instance methods (imports removed)
# PHASE 3D STEP 10.7: Community pattern imports removed - now use CrisisPatternManager directly
from managers.crisis_pattern_manager import CrisisPatternManager

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """
    PHASE 3D STEP 10.7 COMPLETE: Three Zero-Shot Model Ensemble crisis analysis with consolidated community patterns
    Phase 3a: Clean v3.1 architecture with JSON-based patterns
    Phase 3b: Analysis parameters from AnalysisParametersManager  
    Phase 3c: Mode-aware thresholds from ThresholdMappingManager
    Phase 3d Step 7: Feature flags and performance settings from dedicated managers
    Phase 3d Step 10.6: Consolidated scoring functions (no more utils/scoring_helpers.py)
    Phase 3d Step 10.7: Consolidated community patterns (no more utils/community_patterns.py)
    """
    
    def __init__(self, models_manager, crisis_pattern_manager=None, learning_manager=None,
                 analysis_parameters_manager=None, threshold_mapping_manager=None,
                 feature_config_manager=None, performance_config_manager=None,
                 context_pattern_manager=None):  # NEW: Step 10.8
        """
        Initialize Crisis Analyzer with comprehensive manager integration
        Updated for Step 10.8: Context Pattern Manager integration
        FIXED: Added all missing cache timing attributes
        
        Args:
            models_manager: ML model manager for ensemble analysis
            crisis_pattern_manager: CrisisPatternManager for pattern-based analysis
            learning_manager: Optional learning manager for feedback
            analysis_parameters_manager: AnalysisParametersManager for configurable parameters
            threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds
            feature_config_manager: FeatureConfigManager for feature flags
            performance_config_manager: PerformanceConfigManager for performance settings
            context_pattern_manager: ContextPatternManager for context analysis (NEW)
        """
        # Manager dependencies
        self.models_manager = models_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.learning_manager = learning_manager
        self.analysis_parameters_manager = analysis_parameters_manager
        self.threshold_mapping_manager = threshold_mapping_manager
        self.feature_config_manager = feature_config_manager
        self.performance_config_manager = performance_config_manager
        self.context_pattern_manager = context_pattern_manager  # NEW: Step 10.8
        
        # FIXED: Initialize all required cache attributes
        self._feature_cache = {}
        self._performance_cache = {}
        
        # FIXED: Add all missing timing attributes
        self._last_feature_check = 0  # FIXED: Missing attribute causing the error
        self._last_performance_check = 0  # FIXED: Missing attribute
        self._last_feature_refresh = 0  # Keep existing name for compatibility
        self._last_performance_refresh = 0  # Keep existing name for compatibility
        
        # FIXED: Add missing cache duration settings
        self._cache_refresh_interval = 30.0
        self._feature_cache_duration = 30.0  # FIXED: Missing attribute
        self._performance_cache_duration = 30.0  # FIXED: Missing attribute
        
        # Performance tracking
        self.initialization_time = time.time()
        
        logger.info("CrisisAnalyzer v3.1-3d-10.8 initialized with ContextPatternManager integration")

    def extract_context_signals(self, message: str) -> Dict[str, Any]:
        """
        Extract context signals from message using ContextPatternManager
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary containing context signals
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.extract_context_signals(message)
            else:
                logger.warning("⚠️ ContextPatternManager not available, using basic fallback")
                return self._basic_context_fallback(message)
        except Exception as e:
            logger.error(f"❌ Context signal extraction failed: {e}")
            return self._basic_context_fallback(message)

    def analyze_sentiment_context(self, message: str, base_sentiment: float = 0.0) -> Dict[str, Any]:
        """
        Analyze sentiment context using ContextPatternManager
        
        Args:
            message: Message text to analyze
            base_sentiment: Base sentiment score
            
        Returns:
            Dictionary with sentiment context analysis
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.analyze_sentiment_context(message, base_sentiment)
            else:
                logger.warning("⚠️ ContextPatternManager not available for sentiment context analysis")
                return {'base_sentiment': base_sentiment, 'context_available': False}
        except Exception as e:
            logger.error(f"❌ Sentiment context analysis failed: {e}")
            return {'base_sentiment': base_sentiment, 'error': str(e)}

    def perform_enhanced_context_analysis(self, message: str) -> Dict[str, Any]:
        """
        Perform enhanced context analysis with crisis pattern integration
        
        Args:
            message: Message text to analyze
            
        Returns:
            Enhanced context analysis results
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.perform_enhanced_context_analysis(
                    message, self.crisis_pattern_manager
                )
            else:
                logger.warning("⚠️ ContextPatternManager not available for enhanced analysis")
                return {'enhanced_analysis': False, 'context_available': False}
        except Exception as e:
            logger.error(f"❌ Enhanced context analysis failed: {e}")
            return {'enhanced_analysis': False, 'error': str(e)}

    def score_term_in_context(self, term: str, message: str, context_window: Optional[int] = None) -> Dict[str, Any]:
        """
        Score term relevance in message context using ContextPatternManager
        
        Args:
            term: Term to score
            message: Full message text
            context_window: Context window size (optional)
            
        Returns:
            Term scoring results
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.score_term_in_context(term, message, context_window)
            else:
                logger.warning("⚠️ ContextPatternManager not available for term scoring")
                return {'term': term, 'found': False, 'context_available': False}
        except Exception as e:
            logger.error(f"❌ Term context scoring failed: {e}")
            return {'term': term, 'found': False, 'error': str(e)}

    def _basic_context_fallback(self, message: str) -> Dict[str, Any]:
        """Basic context fallback when ContextPatternManager is not available"""
        return {
            'message_length': len(message),
            'word_count': len(message.split()),
            'has_question_mark': '?' in message,
            'has_exclamation': '!' in message,
            'fallback_mode': True,
            'context_manager_available': False
        }

    def _refresh_feature_cache(self):
        """Refresh feature flag cache if needed (Phase 3d Step 7)"""
        current_time = time.time()
        if current_time - self._last_feature_check > self._feature_cache_duration:
            if self.feature_config_manager:
                try:
                    # Use the correct method names for FeatureConfigManager
                    self._feature_cache = {
                        'ensemble_enabled': self.feature_config_manager.is_ensemble_analysis_enabled(),
                        'pattern_analysis': self.feature_config_manager.is_pattern_analysis_enabled(),
                        'sentiment_analysis': self.feature_config_manager.is_semantic_analysis_enabled(),
                        'enhanced_learning': self.feature_config_manager.is_threshold_learning_enabled(),
                        'temporal_boost': self.feature_config_manager.is_temporal_patterns_enabled(),
                        'community_patterns': self.feature_config_manager.is_community_vocab_enabled(),
                        'context_analysis': self.feature_config_manager.is_context_analysis_enabled()
                    }
                    self._last_feature_check = current_time
                    logger.debug("Feature cache refreshed")
                except Exception as e:
                    logger.error(f"Error refreshing feature cache: {e}")
                    # Use safe defaults
                    self._feature_cache = {
                        'ensemble_enabled': True,
                        'pattern_analysis': True,
                        'sentiment_analysis': True,
                        'enhanced_learning': False,
                        'temporal_boost': True,
                        'community_patterns': True,
                        'context_analysis': True
                    }
            else:
                # Default all features enabled if no feature manager
                self._feature_cache = {
                    'ensemble_enabled': True,
                    'pattern_analysis': True,
                    'sentiment_analysis': True,
                    'enhanced_learning': False,
                    'temporal_boost': True,
                    'community_patterns': True,
                    'context_analysis': True
                }

    def _refresh_performance_cache(self):
        """Refresh performance settings cache if needed (Phase 3d Step 7)"""
        current_time = time.time()
        if current_time - self._last_performance_check > self._feature_cache_duration:
            if self.performance_config_manager:
                try:
                    # Use the correct method names for PerformanceConfigManager
                    self._performance_cache = {
                        'analysis_timeout': self.performance_config_manager.get_analysis_timeout(),
                        'model_timeout': self.performance_config_manager.get_analysis_timeout(),  # Use same for model timeout
                        'batch_size': self.performance_config_manager.get_analysis_batch_size(),
                        'cache_enabled': True,  # Default to enabled
                        'parallel_analysis': False  # Default to disabled (handled by FeatureConfigManager)
                    }
                    self._last_performance_check = current_time
                    logger.debug("Performance cache refreshed")
                except Exception as e:
                    logger.error(f"Error refreshing performance cache: {e}")
                    # Use safe defaults
                    self._performance_cache = {
                        'analysis_timeout': 30.0,
                        'model_timeout': 10.0,
                        'batch_size': 1,
                        'cache_enabled': True,
                        'parallel_analysis': False
                    }
            else:
                # Default performance settings if no performance manager
                self._performance_cache = {
                    'analysis_timeout': 30.0,
                    'model_timeout': 10.0,
                    'batch_size': 1,
                    'cache_enabled': True,
                    'parallel_analysis': False
                }

    def _determine_staff_review_requirement(self, final_score: float, crisis_level: str) -> bool:
        """
        Determine if staff review is required based on score and crisis level
        
        Args:
            final_score: Final crisis score (0.0 to 1.0)
            crisis_level: Determined crisis level ('none', 'low', 'medium', 'high', 'critical')
            
        Returns:
            True if staff review is required, False otherwise
        """
        try:
            # Use ThresholdMappingManager if available for staff review determination
            if self.threshold_mapping_manager:
                try:
                    # Try different possible method names for staff review
                    if hasattr(self.threshold_mapping_manager, 'requires_staff_review'):
                        return self.threshold_mapping_manager.requires_staff_review(final_score, crisis_level)
                    elif hasattr(self.threshold_mapping_manager, 'determine_staff_review'):
                        return self.threshold_mapping_manager.determine_staff_review(final_score, crisis_level)
                    elif hasattr(self.threshold_mapping_manager, 'get_staff_review_requirement'):
                        return self.threshold_mapping_manager.get_staff_review_requirement(final_score, crisis_level)
                    else:
                        logger.debug("ThresholdMappingManager has no known staff review method - using fallback")
                except Exception as e:
                    logger.warning(f"⚠️ Staff review determination via manager failed: {e}")
            
            # Fallback logic for staff review determination
            if crisis_level in ['critical', 'high']:
                return True  # Always require review for high/critical
            elif crisis_level == 'medium':
                return final_score >= 0.45  # Medium with high confidence
            elif crisis_level == 'low':
                return final_score >= 0.75  # Low but very high confidence
            else:
                return False  # No review needed for 'none' level
                
        except Exception as e:
            logger.error(f"❌ Staff review determination failed: {e}")
            # Conservative fallback - require review for any significant score
            return final_score >= 0.3

    def _create_error_response(self, message: str, user_id: str, channel_id: str, error: str, start_time: float) -> Dict:
        """
        Create standardized error response for crisis analysis
        
        Args:
            message: Original message
            user_id: User identifier
            channel_id: Channel identifier  
            error: Error description
            start_time: Analysis start time
            
        Returns:
            Standardized error response dictionary
        """
        return {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'analysis_results': {
                'crisis_score': 0.0,
                'crisis_level': 'error',
                'error': error,
                'model_results': {},
                'pattern_analysis': {},
                'context_analysis': {},
                'analysis_metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'analysis_version': 'v3.1-3d-10.8',
                    'error_occurred': True,
                    'features_used': {
                        'ensemble_analysis': False,
                        'pattern_analysis': False,
                        'context_analysis': False,
                        'error_fallback': True
                    }
                }
            },
            'requires_staff_review': True,  # Always require review on errors
            'processing_time': time.time() - start_time,
            'status': 'error'
        }

    def _create_timeout_response(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Create standardized timeout response for crisis analysis
        
        Args:
            message: Original message
            user_id: User identifier
            channel_id: Channel identifier
            start_time: Analysis start time
            
        Returns:
            Standardized timeout response dictionary
        """
        return {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'analysis_results': {
                'crisis_score': 0.0,
                'crisis_level': 'timeout',
                'timeout_occurred': True,
                'model_results': {},
                'pattern_analysis': {},
                'context_analysis': {},
                'analysis_metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'analysis_version': 'v3.1-3d-10.8',
                    'timeout_occurred': True,
                    'features_used': {
                        'ensemble_analysis': False,
                        'pattern_analysis': False,
                        'context_analysis': False,
                        'timeout_fallback': True
                    }
                }
            },
            'requires_staff_review': True,  # Always require review on timeouts
            'processing_time': time.time() - start_time,
            'status': 'timeout'
        }

    async def analyze_crisis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Perform comprehensive crisis analysis using ensemble of models and patterns
        Updated for Step 10.7: Community patterns now accessed via CrisisPatternManager
        
        Args:
            message: User message to analyze
            user_id: User identifier  
            channel_id: Channel identifier
            
        Returns:
            Dictionary containing crisis analysis results
        """
        start_time = time.time()
        logger.info(f"🔍 Starting crisis analysis for user {user_id} in channel {channel_id}")
        
        # Refresh caches
        self._refresh_feature_cache()
        self._refresh_performance_cache()
        
        try:
            # Check if ensemble is enabled by feature flag
            ensemble_enabled = self._feature_cache.get('ensemble_enabled', True)
            
            if ensemble_enabled:
                logger.debug("✅ Ensemble analysis enabled - using full model ensemble")
                return await self._ensemble_crisis_analysis(message, user_id, channel_id, start_time)
            else:
                logger.debug("🔥 Ensemble analysis disabled - using basic pattern analysis")
                return await self._basic_crisis_analysis(message, user_id, channel_id, start_time)
                
        except Exception as e:
            logger.error(f"❌ Crisis analysis failed: {e}")
            return self._create_error_response(message, user_id, channel_id, str(e), start_time)

    async def _ensemble_crisis_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Full ensemble analysis with three models and pattern analysis
        Updated for Step 10.7: Community patterns via CrisisPatternManager
        """
        try:
            logger.debug("🧠 Starting ensemble crisis analysis...")
            
            # Get performance settings
            analysis_timeout = self._performance_cache.get('analysis_timeout', 30.0)
            
            # Use asyncio.wait_for to enforce timeout
            analysis_result = await asyncio.wait_for(
                self._perform_ensemble_analysis(message, user_id, channel_id, start_time),
                timeout=analysis_timeout
            )
            
            return analysis_result
            
        except asyncio.TimeoutError:
            logger.error(f"⏰ Ensemble analysis timed out after {analysis_timeout}s")
            return self._create_timeout_response(message, user_id, channel_id, start_time)
        except Exception as e:
            logger.error(f"❌ Ensemble analysis error: {e}")
            return self._create_error_response(message, user_id, channel_id, str(e), start_time)

    async def _perform_ensemble_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Perform the actual ensemble analysis with integrated context analysis
        Updated for Step 10.8: ContextPatternManager integration
        """
        
        # Step 10.8: Enhanced context analysis using ContextPatternManager
        context_analysis = None
        if self._feature_cache.get('context_analysis', True) and self.context_pattern_manager:
            try:
                logger.debug("🔍 Starting enhanced context analysis via ContextPatternManager...")
                
                # Get basic context signals
                context_signals = self.extract_context_signals(message)
                
                # Perform enhanced context analysis with crisis pattern integration
                enhanced_context = self.perform_enhanced_context_analysis(message)
                
                # Analyze sentiment context if we have model results
                sentiment_context = self.analyze_sentiment_context(message, 0.0)  # Will be updated with actual sentiment
                
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
                logger.error(f"❌ Context analysis failed: {e}")
                context_analysis = {
                    'context_manager_status': 'error',
                    'error': str(e),
                    'fallback_used': True
                }
        else:
            context_analysis = {
                'context_manager_status': 'not_available',
                'feature_enabled': self._feature_cache.get('context_analysis', False)
            }
            logger.debug("Context analysis disabled or ContextPatternManager not available")

        # Continue with existing pattern analysis (Step 10.7)
        pattern_analysis = None
        if self._feature_cache.get('pattern_analysis', True) and self.crisis_pattern_manager:
            try:
                logger.debug("🔍 Starting pattern analysis via CrisisPatternManager...")
                
                # Community patterns analysis via CrisisPatternManager
                community_patterns = []
                if self._feature_cache.get('community_patterns', True):
                    community_patterns = self.crisis_pattern_manager.extract_community_patterns(message)
                    logger.debug(f"Found {len(community_patterns)} community patterns")
                
                # Extract crisis context phrases
                context_phrases = []
                if self._feature_cache.get('context_analysis', True):
                    context_phrases = self.crisis_pattern_manager.extract_crisis_context_phrases(message)
                    logger.debug(f"Found {len(context_phrases)} context phrases")
                
                # Analyze temporal indicators
                temporal_analysis = {}
                if self._feature_cache.get('temporal_boost', True):
                    temporal_analysis = self.crisis_pattern_manager.analyze_temporal_indicators(message)
                    logger.debug(f"Temporal analysis: {temporal_analysis.get('urgency_score', 0)}")
                
                # Enhanced crisis pattern check
                enhanced_patterns = {}
                enhanced_patterns = self.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
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
                logger.error(f"❌ Pattern analysis failed: {e}")
                pattern_analysis = {'error': str(e), 'total_patterns': 0}

        # Model ensemble analysis (existing code continues...)
        model_results = {}
        if self.models_manager:
            try:
                logger.debug("🤖 Starting model ensemble analysis...")
                
                # Get models based on feature flags
                active_models = []
                if self._feature_cache.get('sentiment_analysis', True):
                    active_models.extend(['sentiment', 'depression'])
                
                for model_name in active_models:
                    try:
                        model_timeout = self._performance_cache.get('model_timeout', 10.0)
                        model_result = await asyncio.wait_for(
                            self._analyze_with_model(message, model_name),
                            timeout=model_timeout
                        )
                        model_results[model_name] = model_result
                        
                        # Step 10.8: Update sentiment context with actual sentiment score
                        if model_name == 'sentiment' and context_analysis and 'sentiment_context' in context_analysis:
                            sentiment_score = model_result.get('score', 0.0)
                            updated_sentiment_context = self.analyze_sentiment_context(message, sentiment_score)
                            context_analysis['sentiment_context'] = updated_sentiment_context
                            
                    except asyncio.TimeoutError:
                        logger.warning(f"⏰ Model {model_name} timed out")
                        model_results[model_name] = {'error': 'timeout', 'score': 0.0}
                    except Exception as e:
                        logger.warning(f"❌ Model {model_name} failed: {e}")
                        model_results[model_name] = {'error': str(e), 'score': 0.0}
                        
            except Exception as e:
                logger.error(f"❌ Model ensemble failed: {e}")
                model_results = {'error': str(e)}

        # Combine results with enhanced context integration
        return self._combine_analysis_results(
            message, user_id, channel_id, model_results, pattern_analysis, context_analysis, start_time
        )

    async def _analyze_with_model(self, message: str, model_name: str) -> Dict:
        """Analyze message with specific model"""
        try:
            if model_name == 'sentiment':
                return await self._analyze_sentiment(message)
            elif model_name == 'depression':
                return await self._analyze_depression(message)
            else:
                return {'error': f'Unknown model: {model_name}', 'score': 0.0}
        except Exception as e:
            logger.error(f"❌ Model {model_name} analysis failed: {e}")
            return {'error': str(e), 'score': 0.0}

    async def _analyze_sentiment(self, message: str) -> Dict:
        """Analyze sentiment using sentiment model"""
        try:
            # Placeholder for actual sentiment analysis
            # This would use self.models_manager to get the sentiment model
            logger.debug("🎭 Analyzing sentiment...")
            return {
                'score': 0.3,  # Placeholder
                'confidence': 0.7,
                'model': 'sentiment_analyzer',
                'method': 'ensemble_sentiment'
            }
        except Exception as e:
            logger.error(f"❌ Sentiment analysis failed: {e}")
            return {'error': str(e), 'score': 0.0}

    async def _analyze_depression(self, message: str) -> Dict:
        """Analyze depression indicators using depression model"""
        try:
            # Placeholder for actual depression analysis
            # This would use self.models_manager to get the depression model
            logger.debug("😔 Analyzing depression indicators...")
            return {
                'score': 0.4,  # Placeholder
                'confidence': 0.6,
                'model': 'depression_analyzer',
                'method': 'ensemble_depression'
            }
        except Exception as e:
            logger.error(f"❌ Depression analysis failed: {e}")
            return {'error': str(e), 'score': 0.0}

    def _combine_analysis_results(self, message: str, user_id: str, channel_id: str, 
                                model_results: Dict, pattern_analysis: Dict, 
                                context_analysis: Dict, start_time: float) -> Dict:
        """
        Combine all analysis results with context integration
        Updated for Step 10.8: Context analysis integration
        """
        
        # Calculate base scores from models
        base_score = 0.0
        model_scores = {}
        
        for model_name, result in model_results.items():
            if isinstance(result, dict) and 'score' in result:
                score = float(result['score'])
                model_scores[model_name] = score
                base_score += score * 0.33  # Equal weighting for now
        
        # Apply context adjustments if available
        if context_analysis and context_analysis.get('context_manager_status') == 'available':
            context_signals = context_analysis.get('context_signals', {})
            
            # Apply context boost based on indicators
            context_boost = 0.0
            context_boost += context_signals.get('social_isolation_indicators', 0) * 0.05
            context_boost += context_signals.get('hopelessness_indicators', 0) * 0.08
            context_boost += len(context_signals.get('temporal_indicators', [])) * 0.03
            
            # Apply sentiment context adjustments
            sentiment_context = context_analysis.get('sentiment_context', {})
            if sentiment_context.get('flip_applied', False):
                context_boost += 0.10  # Boost for negation-flipped sentiment
            
            base_score += context_boost
            
            logger.debug(f"Applied context boost: +{context_boost:.3f}")
        
        # Apply pattern adjustments (existing logic)
        if pattern_analysis and pattern_analysis.get('total_patterns', 0) > 0:
            pattern_boost = min(0.25, pattern_analysis['total_patterns'] * 0.05)
            base_score += pattern_boost
            logger.debug(f"Applied pattern boost: +{pattern_boost:.3f}")
        
        # Normalize score
        final_score = max(0.0, min(1.0, base_score))
        
        # Determine crisis level
        crisis_level = self._determine_crisis_level(final_score)
        
        # Build comprehensive response
        return {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'analysis_results': {
                'crisis_score': final_score,
                'crisis_level': crisis_level,
                'model_results': model_results,
                'pattern_analysis': pattern_analysis or {},
                'context_analysis': context_analysis or {},  # NEW: Step 10.8
                'model_scores': model_scores,
                'analysis_metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'analysis_version': 'v3.1-3d-10.8',
                    'features_used': {
                        'ensemble_analysis': bool(model_results),
                        'pattern_analysis': bool(pattern_analysis),
                        'context_analysis': bool(context_analysis),  # NEW
                        'context_manager_available': context_analysis.get('context_manager_status') == 'available'
                    }
                }
            },
            'requires_staff_review': self._determine_staff_review_requirement(final_score, crisis_level),
            'processing_time': time.time() - start_time
        }

    def _extract_categories(self, pattern_analysis: Dict) -> List[str]:
        """Extract detected categories from pattern analysis"""
        categories = []
        
        if pattern_analysis:
            # Community patterns
            community_patterns = pattern_analysis.get('community_patterns', [])
            for pattern in community_patterns:
                if isinstance(pattern, dict) and 'pattern_type' in pattern:
                    categories.append(f"community_{pattern['pattern_type']}")
            
            # Enhanced patterns
            enhanced_patterns = pattern_analysis.get('enhanced_patterns', {})
            for match in enhanced_patterns.get('matches', []):
                if isinstance(match, dict) and 'pattern_group' in match:
                    categories.append(f"enhanced_{match['pattern_group']}")
        
        return list(set(categories))

    def _determine_crisis_level(self, score: float) -> str:
        """
        Determine crisis level from score using ThresholdMappingManager
        Updated for Phase 3c integration with fallback for missing methods
        """
        try:
            if self.threshold_mapping_manager:
                # Try different possible method names on ThresholdMappingManager
                if hasattr(self.threshold_mapping_manager, 'determine_crisis_level'):
                    return self.threshold_mapping_manager.determine_crisis_level(score)
                elif hasattr(self.threshold_mapping_manager, 'get_crisis_level'):
                    return self.threshold_mapping_manager.get_crisis_level(score)
                elif hasattr(self.threshold_mapping_manager, 'map_score_to_level'):
                    return self.threshold_mapping_manager.map_score_to_level(score)
                else:
                    logger.warning("ThresholdMappingManager has no known crisis level method - using fallback")
            
            # Fallback thresholds
            if score >= 0.7:
                return 'critical'
            elif score >= 0.5:
                return 'high'
            elif score >= 0.3:
                return 'medium'
            elif score >= 0.1:
                return 'low'
            else:
                return 'none'

        except Exception as e:
            logger.error(f"❌ Crisis level determination failed: {e}")
            # Conservative fallback
            if score >= 0.5:
                return 'high'
            elif score >= 0.3:
                return 'medium'
            else:
                return 'low'

    async def _basic_crisis_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Basic crisis analysis when ensemble is disabled by feature flag
        Updated for Step 10.7: Direct CrisisPatternManager usage
        """
        logger.info("🔥 Running basic crisis analysis - ensemble disabled by feature flag")
        
        # Check if pattern analysis is enabled
        pattern_analysis_enabled = self._feature_cache.get('pattern_analysis', False)
        
        if pattern_analysis_enabled and self.crisis_pattern_manager:
            logger.debug("✅ Pattern analysis enabled for basic analysis")
            
            # STEP 10.7: Use CrisisPatternManager methods directly
            try:
                enhanced_patterns = self.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
                
                # Simple crisis level determination based on patterns
                if enhanced_patterns.get('matches'):
                    highest_urgency = enhanced_patterns.get('highest_urgency', 'none')
                    
                    if highest_urgency == 'critical':
                        confidence = 0.8
                        crisis_level = 'high'
                    elif highest_urgency == 'high':
                        confidence = 0.6
                        crisis_level = 'medium'
                    else:
                        confidence = 0.4
                        crisis_level = 'low'
                        
                    logger.debug(f"✅ Pattern-based analysis result: {crisis_level} (conf: {confidence})")
                else:
                    crisis_level = 'none'
                    confidence = 0.0
                    logger.debug("📊 No patterns triggered in basic analysis")
                    
            except Exception as e:
                logger.error(f"❌ Basic pattern analysis failed: {e}")
                crisis_level = 'none'
                confidence = 0.0
                enhanced_patterns = {'error': str(e)}
        else:
            logger.debug("🚫 Pattern analysis disabled - returning minimal analysis")
            enhanced_patterns = {'matches': [], 'error': 'Pattern analysis disabled by feature flag'}
            crisis_level = 'none'
            confidence = 0.0
        
        return {
            'needs_response': crisis_level != 'none',
            'crisis_level': crisis_level,
            'confidence_score': confidence,
            'detected_categories': [],
            'pattern_analysis': {'enhanced_patterns': enhanced_patterns},
            'method': 'basic_pattern_only_v3d10.7' if pattern_analysis_enabled else 'basic_disabled_v3d10.7',
            'processing_time_ms': (time.time() - start_time) * 1000,
            'metadata': {
                'user_id': user_id,
                'channel_id': channel_id,
                'analysis_timestamp': time.time(),
                'ensemble_disabled': True,
                'step_10_7_consolidation': True
            }
        }

    # =============================================================================
    # NEW CONTEXT ANALYSIS METHODS - Using ContextPatternManager
    # =============================================================================

    def extract_context_signals(self, message: str) -> Dict[str, Any]:
        """
        Extract context signals from message using ContextPatternManager
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary containing context signals
            
        Note:
            This method now uses the centralized ContextPatternManager instead of utils/context_helpers.py
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.extract_context_signals(message)
            else:
                logger.warning("⚠️ ContextPatternManager not available, using basic fallback")
                return self._basic_context_fallback(message)
        except Exception as e:
            logger.error(f"❌ Context signal extraction failed: {e}")
            return self._basic_context_fallback(message)

    def analyze_sentiment_context(self, message: str, base_sentiment: float = 0.0) -> Dict[str, Any]:
        """
        Analyze sentiment context using ContextPatternManager
        
        Args:
            message: Message text to analyze
            base_sentiment: Base sentiment score
            
        Returns:
            Dictionary with sentiment context analysis
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.analyze_sentiment_context(message, base_sentiment)
            else:
                logger.warning("⚠️ ContextPatternManager not available for sentiment context analysis")
                return {'base_sentiment': base_sentiment, 'context_available': False}
        except Exception as e:
            logger.error(f"❌ Sentiment context analysis failed: {e}")
            return {'base_sentiment': base_sentiment, 'error': str(e)}

    def perform_enhanced_context_analysis(self, message: str) -> Dict[str, Any]:
        """
        Perform enhanced context analysis with crisis pattern integration
        
        Args:
            message: Message text to analyze
            
        Returns:
            Enhanced context analysis results
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.perform_enhanced_context_analysis(
                    message, self.crisis_pattern_manager
                )
            else:
                logger.warning("⚠️ ContextPatternManager not available for enhanced analysis")
                return {'enhanced_analysis': False, 'context_available': False}
        except Exception as e:
            logger.error(f"❌ Enhanced context analysis failed: {e}")
            return {'enhanced_analysis': False, 'error': str(e)}

    def score_term_in_context(self, term: str, message: str, context_window: Optional[int] = None) -> Dict[str, Any]:
        """
        Score term relevance in message context using ContextPatternManager
        
        Args:
            term: Term to score
            message: Full message text
            context_window: Context window size (optional)
            
        Returns:
            Term scoring results
        """
        try:
            if self.context_pattern_manager:
                return self.context_pattern_manager.score_term_in_context(term, message, context_window)
            else:
                logger.warning("⚠️ ContextPatternManager not available for term scoring")
                return {'term': term, 'found': False, 'context_available': False}
        except Exception as e:
            logger.error(f"❌ Term context scoring failed: {e}")
            return {'term': term, 'found': False, 'error': str(e)}

    def _basic_context_fallback(self, message: str) -> Dict[str, Any]:
        """Basic context fallback when ContextPatternManager is not available"""
        return {
            'message_length': len(message),
            'word_count': len(message.split()),
            'has_question_mark': '?' in message,
            'has_exclamation': '!' in message,
            'fallback_mode': True,
            'context_manager_available': False
        }

    def _create_error_response(self, message: str, user_id: str, channel_id: str, error: str, start_time: float) -> Dict:
        """Create error response for failed analysis"""
        return {
            'needs_response': True,  # Conservative - assume crisis on error
            'crisis_level': 'high',  # Conservative - assume high crisis on error
            'confidence_score': 0.0,
            'detected_categories': [],
            'error': error,
            'method': 'error_fallback_v3d10.7',
            'processing_time_ms': (time.time() - start_time) * 1000,
            'metadata': {
                'user_id': user_id,
                'channel_id': channel_id,
                'analysis_timestamp': time.time(),
                'error_occurred': True
            }
        }

    def _create_timeout_response(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """Create timeout response for analysis that takes too long"""
        return {
            'needs_response': True,  # Conservative - assume crisis on timeout
            'crisis_level': 'medium',  # Conservative - assume medium crisis on timeout
            'confidence_score': 0.5,
            'detected_categories': [],
            'error': 'Analysis timed out',
            'method': 'timeout_fallback_v3d10.7',
            'processing_time_ms': (time.time() - start_time) * 1000,
            'metadata': {
                'user_id': user_id,
                'channel_id': channel_id,
                'analysis_timestamp': time.time(),
                'timeout_occurred': True
            }
        }

    # ========================================================================
    # BACKWARD COMPATIBILITY METHOD - analyze_message
    # ========================================================================

    async def analyze_message(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Backward compatibility method for analyze_message (calls analyze_crisis)
        
        Args:
            message: User message to analyze
            user_id: User identifier  
            channel_id: Channel identifier
            
        Returns:
            Dictionary containing crisis analysis results
        """
        logger.debug(f"analyze_message called - delegating to analyze_crisis for backward compatibility")
        return await self.analyze_crisis(message, user_id, channel_id)

    # ========================================================================
    # STEP 10.6: CONSOLIDATED SCORING FUNCTIONS (Instance methods from utils/scoring_helpers.py)
    # ========================================================================
    
    def extract_depression_score(self, message: str, sentiment_model=None, 
                                analysis_parameters_manager=None, context=None,
                                crisis_pattern_manager: Optional[CrisisPatternManager] = None) -> Tuple[float, List[str]]:
        """
        Extract depression indicators from message text (STEP 10.6: Consolidated from utils)
        
        Args:
            message: Message text to analyze
            sentiment_model: Optional sentiment analysis model  
            analysis_parameters_manager: Optional AnalysisParametersManager (uses self.analysis_parameters_manager if None)
            context: Optional context information
            crisis_pattern_manager: Optional CrisisPatternManager (uses self.crisis_pattern_manager if None)
            
        Returns:
            Tuple of (depression_score, detected_categories)
        """
        
        # Use injected managers if not provided
        param_manager = analysis_parameters_manager or self.analysis_parameters_manager
        pattern_manager = crisis_pattern_manager or self.crisis_pattern_manager
        
        logger.debug(f"Depression analysis for: '{message[:50]}...'")
        
        try:
            depression_score = 0.0
            detected_categories = []
            
            # Sentiment analysis
            if sentiment_model:
                try:
                    sentiment_result = sentiment_model(message)
                    sentiment_scores = self._process_sentiment_result(sentiment_result)
                    
                    if sentiment_scores.get('negative', 0) > 0.6:
                        depression_score += 0.3
                        detected_categories.append('negative_sentiment')
                        logger.debug(f"Negative sentiment boost: +0.3")
                except Exception as e:
                    logger.warning(f"Sentiment analysis failed: {e}")
            
            # Pattern-based detection using CrisisPatternManager if available
            if pattern_manager:
                try:
                    pattern_result = pattern_manager.analyze_enhanced_patterns(message)
                    
                    if pattern_result.get('patterns_found'):
                        pattern_score = 0.0
                        for pattern in pattern_result['patterns_found']:
                            pattern_weight = pattern.get('weight', 0.5)
                            crisis_level = pattern.get('crisis_level', 'low')
                            
                            if crisis_level == 'critical':
                                pattern_score += pattern_weight * 0.8
                            elif crisis_level == 'high':
                                pattern_score += pattern_weight * 0.6
                            elif crisis_level == 'medium':
                                pattern_score += pattern_weight * 0.4
                            else:
                                pattern_score += pattern_weight * 0.2
                                
                            detected_categories.append(f"pattern_{pattern.get('pattern_group', 'unknown')}")
                        
                        depression_score += min(pattern_score, 0.5)  # Cap pattern contribution
                        logger.debug(f"Pattern analysis boost: +{min(pattern_score, 0.5):.3f}")
                        
                except Exception as e:
                    logger.warning(f"Pattern analysis failed: {e}")
            
            # Context-based adjustments
            if context:
                # Social isolation indicators
                isolation_count = context.get('social_isolation_indicators', 0)
                if isolation_count > 2:
                    depression_score += 0.1
                    detected_categories.append('social_isolation')
                
                # Hopelessness indicators
                hopelessness_count = context.get('hopelessness_indicators', 0)
                if hopelessness_count > 1:
                    depression_score += 0.15
                    detected_categories.append('hopelessness')
            
            # Configurable parameters from AnalysisParametersManager
            if param_manager:
                try:
                    boost_factor = param_manager.get_depression_boost_factor()
                    max_score_limit = param_manager.get_max_depression_score()
                    
                    depression_score *= boost_factor
                    depression_score = min(depression_score, max_score_limit)
                    
                    logger.debug(f"Parameter adjustments: boost={boost_factor}, max={max_score_limit}")
                except Exception as e:
                    logger.warning(f"Parameter adjustment failed: {e}")
            
            # Ensure score bounds
            depression_score = max(0.0, min(1.0, depression_score))
            
            logger.debug(f"Final depression score: {depression_score:.3f}")
            return depression_score, detected_categories
            
        except Exception as e:
            logger.error(f"Depression analysis failed: {e}")
            return 0.0, ['analysis_error']

    def enhanced_depression_analysis(self, message: str, base_score: float = 0.0, sentiment_model=None, 
                                   analysis_parameters_manager=None, context=None,
                                   crisis_pattern_manager: Optional[CrisisPatternManager] = None) -> Dict:
        """
        Enhanced depression analysis with detailed breakdown (STEP 10.6: Consolidated from utils)
        
        Args:
            message: Message text to analyze
            base_score: Base score to enhance
            sentiment_model: Optional sentiment analysis model  
            context: Optional context information
            crisis_pattern_manager: Optional CrisisPatternManager (uses self.crisis_pattern_manager if None)
            
        Returns:
            Dictionary with enhanced analysis results
        """
        
        # Use injected manager if not provided
        pattern_manager = crisis_pattern_manager or self.crisis_pattern_manager
        
        logger.debug(f"Enhanced depression analysis: base_score={base_score:.3f}")
        
        try:
            detected_categories = []
            adjustment_reasons = []
            
            # Sentiment analysis
            sentiment_scores = {}
            if sentiment_model:
                try:
                    sentiment_result = sentiment_model(message)
                    sentiment_scores = self._process_sentiment_result(sentiment_result)
                except Exception as e:
                    logger.warning(f"Sentiment analysis failed: {e}")
            
            # Pattern-based adjustments using CrisisPatternManager if available
            pattern_adjustment = 0.0
            if pattern_manager:
                try:
                    # STEP 10.7: Apply context weights using CrisisPatternManager
                    modified_score, weight_details = pattern_manager.apply_context_weights(message, base_score)
                    pattern_adjustment = modified_score - base_score
                    
                    if pattern_adjustment != 0:
                        adjustment_reasons.append(f"pattern_analysis({pattern_adjustment:+.3f})")
                        logger.debug(f"Pattern adjustment: {pattern_adjustment:+.3f}")
                    
                except Exception as e:
                    logger.warning(f"Pattern analysis failed: {e}")
            
            # Context-based adjustments (conservative)
            context_adjustment = 0.0
            if context:
                # Social isolation indicators
                isolation_count = context.get('social_isolation_indicators', 0)
                if isolation_count > 2:
                    context_adjustment += 0.04
                    adjustment_reasons.append("social_isolation(+0.04)")
                
                # Hopelessness indicators
                hopelessness_count = context.get('hopelessness_indicators', 0)
                if hopelessness_count > 1:
                    context_adjustment += 0.06
                    adjustment_reasons.append("hopelessness(+0.06)")
                
                # Negation context (reduce score)
                if context.get('negation_context'):
                    context_adjustment -= 0.05
                    adjustment_reasons.append("negation(-0.05)")
            
            # Sentiment-based adjustments (conservative)
            sentiment_adjustment = 0.0
            if sentiment_scores:
                negative_score = sentiment_scores.get('negative', 0.0)
                positive_score = sentiment_scores.get('positive', 0.0)
                
                if negative_score > 0.7:
                    sentiment_adjustment += 0.08
                    adjustment_reasons.append(f"high_negative_sentiment(+0.08)")
                elif positive_score > 0.7:
                    sentiment_adjustment -= 0.04
                    adjustment_reasons.append(f"high_positive_sentiment(-0.04)")
            
            # Calculate final score
            total_adjustment = pattern_adjustment + context_adjustment + sentiment_adjustment
            final_score = max(0.0, min(1.0, base_score + total_adjustment))
            
            return {
                'base_score': base_score,
                'final_score': final_score,
                'total_adjustment': total_adjustment,
                'adjustments': {
                    'pattern_adjustment': pattern_adjustment,
                    'context_adjustment': context_adjustment,
                    'sentiment_adjustment': sentiment_adjustment
                },
                'detected_categories': detected_categories,
                'adjustment_reasons': adjustment_reasons,
                'sentiment_scores': sentiment_scores,
                'analysis_method': 'enhanced_depression_v3d10.6',
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Enhanced depression analysis failed: {e}")
            return {
                'base_score': base_score,
                'final_score': base_score,
                'total_adjustment': 0.0,
                'adjustments': {},
                'detected_categories': ['analysis_error'],
                'adjustment_reasons': [f"error: {str(e)}"],
                'sentiment_scores': {},
                'analysis_method': 'enhanced_depression_v3d10.6',
                'success': False,
                'error': str(e)
            }

    def _process_sentiment_result(self, sentiment_result) -> Dict[str, float]:
        """Process sentiment model result into standardized format"""
        try:
            if isinstance(sentiment_result, list) and len(sentiment_result) > 0:
                result = sentiment_result[0]
                if isinstance(result, dict):
                    scores = {}
                    scores['negative'] = result.get('score', 0.0) if result.get('label') == 'NEGATIVE' else 0.0
                    scores['positive'] = result.get('score', 0.0) if result.get('label') == 'POSITIVE' else 0.0
                    return scores
            
            return {'negative': 0.0, 'positive': 0.0}
        except Exception as e:
            logger.warning(f"Sentiment result processing failed: {e}")
            return {'negative': 0.0, 'positive': 0.0}


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_crisis_analyzer(models_manager, crisis_pattern_manager=None, learning_manager=None,
                          analysis_parameters_manager=None, threshold_mapping_manager=None,
                          feature_config_manager=None, performance_config_manager=None,
                          context_pattern_manager=None) -> CrisisAnalyzer:  # NEW parameter
    """
    Factory function to create CrisisAnalyzer instance with ContextPatternManager
    Updated for Step 10.8: Context Pattern Manager integration
    
    Args:
        models_manager: ML model manager for ensemble analysis
        crisis_pattern_manager: CrisisPatternManager for pattern-based analysis
        learning_manager: Optional learning manager for feedback
        analysis_parameters_manager: AnalysisParametersManager for configurable parameters
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds
        feature_config_manager: FeatureConfigManager for feature flags
        performance_config_manager: PerformanceConfigManager for performance settings
        context_pattern_manager: ContextPatternManager for context analysis (NEW)
        
    Returns:
        CrisisAnalyzer instance with Step 10.8 context pattern integration
    """
    return CrisisAnalyzer(
        models_manager=models_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        learning_manager=learning_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager,
        context_pattern_manager=context_pattern_manager  # NEW
    )

__all__ = ['CrisisAnalyzer', 'create_crisis_analyzer']

logger.info("✅ CrisisAnalyzer v3.1 Step 10.7 loaded - Community pattern consolidation complete")