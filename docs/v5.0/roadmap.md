# Ash-NLP v5.0 Complete Rewrite Roadmap

**Version**: v5.0  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## 📋 **TABLE OF CONTENTS**

1. [Executive Summary](#executive-summary)
2. [Architecture Decision](#architecture-decision)
3. [Model Selection](#model-selection)
4. [Project Phases](#project-phases)
5. [Phase Tracking](#phase-tracking)
6. [Dependencies & Prerequisites](#dependencies--prerequisites)
7. [Success Criteria](#success-criteria)
8. [Rollback Procedures](#rollback-procedures)

---

## 🎯 **EXECUTIVE SUMMARY**

### **Project Goal**
Complete rewrite of Ash-NLP from v3.1 to v5.0, implementing Local Multi-Model Ensemble architecture inspired by LLM Council principles while maintaining Clean Architecture Charter v5.0 compliance.

### **Key Changes**
- ✅ **Architecture**: Single model → Local Multi-Model Ensemble (Council-inspired)
- ✅ **Models**: Upgrade from generic zero-shot to specialized crisis detection models
- ✅ **Testing**: Implement comprehensive model evaluation framework
- ✅ **Context**: Add rolling window analysis for temporal pattern detection
- ✅ **Privacy**: Maintain 100% local processing (no external APIs)
- ✅ **Cost**: Maintain $0 ongoing costs (GPU-based, no API fees)

### **Non-Negotiables**
- ⚠️ **Latency**: Must remain < 5 seconds per analysis
- ⚠️ **Privacy**: All data stays on local server (10.20.30.253)
- ⚠️ **Clean Architecture**: 100% v5.0 Charter compliance
- ⚠️ **Availability**: 24/7 uptime for crisis detection
- ⚠️ **VRAM**: Must fit within 12GB RTX 3060 constraints

---

## 🏛️ **ARCHITECTURE DECISION**

### **Selected Approach: Local Multi-Model Ensemble (Option 3)**

**Rationale**:
```
┌─────────────────────────────────────────────────────────────────┐
│              Discord Message → CrisisAnalyzer                   │
├─────────────────────────────────────────────────────────────────┤
│  Local GPU Ensemble (4 models running in parallel)              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────┐  │
│  │ Model 1:     │ │ Model 2:     │ │ Model 3:     │ │Model 4:│  │
│  │ Crisis       │ │ Emotion      │ │ Sentiment    │ │Irony   │  │
│  │ Severity     │ │ Detection    │ │ Analysis     │ │Detect  │  │
│  │ (Zero-Shot)  │ │ (28 classes) │ │ (Pos/Neg/Neu)│ │(Sarc.) │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Consensus Coordinator (Council-inspired logic)                 │
│  - Cross-validation between models                              │
│  - Confidence weighting                                         │
│  - Disagreement detection                                       │
├─────────────────────────────────────────────────────────────────┤
│  Pattern Enhancement (existing functionality)                   │
│  - Temporal modifiers                                           │
│  - Contextual patterns                                          │
├─────────────────────────────────────────────────────────────────┤
│  Context Analyzer (NEW - rolling window)                        │
│  - User message history (last 5-10 messages)                    │
│  - Escalation detection                                         │
│  - Temporal trends                                              │
├─────────────────────────────────────────────────────────────────┤
│  Crisis Score + Alert Decision                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why This Approach**:
- ✅ **Latency**: 3-7 seconds (acceptable for crisis detection)
- ✅ **Privacy**: 100% local, no external APIs
- ✅ **Cost**: $0 ongoing (electricity only)
- ✅ **Accuracy**: Multi-model consensus reduces false positives/negatives
- ✅ **Council Benefits**: Cross-validation without external dependencies
- ✅ **VRAM Efficient**: ~1.5GB total (well within 12GB limit)

**Rejected Alternatives**:
- ❌ Full LLM Council: 30-90s latency unacceptable for crisis detection
- ❌ API-based ensemble: Privacy concerns + $10-150/day costs
- ❌ Single model upgrade: Less robust than ensemble approach

---

## 🎯 **MODEL SELECTION**

### **Old Models (v3.1)**
```
❌ Depression: MoritzLaurer/deberta-v3-base-zeroshot-v2.0
   - Downloads: 276K | Generic zero-shot, not depression-specific
   
❌ Sentiment: Lowerated/lm6-deberta-v3-topic-sentiment  
   - Downloads: Unknown | Low validation, unclear performance
   
❌ Distress: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
   - Downloads: 7.7M | Good but generic NLI, not distress-specific
```

### **New Model Ensemble (v5.0)**

#### **Model 1: Crisis Severity Classifier (Zero-Shot)**
```yaml
Model: facebook/bart-large-mnli
Downloads: 132.9M (457x more validated than current)
Likes: 1,507
Parameters: 407M
Task: Zero-shot classification with custom crisis labels
VRAM: ~800MB loaded
Latency: ~1-2 seconds

Crisis Labels:
  - "suicide ideation"
  - "self-harm thoughts"
  - "severe depression"
  - "panic attack"
  - "abuse situation"
  - "family rejection"
  - "identity crisis"
  - "mental health emergency"

Why: Industry standard, excellent semantic understanding, flexible labels
```

#### **Model 2: Emotion Detection (28 Classes)**
```yaml
Model: SamLowe/roberta-base-go_emotions
Downloads: 92.8M (most popular emotion detector)
Likes: 640
Parameters: 125M
Task: Multi-label emotion classification
VRAM: ~250MB loaded
Latency: ~0.5-1 second

Key Crisis Emotions:
  - sadness, grief, disappointment
  - fear, nervousness, confusion
  - remorse, disgust (toward self)
  - anger (internalized)

Why: 28 emotion classes provide granular emotional state analysis
Dataset: Google GoEmotions (highest quality emotion dataset)
```

#### **Model 3: Sentiment Analysis (Social Media Optimized)**
```yaml
Model: cardiffnlp/twitter-roberta-base-sentiment-latest
Downloads: 295.9M (most validated sentiment model)
Likes: 746
Parameters: 125M
Task: 3-class sentiment (Negative, Neutral, Positive)
VRAM: ~250MB loaded
Latency: ~0.3-0.5 seconds
Updated: 2025 (most recent)

Classes:
  - Negative (crisis indicator when high)
  - Neutral (context dependent)
  - Positive (reduces crisis score)

Why: Trained on Twitter (similar informal language to Discord)
Specialized: Social media language patterns
```

#### **Model 4: Irony/Sarcasm Detection (NEW)**
```yaml
Model: cardiffnlp/twitter-roberta-base-irony
Downloads: 71.1K
Likes: 29
Parameters: 125M
Task: Binary classification (Ironic / Not Ironic)
VRAM: ~250MB loaded
Latency: ~0.3-0.5 seconds

Critical Use Cases:
  - "I'm just great" (when actually in crisis)
  - "Best day ever" (sarcastic during depression)
  - "Love my life right now" (ironic statement)

Why: Prevents misclassification of sarcastic crisis messages as positive
Essential: LGBTQIA+ community often uses sarcasm to cope
```

### **Total Ensemble Resources**
```
Total VRAM: ~1.55GB (12.9% of 12GB available)
Total Parameters: ~782M
Expected Latency: 3-7 seconds for full ensemble analysis
Remaining VRAM: ~10.45GB for batch processing and caching
```

---

## 📊 **PROJECT PHASES**

### **Phase Dependency Map**
```
Phase 0: Foundation & Planning (Current)
    ↓
Phase 1: Testing Framework Setup ← Prerequisite for all model work
    ↓
Phase 2: Model Migration & Integration
    ↓
Phase 3: Ensemble Decision Engine / API Implementation
    ↓
Phase 4: History Analysis Integration
    ↓
Phase 5: Monitoring & Continuous Improvement
```

---

## 📝 **PHASE 0: FOUNDATION & PLANNING**

### **Status**: ✅ **COMPLETED** (2025-12-30)

### **Deliverables**:
- [x] Architecture decision documented (Local Multi-Model Ensemble)
- [x] Model selection finalized (4 models identified)
- [x] Roadmap created (this document)
- [x] Clean Architecture Charter v5.0 reviewed
- [x] Resource constraints validated (VRAM, latency, cost)

### **Decisions Made**:
1. ✅ Local ensemble approach selected over API-based council
2. ✅ Four-model ensemble composition finalized
3. ✅ Testing-first approach established
4. ✅ Privacy and cost constraints maintained

---

## 📝 **PHASE 1: TESTING FRAMEWORK SETUP**

### **Status**: ✅ **COMPLETED** (2025-12-30)

### **Duration**: 1-2 weeks
### **Priority**: CRITICAL (Prerequisite for all model work)

### **Objectives**:
- Create comprehensive model evaluation framework
- Build test datasets for crisis detection validation
- Establish baseline metrics with current models
- Implement automated model comparison tools

### **Clean Architecture Compliance**:
- ✅ All test classes use factory functions
- ✅ Configuration via JSON + environment variables
- ✅ Dependency injection for test managers
- ✅ File versioning headers on all test files
- ✅ Real-world testing (not mocks) per Rule #8

---

### **Step 1.1: Create Testing Directory Structure**

**Tasks**:
- [x] Create `testing/` directory in project root
- [x] Create `testing/model_evaluator.py` (main orchestrator)
- [x] Create `testing/test_datasets/` directory
- [x] Create `testing/metrics/` directory  
- [x] Create `testing/reports/` directory
- [x] Create `testing/config/` directory for test configuration

**Deliverables**:
- [x] Directory structure created and validated
- [x] `__init__.py` files in all directories
- [x] README.md in `testing/` explaining framework usage

---

### **Step 1.2: Create Test Dataset - Crisis Examples**

**Tasks**:
- [x] Create crisis_examples.json with 50+ test cases
- [x] Review with mental health crisis expert (if available)
- [x] Validate JSON structure and completeness
- [x] Document test case creation methodology

---

### **Step 1.3: Create Test Dataset - Safe Examples**

**Tasks**:
- [x] Create safe_examples.json with 50+ test cases
- [x] Include diverse false positive scenarios
- [x] Cover LGBTQIA+ positive language
- [x] Validate against crisis false positive triggers

---

### **Step 1.4: Create Test Dataset - Edge Cases**

**Tasks**:
- [x] Create edge_cases.json with 50+ challenging cases
- [x] Include heavy sarcasm examples
- [x] Cover ambiguous severity scenarios
- [x] Document expected model behavior on edge cases

---

### **Step 1.5: Create Test Dataset - LGBTQIA+ Specific**

**Tasks**:
- [x] Create lgbtqia_specific.json with 50+ cases
- [x] Get community feedback on test cases
- [x] Ensure cultural sensitivity and accuracy
- [x] Document community-specific patterns

---

### **Step 1.6: Create Test Dataset - Escalation Patterns**

**Tasks**:
- [x] Create escalation_patterns.json with 20+ sequences
- [x] Include various escalation speeds (rapid, gradual, sudden)
- [x] Define clear intervention points
- [x] Document expected context analyzer behavior

---

### **Step 1.7: Implement ModelEvaluator Class**

**Tasks**:
- [x] Implement ModelEvaluator class with factory function
- [x] Create test_config.json with environment overrides
- [x] Implement single test case execution
- [x] Implement dataset testing
- [x] Implement model comparison logic
- [x] Add VRAM and latency tracking
- [x] Create unit tests for ModelEvaluator
- [x] Document usage examples

---

### **Step 1.8: Implement Metrics Calculators**

**Tasks**:
- [x] Implement AccuracyCalculator with all metrics
- [x] Implement ConfusionMatrix with visualization
- [x] Implement PerformanceTracker for system metrics
- [x] Implement EnsembleAnalyzer for multi-model analysis
- [x] Create factory functions for all metrics classes
- [x] Add unit tests for each calculator
- [x] Document calculation methodologies

---

### **Step 1.9: Implement Report Generation**

**Tasks**:
- [x] Implement ModelComparisonReport class
- [x] Implement TestVisualization class
- [x] Implement JSON report export
- [x] Document report interpretation

---

### **Step 1.10: Baseline Current Models**

**Objective**: Establish performance baseline with current v3.1 models

**Tasks**:
- [x] Test MoritzLaurer/deberta-v3-base-zeroshot-v2.0
  - [x] Run against crisis_examples.json
  - [x] Run against safe_examples.json
  - [x] Run against edge_cases.json
  - [x] Record accuracy metrics
  - [x] Record performance metrics (latency, VRAM)

- [x] Test Lowerated/lm6-deberta-v3-topic-sentiment
  - [x] Run against all test datasets
  - [x] Record metrics

- [x] Test MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
  - [x] Run against all test datasets
  - [x] Record metrics

- [x] Generate baseline report
  - [x] Accuracy: Precision, Recall, F1 for each model
  - [x] Performance: Latency, VRAM usage
  - [x] False Positive Rate
  - [x] False Negative Rate
  - [x] Per-category performance

**Deliverables**:
- [x] Baseline performance report (JSON + HTML)
- [x] Identified weaknesses in current models
- [x] Target improvement areas for v5.0 models
- [x] Baseline report stored in `testing/reports/baselines/v3.1_baseline.json`

---

### **Step 1.11: Phase 1 Validation & Sign-Off**

**Phase 1 Complete Checklist**:

**Testing Framework**:
- [x] All directory structure created
- [x] All test dataset files created and validated
- [x] ModelEvaluator class implemented and tested
- [x] All metrics calculators implemented
- [x] Report generation working
- [x] Baseline testing completed

**Clean Architecture Compliance**:
- [x] All files have version headers
- [x] Factory functions used for all classes
- [x] Configuration via JSON + environment variables
- [x] Dependency injection implemented
- [x] No mocks used (real model testing)

**Documentation**:
- [x] Testing framework usage documented
- [x] Test dataset creation methodology documented
- [x] Baseline results documented
- [x] Known issues/limitations documented

**Success Criteria**:
- ✅ Can test any model against standardized datasets
- ✅ Can compare models objectively with metrics
- ✅ Baseline v3.1 performance documented
- ✅ Testing infrastructure ready for Phase 2 model migration

**Sign-Off Required**:
- [x] Project Lead approval
- [x] Testing framework validated
- [x] Baseline metrics accepted
- [x] Ready to proceed to Phase 2

---

## 📝 **PHASE 2: MODEL MIGRATION & INTEGRATION**

### **Status**: ✅ **COMPLETED** (2025-12-31)

### **Duration**: 2-3 weeks
### **Priority**: HIGH

### **Objectives**:
- Download and validate new model ensemble
- Create model loading and caching infrastructure
- Implement individual model wrappers
- Test each model independently against test datasets
- Validate VRAM and latency requirements met

---

### **Step 2.1: Create Model Management Infrastructure**

**Tasks**:
- [x] Implement ModelLoader class with factory function
- [x] Create model_config.json
- [x] Update .env.template with model variables
- [x] Implement model caching logic
- [x] Add model integrity validation
- [x] Create unit tests for ModelLoader
- [x] Document model download process

---

### **Step 2.2: Download and Validate Model 1 - Crisis Classifier**

**Model**: `facebook/bart-large-mnli`

**Tasks**:
- [x] Download model to cache directory
  ```python
  from transformers import pipeline
  
  model = pipeline(
      "zero-shot-classification",
      model="facebook/bart-large-mnli",
      device=0  # GPU
  )
  ```

- [x] Validate model loads successfully
- [x] Test with sample crisis message
- [x] Measure VRAM usage (expected: ~800MB)
- [x] Measure latency (expected: 1-2 seconds)
- [x] Test with custom crisis labels:
  ```python
  labels = [
      "suicide ideation",
      "self-harm thoughts",
      "severe depression",
      "panic attack",
      "abuse situation",
      "family rejection",
      "identity crisis",
      "mental health emergency"
  ]
  ```

- [x] Run ModelEvaluator tests:
  - [x] Test against crisis_examples.json
  - [x] Test against safe_examples.json
  - [x] Test against edge_cases.json
  - [x] Calculate accuracy metrics
  - [x] Compare against v3.1 baseline

**Validation Criteria**:
- ✅ Model downloads without errors
- ✅ VRAM usage < 1GB
- ✅ Latency < 3 seconds per message
- ✅ Accuracy improvement over baseline
- ✅ False positive rate acceptable (<10%)

**Deliverables**:
- [x] Model cached locally
- [x] Model validation report
- [x] Performance comparison vs baseline
- [x] Model integration documentation

---

### **Step 2.3: Download and Validate Model 2 - Emotion Detector**

**Model**: `SamLowe/roberta-base-go_emotions`

**Tasks**:
- [x] Download model to cache directory
- [x] Validate model loads successfully
- [x] Test emotion detection on sample messages
- [x] Measure VRAM usage (expected: ~250MB)
- [x] Measure latency (expected: 0.5-1 second)
- [x] Test all 28 emotion classes
- [x] Focus on crisis-relevant emotions:
  - sadness, grief, disappointment
  - fear, nervousness, confusion
  - remorse, disgust

- [x] Run ModelEvaluator tests against all datasets
- [x] Calculate emotion detection accuracy
- [x] Analyze multi-label performance

**Validation Criteria**:
- ✅ VRAM usage < 300MB
- ✅ Latency < 1.5 seconds
- ✅ Correctly identifies crisis-related emotions
- ✅ Low false positive on positive emotions

**Deliverables**:
- [x] Model cached and validated
- [x] Emotion detection report
- [x] Crisis emotion identification accuracy
- [x] Integration documentation

---

### **Step 2.4: Download and Validate Model 3 - Sentiment Analyzer**

**Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`

**Tasks**:
- [x] Download model to cache directory
- [x] Validate model loads successfully
- [x] Test sentiment classification
- [x] Measure VRAM usage (expected: ~250MB)
- [x] Measure latency (expected: 0.3-0.5 seconds)
- [x] Test 3-class sentiment (Negative, Neutral, Positive)
- [x] Run ModelEvaluator tests
- [x] Validate social media language understanding

**Validation Criteria**:
- ✅ VRAM usage < 300MB
- ✅ Latency < 1 second
- ✅ Correctly identifies negative sentiment in crisis messages
- ✅ Distinguishes neutral from negative

**Deliverables**:
- [x] Model cached and validated
- [x] Sentiment analysis report
- [x] Comparison with v3.1 sentiment model
- [x] Integration documentation

---

### **Step 2.5: Download and Validate Model 4 - Irony Detector**

**Model**: `cardiffnlp/twitter-roberta-base-irony`

**Tasks**:
- [x] Download model to cache directory
- [x] Validate model loads successfully
- [x] Test irony detection on sarcastic messages
- [x] Measure VRAM usage (expected: ~250MB)
- [x] Measure latency (expected: 0.3-0.5 seconds)
- [x] Test binary classification (Ironic / Not Ironic)
- [x] Run ModelEvaluator tests, especially edge_cases.json
- [x] Validate sarcasm detection on crisis messages

**Critical Test Cases**:
```python
test_cases = [
    "I'm just great",  # Should detect irony if contextually negative
    "Best day ever",   # Should detect irony
    "Love my life right now"  # Should detect irony
]
```

**Validation Criteria**:
- ✅ VRAM usage < 300MB
- ✅ Latency < 1 second
- ✅ Correctly identifies sarcastic crisis expressions
- ✅ Low false positive on genuine positive messages

**Deliverables**:
- [x] Model cached and validated
- [x] Irony detection report
- [x] Sarcasm handling analysis
- [x] Integration documentation

---

### **Step 2.6: Validate Total Ensemble Resources**

**Objective**: Confirm all 4 models can run simultaneously within constraints

**Tasks**:
- [x] Load all 4 models simultaneously
- [x] Measure total VRAM usage
  - Expected: ~1.55GB
  - Maximum acceptable: 2GB
  - Target: < 12.9% of 12GB available

- [x] Test sequential execution on single message
  - Measure total latency
  - Expected: 3-7 seconds
  - Maximum acceptable: 10 seconds

- [x] Test batch processing (if needed)
- [x] Monitor GPU memory fragmentation
- [x] Test model unloading/reloading
- [x] Validate model caching effectiveness

**Load Test Scenarios**:
```python
# Scenario 1: Cold start (all models loading from disk)
# Scenario 2: Warm start (models cached in VRAM)
# Scenario 3: 10 messages in rapid succession
# Scenario 4: 100 messages in 1 minute
```

**Validation Criteria**:
- ✅ Total VRAM < 2GB
- ✅ Total latency < 10 seconds per message
- ✅ No memory leaks over 100 messages
- ✅ Models can reload after crash

**Deliverables**:
- [x] Resource utilization report
- [x] Load test results
- [x] Optimization recommendations
- [x] Resource monitoring dashboard

---

### **Step 2.7: Create Unified Model Wrapper Interface**

**Tasks**:
- [x] Implement ModelWrapper base class
- [x] Create specific wrappers for each model type:
  - [x] CrisisClassifierWrapper
  - [x] EmotionDetectorWrapper
  - [x] SentimentAnalyzerWrapper
  - [x] IronyDetectorWrapper
- [x] Implement output standardization
- [x] Add error handling for model failures
- [x] Implement caching for repeated queries
- [x] Create factory function: `create_model_wrapper()`
- [x] Add unit tests for each wrapper
- [x] Document wrapper usage

---

### **Step 2.8: Phase 2 Validation & Sign-Off**

**Phase 2 Complete Checklist**:

**Model Infrastructure**:
- [x] All 4 models downloaded and cached
- [x] ModelLoader implemented and tested
- [x] ModelWrapper interface implemented
- [x] All models validated independently

**Performance Validation**:
- [x] Total VRAM < 2GB ✓
- [x] Total latency < 10 seconds ✓
- [x] Each model tested against all test datasets
- [x] Performance reports generated for each model

**Comparison vs Baseline**:
- [x] Crisis classifier vs v3.1 depression model
- [x] Emotion detector performance validated
- [x] Sentiment analyzer vs v3.1 sentiment model
- [x] Irony detector validated (new capability)

**Clean Architecture Compliance**:
- [x] All files have version headers
- [x] Factory functions used
- [x] Configuration via JSON + environment
- [x] Dependency injection implemented

**Documentation**:
- [x] Model selection rationale documented
- [x] Model integration guide completed
- [x] Performance benchmarks documented
- [x] Known limitations documented

**Success Criteria**:
- ✅ All 4 models operational independently
- ✅ VRAM and latency within acceptable ranges
- ✅ Accuracy improvements over v3.1 baseline
- ✅ Unified model interface working
- ✅ Ready for ensemble coordinator implementation

**Sign-Off Required**:
- [x] Project Lead approval
- [x] Model performance validated
- [x] Resource constraints met
- [x] Ready to proceed to Phase 3

---

## 📝 **PHASE 3: API CREATION AND DOCKER DEPLOYMENT**

### **Status**: ✅ **COMPLETED** (2026-1-1)

### **Duration**: 2-3 weeks
### **Priority**: HIGH

### **Objectives**:
- Implement Ensemble Decision Engine
- Implement API Endpoints
- Implement Docker Deployment
  - Dockerize Ash-NLP
  - Deploy Ash-NLP
- Implement Configuration Management
- Implement Error Handling & Fallbacks
- Implement Logging & Monitoring
- Implement Performance Optimization

---

### **Step 3.1: Design Ensemble Decision Engine**

**Core Responsibilities**:
```
Ensemble Coordinator
├── Parallel Model Execution
│   ├── Distribute message to all 4 models
│   ├── Collect results from each model
│   └── Handle model failures gracefully
├── Consensus Algorithm
│   ├── Weighted voting based on model confidence
│   ├── Detect model agreement/disagreement
│   └── Resolve conflicts between models
├── Result Aggregation
│   ├── Combine crisis scores from all models
│   ├── Identify primary crisis indicators
│   └── Calculate final crisis confidence
└── Explainability
    ├── Show which models contributed to decision
    ├── Highlight areas of disagreement
    └── Provide reasoning for final classification
```

**Tasks**:
- [x] Design EnsembleCoordinator class structure
- [x] Create ensemble_config.json
- [x] Define consensus algorithm options
- [x] Define model weighting strategy
- [x] Create architecture documentation

---

### **Step 3.2: Implement API Endpoints**

**Tasks**:
- [x] Create FastAPI application with lifespan management and OpenAPI docs (Swagger/ReDoc)
- [x] Implement `/api/v1/analyze` POST endpoint for single message crisis detection
- [x] Implement `/api/v1/analyze/batch` POST endpoint for batch processing (1-10 messages)
- [x] Implement `/api/v1/health` GET endpoint with system status and model readiness
- [x] Implement `/api/v1/models` GET endpoint with loaded model information
- [x] Create Pydantic request/response schemas with validation
- [x] Add rate limiting middleware with configurable limits
- [x] Document API application

---

### **Step 3.3: Implement Docker Deployment**

**Tasks**:
- [x] Create multi-stage Dockerfile with NVIDIA CUDA runtime base
- [x] Implement non-root user (UID 1001) for security
- [x] Configure container health checks with appropriate timeouts
- [x] Create docker-compose.yml with GPU and CPU service profiles
- [x] Configure model caching with persistent volume mounts
- [x] Add resource limits (memory, GPU) and security hardening
- [x] Integrate Docker secrets for sensitive credentials
- [x] Document deployment strategy

---

### **Step 3.4: Implement Configuration Management**

**Tasks**:
- [x] Create ConfigManager class with singleton pattern and JSON loading
- [x] Implement environment variable overrides with `NLP_` prefix
- [x] Add configuration validation (weights, thresholds, ports)
- [x] Create config templates (default.json, production.json, .env.template)
- [x] Document all configuration options in `docs/configuration.module`

---

### **Step 3.5: Implement Error Handling & Fallbacks**

**Tasks**:
- [x] Implement FallbackStrategy with weight redistribution on model failure
- [x] Add circuit breaker pattern (CLOSED/OPEN/HALF_OPEN states)
- [x] Implement retry logic with exponential backoff and jitter
- [x] Add timeout handling for model inference
- [x] Create standardized error response schemas with error codes
- [x] Implement Discord webhook alerting for failures and state changes
- [x] Document Error Handleing and Fallbacks

---

### **Step 3.6: Implement Logging & Monitoring**

**Tasks**:
- [x] Implement structured JSON logging with configurable format
- [x] Add request tracing with X-Request-ID header propagation
- [x] Track performance metrics (processing time, per-model latency)
- [x] Create Discord alerting for startup, shutdown, and critical events
- [x] Add optional Prometheus metrics endpoint
- [x] Document Monitoring and Logging

---

### **Step 3.7: Implement Performance Optimization**

**Tasks**:
- [x] Implement model warmup on startup for consistent latency
- [x] Add async parallel model inference using `asyncio.gather()`
- [x] Implement response caching with LRU eviction and TTL expiration
- [ ] Request batching → **Deferred to Phase 5**
- [ ] Benchmarking and profiling → **Deferred to Phase 5**
- [ ] Memory optimization (quantization) → **Deferred to Phase 5**
- [x] Document optimization results

---
### **Step 3.8: Phase 3 Validation & Sign-Off**

**Phase 3 Complete Checklist**:

**Ensemble Implementation**:
- [x] EnsembleCoordinator implemented and tested
- [x] All consensus algorithms working
- [x] Result aggregation functional
- [x] Conflict detection operational
- [x] Explainability layer complete

**API Integration**:
- [x] API endpoints updated
- [x] Factory functions working
- [x] Dependency injection maintained

**Testing**:
- [x] All test datasets passed
- [x] Performance metrics within targets
- [x] Accuracy improved over baseline
- [x] False positive rate acceptable
- [x] Edge cases handled properly

**Performance Validation**:
- [x] Latency < 10 seconds ✓
- [x] VRAM < 2GB ✓
- [x] Can handle 100 messages/minute
- [x] No memory leaks detected

**Clean Architecture Compliance**:
- [x] All files have version headers
- [x] Factory functions used
- [x] Configuration via JSON + environment
- [x] Dependency injection maintained

**Documentation**:
- [x] Ensemble architecture documented
- [x] Consensus algorithms explained
- [x] Configuration guide complete
- [x] Troubleshooting guide created

**Success Criteria**:
- ✅ Ensemble operational with all 4 models
- ✅ Consensus working across algorithms
- ✅ Performance within acceptable ranges
- ✅ Accuracy improved over v3.1 baseline
- ✅ Ready for context analysis integration

**Sign-Off Required**:
- [x] Project Lead approval
- [x] Ensemble performance validated
- [x] Test coverage sufficient
- [x] Ready to proceed to Phase 4

---

## 📝 **PHASE 4: ENSEMBLE COORDINATOR IMPLEMENTATION**

### **Status**: ⏳ **NOT STARTED**

### **Duration**: 2-3 weeks
### **Priority**: HIGH

### **Objectives**:
- Create consensus algorithms (Council-inspired)
- Implement confidence weighting and conflict resolution
- Create ensemble result aggregation

---

### **Step 4.1: Implement Consensus Algorithms**

**Algorithm Options**:

**1. Weighted Voting**:
```python
def weighted_voting_consensus(
    model_results: Dict,
    weights: Dict
) -> Dict:
    """
    Weight each model's prediction by confidence and weight
    
    Formula:
    crisis_score = Σ(model_score * model_weight * model_confidence)
    """
    total_weighted_score = 0
    total_weight = 0
    
    for model_name, result in model_results.items():
        model_weight = weights.get(model_name, 0.25)
        model_confidence = result['confidence']
        model_score = result['crisis_indicator_score']
        
        weighted_contribution = (
            model_score * model_weight * model_confidence
        )
        total_weighted_score += weighted_contribution
        total_weight += model_weight
    
    final_score = total_weighted_score / total_weight
    
    return {
        "consensus_type": "weighted_voting",
        "final_crisis_score": final_score,
        "individual_contributions": {...}
    }
```

**2. Majority Voting**:
```python
def majority_voting_consensus(model_results: Dict) -> Dict:
    """
    Majority vote: Most models agree = final decision
    
    Useful for binary crisis/no-crisis decisions
    """
    crisis_votes = 0
    total_votes = len(model_results)
    
    for result in model_results.values():
        if result['crisis_indicator_score'] > 0.5:
            crisis_votes += 1
    
    is_crisis = crisis_votes > (total_votes / 2)
    confidence = crisis_votes / total_votes
    
    return {
        "consensus_type": "majority_voting",
        "is_crisis": is_crisis,
        "confidence": confidence,
        "votes": {"crisis": crisis_votes, "safe": total_votes - crisis_votes}
    }
```

**3. Unanimous Consensus** (Conservative):
```python
def unanimous_consensus(model_results: Dict) -> Dict:
    """
    All models must agree for crisis classification
    
    Most conservative approach - low false positives
    """
    crisis_threshold = 0.6
    all_agree = all(
        result['crisis_indicator_score'] > crisis_threshold
        for result in model_results.values()
    )
    
    if all_agree:
        avg_score = sum(
            r['crisis_indicator_score'] 
            for r in model_results.values()
        ) / len(model_results)
        return {
            "consensus_type": "unanimous",
            "is_crisis": True,
            "crisis_score": avg_score,
            "agreement": "unanimous"
        }
    else:
        return {
            "consensus_type": "unanimous",
            "is_crisis": False,
            "crisis_score": 0.0,
            "agreement": "not_unanimous"
        }
```

**4. Conflict-Aware Consensus** (NEW - Council-inspired):
```python
def conflict_aware_consensus(model_results: Dict) -> Dict:
    """
    Detect disagreements and flag for review
    
    Inspired by LLM Council's peer review stage
    """
    scores = [r['crisis_indicator_score'] for r in model_results.values()]
    
    # Calculate variance in scores
    mean_score = sum(scores) / len(scores)
    variance = sum((s - mean_score)**2 for s in scores) / len(scores)
    
    # High variance = disagreement
    disagreement_threshold = 0.15
    has_disagreement = variance > disagreement_threshold
    
    if has_disagreement:
        return {
            "consensus_type": "conflict_aware",
            "has_conflict": True,
            "crisis_score": mean_score,
            "variance": variance,
            "requires_review": True,
            "conflicting_models": _identify_outliers(model_results)
        }
    else:
        return {
            "consensus_type": "conflict_aware",
            "has_conflict": False,
            "crisis_score": mean_score,
            "variance": variance,
            "requires_review": False
        }
```

**Tasks**:
- [ ] Implement weighted_voting_consensus
- [ ] Implement majority_voting_consensus
- [ ] Implement unanimous_consensus
- [ ] Implement conflict_aware_consensus
- [ ] Create consensus algorithm selector
- [ ] Document algorithm selection criteria

---

### **Step 4.2: Implement Result Aggregation**

**ResultAggregator Class**:
```python
class ResultAggregator:
    """
    Aggregate multi-model results into final ensemble output
    """
    
    def aggregate(
        self, 
        model_results: Dict, 
        consensus: Dict
    ) -> Dict:
        """
        Combine model results with consensus
        
        Returns comprehensive ensemble result
        """
        return {
            "ensemble_version": "v5.0",
            "timestamp": datetime.utcnow().isoformat(),
            
            # Final Crisis Assessment
            "crisis_assessment": {
                "crisis_score": consensus['final_crisis_score'],
                "crisis_level": self._determine_crisis_level(
                    consensus['final_crisis_score']
                ),
                "confidence": consensus.get('confidence', 0.0),
                "requires_intervention": self._requires_intervention(
                    consensus['final_crisis_score']
                )
            },
            
            # Individual Model Results
            "model_results": {
                "crisis_classifier": {
                    "top_labels": [...],
                    "confidence": 0.XX,
                    "contribution_weight": 0.XX
                },
                "emotion_detector": {...},
                "sentiment_analyzer": {...},
                "irony_detector": {...}
            },
            
            # Consensus Analysis
            "consensus": {
                "algorithm": consensus['consensus_type'],
                "agreement_level": self._calculate_agreement_level(
                    model_results
                ),
                "has_conflict": consensus.get('has_conflict', False),
                "requires_review": consensus.get('requires_review', False)
            },
            
            # Explainability
            "explanation": {
                "primary_indicators": self._identify_primary_indicators(
                    model_results
                ),
                "contributing_factors": [...],
                "model_agreement": {...},
                "confidence_breakdown": {...}
            },
            
            # Performance Metrics
            "performance": {
                "total_latency_ms": sum(
                    r['latency_ms'] for r in model_results.values()
                ),
                "total_vram_mb": sum(
                    r['vram_mb'] for r in model_results.values()
                )
            }
        }
    
    def _determine_crisis_level(self, score: float) -> str:
        """Map crisis score to severity level"""
        if score >= 0.85:
            return "critical"
        elif score >= 0.65:
            return "high"
        elif score >= 0.40:
            return "medium"
        elif score >= 0.20:
            return "low"
        else:
            return "none"
    
    def _requires_intervention(self, score: float) -> bool:
        """Determine if immediate intervention needed"""
        return score >= 0.70
    
    def _calculate_agreement_level(
        self, 
        model_results: Dict
    ) -> str:
        """Calculate how much models agree"""
        scores = [r['crisis_indicator_score'] for r in model_results.values()]
        variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
        
        if variance < 0.05:
            return "strong_agreement"
        elif variance < 0.15:
            return "moderate_agreement"
        else:
            return "significant_disagreement"
    
    def _identify_primary_indicators(
        self, 
        model_results: Dict
    ) -> List[str]:
        """Identify main crisis indicators from all models"""
        indicators = []
        
        # From crisis classifier
        crisis_labels = model_results['crisis_classifier']['top_predictions']
        indicators.extend([l['label'] for l in crisis_labels if l['score'] > 0.5])
        
        # From emotion detector
        crisis_emotions = ['sadness', 'fear', 'grief', 'despair']
        detected_emotions = model_results['emotion_detector']['predictions']
        indicators.extend([
            e['label'] for e in detected_emotions 
            if e['label'] in crisis_emotions and e['score'] > 0.6
        ])
        
        # From sentiment analyzer
        if model_results['sentiment_analyzer']['sentiment'] == 'negative':
            indicators.append('negative_sentiment')
        
        # From irony detector
        if model_results['irony_detector']['is_ironic']:
            indicators.append('sarcastic_expression')
        
        return list(set(indicators))  # Remove duplicates
```

**Tasks**:
- [ ] Implement ResultAggregator class
- [ ] Create comprehensive output structure
- [ ] Implement crisis level determination
- [ ] Implement agreement level calculation
- [ ] Add primary indicator identification
- [ ] Create explainability report
- [ ] Document output format

---

### **Step 4.3: Implement Conflict Detection & Resolution**

**Objective**: Handle cases where models disagree significantly

**ConflictDetector Class**:
```python
class ConflictDetector:
    """
    Detect and handle conflicts between ensemble models
    """
    
    def detect_conflicts(self, model_results: Dict) -> Dict:
        """
        Identify conflicts in model predictions
        
        Returns conflict analysis
        """
        conflicts = []
        
        # Type 1: Score Disagreement
        scores = [r['crisis_indicator_score'] for r in model_results.values()]
        if max(scores) - min(scores) > 0.4:
            conflicts.append({
                "type": "score_disagreement",
                "severity": "high",
                "details": {
                    "max_score": max(scores),
                    "min_score": min(scores),
                    "range": max(scores) - min(scores)
                }
            })
        
        # Type 2: Irony Conflict
        # Sentiment positive but irony detected
        sentiment = model_results['sentiment_analyzer']['sentiment']
        is_ironic = model_results['irony_detector']['is_ironic']
        
        if sentiment == 'positive' and is_ironic:
            conflicts.append({
                "type": "irony_sentiment_conflict",
                "severity": "medium",
                "details": {
                    "surface_sentiment": "positive",
                    "actual_sentiment": "likely_negative",
                    "confidence": model_results['irony_detector']['confidence']
                }
            })
        
        # Type 3: Emotion-Crisis Mismatch
        crisis_score = model_results['crisis_classifier']['confidence']
        crisis_emotions = self._get_crisis_emotions(
            model_results['emotion_detector']
        )
        
        if crisis_score > 0.7 and len(crisis_emotions) == 0:
            conflicts.append({
                "type": "emotion_crisis_mismatch",
                "severity": "medium",
                "details": {
                    "crisis_score": crisis_score,
                    "detected_emotions": crisis_emotions,
                    "expected": "high crisis emotions"
                }
            })
        
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflict_count": len(conflicts),
            "conflicts": conflicts,
            "requires_human_review": self._requires_review(conflicts)
        }
    
    def resolve_conflicts(
        self, 
        model_results: Dict, 
        conflicts: Dict
    ) -> Dict:
        """
        Apply conflict resolution strategies
        """
        resolution_strategy = "conservative"  # Default to safer choice
        
        if conflicts['has_conflicts']:
            # Conservative: Prioritize crisis detection over false negatives
            # Better to over-alert than under-alert for safety
            
            max_crisis_score = max(
                r['crisis_indicator_score'] 
                for r in model_results.values()
            )
            
            return {
                "resolution_method": resolution_strategy,
                "final_score": max_crisis_score,
                "rationale": "Prioritized safety over precision due to conflict",
                "flagged_for_review": True
            }
        else:
            return {
                "resolution_method": "standard_consensus",
                "no_conflicts": True
            }
```

**Tasks**:
- [ ] Implement ConflictDetector class
- [ ] Define conflict types and severity levels
- [ ] Implement conflict detection algorithms
- [ ] Implement conflict resolution strategies
- [ ] Create conflict reporting
- [ ] Document conflict handling procedures

---

### **Step 4.4: Implement Explainability Layer**

**Objective**: Make ensemble decisions transparent and auditable

**ExplainabilityGenerator Class**:
```python
class ExplainabilityGenerator:
    """
    Generate human-readable explanations for ensemble decisions
    """
    
    def generate_explanation(
        self, 
        message: str,
        ensemble_result: Dict
    ) -> Dict:
        """
        Create explanation for ensemble decision
        
        Returns structured explanation
        """
        return {
            "decision_summary": self._create_summary(ensemble_result),
            "model_contributions": self._explain_contributions(
                ensemble_result
            ),
            "key_factors": self._identify_key_factors(ensemble_result),
            "confidence_breakdown": self._explain_confidence(
                ensemble_result
            ),
            "alternative_interpretations": self._provide_alternatives(
                ensemble_result
            ),
            "recommended_action": self._recommend_action(
                ensemble_result
            )
        }
    
    def _create_summary(self, result: Dict) -> str:
        """Generate plain-English summary"""
        crisis_level = result['crisis_assessment']['crisis_level']
        confidence = result['crisis_assessment']['confidence']
        
        if crisis_level == "critical":
            return (
                f"CRITICAL: High-confidence ({confidence:.0%}) crisis "
                f"detected. Immediate intervention recommended."
            )
        elif crisis_level == "high":
            return (
                f"HIGH CONCERN: Models detected significant crisis "
                f"indicators with {confidence:.0%} confidence."
            )
        elif crisis_level == "medium":
            return (
                f"MODERATE CONCERN: Some crisis indicators present. "
                f"Monitoring recommended."
            )
        elif crisis_level == "low":
            return (
                f"LOW CONCERN: Minor negative indicators detected."
            )
        else:
            return "No significant crisis indicators detected."
    
    def _explain_contributions(self, result: Dict) -> List[Dict]:
        """Explain what each model contributed"""
        contributions = []
        
        for model_name, model_result in result['model_results'].items():
            contribution = {
                "model": model_name,
                "finding": self._summarize_model_finding(
                    model_name, 
                    model_result
                ),
                "confidence": model_result['confidence'],
                "weight": model_result['contribution_weight']
            }
            contributions.append(contribution)
        
        return contributions
    
    def _identify_key_factors(self, result: Dict) -> List[str]:
        """List the most important factors in the decision"""
        return result['explanation']['primary_indicators']
    
    def _recommend_action(self, result: Dict) -> Dict:
        """Recommend appropriate response"""
        crisis_score = result['crisis_assessment']['crisis_score']
        
        if crisis_score >= 0.85:
            return {
                "priority": "immediate",
                "action": "alert_staff",
                "message": "Contact user immediately, notify moderators",
                "escalation": "crisis_team"
            }
        elif crisis_score >= 0.65:
            return {
                "priority": "high",
                "action": "monitor_closely",
                "message": "Check user history, consider outreach",
                "escalation": "moderator_review"
            }
        elif crisis_score >= 0.40:
            return {
                "priority": "medium",
                "action": "passive_monitoring",
                "message": "Watch for escalation patterns",
                "escalation": "automated_tracking"
            }
        else:
            return {
                "priority": "low",
                "action": "normal_monitoring",
                "message": "Continue standard monitoring",
                "escalation": "none"
            }
```

**Explanation Output Example**:
```json
{
  "decision_summary": "HIGH CONCERN: Models detected significant crisis indicators with 78% confidence.",
  
  "model_contributions": [
    {
      "model": "crisis_classifier",
      "finding": "Detected 'self-harm thoughts' (0.82) and 'severe depression' (0.67)",
      "confidence": 0.82,
      "weight": 0.4
    },
    {
      "model": "emotion_detector",
      "finding": "Strong sadness (0.91), fear (0.73), and grief (0.58) detected",
      "confidence": 0.91,
      "weight": 0.3
    },
    {
      "model": "sentiment_analyzer",
      "finding": "Highly negative sentiment (0.87)",
      "confidence": 0.87,
      "weight": 0.2
    },
    {
      "model": "irony_detector",
      "finding": "No sarcasm detected - message appears sincere",
      "confidence": 0.89,
      "weight": 0.1
    }
  ],
  
  "key_factors": [
    "self-harm thoughts",
    "severe depression",
    "sadness",
    "fear",
    "negative_sentiment"
  ],
  
  "confidence_breakdown": {
    "model_agreement": "strong_agreement",
    "variance": 0.04,
    "unanimous_concern": true
  },
  
  "recommended_action": {
    "priority": "high",
    "action": "monitor_closely",
    "message": "Check user history, consider outreach",
    "escalation": "moderator_review"
  }
}
```

**Tasks**:
- [ ] Implement ExplainabilityGenerator class
- [ ] Create human-readable summaries
- [ ] Implement contribution explanations
- [ ] Add action recommendations
- [ ] Create explanation templates
- [ ] Document explanation format

---

### **Step 4.5: Phase 4 Validation & Sign-Off**

**Phase 4 Complete Checklist**:

**Ensemble Implementation**:
- [ ] EnsembleCoordinator implemented and tested
- [ ] All consensus algorithms working
- [ ] Result aggregation functional
- [ ] Conflict detection operational
- [ ] Explainability layer complete

**Integration**:
- [ ] Integrated with CrisisAnalyzer
- [ ] API endpoints updated
- [ ] Factory functions working
- [ ] Dependency injection maintained

**Testing**:
- [ ] All test datasets passed
- [ ] Performance metrics within targets
- [ ] Accuracy improved over baseline
- [ ] False positive rate acceptable
- [ ] Edge cases handled properly

**Performance Validation**:
- [ ] Latency < 10 seconds ✓
- [ ] VRAM < 2GB ✓
- [ ] Can handle 100 messages/minute
- [ ] No memory leaks detected

**Clean Architecture Compliance**:
- [ ] All files have version headers
- [ ] Factory functions used
- [ ] Configuration via JSON + environment
- [ ] Dependency injection maintained

**Documentation**:
- [ ] Ensemble architecture documented
- [ ] Consensus algorithms explained
- [ ] Configuration guide complete
- [ ] Troubleshooting guide created

**Success Criteria**:
- ✅ Ensemble operational with all 4 models
- ✅ Consensus working across algorithms
- ✅ Performance within acceptable ranges
- ✅ Accuracy improved over v3.1 baseline
- ✅ Ready for context analysis integration

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Ensemble performance validated
- [ ] Test coverage sufficient
- [ ] Ready to proceed to Phase 4

---

## 📝 **PHASE 5: CONTEXT ANALYSIS INTEGRATION**

### **Status**: ⏳ **NOT STARTED** (Blocked by Phase 4)

### **Duration**: 1-2 weeks
### **Priority**: MEDIUM

### **Objectives**:
- Implement rolling window message history
- Add temporal pattern detection
- Create escalation detection

---

### **Step 5.1: Design Context History Architecture**

**Core Concept**: Track user message history to detect:
- **Escalating crisis** (getting worse over time)
- **Chronic distress** (persistent low-level crisis)
- **Sudden onset** (rapid mood change)
- **Communication patterns** (frequency, isolation)

**Configuration**: `src/config/context_config.json`
```json
{
  "_metadata": {
    "file_version": "v5.0",
    "description": "Context analysis configuration"
  },
  "history": {
    "window_size": "${CONTEXT_WINDOW_SIZE}",
    "min_messages_for_analysis": "${CONTEXT_MIN_MESSAGES}",
    "max_storage_per_user": "${CONTEXT_MAX_STORAGE}"
  },
  "escalation": {
    "detection_threshold": "${CONTEXT_ESCALATION_THRESHOLD}",
    "time_window": "${CONTEXT_ESCALATION_WINDOW}",
    "boost_amount": "${CONTEXT_ESCALATION_BOOST}"
  },
  "temporal": {
    "high_frequency_threshold": "${CONTEXT_HIGH_FREQ_THRESHOLD}",
    "chronic_score_threshold": "${CONTEXT_CHRONIC_THRESHOLD}",
    "trend_sensitivity": "${CONTEXT_TREND_SENSITIVITY}"
  },
  "defaults": {
    "history": {
      "window_size": 10,
      "min_messages_for_analysis": 3,
      "max_storage_per_user": 100
    },
    "escalation": {
      "detection_threshold": 0.2,
      "time_window": 3,
      "boost_amount": 0.15
    },
    "temporal": {
      "high_frequency_threshold": 5,
      "chronic_score_threshold": 0.6,
      "trend_sensitivity": 0.1
    }
  }
}
```

**Tasks**:
- [ ] Design ContextHistory class structure
- [ ] Create context_config.json
- [ ] Define history storage strategy
- [ ] Define escalation detection algorithm
- [ ] Create architecture documentation

---

### **Step 5.2: Implement Message History Storage**

**Requirements**:
- Store last N messages per user
- Include timestamp, message, scores
- Efficient memory usage
- Thread-safe access
- Persistence optional (Phase 6)

**Implementation Options**:

**Redis Cache (Scalable)**:
```python
class RedisHistoryStore:
    """Redis-backed message history for scalability"""
    
    def __init__(self, redis_client, max_window_size: int = 10):
        self.redis = redis_client
        self.max_window_size = max_window_size
    
    def add_message(
        self, 
        user_id: str, 
        message_record: Dict
    ) -> None:
        """Add message to Redis list"""
        key = f"history:{user_id}"
        self.redis.lpush(key, json.dumps(message_record))
        self.redis.ltrim(key, 0, self.max_window_size - 1)
        self.redis.expire(key, 86400 * 7)  # 7 day TTL
    
    def get_history(self, user_id: str) -> List[Dict]:
        """Get user history from Redis"""
        key = f"history:{user_id}"
        records = self.redis.lrange(key, 0, -1)
        return [json.loads(r) for r in records]
```

**Tasks**:
- [ ] Implement RedisHistoryStore
- [ ] Add thread safety (locks if needed)
- [ ] Implement history cleanup
- [ ] Document storage strategy

---

### **Step 5.3: Implement Temporal Pattern Detection**

**TemporalPatternDetector Class**:
```python
class TemporalPatternDetector:
    """
    Detect patterns in message history over time
    """
    
    def detect_patterns(self, history: List[Dict]) -> Dict:
        """
        Analyze temporal patterns in message history
        
        Returns pattern analysis
        """
        if len(history) < 3:
            return {"status": "insufficient_data"}
        
        patterns = []
        
        # Pattern 1: Trend Analysis
        trend = self._analyze_trend(history)
        patterns.append(trend)
        
        # Pattern 2: Frequency Analysis
        frequency = self._analyze_frequency(history)
        patterns.append(frequency)
        
        # Pattern 3: Volatility Analysis
        volatility = self._analyze_volatility(history)
        patterns.append(volatility)
        
        # Pattern 4: Time-of-Day Patterns
        time_pattern = self._analyze_time_patterns(history)
        patterns.append(time_pattern)
        
        return {
            "status": "analyzed",
            "patterns": patterns,
            "summary": self._summarize_patterns(patterns)
        }
    
    def _analyze_trend(self, history: List[Dict]) -> Dict:
        """Detect if crisis is getting better/worse"""
        scores = [h['crisis_score'] for h in history]
        
        # Simple linear regression
        n = len(scores)
        x = list(range(n))
        
        # Calculate slope
        x_mean = sum(x) / n
        y_mean = sum(scores) / n
        
        numerator = sum((x[i] - x_mean) * (scores[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        if slope > 0.05:
            trend = "increasing"
        elif slope < -0.05:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "type": "trend",
            "direction": trend,
            "slope": slope,
            "confidence": abs(slope)
        }
    
    def _analyze_frequency(self, history: List[Dict]) -> Dict:
        """Analyze message frequency"""
        if len(history) < 2:
            return {"type": "frequency", "status": "insufficient_data"}
        
        timestamps = [h['timestamp'] for h in history]
        
        # Calculate time differences
        time_diffs = [
            (timestamps[i+1] - timestamps[i]).total_seconds() / 3600
            for i in range(len(timestamps) - 1)
        ]
        
        avg_interval_hours = sum(time_diffs) / len(time_diffs)
        messages_per_hour = 1 / avg_interval_hours if avg_interval_hours > 0 else 0
        
        if messages_per_hour > 5:
            frequency_level = "very_high"
        elif messages_per_hour > 2:
            frequency_level = "high"
        elif messages_per_hour > 0.5:
            frequency_level = "normal"
        else:
            frequency_level = "low"
        
        return {
            "type": "frequency",
            "messages_per_hour": messages_per_hour,
            "level": frequency_level,
            "avg_interval_hours": avg_interval_hours
        }
    
    def _analyze_volatility(self, history: List[Dict]) -> Dict:
        """Analyze score volatility"""
        scores = [h['crisis_score'] for h in history]
        
        # Calculate variance
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        
        if std_dev > 0.3:
            volatility_level = "high"
        elif std_dev > 0.15:
            volatility_level = "moderate"
        else:
            volatility_level = "low"
        
        return {
            "type": "volatility",
            "level": volatility_level,
            "standard_deviation": std_dev,
            "variance": variance
        }
    
    def _analyze_time_patterns(self, history: List[Dict]) -> Dict:
        """Detect time-of-day patterns"""
        timestamps = [h['timestamp'] for h in history]
        hours = [t.hour for t in timestamps]
        
        # Count messages by time period
        night_messages = sum(1 for h in hours if 22 <= h or h < 6)
        
        if night_messages / len(hours) > 0.6:
            pattern = "primarily_night"  # Potential isolation indicator
        else:
            pattern = "normal_distribution"
        
        return {
            "type": "time_pattern",
            "pattern": pattern,
            "night_message_ratio": night_messages / len(hours)
        }
```

**Tasks**:
- [ ] Implement TemporalPatternDetector class
- [ ] Implement trend analysis
- [ ] Implement frequency analysis
- [ ] Implement volatility analysis
- [ ] Implement time-of-day analysis
- [ ] Document pattern detection

---

### **Step 5.4: Implement Escalation Detection**

**EscalationDetector Class**:
```python
class EscalationDetector:
    """
    Detect escalating crisis situations
    """
    
    def detect_escalation(
        self, 
        history: List[Dict],
        config: Dict
    ) -> Dict:
        """
        Detect if crisis is escalating
        
        Returns escalation analysis
        """
        if len(history) < 3:
            return {
                "is_escalating": False,
                "reason": "insufficient_history"
            }
        
        # Get recent messages
        window_size = config.get('time_window', 3)
        recent_history = history[-window_size:]
        
        # Analyze escalation types
        escalation_analysis = {
            "score_escalation": self._detect_score_escalation(
                recent_history
            ),
            "severity_escalation": self._detect_severity_escalation(
                recent_history
            ),
            "temporal_urgency": self._detect_temporal_urgency(
                recent_history
            ),
            "communication_change": self._detect_communication_change(
                recent_history,
                history
            )
        }
        
        # Determine overall escalation
        is_escalating = any(
            analysis.get('is_escalating', False)
            for analysis in escalation_analysis.values()
        )
        
        if is_escalating:
            severity = self._determine_escalation_severity(
                escalation_analysis
            )
            return {
                "is_escalating": True,
                "severity": severity,
                "escalation_types": escalation_analysis,
                "recommendation": self._get_escalation_recommendation(
                    severity
                )
            }
        
        return {
            "is_escalating": False,
            "analysis": escalation_analysis
        }
    
    def _detect_score_escalation(
        self, 
        recent_history: List[Dict]
    ) -> Dict:
        """Detect if scores are increasing"""
        scores = [h['crisis_score'] for h in recent_history]
        
        # Check if monotonically increasing
        is_increasing = all(
            scores[i] < scores[i+1]
            for i in range(len(scores)-1)
        )
        
        if is_increasing:
            rate = scores[-1] - scores[0]
            return {
                "is_escalating": True,
                "escalation_rate": rate,
                "start_score": scores[0],
                "end_score": scores[-1]
            }
        
        return {"is_escalating": False}
    
    def _detect_severity_escalation(
        self, 
        recent_history: List[Dict]
    ) -> Dict:
        """Detect if crisis level is worsening"""
        levels = [h['crisis_level'] for h in recent_history]
        
        level_order = ["none", "low", "medium", "high", "critical"]
        level_indices = [level_order.index(l) for l in levels]
        
        # Check if levels are increasing
        is_worsening = all(
            level_indices[i] <= level_indices[i+1]
            for i in range(len(level_indices)-1)
        )
        
        if is_worsening and level_indices[-1] > level_indices[0]:
            return {
                "is_escalating": True,
                "start_level": levels[0],
                "end_level": levels[-1],
                "level_jump": level_indices[-1] - level_indices[0]
            }
        
        return {"is_escalating": False}
    
    def _detect_temporal_urgency(
        self, 
        recent_history: List[Dict]
    ) -> Dict:
        """Detect urgent temporal markers"""
        urgent_keywords = [
            "tonight", "right now", "can't wait",
            "immediately", "today", "this moment"
        ]
        
        latest_message = recent_history[-1]['message']
        
        has_urgency = any(
            keyword in latest_message.lower()
            for keyword in urgent_keywords
        )
        
        if has_urgency:
            return {
                "is_escalating": True,
                "urgency_type": "temporal",
                "urgency_indicators": [
                    kw for kw in urgent_keywords 
                    if kw in latest_message.lower()
                ]
            }
        
        return {"is_escalating": False}
    
    def _detect_communication_change(
        self,
        recent_history: List[Dict],
        full_history: List[Dict]
    ) -> Dict:
        """Detect change in communication pattern"""
        if len(full_history) < 6:
            return {"is_escalating": False}
        
        # Compare recent vs. previous frequency
        recent_timestamps = [h['timestamp'] for h in recent_history]
        previous_timestamps = [
            h['timestamp'] for h in full_history[:-len(recent_history)]
        ]
        
        recent_freq = self._calculate_frequency(recent_timestamps)
        previous_freq = self._calculate_frequency(previous_timestamps)
        
        # Sudden increase in frequency can indicate escalation
        if recent_freq > previous_freq * 2:
            return {
                "is_escalating": True,
                "change_type": "increased_frequency",
                "recent_freq": recent_freq,
                "previous_freq": previous_freq
            }
        
        return {"is_escalating": False}
    
    def _calculate_frequency(self, timestamps: List) -> float:
        """Calculate messages per hour"""
        if len(timestamps) < 2:
            return 0
        
        time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600
        return len(timestamps) / time_span if time_span > 0 else 0
    
    def _determine_escalation_severity(
        self, 
        escalation_analysis: Dict
    ) -> str:
        """Determine overall escalation severity"""
        escalation_count = sum(
            1 for analysis in escalation_analysis.values()
            if analysis.get('is_escalating', False)
        )
        
        if escalation_count >= 3:
            return "critical"
        elif escalation_count == 2:
            return "high"
        else:
            return "moderate"
    
    def _get_escalation_recommendation(self, severity: str) -> str:
        """Get recommendation based on escalation severity"""
        if severity == "critical":
            return "IMMEDIATE INTERVENTION REQUIRED"
        elif severity == "high":
            return "Priority monitoring and outreach recommended"
        else:
            return "Increased monitoring recommended"
```

**Tasks**:
- [ ] Implement EscalationDetector class
- [ ] Implement score escalation detection
- [ ] Implement severity escalation detection
- [ ] Implement temporal urgency detection
- [ ] Implement communication change detection
- [ ] Document escalation detection logic

---

### **Step 5.5: Phase 5 Validation & Sign-Off**

**Phase 5 Complete Checklist**:

**Testing**:
- [ ] Escalation patterns detected correctly
- [ ] Temporal analysis accurate
- [ ] False escalation rate acceptable
- [ ] Performance acceptable

**Integration**:
- [ ] Integrated with CrisisAnalyzer
- [ ] Factory functions working
- [ ] Configuration complete
- [ ] API endpoints updated

**Clean Architecture Compliance**:
- [ ] All files have version headers
- [ ] Factory functions used
- [ ] Configuration via JSON + environment
- [ ] Dependency injection maintained

**Documentation**:
- [ ] Escalation detection explained
- [ ] Configuration guide complete
- [ ] Testing methodology documented

**Success Criteria**:
- ✅ Context analysis operational
- ✅ Escalation detection working
- ✅ Temporal patterns identified
- ✅ Integration with ensemble complete
- ✅ Ready for pattern enhancement

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Context analysis validated
- [ ] Test coverage sufficient
- [ ] Ready to proceed to Phase 5

---

## 📝 **PHASE 6: MONITORING & CONTINUOUS IMPROVEMENT**

### **Status**: ⏳ **NOT STARTED** (Ongoing after Phase 4)

### **Duration**: Ongoing
### **Priority**: CONTINUOUS

### **Objectives**:
- Monitor production performance
- Collect real-world feedback
- Iterate on model performance
- Continuous optimization
- Community feedback integration

---

### **Step 6.1: Production Monitoring**

**Daily Tasks**:
- [ ] Review crisis detection metrics
- [ ] Monitor false positive/negative rates
- [ ] Check system performance
- [ ] Review errors and warnings
- [ ] Validate model health

---

### **Step 6.2: Model Performance Analysis**

**Weekly Tasks**:
- [ ] Analyze model accuracy
- [ ] Review edge cases
- [ ] Identify improvement areas
- [ ] Test model updates
- [ ] Document findings

---

### **Step 6.3: Community Feedback Integration**

**Monthly Tasks**:
- [ ] Collect community feedback
- [ ] Review missed crisis cases
- [ ] Update test datasets
- [ ] Enhance patterns
- [ ] Improve documentation

---

### **Step 6.4: Continuous Optimization**

**Quarterly Tasks**:
- [ ] Evaluate new models
- [ ] Update ensemble composition
- [ ] Optimize performance
- [ ] Enhance features
- [ ] Update documentation

---

## 🎯 **SUCCESS CRITERIA**

### **Phase Completion Criteria**:

**Phase 1**: Testing Framework
- ✅ Can test any model objectively
- ✅ Baseline performance documented
- ✅ Test datasets comprehensive

**Phase 2**: Model Migration
- ✅ All 4 models operational
- ✅ Performance within targets
- ✅ Improved over baseline

**Phase 3**: Ensemble/API Framework & Deployment
- ✅ Multi-model consensus working
- ✅ Explainability implemented
- ✅ Conflict resolution functional

**Phase 4**: History Analysis
- ✅ Escalation detection working
- ✅ Temporal patterns identified
- ✅ History tracking operational

**Phase 5**: Continuous Improvement
- ✅ Ongoing monitoring
- ✅ Regular optimization
- ✅ Community feedback integration

---

## 📊 **DEPENDENCIES & PREREQUISITES**

### **Phase Dependencies**:
```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
  ✅       ⏳        ⏳        ⏳        ⏳        ⏳
```

### **Technical Prerequisites**:
- **Server**: Debian 12, AMD Ryzen 7 5800x, 64GB RAM
- **GPU**: NVIDIA RTX 3060 12GB VRAM
- **Docker**: Latest version with GPU support
- **Python**: 3.9+
- **CUDA**: 12.2+

### **Software Dependencies**:
```
transformers==4.35.0
torch==2.1.0
fastapi==0.104.0
uvicorn==0.24.0
numpy==1.24.0
pandas==2.1.0
```

---

## 🔄 **ROLLBACK PROCEDURES**

### **If Phase Fails**:

**Testing Framework Issues (Phase 1)**:
- Rollback: Continue with v3.1 models
- Fix testing framework
- Re-baseline

**Model Migration Issues (Phase 2)**:
- Rollback: Keep v3.1 models
- Fix specific model
- Re-test

**Ensemble Issues (Phase 3)**:
- Rollback: Use single best model
- Fix consensus logic
- Re-test ensemble

**Context Issues (Phase 4)**:
- Rollback: Disable history analysis
- Fix context logic
- Re-enable

**Production Issues (Phase 5)**:
- Rollback: Redeploy v3.1
- Fix production issues
- Re-deploy v5.0

---

## 📈 **PROGRESS TRACKING**

### **Current Status**: Phase 0 Complete ✅

### **Phase Completion**:
- [x] Phase 0: Foundation & Planning - 100% ✅
- [x] Phase 1: Testing Framework - 0%
- [x] Phase 2: Model Migration - 0%
- [x] Phase 3: Ensemble/API & Deployment- 0%
- [ ] Phase 4: Context Analysis - 0%
- [ ] Phase 5: Continuous Improvement - 0%

### **Overall Progress**: 66.67% (4/6 phases complete)

---

## 💾 **VERSION CONTROL**

### **Document Version**: v5.0
### **Last Updated**: 2025-12-30
### **Last Updated By**: Project Team

### **Change Log**:
```
2025-12-30: Initial roadmap created (Phase 0 complete)
- Architecture decision documented
- Model selection finalized
- Comprehensive phase plan created
```

---

## 📞 **STAKEHOLDER COMMUNICATION**

### **Update Frequency**:
- **Daily**: Progress updates during active development
- **Weekly**: Phase completion reports
- **Monthly**: Overall project status

### **Escalation Path**:
1. Development Team
2. Project Lead
3. Community Leadership

---

## 🎓 **LEARNING & DOCUMENTATION**

### **Documentation Requirements**:
- [ ] Architecture diagrams
- [ ] API documentation
- [ ] Configuration guides
- [ ] Troubleshooting guides
- [ ] Runbooks
- [ ] Community guides

### **Knowledge Transfer**:
- [ ] Code review sessions
- [ ] Documentation reviews
- [ ] Training materials
- [ ] Community workshops

---

## 🏁 **FINAL NOTES**

This roadmap represents the complete plan for Ash-NLP v5.0 rewrite. It is designed to be:

1. **Comprehensive**: Covers all aspects of the rewrite
2. **Trackable**: Clear checkboxes and progress indicators
3. **Flexible**: Can adapt to changes and discoveries
4. **Collaborative**: Supports multi-conversation development
5. **Compliant**: Follows Clean Architecture Charter v5.0

**Remember**:
- ⚠️ Always update this roadmap as progress is made
- ⚠️ Document lessons learned in each phase
- ⚠️ Update checklist items as completed
- ⚠️ Communicate blockers immediately
- ⚠️ Maintain Clean Architecture compliance throughout

---

**Built with care for chosen family** 🏳️‍🌈
