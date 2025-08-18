# ash-nlp/analysis/crisis_analyzer.py
"""
Crisis Analyzer for Ash-NLP Service v3.1
FILE VERSION: v3.1-3e-4.2-7
LAST MODIFIED: 2025-08-18
PHASE: 3e, Step 4.2 - Enhanced CrisisAnalyzer with SharedUtilities and LearningSystem integration
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Phase 3e Step 4.2 - Analysis method consolidation with new dependencies
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
import re
import asyncio
from typing import Dict, List, Tuple, Any, Optional

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """
    PHASE 3E STEP 4.2: Enhanced crisis analyzer with consolidated analysis methods
    
    Previous Phases:
    - Phase 3a: Clean v3.1 architecture with JSON-based patterns
    - Phase 3b: Analysis parameters from AnalysisParametersManager  
    - Phase 3c: Mode-aware thresholds from ThresholdMappingManager
    - Phase 3d Step 7: Feature flags and performance settings from dedicated managers
    - Phase 3d Step 10.6: Consolidated scoring functions (no more utils/scoring_helpers.py)
    - Phase 3d Step 10.7: Consolidated community patterns (no more utils/community_patterns.py)
    - Phase 3d Step 10.8: ContextPatternManager integration (no more utils/context_helpers.py)
    
    Phase 3e Enhancements:
    - Step 4.2: SharedUtilitiesManager and LearningSystemManager integration
    - Consolidated analysis methods from AnalysisParameters, ThresholdMapping, ModelEnsemble managers
    - Enhanced error handling using SharedUtilities patterns
    - Learning system integration for adaptive analysis
    """
    
    def __init__(self, unified_config, model_ensemble_manager,
                crisis_pattern_manager=None, analysis_parameters_manager=None,
                threshold_mapping_manager=None, feature_config_manager=None,
                performance_config_manager=None, context_pattern_manager=None,
                 # NEW Phase 3e dependencies
                 shared_utilities_manager=None, learning_system_manager=None):
        """
        Initialize Enhanced Crisis Analyzer with Phase 3e manager integration
        Updated for Step 4.2: SharedUtilities and LearningSystem integration
        
        Args:
            # Existing dependencies (maintained)
            model_ensemble_manager: Model ensemble manager for ensemble analysis
            crisis_pattern_manager: CrisisPatternManager for pattern-based analysis
            analysis_parameters_manager: AnalysisParametersManager for configurable parameters
            threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds
            feature_config_manager: FeatureConfigManager for feature flags
            performance_config_manager: PerformanceConfigManager for performance settings
            context_pattern_manager: ContextPatternManager for context analysis
            
            # NEW Phase 3e dependencies
            shared_utilities_manager: SharedUtilitiesManager for common utilities (Step 2)
            learning_system_manager: LearningSystemManager for adaptive learning (Step 3)
        """
        # Existing manager dependencies (maintained)
        self.unified_config_manager = unified_config
        self.model_ensemble_manager = model_ensemble_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.analysis_parameters_manager = analysis_parameters_manager
        self.threshold_mapping_manager = threshold_mapping_manager
        self.feature_config_manager = feature_config_manager
        self.performance_config_manager = performance_config_manager
        self.context_pattern_manager = context_pattern_manager
        
        # NEW Phase 3e manager dependencies
        self.shared_utilities_manager = shared_utilities_manager
        self.learning_system_manager = learning_system_manager
        
        # Initialize cache attributes (maintained from Phase 3d)
        self._feature_cache = {}
        self._performance_cache = {}
        
        # Cache timing attributes (maintained from Phase 3d)
        self._last_feature_check = 0
        self._last_performance_check = 0
        self._last_feature_refresh = 0
        self._last_performance_refresh = 0
        
        # Cache duration settings (maintained from Phase 3d)
        self._cache_refresh_interval = 30.0
        self._feature_cache_duration = 30.0
        self._performance_cache_duration = 30.0
        
        # Performance tracking
        self.initialization_time = time.time()
        
        # Log enhanced initialization
        logger.info("🚀 CrisisAnalyzer v3.1-3e-4.2-1 initialized with Phase 3e enhancements:")
        logger.info(f"   ✅ SharedUtilitiesManager: {'Available' if shared_utilities_manager else 'Not available'}")
        logger.info(f"   ✅ LearningSystemManager: {'Available' if learning_system_manager else 'Not available'}")
        logger.info("   ✅ Analysis method consolidation ready")

    # ========================================================================
    # PHASE 3E STEP 4.2: CONSOLIDATED ANALYSIS METHODS FROM ANALYSISPARAMETERSMANAGER
    # ========================================================================
    
    def get_analysis_crisis_thresholds(self, mode: str = 'majority') -> Dict[str, float]:
        """
        Get crisis thresholds for analysis (consolidated from AnalysisParametersManager)
        Updated for Phase 3d Step 10.10: Now delegates to ThresholdMappingManager for mode-specific thresholds
        
        Args:
            mode: Ensemble mode ('consensus', 'majority', 'weighted')
            
        Returns:
            Dictionary of crisis threshold settings for the specified mode
        """
        try:
            if self.unified_config_manager:
                # Try to get mode-specific thresholds from threshold_mapping config
                threshold_config = self.unified_config_manager.get_config_section(
                    'threshold_mapping', f'threshold_mapping_by_mode.{mode}.ensemble_thresholds', None
                )
                if threshold_config:
                    return {
                        'low': threshold_config.get('low', 0.12),
                        'medium': threshold_config.get('medium', 0.25),
                        'high': threshold_config.get('high', 0.45),
                        'critical': threshold_config.get('critical', 0.7)
                    }
            
            # Final fallback: Mode-specific defaults based on Phase 3d configuration
            mode_defaults = {
                'consensus': {'low': 0.12, 'medium': 0.30, 'high': 0.50, 'critical': 0.7},
                'majority': {'low': 0.11, 'medium': 0.28, 'high': 0.45, 'critical': 0.65},
                'weighted': {'low': 0.13, 'medium': 0.32, 'high': 0.55, 'critical': 0.75}
            }
            
            thresholds = mode_defaults.get(mode, mode_defaults[f'{mode}'])
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
        Get analysis timeout settings (consolidated from AnalysisParametersManager)
        
        Returns:
            Dictionary of timeout settings in seconds
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_parameters', 'timeouts', {
                        'model_analysis': 10,
                        'pattern_analysis': 5,
                        'total_analysis': 30
                    }
                )
            elif self.analysis_parameters_manager:
                # Fallback to legacy manager
                return self.analysis_parameters_manager.get_analysis_timeouts()
            else:
                logger.warning("⚠️ No config manager available - using default timeouts")
                return {
                    'model_analysis': 10,
                    'pattern_analysis': 5,
                    'total_analysis': 30
                }
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_timeouts",
                lambda: {'model_analysis': 10, 'pattern_analysis': 5, 'total_analysis': 30}
            )

    def get_analysis_confidence_boosts(self) -> Dict[str, float]:
        """
        Get confidence boost settings (consolidated from AnalysisParametersManager)
        
        Returns:
            Dictionary of confidence boost factors
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_parameters', 'confidence_boosts', {
                        'pattern_match': 0.1,
                        'context_boost': 0.15,
                        'temporal_boost': 0.05,
                        'community_pattern': 0.08
                    }
                )
            elif self.analysis_parameters_manager:
                # Fallback to legacy manager
                return self.analysis_parameters_manager.get_confidence_boosts()
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
        Get pattern analysis weights (consolidated from AnalysisParametersManager)
        
        Returns:
            Dictionary of pattern weight settings
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_parameters', 'pattern_weights', {
                        'crisis_patterns': 0.6,
                        'community_patterns': 0.3,
                        'context_patterns': 0.4,
                        'temporal_patterns': 0.2
                    }
                )
            elif self.analysis_parameters_manager:
                # Fallback to legacy manager
                return self.analysis_parameters_manager.get_pattern_weights()
            else:
                logger.warning("⚠️ No config manager available - using default pattern weights")
                return {
                    'crisis_patterns': 0.6,
                    'community_patterns': 0.3,
                    'context_patterns': 0.4,
                    'temporal_patterns': 0.2
                }
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_pattern_weights",
                lambda: {'crisis_patterns': 0.6, 'community_patterns': 0.3}
            )

    def get_analysis_algorithm_parameters(self) -> Dict[str, Any]:
        """
        Get algorithm parameters (consolidated from AnalysisParametersManager)
        
        Returns:
            Dictionary of algorithm configuration parameters
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_parameters', 'algorithm_parameters', {
                        'ensemble_weights': [0.4, 0.3, 0.3],
                        'score_normalization': 'sigmoid',
                        'threshold_adaptation': True,
                        'learning_rate': 0.01,
                        'confidence_threshold': 0.5
                    }
                )
            elif self.analysis_parameters_manager:
                # Fallback to legacy manager
                return self.analysis_parameters_manager.get_algorithm_parameters()
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
    # PHASE 3E STEP 4.2: CONSOLIDATED ANALYSIS METHODS FROM THRESHOLDMAPPINGMANAGER
    # ========================================================================
    
    def apply_crisis_thresholds(self, confidence: float, mode: str = 'consensus') -> str:
        """
        Apply thresholds to determine crisis level (consolidated from ThresholdMappingManager)
        Updated for Phase 3d Step 10.10: Uses proper ensemble mode-specific thresholds
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
            mode: Analysis mode ('consensus', 'majority', 'weighted', 'sensitive', 'conservative')
            
        Returns:
            Crisis level string ('none', 'low', 'medium', 'high', 'critical')
        """
        try:
            # First, try to use ThresholdMappingManager directly (preferred approach)
            if self.threshold_mapping_manager:
                try:
                    # Try different possible method names for threshold application
                    if hasattr(self.threshold_mapping_manager, 'determine_crisis_level'):
                        return self.threshold_mapping_manager.determine_crisis_level(confidence, mode)
                    elif hasattr(self.threshold_mapping_manager, 'apply_thresholds'):
                        return self.threshold_mapping_manager.apply_thresholds(confidence, mode)
                    elif hasattr(self.threshold_mapping_manager, 'get_crisis_level'):
                        return self.threshold_mapping_manager.get_crisis_level(confidence, mode)
                    else:
                        logger.debug("ThresholdMappingManager has no known threshold application method - using consolidated logic")
                except Exception as e:
                    logger.warning(f"⚠️ ThresholdMappingManager threshold application failed: {e}")
            
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
                lambda: self._fallback_crisis_level(confidence)
            )

    def calculate_crisis_level_from_confidence(self, confidence: float, mode: str = 'default') -> str:
        """
        Calculate crisis level from confidence score (consolidated from ThresholdMappingManager)
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
            mode: Analysis mode for calculation
            
        Returns:
            Crisis level string
        """
        return self.apply_crisis_thresholds(confidence, mode)

    def validate_crisis_analysis_thresholds(self, mode: str = 'consensus') -> Dict[str, bool]:
        """
        Validate analysis thresholds (consolidated from ThresholdMappingManager)
        Updated for Phase 3d Step 10.10: Validates mode-specific thresholds
        
        Args:
            mode: Ensemble mode to validate ('consensus', 'majority', 'weighted')
            
        Returns:
            Dictionary of validation results
        """
        try:
            validation_results = {}
            
            # Validate crisis thresholds for specified mode
            crisis_thresholds = self.get_analysis_crisis_thresholds(mode)
            validation_results[f'{mode}_crisis_thresholds_valid'] = all(
                isinstance(v, (int, float)) and 0 <= v <= 1 
                for v in crisis_thresholds.values()
            )
            
            # Validate threshold ordering (low < medium < high < critical)
            thresholds_ordered = (
                crisis_thresholds.get('low', 0) <= 
                crisis_thresholds.get('medium', 0) <= 
                crisis_thresholds.get('high', 0) <= 
                crisis_thresholds.get('critical', 1)
            )
            validation_results[f'{mode}_thresholds_ordered'] = thresholds_ordered
            
            # Validate confidence boosts
            confidence_boosts = self.get_analysis_confidence_boosts()
            validation_results['confidence_boosts_valid'] = all(
                isinstance(v, (int, float)) and -1 <= v <= 1 
                for v in confidence_boosts.values()
            )
            
            # Validate pattern weights
            pattern_weights = self.get_analysis_pattern_weights()
            validation_results['pattern_weights_valid'] = all(
                isinstance(v, (int, float)) and 0 <= v <= 1 
                for v in pattern_weights.values()
            )
            
            # If ThresholdMappingManager available, use its validation
            if self.threshold_mapping_manager:
                try:
                    if hasattr(self.threshold_mapping_manager, 'validate_thresholds'):
                        manager_validation = self.threshold_mapping_manager.validate_thresholds(mode)
                        if isinstance(manager_validation, dict):
                            validation_results.update(manager_validation)
                    elif hasattr(self.threshold_mapping_manager, f'validate_{mode}_thresholds'):
                        method = getattr(self.threshold_mapping_manager, f'validate_{mode}_thresholds')
                        mode_validation = method()
                        if isinstance(mode_validation, dict):
                            validation_results.update(mode_validation)
                except Exception as e:
                    logger.warning(f"⚠️ ThresholdMappingManager validation failed: {e}")
            
            # Use shared utilities for validation logging if available
            if self.shared_utilities_manager:
                for key, value in validation_results.items():
                    if not value:
                        logger.warning(f"⚠️ Validation failed for {key} in mode {mode}")
            
            validation_results['overall_valid'] = all(validation_results.values())
            validation_results['mode_validated'] = mode
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Threshold validation failed for mode '{mode}': {e}")
            return self._safe_analysis_execution(
                "validate_crisis_analysis_thresholds",
                lambda: {'overall_valid': False, 'mode_validated': mode, 'error': str(e)}
            )

    def get_crisis_threshold_for_mode(self, mode: str) -> Dict[str, float]:
        """
        Get mode-specific crisis thresholds (consolidated from ThresholdMappingManager)
        Updated for Phase 3d Step 10.10: Uses proper ThresholdMappingManager delegation
        
        Args:
            mode: Analysis mode ('consensus', 'majority', 'weighted', 'sensitive', 'conservative')
            
        Returns:
            Dictionary of mode-specific thresholds
        """
        try:
            # Handle ensemble modes first (Phase 3d Step 10.10)
            if mode in ['consensus', 'majority', 'weighted']:
                return self.get_analysis_crisis_thresholds(mode)
            
            # Handle analysis sensitivity modes (legacy behavior)
            if mode in ['sensitive', 'conservative', 'default']:
                base_thresholds = self.get_analysis_crisis_thresholds('consensus')  # Use consensus as base
                
                if mode == 'sensitive':
                    # Lower thresholds for more sensitive detection
                    return {k: max(0.0, v - 0.1) for k, v in base_thresholds.items()}
                elif mode == 'conservative':
                    # Higher thresholds for more conservative detection
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
    # PHASE 3E STEP 4.2: CONSOLIDATED ANALYSIS METHODS FROM MODELENSEMBLEMANAGER
    # ========================================================================
    
    def perform_ensemble_crisis_analysis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Enhanced ensemble analysis with learning integration (consolidated from ModelEnsembleManager)
        
        Args:
            message: Message to analyze
            user_id: User identifier
            channel_id: Channel identifier
            
        Returns:
            Enhanced ensemble analysis results
        """
        try:
            start_time = time.time()
            
            # Validate input using shared utilities
            if not self._validate_analysis_input(message, user_id, channel_id):
                raise ValueError("Invalid analysis input")
            
            # Get ensemble weights from algorithm parameters
            algorithm_params = self.get_analysis_algorithm_parameters()
            ensemble_weights = algorithm_params.get('ensemble_weights', [0.4, 0.3, 0.3])
            
            # Perform individual model analyses
            model_results = []
            if self.model_ensemble_manager:
                # Delegate to ModelEnsembleManager for individual model calls
                # This maintains the coordination pattern while enhancing with consolidated logic
                base_result = self.model_ensemble_manager.analyze_message_with_ensemble(
                    message, user_id, channel_id
                )
                model_results = base_result.get('model_results', [])
            
            # Combine results using consolidated logic
            combined_result = self.combine_ensemble_model_results(model_results)
            
            # Apply ensemble weights
            weighted_result = self.apply_analysis_ensemble_weights(combined_result, ensemble_weights)
            
            # Apply learning adjustments if available
            if self.learning_system_manager:
                learning_adjusted = self.learning_system_manager.apply_learning_adjustments(
                    weighted_result, user_id, channel_id
                )
                weighted_result.update(learning_adjusted)
            
            # Add metadata
            weighted_result['analysis_metadata'] = {
                'processing_time': time.time() - start_time,
                'ensemble_weights_used': ensemble_weights,
                'learning_applied': bool(self.learning_system_manager),
                'consolidation_method': 'enhanced_ensemble'
            }
            
            return weighted_result
            
        except Exception as e:
            return self._safe_analysis_execution(
                "perform_ensemble_crisis_analysis",
                lambda: {'error': str(e), 'crisis_score': 0.0, 'crisis_level': 'error'}
            )

    def combine_ensemble_model_results(self, model_results: List[Dict]) -> Dict[str, Any]:
        """
        Combine multiple model results (consolidated from ModelEnsembleManager)
        
        Args:
            model_results: List of individual model analysis results
            
        Returns:
            Combined analysis results
        """
        try:
            if not model_results:
                return {'crisis_score': 0.0, 'confidence': 0.0, 'model_count': 0}
            
            # Extract scores and confidences
            scores = []
            confidences = []
            categories = set()
            
            for result in model_results:
                if isinstance(result, dict):
                    scores.append(result.get('score', 0.0))
                    confidences.append(result.get('confidence', 0.0))
                    if 'categories' in result:
                        categories.update(result['categories'])
            
            # Calculate combined metrics
            combined_score = sum(scores) / len(scores) if scores else 0.0
            combined_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            # Apply confidence boost if high agreement
            if len(set(scores)) == 1:  # All models agree
                boost = self.get_analysis_confidence_boosts().get('pattern_match', 0.1)
                combined_score = min(1.0, combined_score + boost)
                logger.debug(f"Model agreement boost applied: +{boost}")
            
            return {
                'crisis_score': combined_score,
                'confidence': combined_confidence,
                'model_count': len(model_results),
                'individual_scores': scores,
                'detected_categories': list(categories),
                'agreement_level': len(set(scores)) / len(scores) if scores else 0.0
            }
            
        except Exception as e:
            return self._safe_analysis_execution(
                "combine_ensemble_model_results",
                lambda: {'crisis_score': 0.0, 'confidence': 0.0, 'model_count': 0, 'error': str(e)}
            )

    def apply_analysis_ensemble_weights(self, results: Dict, weights: List[float] = None) -> Dict[str, Any]:
        """
        Apply ensemble weights to analysis results (consolidated from ModelEnsembleManager)
        
        Args:
            results: Combined analysis results
            weights: Optional custom weights (uses algorithm parameters if None)
            
        Returns:
            Weighted analysis results
        """
        try:
            if weights is None:
                algorithm_params = self.get_analysis_algorithm_parameters()
                weights = algorithm_params.get('ensemble_weights', [0.4, 0.3, 0.3])
            
            individual_scores = results.get('individual_scores', [])
            if not individual_scores or len(individual_scores) != len(weights):
                logger.warning("⚠️ Score/weight mismatch - using equal weighting")
                weights = [1.0 / len(individual_scores)] * len(individual_scores) if individual_scores else [1.0]
            
            # Apply weighted combination
            weighted_score = sum(score * weight for score, weight in zip(individual_scores, weights))
            
            # Update results
            updated_results = results.copy()
            updated_results['weighted_crisis_score'] = weighted_score
            updated_results['weights_applied'] = weights
            updated_results['weighting_method'] = 'ensemble_weighted'
            
            return updated_results
            
        except Exception as e:
            return self._safe_analysis_execution(
                "apply_analysis_ensemble_weights",
                lambda: {**results, 'weighted_crisis_score': results.get('crisis_score', 0.0)}
            )

    # ========================================================================
    # PHASE 3E STEP 4.2: LEARNING SYSTEM INTEGRATION
    # ========================================================================
    
    def analyze_message_with_learning(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Perform crisis analysis with learning system integration
        
        Args:
            message: Message to analyze
            user_id: User identifier
            channel_id: Channel identifier
            
        Returns:
            Analysis results with learning enhancements
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

    def process_analysis_feedback(self, message: str, user_id: str, channel_id: str, 
                                feedback_type: str, original_result: Dict) -> None:
        """
        Process feedback for learning system improvement
        
        Args:
            message: Original message
            user_id: User identifier
            channel_id: Channel identifier
            feedback_type: 'false_positive', 'false_negative', 'correct'
            original_result: Original analysis result for learning
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

    # ========================================================================
    # PHASE 3E STEP 4.2: SHARED UTILITIES INTEGRATION
    # ========================================================================
    
    def _safe_analysis_execution(self, operation_name: str, operation_func, *args, **kwargs):
        """Safe execution of analysis operations using SharedUtilitiesManager"""
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.execute_safely(
                    operation_name, operation_func, *args, **kwargs
                )
            else:
                # Fallback execution without shared utilities
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

    def _get_analysis_setting(self, section: str, key: str, default: Any = None):
        """Standardized configuration access using SharedUtilitiesManager"""
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(section, key, default)
            else:
                logger.warning(f"⚠️ SharedUtilitiesManager not available for {section}.{key}")
                return default
        except Exception as e:
            logger.error(f"❌ Configuration access failed for {section}.{key}: {e}")
            return default

    def _fallback_crisis_level(self, confidence: float) -> str:
        """Fallback crisis level determination"""
        if confidence >= 0.7:
            return 'critical'
        elif confidence >= 0.5:
            return 'high'
        elif confidence >= 0.3:
            return 'medium'
        elif confidence >= 0.1:
            return 'low'
        else:
            return 'none'

    # ========================================================================
    # EXISTING METHODS (maintained from Phase 3d Step 10.8)
    # ========================================================================
    
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
                        'enhanced_learning': bool(self.learning_system_manager),  # Updated for Phase 3e
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
                    'enhanced_learning': bool(self.learning_system_manager),  # Updated for Phase 3e
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
            'needs_response': True,  # Conservative - assume crisis on error
            'crisis_level': 'high',  # Conservative - assume high crisis on error
            'confidence_score': 0.0,  # Add missing field
            'detected_categories': ['error'],  # Add missing field
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
                    'analysis_version': 'v3.1-3e-4.2-1',
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
            'needs_response': True,  # Conservative - assume crisis on timeout
            'crisis_level': 'medium',  # Conservative - assume medium crisis on timeout
            'confidence_score': 0.5,  # Add missing field
            'detected_categories': ['timeout'],  # Add missing field
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
                    'analysis_version': 'v3.1-3e-4.2-1',
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
        Updated for Phase 3e Step 4.2: Enhanced with consolidated methods and learning integration
        
        Args:
            message: User message to analyze
            user_id: User identifier  
            channel_id: Channel identifier
            
        Returns:
            Dictionary containing crisis analysis results
        """
        start_time = time.time()
        logger.info(f"🔍 Starting enhanced crisis analysis for user {user_id} in channel {channel_id}")
        
        # Refresh caches
        self._refresh_feature_cache()
        self._refresh_performance_cache()
        
        try:
            # Check if ensemble is enabled by feature flag
            ensemble_enabled = self._feature_cache.get('ensemble_enabled', True)
            
            # Use enhanced learning analysis if available
            if self.learning_system_manager and self._feature_cache.get('enhanced_learning', False):
                logger.debug("✅ Enhanced learning analysis enabled - using learning-integrated analysis")
                return await self.analyze_message_with_learning(message, user_id, channel_id)
            elif ensemble_enabled:
                logger.debug("✅ Ensemble analysis enabled - using enhanced ensemble analysis")
                return await self._ensemble_crisis_analysis(message, user_id, channel_id, start_time)
            else:
                logger.debug("🔥 Ensemble analysis disabled - using basic pattern analysis")
                return await self._basic_crisis_analysis(message, user_id, channel_id, start_time)
                
        except Exception as e:
            logger.error(f"❌ Enhanced crisis analysis failed: {e}")
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
        if self.model_ensemble_manager:
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
            # This would use self.model_ensemble_manager to get the sentiment model
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
            # This would use self.model_ensemble_manager to get the depression model
            logger.debug("😞 Analyzing depression indicators...")
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
        Updated for Step 10.8: Context analysis integration + FIXED API response structure
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
        
        # Determine crisis level using consolidated method
        crisis_level = self.apply_crisis_thresholds(final_score)
        
        # Build comprehensive response with ALL required API fields
        response = {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'needs_response': crisis_level != 'none',
            'crisis_level': crisis_level,
            'confidence_score': final_score,
            'detected_categories': self._extract_categories(pattern_analysis),
            'method': 'enhanced_crisis_analyzer',
            'analysis_results': {
                'crisis_score': final_score,
                'crisis_level': crisis_level,
                'model_results': model_results,
                'pattern_analysis': pattern_analysis or {},
                'context_analysis': context_analysis or {},
                'model_scores': model_scores,
                'analysis_metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'analysis_version': 'v3.1-3e-4.2-1',
                    'features_used': {
                        'ensemble_analysis': bool(model_results),
                        'pattern_analysis': bool(pattern_analysis),
                        'context_analysis': bool(context_analysis),
                        'context_manager_available': context_analysis.get('context_manager_status') == 'available',
                        'learning_enhanced': bool(self.learning_system_manager),
                        'shared_utilities': bool(self.shared_utilities_manager)
                    }
                }
            },
            'requires_staff_review': self._determine_staff_review_requirement(final_score, crisis_level),
            'processing_time': time.time() - start_time
        }

        # Debug
        logger.debug(f"🔍 Final response crisis_level={crisis_level}, confidence_score={final_score}")
        logger.debug(f"🔍 Enhanced: needs_response={crisis_level != 'none'}")
        logger.debug(f"🔍 Response structure keys: {list(response.keys())}")

        return response

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

    def _determine_crisis_level(self, score: float, mode: str = 'consensus') -> str:
        """
        Determine crisis level from score using consolidated method
        Updated for Phase 3e: Uses consolidated apply_crisis_thresholds method with proper mode support
        """
        try:
            return self.apply_crisis_thresholds(score, mode)
        except Exception as e:
            logger.error(f"❌ Crisis level determination failed: {e}")
            return self._fallback_crisis_level(score)

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
            
            # Use CrisisPatternManager methods directly
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
        
        # Return proper response structure with all required fields
        return {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'needs_response': crisis_level != 'none',
            'crisis_level': crisis_level,
            'confidence_score': confidence,
            'detected_categories': self._extract_categories({'enhanced_patterns': enhanced_patterns}),
            'method': 'basic_pattern_only' if pattern_analysis_enabled else 'basic_disabled',
            'analysis_results': {
                'crisis_score': confidence,
                'crisis_level': crisis_level,
                'pattern_analysis': {'enhanced_patterns': enhanced_patterns},
                'analysis_metadata': {
                    'processing_time': time.time() - start_time,
                    'timestamp': time.time(),
                    'analysis_version': 'v3.1-3e-4.2-1',
                    'ensemble_disabled': True,
                    'enhanced_consolidation': True
                }
            },
            'requires_staff_review': self._determine_staff_review_requirement(confidence, crisis_level),
            'processing_time': time.time() - start_time
        }

    # ========================================================================
    # STEP 10.6: CONSOLIDATED SCORING FUNCTIONS (Instance methods from utils/scoring_helpers.py)
    # ========================================================================
    
    def extract_depression_score(self, message: str, sentiment_model=None, 
                                analysis_parameters_manager=None, context=None,
                                crisis_pattern_manager=None) -> Tuple[float, List[str]]:
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
            
            # Configurable parameters from AnalysisParametersManager or consolidated methods
            if param_manager:
                try:
                    boost_factor = param_manager.get_depression_boost_factor()
                    max_score_limit = param_manager.get_max_depression_score()
                    
                    depression_score *= boost_factor
                    depression_score = min(depression_score, max_score_limit)
                    
                    logger.debug(f"Parameter adjustments: boost={boost_factor}, max={max_score_limit}")
                except Exception as e:
                    logger.warning(f"Parameter adjustment failed: {e}")
                    # Try using consolidated methods
                    try:
                        algorithm_params = self.get_analysis_algorithm_parameters()
                        boost_factor = algorithm_params.get('depression_boost_factor', 1.0)
                        depression_score *= boost_factor
                        logger.debug(f"Using consolidated algorithm parameters: boost={boost_factor}")
                    except Exception as e2:
                        logger.warning(f"Consolidated parameter access failed: {e2}")
            
            # Ensure score bounds
            depression_score = max(0.0, min(1.0, depression_score))
            
            logger.debug(f"Final depression score: {depression_score:.3f}")
            return depression_score, detected_categories
            
        except Exception as e:
            logger.error(f"Depression analysis failed: {e}")
            return 0.0, ['analysis_error']

    def enhanced_depression_analysis(self, message: str, base_score: float = 0.0, sentiment_model=None, 
                                   analysis_parameters_manager=None, context=None,
                                   crisis_pattern_manager=None) -> Dict:
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
                    # Apply context weights using CrisisPatternManager
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
                'analysis_method': 'enhanced_depression',
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
                'analysis_method': 'enhanced_depression',
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
        logger.debug(f"analyze_message called - delegating to enhanced analyze_crisis for backward compatibility")
        return await self.analyze_crisis(message, user_id, channel_id)


