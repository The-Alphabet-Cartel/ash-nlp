<!-- ash-nlp/docs/tech/technical_guide.md -->
<!--
Technical Guide for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Technical Guide

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# Ash-NLP v5.0 Technical Architecture Guide

Comprehensive technical documentation for developers working with Ash-NLP's crisis detection system.

---

## Architecture Overview

### Clean Architecture v5.0 Implementation

Ash-NLP v5.0 implements Clean Architecture principles with strict dependency direction enforcement and comprehensive separation of concerns.

```
┌────────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                         │
├────────────────────────────────────────────────────────────────┤
│                 Application Services                           │
│  ┌────────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ CrisisAnalyzer │  |Learning     │  | Admin Services      │  │
│  └────────────────┘  │ Services    │  └─────────────────────┘  │
│                      └─────────────┘                           │
├────────────────────────────────────────────────────────────────┤
│                   Manager Layer (Business Logic)               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Specialized Managers with Factory Functions             │   │
│  │ - ModelCoordinationManager                              │   │
│  │ - PatternsDetectionManager                              │   │
│  │ │ ... others                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────┤
│               Infrastructure Layer                             │
│  ┌──────────────────┐  ┌────────────────────────────────┐      │
│  │ UnifiedConfig    │  │ SharedUtilitiesManager         │      │
│  │ Manager          │  │ (Core Utilities)               │      │
│  │ (Foundation)     │  └────────────────────────────────┘      │
│  └──────────────────┘                                          │
└────────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

#### 1. Dependency Direction
All dependencies flow inward toward business logic:
```python
# Correct: Infrastructure depends on managers
SharedUtilitiesManager(unified_config: UnifiedConfigManager)

# Correct: Application services depend on managers  
CrisisAnalyzer(model_manager, learning_manager, ...)

# Never: Managers depending on API layer
```

#### 2. Factory Function Pattern
All managers use factory functions for initialization:
```python
def create_learning_system_manager(
    unified_config: UnifiedConfigManager = None,
    shared_utils: SharedUtilitiesManager = None
) -> LearningSystemManager:
    return LearningSystemManager(unified_config, shared_utils)
```

#### 3. Configuration Externalization
Configuration managed through JSON + environment variables:
```python
# JSON provides defaults
config = {
    "learning_rate": 0.01,
    "max_adjustments": 50
}

