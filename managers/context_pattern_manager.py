#!/usr/bin/env python3
# ash-nlp/managers/context_pattern_manager.py
"""
Context Pattern Manager for Ash NLP Service
FILE VERSION: v3.1-3d-10.8-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.8 - Context Pattern Management
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: NEW - Context pattern functionality consolidated from utils/context_helpers.py
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

SAFETY NOTICE: This manager provides context analysis for crisis detection patterns.
Context signals help determine the severity and urgency of mental health crisis situations.
"""

import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from managers.unified_config_manager import UnifiedConfigManager

logger = logging.getLogger(__name__)

class ContextPatternManager:
    """
    Context Pattern Manager for semantic and contextual analysis of crisis messages
    
    Features:
    - Context signal extraction and analysis
    - Negation detection for sentiment interpretation
    - Sentiment context analysis with polarity flipping
    - Enhanced context analysis with crisis pattern integration
    - Term relevance scoring in context windows
    - v3.1 JSON configuration compatibility with existing environment variables
    - Production-ready error handling and resilience
    
    This manager consolidates all context analysis functionality previously scattered
    across utils/context_helpers.py, providing centralized, configurable context
    pattern management for the crisis detection system.
    
    Integration:
    - Works with CrisisPatternManager for enhanced pattern detection
    - Integrates with AnalysisParametersManager for semantic parameters
    - Used by CrisisAnalyzer for comprehensive message analysis
    """

    def __init__(self, unified_config: UnifiedConfigManager):
        """
        Initialize Context Pattern Manager with dependency injection
        
        Args:
            unified_config: UnifiedConfigManager instance for configuration loading
        """
        self.unified_config = unified_config
        self.context_config = {}
        self.analysis_params = {}
        self.initialization_time = time.time()
        
        # Basic negation patterns (will be enhanced with config)
        self.basic_negation_patterns = [
            r'\b(not?|no|never|neither|nor|can\'t|cannot|won\'t|wouldn\'t|shouldn\'t|couldn\'t|don\'t|doesn\'t|didn\'t|isn\'t|aren\'t|wasn\'t|weren\'t)\b',
            r'\b(barely|hardly|scarcely|seldom|rarely)\b',
            r'\b(without|lacking|missing|absent)\b'
        ]
        
        # Load configuration during initialization
        self._load_configuration()
        
        logger.info("ContextPatternManager v3.1-3d-10.8-1 initialized successfully")

    def _load_configuration(self) -> None:
        """Load context patterns and analysis parameters from configuration"""
        try:
            # Load context patterns configuration
            self.context_config = self.unified_config.get_crisis_patterns('context_patterns')
            if not self.context_config:
                logger.warning("⚠️ Context patterns configuration not found, using safe defaults")
                self.context_config = self._get_safe_context_defaults()
            
            # Load analysis parameters for semantic analysis - FIXED: Use correct method
            try:
                # Try different methods to load analysis parameters
                if hasattr(self.unified_config, 'load_config'):
                    self.analysis_params = self.unified_config.load_config('analysis_parameters')
                elif hasattr(self.unified_config, 'get_config'):
                    self.analysis_params = self.unified_config.get_config('analysis_parameters')
                else:
                    # Fallback to loading from config cache if available
                    self.analysis_params = getattr(self.unified_config, 'config_cache', {}).get('analysis_parameters', {})
            except Exception as param_error:
                logger.warning(f"⚠️ Could not load analysis parameters: {param_error}")
                self.analysis_params = {}
                
            if not self.analysis_params:
                logger.warning("⚠️ Analysis parameters not found, using safe defaults")
                self.analysis_params = self._get_safe_analysis_defaults()
                
            logger.info("✅ Context pattern configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Error loading context configuration: {e}")
            self.context_config = self._get_safe_context_defaults()
            self.analysis_params = self._get_safe_analysis_defaults()

    def _get_safe_context_defaults(self) -> Dict[str, Any]:
        """Get safe default context configuration when JSON loading fails"""
        return {
            'configuration': {
                'enabled': True,
                'global_multiplier': 1.0,
                'context_window': 10,
                'priority_level': 'high',
                'bidirectional_analysis': True
            }
        }

    def _get_safe_analysis_defaults(self) -> Dict[str, Any]:
        """Get safe default analysis parameters when JSON loading fails"""
        return {
            'semantic_analysis': {
                'context_window': 3,
                'similarity_threshold': 0.75,
                'context_boost_weight': 1.5,
                'negative_threshold': 0.6
            }
        }

    # ========================================================================
    # CORE CONTEXT ANALYSIS METHODS - Migrated from utils/context_helpers.py
    # ========================================================================

    def extract_context_signals(self, message: str) -> Dict[str, Any]:
        """
        Extract basic context signals from message
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary containing context signals and metadata
            
        Note:
            Migrated from utils/context_helpers.py - extract_context_signals()
            This function provides basic context signals only.
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
        
        Args:
            message: Message text to analyze
            
        Returns:
            True if negation patterns detected, False otherwise
            
        Note:
            Migrated from utils/context_helpers.py - detect_negation_context()
        """
        message_lower = message.lower().strip()
        
        for pattern in self.basic_negation_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False

    def analyze_sentiment_context(self, message: str, base_sentiment: float = 0.0) -> Dict[str, Any]:
        """
        Analyze sentiment context for the message
        
        Args:
            message: Message text to analyze
            base_sentiment: Base sentiment score to work with
            
        Returns:
            Dictionary with sentiment context analysis results
            
        Note:
            Migrated from utils/context_helpers.py - analyze_sentiment_context()
            Enhanced with configuration support
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

    def process_sentiment_with_flip(self, message: str, sentiment_score: float) -> Dict[str, Any]:
        """
        Process sentiment with potential polarity flipping based on context
        
        Args:
            message: Message text to analyze
            sentiment_score: Original sentiment score
            
        Returns:
            Dictionary with processed sentiment results
            
        Note:
            Migrated from utils/context_helpers.py - process_sentiment_with_flip()
        """
        sentiment_context = self.analyze_sentiment_context(message, sentiment_score)
        
        processed_sentiment = {
            'original_score': sentiment_score,
            'final_score': sentiment_score,
            'flip_applied': False,
            'context_analysis': sentiment_context
        }
        
        # Apply sentiment flip if negation detected and score is significant
        if sentiment_context['sentiment_flip_candidate'] and abs(sentiment_score) > 0.1:
            processed_sentiment['final_score'] = -sentiment_score
            processed_sentiment['flip_applied'] = True
            logger.debug(f"Sentiment flip applied: {sentiment_score} → {-sentiment_score}")
        
        return processed_sentiment

    def perform_enhanced_context_analysis(self, message: str, crisis_pattern_manager=None) -> Dict[str, Any]:
        """
        Perform enhanced context analysis with optional crisis pattern integration
        
        Args:
            message: Message text to analyze  
            crisis_pattern_manager: Optional CrisisPatternManager for enhanced analysis
            
        Returns:
            Enhanced context analysis results
            
        Note:
            Migrated from utils/context_helpers.py - perform_enhanced_context_analysis()
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

    def score_term_in_context(self, term: str, message: str, context_window: Optional[int] = None) -> Dict[str, Any]:
        """
        Score a term's relevance in message context
        
        Args:
            term: Term to score
            message: Full message text
            context_window: Number of words around term to consider (uses config default if None)
            
        Returns:
            Dictionary with term scoring results
            
        Note:
            Migrated from utils/context_helpers.py - score_term_in_context()
        """
        
        if context_window is None:
            context_window = self._get_context_window()
            
        message_lower = message.lower()
        term_lower = term.lower()
        
        if term_lower not in message_lower:
            return {
                'term': term,
                'found': False,
                'relevance_score': 0.0,
                'context_words': []
            }
        
        words = message_lower.split()
        term_positions = []
        
        # Find all positions of the term
        for i, word in enumerate(words):
            if term_lower in word:
                term_positions.append(i)
        
        context_words = []
        for pos in term_positions:
            start = max(0, pos - context_window)
            end = min(len(words), pos + context_window + 1)
            context_words.extend(words[start:end])
        
        # Remove duplicates while preserving order
        context_words = list(dict.fromkeys(context_words))
        
        # Basic relevance scoring based on context
        crisis_indicators = ['crisis', 'help', 'struggling', 'difficult', 'hard', 'scared', 'worried']
        positive_indicators = ['good', 'great', 'happy', 'love', 'amazing', 'wonderful']
        
        crisis_score = sum(1 for word in context_words if word in crisis_indicators)
        positive_score = sum(1 for word in context_words if word in positive_indicators)
        
        relevance_score = (crisis_score * 0.7 + len(context_words) * 0.1) / (positive_score * 0.5 + 1)
        relevance_score = min(1.0, max(0.0, relevance_score))
        
        return {
            'term': term,
            'found': True,
            'positions': term_positions,
            'relevance_score': relevance_score,
            'context_words': context_words,
            'crisis_indicators': crisis_score,
            'positive_indicators': positive_score
        }

    # ========================================================================
    # CONFIGURATION HELPERS - Using existing .env.template variables
    # ========================================================================

    def _get_context_window(self) -> int:
        """Get context window size from configuration"""
        try:
            # Use existing .env.template variable: NLP_ANALYSIS_SEMANTIC_CONTEXT_WINDOW
            return self.unified_config.get_env_int('NLP_ANALYSIS_SEMANTIC_CONTEXT_WINDOW', 3)
        except Exception as e:
            logger.warning(f"⚠️ Error getting context window: {e}, using default: 3")
            return 3

    def _get_context_boost_weight(self) -> float:
        """Get context boost weight from configuration"""
        try:
            # Use existing .env.template variable: NLP_ANALYSIS_CONTEXT_BOOST_WEIGHT
            return self.unified_config.get_env_float('NLP_ANALYSIS_CONTEXT_BOOST_WEIGHT', 1.5)
        except Exception as e:
            logger.warning(f"⚠️ Error getting context boost weight: {e}, using default: 1.5")
            return 1.5

    def _get_negative_threshold(self) -> float:
        """Get negative sentiment threshold from configuration"""
        try:
            # Use existing .env.template variable: NLP_ANALYSIS_SEMANTIC_NEGATIVE_THRESHOLD
            return self.unified_config.get_env_float('NLP_ANALYSIS_SEMANTIC_NEGATIVE_THRESHOLD', 0.6)
        except Exception as e:
            logger.warning(f"⚠️ Error getting negative threshold: {e}, using default: 0.6")
            return 0.6

    # ========================================================================
    # HELPER METHODS - Support functions for context analysis
    # ========================================================================

    def _extract_basic_temporal_indicators(self, message_lower: str) -> List[str]:
        """Extract basic temporal indicators from message"""
        basic_temporal_words = [
            'today', 'yesterday', 'tomorrow', 'lately', 'recently', 'always', 
            'never', 'sometimes', 'right now', 'immediately', 'urgent', 'tonight'
        ]
        
        return [word for word in basic_temporal_words if word in message_lower]

    def _count_social_isolation_indicators(self, message_lower: str) -> int:
        """Count basic social isolation indicators"""
        isolation_words = [
            'alone', 'lonely', 'isolated', 'nobody', 'no one', 'abandoned', 
            'by myself', 'on my own', 'no friends', 'no family'
        ]
        
        return sum(1 for word in isolation_words if word in message_lower)

    def _count_hopelessness_indicators(self, message_lower: str) -> int:
        """Count basic hopelessness indicators"""
        hopelessness_words = [
            'hopeless', 'pointless', 'worthless', 'useless', 'meaningless',
            'give up', 'no point', 'why bother', 'what\'s the point'
        ]
        
        return sum(1 for word in hopelessness_words if word in message_lower)

    # ========================================================================
    # CONFIGURATION AND STATUS METHODS
    # ========================================================================

    def get_configuration_status(self) -> Dict[str, Any]:
        """Get current configuration status"""
        return {
            'manager_version': 'v3.1-3d-10.8-1',
            'initialization_time': self.initialization_time,
            'configuration_loaded': bool(self.context_config),
            'analysis_params_loaded': bool(self.analysis_params),
            'context_window': self._get_context_window(),
            'context_boost_weight': self._get_context_boost_weight(),
            'negative_threshold': self._get_negative_threshold(),
            'patterns_available': len(self.basic_negation_patterns)
        }

    def reload_configuration(self) -> bool:
        """Reload configuration from files"""
        try:
            self._load_configuration()
            logger.info("✅ Context pattern configuration reloaded successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error reloading context configuration: {e}")
            return False

    # ========================================================================
    # FACTORY INTEGRATION SUPPORT
    # ========================================================================

    def is_initialized(self) -> bool:
        """Check if manager is properly initialized"""
        return bool(self.unified_config and self.context_config)


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_context_pattern_manager(unified_config: UnifiedConfigManager) -> ContextPatternManager:
    """
    Factory function to create ContextPatternManager instance with dependency injection
    
    Args:
        unified_config: UnifiedConfigManager instance for configuration loading
        
    Returns:
        ContextPatternManager instance ready for use
        
    Raises:
        RuntimeError: If initialization fails
    """
    try:
        manager = ContextPatternManager(unified_config)
        
        if not manager.is_initialized():
            raise RuntimeError("ContextPatternManager failed to initialize properly")
            
        logger.info("✅ ContextPatternManager created successfully via factory function")
        return manager
        
    except Exception as e:
        logger.error(f"❌ Failed to create ContextPatternManager: {e}")
        raise RuntimeError(f"ContextPatternManager factory function failed: {e}")


# Export for clean architecture
__all__ = [
    'ContextPatternManager',
    'create_context_pattern_manager'
]