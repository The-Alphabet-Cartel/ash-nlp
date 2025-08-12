# ash-nlp/analysis/crisis_analyzer.py
"""
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
import re
import asyncio
from typing import Dict, List, Tuple, Any, Optional
from utils.context_helpers import extract_context_signals, analyze_sentiment_context, process_sentiment_with_flip
from utils.scoring_helpers import (
    extract_depression_score,
    enhanced_depression_analysis, 
    advanced_idiom_detection, 
    enhanced_crisis_level_mapping
)
from managers.crisis_pattern_manager import CrisisPatternManager
from utils.community_patterns import CommunityPatternExtractor

logger = logging.getLogger(__name__)

class CrisisAnalyzer:
    """
    PHASE 3D STEP 7 COMPLETE: Three Zero-Shot Model Ensemble crisis analysis with comprehensive manager integration
    Phase 3a: Clean v3.1 architecture with JSON-based patterns
    Phase 3b: Analysis parameters from AnalysisParametersManager  
    Phase 3c: Mode-aware thresholds from ThresholdMappingManager
    Phase 3d Step 7: Feature flags and performance settings from dedicated managers
    """
    
    def __init__(self, models_manager, crisis_pattern_manager: Optional[CrisisPatternManager] = None, 
                 learning_manager=None, analysis_parameters_manager=None, 
                 threshold_mapping_manager=None, feature_config_manager=None, 
                 performance_config_manager=None):
        """
        Initialize CrisisAnalyzer with all Phase 3d Step 7 managers
        
        Args:
            models_manager: ML model manager for ensemble analysis
            crisis_pattern_manager: CrisisPatternManager for pattern-based analysis (Phase 3a)
            learning_manager: Optional learning manager for feedback
            analysis_parameters_manager: AnalysisParametersManager for configurable parameters (Phase 3b)
            threshold_mapping_manager: ThresholdMappingManager for mode-aware thresholds (Phase 3c)
            feature_config_manager: FeatureConfigManager for feature flags (Phase 3d Step 7)
            performance_config_manager: PerformanceConfigManager for performance settings (Phase 3d Step 7)
        """
        self.models_manager = models_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.learning_manager = learning_manager
        self.analysis_parameters_manager = analysis_parameters_manager  # Phase 3b
        self.threshold_mapping_manager = threshold_mapping_manager  # Phase 3c
        self.feature_config_manager = feature_config_manager  # Phase 3d Step 7
        self.performance_config_manager = performance_config_manager  # Phase 3d Step 7
        
        # Initialize community pattern extractor if crisis pattern manager available
        if self.crisis_pattern_manager:
            self.community_extractor = CommunityPatternExtractor(self.crisis_pattern_manager)
            logger.info("CrisisAnalyzer v3.1d.7 initialized with CrisisPatternManager")
        else:
            self.community_extractor = None
            logger.warning("CrisisAnalyzer initialized without CrisisPatternManager - pattern analysis limited")
        
        # Validate threshold mapping manager integration
        if self.threshold_mapping_manager:
            logger.info("✅ CrisisAnalyzer Phase 3c: ThresholdMappingManager integration active")
            self._log_current_thresholds()
        else:
            logger.warning("⚠️ CrisisAnalyzer: No ThresholdMappingManager - using fallback thresholds")
        
        # Validate Phase 3d Step 7 manager availability
        manager_status = {
            'models_manager': 'available' if models_manager else 'missing',
            'crisis_pattern_manager': 'available' if crisis_pattern_manager else 'missing',
            'analysis_parameters_manager': 'available' if analysis_parameters_manager else 'missing',
            'threshold_mapping_manager': 'available' if threshold_mapping_manager else 'missing',
            'feature_config_manager': 'available' if feature_config_manager else 'missing',
            'performance_config_manager': 'available' if performance_config_manager else 'missing'
        }
        
        available_managers = [k for k, v in manager_status.items() if v == 'available']
        missing_managers = [k for k, v in manager_status.items() if v == 'missing']
        
        logger.info(f"✅ CrisisAnalyzer Phase 3d Step 7 - Available managers: {', '.join(available_managers)}")
        if missing_managers:
            logger.warning(f"⚠️ Missing managers (will use fallbacks): {', '.join(missing_managers)}")
        
        # Cache feature flags for performance - Phase 3d Step 7
        self._feature_cache = {}
        self._performance_cache = {}
        self._cache_initialized = False
        
        logger.info("✅ CrisisAnalyzer Phase 3d Step 7 initialized successfully")
    
    def _ensure_feature_cache(self):
        """Initialize feature and performance caches for optimal performance"""
        if self._cache_initialized:
            return
        
        try:
            # Cache feature flags - Phase 3d Step 7
            if self.feature_config_manager:
                self._feature_cache = {
                    'ensemble_analysis': self.feature_config_manager.is_ensemble_analysis_enabled(),
                    'pattern_integration': self.feature_config_manager.is_pattern_integration_enabled(),
                    'pattern_analysis': self.feature_config_manager.is_pattern_analysis_enabled(),
                    'semantic_analysis': self.feature_config_manager.is_semantic_analysis_enabled(),
                    'safety_controls': self.feature_config_manager.is_safety_controls_enabled(),
                    'experimental_features': self.feature_config_manager.get_experimental_features(),
                    'development_features': self.feature_config_manager.get_development_debug_features()
                }
                logger.debug("✅ Feature flags cached successfully")
            else:
                # Safe defaults when manager not available
                self._feature_cache = {
                    'ensemble_analysis': True,
                    'pattern_integration': True,
                    'pattern_analysis': True,
                    'semantic_analysis': True,
                    'safety_controls': True,
                    'experimental_features': {},
                    'development_features': {}
                }
                logger.debug("⚠️ Using default feature flags (FeatureConfigManager not available)")
            
            # Cache performance settings - Phase 3d Step 7  
            if self.performance_config_manager:
                self._performance_cache = {
                    'analysis_timeout': self.performance_config_manager.get_analysis_timeout(),
                    'request_timeout': self.performance_config_manager.get_request_timeout(),
                    'max_concurrent_requests': self.performance_config_manager.get_max_concurrent_requests(),
                    'cache_settings': self.performance_config_manager.get_cache_settings(),
                    'optimization_settings': self.performance_config_manager.get_optimization_settings()
                }
                logger.debug("✅ Performance settings cached successfully")
            else:
                # Safe defaults when manager not available
                self._performance_cache = {
                    'analysis_timeout': 30.0,
                    'request_timeout': 30.0,
                    'max_concurrent_requests': 10,
                    'cache_settings': {'enabled': True, 'ttl': 300},
                    'optimization_settings': {'batch_processing': True, 'parallel_models': True}
                }
                logger.debug("⚠️ Using default performance settings (PerformanceConfigManager not available)")
            
            self._cache_initialized = True
            logger.debug("✅ Feature and performance caches initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing feature/performance caches: {e}")
            # Use safe defaults on error
            self._feature_cache = {
                'ensemble_analysis': True,
                'pattern_integration': True,
                'pattern_analysis': True,
                'semantic_analysis': True,
                'safety_controls': True,
                'experimental_features': {},
                'development_features': {}
            }
            self._performance_cache = {
                'analysis_timeout': 30.0,
                'request_timeout': 30.0,
                'max_concurrent_requests': 10,
                'cache_settings': {'enabled': True, 'ttl': 300},
                'optimization_settings': {'batch_processing': True, 'parallel_models': True}
            }
            self._cache_initialized = True

    def _log_current_thresholds(self) -> None:
        """Log current threshold configuration for debugging"""
        try:
            if self.threshold_mapping_manager:
                current_mode = self.threshold_mapping_manager.get_current_ensemble_mode()
                crisis_mapping = self.threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                ensemble_thresholds = self.threshold_mapping_manager.get_ensemble_thresholds_for_mode()
                
                logger.debug(f"🎯 Current Ensemble Mode: {current_mode}")
                logger.debug(f"📊 Crisis Mapping: {crisis_mapping}")
                logger.debug(f"🔧 Ensemble Thresholds: {ensemble_thresholds}")
        except Exception as e:
            logger.warning(f"⚠️ Could not log current thresholds: {e}")

    async def analyze_message(self, message: str, user_id: str = None, channel_id: str = None) -> Dict[str, Any]:
        """
        Main analysis method - FIXED FEATURE FLAG ENFORCEMENT
        
        This method now properly respects all feature flags set in .env
        Enhanced for Phase 3d Step 7 with comprehensive feature flag checking
        """
        start_time = time.time()
        reasoning_steps = []
        
        # Ensure feature cache is initialized
        self._ensure_feature_cache()
        
        # Log current feature flag status for debugging
        logger.debug(f"🔧 Feature flags: pattern_analysis={self._feature_cache.get('pattern_analysis', 'unknown')}, "
                    f"ensemble_analysis={self._feature_cache.get('ensemble_analysis', 'unknown')}")
        
        # STEP 1: Check if ensemble analysis is enabled
        if not self._feature_cache.get('ensemble_analysis', True):
            logger.info("🚫 Ensemble analysis disabled by feature flag - using basic analysis")
            return await self._basic_crisis_analysis(message, user_id, channel_id, start_time)
        
        # STEP 2: Pattern Analysis - ONLY if feature flag enabled
        if self._feature_cache.get('pattern_analysis', False) and self.crisis_pattern_manager:
            pattern_analysis = await self._analyze_with_crisis_patterns(message)
            reasoning_steps.append(f"Pattern Analysis: {pattern_analysis.get('summary', 'none')}")
            logger.debug(f"✅ Pattern analysis enabled: {pattern_analysis.get('summary', 'none')}")
        else:
            pattern_analysis = {'patterns_triggered': [], 'adjustments': {}, 'summary': 'Pattern analysis disabled by feature flag'}
            reasoning_steps.append("Pattern Analysis: Disabled by feature flag")
            logger.debug("🚫 Pattern analysis disabled by feature flag")
        
        # STEP 3: Three Zero-Shot Model Ensemble ANALYSIS
        if hasattr(self.models_manager, 'analyze_with_ensemble'):
            # Use the new Three Zero-Shot Model Ensemble
            ensemble_result = self.models_manager.analyze_with_ensemble(message)
            
            # Extract consensus prediction for crisis level mapping
            consensus = ensemble_result.get('consensus', {})
            consensus_prediction = consensus.get('prediction', 'unknown')
            consensus_confidence = consensus.get('confidence', 0.0)
            
            # PHASE 3C: Use ThresholdMappingManager for crisis level mapping
            crisis_level = self._map_consensus_to_crisis_level_v3c(consensus_prediction, consensus_confidence)
            
            # Apply pattern-based adjustments ONLY if pattern analysis is enabled AND patterns were found
            if (self._feature_cache.get('pattern_analysis', False) and 
                pattern_analysis.get('adjustments') and 
                self._feature_cache.get('pattern_integration', True)):
                
                crisis_level, consensus_confidence = self._apply_pattern_adjustments_v3c(
                    crisis_level, consensus_confidence, pattern_analysis['adjustments']
                )
                logger.debug(f"✅ Pattern adjustments applied to ensemble result")
            else:
                logger.debug(f"🚫 Pattern adjustments skipped - pattern_analysis={self._feature_cache.get('pattern_analysis')} or no patterns")
            
            # Phase 3c: Determine if staff review required
            staff_review_required = self._is_staff_review_required(
                crisis_level, consensus_confidence, ensemble_result
            )
            
            # Build final result with ensemble data
            result = {
                'needs_response': crisis_level != 'none',
                'crisis_level': crisis_level,
                'confidence_score': consensus_confidence,
                'detected_categories': ensemble_result.get('detected_categories', []),
                'method': 'ensemble_and_patterns_integrated_v3d7' if pattern_analysis.get('patterns_triggered') else 'ensemble_only_v3d7',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': f"Three Zero-Shot Model Ensemble + Pattern Analysis ({'enabled' if self._feature_cache.get('pattern_analysis') else 'disabled'})",
                'reasoning': ' | '.join(reasoning_steps),
                'ensemble_details': ensemble_result,
                'pattern_analysis': pattern_analysis,
                'staff_review_required': staff_review_required,
                'threshold_mode': self._get_current_threshold_mode(),
                'threshold_config': self._get_threshold_debug_info(),
                'feature_flags_applied': {
                    'pattern_analysis': self._feature_cache.get('pattern_analysis', False),
                    'ensemble_analysis': self._feature_cache.get('ensemble_analysis', True),
                    'pattern_integration': self._feature_cache.get('pattern_integration', True)
                }
            }
            
            logger.debug(f"✅ ENSEMBLE+PATTERNS (pattern_analysis={self._feature_cache.get('pattern_analysis')}): "
                       f"{crisis_level} (conf={consensus_confidence:.3f}) "
                       f"consensus={consensus_prediction} mode={result['threshold_mode']}")
            
            # Phase 3c: Learning system feedback
            if self.learning_manager and self.threshold_mapping_manager:
                await self._provide_learning_feedback(result)
            
            return result
            
        else:
            # Fallback to legacy two-model analysis with Phase 3c thresholds
            return await self._legacy_two_model_analysis_v3c(message, user_id, channel_id, start_time)
    
    async def _full_ensemble_analysis(self, message: str, user_id: str, channel_id: str, start_time: float, reasoning_steps: List[str]) -> Dict:
        """Full ensemble analysis with Phase 3d Step 7 feature flag integration"""
        
        # Step 1: Extract context signals
        context = extract_context_signals(message)
        reasoning_steps.append(f"Context: {context}")
        
        # Step 2: Crisis Pattern Analysis (Phase 3a) - Check if enabled
        if self._feature_cache.get('pattern_analysis', True):
            pattern_analysis = await self._analyze_with_crisis_patterns(message)
            reasoning_steps.append(f"Pattern Analysis: {pattern_analysis.get('summary', 'none')}")
        else:
            pattern_analysis = {'patterns_triggered': [], 'adjustments': {}, 'summary': 'Pattern analysis disabled'}
            reasoning_steps.append("Pattern Analysis: Disabled by feature flag")
        
        # Step 3: Three Zero-Shot Model Ensemble ANALYSIS
        if hasattr(self.models_manager, 'analyze_with_ensemble'):
            # Use the new Three Zero-Shot Model Ensemble
            ensemble_result = self.models_manager.analyze_with_ensemble(message)
            
            # Extract consensus prediction for crisis level mapping
            consensus = ensemble_result.get('consensus', {})
            consensus_prediction = consensus.get('prediction', 'unknown')
            consensus_confidence = consensus.get('confidence', 0.0)
            
            # PHASE 3C: Use ThresholdMappingManager for crisis level mapping
            crisis_level = self._map_consensus_to_crisis_level_v3c(consensus_prediction, consensus_confidence)
            
            # Apply pattern-based adjustments (Phase 3c enhanced) - Check if enabled
            if pattern_analysis.get('adjustments') and self._feature_cache.get('pattern_integration', True):
                crisis_level, consensus_confidence = self._apply_pattern_adjustments_v3c(
                    crisis_level, consensus_confidence, pattern_analysis['adjustments']
                )
            
            # Phase 3c: Determine if staff review required
            staff_review_required = self._is_staff_review_required(
                crisis_level, consensus_confidence, ensemble_result
            )
            
            # Build final result with ensemble data
            result = {
                'needs_response': crisis_level != 'none',
                'crisis_level': crisis_level,
                'confidence_score': consensus_confidence,
                'detected_categories': ensemble_result.get('detected_categories', []),
                'method': 'three_model_ensemble_with_patterns_v3d7',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': f"Ensemble: {ensemble_result.get('model_info', 'unknown')}",
                'reasoning': ' | '.join(reasoning_steps),
                'ensemble_details': ensemble_result,
                'pattern_analysis': pattern_analysis,
                'staff_review_required': staff_review_required,
                'threshold_mode': self._get_current_threshold_mode(),
                'threshold_config': self._get_threshold_debug_info()
            }
            
            logger.debug(f"✅ ENSEMBLE+PATTERNS+THRESHOLDS+FEATURES: {crisis_level} (conf={consensus_confidence:.3f}) "
                       f"consensus={consensus_prediction} mode={result['threshold_mode']}")
            
            # Phase 3c: Learning system feedback
            if self.learning_manager and self.threshold_mapping_manager:
                await self._provide_learning_feedback(result)
            
            return result
            
        else:
            # Fallback to legacy two-model analysis with Phase 3c thresholds
            return await self._legacy_two_model_analysis_v3c(message, user_id, channel_id, start_time)
    
    async def _basic_crisis_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Basic crisis analysis when ensemble is disabled by feature flag
        FIXED: Properly respects pattern analysis feature flag
        """
        logger.info("🔥 Running basic crisis analysis - ensemble disabled by feature flag")
        
        # Check if pattern analysis is enabled
        pattern_analysis_enabled = self._feature_cache.get('pattern_analysis', False)
        
        if pattern_analysis_enabled and self.crisis_pattern_manager:
            logger.debug("✅ Pattern analysis enabled for basic analysis")
            pattern_analysis = await self._analyze_with_crisis_patterns(message)
            
            # Simple crisis level determination based on patterns
            if pattern_analysis.get('patterns_triggered'):
                highest_level = self._get_highest_pattern_crisis_level(pattern_analysis['patterns_triggered'])
                confidence = 0.6  # Conservative confidence for basic analysis
                logger.debug(f"✅ Pattern-based analysis result: {highest_level} (conf: {confidence})")
            else:
                highest_level = 'none'
                confidence = 0.0
                logger.debug("📊 No patterns triggered in basic analysis")
        else:
            logger.debug("🚫 Pattern analysis disabled - returning minimal analysis")
            pattern_analysis = {'patterns_triggered': [], 'adjustments': {}, 'summary': 'Pattern analysis disabled by feature flag'}
            highest_level = 'none'
            confidence = 0.0
        
        return {
            'needs_response': highest_level != 'none',
            'crisis_level': highest_level,
            'confidence_score': confidence,
            'detected_categories': [],
            'method': 'basic_pattern_only_v3d7' if pattern_analysis_enabled else 'basic_disabled_v3d7',
            'processing_time_ms': (time.time() - start_time) * 1000,
            'model_info': f"Basic analysis (pattern_analysis={'enabled' if pattern_analysis_enabled else 'disabled'})",
            'reasoning': f"Ensemble analysis disabled by feature flag, pattern analysis {'enabled' if pattern_analysis_enabled else 'disabled'}",
            'pattern_analysis': pattern_analysis,
            'staff_review_required': highest_level in ['high', 'medium'],
            'threshold_mode': 'basic',
            'threshold_config': {'mode': 'basic_fallback'},
            'feature_flags_applied': {
                'pattern_analysis': pattern_analysis_enabled,
                'ensemble_analysis': False,
                'pattern_integration': False
            },
            'note': f"Basic analysis - ensemble disabled, pattern analysis {'enabled' if pattern_analysis_enabled else 'disabled'}"
        }
    
    async def _quick_crisis_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """Quick crisis analysis for timeout scenarios"""
        logger.warning("⏰ Running quick crisis analysis due to timeout")
        
        # Quick pattern check only
        if self.crisis_pattern_manager:
            try:
                triggered_patterns = self.crisis_pattern_manager.find_triggered_patterns(message)
                if triggered_patterns:
                    crisis_level = 'medium'  # Conservative escalation for timeout scenario
                    confidence = 0.7
                else:
                    crisis_level = 'none'
                    confidence = 0.0
            except:
                crisis_level = 'low'  # Conservative fallback
                confidence = 0.5
        else:
            crisis_level = 'low'  # Conservative fallback when no pattern manager
            confidence = 0.5
        
        return {
            'needs_response': crisis_level != 'none',
            'crisis_level': crisis_level,
            'confidence_score': confidence,
            'detected_categories': [],
            'method': 'quick_timeout_analysis_v3d7',
            'processing_time_ms': (time.time() - start_time) * 1000,
            'model_info': 'Quick timeout analysis',
            'reasoning': 'Analysis timeout - using quick pattern check',
            'pattern_analysis': {'summary': 'Quick timeout check'},
            'staff_review_required': True,  # Always require review for timeout scenarios
            'threshold_mode': 'timeout',
            'threshold_config': {'mode': 'timeout_fallback'},
            'warning': 'Quick analysis due to timeout - review recommended'
        }

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status including Phase 3d Step 7 enhancements
        
        Returns:
            Dictionary with system status and manager availability
        """
        self._ensure_feature_cache()
        
        return {
            'version': '3d.7',
            'architecture': 'clean_v3.1_phase_3d_step_7_complete',
            'managers': {
                'models_manager': 'available' if self.models_manager else 'missing',
                'crisis_pattern_manager': 'available' if self.crisis_pattern_manager else 'missing', 
                'analysis_parameters_manager': 'available' if self.analysis_parameters_manager else 'missing',
                'threshold_mapping_manager': 'available' if self.threshold_mapping_manager else 'missing',
                'feature_config_manager': 'available' if self.feature_config_manager else 'missing',
                'performance_config_manager': 'available' if self.performance_config_manager else 'missing'
            },
            'capabilities': {
                'crisis_detection': True,
                'pattern_analysis': self._feature_cache.get('pattern_analysis', True),
                'semantic_analysis': self._feature_cache.get('semantic_analysis', True),
                'ensemble_analysis': self._feature_cache.get('ensemble_analysis', True),
                'community_patterns': self.community_extractor is not None,
                'learning_system': self.learning_manager is not None
            },
            'feature_flags': self._feature_cache,
            'performance_settings': self._performance_cache,
            'phase_3d_status': 'step_7_complete'
        }
    
    def get_feature_status(self) -> Dict[str, Any]:
        """
        Get current feature flag status - Phase 3d Step 7
        
        Returns:
            Dictionary with all feature flag states
        """
        self._ensure_feature_cache()
        
        if self.feature_config_manager:
            try:
                return {
                    'manager_available': True,
                    'core_features': self.feature_config_manager.get_core_system_features(),
                    'analysis_features': self.feature_config_manager.get_analysis_component_features(),
                    'experimental_features': self.feature_config_manager.get_experimental_features(),
                    'development_features': self.feature_config_manager.get_development_debug_features(),
                    'validation_errors': self.feature_config_manager.get_validation_errors()
                }
            except Exception as e:
                logger.error(f"❌ Error getting feature status: {e}")
                return {'manager_available': True, 'error': str(e)}
        else:
            return {
                'manager_available': False,
                'fallback_features': self._feature_cache,
                'note': 'Using cached defaults - FeatureConfigManager not available'
            }
    
    def get_performance_status(self) -> Dict[str, Any]:
        """
        Get current performance settings status - Phase 3d Step 7
        
        Returns:
            Dictionary with all performance settings
        """
        self._ensure_feature_cache()
        
        if self.performance_config_manager:
            try:
                return {
                    'manager_available': True,
                    'analysis_settings': {
                        'timeout': self.performance_config_manager.get_analysis_timeout(),
                        'max_concurrent': self.performance_config_manager.get_max_concurrent_requests()
                    },
                    'cache_settings': self.performance_config_manager.get_cache_settings(),
                    'optimization_settings': self.performance_config_manager.get_optimization_settings(),
                    'performance_profile': self.performance_config_manager.get_performance_profile()
                }
            except Exception as e:
                logger.error(f"❌ Error getting performance status: {e}")
                return {'manager_available': True, 'error': str(e)}
        else:
            return {
                'manager_available': False,
                'fallback_settings': self._performance_cache,
                'note': 'Using cached defaults - PerformanceConfigManager not available'
            }

    # ============================================================================
    # PHASE 3C METHODS - PRESERVED AND ENHANCED
    # ============================================================================

    def _map_consensus_to_crisis_level_v3c(self, consensus_prediction: str, confidence: float) -> str:
        """
        PHASE 3C: Mode-aware consensus prediction to crisis level mapping using ThresholdMappingManager
        Replaces hardcoded threshold logic with dynamic, mode-aware thresholds
        """
        try:
            # Get mode-aware thresholds
            if self.threshold_mapping_manager:
                crisis_mapping = self.threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                current_mode = self.threshold_mapping_manager.get_current_ensemble_mode()
                
                logger.debug(f"🎯 Using {current_mode} mode thresholds for mapping: {consensus_prediction} + {confidence:.3f}")
            else:
                # Fallback to default thresholds
                crisis_mapping = {
                    'crisis_to_high': 0.50,
                    'crisis_to_medium': 0.30,
                    'mild_crisis_to_low': 0.40,
                    'negative_to_low': 0.70,
                    'unknown_to_low': 0.50
                }
                logger.warning("⚠️ Using fallback thresholds - ThresholdMappingManager not available")
            
            pred_lower = consensus_prediction.lower()
            
            # CRISIS predictions (normalized from ensemble)
            if pred_lower == 'crisis':
                if confidence >= crisis_mapping.get('crisis_to_high', 0.50):
                    return 'high'      # High confidence crisis
                elif confidence >= crisis_mapping.get('crisis_to_medium', 0.30):
                    return 'medium'    # Medium confidence crisis  
                else:
                    return 'low'       # Low confidence crisis, but still crisis
            
            # MILD_CRISIS predictions
            elif pred_lower == 'mild_crisis':
                if confidence >= crisis_mapping.get('mild_crisis_to_low', 0.40):
                    return 'low'       # Mild crisis with sufficient confidence
                else:
                    return 'none'      # Very low confidence mild crisis
            
            # NEGATIVE sentiment predictions
            elif pred_lower in ['negative', 'very_negative']:
                if confidence >= crisis_mapping.get('negative_to_low', 0.70):
                    return 'low'       # High confidence negative → low crisis
                else:
                    return 'none'      # Low confidence negative
            
            # LOW_RISK or similar predictions
            elif pred_lower in ['low_risk', 'minimal_distress']:
                # These typically map to low crisis only with very high confidence
                if confidence >= 0.80:  # Higher threshold for these categories
                    return 'low'
                else:
                    return 'none'
            
            # UNKNOWN predictions (high confidence unknown can be concerning)
            elif pred_lower == 'unknown':
                if confidence >= crisis_mapping.get('unknown_to_low', 0.50):
                    return 'low'       # High confidence unknown → investigate
                else:
                    return 'none'
            
            # POSITIVE/NEUTRAL predictions
            elif pred_lower in ['positive', 'very_positive', 'neutral', 'no_risk']:
                return 'none'          # Positive predictions don't indicate crisis
            
            # Catch-all for unexpected predictions
            else:
                logger.warning(f"⚠️ Unexpected consensus prediction: {consensus_prediction}")
                if confidence >= 0.60:  # Conservative threshold for unknown predictions
                    return 'low'
                else:
                    return 'none'
                    
        except Exception as e:
            logger.error(f"❌ Error in consensus to crisis level mapping: {e}")
            # Safe fallback - if unsure and high confidence, escalate
            return 'low' if confidence >= 0.50 else 'none'

    def _apply_pattern_adjustments_v3c(self, crisis_level: str, confidence: float, adjustments: Dict[str, Any]) -> Tuple[str, float]:
        """
        PHASE 3C: Apply pattern-based adjustments using ThresholdMappingManager configuration
        Enhanced with learning system integration and mode-aware adjustment limits
        """
        try:
            # Get pattern integration configuration
            if self.threshold_mapping_manager:
                pattern_config = self.threshold_mapping_manager.get_pattern_integration_config()
            else:
                pattern_config = {
                    'pattern_weight_multiplier': 1.2,
                    'confidence_boost_limit': 0.15,
                    'escalation_required_minimum': 'low'
                }
            
            # Apply confidence adjustments with configured limits
            confidence_adjustment = adjustments.get('confidence_adjustment', 0.0)
            max_boost = pattern_config.get('confidence_boost_limit', 0.15)
            
            # Scale adjustment by pattern weight multiplier
            scaled_adjustment = confidence_adjustment * pattern_config.get('pattern_weight_multiplier', 1.2)
            scaled_adjustment = max(-max_boost, min(max_boost, scaled_adjustment))
            
            adjusted_confidence = confidence + scaled_adjustment
            adjusted_confidence = max(0.0, min(1.0, adjusted_confidence))
            
            crisis_boost = adjustments.get('crisis_boost', 0.0)
            
            # Get mode-specific ensemble thresholds for escalation decisions
            if self.threshold_mapping_manager:
                ensemble_thresholds = self.threshold_mapping_manager.get_ensemble_thresholds_for_mode()
                escalation_thresholds = {
                    'to_low': ensemble_thresholds.get('low', 0.12),
                    'to_medium': ensemble_thresholds.get('medium', 0.25),
                    'to_high': ensemble_thresholds.get('high', 0.45)
                }
            else:
                escalation_thresholds = {
                    'to_low': 0.15,
                    'to_medium': 0.25,
                    'to_high': 0.50
                }
            
            # Apply pattern-based crisis level escalation
            if crisis_boost >= 0.15:  # Significant pattern boost
                if crisis_level == 'none' and adjusted_confidence > escalation_thresholds['to_low']:
                    crisis_level = 'low'
                    logger.debug(f"📈 Pattern escalation: none → low (boost={crisis_boost:.3f})")
                elif crisis_level == 'low' and adjusted_confidence > escalation_thresholds['to_medium']:
                    crisis_level = 'medium'
                    logger.debug(f"📈 Pattern escalation: low → medium (boost={crisis_boost:.3f})")
                elif crisis_level == 'medium' and adjusted_confidence > escalation_thresholds['to_high']:
                    crisis_level = 'high'
                    logger.debug(f"📈 Pattern escalation: medium → high (boost={crisis_boost:.3f})")
            
            # Handle escalation requirements
            escalation_minimum = pattern_config.get('escalation_required_minimum', 'low')
            if adjustments.get('escalation_required') and crisis_level == 'none':
                crisis_level = escalation_minimum
                logger.debug(f"⬆️ Escalation required: none → {escalation_minimum}")
            
            # Apply pattern override for very high pattern confidence
            pattern_override_threshold = pattern_config.get('pattern_override_threshold', 0.8)
            if (adjustments.get('pattern_confidence', 0) >= pattern_override_threshold and 
                crisis_level == 'none'):
                crisis_level = 'low'
                logger.debug(f"🔀 Pattern override: none → low (pattern_conf={adjustments.get('pattern_confidence', 0):.3f})")
            
            return crisis_level, adjusted_confidence
            
        except Exception as e:
            logger.error(f"❌ Error applying pattern adjustments: {e}")
            return crisis_level, confidence

    def _is_staff_review_required(self, crisis_level: str, confidence: float, 
                                ensemble_result: Dict[str, Any]) -> bool:
        """
        PHASE 3C: Determine if staff review is required using ThresholdMappingManager
        """
        try:
            if not self.threshold_mapping_manager:
                # Fallback logic
                return crisis_level == 'high' or (crisis_level == 'medium' and confidence >= 0.45)
            
            # Check for model disagreement and gap detection
            has_model_disagreement = ensemble_result.get('gap_detection', {}).get('gap_detected', False)
            has_gap_detection = ensemble_result.get('gap_detection', {}).get('requires_review', False)
            
            return self.threshold_mapping_manager.is_staff_review_required(
                crisis_level, confidence, has_model_disagreement, has_gap_detection
            )
            
        except Exception as e:
            logger.error(f"❌ Error determining staff review requirement: {e}")
            # Conservative fallback - require review for medium+ crisis levels
            return crisis_level in ['high', 'medium']

    def _get_current_threshold_mode(self) -> str:
        """Get current threshold mode for debugging"""
        try:
            if self.threshold_mapping_manager:
                return self.threshold_mapping_manager.get_current_ensemble_mode()
            return 'fallback'
        except Exception:
            return 'error'

    def _get_threshold_debug_info(self) -> Dict[str, Any]:
        """Get threshold configuration debug information"""
        try:
            if self.threshold_mapping_manager:
                return {
                    'crisis_mapping': self.threshold_mapping_manager.get_crisis_level_mapping_for_mode(),
                    'ensemble_thresholds': self.threshold_mapping_manager.get_ensemble_thresholds_for_mode(),
                    'staff_review_config': self.threshold_mapping_manager.get_staff_review_config(),
                    'pattern_integration': self.threshold_mapping_manager.get_pattern_integration_config()
                }
            return {'mode': 'fallback', 'source': 'hardcoded_defaults'}
        except Exception as e:
            return {'error': str(e), 'mode': 'error'}

    async def _provide_learning_feedback(self, result: Dict[str, Any]) -> None:
        """
        PHASE 3C: Provide feedback to learning system for threshold adjustment
        """
        try:
            if not (self.learning_manager and self.threshold_mapping_manager):
                return
            
            learning_config = self.threshold_mapping_manager.get_learning_system_config()
            if not learning_config.get('enable_threshold_learning', True):
                return
            
            # Prepare learning feedback based on analysis result
            feedback_data = {
                'crisis_level': result.get('crisis_level'),
                'confidence': result.get('confidence_score'),
                'ensemble_prediction': result.get('ensemble_details', {}).get('consensus', {}).get('prediction'),
                'pattern_triggered': bool(result.get('pattern_analysis', {}).get('patterns_triggered')),
                'staff_review_required': result.get('staff_review_required', False),
                'processing_time': result.get('processing_time_ms'),
                'current_mode': self._get_current_threshold_mode()
            }
            
            # Send to learning manager for threshold optimization
            await self.learning_manager.record_analysis_feedback(feedback_data)
            
            logger.debug("🎓 Learning feedback provided for threshold optimization")
            
        except Exception as e:
            logger.warning(f"⚠️ Error providing learning feedback: {e}")

    async def _legacy_two_model_analysis_v3c(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        PHASE 3C: Legacy two-model analysis updated with ThresholdMappingManager
        Fallback method when ensemble analysis is not available
        """
        try:
            logger.warning("⚠️ Using legacy two-model analysis - ensemble not available")
            
            # Get ensemble thresholds for legacy analysis
            if self.threshold_mapping_manager:
                ensemble_thresholds = self.threshold_mapping_manager.get_ensemble_thresholds_for_mode()
                current_mode = self.threshold_mapping_manager.get_current_ensemble_mode()
                logger.debug(f"🔧 Legacy analysis using {current_mode} mode thresholds: {ensemble_thresholds}")
            else:
                ensemble_thresholds = {'high': 0.45, 'medium': 0.25, 'low': 0.12}
                current_mode = 'fallback'
            
            # Perform legacy analysis steps (simplified for Phase 3c)
            context = extract_context_signals(message)
            
            # Pattern analysis
            pattern_analysis = await self._analyze_with_crisis_patterns(message)
            
            # Simplified scoring using available models
            base_confidence = 0.3  # Default base confidence for legacy mode
            
            # Apply pattern adjustments
            adjusted_confidence = base_confidence
            crisis_level = 'none'
            
            if pattern_analysis.get('adjustments'):
                crisis_level, adjusted_confidence = self._apply_pattern_adjustments_v3c(
                    crisis_level, adjusted_confidence, pattern_analysis['adjustments']
                )
            
            # Apply ensemble thresholds to determine final crisis level
            if adjusted_confidence >= ensemble_thresholds['high']:
                crisis_level = 'high'
            elif adjusted_confidence >= ensemble_thresholds['medium']:
                crisis_level = 'medium'  
            elif adjusted_confidence >= ensemble_thresholds['low']:
                crisis_level = 'low'
            
            # Determine staff review requirement
            staff_review_required = self._is_staff_review_required(
                crisis_level, adjusted_confidence, {}
            )
            
            return {
                'needs_response': crisis_level != 'none',
                'crisis_level': crisis_level,
                'confidence_score': adjusted_confidence,
                'detected_categories': [],
                'method': f'legacy_two_model_v3c_{current_mode}',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': 'Legacy two-model fallback',
                'reasoning': f'Legacy analysis with {current_mode} thresholds',
                'pattern_analysis': pattern_analysis,
                'staff_review_required': staff_review_required,
                'threshold_mode': current_mode,
                'threshold_config': self._get_threshold_debug_info(),
                'warning': 'Using legacy analysis - ensemble not available'
            }
            
        except Exception as e:
            logger.error(f"❌ Error in legacy two-model analysis: {e}")
            return {
                'needs_response': False,
                'crisis_level': 'none',
                'confidence_score': 0.0,
                'detected_categories': [],
                'method': 'legacy_error_fallback',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'error': str(e),
                'staff_review_required': True
            }

    async def _analyze_with_crisis_patterns(self, message: str) -> Dict[str, Any]:
        """
        Crisis pattern analysis using CrisisPatternManager with semantic NLP integration
        Enhanced with Phase 3c threshold awareness and semantic classification
        """
        try:
            if not self.crisis_pattern_manager:
                return {
                    'patterns_triggered': [],
                    'adjustments': {},
                    'summary': 'No crisis pattern manager available',
                    'error': 'CrisisPatternManager not initialized'
                }
            
            # UPDATED: Pass models_manager to enable semantic pattern matching
            triggered_patterns = self.crisis_pattern_manager.find_triggered_patterns(
                message, 
                models_manager=self.models_manager  # Pass the models manager for semantic analysis
            )
            
            if not triggered_patterns:
                return {
                    'patterns_triggered': [],
                    'adjustments': {},
                    'summary': 'No patterns triggered'
                }
            
            # Calculate pattern-based adjustments with Phase 3c awareness
            adjustments = self._calculate_pattern_adjustments_v3c(triggered_patterns, message)
            
            # Enhanced summary with semantic classification info
            pattern_sources = list(set(p.get('source', 'unknown') for p in triggered_patterns))
            semantic_patterns = [p for p in triggered_patterns if p.get('pattern_type') == 'semantic_classification']
            
            summary_parts = [f"{len(triggered_patterns)} patterns triggered"]
            if semantic_patterns:
                summary_parts.append(f"{len(semantic_patterns)} semantic")
            if 'zero_shot_nlp_model' in pattern_sources:
                summary_parts.append("(NLP-powered)")
            
            return {
                'patterns_triggered': triggered_patterns,
                'adjustments': adjustments,
                'summary': " ".join(summary_parts),
                'pattern_categories': list(set(p.get('category', 'unknown') for p in triggered_patterns)),
                'highest_crisis_level': self._get_highest_pattern_crisis_level(triggered_patterns),
                'semantic_classification_used': len(semantic_patterns) > 0,
                'pattern_sources': pattern_sources
            }
            
        except Exception as e:
            logger.error(f"❌ Error in crisis pattern analysis: {e}")
            return {
                'patterns_triggered': [],
                'adjustments': {},
                'summary': 'Pattern analysis error',
                'error': str(e)
            }

    def _calculate_pattern_adjustments_v3c(self, triggered_patterns: List[Dict], message: str) -> Dict[str, Any]:
        """
        PHASE 3C: Calculate pattern adjustments using ThresholdMappingManager configuration
        Enhanced with mode-aware adjustment scaling
        """
        try:
            if not triggered_patterns:
                return {}
            
            # Get pattern integration configuration
            if self.threshold_mapping_manager:
                pattern_config = self.threshold_mapping_manager.get_pattern_integration_config()
                current_mode = self.threshold_mapping_manager.get_current_ensemble_mode()
            else:
                pattern_config = {
                    'pattern_weight_multiplier': 1.2,
                    'confidence_boost_limit': 0.15,
                    'community_pattern_boost': 1.1
                }
                current_mode = 'fallback'
            
            total_confidence_boost = 0.0
            total_crisis_boost = 0.0
            escalation_required = False
            pattern_confidence = 0.0
            
            # Process each triggered pattern
            for pattern in triggered_patterns:
                pattern_weight = pattern.get('weight', 1.0)
                crisis_level = pattern.get('crisis_level', 'low')
                
                # Apply community-specific boosts
                if pattern.get('category') in ['lgbtqia_patterns', 'community_vocabulary']:
                    community_boost = pattern_config.get('community_pattern_boost', 1.1)
                    pattern_weight *= community_boost
                
                # Calculate confidence adjustment based on crisis level
                if crisis_level == 'high':
                    confidence_adjustment = 0.12 * pattern_weight
                    crisis_boost = 0.20 * pattern_weight
                elif crisis_level == 'medium':
                    confidence_adjustment = 0.08 * pattern_weight
                    crisis_boost = 0.12 * pattern_weight
                else:  # low
                    confidence_adjustment = 0.05 * pattern_weight
                    crisis_boost = 0.08 * pattern_weight
                
                total_confidence_boost += confidence_adjustment
                total_crisis_boost += crisis_boost
                
                # Track pattern confidence
                pattern_confidence = max(pattern_confidence, pattern.get('confidence', 0.5))
                
                # Check for escalation requirements
                if pattern.get('requires_escalation', False):
                    escalation_required = True
            
            # Apply mode-specific scaling
            mode_multipliers = {
                'consensus': 0.9,    # Conservative scaling for consensus mode
                'majority': 1.0,     # Baseline scaling for majority mode
                'weighted': 1.1,     # Slightly higher scaling for weighted mode (depression-heavy)
                'fallback': 1.0
            }
            
            mode_multiplier = mode_multipliers.get(current_mode, 1.0)
            total_confidence_boost *= mode_multiplier
            total_crisis_boost *= mode_multiplier
            
            # Apply pattern weight multiplier
            pattern_multiplier = pattern_config.get('pattern_weight_multiplier', 1.2)
            total_confidence_boost *= pattern_multiplier
            total_crisis_boost *= pattern_multiplier
            
            # Apply boost limits
            max_boost = pattern_config.get('confidence_boost_limit', 0.15)
            total_confidence_boost = min(total_confidence_boost, max_boost)
            total_crisis_boost = min(total_crisis_boost, max_boost)
            
            adjustments = {
                'confidence_adjustment': total_confidence_boost,
                'crisis_boost': total_crisis_boost,
                'escalation_required': escalation_required,
                'pattern_confidence': pattern_confidence,
                'mode_multiplier': mode_multiplier,
                'pattern_count': len(triggered_patterns)
            }
            
            logger.debug(f"🔧 Pattern adjustments ({current_mode} mode): {adjustments}")
            return adjustments
            
        except Exception as e:
            logger.error(f"❌ Error calculating pattern adjustments: {e}")
            return {}

    def _get_highest_pattern_crisis_level(self, patterns: List[Dict]) -> str:
        """Get the highest crisis level among triggered patterns"""
        if not patterns:
            return 'none'
        
        crisis_levels = {'high': 3, 'medium': 2, 'low': 1, 'none': 0}
        reverse_levels = {3: 'high', 2: 'medium', 1: 'low', 0: 'none'}
        
        highest_level = 0
        for pattern in patterns:
            level = crisis_levels.get(pattern.get('crisis_level', 'none'), 0)
            highest_level = max(highest_level, level)
        
        return reverse_levels.get(highest_level, 'none')

    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        PHASE 3D STEP 7: Get comprehensive configuration summary for debugging
        Enhanced with feature flag and performance settings information
        """
        self._ensure_feature_cache()
        
        summary = {
            'phase': '3d.7',
            'architecture': 'clean_v3_1_phase_3d_step_7_complete',
            'components': {
                'crisis_pattern_manager': self.crisis_pattern_manager is not None,
                'analysis_parameters_manager': self.analysis_parameters_manager is not None,
                'threshold_mapping_manager': self.threshold_mapping_manager is not None,
                'feature_config_manager': self.feature_config_manager is not None,
                'performance_config_manager': self.performance_config_manager is not None,
                'learning_manager': self.learning_manager is not None
            },
            'feature_flags': self._feature_cache,
            'performance_settings': self._performance_cache
        }
        
        if self.threshold_mapping_manager:
            try:
                summary['threshold_configuration'] = {
                    'current_mode': self.threshold_mapping_manager.get_current_ensemble_mode(),
                    'crisis_mapping': self.threshold_mapping_manager.get_crisis_level_mapping_for_mode(),
                    'staff_review_enabled': self.threshold_mapping_manager.get_staff_review_config().get('high_always', True),
                    'learning_enabled': self.threshold_mapping_manager.get_learning_system_config().get('enable_threshold_learning', True)
                }
                
                summary['validation_status'] = self.threshold_mapping_manager.get_validation_summary()
            except Exception as e:
                summary['threshold_configuration_error'] = str(e)
        
        # Add Phase 3d Step 7 status
        if self.feature_config_manager:
            try:
                summary['feature_management'] = {
                    'manager_available': True,
                    'total_features': len(self._feature_cache),
                    'enabled_features': sum(1 for v in self._feature_cache.values() if isinstance(v, bool) and v),
                    'validation_errors': len(self.feature_config_manager.get_validation_errors()) if hasattr(self.feature_config_manager, 'get_validation_errors') else 0
                }
            except Exception as e:
                summary['feature_management_error'] = str(e)
        
        if self.performance_config_manager:
            try:
                summary['performance_management'] = {
                    'manager_available': True,
                    'analysis_timeout': self._performance_cache.get('analysis_timeout', 30.0),
                    'cache_enabled': self._performance_cache.get('cache_settings', {}).get('enabled', True),
                    'optimization_enabled': len([k for k, v in self._performance_cache.get('optimization_settings', {}).items() if v])
                }
            except Exception as e:
                summary['performance_management_error'] = str(e)
        
        return summary