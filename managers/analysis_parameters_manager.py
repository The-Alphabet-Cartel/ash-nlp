# ash-nlp/managers/analysis_parameters_manager.py
"""
Analysis Parameters Manager for Ash NLP Service
FILE VERSION: v3.1-3e-5.1-1
LAST MODIFIED: 2025-08-18
PHASE: 3e, Step 5.1 - Systematic Manager Cleanup
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalysisParametersManager:
    """
    Analysis Parameters Manager with Phase 3e functionality and v3.1 JSON compatibility
    
    PHASE 3E STEP 5.1 UPDATES:
    - Crisis analysis methods migrated to CrisisAnalyzer for better consolidation
    - Learning methods previously migrated to LearningSystemManager (Step 3)
    - Core analysis parameter functionality preserved
    - Migration references provided for moved methods
    
    Hybrid approach: Preserves all current enhanced functionality while ensuring
    compatibility with Clean v3.1 JSON configuration standards.
    """
    
    def __init__(self, config_manager):
        """
        Initialize Analysis Parameters Manager
        
        Args:
            config_manager: UnifiedConfigManager instance for configuration access
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for AnalysisParametersManager")
        
        self.config_manager = config_manager
        self.analysis_config = {}
        self._full_config = {}
        
        logger.info("✅ AnalysisParametersManager v3.1e-5.1 initialized - Phase 3e Step 5.1 cleanup")
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self):
        """Load analysis parameters configuration with v3.1 compatibility"""
        try:
            # Load analysis parameters via UnifiedConfigManager
            analysis_config_raw = self.config_manager.get_config_section('analysis_parameters', {})
            
            if not analysis_config_raw:
                logger.error("❌ Could not load analysis_parameters.json configuration")
                raise ValueError("Analysis parameters configuration not available")
            
            # Extract analysis system configuration (backward compatibility)
            self.analysis_config = analysis_config_raw.get("analysis_system", {})
            
            # Store the full configuration for access by parameter methods
            self._full_config = analysis_config_raw
            
            # Log v3.1 metadata if available
            metadata = self._full_config.get('_metadata', {})
            config_version = metadata.get('configuration_version', 'unknown')
            compliance = metadata.get('compliance', 'unknown')
            
            logger.info("✅ Analysis parameters loaded from JSON configuration with environment overrides")
            logger.debug(f"📋 Configuration version: {config_version}")
            logger.debug(f"🗒️ Compliance: {compliance}")
            logger.debug(f"🔧 Architecture: {self.analysis_config.get('architecture', 'v3.1')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load analysis parameters: {e}")
            raise ValueError(f"Analysis parameters configuration error: {e}")
    
    # ========================================================================
    # CRISIS ANALYSIS METHODS - PHASE 3E STEP 5.1: MIGRATED TO CRISIS ANALYZER
    # ========================================================================
    
    def get_crisis_thresholds(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 5.1: Crisis threshold management now handled by CrisisAnalyzer
        
        This method has been migrated to CrisisAnalyzer for specialized crisis analysis
        functionality and better consolidation of crisis-related parameters.
        
        Returns:
            Dictionary indicating where to get crisis thresholds
        """
        logger.info("ℹ️ Phase 3e Step 5.1: Crisis thresholds now managed by CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.get_analysis_crisis_thresholds() for crisis threshold configuration")
        
        return {
            'note': 'Crisis thresholds managed by CrisisAnalyzer',
            'use_instead': 'CrisisAnalyzer.get_analysis_crisis_thresholds()',
            'reason': 'Phase 3e Step 5.1 crisis analysis consolidation - moved to specialized crisis analyzer',
            'migration_date': '2025-08-18',
            'phase': '3e.5.1',
            'benefits': [
                'Specialized crisis analysis functionality management',
                'Enhanced crisis threshold processing',
                'Consolidated crisis-related parameters',
                'Better separation of concerns',
                'Improved crisis detection accuracy'
            ]
        }

    def get_analysis_timeouts(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 5.1: Analysis timeout management now handled by CrisisAnalyzer
        
        This method has been migrated to CrisisAnalyzer for specialized timeout
        handling in crisis analysis scenarios.
        
        Returns:
            Dictionary indicating where to get analysis timeouts
        """
        logger.info("ℹ️ Phase 3e Step 5.1: Analysis timeouts now managed by CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.get_analysis_timeouts() for timeout configuration")
        
        return {
            'note': 'Analysis timeouts managed by CrisisAnalyzer',
            'use_instead': 'CrisisAnalyzer.get_analysis_timeouts()',
            'reason': 'Phase 3e Step 5.1 crisis analysis consolidation - moved to specialized crisis analyzer',
            'migration_date': '2025-08-18',
            'phase': '3e.5.1',
            'benefits': [
                'Specialized timeout management for crisis scenarios',
                'Enhanced analysis performance control',
                'Crisis-specific timeout optimization',
                'Better error handling for timeouts',
                'Improved system reliability'
            ]
        }

    def get_confidence_boosts(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 5.1: Confidence boost management now handled by CrisisAnalyzer
        
        This method has been migrated to CrisisAnalyzer for specialized confidence
        boost handling in crisis analysis algorithms.
        
        Returns:
            Dictionary indicating where to get confidence boosts
        """
        logger.info("ℹ️ Phase 3e Step 5.1: Confidence boosts now managed by CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.get_analysis_confidence_boosts() for confidence boost configuration")
        
        return {
            'note': 'Confidence boosts managed by CrisisAnalyzer',
            'use_instead': 'CrisisAnalyzer.get_analysis_confidence_boosts()',
            'reason': 'Phase 3e Step 5.1 crisis analysis consolidation - moved to specialized crisis analyzer',
            'migration_date': '2025-08-18',
            'phase': '3e.5.1',
            'benefits': [
                'Specialized confidence boost algorithms for crisis detection',
                'Enhanced accuracy in crisis analysis',
                'Crisis-specific confidence adjustments',
                'Better false positive/negative handling',
                'Improved crisis detection reliability'
            ]
        }

    def get_pattern_weights(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 5.1: Pattern weight management now handled by CrisisAnalyzer
        
        This method has been migrated to CrisisAnalyzer for specialized pattern
        weighting in crisis analysis scenarios.
        
        Returns:
            Dictionary indicating where to get pattern weights
        """
        logger.info("ℹ️ Phase 3e Step 5.1: Pattern weights now managed by CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.get_analysis_pattern_weights() for pattern weight configuration")
        
        return {
            'note': 'Pattern weights managed by CrisisAnalyzer',
            'use_instead': 'CrisisAnalyzer.get_analysis_pattern_weights()',
            'reason': 'Phase 3e Step 5.1 crisis analysis consolidation - moved to specialized crisis analyzer',
            'migration_date': '2025-08-18',
            'phase': '3e.5.1',
            'benefits': [
                'Specialized pattern weighting for crisis scenarios',
                'Enhanced pattern recognition in crisis detection',
                'Crisis-specific pattern optimization',
                'Better pattern matching accuracy',
                'Improved crisis analysis precision'
            ]
        }

    def get_algorithm_parameters(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 5.1: Algorithm parameter management now handled by CrisisAnalyzer
        
        This method has been migrated to CrisisAnalyzer for specialized algorithm
        parameter management in crisis analysis.
        
        Returns:
            Dictionary indicating where to get algorithm parameters
        """
        logger.info("ℹ️ Phase 3e Step 5.1: Algorithm parameters now managed by CrisisAnalyzer")
        logger.info("💡 Use CrisisAnalyzer.get_analysis_algorithm_parameters() for algorithm parameter configuration")
        
        return {
            'note': 'Algorithm parameters managed by CrisisAnalyzer',
            'use_instead': 'CrisisAnalyzer.get_analysis_algorithm_parameters()',
            'reason': 'Phase 3e Step 5.1 crisis analysis consolidation - moved to specialized crisis analyzer',
            'migration_date': '2025-08-18',
            'phase': '3e.5.1',
            'benefits': [
                'Specialized algorithm parameters for crisis analysis',
                'Enhanced algorithm performance for crisis detection',
                'Crisis-specific algorithm optimization',
                'Better algorithm tuning capabilities',
                'Improved crisis analysis effectiveness'
            ]
        }
    
    # ========================================================================
    # PRESERVED CONFIDENCE BOOST PARAMETERS - Core Algorithm Configuration
    # ========================================================================
    
    def get_confidence_boost_parameters(self) -> Dict[str, float]:
        """
        Get confidence boost parameters for analysis algorithms
        
        NOTE: This method preserves backward compatibility while the specialized
        crisis confidence boosts are handled by CrisisAnalyzer.
        
        Returns:
            Dictionary with confidence boost settings
        """
        try:
            boost_config = self._full_config.get('confidence_boost', {})
            defaults = boost_config.get('defaults', {})
            
            return {
                'high_confidence_boost': float(boost_config.get('high_confidence_boost', defaults.get('high_confidence_boost', 0.15))),
                'medium_confidence_boost': float(boost_config.get('medium_confidence_boost', defaults.get('medium_confidence_boost', 0.10))),
                'low_confidence_boost': float(boost_config.get('low_confidence_boost', defaults.get('low_confidence_boost', 0.05))),
                'pattern_confidence_boost': float(boost_config.get('pattern_confidence_boost', defaults.get('pattern_confidence_boost', 0.05))),
                'model_confidence_boost': float(boost_config.get('model_confidence_boost', defaults.get('model_confidence_boost', 0.0)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading confidence boost parameters: {e}")
            return {
                'high_confidence_boost': 0.15,
                'medium_confidence_boost': 0.10,
                'low_confidence_boost': 0.05,
                'pattern_confidence_boost': 0.05,
                'model_confidence_boost': 0.0
            }
    
    # ========================================================================
    # PHRASE EXTRACTION PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_phrase_extraction_parameters(self) -> Dict[str, Any]:
        """
        Get phrase extraction parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with phrase extraction settings
        """
        try:
            phrase_config = self._full_config.get('phrase_extraction', {})
            defaults = phrase_config.get('defaults', {})
            
            return {
                'min_phrase_length': int(phrase_config.get('min_phrase_length', defaults.get('min_phrase_length', 3))),
                'max_phrase_length': int(phrase_config.get('max_phrase_length', defaults.get('max_phrase_length', 6))),
                'crisis_focus': phrase_config.get('crisis_focus', defaults.get('crisis_focus', True)),
                'community_specific': phrase_config.get('community_specific', defaults.get('community_specific', True)),
                'min_confidence': float(phrase_config.get('min_confidence', defaults.get('min_confidence', 0.3))),
                'max_results': int(phrase_config.get('max_results', defaults.get('max_results', 20)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading phrase extraction parameters: {e}")
            return {
                'min_phrase_length': 3,
                'max_phrase_length': 6,
                'crisis_focus': True,
                'community_specific': True,
                'min_confidence': 0.3,
                'max_results': 20
            }
    
    # ========================================================================
    # PATTERN LEARNING PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_pattern_learning_parameters(self) -> Dict[str, Any]:
        """
        Get pattern learning parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with pattern learning settings
        """
        try:
            learning_config = self._full_config.get('pattern_learning', {})
            defaults = learning_config.get('defaults', {})
            
            return {
                'min_crisis_messages': int(learning_config.get('min_crisis_messages', defaults.get('min_crisis_messages', 10))),
                'max_phrases_to_analyze': int(learning_config.get('max_phrases_to_analyze', defaults.get('max_phrases_to_analyze', 200))),
                'min_distinctiveness_ratio': float(learning_config.get('min_distinctiveness_ratio', defaults.get('min_distinctiveness_ratio', 2.0))),
                'min_frequency': int(learning_config.get('min_frequency', defaults.get('min_frequency', 3))),
                'confidence_thresholds': learning_config.get('confidence_thresholds', defaults.get('confidence_thresholds', {
                    'high_confidence': 0.7,
                    'medium_confidence': 0.4,
                    'low_confidence': 0.1
                }))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading pattern learning parameters: {e}")
            return {
                'min_crisis_messages': 10,
                'max_phrases_to_analyze': 200,
                'min_distinctiveness_ratio': 2.0,
                'min_frequency': 3,
                'confidence_thresholds': {
                    'high_confidence': 0.7,
                    'medium_confidence': 0.4,
                    'low_confidence': 0.1
                }
            }
    
    # ========================================================================
    # SEMANTIC ANALYSIS PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_semantic_analysis_parameters(self) -> Dict[str, Any]:
        """
        Get semantic analysis parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with semantic analysis settings
        """
        try:
            semantic_config = self._full_config.get('semantic_analysis', {})
            defaults = semantic_config.get('defaults', {})
            
            return {
                'context_window': int(semantic_config.get('context_window', defaults.get('context_window', 3))),
                'similarity_threshold': float(semantic_config.get('similarity_threshold', defaults.get('similarity_threshold', 0.75))),
                'context_boost_weight': float(semantic_config.get('context_boost_weight', defaults.get('context_boost_weight', 1.5))),
                'negative_threshold': float(semantic_config.get('negative_threshold', defaults.get('negative_threshold', 0.6))),
                'boost_weights': semantic_config.get('boost_weights', defaults.get('boost_weights', {
                    'high_relevance_boost': 0.1,
                    'medium_relevance_boost': 0.05,
                    'family_rejection_boost': 0.15,
                    'discrimination_fear_boost': 0.15,
                    'support_seeking_boost': -0.05
                }))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading semantic analysis parameters: {e}")
            return {
                'context_window': 3,
                'similarity_threshold': 0.75,
                'context_boost_weight': 1.5,
                'negative_threshold': 0.6,
                'boost_weights': {
                    'high_relevance_boost': 0.1,
                    'medium_relevance_boost': 0.05,
                    'family_rejection_boost': 0.15,
                    'discrimination_fear_boost': 0.15,
                    'support_seeking_boost': -0.05
                }
            }
    
    # ========================================================================
    # CONTEXTUAL WEIGHTING PARAMETERS - NEW v3.1 Support
    # ========================================================================
    
    def get_contextual_weighting_parameters(self) -> Dict[str, Any]:
        """
        Get contextual weighting parameters from v3.1 JSON configuration
        
        NEW METHOD: Added to support v3.1 JSON contextual_weighting section
        
        Returns:
            Dictionary with contextual weighting settings
        """
        try:
            context_config = self._full_config.get('contextual_weighting', {})
            defaults = context_config.get('defaults', {})
            
            return {
                'temporal_context_weight': float(context_config.get('temporal_context_weight', defaults.get('temporal_context_weight', 1.0))),
                'social_context_weight': float(context_config.get('social_context_weight', defaults.get('social_context_weight', 1.2))),
                'context_signal_weight': float(context_config.get('context_signal_weight', defaults.get('context_signal_weight', 0.8))),
                'temporal_urgency_multiplier': float(context_config.get('temporal_urgency_multiplier', defaults.get('temporal_urgency_multiplier', 1.5))),
                'community_awareness_boost': float(context_config.get('community_awareness_boost', defaults.get('community_awareness_boost', 0.3)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading contextual weighting parameters: {e}")
            return {
                'temporal_context_weight': 1.0,
                'social_context_weight': 1.2,
                'context_signal_weight': 0.8,
                'temporal_urgency_multiplier': 1.5,
                'community_awareness_boost': 0.3
            }
    
    # ========================================================================
    # PERFORMANCE AND INTEGRATION PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_performance_parameters(self) -> Dict[str, Any]:
        """
        Get performance and timeout parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with performance settings
        """
        try:
            perf_config = self._full_config.get('performance_settings', {})
            defaults = perf_config.get('defaults', {})
            
            return {
                'timeout_ms': int(perf_config.get('timeout_ms', defaults.get('timeout_ms', 5000))),
                'max_concurrent': int(perf_config.get('max_concurrent', defaults.get('max_concurrent', 10))),
                'enable_caching': perf_config.get('enable_caching', defaults.get('enable_caching', True)),
                'cache_ttl_seconds': int(perf_config.get('cache_ttl_seconds', defaults.get('cache_ttl_seconds', 300))),
                'enable_parallel_processing': perf_config.get('enable_parallel_processing', defaults.get('enable_parallel_processing', True))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading performance parameters: {e}")
            return {
                'timeout_ms': 5000,
                'max_concurrent': 10,
                'enable_caching': True,
                'cache_ttl_seconds': 300,
                'enable_parallel_processing': True
            }
    
    def get_integration_settings(self) -> Dict[str, Any]:
        """
        Get integration settings for pattern analysis from v3.1 JSON configuration
        
        Returns:
            Dictionary with integration settings
        """
        try:
            integration_config = self._full_config.get('integration_settings', {})
            defaults = integration_config.get('defaults', {})
            
            return {
                'enable_pattern_analysis': integration_config.get('enable_pattern_analysis', defaults.get('enable_pattern_analysis', False)),
                'enable_semantic_analysis': integration_config.get('enable_semantic_analysis', defaults.get('enable_semantic_analysis', False)),
                'enable_phrase_extraction': integration_config.get('enable_phrase_extraction', defaults.get('enable_phrase_extraction', False)),
                'enable_pattern_learning': integration_config.get('enable_pattern_learning', defaults.get('enable_pattern_learning', False)),
                'integration_mode': integration_config.get('integration_mode', defaults.get('integration_mode', 'full'))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading integration settings: {e}")
            return {
                'enable_pattern_analysis': False,
                'enable_semantic_analysis': False,
                'enable_phrase_extraction': False,
                'enable_pattern_learning': False,
                'integration_mode': 'full'
            }
    
    # ========================================================================
    # DEBUGGING AND EXPERIMENTAL PARAMETERS - v3.1 Compatible
    # ========================================================================
    
    def get_debugging_settings(self) -> Dict[str, Any]:
        """
        Get debugging and logging settings from v3.1 JSON configuration
        
        Returns:
            Dictionary with debugging settings
        """
        try:
            debug_config = self._full_config.get('debugging_settings', {})
            defaults = debug_config.get('defaults', {})
            
            return {
                'enable_detailed_logging': debug_config.get('enable_detailed_logging', defaults.get('enable_detailed_logging', True)),
                'log_analysis_steps': debug_config.get('log_analysis_steps', defaults.get('log_analysis_steps', False)),
                'include_reasoning': debug_config.get('include_reasoning', defaults.get('include_reasoning', True)),
                'enable_performance_metrics': debug_config.get('enable_performance_metrics', defaults.get('enable_performance_metrics', True)),
                'save_intermediate_results': debug_config.get('save_intermediate_results', defaults.get('save_intermediate_results', False)),
                'enable_timing_metrics': debug_config.get('enable_timing_metrics', defaults.get('enable_timing_metrics', True))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading debugging settings: {e}")
            return {
                'enable_detailed_logging': True,
                'log_analysis_steps': False,
                'include_reasoning': True,
                'enable_performance_metrics': True,
                'save_intermediate_results': False,
                'enable_timing_metrics': True
            }
    
    def get_experimental_features(self) -> Dict[str, Any]:
        """
        Get experimental feature flags from v3.1 JSON configuration
        
        Returns:
            Dictionary with experimental feature settings
        """
        try:
            experimental_config = self._full_config.get('experimental_features', {})
            defaults = experimental_config.get('defaults', {})
            
            return {
                'advanced_context': experimental_config.get('advanced_context', defaults.get('advanced_context', False)),
                'community_vocab': experimental_config.get('community_vocab', defaults.get('community_vocab', True)),
                'temporal_patterns': experimental_config.get('temporal_patterns', defaults.get('temporal_patterns', True)),
                'multi_language': experimental_config.get('multi_language', defaults.get('multi_language', False))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading experimental features: {e}")
            return {
                'advanced_context': False,
                'community_vocab': True,
                'temporal_patterns': True,
                'multi_language': False
            }
    
    # ========================================================================
    # ADVANCED PARAMETERS - Enhanced Functionality
    # ========================================================================

    def get_advanced_parameters(self) -> Dict[str, Any]:
        """
        Get advanced analysis parameters from v3.1 JSON configuration
        
        Returns:
            Dictionary with advanced analysis parameters
        """
        try:
            advanced_config = self._full_config.get('advanced_parameters', {})
            defaults = advanced_config.get('defaults', {})
            
            return {
                'pattern_confidence_boost': float(advanced_config.get('pattern_confidence_boost', defaults.get('pattern_confidence_boost', 0.05))),
                'model_confidence_boost': float(advanced_config.get('model_confidence_boost', defaults.get('model_confidence_boost', 0.0))),
                'context_signal_weight': float(advanced_config.get('context_signal_weight', defaults.get('context_signal_weight', 1.0))),
                'temporal_urgency_multiplier': float(advanced_config.get('temporal_urgency_multiplier', defaults.get('temporal_urgency_multiplier', 1.2))),
                'community_awareness_boost': float(advanced_config.get('community_awareness_boost', defaults.get('community_awareness_boost', 0.1)))
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading advanced parameters: {e}")
            return {
                'pattern_confidence_boost': 0.05,
                'model_confidence_boost': 0.0,
                'context_signal_weight': 1.0,
                'temporal_urgency_multiplier': 1.2,
                'community_awareness_boost': 0.1
            }
    
    # ========================================================================
    # ENSEMBLE WEIGHT ACCESS - PHASE 3D CLEANED: REMOVED DUPLICATE VARIABLES
    # ========================================================================
    
    def get_ensemble_weights(self) -> Dict[str, float]:
        """
        PHASE 3D CLEANED: Get ensemble weights from ModelEnsembleManager instead
        
        Note: This method now refers users to ModelEnsembleManager for ensemble weights.
        The duplicate NLP_ANALYSIS_ENSEMBLE_WEIGHT_* variables have been removed.
        
        Returns:
            Dictionary indicating where to get ensemble weights
        """
        logger.info("ℹ️ Phase 3d: Ensemble weights now managed by ModelEnsembleManager")
        logger.info("💡 Use ModelEnsembleManager.get_model_weights() for ensemble weights")
        
        return {
            'note': 'Ensemble weights managed by ModelEnsembleManager',
            'use_instead': 'ModelEnsembleManager.get_model_weights()',
            'reason': 'Phase 3d duplicate variable cleanup - removed NLP_ANALYSIS_ENSEMBLE_WEIGHT_* variables'
        }
    
    # ========================================================================
    # LEARNING SYSTEM PARAMETERS - PHASE 3E STEP 3 FUNCTIONALITY
    # ========================================================================

    def get_learning_system_parameters(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 3: Learning system parameters now managed by LearningSystemManager
        
        This method has been migrated to LearningSystemManager for better consolidation
        and specialized learning functionality management.
        
        Returns:
            Dictionary indicating where to get learning system parameters
        """
        logger.info("ℹ️ Phase 3e: Learning system parameters now managed by LearningSystemManager")
        logger.info("💡 Use LearningSystemManager.get_learning_parameters() for learning system configuration")
        
        return {
            'note': 'Learning system parameters managed by LearningSystemManager',
            'use_instead': 'LearningSystemManager.get_learning_parameters()',
            'reason': 'Phase 3e Step 3 learning method consolidation - moved to specialized learning manager',
            'migration_date': '2025-08-17',
            'phase': '3e.3',
            'benefits': [
                'Specialized learning functionality management',
                'Enhanced false positive/negative handling',
                'Consolidated learning system configuration',
                'Better separation of concerns',
                'Improved maintainability'
            ]
        }

    def validate_learning_system_parameters(self) -> Dict[str, Any]:
        """
        PHASE 3E STEP 3: Learning system parameter validation now managed by LearningSystemManager
        
        This validation method has been migrated to LearningSystemManager for specialized
        learning parameter validation with enhanced bounds checking.
        
        Returns:
            Dictionary indicating where to get learning system validation
        """
        logger.info("ℹ️ Phase 3e: Learning parameter validation now managed by LearningSystemManager")
        logger.info("💡 Use LearningSystemManager.validate_learning_parameters() for learning system validation")
        
        return {
            'note': 'Learning parameter validation managed by LearningSystemManager', 
            'use_instead': 'LearningSystemManager.validate_learning_parameters()',
            'reason': 'Phase 3e Step 3 learning method consolidation - moved to specialized learning manager',
            'migration_date': '2025-08-17',
            'phase': '3e.3',
            'enhanced_features': [
                'Advanced bounds checking using SharedUtilitiesManager',
                'Comprehensive validation error reporting',
                'Learning-specific parameter range validation',
                'Enhanced error handling and fallbacks',
                'Structured validation results'
            ]
        }
    
    # ========================================================================
    # AGGREGATE ACCESS METHODS - Enhanced for v3.1 with Phase 3e Updates
    # ========================================================================
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all analysis parameters in organized structure
        Enhanced for v3.1 compatibility with Phase 3e Step 5.1 crisis analysis consolidation
        """
        metadata = self._full_config.get('_metadata', {})
        
        return {
            'version': '3.1e-5.1-consolidated',
            'architecture': 'clean-v3.1-crisis-analysis-consolidated', 
            'json_version': metadata.get('configuration_version', 'unknown'),
            'compliance': metadata.get('compliance', 'unknown'),
            'phase_3e_step_5_1_changes': {
                'crisis_analysis_consolidation': 'Crisis analysis methods moved to CrisisAnalyzer',
                'learning_consolidation': 'Learning methods moved to LearningSystemManager (Step 3)',
                'enhanced_specialization': 'Better separation of analysis vs crisis vs learning concerns',
                'consolidated_utilities': 'Uses SharedUtilitiesManager for common operations',
                'preserved_functionality': 'All analysis parameter functionality maintained'
            },
            'migrated_to_crisis_analyzer': {
                'get_crisis_thresholds': 'CrisisAnalyzer.get_analysis_crisis_thresholds()',
                'get_analysis_timeouts': 'CrisisAnalyzer.get_analysis_timeouts()', 
                'get_confidence_boosts': 'CrisisAnalyzer.get_analysis_confidence_boosts()',
                'get_pattern_weights': 'CrisisAnalyzer.get_analysis_pattern_weights()',
                'get_algorithm_parameters': 'CrisisAnalyzer.get_analysis_algorithm_parameters()'
            },
            'preserved_parameters': {
                'confidence_boost': self.get_confidence_boost_parameters(),
                'phrase_extraction': self.get_phrase_extraction_parameters(),
                'pattern_learning': self.get_pattern_learning_parameters(),
                'semantic_analysis': self.get_semantic_analysis_parameters(),
                'contextual_weighting': self.get_contextual_weighting_parameters(),
                'advanced_parameters': self.get_advanced_parameters(),
                'integration_settings': self.get_integration_settings(),
                'performance_settings': self.get_performance_parameters(),
                'debugging_settings': self.get_debugging_settings(),
                'experimental_features': self.get_experimental_features()
            },
            'migration_references': {
                'learning_system_note': self.get_learning_system_parameters(),  # Migration info
                'ensemble_weights_info': self.get_ensemble_weights(),  # Migration info
                'crisis_thresholds_note': self.get_crisis_thresholds(),  # Migration info
                'confidence_boosts_note': self.get_confidence_boosts(),  # Migration info
                'pattern_weights_note': self.get_pattern_weights(),  # Migration info
                'algorithm_parameters_note': self.get_algorithm_parameters(),  # Migration info
                'analysis_timeouts_note': self.get_analysis_timeouts()  # Migration info
            }
        }

    def validate_parameters(self) -> Dict[str, Any]:
        """
        Validate all analysis parameters with v3.1 compliance checks
        Updated for Phase 3e Step 5.1 with crisis analysis migration awareness
        
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        try:
            # Check v3.1 compliance
            metadata = self._full_config.get('_metadata', {})
            if not metadata:
                warnings.append("Missing _metadata section - not fully v3.1 compliant")
            elif metadata.get('configuration_version', '').startswith('3d.'):
                logger.info("✅ Configuration is v3.1 compliant")
            
            # Note about migrated crisis analysis methods
            warnings.append("Phase 3e Step 5.1: Crisis analysis methods migrated to CrisisAnalyzer")
            
            # Validate confidence boost parameters (preserved)
            boost_params = self.get_confidence_boost_parameters()
            for param, value in boost_params.items():
                if not isinstance(value, (int, float)):
                    errors.append(f"Confidence boost parameter '{param}' is not numeric: {value}")
                elif value < 0:
                    warnings.append(f"Confidence boost parameter '{param}' is negative: {value}")
            
            # Validate phrase extraction parameters
            phrase_params = self.get_phrase_extraction_parameters()
            if phrase_params['min_phrase_length'] >= phrase_params['max_phrase_length']:
                errors.append("Phrase min_length must be less than max_length")
            
            # Validate contextual weighting parameters
            context_params = self.get_contextual_weighting_parameters()
            for param, value in context_params.items():
                if not isinstance(value, (int, float)):
                    errors.append(f"Contextual weighting parameter '{param}' is not numeric: {value}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'parameters_validated': 'analysis-parameters-post-crisis-migration',
                'json_compliance': 'v3.1' if metadata else 'partial',
                'phase_3e_step_5_1_status': 'crisis-analysis-methods-migrated',
                'validation_timestamp': str(datetime.now())
            }
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': warnings,
                'parameters_validated': 'partial',
                'validation_timestamp': str(datetime.now())
            }

    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get summary of current configuration for monitoring and debugging
        Enhanced for v3.1 hybrid compatibility with Phase 3e Step 5.1 updates
        
        Returns:
            Dictionary with configuration summary
        """
        try:
            metadata = self._full_config.get('_metadata', {})
            
            return {
                'manager_version': 'v3.1e-5.1-crisis-migrated',
                'json_configuration_version': metadata.get('configuration_version', 'unknown'),
                'json_compliance': metadata.get('compliance', 'unknown'),
                'last_updated': metadata.get('updated_date', 'unknown'),
                'total_parameter_categories': 9,  # Parameter categories after migration
                'migrated_methods': 5,  # Crisis analysis methods migrated to CrisisAnalyzer
                'integration_mode': self.get_integration_settings().get('integration_mode', 'unknown'),
                'performance_timeout_ms': self.get_performance_parameters().get('timeout_ms', 'unknown'),
                'debug_logging_enabled': self.get_debugging_settings().get('enable_detailed_logging', False),
                'contextual_weighting_enabled': True,  # v3.1 feature
                'manager_initialized': True,
                'configuration_loaded': self._full_config is not None,
                'phase_3e_step_5_1_features': {
                    'crisis_analysis_migrated': 'Methods moved to CrisisAnalyzer',
                    'learning_system_migrated': 'Methods moved to LearningSystemManager',
                    'preserved_core_parameters': 'Analysis parameters maintained',
                    'enhanced_specialization': 'Better separation of concerns',
                    'migration_references': 'All moved methods have migration guidance'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting configuration summary: {e}")
            return {
                'manager_version': 'v3.1e-5.1-crisis-migrated',
                'json_configuration_version': 'error',
                'error': str(e),
                'manager_initialized': False
            }

# ============================================================================
# Factory Function - Clean v3.1 Architecture Compliance
# ============================================================================

def create_analysis_parameters_manager(config_manager) -> AnalysisParametersManager:
    """
    Factory function to create AnalysisParametersManager instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        
    Returns:
        AnalysisParametersManager instance with v3.1 compatibility and Phase 3e Step 5.1 updates
    """
    return AnalysisParametersManager(config_manager)

__all__ = ['AnalysisParametersManager', 'create_analysis_parameters_manager']

logger.info("✅ AnalysisParametersManager v3.1e-5.1 loaded - Phase 3e Step 5.1 crisis analysis consolidation complete")