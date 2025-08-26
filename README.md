<!-- ash-nlp/README.md -->
<!--
README Documentation for Ash-NLP Service
FILE VERSION: v3.1-3d-8.3-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Ash-NLP v3.1 - Crisis Detection Service

**Production-ready mental health crisis detection with 74% performance improvement**

[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da)](https://discord.gg/alphabetcartel)
[![Website](https://img.shields.io/badge/Website-alphabetcartel.org-blue)](https://alphabetcartel.org)
[![GitHub](https://img.shields.io/badge/Version-v3.1-green)](https://github.com/the-alphabet-cartel/ash-nlp)

---

## What is Ash-NLP v3.1?

**Ash-NLP v3.1** is a production-ready crisis detection service engineered for The Alphabet Cartel LGBTQIA+ Discord community. Built with Clean Architecture v3.1 principles, it provides intelligent mental health crisis detection with adaptive learning capabilities and sub-200ms response times.

### Core System Vision
1. **FIRST**: Uses Zero-Shot AI models for primary semantic classification
2. **SECOND**: Enhances AI results with contextual pattern analysis
3. **FALLBACK**: Uses pattern-only classification if AI models fail
4. **PURPOSE**: Detect crisis messages in Discord community communications

---

## Key Features

### Advanced Crisis Detection
- **Multi-model ensemble** with intelligent consensus algorithms
- **Zero-shot classification** for semantic understanding beyond keywords
- **Pattern-based fallback** ensuring continuous operation
- **Adaptive threshold learning** from false positive/negative feedback
- **Context-aware analysis** understanding community-specific language patterns

### Production Performance
- **147ms average response time** (74% improvement from v3.0)
- **Sub-200ms operational performance** exceeding 500ms target by 70%
- **Cold start: 713ms** (acceptable for AI model initialization)
- **27ms variance** providing highly stable performance
- **Comprehensive detailed analysis** with individual AI model scores preserved

### System Architecture
- **Clean Architecture v3.1 compliant** with 100% validated compliance
- **15 specialized managers** with factory function patterns
- **Dependency injection** throughout system architecture
- **Comprehensive error handling** with graceful degradation
- **Docker-first deployment** with production-ready configuration

### Learning Capabilities
- **False positive/negative learning** with automatic threshold adjustment
- **Adaptive sensitivity** based on community feedback patterns
- **Daily adjustment limits** preventing system instability
- **Learning history tracking** with comprehensive audit trails
- **Bounds enforcement** maintaining operational parameters

---

## Quick Start

### Prerequisites
- Docker and Docker Compose
- NVIDIA GPU with 4GB+ VRAM (recommended for AI models)
- 8GB+ system RAM

### Installation

```bash
# Clone repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp

# Set up environment
cp .env.template .env
# Configure your environment variables in .env

# Build and start service
docker-compose build ash-nlp
docker-compose up ash-nlp
```

### Quick Test

```bash
# Health check
curl http://localhost:8881/health

# Crisis analysis
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling really down", 
    "user_id": "test", 
    "channel_id": "test"
  }'
```

### Expected Response
```json
{
  "crisis_score": 0.75,
  "crisis_level": "high",
  "needs_response": true,
  "confidence_score": 0.82,
  "method": "ensemble_consensus",
  "detected_categories": ["emotional_distress", "depression_indicators"],
  "requires_staff_review": false,
  "processing_time": 147.6,
  "ai_model_details": {
    "model_1_score": 0.78,
    "model_2_score": 0.71,
    "model_3_score": 0.76,
    "consensus_reached": true
  }
}
```

---

## Performance Metrics

| Metric | v3.0 Baseline | v3.1 Achievement | Improvement |
|--------|---------------|-------------------|-------------|
| **Average Response Time** | 565ms | 147ms | 74% faster |
| **Cold Start Time** | ~1200ms | 713ms | 40% faster |
| **Memory Efficiency** | Standard | Optimized | ~30% reduction |
| **Architecture Compliance** | 85% | 100% | Full compliance |
| **Code Duplication** | 150+ methods | 15 utilities | 90% reduction |

---

## Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Server Configuration
NLP_SERVER_HOST=0.0.0.0
NLP_SERVER_PORT=8881

# AI Model Configuration
NLP_MODEL_ENSEMBLE_WEIGHTS=[0.4, 0.3, 0.3]
NLP_MODEL_CACHE_ENABLED=true

# Crisis Detection Thresholds
NLP_THRESHOLD_LOW=0.2
NLP_THRESHOLD_MEDIUM=0.4
NLP_THRESHOLD_HIGH=0.6
NLP_THRESHOLD_CRITICAL=0.8

# Learning System
NLP_LEARNING_ENABLED=true
NLP_LEARNING_RATE=0.01
NLP_LEARNING_MAX_ADJUSTMENTS_PER_DAY=50

# Performance Optimization
NLP_PERFORMANCE_BATCH_SIZE=48
NLP_PERFORMANCE_WORKER_THREADS=16
```

### Docker Configuration

Service runs on port 8881 with Docker secrets support:

```yaml
# docker-compose.yml
services:
  ash-nlp:
    build: .
    ports:
      - "8881:8881"
    environment:
      - NLP_SERVER_PORT=8881
    secrets:
      - hugging_face_token
```

---

## API Documentation

### Core Endpoints

#### POST /analyze
Primary crisis detection endpoint
```json
{
  "message": "string",
  "user_id": "string", 
  "channel_id": "string"
}
```

#### GET /health
Service health and status
```json
{
  "status": "healthy",
  "models_loaded": true,
  "response_time": 147.6,
  "version": "v3.1"
}
```

#### POST /learning/feedback
Submit learning feedback
```json
{
  "message": "string",
  "user_id": "string",
  "feedback_type": "false_positive|false_negative|correct",
  "original_result": {}
}
```

### Admin Endpoints

#### GET /admin/stats
System performance statistics

#### POST /admin/thresholds
Update crisis detection thresholds

#### GET /admin/learning/status
Learning system health and metrics

---

## Architecture Overview

### Manager System
Ash-NLP v3.1 uses a clean architecture with 15 specialized managers:

- **UnifiedConfigManager** - Configuration foundation
- **SharedUtilitiesManager** - Common utilities (eliminates 150+ duplicates)
- **LearningSystemManager** - Adaptive learning and feedback processing
- **CrisisAnalyzer** - Primary analysis coordination
- **ModelCoordinationManager** - AI model ensemble management
- **PatternDetectionManager** - Crisis pattern recognition
- **ContextAnalysisManager** - Community context understanding

### Dependencies
```
UnifiedConfigManager (Foundation)
├── SharedUtilitiesManager (Universal utilities)
├── LearningSystemManager (Adaptive learning)
├── ModelCoordinationManager (AI models)
├── CrisisAnalyzer (Analysis coordination)
└── All other specialized managers
```

### Data Flow
```
Discord Message → API → CrisisAnalyzer → AI Models → Pattern Analysis 
                                      → Learning System → Response
```

---

## Integration with Ash Ecosystem

Ash-NLP v3.1 integrates with The Alphabet Cartel ecosystem:

- **[Ash Bot](https://github.com/the-alphabet-cartel/ash-bot)** - Discord crisis response bot
- **[The Alphabet Cartel](https://github.com/the-alphabet-cartel)** - Community organization

### Discord Bot Integration
```python
import aiohttp

async def check_crisis(message, user_id, channel_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8881/analyze',
            json={
                'message': message,
                'user_id': user_id,
                'channel_id': channel_id
            }
        ) as response:
            return await response.json()
```

---

## Development

### Project Structure
```
ash-nlp/
├── main.py                 # Application entry point
├── managers/              # Core business logic managers
│   ├── unified_config.py
│   ├── shared_utilities.py
│   ├── learning_system.py
│   └── ...
├── analysis/              # Crisis analysis components
├── api/                   # FastAPI endpoints
├── config/                # Configuration files
└── docs/                  # Documentation
```

### Code Quality
- **Clean Architecture v3.1** with 100% compliance validation
- **Factory function patterns** for all managers
- **Comprehensive error handling** with graceful degradation
- **Type hints** throughout codebase
- **Docker-first** development and deployment

### Testing
```bash
# Run tests
docker exec ash-nlp python -m pytest tests/

# Performance benchmarks
docker exec ash-nlp python benchmarks/performance_test.py

# Integration tests
docker exec ash-nlp python tests/integration/test_full_pipeline.py
```

---

## Security & Privacy

### Data Protection
- **No persistent storage** - Messages analyzed in-memory only
- **Docker secrets** for sensitive configuration
- **Environment variable validation** preventing exposure
- **Audit logging** for security monitoring

### API Security
- **CORS protection** with configurable origins
- **Rate limiting** preventing abuse
- **Input validation** with comprehensive sanitization
- **Error handling** preventing information disclosure

---

## Monitoring & Observability

### Health Monitoring
```bash
# Service health
curl http://localhost:8881/health

# System statistics  
curl http://localhost:8881/admin/stats

# Learning system status
curl http://localhost:8881/admin/learning/status
```

### Metrics Available
- Response time percentiles
- Crisis detection accuracy
- Model performance metrics
- Learning system effectiveness
- System resource utilization

---

## Community Impact

**Serving The Alphabet Cartel LGBTQIA+ Discord Community**

### Mental Health Focus
- **Crisis pattern recognition** specific to LGBTQIA+ experiences
- **Community-aware language** understanding chosen family dynamics
- **Adaptive learning** from community feedback patterns
- **Immediate response capability** for mental health emergencies

### Technology for Good
- **Open source** for transparency and community improvement
- **Privacy-first** design with no data persistence
- **Community-driven** development with user feedback integration
- **Accessible deployment** with Docker-based setup

---

## Documentation

### Complete Documentation Suite
- **[API Guide](docs/api/api_guide.md)** - Complete API reference and integration guide
- **[Team Guide](docs/team/team_guide.md)** - Crisis response team operational guide
- **[Technical Guide](docs/tech/technical_guide.md)** - Architecture and development guide
- **[Manager Documentation](docs/tech/managers/)** - Individual manager specifications

### Troubleshooting
- **[Common Issues](docs/troubleshooting.md)** - Solutions for typical problems
- **[Performance Optimization](docs/performance.md)** - System tuning guidance
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions

---

## Contributing

We welcome contributions to enhance crisis detection capabilities for LGBTQIA+ communities:

1. **Fork the repository** and create a feature branch
2. **Follow Clean Architecture v3.1** principles in all code changes
3. **Add comprehensive tests** for new functionality
4. **Update documentation** to reflect changes
5. **Submit pull request** with detailed description

### Development Environment
```bash
# Set up development environment
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp
cp .env.template .env.dev
docker-compose -f docker-compose.dev.yml up --build
```

---

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

**Open source for community mental health support.**

---

## Community

**The Alphabet Cartel** - Building technology for LGBTQIA+ communities

### Core Values
- **Safety First** - Every design decision prioritizes user wellbeing
- **Community-Driven** - Built with and for the communities we serve  
- **Transparency** - Open source, auditable, and improvable by all
- **Chosen Family** - Technology supporting found family connections

### Connect With Us
- **Discord**: [Join our community](https://discord.gg/alphabetcartel)
- **Website**: [alphabetcartel.org](https://alphabetcartel.org)
- **GitHub**: [github.com/the-alphabet-cartel](https://github.com/the-alphabet-cartel)

---

*Ash-NLP v3.1: Engineered for community mental health support, one conversation at a time.*

**Built with care for chosen family** 🏳️‍🌈