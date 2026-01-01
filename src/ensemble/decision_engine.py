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
FILE VERSION: v5.0-4-2.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 4 - Ensemble Coordinator Enhancement
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Orchestrate multi-model ensemble inference
- Coordinate model loading, scoring, and fallback
- Provide unified analyze() method for API
- Calculate final crisis assessment
- Handle async parallel inference with asyncio.gather()
- Cache responses for repeated messages

PHASE 4 ENHANCEMENTS:
- Consensus algorithm selection (weighted, majority, unanimous, conflict-aware)
- Conflict detection and resolution
- Comprehensive result aggregation
- Human-readable explainability

This is the PRIMARY INTERFACE for crisis detection.
API endpoints call this engine to analyze messages.

PERFORMANCE OPTIMIZATIONS (Phase 3.7):
- 3.7.1: Model warmup on startup with alerting
- 3.7.2: Async parallel inference with asyncio.gather()
- 3.7.4: Response caching for repeated messages
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

# Phase 4 imports
from .consensus import (
    ConsensusSelector,
    ConsensusAlgorithm,
    ConsensusResult,
    create_consensus_selector,
)
from .conflict_detector import (
    ConflictDetector,
    ConflictReport,
    ModelSignals,
    create_conflict_detector,
)
from .conflict_resolver import (
    ConflictResolver,
    ResolutionStrategy,
    ResolutionResult,
    create_conflict_resolver,
)
from .aggregator import (
    ResultAggregator,
    AggregatedResult,
    CrisisLevel,
    create_result_aggregator,
)
from .explainability import (
    ExplainabilityGenerator,
    VerbosityLevel,
    Explanation,
    create_explainability_generator,
)

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager
    from src.utils.cache import ResponseCache
    from src.utils.alerting import DiscordAlerter