# Environment variables override
NLP_LEARNING_RATE=0.02
NLP_LEARNING_MAX_ADJUSTMENTS=75
```

---

## System Components

### Core Analysis Pipeline

The crisis detection pipeline follows this flow:

1. **Message Input** → API receives Discord message
2. **CrisisAnalyzer** → Coordinates analysis across managers
3. **AI Model Processing** → Zero-shot classification via ModelCoordinationManager
4. **Pattern Analysis** → Contextual patterns via PatternDetectionManager  
5. **Learning Application** → Adjustments via LearningSystemManager
6. **Response Generation** → Structured result with confidence scores

### Manager System

#### UnifiedConfigManager (Foundation Layer)
**Purpose**: Single source of truth for all configuration access
**Dependencies**: None (foundation layer)
**Key Methods**:
- `get_config_section(section, key, default)`
- `get_env_str(key, default)`
- `get_env_dict()`

```python
# Always access config through this manager
config = unified_config.get_config_section('models', 'ensemble_weights', [0.4, 0.3, 0.3])
```

#### SharedUtilitiesManager (Universal Utilities)
**Purpose**: Eliminate 150+ duplicate methods across managers
**Dependencies**: UnifiedConfigManager
**Key Utilities**:
- `safe_bool_convert()` - Gold standard boolean conversion
- `safe_int_convert()` / `safe_float_convert()` - Type conversion with validation
- `get_setting_with_type_conversion()` - Configuration with type safety
- `handle_error_with_fallback()` - Structured error handling

```python
# Example usage in any manager
enabled = shared_utils.safe_bool_convert(
    config_value, 
    default=True, 
    param_name='crisis_detection_enabled'
)
```

#### LearningSystemManager (Adaptive Learning)
**Purpose**: Consolidated learning from false positive/negative feedback
**Dependencies**: UnifiedConfigManager, SharedUtilitiesManager
**Key Capabilities**:
- Threshold adjustments with safety bounds
- Daily adjustment limits (prevent system instability)
- Learning history tracking and analysis
- Feedback processing for continuous improvement

```python
# Adjust threshold after false positive
result = learning_manager.adjust_threshold_for_false_positive(
    current_threshold=0.6,
    crisis_level="medium"
)
# Returns: {"old_threshold": 0.6, "new_threshold": 0.58, "adjusted": true}
```

#### ModelCoordinationManager (AI Model Ensemble)
**Purpose**: Coordinate multiple AI models for crisis detection
**Key Features**:
- Three-model ensemble (depression, sentiment, distress detection)
- Consensus algorithms (majority, weighted, unanimous)
- Model loading and health monitoring
- Performance optimization and caching

```python
# Ensemble analysis
result = model_manager.ensemble_analyze(
    message="I'm feeling really down",
    method="weighted_consensus"
)
# Returns detailed analysis with individual model scores
```

#### PatternDetectionManager (Crisis Patterns)
**Purpose**: Detect crisis patterns beyond AI model classification
**Key Patterns**:
- Keyword-based detection for fallback scenarios
- Contextual pattern analysis
- Community-specific language patterns
- Pattern confidence scoring

#### CrisisThresholdManager (Threshold Management)
**Purpose**: Manage crisis level thresholds and boundaries
**Key Features**:
- Dynamic threshold adjustment based on learning
- Bounds enforcement for system stability
- Threshold validation and safety checks

---

## Development Environment

### Prerequisites

#### System Requirements
- **Docker** 20.10+ with Docker Compose
- **Python** 3.9+ (for local development)
- **NVIDIA GPU** with 4GB+ VRAM (recommended for AI models)
- **8GB+ RAM** for full system operation

#### Development Setup
```bash
# Clone repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp

# Copy development environment template
cp .env.template .env.development

# Build development container
docker-compose -f docker-compose.dev.yml build

# Start development environment
docker-compose -f docker-compose.dev.yml up
```

### Project Structure
```
ash-nlp/
├── .env                        # Environment Variables
├── analysis/                   # Crisis analysis components
|   └── crisis_analysis.py      # Crisis Analysis Module
├── api/                        # FastAPI endpoints
|   ├── admin_endpoints.py      # Admin endpoints
|   └── user_endpoints.py       # User endpoints
├── backups/                    # Backup management
|   ├── daily                   # Daily backups
|   ├── monthly                 # Monthly backups
|   ├── weekly                  # Weekly backups
|   └── yearly                  # Yearly backups
├── cache/                      # Cache management
|   └── models/                 # Models Cache
|       └── offload/            # Offloaded models
├── config/                     # Configuration files
|   ├── analysis_config.json    # Analysis Configuration
|   ├── feature_flags.json      # Feature Flags Configuration
|   ├── logging_config.json     # Logging Configuration
|   ├── model_config.json       # Model Configuration
|   ├── patterns_config.json    # Patterns Configuration
|   ├── performance_config.json # Performance Configuration
|   ├── server_config.json      # Server Configuration
|   ├── settings_config.json    # Settings Configuration
|   ├── storage_config.json     # Storage Configuration
|   ├── threshold_config.json   # Crisis Threshold Configuration
|   └── zero_shot.json          # Zero Shot Label Configuration
├── data/                       # Data management
|   ├── analysis                # Analysis data
|   ├── learning                # Learning data (Future)
|   └── patterns                # Patterns data
├── docker-compose.yml          # Docker Configuration
├── docs/                       # Documentation
├── logs/                       # Logs management
├── main.py                     # Application entry point
└── managers/                   # Core managers
|   ├── context_analysis.py     # Context Analysis Manager
|   ├── feature_flags.py        # Feature Flags Manager
|   ├── logging_manager.py      # Logging Manager
|   ├── model_manager.py        # Model Manager
|   ├── patterns_manager.py     # Patterns Manager
|   ├── performance_manager.py  # Performance Manager
|   ├── server_config.py        # Server Configuration Manager
|   ├── settings_config.py      # Settings Configuration Manager
|   ├── shared_utilities.py     # Shared Utilities Manager
|   ├── storage_config.py       # Storage Configuration Manager
|   ├── threshold_manager.py    # Threshold Manager
|   ├── unified_config.py       # Unified Configuration Manager
|   └── zero_shot.py            # Zero-Shot Manager
└── tests/                      # Testing Suites
    ├── fixtures                # Fixtures for testing
    ├── integrations            # Integration tests
    ├── performance             # Performance tests
    └── unit                    # Unit tests
