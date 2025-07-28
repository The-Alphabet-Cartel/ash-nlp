# Ash NLP Server - API Documentation v2.1

**Complete REST API Reference for Advanced Crisis Detection NLP Processing**

Part of The Alphabet Cartel's [Ash Crisis Detection & Community Support Ecosystem](https://github.com/the-alphabet-cartel/ash)

---

## 🌐 API Overview

The Ash NLP Server provides a comprehensive REST API for real-time crisis detection, machine learning feedback, and system monitoring. The API is designed for high-performance integration with Discord bots, analytics dashboards, and testing suites.

### Base Configuration
- **Base URL**: `http://10.20.30.16:8881`
- **API Version**: v2.1
- **Content-Type**: `application/json`
- **Authentication**: Not required (internal network only)
- **Rate Limiting**: 1000 requests/minute per client
- **Timeout**: 30 seconds

### API Principles
- **Performance First**: Sub-200ms response times for analysis endpoints
- **Reliability**: 99.5% uptime with graceful error handling
- **Privacy**: No persistent message storage, ephemeral processing only
- **Learning**: Continuous improvement through feedback integration

## 🔌 Core Endpoints

### Health & Status

#### GET /health
**Purpose**: System health check and service status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-27T15:30:45Z",
  "version": "2.1.1",
  "uptime_seconds": 8645,
  "services": {
    "nlp_engine": "operational",
    "learning_system": "operational",
    "gpu": "available",
    "model_cache": "loaded"
  },
  "performance": {
    "average_response_time_ms": 145,
    "requests_per_minute": 127,
    "gpu_utilization_percent": 23,
    "memory_usage_mb": 4096
  }
}
```

**Status Codes**:
- `200`: System healthy and operational
- `503`: System unhealthy or degraded performance

---

#### GET /model_status
**Purpose**: Detailed AI model status and capabilities

**Response**:
```json
{
  "models": {
    "depression_model": {
      "name": "rafalposwiata/deproberta-large-depression",
      "status": "loaded",
      "version": "1.0",
      "load_time_ms": 2341,
      "memory_usage_mb": 1534,
      "last_inference": "2025-07-27T15:29:12Z"
    },
    "sentiment_model": {
      "name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
      "status": "loaded",
      "version": "2023.12",
      "load_time_ms": 1876,
      "memory_usage_mb": 892,
      "last_inference": "2025-07-27T15:29:12Z"
    }
  },
  "ensemble": {
    "status": "operational",
    "calibration_version": "2.1.0",
    "last_calibration": "2025-07-25T08:00:00Z"
  },
  "learning_system": {
    "status": "active",
    "adjustments_today": 23,
    "total_adjustments": 1547,
    "last_learning_update": "2025-07-27T14:45:30Z"
  }
}
```

---

### Message Analysis

#### POST /analyze
**Purpose**: Analyze message content for crisis indicators

**Request Body**:
```json
{
  "message": "feeling really down today, nothing seems to matter anymore",
  "user_id": "123456789012345678",
  "channel_id": "987654321098765432",
  "context": {
    "previous_messages": [
      {
        "message": "had a rough day at work",
        "timestamp": "2025-07-27T14:30:00Z"
      }
    ],
    "user_history": {
      "recent_mood": "declining",
      "previous_detections": ["medium_crisis"]
    }
  },
  "metadata": {
    "timestamp": "2025-07-27T15:30:45Z",
    "channel_type": "text",
    "guild_id": "456789012345678901"
  }
}
```

**Request Parameters**:
- `message` (string, required): Message content to analyze
- `user_id` (string, required): Discord user ID for context
- `channel_id` (string, required): Discord channel ID for context
- `context` (object, optional): Additional context for analysis
- `metadata` (object, optional): Additional metadata for logging

**Response**:
```json
{
  "risk_level": "medium",
  "confidence": 0.78,
  "analysis": {
    "depression_score": 0.65,
    "sentiment_score": -0.42,
    "crisis_indicators": [
      "mood_negative",
      "hopelessness",
      "existential_concern"
    ],
    "protective_factors": [
      "social_engagement",
      "future_orientation"
    ]
  },
  "recommendations": [
    "close_monitoring",
    "check_in_6h",
    "peer_support"
  ],
  "thresholds": {
    "high_crisis": 0.50,
    "medium_crisis": 0.22,
    "low_crisis": 0.12
  },
  "processing": {
    "time_ms": 147,
    "model_versions": {
      "depression": "1.0",
      "sentiment": "2023.12"
    },
    "learning_applied": true
  },
  "metadata": {
    "analysis_id": "nlp_20250727_153045_abc123",
    "timestamp": "2025-07-27T15:30:45Z",
    "server_id": "nlp-server-01"
  }
}
```

**Risk Level Classifications**:
- `high`: Score ≥ 0.50 (Immediate intervention required)
- `medium`: Score ≥ 0.22 (Close monitoring needed)
- `low`: Score ≥ 0.12 (Supportive check-in)
- `none`: Score < 0.12 (No crisis indicators detected)

**Status Codes**:
- `200`: Analysis completed successfully
- `400`: Invalid request format or missing required fields
- `422`: Unable to process message content
- `503`: NLP service temporarily unavailable

---

#### POST /analyze_batch
**Purpose**: Analyze multiple messages in a single request for improved performance

**Request Body**:
```json
{
  "messages": [
    {
      "id": "msg_001",
      "message": "feeling down today",
      "user_id": "123456789012345678",
      "channel_id": "987654321098765432"
    },
    {
      "id": "msg_002", 
      "message": "this game is frustrating",
      "user_id": "234567890123456789",
      "channel_id": "987654321098765432"
    }
  ],
  "options": {
    "include_low_priority": false,
    "max_processing_time_ms": 5000
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "id": "msg_001",
      "risk_level": "medium",
      "confidence": 0.65,
      "analysis": { /* ... */ }
    },
    {
      "id": "msg_002",
      "risk_level": "none",
      "confidence": 0.05,
      "analysis": { /* ... */ }
    }
  ],
  "summary": {
    "total_processed": 2,
    "high_risk_count": 0,
    "medium_risk_count": 1,
    "low_risk_count": 0,
    "processing_time_ms": 234
  }
}
```

---

### Learning & Feedback

#### POST /learning_feedback
**Purpose**: Provide feedback to improve detection accuracy

**Request Body**:
```json
{
  "analysis_id": "nlp_20250727_153045_abc123",
  "feedback_type": "false_positive",
  "correct_classification": "low",
  "message_content": "feeling really down today",
  "user_context": {
    "user_id": "123456789012345678",
    "typical_communication_style": "expressive",
    "gaming_context": true
  },
  "team_notes": "User was discussing game difficulty, not personal crisis",
  "submitted_by": "crisis_team_member_001"
}
```

**Feedback Types**:
- `false_positive`: System incorrectly flagged non-crisis message
- `false_negative`: System missed actual crisis message
- `severity_adjustment`: Correct detection but wrong severity level
- `correct_classification`: Confirmation that detection was accurate

**Response**:
```json
{
  "feedback_id": "fb_20250727_153100_xyz789",
  "status": "accepted",
  "learning_impact": {
    "adjustment_applied": true,
    "confidence_delta": -0.15,
    "affected_similar_patterns": 127
  },
  "processing_time_ms": 45,
  "next_model_update": "2025-07-27T16:00:00Z"
}
```

**Status Codes**:
- `200`: Feedback processed successfully
- `400`: Invalid feedback format
- `404`: Analysis ID not found
- `409`: Conflicting feedback already exists

---

#### GET /learning_statistics
**Purpose**: Retrieve learning system performance and statistics

**Response**:
```json
{
  "learning_system": {
    "status": "active",
    "version": "2.1.0",
    "enabled_features": [
      "real_time_adjustment",
      "pattern_recognition",
      "severity_calibration"
    ]
  },
  "feedback_stats": {
    "total_feedback_received": 1547,
    "feedback_today": 23,
    "feedback_types": {
      "false_positive": 812,
      "false_negative": 156,
      "severity_adjustment": 445,
      "correct_classification": 134
    }
  },
  "learning_impact": {
    "accuracy_improvement": 0.12,
    "false_positive_reduction": 0.08,
    "confidence_calibration": 0.94
  },
  "recent_adjustments": [
    {
      "timestamp": "2025-07-27T14:45:30Z",
      "pattern": "gaming_frustration_vs_crisis",
      "adjustment_type": "threshold_reduction",
      "impact_score": 0.03
    }
  ]
}
```

---

### Performance & Analytics

#### GET /performance_metrics
**Purpose**: Detailed performance metrics for monitoring and optimization

**Query Parameters**:
- `timeframe` (string, optional): `hour`, `day`, `week`, `month` (default: `hour`)
- `include_breakdown` (boolean, optional): Include detailed breakdowns (default: `false`)

**Response**:
```json
{
  "timeframe": "hour",
  "timestamp": "2025-07-27T15:30:45Z",
  "performance": {
    "requests": {
      "total": 1247,
      "successful": 1243,
      "failed": 4,
      "success_rate": 0.997
    },
    "response_times": {
      "average_ms": 145,
      "median_ms": 132,
      "p95_ms": 287,
      "p99_ms": 445,
      "max_ms": 892
    },
    "accuracy": {
      "overall": 0.87,
      "high_crisis_detection": 0.96,
      "false_positive_rate": 0.062,
      "false_negative_rate": 0.024
    },
    "resource_usage": {
      "cpu_percent": 23,
      "memory_mb": 4096,
      "gpu_utilization": 0.23,
      "gpu_memory_mb": 3200
    }
  },
  "trends": {
    "accuracy_trend": "improving",
    "performance_trend": "stable",
    "load_trend": "increasing"
  }
}
```

---

#### GET /analytics_export
**Purpose**: Export analytics data for dashboard integration

**Query Parameters**:
- `format` (string, optional): `json`, `csv` (default: `json`)
- `start_time` (string, optional): ISO 8601 timestamp
- `end_time` (string, optional): ISO 8601 timestamp
- `categories` (array, optional): Categories to include

**Response**:
```json
{
  "export_info": {
    "generated_at": "2025-07-27T15:30:45Z",
    "timeframe": {
      "start": "2025-07-27T14:30:45Z",
      "end": "2025-07-27T15:30:45Z"
    },
    "total_records": 1247
  },
  "detection_summary": {
    "high_crisis": 12,
    "medium_crisis": 45,
    "low_crisis": 89,
    "no_crisis": 1101
  },
  "performance_summary": {
    "average_response_time": 145,
    "accuracy_rate": 0.87,
    "total_processing_time": 180815
  },
  "learning_activity": {
    "feedback_received": 23,
    "adjustments_applied": 8,
    "patterns_updated": 15
  }
}
```

---

## 🔧 Advanced Features

### Contextual Analysis

#### POST /analyze_conversation
**Purpose**: Analyze entire conversation context for improved accuracy

**Request Body**:
```json
{
  "conversation": [
    {
      "message": "having a really tough day",
      "user_id": "123456789012345678",
      "timestamp": "2025-07-27T14:00:00Z"
    },
    {
      "message": "yeah work has been brutal lately",
      "user_id": "123456789012345678", 
      "timestamp": "2025-07-27T14:15:00Z"
    },
    {
      "message": "honestly don't know how much more I can take",
      "user_id": "123456789012345678",
      "timestamp": "2025-07-27T14:30:00Z"
    }
  ],
  "analysis_options": {
    "context_window": 10,
    "weight_recent_messages": true,
    "include_emotional_trajectory": true
  }
}
```

**Response**:
```json
{
  "conversation_analysis": {
    "overall_risk_level": "medium",
    "trajectory": "escalating",
    "confidence": 0.82,
    "key_indicators": [
      "stress_accumulation",
      "capacity_concern",
      "escalation_pattern"
    ]
  },
  "individual_messages": [
    {
      "message_index": 0,
      "risk_level": "low",
      "confidence": 0.34
    },
    {
      "message_index": 1,
      "risk_level": "low", 
      "confidence": 0.28
    },
    {
      "message_index": 2,
      "risk_level": "medium",
      "confidence": 0.67
    }
  ],
  "recommendations": [
    "immediate_check_in",
    "monitor_for_escalation",
    "provide_stress_resources"
  ]
}
```

---

### Model Management

#### POST /model_update
**Purpose**: Trigger model updates or refresh model cache

**Request Body**:
```json
{
  "action": "refresh_cache",
  "models": ["depression", "sentiment"],
  "force_reload": false
}
```

**Actions Available**:
- `refresh_cache`: Reload models from cache
- `update_models`: Download latest model versions
- `calibrate_ensemble`: Recalibrate ensemble scoring
- `reset_learning`: Reset learning adjustments (admin only)

**Response**:
```json
{
  "status": "completed",
  "actions_performed": [
    {
      "action": "refresh_cache",
      "model": "depression",
      "duration_ms": 2341,
      "success": true
    },
    {
      "action": "refresh_cache", 
      "model": "sentiment",
      "duration_ms": 1876,
      "success": true
    }
  ],
  "new_status": {
    "all_models_loaded": true,
    "ensemble_ready": true,
    "estimated_warmup_time": 0
  }
}
```

---

## 📊 Response Formats & Data Types

### Standard Response Structure

All API responses follow this consistent structure:

```json
{
  "data": { /* Response payload */ },
  "metadata": {
    "timestamp": "2025-07-27T15:30:45Z",
    "request_id": "req_20250727_153045_abc123",
    "processing_time_ms": 145,
    "server_id": "nlp-server-01",
    "api_version": "2.1"
  },
  "status": "success"
}
```

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Required field 'message' is missing",
    "details": {
      "field": "message",
      "expected_type": "string",
      "received": null
    }
  },
  "metadata": {
    "timestamp": "2025-07-27T15:30:45Z",
    "request_id": "req_20250727_153045_xyz789",
    "api_version": "2.1"
  },
  "status": "error"
}
```

