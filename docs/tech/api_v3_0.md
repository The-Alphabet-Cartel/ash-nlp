# Ash NLP v3.0 API Documentation

**Complete API reference for the three-model ensemble crisis detection system**

---

## 🚀 API Overview

Ash NLP v3.0 provides a RESTful API for mental health crisis detection using a sophisticated three-model ensemble. The API is designed for:

- **Real-time message analysis** with sub-35ms response times
- **Multiple analysis modes** from basic to advanced ensemble
- **Comprehensive monitoring** and health checking
- **Secure authentication** with Docker secrets support

**Base URL**: `http://localhost:8881` (default)  
**Content-Type**: `application/json`  
**Authentication**: Optional (configurable via environment)

---

## 📊 Quick Reference

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/health` | GET | System health check | ~1ms |
| `/stats` | GET | Service statistics | ~2ms |
| `/analyze` | POST | Three-model ensemble analysis | ~63ms |
| `/extract_phrases` | POST | Crisis keyword extraction | ~200ms |
| `/learning_statistics` | GET | Learning system metrics | ~3ms |

---

## 🏥 Health & Status Endpoints

### GET `/health`

**Purpose**: Check system health and model status

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime_seconds": 1604.6477420330048,
  "hardware_info": {
    "device": "auto",
    "precision": "float16",
    "max_batch_size": 32,
    "inference_threads": 16,
    "components_available": {
      "model_manager": true,
      "crisis_analyzer": true,
      "phrase_extractor": true,
      "enhanced_learning": true,
      "three_model_ensemble": true
    },
    "learning_system": "enabled",
    "secrets_status": {
      "claude_api_key": true,
      "huggingface_token": true,
      "openai_api_key": false
    },
    "using_secrets": true,
    "ensemble_info": {
      "models_count": 3,
      "ensemble_modes": [
        "consensus",
        "majority",
        "weighted"
      ],
      "gap_detection": "enabled"
    }
  }
}
```

**Status Codes**:
- `200`: System healthy and operational
- `503`: System unhealthy (models not loaded)

---

### GET `/stats`

**Purpose**: Detailed service statistics and configuration

**Response**:
```json
{
  "service": "Enhanced Ash NLP Service - Three-Model Ensemble",
  "version": "4.5.0",
  "uptime_seconds": 1635.8521761894226,
  "models_loaded": {
    "models_loaded": true,
    "device": 0,
    "precision": "float16",
    "ensemble_mode": "consensus",
    "models": {
      "depression": {
        "name": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
        "loaded": true,
        "purpose": "Primary crisis classification"
      },
      "sentiment": {
        "name": "Lowerated/lm6-deberta-v3-topic-sentiment",
        "loaded": true,
        "purpose": "Contextual validation"
      },
      "emotional_distress": {
        "name": "facebook/bart-large-mnli",
        "loaded": true,
        "purpose": "Emotional distress detection"
      }
    },
    "gap_detection": {
      "enabled": true,
      "disagreement_threshold": 0.35,
      "gap_detection_threshold": 0.25
    }
  },
  "configuration": {
    "learning_enabled": true,
    "device": "auto",
    "precision": "float16",
    "using_secrets": true,
    "ensemble_enabled": true,
    "models_count": 3,
    "thresholds": {
      "high": 0.45,
      "medium": 0.25,
      "low": 0.15
    }
  },
  "secrets_status": {
    "claude_api_key": true,
    "huggingface_token": true,
    "openai_api_key": false
  },
  "components_available": {
    "model_manager": true,
    "crisis_analyzer": true,
    "phrase_extractor": true,
    "enhanced_learning": true,
    "three_model_ensemble": true
  },
  "hardware_config": {
    "max_batch_size": 32,
    "inference_threads": 16,
    "max_concurrent_requests": 20,
    "request_timeout": 40
  },
  "ensemble_info": {
    "depression_model": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
    "sentiment_model": "Lowerated/lm6-deberta-v3-topic-sentiment",
    "emotional_distress_model": "unknown",
    "ensemble_mode": "weighted",
    "gap_detection_enabled": true
  }
}
```

---

## 🧠 Analysis Endpoints

### POST `/analyze`

**Purpose**: Advanced three-model ensemble analysis with gap detection