```

### Code Standards

#### Clean Architecture Compliance
Every code change must follow Clean Architecture v5.0 principles:

```python
# ✅ Correct: Factory function with dependency injection
def create_example_manager(unified_config: UnifiedConfigManager) -> ExampleManager:
    if not unified_config:
        raise ValueError("unified_config is required")
    return ExampleManager(unified_config)

# ❌ Incorrect: Direct constructor call
manager = ExampleManager()  # Missing dependencies
```

#### File Version Headers
All Python files must include version headers:
```python
"""
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
"""
```

#### Error Handling Pattern
Use SharedUtilitiesManager for consistent error handling:
```python
try:
    result = risky_operation()
    return result
except Exception as e:
    return self.shared_utils.handle_error_with_fallback(
        e,
        fallback_value={'status': 'error', 'score': 0.5},
        context='crisis_analysis',
        operation='analyze_message'
    )
```

---

## AI Model Integration

### Model Architecture

#### Three-Model Ensemble System
1. **Depression Detection Model**
   - Model: `MoritzLaurer/deberta-v3-base-zeroshot-v2.0`
   - Purpose: Primary crisis classification with clinical focus
   - Weight: 40% in ensemble

2. **Sentiment Analysis Model**  
   - Model: `Lowerated/lm6-deberta-v3-topic-sentiment`
   - Purpose: Emotional tone and context analysis
   - Weight: 30% in ensemble

3. **Distress Detection Model**
   - Model: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`
   - Purpose: General emotional distress indicators
   - Weight: 30% in ensemble

### Model Coordination Implementation

```python
class ModelCoordinationManager:
    def ensemble_analyze(self, message: str, method: str = "weighted") -> Dict:
        # Load models if not already cached
        models = self._ensure_models_loaded()
        
        # Analyze with each model
        model_results = []
        for model in models:
            result = self._analyze_with_model(model, message)
            model_results.append(result)
        
        # Apply ensemble method
        if method == "weighted":
            return self._weighted_consensus(model_results)
        elif method == "majority":
            return self._majority_consensus(model_results)
        elif method == "unanimous":
            return self._unanimous_consensus(model_results)
```

### Performance Optimization

#### Caching Strategy
- **Model caching**: Keep loaded models in GPU memory
- **Result caching**: Cache analysis results for identical messages
- **Configuration caching**: Cache configuration access patterns

#### Batch Processing
```python
# Process multiple messages efficiently
batch_results = model_manager.batch_analyze(
    messages=message_list,
    batch_size=48,  # Optimized for RTX 3060
    return_individual_scores=True
)
```

#### Memory Management
- **Lazy loading**: Load models only when needed
- **Memory monitoring**: Track GPU and system memory usage
- **Cleanup procedures**: Release unused models and cached data

---

## Database Integration

### Current State (v5.0)
Ash-NLP v5.0 operates without persistent database storage, analyzing messages in-memory only for privacy protection.

