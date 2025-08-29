# ash-nlp/analysis/helpers/analysis_tracking_helper.py
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
Analysis Tracking Helper for Phase 4a Step 2 - Analysis Flow Verification
---
FILE VERSION: v3.1-4a-2-1
LAST MODIFIED: 2025-08-28
PHASE: 4a, Step 2 - Analysis Flow Verification & Tracking
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
import time
from typing import Dict, List, Tuple, Any, Optional

logger = logging.getLogger(__name__)

class AnalysisTrackingHelper:
    """
    Phase 4a Step 2: Helper class for comprehensive analysis flow tracking
    
    This helper provides all tracking functionality for the enhanced CrisisAnalyzer,
    allowing complete visibility into each step of the analysis pipeline without
    cluttering the main CrisisAnalyzer class.
    """
    
    def __init__(self, crisis_analyzer):
        """
        Initialize tracking helper with CrisisAnalyzer instance
        
        Args:
            crisis_analyzer: CrisisAnalyzer instance to track
        """
        self.crisis_analyzer = crisis_analyzer
        self.enable_tracking = self._get_tracking_config()
        
        logger.info(f"AnalysisTrackingHelper initialized: tracking={'enabled' if self.enable_tracking else 'disabled'}")
    
    def _get_tracking_config(self) -> bool:
        """Get analysis tracking configuration setting with environment variable support"""
        try:
            if self.crisis_analyzer.unified_config_manager:
                # UnifiedConfigManager handles env var overrides and type conversion automatically
                # Use the correct config file: analysis_tracking.json, not analysis_config.json
                tracking_config = self.crisis_analyzer.unified_config_manager.get_config_section(
                    'analysis_tracking', 'tracking.enabled', True
                )
                logger.debug(f"Tracking configuration loaded from analysis_tracking: {tracking_config}")
                return tracking_config
            else:
                logger.warning("UnifiedConfigManager not available, defaulting tracking to enabled")
                return True
                
        except Exception as e:
            logger.error(f"Failed to get tracking config: {e}")
            return True  # Default to enabled for safety

    def init_analysis_tracking(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """Initialize analysis execution tracking structure"""
        # If tracking is disabled, return minimal structure
        if not self.enable_tracking:
            return {
                "tracking_enabled": False,
                "analysis_start_time": time.time(),
                "message_metadata": {
                    "message_length": len(message),
                    "user_id": user_id,
                    "channel_id": channel_id,
                    "timestamp": time.time()
                }
            }
        
        # Full tracking structure when enabled
        return {
            "tracking_enabled": True,
            "analysis_start_time": time.time(),
            "message_metadata": {
                "message_length": len(message),
                "user_id": user_id,
                "channel_id": channel_id,
                "timestamp": time.time()
            },
            "step_1_zero_shot_ai": {
                "executed": False,
                "started": False,
                "completed": False
            },
            "step_2_pattern_enhancement": {
                "executed": False,
                "started": False,
                "completed": False
            },
            "step_3_learning_adjustments": {
                "executed": False,
                "started": False,
                "completed": False
            },
            "fallback_scenarios": {
                "ai_models_failed": False,
                "pattern_only_used": False,
                "emergency_fallback": False
            },
            "performance_metrics": {
                "target_time_ms": 500,
                "optimization_applied": False
            }
        }

    def update_tracking_step(self, tracking: Dict[str, Any], step_name: str, 
                           status: str, data: Dict[str, Any] = None, 
                           error: Exception = None) -> None:
        """Update tracking information for a specific analysis step"""
        if not self.enable_tracking or step_name not in tracking:
            return
        
        step_info = tracking[step_name]
        current_time = time.time()
        
        if status == "started":
            step_info["started"] = True
            step_info["start_time"] = current_time
            
        elif status == "completed":
            step_info["completed"] = True
            step_info["executed"] = True
            step_info["end_time"] = current_time
            
            if "start_time" in step_info:
                step_info["processing_time_ms"] = (current_time - step_info["start_time"]) * 1000
            
            if data:
                step_info.update(data)
                
        elif status == "failed":
            step_info["completed"] = False
            step_info["executed"] = False
            step_info["failed"] = True
            step_info["error"] = str(error) if error else "Unknown error"
            step_info["end_time"] = current_time
            
            if "start_time" in step_info:
                step_info["processing_time_ms"] = (current_time - step_info["start_time"]) * 1000

    def finalize_tracking(self, tracking: Dict[str, Any], final_result: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize tracking information and add to result"""
        current_time = time.time()
        total_time_ms = (current_time - tracking["analysis_start_time"]) * 1000
        
        # If tracking is disabled, add minimal tracking info
        if not self.enable_tracking or not tracking.get("tracking_enabled", True):
            final_result["analysis_execution_tracking"] = {
                "tracking_enabled": False,
                "message_metadata": tracking.get("message_metadata", {}),
                "total_processing_time_ms": total_time_ms
            }
            return final_result
        
        # Calculate summary statistics for enabled tracking
        steps_attempted = sum(1 for step in ["step_1_zero_shot_ai", "step_2_pattern_enhancement", "step_3_learning_adjustments"] 
                             if step in tracking and tracking[step].get("started", False))
        steps_completed = sum(1 for step in ["step_1_zero_shot_ai", "step_2_pattern_enhancement", "step_3_learning_adjustments"] 
                             if step in tracking and tracking[step].get("completed", False))
        
        # Safely get performance metrics
        performance_metrics = tracking.get("performance_metrics", {})
        target_time_ms = performance_metrics.get("target_time_ms", 500)
        
        # Add summary information
        tracking_summary = {
            "total_processing_time_ms": total_time_ms,
            "steps_attempted": steps_attempted,
            "steps_completed": steps_completed,
            "success_rate": (steps_completed / max(steps_attempted, 1)) * 100,
            "performance_target_met": total_time_ms <= target_time_ms,
            "analysis_method": final_result.get("method", "unknown"),
            "crisis_detection_pipeline": {
                "ai_models_used": tracking.get("step_1_zero_shot_ai", {}).get("completed", False),
                "pattern_enhancement_applied": tracking.get("step_2_pattern_enhancement", {}).get("completed", False),
                "learning_adjustments_applied": tracking.get("step_3_learning_adjustments", {}).get("completed", False)
            }
        }
        
        # Clean up internal tracking fields safely
        for step in ["step_1_zero_shot_ai", "step_2_pattern_enhancement", "step_3_learning_adjustments"]:
            if step in tracking and isinstance(tracking[step], dict):
                # Remove internal timestamps but keep processing times
                tracking[step].pop("start_time", None)
                tracking[step].pop("end_time", None)
        
        tracking.pop("analysis_start_time", None)
        
        # Add complete tracking to result
        final_result["analysis_execution_tracking"] = tracking
        final_result["tracking_summary"] = tracking_summary
        
        return final_result

    async def execute_zero_shot_analysis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """Execute zero-shot AI model analysis (Step 1) with tracking"""
        if self.crisis_analyzer.model_coordination_manager:
            # Get zero-shot labels being used
            zero_shot_labels_info = self.get_zero_shot_labels_info()
            
            # Try synchronous path first (optimized)
            try:
                if hasattr(self.crisis_analyzer.model_coordination_manager, 'classify_sync_ensemble'):
                    result = self.crisis_analyzer.model_coordination_manager.classify_sync_ensemble(message, self.crisis_analyzer.zero_shot_manager)
                    if result:
                        return {
                            "crisis_score": result.get("ensemble_score", 0.0),
                            "confidence_score": result.get("ensemble_confidence", 0.0),
                            "method": result.get("method", "sync_ensemble"),
                            "models_used": result.get("models_used", 0),
                            "individual_results": result.get("individual_results", {}),
                            "zero_shot_manager_used": result.get("zero_shot_manager_used", False),
                            "zero_shot_labels_info": zero_shot_labels_info
                        }
                
                # Fallback to async path
                result = await self.crisis_analyzer.model_coordination_manager.classify_ensemble_async(message, self.crisis_analyzer.zero_shot_manager)
                return {
                    "crisis_score": result.get("ensemble_score", 0.0),
                    "confidence_score": result.get("ensemble_confidence", 0.0),
                    "method": result.get("method", "async_ensemble"),
                    "models_used": result.get("models_used", 0),
                    "individual_results": result.get("individual_results", {}),
                    "zero_shot_manager_used": result.get("zero_shot_manager_used", False),
                    "zero_shot_labels_info": zero_shot_labels_info
                }
                
            except Exception as e:
                logger.error(f"Model coordination failed: {e}")
                raise
        else:
            raise RuntimeError("ModelCoordinationManager not available")

    def get_zero_shot_labels_info(self) -> Dict[str, Any]:
        """Get zero-shot labels information for tracking (lightweight reference only)"""
        # Check both general tracking and specific zero-shot tracking
        if not self.enable_tracking:
            return {"labels_available": False, "reason": "Analysis tracking disabled"}
        
        # Check specific zero-shot tracking setting from the correct config file
        try:
            zero_shot_tracking = self.crisis_analyzer.unified_config_manager.get_config_section(
                'analysis_tracking', 'step_tracking.zero_shot_ai_tracking', True
            )
            if not zero_shot_tracking:
                return {"labels_available": False, "reason": "Zero-shot AI tracking disabled"}
        except Exception:
            # If we can't read the config, respect the general tracking setting
            pass
            
        try:
            if not self.crisis_analyzer.zero_shot_manager:
                return {"labels_available": False, "reason": "ZeroShotManager not available"}
            
            # Get ONLY lightweight metadata - no duplicate label fetching
            # The full labels are already in the main ai_model_details section
            current_label_set = self.crisis_analyzer.zero_shot_manager.get_current_label_set()
            zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
            
            return {
                "labels_available": True,
                "current_label_set": current_label_set,
                "hypothesis_template": zero_shot_settings.get("hypothesis_template", "This text expresses {}."),
                "confidence_threshold": zero_shot_settings.get("confidence_threshold", 0.3),
                "multi_label": zero_shot_settings.get("multi_label", False),
                "full_labels_location": "See ai_model_details.zero_shot_labels_info for complete label lists"
            }
            
        except Exception as e:
            logger.warning(f"Failed to get zero-shot labels info: {e}")
            return {
                "labels_available": False, 
                "error": str(e),
                "reason": "Failed to retrieve label information"
            }

    async def execute_pattern_enhancement(self, message: str, ai_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute pattern analysis enhancement (Step 2) with tracking"""
        if self.crisis_analyzer.pattern_detection_manager:
            try:
                # Get enhanced patterns
                pattern_result = self.crisis_analyzer.pattern_detection_manager.analyze_enhanced_patterns(message)
                
                # Calculate enhancement boost
                ai_confidence = ai_result.get("confidence_score", 0.0)
                patterns_found = pattern_result.get("patterns_found", [])
                confidence_boost = len(patterns_found) * 0.05  # 5% boost per pattern found
                
                return {
                    "patterns_found": patterns_found,
                    "pattern_confidence": pattern_result.get("confidence_score", 0.0),
                    "detected_categories": [p.get("category", "unknown") for p in patterns_found],
                    "enhancement_applied": len(patterns_found) > 0,
                    "confidence_boost": confidence_boost,
                    "enhanced_confidence": min(1.0, ai_confidence + confidence_boost)
                }
                
            except Exception as e:
                logger.error(f"Pattern analysis failed: {e}")
                raise
        else:
            return {
                "patterns_found": [],
                "enhancement_applied": False,
                "confidence_boost": 0.0,
                "reason": "PatternDetectionManager not available"
            }

    async def execute_learning_adjustments(self, ai_result: Dict[str, Any], pattern_result: Dict[str, Any], 
                                          user_id: str, channel_id: str) -> Dict[str, Any]:
        """Execute learning system adjustments (Step 3) with tracking"""
        try:
            combined_result = {**ai_result, **pattern_result}
            learning_adjustment = self.crisis_analyzer.learning_system_manager.apply_learning_adjustments(
                combined_result, user_id, channel_id
            )
            
            return {
                "adjustments": learning_adjustment.get("adjustments", {}),
                "confidence_delta": learning_adjustment.get("confidence_delta", 0.0),
                "adjusted_score": learning_adjustment.get("adjusted_score", ai_result.get("crisis_score", 0.0)),
                "metadata": learning_adjustment.get("metadata", {}),
                "learning_applied": True
            }
            
        except Exception as e:
            logger.error(f"Learning adjustments failed: {e}")
            raise

    def combine_analysis_results(self, ai_result: Dict[str, Any], pattern_result: Dict[str, Any], 
                                learning_result: Dict[str, Any]) -> Dict[str, Any]:
        """Combine results from all analysis steps with enhanced tracking"""
        # Base score from AI models
        base_score = ai_result.get("crisis_score", 0.0)
        base_confidence = ai_result.get("confidence_score", 0.0)
        
        # Apply pattern enhancement
        pattern_boost = pattern_result.get("confidence_boost", 0.0)
        enhanced_confidence = min(1.0, base_confidence + pattern_boost)
        
        # Apply learning adjustments
        final_score = learning_result.get("adjusted_score", base_score)
        
        # Determine crisis level
        crisis_level = self.crisis_analyzer.apply_crisis_thresholds(final_score)
        
        return {
            "crisis_score": final_score,
            "confidence_score": enhanced_confidence,
            "crisis_level": crisis_level,
            "needs_response": crisis_level in ["medium", "high", "critical"],
            "requires_staff_review": crisis_level in ["high", "critical"],
            "method": "enhanced_three_step_analysis",
            "detected_categories": pattern_result.get("detected_categories", []),
            "ai_model_details": {
                "models_used": ai_result.get("models_used", []),
                "individual_results": ai_result.get("individual_results", {}),
                "base_confidence": base_confidence,
                "zero_shot_labels_info": ai_result.get("zero_shot_labels_info", {})
            },
            "pattern_analysis": {
                "patterns_matched": pattern_result.get("patterns_found", []),
                "enhancement_boost": pattern_boost,
                "pattern_confidence": pattern_result.get("pattern_confidence", 0.0)
            },
            "learning_adjustments": {
                "applied": learning_result.get("learning_applied", False),
                "score_adjustment": final_score - base_score,
                "metadata": learning_result.get("metadata", {})
            }
        }

# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_analysis_tracking_helper(crisis_analyzer) -> AnalysisTrackingHelper:
    """
    Factory function for AnalysisTrackingHelper
    
    Args:
        crisis_analyzer: CrisisAnalyzer instance
        
    Returns:
        AnalysisTrackingHelper instance
    """
    return AnalysisTrackingHelper(crisis_analyzer)

__all__ = ['AnalysisTrackingHelper', 'create_analysis_tracking_helper']

logger.info("AnalysisTrackingHelper v3.1-4a-2-1 loaded - Phase 4a Step 2 tracking functionality complete")