### Common Error Codes

- `INVALID_REQUEST`: Malformed request or missing required fields
- `ANALYSIS_FAILED`: Unable to process message content
- `MODEL_UNAVAILABLE`: AI models not loaded or unavailable
- `RATE_LIMITED`: Too many requests from client
- `SERVICE_UNAVAILABLE`: NLP service temporarily down
- `LEARNING_ERROR`: Issue with learning system processing
- `TIMEOUT`: Request exceeded processing timeout

---

## 🚀 Integration Examples

### Discord Bot Integration

```python
import aiohttp
import asyncio

class AshNLPClient:
    def __init__(self, base_url="http://10.20.30.16:8881"):
        self.base_url = base_url
        self.session = None
    
    async def analyze_message(self, message, user_id, channel_id, context=None):
        """Analyze a Discord message for crisis indicators"""
        payload = {
            "message": message,
            "user_id": str(user_id),
            "channel_id": str(channel_id)
        }
        
        if context:
            payload["context"] = context
            
        async with self.session.post(
            f"{self.base_url}/analyze",
            json=payload,
            timeout=30
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"NLP analysis failed: {response.status}")
    
    async def provide_feedback(self, analysis_id, feedback_type, correct_classification):
        """Provide learning feedback"""
        payload = {
            "analysis_id": analysis_id,
            "feedback_type": feedback_type,
            "correct_classification": correct_classification
        }
        
        async with self.session.post(
            f"{self.base_url}/learning_feedback",
            json=payload
        ) as response:
            return await response.json()

# Usage example
async def handle_message(message):
    nlp = AshNLPClient()
    nlp.session = aiohttp.ClientSession()
    
    try:
        result = await nlp.analyze_message(
            message.content,
            message.author.id,
            message.channel.id
        )
        
        if result["risk_level"] in ["high", "medium"]:
            await handle_crisis_detection(message, result)
            
    except Exception as e:
        print(f"NLP analysis error: {e}")
        # Fallback to keyword-based detection
        
    finally:
        await nlp.session.close()
```

