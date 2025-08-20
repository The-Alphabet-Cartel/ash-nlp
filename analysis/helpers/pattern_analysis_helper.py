# ash-nlp/analysis/helpers/pattern_analysis_helper.py
"""
Pattern Analysis Helper for CrisisAnalyzer
FILE VERSION: v3.1-3e-5.5-6-1
CREATED: 2025-08-20
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

MIGRATION NOTICE: Methods moved from CrisisAnalyzer for optimization
Original location: analysis/crisis_analyzer.py - pattern analysis and detection methods
"""

import logging
import re
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class PatternAnalysisHelper:
    """Helper class for pattern analysis operations moved from CrisisAnalyzer"""
    
    def __init__(self, crisis_analyzer):
        """
        Initialize with reference to parent CrisisAnalyzer
        
        Args:
            crisis_analyzer: Parent CrisisAnalyzer instance
        """
        self.crisis_analyzer = crisis_analyzer
    
    # ========================================================================
    # CONTEXT SIGNAL EXTRACTION
    # ========================================================================
    
    def extract_context_signals(self, message: str) -> Dict[str, Any]:
        """
        Extract basic context signals from message
        Migrated from: CrisisAnalyzer.extract_context_signals()
        """
        message_lower = message.lower().strip()
        
        # Basic context signals
        context = {
            'message_length': len(message),
            'word_count': len(message.split()),
            'has_question_mark': '?' in message,
            'has_exclamation': '!' in message,
            'has_capitalization': any(c.isupper() for c in message),
            'negation_context': self.detect_negation_context(message),
            'temporal_indicators': self._extract_basic_temporal_indicators(message_lower),
            'message_lower': message_lower,
            'social_isolation_indicators': self._count_social_isolation_indicators(message_lower),
            'hopelessness_indicators': self._count_hopelessness_indicators(message_lower),
            # Flags for pattern analysis integration
            'requires_pattern_analysis': True,
            'pattern_manager_needed': True
        }
        
        return context

    def detect_negation_context(self, message: str) -> bool:
        """
        Detect if the message contains negation that might affect crisis interpretation
        Migrated from: CrisisAnalyzer.detect_negation_context()
        """
        message_lower = message.lower().strip()
        
        for pattern in self.crisis_analyzer.basic_negation_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False

    def analyze_sentiment_context(self, message: str, base_sentiment: float = 0.0) -> Dict[str, Any]:
        """
        Analyze sentiment context for the message
        Migrated from: CrisisAnalyzer.analyze_sentiment_context()
        """
        context = self.extract_context_signals(message)
        
        # Get semantic analysis parameters from existing .env.template variables
        context_window = self._get_context_window()
        negative_threshold = self._get_negative_threshold()
        
        sentiment_context = {
            'base_sentiment': base_sentiment,
            'negation_detected': context['negation_context'],
            'context_window': context_window,
            'negative_threshold': negative_threshold,
            'message_indicators': {
                'social_isolation': context['social_isolation_indicators'],
                'hopelessness': context['hopelessness_indicators'],
                'temporal_urgency': len(context['temporal_indicators'])
            }
        }
        
        # Analyze sentiment polarity
        if context['negation_context'] and base_sentiment != 0.0:
            sentiment_context['sentiment_flip_candidate'] = True
            sentiment_context['original_sentiment'] = base_sentiment
        else:
            sentiment_context['sentiment_flip_candidate'] = False
            
        return sentiment_context

    def perform_enhanced_context_analysis(self, message: str, crisis_pattern_manager=None) -> Dict[str, Any]:
        """
        Perform enhanced context analysis with optional crisis pattern integration
        Migrated from: CrisisAnalyzer.perform_enhanced_context_analysis()
        """
        
        # Start with basic context signals
        context = self.extract_context_signals(message)
        
        if crisis_pattern_manager:
            try:
                # Get enhanced pattern analysis from CrisisPatternManager
                context_patterns = crisis_pattern_manager.get_crisis_context_patterns()
                positive_patterns = crisis_pattern_manager.get_positive_context_patterns()
                temporal_analysis = crisis_pattern_manager.analyze_temporal_indicators(message)
                
                # Merge advanced analysis into context
                context.update({
                    'crisis_context_available': True,
                    'temporal_analysis': temporal_analysis,
                    'pattern_manager_status': 'available'
                })
                
                logger.debug("Enhanced context analysis completed with CrisisPatternManager")
                
            except Exception as e:
                logger.error(f"Error in enhanced context analysis: {e}")
                context.update({
                    'crisis_context_available': False,
                    'pattern_manager_status': 'error',
                    'pattern_manager_error': str(e)
                })
        else:
            context.update({
                'crisis_context_available': False,
                'pattern_manager_status': 'not_available'
            })
            logger.debug("Basic context analysis only - CrisisPatternManager not available")
        
        return context
    
    # ========================================================================
    # HELPER METHODS - Support functions for context analysis
    # ========================================================================

    def _extract_basic_temporal_indicators(self, message_lower: str) -> List[str]:
        """
        Extract basic temporal indicators from message
        Migrated from: CrisisAnalyzer._extract_basic_temporal_indicators()
        """
        basic_temporal_words = [
            'today', 'yesterday', 'tomorrow', 'lately', 'recently', 'always', 
            'never', 'sometimes', 'right now', 'immediately', 'urgent', 'tonight'
        ]
        
        return [word for word in basic_temporal_words if word in message_lower]

    def _count_social_isolation_indicators(self, message_lower: str) -> int:
        """
        Count basic social isolation indicators
        Migrated from: CrisisAnalyzer._count_social_isolation_indicators()
        """
        isolation_words = [
            'alone', 'lonely', 'isolated', 'nobody', 'no one', 'abandoned', 
            'by myself', 'on my own', 'no friends', 'no family'
        ]
        
        return sum(1 for word in isolation_words if word in message_lower)

    def _count_hopelessness_indicators(self, message_lower: str) -> int:
        """
        Count basic hopelessness indicators
        Migrated from: CrisisAnalyzer._count_hopelessness_indicators()
        """
        hopelessness_words = [
            'hopeless', 'pointless', 'worthless', 'useless', 'meaningless',
            'give up', 'no point', 'why bother', 'what\'s the point'
        ]
        
        return sum(1 for word in hopelessness_words if word in message_lower)

    def _get_context_window(self) -> int:
        """
        Get context window size from configuration
        Migrated from: CrisisAnalyzer._get_context_window()
        """
        try:
            value = self.crisis_analyzer.unified_config_manager.get_config_section('analysis_parameters', 'semantic_analysis.context_window', 3)
            return int(value) if value is not None else 3
        except Exception as e:
            logger.warning(f"Error getting context window: {e}, using default: 3")
            return 3

    def _get_negative_threshold(self) -> float:
        """
        Get negative sentiment threshold from configuration
        Migrated from: CrisisAnalyzer._get_negative_threshold()
        """
        try:
            value = self.crisis_analyzer.unified_config_manager.get_config_section('analysis_parameters', 'semantic_analysis.negative_threshold', 0.6)
            return float(value) if value is not None else 0.6
        except Exception as e:
            logger.warning(f"Error getting negative threshold: {e}, using default: 0.6")
            return 0.6
    
    # ========================================================================
    # PATTERN SCORING AND ANALYSIS
    # ========================================================================
    
    def score_term_in_context(self, term: str, message: str, context_window: Optional[int] = None) -> Dict[str, Any]:
        """
        Score term relevance in message context using ContextPatternManager
        Migrated from: CrisisAnalyzer.score_term_in_context()
        """
        try:
            if self.crisis_analyzer.context_pattern_manager:
                return self.crisis_analyzer.context_pattern_manager.score_term_in_context(term, message, context_window)
            else:
                logger.warning("ContextPatternManager not available for term scoring")
                return {'term': term, 'found': False, 'context_available': False}
        except Exception as e:
            logger.error(f"Term context scoring failed: {e}")
            return {'term': term, 'found': False, 'error': str(e)}
    
    def get_basic_context_fallback(self, message: str) -> Dict[str, Any]:
        """
        Basic context fallback when ContextPatternManager is not available
        Migrated from: CrisisAnalyzer._basic_context_fallback()
        """
        return {
            'message_length': len(message),
            'word_count': len(message.split()),
            'has_question_mark': '?' in message,
            'has_exclamation': '!' in message,
            'fallback_mode': True,
            'context_manager_available': False
        }
    
    # ========================================================================
    # BASIC CRISIS ANALYSIS PATTERNS
    # ========================================================================
    
    async def basic_crisis_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Basic crisis analysis when ensemble is disabled by feature flag
        Migrated from: CrisisAnalyzer._basic_crisis_analysis()
        """
        logger.info("Running basic crisis analysis - ensemble disabled by feature flag")
        
        # Check if pattern analysis is enabled
        pattern_analysis_enabled = self.crisis_analyzer._feature_cache.get('pattern_analysis', False)
        
        if pattern_analysis_enabled and self.crisis_analyzer.crisis_pattern_manager:
            logger.debug("Pattern analysis enabled for basic analysis")
            
            # Use CrisisPatternManager methods directly
            try:
                enhanced_patterns = self.crisis_analyzer.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
                
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
                        
                    logger.debug(f"Pattern-based analysis result: {crisis_level} (conf: {confidence})")
                else:
                    crisis_level = 'none'
                    confidence = 0.0
                    logger.debug("No patterns triggered in basic analysis")
                    
            except Exception as e:
                logger.error(f"Basic pattern analysis failed: {e}")
                crisis_level = 'none'
                confidence = 0.0
                enhanced_patterns = {'error': str(e)}
        else:
            logger.debug("Pattern analysis disabled - returning minimal analysis")
            enhanced_patterns = {'matches': [], 'error': 'Pattern analysis disabled by feature flag'}
            crisis_level = 'none'
            confidence = 0.0
        
        # Return proper response structure with all required fields
        return {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'needs_response': crisis_level != 'none',
            'crisis_level': crisis_level,
            'confidence_score': confidence,
            'detected_categories': self._extract_categories_from_patterns({'enhanced_patterns': enhanced_patterns}),
            'method': 'basic_pattern_only' if pattern_analysis_enabled else 'basic_disabled',
            'analysis_results': {
                'crisis_score': confidence,
                'crisis_level': crisis_level,
                'pattern_analysis': {'enhanced_patterns': enhanced_patterns},
                'analysis_metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'analysis_version': 'v3.1-3e-5.5-6',
                    'ensemble_disabled': True,
                    'enhanced_consolidation': True
                }
            },
            'requires_staff_review': self.crisis_analyzer._determine_staff_review_requirement(confidence, crisis_level),
            'processing_time': time.time() - start_time
        }
    
    def _extract_categories_from_patterns(self, pattern_analysis: Dict) -> List[str]:
        """
        Extract detected categories from pattern analysis
        Helper method for pattern analysis
        """
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