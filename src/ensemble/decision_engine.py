"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Ensemble Decision Engine for Ash-NLP Service
---
FILE VERSION: v5.0-3-4.3-4
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 Step 4.3 - Ensemble Decision Engine
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Orchestrate multi-model ensemble inference
- Coordinate model loading, scoring, and fallback
- Provide unified analyze() method for API
- Calculate final crisis assessment
- Handle async parallel inference (optional)

This is the PRIMARY INTERFACE for crisis detection.
API endpoints call this engine to analyze messages.
"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from src.models import ModelResult

from .model_loader import ModelLoader, create_model_loader
from .scoring import (
    WeightedScorer,
    create_weighted_scorer,
    EnsembleScore,
    CrisisSeverity,
)
from .fallback import (
    FallbackStrategy,
    create_fallback_strategy,
    CriticalModelFailure,
)

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager

# Module version
__version__ = "v5.0-3-4.3-4"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Crisis Assessment Result
# =============================================================================


@dataclass
class CrisisAssessment:
    """
    Complete crisis assessment result.

    This is the primary output from the Decision Engine,
    containing all information needed for API response.

    Attributes:
        crisis_detected: Whether a crisis was detected
        severity: Crisis severity level
        confidence: Confidence in assessment (0.0 - 1.0)
        crisis_score: Final weighted crisis score (0.0 - 1.0)
        requires_intervention: Whether immediate action is recommended
        recommended_action: Suggested response action
        signals: Individual model signals
        processing_time_ms: Total processing time
        models_used: Which models contributed
        is_degraded: Whether ensemble is operating in degraded mode
        message: Original message analyzed
    """

    crisis_detected: bool
    severity: CrisisSeverity
    confidence: float
    crisis_score: float
    requires_intervention: bool
    recommended_action: str
    signals: Dict[str, Any]
    processing_time_ms: float
    models_used: List[str]
    is_degraded: bool = False
    degradation_reason: str = ""
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "crisis_detected": self.crisis_detected,
            "severity": self.severity.value,
            "confidence": round(self.confidence, 4),
            "crisis_score": round(self.crisis_score, 4),
            "requires_intervention": self.requires_intervention,
            "recommended_action": self.recommended_action,
            "signals": self.signals,
            "processing_time_ms": round(self.processing_time_ms, 2),
            "models_used": self.models_used,
            "is_degraded": self.is_degraded,
        }

    @staticmethod
    def create_error(
        error: str,
        message: str = "",
        processing_time_ms: float = 0.0,
    ) -> "CrisisAssessment":
        """Create an error assessment."""
        return CrisisAssessment(
            crisis_detected=False,
            severity=CrisisSeverity.SAFE,
            confidence=0.0,
            crisis_score=0.0,
            requires_intervention=False,
            recommended_action="error",
            signals={"error": error},
            processing_time_ms=processing_time_ms,
            models_used=[],
            is_degraded=True,
            degradation_reason=error,
            message=message,
        )


# =============================================================================
# Recommended Actions
# =============================================================================


class RecommendedAction:
    """Recommended actions based on severity."""

    IMMEDIATE_OUTREACH = "immediate_outreach"
    PRIORITY_RESPONSE = "priority_response"
    STANDARD_MONITORING = "standard_monitoring"
    PASSIVE_MONITORING = "passive_monitoring"
    NONE = "none"
    ERROR = "error"

    @classmethod
    def from_severity(cls, severity: CrisisSeverity) -> str:
        """Map severity to recommended action."""
        mapping = {
            CrisisSeverity.CRITICAL: cls.IMMEDIATE_OUTREACH,
            CrisisSeverity.HIGH: cls.PRIORITY_RESPONSE,
            CrisisSeverity.MEDIUM: cls.STANDARD_MONITORING,
            CrisisSeverity.LOW: cls.PASSIVE_MONITORING,
            CrisisSeverity.SAFE: cls.NONE,
        }
        return mapping.get(severity, cls.NONE)


# =============================================================================
# Ensemble Decision Engine
# =============================================================================


