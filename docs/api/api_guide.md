<!-- ash-nlp/docs/api/api_guide.md -->
<!--
API Guide for Ash-NLP Service
FILE VERSION: v3.1-3d-8.3-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# API Guide

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-3e-8.3-1
**LAST UPDATED**: 2025-08-26
**PHASE**: 3e, Step 8
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

# Ash-NLP v3.1 API Reference

Complete API documentation for integrating with Ash-NLP's crisis detection service.

---

## Base Configuration

### Service Endpoint
- **Base URL**: `http://localhost:8881`
- **Protocol**: HTTP/HTTPS
- **Content-Type**: `application/json`
- **Default Port**: 8881

### Authentication
Currently, no authentication is required for API access. Future versions may implement API key authentication.

---

## Core Endpoints

### 1. Crisis Analysis

**Endpoint**: `POST /analyze`

Primary endpoint for crisis detection analysis.

#### Request Format
```json
{
  "message": "string",           // Required: Message text to analyze
  "user_id": "string",          // Required: User identifier
  "channel_id": "string",       // Required: Channel identifier
  "context": {                  // Optional: Additional context
    "previous_messages": ["string"],
    "user_history_summary": "string",
    "channel_type": "string"
  }
}
```

#### Response Format
```json
{
  "crisis_score": 0.75,                    // Crisis probability (0.0-1.0)
  "crisis_level": "high",                  // none|low|medium|high|critical
  "needs_response": true,                  // Boolean: requires intervention
  "confidence_score": 0.82,               // Analysis confidence (0.0-1.0)
  "method": "ensemble_consensus",          // Analysis method used
  "detected_categories": [                 // Crisis pattern categories
    "emotional_distress", 
    "depression_indicators"
  ],
  "requires_staff_review": false,          // Human review needed
  "processing_time": 147.6,                // Response time (ms)
  "ai_model_details": {                    // AI model breakdown
    "model_1_score": 0.78,
    "model_2_score": 0.71,
    "model_3_score": 0.76,
    "consensus_reached": true,
    "disagreement_detected": false
  },
  "pattern_analysis": {                    // Pattern detection results
    "keyword_matches": ["down", "sad"],
    "semantic_patterns": ["emotional_distress"],
    "context_factors": ["isolation_indicators"]
  },
  "learning_adjustments": {                // Learning system modifications
    "threshold_adjustments": {},
    "confidence_modifications": 0.02,
    "learning_metadata": {}
  }
}
```

#### HTTP Status Codes
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request format or missing required fields
- `422 Unprocessable Entity`: Valid JSON but invalid data values
- `500 Internal Server Error`: Analysis processing failed
- `503 Service Unavailable`: AI models not loaded or service unavailable

#### Example Request
```bash
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have been feeling really down lately and don'\''t know what to do",
    "user_id": "user123",
    "channel_id": "general"
  }'
```

---

### 2. Service Health

**Endpoint**: `GET /health`

Service health check and system status.

#### Response Format
```json
{
  "status": "healthy",                     // healthy|degraded|unhealthy
  "version": "v3.1-3e-8-3",               // Service version
  "models_loaded": true,                   // AI models status
  "managers_initialized": 15,              // Manager count
  "response_time": 147.6,                  // Average response time (ms)
  "uptime": 86400,                        // Uptime in seconds
  "system_health": {
    "memory_usage": "2.1GB",
    "gpu_memory": "1.03GB",
    "cpu_usage": "12%",
    "disk_usage": "45%"
  },
  "service_metrics": {
    "requests_processed": 1247,
    "crisis_detections": 89,
    "false_positives": 7,
    "learning_adjustments": 23
  }
}
```

#### HTTP Status Codes
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy or starting up

---

### 3. Learning Feedback

**Endpoint**: `POST /learning/feedback`

Submit feedback for the learning system to improve accuracy.

