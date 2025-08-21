# ash-nlp/managers/learning_system_manager.py
"""
Learning System Manager for Ash-NLP Service
FILE VERSION: v3.1-3e-5.5-6-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 3.2 - LearningSystemManager Implementation (Corrected)
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
        
        self.logger.info("✅ LearningSystemManager v3.1-3e-3.2-2 initialized with Clean v3.1 compliance")
    
    # ========================================================================
    # CORE LEARNING CONFIGURATION - Extracted from AnalysisParametersManager
    # ========================================================================
    
    def _load_learning_configuration(self) -> None:
        """Load learning system configuration from UnifiedConfigManager"""
        try:
            # Access learning configuration through UnifiedConfigManager
            self._learning_config = self.config_manager.get_config_section('learning_system', 'learning_configuration', {})
            
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
        Get complete learning system parameters (Extracted from AnalysisParametersManager)
        
        Accesses learning configuration via UnifiedConfigManager with environment
        variable overrides following Rule #7 compliance (existing variables only).
        
        Returns:
            Dictionary with complete learning system configuration
        """
        try:
            learning_config = self._learning_config or {}
            defaults = learning_config.get('defaults', {})
            
            # Build core parameters using existing environment variables
            core_params = {
                'enabled': self.shared_utils.safe_bool_convert(
                    learning_config.get('enabled', defaults.get('enabled', True)),
                    default=True,
                    param_name='learning_enabled'
                ),
                'learning_rate': self.shared_utils.safe_float_convert(
                    learning_config.get('learning_rate', defaults.get('learning_rate', 0.01)),
                    default=0.01,
                    min_val=0.0001,
                    max_val=1.0,
                    param_name='learning_rate'
                ),
                'min_confidence_adjustment': self.shared_utils.safe_float_convert(
                    learning_config.get('min_confidence_adjustment', defaults.get('min_confidence_adjustment', 0.05)),
                    default=0.05,
                    min_val=0.01,
                    max_val=1.0,
                    param_name='min_confidence_adjustment'
                ),
                'max_confidence_adjustment': self.shared_utils.safe_float_convert(
                    learning_config.get('max_confidence_adjustment', defaults.get('max_confidence_adjustment', 0.30)),
                    default=0.30,
                    min_val=0.01,
                    max_val=1.0,
                    param_name='max_confidence_adjustment'
                ),
                'max_adjustments_per_day': self.shared_utils.safe_int_convert(
                    learning_config.get('max_adjustments_per_day', defaults.get('max_adjustments_per_day', 50)),
                    default=50,
                    min_val=1,
                    max_val=1000,
                    param_name='max_adjustments_per_day'
                ),
                'persistence_file': learning_config.get('persistence_file', 
                                                       defaults.get('persistence_file', './learning_data/adjustments.json')),
                'feedback_weight': self.shared_utils.safe_float_convert(
                    learning_config.get('feedback_weight', defaults.get('feedback_weight', 0.1)),
                    default=0.1,
                    min_val=0.0,
                    max_val=1.0,
                    param_name='feedback_weight'
                ),
                'min_samples': self.shared_utils.safe_int_convert(
                    learning_config.get('min_samples', defaults.get('min_samples', 5)),
                    default=5,
                    min_val=1,
                    max_val=100,
                    param_name='min_samples'
                ),
                'adjustment_limit': self.shared_utils.safe_float_convert(
                    learning_config.get('adjustment_limit', defaults.get('adjustment_limit', 0.05)),
                    default=0.05,
                    min_val=0.01,
                    max_val=0.5,
                    param_name='adjustment_limit'
                ),
                'max_drift': self.shared_utils.safe_float_convert(
                    learning_config.get('max_drift', defaults.get('max_drift', 0.1)),
                    default=0.1,
                    min_val=0.01,
                    max_val=1.0,
                    param_name='max_drift'
                )
            }
            
            # Add sensitivity bounds
            sensitivity_config = learning_config.get('sensitivity_bounds', {})
            sensitivity_defaults = defaults.get('sensitivity_bounds', {})
            core_params['sensitivity_bounds'] = {
                'min_global_sensitivity': self.shared_utils.safe_float_convert(
                    sensitivity_config.get('min_global_sensitivity', 
                                          sensitivity_defaults.get('min_global_sensitivity', 0.5)),
                    default=0.5,
                    min_val=0.1,
                    max_val=2.0,
                    param_name='min_global_sensitivity'
                ),
                'max_global_sensitivity': self.shared_utils.safe_float_convert(
                    sensitivity_config.get('max_global_sensitivity', 
                                          sensitivity_defaults.get('max_global_sensitivity', 1.5)),
                    default=1.5,
                    min_val=0.1,
                    max_val=5.0,
                    param_name='max_global_sensitivity'
                )
            }
            
            # Add adjustment factors
            adjustment_config = learning_config.get('adjustment_factors', {})
            adjustment_defaults = defaults.get('adjustment_factors', {})
            core_params['adjustment_factors'] = {
                'false_positive_factor': self.shared_utils.safe_float_convert(
                    adjustment_config.get('false_positive_factor', 
                                         adjustment_defaults.get('false_positive_factor', -0.1)),
                    default=-0.1,
                    min_val=-1.0,
                    max_val=1.0,
                    param_name='false_positive_factor'
                ),
                'false_negative_factor': self.shared_utils.safe_float_convert(
                    adjustment_config.get('false_negative_factor', 
                                         adjustment_defaults.get('false_negative_factor', 0.1)),
                    default=0.1,
                    min_val=-1.0,
                    max_val=1.0,
                    param_name='false_negative_factor'
                )
            }
            
            # Add severity multipliers
            severity_config = learning_config.get('severity_multipliers', {})
            severity_defaults = defaults.get('severity_multipliers', {})
            core_params['severity_multipliers'] = {
                'high_severity': self.shared_utils.safe_float_convert(
                    severity_config.get('high_severity', severity_defaults.get('high_severity', 3.0)),
                    default=3.0,
                    min_val=0.1,
                    max_val=10.0,
                    param_name='high_severity'
                ),
                'medium_severity': self.shared_utils.safe_float_convert(
                    severity_config.get('medium_severity', severity_defaults.get('medium_severity', 2.0)),
                    default=2.0,
                    min_val=0.1,
                    max_val=10.0,
                    param_name='medium_severity'
                ),
                'low_severity': self.shared_utils.safe_float_convert(
                    severity_config.get('low_severity', severity_defaults.get('low_severity', 1.0)),
                    default=1.0,
                    min_val=0.1,
                    max_val=10.0,
                    param_name='low_severity'
                )
            }
            
            return core_params
            
        except Exception as e:
            self.logger.error(f"❌ Error loading learning system parameters: {e}")
            # Re-raise the exception to prevent adjustments when SharedUtils fails
            raise RuntimeError(f"Failed to load learning parameters: {str(e)}")
    
    def get_learning_thresholds(self) -> Dict[str, Any]:
        """
        Get learning system threshold configuration (Extracted from ThresholdMappingManager)
        
        This method was moved from ThresholdMappingManager to consolidate all learning
        functionality into the specialized LearningSystemManager.
        
        Returns:
            Dictionary with learning threshold configuration
        """
        try:
            # Access threshold configuration through UnifiedConfigManager
            threshold_config = self.config_manager.get_threshold_config()
            learning_config = threshold_config.get('learning_thresholds', {})
            
            return {
                'learning_rate': self.shared_utils.safe_float_convert(
                    learning_config.get('learning_rate', 0.1),
                    default=0.1,
                    min_val=0.01,
                    max_val=1.0,
                    param_name='threshold_learning_rate'
                ),
                'max_adjustments_per_day': self.shared_utils.safe_int_convert(
                    learning_config.get('max_adjustments_per_day', 50),
                    default=50,
                    min_val=1,
                    max_val=1000,
                    param_name='threshold_max_adjustments_per_day'
                ),
                'min_confidence_for_learning': self.shared_utils.safe_float_convert(
                    learning_config.get('min_confidence_for_learning', 0.3),
                    default=0.3,
                    min_val=0.1,
                    max_val=1.0,
                    param_name='threshold_min_confidence_for_learning'
                )
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error getting learning thresholds: {e}")
            return {
                'learning_rate': 0.1,
                'max_adjustments_per_day': 50,
                'min_confidence_for_learning': 0.3
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
    
    # ========================================================================
    # THRESHOLD ADJUSTMENT METHODS - New functionality for Step 3
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
    
    def apply_learning_adjustments(self, base_result: Dict[str, Any], user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Apply learning adjustments to analysis results
        
        Args:
            base_result: Base analysis result to adjust
            user_id: User identifier for context
            channel_id: Channel identifier for context
            
        Returns:
            Dictionary with learning adjustments applied
        """
        try:
            if not self.get_learning_parameters().get('enabled', False):
                return {
                    'adjusted_score': base_result.get('crisis_score', 0.0),
                    'adjustments': {},
                    'metadata': {'learning_disabled': True}
                }
            
            original_score = base_result.get('crisis_score', 0.0)
            crisis_level = base_result.get('crisis_level', 'none')
            
            # Apply basic learning adjustments
            adjustment_factor = 1.0
            adjustments = {}
            
            # Get learning parameters
            params = self.get_learning_parameters()
            learning_rate = params.get('learning_rate', 0.01)
            
            # Apply historical adjustments if available
            if hasattr(self, '_adjustment_history') and self._adjustment_history:
                recent_adjustments = self._adjustment_history[-10:]  # Last 10 adjustments
                avg_adjustment = sum(adj.get('adjustment_amount', 0) for adj in recent_adjustments) / len(recent_adjustments)
                adjustment_factor += avg_adjustment * learning_rate
                adjustments['historical_adjustment'] = avg_adjustment
            
            # Apply severity-based adjustments
            severity_multipliers = params.get('severity_multipliers', {})
            if crisis_level in ['critical', 'high']:
                multiplier = severity_multipliers.get('high_severity', 1.0)
                adjustment_factor *= multiplier
                adjustments['severity_adjustment'] = multiplier
            
            # Calculate final adjusted score
            adjusted_score = max(0.0, min(1.0, original_score * adjustment_factor))
            
            return {
                'adjusted_score': adjusted_score,
                'adjustments': adjustments,
                'metadata': {
                    'original_score': original_score,
                    'adjustment_factor': adjustment_factor,
                    'learning_enabled': True,
                    'user_id': user_id,
                    'channel_id': channel_id
                }
            }
            
        except Exception as e:
            logger.error(f"Learning adjustment failed: {e}")
            return {
                'adjusted_score': base_result.get('crisis_score', 0.0),
                'adjustments': {},
                'metadata': {'learning_error': str(e)}
            }

    def apply_threshold_adjustments(self, confidence: float, mode: str = 'consensus') -> float:
        """
        Apply threshold adjustments based on learning history
        
        Args:
            confidence: Original confidence score
            mode: Threshold mode (consensus, majority, weighted)
            
        Returns:
            Adjusted confidence score
        """
        try:
            if not self.get_learning_parameters().get('enabled', False):
                return confidence
            
            # Apply learning-based threshold adjustments
            params = self.get_learning_parameters()
            learning_rate = params.get('learning_rate', 0.01)
            
            # Calculate adjustment based on recent feedback
            adjustment = 0.0
            if hasattr(self, '_adjustment_history') and self._adjustment_history:
                recent_false_positives = [adj for adj in self._adjustment_history[-20:] 
                                        if adj.get('type') == 'false_positive']
                recent_false_negatives = [adj for adj in self._adjustment_history[-20:] 
                                        if adj.get('type') == 'false_negative']
                
                # Adjust based on recent pattern
                if len(recent_false_positives) > len(recent_false_negatives):
                    adjustment = -learning_rate * 0.1  # Reduce sensitivity
                elif len(recent_false_negatives) > len(recent_false_positives):
                    adjustment = learning_rate * 0.1   # Increase sensitivity
            
            adjusted_confidence = max(0.0, min(1.0, confidence + adjustment))
            
            if adjustment != 0:
                logger.debug(f"Applied learning threshold adjustment: {confidence:.3f} → {adjusted_confidence:.3f}")
            
            return adjusted_confidence
            
        except Exception as e:
            logger.error(f"Threshold adjustment failed: {e}")
            return confidence

    def process_feedback(self, message: str, user_id: str, channel_id: str, feedback_type: str, original_result: Dict) -> None:
        """
        Process feedback for learning system improvement
        
        Args:
            message: Original message that was analyzed
            user_id: User identifier
            channel_id: Channel identifier  
            feedback_type: Type of feedback ('false_positive', 'false_negative', 'correct')
            original_result: Original analysis result
        """
        try:
            if not self.get_learning_parameters().get('enabled', False):
                logger.info("Learning system disabled - feedback not processed")
                return
            
            # Record feedback
            feedback_record = {
                'timestamp': datetime.now().isoformat(),
                'feedback_type': feedback_type,
                'user_id': user_id,
                'channel_id': channel_id,
                'original_score': original_result.get('crisis_score', 0.0),
                'original_level': original_result.get('crisis_level', 'none'),
                'message_length': len(message)
            }
            
            # Apply threshold adjustment if needed
            if feedback_type == 'false_positive':
                original_score = original_result.get('crisis_score', 0.0)
                self.adjust_threshold_for_false_positive(original_score, original_result.get('crisis_level', 'medium'))
            elif feedback_type == 'false_negative':
                original_score = original_result.get('crisis_score', 0.0)
                self.adjust_threshold_for_false_negative(original_score, original_result.get('crisis_level', 'medium'))
            
            logger.info(f"Processed learning feedback: {feedback_type} for user {user_id}")
            
        except Exception as e:
            logger.error(f"Feedback processing failed: {e}")

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

logger.info("✅ LearningSystemManager v3.1-3e-3.2-2 loaded - Complete learning system with methods from both AnalysisParametersManager and ThresholdMappingManager")