class EnsembleDecisionEngine:
    """
    Ensemble Decision Engine - Primary Crisis Detection Interface.

    Orchestrates the multi-model ensemble:
    1. Loads and manages models via ModelLoader
    2. Runs inference on all models
    3. Calculates weighted scores via WeightedScorer
    4. Handles failures via FallbackStrategy
    5. Returns comprehensive CrisisAssessment

    This is the main interface for the API to call.

    Clean Architecture v5.1 Compliance:
    - Factory function: create_decision_engine()
    - Configuration via ConfigManager
    - Dependency injection pattern
    - Resilient error handling (Rule #5)
    """

    def __init__(
        self,
        config_manager: Optional["ConfigManager"] = None,
        model_loader: Optional[ModelLoader] = None,
        scorer: Optional[WeightedScorer] = None,
        fallback: Optional[FallbackStrategy] = None,
        async_inference: bool = True,
    ):
        """
        Initialize Ensemble Decision Engine.

        Args:
            config_manager: Configuration manager instance
            model_loader: Pre-configured model loader (optional)
            scorer: Pre-configured scorer (optional)
            fallback: Pre-configured fallback strategy (optional)
            async_inference: Enable parallel model inference
        """
        self.config_manager = config_manager
        self.async_inference = async_inference

        # Initialize components
        self.model_loader = model_loader or create_model_loader(
            config_manager=config_manager,
            lazy_load=True,
            warmup_on_load=True,
        )

        self.scorer = scorer or create_weighted_scorer(config_manager=config_manager)

        self.fallback = fallback or create_fallback_strategy(
            config_manager=config_manager
        )

        # Performance tracking
        self._total_requests: int = 0
        self._total_latency_ms: float = 0.0
        self._crisis_detections: int = 0

        # Thread pool for parallel inference
        self._executor: Optional[ThreadPoolExecutor] = None
        if async_inference:
            self._executor = ThreadPoolExecutor(max_workers=4)

        logger.info(f"🧠 EnsembleDecisionEngine initialized (async={async_inference})")

    # =========================================================================
    # Main Analysis Methods
    # =========================================================================

    def analyze(self, message: str) -> CrisisAssessment:
        """
        Analyze a message for crisis signals.

        This is the PRIMARY method for crisis detection.

        Args:
            message: Text message to analyze

        Returns:
            CrisisAssessment with complete analysis
        """
        start_time = time.perf_counter()

        try:
            # Run inference on all models
            if self.async_inference and self._executor:
                results = self._run_parallel_inference(message)
            else:
                results = self._run_sequential_inference(message)

            # Calculate ensemble score
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # Calculate processing time
            processing_time_ms = (time.perf_counter() - start_time) * 1000

            # Build assessment
            assessment = self._build_assessment(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
            )

            # Update stats
            self._total_requests += 1
            self._total_latency_ms += processing_time_ms
            if assessment.crisis_detected:
                self._crisis_detections += 1

            return assessment

        except CriticalModelFailure as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.critical(f"🚨 Critical model failure during analysis: {e}")
            return CrisisAssessment.create_error(
                error=str(e),
                message=message,
                processing_time_ms=processing_time_ms,
            )

        except Exception as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"❌ Analysis failed: {e}")
            return CrisisAssessment.create_error(
                error=str(e),
                message=message,
                processing_time_ms=processing_time_ms,
            )

    async def analyze_async(self, message: str) -> CrisisAssessment:
        """
        Async version of analyze for use in async frameworks.

        Args:
            message: Text message to analyze

        Returns:
            CrisisAssessment with complete analysis
        """
        # Run in thread pool to not block event loop
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            self.analyze,
            message,
        )

    def _run_sequential_inference(
        self, message: str
    ) -> Dict[str, Optional[ModelResult]]:
        """
        Run inference on all models sequentially.

        Args:
            message: Text to analyze

        Returns:
            Dictionary of model_name -> ModelResult
        """
        results: Dict[str, Optional[ModelResult]] = {}

        # BART (Primary - Required)
        if self.fallback.can_call_model("bart"):
            try:
                bart = self.model_loader.get_bart()
                if bart:
                    results["bart"] = bart.analyze(message)
                    self.fallback.handle_model_success("bart")
            except Exception as e:
                self.fallback.handle_model_failure("bart", str(e))

        # Sentiment (Secondary)
        if self.fallback.can_call_model("sentiment"):
            try:
                sentiment = self.model_loader.get_sentiment()
                if sentiment:
                    results["sentiment"] = sentiment.analyze(message)
                    self.fallback.handle_model_success("sentiment")
            except Exception as e:
                self.fallback.handle_model_failure("sentiment", str(e))

        # Irony (Tertiary)
        if self.fallback.can_call_model("irony"):
            try:
                irony = self.model_loader.get_irony()
                if irony:
                    results["irony"] = irony.analyze(message)
                    self.fallback.handle_model_success("irony")
            except Exception as e:
                self.fallback.handle_model_failure("irony", str(e))

        # Emotions (Supplementary)
        if self.fallback.can_call_model("emotions"):
            try:
                emotions = self.model_loader.get_emotions()
                if emotions:
                    results["emotions"] = emotions.analyze(message)
                    self.fallback.handle_model_success("emotions")
            except Exception as e:
                self.fallback.handle_model_failure("emotions", str(e))

        return results

    def _run_parallel_inference(self, message: str) -> Dict[str, Optional[ModelResult]]:
        """
        Run inference on all models in parallel.

        Args:
            message: Text to analyze

        Returns:
            Dictionary of model_name -> ModelResult
        """
        results: Dict[str, Optional[ModelResult]] = {}
        futures = {}

        def run_model(model_name: str):
            """Run a single model inference."""
            if not self.fallback.can_call_model(model_name):
                return None

            try:
                model = self.model_loader.get_model(model_name)
                if model:
                    result = model.analyze(message)
                    self.fallback.handle_model_success(model_name)
                    return result
                return None
            except Exception as e:
                self.fallback.handle_model_failure(model_name, str(e))
                return None

        # Submit all model tasks
        model_names = ["bart", "sentiment", "irony", "emotions"]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(run_model, name): name for name in model_names}

            for future in futures:
                model_name = futures[future]
                try:
                    result = future.result(timeout=30)
                    if result:
                        results[model_name] = result
                except Exception as e:
                    logger.error(f"Parallel inference failed for {model_name}: {e}")

        return results

    def _build_assessment(
        self,
        ensemble_score: EnsembleScore,
        results: Dict[str, Optional[ModelResult]],
        message: str,
        processing_time_ms: float,
    ) -> CrisisAssessment:
        """
        Build final CrisisAssessment from ensemble score.

        Args:
            ensemble_score: Calculated ensemble score
            results: Model results
            message: Original message
            processing_time_ms: Processing time

        Returns:
            Complete CrisisAssessment
        """
        # Determine recommended action
        recommended_action = RecommendedAction.from_severity(ensemble_score.severity)

        # Build signals dict for response
        signals = {}
        for name, signal in ensemble_score.signals.items():
            signals[name] = {
                "label": signal.label,
                "score": round(signal.raw_score, 4),
                "crisis_signal": round(signal.crisis_signal, 4),
            }

        # List models that contributed
        models_used = list(results.keys())

        return CrisisAssessment(
            crisis_detected=ensemble_score.crisis_detected,
            severity=ensemble_score.severity,
            confidence=ensemble_score.confidence,
            crisis_score=ensemble_score.crisis_score,
            requires_intervention=ensemble_score.requires_intervention,
            recommended_action=recommended_action,
            signals=signals,
            processing_time_ms=processing_time_ms,
            models_used=models_used,
            is_degraded=self.fallback.is_degraded(),
            degradation_reason=self.fallback.get_degradation_reason(),
            message=message,
        )

    # =========================================================================
    # Initialization and Management
    # =========================================================================

    def initialize(self) -> bool:
        """
        Initialize the engine (load all models).

        Returns:
            True if initialization succeeded
        """
        logger.info("🚀 Initializing Decision Engine...")

        try:
            results = self.model_loader.load_all_models()

            success_count = sum(1 for r in results.values() if r)
            total_count = len(results)

            if results.get("bart", False):
                logger.info(
                    f"✅ Engine initialized ({success_count}/{total_count} models)"
                )
                return True
            else:
                logger.error("❌ BART model failed to load - engine not ready")
                return False

        except Exception as e:
            logger.error(f"❌ Engine initialization failed: {e}")
            return False

    def shutdown(self) -> None:
        """Shutdown the engine and release resources."""
        logger.info("🛑 Shutting down Decision Engine...")

        # Unload models
        self.model_loader.unload_all_models()

        # Shutdown thread pool
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None

        logger.info("✅ Decision Engine shutdown complete")

    def warmup(self, sample_text: str = "Hello, how are you today?") -> bool:
        """
        Warm up the engine with a sample analysis.

        Args:
            sample_text: Text to use for warmup

        Returns:
            True if warmup succeeded
        """
        logger.info("🔥 Warming up Decision Engine...")

        try:
            result = self.analyze(sample_text)

            if result.crisis_score >= 0:  # Valid result
                logger.info(
                    f"✅ Engine warmed up (latency: {result.processing_time_ms:.1f}ms)"
                )
                return True
            else:
                logger.warning("⚠️ Warmup returned invalid result")
                return False

        except Exception as e:
            logger.error(f"❌ Warmup failed: {e}")
            return False

    # =========================================================================
    # Status and Metrics
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive engine status.

        Returns:
            Status dictionary
        """
        avg_latency = (
            self._total_latency_ms / self._total_requests
            if self._total_requests > 0
            else 0.0
        )

        return {
            "is_ready": self.is_ready(),
            "is_degraded": self.fallback.is_degraded(),
            "degradation_reason": self.fallback.get_degradation_reason(),
            "async_inference": self.async_inference,
            "stats": {
                "total_requests": self._total_requests,
                "crisis_detections": self._crisis_detections,
                "average_latency_ms": round(avg_latency, 2),
            },
            "models": self.model_loader.get_status(),
            "weights": self.scorer.get_weights(),
            "thresholds": self.scorer.get_thresholds(),
            "fallback": self.fallback.get_status(),
        }

    def get_model_info(self) -> List[Dict[str, Any]]:
        """
        Get information about loaded models.

        Returns:
            List of model info dictionaries
        """
        return [info.to_dict() for info in self.model_loader.get_model_info()]

    def is_ready(self) -> bool:
        """
        Check if engine is ready for analysis.

        Returns:
            True if at least BART is loaded and operational
        """
        return self.model_loader.is_ready() and self.fallback.is_operational()

    def get_health(self) -> Dict[str, Any]:
        """
        Get health check information.

        Returns:
            Health status for API endpoint
        """
        return {
            "status": "healthy" if self.is_ready() else "unhealthy",
            "ready": self.is_ready(),
            "degraded": self.fallback.is_degraded(),
            "models_loaded": self.model_loader._models_loaded,
            "total_models": len(self.model_loader._models),
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_decision_engine(
    config_manager: Optional["ConfigManager"] = None,
    auto_initialize: bool = False,
    async_inference: bool = True,
) -> EnsembleDecisionEngine:
    """
    Factory function for EnsembleDecisionEngine.

    Creates a fully configured decision engine.

    Args:
        config_manager: Configuration manager instance
        auto_initialize: If True, load models immediately
        async_inference: Enable parallel model inference

    Returns:
        Configured EnsembleDecisionEngine instance

    Example:
        >>> engine = create_decision_engine(config_manager=config)
        >>> engine.initialize()
        >>> assessment = engine.analyze("I'm feeling really down today")
    """
    # Get async setting from config
    if config_manager is not None:
        perf_config = config_manager.get_performance_config()
        if perf_config:
            async_inference = perf_config.get("async_inference", async_inference)

    engine = EnsembleDecisionEngine(
        config_manager=config_manager,
        async_inference=async_inference,
    )

    if auto_initialize:
        engine.initialize()

    return engine


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "EnsembleDecisionEngine",
    "create_decision_engine",
    "CrisisAssessment",
    "RecommendedAction",
]