### Planned Database Integration (Future)
```python
# Future database integration pattern
class DatabaseManager:
    def record_analysis(self, analysis_result: Dict, store_message: bool = False):
        # Store analysis metadata without message content
        record = {
            'timestamp': analysis_result['timestamp'],
            'crisis_score': analysis_result['crisis_score'],
            'crisis_level': analysis_result['crisis_level'],
            'user_id_hash': self._hash_user_id(analysis_result['user_id']),
            'channel_id': analysis_result['channel_id'],
            'processing_time': analysis_result['processing_time'],
            'model_consensus': analysis_result.get('consensus_reached', False)
        }
        if store_message:  # Only with explicit consent
            record['message_hash'] = self._hash_message(analysis_result['message'])
        
        return self._store_record(record)
```

---

## Performance Optimization

### Phase 3e Performance Achievements
- **74% performance improvement** (565ms → 147ms average response time)
- **Cold start optimization** (1200ms → 713ms initialization time)
- **Memory efficiency** (~30% reduction in duplicate code)
- **Architecture consolidation** (150+ duplicate methods → 15 utilities)

### Optimization Techniques

#### 1. Analysis Pipeline Optimization
```python
# Located in analysis/performance_optimizations.py
class PerformanceOptimizer:
    def optimize_analysis_pipeline(self, message: str) -> Dict:
        # Lazy load models only when needed
        if not self._models_cached:
            self._load_models_async()
        
        # Use synchronous methods for better performance
        model_results = self._batch_model_analysis(message)
        pattern_results = self._fast_pattern_analysis(message)
        
        # Combine results efficiently
        return self._merge_analysis_results(model_results, pattern_results)
```

#### 2. Configuration Management Optimization
```python
# Lazy loading with runtime fallback
class UnifiedConfigManager:
    def get_config_section(self, section: str, key: str, default: Any) -> Any:
        if not self._config_loaded:
            self._lazy_load_config()
        
        # Use cached configuration access patterns
        cache_key = f"{section}.{key}"
        if cache_key in self._config_cache:
            return self._config_cache[cache_key]
        
        value = self._get_nested_value(section, key, default)
        self._config_cache[cache_key] = value
        return value
```

#### 3. Model Coordination Enhancements
```python
# Synchronous methods for performance
class ModelCoordinationManager:
    def get_ensemble_analysis_sync(self, message: str) -> Dict:
        # Use synchronous model calls for better performance
        results = {
            'model_1': self._model_1_analyze_sync(message),
            'model_2': self._model_2_analyze_sync(message), 
            'model_3': self._model_3_analyze_sync(message)
        }
        
        return self._calculate_consensus(results)
```

### Benchmarking and Monitoring

#### Performance Metrics Collection
```python
class PerformanceMonitor:
    def measure_analysis_performance(self) -> Dict:
        return {
            'response_times': {
                'average': 147.6,
                'p50': 142.3,
                'p95': 186.7,
                'p99': 234.5
            },
            'system_metrics': {
                'memory_usage': self._get_memory_usage(),
                'gpu_memory': self._get_gpu_memory(),
                'cpu_utilization': self._get_cpu_usage()
            },
            'analysis_metrics': {
                'requests_per_minute': self._get_throughput(),
                'error_rate': self._get_error_rate(),
                'model_consensus_rate': self._get_consensus_rate()
            }
        }
```

---

## Testing Framework

### Test Structure
```
tests/
├── unit/                      # Unit tests for individual managers
│   ├── test_learning_system.py
│   ├── test_shared_utilities.py
│   ├── test_model_coordination.py
│   └── ...
├── integration/               # Integration tests across components
│   ├── test_full_pipeline.py
│   ├── test_manager_integration.py
│   └── test_api_endpoints.py
├── performance/               # Performance and benchmark tests
│   ├── test_response_times.py
│   ├── test_memory_usage.py
│   └── benchmark_analysis.py
└── fixtures/                  # Test data and configuration
    ├── sample_messages.json
    ├── test_config.json
    └── mock_responses.json
```