### Dashboard Integration

```javascript
class AshNLPDashboard {
    constructor(baseUrl = 'http://10.20.30.16:8881') {
        this.baseUrl = baseUrl;
    }
    
    async getPerformanceMetrics(timeframe = 'hour') {
        const response = await fetch(
            `${this.baseUrl}/performance_metrics?timeframe=${timeframe}`
        );
        return await response.json();
    }
    
    async getLearningStatistics() {
        const response = await fetch(`${this.baseUrl}/learning_statistics`);
        return await response.json();
    }
    
    async exportAnalytics(startTime, endTime) {
        const params = new URLSearchParams({
            start_time: startTime,
            end_time: endTime,
            format: 'json'
        });
        
        const response = await fetch(
            `${this.baseUrl}/analytics_export?${params}`
        );
        return await response.json();
    }
}

// Real-time dashboard updates
const dashboard = new AshNLPDashboard();

setInterval(async () => {
    try {
        const metrics = await dashboard.getPerformanceMetrics();
        updateDashboardCharts(metrics);
        
        const learning = await dashboard.getLearningStatistics();
        updateLearningDisplay(learning);
        
    } catch (error) {
        console.error('Dashboard update failed:', error);
        showConnectionError();
    }
}, 30000); // Update every 30 seconds
```

