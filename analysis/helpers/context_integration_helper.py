# ash-nlp/analysis/helpers/context_integration_helper.py
"""
Context Integration Helper for CrisisAnalyzer
FILE VERSION: v3.1-3e-5.5-6-1
CREATED: 2025-08-20
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

MIGRATION NOTICE: Methods moved from CrisisAnalyzer for optimization
Original location: analysis/crisis_analyzer.py - context integration and response building methods
"""

import logging
import time
import asyncio
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ContextIntegrationHelper:
    """Helper class for context integration operations moved from CrisisAnalyzer"""
    
    def __init__(self, crisis_analyzer):
        """
        Initialize with reference to parent CrisisAnalyzer
        
        Args:
            crisis_analyzer: Parent CrisisAnalyzer instance
        """
        self.crisis_analyzer = crisis_analyzer
    
    # ========================================================================
    # RESPONSE CREATION AND ERROR HANDLING
    # ========================================================================
    
    def create_error_response(self, message: str, user_id: str, channel_id: str, error: str, start_time: float) -> Dict:
        """
        Create standardized error response for crisis analysis
        Migrated from: CrisisAnalyzer._create_error_response()
        """
        return {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'needs_response': True,  # Conservative - assume crisis on error
            'crisis_level': 'high',  # Conservative - assume high crisis on error
            'confidence_score': 0.0,
            'detected_categories': ['error'],
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
                    'analysis_version': 'v3.1-3e-5.5-6',
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

    def create_timeout_response(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Create standardized timeout response for crisis analysis
        Migrated from: CrisisAnalyzer._create_timeout_response()
        """
        timeout_response = {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'needs_response': True,  # Conservative - assume crisis on timeout
            'crisis_level': 'medium',  # Conservative - assume medium crisis on timeout
            'confidence_score': 0.5,
            'detected_categories': ['timeout'],
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
                    'analysis_version': 'v3.1-3e-5.5-6',
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
        
        return timeout_response
    
    # ========================================================================
    # ENSEMBLE ANALYSIS COORDINATION
    # ========================================================================
    
    async def ensemble_crisis_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Full ensemble analysis with three models and pattern analysis
        Migrated from: CrisisAnalyzer._ensemble_crisis_analysis()
        """
        try:
            logger.debug("Starting ensemble crisis analysis...")
            
            # Get performance settings
            analysis_timeout = self.crisis_analyzer._performance_cache.get('analysis_timeout', 30.0)
            
            # Use asyncio.wait_for to enforce timeout
            analysis_result = await asyncio.wait_for(
                self._perform_comprehensive_analysis(message, user_id, channel_id, start_time),
                timeout=analysis_timeout
            )
            
            return analysis_result
            
        except asyncio.TimeoutError:
            logger.error(f"Ensemble analysis timed out after {analysis_timeout}s")
            return self.create_timeout_response(message, user_id, channel_id, start_time)
        except Exception as e:
            logger.error(f"Ensemble analysis error: {e}")
            return self.create_error_response(message, user_id, channel_id, str(e), start_time)

    async def _perform_comprehensive_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Perform comprehensive analysis coordinating all helper components
        """
        try:
            # Import helper classes for delegation
            from .ensemble_analysis_helper import EnsembleAnalysisHelper
            from .scoring_calculation_helper import ScoringCalculationHelper
            from .pattern_analysis_helper import PatternAnalysisHelper
            
            # Create helper instances
            ensemble_helper = EnsembleAnalysisHelper(self.crisis_analyzer)
            scoring_helper = ScoringCalculationHelper(self.crisis_analyzer)
            pattern_helper = PatternAnalysisHelper(self.crisis_analyzer)
            
            # Delegate to ensemble analysis helper
            return await ensemble_helper.perform_ensemble_analysis(message, user_id, channel_id, start_time)
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return self.create_error_response(message, user_id, channel_id, str(e), start_time)
    
    # ========================================================================
    # CACHE MANAGEMENT
    # ========================================================================
    
    def refresh_feature_cache(self):
        """
        Refresh feature flag cache if needed
        Migrated from: CrisisAnalyzer._refresh_feature_cache()
        """
        current_time = time.time()
        if current_time - self.crisis_analyzer._last_feature_check > self.crisis_analyzer._feature_cache_duration:
            if self.crisis_analyzer.feature_config_manager:
                try:
                    # Use the correct method names for FeatureConfigManager
                    self.crisis_analyzer._feature_cache = {
                        'ensemble_enabled': self.crisis_analyzer.feature_config_manager.is_ensemble_analysis_enabled(),
                        'pattern_analysis': self.crisis_analyzer.feature_config_manager.is_pattern_analysis_enabled(),
                        'sentiment_analysis': self.crisis_analyzer.feature_config_manager.is_semantic_analysis_enabled(),
                        'enhanced_learning': self.crisis_analyzer.feature_config_manager.is_threshold_learning_enabled(),
                        'temporal_boost': self.crisis_analyzer.feature_config_manager.is_temporal_patterns_enabled(),
                        'community_patterns': self.crisis_analyzer.feature_config_manager.is_community_vocab_enabled(),
                        'context_analysis': self.crisis_analyzer.feature_config_manager.is_context_analysis_enabled()
                    }
                    self.crisis_analyzer._last_feature_check = current_time
                    logger.debug("Feature cache refreshed")
                except Exception as e:
                    logger.error(f"Error refreshing feature cache: {e}")
                    # Use safe defaults
                    self.crisis_analyzer._feature_cache = {
                        'ensemble_enabled': True,
                        'pattern_analysis': True,
                        'sentiment_analysis': True,
                        'enhanced_learning': bool(self.crisis_analyzer.learning_system_manager),
                        'temporal_boost': True,
                        'community_patterns': True,
                        'context_analysis': True
                    }
            else:
                # Default all features enabled if no feature manager
                self.crisis_analyzer._feature_cache = {
                    'ensemble_enabled': True,
                    'pattern_analysis': True,
                    'sentiment_analysis': True,
                    'enhanced_learning': bool(self.crisis_analyzer.learning_system_manager),
                    'temporal_boost': True,
                    'community_patterns': True,
                    'context_analysis': True
                }

    def refresh_performance_cache(self):
        """
        Refresh performance settings cache if needed
        Migrated from: CrisisAnalyzer._refresh_performance_cache()
        """
        current_time = time.time()
        if current_time - self.crisis_analyzer._last_performance_check > self.crisis_analyzer._feature_cache_duration:
            if self.crisis_analyzer.performance_config_manager:
                try:
                    # Use the correct method names for PerformanceConfigManager
                    self.crisis_analyzer._performance_cache = {
                        'analysis_timeout': self.crisis_analyzer.performance_config_manager.get_analysis_timeout(),
                        'model_timeout': self.crisis_analyzer.performance_config_manager.get_analysis_timeout(),  # Use same for model timeout
                        'batch_size': 1,  # Fixed: Use default since get_analysis_batch_size may not exist
                        'cache_enabled': True,  # Default to enabled
                        'parallel_analysis': False  # Default to disabled (handled by FeatureConfigManager)
                    }
                    self.crisis_analyzer._last_performance_check = current_time
                    logger.debug("Performance cache refreshed")
                except Exception as e:
                    logger.error(f"Error refreshing performance cache: {e}")
                    # Use safe defaults
                    self.crisis_analyzer._performance_cache = {
                        'analysis_timeout': 30.0,
                        'model_timeout': 10.0,
                        'batch_size': 1,
                        'cache_enabled': True,
                        'parallel_analysis': False
                    }
            else:
                # Default performance settings if no performance manager
                self.crisis_analyzer._performance_cache = {
                    'analysis_timeout': 30.0,
                    'model_timeout': 10.0,
                    'batch_size': 1,
                    'cache_enabled': True,
                    'parallel_analysis': False
                }
    
    # ========================================================================
    # STAFF REVIEW AND CRISIS LEVEL DETERMINATION
    # ========================================================================
    
    def determine_staff_review_requirement(self, final_score: float, crisis_level: str) -> bool:
        """
        Determine if staff review is required based on score and crisis level
        Migrated from: CrisisAnalyzer._determine_staff_review_requirement()
        """
        try:
            # Use ThresholdMappingManager if available for staff review determination
            if self.crisis_analyzer.threshold_mapping_manager:
                try:
                    # Try different possible method names for staff review
                    if hasattr(self.crisis_analyzer.threshold_mapping_manager, 'requires_staff_review'):
                        return self.crisis_analyzer.threshold_mapping_manager.requires_staff_review(final_score, crisis_level)
                    elif hasattr(self.crisis_analyzer.threshold_mapping_manager, 'determine_staff_review'):
                        return self.crisis_analyzer.threshold_mapping_manager.determine_staff_review(final_score, crisis_level)
                    elif hasattr(self.crisis_analyzer.threshold_mapping_manager, 'get_staff_review_requirement'):
                        return self.crisis_analyzer.threshold_mapping_manager.get_staff_review_requirement(final_score, crisis_level)
                    else:
                        logger.debug("ThresholdMappingManager has no known staff review method - using fallback")
                except Exception as e:
                    logger.warning(f"Staff review determination via manager failed: {e}")
            
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
            logger.error(f"Staff review determination failed: {e}")
            # Conservative fallback - require review for any significant score
            return final_score >= 0.3
    
    def fallback_crisis_level(self, confidence: float) -> str:
        """
        Fallback crisis level determination
        Migrated from: CrisisAnalyzer._fallback_crisis_level()
        """
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