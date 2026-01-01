# Ash-NLP API Documentation

**Version**: v5.0  
**Base URL**: `http://localhost:30880` (or `http://10.20.30.253:30880` on Lofn)  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Rate Limiting](#rate-limiting)
4. [Endpoints](#endpoints)
   - [Analysis](#analysis-endpoints)
   - [Health & Status](#health--status-endpoints)
   - [Models](#model-endpoints)
5. [Request/Response Schemas](#requestresponse-schemas)
6. [Error Handling](#error-handling)
7. [Examples](#examples)

---

## Overview

Ash-NLP is a crisis detection API that uses a multi-model ensemble to identify crisis signals in text messages. The API is designed for integration with Discord bots and other community moderation tools.

### Base Architecture

```
Message → [BART 0.50] → [Sentiment 0.25] → [Irony 0.15] → [Emotions 0.10] → Crisis Score
```

### Crisis Severity Levels

| Level | Score Range | Recommended Action |
|-------|-------------|-------------------|
| 🔴 CRITICAL | ≥ 0.85 | Immediate intervention |
| 🟠 HIGH | ≥ 0.70 | Priority response |
| 🟡 MEDIUM | ≥ 0.50 | Standard monitoring |
| 🟢 LOW | ≥ 0.30 | Passive monitoring |
| ⚪ SAFE | < 0.30 | No action needed |

### Interactive Documentation

- **Swagger UI**: http://localhost:30880/docs
- **ReDoc**: http://localhost:30880/redoc
- **OpenAPI Schema**: http://localhost:30880/openapi.json

---

## Authentication

Currently, Ash-NLP does not require authentication. For production deployments behind a reverse proxy, consider implementing:

- API key authentication via `X-API-Key` header
- OAuth2 / JWT tokens
- IP allowlisting

---

## Rate Limiting

Default rate limiting is enabled:

| Limit | Value |
|-------|-------|
| Requests per minute | 60 |
| Per client (IP-based) | Yes |
| Burst allowed | No |

### Rate Limit Headers

When rate limited, the response includes:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-Request-ID: req_abc123
```

### Rate Limit Response

```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Max 60 requests per minute.",
  "request_id": "req_abc123",
  "timestamp": "2025-12-31T12:00:00Z"
}
```

---

## Endpoints

### Analysis Endpoints

#### POST /analyze

Analyze a single message for crisis signals.

**Request**

```http
POST /analyze HTTP/1.1
Host: localhost:30880
Content-Type: application/json

{
  "message": "I don't know if I can keep going anymore",
  "user_id": "user_12345",
  "channel_id": "general",
  "metadata": {
    "source": "discord",
    "guild_id": "guild_67890"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | ✅ Yes | Text to analyze (1-10,000 chars) |
| `user_id` | string | No | Optional user identifier |
| `channel_id` | string | No | Optional channel identifier |
| `metadata` | object | No | Optional additional context |

**Response**

```json
{
  "crisis_detected": true,
  "severity": "high",
  "confidence": 0.87,
  "crisis_score": 0.78,
  "requires_intervention": true,
  "recommended_action": "priority_response",
  "signals": {
    "bart": {
      "label": "emotional distress",
      "score": 0.89,
      "crisis_signal": 0.89
    },
    "sentiment": {
      "label": "negative",
      "score": 0.92,
      "crisis_signal": 0.75
    },
    "irony": {
      "label": "non_irony",
      "score": 0.95,
      "crisis_signal": 0.95
    },
    "emotions": {
      "label": "sadness",
      "score": 0.78,
      "crisis_signal": 0.65
    }
  },
  "processing_time_ms": 125.32,
  "models_used": ["bart", "sentiment", "irony", "emotions"],
  "is_degraded": false,
  "request_id": "req_abc123def456",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `crisis_detected` | boolean | Whether crisis signals were detected |
| `severity` | string | Crisis severity level (critical/high/medium/low/safe) |
| `confidence` | float | Confidence in assessment (0.0-1.0) |
| `crisis_score` | float | Final weighted crisis score (0.0-1.0) |
| `requires_intervention` | boolean | True if severity is HIGH or CRITICAL |
| `recommended_action` | string | Suggested response action |
| `signals` | object | Individual model signals |
| `processing_time_ms` | float | Total processing time |
| `models_used` | array | Models that contributed to analysis |
| `is_degraded` | boolean | Whether service is in degraded mode |
| `request_id` | string | Unique request identifier |
| `timestamp` | string | Response timestamp (ISO 8601) |

**Recommended Actions**

| Action | Severity | Description |
|--------|----------|-------------|
| `immediate_outreach` | CRITICAL | Contact user immediately |
| `priority_response` | HIGH | Respond within minutes |
| `standard_monitoring` | MEDIUM | Add to watch list |
| `passive_monitoring` | LOW | Normal observation |
| `none` | SAFE | No action required |

---

#### POST /analyze/batch

Analyze multiple messages in a single request.

**Request**

```http
POST /analyze/batch HTTP/1.1
Host: localhost:30880
Content-Type: application/json

{
  "messages": [
    "I'm having a great day!",
    "Everything is falling apart",
    "Just finished lunch, it was okay"
  ],
  "include_details": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messages` | array | ✅ Yes | List of messages (1-100) |
| `include_details` | boolean | No | Include detailed signals (default: false) |

**Response**

```json
{
  "total_messages": 3,
  "crisis_count": 1,
  "critical_count": 0,
  "high_count": 1,
  "results": [
    {
      "index": 0,
      "message_preview": "I'm having a great day!",
      "crisis_detected": false,
      "severity": "safe",
      "crisis_score": 0.12,
      "requires_intervention": false
    },
    {
      "index": 1,
      "message_preview": "Everything is falling apart",
      "crisis_detected": true,
      "severity": "high",
      "crisis_score": 0.75,
      "requires_intervention": true
    },
    {
      "index": 2,
      "message_preview": "Just finished lunch, it was okay",
      "crisis_detected": false,
      "severity": "safe",
      "crisis_score": 0.08,
      "requires_intervention": false
    }
  ],
  "processing_time_ms": 425.67,
  "request_id": "req_batch_123",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

---

### Health & Status Endpoints

#### GET /health

Simple health check for load balancers.

**Response (Healthy)**

```http
HTTP/1.1 200 OK

{
  "status": "healthy",
  "ready": true,
  "degraded": false,
  "models_loaded": 4,
  "total_models": 4,
  "uptime_seconds": 3600.5,
  "version": "v5.0.0",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

**Response (Unhealthy)**

```http
HTTP/1.1 503 Service Unavailable

{
  "status": "unhealthy",
  "ready": false,
  "degraded": false,
  "models_loaded": 0,
  "total_models": 4,
  "version": "v5.0.0",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

| Status | HTTP Code | Description |
|--------|-----------|-------------|
| `healthy` | 200 | All systems operational |
| `degraded` | 200 | Some models unavailable |
| `unhealthy` | 503 | Service not ready |

---

#### GET /healthz

Kubernetes-style health check (alias for /health).

---

#### GET /ready

Readiness probe for Kubernetes.

**Response (Ready)**

```json
{
  "ready": true,
  "message": "Service is ready"
}
```

**Response (Not Ready)**

```http
HTTP/1.1 503 Service Unavailable

{
  "ready": false,
  "message": "Service not ready"
}
```

---

#### GET /status

Detailed service status information.

**Response**

```json
{
  "service": "ash-nlp",
  "version": "v5.0.0",
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
    },
    {
      "name": "sentiment",
      "loaded": true,
      "enabled": true,
      "device": "cuda:0",
      "weight": 0.25,
      "average_latency_ms": 12.5
    },
    {
      "name": "irony",
      "loaded": true,
      "enabled": true,
      "device": "cuda:0",
      "weight": 0.15,
      "average_latency_ms": 11.8
    },
    {
      "name": "emotions",
      "loaded": true,
      "enabled": true,
      "device": "cuda:0",
      "weight": 0.10,
      "average_latency_ms": 13.2
    }
  ],
  "stats": {
    "total_requests": 1523,
    "crisis_detections": 47,
    "average_latency_ms": 125.4
  },
  "config": {
    "weights": {
      "bart": 0.50,
      "sentiment": 0.25,
      "irony": 0.15,
      "emotions": 0.10
    },
    "thresholds": {
      "critical": 0.85,
      "high": 0.70,
      "medium": 0.50,
      "low": 0.30
    },
    "async_inference": true
  },
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

---

### Model Endpoints

#### GET /models

List all ensemble models.

**Response**

```json
[
  {
    "name": "bart",
    "loaded": true,
    "enabled": true,
    "device": "cuda:0",
    "weight": 0.50,
    "average_latency_ms": 45.2
  },
  {
    "name": "sentiment",
    "loaded": true,
    "enabled": true,
    "device": "cuda:0",
    "weight": 0.25,
    "average_latency_ms": 12.5
  },
  {
    "name": "irony",
    "loaded": true,
    "enabled": true,
    "device": "cuda:0",
    "weight": 0.15,
    "average_latency_ms": 11.8
  },
  {
    "name": "emotions",
    "loaded": true,
    "enabled": true,
    "device": "cuda:0",
    "weight": 0.10,
    "average_latency_ms": 13.2
  }
]
```

---

#### GET /models/{model_name}

Get details for a specific model.

**Request**

```http
GET /models/bart HTTP/1.1
Host: localhost:30880
```

**Response**

```json
{
  "name": "bart",
  "loaded": true,
  "enabled": true,
  "device": "cuda:0",
  "weight": 0.50,
  "average_latency_ms": 45.2
}
```

**Error Response (404)**

```json
{
  "detail": "Model 'invalid_model' not found"
}
```

---

## Request/Response Schemas

### AnalyzeRequest

```json
{
  "type": "object",
  "required": ["message"],
  "properties": {
    "message": {
      "type": "string",
      "minLength": 1,
      "maxLength": 10000,
      "description": "Text message to analyze"
    },
    "user_id": {
      "type": "string",
      "maxLength": 100,
      "description": "Optional user identifier"
    },
    "channel_id": {
      "type": "string",
      "maxLength": 100,
      "description": "Optional channel identifier"
    },
    "metadata": {
      "type": "object",
      "description": "Optional additional context"
    }
  }
}
```

### AnalyzeResponse

```json
{
  "type": "object",
  "properties": {
    "crisis_detected": {"type": "boolean"},
    "severity": {"type": "string", "enum": ["critical", "high", "medium", "low", "safe"]},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "crisis_score": {"type": "number", "minimum": 0, "maximum": 1},
    "requires_intervention": {"type": "boolean"},
    "recommended_action": {
      "type": "string",
      "enum": ["immediate_outreach", "priority_response", "standard_monitoring", "passive_monitoring", "none"]
    },
    "signals": {"type": "object"},
    "processing_time_ms": {"type": "number"},
    "models_used": {"type": "array", "items": {"type": "string"}},
    "is_degraded": {"type": "boolean"},
    "request_id": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"}
  }
}
```

### SeverityLevel Enum

```
critical | high | medium | low | safe
```

### HealthStatus Enum

```
healthy | degraded | unhealthy
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "error_type",
  "message": "Human-readable error message",
  "details": [
    {
      "code": "error_code",
      "message": "Specific error detail",
      "field": "field_name"
    }
  ],
  "request_id": "req_abc123",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

### HTTP Status Codes

| Code | Description | When |
|------|-------------|------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Malformed request body |
| 422 | Validation Error | Request validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Service not ready |

### Common Errors

**Validation Error (422)**

```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": [
    {
      "code": "value_error",
      "message": "Message cannot be empty or whitespace only",
      "field": "message"
    }
  ],
  "request_id": "req_abc123",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

**Service Unavailable (503)**

```json
{
  "error": "service_unavailable",
  "message": "Service not initialized",
  "request_id": "req_abc123",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

---

## Examples

### cURL Examples

**Basic Analysis**

```bash
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling overwhelmed and anxious"}'
```

**With Metadata**

```bash
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I dont know what to do anymore",
    "user_id": "user_123",
    "channel_id": "support",
    "metadata": {"source": "discord"}
  }'
```

**Batch Analysis**

```bash
curl -X POST http://localhost:30880/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "Having a great time!",
      "I feel so alone",
      "Anyone want to play games?"
    ]
  }'
```

**Health Check**

```bash
curl http://localhost:30880/health
```

**Detailed Status**

```bash
curl http://localhost:30880/status | jq
```

### Python Examples

**Using requests**

```python
import requests

# Analyze a message
response = requests.post(
    "http://localhost:30880/analyze",
    json={"message": "I'm struggling today"}
)

result = response.json()
if result["crisis_detected"]:
    print(f"Crisis detected! Severity: {result['severity']}")
    print(f"Recommended action: {result['recommended_action']}")
```

**Using httpx (async)**

```python
import httpx
import asyncio

async def analyze_message(message: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:30880/analyze",
            json={"message": message}
        )
        return response.json()

result = asyncio.run(analyze_message("I need help"))
print(result)
```

### JavaScript Examples

**Using fetch**

```javascript
async function analyzeMessage(message) {
  const response = await fetch('http://localhost:30880/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });
  
  return response.json();
}

analyzeMessage("I'm feeling down today")
  .then(result => {
    if (result.crisis_detected) {
      console.log(`Alert: ${result.severity} severity detected`);
    }
  });
```

---

## Request Headers

### Standard Headers

| Header | Value | Description |
|--------|-------|-------------|
| `Content-Type` | `application/json` | Required for POST requests |
| `Accept` | `application/json` | Optional, default response format |
| `X-Request-ID` | `string` | Optional custom request ID |

### Response Headers

| Header | Description |
|--------|-------------|
| `X-Request-ID` | Unique request identifier |
| `Content-Type` | Response content type |
| `Retry-After` | Seconds until rate limit resets (on 429) |

---

## Webhooks (Future)

*Coming in future release*

Crisis alerts can be sent to configured webhook endpoints:

```json
{
  "alert_type": "crisis_detected",
  "severity": "critical",
  "crisis_score": 0.92,
  "confidence": 0.89,
  "recommended_action": "immediate_outreach",
  "message_preview": "I don't know if I can...",
  "user_id": "user_123",
  "channel_id": "general",
  "request_id": "req_abc123",
  "timestamp": "2025-12-31T12:00:00.000Z"
}
```

---

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Website**: [alphabetcartel.org](https://alphabetcartel.org)

---

**Built with care for chosen family** 🏳️‍🌈
