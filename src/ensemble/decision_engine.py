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
FILE VERSION: v5.1-6-6.4.3-1
LAST MODIFIED: 2026-02-15
PHASE: Phase 6 - Step 6.4.3 Decision Engine Decomposition
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

RESPONSIBILITIES:
- Orchestrate multi-model ensemble inference
- Coordinate model loading, scoring, and fallback
- Provide unified analyze() method for API
- Calculate final crisis assessment
- Handle async parallel inference with asyncio.gather()
- Cache responses for repeated messages
- Integrate Ash-Vigil for specialized risk detection (Phase 3 Vigil)

PHASE 3 VIGIL INTEGRATION:
- Ash-Vigil client integration for mental health risk detection
- Risk amplification for subtle crisis signals BART missed
- Configurable skip threshold and amplify_medium toggle
- Hard score cap at 1.0 to prevent exponential creep
- Graceful fallback when Vigil unavailable
- requires_review flag for HIGH/CRITICAL or Vigil unavailable

PROCESSING FLOW (Phase 3 Vigil):
1. Run 4-model ensemble → base score (no irony dampening yet)
2. Determine preliminary severity from base score
3. Decision Gate: Should we call Vigil?
   - If base_score >= skip_threshold → Skip Vigil (score-based)
   - If BART confidence >= crisis_threshold AND crisis label → Skip Vigil (confident crisis)
   - If BART confidence >= safe_threshold AND safe label → Skip Vigil (confident safe)
   - If MEDIUM severity and amplify_medium=false → Skip Vigil
   - Otherwise → Call Vigil
4. Apply Vigil amplification (cap at 1.0)
5. Apply irony dampening (FINAL step)
6. Determine final severity, set requires_review for HIGH/CRITICAL
7. Return response with vigil field

PHASE 4 ENHANCEMENTS:
- Consensus algorithm selection (weighted, majority, unanimous, conflict-aware)
- Conflict detection and resolution
- Comprehensive result aggregation
- Human-readable explainability

PHASE 5 ENHANCEMENTS:
- Context history analysis integration
- Escalation pattern detection (rapid, gradual, sudden)
- Temporal pattern detection (late night, rapid posting)
- Trend analysis (worsening, stable, improving)
- Intervention urgency recommendations

This is the PRIMARY INTERFACE for crisis detection.
API endpoints call this engine to analyze messages.

