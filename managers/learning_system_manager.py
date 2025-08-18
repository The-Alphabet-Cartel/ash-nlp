# ash-nlp/managers/learning_system_manager.py
"""
Learning System Manager for Ash-NLP Service
FILE VERSION: v3.1-3e-4-3
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 4 - LearningSystemManager Enhancement (Missing Methods Added)
CLEAN ARCHITECTURE: v3.1 Compliant with proper UnifiedConfigManager usage
MIGRATION STATUS: Learning methods extracted from both AnalysisParametersManager and ThresholdMappingManager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

# Import dependencies following Clean v3.1 architecture
from managers.unified_config_manager import UnifiedConfigManager
from managers.shared_utilities import SharedUtilitiesManager

logger = logging.getLogger(__name__)


class LearningSystemManager:
    """
    Consolidated Learning System Manager for False Positive/Negative Management
    
    Manages adaptive threshold adjustments and learning system configuration
    for enhanced crisis detection accuracy through feedback-based learning.
    
    Phase 3e Step 3: Extracted from AnalysisParametersManager and ThresholdMappingManager
    with enhanced threshold adjustment capabilities for comprehensive learning integration.
    
    Core Responsibilities:
    - Learning system parameter access and validation (from AnalysisParametersManager)
    - Learning threshold configuration (from ThresholdMappingManager)
    - False positive/negative threshold adjustments  
    - Learning feedback processing and persistence
    - Threshold drift management and bounds checking
    - Learning system health monitoring and reporting
    """
    
    def __init__(self, unified_config: UnifiedConfigManager, shared_utils: SharedUtilitiesManager):
        """
        Initialize LearningSystemManager with dependency injection (Clean v3.1)
        
        Args:
            unified_config: UnifiedConfigManager instance for configuration access
            shared_utils: SharedUtilitiesManager instance for common utilities
            
        Raises:
            ValueError: If required dependencies are missing or invalid
        """
        if not unified_config:
            raise ValueError("unified_config is required for LearningSystemManager")
        if not shared_utils:
            raise ValueError("shared_utils is required for LearningSystemManager")
            
        # Store dependencies
        self.config_manager = unified_config
        self.shared_utils = shared_utils
        self.logger = logging.getLogger(__name__)
        
        # Learning system state
        self._learning_config = None
        self._validation_errors = []
        self._adjustment_history = []
        self._daily_adjustment_count = 0
        self._last_reset_date = datetime.now().date()
        
        # Load learning system configuration
        self._load_learning_configuration()
        
        self.logger.info("✅ LearningSystemManager v3.1-3e-3.2-3 initialized with Clean v3.1 compliance")
    
    # ========================================================================
    # CORE LEARNING CONFIGURATION - Extracted from AnalysisParametersManager
    # ========================================================================
    
    def _load_learning_configuration(self) -> None:
        """Load learning system configuration from UnifiedConfigManager (FIXED)"""
        try:
            # ✅ FIXED: Use correct UnifiedConfigManager method
            # OLD (BROKEN): self.config_manager.get_analysis_config().get('learning_system', {})
            # NEW (CORRECT): get_config_section() method
            self._learning_config = self.config_manager.get_config_section(
                'analysis_parameters', 'learning_system', {}
            )
            
            if not self._learning_config:
                self.logger.warning("⚠️ No learning_system configuration found, using defaults")
                self._learning_config = self._get_default_learning_config()
            
            self.logger.info("✅ Learning system configuration loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error loading learning configuration: {e}")
            self._learning_config = self._get_default_learning_config()
    
    def _get_default_learning_config(self) -> Dict[str, Any]:
        """Get default learning system configuration with environment variable support"""
        return {
            'enabled': True,
            'learning_rate': 0.01,
            'min_confidence_adjustment': 0.05,
            'max_confidence_adjustment': 0.30,
            'max_adjustments_per_day': 50,
            'persistence_file': './learning_data/adjustments.json',
            'feedback_weight': 0.1,
            'min_samples': 5,
            'adjustment_limit': 0.05,
            'max_drift': 0.1,
            'sensitivity_bounds': {
                'min_global_sensitivity': 0.5,
                'max_global_sensitivity': 1.5
            },
            'adjustment_factors': {
                'false_positive_factor': -0.1,
                'false_negative_factor': 0.1
            },
            'severity_multipliers': {
                'high_severity': 3.0,
                'medium_severity': 2.0,
                'low_severity': 1.0
            }
        }
    
    def get_learning_parameters(self) -> Dict[str, Any]:
        """
        Get complete learning system parameters (FIXED - correct UnifiedConfigManager usage)
        
        Accesses learning configuration via UnifiedConfigManager with environment
        variable overrides following Rule #7 compliance (existing variables only).
        
        Returns:
            Dict containing complete learning system configuration
        """
        try:
            # ✅ FIXED: Use correct UnifiedConfigManager method
            learning_params = self.config_manager.get_config_section(
                'analysis_parameters', 'learning_system', {}
            )
            
            if not learning_params:
                self.logger.warning("⚠️ No learning parameters found, using defaults")
                return self._get_default_learning_config()
            
            # Apply any learning-specific validation
            validated_params = self._validate_learning_parameters(learning_params)
            
            self.logger.info("✅ Learning parameters retrieved successfully")
            return validated_params
            
        except Exception as e:
            self.logger.error(f"❌ Error getting learning parameters: {e}")
            return self._get_default_learning_config()

    def get_learning_thresholds(self) -> Dict[str, float]:
        """
        Get learning-specific threshold configuration (FIXED)
        
        Returns:
            Dict containing learning threshold settings
        """
        try:
            # ✅ FIXED: Use correct UnifiedConfigManager method  
            threshold_config = self.config_manager.get_config_section(
                'threshold_mapping', 'learning_thresholds', {}
            )
            
            if not threshold_config:
                # Fallback to analysis parameters learning section
                learning_config = self.config_manager.get_config_section(
                    'analysis_parameters', 'learning_system', {}
                )
                threshold_config = learning_config.get('thresholds', {})
            
            if not threshold_config:
                self.logger.warning("⚠️ No learning thresholds found, using defaults")
                return {
                    'adjustment_rate': 0.05,
                    'max_adjustment': 0.30,
                    'min_confidence': 0.10,
                    'max_confidence': 0.95
                }
            
            return threshold_config
            
        except Exception as e:
            self.logger.error(f"❌ Error getting learning thresholds: {e}")
            return {
                'adjustment_rate': 0.05,
                'max_adjustment': 0.30,
                'min_confidence': 0.10,
                'max_confidence': 0.95
            }

    def validate_learning_parameters(self) -> Dict[str, Any]:
        """
        Validate learning system parameter ranges and types (Extracted from AnalysisParametersManager)
        
        Returns:
            Dictionary with validation results and any errors/warnings
        """
        try:
            params = self.get_learning_parameters()
            errors = []
            warnings = []
            
            # Validate learning rate
            if not self.shared_utils.validate_range(params['learning_rate'], 0.001, 1.0, 'learning_rate'):
                errors.append(f"Learning rate {params['learning_rate']} outside valid range [0.001, 1.0]")
            
            # Validate confidence adjustments
            if not self.shared_utils.validate_range(params['min_confidence_adjustment'], 0.01, 1.0, 'min_confidence_adjustment'):
                errors.append(f"Min confidence adjustment {params['min_confidence_adjustment']} outside valid range [0.01, 1.0]")
            
            if not self.shared_utils.validate_range(params['max_confidence_adjustment'], 0.01, 1.0, 'max_confidence_adjustment'):
                errors.append(f"Max confidence adjustment {params['max_confidence_adjustment']} outside valid range [0.01, 1.0]")
            
            # Check logical ordering
            if params['min_confidence_adjustment'] >= params['max_confidence_adjustment']:
                errors.append("Min confidence adjustment must be less than max confidence adjustment")
            
            # Validate adjustment limits
            if not self.shared_utils.validate_range(params['max_adjustments_per_day'], 1, 1000, 'max_adjustments_per_day'):
                errors.append(f"Max adjustments per day {params['max_adjustments_per_day']} outside valid range [1, 1000]")
            
            # Validate drift limits
            if not self.shared_utils.validate_range(params['max_drift'], 0.01, 1.0, 'max_drift'):
                errors.append(f"Max drift {params['max_drift']} outside valid range [0.01, 1.0]")
            
            # Validate sensitivity bounds
            bounds = params['sensitivity_bounds']
            if not self.shared_utils.validate_range(bounds['min_global_sensitivity'], 0.1, 2.0, 'min_global_sensitivity'):
                errors.append(f"Min global sensitivity {bounds['min_global_sensitivity']} outside valid range [0.1, 2.0]")
            
            if not self.shared_utils.validate_range(bounds['max_global_sensitivity'], 0.1, 5.0, 'max_global_sensitivity'):
                errors.append(f"Max global sensitivity {bounds['max_global_sensitivity']} outside valid range [0.1, 5.0]")
            
            # Check sensitivity bounds ordering
            if bounds['min_global_sensitivity'] >= bounds['max_global_sensitivity']:
                errors.append("Min global sensitivity must be less than max global sensitivity")
            
            # Validate adjustment factors
            factors = params['adjustment_factors']
            if not self.shared_utils.validate_range(factors['false_positive_factor'], -1.0, 1.0, 'false_positive_factor'):
                errors.append(f"False positive factor {factors['false_positive_factor']} outside valid range [-1.0, 1.0]")
            
            if not self.shared_utils.validate_range(factors['false_negative_factor'], -1.0, 1.0, 'false_negative_factor'):
                errors.append(f"False negative factor {factors['false_negative_factor']} outside valid range [-1.0, 1.0]")
            
            # Validate severity multipliers
            multipliers = params['severity_multipliers']
            for severity, multiplier in multipliers.items():
                if not self.shared_utils.validate_range(multiplier, 0.1, 10.0, f'severity_multiplier_{severity}'):
                    errors.append(f"Severity multiplier {severity} value {multiplier} outside valid range [0.1, 10.0]")
            
            # Check logical ordering of severity multipliers
            if not (multipliers['high_severity'] >= multipliers['medium_severity'] >= multipliers['low_severity']):
                warnings.append("Severity multipliers should follow pattern: high >= medium >= low")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'parameters_validated': len(params),
                'validation_timestamp': str(datetime.now())
            }
            
        except Exception as e:
            error_msg = f"Validation failed: {str(e)}"
            self.logger.error(f"❌ Error validating learning system parameters: {e}")
            return {
                'valid': False,
                'errors': [error_msg],
                'warnings': [],
                'parameters_validated': 0,
                'validation_timestamp': str(datetime.now())
            }

    def _validate_learning_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal validation method that returns parameters with applied validation
        
        Args:
            params: Raw learning parameters to validate
            
        Returns:
            Validated parameters with corrections applied
        """
        try:
            validated_params = params.copy()
            
            # Apply safe conversions and bounds
            validated_params['learning_rate'] = self.shared_utils.safe_float_convert(
                params.get('learning_rate', 0.01), 0.01, 0.001, 1.0, 'learning_rate'
            )
            
            validated_params['min_confidence_adjustment'] = self.shared_utils.safe_float_convert(
                params.get('min_confidence_adjustment', 0.05), 0.05, 0.01, 1.0, 'min_confidence_adjustment'
            )
            
            validated_params['max_confidence_adjustment'] = self.shared_utils.safe_float_convert(
                params.get('max_confidence_adjustment', 0.30), 0.30, 0.01, 1.0, 'max_confidence_adjustment'
            )
            
            validated_params['max_adjustments_per_day'] = self.shared_utils.safe_int_convert(
                params.get('max_adjustments_per_day', 50), 50, 1, 1000, 'max_adjustments_per_day'
            )
            
            # Ensure logical ordering
            if validated_params['min_confidence_adjustment'] >= validated_params['max_confidence_adjustment']:
                validated_params['max_confidence_adjustment'] = validated_params['min_confidence_adjustment'] + 0.05
            
            return validated_params
            
        except Exception as e:
            self.logger.error(f"❌ Error in internal parameter validation: {e}")
            return self._get_default_learning_config()
    
    # ========================================================================
    # NEW MISSING METHODS - Required by CrisisAnalyzer Integration
    # ========================================================================
    
    def adapt_thresholds_for_analysis(self, base_thresholds: Dict[str, float], 
                                     context: Dict[str, Any] = None) -> Dict[str, float]:
        """
        Adapt thresholds based on learning system feedback and context
        
        This is the most critical missing method used throughout CrisisAnalyzer.
        
        Args:
            base_thresholds: Base threshold values to adapt
            context: Analysis context (user, message type, etc.)
            
        Returns:
            Adapted thresholds with learning enhancements
        """
        try:
            if not self.get_learning_parameters().get('enabled', False):
                return base_thresholds
            
            adapted_thresholds = base_thresholds.copy()
            learning_params = self.get_learning_parameters()
            
            # Apply learning-based adaptations
            for threshold_name, base_value in base_thresholds.items():
                # Get historical performance for this threshold
                historical_performance = self._get_threshold_performance(threshold_name, context)
                
                # Calculate adaptation based on recent performance
                if historical_performance:
                    false_positive_rate = historical_performance.get('false_positive_rate', 0.0)
                    false_negative_rate = historical_performance.get('false_negative_rate', 0.0)
                    
                    # Adapt based on error rates
                    adaptation_factor = 0.0
                    if false_positive_rate > 0.1:  # Too many false positives - increase threshold
                        adaptation_factor = min(0.1, false_positive_rate * learning_params['learning_rate'])
                    elif false_negative_rate > 0.1:  # Too many false negatives - decrease threshold
                        adaptation_factor = -min(0.1, false_negative_rate * learning_params['learning_rate'])
                    
                    # Apply adaptation with bounds
                    adapted_value = base_value + adaptation_factor
                    adapted_thresholds[threshold_name] = self._apply_threshold_bounds(adapted_value, learning_params)
            
            self.logger.info(f"✅ Thresholds adapted for analysis with learning enhancements")
            return adapted_thresholds
            
        except Exception as e:
            self.logger.error(f"❌ Error adapting thresholds for analysis: {e}")
            return base_thresholds
    
    def enhance_analysis_results(self, analysis_results: Dict[str, Any], 
                               context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhance analysis results with learning system insights
        
        Args:
            analysis_results: Base analysis results from ensemble
            context: Analysis context for enhancement
            
        Returns:
            Enhanced results with learning metadata
        """
        try:
            enhanced_results = analysis_results.copy()
            
            if not self.get_learning_parameters().get('enabled', False):
                enhanced_results['learning_enhanced'] = False
                return enhanced_results
            
            # Add learning confidence adjustments
            if 'confidence' in analysis_results:
                base_confidence = analysis_results['confidence']
                confidence_boost = self._calculate_confidence_boost(base_confidence, context)
                enhanced_results['confidence'] = min(1.0, base_confidence + confidence_boost)
                enhanced_results['confidence_boost_applied'] = confidence_boost
            
            # Add learning metadata
            enhanced_results['learning_enhanced'] = True
            enhanced_results['learning_insights'] = self.get_context_insights(context)
            enhanced_results['enhancement_timestamp'] = datetime.now().isoformat()
            
            self.logger.info("✅ Analysis results enhanced with learning system")
            return enhanced_results
            
        except Exception as e:
            self.logger.error(f"❌ Error enhancing analysis results: {e}")
            enhanced_results = analysis_results.copy()
            enhanced_results['learning_enhanced'] = False
            enhanced_results['enhancement_error'] = str(e)
            return enhanced_results
    
    def adjust_thresholds_for_context(self, thresholds: Dict[str, float], 
                                    context: Dict[str, Any]) -> Dict[str, float]:
        """
        Adjust thresholds based on specific context (user, time, message type)
        
        Args:
            thresholds: Base thresholds to adjust
            context: Context information for adjustment
            
        Returns:
            Context-adjusted thresholds
        """
        try:
            if not context or not self.get_learning_parameters().get('enabled', False):
                return thresholds
            
            adjusted_thresholds = thresholds.copy()
            
            # Context-based adjustments
            user_id = context.get('user_id')
            message_type = context.get('message_type', 'default')
            time_of_day = context.get('time_of_day')
            
            # User-specific adjustments based on history
            if user_id:
                user_adjustments = self._get_user_threshold_adjustments(user_id)
                for threshold_name, adjustment in user_adjustments.items():
                    if threshold_name in adjusted_thresholds:
                        adjusted_thresholds[threshold_name] += adjustment
            
            # Message type adjustments
            if message_type == 'urgent':
                # Lower thresholds for urgent messages (more sensitive)
                for key in adjusted_thresholds:
                    adjusted_thresholds[key] *= 0.9
            elif message_type == 'casual':
                # Higher thresholds for casual messages (less sensitive)
                for key in adjusted_thresholds:
                    adjusted_thresholds[key] *= 1.1
            
            # Apply bounds to all adjusted thresholds
            learning_params = self.get_learning_parameters()
            for key, value in adjusted_thresholds.items():
                adjusted_thresholds[key] = self._apply_threshold_bounds(value, learning_params)
            
            self.logger.info(f"✅ Thresholds adjusted for context: {list(context.keys())}")
            return adjusted_thresholds
            
        except Exception as e:
            self.logger.error(f"❌ Error adjusting thresholds for context: {e}")
            return thresholds
    
    def get_context_insights(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get learning-based insights for the given context
        
        Args:
            context: Analysis context
            
        Returns:
            Learning insights and recommendations
        """
        try:
            insights = {
                'context_analyzed': bool(context),
                'learning_active': self.get_learning_parameters().get('enabled', False),
                'insights_generated': datetime.now().isoformat()
            }
            
            if not context or not insights['learning_active']:
                insights['recommendations'] = []
                return insights
            
            recommendations = []
            
            # Analyze context patterns
            user_id = context.get('user_id')
            if user_id:
                user_history = self._get_user_analysis_history(user_id)
                if user_history:
                    recent_false_positives = user_history.get('recent_false_positives', 0)
                    recent_false_negatives = user_history.get('recent_false_negatives', 0)
                    
                    if recent_false_positives > 3:
                        recommendations.append({
                            'type': 'threshold_adjustment',
                            'reason': 'High false positive rate for user',
                            'suggestion': 'Consider increasing thresholds'
                        })
                    
                    if recent_false_negatives > 2:
                        recommendations.append({
                            'type': 'threshold_adjustment', 
                            'reason': 'Recent false negatives detected',
                            'suggestion': 'Consider decreasing thresholds'
                        })
            
            insights['recommendations'] = recommendations
            insights['context_factors_analyzed'] = list(context.keys())
            
            return insights
            
        except Exception as e:
            self.logger.error(f"❌ Error getting context insights: {e}")
            return {
                'context_analyzed': False,
                'learning_active': False,
                'error': str(e),
                'insights_generated': datetime.now().isoformat()
            }
    
    def adapt_confidence_boosts(self, base_boosts: Dict[str, float], 
                               context: Dict[str, Any] = None) -> Dict[str, float]:
        """
        Adapt confidence boosts based on learning system feedback
        
        Args:
            base_boosts: Base confidence boost values
            context: Analysis context
            
        Returns:
            Adapted confidence boosts
        """
        try:
            if not self.get_learning_parameters().get('enabled', False):
                return base_boosts
            
            adapted_boosts = base_boosts.copy()
            learning_params = self.get_learning_parameters()
            
            # Apply learning-based boost adaptations
            for boost_name, base_value in base_boosts.items():
                # Get effectiveness data for this boost type
                boost_effectiveness = self._get_boost_effectiveness(boost_name, context)
                
                if boost_effectiveness:
                    effectiveness_score = boost_effectiveness.get('effectiveness_score', 1.0)
                    
                    # Adapt boost based on effectiveness
                    if effectiveness_score > 1.2:  # Very effective - increase boost
                        adaptation = base_value * 0.1 * learning_params['learning_rate']
                        adapted_boosts[boost_name] = min(0.5, base_value + adaptation)
                    elif effectiveness_score < 0.8:  # Less effective - decrease boost
                        adaptation = base_value * 0.1 * learning_params['learning_rate']
                        adapted_boosts[boost_name] = max(0.0, base_value - adaptation)
            
            self.logger.info("✅ Confidence boosts adapted based on learning")
            return adapted_boosts
            
        except Exception as e:
            self.logger.error(f"❌ Error adapting confidence boosts: {e}")
            return base_boosts
    
    def adapt_ensemble_weights(self, base_weights: Dict[str, float], 
                             context: Dict[str, Any] = None) -> Dict[str, float]:
        """
        Adapt ensemble model weights based on learning system performance data
        
        Args:
            base_weights: Base ensemble weights
            context: Analysis context
            
        Returns:
            Learning-adapted ensemble weights
        """
        try:
            if not self.get_learning_parameters().get('enabled', False):
                return base_weights
            
            adapted_weights = base_weights.copy()
            learning_params = self.get_learning_parameters()
            
            # Get model performance data
            total_weight = 0.0
            for model_name, base_weight in base_weights.items():
                model_performance = self._get_model_performance(model_name, context)
                
                if model_performance:
                    accuracy = model_performance.get('accuracy', 0.8)
                    false_positive_rate = model_performance.get('false_positive_rate', 0.1)
                    false_negative_rate = model_performance.get('false_negative_rate', 0.1)
                    
                    # Calculate performance score
                    performance_score = accuracy - (false_positive_rate + false_negative_rate) * 0.5
                    
                    # Adapt weight based on performance
                    weight_adjustment = (performance_score - 0.8) * learning_params['learning_rate']
                    adapted_weights[model_name] = max(0.01, base_weight + weight_adjustment)
                
                total_weight += adapted_weights[model_name]
            
            # Normalize weights to sum to 1.0
            if total_weight > 0:
                for model_name in adapted_weights:
                    adapted_weights[model_name] /= total_weight
            
            self.logger.info("✅ Ensemble weights adapted based on learning data")
            return adapted_weights
            
        except Exception as e:
            self.logger.error(f"❌ Error adapting ensemble weights: {e}")
            return base_weights
    
    # ========================================================================
    # LEARNING DATA HELPERS - Support methods for new functionality
    # ========================================================================
    
    def _get_threshold_performance(self, threshold_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get historical performance data for a threshold"""
        try:
            # This would integrate with persistent learning data storage
            # For now, return mock data based on recent adjustments
            recent_adjustments = [adj for adj in self._adjustment_history 
                                if 'threshold_name' in adj and adj['threshold_name'] == threshold_name]
            
            if not recent_adjustments:
                return {}
            
            false_positive_count = len([adj for adj in recent_adjustments if adj['type'] == 'false_positive'])
            false_negative_count = len([adj for adj in recent_adjustments if adj['type'] == 'false_negative'])
            total_count = len(recent_adjustments)
            
            return {
                'false_positive_rate': false_positive_count / max(1, total_count),
                'false_negative_rate': false_negative_count / max(1, total_count),
                'sample_size': total_count
            }
        except Exception as e:
            self.logger.error(f"❌ Error getting threshold performance: {e}")
            return {}
    
    def _calculate_confidence_boost(self, base_confidence: float, context: Dict[str, Any] = None) -> float:
        """Calculate confidence boost based on learning data"""
        try:
            if not context:
                return 0.0
            
            # Base boost calculation
            boost = 0.0
            
            # User-specific confidence patterns
            user_id = context.get('user_id')
            if user_id:
                user_confidence_history = self._get_user_confidence_history(user_id)
                if user_confidence_history:
                    avg_accuracy = user_confidence_history.get('average_accuracy', 0.8)
                    if avg_accuracy > 0.9:
                        boost += 0.05  # Reliable user patterns
                    elif avg_accuracy < 0.7:
                        boost -= 0.03  # Less reliable patterns
            
            # Context-based confidence boosts
            message_urgency = context.get('urgency_level', 'medium')
            if message_urgency == 'high':
                boost += 0.02  # Slight boost for urgent messages
            
            return max(-0.1, min(0.1, boost))  # Cap boost at ±0.1
            
        except Exception as e:
            self.logger.error(f"❌ Error calculating confidence boost: {e}")
            return 0.0
    
    def _get_user_threshold_adjustments(self, user_id: str) -> Dict[str, float]:
        """Get user-specific threshold adjustments based on history"""
        try:
            # This would integrate with user-specific learning data
            # For now, return empty dict (no user-specific adjustments)
            return {}
        except Exception as e:
            self.logger.error(f"❌ Error getting user threshold adjustments: {e}")
            return {}
    
    def _get_user_analysis_history(self, user_id: str) -> Dict[str, Any]:
        """Get user analysis history for insights"""
        try:
            # This would integrate with user analysis tracking
            # For now, return basic mock data
            return {
                'recent_false_positives': 1,
                'recent_false_negatives': 0,
                'total_analyses': 10
            }
        except Exception as e:
            self.logger.error(f"❌ Error getting user analysis history: {e}")
            return {}
    
    def _get_boost_effectiveness(self, boost_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get effectiveness data for confidence boosts"""
        try:
            # This would integrate with boost effectiveness tracking
            # For now, return neutral effectiveness
            return {'effectiveness_score': 1.0}
        except Exception as e:
            self.logger.error(f"❌ Error getting boost effectiveness: {e}")
            return {}
    
    def _get_model_performance(self, model_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get model performance data for ensemble weight adaptation"""
        try:
            # This would integrate with model performance tracking
            # For now, return baseline performance data
            return {
                'accuracy': 0.8,
                'false_positive_rate': 0.1,
                'false_negative_rate': 0.1
            }
        except Exception as e:
            self.logger.error(f"❌ Error getting model performance: {e}")
            return {}
    
    def _get_user_confidence_history(self, user_id: str) -> Dict[str, Any]:
        """Get user confidence pattern history"""
        try:
            # This would integrate with user confidence tracking
            # For now, return baseline data
            return {'average_accuracy': 0.8}
        except Exception as e:
            self.logger.error(f"❌ Error getting user confidence history: {e}")
            return {}
    
    # ========================================================================
    # THRESHOLD ADJUSTMENT METHODS - Existing functionality
    # ========================================================================
    
    def adjust_threshold_for_false_positive(self, current_threshold: float, 
                                          crisis_level: str = "medium") -> Dict[str, Any]:
        """
        Adjust threshold after false positive detection
        
        Reduces sensitivity to prevent similar false positives while maintaining
        crisis detection capability.
        
        Args:
            current_threshold: Current threshold value
            crisis_level: Crisis level for severity-based adjustment
            
        Returns:
            Dictionary with adjustment results and new threshold
        """
        try:
            if not self._can_make_adjustment():
                return self._generate_adjustment_result(
                    current_threshold, current_threshold, 
                    "Daily adjustment limit reached", False
                )
            
            params = self.get_learning_parameters()
            
            # Calculate adjustment amount
            base_adjustment = params['adjustment_factors']['false_positive_factor']
            severity_multiplier = params['severity_multipliers'].get(f'{crisis_level}_severity', 2.0)
            learning_rate = params['learning_rate']
            
            adjustment_amount = base_adjustment * severity_multiplier * learning_rate
            new_threshold = current_threshold + adjustment_amount
            
            # Apply bounds and drift limits BEFORE recording
            bounded_threshold = self._apply_threshold_bounds(new_threshold, params)
            final_adjustment = bounded_threshold - current_threshold
            drift = abs(final_adjustment)
            
            # Check drift limits
            if drift > params['max_drift']:
                direction = -1 if adjustment_amount < 0 else 1
                bounded_threshold = current_threshold + (params['max_drift'] * direction)
                bounded_threshold = self._apply_threshold_bounds(bounded_threshold, params)
                final_adjustment = bounded_threshold - current_threshold
                drift = abs(final_adjustment)
            
            # Only record adjustment if there's an actual change
            if abs(final_adjustment) > 0.0001:  # Avoid floating point precision issues
                self._record_adjustment("false_positive", current_threshold, bounded_threshold, 
                                      final_adjustment, crisis_level)
                
                return self._generate_adjustment_result(
                    current_threshold, bounded_threshold, 
                    f"Threshold reduced for false positive ({crisis_level} severity)", True,
                    final_adjustment, drift
                )
            else:
                return self._generate_adjustment_result(
                    current_threshold, current_threshold, 
                    "No adjustment needed - threshold already at optimal value", False
                )
            
        except Exception as e:
            self.logger.error(f"❌ Error in false positive adjustment: {e}")
            return self._generate_adjustment_result(
                current_threshold, current_threshold, 
                f"Adjustment failed: {str(e)}", False
            )
    
    def adjust_threshold_for_false_negative(self, current_threshold: float, 
                                          crisis_level: str = "medium") -> Dict[str, Any]:
        """
        Adjust threshold after false negative detection
        
        Increases sensitivity to catch similar crises while preventing
        over-sensitivity.
        
        Args:
            current_threshold: Current threshold value
            crisis_level: Crisis level for severity-based adjustment
            
        Returns:
            Dictionary with adjustment results and new threshold
        """
        try:
            if not self._can_make_adjustment():
                return self._generate_adjustment_result(
                    current_threshold, current_threshold, 
                    "Daily adjustment limit reached", False
                )
            
            params = self.get_learning_parameters()
            
            # Calculate adjustment amount
            base_adjustment = params['adjustment_factors']['false_negative_factor']
            severity_multiplier = params['severity_multipliers'].get(f'{crisis_level}_severity', 2.0)
            learning_rate = params['learning_rate']
            
            adjustment_amount = base_adjustment * severity_multiplier * learning_rate
            new_threshold = current_threshold + adjustment_amount
            
            # Apply bounds and drift limits BEFORE recording
            bounded_threshold = self._apply_threshold_bounds(new_threshold, params)
            final_adjustment = bounded_threshold - current_threshold
            drift = abs(final_adjustment)
            
            # Check drift limits
            if drift > params['max_drift']:
                direction = 1 if adjustment_amount > 0 else -1
                bounded_threshold = current_threshold + (params['max_drift'] * direction)
                bounded_threshold = self._apply_threshold_bounds(bounded_threshold, params)
                final_adjustment = bounded_threshold - current_threshold
                drift = abs(final_adjustment)
            
            # Only record adjustment if there's an actual change
            if abs(final_adjustment) > 0.0001:  # Avoid floating point precision issues
                self._record_adjustment("false_negative", current_threshold, bounded_threshold, 
                                      final_adjustment, crisis_level)
                
                return self._generate_adjustment_result(
                    current_threshold, bounded_threshold, 
                    f"Threshold increased for false negative ({crisis_level} severity)", True,
                    final_adjustment, drift
                )
            else:
                return self._generate_adjustment_result(
                    current_threshold, current_threshold, 
                    "No adjustment needed - threshold already at optimal value", False
                )
            
        except Exception as e:
            self.logger.error(f"❌ Error in false negative adjustment: {e}")
            return self._generate_adjustment_result(
                current_threshold, current_threshold, 
                f"Adjustment failed: {str(e)}", False
            )
    
    def process_learning_feedback(self, feedback_type: str, current_thresholds: Dict[str, float], 
                                crisis_level: str = "medium", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process learning feedback and adjust multiple thresholds
        
        Args:
            feedback_type: 'false_positive', 'false_negative', or 'correct'
            current_thresholds: Dictionary of threshold names and values
            crisis_level: Crisis level for severity-based adjustment
            context: Additional context for learning
            
        Returns:
            Dictionary with adjustment results for all thresholds
        """
        try:
            if feedback_type == "correct":
                return {
                    'feedback_type': feedback_type,
                    'adjustments_made': 0,
                    'message': 'No adjustment needed for correct classification',
                    'thresholds': current_thresholds
                }
            
            results = {
                'feedback_type': feedback_type,
                'original_thresholds': current_thresholds.copy(),
                'adjusted_thresholds': {},
                'adjustments_made': 0,
                'results': {}
            }
            
            for threshold_name, threshold_value in current_thresholds.items():
                if feedback_type == "false_positive":
                    adjustment_result = self.adjust_threshold_for_false_positive(threshold_value, crisis_level)
                elif feedback_type == "false_negative":
                    adjustment_result = self.adjust_threshold_for_false_negative(threshold_value, crisis_level)
                else:
                    adjustment_result = self._generate_adjustment_result(
                        threshold_value, threshold_value, 
                        f"Unknown feedback type: {feedback_type}", False
                    )
                
                results['results'][threshold_name] = adjustment_result
                results['adjusted_thresholds'][threshold_name] = adjustment_result['new_threshold']
                
                if adjustment_result['adjusted']:
                    results['adjustments_made'] += 1
            
            return results
            
        except Exception as e:
            return self.shared_utils.handle_error_with_fallback(
                e, {
                    'feedback_type': feedback_type,
                    'error': str(e),
                    'adjustments_made': 0,
                    'thresholds': current_thresholds
                },
                "learning_feedback_processing", "process_learning_feedback"
            )
    
    # ========================================================================
    # LEARNING SYSTEM UTILITIES AND HELPERS
    # ========================================================================
    
    def _can_make_adjustment(self) -> bool:
        """Check if daily adjustment limit allows new adjustment"""
        try:
            self._reset_daily_count_if_needed()
            params = self.get_learning_parameters()
            return self._daily_adjustment_count < params['max_adjustments_per_day']
        except Exception as e:
            # If we can't load parameters, don't allow adjustments
            self.logger.warning(f"⚠️ Cannot verify adjustment limits, blocking adjustment: {e}")
            return False
    
    def _reset_daily_count_if_needed(self) -> None:
        """Reset daily adjustment count if new day"""
        today = datetime.now().date()
        if today > self._last_reset_date:
            self._daily_adjustment_count = 0
            self._last_reset_date = today
            self.logger.info(f"✅ Daily adjustment count reset for {today}")
    
    def _apply_threshold_bounds(self, threshold: float, params: Dict[str, Any]) -> float:
        """Apply sensitivity bounds to threshold value with strict enforcement"""
        try:
            bounds = params['sensitivity_bounds']
            min_threshold = bounds['min_global_sensitivity']
            max_threshold = bounds['max_global_sensitivity']
            
            # Strict bounds enforcement
            bounded_value = max(min_threshold, min(threshold, max_threshold))
            
            # Log bounds enforcement if applied
            if bounded_value != threshold:
                self.logger.debug(f"🔒 Bounds enforced: {threshold:.4f} → {bounded_value:.4f} "
                                f"[{min_threshold}, {max_threshold}]")
            
            return bounded_value
            
        except Exception as e:
            self.logger.error(f"❌ Error applying threshold bounds: {e}")
            # Return safe fallback value
            return max(0.1, min(threshold, 2.0))
    
    def _record_adjustment(self, adjustment_type: str, old_threshold: float, 
                          new_threshold: float, adjustment_amount: float, 
                          crisis_level: str) -> None:
        """Record threshold adjustment for history tracking"""
        try:
            adjustment_record = {
                'timestamp': datetime.now().isoformat(),
                'type': adjustment_type,
                'crisis_level': crisis_level,
                'old_threshold': old_threshold,
                'new_threshold': new_threshold,
                'adjustment_amount': adjustment_amount,
                'daily_count': self._daily_adjustment_count + 1
            }
            
            self._adjustment_history.append(adjustment_record)
            self._daily_adjustment_count += 1
            
            # Keep only last 1000 adjustments to prevent memory issues
            if len(self._adjustment_history) > 1000:
                self._adjustment_history = self._adjustment_history[-1000:]
                
        except Exception as e:
            self.logger.error(f"❌ Error recording adjustment: {e}")
    
    def _generate_adjustment_result(self, old_threshold: float, new_threshold: float, 
                                  message: str, adjusted: bool, adjustment_amount: float = 0.0, 
                                  drift: float = 0.0) -> Dict[str, Any]:
        """Generate standardized adjustment result dictionary"""
        return {
            'old_threshold': old_threshold,
            'new_threshold': new_threshold,
            'adjustment_amount': adjustment_amount,
            'drift': drift,
            'adjusted': adjusted,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'daily_adjustments_remaining': self.get_remaining_daily_adjustments()
        }
    
    # ========================================================================
    # LEARNING SYSTEM STATUS AND MONITORING
    # ========================================================================
    
    def get_learning_system_status(self) -> Dict[str, Any]:
        """Get comprehensive learning system status"""
        try:
            params = self.get_learning_parameters()
            validation = self.validate_learning_parameters()
            
            return {
                'enabled': params['enabled'],
                'validation_status': validation['valid'],
                'validation_errors': validation['errors'],
                'validation_warnings': validation['warnings'],
                'daily_adjustments_made': self._daily_adjustment_count,
                'daily_adjustments_remaining': self.get_remaining_daily_adjustments(),
                'total_adjustments_in_history': len(self._adjustment_history),
                'last_adjustment': self._adjustment_history[-1] if self._adjustment_history else None,
                'learning_rate': params['learning_rate'],
                'sensitivity_bounds': params['sensitivity_bounds'],
                'adjustment_factors': params['adjustment_factors'],
                'status_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return self.shared_utils.handle_error_with_fallback(
                e, {
                    'enabled': False,
                    'error': str(e),
                    'status_timestamp': datetime.now().isoformat()
                },
                "learning_system_status", "get_learning_system_status"
            )
    
    def get_remaining_daily_adjustments(self) -> int:
        """Get remaining adjustment count for today"""
        try:
            self._reset_daily_count_if_needed()
            params = self.get_learning_parameters()
            return max(0, params['max_adjustments_per_day'] - self._daily_adjustment_count)
        except Exception as e:
            # Return safe default when parameter loading fails
            self.logger.warning(f"⚠️ Could not get remaining adjustments, using default: {e}")
            return max(0, 50 - self._daily_adjustment_count)  # Default max_adjustments_per_day = 50
    
    def get_adjustment_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent adjustment history"""
        return self._adjustment_history[-limit:] if self._adjustment_history else []
    
    def clear_adjustment_history(self) -> Dict[str, Any]:
        """Clear adjustment history (admin function)"""
        try:
            count = len(self._adjustment_history)
            self._adjustment_history.clear()
            
            return {
                'cleared': True,
                'records_cleared': count,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return self.shared_utils.handle_error_with_fallback(
                e, {
                    'cleared': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                },
                "clear_adjustment_history", "clear_adjustment_history"
            )
    
    # ========================================================================
    # LEARNING SYSTEM HEALTH AND VALIDATION
    # ========================================================================
    
    def validate_threshold_adjustments(self, thresholds: Dict[str, float]) -> Dict[str, Any]:
        """
        Validate proposed threshold adjustments against learning system bounds
        
        Args:
            thresholds: Dictionary of threshold names and proposed values
            
        Returns:
            Validation results with any bound violations
        """
        try:
            params = self.get_learning_parameters()
            bounds = params['sensitivity_bounds']
            
            results = {
                'valid': True,
                'violations': [],
                'warnings': [],
                'validated_thresholds': {}
            }
            
            for name, value in thresholds.items():
                # Apply bounds checking
                bounded_value = self._apply_threshold_bounds(value, params)
                results['validated_thresholds'][name] = bounded_value
                
                # Check for violations
                if bounded_value != value:
                    violation = {
                        'threshold': name,
                        'original_value': value,
                        'bounded_value': bounded_value,
                        'reason': f"Value {value} outside bounds [{bounds['min_global_sensitivity']}, {bounds['max_global_sensitivity']}]"
                    }
                    results['violations'].append(violation)
                    results['valid'] = False
            
            return results
            
        except Exception as e:
            return self.shared_utils.handle_error_with_fallback(
                e, {
                    'valid': False,
                    'error': str(e),
                    'violations': [],
                    'validated_thresholds': {}
                },
                "threshold_validation", "validate_threshold_adjustments"
            )
    
    def get_learning_health_check(self) -> Dict[str, Any]:
        """Comprehensive learning system health check"""
        try:
            params = self.get_learning_parameters()
            validation = self.validate_learning_parameters()
            status = self.get_learning_system_status()
            
            # Determine health status
            health_score = 100
            issues = []
            
            if not validation['valid']:
                health_score -= 30
                issues.extend(validation['errors'])
            
            if validation['warnings']:
                health_score -= 10
                issues.extend(validation['warnings'])
            
            if self.get_remaining_daily_adjustments() < 5:
                health_score -= 20
                issues.append("Low remaining daily adjustments")
            
            if not params['enabled']:
                health_score = 0
                issues.append("Learning system disabled")
            
            health_status = "excellent" if health_score >= 90 else \
                           "good" if health_score >= 70 else \
                           "warning" if health_score >= 50 else "critical"
            
            return {
                'health_status': health_status,
                'health_score': health_score,
                'issues': issues,
                'enabled': params['enabled'],
                'validation_passed': validation['valid'],
                'daily_adjustments_available': self.get_remaining_daily_adjustments() > 0,
                'configuration_valid': len(validation['errors']) == 0,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return self.shared_utils.handle_error_with_fallback(
                e, {
                    'health_status': 'critical',
                    'health_score': 0,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                },
                "learning_health_check", "get_learning_health_check"
            )


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_learning_system_manager(unified_config: UnifiedConfigManager = None, 
                                 shared_utils: SharedUtilitiesManager = None) -> LearningSystemManager:
    """
    Factory function to create LearningSystemManager with dependency injection (Clean v3.1)
    
    Args:
        unified_config: UnifiedConfigManager instance (required)
        shared_utils: SharedUtilitiesManager instance (required)
        
    Returns:
        LearningSystemManager: Configured manager instance
        
    Raises:
        ValueError: If required dependencies are missing
    """
    if not unified_config:
        raise ValueError("unified_config is required for LearningSystemManager")
    if not shared_utils:
        raise ValueError("shared_utils is required for LearningSystemManager")
    
    return LearningSystemManager(unified_config, shared_utils)


# ============================================================================
# CLEAN ARCHITECTURE EXPORTS
# ============================================================================

__all__ = [
    'LearningSystemManager',
    'create_learning_system_manager'
]

logger.info("✅ LearningSystemManager v3.1-3e-3.2-3 loaded - Complete learning system with missing methods added for CrisisAnalyzer integration")