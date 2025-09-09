# ash-nlp/managers/helpers/ensemble_voting_helper.py
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
Ensemble Voting and Weight Management Helper for Ash-NLP Service
---
FILE VERSION: v3.1-3e-7-1
LAST MODIFIED: 2025-09-09
PHASE: 3e Step 7 - Model Coordination Refactoring
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Handle ensemble voting logic and dynamic weight management
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class EnsembleVotingHelper:
    """
    Ensemble Voting and Weight Management Helper
    
    Handles:
    - Ensemble classification with multiple models
    - Weighted, majority, and consensus voting
    - Dynamic weight management and optimization
    - Crisis analyzer reference management
    """
    
    def __init__(self, config_manager, model_coordination_manager, classification_helper):
        """
        Initialize Ensemble Voting Helper
        
        Args:
            config_manager: UnifiedConfigManager instance
            model_coordination_manager: Parent ModelCoordinationManager instance
            classification_helper: ClassificationHelper instance
        """
        if config_manager is None:
            raise ValueError("UnifiedConfigManager is required for EnsembleVotingHelper")
        if model_coordination_manager is None:
            raise ValueError("ModelCoordinationManager is required for EnsembleVotingHelper")
        if classification_helper is None:
            raise ValueError("ClassificationHelper is required for EnsembleVotingHelper")
        
        self.config_manager = config_manager
        self.model_manager = model_coordination_manager
        self.classification_helper = classification_helper
        
        logger.info("EnsembleVotingHelper initialized for ensemble voting and weight management")

    async def classify_with_ensemble(self, text: str, zero_shot_manager=None) -> Dict[str, Any]:
        """
        Ensemble classification using multiple models
        
        Args:
            text: Text to classify
            zero_shot_manager: ZeroShotManager instance for label management
            
        Returns:
            Ensemble classification results
        """
        try:
            model_results = {}
            models = self.model_manager.get_model_definitions()
            
            # Check for dynamic weights from performance optimizer
            dynamic_weights = self._get_dynamic_weights_if_available()
            if dynamic_weights:
                logger.info(f"🎯 ASYNC ENSEMBLE: Using dynamic weights: {dynamic_weights}")
            else:
                logger.info(f"🎯 ASYNC ENSEMBLE: Using configuration weights")
            
            # Get labels from ZeroShotManager if available
            labels = None
            hypothesis_template = "This text expresses {}."
            
            if zero_shot_manager:
                try:
                    all_labels = zero_shot_manager.get_all_labels()
                    zero_shot_settings = zero_shot_manager.get_zero_shot_settings()
                    hypothesis_template = zero_shot_settings.get('hypothesis_template', hypothesis_template)
                    logger.debug(f"✅ Using ZeroShotManager for label management")
                except Exception as e:
                    logger.warning(f"⚠️ ZeroShotManager access failed: {e}")
                    all_labels = {}
            else:
                all_labels = {}
            
            # Classify with each model
            for model_type in models.keys():
                try:
                    # Get labels for this model type
                    if isinstance(all_labels, dict) and model_type in all_labels:
                        model_labels = all_labels[model_type]
                    elif isinstance(all_labels, dict):
                        # Use general labels if model-specific not available
                        model_labels = all_labels.get('crisis', all_labels.get('enhanced_crisis', []))
                    else:
                        model_labels = self.classification_helper._get_fallback_labels(model_type)
                    
                    if not model_labels:
                        model_labels = self.classification_helper._get_fallback_labels(model_type)
                    
                    # Perform classification
                    result = await self.classification_helper.classify_with_zero_shot(
                        text, model_labels, model_type, hypothesis_template
                    )
                    model_results[model_type] = result
                    
                except Exception as e:
                    logger.error(f"❌ Model {model_type} classification failed: {e}")
                    model_results[model_type] = {
                        'score': 0.0,
                        'confidence': 0.0,
                        'error': str(e),
                        'model_type': model_type
                    }
            
            # Perform ensemble voting with dynamic weights
            ensemble_result = self._perform_ensemble_voting(model_results, override_weights=dynamic_weights)
            
            return {
                'ensemble_score': ensemble_result['score'],
                'ensemble_confidence': ensemble_result['confidence'],
                'ensemble_mode': self.model_manager.get_ensemble_mode(),
                'individual_results': model_results,
                'models_used': len(model_results),
                'zero_shot_manager_used': zero_shot_manager is not None,
                'method': 'ensemble_classification',
                'dynamic_weights_used': dynamic_weights is not None,
                'weights_source': 'dynamic' if dynamic_weights else 'configuration'
            }
            
        except Exception as e:
            logger.error(f"❌ Ensemble classification failed: {e}")
            return {
                'ensemble_score': 0.0,
                'ensemble_confidence': 0.0,
                'error': str(e),
                'method': 'ensemble_classification_error'
            }

    def _perform_ensemble_voting(self, model_results: Dict[str, Dict], override_weights: Dict[str, float] = None) -> Dict[str, float]:
        """
        Perform ensemble voting on multiple model results
        
        Args:
            model_results: Dictionary of model results
            override_weights: Optional weights to override configuration weights
            
        Returns:
            Ensemble score and confidence
        """
        logger.debug("WEIGHT DEBUG: EnsembleVotingHelper voting called!")
        if override_weights:
            logger.debug(f"🎯 WEIGHT DEBUG: Using override weights: {override_weights}")
        else:
            logger.debug(f"🎯 WEIGHT DEBUG: Using configuration weights")
            
        try:
            ensemble_mode = self.model_manager.get_ensemble_mode()
            valid_results = []
            
            # Extract valid results
            for model_type, result in model_results.items():
                if isinstance(result, dict) and 'score' in result:
                    score = result.get('score', 0.0)
                    confidence = result.get('confidence', 0.0)
                    
                    # Use override weights if provided
                    if override_weights and model_type in override_weights:
                        weight = override_weights[model_type]
                        logger.debug(f"🎯 WEIGHT DEBUG: {model_type} using OVERRIDE weight {weight}")
                    else:
                        weight = self.model_manager.get_model_weight(model_type)
                        logger.debug(f"🎯 WEIGHT DEBUG: {model_type} using CONFIG weight {weight}")
                            
                    valid_results.append({
                        'score': score,
                        'confidence': confidence,
                        'weight': weight,
                        'model_type': model_type
                    })
            
            if not valid_results:
                return {'score': 0.0, 'confidence': 0.0}
            
            # Perform voting based on ensemble mode
            if ensemble_mode == 'weighted':
                return self._weighted_ensemble_voting(valid_results)
            elif ensemble_mode == 'majority':
                return self._majority_ensemble_voting(valid_results)
            elif ensemble_mode == 'consensus':
                return self._consensus_ensemble_voting(valid_results)
            else:
                # Default to weighted
                return self._weighted_ensemble_voting(valid_results)
                
        except Exception as e:
            logger.error(f"❌ Ensemble voting failed: {e}")
            return {'score': 0.0, 'confidence': 0.0}
    
    def _weighted_ensemble_voting(self, results: List[Dict]) -> Dict[str, float]:
        """Weighted ensemble voting"""
        total_weight = sum(r['weight'] for r in results)
        if total_weight == 0:
            return {'score': 0.0, 'confidence': 0.0}
        
        weighted_score = sum(r['score'] * r['weight'] for r in results) / total_weight
        weighted_confidence = sum(r['confidence'] * r['weight'] for r in results) / total_weight
        
        return {'score': weighted_score, 'confidence': weighted_confidence}
    
    def _majority_ensemble_voting(self, results: List[Dict]) -> Dict[str, float]:
        """Majority ensemble voting"""
        if not results:
            return {'score': 0.0, 'confidence': 0.0}
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        return {'score': avg_score, 'confidence': avg_confidence}
    
    def _consensus_ensemble_voting(self, results: List[Dict]) -> Dict[str, float]:
        """Consensus ensemble voting"""
        if not results:
            return {'score': 0.0, 'confidence': 0.0}
        
        # For consensus, require agreement (similar scores)
        scores = [r['score'] for r in results]
        score_std = (sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores))**0.5
        
        if score_std > 0.3:  # High disagreement
            consensus_confidence = 0.3
        else:
            consensus_confidence = 0.8
        
        avg_score = sum(scores) / len(scores)
        return {'score': avg_score, 'confidence': consensus_confidence}

    def _get_dynamic_weights_if_available(self) -> Optional[Dict[str, float]]:
        """
        Get dynamic weights from performance optimizer cache if available
        
        This method attempts to access the performance optimizer cache to get weights
        that were set via the /ensemble/set-weights endpoint.
        
        Returns:
            Dict of dynamic weights if available, None if not available or not set
        """
        try:
            # Method 1: Check if we have a stored reference to the crisis analyzer
            if hasattr(self, '_crisis_analyzer_ref'):
                crisis_analyzer = self._crisis_analyzer_ref()  # Weak reference
                if (crisis_analyzer and 
                    hasattr(crisis_analyzer, 'performance_optimizer') and
                    hasattr(crisis_analyzer.performance_optimizer, '_cached_model_weights')):
                    
                    cached_weights = crisis_analyzer.performance_optimizer._cached_model_weights
                    if cached_weights and isinstance(cached_weights, dict) and len(cached_weights) > 0:
                        logger.debug(f"🎯 Found dynamic weights via crisis analyzer: {cached_weights}")
                        return cached_weights
            
            # Method 2: Try to find the crisis analyzer through global module search
            try:
                import gc
                # Search for CrisisAnalyzer instances in memory
                for obj in gc.get_objects():
                    if (hasattr(obj, '__class__') and 
                        obj.__class__.__name__ == 'CrisisAnalyzer' and
                        hasattr(obj, 'performance_optimizer') and
                        hasattr(obj.performance_optimizer, '_cached_model_weights')):
                        
                        cached_weights = obj.performance_optimizer._cached_model_weights
                        if cached_weights and isinstance(cached_weights, dict) and len(cached_weights) > 0:
                            logger.debug(f"🎯 Found dynamic weights via memory search: {cached_weights}")
                            return cached_weights
            except Exception as e:
                logger.debug(f"Memory search failed: {e}")
            
            # Method 3: Check for global variables that might contain the crisis analyzer
            try:
                import sys
                # Check main module
                main_module = sys.modules.get('__main__')
                if main_module:
                    for attr_name in dir(main_module):
                        try:
                            attr_value = getattr(main_module, attr_name)
                            if (hasattr(attr_value, 'performance_optimizer') and
                                hasattr(attr_value.performance_optimizer, '_cached_model_weights')):
                                
                                cached_weights = attr_value.performance_optimizer._cached_model_weights
                                if cached_weights and isinstance(cached_weights, dict):
                                    logger.debug(f"🎯 Found dynamic weights via main.{attr_name}: {cached_weights}")
                                    return cached_weights
                        except Exception:
                            continue
            except Exception as e:
                logger.debug(f"Global variable search failed: {e}")
            
            # No dynamic weights found
            logger.debug("🔧 No dynamic weights found, will use configuration weights")
            return None
            
        except Exception as e:
            logger.warning(f"Failed to check for dynamic weights: {e}")
            return None

    def set_crisis_analyzer_reference(self, crisis_analyzer):
        """
        Set a weak reference to the crisis analyzer for dynamic weight access
        
        This method allows the EnsembleVotingHelper to access the performance optimizer
        cache through the crisis analyzer. This should be called during initialization.
        
        Args:
            crisis_analyzer: CrisisAnalyzer instance
        """
        try:
            import weakref
            self._crisis_analyzer_ref = weakref.ref(crisis_analyzer)
            logger.debug("🔗 Crisis analyzer reference set for dynamic weight access")
        except Exception as e:
            logger.warning(f"Failed to set crisis analyzer reference: {e}")

# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_ensemble_voting_helper(config_manager, model_coordination_manager, classification_helper) -> EnsembleVotingHelper:
    """
    Factory function to create EnsembleVotingHelper instance
    
    Args:
        config_manager: UnifiedConfigManager instance
        model_coordination_manager: ModelCoordinationManager instance
        classification_helper: ClassificationHelper instance
        
    Returns:
        EnsembleVotingHelper instance
    """
    return EnsembleVotingHelper(config_manager, model_coordination_manager, classification_helper)
# ============================================================================

__all__ = [
    'EnsembleVotingHelper',
    'create_ensemble_voting_helper'
]

logger.info("EnsembleVotingHelper v3.1-3e-7-1 loaded - Ensemble voting and weight management functionality")