### Testing Suite Integration

```bash
#!/bin/bash
# Comprehensive NLP testing script

BASE_URL="http://10.20.30.16:8881"

# Health check
echo "Testing NLP server health..."
health_response=$(curl -s "$BASE_URL/health")
if [[ $(echo $health_response | jq -r '.status') != "healthy" ]]; then
    echo "ERROR: NLP server not healthy"
    exit 1
fi

# Test analysis endpoint
echo "Testing message analysis..."
test_message='{
    "message": "feeling really down today, nothing seems to matter",
    "user_id": "test_user_123",
    "channel_id": "test_channel_456"
}'

analysis_response=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$test_message" \
    "$BASE_URL/analyze")

risk_level=$(echo $analysis_response | jq -r '.risk_level')
confidence=$(echo $analysis_response | jq -r '.confidence')

echo "Analysis result: $risk_level (confidence: $confidence)"

# Test learning feedback
echo "Testing learning feedback..."
analysis_id=$(echo $analysis_response | jq -r '.metadata.analysis_id')

feedback='{
    "analysis_id": "'$analysis_id'",
    "feedback_type": "correct_classification",
    "correct_classification": "'$risk_level'"
}'

feedback_response=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$feedback" \
    "$BASE_URL/learning_feedback")

echo "Feedback submitted: $(echo $feedback_response | jq -r '.status')"

# Performance test
echo "Running performance test..."
start_time=$(date +%s%N)
for i in {1..10}; do
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$test_message" \
        "$BASE_URL/analyze" > /dev/null
done
end_time=$(date +%s%N)

total_time=$(((end_time - start_time) / 1000000))
avg_time=$((total_time / 10))

echo "Average response time: ${avg_time}ms"

if [ $avg_time -lt 200 ]; then
    echo "✅ Performance test PASSED"
else
    echo "❌ Performance test FAILED (too slow)"
fi
```

