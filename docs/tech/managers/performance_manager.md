<!-- ash-nlp/docs/tech/managers/performance_manager.md -->
<!--
Performance Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE:Compliant
-->
# Performance Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# Performance Manager Documentation

The Performance Manager handles performance optimization configuration for the Ash-NLP crisis detection system.

---

## Overview

Performance Manager provides centralized configuration for performance optimization features, caching strategies, and resource management, directly supporting the dramatic performance improvements that enable sub-200ms crisis detection response times.

### Core Responsibilities
- **Performance optimization configuration** - Controls performance enhancement features and settings
- **Caching strategy management** - Configures analysis result caching and model caching
- **Resource allocation control** - Manages CPU, memory, and GPU resource utilization
- **Throughput optimization** - Configures batch processing and concurrent analysis capabilities
- **Response time monitoring** - Tracks and optimizes crisis detection response times

---

## Manager Interface

### Factory Function
```python
def create_performance_config_manager(unified_config: UnifiedConfigManager) -> PerformanceConfigManager
```

### Core Methods
- `get_performance_config()` - Retrieves current performance optimization configuration
- `get_caching_config()` - Gets caching strategy and settings
- `get_resource_limits()` - Retrieves resource allocation limits and preferences
- `is_optimization_enabled(optimization_name: str)` - Checks if specific optimization is enabled
- `get_batch_processing_config()` - Gets batch processing and concurrency settings
- `update_performance_setting(setting: str, value: any)` - Runtime performance tuning

---

## Configuration Structure

### JSON Configuration (`config/performance_settings.json`)
```json
{
    "optimizations": {
        "synchronous_analysis": true,
        "lazy_loading": true,
        "configuration_caching": true,
        "model_preloading": true,
        "batch_processing": false
    },
    "caching": {
        "analysis_results": {
            "enabled": true,
            "ttl_seconds": 300,
            "max_entries": 1000
        },
        "model_outputs": {
            "enabled": true,
            "ttl_seconds": 600,
            "max_entries": 500
        },
        "pattern_matches": {
            "enabled": true,
            "ttl_seconds": 900,
            "max_entries": 2000
        }
    },
    "resource_limits": {
        "max_concurrent_analyses": 10,
        "memory_threshold_mb": 4096,
        "gpu_memory_threshold_mb": 8192,
        "cpu_thread_pool_size": 8
    },
    "response_targets": {
        "cold_start_ms": 1000,
        "operational_ms": 200,
        "batch_timeout_ms": 5000
    }
}
```

### Environment Variable Overrides
- `ASH_PERF_SYNC_ANALYSIS` - Override synchronous analysis setting
- `ASH_PERF_LAZY_LOADING` - Override lazy loading optimization
- `ASH_PERF_CACHE_ENABLED` - Override caching enablement
- `ASH_PERF_MAX_CONCURRENT` - Override maximum concurrent analyses
- `ASH_PERF_RESPONSE_TARGET_MS` - Override operational response time target

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - Performance monitoring utilities and resource management

### Used By
- **CrisisAnalyzer** - Performance optimization settings for crisis detection
- **ModelCoordinationManager** - AI model performance and resource management
- **Analysis Performance Module** - Direct integration with performance optimizations
- **API Endpoints** - Response time targets and throughput configuration

---

## Performance Monitoring

### Response Time Tracking
- **Cold start monitoring** - Tracks initial system startup performance
- **Operational response tracking** - Monitors ongoing crisis detection response times
- **Performance regression detection** - Alerts when performance degrades beyond thresholds
- **Resource utilization monitoring** - Tracks CPU, memory, and GPU usage patterns

### Optimization Effectiveness
- **Before/after comparison** - Compares performance with and without optimizations
- **Feature impact analysis** - Measures individual optimization feature effectiveness
- **Resource efficiency metrics** - Tracks resource usage efficiency improvements
- **Community impact measurement** - Monitors real-world crisis detection performance

---

## Error Handling and Resilience

### Graceful Degradation
- **Optimization failures** - Falls back to baseline performance if optimizations fail
- **Caching errors** - Continues operation without caching if cache systems fail
- **Resource exhaustion** - Gracefully handles memory and CPU resource limits
- **Performance degradation** - Adjusts optimization settings under resource pressure

### Production Safety
- **Conservative defaults** - Safe performance settings that never compromise crisis detection
- **Automatic resource scaling** - Adjusts resource usage based on available system resources
- **Performance monitoring** - Continuous monitoring ensures performance targets are maintained
- **Emergency fallback modes** - Simplified processing modes for critical resource situations

---

*Performance Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
