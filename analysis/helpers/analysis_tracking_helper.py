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
    
    # ============================================================================
    # INITIALIZE
    # ============================================================================
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
    # ============================================================================

    # ============================================================================
    # TRACKING
    # ============================================================================
    def update_tracking_step(self, tracking: Dict[str, Any], step_name: str, status: str, data: Dict[str, Any] = None, error: Exception = None) -> None:
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
    # ============================================================================

    # ============================================================================
    # ANALYSIS
    # ============================================================================
    async def execute_zero_shot_analysis(self, message: str, user_id: str, channel_id: str) -> Dict[str, Any]:
        """Execute zero-shot AI model analysis (Step 1) with tracking"""
        if self.crisis_analyzer.model_coordination_manager:
            # Get zero-shot labels being used
            zero_shot_labels_info = self.get_zero_shot_labels_info()
            
            # Try synchronous path first (optimized)
            try:
                if hasattr(self.crisis_analyzer.model_coordination_manager, 'classify_sync_ensemble'):
                    # Get dynamic weights from performance optimizer if available
                    dynamic_weights = None
                    if (hasattr(self.crisis_analyzer, 'performance_optimizer') and 
                        hasattr(self.crisis_analyzer.performance_optimizer, '_cached_model_weights')):
                        dynamic_weights = self.crisis_analyzer.performance_optimizer._cached_model_weights

                    result = self.crisis_analyzer.model_coordination_manager.classify_sync_ensemble(
                        message, 
                        self.crisis_analyzer.zero_shot_manager,
                        override_weights=dynamic_weights
                    )

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
                result = await self.crisis_analyzer.model_coordination_manager.classify_with_ensemble(message, self.crisis_analyzer.zero_shot_manager)
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
        """Get detailed zero-shot labels information for tracking (only when tracking enabled)"""
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
            
            # Get full label information when tracking is enabled
            current_label_set = self.crisis_analyzer.zero_shot_manager.get_current_label_set()
            all_labels = self.crisis_analyzer.zero_shot_manager.get_all_labels()
            zero_shot_settings = self.crisis_analyzer.zero_shot_manager.get_zero_shot_settings()
            
            return {
                "labels_available": True,
                "current_label_set": current_label_set,
                "labels_by_category": all_labels,
                "total_label_categories": len(all_labels),
                "total_labels": sum(len(labels) for labels in all_labels.values()),
                "hypothesis_template": zero_shot_settings.get("hypothesis_template", "This text expresses {}."),
                "confidence_threshold": zero_shot_settings.get("confidence_threshold", 0.25),
                "multi_label": zero_shot_settings.get("multi_label", False)
            }
            
        except Exception as e:
            logger.warning(f"Failed to get zero-shot labels info: {e}")
            return {
                "labels_available": False, 
                "error": str(e),
                "reason": "Failed to retrieve label information"
            }
    # ============================================================================

    # ============================================================================
    # EXECUTE!
    # ============================================================================
    async def execute_pattern_enhancement(self, message: str, ai_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Execute pattern enhancement analysis (Step 2) with proper temporal data inclusion
        
        CHANGES MADE:
        1. Ensures temporal analysis results are included in pattern_result
        2. Properly structures temporal data for _extract_temporal_factors_from_pattern_result
        3. Maintains backward compatibility with existing pattern analysis
        """
        try:
            start_time = time.time()
            
            # Get pattern analysis from PatternDetectionManager
            pattern_analysis = self.crisis_analyzer.pattern_detection_manager.analyze_enhanced_patterns(message)
            
            # CRITICAL FIX: Ensure temporal analysis is properly included
            temporal_analysis = {}
            if hasattr(self.crisis_analyzer.pattern_detection_manager, 'analyze_temporal_indicators'):
                try:
                    temporal_analysis = self.crisis_analyzer.pattern_detection_manager.analyze_temporal_indicators(message)
                    logger.debug(f"🕐 Temporal analysis extracted: {len(temporal_analysis.get('found_indicators', []))} indicators")
                except Exception as e:
                    logger.warning(f"⚠️ Temporal analysis extraction failed: {e}")
                    temporal_analysis = {'found_indicators': [], 'urgency_score': 0.0}
            
            # Build comprehensive pattern result with temporal data
            pattern_result = {
                'patterns_found': pattern_analysis.get('patterns_triggered', []),
                'detected_categories': pattern_analysis.get('detected_categories', []),
                'enhancement_applied': len(pattern_analysis.get('patterns_triggered', [])) > 0,
                'confidence_boost': pattern_analysis.get('confidence_boost', 0.0),
                'pattern_confidence': pattern_analysis.get('pattern_confidence', 0.0),
                'details': pattern_analysis.get('details', {}),
                
                # CRITICAL FIX: Include temporal analysis at the top level
                'temporal_analysis': temporal_analysis,
                
                # ALSO include in details for backward compatibility
                'details': {
                    **pattern_analysis.get('details', {}),
                    'temporal_analysis': temporal_analysis
                }
            }
            
            # ADDITIONAL FIX: Convert temporal indicators to the format expected by extraction
            temporal_factors = []
            for indicator in temporal_analysis.get('found_indicators', []):
                temporal_factors.append({
                    'indicator_type': indicator.get('indicator_type', 'unknown'),
                    'boost_factor': indicator.get('boost_factor', 0.0),
                    'crisis_boost': indicator.get('crisis_boost', 0.0),
                    'urgency_score': indicator.get('urgency_score', 0.0),
                    'matched_phrase': indicator.get('matched_phrase', ''),
                    'temporal_category': indicator.get('temporal_category', 'general')
                })
            
            # Include temporal factors directly in pattern result for easier extraction
            pattern_result['temporal_factors'] = temporal_factors
            
            processing_time = (time.time() - start_time) * 1000
            pattern_result['processing_time_ms'] = processing_time
            
            logger.debug(f"Pattern enhancement completed with temporal data: "
                        f"{len(pattern_result['patterns_found'])} patterns, "
                        f"{len(temporal_factors)} temporal factors")
            
            return pattern_result
            
        except Exception as e:
            logger.error(f"Pattern enhancement execution failed: {e}")
            raise

    async def execute_learning_adjustments(self, ai_result: Dict[str, Any], pattern_result: Dict[str, Any], user_id: str, channel_id: str) -> Dict[str, Any]:
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
    # ============================================================================

    # ============================================================================
    # COMBINE IT ALL!
    # ============================================================================
    def combine_analysis_results(self, ai_result: Dict[str, Any], pattern_result: Dict[str, Any], learning_result: Dict[str, Any], mode: Optional[str] = None) -> Dict[str, Any]:
        """
        UPDATED: Combine results from all analysis steps with temporal adjustment integration
        
        CHANGES:
        1. Maintains existing AI + pattern + learning combination logic
        2. ADDS temporal adjustment application after learning adjustments
        3. Ensures temporal indicators boost crisis scores appropriately
        4. Includes comprehensive temporal analysis tracking
        """
        # Base score from AI models (existing logic preserved)
        base_score = ai_result.get("crisis_score", 0.0)
        base_confidence = ai_result.get("confidence_score", 0.0)
        
        # Apply pattern enhancement (existing logic preserved)
        pattern_boost = pattern_result.get("confidence_boost", 0.0)
        enhanced_confidence = min(1.0, base_confidence + pattern_boost)
        
        # Apply learning adjustments (existing logic preserved)
        learning_adjusted_score = learning_result.get("adjusted_score", base_score)
        
        # NEW: Apply temporal adjustments to the learning-adjusted score
        try:
            temporal_factors = self._extract_temporal_factors_from_pattern_result(pattern_result)
            final_score, temporal_details = self._apply_temporal_adjustments(
                learning_adjusted_score, temporal_factors
            )
            
            if temporal_details.get('temporal_boost_applied', False):
                logger.info(f"🕐 Temporal adjustment applied: {learning_adjusted_score:.3f} → {final_score:.3f} "
                          f"(boost: +{temporal_details.get('total_temporal_boost', 0.0):.3f})")
            else:
                final_score = learning_adjusted_score
                logger.debug("🕐 No temporal factors - no temporal adjustment")
                
        except Exception as e:
            logger.warning(f"⚠️ Temporal adjustment failed: {e}")
            final_score = learning_adjusted_score  # Resilient fallback
            temporal_details = {
                'temporal_boost_applied': False,
                'error': str(e),
                'final_score': learning_adjusted_score
            }
        
        # Determine crisis level using final score (existing logic preserved)
        crisis_level = self.crisis_analyzer.apply_crisis_thresholds(final_score, mode)
        
        # Build comprehensive result with temporal analysis (enhanced)
        return {
            "crisis_score": final_score,
            "confidence_score": enhanced_confidence,
            "crisis_level": crisis_level,
            "needs_response": crisis_level in ["medium", "high", "critical"],
            "requires_staff_review": crisis_level in ["high", "critical"],
            "method": "enhanced_three_step_analysis",
            "detected_categories": pattern_result.get("detected_categories", []),
            "ai_model_details": {
                "base_confidence": base_confidence,
                "models_used": ai_result.get("models_used", 0),
                "individual_results": ai_result.get("individual_results", {}),
                "zero_shot_labels_info": ai_result.get("zero_shot_labels_info", {})
            },
            "pattern_analysis": {
                "patterns_matched": pattern_result.get("patterns_found", []),
                "enhancement_boost": pattern_boost,
                "pattern_confidence": pattern_result.get("pattern_confidence", 0.0)
            },
            "learning_adjustments": {
                "applied": learning_result.get("learning_applied", False),
                "score_adjustment": learning_adjusted_score - base_score,
                "metadata": learning_result.get("metadata", {})
            },
            "temporal_analysis": temporal_details if 'temporal_details' in locals() else {
                'temporal_boost_applied': False,
                'final_score': final_score
            },
            "score_progression": {
                "base_ai_score": base_score,
                "after_pattern_boost": base_score + pattern_boost,
                "after_learning_adjustment": learning_adjusted_score,
                "final_with_temporal": final_score
            }
        }
    # ============================================================================

    # ============================================================================
    # HELPERS
    # ============================================================================
    def _extract_temporal_factors_from_pattern_result(self, pattern_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        FIXED: Extract temporal factors from pattern analysis results
        
        CHANGES MADE:
        1. Check multiple locations for temporal data (top-level, details, temporal_factors)
        2. Handle different temporal data structures
        3. Provide fallback extraction from pattern matches
        """
        try:
            temporal_factors = []
            
            # METHOD 1: Check for direct temporal_factors (new structure)
            if 'temporal_factors' in pattern_result:
                temporal_factors.extend(pattern_result['temporal_factors'])
                logger.debug(f"🕐 Found {len(temporal_factors)} temporal factors from direct structure")
            
            # METHOD 2: Check temporal_analysis at top level
            elif 'temporal_analysis' in pattern_result:
                temporal_analysis = pattern_result['temporal_analysis']
                for indicator in temporal_analysis.get('found_indicators', []):
                    temporal_factors.append({
                        'indicator_type': indicator.get('indicator_type', 'unknown'),
                        'boost_factor': indicator.get('boost_factor', 0.0),
                        'crisis_boost': indicator.get('crisis_boost', 0.0),
                        'urgency_score': indicator.get('urgency_score', 0.0),
                        'matched_phrase': indicator.get('matched_phrase', ''),
                        'temporal_category': indicator.get('temporal_category', 'general')
                    })
                logger.debug(f"🕐 Found {len(temporal_factors)} temporal factors from temporal_analysis")
            
            # METHOD 3: Check details.temporal_analysis (fallback)
            elif pattern_result.get('details', {}).get('temporal_analysis'):
                temporal_analysis = pattern_result['details']['temporal_analysis']
                for indicator in temporal_analysis.get('found_indicators', []):
                    temporal_factors.append({
                        'indicator_type': indicator.get('indicator_type', 'unknown'),
                        'boost_factor': indicator.get('boost_factor', 0.0),
                        'crisis_boost': indicator.get('crisis_boost', 0.0),
                        'urgency_score': indicator.get('urgency_score', 0.0),
                        'matched_phrase': indicator.get('matched_phrase', ''),
                        'temporal_category': indicator.get('temporal_category', 'general')
                    })
                logger.debug(f"🕐 Found {len(temporal_factors)} temporal factors from details")
            
            # METHOD 4: Check pattern matches for temporal patterns (last resort)
            else:
                patterns_found = pattern_result.get('patterns_found', [])
                for pattern in patterns_found:
                    if isinstance(pattern, dict):
                        pattern_name = pattern.get('pattern_name', '').lower()
                        pattern_group = pattern.get('pattern_group', '').lower()
                        
                        # Check if this pattern indicates temporal urgency
                        if any(keyword in pattern_name or keyword in pattern_group 
                               for keyword in ['temporal', 'urgent', 'immediate', 'tonight', 'now', 'time']):
                            temporal_factors.append({
                                'indicator_type': pattern.get('pattern_group', 'unknown'),
                                'boost_factor': pattern.get('weight', 0.0),
                                'crisis_boost': pattern.get('crisis_level', 'none'),
                                'urgency_score': pattern.get('confidence', 0.0),
                                'matched_phrase': pattern.get('matched_text', pattern.get('pattern_name', '')),
                                'temporal_category': 'pattern_inferred'
                            })
                
                if temporal_factors:
                    logger.debug(f"🕐 Inferred {len(temporal_factors)} temporal factors from pattern matches")
            
            # Log results
            if temporal_factors:
                logger.info(f"🕐 Extracted {len(temporal_factors)} temporal factors for boost calculation")
                for factor in temporal_factors:
                    logger.debug(f"🕐   - {factor['indicator_type']}: boost={factor['boost_factor']:.3f}, phrase='{factor['matched_phrase']}'")
            else:
                logger.debug("🕐 No temporal factors found in pattern result")
            
            return temporal_factors
            
        except Exception as e:
            logger.error(f"Failed to extract temporal factors from pattern result: {e}")
            return []

    def _apply_temporal_adjustments(self, base_score: float, temporal_factors: List[Dict[str, Any]]) -> Tuple[float, Dict[str, Any]]:
        """
        FIXED: Apply temporal boost factors to crisis scores with proper configuration lookup
        
        CHANGES MADE:
        1. Looks up boost factors from configuration when temporal factors have 0.0 boost
        2. Maps indicator types to configured boost values
        3. Handles fallback scenarios gracefully
        4. Applies proper temporal boost caps
        """
        try:
            temporal_details = {
                'temporal_boost_applied': False,
                'temporal_factors_found': [],
                'total_temporal_boost': 0.0,
                'original_score': base_score,
                'final_score': base_score
            }
            
            if not temporal_factors:
                logger.debug("🕐 No temporal factors found - no temporal adjustment applied")
                return base_score, temporal_details
            
            # Get temporal configuration for boost factor lookup
            temporal_config = self._get_temporal_boost_configuration()
            
            # Process temporal factors and calculate boost
            max_boost = 0.0
            applied_indicators = []
            
            for factor in temporal_factors:
                try:
                    # Extract current boost values
                    boost_factor = factor.get('boost_factor', 0.0)
                    crisis_boost = factor.get('crisis_boost', 0.0)
                    urgency_score = factor.get('urgency_score', 0.0)
                    indicator_type = factor.get('indicator_type', 'unknown')
                    matched_phrase = factor.get('matched_phrase', '')
                    
                    # CRITICAL FIX: If all boost values are 0, look up from configuration
                    if boost_factor == 0.0 and crisis_boost == 0.0 and urgency_score == 0.0:
                        config_boost = self._get_boost_factor_for_indicator_type(indicator_type, temporal_config)
                        if config_boost > 0:
                            boost_factor = config_boost
                            logger.debug(f"🕐 Applied config boost for {indicator_type}: {config_boost:.3f}")
                    
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
                        logger.debug(f"🕐 Temporal factor: {indicator_type} = {effective_boost:.3f} ('{matched_phrase}')")
                        
                except Exception as e:
                    logger.warning(f"Failed to process temporal factor {factor}: {e}")
                    continue
            
            # Apply temporal boost configuration limits
            try:
                max_temporal_boost = temporal_config.get('max_temporal_boost', 0.50)
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
                
                logger.info(f"🕐 TEMPORAL BOOST APPLIED: {base_score:.3f} → {adjusted_score:.3f} (+{capped_boost:.3f})")
                for indicator in applied_indicators:
                    logger.debug(f"🕐   - {indicator['type']}: +{indicator['boost']:.3f} '{indicator['phrase']}'")
                
                return adjusted_score, temporal_details
            else:
                logger.debug("🕐 No effective temporal boost - no adjustment applied")
            
            return base_score, temporal_details
            
        except Exception as e:
            logger.error(f"⚠️ Temporal adjustment failed: {e}")
            # Resilient fallback per Clean Architecture Charter Rule #5
            temporal_details['error'] = str(e)
            return base_score, temporal_details

    def _get_boost_factor_for_indicator_type(self, indicator_type: str, temporal_config: Dict[str, Any]) -> float:
        """
        NEW METHOD: Get boost factor for specific indicator type from configuration
        
        Args:
            indicator_type: Type of temporal indicator ('immediate', 'future_fear', etc.)
            temporal_config: Temporal configuration dictionary
            
        Returns:
            Boost factor value for the indicator type
        """
        try:
            # Map indicator types to configuration keys
            indicator_mapping = {
                'immediate': 'immediate_boost_factor',
                'future_fear': 'future_fear_boost_factor', 
                'ongoing': 'ongoing_boost_factor',
                'recent': 'recent_boost_factor',
                'escalation': 'escalation_boost_factor'
            }
            
            config_key = indicator_mapping.get(indicator_type.lower())
            if config_key and config_key in temporal_config:
                boost_value = temporal_config[config_key]
                logger.debug(f"🕐 Found config boost for {indicator_type}: {boost_value}")
                return float(boost_value)
            
            # Fallback: try direct key lookup
            direct_key = f"{indicator_type.lower()}_boost_factor"
            if direct_key in temporal_config:
                boost_value = temporal_config[direct_key]
                logger.debug(f"🕐 Found direct config boost for {indicator_type}: {boost_value}")
                return float(boost_value)
            
            logger.debug(f"🕐 No config boost found for indicator type: {indicator_type}")
            return 0.0
            
        except Exception as e:
            logger.warning(f"Failed to get boost factor for {indicator_type}: {e}")
            return 0.0

    def _get_temporal_boost_configuration(self) -> Dict[str, Any]:
        """
        NEW METHOD: Get temporal boost configuration from patterns_temporal or environment variables
        
        Returns:
            Dictionary containing temporal boost configuration
        """
        try:
            temporal_config = {}
            
            # Try to get from UnifiedConfigManager patterns_temporal
            if hasattr(self.crisis_analyzer, 'unified_config_manager'):
                try:
                    patterns_temporal = self.crisis_analyzer.unified_config_manager.get_patterns_crisis('patterns_temporal')
                    if patterns_temporal:
                        # Extract escalation rules which contain the boost factors
                        escalation_rules = patterns_temporal.get('escalation_rules', {})
                        temporal_config.update(escalation_rules)
                        logger.debug(f"🕐 Loaded temporal config from patterns_temporal: {len(temporal_config)} settings")
                except Exception as e:
                    logger.debug(f"Failed to load patterns_temporal: {e}")
            
            # Fallback: Get from environment variables (these override JSON config)
            env_mapping = {
                'immediate_boost_factor': 'NLP_TEMPORAL_IMMEDIATE_BOOST_FACTOR',
                'future_fear_boost_factor': 'NLP_TEMPORAL_FUTURE_FEAR_BOOST_FACTOR',
                'ongoing_boost_factor': 'NLP_TEMPORAL_ONGOING_BOOST_FACTOR',
                'recent_boost_factor': 'NLP_TEMPORAL_RECENT_BOOST_FACTOR',
                'escalation_boost_factor': 'NLP_TEMPORAL_ESCALATION_BOOST_FACTOR',
                'max_temporal_boost': 'NLP_TEMPORAL_MAX_BOOST'
            }
            
            import os
            for config_key, env_key in env_mapping.items():
                env_value = os.getenv(env_key)
                if env_value:
                    try:
                        temporal_config[config_key] = float(env_value)
                        logger.debug(f"🕐 Loaded from env: {config_key} = {env_value}")
                    except ValueError:
                        logger.warning(f"Invalid env value for {env_key}: {env_value}")
            
            # Provide safe defaults if nothing found
            if not temporal_config:
                temporal_config = {
                    'immediate_boost_factor': 0.35,
                    'future_fear_boost_factor': 0.40,
                    'ongoing_boost_factor': 0.30,
                    'recent_boost_factor': 0.20,
                    'escalation_boost_factor': 0.25,
                    'max_temporal_boost': 0.50
                }
                logger.debug("🕐 Using fallback temporal configuration")
            
            return temporal_config
            
        except Exception as e:
            logger.error(f"Failed to get temporal boost configuration: {e}")
            # Return safe defaults
            return {
                'immediate_boost_factor': 0.35,
                'future_fear_boost_factor': 0.40,
                'ongoing_boost_factor': 0.30,
                'max_temporal_boost': 0.50
            }

    def _convert_crisis_level_to_boost(self, crisis_level: str) -> float:
        """
        NEW METHOD: Convert crisis level string to numeric boost factor
        
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
        NEW METHOD: Get maximum temporal boost limit from configuration
        
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
    # ============================================================================

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