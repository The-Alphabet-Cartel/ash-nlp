# Ash-NLP API Response Documentation

**FILE VERSION**: v5.0  
**LAST UPDATED**: 2026-01-02  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## Overview

This document describes the JSON response structure returned by the Ash-NLP `/analyze` endpoint. The response provides comprehensive crisis assessment data from the multi-model ensemble system.

---

## Quick Reference

```
POST /analyze
Content-Type: application/json

Request:  { "message": "string", "user_id"?: "string", "channel_id"?: "string" }
Response: CrisisAssessmentResponse (documented below)
```

---

## Response Structure

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `crisis_detected` | boolean | Whether a crisis situation was detected |
| `severity` | string | Crisis severity level: `critical`, `high`, `medium`, `low`, `safe` |
| `confidence` | float | Model agreement confidence (0.0-1.0). Lower values indicate model disagreement |
| `crisis_score` | float | Final crisis score after conflict resolution (0.0-1.0) |
| `requires_intervention` | boolean | Whether human intervention is recommended |
| `recommended_action` | string | Suggested action: `immediate_outreach`, `priority_response`, `standard_monitoring`, `passive_monitoring`, `none` |
| `processing_time_ms` | float | Total processing time in milliseconds |
| `models_used` | array | List of models that contributed to the assessment |
| `is_degraded` | boolean | Whether the system is operating in degraded mode (model failures) |
| `request_id` | string | Unique identifier for this request |
| `timestamp` | string | ISO-8601 timestamp of the analysis |

### Severity Levels

| Level | Score Range | Description | Action |
|-------|-------------|-------------|--------|
| `critical` | ≥ 0.85 | Immediate danger indicators | Immediate outreach required |
| `high` | ≥ 0.70 | Significant distress signals | Priority response needed |
| `medium` | ≥ 0.50 | Moderate concern indicators | Standard monitoring |
| `low` | ≥ 0.30 | Minor concern signals | Passive monitoring |
| `safe` | < 0.30 | No crisis indicators | No action needed |

---

## Model Signals

The `signals` object contains individual results from each model in the ensemble.

```json
"signals": {
  "bart": { "label": "string", "score": float, "crisis_signal": float },
  "sentiment": { "label": "string", "score": float, "crisis_signal": float },
  "irony": { "label": "string", "score": float, "crisis_signal": float },
  "emotions": { "label": "string", "score": float, "crisis_signal": float }
}
```

### Model Descriptions

| Model | Role | Weight | Purpose |
|-------|------|--------|---------|
| **bart** | Primary | 0.50 | Zero-shot crisis classification (suicide ideation, emotional distress, etc.) |
| **sentiment** | Secondary | 0.25 | Sentiment analysis (positive, negative, neutral) |
| **irony** | Tertiary | 0.15 | Irony/sarcasm detection to reduce false positives |
| **emotions** | Supplementary | 0.10 | Emotion classification (sadness, fear, anger, joy, etc.) |

### Signal Fields

| Field | Description |
|-------|-------------|
| `label` | The classification label from the model |
| `score` | Raw model confidence score (0.0-1.0) |
| `crisis_signal` | Transformed crisis relevance score (0.0-1.0) |

### BART Crisis Labels

The BART model classifies messages into these categories:
- `suicide ideation` - Direct or indirect suicidal thoughts
- `emotional distress` - Significant emotional pain or suffering
- `self-harm` - References to self-injury
- `hopelessness` - Expressions of despair or giving up
- `casual conversation` - Normal, non-crisis communication
- `positive sharing` - Positive emotional expression
- `seeking support` - Asking for help (non-crisis)

---

## Explanation

The `explanation` object provides human-readable interpretation of the assessment.

```json
"explanation": {
  "verbosity": "standard",
  "decision_summary": "string",
  "key_factors": ["string"],
  "recommended_action": {
    "priority": "string",
    "action": "string",
    "escalation": "string",
    "rationale": "string"
  },
  "plain_text": "string",
  "confidence_summary": "string|null",
  "model_contributions": "array|null",
  "conflict_summary": "string|null"
}
```

### Verbosity Levels

| Level | Contents |
|-------|----------|
| `minimal` | Decision summary only |
| `standard` | Summary + key factors + recommended action |
| `detailed` | Full breakdown including model contributions and confidence analysis |

### Recommended Action Object

| Field | Description |
|-------|-------------|
| `priority` | `IMMEDIATE`, `HIGH`, `STANDARD`, `LOW`, `NONE` |
| `action` | Specific action to take |
| `escalation` | Whether/how to escalate |
| `rationale` | Reasoning behind the recommendation |

---

## Conflict Analysis

The `conflict_analysis` object describes disagreements between models and how they were resolved.

```json
"conflict_analysis": {
  "has_conflicts": boolean,
  "conflict_count": integer,
  "conflicts": [ConflictObject],
  "highest_severity": "string|null",
  "requires_review": boolean,
  "summary": "string",
  "resolution_strategy": "string",
  "original_score": float,
  "resolved_score": float
}
```

### Conflict Types

| Type | Description |
|------|-------------|
| `score_disagreement` | Large gap between model crisis signals |
| `irony_sentiment_conflict` | Irony detected with negative sentiment (possible sarcasm) |
| `emotion_crisis_mismatch` | High crisis score but non-crisis emotions detected |
| `label_disagreement` | Models disagree on classification labels |

### Conflict Severity

| Severity | Description |
|----------|-------------|
| `high` | Significant disagreement requiring human review |
| `medium` | Moderate disagreement, review recommended |
| `low` | Minor disagreement, informational only |

