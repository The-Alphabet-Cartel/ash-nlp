# ash-nlp/utils/context_helpers.py
"""
Backward Compatibility Layer for utils/context_helpers.py
FILE VERSION: v3.1-3d-10.8-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.8 - Context Pattern Management Transition
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: DEPRECATED - Functions moved to ContextPatternManager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This module provides backward compatibility during the transition from
utils/context_helpers.py to the new ContextPatternManager approach.

⚠️  DEPRECATION NOTICE:
These functions are deprecated and will be removed in a future version.
New code should use ContextPatternManager directly through dependency injection.

Migration Path:
1. Replace direct imports with manager-based access
2. Use factory functions to create ContextPatternManager instances  
3. Access methods via CrisisAnalyzer's context_pattern_manager attribute
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# ============================================================================
# BACKWARD COMPATIBILITY FUNCTIONS - DEPRECATED
# ============================================================================

def extract_context_signals(message: str) -> Dict[str, Any]:
    """
    DEPRECATED: Extract basic context signals from message
    
    Args:
        message: Message text to analyze
        
    Returns:
        Dictionary containing context signals
        
    Note:
        This function is deprecated. Use ContextPatternManager.extract_context_signals() instead.
        Migration: context_pattern_manager.extract_context_signals(message)
    """
    logger.warning("⚠️ DEPRECATED: extract_context_signals() moved to ContextPatternManager")
    
    try:
        # Try to use the new ContextPatternManager if available
        from managers.context_pattern_manager import create_context_pattern_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager()
        context_manager = create_context_pattern_manager(config_manager)
        return context_manager.extract_context_signals(message)
        
    except Exception as e:
        logger.error(f"❌ Failed to use ContextPatternManager, using fallback: {e}")
        return _legacy_context_signals_fallback(message)

def detect_negation_context(message: str) -> bool:
    """
    DEPRECATED: Detect if the message contains negation
    
    Args:
        message: Message text to analyze
        
    Returns:
        True if negation patterns detected
        
    Note:
        This function is deprecated. Use ContextPatternManager.detect_negation_context() instead.
        Migration: context_pattern_manager.detect_negation_context(message)
    """
    logger.warning("⚠️ DEPRECATED: detect_negation_context() moved to ContextPatternManager")
    
    try:
        from managers.context_pattern_manager import create_context_pattern_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager()
        context_manager = create_context_pattern_manager(config_manager)
        return context_manager.detect_negation_context(message)
        
    except Exception as e:
        logger.error(f"❌ Failed to use ContextPatternManager, using fallback: {e}")
        return _legacy_negation_fallback(message)

def analyze_sentiment_context(message: str, base_sentiment: float = 0.0) -> Dict[str, Any]:
    """
    DEPRECATED: Analyze sentiment context for the message
    
    Args:
        message: Message text to analyze
        base_sentiment: Base sentiment score
        
    Returns:
        Dictionary with sentiment context analysis results
        
    Note:
        This function is deprecated. Use ContextPatternManager.analyze_sentiment_context() instead.
        Migration: context_pattern_manager.analyze_sentiment_context(message, base_sentiment)
    """
    logger.warning("⚠️ DEPRECATED: analyze_sentiment_context() moved to ContextPatternManager")
    
    try:
        from managers.context_pattern_manager import create_context_pattern_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager()
        context_manager = create_context_pattern_manager(config_manager)
        return context_manager.analyze_sentiment_context(message, base_sentiment)
        
    except Exception as e:
        logger.error(f"❌ Failed to use ContextPatternManager, using fallback: {e}")
        return {'base_sentiment': base_sentiment, 'error': str(e), 'fallback_used': True}

def process_sentiment_with_flip(message: str, sentiment_score: float) -> Dict[str, Any]:
    """
    DEPRECATED: Process sentiment with potential polarity flipping
    
    Args:
        message: Message text to analyze
        sentiment_score: Original sentiment score
        
    Returns:
        Dictionary with processed sentiment results
        
    Note:
        This function is deprecated. Use ContextPatternManager.process_sentiment_with_flip() instead.
        Migration: context_pattern_manager.process_sentiment_with_flip(message, sentiment_score)
    """
    logger.warning("⚠️ DEPRECATED: process_sentiment_with_flip() moved to ContextPatternManager")
    
    try:
        from managers.context_pattern_manager import create_context_pattern_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager()
        context_manager = create_context_pattern_manager(config_manager)
        return context_manager.process_sentiment_with_flip(message, sentiment_score)
        
    except Exception as e:
        logger.error(f"❌ Failed to use ContextPatternManager, using fallback: {e}")
        return {
            'original_score': sentiment_score,
            'final_score': sentiment_score,
            'flip_applied': False,
            'error': str(e),
            'fallback_used': True
        }

def perform_enhanced_context_analysis(message: str, crisis_pattern_manager=None) -> Dict[str, Any]:
    """
    DEPRECATED: Perform enhanced context analysis
    
    Args:
        message: Message text to analyze
        crisis_pattern_manager: Optional CrisisPatternManager instance
        
    Returns:
        Enhanced context analysis results
        
    Note:
        This function is deprecated. Use ContextPatternManager.perform_enhanced_context_analysis() instead.
        Migration: context_pattern_manager.perform_enhanced_context_analysis(message, crisis_pattern_manager)
    """
    logger.warning("⚠️ DEPRECATED: perform_enhanced_context_analysis() moved to ContextPatternManager")
    
    try:
        from managers.context_pattern_manager import create_context_pattern_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager()
        context_manager = create_context_pattern_manager(config_manager)
        return context_manager.perform_enhanced_context_analysis(message, crisis_pattern_manager)
        
    except Exception as e:
        logger.error(f"❌ Failed to use ContextPatternManager, using fallback: {e}")
        return {
            'crisis_context_available': False,
            'pattern_manager_status': 'error',
            'error': str(e),
            'fallback_used': True
        }

def score_term_in_context(term: str, message: str, context_window: int = 3) -> Dict[str, Any]:
    """
    DEPRECATED: Score a term's relevance in message context
    
    Args:
        term: Term to score
        message: Full message text
        context_window: Number of words around term to consider
        
    Returns:
        Dictionary with term scoring results
        
    Note:
        This function is deprecated. Use ContextPatternManager.score_term_in_context() instead.
        Migration: context_pattern_manager.score_term_in_context(term, message, context_window)
    """
    logger.warning("⚠️ DEPRECATED: score_term_in_context() moved to ContextPatternManager")
    
    try:
        from managers.context_pattern_manager import create_context_pattern_manager
        from managers.unified_config_manager import create_unified_config_manager
        
        config_manager = create_unified_config_manager()
        context_manager = create_context_pattern_manager(config_manager)
        return context_manager.score_term_in_context(term, message, context_window)
        
    except Exception as e:
        logger.error(f"❌ Failed to use ContextPatternManager, using fallback: {e}")
        return {
            'term': term,
            'found': False,
            'relevance_score': 0.0,
            'context_words': [],
            'error': str(e),
            'fallback_used': True
        }

# ============================================================================
# LEGACY FALLBACK IMPLEMENTATIONS - Minimal functionality
# ============================================================================

def _legacy_context_signals_fallback(message: str) -> Dict[str, Any]:
    """Minimal context signals fallback when ContextPatternManager fails"""
    return {
        'message_length': len(message),
        'word_count': len(message.split()),
        'has_question_mark': '?' in message,
        'has_exclamation': '!' in message,
        'has_capitalization': any(c.isupper() for c in message),
        'negation_context': _legacy_negation_fallback(message),
        'temporal_indicators': [],
        'social_isolation_indicators': 0,
        'hopelessness_indicators': 0,
        'fallback_mode': True,
        'manager_available': False
    }

def _legacy_negation_fallback(message: str) -> bool:
    """Basic negation detection fallback"""
    negation_words = ['not', 'no', 'never', 'neither', 'nor', "can't", "cannot", 
                     "won't", "wouldn't", "shouldn't", "couldn't", "don't", 
                     "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't"]
    
    message_lower = message.lower()
    return any(word in message_lower for word in negation_words)

# ============================================================================
# MIGRATION HELPER FUNCTIONS
# ============================================================================

def get_migration_info() -> Dict[str, Any]:
    """
    Get information about migrating from utils/context_helpers.py to ContextPatternManager
    
    Returns:
        Dictionary with migration guidance
    """
    return {
        'migration_status': 'DEPRECATED - Functions moved to ContextPatternManager',
        'new_manager': 'ContextPatternManager',
        'factory_function': 'create_context_pattern_manager(unified_config)',
        'integration_point': 'CrisisAnalyzer.context_pattern_manager',
        'function_mapping': {
            'extract_context_signals': 'ContextPatternManager.extract_context_signals()',
            'detect_negation_context': 'ContextPatternManager.detect_negation_context()',
            'analyze_sentiment_context': 'ContextPatternManager.analyze_sentiment_context()',
            'process_sentiment_with_flip': 'ContextPatternManager.process_sentiment_with_flip()',
            'perform_enhanced_context_analysis': 'ContextPatternManager.perform_enhanced_context_analysis()',
            'score_term_in_context': 'ContextPatternManager.score_term_in_context()'
        },
        'benefits': [
            'Centralized configuration management',
            'Proper dependency injection',
            'Enhanced error handling and resilience',
            'Integration with existing manager ecosystem',
            'Production-ready performance optimization'
        ],
        'migration_steps': [
            '1. Replace direct function imports with manager-based access',
            '2. Update constructor dependency injection to include ContextPatternManager',
            '3. Access context functions via manager instance methods',
            '4. Remove direct imports from utils.context_helpers',
            '5. Test functionality with new manager integration'
        ]
    }

def log_deprecation_warning(function_name: str) -> None:
    """Log deprecation warning for legacy function usage"""
    logger.warning(
        f"⚠️ DEPRECATION WARNING: {function_name} is deprecated. "
        f"Use ContextPatternManager.{function_name}() instead. "
        f"See get_migration_info() for migration guidance."
    )

# ============================================================================
# EXPORT DECLARATIONS - Maintain backward compatibility
# ============================================================================

__all__ = [
    # Deprecated functions - maintained for backward compatibility
    'extract_context_signals',
    'detect_negation_context', 
    'analyze_sentiment_context',
    'process_sentiment_with_flip',
    'perform_enhanced_context_analysis',
    'score_term_in_context',
    
    # Migration helpers
    'get_migration_info',
    'log_deprecation_warning'
]

# ============================================================================
# MODULE INITIALIZATION - Log deprecation status
# ============================================================================

logger.warning("⚠️ DEPRECATED MODULE: utils.context_helpers compatibility layer loaded")
logger.info("📋 Migration info available via get_migration_info() function")
logger.info("🎯 Target: Use ContextPatternManager via dependency injection")