### Testing Patterns

#### Manager Unit Testing
```python
# tests/unit/test_learning_system.py
import pytest
from managers.learning_system import create_learning_system_manager
from managers.unified_config import create_unified_config_manager
from managers.shared_utilities import create_shared_utilities_manager

class TestLearningSystemManager:
    def setup_method(self):
        """Setup test dependencies using factory functions"""
        self.unified_config = create_unified_config_manager()
        self.shared_utils = create_shared_utilities_manager(self.unified_config)
        self.learning_manager = create_learning_system_manager(
            self.unified_config, 
            self.shared_utils
        )
    
    def test_false_positive_adjustment(self):
        """Test threshold adjustment for false positive feedback"""
        result = self.learning_manager.adjust_threshold_for_false_positive(
            current_threshold=0.6,
            crisis_level="medium"
        )
        
        assert result['adjusted'] == True
        assert result['new_threshold'] < 0.6  # Should reduce threshold
        assert 0.5 <= result['new_threshold'] <= 1.5  # Within bounds
    
    def test_daily_adjustment_limits(self):
        """Test daily adjustment limit enforcement"""
        # Make maximum adjustments
        for _ in range(50):  # Default daily limit
            self.learning_manager.adjust_threshold_for_false_positive(0.6, "medium")
        
        # Next adjustment should be blocked
        result = self.learning_manager.adjust_threshold_for_false_positive(0.6, "medium")
        assert result['adjusted'] == False
        assert "Daily adjustment limit reached" in result['message']
```

#### Integration Testing
```python
# tests/integration/test_full_pipeline.py
class TestFullAnalysisPipeline:
    def test_complete_crisis_analysis(self):
        """Test end-to-end crisis analysis pipeline"""
        # Setup complete system
        system = self._setup_complete_system()
        
        # Test message requiring crisis response
        message = "I can't take this anymore and don't want to be here"
        result = system.analyze_crisis(message, "test_user", "test_channel")
        
        # Verify comprehensive analysis
        assert result['crisis_score'] > 0.6  # High crisis score expected
        assert result['crisis_level'] in ['high', 'critical']
        assert result['needs_response'] == True
        assert 'ai_model_details' in result
        assert 'pattern_analysis' in result
        
        # Verify performance requirements
        assert result['processing_time'] < 500  # Under 500ms target
    
    def test_learning_feedback_integration(self):
        """Test learning system integration with analysis pipeline"""
        system = self._setup_complete_system()
        
        # Analyze message
        message = "Having a rough day but I'll be okay"
        result = system.analyze_crisis(message, "test_user", "test_channel")
        
        # Submit false positive feedback
        feedback_result = system.process_feedback(
            message, "test_user", "test_channel", 
            "false_positive", result
        )
        
        assert feedback_result['feedback_processed'] == True
        assert feedback_result['learning_applied'] == True
```

#### Performance Testing
```python
# tests/performance/benchmark_analysis.py
class PerformanceBenchmark:
    def test_response_time_requirements(self):
        """Verify response time meets performance targets"""
        system = self._setup_performance_system()
        test_messages = self._load_test_messages(100)
        
        response_times = []
        for message in test_messages:
            start_time = time.time()
            result = system.analyze_crisis(message, "perf_user", "perf_channel")
            end_time = time.time()
            
            response_times.append((end_time - start_time) * 1000)
        
        # Verify performance targets
        avg_time = sum(response_times) / len(response_times)
        p95_time = sorted(response_times)[94]  # 95th percentile
        
        assert avg_time < 200  # Average under 200ms
        assert p95_time < 300  # 95th percentile under 300ms
        
    def test_memory_usage_stability(self):
        """Test memory usage remains stable under load"""
        system = self._setup_performance_system()
        initial_memory = self._get_memory_usage()
        
        # Process 1000 messages
        for i in range(1000):
            message = f"Test message {i} with varying content lengths"
            system.analyze_crisis(message, f"user_{i}", "perf_channel")
        
        final_memory = self._get_memory_usage()
        memory_growth = final_memory - initial_memory
        
        # Memory growth should be minimal
        assert memory_growth < 100  # Less than 100MB growth
```

