# ash-nlp/managers/context_pattern_manager.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
---
*****************  CORE SYSTEM VISION (Never to be violated):  *****************
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Context Pattern Manager for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-1
LAST MODIFIED: 2025-08-22
PHASE: 3e, Sub-step 5.4 - ContextPatternManager Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
CONSOLIDATION STATUS: Methods migrated to SharedUtilities + CrisisAnalyzer with references
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

SAFETY NOTICE: This manager provides context analysis for crisis detection patterns.
Context signals help determine the severity and urgency of mental health crisis situations.

MIGRATION REFERENCES (Phase 3e):
- validate_context_data() → SharedUtilitiesManager.validate_data_structure()
- log_context_performance() → SharedUtilitiesManager.log_performance_metric()  
- extract_context_signals() → CrisisAnalyzer.extract_context_signals()
- analyze_sentiment_context() → CrisisAnalyzer.analyze_sentiment_context()
- score_term_in_context() → CrisisAnalyzer.score_term_in_context()
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
    - Enhanced context analysis with crisis pattern integration
    - Negation detection for sentiment interpretation
    - Context signal processing for crisis detection
    - v3.1 JSON configuration compatibility with existing environment variables
    - Production-ready error handling and resilience
    
    This manager consolidates core context analysis functionality while delegating
    utility methods to SharedUtilitiesManager and analysis methods to CrisisAnalyzer
    for better architecture compliance and reduced duplication.
    
    Integration:
    - Works with PatternDetectionManager for enhanced pattern detection
    - Integrates with CrisisAnalyzer for comprehensive message analysis
    - Uses SharedUtilitiesManager for common utility functions
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
        
        logger.info("ContextPatternManager v3.1-3e-5.4-1 initialized successfully")

    def _load_configuration(self) -> None:
        """Load context patterns and analysis parameters from configuration"""
        logger.debug("📋 Loading Context Patterns and Analysis Parameters...")
        try:
            # Load context patterns configuration
            logger.debug("📋 Loading Context Patterns...")
            self.context_config = self.unified_config.get_patterns_crisis('patterns_context')
            if not self.context_config:
                logger.warning("⚠️ Context patterns configuration not found, using safe defaults")
                self.context_config = self._get_safe_context_defaults()
            else:
                logger.debug("✅ Context Patterns Loaded.")
            
            # Load analysis parameters using get_config_section
            try:
                logger.debug("📋 Loading Analysis Parameters...")
                self.analysis_params = self.unified_config.get_config_section('analysis_config')
                if not self.analysis_params:
                    logger.warning("⚠️ Analysis parameters not found, using safe defaults")
                    self.analysis_params = self._get_safe_analysis_defaults()
            except Exception as param_error:
                logger.warning(f"⚠️ Could not load analysis parameters: {param_error}")
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
    # MIGRATION REFERENCES - Phase 3e Consolidation
    # ========================================================================

    def _handle_deprecated_method(self, method_name: str, new_location: str, 
                                 additional_info: str = "") -> Dict[str, Any]:
        """
        Consolidated handler for deprecated methods moved during Phase 3e consolidation
        
        Args:
            method_name: Name of the deprecated method
            new_location: Where the method has been moved to
            additional_info: Additional context for the migration
            
        Returns:
            Dictionary with migration information and benefits
        """
        migration_info = {
            'status': 'moved',
            'original_method': method_name,
            'new_location': new_location,
            'migration_phase': 'Phase 3e - Manager Consolidation',
            'benefits': [
                'Eliminated code duplication across managers',
                'Centralized utility functions for better maintainability',
                'Improved architecture compliance with Clean v3.1',
                'Enhanced crisis detection through consolidated analysis'
            ],
            'usage_instruction': f'Use {new_location} instead of ContextPatternManager.{method_name}()',
            'additional_info': additional_info
        }
        
        logger.info(f"🔄 Method '{method_name}' has been moved to {new_location} (Phase 3e)")
        return migration_info

    def validate_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        """
        DEPRECATED: Moved to SharedUtilitiesManager.validate_data_structure()
        
        This method has been moved to SharedUtilitiesManager for better code organization.
        """
        return self._handle_deprecated_method(
            'validate_context_data',
            'SharedUtilitiesManager.validate_data_structure',
            'Context data validation is now handled by centralized validation utilities'
        )

    def log_context_performance(self, *args, **kwargs) -> Dict[str, Any]:
        """
        DEPRECATED: Moved to SharedUtilitiesManager.log_performance_metric()
        
        This method has been moved to SharedUtilitiesManager for better code organization.
        """
        return self._handle_deprecated_method(
            'log_context_performance',
            'SharedUtilitiesManager.log_performance_metric',
            'Performance logging is now handled by centralized logging utilities'
        )

    def extract_context_signals(self, *args, **kwargs) -> Dict[str, Any]:
        """
        DEPRECATED: Moved to CrisisAnalyzer.extract_context_signals()
        
        This method has been moved to CrisisAnalyzer for enhanced crisis detection capabilities.
        """
        return self._handle_deprecated_method(
            'extract_context_signals',
            'CrisisAnalyzer.extract_context_signals',
            'Context signal extraction is now part of the enhanced crisis analysis system'
        )

    def analyze_sentiment_context(self, *args, **kwargs) -> Dict[str, Any]:
        """
        DEPRECATED: Moved to CrisisAnalyzer.analyze_sentiment_context()
        
        This method has been moved to CrisisAnalyzer for enhanced crisis detection capabilities.
        """
        return self._handle_deprecated_method(
            'analyze_sentiment_context',
            'CrisisAnalyzer.analyze_sentiment_context',
            'Sentiment context analysis is now integrated with crisis detection algorithms'
        )

    def score_term_in_context(self, *args, **kwargs) -> Dict[str, Any]:
        """
        DEPRECATED: Moved to CrisisAnalyzer.score_term_in_context()
        
        This method has been moved to CrisisAnalyzer for enhanced crisis detection capabilities.
        """
        return self._handle_deprecated_method(
            'score_term_in_context',
            'CrisisAnalyzer.score_term_in_context',
            'Term scoring in context is now optimized for crisis detection scenarios'
        )

    # ========================================================================
    # CORE CONTEXT ANALYSIS METHODS - Enhanced and Crisis-Specific
    # ========================================================================

    def detect_negation_context(self, message: str) -> bool:
        """
        Detect if the message contains negation that might affect crisis interpretation
        
        Args:
            message: Message text to analyze
            
        Returns:
            True if negation patterns detected, False otherwise
        """
        message_lower = message.lower().strip()
        
        for pattern in self.basic_negation_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False

    def process_sentiment_with_flip(self, message: str, sentiment_score: float) -> Dict[str, Any]:
        """
        Process sentiment with potential polarity flipping based on context
        
        Args:
            message: Message text to analyze
            sentiment_score: Original sentiment score
            
        Returns:
            Dictionary with processed sentiment results
            
        Note: Uses CrisisAnalyzer.analyze_sentiment_context() for enhanced analysis
        """
        # This method now delegates to CrisisAnalyzer for enhanced context analysis
        processed_sentiment = {
            'original_score': sentiment_score,
            'final_score': sentiment_score,
            'flip_applied': False,
            'context_analysis': {
                'negation_detected': self.detect_negation_context(message),
                'note': 'Enhanced analysis available via CrisisAnalyzer.analyze_sentiment_context()'
            }
        }
        
        # Apply basic sentiment flip if negation detected and score is significant
        if processed_sentiment['context_analysis']['negation_detected'] and abs(sentiment_score) > 0.1:
            processed_sentiment['final_score'] = -sentiment_score
            processed_sentiment['flip_applied'] = True
            logger.debug(f"Basic sentiment flip applied: {sentiment_score} → {-sentiment_score}")
        
        return processed_sentiment

    def perform_enhanced_context_analysis(self, message: str, pattern_detection_manager=None) -> Dict[str, Any]:
        """
        Perform enhanced context analysis with optional crisis pattern integration
        
        Args:
            message: Message text to analyze  
            pattern_detection_manager: Optional PatternDetectionManager for enhanced analysis
            
        Returns:
            Enhanced context analysis results
        """
        
        # Basic context information
        context = {
            'message_length': len(message),
            'word_count': len(message.split()),
            'has_question_mark': '?' in message,
            'has_exclamation': '!' in message,
            'has_capitalization': any(c.isupper() for c in message),
            'negation_context': self.detect_negation_context(message),
            'temporal_indicators': self._extract_basic_temporal_indicators(message.lower()),
        }
        
        if pattern_detection_manager:
            try:
                # Get enhanced pattern analysis from PatternDetectionManager
                temporal_analysis = pattern_detection_manager.analyze_temporal_indicators(message)
                
                # Merge advanced analysis into context
                context.update({
                    'crisis_context_available': True,
                    'temporal_analysis': temporal_analysis,
                    'pattern_manager_status': 'available'
                })
                
                logger.debug("Enhanced context analysis completed with PatternDetectionManager")
                
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
            logger.debug("Basic context analysis only - PatternDetectionManager not available")
        
        return context

    # ========================================================================
    # CONFIGURATION HELPERS - Using existing .env.template variables
    # ========================================================================

    def _get_context_window(self) -> int:
        """Get context window size from configuration"""
        try:
            value = self.unified_config.get_config_section('analysis_config', 'semantic_analysis.context_window', 3)
            return int(value) if value is not None else 3
        except Exception as e:
            logger.warning(f"⚠️ Error getting context window: {e}, using default: 3")
            return 3

    def _get_context_boost_weight(self) -> float:
        """Get context boost weight from configuration"""
        try:
            value = self.unified_config.get_config_section('analysis_config', 'semantic_analysis.context_boost_weight', 1.5)
            return float(value) if value is not None else 1.5
        except Exception as e:
            logger.warning(f"⚠️ Error getting context boost weight: {e}, using default: 1.5")
            return 1.5

    def _get_negative_threshold(self) -> float:
        """Get negative sentiment threshold from configuration"""
        try:
            value = self.unified_config.get_config_section('analysis_config', 'semantic_analysis.negative_threshold', 0.6)
            return float(value) if value is not None else 0.6
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
            'manager_version': 'v3.1-3e-5.4-1',
            'phase': 'Phase 3e Sub-step 5.4 - Cleanup Complete',
            'initialization_time': self.initialization_time,
            'configuration_loaded': bool(self.context_config),
            'analysis_params_loaded': bool(self.analysis_params),
            'context_window': self._get_context_window(),
            'context_boost_weight': self._get_context_boost_weight(),
            'negative_threshold': self._get_negative_threshold(),
            'patterns_available': len(self.basic_negation_patterns),
            'migrated_methods': [
                'validate_context_data → SharedUtilitiesManager.validate_data_structure',
                'log_context_performance → SharedUtilitiesManager.log_performance_metric',
                'extract_context_signals → CrisisAnalyzer.extract_context_signals',
                'analyze_sentiment_context → CrisisAnalyzer.analyze_sentiment_context',
                'score_term_in_context → CrisisAnalyzer.score_term_in_context'
            ]
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