---

## 📚 API Best Practices

### Performance Optimization

**Batch Processing:**
```json
// Instead of multiple single requests
// Use batch analysis for better performance
{
  "messages": [
    {"id": "1", "message": "text1", "user_id": "user1"},
    {"id": "2", "message": "text2", "user_id": "user2"}
  ]
}
```

**Connection Pooling:**
```python
# Maintain persistent connections
session = aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(limit=100),
    timeout=aiohttp.ClientTimeout(total=30)
)
```

**Caching:**
```python
# Cache results for identical messages (with TTL)
import hashlib
message_hash = hashlib.md5(message.encode()).hexdigest()
cached_result = cache.get(f"nlp:{message_hash}")
```

### Error Handling

**Retry Logic:**
```python
async def analyze_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await nlp_client.analyze(message)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

**Graceful Degradation:**
```python
try:
    nlp_result = await analyze_message(message)
    return nlp_result
except Exception:
    # Fallback to keyword-based detection
    return keyword_analysis(message)
```

### Security Considerations

**Input Validation:**
```python
def validate_request(data):
    required_fields = ['message', 'user_id', 'channel_id']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if len(data['message']) > 2000:
        raise ValueError("Message too long")
```

**Rate Limiting:**
```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests
        client_requests[:] = [req for req in client_requests 
                             if now - req < self.window]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True
```

---

## 🔗 Related Documentation

- **[Deployment Guide](../deployment_v2_1.md)** - Production deployment procedures
- **[Team Guide](../team/team_guide_v2_1.md)** - Crisis response team procedures
- **[Troubleshooting Guide](troubleshooting_v2_1.md)** - Problem diagnosis and resolution
- **[Main Repository](https://github.com/the-alphabet-cartel/ash)** - Ecosystem overview

---

## 📞 API Support

### Technical Support
- **GitHub Issues**: [ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Discord #tech-support**: Quick technical questions
- **API Documentation**: This guide and inline API docs

### Integration Assistance
- **Discord #development**: Developer discussions and integration help
- **Example Code**: Available in repository `/examples` directory
- **Best Practices**: Community-shared integration patterns

---

**The Alphabet Cartel** - Building inclusive gaming communities through technology.

**Discord:** https://discord.gg/alphabetcartel | **Website:** https://alphabetcartel.org

*Powerful APIs enabling safer communities through advanced crisis detection.*