### Running Tests
```bash
# Run all tests
docker exec ash-nlp python -m pytest tests/

# Run specific test categories
docker exec ash-nlp python -m pytest tests/unit/
docker exec ash-nlp python -m pytest tests/integration/
docker exec ash-nlp python -m pytest tests/performance/

# Run with coverage reporting
docker exec ash-nlp python -m pytest --cov=managers tests/

# Run performance benchmarks
docker exec ash-nlp python tests/performance/benchmark_analysis.py
```

---

## Deployment Guide

### Production Deployment

#### Docker Configuration
```yaml
# docker-compose.yml
services:
  ash-nlp:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "30880:30880"
    environment:
      - NLP_SERVER_HOST=0.0.0.0
      - NLP_SERVER_PORT=30880
      - NLP_PERFORMANCE_OPTIMIZATION=true
    secrets:
      - hugging_face_token
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    restart: unless-stopped

secrets:
  hugging_face_token:
    file: ./secrets/hugging_face_token.txt
```

#### Environment Configuration
```bash
# Production .env file
NLP_SERVER_HOST=0.0.0.0
NLP_SERVER_PORT=30880

# Performance optimization
NLP_PERFORMANCE_BATCH_SIZE=48
NLP_PERFORMANCE_WORKER_THREADS=16
NLP_PERFORMANCE_MODEL_CACHING=true

# Crisis detection thresholds
NLP_THRESHOLD_LOW=0.2
NLP_THRESHOLD_MEDIUM=0.4
NLP_THRESHOLD_HIGH=0.6
NLP_THRESHOLD_CRITICAL=0.8

# Learning system
NLP_LEARNING_ENABLED=true
NLP_LEARNING_RATE=0.01
NLP_LEARNING_MAX_ADJUSTMENTS_PER_DAY=50

# AI Model configuration
NLP_MODEL_ENSEMBLE_WEIGHTS=[0.4,0.3,0.3]
NLP_MODEL_CACHE_ENABLED=true
NLP_MODEL_TIMEOUT=30

# Logging
NLP_LOGGING_LEVEL=INFO
NLP_LOGGING_FORMAT=json
NLP_LOGGING_FILE=/app/logs/ash-nlp.log
```

### Health Monitoring

#### Health Check Endpoint
```python
# Comprehensive health monitoring
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "v5.0",
        "models_loaded": model_manager.are_models_loaded(),
        "managers_initialized": len(initialized_managers),
        "response_time": performance_monitor.get_avg_response_time(),
        "memory_usage": system_monitor.get_memory_info(),
        "uptime": time.time() - start_time
    }
```

#### Monitoring Integration
```python
# Prometheus metrics integration
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
analysis_requests = Counter('analysis_requests_total', 'Total analysis requests')
analysis_duration = Histogram('analysis_duration_seconds', 'Analysis processing time')
crisis_detections = Counter('crisis_detections_total', 'Total crisis detections', ['level'])
system_health = Gauge('system_health_score', 'Overall system health score')

# Use in analysis pipeline
@analysis_duration.time()
def analyze_crisis(message: str, user_id: str, channel_id: str):
    analysis_requests.inc()
    result = perform_analysis(message, user_id, channel_id)
    
    if result['needs_response']:
        crisis_detections.labels(level=result['crisis_level']).inc()
    
    return result
```

### Security Considerations

