# ash-nlp/analysis/helpers/scoring_calculation_helper.py
"""
Scoring Calculation Helper for CrisisAnalyzer
FILE VERSION: v3.1-3e-5.5-6-1
CREATED: 2025-08-20
PHASE: 3e Sub-step 5.5-6 - CrisisAnalyzer Optimization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

MIGRATION NOTICE: Methods moved from CrisisAnalyzer for optimization
Original location: analysis/crisis_analyzer.py - scoring and calculation methods
"""

import logging
from typing import Dict, List, Tuple, Any, Optional

logger = logging.getLogger(__name__)

class ScoringCalculationHelper:
    """Helper class for scoring calculations moved from CrisisAnalyzer"""
    
    def __init__(self, crisis_analyzer):
        """
        Initialize with reference to parent CrisisAnalyzer
        
        Args:
            crisis_analyzer: Parent CrisisAnalyzer instance
        """
        self.crisis_analyzer = crisis_analyzer
    
    # ========================================================================
    # CONSOLIDATED SCORING FUNCTIONS (Migrated from CrisisAnalyzer)
    # ========================================================================
    
    def extract_depression_score(self, message: str, sentiment_model=None, analysis_parameters_manager=None, context=None, crisis_pattern_manager=None) -> Tuple[float, List[str]]:
        """
        Extract depression indicators from message text
        Migrated from: CrisisAnalyzer.extract_depression_score()
        """
        
        # Use injected managers if not provided
        param_manager = analysis_parameters_manager or self.crisis_analyzer.analysis_parameters_manager
        pattern_manager = crisis_pattern_manager or self.crisis_analyzer.crisis_pattern_manager
        
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

    def enhanced_depression_analysis(self, message: str, base_score: float = 0.0, sentiment_model=None, analysis_parameters_manager=None, context=None, crisis_pattern_manager=None) -> Dict:
        """
        Enhanced depression analysis with detailed breakdown
        Migrated from: CrisisAnalyzer.enhanced_depression_analysis()
        """
        
        # Use injected manager if not provided
        pattern_manager = crisis_pattern_manager or self.crisis_analyzer.crisis_pattern_manager
        
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
    # RESULTS COMBINATION AND SCORING
    # ========================================================================
    
    def combine_analysis_results(self, message: str, user_id: str, channel_id: str, model_results: Dict, pattern_analysis: Dict, context_analysis: Dict, start_time: float) -> Dict:
        """
        Combine all analysis results with context integration
        Migrated from: CrisisAnalyzer._combine_analysis_results()
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
        crisis_level = self.crisis_analyzer.apply_crisis_thresholds(final_score)
        
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
                    'analysis_version': 'v3.1-3e-5.5-6',
                    'features_used': {
                        'ensemble_analysis': bool(model_results),
                        'pattern_analysis': bool(pattern_analysis),
                        'context_analysis': bool(context_analysis),
                        'context_manager_available': context_analysis.get('context_manager_status') == 'available',
                        'learning_enhanced': bool(self.crisis_analyzer.learning_system_manager),
                        'shared_utilities': bool(self.crisis_analyzer.shared_utilities_manager)
                    }
                }
            },
            'requires_staff_review': self.crisis_analyzer._determine_staff_review_requirement(final_score, crisis_level),
            'processing_time': time.time() - start_time
        }

        # Debug
        logger.debug(f"Final response crisis_level={crisis_level}, confidence_score={final_score}")
        logger.debug(f"Enhanced: needs_response={crisis_level != 'none'}")
        logger.debug(f"Response structure keys: {list(response.keys())}")

        return response

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