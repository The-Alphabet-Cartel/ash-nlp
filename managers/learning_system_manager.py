# ash-nlp/managers/learning_system_manager.py
"""
Learning System Manager for Ash-NLP Service
FILE VERSION: v3.1-3e-3.2-1
LAST MODIFIED: 2025-08-17
PHASE: 3e Step 3 - LearningSystemManager Creation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

from managers.unified_config_manager import UnifiedConfigManager
from managers.shared_utilities import SharedUtilitiesManager

# Configure logging
logger = logging.getLogger(__name__)


class LearningSystemManager:
    """
    Learning System Manager for False Positive/Negative Management
    
    Phase 3e Step 3: Consolidates learning methods from multiple managers to eliminate
    overlap and provide centralized false positive/negative threshold adjustment.
    
    Clean v3.1 Architecture Compliance:
    - Factory function pattern for object creation
    - Dependency injection (UnifiedConfigManager, SharedUtilitiesManager)
    - JSON configuration with environment variable overrides
    - Resilient error handling with fallbacks
    - Uses existing environment variables (Rule #7 compliant)
    """
    
    def __init__(self, unified_config_manager: UnifiedConfigManager, 
                 shared_utilities_manager: SharedUtilitiesManager):
        """
        Initialize LearningSystemManager with injected dependencies
        
        Args:
            unified_config_manager: Configuration access via JSON + environment
            shared_utilities_manager: Shared utility methods for validation/error handling
        """
        self.unified_config = unified_config_manager
        self.shared_utilities = shared_utilities_manager
        
        # Initialize learning configuration
        self.learning_config = {}
        self.learning_history = []
        self.adjustment_counts = {}
        self.last_adjustment_time = {}
        
        # Load configuration on initialization
        self._load_learning_configuration()
        
        # Initialize adjustment tracking
        self._initialize_adjustment_tracking()
        
        logger.info("✅ LearningSystemManager initialized successfully")
    
    def _load_learning_configuration(self):
        """Load learning configuration via UnifiedConfigManager"""
        try:
            # Load learning system configuration from analysis_parameters.json
            # This uses existing configuration structure (Rule #7 compliant)
            self.learning_config = {
                'enabled': self.unified_config.get_env_bool('NLP_ANALYSIS_LEARNING_ENABLED', True),
                'learning_rate': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_RATE', 0.01),
                'min_confidence_adjustment': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_MIN_CONFIDENCE_ADJUSTMENT', 0.05),
                'max_confidence_adjustment': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_MAX_CONFIDENCE_ADJUSTMENT', 0.30),
                'max_adjustments_per_day': self.unified_config.get_env_int('NLP_ANALYSIS_LEARNING_MAX_ADJUSTMENTS_PER_DAY', 50),
                'persistence_file': self.unified_config.get_env_str('NLP_ANALYSIS_LEARNING_PERSISTENCE_FILE', './learning_data/adjustments.json'),
                'feedback_weight': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_FEEDBACK_WEIGHT', 0.1),
                'min_samples': self.unified_config.get_env_int('NLP_ANALYSIS_LEARNING_MIN_SAMPLES', 5),
                'adjustment_limit': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_ADJUSTMENT_LIMIT', 0.05),
                'max_drift': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_MAX_DRIFT', 0.1),
                'sensitivity_bounds': {
                    'min_global_sensitivity': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_MIN_SENSITIVITY', 0.5),
                    'max_global_sensitivity': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_MAX_SENSITIVITY', 1.5)
                },
                'adjustment_factors': {
                    'false_positive_factor': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_FALSE_POSITIVE_FACTOR', -0.1),
                    'false_negative_factor': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_FALSE_NEGATIVE_FACTOR', 0.1)
                },
                'severity_multipliers': {
                    'high_severity': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_SEVERITY_HIGH', 3.0),
                    'medium_severity': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_SEVERITY_MEDIUM', 2.0),
                    'low_severity': self.unified_config.get_env_float('NLP_ANALYSIS_LEARNING_SEVERITY_LOW', 1.0)
                }
            }
            
            logger.info("✅ Learning configuration loaded via UnifiedConfigManager")
            
        except Exception as e:
            error_msg = f"Error loading learning configuration: {e}"
            logger.error(f"❌ {error_msg}")
            
            # Use shared utilities for error handling with fallbacks
            self.learning_config = self.shared_utilities.handle_error_with_fallback(
                error=e,
                fallback_value=self._get_default_learning_config(),
                context="learning_configuration_loading",
                operation="load_learning_configuration"
            )
    
    def _get_default_learning_config(self) -> Dict[str, Any]:
        """Get default learning configuration as fallback"""
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
    
    def _initialize_adjustment_tracking(self):
        """Initialize adjustment tracking for daily limits"""
        try:
            # Load existing adjustment history if available
            persistence_file = Path(self.learning_config['persistence_file'])
            
            if persistence_file.exists():
                with open(persistence_file, 'r') as f:
                    data = json.load(f)
                    self.learning_history = data.get('history', [])
                    self.adjustment_counts = data.get('adjustment_counts', {})
                    self.last_adjustment_time = data.get('last_adjustment_time', {})
                
                logger.info(f"✅ Loaded {len(self.learning_history)} learning adjustments from persistence file")
            else:
                logger.info("ℹ️ No existing learning history found, starting fresh")
                
        except Exception as e:
            logger.warning(f"⚠️ Could not load learning history: {e}, starting fresh")
            self.learning_history = []
            self.adjustment_counts = {}
            self.last_adjustment_time = {}
    
    # ========================================================================
    # CORE LEARNING PARAMETER ACCESS (Extracted from AnalysisParametersManager)
    # ========================================================================
    
    def get_learning_parameters(self) -> Dict[str, Any]:
        """
        Get complete learning system parameters
        
        Extracted from AnalysisParametersManager.get_learning_system_parameters()
        Rule #7 Compliant: Uses existing NLP_ANALYSIS_LEARNING_* variables
        
        Returns:
            Dictionary with all learning system configuration
        """
        try:
            # Return learning configuration with validation
            validated_config = self.learning_config.copy()
            
            # Use SharedUtilities for validation
            validation_result = self.validate_learning_parameters()
            
            if validation_result.get('errors'):
                logger.warning(f"⚠️ Learning parameter validation found {len(validation_result['errors'])} errors")
                
            return validated_config
            
        except Exception as e:
            return self.shared_utilities.handle_error_with_fallback(
                error=e,
                fallback_value=self._get_default_learning_config(),
                context="get_learning_parameters",
                operation="parameter_access"
            )
    
    def validate_learning_parameters(self) -> Dict[str, Any]:
        """
        Validate learning system parameter ranges and types
        
        Extracted from AnalysisParametersManager.validate_learning_system_parameters()
        Uses SharedUtilitiesManager for validation
        
        Returns:
            Dictionary with validation results
        """
        try:
            params = self.learning_config
            errors = []
            warnings = []
            
            # Validate learning rate using SharedUtilities
            if not self.shared_utilities.validate_range(
                params['learning_rate'], 0.001, 1.0, "learning_rate"
            ):
                errors.append(f"Learning rate {params['learning_rate']} outside valid range [0.001, 1.0]")
            
            # Validate confidence adjustments
            min_adj = params['min_confidence_adjustment']
            max_adj = params['max_confidence_adjustment']
            
            if not self.shared_utilities.validate_range(min_adj, 0.01, 1.0, "min_confidence_adjustment"):
                errors.append(f"Min confidence adjustment {min_adj} outside valid range [0.01, 1.0]")
                
            if not self.shared_utilities.validate_range(max_adj, 0.01, 1.0, "max_confidence_adjustment"):
                errors.append(f"Max confidence adjustment {max_adj} outside valid range [0.01, 1.0]")
            
            if min_adj >= max_adj:
                errors.append(f"Min confidence adjustment {min_adj} >= max confidence adjustment {max_adj}")
            
            # Validate daily adjustment limits
            max_per_day = params['max_adjustments_per_day']
            if not self.shared_utilities.validate_range(max_per_day, 1, 1000, "max_adjustments_per_day"):
                errors.append(f"Max adjustments per day {max_per_day} outside valid range [1, 1000]")
            
            # Validate sensitivity bounds
            min_sens = params['sensitivity_bounds']['min_global_sensitivity']
            max_sens = params['sensitivity_bounds']['max_global_sensitivity']
            
            if min_sens >= max_sens:
                errors.append(f"Min sensitivity {min_sens} >= max sensitivity {max_sens}")
            
            # Validate severity multipliers
            severity_mults = params['severity_multipliers']
            if not (severity_mults['low_severity'] <= severity_mults['medium_severity'] <= severity_mults['high_severity']):
                errors.append("Severity multipliers must be in ascending order: low <= medium <= high")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'parameter_count': len(params)
            }
            
        except Exception as e:
            logger.error(f"❌ Error validating learning parameters: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {e}"],
                'warnings': [],
                'parameter_count': 0
            }
    
    # ========================================================================
    # FALSE POSITIVE/NEGATIVE ADJUSTMENT METHODS (Core Functionality)
    # ========================================================================
    
    def adjust_threshold_false_positive(self, current_threshold: float, severity: str = "medium") -> float:
        """
        Adjust threshold down after false positive feedback
        
        Args:
            current_threshold: Current threshold value
            severity: Severity level ("low", "medium", "high")
            
        Returns:
            Adjusted threshold value (reduced for false positive)
        """
        try:
            if not self.learning_config['enabled']:
                logger.info("ℹ️ Learning system disabled, returning unchanged threshold")
                return current_threshold
            
            # Check daily adjustment limits
            if not self._can_make_adjustment():
                logger.warning("⚠️ Daily adjustment limit reached, returning unchanged threshold")
                return current_threshold
            
            # Calculate adjustment factor
            base_factor = self.learning_config['adjustment_factors']['false_positive_factor']
            severity_multiplier = self.learning_config['severity_multipliers'].get(f"{severity}_severity", 1.0)
            adjustment_factor = base_factor * severity_multiplier
            
            # Apply adjustment with bounds checking
            adjustment = current_threshold * adjustment_factor * self.learning_config['learning_rate']
            new_threshold = current_threshold + adjustment  # adjustment_factor is negative for FP
            
            # Apply bounds checking using SharedUtilities
            min_threshold = self.learning_config['sensitivity_bounds']['min_global_sensitivity'] * 0.1
            max_threshold = self.learning_config['sensitivity_bounds']['max_global_sensitivity'] * 0.9
            
            new_threshold = max(min_threshold, min(max_threshold, new_threshold))
            
            # Record adjustment
            self._record_adjustment("false_positive", current_threshold, new_threshold, severity)
            
            logger.info(f"✅ False positive adjustment: {current_threshold:.3f} → {new_threshold:.3f} (severity: {severity})")
            return new_threshold
            
        except Exception as e:
            logger.error(f"❌ Error adjusting threshold for false positive: {e}")
            return current_threshold
    
    def adjust_threshold_false_negative(self, current_threshold: float, severity: str = "medium") -> float:
        """
        Adjust threshold up after false negative feedback
        
        Args:
            current_threshold: Current threshold value
            severity: Severity level ("low", "medium", "high")
            
        Returns:
            Adjusted threshold value (increased for false negative)
        """
        try:
            if not self.learning_config['enabled']:
                logger.info("ℹ️ Learning system disabled, returning unchanged threshold")
                return current_threshold
            
            # Check daily adjustment limits
            if not self._can_make_adjustment():
                logger.warning("⚠️ Daily adjustment limit reached, returning unchanged threshold")
                return current_threshold
            
            # Calculate adjustment factor
            base_factor = self.learning_config['adjustment_factors']['false_negative_factor']
            severity_multiplier = self.learning_config['severity_multipliers'].get(f"{severity}_severity", 1.0)
            adjustment_factor = base_factor * severity_multiplier
            
            # Apply adjustment with bounds checking
            adjustment = current_threshold * adjustment_factor * self.learning_config['learning_rate']
            new_threshold = current_threshold + adjustment  # adjustment_factor is positive for FN
            
            # Apply bounds checking using SharedUtilities
            min_threshold = self.learning_config['sensitivity_bounds']['min_global_sensitivity'] * 0.1
            max_threshold = self.learning_config['sensitivity_bounds']['max_global_sensitivity'] * 0.9
            
            new_threshold = max(min_threshold, min(max_threshold, new_threshold))
            
            # Record adjustment
            self._record_adjustment("false_negative", current_threshold, new_threshold, severity)
            
            logger.info(f"✅ False negative adjustment: {current_threshold:.3f} → {new_threshold:.3f} (severity: {severity})")
            return new_threshold
            
        except Exception as e:
            logger.error(f"❌ Error adjusting threshold for false negative: {e}")
            return current_threshold
    
    def process_feedback(self, feedback_type: str, data: Dict[str, Any]) -> bool:
        """
        Process feedback for threshold adjustment
        
        Args:
            feedback_type: Type of feedback ("false_positive" or "false_negative")
            data: Feedback data including threshold, severity, context
            
        Returns:
            True if feedback processed successfully, False otherwise
        """
        try:
            current_threshold = data.get('current_threshold', 0.5)
            severity = data.get('severity', 'medium')
            
            if feedback_type == "false_positive":
                new_threshold = self.adjust_threshold_false_positive(current_threshold, severity)
            elif feedback_type == "false_negative":
                new_threshold = self.adjust_threshold_false_negative(current_threshold, severity)
            else:
                logger.error(f"❌ Unknown feedback type: {feedback_type}")
                return False
            
            # Store the adjusted threshold in data for caller to use
            data['adjusted_threshold'] = new_threshold
            data['adjustment_made'] = abs(new_threshold - current_threshold) > 0.001
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error processing feedback: {e}")
            return False
    
    # ========================================================================
    # ADJUSTMENT TRACKING AND PERSISTENCE
    # ========================================================================
    
    def _can_make_adjustment(self) -> bool:
        """Check if adjustment can be made within daily limits"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            current_count = self.adjustment_counts.get(today, 0)
            max_per_day = self.learning_config['max_adjustments_per_day']
            
            return current_count < max_per_day
            
        except Exception as e:
            logger.warning(f"⚠️ Error checking adjustment limits: {e}")
            return True  # Allow adjustment on error to prevent blocking
    
    def _record_adjustment(self, adjustment_type: str, old_threshold: float, 
                          new_threshold: float, severity: str):
        """Record adjustment for tracking and persistence"""
        try:
            timestamp = datetime.now()
            today = timestamp.strftime('%Y-%m-%d')
            
            # Update daily count
            self.adjustment_counts[today] = self.adjustment_counts.get(today, 0) + 1
            
            # Record adjustment
            adjustment_record = {
                'timestamp': timestamp.isoformat(),
                'type': adjustment_type,
                'old_threshold': old_threshold,
                'new_threshold': new_threshold,
                'adjustment': new_threshold - old_threshold,
                'severity': severity,
                'daily_count': self.adjustment_counts[today]
            }
            
            self.learning_history.append(adjustment_record)
            self.last_adjustment_time[adjustment_type] = timestamp.isoformat()
            
            # Persist to file
            self._persist_learning_data()
            
        except Exception as e:
            logger.warning(f"⚠️ Error recording adjustment: {e}")
    
    def _persist_learning_data(self):
        """Persist learning data to file"""
        try:
            persistence_file = Path(self.learning_config['persistence_file'])
            persistence_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'history': self.learning_history,
                'adjustment_counts': self.adjustment_counts,
                'last_adjustment_time': self.last_adjustment_time,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(persistence_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"⚠️ Error persisting learning data: {e}")
    
    # ========================================================================
    # STATUS AND REPORTING METHODS
    # ========================================================================
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get current learning system status"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            current_count = self.adjustment_counts.get(today, 0)
            max_per_day = self.learning_config['max_adjustments_per_day']
            
            return {
                'enabled': self.learning_config['enabled'],
                'adjustments_today': current_count,
                'adjustments_remaining': max(0, max_per_day - current_count),
                'total_adjustments': len(self.learning_history),
                'learning_rate': self.learning_config['learning_rate'],
                'last_adjustment': self.last_adjustment_time.get('false_positive') or self.last_adjustment_time.get('false_negative'),
                'status': 'healthy' if self.learning_config['enabled'] else 'disabled'
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting learning status: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def get_adjustment_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent adjustment history"""
        try:
            # Return most recent adjustments
            return self.learning_history[-limit:] if limit > 0 else self.learning_history
            
        except Exception as e:
            logger.error(f"❌ Error getting adjustment history: {e}")
            return []


# ============================================================================
# FACTORY FUNCTION - Clean v3.1 Architecture Compliance
# ============================================================================

def create_learning_system_manager(unified_config_manager: UnifiedConfigManager,
                                  shared_utilities_manager: SharedUtilitiesManager) -> LearningSystemManager:
    """
    Factory function to create LearningSystemManager with dependency injection
    
    Args:
        unified_config_manager: UnifiedConfigManager instance for configuration
        shared_utilities_manager: SharedUtilitiesManager instance for utilities
        
    Returns:
        LearningSystemManager instance ready for use
        
    Raises:
        RuntimeError: If initialization fails
    """
    try:
        # Validate dependencies
        if not unified_config_manager:
            raise ValueError("unified_config_manager is required")
            
        if not shared_utilities_manager:
            raise ValueError("shared_utilities_manager is required")
        
        # Create manager instance
        manager = LearningSystemManager(unified_config_manager, shared_utilities_manager)
        
        # Verify initialization
        status = manager.get_learning_status()
        if status.get('status') == 'error':
            raise RuntimeError(f"LearningSystemManager initialization failed: {status.get('error')}")
            
        logger.info("✅ LearningSystemManager created successfully via factory function")
        return manager
        
    except Exception as e:
        logger.error(f"❌ Failed to create LearningSystemManager: {e}")
        raise RuntimeError(f"LearningSystemManager factory function failed: {e}")


# ============================================================================
# EXPORT FOR CLEAN ARCHITECTURE
# ============================================================================

__all__ = [
    'LearningSystemManager',
    'create_learning_system_manager'
]