**Request Body**:
```json
{
  "message": "This exam is killing me but I think I can handle it",
  "user_id": "user123", 
  "channel_id": "channel456"
}
```

**Parameters**: Same as `/analyze`

**Response**:
```json
{
  "message_analyzed": "This exam is killing me but I think I can handle it",
  "user_id": "user123",
  "channel_id": "channel456",
  "ensemble_analysis": {
    "individual_results": {
      "depression": [
        {
          "label": "not depression",
          "score": 0.9633975625038147
        },
        {
          "label": "moderate", 
          "score": 0.03377213701605797
        },
        {
          "label": "severe",
          "score": 0.002830314915627241
        }
      ],
      "sentiment": [
        {
          "label": "negative",
          "score": 0.694797933101654
        },
        {
          "label": "neutral",
          "score": 0.21424223482608795
        },
        {
          "label": "positive",
          "score": 0.0909598246216774
        }
      ],
      "emotional_distress": [
        {
          "label": "NEGATIVE",
          "score": 0.9296960830688477
        },
        {
          "label": "POSITIVE",
          "score": 0.07030384242534637
        }
      ]
    },
    "confidence_scores": {
      "depression": 0.9633975625038147,
      "sentiment": 0.694797933101654,
      "emotional_distress": 0.9296960830688477
    },
    "predictions": {
      "depression": "not depression",
      "sentiment": "negative",
      "emotional_distress": "NEGATIVE"
    },
    "normalized_predictions": {
      "depression": "safe",
      "sentiment": "crisis", 
      "emotional_distress": "crisis"
    },
    "gaps_detected": true,
    "gap_details": [
      {
        "type": "meaningful_disagreement",
        "crisis_models": ["sentiment", "emotional_distress"],
        "safe_models": ["depression"]
      }
    ],
    "consensus": {
      "prediction": "not depression",
      "confidence": 0.6743782937526702,
      "method": "best_of_disagreeing"
    },
    "ensemble_mode": "consensus"
  },
  "processing_time_ms": 31.25,
  "model_info": "three_model_ensemble",
  "timestamp": 1753911604.3766992,
  "requires_staff_review": true,
  "gap_summary": {
    "total_gaps": 1,
    "gap_types": {
      "meaningful_disagreement": 1
    },
    "requires_immediate_attention": false
  },
  "consensus_prediction": "not depression",
  "consensus_confidence": 0.6743782937526702,
  "consensus_method": "best_of_disagreeing",
  "crisis_level": "none",
  "needs_response": false
}
```

**Key Response Fields**:
- `gaps_detected` (boolean): Whether models disagreed significantly
- `gap_details` (array): Detailed analysis of disagreements
- `requires_staff_review` (boolean): AI recommendation for human review
- `consensus` (object): How final decision was reached
- `individual_results` (object): Raw output from each model

**Gap Types**:
- `meaningful_disagreement`: Some models detect crisis, others safety
- `confidence_disagreement`: Models agree on prediction but confidence varies

**Consensus Methods**:
- `unanimous_consensus`: All models agree
- `best_of_disagreeing`: Models disagree, highest confidence chosen
- `majority_vote`: Democratic decision with confidence weighting
- `weighted_ensemble`: Configurable model importance ratios

---

## 🔍 Analysis Tools

### POST `/extract_phrases`

**Purpose**: Extract potential crisis keywords and phrases using model scoring

**Request Body**:
```json
{
  "message": "I am struggling with severe depression and anxiety",
  "user_id": "test_user_phrases",
  "channel_id": "test_channel",
  "parameters": {
    "min_phrase_length": 2,
    "max_phrase_length": 6,
    "crisis_focus": true,
    "community_specific": true,
    "min_confidence": 0.3,
    "max_results": 20
  }
}
```

**Parameters**:
- `message` (string, required): Text to analyze for crisis phrases
- `user_id` (string, required): User identifier
- `channel_id` (string, required): Channel identifier
- `parameters` (object, optional): Analysis configuration
  - `min_phrase_length` (integer): Minimum words in extracted phrases
  - `max_phrase_length` (integer): Maximum words in extracted phrases
  - `crisis_focus` (boolean): Focus on crisis-related phrases
  - `community_specific` (boolean): Include LGBTQIA+ specific patterns
  - `min_confidence` (float): Minimum confidence threshold
  - `max_results` (integer): Maximum phrases to return

