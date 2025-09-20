# ash-nlp/analysis/helpers/scoring_calculation_helper.py
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
Scoring Calculation Helper for CrisisAnalyzer
---
FILE VERSION: v3.1-3e-6-2
CREATED: 2025-08-22
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
from typing import Dict, List, Tuple, Any, Optional

logger = logging.getLogger(__name__)

class ScoringCalculationHelper:
    """Helper class for scoring calculations moved from CrisisAnalyzer"""
    
    # ========================================================================
    # INITIALIZE
    # ========================================================================
    def __init__(self, crisis_analyzer):
        """
        Initialize with reference to parent CrisisAnalyzer
        
        Args:
            crisis_analyzer: Parent CrisisAnalyzer instance
        """
        from .context_integration_helper import ContextIntegrationHelper
        
        self.crisis_analyzer = crisis_analyzer
        self.context_helper = ContextIntegrationHelper(crisis_analyzer)
    # ========================================================================
    
    # ========================================================================
    # CONSOLIDATED SCORING FUNCTIONS
    # ========================================================================
    def extract_depression_score(self, message: str, sentiment_model=None, analysis_config_manager=None, context=None, pattern_detection_manager=None) -> Tuple[float, List[str]]:
        """
        Extract depression indicators from message text
        Migrated from: CrisisAnalyzer.extract_depression_score()
        """
        
        # Use injected managers if not provided
        param_manager = analysis_config_manager or self.crisis_analyzer.analysis_config_manager
        pattern_manager = pattern_detection_manager or self.crisis_analyzer.pattern_detection_manager
        
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
            
            # Pattern-based detection using PatternDetectionManager if available
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
            
            # Configurable parameters from AnalysisConfigManager or consolidated methods
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
                        algorithm_params = self.crisis_analyzer.get_analysis_algorithm_parameters()
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

    def enhanced_depression_analysis(self, message: str, base_score: float = 0.0, sentiment_model=None, analysis_config_manager=None, context=None, pattern_detection_manager=None) -> Dict:
        """
        Enhanced depression analysis with detailed breakdown
        Migrated from: CrisisAnalyzer.enhanced_depression_analysis()
        """
        
        # Use injected manager if not provided
        pattern_manager = pattern_detection_manager or self.crisis_analyzer.pattern_detection_manager
        
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
            
            # Pattern-based adjustments using PatternDetectionManager if available
            pattern_adjustment = 0.0
            if pattern_manager:
                try:
                    # Apply context weights using PatternDetectionManager
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
        """
        Process sentiment model result into standardized format
        Migrated from: CrisisAnalyzer._process_sentiment_result()
        """
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
    
    # ========================================================================
    # RESULTS COMBINATION AND SCORING
    # ========================================================================
    def combine_analysis_results(self, message: str, user_id: str, channel_id: str, model_results: Dict, pattern_analysis: Dict, context_analysis: Dict, start_time: float) -> Dict:
        """
        UPDATED: Combine all analysis results with temporal adjustment integration
        
        CHANGES:
        1. Maintains existing ensemble/pattern/context logic
        2. ADDS temporal adjustment application after base score calculation
        3. Ensures temporal indicators boost crisis scores appropriately
        4. Includes comprehensive temporal analysis tracking
        """
        
        # Calculate base scores from models (existing logic preserved)
        base_score = 0.0
        model_scores = {}
        
        for model_name, result in model_results.items():
            if isinstance(result, dict) and 'score' in result:
                score = float(result['score'])
                model_scores[model_name] = score
                base_score += score * 0.33  # Equal weighting for now
        
        # Apply context adjustments if available (existing logic preserved)
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
        
        # Apply pattern adjustments (existing logic preserved)
        combined_score = base_score
        if pattern_analysis and pattern_analysis.get('total_patterns', 0) > 0:
            pattern_boost = 0.0
            patterns_matched = pattern_analysis.get('patterns_matched', [])
            
            for pattern in patterns_matched:
                if isinstance(pattern, dict):
                    pattern_score = pattern.get('confidence', 0.5)
                    pattern_weight = pattern.get('weight', 0.1)
                    pattern_boost += pattern_score * pattern_weight
            
            combined_score += pattern_boost
            logger.debug(f"Applied pattern boost: +{pattern_boost:.3f}")
        
        # NEW: Apply temporal adjustments to the combined score
        try:
            final_score, temporal_details = self._apply_temporal_adjustments(
                combined_score, message, pattern_analysis
            )
            
            if temporal_details.get('temporal_boost_applied', False):
                logger.debug(f"🕐 Temporal boost applied: {combined_score:.3f} → {final_score:.3f}")
            else:
                final_score = combined_score
                logger.debug("🕐 No temporal factors - no temporal adjustment")
                
        except Exception as e:
            logger.warning(f"⚠️ Temporal adjustment failed: {e}")
            final_score = combined_score  # Resilient fallback
            temporal_details = {
                'temporal_boost_applied': False,
                'error': str(e),
                'final_score': combined_score
            }
        
        # Ensure score is within valid range
        final_score = max(0.0, min(1.0, final_score))
        
        # Calculate confidence score
        total_confidence = 0.0
        confidence_count = 0
        
        for result in model_results.values():
            if isinstance(result, dict) and 'confidence' in result:
                total_confidence += float(result['confidence'])
                confidence_count += 1
        
        confidence_score = total_confidence / confidence_count if confidence_count > 0 else 0.5
        
        # Apply pattern confidence boost if patterns matched
        if pattern_analysis and pattern_analysis.get('total_patterns', 0) > 0:
            confidence_score = min(1.0, confidence_score + 0.1)
        
        # Build comprehensive result with temporal analysis
        result = {
            'crisis_score': final_score,
            'confidence_score': confidence_score,
            'base_score': base_score,
            'combined_score_before_temporal': combined_score,
            'model_scores': model_scores,
            'processing_time': (time.time() - start_time) * 1000,
            'analysis_components': {
                'model_analysis': bool(model_results),
                'pattern_analysis': bool(pattern_analysis and pattern_analysis.get('total_patterns', 0) > 0),
                'context_analysis': bool(context_analysis and context_analysis.get('context_manager_status') == 'available'),
                'temporal_analysis': temporal_details.get('temporal_boost_applied', False)
            },
            'temporal_analysis': temporal_details,
            'method': 'enhanced_scoring_with_temporal_adjustment'
        }
        
        logger.debug(f"🔧 Final combined analysis result: {final_score:.3f} "
                    f"(base: {base_score:.3f}, temporal: {temporal_details.get('temporal_boost_applied', False)})")
        
        return result

    def _extract_categories(self, pattern_analysis: Dict) -> List[str]:
        """
        Extract detected categories from pattern analysis
        Migrated from: CrisisAnalyzer._extract_categories()
        """
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
    # ========================================================================
    
    # ========================================================================
    # ENSEMBLE SCORING METHODS
    # ========================================================================
    def combine_ensemble_model_results(self, model_results: List[Dict]) -> Dict[str, Any]:
        """
        Combine multiple model results
        Migrated from: CrisisAnalyzer.combine_ensemble_model_results()
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
                boost = self.crisis_analyzer.get_analysis_confidence_boosts().get('pattern_match', 0.1)
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
            return self.crisis_analyzer._safe_analysis_execution(
                "combine_ensemble_model_results",
                lambda: {'crisis_score': 0.0, 'confidence': 0.0, 'model_count': 0, 'error': str(e)}
            )

    def apply_analysis_ensemble_weights(self, results: Dict, weights: List[float] = None) -> Dict[str, Any]:
        """
        Apply ensemble weights to analysis results
        Migrated from: CrisisAnalyzer.apply_analysis_ensemble_weights()
        """
        try:
            if weights is None:
                algorithm_params = self.crisis_analyzer.get_analysis_algorithm_parameters()
                weights = algorithm_params.get('ensemble_weights', [0.4, 0.3, 0.3])
            
            individual_scores = results.get('individual_scores', [])
            if not individual_scores or len(individual_scores) != len(weights):
                logger.warning("Score/weight mismatch - using equal weighting")
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
            return self.crisis_analyzer._safe_analysis_execution(
                "apply_analysis_ensemble_weights",
                lambda: {**results, 'weighted_crisis_score': results.get('crisis_score', 0.0)}
            )
    # ========================================================================

    # ========================================================================
    # TEMPORAL SETTINGS
    # ========================================================================
    def _apply_temporal_adjustments(self, base_score: float, message: str, pattern_analysis: Dict[str, Any] = None) -> Tuple[float, Dict[str, Any]]:
        """
        NEW METHOD: Apply temporal boost factors to crisis scores
        
        This method extracts temporal indicators from pattern analysis and applies
        appropriate boosts for immediate intervention capability.
        
        Args:
            base_score: Base crisis score before temporal adjustments
            message: Original message for direct pattern detection if needed
            pattern_analysis: Pattern analysis results containing temporal indicators
            
        Returns:
            Tuple of (adjusted_score, temporal_analysis_details)
        """
        try:
            temporal_details = {
                'temporal_boost_applied': False,
                'temporal_factors_found': [],
                'total_temporal_boost': 0.0,
                'original_score': base_score,
                'final_score': base_score
            }
            
            # Extract temporal factors from pattern analysis
            temporal_factors = self._extract_temporal_factors_from_analysis(pattern_analysis, message)
            
            if not temporal_factors:
                logger.debug("No temporal factors found - no temporal adjustment applied")
                return base_score, temporal_details
            
            # Process temporal factors and calculate boost
            max_boost = 0.0
            applied_indicators = []
            
            for factor in temporal_factors:
                try:
                    # Extract boost value
                    boost_factor = factor.get('boost_factor', 0.0)
                    crisis_boost = factor.get('crisis_boost', 0.0)
                    urgency_score = factor.get('urgency_score', 0.0)
                    indicator_type = factor.get('indicator_type', 'unknown')
                    matched_phrase = factor.get('matched_phrase', '')
                    
                    # Convert string levels to numeric boosts
                    if isinstance(crisis_boost, str):
                        crisis_boost = self._convert_crisis_level_to_boost(crisis_boost)
                    
                    # Use the highest available boost value
                    effective_boost = max(boost_factor, crisis_boost, urgency_score)
                    
                    if effective_boost > 0:
                        max_boost = max(max_boost, effective_boost)
                        applied_indicators.append({
                            'type': indicator_type,
                            'phrase': matched_phrase,
                            'boost': effective_boost
                        })
                        
                except Exception as e:
                    logger.warning(f"Failed to process temporal factor {factor}: {e}")
                    continue
            
            # Apply temporal boost configuration limits
            try:
                # Get max temporal boost from configuration
                max_temporal_boost = self._get_max_temporal_boost_from_config()
                capped_boost = min(max_boost, max_temporal_boost)
            except Exception:
                capped_boost = min(max_boost, 0.50)  # Safe default cap
            
            # Apply temporal adjustment
            if capped_boost > 0:
                adjusted_score = min(1.0, base_score + capped_boost)
                
                # Update temporal details
                temporal_details.update({
                    'temporal_boost_applied': True,
                    'temporal_factors_found': applied_indicators,
                    'total_temporal_boost': capped_boost,
                    'final_score': adjusted_score
                })
                
                logger.info(f"🕐 Temporal adjustment applied: {base_score:.3f} → {adjusted_score:.3f} "
                          f"(boost: +{capped_boost:.3f}, indicators: {len(applied_indicators)})")
                
                for indicator in applied_indicators:
                    logger.debug(f"   📍 {indicator['type']}: +{indicator['boost']:.3f} '{indicator['phrase']}'")
                
                return adjusted_score, temporal_details
            
            return base_score, temporal_details
            
        except Exception as e:
            logger.error(f"❌ Temporal adjustment failed: {e}")
            # Resilient fallback per Clean Architecture Charter Rule #5
            temporal_details['error'] = str(e)
            return base_score, temporal_details

    def _extract_temporal_factors_from_analysis(self, pattern_analysis: Dict[str, Any], message: str) -> List[Dict[str, Any]]:
        """
        Extract temporal factors from pattern analysis results
        
        Args:
            pattern_analysis: Pattern analysis results
            message: Original message for direct extraction if needed
            
        Returns:
            List of temporal factors with boost information
        """
        try:
            temporal_factors = []
            
            # Try to extract from pattern analysis first
            if pattern_analysis:
                # Check for temporal analysis in pattern details
                temporal_analysis = pattern_analysis.get('temporal_analysis', {})
                if temporal_analysis and 'found_indicators' in temporal_analysis:
                    for indicator in temporal_analysis['found_indicators']:
                        temporal_factors.append({
                            'indicator_type': indicator.get('indicator_type', 'unknown'),
                            'boost_factor': indicator.get('boost_factor', 0.0),
                            'crisis_boost': indicator.get('crisis_boost', 0.0),
                            'urgency_score': indicator.get('urgency_score', 0.0),
                            'matched_phrase': indicator.get('matched_phrase', ''),
                            'temporal_category': indicator.get('temporal_category', 'general')
                        })
                
                # Check pattern matches for temporal patterns
                pattern_matches = pattern_analysis.get('pattern_matches', [])
                for match in pattern_matches:
                    if isinstance(match, dict) and 'temporal' in match.get('pattern_type', '').lower():
                        temporal_factors.append({
                            'indicator_type': match.get('pattern_group', 'pattern_match'),
                            'boost_factor': match.get('boost_factor', 0.0),
                            'crisis_boost': match.get('crisis_level', 'none'),
                            'urgency_score': match.get('urgency_score', 0.0),
                            'matched_phrase': match.get('matched_text', ''),
                            'temporal_category': 'pattern_match'
                        })
            
            # If no temporal factors found, try direct pattern detection
            if not temporal_factors and hasattr(self.crisis_analyzer, 'pattern_detection_manager'):
                try:
                    pattern_manager = self.crisis_analyzer.pattern_detection_manager
                    if pattern_manager and hasattr(pattern_manager, 'analyze_temporal_indicators'):
                        temporal_analysis = pattern_manager.analyze_temporal_indicators(message)
                        
                        if temporal_analysis and 'found_indicators' in temporal_analysis:
                            for indicator in temporal_analysis['found_indicators']:
                                temporal_factors.append({
                                    'indicator_type': indicator.get('indicator_type', 'unknown'),
                                    'boost_factor': indicator.get('boost_factor', 0.0),
                                    'crisis_boost': indicator.get('crisis_boost', 0.0),
                                    'urgency_score': indicator.get('urgency_score', 0.0),
                                    'matched_phrase': indicator.get('matched_phrase', ''),
                                    'temporal_category': indicator.get('temporal_category', 'general')
                                })
                                
                except Exception as e:
                    logger.debug(f"Direct temporal pattern detection failed: {e}")
            
            logger.debug(f"🕐 Extracted {len(temporal_factors)} temporal factors for scoring")
            return temporal_factors
            
        except Exception as e:
            logger.error(f"Failed to extract temporal factors: {e}")
            return []

    def _convert_crisis_level_to_boost(self, crisis_level: str) -> float:
        """
        Convert crisis level string to numeric boost factor
        
        Args:
            crisis_level: Crisis level string ('low', 'medium', 'high', 'critical')
            
        Returns:
            Numeric boost factor
        """
        level_mapping = {
            'critical': 0.40,
            'high': 0.30,
            'medium': 0.20,
            'low': 0.10,
            'none': 0.0
        }
        return level_mapping.get(crisis_level.lower(), 0.0)

    def _get_max_temporal_boost_from_config(self) -> float:
        """
        Get maximum temporal boost limit from configuration
        
        Returns:
            Maximum temporal boost value
        """
        try:
            # Try to get from UnifiedConfigManager
            if hasattr(self.crisis_analyzer, 'unified_config_manager'):
                temporal_config = self.crisis_analyzer.unified_config_manager.get_patterns_crisis('patterns_temporal')
                if temporal_config:
                    escalation_rules = temporal_config.get('escalation_rules', {})
                    return float(escalation_rules.get('max_temporal_boost', 0.50))
            
            # Fallback to safe default
            return 0.50
            
        except Exception as e:
            logger.warning(f"Failed to get temporal boost configuration: {e}")
            return 0.50  # Safe default
# ========================================================================