#### Request Format
```json
{
  "message": "string",                     // Original message analyzed
  "user_id": "string",                     // User identifier
  "channel_id": "string",                  // Channel identifier
  "feedback_type": "false_positive",       // false_positive|false_negative|correct
  "original_result": {},                   // Original analysis result
  "context": {                            // Optional feedback context
    "staff_notes": "string",
    "severity_correction": "string",
    "category_corrections": ["string"]
  }
}
```

#### Response Format
```json
{
  "feedback_processed": true,              // Feedback acceptance status
  "learning_applied": true,                // Whether adjustments were made
  "adjustments_made": 2,                   // Number of threshold adjustments
  "daily_adjustments_remaining": 47,       // Remaining daily adjustment capacity
  "adjustment_summary": {
    "threshold_changes": {
      "depression_threshold": -0.02,
      "distress_threshold": -0.01
    },
    "learning_metadata": {
      "adjustment_reason": "false_positive",
      "severity_level": "medium",
      "confidence_impact": 0.85
    }
  }
}
```

#### Feedback Types
- **`false_positive`**: System incorrectly identified crisis when none existed
- **`false_negative`**: System missed crisis that human identified
- **`correct`**: System analysis was accurate and appropriate

#### HTTP Status Codes
- `200 OK`: Feedback processed successfully
- `400 Bad Request`: Invalid feedback format
- `429 Too Many Requests`: Daily learning limit reached
- `500 Internal Server Error`: Learning system processing failed

---

## Administrative Endpoints

### 4. System Statistics

**Endpoint**: `GET /admin/stats`

Comprehensive system performance and usage statistics.

#### Response Format
```json
{
  "performance_metrics": {
    "average_response_time": 147.6,        // ms
    "response_time_p50": 142.3,           // 50th percentile
    "response_time_p95": 186.7,           // 95th percentile
    "response_time_p99": 234.5,           // 99th percentile
    "requests_per_minute": 45.2,
    "error_rate": 0.003                   // Error percentage
  },
  "crisis_detection_stats": {
    "total_messages_analyzed": 12847,
    "crisis_detected": 1247,
    "crisis_rate": 0.097,                 // 9.7%
    "false_positive_rate": 0.056,         // 5.6%
    "false_negative_rate": 0.023,         // 2.3%
    "accuracy": 0.921                     // 92.1%
  },
  "model_performance": {
    "model_1_average_confidence": 0.734,
    "model_2_average_confidence": 0.689,
    "model_3_average_confidence": 0.712,
    "consensus_rate": 0.834,              // 83.4%
    "disagreement_rate": 0.166            // 16.6%
  },
  "learning_system_stats": {
    "enabled": true,
    "adjustments_today": 23,
    "adjustments_remaining": 27,
    "learning_effectiveness": 0.887,       // 88.7%
    "threshold_drift": 0.032              // 3.2%
  }
}
```

#### HTTP Status Codes
- `200 OK`: Statistics retrieved successfully
- `503 Service Unavailable`: Statistics collection unavailable

---

### 5. Threshold Management

**Endpoint**: `POST /admin/thresholds`

Update crisis detection thresholds (administrative function).

#### Request Format
```json
{
  "thresholds": {
    "low": 0.25,                         // Low crisis threshold
    "medium": 0.45,                      // Medium crisis threshold  
    "high": 0.65,                        // High crisis threshold
    "critical": 0.85                     // Critical crisis threshold
  },
  "validation": {
    "override_bounds_check": false,      // Override safety bounds
    "reason": "string"                   // Reason for threshold change
  }
}
```

#### Response Format
```json
{
  "thresholds_updated": true,
  "validation_results": {
    "bounds_validated": true,
    "warnings": [],
    "errors": []
  },
  "previous_thresholds": {
    "low": 0.2,
    "medium": 0.4,
    "high": 0.6,
    "critical": 0.8
  },
  "applied_thresholds": {
    "low": 0.25,
    "medium": 0.45,
    "high": 0.65,
    "critical": 0.85
  }
}
```

#### HTTP Status Codes
- `200 OK`: Thresholds updated successfully
- `400 Bad Request`: Invalid threshold values
- `422 Unprocessable Entity`: Thresholds outside safety bounds
- `500 Internal Server Error`: Threshold update failed