**Response**:
```json
{
  "phrases": [
    {
      "text": "severe depression",
      "confidence": 0.85,
      "type": "ngram",
      "category": "mental_health",
      "source_position": 5,
      "context_score": 0.92
    },
    {
      "text": "struggling with",
      "confidence": 0.73,
      "type": "crisis_context", 
      "category": "difficulty_expression",
      "source_position": 2,
      "context_score": 0.67
    }
  ],
  "total_extracted": 15,
  "total_scored": 12,
  "filtered_count": 10,
  "processing_time_ms": 185.4,
  "extraction_methods": [
    "ngrams",
    "community_patterns", 
    "crisis_context",
    "model_scoring"
  ]
}
```

**Status Codes**:
- `200`: Phrase extraction completed
- `400`: Invalid parameters
- `503`: Phrase extraction not available

---

## 📈 Learning & Analytics

### GET `/learning_statistics` (Work in Progress)

**Purpose**: Get learning system performance metrics

**Response**:
```json
{
  "learning_system": {
    "enabled": true,
    "total_false_positives": 23,
    "total_false_negatives": 12,
    "false_positives_by_level": {
      "high": 5,
      "medium": 12,
      "low": 6
    },
    "false_negatives_by_level": {
      "high": 2,
      "medium": 7,
      "low": 3
    },
    "learning_effectiveness": {
      "patterns_learned": 45,
      "adjustments_applied": 78,
      "last_update": "2025-07-30T21:30:26Z"
    },
    "common_patterns": {
      "false_positive_phrases": [
        "killing it",
        "dead tired", 
        "dying of laughter"
      ],
      "missed_crisis_patterns": [
        "can't go on",
        "what's the point",
        "too much to handle"
      ]
    }
  },
  "model_performance": {
    "accuracy_trend": 0.756,
    "precision": 0.834,
    "recall": 0.692,
    "f1_score": 0.754
  }
}
```

---

## ⚙️ Configuration

### Environment Variables

#### Three-Model Configuration
```bash
# Model Selection
NLP_DEPRESSION_MODEL=MoritzLaurer/deberta-v3-base-zeroshot-v2.0
NLP_SENTIMENT_MODEL=Lowerated/lm6-deberta-v3-topic-sentiment  
NLP_EMOTIONAL_DISTRESS_MODEL=facebook/bart-large-mnli

# Ensemble Settings
NLP_ENSEMBLE_MODE=weighted              # consensus, majority, weighted
NLP_GAP_DETECTION_THRESHOLD=0.4          # 0.0-1.0
NLP_DISAGREEMENT_THRESHOLD=0.5           # 0.0-1.0
NLP_AUTO_FLAG_DISAGREEMENTS=true

# Model Weights (for weighted mode)
NLP_DEPRESSION_MODEL_WEIGHT=0.5          # 0.0-1.0
NLP_SENTIMENT_MODEL_WEIGHT=0.2           # 0.0-1.0  
NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT=0.3  # 0.0-1.0
```

#### Hardware Optimization
```bash
# Device Configuration
NLP_DEVICE=auto                    # auto, cpu, cuda, cuda:0
NLP_MODEL_PRECISION=float16        # float32, float16, bfloat16

# Performance Tuning (RTX 3060 Optimized)
NLP_MAX_BATCH_SIZE=48              # 1-128
NLP_INFERENCE_THREADS=16           # 1-32  
NLP_MAX_CONCURRENT_REQUESTS=20     # 1-100
NLP_REQUEST_TIMEOUT=35             # 5-300 seconds
```

#### Server Configuration
```bash
# Network Settings
NLP_SERVICE_HOST=0.0.0.0           # Bind address
NLP_SERVICE_PORT=8881              # Port number
NLP_UVICORN_WORKERS=1              # Worker processes

# Security
GLOBAL_ALLOWED_IPS=10.20.30.0/24,127.0.0.1,::1
GLOBAL_ENABLE_CORS=true
```

#### Crisis Detection Thresholds
```bash
# Individual Model Thresholds
NLP_HIGH_CRISIS_THRESHOLD=0.55     # 0.0-1.0
NLP_MEDIUM_CRISIS_THRESHOLD=0.28   # 0.0-1.0
NLP_LOW_CRISIS_THRESHOLD=0.16      # 0.0-1.0

# Ensemble-Specific Thresholds
NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD=0.60    # 0.0-1.0
NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD=0.35  # 0.0-1.0
NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD=0.20     # 0.0-1.0
```