# ============================================================================
# ENHANCED FACTORY FUNCTION - Phase 3e Step 4.2
# ============================================================================

def create_crisis_analyzer(unified_config, model_ensemble_manager, crisis_pattern_manager=None,
                          analysis_parameters_manager=None, threshold_mapping_manager=None,
                          feature_config_manager=None, performance_config_manager=None,
                          context_pattern_manager=None,
                          # NEW Phase 3e parameters
                          shared_utilities_manager=None, learning_system_manager=None) -> CrisisAnalyzer:
    """
    Enhanced factory function for CrisisAnalyzer with Phase 3e integration
    Updated for Step 4.2: SharedUtilities and LearningSystem integration
    
    Args:
        # Existing parameters (maintained)
        model_ensemble_manager: Model ensemble manager for ensemble analysis
        crisis_pattern_manager: CrisisPatternManager for pattern-based analysis
        analysis_parameters_manager: AnalysisParametersManager for configurable parameters
        threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds
        feature_config_manager: FeatureConfigManager for feature flags
        performance_config_manager: PerformanceConfigManager for performance settings
        context_pattern_manager: ContextPatternManager for context analysis
        
        # NEW Phase 3e parameters
        shared_utilities_manager: SharedUtilitiesManager for common utilities
        learning_system_manager: LearningSystemManager for adaptive learning
        
    Returns:
        Enhanced CrisisAnalyzer instance with Phase 3e capabilities
    """
    return CrisisAnalyzer(
        unified_config,
        model_ensemble_manager=model_ensemble_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        analysis_parameters_manager=analysis_parameters_manager,
        threshold_mapping_manager=threshold_mapping_manager,
        feature_config_manager=feature_config_manager,
        performance_config_manager=performance_config_manager,
        context_pattern_manager=context_pattern_manager,
        # NEW Phase 3e dependencies
        shared_utilities_manager=shared_utilities_manager,
        learning_system_manager=learning_system_manager
    )

__all__ = ['CrisisAnalyzer', 'create_crisis_analyzer']

logger.info("✅ Enhanced CrisisAnalyzer v3.1-3e-4.2-1 loaded - Phase 3e Step 4.2 with consolidated analysis methods and learning integration complete")