### Resolution Strategies

| Strategy | Description |
|----------|-------------|
| `conservative` | Use highest crisis score (default - errs on side of caution) |
| `optimistic` | Use lowest crisis score |
| `mean` | Use average of all scores |
| `review_flag` | Use conservative but always flag for review |

---

## Consensus

The `consensus` object shows how the weighted voting algorithm reached its decision.

```json
"consensus": {
  "algorithm": "weighted_voting",
  "crisis_score": float,
  "confidence": float,
  "agreement_level": "string",
  "is_crisis": boolean,
  "requires_review": boolean,
  "has_conflict": boolean,
  "individual_scores": { "model": float },
  "vote_breakdown": {
    "total_weight": float,
    "weighted_sum": float
  }
}
```

### Agreement Levels

| Level | Variance | Description |
|-------|----------|-------------|
| `strong_agreement` | < 0.05 | Models highly aligned |
| `moderate_agreement` | < 0.15 | Models generally aligned |
| `weak_agreement` | < 0.25 | Some disagreement present |
| `significant_disagreement` | ≥ 0.25 | Major model disagreement |

### Consensus Algorithm

The weighted voting formula:

```
crisis_score = Σ(signal_i × weight_i) / Σ(weight_i)
```

Where default weights are:
- BART: 0.50 (primary)
- Sentiment: 0.25 (secondary)
- Irony: 0.15 (tertiary)
- Emotions: 0.10 (supplementary)

---

## Context Analysis (Phase 5)

The `context_analysis` object provides temporal and escalation analysis when message history is available.

```json
"context_analysis": {
  "escalation_detected": boolean,
  "escalation_rate": "string",
  "escalation_pattern": "string|null",
  "pattern_confidence": float,
  "trend": {
    "direction": "string",
    "velocity": "string",
    "score_delta": float,
    "time_span_hours": float
  },
  "temporal_factors": {
    "late_night_risk": boolean,
    "rapid_posting": boolean,
    "time_risk_modifier": float,
    "hour_of_day": integer,
    "is_weekend": boolean
  },
  "trajectory": {
    "start_score": float,
    "end_score": float,
    "peak_score": float,
    "scores": [float]
  },
  "intervention": {
    "urgency": "string",
    "recommended_point": "string|null",
    "intervention_delayed": boolean,
    "reason": "string"
  },
  "history_analyzed": {
    "message_count": integer,
    "time_span_hours": float,
    "oldest_timestamp": "string|null",
    "newest_timestamp": "string|null"
  }
}
```

### Escalation Rates

| Rate | Description |
|------|-------------|
| `rapid` | Fast escalation (> 0.3 score increase per hour) |
| `gradual` | Slow escalation (0.1-0.3 per hour) |
| `stable` | No significant change |
| `improving` | Crisis indicators decreasing |
| `none` | No history to analyze |

### Escalation Patterns

| Pattern | Description |
|---------|-------------|
| `linear` | Steady increase over time |
| `exponential` | Accelerating increase |
| `spike` | Sudden jump in crisis score |
| `plateau` | Elevated but stable |
| `oscillating` | Fluctuating up and down |

### Trend Directions

| Direction | Description |
|-----------|-------------|
| `escalating` | Crisis indicators increasing |
| `stable` | No significant change |
| `improving` | Crisis indicators decreasing |

### Intervention Urgency

| Urgency | Description |
|---------|-------------|
| `critical` | Immediate intervention required |
| `high` | Intervention needed soon |
| `moderate` | Standard response appropriate |
| `low` | Monitoring sufficient |
| `none` | No intervention needed |

### Temporal Risk Factors

| Factor | Description |
|--------|-------------|
| `late_night_risk` | Message sent between 11 PM - 5 AM (higher risk period) |
| `rapid_posting` | Multiple messages in short time span |
| `time_risk_modifier` | Multiplier applied to score (1.0 = no modification, 1.2 = 20% increase) |

---

## Example Response

See `docs/sample_analyze_response.json` for a complete example of a critical crisis detection response.

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Successful analysis |
| `422` | Validation error (empty message, too long, etc.) |
| `500` | Internal server error |
| `503` | Service unavailable (models not loaded) |

---

## Rate Limiting

The API includes rate limiting headers:

| Header | Description |
|--------|-------------|
| `X-Request-ID` | Unique request identifier |
| `X-RateLimit-Limit` | Maximum requests per window |
| `X-RateLimit-Remaining` | Remaining requests in window |
| `X-RateLimit-Reset` | Window reset timestamp |

---

## Integration Notes

### For Discord Bots

When integrating with a Discord bot:

1. **Check `crisis_detected`** first for quick filtering
2. **Use `severity`** to determine response urgency
3. **Check `requires_intervention`** to decide on alerting moderators
4. **Include `request_id`** in logs for troubleshooting
5. **Monitor `is_degraded`** for system health alerts

### Recommended Response Flow

```
if crisis_detected:
    if severity == "critical":
        → Immediate moderator alert
        → DM user with crisis resources
    elif severity == "high":
        → Priority moderator queue
        → Monitor user activity
    elif severity == "medium":
        → Standard monitoring
        → Log for review
    else:
        → Passive monitoring
else:
    → No action needed
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v5.0 | 2026-01-02 | Added Phase 5 context analysis, conflict resolution, consensus algorithms |
| v4.0 | 2025-12-30 | Added explanation layer, conflict detection |
| v3.0 | 2025-12-28 | Initial multi-model ensemble release |

---

**Built with care for chosen family** 🏳️‍🌈