#### Experimental Features
```bash
# Advanced Features
NLP_ENABLE_ENSEMBLE_ANALYSIS=true
NLP_ENABLE_GAP_DETECTION=true
NLP_ENABLE_CONFIDENCE_SPREADING=true
NLP_LOG_MODEL_DISAGREEMENTS=true
```

---

## 🔒 Authentication & Security

### Docker Secrets Integration

Recommended for production deployments:

```bash
# Docker secrets paths
GLOBAL_HUGGINGFACE_TOKEN=/run/secrets/huggingface
GLOBAL_CLAUDE_API_KEY=/run/secrets/claude_api_key
```

### Rate Limiting

```bash
# Rate Limiting (Hardware Optimized)
NLP_MAX_REQUESTS_PER_MINUTE=120    # Requests per minute
NLP_MAX_REQUESTS_PER_HOUR=2000     # Requests per hour
```

### CORS Configuration

```bash
# CORS Settings
GLOBAL_ENABLE_CORS=true
GLOBAL_ALLOWED_IPS=10.20.30.0/24,172.20.0.0/16,127.0.0.1,::1
```

---

## 📊 Response Codes & Error Handling

### HTTP Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid JSON or missing required fields |
| 401 | Unauthorized | Authentication required but not provided |
| 403 | Forbidden | API key invalid or insufficient permissions |
| 422 | Unprocessable Entity | Valid JSON but invalid content (empty message, etc.) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Model loading failed or analysis error |
| 503 | Service Unavailable | System not ready (models still loading) |

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_MESSAGE",
    "message": "Message content cannot be empty",
    "details": {
      "field": "message",
      "provided_value": "",
      "expected": "non-empty string"
    },
    "timestamp": "2025-07-30T21:30:26Z",
    "request_id": "req_abc123"
  }
}
```

### Common Error Codes

- `INVALID_MESSAGE`: Empty or invalid message content
- `MODEL_NOT_READY`: Models still loading, try again
- `ANALYSIS_FAILED`: Internal analysis error
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `AUTHENTICATION_REQUIRED`: Missing or invalid API key
- `ENSEMBLE_UNAVAILABLE`: Ensemble analysis not available

---

## 🧪 Testing & Examples

### Example Requests

#### Ensemble Analysis with Gap Detection
```bash
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "This test is killing me but I think I can handle it",
    "user_id": "student456", 
    "channel_id": "study-group"
  }'
```

#### Phrase Extraction (Not Yet Implemented)
```bash
curl -X POST http://localhost:8881/extract_phrases \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am struggling with severe depression and anxiety",
    "user_id": "test_user",
    "channel_id": "test_channel",
    "parameters": {
      "crisis_focus": true,
      "max_results": 10
    }
  }'
```

### Test Messages for Different Scenarios

#### High Crisis (Should detect)
- "I want to end it all"
- "I cannot go on like this anymore"
- "Life is not worth living"

#### Medium Crisis (Should detect)
- "I am feeling really down and hopeless"
- "Everything feels overwhelming and pointless"
- "I do not know how much more I can take"

#### Gap Detection Triggers (Should flag for review)
- "This exam is killing me but I can handle it"
- "I am dying to see that movie" (humor/idiom)
- "Work is murder but at least it pays well" (mixed sentiment)

#### Safe Messages (Should not detect)
- "I am having a great day"
- "Looking forward to the weekend"
- "Thanks for your help"

---

## 🚀 Performance Optimization

### Response Time Targets

| Endpoint | Target | Typical | Hardware |
|----------|--------|---------|----------|
| `/health` | <2ms | ~1ms | Any |
| `/stats` | <5ms | ~2ms | Any |
| `/analyze` | <100ms | ~25ms | GPU Recommended |
| `/extract_phrases` | <250ms | ~185ms | GPU Recommended |

### Hardware Recommendations

#### Minimum Requirements
- **CPU**: 4 cores, 8GB RAM
- **Response Time**: ~50ms
- **Concurrent Users**: 5-10

#### Recommended Configuration  
- **CPU**: 8+ cores, 16GB RAM
- **GPU**: GTX 1660 or better
- **Response Time**: ~25-35ms
- **Concurrent Users**: 20-50

#### Optimal Configuration (Current)
- **CPU**: Ryzen 7 5800X, 64GB RAM
- **GPU**: RTX 3060 (12GB VRAM)
- **Response Time**: ~25-31ms
- **Concurrent Users**: 100+

### Monitoring Performance

```bash
# Check current performance
curl http://localhost:8881/stats | jq '.hardware_config'