#### Input Validation
```python
from pydantic import BaseModel, Field, validator

class MessageRequest(BaseModel):
    message: str = Field(..., max_length=4000, min_length=1)
    user_id: str = Field(..., max_length=100, min_length=1)
    channel_id: str = Field(..., max_length=100, min_length=1)
    
    @validator('message')
    def validate_message(cls, v):
        # Sanitize input but preserve crisis detection capability
        if len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        
        # Check for potential injection attempts
        suspicious_patterns = ['<script', 'javascript:', 'data:']
        if any(pattern in v.lower() for pattern in suspicious_patterns):
            raise ValueError('Message contains potentially harmful content')
        
        return v.strip()
```

#### API Security
```python
from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.post("/analyze")
@limiter.limit("60/minute")  # 60 requests per minute per IP
async def analyze_crisis(request: Request, message_request: MessageRequest):
    try:
        # Validate and process request
        result = crisis_analyzer.analyze_crisis(
            message_request.message,
            message_request.user_id,
            message_request.channel_id
        )
        return result
    except Exception as e:
        # Log error without exposing internal details
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis processing failed")
```

---

## Troubleshooting

### Common Issues

#### 1. Model Loading Failures
**Symptoms**: 503 Service Unavailable, "AI models not loaded"
**Causes**: Insufficient GPU memory, network issues, missing tokens
**Solutions**:
```bash
# Check GPU memory
nvidia-smi

# Check container logs
docker logs ash-nlp

# Verify Hugging Face token
docker exec ash-nlp python -c "from huggingface_hub import HfApi; api = HfApi(); print(api.whoami())"

# Clear model cache and restart
docker exec ash-nlp rm -rf ~/.cache/huggingface/
docker-compose restart ash-nlp
```

#### 2. High Response Times
**Symptoms**: Analysis taking >1000ms consistently
**Causes**: Cold start, insufficient resources, configuration issues
**Solutions**:
```bash
# Check system resources
docker stats ash-nlp

# Enable performance optimizations
export NLP_PERFORMANCE_OPTIMIZATION=true
export NLP_PERFORMANCE_BATCH_SIZE=32

# Warm up models
curl -X POST http://localhost:30880/analyze -d '{"message":"test","user_id":"warmup","channel_id":"warmup"}'
```

#### 3. Learning System Issues
**Symptoms**: No learning adjustments, high false positive rate
**Causes**: Daily limits reached, configuration errors, validation failures
**Solutions**:
```bash
# Check learning system status
curl http://localhost:30880/admin/learning/status

# Reset daily adjustment count (admin only)
docker exec ash-nlp python -c "
from managers.learning_system import create_learning_system_manager
from managers.unified_config import create_unified_config_manager
from managers.shared_utilities import create_shared_utilities_manager

config = create_unified_config_manager()
utils = create_shared_utilities_manager(config)
learning = create_learning_system_manager(config, utils)
print(learning.clear_adjustment_history())
"
```

#### 4. Configuration Issues
**Symptoms**: Default values being used, missing environment variables
**Causes**: Incorrect .env file, missing configuration files
**Solutions**:
```bash
# Validate configuration
docker exec ash-nlp python -c "
from managers.unified_config import create_unified_config_manager
config = create_unified_config_manager()
print('Config loaded:', config.get_env_dict().keys())
"

# Check configuration file permissions
ls -la config/

# Reload configuration
docker-compose restart ash-nlp
```

### Debug Mode

#### Enable Debug Logging
```bash
# Set debug environment variables
export NLP_LOGGING_LEVEL=DEBUG
export NLP_DEBUG_MODE=true

# Restart with debug logging
docker-compose up ash-nlp
```

#### Debug Analysis Pipeline
```python
# Debug specific analysis
import requests

response = requests.post('http://localhost:30880/analyze', json={
    'message': 'debug test message',
    'user_id': 'debug_user',
    'channel_id': 'debug_channel',
    'debug': True  # Enable debug mode
})

print("Debug Analysis Result:")
print(response.json())
```

---

## Contributing

### Development Workflow

#### 1. Fork and Clone
```bash
git clone https://github.com/your-username/ash-nlp.git
cd ash-nlp
git checkout -b feature/your-feature-name
```

