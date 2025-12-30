<!-- ash-nlp/docs/tech/managers/zero_shot.md -->
<!--
Zero Shot Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Zero Shot Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# ZeroShotManager Documentation

The **ZeroShotManager** handles zero-shot classification AI model management and coordination for the Ash-NLP crisis detection system, implementing the primary semantic analysis component of the crisis detection pipeline as defined in the Core System Vision.

---

## Overview

**ZeroShotManager** provides centralized management of zero-shot classification models, implementing the **FIRST** component of Ash-NLP's crisis detection approach: "Uses Zero-Shot AI models for primary semantic classification." This manager coordinates AI model loading, inference, and optimization for rapid crisis detection.

### Core Responsibilities
- **Zero-shot model management** - Loading, initialization, and lifecycle management of AI classification models
- **Primary semantic classification** - Core AI-powered crisis detection using zero-shot classification
- **Model inference coordination** - Efficient AI model inference with performance optimization
- **Model result interpretation** - Processing and formatting AI model outputs for crisis analysis
- **GPU resource management** - Optimal utilization of NVIDIA RTX 3060 12GB GPU resources

### Phase 3e Consolidation Impact
- **Configuration pattern standardization** - Now uses `get_config_section()` for all configuration access
- **Integration with SharedUtilitiesManager** - Leverages shared AI model utilities and validation
- **Performance optimization compatibility** - AI model management optimized for 74% performance improvement with synchronous processing

---

## Manager Interface

### Factory Function
```python
def create_zero_shot_manager(unified_config: UnifiedConfigManager) -> ZeroShotManager
```

### Core Methods
- `load_models()` - Loads and initializes zero-shot classification models
- `classify_text(text: str, labels: list)` - Performs zero-shot classification on input text
- `get_model_info()` - Retrieves information about loaded models and capabilities
- `classify_crisis(text: str)` - Specialized crisis classification using pre-defined crisis labels
- `batch_classify(texts: list, labels: list)` - Efficient batch classification for multiple texts
- `get_model_performance()` - Retrieves model performance metrics and statistics

---

## Configuration Structure

### JSON Configuration (`config/zero_shot_config.json`)
```json
{
    "models": {
        "primary_model": {
            "name": "facebook/bart-large-mnli",
            "model_type": "zero-shot-classification",
            "cache_dir": "models/zero_shot/",
            "device": "cuda",
            "max_length": 1024
        },
        "backup_model": {
            "name": "microsoft/DialoGPT-medium",
            "model_type": "zero-shot-classification",
            "cache_dir": "models/zero_shot/",
            "device": "cpu",
            "max_length": 512
        }
    },
    "inference": {
        "batch_size": 8,
        "max_concurrent": 4,
        "timeout_seconds": 30,
        "retry_attempts": 3,
        "confidence_threshold": 0.1
    },
    "crisis_labels": [
        "suicide ideation",
        "self-harm thoughts",
        "severe depression",
        "panic attack",
        "abuse situation",
        "domestic violence",
        "mental health crisis",
        "emotional distress",
        "identity crisis",
        "family rejection"
    ],
    "performance": {
        "model_caching": true,
        "result_caching": true,
        "gpu_memory_fraction": 0.8,
        "synchronous_inference": true
    }
}
```

### Environment Variable Overrides
- `ASH_ZERO_SHOT_PRIMARY_MODEL` - Override primary model selection
- `ASH_ZERO_SHOT_DEVICE` - Override device selection (cuda/cpu)
- `ASH_ZERO_SHOT_BATCH_SIZE` - Override inference batch size
- `ASH_ZERO_SHOT_GPU_MEMORY_FRACTION` - Override GPU memory allocation
- `ASH_ZERO_SHOT_SYNC_INFERENCE` - Override synchronous inference setting

---

## AI Model Architecture

### Primary Model (BART-Large-MNLI)
- **Model**: Facebook's BART-Large fine-tuned on Multi-Genre Natural Language Inference
- **Purpose**: Primary zero-shot classification for crisis detection
- **Strengths**: Excellent semantic understanding, robust crisis pattern recognition
- **Device**: NVIDIA RTX 3060 GPU (CUDA acceleration)
- **Memory**: ~1.4GB GPU memory usage

### Backup Model Configuration
- **Fallback capability** - Automatic fallback to CPU-based models if GPU unavailable
- **Redundancy** - Multiple model options for system reliability
- **Performance scaling** - Different models for different performance requirements
- **Disaster recovery** - Ensures crisis detection continues under hardware failures

### LGBTQIA+ Community Optimization
- **Identity-aware classification** - Models trained to recognize LGBTQIA+ specific crisis indicators
- **Inclusive language understanding** - Specialized handling of community-specific terminology
- **Pronoun sensitivity** - Proper handling of diverse pronouns and gender expressions
- **Community context awareness** - Understanding of LGBTQIA+ community support structures

---

## Performance Optimization