# Monitor response times
time curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "user_id": "test", "channel_id": "test"}'
```

---

## 🔧 Troubleshooting

### Common Issues

#### Models Not Loading
**Symptoms**: 503 errors, "model_loaded": false  
**Solutions**:
1. Check GPU memory availability
2. Verify Hugging Face token
3. Ensure adequate disk space
4. Check Docker resource limits

#### Slow Response Times
**Symptoms**: >100ms response times  
**Solutions**:
1. Increase batch size if GPU has memory
2. Reduce concurrent request limit
3. Enable GPU acceleration
4. Check CPU/memory usage

#### Gap Detection Not Working
**Symptoms**: No gaps detected for ambiguous messages  
**Solutions**:
1. Lower `NLP_DISAGREEMENT_THRESHOLD`
2. Verify all three models are loaded
3. Check ensemble mode configuration
4. Test with known gap-triggering messages

### Debug Commands

```bash
# Check model loading status
curl http://localhost:8881/health | jq '.hardware_info.components_available'

# Verify ensemble configuration
curl http://localhost:8881/stats | jq '.configuration.ensemble'

# Test gap detection
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "This is killing me but I got this", "user_id": "test", "channel_id": "test"}' \
  | jq '.ensemble_analysis.gaps_detected'
```

---

## 📚 Integration Examples

### Discord Bot Integration

```python
import aiohttp
import json