PERFORMANCE OPTIMIZATIONS (Phase 3.7):
- 3.7.1: Model warmup on startup with alerting
- 3.7.2: Async parallel inference with asyncio.gather()
- 3.7.4: Response caching for repeated messages
"""

import asyncio
import copy
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

from src.models import ModelResult

from .model_loader import ModelLoader, create_model_loader
from .scoring import (
    WeightedScorer,
    create_weighted_scorer,
    EnsembleScore,
    CrisisSeverity,
    ModelSignal,
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

# Phase 5 imports
from src.context import (
    ContextAnalyzer,
    create_context_analyzer,
    MessageHistoryItem,
    ContextAnalysisResult,
)

# Phase 3 Vigil imports
from src.clients.vigil_client import (
    VigilClient,
    VigilStatus,
    create_vigil_client,
)

if TYPE_CHECKING:
    from src.managers.config_manager import ConfigManager
    from src.utils.cache import ResponseCache
    from src.utils.alerting import DiscordAlerter

# Module version
__version__ = "v5.1-6-6.4.3-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Data Models (extracted to data_models.py in Step 6.4.3)
# =============================================================================

from .data_models import (
    WarmupResult,
    VigilResponse,
    CrisisAssessment,
    RecommendedAction,
    IronyGateResult,
    IronyGate,
    create_irony_gate,
)

from .vigil_amplification import (
    DEFAULT_VIGIL_AMPLIFICATION,
    load_vigil_config,
    apply_vigil_amplification,
    apply_vigil_amplification_sync,
    determine_requires_review,
)

from .inference import (
    run_sequential_inference,
    run_parallel_inference,
    run_async_parallel_inference,
)

from .consensus_escalation import (
    ConsensusEscalation,
    ConsensusEscalationResult,
    create_consensus_escalation,
)


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

    Phase 3 Vigil Integration:
    - Calls Ash-Vigil for specialized mental health risk detection
    - Amplifies base scores when Vigil detects subtle crisis signals
    - Sets requires_review for HIGH/CRITICAL or Vigil unavailable

    Phase 4 Enhancements:
    - Consensus algorithm selection
    - Conflict detection and resolution
    - Comprehensive result aggregation
    - Human-readable explainability

    Phase 5 Enhancements:
    - Context history analysis integration
    - Escalation, temporal, and trend detection
    - Intervention urgency recommendations

    Phase 6 Enhancements:
    - Irony gatekeeper replaces continuous dampening
    - IronyGate applied AFTER Vigil amplification, BEFORE final severity
    - Only fires when irony confidence >= configurable threshold
    - Zero effect when irony not detected (true pass-through)

    This is the main interface for the API to call.

    Performance Optimizations (Phase 3.7):
    - Model warmup on startup (3.7.1)
    - Async parallel inference with asyncio.gather (3.7.2)
    - Response caching (3.7.4)

    Clean Architecture v5.2.3 Compliance:
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
        # Phase 3 Vigil components
        vigil_client: Optional[VigilClient] = None,
        vigil_enabled: bool = True,
        # Phase 4 components
        consensus_selector: Optional[ConsensusSelector] = None,
        conflict_detector: Optional[ConflictDetector] = None,
        conflict_resolver: Optional[ConflictResolver] = None,
        result_aggregator: Optional[ResultAggregator] = None,
        explainability_generator: Optional[ExplainabilityGenerator] = None,
        phase4_enabled: bool = True,
        # Phase 5 components
        context_analyzer: Optional[ContextAnalyzer] = None,
        phase5_enabled: bool = True,
        # Phase 6 components
        irony_gate: Optional[IronyGate] = None,
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

            # Phase 3 Vigil components
            vigil_client: Pre-configured Vigil client (optional)
            vigil_enabled: Enable Vigil integration (default: True)

            # Phase 4 components
            consensus_selector: Consensus algorithm selector
            conflict_detector: Conflict detection component
            conflict_resolver: Conflict resolution component
            result_aggregator: Result aggregation component
            explainability_generator: Explainability component
            phase4_enabled: Enable Phase 4 features (default: True)

            # Phase 5 components
            context_analyzer: Context history analyzer component
            phase5_enabled: Enable Phase 5 features (default: True)

            # Phase 6 components
            irony_gate: Pre-configured IronyGate (optional, auto-created from config)
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
        # Initialize Phase 3 Vigil components
        # =====================================================================

        self.vigil_enabled = vigil_enabled
        self._vigil_client: Optional[VigilClient] = None
        self._vigil_amplification_config = copy.deepcopy(DEFAULT_VIGIL_AMPLIFICATION)

        if vigil_enabled:
            # Load Vigil configuration (extracted to vigil_amplification.py)
            self._vigil_amplification_config = load_vigil_config(
                config_manager, self._vigil_amplification_config
            )

            # Initialize Vigil client
            if vigil_client is not None:
                self._vigil_client = vigil_client
            else:
                self._vigil_client = create_vigil_client(
                    config_manager=config_manager,
                )

            logger.info(
                f"🔌 Phase 3 Vigil integration initialized "
                f"(skip_threshold={self._vigil_amplification_config['skip_threshold']}, "
                f"amplify_medium={self._vigil_amplification_config['amplify_medium']})"
            )
        else:
            logger.info("🔌 Phase 3 Vigil integration DISABLED")

        # =====================================================================
        # Initialize Phase 4 components
        # =====================================================================

        if phase4_enabled:
            # v5.1-6-6.4.3: Consensus selector RE-ENABLED as READ-ONLY.
            # The consensus score is used by ConsensusEscalation as a
            # safety net — it never overrides the pipeline score, only
            # provides a severity floor when significant disagreement
            # is detected. Conflict resolver remains DISABLED.
            self.consensus_selector = (
                consensus_selector
                or create_consensus_selector(config_manager=config_manager)
            )
            self.conflict_resolver = None

            self.conflict_detector = conflict_detector or create_conflict_detector(
                config_manager=config_manager
            )

            self.result_aggregator = result_aggregator or create_result_aggregator(
                config_manager=config_manager
            )

            self.explainability_generator = (
                explainability_generator
                or create_explainability_generator(config_manager=config_manager)
            )

            # Step 6.4.3: Consensus Escalation (severity floor safety net)
            self.consensus_escalation = create_consensus_escalation(
                config_manager=config_manager,
            )

            logger.info(
                "✨ Phase 4 components initialized "
                "(consensus=read-only for escalation, resolution=disabled)"
            )
        else:
            self.consensus_selector = None
            self.conflict_detector = None
            self.conflict_resolver = None
            self.result_aggregator = None
            self.explainability_generator = None
            self.consensus_escalation = None

        # =====================================================================
        # Initialize Phase 5 components
        # =====================================================================

        self.phase5_enabled = phase5_enabled

        if phase5_enabled:
            self.context_analyzer = context_analyzer or create_context_analyzer()
            logger.info("🌊 Phase 5 context analyzer initialized")
        else:
            self.context_analyzer = None

        # =====================================================================
        # Initialize Phase 6 components
        # =====================================================================

        self.irony_gate = irony_gate or create_irony_gate(
            config_manager=config_manager
        )

        # Performance tracking
        self._total_requests: int = 0
        self._total_latency_ms: float = 0.0
        self._crisis_detections: int = 0
        self._cache_hits: int = 0
        self._conflicts_detected: int = 0
        self._vigil_calls: int = 0
        self._vigil_amplifications: int = 0
        self._vigil_confidence_skips: int = 0
        self._irony_gate_triggers: int = 0
        self._consensus_escalations: int = 0

        # Thread pool for parallel inference
        self._executor: Optional[ThreadPoolExecutor] = None
        if async_inference:
            self._executor = ThreadPoolExecutor(max_workers=4)

        logger.info(
            f"🧠 EnsembleDecisionEngine initialized "
            f"(async={async_inference}, cache={cache_enabled}, "
            f"vigil={vigil_enabled}, phase4={phase4_enabled}, phase5={phase5_enabled})"
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
        message_history: Optional[List[Dict]] = None,
        include_context_analysis: bool = True,
    ) -> CrisisAssessment:
        """
        Analyze a message for crisis signals.

        This is the PRIMARY method for crisis detection.
        Includes Phase 3 Vigil, Phase 4, and Phase 5 enhancements.

        Args:
            message: Text message to analyze
            use_cache: Whether to use response cache (default: True)
            include_explanation: Include human-readable explanation (Phase 4)
            verbosity: Explanation verbosity: minimal, standard, detailed (Phase 4)
            consensus_algorithm: Override consensus algorithm (Phase 4)
            message_history: List of prior messages with timestamps/scores (Phase 5)
            include_context_analysis: Include context analysis in response (Phase 5)

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
                    logger.debug(
                        f"Cache hit for message (hash: {hash(message) % 10000})"
                    )
                    return cached_result

            # Run inference on all models
            inference_start = time.perf_counter()
            if self.async_inference and self._executor:
                results, per_model_latency = self._run_parallel_inference_with_timing(
                    message
                )
            else:
                results, per_model_latency = self._run_sequential_inference_with_timing(
                    message
                )

            # Calculate ensemble score (Phase 3 scoring)
            # This gives us base_score (before irony) and irony_dampening factor
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # =================================================================
            # Phase 3 Vigil: Apply amplification BEFORE irony gate
            # =================================================================

            # Get base score (Phase 6: irony_dampening is always 1.0 from scorer)
            base_score = ensemble_score.base_score

            # Determine preliminary severity from base score
            preliminary_severity = CrisisSeverity.from_score(
                base_score, self.scorer.get_thresholds()
            )

            # Apply Vigil amplification (sync version)
            vigil_response: VigilResponse
            if self.vigil_enabled:
                bart_signal = ensemble_score.signals.get("bart")
                amplified_score, vigil_response, was_called, was_amplified, was_conf_skip = (
                    apply_vigil_amplification_sync(
                        base_score=base_score,
                        base_severity=preliminary_severity,
                        text=message,
                        config=self._vigil_amplification_config,
                        vigil_client=self._vigil_client,
                        bart_signal=bart_signal,
                    )
                )
                if was_called:
                    self._vigil_calls += 1
                if was_amplified:
                    self._vigil_amplifications += 1
                if was_conf_skip:
                    self._vigil_confidence_skips += 1
            else:
                amplified_score = base_score
                vigil_response = VigilResponse(
                    status=VigilStatus.DISABLED,
                    base_score=base_score,
                )

            # =================================================================
            # Phase 6: Apply Irony Gatekeeper AFTER Vigil amplification
            # =================================================================

            irony_signal = ensemble_score.signals.get("irony")
            irony_gate_result = self.irony_gate.apply(
                score=amplified_score,
                irony_signal=irony_signal,
            )
            final_score = irony_gate_result.gated_score

            if irony_gate_result.triggered:
                self._irony_gate_triggers += 1

            # Pipeline score/severity (pre-escalation)
            pipeline_score = final_score
            pipeline_severity = CrisisSeverity.from_score(
                pipeline_score, self.scorer.get_thresholds()
            )

            # =================================================================
            # Step 6.4.3: Consensus Disagreement Escalation (severity floor)
            # =================================================================

            consensus_escalation_result: Optional[ConsensusEscalationResult] = None
            consensus_result_from_escalation: Optional[ConsensusResult] = None

            if (
                self.phase4_enabled
                and self.consensus_selector is not None
                and self.consensus_escalation is not None
            ):
                try:
                    # Extract per-model crisis signals for consensus vote
                    crisis_scores_for_consensus = {
                        name: signal.crisis_signal
                        for name, signal in ensemble_score.signals.items()
                    }

                    # Run consensus algorithm (read-only — score not used directly)
                    consensus_run_result = self.consensus_selector.select_and_run(
                        model_signals=crisis_scores_for_consensus,
                    )

                    if consensus_run_result is not None:
                        # Store for Phase 4 aggregation
                        consensus_result_from_escalation = consensus_run_result

                        # Apply severity floor
                        consensus_escalation_result = self.consensus_escalation.apply_floor(
                            pipeline_score=pipeline_score,
                            pipeline_severity=pipeline_severity,
                            consensus_score=consensus_run_result.crisis_score,
                            thresholds=self.scorer.get_thresholds(),
                        )

                        if consensus_escalation_result.triggered:
                            # Floor was applied — update final score/severity
                            final_score = consensus_escalation_result.final_score
                            self._consensus_escalations += 1
                            logger.info(
                                f"🛡️ Consensus escalation applied: "
                                f"{pipeline_score:.3f} → {final_score:.3f}"
                            )

                except Exception as e:
                    logger.warning(f"⚠️ Consensus escalation failed (non-fatal): {e}")

            # Recalculate final severity (may have been updated by escalation)
            final_severity = CrisisSeverity.from_score(
                final_score, self.scorer.get_thresholds()
            )

            # Determine if review required
            requires_review = determine_requires_review(
                final_severity, vigil_response
            )

            # Step 6.4.3: Escalation also sets requires_review
            if (
                consensus_escalation_result is not None
                and consensus_escalation_result.triggered
                and self.consensus_escalation is not None
                and self.consensus_escalation.set_requires_review
            ):
                requires_review = True

            # Update ensemble_score with our recalculated values
            # (We override the scorer's irony-dampened value with our Vigil-amplified one)
            ensemble_score.crisis_score = final_score
            ensemble_score.severity = final_severity
            ensemble_score.crisis_detected = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
                CrisisSeverity.MEDIUM,
            )
            ensemble_score.requires_intervention = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
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

                # v5.1-6-6.4.3: Consensus was already run in the escalation
                # block above. Use the stored result for aggregation.
                consensus_result = consensus_result_from_escalation

                # Run conflict detection (informational only — does not modify scores)
                if self.conflict_detector:
                    model_signals = ModelSignals.from_ensemble_signals(signals_dict)
                    conflict_report = self.conflict_detector.detect_conflicts(
                        model_signals=model_signals,
                        crisis_scores=crisis_scores,
                    )

                    if conflict_report.has_conflicts:
                        self._conflicts_detected += 1

                # v5.1-6-6.4-2: Conflict resolution DISABLED — see init comment.

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
                if (
                    include_explanation
                    and self.explainability_generator
                    and aggregated_result
                ):
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

            # =========================================================
            # Phase 5: Context History Analysis
            # =========================================================

            context_analysis_result: Optional[ContextAnalysisResult] = None

            if (
                self.phase5_enabled
                and include_context_analysis
                and self.context_analyzer
            ):
                try:
                    # Convert message history to MessageHistoryItem objects
                    history_items: List[MessageHistoryItem] = []
                    if message_history:
                        for item in message_history:
                            history_items.append(MessageHistoryItem.from_dict(item))

                    # Run context analysis with current message score
                    context_analysis_result = self.context_analyzer.analyze(
                        current_message=message,
                        current_score=final_score,
                        message_history=history_items,
                    )

                    logger.debug(
                        f"Context analysis: escalation={context_analysis_result.escalation.detected}, "
                        f"trend={context_analysis_result.trend.direction}, "
                        f"urgency={context_analysis_result.intervention.urgency}"
                    )

                except Exception as e:
                    logger.error(f"Context analysis failed: {e}")
                    # Continue without context analysis - non-critical failure

            # Build assessment
            assessment = self._build_assessment_enhanced(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
                vigil_response=vigil_response,
                requires_review=requires_review,
                consensus_result=consensus_result,
                conflict_report=conflict_report,
                resolution_result=resolution_result,
                aggregated_result=aggregated_result,
                explanation=explanation,
                context_analysis_result=context_analysis_result,
                irony_gate_result=irony_gate_result,
                consensus_escalation_result=consensus_escalation_result,
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
        message_history: Optional[List[Dict]] = None,
        include_context_analysis: bool = True,
    ) -> CrisisAssessment:
        """
        Async version of analyze using asyncio.gather for parallel inference.

        This is the optimized async implementation (Phase 3.7.2).
        Includes Phase 3 Vigil, Phase 4, and Phase 5 enhancements.

        Args:
            message: Text message to analyze
            use_cache: Whether to use response cache
            include_explanation: Include human-readable explanation (Phase 4)
            verbosity: Explanation verbosity level (Phase 4)
            consensus_algorithm: Override consensus algorithm (Phase 4)
            message_history: List of prior messages with timestamps/scores (Phase 5)
            include_context_analysis: Include context analysis in response (Phase 5)

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
            (
                results,
                per_model_latency,
            ) = await self._run_async_parallel_inference_with_timing(message)

            # Calculate ensemble score
            ensemble_score = self.scorer.calculate_score(
                bart_result=results.get("bart"),
                sentiment_result=results.get("sentiment"),
                irony_result=results.get("irony"),
                emotions_result=results.get("emotions"),
            )

            # =================================================================
            # Phase 3 Vigil: Apply amplification BEFORE irony gate
            # =================================================================

            base_score = ensemble_score.base_score

            preliminary_severity = CrisisSeverity.from_score(
                base_score, self.scorer.get_thresholds()
            )

            # Apply Vigil amplification (async version)
            vigil_response: VigilResponse
            if self.vigil_enabled:
                bart_signal = ensemble_score.signals.get("bart")
                amplified_score, vigil_response, was_called, was_amplified, was_conf_skip = (
                    await apply_vigil_amplification(
                        base_score=base_score,
                        base_severity=preliminary_severity,
                        text=message,
                        config=self._vigil_amplification_config,
                        vigil_client=self._vigil_client,
                        bart_signal=bart_signal,
                    )
                )
                if was_called:
                    self._vigil_calls += 1
                if was_amplified:
                    self._vigil_amplifications += 1
                if was_conf_skip:
                    self._vigil_confidence_skips += 1
            else:
                amplified_score = base_score
                vigil_response = VigilResponse(
                    status=VigilStatus.DISABLED,
                    base_score=base_score,
                )

            # =================================================================
            # Phase 6: Apply Irony Gatekeeper AFTER Vigil amplification
            # =================================================================

            irony_signal = ensemble_score.signals.get("irony")
            irony_gate_result = self.irony_gate.apply(
                score=amplified_score,
                irony_signal=irony_signal,
            )
            final_score = irony_gate_result.gated_score

            if irony_gate_result.triggered:
                self._irony_gate_triggers += 1

            # Pipeline score/severity (pre-escalation)
            pipeline_score = final_score
            pipeline_severity = CrisisSeverity.from_score(
                pipeline_score, self.scorer.get_thresholds()
            )

            # =================================================================
            # Step 6.4.3: Consensus Disagreement Escalation (severity floor)
            # =================================================================

            consensus_escalation_result: Optional[ConsensusEscalationResult] = None
            consensus_result_from_escalation: Optional[ConsensusResult] = None

            if (
                self.phase4_enabled
                and self.consensus_selector is not None
                and self.consensus_escalation is not None
            ):
                try:
                    crisis_scores_for_consensus = {
                        name: signal.crisis_signal
                        for name, signal in ensemble_score.signals.items()
                    }

                    consensus_run_result = self.consensus_selector.select_and_run(
                        model_signals=crisis_scores_for_consensus,
                    )

                    if consensus_run_result is not None:
                        consensus_result_from_escalation = consensus_run_result

                        consensus_escalation_result = self.consensus_escalation.apply_floor(
                            pipeline_score=pipeline_score,
                            pipeline_severity=pipeline_severity,
                            consensus_score=consensus_run_result.crisis_score,
                            thresholds=self.scorer.get_thresholds(),
                        )

                        if consensus_escalation_result.triggered:
                            final_score = consensus_escalation_result.final_score
                            self._consensus_escalations += 1
                            logger.info(
                                f"🛡️ Consensus escalation applied: "
                                f"{pipeline_score:.3f} → {final_score:.3f}"
                            )

                except Exception as e:
                    logger.warning(f"⚠️ Consensus escalation failed (non-fatal): {e}")

            # Recalculate final severity (may have been updated by escalation)
            final_severity = CrisisSeverity.from_score(
                final_score, self.scorer.get_thresholds()
            )

            # Determine if review required
            requires_review = determine_requires_review(
                final_severity, vigil_response
            )

            # Step 6.4.3: Escalation also sets requires_review
            if (
                consensus_escalation_result is not None
                and consensus_escalation_result.triggered
                and self.consensus_escalation is not None
                and self.consensus_escalation.set_requires_review
            ):
                requires_review = True

            # Update ensemble_score
            ensemble_score.crisis_score = final_score
            ensemble_score.severity = final_severity
            ensemble_score.crisis_detected = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
                CrisisSeverity.MEDIUM,
            )
            ensemble_score.requires_intervention = final_severity in (
                CrisisSeverity.CRITICAL,
                CrisisSeverity.HIGH,
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

                # v5.1-6-6.4.3: Consensus was already run in the escalation
                # block above. Use the stored result for aggregation.
                consensus_result = consensus_result_from_escalation

                # Run conflict detection (informational only — does not modify scores)
                if self.conflict_detector:
                    model_signals = ModelSignals.from_ensemble_signals(signals_dict)
                    conflict_report = self.conflict_detector.detect_conflicts(
                        model_signals=model_signals,
                        crisis_scores=crisis_scores,
                    )

                    if conflict_report.has_conflicts:
                        self._conflicts_detected += 1

                # v5.1-6-6.4-2: Conflict resolution DISABLED (async path).

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
                if (
                    include_explanation
                    and self.explainability_generator
                    and aggregated_result
                ):
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

            # =========================================================
            # Phase 5: Context History Analysis (Async)
            # =========================================================

            context_analysis_result: Optional[ContextAnalysisResult] = None

            if (
                self.phase5_enabled
                and include_context_analysis
                and self.context_analyzer
            ):
                try:
                    # Convert message history to MessageHistoryItem objects
                    history_items: List[MessageHistoryItem] = []
                    if message_history:
                        for item in message_history:
                            history_items.append(MessageHistoryItem.from_dict(item))

                    # Run context analysis with current message score
                    context_analysis_result = self.context_analyzer.analyze(
                        current_message=message,
                        current_score=final_score,
                        message_history=history_items,
                    )

                    logger.debug(
                        f"Context analysis (async): escalation={context_analysis_result.escalation.detected}, "
                        f"trend={context_analysis_result.trend.direction}, "
                        f"urgency={context_analysis_result.intervention.urgency}"
                    )

                except Exception as e:
                    logger.error(f"Context analysis failed (async): {e}")
                    # Continue without context analysis - non-critical failure

            # Build assessment
            assessment = self._build_assessment_enhanced(
                ensemble_score=ensemble_score,
                results=results,
                message=message,
                processing_time_ms=processing_time_ms,
                vigil_response=vigil_response,
                requires_review=requires_review,
                consensus_result=consensus_result,
                conflict_report=conflict_report,
                resolution_result=resolution_result,
                aggregated_result=aggregated_result,
                explanation=explanation,
                context_analysis_result=context_analysis_result,
                irony_gate_result=irony_gate_result,
                consensus_escalation_result=consensus_escalation_result,
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
                await self._alerter.alert_model_failure(
                    "bart", str(e), is_critical=True
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

    # =========================================================================
    # Inference Methods (delegated to inference.py in Step 6.4.3)
    # =========================================================================

    def _run_sequential_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run sequential inference with per-model timing."""
        return run_sequential_inference(message, self.model_loader, self.fallback)

    def _run_parallel_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run parallel inference with per-model timing."""
        return run_parallel_inference(message, self.model_loader, self.fallback)

    async def _run_async_parallel_inference_with_timing(
        self, message: str
    ) -> tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
        """Run async parallel inference with per-model timing."""
        return await run_async_parallel_inference(
            message, self.model_loader, self.fallback, self._executor
        )

    # =========================================================================
    # Assessment Building
    # =========================================================================

    def _build_assessment_enhanced(
        self,
        ensemble_score: EnsembleScore,
        results: Dict[str, Optional[ModelResult]],
        message: str,
        processing_time_ms: float,
        vigil_response: VigilResponse,
        requires_review: bool,
        consensus_result: Optional[ConsensusResult] = None,
        conflict_report: Optional[ConflictReport] = None,
        resolution_result: Optional[ResolutionResult] = None,
        aggregated_result: Optional[AggregatedResult] = None,
        explanation: Optional[Explanation] = None,
        context_analysis_result: Optional[ContextAnalysisResult] = None,
        irony_gate_result: Optional[IronyGateResult] = None,
        consensus_escalation_result: Optional[ConsensusEscalationResult] = None,
    ) -> CrisisAssessment:
        """
        Build CrisisAssessment with Phase 3 Vigil, Phase 4, Phase 5, and Phase 6 enhancements.

        Args:
            ensemble_score: Calculated ensemble score (with Vigil-amplified crisis_score)
            results: Model results
            message: Original message
            processing_time_ms: Processing time
            vigil_response: Phase 3 Vigil response
            requires_review: Phase 3 Vigil requires_review flag
            consensus_result: Phase 4 consensus result
            conflict_report: Phase 4 conflict report
            resolution_result: Phase 4 resolution result
            aggregated_result: Phase 4 aggregated result
            explanation: Phase 4 explanation
            context_analysis_result: Phase 5 context analysis result
            irony_gate_result: Phase 6 irony gatekeeper result

        Returns:
            Complete CrisisAssessment with all phase data
        """
        # v5.1-6-6.4-2: Always use ensemble pipeline score. The resolved_score
        # from Phase 4 conflict resolution is no longer used because the v5.1
        # ensemble → Vigil → irony gate pipeline already produces the
        # authoritative final score. Consensus/resolution score overrides
        # were causing score↔severity mismatches.
        final_crisis_score = ensemble_score.crisis_score

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

        # Check if review required (from Phase 4 as well)
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
            requires_intervention=ensemble_score.requires_intervention
            or requires_review,
            requires_review=requires_review,
            recommended_action=recommended_action,
            signals=signals,
            processing_time_ms=processing_time_ms,
            models_used=models_used,
            is_degraded=self.fallback.is_degraded(),
            degradation_reason=self.fallback.get_degradation_reason(),
            message=message,
            # Phase 3 Vigil fields
            vigil=vigil_response,
            # Phase 4 fields
            explanation=explanation.to_dict() if explanation else None,
            conflict_report=conflict_report.to_dict() if conflict_report else None,
            consensus_result=consensus_result.to_dict() if consensus_result else None,
            aggregated_result=aggregated_result,
            # Phase 5 fields
            context_analysis=context_analysis_result,
            # Phase 6 fields
            irony_gate_result=irony_gate_result,
            # Step 6.4.3 fields
            consensus_escalation_result=consensus_escalation_result,
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

    def warmup(self, sample_text: str = "Hello, how are you today?") -> WarmupResult:
        """
        Warm up the engine with a sample analysis (FE-004 Enhanced).

        Phase 3.7.1: Model warmup on startup.
        Phase 6 FE-004: Enhanced with WarmupResult tracking.

        Note: Alerting and Vigil are disabled during warmup to prevent spurious notifications.

        Args:
            sample_text: Text to use for warmup

        Returns:
            WarmupResult with detailed timing and status information
        """
        logger.info("🔥 Warming up Decision Engine...")
        start_time = time.perf_counter()

        # Temporarily disable alerting during warmup
        original_alerter = None
        if self.conflict_resolver:
            original_alerter = self.conflict_resolver._alerter
            self.conflict_resolver._alerter = None

        # Temporarily disable Vigil during warmup
        original_vigil_enabled = self.vigil_enabled
        self.vigil_enabled = False

        try:
            # Run warmup analysis (bypass cache, no explanations)
            # Use sequential inference to get accurate per-model timing
            results, per_model_latency = self._run_sequential_inference_with_timing(
                sample_text
            )

            total_latency_ms = (time.perf_counter() - start_time) * 1000
            models_warmed = list(results.keys())

            if "bart" in results and results["bart"] is not None:
                warmup_result = WarmupResult(
                    success=True,
                    total_latency_ms=total_latency_ms,
                    per_model_latency_ms=per_model_latency,
                    models_warmed=models_warmed,
                )

                # Store warmup result for status reporting
                self._warmup_result = warmup_result

                logger.info(
                    f"✅ Engine warmed up (total: {total_latency_ms:.1f}ms, "
                    f"models: {len(models_warmed)})"
                )
                for model, latency in per_model_latency.items():
                    logger.debug(f"   {model}: {latency:.1f}ms")

                return warmup_result
            else:
                warmup_result = WarmupResult(
                    success=False,
                    total_latency_ms=total_latency_ms,
                    per_model_latency_ms=per_model_latency,
                    models_warmed=models_warmed,
                    error="BART model did not return valid result",
                )
                self._warmup_result = warmup_result
                logger.warning("⚠️ Warmup returned invalid result")
                return warmup_result

        except Exception as e:
            total_latency_ms = (time.perf_counter() - start_time) * 1000
            warmup_result = WarmupResult(
                success=False,
                total_latency_ms=total_latency_ms,
                error=str(e),
            )
            self._warmup_result = warmup_result
            logger.error(f"❌ Warmup failed: {e}")
            return warmup_result

        finally:
            # Restore alerter after warmup
            if self.conflict_resolver and original_alerter is not None:
                self.conflict_resolver._alerter = original_alerter

            # Restore Vigil after warmup
            self.vigil_enabled = original_vigil_enabled

    def get_warmup_result(self) -> Optional[WarmupResult]:
        """
        Get the last warmup result (FE-004).

        Returns:
            WarmupResult from last warmup, or None if never warmed up
        """
        return getattr(self, "_warmup_result", None)

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
    # Phase 3 Vigil Configuration Methods
    # =========================================================================

    def get_vigil_config(self) -> Dict[str, Any]:
        """
        Get current Vigil configuration.

        Returns:
            Vigil configuration dictionary
        """
        return {
            "enabled": self.vigil_enabled,
            "client_enabled": self._vigil_client.enabled
            if self._vigil_client
            else False,
            "amplification": self._vigil_amplification_config,
            "client_health": self._vigil_client.get_health()
            if self._vigil_client
            else None,
        }

    def get_vigil_stats(self) -> Dict[str, Any]:
        """
        Get Vigil usage statistics.

        Returns:
            Vigil statistics dictionary
        """
        return {
            "calls": self._vigil_calls,
            "amplifications": self._vigil_amplifications,
            "amplification_rate": (
                self._vigil_amplifications / self._vigil_calls
                if self._vigil_calls > 0
                else 0.0
            ),
        }

    def reset_vigil_circuit(self) -> None:
        """
        Manually reset the Vigil circuit breaker.

        Useful for administrative recovery after fixing Vigil issues.
        """
        if self._vigil_client:
            self._vigil_client.reset_circuit()
            logger.info("Vigil circuit breaker reset via engine")

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
    # Phase 5 Configuration Methods
    # =========================================================================

    def get_context_config(self) -> Optional[Dict[str, Any]]:
        """
        Get current context analysis configuration.

        Returns:
            Context configuration dictionary or None if disabled
        """
        if self.context_analyzer and self.phase5_enabled:
            return {
                "enabled": self.context_analyzer.is_enabled(),
                "max_history_size": self.context_analyzer.get_max_history_size(),
            }
        return None

    def is_context_analysis_enabled(self) -> bool:
        """
        Check if context analysis is enabled.

        Returns:
            True if Phase 5 and context analyzer are enabled
        """
        if self.phase5_enabled and self.context_analyzer:
            return self.context_analyzer.is_enabled()
        return False

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
            self._cache_hits / self._total_requests if self._total_requests > 0 else 0.0
        )

        status = {
            "is_ready": self.is_ready(),
            "is_degraded": self.fallback.is_degraded(),
            "degradation_reason": self.fallback.get_degradation_reason(),
            "async_inference": self.async_inference,
            "cache_enabled": self.cache_enabled,
            "vigil_enabled": self.vigil_enabled,
            "phase4_enabled": self.phase4_enabled,
            "phase5_enabled": self.phase5_enabled,
            "stats": {
                "total_requests": self._total_requests,
                "crisis_detections": self._crisis_detections,
                "conflicts_detected": self._conflicts_detected,
                "cache_hits": self._cache_hits,
                "cache_hit_rate": round(cache_hit_rate, 4),
                "average_latency_ms": round(avg_latency, 2),
                "vigil_calls": self._vigil_calls,
                "vigil_amplifications": self._vigil_amplifications,
                "vigil_confidence_skips": self._vigil_confidence_skips,
                "consensus_escalations": self._consensus_escalations,
            },
            "models": self.model_loader.get_status(),
            "weights": self.scorer.get_weights(),
            "thresholds": self.scorer.get_thresholds(),
            "fallback": self.fallback.get_status(),
            "cache": self.get_cache_stats(),
        }

        # Add Phase 3 Vigil component status
        if self.vigil_enabled:
            status["vigil"] = self.get_vigil_config()

        # Add Phase 4 component status
        if self.phase4_enabled:
            status["phase4"] = {
                "consensus": self.get_consensus_config(),
                "conflict_detection": self.get_conflict_config(),
                "conflict_resolution": (
                    self.conflict_resolver.get_config()
                    if self.conflict_resolver
                    else None
                ),
                "explainability": (
                    self.explainability_generator.get_config()
                    if self.explainability_generator
                    else None
                ),
            }

        # Add Phase 5 component status
        if self.phase5_enabled:
            status["phase5"] = {
                "context_analysis": self.get_context_config(),
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
        vigil_healthy = False
        if self.vigil_enabled and self._vigil_client:
            vigil_healthy = self._vigil_client.status not in (
                VigilStatus.CIRCUIT_OPEN,
                VigilStatus.UNAVAILABLE,
            )

        return {
            "status": "healthy" if self.is_ready() else "unhealthy",
            "ready": self.is_ready(),
            "degraded": self.fallback.is_degraded(),
            "models_loaded": self.model_loader._models_loaded,
            "total_models": len(self.model_loader._models),
            "cache_enabled": self.cache_enabled,
            "vigil_enabled": self.vigil_enabled,
            "vigil_healthy": vigil_healthy,
            "phase4_enabled": self.phase4_enabled,
            "phase5_enabled": self.phase5_enabled,
            "context_analysis_enabled": self.is_context_analysis_enabled(),
        }


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.2.3 Compliance (Rule #1)
# =============================================================================


def create_decision_engine(
    config_manager: Optional["ConfigManager"] = None,
    auto_initialize: bool = False,
    async_inference: bool = True,
    cache_enabled: bool = True,
    alerter: Optional["DiscordAlerter"] = None,
    vigil_enabled: bool = True,
    phase4_enabled: bool = True,
    phase5_enabled: bool = True,
) -> EnsembleDecisionEngine:
    """
    Factory function for EnsembleDecisionEngine.

    Creates a fully configured decision engine with Phase 3 Vigil,
    Phase 4, and Phase 5 enhancements.

    Args:
        config_manager: Configuration manager instance
        auto_initialize: If True, load models immediately
        async_inference: Enable parallel model inference
        cache_enabled: Enable response caching
        alerter: Discord alerter for notifications
        vigil_enabled: Enable Phase 3 Vigil integration (default: True)
        phase4_enabled: Enable Phase 4 features (default: True)
        phase5_enabled: Enable Phase 5 context analysis (default: True)

    Returns:
        Configured EnsembleDecisionEngine instance

    Example:
        >>> engine = create_decision_engine(config_manager=config)
        >>> engine.initialize()
        >>> assessment = engine.analyze(
        ...     "I'm feeling really down today",
        ...     message_history=[...],  # Phase 5 context
        ... )
        >>> print(assessment.vigil)  # Phase 3 Vigil response
        >>> print(assessment.explanation)  # Phase 4 explanation
        >>> print(assessment.context_analysis)  # Phase 5 analysis
    """
    # Get settings from config
    perf_config = {}
    if config_manager is not None:
        perf_config = config_manager.get_performance_config() or {}
        async_inference = perf_config.get("async_inference", async_inference)
        cache_enabled = perf_config.get("cache_enabled", cache_enabled)

        # Check if Vigil is enabled in config
        vigil_config = config_manager.get_section("vigil") or {}
        vigil_enabled = vigil_config.get("enabled", vigil_enabled)

    cache_ttl = perf_config.get("cache_ttl", 300.0)
    cache_max_size = perf_config.get("cache_max_size", 1000)

    engine = EnsembleDecisionEngine(
        config_manager=config_manager,
        async_inference=async_inference,
        cache_enabled=cache_enabled,
        cache_ttl=cache_ttl,
        cache_max_size=cache_max_size,
        alerter=alerter,
        vigil_enabled=vigil_enabled,
        phase4_enabled=phase4_enabled,
        phase5_enabled=phase5_enabled,
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
    "WarmupResult",
    "VigilResponse",  # Phase 3 Vigil
]
