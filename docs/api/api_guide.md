<!-- ash-nlp/docs/api/api_guide.md -->
<!--
API Guide for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# API Guide

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# Ash-NLP v5.0 API Reference

Complete API documentation for integrating with Ash-NLP's crisis detection service.

---

## Base Configuration

### Service Endpoint
- **Base URL**: `http://localhost:30880`
- **Protocol**: HTTP/HTTPS
- **Content-Type**: `application/json`
- **Default Port**: 30880

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
...TBA...
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
curl -X POST http://localhost:30880/analyze \
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
  "version": "v5.0",               // Service version
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

## Administrative Endpoints

### 3. System Statistics

**Endpoint**: `GET /admin/stats`

Comprehensive system performance and usage statistics.

#### Response Format
```json
{
...TBA...
}
```

#### HTTP Status Codes
- `200 OK`: Statistics retrieved successfully
- `503 Service Unavailable`: Statistics collection unavailable

---

## Integration Examples

### Discord Bot Integration

#### Basic Crisis Detection
```python
...TBA...
```

#### Advanced Integration with Feedback
```python
...TBA...
```

### HTTP Client Examples

#### cURL Commands
```bash
# Basic analysis
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am struggling with everything right now",
    "user_id": "test_user",
    "channel_id": "test_channel"
  }'

# Health check
curl http://localhost:30880/health

# Get system stats (admin)
curl http://localhost:30880/admin/stats
```

#### JavaScript/Node.js
```javascript
...TBA...
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
- No explicit rate limiting implemented in v5.0
- Natural limits from processing time (147ms average)

### Recommended Client-Side Limits
- Maximum 10 concurrent analysis requests
- Maximum 1000 requests per minute per client
- Implement request queuing for high-volume scenarios

---

## API Versioning

### Current Version
- **API Version**: v5.0

### Version Headers
```bash
# Optional: Include API version in requests
curl -H "API-Version: v5.0" http://localhost:30880/analyze
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

*API Guide for Ash-NLP v5.0 - Comprehensive crisis detection integration documentation.*

**Built with care for chosen family** 🏳️‍🌈
