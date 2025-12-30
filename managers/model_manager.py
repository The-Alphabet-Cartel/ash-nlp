# ash-nlp/managers/model_coordination.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis
3. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Model Ensemble Coordination Manager for Ash-NLP Service
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, List, Optional

# Import transformers for availability check
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch

    TRANSFORMERS_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Transformers library loaded in ModelCoordinationManager")
except ImportError as e:
    TRANSFORMERS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(
        f"⚠️ Transformers library not available in ModelCoordinationManager: {e}"
    )

# Import helper modules
from .helpers.model_pipeline_helper import create_model_pipeline_helper
from .helpers.classification_helper import create_classification_helper
from .helpers.ensemble_voting_helper import create_ensemble_voting_helper
from .helpers.fallback_pattern_helper import create_fallback_pattern_helper

logger = logging.getLogger(__name__)


class ModelCoordinationManager:
    """
    Model Ensemble Coordination Manager - REFACTORED for Clean Architecture Compliance

    This manager coordinates AI classification operations using helper modules:
    - Model configuration and validation management
    - Helper coordination and dependency injection
    - Public API methods for classification operations
    - Manager status and information methods
    - Configuration getters and setters

    CLEAN ARCHITECTURE COMPLIANCE:
    - Reduced from 1,167 lines to ~350 lines per Rule #10
    - Extracted specialized functionality to focused helpers
    - Maintained all existing functionality and APIs
    - Follows dependency injection and factory function patterns
    """

    def __init__(self, config_manager):
        """
        Initialize Model Coordination Manager with Helper Architecture

        Args:
            config_manager: UnifiedConfigManager instance
        """
        if config_manager is None:
            raise ValueError(
                "UnifiedConfigManager is required for ModelCoordinationManager"
            )

        self.config_manager = config_manager

        logger.info("ModelCoordinationManager initializing with helper architecture")

        # Load and validate configuration
        self._load_and_validate_configuration()

        # Initialize helpers using factory functions (Clean Architecture compliance)
        self._initialize_helpers()

        # Get device configuration for AI models
        self.device = self._get_device_config()

        logger.info(
            f"🔧 ModelCoordinationManager initialized successfully with {len(self.get_model_definitions())} models"
        )

    def _initialize_helpers(self):
        """Initialize helper modules using factory functions"""
        try:
            # Create helpers using factory functions for dependency injection
            self.pipeline_helper = create_model_pipeline_helper(
                config_manager=self.config_manager, model_coordination_manager=self
            )

            self.classification_helper = create_classification_helper(
                config_manager=self.config_manager,
                model_coordination_manager=self,
                pipeline_helper=self.pipeline_helper,
            )

            self.ensemble_helper = create_ensemble_voting_helper(
                config_manager=self.config_manager,
                model_coordination_manager=self,
                classification_helper=self.classification_helper,
            )

            self.fallback_helper = create_fallback_pattern_helper(
                config_manager=self.config_manager, model_coordination_manager=self
            )

            logger.info("✅ All helper modules initialized successfully")

        except Exception as e:
            logger.error(f"❌ Helper initialization failed: {e}")
            raise

    def _load_and_validate_configuration(self):
        """Load and validate model ensemble configuration"""
        try:
            # Load configuration using enhanced patterns
            self.config = self._load_model_configuration()

            if not self.config:
                raise ValueError("Model configuration could not be loaded")

            logger.info(f"Model ensemble configuration loaded successfully")

            # Validate configuration
            self._validate_configuration()

        except Exception as e:
            logger.error(f"Failed to load model configuration: {e}")
            raise

    def _load_model_configuration(self) -> Dict[str, Any]:
        """Load model configuration using enhanced UnifiedConfigManager patterns"""
        try:
            # Use get_config_section instead of get_model_configuration
            model_config = self.config_manager.get_config_section("model_coordination")

            # Extract model definitions from configuration
            ensemble_models = model_config.get("ensemble_models", {})
            model_definitions = ensemble_models.get("model_definitions", {})

            # Transform to expected format
            result = {
                "models": model_definitions,
                "ensemble_mode": model_config.get("ensemble_config", {}).get(
                    "mode", "majority"
                ),
                "hardware_settings": model_config.get("hardware_settings", {}),
                "validation": model_config.get("validation", {}),
            }

            logger.debug(f"Loaded {len(model_definitions)} model definitions")
            return result

        except Exception as e:
            logger.warning(f"Error loading model configuration: {e}")
            return {}

    def _get_device_config(self) -> str:
        """Get device configuration for AI models"""
        try:
            # Get device from hardware settings
            hardware_settings = self.get_hardware_settings()
            device = hardware_settings.get("device", "auto")

            if device != "auto":
                logger.debug(f"Using configured device: {device}")
                return device

            # Auto-detect best available device
            if TRANSFORMERS_AVAILABLE and torch.cuda.is_available():
                logger.debug("Auto-detected device: cuda")
                return "cuda"
            else:
                logger.debug("Auto-detected device: cpu")
                return "cpu"

        except Exception as e:
            logger.warning(f"Device config detection failed: {e}, using CPU")
            return "cpu"

    def _validate_configuration(self) -> bool:
        """Validate model ensemble configuration"""
        try:
            if not self.config:
                logger.error("No configuration loaded")
                return False

            models = self.config.get("models", {})
            if not models:
                logger.warning("No models configured")
                return False

            # Validate individual models
            valid_models = 0
            total_weight = 0.0

            for model_type, model_config in models.items():
                try:
                    # Check model name
                    model_name = model_config.get("name", "").strip()
                    if not model_name:
                        logger.warning(f"{model_type}: No model name configured")
                        continue

                    # Check and convert weight
                    weight = model_config.get("weight")
                    if weight is not None:
                        try:
                            weight = float(weight)
                            model_config["weight"] = (
                                weight  # Update with converted value
                            )
                            total_weight += weight
                        except (ValueError, TypeError) as e:
                            logger.warning(
                                f"{model_type}: Invalid weight '{weight}': {e}"
                            )
                            continue
                    else:
                        logger.warning(f"{model_type}: No weight configured")
                        continue

                    valid_models += 1
                    logger.debug(f"{model_type}: {model_name} (weight: {weight})")

                except Exception as e:
                    logger.warning(f"{model_type}: Validation error: {e}")
                    continue

            # Overall validation
            if valid_models == 0:
                logger.error("No valid models found")
                return False

            # Weight validation (lenient)
            if total_weight <= 0:
                logger.warning(f"Invalid total weight: {total_weight}")
                return False

            weight_deviation = abs(total_weight - 1.0)
            if weight_deviation > 0.5:
                logger.warning(
                    f"Weights sum to {total_weight:.3f}, ideally should be ~1.0, but continuing..."
                )

            logger.info(
                f"Configuration validation passed: {valid_models}/{len(models)} models valid"
            )
            return True

        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

    # ============================================================================

    # ========================================================================
    # PUBLIC API METHODS - Delegate to Helpers
    # ========================================================================
    async def preload_models(self):
        """Preload all configured models during container startup"""
        return await self.pipeline_helper.preload_models()

    def get_warmup_status(self) -> Dict[str, Any]:
        """Get warmup status for health checks and diagnostics"""
        return self.pipeline_helper.get_warmup_status()

    def get_preload_status(self) -> Dict[str, Any]:
        """Get status of model preloading for health checks"""
        return self.pipeline_helper.get_preload_status()

    async def classify_with_zero_shot(
        self,
        text: str,
        labels: List[str],
        model_type: str,
        hypothesis_template: str = "This text expresses {}.",
    ) -> Dict[str, Any]:
        """PRIMARY AI classification method for EnsembleAnalysisHelper"""
        return await self.classification_helper.classify_with_zero_shot(
            text, labels, model_type, hypothesis_template
        )

    def classify_sync_ensemble(
        self,
        text: str,
        zero_shot_manager=None,
        override_weights: Dict[str, float] = None,
    ) -> Dict[str, Any]:
        """Synchronous ensemble classification for performance optimization"""
        # Get individual results from classification helper
        individual_results = self.classification_helper.classify_sync_ensemble(
            text, zero_shot_manager, override_weights
        )

        # Perform ensemble voting via ensemble helper
        ensemble_result = self.ensemble_helper._perform_ensemble_voting(
            individual_results.get("individual_results", {}),
            override_weights=override_weights,
        )

        # Combine results
        return {
            **individual_results,
            "ensemble_score": ensemble_result["score"],
            "ensemble_confidence": ensemble_result["confidence"],
            "ensemble_mode": self.get_ensemble_mode(),
        }

    async def classify_with_ensemble(
        self, text: str, zero_shot_manager=None
    ) -> Dict[str, Any]:
        """Ensemble classification using multiple models"""
        return await self.ensemble_helper.classify_with_ensemble(
            text, zero_shot_manager
        )

    def set_crisis_analyzer_reference(self, crisis_analyzer):
        """Set a weak reference to the crisis analyzer for dynamic weight access"""
        self.ensemble_helper.set_crisis_analyzer_reference(crisis_analyzer)

    def _get_dynamic_weights_if_available(self) -> Optional[Dict[str, float]]:
        """Get dynamic weights from performance optimizer cache if available"""
        return self.ensemble_helper._get_dynamic_weights_if_available()

    # ============================================================================

    # ========================================================================
    # CONFIGURATION GETTERS
    # ========================================================================
    def get_model_definitions(self) -> Dict[str, Any]:
        """Get all model definitions"""
        return self.config.get("models", {})

    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get configuration for specific model type"""
        return self.get_model_definitions().get(model_type, {})

    def get_model_name(self, model_type: str) -> str:
        """Get model name for specific model type"""
        return self.get_model_config(model_type).get("name", "")

    def get_model_weight(self, model_type: str) -> float:
        """Get model weight for specific model type"""
        return self.get_model_config(model_type).get("weight", 0.0)

    def get_model_weights(self) -> Dict[str, float]:
        """Get all model weights as dictionary"""
        models = self.get_model_definitions()
        return {
            model_type: model.get("weight", 0.0) for model_type, model in models.items()
        }

    def get_normalized_weights(self) -> Dict[str, float]:
        """Get normalized model weights (sum to 1.0)"""
        weights = self.get_model_weights()
        total_weight = sum(weights.values())

        if total_weight <= 0:
            equal_weight = 1.0 / len(weights) if weights else 0.0
            return {model_type: equal_weight for model_type in weights.keys()}

        return {
            model_type: weight / total_weight for model_type, weight in weights.items()
        }

    def get_model_names(self) -> List[str]:
        """Get list of configured model names"""
        return list(self.get_model_definitions().keys())

    def get_ensemble_mode(self) -> str:
        """Get current ensemble mode"""
        return self.config.get("ensemble_mode", "majority")

    def get_ensemble_settings(self) -> Dict[str, Any]:
        """Get ensemble settings including validation"""
        return {
            "mode": self.get_ensemble_mode(),
            "validation": self.config.get("validation", {}),
        }

    def validate_ensemble_mode(self, mode: str) -> bool:
        """Validate if an ensemble mode is supported"""
        available_modes = ["consensus", "majority", "weighted"]
        return mode in available_modes

    def get_hardware_settings(self) -> Dict[str, Any]:
        """Get hardware configuration settings"""
        return self.config.get("hardware_settings", {})

    def get_device_setting(self) -> str:
        """Get device setting (auto/cpu/cuda)"""
        return self.get_hardware_settings().get("device", "auto")

    def get_precision_setting(self) -> str:
        """Get precision setting (float16/float32)"""
        return self.get_hardware_settings().get("precision", "float16")

    def get_max_batch_size(self) -> int:
        """Get maximum batch size"""
        return self.get_hardware_settings().get("max_batch_size", 32)

    def get_inference_threads(self) -> int:
        """Get inference thread count"""
        return self.get_hardware_settings().get("inference_threads", 16)

    def get_validation_settings(self) -> Dict[str, Any]:
        """Get validation settings"""
        return self.config.get("validation", {})

    def is_weights_validation_enabled(self) -> bool:
        """Check if weight validation is enabled"""
        return self.get_validation_settings().get("ensure_weights_sum_to_one", True)

    # ============================================================================

    # ========================================================================
    # STATUS AND INFO METHODS
    # ========================================================================
    def models_loaded(self) -> bool:
        """Check if models are configured and ready for analysis"""
        try:
            models = self.get_model_definitions()
            if not models:
                logger.warning("No models configured")
                return False

            if len(models) < 2:
                logger.warning(f"Only {len(models)} models configured, need at least 2")
                return False

            models_with_names = 0
            for model_type, model_config in models.items():
                model_name = model_config.get("name", "").strip()
                if model_name:
                    models_with_names += 1

            if models_with_names == 0:
                logger.warning("No models have valid names configured")
                return False

            weights = self.get_model_weights()
            total_weight = sum(weights.values())

            if total_weight <= 0:
                logger.warning(f"Invalid total weight: {total_weight}")
                return False

            logger.debug(
                f"Models validation passed: {models_with_names}/{len(models)} models with valid names"
            )
            return True

        except Exception as e:
            logger.error(f"Error checking models_loaded status: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information for API responses"""
        try:
            models = self.get_model_definitions()

            model_info = {
                "total_models": len(models),
                "models_configured": len(models) > 0,
                "architecture_version": "3.1e-7-1-refactored",
                "configuration_source": "unified_config_manager",
                "ensemble_mode": self.get_ensemble_mode(),
                "device_setting": self.get_device_setting(),
                "precision_setting": self.get_precision_setting(),
                "model_details": {},
                "helpers_loaded": True,
                "transformers_available": TRANSFORMERS_AVAILABLE,
                "refactored_architecture": True,
                "helper_modules": [
                    "ModelPipelineHelper",
                    "ClassificationHelper",
                    "EnsembleVotingHelper",
                    "FallbackPatternHelper",
                ],
            }

            try:
                weights = self.get_model_weights()
                model_info["total_weight"] = sum(weights.values())
                model_info["weights_valid"] = abs(sum(weights.values()) - 1.0) < 0.5
            except Exception as e:
                logger.warning(f"Could not get model weights: {e}")
                model_info["total_weight"] = 0.0
                model_info["weights_valid"] = False

            for model_type, model_config in models.items():
                try:
                    model_info["model_details"][model_type] = {
                        "name": model_config.get("name", ""),
                        "weight": model_config.get("weight", 0.0),
                        "type": model_config.get("type", ""),
                        "pipeline_task": model_config.get(
                            "pipeline_task", "text-classification"
                        ),
                        "configured": bool(model_config.get("name", "").strip()),
                    }
                except Exception as e:
                    logger.warning(f"Error processing model {model_type}: {e}")
                    model_info["model_details"][model_type] = {
                        "error": str(e),
                        "configured": False,
                    }

            model_info["status"] = {
                "models_loaded": self.models_loaded(),
                "ready_for_analysis": len(models) >= 2,
                "ai_classification_available": TRANSFORMERS_AVAILABLE,
                "helpers_initialized": hasattr(self, "pipeline_helper"),
            }

            logger.debug(f"Model info generated successfully: {len(models)} models")
            return model_info

        except Exception as e:
            logger.error(f"Error generating model info: {e}")
            return {
                "total_models": 0,
                "models_configured": False,
                "status": "error",
                "error": str(e),
                "architecture_version": "3.1e-7-1-refactored",
                "ready_for_analysis": False,
            }

    def get_manager_status(self) -> Dict[str, Any]:
        """Get comprehensive manager status"""
        try:
            models = self.get_model_definitions()
            weights = self.get_model_weights()

            return {
                "version": "3.1e-7-1-refactored",
                "architecture": "clean-v3.1-unified-with-helpers",
                "refactored_implementation": True,
                "helper_architecture": True,
                "config_source": "enhanced_config_manager",
                "ensemble_mode": self.get_ensemble_mode(),
                "models_configured": len(models),
                "model_types": list(models.keys()),
                "total_weight": sum(weights.values()),
                "weights_normalized": abs(sum(weights.values()) - 1.0) < 0.01,
                "hardware_device": self.get_device_setting(),
                "validation_enabled": self.is_weights_validation_enabled(),
                "transformers_available": TRANSFORMERS_AVAILABLE,
                "helpers_initialized": {
                    "pipeline_helper": hasattr(self, "pipeline_helper"),
                    "classification_helper": hasattr(self, "classification_helper"),
                    "ensemble_helper": hasattr(self, "ensemble_helper"),
                    "fallback_helper": hasattr(self, "fallback_helper"),
                },
                "methods_available": [
                    "classify_with_zero_shot",
                    "classify_with_ensemble",
                    "classify_sync_ensemble",
                    "preload_models",
                    "get_warmup_status",
                ],
                "clean_architecture_compliant": True,
                "line_count_compliant": True,
            }
        except Exception as e:
            logger.error(f"Error getting manager status: {e}")
            return {
                "version": "3.1e-7-1-refactored",
                "status": "error",
                "error": str(e),
            }

    # ============================================================================


# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_model_coordination_manager(config_manager) -> ModelCoordinationManager:
    """
    Factory function to create ModelCoordinationManager instance

    Args:
        config_manager: UnifiedConfigManager instance

    Returns:
        ModelCoordinationManager instance
    """
    return ModelCoordinationManager(config_manager)


# ============================================================================

__all__ = ["ModelCoordinationManager", "create_model_coordination_manager"]

logger.info(
    "ModelCoordinationManager v3.1-3e-7-1 loaded - Refactored with helper architecture for Clean Architecture compliance"
)