---

### 6. Learning System Status

**Endpoint**: `GET /admin/learning/status`

Detailed learning system health and configuration.

#### Response Format
```json
{
  "learning_enabled": true,
  "health_status": "excellent",           // excellent|good|warning|critical
  "health_score": 95,                     // 0-100 health rating
  "configuration": {
    "learning_rate": 0.01,
    "max_adjustments_per_day": 50,
    "sensitivity_bounds": {
      "min_global_sensitivity": 0.5,
      "max_global_sensitivity": 1.5
    },
    "adjustment_factors": {
      "false_positive_factor": -0.1,
      "false_negative_factor": 0.1
    }
  },
  "daily_status": {
    "adjustments_made": 23,
    "adjustments_remaining": 27,
    "last_adjustment": "2025-08-26T14:30:22Z"
  },
  "effectiveness_metrics": {
    "false_positive_reduction": 0.34,     // 34% reduction
    "false_negative_reduction": 0.28,     // 28% reduction
    "overall_accuracy_improvement": 0.067  // 6.7% improvement
  },
  "adjustment_history": [
    {
      "timestamp": "2025-08-26T14:30:22Z",
      "type": "false_positive",
      "adjustment_amount": -0.02,
      "crisis_level": "medium"
    }
  ]
}
```

#### HTTP Status Codes
- `200 OK`: Learning status retrieved successfully
- `503 Service Unavailable`: Learning system unavailable

---

## Integration Examples

### Discord Bot Integration

#### Basic Crisis Detection
```python
import aiohttp
import asyncio

class CrisisDetector:
    def __init__(self, api_base="http://localhost:8881"):
        self.api_base = api_base
    
    async def analyze_message(self, message, user_id, channel_id):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.api_base}/analyze",
                    json={
                        "message": message,
                        "user_id": user_id,
                        "channel_id": channel_id
                    }
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"API returned {response.status}"}
            except Exception as e:
                return {"error": str(e)}

# Usage
detector = CrisisDetector()
result = await detector.analyze_message(
    "I'm feeling really down today",
    "user123", 
    "general"
)

if result.get("needs_response"):
    # Trigger crisis response
    print(f"Crisis detected: {result['crisis_level']}")
```

#### Advanced Integration with Feedback
```python
class AdvancedCrisisBot:
    def __init__(self, api_base="http://localhost:8881"):
        self.api_base = api_base
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def analyze_with_context(self, message, user_id, channel_id, context=None):
        payload = {
            "message": message,
            "user_id": user_id,
            "channel_id": channel_id
        }
        if context:
            payload["context"] = context
            
        async with self.session.post(f"{self.api_base}/analyze", json=payload) as response:
            return await response.json()
    
    async def submit_feedback(self, message, user_id, channel_id, feedback_type, original_result):
        payload = {
            "message": message,
            "user_id": user_id,
            "channel_id": channel_id,
            "feedback_type": feedback_type,
            "original_result": original_result
        }
        
        async with self.session.post(f"{self.api_base}/learning/feedback", json=payload) as response:
            return await response.json()
    
    async def get_health_status(self):
        async with self.session.get(f"{self.api_base}/health") as response:
            return await response.json()

# Usage with context manager
async def bot_main():
    async with AdvancedCrisisBot() as bot:
        # Analyze message with context
        result = await bot.analyze_with_context(
            "I don't think I can handle this anymore",
            "user456",
            "support",
            context={
                "previous_messages": ["Things have been rough lately"],
                "channel_type": "support"
            }
        )
        
        if result["crisis_level"] in ["high", "critical"]:
            # Handle crisis response
            await handle_crisis_response(result)
        
        # Later, if human review determines this was incorrect:
        feedback_result = await bot.submit_feedback(
            result["message"],
            result["user_id"], 
            result["channel_id"],
            "false_positive",
            result
        )
```

### HTTP Client Examples