# Module version
__version__ = "v5.0-4-2.0-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Crisis Assessment Result (Phase 3 - Backward Compatible)
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
        cached: Whether result was from cache
        
        # Phase 4 Enhanced Fields
        explanation: Human-readable explanation (Phase 4)
        conflict_report: Conflict detection report (Phase 4)
        consensus_result: Consensus algorithm result (Phase 4)
        aggregated_result: Full aggregated result (Phase 4)
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
    cached: bool = False
    
    # Phase 4 Enhanced Fields
    explanation: Optional[Dict[str, Any]] = None
    conflict_report: Optional[Dict[str, Any]] = None
    consensus_result: Optional[Dict[str, Any]] = None
    aggregated_result: Optional[AggregatedResult] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        result = {
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
            "cached": self.cached,
        }
        
        # Include Phase 4 fields if present
        if self.explanation:
            result["explanation"] = self.explanation
        if self.conflict_report:
            result["conflict_analysis"] = self.conflict_report
        if self.consensus_result:
            result["consensus"] = self.consensus_result
            
        return result

    def to_enhanced_dict(self) -> Dict[str, Any]:
        """Convert to full enhanced dictionary with all Phase 4 data."""
        if self.aggregated_result:
            return self.aggregated_result.to_dict()
        return self.to_dict()

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
    2. Runs inference on all models (parallel with asyncio.gather)
    3. Calculates weighted scores via WeightedScorer
    4. Handles failures via FallbackStrategy
    5. Caches responses for repeated messages
    6. Returns comprehensive CrisisAssessment

    Phase 4 Enhancements:
    - Consensus algorithm selection
    - Conflict detection and resolution
    - Comprehensive result aggregation
    - Human-readable explainability

    This is the main interface for the API to call.

    Performance Optimizations (Phase 3.7):
    - Model warmup on startup (3.7.1)
    - Async parallel inference with asyncio.gather (3.7.2)
    - Response caching (3.7.4)

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
        cache: Optional["ResponseCache"] = None,
        alerter: Optional["DiscordAlerter"] = None,
        async_inference: bool = True,
        cache_enabled: bool = True,
        cache_ttl: float = 300.0,
        cache_max_size: int = 1000,
        # Phase 4 components
        consensus_selector: Optional[ConsensusSelector] = None,
        conflict_detector: Optional[ConflictDetector] = None,
        conflict_resolver: Optional[ConflictResolver] = None,
        result_aggregator: Optional[ResultAggregator] = None,
        explainability_generator: Optional[ExplainabilityGenerator] = None,
        phase4_enabled: bool = True,
    ):
        """
        Initialize Ensemble Decision Engine.

        Args:
            config_manager: Configuration manager instance
            model_loader: Pre-configured model loader (optional)
            scorer: Pre-configured scorer (optional)
            fallback: Pre-configured fallback strategy (optional)
            cache: Pre-configured response cache (optional)
            alerter: Discord alerter for notifications (optional)
            async_inference: Enable parallel model inference
            cache_enabled: Enable response caching
            cache_ttl: Cache time-to-live in seconds
            cache_max_size: Maximum cache entries
            
            # Phase 4 components
            consensus_selector: Consensus algorithm selector
            conflict_detector: Conflict detection component
            conflict_resolver: Conflict resolution component
            result_aggregator: Result aggregation component
            explainability_generator: Explainability component
            phase4_enabled: Enable Phase 4 features (default: True)
        """
        self.config_manager = config_manager
        self.async_inference = async_inference
        self.cache_enabled = cache_enabled
        self.phase4_enabled = phase4_enabled

        # Initialize Phase 3 components
        self.model_loader = model_loader or create_model_loader(
            config_manager=config_manager,
            lazy_load=True,
            warmup_on_load=True,
        )

        self.scorer = scorer or create_weighted_scorer(config_manager=config_manager)

        self.fallback = fallback or create_fallback_strategy(
            config_manager=config_manager
        )

        # Initialize cache (Phase 3.7.4)
        if cache is not None:
            self._cache = cache
        elif cache_enabled:
            from src.utils.cache import create_response_cache
            self._cache = create_response_cache(
                max_size=cache_max_size,
                ttl_seconds=cache_ttl,
                config_manager=config_manager,
            )
        else:
            self._cache = None

        # Alerter for notifications (Phase 3.7.1)
        self._alerter = alerter

        # =====================================================================
        # Initialize Phase 4 components
        # =====================================================================
        
        if phase4_enabled:
            self.consensus_selector = consensus_selector or create_consensus_selector(
                config_manager=config_manager
            )
            
            self.conflict_detector = conflict_detector or create_conflict_detector(
                config_manager=config_manager
            )
            
            self.conflict_resolver = conflict_resolver or create_conflict_resolver(
                config_manager=config_manager,
                alerter=alerter,
            )
            
            self.result_aggregator = result_aggregator or create_result_aggregator(
                config_manager=config_manager
            )
            
            self.explainability_generator = (
                explainability_generator or create_explainability_generator(
                    config_manager=config_manager
                )
            )
            
            logger.info("✨ Phase 4 components initialized")
        else:
            self.consensus_selector = None
            self.conflict_detector = None
            self.conflict_resolver = None
            self.result_aggregator = None
            self.explainability_generator = None

        # Performance tracking
        self._total_requests: int = 0
        self._total_latency_ms: float = 0.0
        self._crisis_detections: int = 0
        self._cache_hits: int = 0
        self._conflicts_detected: int = 0

        # Thread pool for parallel inference
        self._executor: Optional[ThreadPoolExecutor] = None
        if async_inference:
            self._executor = ThreadPoolExecutor(max_workers=4)

        logger.info(
            f"🧠 EnsembleDecisionEngine initialized "
            f"(async={async_inference}, cache={cache_enabled}, phase4={phase4_enabled})"
        )

    # =========================================================================
    # Main Analysis Methods
    # =========================================================================

    def analyze(
        self,
        message: str,
        use_cache: bool = True,
        include_explanation: bool = True,
        verbosity: Optional[str] = None,
        consensus_algorithm: Optional[str] = None,
    ) -> CrisisAssessment:
        """
        Analyze a message for crisis signals.

        This is the PRIMARY method for crisis detection.
        Includes Phase 4 enhancements when enabled.

        Args:
            message: Text message to analyze
            use_cache: Whether to use response cache (default: True)
            include_explanation: Include human-readable explanation (Phase 4)
            verbosity: Explanation verbosity: minimal, standard, detailed (Phase 4)
            consensus_algorithm: Override consensus algorithm (Phase 4)

        Returns:
            CrisisAssessment with complete analysis
        """
        start_time = time.perf_counter()
        per_model_latency: Dict[str, float] = {}

        try:
            # Check cache first (Phase 3.7.4)
            if use_cache and self._cache is not None and self.cache_enabled:
                cached_result = self._cache.get(message)
                if cached_result is not None:
                    self._cache_hits += 1
                    self._total_requests += 1
                    # Update timing for cached response
                    cached_result.processing_time_ms = (
                        time.perf_counter() - start_time
                    ) * 1000
                    cached_result.cached = True
                    logger.debug(f"Cache hit for message (hash: {hash(message) % 10000})")
                    return cached_result

            # Run inference on all models
            inference_start = time.perf_counter()
            if self.async_inference and self._executor:
                results, per_model_latency = self._run_parallel_inference_with_timing(message)
            else:
                results, per_model_latency = self._run_sequential_inference_with_timing(message)

            # Calculate ensemble score (Phase 3 scoring)
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # Calculate processing time
            processing_time_ms = (time.perf_counter() - start_time) * 1000

            # =========================================================
            # Phase 4: Enhanced Processing
            # =========================================================
            
            consensus_result: Optional[ConsensusResult] = None
            conflict_report: Optional[ConflictReport] = None
            resolution_result: Optional[ResolutionResult] = None
            aggregated_result: Optional[AggregatedResult] = None
            explanation: Optional[Explanation] = None
            
            if self.phase4_enabled:
                # Extract crisis signals for consensus
                crisis_scores = {
                    name: signal.crisis_signal
                    for name, signal in ensemble_score.signals.items()
                }
                
                # Build signals dict for conflict detection
                signals_dict = {
                    name: {
                        "crisis_signal": signal.crisis_signal,
                        "label": signal.label,
                        "raw_score": signal.raw_score,
                        "score": signal.raw_score,
                        "metadata": signal.metadata,
                    }
                    for name, signal in ensemble_score.signals.items()
                }
                
                # Run consensus algorithm
                if self.consensus_selector:
                    algo = None
                    if consensus_algorithm:
                        try:
                            algo = ConsensusAlgorithm(consensus_algorithm)
                        except ValueError:
                            logger.warning(f"Invalid consensus algorithm: {consensus_algorithm}")
                    
                    consensus_result = self.consensus_selector.select_and_run(
                        model_signals=crisis_scores,
                        algorithm=algo,
                    )
                
                # Run conflict detection
                if self.conflict_detector:
                    model_signals = ModelSignals.from_ensemble_signals(signals_dict)
                    conflict_report = self.conflict_detector.detect_conflicts(
                        model_signals=model_signals,
                        crisis_scores=crisis_scores,
                    )
                    
                    if conflict_report.has_conflicts:
                        self._conflicts_detected += 1
                
                # Run conflict resolution if conflicts found
                if self.conflict_resolver and conflict_report and conflict_report.has_conflicts:
                    resolution_result = self.conflict_resolver.resolve(
                        crisis_scores=crisis_scores,
                        conflict_report=conflict_report,
                        message_preview=message[:100],
                    )
                
                # Aggregate results
                if self.result_aggregator:
                    aggregated_result = self.result_aggregator.aggregate(
                        model_signals=signals_dict,
                        consensus_result=consensus_result,
                        conflict_report=conflict_report,
                        resolution_result=resolution_result,
                        processing_time_ms=processing_time_ms,
                        per_model_latency=per_model_latency,
                        is_degraded=self.fallback.is_degraded(),
                        degradation_reason=self.fallback.get_degradation_reason(),
                        message=message,
                        cached=False,
                    )
                
                # Generate explanation
                if include_explanation and self.explainability_generator and aggregated_result:
                    verbosity_level = None
                    if verbosity:
                        try:
                            verbosity_level = VerbosityLevel(verbosity)
                        except ValueError:
                            pass
                    
                    explanation = self.explainability_generator.generate(
                        result=aggregated_result,
                        verbosity=verbosity_level,
                    )
                    
                    # Attach explanation to aggregated result
                    aggregated_result.explanation = explanation.to_dict()

            # Build assessment
            assessment = self._build_assessment_enhanced(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
                consensus_result=consensus_result,
                conflict_report=conflict_report,
                resolution_result=resolution_result,
                aggregated_result=aggregated_result,
                explanation=explanation,
            )

            # Store in cache (Phase 3.7.4)
            if use_cache and self._cache is not None and self.cache_enabled:
                self._cache.set(message, assessment)

            # Update stats
            self._total_requests += 1
            self._total_latency_ms += processing_time_ms
            if assessment.crisis_detected:
                self._crisis_detections += 1

            return assessment

        except CriticalModelFailure as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.critical(f"🚨 Critical model failure during analysis: {e}")
            
            # Send alert if alerter configured
            if self._alerter:
                asyncio.create_task(
                    self._alerter.alert_model_failure("bart", str(e), is_critical=True)
                )
            
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

    async def analyze_async(
        self,
        message: str,
        use_cache: bool = True,
        include_explanation: bool = True,
        verbosity: Optional[str] = None,
        consensus_algorithm: Optional[str] = None,
    ) -> CrisisAssessment:
        """
        Async version of analyze using asyncio.gather for parallel inference.

        This is the optimized async implementation (Phase 3.7.2).
        Includes Phase 4 enhancements when enabled.

        Args:
            message: Text message to analyze
            use_cache: Whether to use response cache
            include_explanation: Include human-readable explanation (Phase 4)
            verbosity: Explanation verbosity level (Phase 4)
            consensus_algorithm: Override consensus algorithm (Phase 4)

        Returns:
            CrisisAssessment with complete analysis
        """
        start_time = time.perf_counter()
        per_model_latency: Dict[str, float] = {}

        try:
            # Check cache first (Phase 3.7.4)
            if use_cache and self._cache is not None and self.cache_enabled:
                cached_result = self._cache.get(message)
                if cached_result is not None:
                    self._cache_hits += 1
                    self._total_requests += 1
                    cached_result.processing_time_ms = (
                        time.perf_counter() - start_time
                    ) * 1000
                    cached_result.cached = True
                    return cached_result

            # Run parallel inference with asyncio.gather (Phase 3.7.2)
            results, per_model_latency = await self._run_async_parallel_inference_with_timing(message)

            # Calculate ensemble score
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # Calculate processing time
            processing_time_ms = (time.perf_counter() - start_time) * 1000

            # =========================================================
            # Phase 4: Enhanced Processing (Async)
            # =========================================================
            
            consensus_result: Optional[ConsensusResult] = None
            conflict_report: Optional[ConflictReport] = None
            resolution_result: Optional[ResolutionResult] = None
            aggregated_result: Optional[AggregatedResult] = None
            explanation: Optional[Explanation] = None
            
            if self.phase4_enabled:
                # Extract crisis signals
                crisis_scores = {
                    name: signal.crisis_signal
                    for name, signal in ensemble_score.signals.items()
                }
                
                signals_dict = {
                    name: {
                        "crisis_signal": signal.crisis_signal,
                        "label": signal.label,
                        "raw_score": signal.raw_score,
                        "score": signal.raw_score,
                        "metadata": signal.metadata,
                    }
                    for name, signal in ensemble_score.signals.items()
                }
                
                # Run consensus
                if self.consensus_selector:
                    algo = None
                    if consensus_algorithm:
                        try:
                            algo = ConsensusAlgorithm(consensus_algorithm)
                        except ValueError:
                            pass
                    
                    consensus_result = self.consensus_selector.select_and_run(
                        model_signals=crisis_scores,
                        algorithm=algo,
                    )
                
                # Run conflict detection
                if self.conflict_detector:
                    model_signals = ModelSignals.from_ensemble_signals(signals_dict)
                    conflict_report = self.conflict_detector.detect_conflicts(
                        model_signals=model_signals,
                        crisis_scores=crisis_scores,
                    )
                    
                    if conflict_report.has_conflicts:
                        self._conflicts_detected += 1
                
                # Run conflict resolution (async)
                if self.conflict_resolver and conflict_report and conflict_report.has_conflicts:
                    resolution_result = await self.conflict_resolver.resolve_async(
                        crisis_scores=crisis_scores,
                        conflict_report=conflict_report,
                        message_preview=message[:100],
                    )
                
                # Aggregate results
                if self.result_aggregator:
                    aggregated_result = self.result_aggregator.aggregate(
                        model_signals=signals_dict,
                        consensus_result=consensus_result,
                        conflict_report=conflict_report,
                        resolution_result=resolution_result,
                        processing_time_ms=processing_time_ms,
                        per_model_latency=per_model_latency,
                        is_degraded=self.fallback.is_degraded(),
                        degradation_reason=self.fallback.get_degradation_reason(),
                        message=message,
                        cached=False,
                    )
                
                # Generate explanation
                if include_explanation and self.explainability_generator and aggregated_result:
                    verbosity_level = None
                    if verbosity:
                        try:
                            verbosity_level = VerbosityLevel(verbosity)
                        except ValueError:
                            pass
                    
                    explanation = self.explainability_generator.generate(
                        result=aggregated_result,
                        verbosity=verbosity_level,
                    )
                    
                    aggregated_result.explanation = explanation.to_dict()

            # Build assessment
            assessment = self._build_assessment_enhanced(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
                consensus_result=consensus_result,
                conflict_report=conflict_report,
                resolution_result=resolution_result,
                aggregated_result=aggregated_result,
                explanation=explanation,
            )

            # Store in cache
            if use_cache and self._cache is not None and self.cache_enabled:
                self._cache.set(message, assessment)

            # Update stats
            self._total_requests += 1
            self._total_latency_ms += processing_time_ms
            if assessment.crisis_detected:
                self._crisis_detections += 1

            return assessment

        except CriticalModelFailure as e:
            processing_time_ms = (time.perf_counter() - start_time) * 1000
            logger.critical(f"🚨 Critical model failure during analysis: {e}")
            
            if self._alerter:
                await self._alerter.alert_model_failure("bart", str(e), is_critical=True)
            
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

    # =========================================================================
    # Inference Methods with Timing
    # =========================================================================

    def _run_sequential_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run sequential inference with per-model timing."""
        results: Dict[str, Optional[ModelResult]] = {}
        latencies: Dict[str, float] = {}
        model_names = ["bart", "sentiment", "irony", "emotions"]

        for model_name in model_names:
            if self.fallback.can_call_model(model_name):
                model_start = time.perf_counter()
                try:
                    model = self.model_loader.get_model(model_name)
                    if model:
                        results[model_name] = model.analyze(message)
                        self.fallback.handle_model_success(model_name)
                except Exception as e:
                    self.fallback.handle_model_failure(model_name, str(e))
                finally:
                    latencies[model_name] = (time.perf_counter() - model_start) * 1000

        return results, latencies

    def _run_parallel_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run parallel inference with per-model timing."""
        results: Dict[str, Optional[ModelResult]] = {}
        latencies: Dict[str, float] = {}

        def run_model(model_name: str) -> tuple:
            if not self.fallback.can_call_model(model_name):
                return (model_name, None, 0.0)

            model_start = time.perf_counter()
            try:
                model = self.model_loader.get_model(model_name)
                if model:
                    result = model.analyze(message)
                    self.fallback.handle_model_success(model_name)
                    latency = (time.perf_counter() - model_start) * 1000
                    return (model_name, result, latency)
                return (model_name, None, 0.0)
            except Exception as e:
                self.fallback.handle_model_failure(model_name, str(e))
                latency = (time.perf_counter() - model_start) * 1000
                return (model_name, None, latency)

        model_names = ["bart", "sentiment", "irony", "emotions"]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(run_model, name): name for name in model_names}

            for future in futures:
                model_name = futures[future]
                try:
                    name, result, latency = future.result(timeout=30)
                    if result:
                        results[name] = result
                    latencies[name] = latency
                except Exception as e:
                    logger.error(f"Parallel inference failed for {model_name}: {e}")

        return results, latencies

    async def _run_async_parallel_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run async parallel inference with per-model timing."""
        loop = asyncio.get_event_loop()

        async def run_model_async(model_name: str) -> tuple:
            if not self.fallback.can_call_model(model_name):
                return (model_name, None, 0.0)

            model_start = time.perf_counter()
            try:
                model = self.model_loader.get_model(model_name)
                if model:
                    result = await loop.run_in_executor(
                        self._executor,
                        model.analyze,
                        message,
                    )
                    self.fallback.handle_model_success(model_name)
                    latency = (time.perf_counter() - model_start) * 1000
                    return (model_name, result, latency)
                return (model_name, None, 0.0)
            except Exception as e:
                self.fallback.handle_model_failure(model_name, str(e))
                logger.warning(f"Model {model_name} failed: {e}")
                latency = (time.perf_counter() - model_start) * 1000
                return (model_name, None, latency)

        model_names = ["bart", "sentiment", "irony", "emotions"]
        tasks = [run_model_async(name) for name in model_names]
        
        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        results: Dict[str, Optional[ModelResult]] = {}
        latencies: Dict[str, float] = {}

        for item in results_list:
            if isinstance(item, Exception):
                logger.error(f"Async inference exception: {item}")
                continue
            if isinstance(item, tuple) and len(item) == 3:
                model_name, result, latency = item
                if result is not None:
                    results[model_name] = result
                latencies[model_name] = latency

        return results, latencies

    # =========================================================================
    # Assessment Building
    # =========================================================================

    def _build_assessment_enhanced(
        self,
        ensemble_score: EnsembleScore,
        results: Dict[str, Optional[ModelResult]],
        message: str,
        processing_time_ms: float,
        consensus_result: Optional[ConsensusResult] = None,
        conflict_report: Optional[ConflictReport] = None,
        resolution_result: Optional[ResolutionResult] = None,
        aggregated_result: Optional[AggregatedResult] = None,
        explanation: Optional[Explanation] = None,
    ) -> CrisisAssessment:
        """
        Build CrisisAssessment with Phase 4 enhancements.

        Args:
            ensemble_score: Calculated ensemble score
            results: Model results
            message: Original message
            processing_time_ms: Processing time
            consensus_result: Phase 4 consensus result
            conflict_report: Phase 4 conflict report
            resolution_result: Phase 4 resolution result
            aggregated_result: Phase 4 aggregated result
            explanation: Phase 4 explanation

        Returns:
            Complete CrisisAssessment with Phase 4 data
        """
        # Use resolved score if available, otherwise ensemble score
        final_crisis_score = ensemble_score.crisis_score
        if resolution_result and resolution_result.was_modified:
            final_crisis_score = resolution_result.resolved_score

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

        # Check if review required
        requires_review = False
        if resolution_result and resolution_result.requires_review:
            requires_review = True
        elif conflict_report and conflict_report.requires_review:
            requires_review = True

        # Build assessment
        assessment = CrisisAssessment(
            crisis_detected=ensemble_score.crisis_detected,
            severity=ensemble_score.severity,
            confidence=ensemble_score.confidence,
            crisis_score=final_crisis_score,
            requires_intervention=ensemble_score.requires_intervention or requires_review,
            recommended_action=recommended_action,
            signals=signals,
            processing_time_ms=processing_time_ms,
            models_used=models_used,
            is_degraded=self.fallback.is_degraded(),
            degradation_reason=self.fallback.get_degradation_reason(),
            message=message,
            # Phase 4 fields
            explanation=explanation.to_dict() if explanation else None,
            conflict_report=conflict_report.to_dict() if conflict_report else None,
            consensus_result=consensus_result.to_dict() if consensus_result else None,
            aggregated_result=aggregated_result,
        )

        return assessment

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

        # Clear cache
        if self._cache:
            self._cache.clear()

        logger.info("✅ Decision Engine shutdown complete")

    def warmup(self, sample_text: str = "Hello, how are you today?") -> bool:
        """
        Warm up the engine with a sample analysis.

        Phase 3.7.1: Model warmup on startup.

        Args:
            sample_text: Text to use for warmup

        Returns:
            True if warmup succeeded
        """
        logger.info("🔥 Warming up Decision Engine...")

        try:
            # Run warmup analysis (bypass cache)
            result = self.analyze(sample_text, use_cache=False, include_explanation=False)

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

    def set_alerter(self, alerter: "DiscordAlerter") -> None:
        """
        Set the Discord alerter for notifications.

        Args:
            alerter: DiscordAlerter instance
        """
        self._alerter = alerter
        
        # Also set on conflict resolver
        if self.conflict_resolver:
            self.conflict_resolver.set_alerter(alerter)
            
        logger.debug("Discord alerter configured")

    # =========================================================================
    # Phase 4 Configuration Methods
    # =========================================================================

    def set_consensus_algorithm(self, algorithm: str) -> None:
        """Set the default consensus algorithm."""
        if self.consensus_selector:
            try:
                algo = ConsensusAlgorithm(algorithm)
                self.consensus_selector.set_algorithm(algo)
                logger.info(f"Consensus algorithm set to: {algorithm}")
            except ValueError:
                logger.warning(f"Invalid consensus algorithm: {algorithm}")

    def set_resolution_strategy(self, strategy: str) -> None:
        """Set the default conflict resolution strategy."""
        if self.conflict_resolver:
            try:
                strat = ResolutionStrategy(strategy)
                self.conflict_resolver.set_strategy(strat)
                logger.info(f"Resolution strategy set to: {strategy}")
            except ValueError:
                logger.warning(f"Invalid resolution strategy: {strategy}")

    def set_explainability_verbosity(self, verbosity: str) -> None:
        """Set the default explainability verbosity."""
        if self.explainability_generator:
            try:
                level = VerbosityLevel(verbosity)
                self.explainability_generator.set_verbosity(level)
                logger.info(f"Explainability verbosity set to: {verbosity}")
            except ValueError:
                logger.warning(f"Invalid verbosity level: {verbosity}")

    def get_consensus_config(self) -> Optional[Dict[str, Any]]:
        """Get current consensus configuration."""
        if self.consensus_selector:
            return self.consensus_selector.get_config()
        return None

    def get_conflict_config(self) -> Optional[Dict[str, Any]]:
        """Get current conflict detection configuration."""
        if self.conflict_detector:
            return self.conflict_detector.get_config()
        return None

    # =========================================================================
    # Cache Management
    # =========================================================================

    def clear_cache(self) -> int:
        """
        Clear the response cache.

        Returns:
            Number of entries cleared
        """
        if self._cache:
            return self._cache.clear()
        return 0

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Cache stats dictionary
        """
        if self._cache:
            return self._cache.get_stats()
        return {"enabled": False}

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

        cache_hit_rate = (
            self._cache_hits / self._total_requests
            if self._total_requests > 0
            else 0.0
        )

        status = {
            "is_ready": self.is_ready(),
            "is_degraded": self.fallback.is_degraded(),
            "degradation_reason": self.fallback.get_degradation_reason(),
            "async_inference": self.async_inference,
            "cache_enabled": self.cache_enabled,
            "phase4_enabled": self.phase4_enabled,
            "stats": {
                "total_requests": self._total_requests,
                "crisis_detections": self._crisis_detections,
                "conflicts_detected": self._conflicts_detected,
                "cache_hits": self._cache_hits,
                "cache_hit_rate": round(cache_hit_rate, 4),
                "average_latency_ms": round(avg_latency, 2),
            },
            "models": self.model_loader.get_status(),
            "weights": self.scorer.get_weights(),
            "thresholds": self.scorer.get_thresholds(),
            "fallback": self.fallback.get_status(),
            "cache": self.get_cache_stats(),
        }
        
        # Add Phase 4 component status
        if self.phase4_enabled:
            status["phase4"] = {
                "consensus": self.get_consensus_config(),
                "conflict_detection": self.get_conflict_config(),
                "conflict_resolution": (
                    self.conflict_resolver.get_config() if self.conflict_resolver else None
                ),
                "explainability": (
                    self.explainability_generator.get_config() if self.explainability_generator else None
                ),
            }
            
        return status

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
            "cache_enabled": self.cache_enabled,
            "phase4_enabled": self.phase4_enabled,
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


