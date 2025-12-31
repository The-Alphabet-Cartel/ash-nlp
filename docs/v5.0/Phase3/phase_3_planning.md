# Ash-NLP v5.0 Phase 3 Planning Document

**Document Version**: v5.0-3-PLAN  
**Created**: 2025-12-31  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [Website](https://alphabetcartel.org)

---

## Executive Summary

Phase 3 focuses on **Production Integration** - taking the validated multi-model ensemble from Phase 2 and integrating it into the live Ash-NLP system for real-time Discord crisis detection.

---

## Phase 3 Objectives

| Objective | Priority | Description |
|-----------|----------|-------------|
| Ensemble Integration | P0 | Implement weighted multi-model decision engine |
| API Endpoints | P0 | Create REST API for crisis detection |
| Production Docker | P0 | Production-ready containerization |
| Error Handling | P1 | Graceful degradation and fallbacks |
| Monitoring | P1 | Logging, metrics, and alerting |
| Performance Optimization | P2 | Batching, caching, response times |
| Documentation | P2 | API docs, deployment guides |

---

## Architecture Target

### Production System Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Ash Discord Bot                                  │
│                              │                                           │
│                              ▼                                           │
│                    ┌─────────────────┐                                   │
│                    │  Message Event  │                                   │
│                    └────────┬────────┘                                   │
│                              │                                           │
└──────────────────────────────┼───────────────────────────────────────────┘
                               │ HTTP POST /api/v1/analyze
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       Ash-NLP Container (Port 30880)                     │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                        API Gateway                                 │  │
│  │                    /api/v1/analyze                                 │  │
│  │                    /api/v1/health                                  │  │
│  │                    /api/v1/models                                  │  │
│  └──────────────────────────┬─────────────────────────────────────────┘  │
│                             │                                            │
│  ┌──────────────────────────▼─────────────────────────────────────────┐  │
│  │                    Ensemble Orchestrator                           │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                │  │
│  │  │  BART   │  │Sentiment│  │  Irony  │  │Emotions │                │  │
│  │  │  0.50   │  │  0.25   │  │  0.15   │  │  0.10   │                │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘                │  │
│  │       │            │            │            │                     │  │
│  │       └────────────┴─────┬──────┴────────────┘                     │  │
│  │                          ▼                                         │  │
│  │              ┌─────────────────────┐                               │  │
│  │              │  Decision Engine    │                               │  │
│  │              │  - Weighted scoring │                               │  │
│  │              │  - Confidence calc  │                               │  │
│  │              │  - Severity mapping │                               │  │
│  │              └──────────┬──────────┘                               │  │
│  └─────────────────────────┼──────────────────────────────────────────┘  │
│                            ▼                                             │
│                   ┌────────────────┐                                     │
│                   │  JSON Response │                                     │
│                   └────────────────┘                                     │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Deliverables

### 3.1 Ensemble Decision Engine

**File**: `src/ensemble/decision_engine.py`

```python
# Target Implementation
class EnsembleDecisionEngine:
    """
    Orchestrates multi-model inference and weighted decision making.
    """
    
    WEIGHTS = {
        "bart_crisis": 0.50,
        "cardiff_sentiment": 0.25,
        "cardiff_irony": 0.15,
        "roberta_emotions": 0.10
    }
    
    SEVERITY_THRESHOLDS = {
        "critical": 0.85,
        "high": 0.70,
        "medium": 0.50,
        "low": 0.30,
        "safe": 0.0
    }
    
    async def analyze(self, message: str) -> CrisisAssessment:
        """Run all models and return weighted assessment."""
        pass
    
    def calculate_confidence(self, results: dict) -> float:
        """Calculate ensemble confidence score."""
        pass
    
    def determine_severity(self, score: float, signals: dict) -> str:
        """Map score to severity level with signal boosting."""
        pass
```

**Tasks**:
- [ ] 3.1.1 Create EnsembleDecisionEngine class
- [ ] 3.1.2 Implement async model inference
- [ ] 3.1.3 Implement weighted scoring algorithm
- [ ] 3.1.4 Implement confidence calculation
- [ ] 3.1.5 Implement severity mapping with signal boosting
- [ ] 3.1.6 Add model fallback handling
- [ ] 3.1.7 Unit tests for decision engine

---

### 3.2 API Endpoints

**File**: `src/api/routes.py`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/analyze` | POST | Analyze message for crisis signals |
| `/api/v1/health` | GET | Health check and model status |
| `/api/v1/models` | GET | List loaded models and versions |

**Request Schema** (`/api/v1/analyze`):
```json
{
  "message": "string",
  "context": {
    "user_id": "string (optional)",
    "channel_id": "string (optional)",
    "previous_messages": ["string"] (optional)
  },
  "options": {
    "include_emotions": true,
    "include_confidence": true,
    "threshold_override": 0.0 (optional)
  }
}
```

**Response Schema**:
```json
{
  "crisis_detected": true,
  "severity": "critical|high|medium|low|safe",
  "confidence": 0.95,
  "crisis_score": 0.92,
  "signals": {
    "bart_crisis": {
      "label": "suicide ideation",
      "score": 0.94
    },
    "sentiment": {
      "label": "negative",
      "score": 0.89
    },
    "irony": {
      "label": "non_irony",
      "score": 0.97
    },
    "emotions": {
      "label": "grief",
      "score": 0.76
    }
  },
  "requires_intervention": true,
  "recommended_action": "immediate_outreach",
  "processing_time_ms": 45.2
}
```

**Tasks**:
- [ ] 3.2.1 Create FastAPI application structure
- [ ] 3.2.2 Implement `/api/v1/analyze` endpoint
- [ ] 3.2.3 Implement `/api/v1/health` endpoint
- [ ] 3.2.4 Implement `/api/v1/models` endpoint
- [ ] 3.2.5 Add request validation with Pydantic
- [ ] 3.2.6 Add rate limiting
- [ ] 3.2.7 API integration tests

---

### 3.3 Production Docker Configuration

**Files**:
- `Dockerfile` - Production container
- `docker-compose.yml` - Production orchestration

**Dockerfile Target**:
```dockerfile
# Multi-stage build for production
FROM python:3.11-slim AS builder
# Install dependencies
# ...

FROM nvidia/cuda:12.1-runtime-ubuntu22.04 AS production
# Copy only necessary files
# Optimized for size and security
# Health check included
# Non-root user
```

**Tasks**:
- [ ] 3.3.1 Create multi-stage production Dockerfile
- [ ] 3.3.2 Optimize image size (target < 5GB)
- [ ] 3.3.3 Implement non-root user
- [ ] 3.3.4 Add health check endpoint
- [ ] 3.3.5 Create production docker-compose.yml
- [ ] 3.3.6 Configure model caching/persistence
- [ ] 3.3.7 Add resource limits (memory, GPU)
- [ ] 3.3.8 Security hardening

---

### 3.4 Configuration Management

**File**: `config/production.json`

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 30880,
    "workers": 4,
    "timeout": 30
  },
  "models": {
    "bart_crisis": {
      "model_id": "facebook/bart-large-mnli",
      "weight": 0.50,
      "enabled": true,
      "cache_dir": "/models/bart"
    },
    "cardiff_sentiment": {
      "model_id": "cardiffnlp/twitter-roberta-base-sentiment-latest",
      "weight": 0.25,
      "enabled": true
    },
    "cardiff_irony": {
      "model_id": "cardiffnlp/twitter-roberta-base-irony",
      "weight": 0.15,
      "enabled": true
    },
    "roberta_emotions": {
      "model_id": "SamLowe/roberta-base-go_emotions",
      "weight": 0.10,
      "enabled": true
    }
  },
  "thresholds": {
    "critical": 0.85,
    "high": 0.70,
    "medium": 0.50,
    "low": 0.30
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "output": "/logs/ash-nlp.log"
  }
}
```

**Tasks**:
- [ ] 3.4.1 Create ConfigManager class
- [ ] 3.4.2 Implement environment variable overrides
- [ ] 3.4.3 Add configuration validation
- [ ] 3.4.4 Create config templates for dev/staging/prod
- [ ] 3.4.5 Document all configuration options

---

### 3.5 Error Handling & Fallbacks

**Strategy**: Graceful degradation if individual models fail

```python
class ModelFallbackStrategy:
    """
    If a model fails, adjust weights and continue.
    Only fail completely if BART (primary) fails.
    """
    
    def handle_model_failure(self, failed_model: str):
        if failed_model == "bart_crisis":
            raise CriticalModelFailure("Primary model unavailable")
        
        # Redistribute weight to remaining models
        remaining_weight = self.weights[failed_model]
        active_models = [m for m in self.weights if m != failed_model]
        redistribution = remaining_weight / len(active_models)
        
        for model in active_models:
            self.weights[model] += redistribution
```

**Tasks**:
- [ ] 3.5.1 Implement ModelFallbackStrategy
- [ ] 3.5.2 Add circuit breaker pattern
- [ ] 3.5.3 Implement retry logic with backoff
- [ ] 3.5.4 Add timeout handling
- [ ] 3.5.5 Create error response schemas
- [ ] 3.5.6 Add alerting for model failures

---

### 3.6 Monitoring & Logging

**Metrics to Track**:

| Metric | Type | Description |
|--------|------|-------------|
| `ash_nlp_requests_total` | Counter | Total API requests |
| `ash_nlp_crisis_detected_total` | Counter | Crisis detections by severity |
| `ash_nlp_inference_duration_seconds` | Histogram | Model inference latency |
| `ash_nlp_model_errors_total` | Counter | Model failures by type |
| `ash_nlp_gpu_memory_bytes` | Gauge | GPU memory usage |

**Logging Format** (JSON):
```json
{
  "timestamp": "2025-12-31T20:15:30.123Z",
  "level": "INFO",
  "service": "ash-nlp",
  "event": "crisis_detected",
  "severity": "critical",
  "confidence": 0.95,
  "processing_time_ms": 45.2,
  "trace_id": "abc123"
}
```

**Tasks**:
- [ ] 3.6.1 Implement structured JSON logging
- [ ] 3.6.2 Implement request tracing
- [ ] 3.6.3 Add performance profiling hooks
- [ ] 3.6.4 Create alerting rules

---

### 3.7 Performance Optimization

**Targets**:
- Single message: < 100ms p95
- Batch (10 messages): < 500ms p95
- Startup time: < 30 seconds
- Memory usage: < 8GB

**Optimization Strategies**:

| Strategy | Impact | Priority |
|----------|--------|----------|
| Model warmup on startup | High | P0 |
| Inference batching | High | P1 |
| Response caching (identical messages) | Medium | P2 |
| Async parallel inference | High | P0 |
| Model quantization (optional) | Medium | P3 |

**Tasks**:
- [ ] 3.7.1 Implement model warmup on startup
- [ ] 3.7.2 Add async parallel model inference
- [ ] 3.7.3 Implement request batching
- [ ] 3.7.4 Add response caching layer
- [ ] 3.7.5 Benchmark and profile
- [ ] 3.7.6 Optimize memory usage

---

## File Structure Target

```
ash-nlp/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py              # FastAPI application
│   │   ├── routes.py           # API endpoints
│   │   ├── schemas.py          # Pydantic models
│   │   └── middleware.py       # Logging, auth, rate limiting
│   │
│   ├── ensemble/
│   │   ├── __init__.py
│   │   ├── decision_engine.py  # Main orchestrator
│   │   ├── model_loader.py     # Model initialization
│   │   ├── fallback.py         # Error handling
│   │   └── scoring.py          # Weighted scoring logic
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bart_classifier.py  # BART wrapper
│   │   ├── sentiment.py        # Cardiff sentiment wrapper
│   │   ├── irony.py            # Cardiff irony wrapper
│   │   └── emotions.py         # RoBERTa emotions wrapper
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py          # Structured logging
│       ├── metrics.py          # Prometheus metrics
│       └── cache.py            # Response caching
│
├── config/
│   ├── default.json            # Default configuration
│   ├── production.json         # Production overrides
│   └── testing.json            # Testing configuration
│
├── managers/
│   └── config_manager.py       # Configuration management
│
├── testing/                    # FROM PHASE 2
│   ├── model_evaluator.py
│   ├── test_datasets/
│   └── reports/
│
├── docs/
│   ├── api.md                  # API documentation
│   ├── deployment.md           # Deployment guide
│   └── configuration.md        # Config reference
│
├── Dockerfile                  # Production container
├── Dockerfile.testing          # Testing container (Phase 2)
├── docker-compose.yml          # Production orchestration
├── docker-compose.testing.yml  # Testing orchestration
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
└── .env.example               # Environment template
```

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| API Response Time | < 100ms p95 | Performance tests |
| Crisis Detection Accuracy | 100% (critical) | Validation tests |
| Uptime | 99.9% | Monitoring |
| False Positive Rate | < 5% | Production metrics |
| Container Startup | < 30s | Deployment tests |
| Memory Usage | < 8GB | Resource monitoring |

---

## Timeline Estimate

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | Core Integration | 3.1, 3.4 - Decision engine + Config |
| 2 | API Development | 3.2 - All endpoints functional |
| 3 | Docker + Monitoring | 3.3, 3.6 - Production containers |
| 4 | Error Handling + Optimization | 3.5, 3.7 - Robustness |
| 5 | Testing + Documentation | Integration tests, docs |
| 6 | Staging Deployment | Deploy to staging, validation |

---

## Dependencies

### External
- HuggingFace Transformers 4.57+
- FastAPI 0.100+
- Docker with NVIDIA runtime
- Python 3.11+

### Internal
- Phase 2 test datasets (completed)
- Phase 2 model validation (completed)
- Ash Discord bot integration endpoint

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Model loading time | Medium | High | Pre-warm on startup, health checks |
| Memory exhaustion | Low | High | Resource limits, monitoring |
| API timeout | Medium | Medium | Async processing, timeouts |
| Model version drift | Low | Medium | Pinned versions, validation tests |
| GPU unavailability | Low | Critical | CPU fallback mode |

---

## Approval

| Role | Name | Approved | Date |
|------|------|----------|------|
| Development Lead | PapaBearDoes | ✅ | 31 Dec 2025 |
| Community Admin | Valkyrie | ✅ | 31 Dec 2025 |

---

*Built with care for chosen family* 🏳️‍🌈
