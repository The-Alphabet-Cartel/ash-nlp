"""
CRITICAL FIXES for Crisis Analyzer - Three Zero-Shot Model Ensemble INTEGRATION
Phase 3a: Updated to use CrisisPatternManager instead of hardcoded patterns

These changes fix the dangerous under-response bug and integrate ensemble analysis
with clean v3.1 architecture and JSON-based crisis patterns.
"""

import logging
import time
import re
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
    UPDATED: Three Zero-Shot Model Ensemble crisis analysis with CrisisPatternManager integration
    Phase 3a: Clean v3.1 architecture with JSON-based patterns
    """
    
    def __init__(self, models_manager, crisis_pattern_manager: Optional[CrisisPatternManager] = None, learning_manager=None):
        """
        Initialize CrisisAnalyzer with managers
        
        Args:
            models_manager: ML model manager for ensemble analysis
            crisis_pattern_manager: CrisisPatternManager for pattern-based analysis
            learning_manager: Optional learning manager for feedback
        """
        self.models_manager = models_manager
        self.crisis_pattern_manager = crisis_pattern_manager
        self.learning_manager = learning_manager
        
        # Initialize community pattern extractor if crisis pattern manager available
        if self.crisis_pattern_manager:
            self.community_extractor = CommunityPatternExtractor(self.crisis_pattern_manager)
            logger.info("CrisisAnalyzer v3.1 initialized with CrisisPatternManager")
        else:
            self.community_extractor = None
            logger.warning("CrisisAnalyzer initialized without CrisisPatternManager - pattern analysis limited")
        
        # Load crisis thresholds from pattern manager or use defaults
        self.crisis_thresholds = self._load_crisis_thresholds()

    def _load_crisis_thresholds(self) -> Dict[str, float]:
        """Load crisis thresholds from configuration or use defaults"""
        try:
            if self.crisis_pattern_manager:
                # Try to get thresholds from enhanced crisis patterns configuration
                enhanced_patterns = self.crisis_pattern_manager.get_enhanced_crisis_patterns()
                if enhanced_patterns and enhanced_patterns.get('configuration'):
                    # Extract thresholds if available in configuration
                    pass
            
            # Use default thresholds
            return {
                "high": 0.55,    # Reduced from 0.50 - matches new systematic approach
                "medium": 0.28,  # Reduced from 0.22 - more selective for medium alerts
                "low": 0.16      # Reduced from 0.12 - avoids very mild expressions
            }
        except Exception as e:
            logger.error(f"Error loading crisis thresholds: {e}")
            return {"high": 0.55, "medium": 0.28, "low": 0.16}

    async def analyze_message(self, message: str, user_id: str = "unknown", channel_id: str = "unknown") -> Dict:
        """
        UPDATED: Three Zero-Shot Model Ensemble analysis with FIXED crisis level mapping
        Phase 3a: Enhanced with CrisisPatternManager integration
        """
        
        start_time = time.time()
        reasoning_steps = []
        
        try:
            # Step 1: Extract context signals
            context = extract_context_signals(message)
            reasoning_steps.append(f"Context: {context}")
            
            # Step 2: Crisis Pattern Analysis (Phase 3a)
            pattern_analysis = await self._analyze_with_crisis_patterns(message)
            reasoning_steps.append(f"Pattern Analysis: {pattern_analysis.get('summary', 'none')}")
            
            # Step 3: Three Zero-Shot Model Ensemble ANALYSIS
            if hasattr(self.models_manager, 'analyze_with_ensemble'):
                # Use the new Three Zero-Shot Model Ensemble if available
                ensemble_result = self.models_manager.analyze_with_ensemble(message)
                
                # Extract consensus prediction for crisis level mapping
                consensus = ensemble_result.get('consensus', {})
                consensus_prediction = consensus.get('prediction', 'unknown')
                consensus_confidence = consensus.get('confidence', 0.0)
                
                # CRITICAL FIX: Map consensus prediction to crisis level
                crisis_level = self._map_consensus_to_crisis_level(consensus_prediction, consensus_confidence)
                
                # Apply pattern-based adjustments
                if pattern_analysis.get('adjustments'):
                    crisis_level, consensus_confidence = self._apply_pattern_adjustments(
                        crisis_level, consensus_confidence, pattern_analysis['adjustments']
                    )
                
                # Build final result with ensemble data
                result = {
                    'needs_response': crisis_level != 'none',
                    'crisis_level': crisis_level,
                    'confidence_score': consensus_confidence,
                    'detected_categories': ensemble_result.get('detected_categories', []),
                    'method': 'three_model_ensemble_with_patterns',
                    'processing_time_ms': (time.time() - start_time) * 1000,
                    'model_info': f"Ensemble: {ensemble_result.get('model_info', 'unknown')}",
                    'reasoning': ' | '.join(reasoning_steps),
                    'ensemble_details': ensemble_result,
                    'pattern_analysis': pattern_analysis
                }
                
                logger.debug(f"✅ ENSEMBLE+PATTERNS: {crisis_level} (conf={consensus_confidence:.3f}) consensus={consensus_prediction}")
                return result
                
            else:
                # Fallback to legacy two-model analysis
                return await self._legacy_two_model_analysis(message, user_id, channel_id, start_time)
                
        except Exception as e:
            logger.error(f"Error in ensemble crisis analysis: {e}")
            logger.exception("Full traceback:")
            # Return a safe fallback result
            return {
                'needs_response': False,
                'crisis_level': 'none', 
                'confidence_score': 0.0,
                'detected_categories': [],
                'method': 'error_fallback',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': 'Error fallback',
                'reasoning': f"Analysis failed: {str(e)}"
            }

    async def _analyze_with_crisis_patterns(self, message: str) -> Dict[str, Any]:
        """
        Analyze message using CrisisPatternManager patterns
        
        Args:
            message: Message text to analyze
            
        Returns:
            Dictionary with pattern analysis results and adjustments
        """
        if not self.crisis_pattern_manager:
            return {'summary': 'no_pattern_manager', 'adjustments': {}}
        
        try:
            pattern_results = {
                'community_patterns': [],
                'context_phrases': [],
                'temporal_indicators': {},
                'enhanced_patterns': {},
                'adjustments': {
                    'crisis_boost': 0.0,
                    'confidence_adjustment': 0.0,
                    'escalation_required': False,
                    'staff_alert': False
                }
            }
            
            # Extract community patterns
            if self.community_extractor:
                pattern_results['community_patterns'] = self.community_extractor.extract_community_patterns(message)
                pattern_results['context_phrases'] = self.community_extractor.extract_crisis_context_phrases(message)
                pattern_results['temporal_indicators'] = self.community_extractor.analyze_temporal_indicators(message)
            
            # Check enhanced crisis patterns
            pattern_results['enhanced_patterns'] = self.crisis_pattern_manager.check_enhanced_crisis_patterns(message)
            
            # Calculate adjustments based on pattern findings
            adjustments = self._calculate_pattern_adjustments(pattern_results)
            pattern_results['adjustments'] = adjustments
            
            # Create summary
            total_patterns = (
                len(pattern_results['community_patterns']) +
                len(pattern_results['context_phrases']) +
                len(pattern_results['temporal_indicators'].get('found_indicators', [])) +
                len(pattern_results['enhanced_patterns'].get('matches', []))
            )
            
            pattern_results['summary'] = f"{total_patterns} patterns found"
            
            return pattern_results
            
        except Exception as e:
            logger.error(f"Error in crisis pattern analysis: {e}")
            return {'summary': f'pattern_error: {str(e)}', 'adjustments': {}}

    def _calculate_pattern_adjustments(self, pattern_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate crisis level and confidence adjustments based on pattern findings
        
        Args:
            pattern_results: Results from pattern analysis
            
        Returns:
            Dictionary with adjustment values
        """
        adjustments = {
            'crisis_boost': 0.0,
            'confidence_adjustment': 0.0,
            'escalation_required': False,
            'staff_alert': False
        }
        
        try:
            # Community pattern adjustments
            for pattern in pattern_results.get('community_patterns', []):
                if pattern.get('crisis_level') == 'high':
                    adjustments['crisis_boost'] += 0.15
                    adjustments['escalation_required'] = True
                elif pattern.get('crisis_level') == 'medium':
                    adjustments['crisis_boost'] += 0.08
            
            # Temporal indicator adjustments
            temporal = pattern_results.get('temporal_indicators', {})
            if temporal.get('auto_escalate'):
                adjustments['escalation_required'] = True
                adjustments['crisis_boost'] += temporal.get('total_boost', 0.0)
            if temporal.get('staff_alert'):
                adjustments['staff_alert'] = True
            
            # Enhanced pattern adjustments
            enhanced = pattern_results.get('enhanced_patterns', {})
            if enhanced.get('requires_immediate_attention'):
                adjustments['escalation_required'] = True
                adjustments['staff_alert'] = True
                adjustments['crisis_boost'] += 0.20
            elif enhanced.get('auto_escalate'):
                adjustments['escalation_required'] = True
                adjustments['crisis_boost'] += enhanced.get('total_weight', 0.0) * 0.1
            
            # Cap maximum boost
            adjustments['crisis_boost'] = min(adjustments['crisis_boost'], 0.40)
            
        except Exception as e:
            logger.error(f"Error calculating pattern adjustments: {e}")
        
        return adjustments

    def _apply_pattern_adjustments(self, crisis_level: str, confidence: float, adjustments: Dict[str, Any]) -> Tuple[str, float]:
        """
        Apply pattern-based adjustments to crisis level and confidence
        
        Args:
            crisis_level: Current crisis level
            confidence: Current confidence score
            adjustments: Pattern-based adjustments to apply
            
        Returns:
            Tuple of (adjusted_crisis_level, adjusted_confidence)
        """
        try:
            adjusted_confidence = confidence + adjustments.get('confidence_adjustment', 0.0)
            adjusted_confidence = max(0.0, min(1.0, adjusted_confidence))
            
            crisis_boost = adjustments.get('crisis_boost', 0.0)
            
            # If significant pattern boost, consider upgrading crisis level
            if crisis_boost >= 0.15:
                if crisis_level == 'none' and adjusted_confidence > 0.15:
                    crisis_level = 'low'
                elif crisis_level == 'low' and adjusted_confidence > 0.25:
                    crisis_level = 'medium'
                elif crisis_level == 'medium' and adjusted_confidence > 0.50:
                    crisis_level = 'high'
            
            # Handle escalation requirements
            if adjustments.get('escalation_required') and crisis_level == 'none':
                crisis_level = 'low'  # Minimum escalation level
            
            return crisis_level, adjusted_confidence
            
        except Exception as e:
            logger.error(f"Error applying pattern adjustments: {e}")
            return crisis_level, confidence

    def _map_consensus_to_crisis_level(self, consensus_prediction: str, confidence: float) -> str:
        """
        CRITICAL FIX: Properly map ensemble consensus to crisis levels
        This fixes the dangerous under-response bug
        """
        pred_lower = consensus_prediction.lower()
        
        # CRISIS predictions (normalized from ensemble)
        if pred_lower == 'crisis':
            if confidence >= 0.70:
                return 'high'      # High confidence crisis
            elif confidence >= 0.45:
                return 'medium'    # Medium confidence crisis  
            else:
                return 'low'       # Low confidence crisis, but still crisis
        
        # MILD_CRISIS predictions 
        elif pred_lower == 'mild_crisis':
            if confidence >= 0.60:
                return 'low'       # Mild crisis with good confidence
            else:
                return 'none'      # Very uncertain mild crisis
        
        # SAFE predictions
        elif pred_lower in ['safe', 'neutral']:
            return 'none'
        
        # UNKNOWN or error cases - be conservative
        else:
            logger.warning(f"Unknown consensus prediction: {consensus_prediction}")
            if confidence > 0.50:  # If we're confident about something unknown, be cautious
                return 'low'
            else:
                return 'none'

    async def _legacy_two_model_analysis(self, message: str, user_id: str, channel_id: str, start_time: float) -> Dict:
        """
        Fallback to legacy two-model analysis when ensemble not available
        Enhanced with pattern analysis if available
        """
        try:
            # Extract context and phrase analysis
            context = extract_context_signals(message)
            depression_score = extract_depression_score(message, self.models_manager.get_model('depression'))
            
            # Apply pattern-based enhancements if available
            base_score = depression_score
            pattern_analysis = await self._analyze_with_crisis_patterns(message)
            
            if pattern_analysis.get('adjustments'):
                # Apply context weights if pattern manager available
                if self.community_extractor:
                    modified_score, weight_details = self.community_extractor.apply_context_weights(message, base_score)
                    depression_score = modified_score
            
            # Enhanced analysis
            enhanced_result = enhanced_depression_analysis(
                message, 
                depression_score, 
                self.models_manager.get_model('depression'),
                self.models_manager.get_model('sentiment')
            )
            
            crisis_level = enhanced_crisis_level_mapping(enhanced_result['final_score'], self.crisis_thresholds)
            
            return {
                'needs_response': crisis_level != 'none',
                'crisis_level': crisis_level,
                'confidence_score': enhanced_result['final_score'],
                'detected_categories': enhanced_result.get('detected_categories', []),
                'method': 'legacy_two_model_with_patterns',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': 'Legacy two-model analysis with pattern enhancement',
                'reasoning': enhanced_result.get('reasoning', 'Legacy analysis'),
                'pattern_analysis': pattern_analysis
            }
            
        except Exception as e:
            logger.error(f"Error in legacy analysis: {e}")
            return {
                'needs_response': False,
                'crisis_level': 'none',
                'confidence_score': 0.0,
                'detected_categories': [],
                'method': 'error_fallback',
                'processing_time_ms': (time.time() - start_time) * 1000,
                'model_info': 'Error fallback',
                'reasoning': f"Legacy analysis failed: {str(e)}"
            }

    def get_status(self) -> Dict[str, Any]:
        """Get CrisisAnalyzer status information"""
        return {
            'analyzer': 'CrisisAnalyzer',
            'version': '3.1.0',
            'architecture': 'v3.1_clean_with_patterns',
            'models_manager_available': self.models_manager is not None,
            'crisis_pattern_manager_available': self.crisis_pattern_manager is not None,
            'community_extractor_available': self.community_extractor is not None,
            'learning_manager_available': self.learning_manager is not None,
            'crisis_thresholds': self.crisis_thresholds,
            'ensemble_analysis_available': hasattr(self.models_manager, 'analyze_with_ensemble') if self.models_manager else False
        }


# Factory function for clean architecture
def create_crisis_analyzer(models_manager, crisis_pattern_manager: Optional[CrisisPatternManager] = None, learning_manager=None) -> CrisisAnalyzer:
    """
    Factory function to create CrisisAnalyzer instance with dependency injection
    
    Args:
        models_manager: ML model manager for ensemble analysis
        crisis_pattern_manager: Optional CrisisPatternManager for pattern analysis
        learning_manager: Optional learning manager for feedback
        
    Returns:
        CrisisAnalyzer instance
    """
    return CrisisAnalyzer(models_manager, crisis_pattern_manager, learning_manager)


# Export for clean architecture
__all__ = [
    'CrisisAnalyzer',
    'create_crisis_analyzer'
]