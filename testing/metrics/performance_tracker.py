"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community

Performance Tracker - System Metrics
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: v5.0 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import time
import logging
from typing import Optional, Callable, Any, Tuple, Dict
from contextlib import contextmanager

try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """
    Track system performance metrics during model evaluation

    Responsibilities:
    - Measure execution latency
    - Track GPU VRAM usage
    - Monitor CPU usage
    - Generate performance reports

    Clean Architecture v5.0 Compliance:
    - Factory function pattern
    - Real system metrics (no mocks per Rule #8)
    """

    def __init__(self):
        """Initialize PerformanceTracker"""
        self.has_gpu = HAS_TORCH and torch.cuda.is_available()
        self.has_psutil = HAS_PSUTIL

        if not self.has_psutil:
            logger.warning("psutil not installed - CPU metrics unavailable")

        logger.info(
            f"PerformanceTracker v5.0 initialized "
            f"(GPU: {self.has_gpu}, CPU tracking: {self.has_psutil})"
        )

    def measure_latency(self, func: Callable, *args, **kwargs) -> Tuple[Any, float]:
        """
        Measure function execution time

        Args:
            func: Function to measure
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Tuple of (function result, latency in milliseconds)
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        latency_ms = (end_time - start_time) * 1000

        return result, latency_ms

    @contextmanager
    def track_latency(self):
        """
        Context manager for tracking latency

        Usage:
            with tracker.track_latency() as timer:
                # do work
            latency_ms = timer.elapsed_ms()
        """
        timer = _LatencyTimer()
        yield timer
        timer.stop()

    def get_vram_usage(self) -> float:
        """
        Get current GPU VRAM usage in MB

        Returns:
            VRAM usage in MB, or 0.0 if GPU unavailable
        """
        if not self.has_gpu:
            return 0.0

        try:
            allocated = torch.cuda.memory_allocated(0) / (1024 * 1024)  # Convert to MB
            return allocated
        except Exception as e:
            logger.error(f"Error getting VRAM usage: {e}")
            return 0.0

    def get_vram_reserved(self) -> float:
        """
        Get reserved GPU VRAM in MB

        Returns:
            Reserved VRAM in MB, or 0.0 if GPU unavailable
        """
        if not self.has_gpu:
            return 0.0

        try:
            reserved = torch.cuda.memory_reserved(0) / (1024 * 1024)  # Convert to MB
            return reserved
        except Exception as e:
            logger.error(f"Error getting reserved VRAM: {e}")
            return 0.0

    def get_gpu_memory_stats(self) -> Dict:
        """
        Get comprehensive GPU memory statistics

        Returns:
            Dictionary with GPU memory stats
        """
        if not self.has_gpu:
            return {
                "available": False,
                "allocated_mb": 0.0,
                "reserved_mb": 0.0,
                "free_mb": 0.0,
            }

        try:
            allocated = torch.cuda.memory_allocated(0) / (1024 * 1024)
            reserved = torch.cuda.memory_reserved(0) / (1024 * 1024)
            total = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
            free = total - allocated

            return {
                "available": True,
                "device_name": torch.cuda.get_device_name(0),
                "allocated_mb": allocated,
                "reserved_mb": reserved,
                "free_mb": free,
                "total_mb": total,
                "utilization_percent": (allocated / total * 100) if total > 0 else 0.0,
            }
        except Exception as e:
            logger.error(f"Error getting GPU memory stats: {e}")
            return {"available": False, "error": str(e)}

    def get_cpu_usage(self) -> float:
        """
        Get current CPU usage percentage

        Returns:
            CPU usage percentage (0-100), or 0.0 if psutil unavailable
        """
        if not self.has_psutil:
            return 0.0

        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception as e:
            logger.error(f"Error getting CPU usage: {e}")
            return 0.0

    def get_memory_usage(self) -> Dict:
        """
        Get system RAM usage

        Returns:
            Dictionary with RAM usage stats
        """
        if not self.has_psutil:
            return {"available": False, "used_mb": 0.0, "total_mb": 0.0, "percent": 0.0}

        try:
            mem = psutil.virtual_memory()
            return {
                "available": True,
                "used_mb": mem.used / (1024 * 1024),
                "total_mb": mem.total / (1024 * 1024),
                "percent": mem.percent,
                "available_mb": mem.available / (1024 * 1024),
            }
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return {"available": False, "error": str(e)}

    def generate_performance_report(
        self, latencies: List[float], vram_usages: Optional[List[float]] = None
    ) -> Dict:
        """
        Generate comprehensive performance report

        Args:
            latencies: List of latency measurements in milliseconds
            vram_usages: Optional list of VRAM measurements in MB

        Returns:
            Performance report dictionary
        """
        if not latencies:
            return {"error": "No latency data provided"}

        # Calculate latency statistics
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)

        # Calculate percentiles
        sorted_latencies = sorted(latencies)
        p50_idx = int(len(sorted_latencies) * 0.50)
        p95_idx = int(len(sorted_latencies) * 0.95)
        p99_idx = int(len(sorted_latencies) * 0.99)

        report = {
            "latency": {
                "avg_ms": avg_latency,
                "min_ms": min_latency,
                "max_ms": max_latency,
                "p50_ms": sorted_latencies[p50_idx],
                "p95_ms": sorted_latencies[p95_idx],
                "p99_ms": sorted_latencies[p99_idx],
                "total_samples": len(latencies),
            }
        }

        # Add VRAM statistics if available
        if vram_usages:
            avg_vram = sum(vram_usages) / len(vram_usages)
            min_vram = min(vram_usages)
            max_vram = max(vram_usages)

            report["vram"] = {
                "avg_mb": avg_vram,
                "min_mb": min_vram,
                "max_mb": max_vram,
                "peak_mb": max_vram,
            }

        # Add current system stats
        report["system"] = {
            "gpu_memory": self.get_gpu_memory_stats(),
            "ram": self.get_memory_usage(),
            "cpu_percent": self.get_cpu_usage(),
        }

        return report

    def clear_gpu_cache(self):
        """Clear GPU cache to free memory"""
        if self.has_gpu:
            try:
                torch.cuda.empty_cache()
                logger.info("GPU cache cleared")
            except Exception as e:
                logger.error(f"Error clearing GPU cache: {e}")


class _LatencyTimer:
    """Internal timer class for context manager"""

    def __init__(self):
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        """Stop the timer"""
        self.end_time = time.time()

    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds"""
        end = self.end_time if self.end_time else time.time()
        return (end - self.start_time) * 1000


# ============================================================================
# FACTORY FUNCTION - Clean Architecture v5.0 Compliance
# ============================================================================


def create_performance_tracker() -> PerformanceTracker:
    """
    Factory function for PerformanceTracker (Clean Architecture v5.0 Pattern)

    Returns:
        PerformanceTracker instance
    """
    return PerformanceTracker()


# ============================================================================
# Export public interface
# ============================================================================

__all__ = ["PerformanceTracker", "create_performance_tracker"]

logger.info("PerformanceTracker v5.0 loaded")