### Phase 3e Performance Integration
- **Synchronous inference** - Eliminates async/sync overhead contributing to 40%+ performance gain
- **Model caching** - Pre-loaded models reduce inference latency
- **Result caching** - Caches classification results for similar inputs
- **GPU optimization** - Optimized GPU memory usage for NVIDIA RTX 3060

### Inference Optimization
- **Batch processing** - Efficient batch inference for multiple texts
- **Memory management** - Optimal GPU memory allocation and cleanup
- **Model warmup** - Pre-warmed models for consistent response times
- **Concurrent processing** - Safe concurrent inference within memory limits

---

## Crisis Detection Integration

### Core System Vision Implementation
Implements the **FIRST** component of the crisis detection pipeline:
1. **✅ FIRST: Uses Zero-Shot AI models for primary semantic classification**
2. SECOND: Enhances AI results with contextual pattern analysis (PatternDetectionManager)
3. FALLBACK: Uses pattern-only classification if AI models fail (CrisisAnalyzer)
4. PURPOSE: Detect crisis messages in Discord community communications

### Crisis Classification Process
```python
# Example crisis classification workflow
def classify_crisis_message(message: str) -> dict:
    # Primary zero-shot classification
    classification = zero_shot_manager.classify_crisis(message)
    
    # Enhanced with community context
    community_context = get_community_context(message)
    
    # Combined analysis result
    return {
        'ai_classification': classification,
        'confidence': classification['scores'][0],
        'crisis_type': classification['labels'][0],
        'community_context': community_context
    }
```

### Crisis Label Management
- **Pre-defined crisis labels** - Carefully curated set of crisis indicators
- **LGBTQIA+ specific labels** - Community-specific crisis patterns
- **Dynamic label expansion** - Ability to add new crisis categories
- **Label confidence scoring** - Confidence scores for each potential crisis type

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - AI model utilities, validation, and common processing functions

### Used By
- **CrisisAnalyzer** - Primary consumer of zero-shot classification results
- **ModelCoordinationManager** - Coordinates zero-shot models with other AI models
- **API Endpoints** - Direct access to classification capabilities for testing and admin functions
- **Learning System** - Provides training data and feedback for model improvement

---

## Error Handling and Resilience

### Model Loading Failures
- **Automatic model fallback** - Falls back to backup models if primary model fails to load
- **CPU fallback** - Automatic CPU fallback if GPU resources unavailable
- **Progressive degradation** - Reduced functionality rather than complete failure
- **Error logging** - Comprehensive logging of model loading issues

### Inference Failures
- **Retry mechanisms** - Automatic retry for transient inference failures
- **Timeout handling** - Graceful handling of inference timeouts
- **Memory management** - Automatic cleanup of GPU memory on failures
- **Fallback processing** - Alternative processing paths when AI models fail

### Production Safety
- **Conservative classification** - Bias toward detecting potential crises to ensure safety
- **Graceful degradation** - System continues operating with reduced AI capabilities
- **Resource monitoring** - Continuous monitoring of GPU memory and performance
- **Crisis detection continuity** - Ensures crisis detection never completely fails

---

## Community Features

### LGBTQIA+ Community Support
- **Identity-sensitive classification** - AI models trained to understand diverse identity expressions
- **Pronoun recognition** - Proper handling of diverse pronouns in crisis context
- **Community terminology** - Understanding of LGBTQIA+ community-specific language
- **Inclusive crisis detection** - Recognition of community-specific crisis indicators

### Privacy Protection
- **Data minimization** - Only processes text necessary for crisis detection
- **No model training on community data** - Uses pre-trained models to protect privacy
- **Secure inference** - All processing occurs on secure, community-controlled infrastructure
- **Audit capabilities** - Comprehensive logging for community safety auditing

---

## Testing and Validation

### Model Performance Testing
- **Crisis detection accuracy** - Regular testing of crisis detection accuracy
- **False positive/negative monitoring** - Continuous monitoring of classification errors
- **Community feedback integration** - Incorporates community feedback into model evaluation
- **Performance regression testing** - Ensures model updates don't degrade performance

### Integration Testing
- **Manager integration testing** - Tests integration with CrisisAnalyzer and other managers
- **GPU resource testing** - Tests GPU memory usage and performance under load
- **Fallback mechanism testing** - Tests automatic fallback to backup models and CPU processing
- **Concurrent inference testing** - Tests safe concurrent model inference

---

## Best Practices

### Model Selection
- **Primary model reliability** - Use well-tested, reliable models for primary classification
- **Backup model diversity** - Ensure backup models use different architectures for redundancy
- **Community testing** - Regular testing with LGBTQIA+ community feedback
- **Performance monitoring** - Continuous monitoring of model performance and accuracy

### Resource Management
- **GPU memory monitoring** - Regular monitoring of GPU memory usage and optimization
- **Model lifecycle management** - Proper loading, caching, and cleanup of AI models
- **Concurrent access control** - Safe concurrent access to AI models within resource limits
- **Performance profiling** - Regular profiling of inference performance and optimization opportunities

---

*Zero Shot Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
