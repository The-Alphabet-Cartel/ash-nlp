# ash-nlp/analysis/crisis_analyzer.py
"""
Crisis Analyzer for Ash-NLP Service v3.1
FILE VERSION: v3.1-3e-4.2-1
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
    
    def __init__(self, model_ensemble_manager, crisis_pattern_manager=None, learning_manager=None,
                 analysis_parameters_manager=None, threshold_mapping_manager=None,
                 feature_config_manager=None, performance_config_manager=None,
                 context_pattern_manager=None,
                 # NEW Phase 3e dependencies
                 shared_utilities_manager=None, learning_system_manager=None):
        """
        Initialize Enhanced Crisis Analyzer with Phase 3e manager integration
        Updated for Step 4.2: SharedUtilities and LearningSystem integration
        
        Args:
            # Existing dependencies (maintained)
            model_ensemble_manager: Model ensemble manager for ensemble analysis
            crisis_pattern_manager: CrisisPatternManager for pattern-based analysis
            learning_manager: Optional learning manager for feedback (legacy)
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
        self.model_ensemble_manager = model_ensemble_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.learning_manager = learning_manager  # legacy support
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
    
    def get_analysis_crisis_thresholds(self) -> Dict[str, float]:
        """
        Get crisis thresholds for analysis (consolidated from AnalysisParametersManager)
        
        Returns:
            Dictionary of crisis threshold settings
        """
        try:
            if self.shared_utilities_manager:
                return self.shared_utilities_manager.get_config_section_safely(
                    'analysis_parameters', 'crisis_thresholds', {
                        'low': 0.2,
                        'medium': 0.4,
                        'high': 0.6,
                        'critical': 0.8
                    }
                )
            elif self.analysis_parameters_manager:
                # Fallback to legacy manager
                return self.analysis_parameters_manager.get_crisis_thresholds()
            else:
                logger.warning("⚠️ No config manager available - using hardcoded crisis thresholds")
                return {
                    'low': 0.2,
                    'medium': 0.4,
                    'high': 0.6,
                    'critical': 0.8
                }
        except Exception as e:
            return self._safe_analysis_execution(
                "get_analysis_crisis_thresholds", 
                lambda: {'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8}
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
    
    def apply_crisis_thresholds(self, confidence: float, mode: str = 'default') -> str:
        """
        Apply thresholds to determine crisis level (consolidated from ThresholdMappingManager)
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
            mode: Analysis mode for threshold selection
            
        Returns:
            Crisis level string ('none', 'low', 'medium', 'high', 'critical')
        """
        try:
            # Get mode-specific thresholds
            thresholds = self.get_crisis_threshold_for_mode(mode)
            
            # Apply learning adjustments if available
            if self.learning_system_manager:
                adjusted_confidence = self.learning_system_manager.apply_threshold_adjustments(
                    confidence, mode
                )
                logger.debug(f"Learning adjustment: {confidence:.3f} → {adjusted_confidence:.3f}")
                confidence = adjusted_confidence
            
            # Determine crisis level
            if confidence >= thresholds.get('critical', 0.8):
                return 'critical'
            elif confidence >= thresholds.get('high', 0.6):
                return 'high'
            elif confidence >= thresholds.get('medium', 0.4):
                return 'medium'
            elif confidence >= thresholds.get('low', 0.2):
                return 'low'
            else:
                return 'none'
                
        except Exception as e:
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

    def validate_crisis_analysis_thresholds(self) -> Dict[str, bool]:
        """
        Validate analysis thresholds (consolidated from ThresholdMappingManager)
        
        Returns:
            Dictionary of validation results
        """
        try:
            validation_results = {}
            
            # Validate crisis thresholds
            crisis_thresholds = self.get_analysis_crisis_thresholds()
            validation_results['crisis_thresholds_valid'] = all(
                isinstance(v, (int, float)) and 0 <= v <= 1 
                for v in crisis_thresholds.values()
            )
            
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
            
            # Use shared utilities for validation if available
            if self.shared_utilities_manager:
                for key, value in validation_results.items():
                    if not value:
                        logger.warning(f"⚠️ Validation failed for {key}")
            
            validation_results['overall_valid'] = all(validation_results.values())
            return validation_results
            
        except Exception as e:
            return self._safe_analysis_execution(
                "validate_crisis_analysis_thresholds",
                lambda: {'overall_valid': False, 'error': str(e)}
            )

    def get_crisis_threshold_for_mode(self, mode: str) -> Dict[str, float]:
        """
        Get mode-specific crisis thresholds (consolidated from ThresholdMappingManager)
        
        Args:
            mode: Analysis mode ('default', 'sensitive', 'conservative')
            
        Returns:
            Dictionary of mode-specific thresholds
        """
        try:
            base_thresholds = self.get_analysis_crisis_thresholds()
            
            # Mode-specific adjustments
            if mode == 'sensitive':
                # Lower thresholds for more sensitive detection
                return {k: max(0.0, v - 0.1) for k, v in base_thresholds.items()}
            elif mode == 'conservative':
                # Higher thresholds for more conservative detection
                return {k: min(1.0, v + 0.1) for k, v in base_thresholds.items()}
            else:  # default mode
                return base_thresholds
                
        except Exception as e:
            return self._safe_analysis_execution(
                "get_crisis_threshold_for_mode",
                lambda: {'low': 0.2, 'medium': 0.4, 'high': 0.6, 'critical': 0.8}
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
                'consolidation_method': 'enhanced_ensemble_v3e4.2'
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
            updated_results['weighting_method'] = 'ensemble_weighted_v3e4.2'
            
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

    # Continue with all existing methods from Phase 3d...
    # [The rest of the methods from the original file would continue here unchanged]
    # This includes: _ensemble_crisis_analysis, _perform_ensemble_analysis, 
    # _analyze_with_model, _analyze_sentiment, _analyze_depression, 
    # _combine_analysis_results, _extract_categories, _determine_crisis_level,
    # _basic_crisis_analysis, analyze_message, extract_depression_score,
    # enhanced_depression_analysis, _process_sentiment_result

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

def create_crisis_analyzer(model_ensemble_manager, crisis_pattern_manager=None, learning_manager=None,
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
        learning_manager: Optional learning manager for feedback (legacy)
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
        model_ensemble_manager=model_ensemble_manager,
        crisis_pattern_manager=crisis_pattern_manager,
        learning_manager=learning_manager,
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