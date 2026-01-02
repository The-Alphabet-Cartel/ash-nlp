# Ash-NLP Phase 4: API Reference

**FILE VERSION:** v5.0-4-DOC-2.0  
**LAST MODIFIED:** 2026-01-01  
**Repository:** https://github.com/the-alphabet-cartel/ash-nlp  
**Community:** [The Alphabet Cartel](https://discord.gg/alphabetcartel) | https://alphabetcartel.org

---

## Table of Contents

1. [Analysis Endpoints](#analysis-endpoints)
2. [Configuration Endpoints](#configuration-endpoints)
3. [Health Endpoints](#health-endpoints)
4. [Request Schemas](#request-schemas)
5. [Response Schemas](#response-schemas)
6. [Enumerations](#enumerations)
7. [Error Handling](#error-handling)

---

## Analysis Endpoints

### POST /analyze

Analyze a single message for crisis signals with Phase 4 enhancements.

**Request:**

```json
{
  "message": "string (required, 1-10000 chars)",
  "user_id": "string (optional)",
  "channel_id": "string (optional)",
  "metadata": "object (optional)",
  "include_explanation": "boolean (default: true)",
  "verbosity": "minimal | standard | detailed (optional)",
  "consensus_algorithm": "weighted_voting | majority_voting | unanimous | conflict_aware (optional)"
}
```

**Response (200 OK):**

```json
{
  "crisis_detected": true,
  "severity": "critical | high | medium | low | safe",
  "confidence": 0.87,
  "crisis_score": 0.78,
  "requires_intervention": true,
  "recommended_action": "immediate_outreach | priority_response | standard_monitoring | passive_monitoring | none",
  "signals": {
    "bart": {
      "label": "suicide ideation",
      "score": 0.89,
      "crisis_signal": 0.89
    },
    "sentiment": {
      "label": "negative",
      "score": 0.85,
      "crisis_signal": 0.75
    }
  },
  "processing_time_ms": 145.32,
  "models_used": ["bart", "sentiment", "irony", "emotions"],
  "is_degraded": false,
  "request_id": "req_abc123",
  "timestamp": "2026-01-01T12:00:00Z",
  
  "explanation": {
    "verbosity": "standard",
    "decision_summary": "HIGH CONCERN: Crisis indicators detected with 87% confidence.",
    "key_factors": ["emotional distress", "negative sentiment"],
    "recommended_action": {
      "priority": "HIGH",
      "action": "Respond promptly with supportive outreach",
      "escalation": "Monitor for escalation",
      "rationale": "Crisis indicators detected requiring attention"
    },
    "plain_text": "DECISION SUMMARY:\n...",
    "confidence_summary": "High confidence (87%) based on 4 models",
    "model_contributions": [...],
    "conflict_summary": null
  },
  
  "consensus": {
    "algorithm": "weighted_voting",
    "crisis_score": 0.78,
    "confidence": 0.87,
    "agreement_level": "strong_agreement | moderate_agreement | weak_agreement | significant_disagreement",
    "is_crisis": true,
    "requires_review": false,
    "has_conflict": false,
    "individual_scores": {
      "bart": 0.89,
      "sentiment": 0.75,
      "irony": 0.95,
      "emotions": 0.70
    },
    "vote_breakdown": null
  },
  
  "conflict_analysis": {
    "has_conflicts": false,
    "conflict_count": 0,
    "conflicts": [],
    "highest_severity": null,
    "requires_review": false,
    "summary": "No conflicts detected",
    "resolution_strategy": null,
    "original_score": null,
    "resolved_score": null
  }
}
```

**Example cURL:**

```bash
curl -X POST "http://localhost:30880/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I dont know if I can keep going anymore",
    "include_explanation": true,
    "verbosity": "standard"
  }'
```

---

### POST /analyze/batch

Analyze multiple messages in a single request.

**Request:**

```json
{
  "messages": ["string", "string", ...],
  "include_details": false,
  "include_explanation": false
}
```

**Response (200 OK):**

```json
{
  "total_messages": 10,
  "crisis_count": 3,
  "critical_count": 1,
  "high_count": 2,
  "results": [
    {
      "index": 0,
      "message_preview": "First 50 chars of message...",
      "crisis_detected": true,
      "severity": "high",
      "crisis_score": 0.75,
      "requires_intervention": true,
      "explanation_summary": "HIGH CONCERN: Crisis indicators..."
    }
  ],
  "processing_time_ms": 1250.50,
  "request_id": "req_batch_123",
  "timestamp": "2026-01-01T12:00:00Z"
}
```

---

## Configuration Endpoints

### GET /config/consensus

Get current consensus algorithm configuration.

**Response (200 OK):**

```json
{
  "default_algorithm": "weighted_voting",
  "available_algorithms": [
    "weighted_voting",
    "majority_voting",
    "unanimous",
    "conflict_aware"
  ],
  "weights": {
    "bart": 0.50,
    "sentiment": 0.25,
    "irony": 0.15,
    "emotions": 0.10
  },
  "thresholds": {
    "crisis": 0.5,
    "majority": 0.5,
    "unanimous": 0.6,
    "disagreement": 0.15
  },
  "conflict_detection_enabled": true,
  "resolution_strategy": "conservative",
  "explainability_verbosity": "standard"
}
```

---

### PUT /config/consensus

Update consensus algorithm configuration. Changes take effect immediately.

**Request:**

```json
{
  "default_algorithm": "conflict_aware",
  "resolution_strategy": "review_flag",
  "explainability_verbosity": "detailed",
  "thresholds": {
    "crisis": 0.45,
    "disagreement": 0.20
  }
}
```

**Response (200 OK):**

Returns updated configuration (same schema as GET).

---

## Health Endpoints

### GET /health

Health check endpoint for load balancers.

**Response (200 OK / 503 Service Unavailable):**

```json
{
  "status": "healthy | degraded | unhealthy",
  "ready": true,
  "degraded": false,
  "models_loaded": 4,
  "total_models": 4,
  "uptime_seconds": 3600.5,
  "version": "v5.0-4-5.2-1",
  "phase4_enabled": true,
  "timestamp": "2026-01-01T12:00:00Z"
}
```

---

### GET /status

Detailed service status including Phase 4 components.

**Response (200 OK):**

```json
{
  "service": "ash-nlp",
  "version": "v5.0-4-5.2-1",
  "environment": "production",
  "status": "healthy",
  "ready": true,
  "degraded": false,
  "degradation_reason": null,
  "models": [
    {
      "name": "bart",
      "loaded": true,
      "enabled": true,
      "device": "cuda:0",
      "weight": 0.50,
      "average_latency_ms": 45.2
    }
  ],
  "stats": {
    "total_requests": 1500,
    "crisis_detections": 45,
    "conflicts_detected": 12,
    "cache_hits": 350,
    "cache_hit_rate": 0.2333,
    "average_latency_ms": 125.5
  },
  "config": {
    "weights": {...},
    "thresholds": {...},
    "async_inference": true
  },
  "phase4": {
    "enabled": true,
    "consensus_algorithm": "weighted_voting",
    "resolution_strategy": "conservative",
    "explainability_verbosity": "standard",
    "conflicts_detected": 12
  },
  "timestamp": "2026-01-01T12:00:00Z"
}
```

---

## Request Schemas

### AnalyzeRequest

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `message` | string | Yes | - | Message to analyze (1-10000 chars) |
| `user_id` | string | No | null | User identifier for tracking |
| `channel_id` | string | No | null | Channel identifier |
| `metadata` | object | No | null | Additional context |
| `include_explanation` | boolean | No | true | Include explanation in response |
| `verbosity` | string | No | null | Explanation verbosity level |
| `consensus_algorithm` | string | No | null | Override default consensus algorithm |

### ConsensusConfigUpdateRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `default_algorithm` | string | No | Set default consensus algorithm |
| `resolution_strategy` | string | No | Set conflict resolution strategy |
| `explainability_verbosity` | string | No | Set default verbosity |
| `thresholds` | object | No | Update threshold values |

---

## Response Schemas

### ExplanationResponse

| Field | Type | Verbosity | Description |
|-------|------|-----------|-------------|
| `verbosity` | string | All | Verbosity level used |
| `decision_summary` | string | All | Plain-English summary |
| `key_factors` | string[] | Standard+ | Primary crisis factors |
| `recommended_action` | object | Standard+ | Action recommendation |
| `plain_text` | string | All | Full plain-text explanation |
| `confidence_summary` | string | Detailed | Confidence explanation |
| `model_contributions` | object[] | Detailed | Per-model breakdown |
| `conflict_summary` | string | Detailed | Conflict summary if any |

### ConflictAnalysisResponse

| Field | Type | Description |
|-------|------|-------------|
| `has_conflicts` | boolean | Whether conflicts were detected |
| `conflict_count` | integer | Number of conflicts |
| `conflicts` | object[] | List of detected conflicts |
| `highest_severity` | string | Most severe conflict level |
| `requires_review` | boolean | Whether human review recommended |
| `summary` | string | Brief conflict summary |
| `resolution_strategy` | string | Strategy used (if resolved) |
| `original_score` | float | Score before resolution |
| `resolved_score` | float | Score after resolution |

### ConsensusResponse

| Field | Type | Description |
|-------|------|-------------|
| `algorithm` | string | Algorithm used |
| `crisis_score` | float | Consensus crisis score |
| `confidence` | float | Confidence in consensus |
| `agreement_level` | string | Model agreement level |
| `is_crisis` | boolean | Binary crisis determination |
| `requires_review` | boolean | Whether review recommended |
| `has_conflict` | boolean | Whether conflict detected |
| `individual_scores` | object | Per-model scores |
| `vote_breakdown` | object | Voting details (for voting algorithms) |

---

## Enumerations

### ConsensusAlgorithm

| Value | Description |
|-------|-------------|
| `weighted_voting` | Weight-based scoring (default) |
| `majority_voting` | Binary majority decision |
| `unanimous` | All models must agree |
| `conflict_aware` | Detect disagreements |

### ResolutionStrategy

| Value | Description |
|-------|-------------|
| `conservative` | Use highest crisis score (default) |
| `optimistic` | Use lowest crisis score |
| `mean` | Use average score |
| `review_flag` | Flag for human review |

### VerbosityLevel

| Value | Description |
|-------|-------------|
| `minimal` | Crisis level and score only |
| `standard` | Summary + key factors + recommendation |
| `detailed` | Full model breakdown |

### SeverityLevel

| Value | Threshold |
|-------|-----------|
| `critical` | ≥ 0.85 |
| `high` | ≥ 0.70 |
| `medium` | ≥ 0.50 |
| `low` | ≥ 0.30 |
| `safe` | < 0.30 |

### AgreementLevel

| Value | Description |
|-------|-------------|
| `strong_agreement` | Variance < 0.05 |
| `moderate_agreement` | Variance < 0.10 |
| `weak_agreement` | Variance < 0.15 |
| `significant_disagreement` | Variance ≥ 0.15 |

### ConflictType

| Value | Severity | Description |
|-------|----------|-------------|
| `score_disagreement` | HIGH | Max-min score > threshold |
| `irony_sentiment_conflict` | MEDIUM | Positive sentiment + irony |
| `emotion_crisis_mismatch` | MEDIUM | High crisis, no crisis emotions |
| `label_disagreement` | MEDIUM | Crisis label with positive sentiment |

### ConflictSeverity

| Value | Description |
|-------|-------------|
| `high` | Requires immediate attention |
| `medium` | Should be reviewed |
| `low` | Informational |

---

## Error Handling

### Error Response Schema

```json
{
  "error": "validation_error | internal_error | service_unavailable",
  "message": "Human-readable error message",
  "details": [
    {
      "code": "value_error",
      "message": "Message cannot be empty",
      "field": "message"
    }
  ],
  "request_id": "req_abc123",
  "timestamp": "2026-01-01T12:00:00Z"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Invalid request (validation error) |
| 404 | Resource not found |
| 500 | Internal server error |
| 503 | Service unavailable (not initialized) |

---

## Interactive Documentation

When the service is running, interactive API documentation is available at:

- **Swagger UI:** http://localhost:30880/docs
- **ReDoc:** http://localhost:30880/redoc

---

**Built with care for chosen family** 🏳️‍🌈
