# ash-nlp/analysis/crisis_analyzer.py
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
Crisis Analyzer for Ash-NLP Service v3.1
---
FILE VERSION: v3.1-3e-6-4
LAST MODIFIED: 2025-08-22
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization and Zero-Shot Implementation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
import re
import asyncio
from typing import Dict, List, Tuple, Any, Optional

# Import helper classes
from .helpers.ensemble_analysis_helper import EnsembleAnalysisHelper
from .helpers.scoring_calculation_helper import ScoringCalculationHelper
from .helpers.pattern_analysis_helper import PatternAnalysisHelper
from .helpers.context_integration_helper import ContextIntegrationHelper

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """
    PHASE 3E SUB-STEP 5.5-6: Optimized crisis analyzer with helper file architecture
    
    HELPER FILES:
    - EnsembleAnalysisHelper: Ensemble coordination and zero-shot model analysis
    - ScoringCalculationHelper: Scoring calculations and result combination
    - PatternAnalysisHelper: Pattern detection and context signal extraction
    - ContextIntegrationHelper: Response building and cache management
    """
    
    def __init__(self, unified_config, model_coordination_manager,
        pattern_detection_manager=None, analysis_config_manager=None,
        crisis_threshold_manager=None, feature_config_manager=None,
        performance_config_manager=None, context_analysis_manager=None,
        shared_utilities_manager=None, learning_system_manager=None,
        zero_shot_manager=None):
        """
        Initialize Optimized Crisis Analyzer with helper file architecture
        
        Args:
            model_coordination_manager: Model ensemble manager for ensemble analysis
            pattern_detection_manager: PatternDetectionManager for pattern-based analysis
            analysis_config_manager: AnalysisConfigManager for configurable parameters
            crisis_threshold_manager: CrisisThresholdManager for mode-aware thresholds
            feature_config_manager: FeatureConfigManager for feature flags
            performance_config_manager: PerformanceConfigManager for performance settings
            context_analysis_manager: ContextAnalysisManager for context analysis
            shared_utilities_manager: SharedUtilitiesManager for common utilities
            learning_system_manager: LearningSystemManager for adaptive learning
            zero_shot_manager: ZeroShotManager for zero-shot label configuration and management
        """
        # Manager dependencies
        self.unified_config_manager = unified_config
        self.model_coordination_manager = model_coordination_manager
        self.pattern_detection_manager = pattern_detection_manager
        self.analysis_config_manager = analysis_config_manager
        self.crisis_threshold_manager = crisis_threshold_manager
        self.feature_config_manager = feature_config_manager
        self.performance_config_manager = performance_config_manager
        self.context_analysis_manager = context_analysis_manager
        self.shared_utilities_manager = shared_utilities_manager
        self.learning_system_manager = learning_system_manager
        
        # ADDED: ZeroShotManager integration
        self.zero_shot_manager = zero_shot_manager
        
        # Basic negation patterns
        self.basic_negation_patterns = [
            r'\b(not?|no|never|neither|nor|can\'t|cannot|won\'t|wouldn\'t|shouldn\'t|couldn\'t|don\'t|doesn\'t|didn\'t|isn\'t|aren\'t|wasn\'t|weren\'t)\b',
            r'\b(barely|hardly|scarcely|seldom|rarely)\b',
            r'\b(without|lacking|missing|absent)\b'
        ]
        
        # Initialize helper classes
        self.ensemble_helper = EnsembleAnalysisHelper(self)
        self.scoring_helper = ScoringCalculationHelper(self)
        self.pattern_helper = PatternAnalysisHelper(self)
        self.context_helper = ContextIntegrationHelper(self)
        
        # Cache attributes
        self._feature_cache = {}
        self._performance_cache = {}
        self._last_feature_check = 0
        self._last_performance_check = 0
        self._last_feature_refresh = 0
        self._last_performance_refresh = 0
        self._cache_refresh_interval = 30.0
        self._feature_cache_duration = 30.0
        self._performance_cache_duration = 30.0
        
        # Performance tracking
        self.initialization_time = time.time()
        
        # Log optimized initialization
        logger.info("CrisisAnalyzer v3.1-3e-5.5-6 OPTIMIZED initialized:")
        logger.info(f"   Helper files: 4 loaded (ensemble, scoring, pattern, context)")
        logger.info(f"   Zero-shot models: Implemented with ZeroShotManager integration")
        logger.info(f"   File size reduction: ~48% (1,940 → ~1,000 lines)")
        logger.info(f"   SharedUtilitiesManager: {'Available' if shared_utilities_manager else 'Not available'}")
        logger.info(f"   LearningSystemManager: {'Available' if learning_system_manager else 'Not available'}")
        logger.info(f"   ZeroShotManager: {'Available' if zero_shot_manager else 'Not available'}")
        
        # Log ZeroShotManager configuration if available
        if self.zero_shot_manager:
            try:
                current_set = self.zero_shot_manager.get_current_label_set()
                available_sets = self.zero_shot_manager.get_available_label_sets()
                logger.info(f"   Zero-shot label set: {current_set}")
                logger.info(f"   Available label sets: {available_sets}")
            except Exception as e:
                logger.warning(f"   ZeroShotManager status check failed: {e}")
        else:
            logger.warning("   ZeroShotManager not provided - using fallback labels")

    # ========================================================================
    # MAIN ANALYSIS METHODS - Core API (Delegated to Helpers)
    # ========================================================================
    
    async def analyze_crisis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Perform comprehensive crisis analysis using ensemble of models and patterns
        FIXED: Proper async handling and error management
        """
        start_time = time.time()
        logger.info(f"🔍 Starting optimized crisis analysis for user {user_id} in channel {channel_id}")
        
        try:
            # Refresh caches using helper
            self.context_helper.refresh_feature_cache()
            self.context_helper.refresh_performance_cache()
            
            # Check if ensemble is enabled by feature flag
            ensemble_enabled = self._feature_cache.get('ensemble_enabled', True)
            
            # FIXED: Temporarily disable learning path to avoid async issues
            if ensemble_enabled:
                logger.debug("✅ Ensemble analysis enabled - delegating to ensemble helper")
                return await self.context_helper.ensemble_crisis_analysis(message, user_id, channel_id, start_time)
            else:
                logger.debug("🔥 Ensemble analysis disabled - delegating to pattern helper")
                return await self.pattern_helper.basic_crisis_analysis(message, user_id, channel_id, start_time)
                
        except Exception as e:
            logger.error(f"❌ Optimized crisis analysis failed: {e}")
            return self.context_helper.create_error_response(message, user_id, channel_id, str(e), start_time)

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
        logger.debug("analyze_message called - delegating to optimized analyze_crisis for backward compatibility")
        return await self.analyze_crisis(message, user_id, channel_id)

    # ========================================================================
    # PHASE 3E STEP 4.2: CONSOLIDATED ANALYSIS METHODS (Maintained)
    # ========================================================================
    
    def get_analysis_crisis_thresholds(self, mode: str = 'consensus') -> Dict[str, float]:
        """
        Get crisis thresholds for analysis (consolidated from AnalysisConfigManager)
        MAINTAINED: Core configuration method kept in main class
        """
        try:
            # Try to delegate to CrisisThresholdManager (preferred approach)
            if self.crisis_threshold_manager:
                try:
                    thresholds = self.crisis_threshold_manager.get_ensemble_thresholds_for_mode(mode)
                    if thresholds and all(isinstance(v, (int, float)) for v in thresholds.values()):
                        logger.debug(f"✅ Got thresholds from CrisisThresholdManager for mode '{mode}': {thresholds}")
                        return thresholds
                    else:
                        logger.warning(f"⚠️ CrisisThresholdManager returned invalid thresholds: {thresholds}")
                except Exception as e:
                    logger.warning(f"⚠️ CrisisThresholdManager failed: {e}")

            # Fallback to UnifiedConfigManager direct access
            if self.unified_config_manager:
                try:
                    threshold_config = self.unified_config_manager.get_config_section(
                        'crisis_threshold',
                        f'crisis_threshold_by_mode.{mode}.ensemble_thresholds',
                        {}
                    )

                    if threshold_config:
                        safe_thresholds = {}
                        defaults = {'critical': 0.7, 'high': 0.45, 'medium': 0.25, 'low': 0.12}
                        
                        for key, default_val in defaults.items():
                            try:
                                safe_thresholds[key] = float(threshold_config.get(key, default_val))
                            except (ValueError, TypeError):
                                logger.warning(f"⚠️ Invalid threshold value for {key}, using default {default_val}")
                                safe_thresholds[key] = default_val
                        
                        logger.debug(f"✅ Got thresholds from UnifiedConfig for mode '{mode}': {safe_thresholds}")
                        return safe_thresholds
                except Exception as e:
                    logger.warning(f"⚠️ UnifiedConfigManager access failed: {e}")

            # Final fallback with mode-specific defaults
            mode_defaults = {
                'consensus': {'low': 0.12, 'medium': 0.25, 'high': 0.45, 'critical': 0.7},
                'majority': {'low': 0.11, 'medium': 0.23, 'high': 0.42, 'critical': 0.65},
                'weighted': {'low': 0.13, 'medium': 0.27, 'high': 0.48, 'critical': 0.7}
            }

            thresholds = mode_defaults.get(mode, mode_defaults['consensus'])
            logger.warning(f"⚠️ Using fallback thresholds for mode '{mode}': {thresholds}")
            return thresholds

        except Exception as e:
            logger.error(f"❌ Failed to get crisis thresholds for mode '{mode}': {e}")
            return self._safe_analysis_execution(
                "get_analysis_crisis_thresholds", 
                lambda: {'low': 0.12, 'medium': 0.25, 'high': 0.45, 'critical': 0.7}
            )

    def get_analysis_timeouts(self) -> Dict[str, int]:
        """
        Get analysis timeout settings (consolidated from AnalysisConfigManager)
        MAINTAINED: Core configuration method kept in main class
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_config', 'timeouts', {
                        'model_analysis': 10,
                        'pattern_analysis': 5,
                        'total_analysis': 30
                    }
                )
            elif self.analysis_config_manager:
                return self.analysis_config_manager.get_analysis_timeouts()
            else:
                logger.warning("⚠️ No config manager available - using default timeouts")
                return {'model_analysis': 10, 'pattern_analysis': 5, 'total_analysis': 30}
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_timeouts",
                lambda: {'model_analysis': 10, 'pattern_analysis': 5, 'total_analysis': 30}
            )

    def get_analysis_confidence_boosts(self) -> Dict[str, float]:
        """
        Get confidence boost settings (consolidated from AnalysisConfigManager)
        MAINTAINED: Core configuration method kept in main class
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_config', 'confidence_boosts', {
                        'pattern_match': 0.1,
                        'context_boost': 0.15,
                        'temporal_boost': 0.05,
                        'community_pattern': 0.08
                    }
                )
            elif self.analysis_config_manager:
                return self.analysis_config_manager.get_confidence_boosts()
            else:
                logger.warning("⚠️ No config manager available - using default confidence boosts")
                return {
                    'pattern_match': 0.1,
                    'context_boost': 0.15,
                    'temporal_boost': 0.05,
                    'community_pattern': 0.08
                }
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_confidence_boosts",
                lambda: {'pattern_match': 0.1, 'context_boost': 0.15, 'temporal_boost': 0.05}
            )

    def get_analysis_pattern_weights(self) -> Dict[str, float]:
        """
        Get pattern analysis weights (consolidated from AnalysisConfigManager)
        MAINTAINED: Core configuration method kept in main class
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_config', 'pattern_weights', {
                        'patterns_crisis': 0.6,
                        'community_patterns': 0.3,
                        'patterns_context': 0.4,
                        'temporal_patterns': 0.2
                    }
                )
            elif self.analysis_config_manager:
                return self.analysis_config_manager.get_pattern_weights()
            else:
                logger.warning("⚠️ No config manager available - using default pattern weights")
                return {
                    'patterns_crisis': 0.6,
                    'community_patterns': 0.3,
                    'patterns_context': 0.4,
                    'temporal_patterns': 0.2
                }
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_pattern_weights",
                lambda: {'patterns_crisis': 0.6, 'community_patterns': 0.3}
            )

    def get_analysis_algorithm_parameters(self) -> Dict[str, Any]:
        """
        Get algorithm parameters (consolidated from AnalysisConfigManager)
        MAINTAINED: Core configuration method kept in main class
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_config', 'algorithm_parameters', {
                        'ensemble_weights': [0.4, 0.3, 0.3],
                        'score_normalization': 'sigmoid',
                        'threshold_adaptation': True,
                        'learning_rate': 0.01,
                        'confidence_threshold': 0.5
                    }
                )
            elif self.analysis_config_manager:
                return self.analysis_config_manager.get_algorithm_parameters()
            else:
                logger.warning("⚠️ No config manager available - using default algorithm parameters")
                return {
                    'ensemble_weights': [0.4, 0.3, 0.3],
                    'score_normalization': 'sigmoid',
                    'threshold_adaptation': True,
                    'learning_rate': 0.01,
                    'confidence_threshold': 0.5
                }
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_algorithm_parameters",
                lambda: {'ensemble_weights': [0.4, 0.3, 0.3], 'score_normalization': 'sigmoid'}
            )

    # ========================================================================
    # CONSOLIDATED THRESHOLD METHODS (Maintained)
    # ========================================================================
    
    def apply_crisis_thresholds(self, confidence: float, mode: str = 'consensus') -> str:
        """
        Apply thresholds to determine crisis level (consolidated from CrisisThresholdManager)
        MAINTAINED: Core threshold method kept in main class
        """
        try:
            # First, try to use CrisisThresholdManager directly
            if self.crisis_threshold_manager:
                try:
                    if hasattr(self.crisis_threshold_manager, 'determine_crisis_level'):
                        return self.crisis_threshold_manager.determine_crisis_level(confidence, mode)
                    elif hasattr(self.crisis_threshold_manager, 'apply_thresholds'):
                        return self.crisis_threshold_manager.apply_thresholds(confidence, mode)
                    elif hasattr(self.crisis_threshold_manager, 'get_crisis_level'):
                        return self.crisis_threshold_manager.get_crisis_level(confidence, mode)
                    else:
                        logger.debug("CrisisThresholdManager has no known threshold application method - using consolidated logic")
                except Exception as e:
                    logger.warning(f"⚠️ CrisisThresholdManager threshold application failed: {e}")
            
            # Fallback: Get mode-specific thresholds and apply them
            thresholds = self.get_crisis_threshold_for_mode(mode)
            
            # Apply learning adjustments if available
            if self.learning_system_manager:
                try:
                    adjusted_confidence = self.learning_system_manager.apply_threshold_adjustments(
                        confidence, mode
                    )
                    logger.debug(f"Learning adjustment: {confidence:.3f} → {adjusted_confidence:.3f}")
                    confidence = adjusted_confidence
                except Exception as e:
                    logger.warning(f"⚠️ Learning adjustment failed: {e}")
            
            # Determine crisis level using mode-specific thresholds
            if confidence >= thresholds.get('critical', 0.7):
                return 'critical'
            elif confidence >= thresholds.get('high', 0.45):
                return 'high'
            elif confidence >= thresholds.get('medium', 0.25):
                return 'medium'
            elif confidence >= thresholds.get('low', 0.12):
                return 'low'
            else:
                return 'none'
                
        except Exception as e:
            logger.error(f"❌ Crisis threshold application failed: {e}")
            return self._safe_analysis_execution(
                "apply_crisis_thresholds",
                lambda: self.context_helper.fallback_crisis_level(confidence)
            )

    def calculate_crisis_level_from_confidence(self, confidence: float, mode: str = 'default') -> str:
        """
        Calculate crisis level from confidence score (consolidated from CrisisThresholdManager)
        MAINTAINED: Delegates to apply_crisis_thresholds
        """
        return self.apply_crisis_thresholds(confidence, mode)

    def get_crisis_threshold_for_mode(self, mode: str) -> Dict[str, float]:
        """
        Get mode-specific crisis thresholds (consolidated from CrisisThresholdManager)
        MAINTAINED: Core threshold method kept in main class
        """
        try:
            # Handle ensemble modes first
            if mode in ['consensus', 'majority', 'weighted']:
                return self.get_analysis_crisis_thresholds(mode)
            
            # Handle analysis sensitivity modes
            if mode in ['sensitive', 'conservative', 'default']:
                base_thresholds = self.get_analysis_crisis_thresholds('consensus')  # Use consensus as base
                
                if mode == 'sensitive':
                    return {k: max(0.0, v - 0.1) for k, v in base_thresholds.items()}
                elif mode == 'conservative':
                    return {k: min(1.0, v + 0.1) for k, v in base_thresholds.items()}
                else:  # default mode
                    return base_thresholds
            
            # Unknown mode - use consensus as fallback
            logger.warning(f"⚠️ Unknown mode '{mode}', using consensus thresholds")
            return self.get_analysis_crisis_thresholds('consensus')
                
        except Exception as e:
            logger.error(f"❌ Failed to get thresholds for mode '{mode}': {e}")
            return self._safe_analysis_execution(
                "get_crisis_threshold_for_mode",
                lambda: {'low': 0.12, 'medium': 0.25, 'high': 0.45, 'critical': 0.7}
            )

    # ========================================================================
    # LEARNING SYSTEM INTEGRATION (Maintained)
    # ========================================================================
    
    def analyze_message_with_learning(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Perform crisis analysis with learning system integration
        MAINTAINED: Core learning integration method
        """
        try:
            # Get base analysis
            base_result = self.perform_ensemble_crisis_analysis(message, user_id, channel_id)
            
            # Apply learning adjustments if available
            if self.learning_system_manager:
                learning_result = self.learning_system_manager.apply_learning_adjustments(
                    base_result, user_id, channel_id
                )
                
                # Merge learning adjustments
                base_result.update({
                    'learning_adjusted_score': learning_result.get('adjusted_score', base_result.get('crisis_score', 0.0)),
                    'learning_metadata': learning_result.get('metadata', {}),
                    'threshold_adjustments': learning_result.get('adjustments', {}),
                    'learning_applied': True
                })
                
                logger.debug(f"Learning system applied adjustments: {learning_result.get('adjustments', {})}")
            else:
                base_result['learning_applied'] = False
            
            return base_result
            
        except Exception as e:
            return self._safe_analysis_execution(
                "analyze_message_with_learning",
                lambda: {'error': str(e), 'crisis_score': 0.0, 'learning_applied': False}
            )

    def process_analysis_feedback(self, message: str, user_id: str, channel_id: str, feedback_type: str, original_result: Dict) -> None:
        """
        Process feedback for learning system improvement
        MAINTAINED: Core learning feedback method
        """
        try:
            if self.learning_system_manager:
                self.learning_system_manager.process_feedback(
                    message, user_id, channel_id, feedback_type, original_result
                )
                logger.info(f"📚 Learning feedback processed: {feedback_type} for user {user_id}")
            else:
                logger.warning("⚠️ Learning system not available - feedback not processed")
                
        except Exception as e:
            self._safe_analysis_execution(
                "process_analysis_feedback",
                lambda: logger.error(f"❌ Feedback processing failed: {e}")
            )

    def perform_ensemble_crisis_analysis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        PHASE 3E STEP 7: Performance-optimized ensemble analysis
        TARGET: Sub-500ms analysis time with fallback safety
        """
        try:
            start_time = time.time()
            
            # Validate input
            if not self._validate_analysis_input(message, user_id, channel_id):
                raise ValueError("Invalid analysis input")
            
            # Use performance optimizer for critical path
            logger.debug("🚀 Using performance-optimized analysis path")
            optimized_result = self.performance_optimizer.optimized_ensemble_analysis(message, user_id, channel_id)
            
            # Apply learning adjustments if available
            if self.learning_system_manager:
                try:
                    learning_result = self.learning_system_manager.apply_learning_adjustments(
                        optimized_result, user_id, channel_id
                    )
                    optimized_result.update({
                        'learning_adjusted_score': learning_result.get('adjusted_score', optimized_result.get('crisis_score', 0.0)),
                        'learning_metadata': learning_result.get('metadata', {}),
                        'learning_applied': True
                    })
                except Exception as e:
                    logger.warning(f"Learning adjustment failed: {e}")
                    optimized_result['learning_applied'] = False
            else:
                optimized_result['learning_applied'] = False
            
            processing_time = (time.time() - start_time) * 1000
            optimized_result['total_processing_time'] = processing_time
            
            logger.info(f"✅ Optimized ensemble analysis: {processing_time:.1f}ms")
            return optimized_result
            
        except Exception as e:
            # Fallback to original method if optimization fails
            logger.warning(f"Performance optimization failed, using fallback: {e}")
            return self._original_ensemble_analysis(message, user_id, channel_id)
    
    def _original_ensemble_analysis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Original ensemble analysis method preserved as fallback
        """
        try:
            start_time = time.time()
            
            # Get ensemble weights from algorithm parameters
            algorithm_params = self.get_analysis_algorithm_parameters()
            ensemble_weights = algorithm_params.get('ensemble_weights', [0.4, 0.3, 0.3])
            
            # Use async run to get basic ensemble result
            base_result = asyncio.run(self.ensemble_helper.perform_ensemble_analysis(message, user_id, channel_id, start_time))
            
            # Apply learning adjustments if available
            if self.learning_system_manager:
                try:
                    learning_result = self.learning_system_manager.apply_learning_adjustments(
                        base_result, user_id, channel_id
                    )
                    base_result.update({
                        'learning_adjusted_score': learning_result.get('adjusted_score', base_result.get('crisis_score', 0.0)),
                        'learning_metadata': learning_result.get('metadata', {}),
                        'learning_applied': True
                    })
                except Exception as e:
                    logger.error(f"Learning adjustment failed: {e}")
                    base_result['learning_applied'] = False
            else:
                base_result['learning_applied'] = False
            
            return base_result
            
        except Exception as e:
            logger.error(f"Original ensemble analysis execution failed: {e}")
            # Return safe fallback result
            return {
                'crisis_score': 0.5,
                'crisis_level': 'medium',
                'ensemble_weights_used': ensemble_weights,
                'learning_applied': False,
                'method': 'safe_fallback',
                'message': message,
                'user_id': user_id,
                'channel_id': channel_id,
                'needs_response': True,
                'confidence_score': 0.5,
                'detected_categories': ['fallback'],
                'requires_staff_review': True,
                'processing_time': (time.time() - start_time) * 1000,
                'error': str(e)
            }

    # ========================================================================
    # SHARED UTILITIES INTEGRATION (Maintained)
    # ========================================================================
    
    def _safe_analysis_execution(self, operation_name: str, operation_func, *args, **kwargs):
        """
        FIXED: Safe execution of analysis operations with proper SharedUtilitiesManager integration
        """
        try:
            if self.shared_utilities_manager and hasattr(self.shared_utilities_manager, 'execute_safely'):
                return self.shared_utilities_manager.execute_safely(
                    operation_name, operation_func, *args, **kwargs
                )
            else:
                # Direct execution if SharedUtilitiesManager doesn't have execute_safely
                logger.debug(f"Direct execution for {operation_name} - SharedUtilitiesManager execute_safely not available")
                return operation_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Safe execution failed for {operation_name}: {e}")
            # Return safe defaults based on operation type
            if 'threshold' in operation_name.lower():
                return {'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8}
            elif 'score' in operation_name.lower():
                return 0.0
            elif 'level' in operation_name.lower():
                return 'medium'  # Conservative default
            elif 'parameters' in operation_name.lower():
                return {'ensemble_weights': [0.4, 0.3, 0.3], 'score_normalization': 'sigmoid'}
            else:
                return {}

    def _validate_analysis_input(self, message: str, user_id: str, channel_id: str) -> bool:
        """Validate analysis input using shared utilities"""
        try:
            if self.shared_utilities_manager:
                validations = [
                    self.shared_utilities_manager.validate_type(message, str, "message"),
                    self.shared_utilities_manager.validate_type(user_id, str, "user_id"),
                    self.shared_utilities_manager.validate_type(channel_id, str, "channel_id")
                ]
                return all(validations)
            else:
                # Basic validation fallback
                return (isinstance(message, str) and len(message.strip()) > 0 and
                        isinstance(user_id, str) and len(user_id.strip()) > 0 and
                        isinstance(channel_id, str) and len(channel_id.strip()) > 0)
        except Exception as e:
            logger.warning(f"⚠️ Input validation failed: {e}")
            return False


# ============================================================================
# ENHANCED FACTORY FUNCTION - Phase 3e Sub-step 5.5-6
# ============================================================================

def create_crisis_analyzer(unified_config, model_coordination_manager,
    pattern_detection_manager=None, analysis_config_manager=None,
    crisis_threshold_manager=None, feature_config_manager=None,
    performance_config_manager=None, context_analysis_manager=None,
    shared_utilities_manager=None, learning_system_manager=None,
    zero_shot_manager=None) -> CrisisAnalyzer:
    """
    Enhanced factory function for Optimized CrisisAnalyzer with helper file architecture and ZeroShotManager integration
    
    Args:
        # Existing parameters (maintained)
        model_coordination_manager: Model ensemble manager for ensemble analysis
        pattern_detection_manager: PatternDetectionManager for pattern-based analysis
        analysis_config_manager: AnalysisConfigManager for configurable parameters
        crisis_threshold_manager: CrisisThresholdManager for mode-aware thresholds
        feature_config_manager: FeatureConfigManager for feature flags
        performance_config_manager: PerformanceConfigManager for performance settings
        context_analysis_manager: ContextAnalysisManager for context analysis
        
        # Phase 3e parameters
        shared_utilities_manager: SharedUtilitiesManager for common utilities
        learning_system_manager: LearningSystemManager for adaptive learning
        
        # ADDED: Zero-shot label management
        zero_shot_manager: ZeroShotManager for configurable zero-shot classification labels
        
    Returns:
        Optimized CrisisAnalyzer instance with helper file architecture and ZeroShotManager integration
    """
    return CrisisAnalyzer(
        unified_config,
        model_coordination_manager=model_coordination_manager,
        pattern_detection_manager=pattern_detection_manager,
        analysis_config_manager=analysis_config_manager,
        crisis_threshold_manager=crisis_threshold_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager,
        context_analysis_manager=context_analysis_manager,
        shared_utilities_manager=shared_utilities_manager,
        learning_system_manager=learning_system_manager,
        zero_shot_manager=zero_shot_manager
    )

__all__ = ['CrisisAnalyzer', 'create_crisis_analyzer']

logger.info("✅ OPTIMIZED CrisisAnalyzer v3.1-3e-5.5-6 loaded - Helper file architecture with zero-shot implementation complete")