#### 2. Set Up Development Environment
```bash
cp .env.template .env.development
# Configure development settings
docker-compose -f docker-compose.dev.yml up --build
```

#### 3. Make Changes Following Clean Architecture
```python
# Example: Adding new manager
def create_new_manager(unified_config: UnifiedConfigManager) -> NewManager:
    """Factory function following Clean v5.0 pattern"""
    if not unified_config:
        raise ValueError("unified_config is required")
    return NewManager(unified_config)

class NewManager:
    def __init__(self, unified_config: UnifiedConfigManager):
        # Follow dependency injection pattern
        self.config_manager = unified_config
        self.logger = logging.getLogger(__name__)
        
    def new_functionality(self) -> Dict[str, Any]:
        # Use SharedUtilitiesManager for common operations
        return self.shared_utils.handle_error_with_fallback(
            operation, fallback_value, context, operation_name
        )
```

#### 4. Add Tests
```python
# tests/unit/test_new_manager.py
class TestNewManager:
    def setup_method(self):
        self.config = create_unified_config_manager()
        self.manager = create_new_manager(self.config)
    
    def test_new_functionality(self):
        result = self.manager.new_functionality()
        assert result is not None
        # Add comprehensive assertions
```

#### 5. Submit Pull Request
- Ensure all tests pass
- Update documentation
- Follow commit message conventions
- Request review from maintainers

### Code Review Checklist

#### Architecture Compliance
- [ ] Uses factory functions for all managers
- [ ] Follows dependency injection patterns  
- [ ] Dependencies flow inward toward business logic
- [ ] Uses SharedUtilitiesManager for common operations
- [ ] Includes proper error handling with fallbacks

#### Code Quality
- [ ] Includes comprehensive tests with >90% coverage
- [ ] Follows type hints throughout
- [ ] Includes proper logging and monitoring
- [ ] Updates documentation for new features
- [ ] Maintains performance standards (<200ms avg response)

#### Security and Privacy
- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user data
- [ ] No persistent storage of message content
- [ ] Proper error handling without information disclosure

---

## Future Roadmap

### Planned Enhancements

#### Database Integration
- **Metadata storage** for analysis patterns and performance metrics
- **Learning history persistence** across service restarts
- **User feedback tracking** for continuous improvement
- **Analytics dashboard** for crisis response team insights

#### Advanced AI Models
- **Fine-tuned models** specifically for LGBTQIA+ community language
- **Multi-language support** for diverse community members
- **Context-aware analysis** using conversation history
- **Emotional intelligence** improvements with better empathy detection

#### Scalability Improvements
- **Horizontal scaling** with load balancer support
- **Microservices architecture** for component isolation
- **Kubernetes deployment** for container orchestration
- **Multi-region deployment** for global community support

#### Enhanced Learning System
- **Community-specific learning** based on server context
- **Temporal pattern recognition** for seasonal or event-based adjustments
- **Advanced feedback mechanisms** with staff rating systems
- **Automated threshold optimization** using machine learning

---

## Conclusion

Ash-NLP v5.0 represents a significant advancement in crisis detection technology specifically designed for LGBTQIA+ communities. The Clean Architecture implementation provides a solid foundation for continued development.

### Key Technical Achievements
- **74% performance improvement** through architectural optimization
- **100% Clean Architecture compliance** with comprehensive validation
- **90% code reduction** through utility consolidation
- **Production-ready deployment** with comprehensive monitoring

### Development Principles
- **Community-first design** prioritizing user safety and privacy
- **Transparent decision-making** with explainable AI analysis
- **Continuous learning** from community feedback and usage patterns
- **Open source collaboration** enabling community-driven improvements

The combination of advanced AI capabilities, clean architecture, and community-focused design creates a powerful platform for supporting mental health in LGBTQIA+ Discord communities.

---

*Technical Guide for Ash-NLP v5.0 - Engineering excellence for community mental health support.*

**Built with care for chosen family** 🏳️‍🌈