def create_decision_engine(
    config_manager: Optional["ConfigManager"] = None,
    auto_initialize: bool = False,
    async_inference: bool = True,
    cache_enabled: bool = True,
    alerter: Optional["DiscordAlerter"] = None,
    phase4_enabled: bool = True,
) -> EnsembleDecisionEngine:
    """
    Factory function for EnsembleDecisionEngine.

    Creates a fully configured decision engine with Phase 4 enhancements.

    Args:
        config_manager: Configuration manager instance
        auto_initialize: If True, load models immediately
        async_inference: Enable parallel model inference
        cache_enabled: Enable response caching
        alerter: Discord alerter for notifications
        phase4_enabled: Enable Phase 4 features (default: True)

    Returns:
        Configured EnsembleDecisionEngine instance

    Example:
        >>> engine = create_decision_engine(config_manager=config)
        >>> engine.initialize()
        >>> assessment = engine.analyze("I'm feeling really down today")
        >>> print(assessment.explanation)  # Phase 4 explanation
    """
    # Get settings from config
    perf_config = {}
    if config_manager is not None:
        perf_config = config_manager.get_performance_config() or {}
        async_inference = perf_config.get("async_inference", async_inference)
        cache_enabled = perf_config.get("cache_enabled", cache_enabled)

    cache_ttl = perf_config.get("cache_ttl", 300.0)
    cache_max_size = perf_config.get("cache_max_size", 1000)

    engine = EnsembleDecisionEngine(
        config_manager=config_manager,
        async_inference=async_inference,
        cache_enabled=cache_enabled,
        cache_ttl=cache_ttl,
        cache_max_size=cache_max_size,
        alerter=alerter,
        phase4_enabled=phase4_enabled,
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
