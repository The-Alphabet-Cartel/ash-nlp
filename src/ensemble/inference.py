"""
============================================================================
Ash-NLP: Crisis Detection NLP Server
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Analyze  → Process messages through multi-model ensemble classification
    Detect   → Identify crisis signals with weighted consensus algorithms
    Explain  → Provide human-readable explanations for all decisions
    Protect  → Safeguard our LGBTQIA+ community through accurate detection

============================================================================
Inference Runner Functions for Ensemble Decision Engine

Standalone functions for running model inference with timing:
- run_sequential_inference: Sequential model execution
- run_parallel_inference: ThreadPoolExecutor parallel execution
- run_async_parallel_inference: asyncio.gather parallel execution
----------------------------------------------------------------------------
FILE VERSION: v5.1-6-6.4.3-1
LAST MODIFIED: 2026-02-18
PHASE: Phase 7 - Figurative Language Gate
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================
"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, Tuple

from src.models import ModelResult

from .model_loader import ModelLoader
from .fallback import FallbackStrategy

# Module version
__version__ = "v5.1-6-6.4.3-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Sequential Inference
# =============================================================================


def run_sequential_inference(
    message: str,
    model_loader: ModelLoader,
    fallback: FallbackStrategy,
) -> Tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
    """
    Run sequential inference with per-model timing.

    Executes each model one at a time, tracking latency per model.
    Used when async inference is disabled.

    Args:
        message: Text message to analyze
        model_loader: ModelLoader instance for accessing models
        fallback: FallbackStrategy for circuit breaker checks

    Returns:
        Tuple of (model_results, per_model_latencies)
    """
    results: Dict[str, Optional[ModelResult]] = {}
    latencies: Dict[str, float] = {}
    model_names = ["bart", "sentiment", "emotions", "figurative"]

    for model_name in model_names:
        if fallback.can_call_model(model_name):
            model_start = time.perf_counter()
            try:
                model = model_loader.get_model(model_name)
                if model:
                    results[model_name] = model.analyze(message)
                    fallback.handle_model_success(model_name)
            except Exception as e:
                fallback.handle_model_failure(model_name, str(e))
            finally:
                latencies[model_name] = (time.perf_counter() - model_start) * 1000

    return results, latencies


# =============================================================================
# Parallel Inference (ThreadPoolExecutor)
# =============================================================================


def run_parallel_inference(
    message: str,
    model_loader: ModelLoader,
    fallback: FallbackStrategy,
) -> Tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
    """
    Run parallel inference with per-model timing using ThreadPoolExecutor.

    Executes all models concurrently in a thread pool.
    Used by the sync analyze() method when async_inference is enabled.

    Args:
        message: Text message to analyze
        model_loader: ModelLoader instance for accessing models
        fallback: FallbackStrategy for circuit breaker checks

    Returns:
        Tuple of (model_results, per_model_latencies)
    """
    results: Dict[str, Optional[ModelResult]] = {}
    latencies: Dict[str, float] = {}

    def run_model(model_name: str) -> tuple:
        if not fallback.can_call_model(model_name):
            return (model_name, None, 0.0)

        model_start = time.perf_counter()
        try:
            model = model_loader.get_model(model_name)
            if model:
                result = model.analyze(message)
                fallback.handle_model_success(model_name)
                latency = (time.perf_counter() - model_start) * 1000
                return (model_name, result, latency)
            return (model_name, None, 0.0)
        except Exception as e:
            fallback.handle_model_failure(model_name, str(e))
            latency = (time.perf_counter() - model_start) * 1000
            return (model_name, None, latency)

    model_names = ["bart", "sentiment", "emotions", "figurative"]

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


# =============================================================================
# Async Parallel Inference (asyncio.gather)
# =============================================================================


async def run_async_parallel_inference(
    message: str,
    model_loader: ModelLoader,
    fallback: FallbackStrategy,
    executor: Optional[ThreadPoolExecutor] = None,
) -> Tuple[Dict[str, Optional[ModelResult]], Dict[str, float]]:
    """
    Run async parallel inference with per-model timing using asyncio.gather.

    Executes all models concurrently via asyncio, offloading blocking
    model.analyze() calls to a thread pool executor.
    Used by the async analyze_async() method (Phase 3.7.2).

    Args:
        message: Text message to analyze
        model_loader: ModelLoader instance for accessing models
        fallback: FallbackStrategy for circuit breaker checks
        executor: ThreadPoolExecutor for offloading blocking calls

    Returns:
        Tuple of (model_results, per_model_latencies)
    """
    loop = asyncio.get_event_loop()

    async def run_model_async(model_name: str) -> tuple:
        if not fallback.can_call_model(model_name):
            return (model_name, None, 0.0)

        model_start = time.perf_counter()
        try:
            model = model_loader.get_model(model_name)
            if model:
                result = await loop.run_in_executor(
                    executor,
                    model.analyze,
                    message,
                )
                fallback.handle_model_success(model_name)
                latency = (time.perf_counter() - model_start) * 1000
                return (model_name, result, latency)
            return (model_name, None, 0.0)
        except Exception as e:
            fallback.handle_model_failure(model_name, str(e))
            logger.warning(f"Model {model_name} failed: {e}")
            latency = (time.perf_counter() - model_start) * 1000
            return (model_name, None, latency)

    model_names = ["bart", "sentiment", "emotions", "figurative"]
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


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "run_sequential_inference",
    "run_parallel_inference",
    "run_async_parallel_inference",
]
