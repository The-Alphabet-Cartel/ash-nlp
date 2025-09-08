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
FILE VERSION: v3.1-4a-2-1
LAST MODIFIED: 2025-08-28
PHASE: 4a, Step 2 - Analysis Flow Verification & Tracking Enhancement
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
from .helpers.analysis_tracking_helper import create_analysis_tracking_helper
from .performance_optimizations import integrate_performance_optimizations

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """
    PHASE 4A STEP 2: Enhanced crisis analyzer with comprehensive analysis flow tracking
    
    HELPER FILES:
    - EnsembleAnalysisHelper: Ensemble coordination and zero-shot model analysis
    - ScoringCalculationHelper: Scoring calculations and result combination
    - PatternAnalysisHelper: Pattern detection and context signal extraction
    - ContextIntegrationHelper: Response building and cache management
    - AnalysisTrackingHelper: Phase 4a Step 2 analysis flow tracking (NEW)
    
    NEW FEATURES (Phase 4a Step 2):
    - Comprehensive step-by-step execution tracking
    - Zero-shot labels information in response
    - Performance metrics for each analysis step
    - Fallback scenario detection and reporting
    """
    
    def __init__(self, unified_config, model_coordination_manager,
        pattern_detection_manager=None, analysis_config_manager=None,
        crisis_threshold_manager=None, feature_config_manager=None,
        performance_config_manager=None, context_analysis_manager=None,
        shared_utilities_manager=None, learning_system_manager=None,
        zero_shot_manager=None):
        """
        Initialize Crisis Analyzer with Phase 4a Step 2 analysis flow tracking
        
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
        
        # PHASE 4A STEP 2: Initialize analysis tracking helper
        self.tracking_helper = create_analysis_tracking_helper(self)
        
        # PHASE 3E STEP 7: Performance optimization integration
        self.performance_optimizer = integrate_performance_optimizations(self)
        logger.info("Performance optimizations integrated - targeting 500ms analysis time")

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
        logger.info("CrisisAnalyzer v3.1-4a-2-1 ENHANCED initialized:")
        logger.info(f"   Helper files: 5 loaded (ensemble, scoring, pattern, context, tracking)")
        logger.info(f"   Zero-shot models: Implemented with ZeroShotManager integration")
        logger.info(f"   Analysis flow tracking: {'Enabled' if self.tracking_helper.enable_tracking else 'Disabled'}")
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
    # ENHANCED MAIN ANALYSIS METHODS - Phase 4a Step 2
    # ========================================================================
    async def analyze_crisis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
            """
            PHASE 4A STEP 2: Enhanced crisis analysis with comprehensive flow tracking
            
            This is the main entry point called by API endpoints.
            Now includes complete step-by-step execution tracking and verification.
            """
            # Initialize tracking
            tracking = self.tracking_helper.init_analysis_tracking(message, user_id, channel_id)
            
            # Check if tracking is actually enabled - if not, use optimized path with same ZeroShot analysis
            if not self.tracking_helper.enable_tracking:
                logger.debug("Tracking disabled - using ZeroShot analysis without detailed tracking")
                try:
                    # FIXED: Use the same ZeroShot analysis path for both tracking enabled/disabled
                    start_time = time.time()
                    
                    # Use the same execute_zero_shot_analysis method that tracking uses
                    optimized_result = await self.tracking_helper.execute_zero_shot_analysis(message, user_id, channel_id)
                    
                    # Apply crisis thresholds to the ZeroShot result
                    crisis_score = optimized_result.get('crisis_score', 0.0)
                    optimized_result['crisis_level'] = self.apply_crisis_thresholds(crisis_score)
                    optimized_result['needs_response'] = crisis_score >= 0.25
                    optimized_result['requires_staff_review'] = crisis_score >= 0.45
                    
                    # Apply learning if available
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
                    optimized_result['api_processing_time'] = processing_time
                    
                    # Add minimal tracking info only
                    return self.tracking_helper.finalize_tracking(tracking, optimized_result)
                    
                except Exception as e:
                    logger.error(f"ZeroShot analysis failed (tracking disabled): {e}")
                    # Return simple fallback without complex tracking
                    return {
                        "crisis_score": 0.5,
                        "crisis_level": "medium",
                        "confidence_score": 0.0,
                        "method": "emergency_fallback",
                        "needs_response": True,
                        "requires_staff_review": True,
                        "error": str(e),
                        "zero_shot_manager_used": False,
                        "analysis_execution_tracking": {
                            "tracking_enabled": False,
                            "total_processing_time_ms": (time.time() - time.time()) * 1000
                        }
                    }
            
            # Full tracking enabled - proceed with detailed tracking
            logger.info(f"Phase 4a Step 2: Starting comprehensive crisis analysis for user {user_id} in channel {channel_id}")
            
            try:
                # Refresh caches using helper
                self.context_helper.refresh_feature_cache()
                self.context_helper.refresh_performance_cache()
                
                # Check if ensemble is enabled by feature flag
                ensemble_enabled = self._feature_cache.get('ensemble_enabled', True)
                
                if ensemble_enabled:
                    logger.debug("Using performance-optimized analysis with tracking")
                    
                    # STEP 1: Zero-Shot AI Models (PRIMARY CLASSIFICATION)
                    self.tracking_helper.update_tracking_step(tracking, "step_1_zero_shot_ai", "started")
                    try:
                        ensemble_result = await self.tracking_helper.execute_zero_shot_analysis(message, user_id, channel_id)
                        self.tracking_helper.update_tracking_step(tracking, "step_1_zero_shot_ai", "completed", {
                            "method": ensemble_result.get("method", "unknown"),
                            "models_used": ensemble_result.get("models_used", []),
                            "individual_scores": ensemble_result.get("individual_results", {}),
                            "ensemble_confidence": ensemble_result.get("confidence_score", 0.0),
                            "ai_classification_successful": True,
                            "zero_shot_labels_info": ensemble_result.get("zero_shot_labels_info", {})
                        })
                        logger.debug("Step 1: Zero-shot AI analysis completed successfully")
                        
                    except Exception as e:
                        logger.warning(f"Step 1: Zero-shot AI analysis failed: {e}")
                        self.tracking_helper.update_tracking_step(tracking, "step_1_zero_shot_ai", "failed", error=e)
                        tracking["fallback_scenarios"]["ai_models_failed"] = True
                        ensemble_result = {"crisis_score": 0.0, "confidence_score": 0.0, "method": "ai_fallback"}
                    
                    # STEP 2: Pattern Enhancement (CONTEXTUAL ANALYSIS)
                    self.tracking_helper.update_tracking_step(tracking, "step_2_pattern_enhancement", "started")
                    try:
                        pattern_result = await self.tracking_helper.execute_pattern_enhancement(message, ensemble_result)
                        self.tracking_helper.update_tracking_step(tracking, "step_2_pattern_enhancement", "completed", {
                            "patterns_matched": pattern_result.get("patterns_found", []),
                            "pattern_categories": pattern_result.get("detected_categories", []),
                            "enhancement_applied": pattern_result.get("enhancement_applied", False),
                            "confidence_boost": pattern_result.get("confidence_boost", 0.0),
                            "pattern_analysis_successful": True
                        })
                        logger.debug("Step 2: Pattern enhancement completed successfully")
                        
                    except Exception as e:
                        logger.warning(f"Step 2: Pattern enhancement failed: {e}")
                        self.tracking_helper.update_tracking_step(tracking, "step_2_pattern_enhancement", "failed", error=e)
                        pattern_result = {"enhancement_applied": False}
                    
                    # STEP 3: Learning System Adjustments (ADAPTIVE LEARNING)
                    self.tracking_helper.update_tracking_step(tracking, "step_3_learning_adjustments", "started")
                    try:
                        if self.learning_system_manager:
                            learning_result = await self.tracking_helper.execute_learning_adjustments(ensemble_result, pattern_result, user_id, channel_id)
                            self.tracking_helper.update_tracking_step(tracking, "step_3_learning_adjustments", "completed", {
                                "threshold_adjustments": learning_result.get("adjustments", {}),
                                "confidence_modifications": learning_result.get("confidence_delta", 0.0),
                                "learning_metadata": learning_result.get("metadata", {}),
                                "learning_applied": True
                            })
                            logger.debug("Step 3: Learning adjustments applied successfully")
                        else:
                            self.tracking_helper.update_tracking_step(tracking, "step_3_learning_adjustments", "completed", {
                                "learning_applied": False,
                                "reason": "LearningSystemManager not available"
                            })
                            logger.debug("Step 3: Learning system not available - skipped")
                            learning_result = {"learning_applied": False}
                            
                    except Exception as e:
                        logger.warning(f"Step 3: Learning adjustments failed: {e}")
                        self.tracking_helper.update_tracking_step(tracking, "step_3_learning_adjustments", "failed", error=e)
                        learning_result = {"learning_applied": False}
                    
                    # Combine results
                    final_result = self.tracking_helper.combine_analysis_results(ensemble_result, pattern_result, learning_result)
                    
                    # Mark performance optimization
                    if "performance_metrics" in tracking:
                        tracking["performance_metrics"]["optimization_applied"] = True
                    
                else:
                    logger.debug("Ensemble analysis disabled - using pattern-only fallback")
                    if "fallback_scenarios" in tracking:
                        tracking["fallback_scenarios"]["pattern_only_used"] = True
                    
                    # Pattern-only analysis
                    self.tracking_helper.update_tracking_step(tracking, "step_2_pattern_enhancement", "started")
                    try:
                        final_result = await self.pattern_helper.basic_crisis_analysis(message, user_id, channel_id, time.time())
                        self.tracking_helper.update_tracking_step(tracking, "step_2_pattern_enhancement", "completed", {
                            "method": "pattern_only_fallback",
                            "patterns_analysis_successful": True
                        })
                    except Exception as e:
                        self.tracking_helper.update_tracking_step(tracking, "step_2_pattern_enhancement", "failed", error=e)
                        raise
                
                # Finalize tracking and add to result
                final_result = self.tracking_helper.finalize_tracking(tracking, final_result)
                
                total_time = final_result.get("tracking_summary", {}).get("total_processing_time_ms", 0)
                logger.info(f"Phase 4a Step 2: Crisis analysis completed in {total_time:.1f}ms")
                
                return final_result
                    
            except Exception as e:
                logger.error(f"Phase 4a Step 2: Crisis analysis failed: {e}")
                if "fallback_scenarios" in tracking:
                    tracking["fallback_scenarios"]["emergency_fallback"] = True
                
                # Emergency fallback with tracking
                emergency_result = {
                    "crisis_score": 0.5,
                    "crisis_level": "medium",
                    "confidence_score": 0.0,
                    "method": "emergency_fallback",
                    "needs_response": True,
                    "requires_staff_review": True,
                    "error": str(e),
                    "message": message,
                    "user_id": user_id,
                    "channel_id": channel_id,
                    "zero_shot_manager_used": False
                }
                
                return self.tracking_helper.finalize_tracking(tracking, emergency_result)

    async def analyze_message(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Backward compatibility method for analyze_message (calls analyze_crisis)
        
        Args:
            message: User message to analyze
            user_id: User identifier  
            channel_id: Channel identifier
            
        Returns:
            Dictionary containing crisis analysis results with tracking
        """
        logger.debug("analyze_message called - delegating to enhanced analyze_crisis for backward compatibility")
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
                        logger.debug(f"Got thresholds from CrisisThresholdManager for mode '{mode}': {thresholds}")
                        return thresholds
                    else:
                        logger.warning(f"CrisisThresholdManager returned invalid thresholds: {thresholds}")
                except Exception as e:
                    logger.warning(f"CrisisThresholdManager failed: {e}")

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
                                logger.warning(f"Invalid threshold value for {key}, using default {default_val}")
                                safe_thresholds[key] = default_val
                        
                        logger.debug(f"Got thresholds from UnifiedConfig for mode '{mode}': {safe_thresholds}")
                        return safe_thresholds
                except Exception as e:
                    logger.warning(f"UnifiedConfigManager access failed: {e}")

            # Final fallback with mode-specific defaults
            mode_defaults = {
                'consensus': {'low': 0.12, 'medium': 0.25, 'high': 0.45, 'critical': 0.7},
                'majority': {'low': 0.11, 'medium': 0.23, 'high': 0.42, 'critical': 0.65},
                'weighted': {'low': 0.13, 'medium': 0.27, 'high': 0.48, 'critical': 0.7}
            }

            thresholds = mode_defaults.get(mode, mode_defaults['consensus'])
            logger.warning(f"Using fallback thresholds for mode '{mode}': {thresholds}")
            return thresholds

        except Exception as e:
            logger.error(f"Failed to get crisis thresholds for mode '{mode}': {e}")
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
                logger.warning("No config manager available - using default timeouts")
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
                logger.warning("No config manager available - using default confidence boosts")
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
            if self.unified_config_manager:
                return self.unified_config_manager.get_config_section(
                    'analysis_config', 'pattern_weights', {
                        'patterns_crisis': 0.6,
                        'community_patterns': 0.3,
                        'patterns_context': 0.4,
                        'temporal_patterns': 0.2
                    }
                )
            else:
                logger.warning("No config manager available - using default pattern weights")
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
        
        ENHANCEMENT: Now checks performance optimizer cache FIRST for dynamically set weights
        This ensures weights set via /ensemble/set-weights endpoint are actually used
        """
        try:
            # PRIORITY 1: Check performance optimizer cache for dynamically set weights
            if (hasattr(self, 'performance_optimizer') and 
                self.performance_optimizer and 
                hasattr(self.performance_optimizer, '_cached_model_weights') and
                self.performance_optimizer._cached_model_weights):
                
                cached_weights = self.performance_optimizer._cached_model_weights
                cached_mode = getattr(self.performance_optimizer, '_cached_ensemble_mode', 'weighted')
                
                logger.debug(f"🎯 Using cached weights from performance optimizer: {cached_weights}")
                
                # Convert dict weights to list format [depression, sentiment, distress]
                weights_list = [
                    cached_weights.get('depression', 0.4),
                    cached_weights.get('sentiment', 0.3), 
                    cached_weights.get('emotional_distress', 0.3)
                ]
                
                # Return with cached weights prioritized
                return {
                    'ensemble_weights': weights_list,
                    'ensemble_mode': cached_mode,
                    'score_normalization': 'sigmoid',
                    'threshold_adaptation': True,
                    'learning_rate': 0.01,
                    'confidence_threshold': 0.25,
                    'weights_source': 'performance_optimizer_cache'
                }
            
            # PRIORITY 2: Fall back to configuration-based weights
            if self.shared_utilities_manager:
                config_params = self.shared_utilities_manager.get_config_section_safely(
                    'analysis_config', 'algorithm_parameters', {
                        'ensemble_weights': [0.4, 0.3, 0.3],
                        'score_normalization': 'sigmoid',
                        'threshold_adaptation': True,
                        'learning_rate': 0.01,
                        'confidence_threshold': 0.25
                    }
                )
                config_params['weights_source'] = 'configuration'
                return config_params
                
            elif self.analysis_config_manager:
                config_params = self.analysis_config_manager.get_algorithm_parameters()
                config_params['weights_source'] = 'analysis_config_manager'
                return config_params
                
            else:
                logger.warning("No config manager available - using default algorithm parameters")
                return {
                    'ensemble_weights': [0.4, 0.3, 0.3],
                    'score_normalization': 'sigmoid',
                    'threshold_adaptation': True,
                    'learning_rate': 0.01,
                    'confidence_threshold': 0.25,
                    'weights_source': 'fallback_defaults'
                }
                
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_algorithm_parameters",
                lambda: {
                    'ensemble_weights': [0.4, 0.3, 0.3], 
                    'score_normalization': 'sigmoid',
                    'weights_source': 'error_fallback'
                }
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
                    logger.warning(f"CrisisThresholdManager threshold application failed: {e}")
            
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
                    logger.warning(f"Learning adjustment failed: {e}")
            
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
            logger.error(f"Crisis threshold application failed: {e}")
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
            logger.warning(f"Unknown mode '{mode}', using consensus thresholds")
            return self.get_analysis_crisis_thresholds('consensus')
                
        except Exception as e:
            logger.error(f"Failed to get thresholds for mode '{mode}': {e}")
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
                logger.info(f"Learning feedback processed: {feedback_type} for user {user_id}")
            else:
                logger.warning("Learning system not available - feedback not processed")
                
        except Exception as e:
            self._safe_analysis_execution(
                "process_analysis_feedback",
                lambda: logger.error(f"Feedback processing failed: {e}")
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
            logger.debug("Using performance-optimized analysis path")
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
            
            logger.info(f"Optimized ensemble analysis: {processing_time:.1f}ms")
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
            logger.error(f"Safe execution failed for {operation_name}: {e}")
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
            logger.warning(f"Input validation failed: {e}")
            return False


# ============================================================================
# ENHANCED FACTORY FUNCTION - Phase 4a Step 2
# ============================================================================

def create_crisis_analyzer(unified_config, model_coordination_manager,
    pattern_detection_manager=None, analysis_config_manager=None,
    crisis_threshold_manager=None, feature_config_manager=None,
    performance_config_manager=None, context_analysis_manager=None,
    shared_utilities_manager=None, learning_system_manager=None,
    zero_shot_manager=None) -> CrisisAnalyzer:
    """
    Enhanced factory function for CrisisAnalyzer with Phase 4a Step 2 analysis flow tracking
    
    Args:
        # Existing parameters (maintained)
        model_coordination_manager: Model ensemble manager for ensemble analysis
        pattern_detection_manager: PatternDetectionManager for pattern-based analysis
        analysis_config_manager: AnalysisConfigManager for configurable parameters
        crisis_threshold_manager: CrisisThresholdManager for mode-aware thresholds
        feature_config_manager: FeatureConfigManager for feature flags
        performance_config_manager: PerformanceConfigManager for performance settings
        context_analysis_manager: ContextAnalysisManager for context analysis
        shared_utilities_manager: SharedUtilitiesManager for common utilities
        learning_system_manager: LearningSystemManager for adaptive learning
        zero_shot_manager: ZeroShotManager for configurable zero-shot classification labels
        
    Returns:
        Enhanced CrisisAnalyzer instance with comprehensive analysis flow tracking
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

logger.info("ENHANCED CrisisAnalyzer v3.1-4a-2-1 loaded - Comprehensive analysis flow tracking implemented")