class AshNLPClient:
    def __init__(self, base_url="http://localhost:8881"):
        self.base_url = base_url
        
    async def analyze_message(self, message, user_id, channel_id, use_ensemble=True):
        """Analyze a Discord message for crisis indicators"""
        endpoint = "/analyze" if use_ensemble else "/analyze"
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "message": message,
                "user_id": str(user_id),
                "channel_id": str(channel_id)
            }
            
            async with session.post(f"{self.base_url}{endpoint}", 
                                  json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"API Error: {response.status}")
    
    async def check_health(self):
        """Check if the NLP service is healthy"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health") as response:
                data = await response.json()
                return data.get("status") == "healthy"

# Usage in Discord bot
@bot.event
async def on_message(message):
    if message.author.bot:
        return
        
    nlp = AshNLPClient()
    
    try:
        result = await nlp.analyze_message(
            message.content, 
            message.author.id, 
            message.channel.id
        )
        
        if result.get("requires_staff_review"):
            # Handle gap detection case
            await notify_staff_review(message, result)
        elif result.get("crisis_level") == "high":
            # Handle high crisis
            await handle_crisis_response(message, result)
        elif result.get("needs_response"):
            # Handle medium/low crisis
            await handle_supportive_response(message, result)
            
    except Exception as e:
        print(f"NLP Analysis failed: {e}")
```

### Web Application Integration

```javascript
class AshNLPAPI {
    constructor(baseURL = 'http://localhost:8881') {
        this.baseURL = baseURL;
    }
    
    async analyzeMessage(message, userId, channelId, useEnsemble = true) {
        const endpoint = useEnsemble ? '/analyze' : '/analyze';
        
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user_id: userId,
                channel_id: channelId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async getHealth() {
        const response = await fetch(`${this.baseURL}/health`);
        return await response.json();
    }
    
    async getStats() {
        const response = await fetch(`${this.baseURL}/stats`);
        return await response.json();
    }
}

// Usage example
const nlpAPI = new AshNLPAPI();

document.getElementById('analyze-btn').addEventListener('click', async () => {
    const message = document.getElementById('message-input').value;
    
    try {
        const result = await nlpAPI.analyzeMessage(message, 'web-user', 'web-channel');
        
        // Display results
        document.getElementById('crisis-level').textContent = result.crisis_level;
        document.getElementById('confidence').textContent = 
            (result.consensus_confidence * 100).toFixed(1) + '%';
        
        if (result.gaps_detected) {
            document.getElementById('gap-warning').style.display = 'block';
            document.getElementById('gap-details').textContent = 
                JSON.stringify(result.gap_details, null, 2);
        }
        
    } catch (error) {
        console.error('Analysis failed:', error);
    }
});
```

### Monitoring Dashboard Integration (Not Yet Implemented)

```python
import asyncio
import aiohttp
from datetime import datetime

class AshNLPMonitor:
    def __init__(self, nlp_url="http://localhost:8881"):
        self.nlp_url = nlp_url
        self.metrics = {
            'total_requests': 0,
            'avg_response_time': 0,
            'crisis_detections': 0,
            'gaps_detected': 0,
            'system_health': 'unknown'
        }
    
    async def monitor_health(self):
        """Continuously monitor system health"""
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    start_time = datetime.now()
                    
                    async with session.get(f"{self.nlp_url}/health") as response:
                        health_data = await response.json()
                        response_time = (datetime.now() - start_time).total_seconds() * 1000
                        
                        self.metrics['system_health'] = health_data.get('status', 'unknown')
                        self.metrics['avg_response_time'] = response_time
                        
                        # Log health metrics
                        print(f"Health: {health_data['status']}, "
                              f"Models: {health_data['model_loaded']}, "
                              f"Uptime: {health_data['uptime_seconds']:.1f}s")
                        
            except Exception as e:
                print(f"Health check failed: {e}")
                self.metrics['system_health'] = 'error'
            
            await asyncio.sleep(30)  # Check every 30 seconds
    
    async def analyze_and_track(self, message, user_id, channel_id):
        """Analyze message and track metrics"""
        try:
            start_time = datetime.now()
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "message": message,
                    "user_id": user_id,
                    "channel_id": channel_id
                }
                
                async with session.post(f"{self.nlp_url}/analyze", 
                                      json=payload) as response:
                    result = await response.json()
                    
                    # Update metrics
                    self.metrics['total_requests'] += 1
                    
                    if result.get('crisis_level') in ['high', 'medium']:
                        self.metrics['crisis_detections'] += 1
                    
                    if result.get('gaps_detected'):
                        self.metrics['gaps_detected'] += 1
                    
                    return result
                    
        except Exception as e:
            print(f"Analysis tracking failed: {e}")
            return None

# Usage
monitor = AshNLPMonitor()

# Start health monitoring
asyncio.create_task(monitor.monitor_health())

# Analyze messages with tracking
result = await monitor.analyze_and_track("Test message", "user123", "channel456")
```

---

## 🔄 Webhook Integration

### Webhook Configuration

```bash
# Environment variables for webhook support
WEBHOOK_ENABLED=true
WEBHOOK_URL=https://your-app.com/ash-nlp-webhook
WEBHOOK_SECRET=your_webhook_secret
WEBHOOK_EVENTS=crisis_detected,gap_detected,system_health
```

### Webhook Payload Examples

#### Crisis Detection Webhook
```json
{
  "event": "crisis_detected",
  "timestamp": "2025-07-30T21:30:26Z",
  "data": {
    "message_id": "msg_123456",
    "user_id": "user789",
    "channel_id": "channel101",
    "crisis_level": "high",
    "confidence": 0.87,
    "needs_immediate_attention": true,
    "analysis_method": "three_model_ensemble"
  }
}
```

#### Gap Detection Webhook  
```json
{
  "event": "gap_detected",
  "timestamp": "2025-07-30T21:30:26Z",
  "data": {
    "message_id": "msg_789012",
    "user_id": "user345",
    "channel_id": "channel202",
    "gap_type": "meaningful_disagreement",
    "requires_staff_review": true,
    "model_predictions": {
      "depression": "safe",
      "sentiment": "crisis",
      "emotional_distress": "crisis"
    }
  }
}
```

---

## 🧰 SDK & Libraries

### Python SDK Example

```python
# ash_nlp_sdk.py
import aiohttp
import asyncio
from typing import Dict, Optional, List
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    crisis_level: str
    confidence: float
    needs_response: bool
    processing_time_ms: float
    gaps_detected: bool = False
    requires_staff_review: bool = False
    gap_details: Optional[List[Dict]] = None

class AshNLPSDK:
    def __init__(self, base_url: str = "http://localhost:8881", 
                 api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers
    
    async def analyze(self, message: str, user_id: str, channel_id: str,
                     use_ensemble: bool = True) -> AnalysisResult:
        """Analyze a message for crisis indicators"""
        endpoint = '/analyze' if use_ensemble else '/analyze'
        
        payload = {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id
        }
        
        async with self.session.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=self._get_headers()
        ) as response:
            if response.status != 200:
                raise Exception(f"API Error {response.status}: {await response.text()}")
            
            data = await response.json()
            
            return AnalysisResult(
                crisis_level=data.get('crisis_level', 'none'),
                confidence=data.get('consensus_confidence', data.get('confidence_score', 0.0)),
                needs_response=data.get('needs_response', False),
                processing_time_ms=data.get('processing_time_ms', 0.0),
                gaps_detected=data.get('gaps_detected', False),
                requires_staff_review=data.get('requires_staff_review', False),
                gap_details=data.get('gap_details', [])
            )
    
    async def health_check(self) -> Dict:
        """Check system health"""
        async with self.session.get(
            f"{self.base_url}/health",
            headers=self._get_headers()
        ) as response:
            return await response.json()
    
    async def extract_phrases(self, message: str, user_id: str, channel_id: str,
                            **params) -> Dict:
        """Extract crisis-related phrases"""
        payload = {
            'message': message,
            'user_id': user_id,
            'channel_id': channel_id,
            'parameters': params
        }
        
        async with self.session.post(
            f"{self.base_url}/extract_phrases",
            json=payload,
            headers=self._get_headers()
        ) as response:
            return await response.json()

# Usage example
async def main():
    async with AshNLPSDK() as nlp:
        # Health check
        health = await nlp.health_check()
        print(f"System health: {health['status']}")
        
        # Analyze message
        result = await nlp.analyze(
            message="I am feeling really overwhelmed",
            user_id="user123",
            channel_id="support"
        )
        
        print(f"Crisis level: {result.crisis_level}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Needs response: {result.needs_response}")
        
        if result.gaps_detected:
            print("⚠️ Gap detected - human review recommended")
            print(f"Gap details: {result.gap_details}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔄 Version Migration

### Migrating from v2.x to v3.0

#### API Changes
```javascript
// v2.x Response
{
  "crisis_level": "medium",
  "confidence": 0.67,
  "needs_response": true
}

// v3.0 Response (backward compatible)
{
  "crisis_level": "medium", 
  "confidence_score": 0.67,     // renamed from confidence
  "consensus_confidence": 0.67,  // new ensemble confidence
  "needs_response": true,
  "gaps_detected": false,        // new field
  "requires_staff_review": false // new field
}
```

#### Migration Code
```python
def handle_response_v2_to_v3(response_data):
    """Handle both v2.x and v3.0 response formats"""
    
    # Get confidence (v2.x vs v3.0 field names)
    confidence = (
        response_data.get('consensus_confidence') or 
        response_data.get('confidence_score') or
        response_data.get('confidence', 0.0)
    )
    
    # Check for new v3.0 features
    gaps_detected = response_data.get('gaps_detected', False)
    requires_review = response_data.get('requires_staff_review', False)
    
    # Handle gap detection (v3.0 only)
    if gaps_detected:
        print("⚠️ Model disagreement detected - human review recommended")
        gap_details = response_data.get('gap_details', [])
        for gap in gap_details:
            print(f"Gap type: {gap.get('type')}")
    
    return {
        'crisis_level': response_data.get('crisis_level'),
        'confidence': confidence,
        'needs_response': response_data.get('needs_response', False),
        'requires_review': requires_review
    }
```

---

## 📋 API Changelog

### v3.0.0 (Current)
- ✅ Added three-model ensemble analysis
- ✅ Added `/analyze` endpoint
- ✅ Added gap detection system
- ✅ Added ensemble configuration options
- ✅ Enhanced `/health` and `/stats` endpoints
- ✅ Added Docker secrets support
- ✅ Improved performance optimization
- ✅ Added comprehensive error handling

### v2.1.0 (Previous)
- Added `/extract_phrases` endpoint
- Enhanced learning system
- Improved false positive reduction

### v2.0.0 (Legacy)
- Basic two-model analysis
- Simple `/analyze` endpoint
- Basic health checking

---

**🏳️‍🌈 Built with precision for chosen family - API documentation that grows with your needs.**

*For additional support, join our Discord community or check the troubleshooting guide.*