#### cURL Commands
```bash
# Basic analysis
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am struggling with everything right now",
    "user_id": "test_user",
    "channel_id": "test_channel"
  }'

# Health check
curl http://localhost:8881/health

# Submit feedback
curl -X POST http://localhost:8881/learning/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am struggling with everything right now",
    "user_id": "test_user",
    "channel_id": "test_channel", 
    "feedback_type": "correct",
    "original_result": {}
  }'

# Get system stats (admin)
curl http://localhost:8881/admin/stats
```

#### JavaScript/Node.js
```javascript
const axios = require('axios');

class AshNLPClient {
  constructor(baseURL = 'http://localhost:8881') {
    this.client = axios.create({ baseURL });
  }

  async analyzeCrisis(message, userId, channelId, context = null) {
    try {
      const response = await this.client.post('/analyze', {
        message,
        user_id: userId,
        channel_id: channelId,
        context
      });
      return response.data;
    } catch (error) {
      throw new Error(`Crisis analysis failed: ${error.message}`);
    }
  }

  async submitFeedback(message, userId, channelId, feedbackType, originalResult) {
    try {
      const response = await this.client.post('/learning/feedback', {
        message,
        user_id: userId,
        channel_id: channelId,
        feedback_type: feedbackType,
        original_result: originalResult
      });
      return response.data;
    } catch (error) {
      throw new Error(`Feedback submission failed: ${error.message}`);
    }
  }

  async getHealthStatus() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }
}

// Usage
const client = new AshNLPClient();

async function handleMessage(message, userId, channelId) {
  const result = await client.analyzeCrisis(message, userId, channelId);
  
  if (result.needs_response) {
    console.log(`Crisis detected: ${result.crisis_level}`);
    console.log(`Confidence: ${result.confidence_score}`);
    // Implement crisis response logic
  }
  
  return result;
}
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Bad Request",
  "detail": "Missing required field: message",
  "error_code": "MISSING_FIELD"
}
```

#### 422 Unprocessable Entity
```json
{
  "error": "Unprocessable Entity", 
  "detail": "Message too long (maximum 4000 characters)",
  "error_code": "VALIDATION_ERROR"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "detail": "Analysis processing failed", 
  "error_code": "PROCESSING_ERROR"
}
```

#### 503 Service Unavailable
```json
{
  "error": "Service Unavailable",
  "detail": "AI models not loaded",
  "error_code": "SERVICE_UNAVAILABLE" 
}
```

### Error Handling Best Practices

1. **Implement retry logic** for 503 errors with exponential backoff
2. **Validate input** before sending to prevent 400 errors
3. **Handle timeout scenarios** with appropriate fallback responses
4. **Log error responses** for debugging and monitoring
5. **Provide user feedback** for service unavailability

---

## Rate Limiting

### Current Limits
- No explicit rate limiting implemented in v3.1
- Natural limits from processing time (147ms average)
- Learning system has daily adjustment limits (50 per day)

### Recommended Client-Side Limits
- Maximum 10 concurrent analysis requests
- Maximum 1000 requests per minute per client
- Implement request queuing for high-volume scenarios

---

## API Versioning

### Current Version
- **API Version**: v3.1
- **Compatibility**: Backward compatible with v3.0 for core endpoints
- **Deprecation Policy**: 6-month notice for breaking changes

### Version Headers
```bash
# Optional: Include API version in requests
curl -H "API-Version: v3.1" http://localhost:8881/analyze
```

---

## Support and Troubleshooting

### Common Integration Issues

1. **Connection Refused**: Verify service is running on correct port
2. **Timeout Errors**: Increase client timeout to 30+ seconds for cold starts  
3. **Memory Errors**: Ensure adequate RAM (8GB+) and GPU memory (4GB+)
4. **Model Loading**: First requests may be slower while models initialize

### Getting Help

- **GitHub Issues**: [Report bugs and feature requests](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Discord Community**: [Join for real-time support](https://discord.gg/alphabetcartel)
- **Documentation**: [Complete technical documentation](https://github.com/the-alphabet-cartel/ash-nlp/tree/main/docs)

---

*API Guide for Ash-NLP v3.1 - Comprehensive crisis detection integration documentation.*