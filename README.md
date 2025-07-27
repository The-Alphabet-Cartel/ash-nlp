# Ash-NLP - Natural Language Processing Server

**Part of the Ash Ecosystem** | **Main Repository:** https://github.com/the-alphabet-cartel/ash

This repository contains **only the NLP processing server component** of the Ash crisis detection system. For the complete ecosystem including Discord bot, dashboard, and testing suite, see the [main Ash repository](https://github.com/the-alphabet-cartel/ash).

**Discord Community:** https://discord.gg/alphabetcartel  
**Website:** http://alphabetcartel.org  
**Organization:** https://github.com/the-alphabet-cartel

## 🧠 About Ash-NLP

Ash-NLP is the machine learning brain of The Alphabet Cartel's crisis detection system. It provides advanced natural language processing capabilities to analyze Discord messages for crisis indicators, working in conjunction with the Discord bot's keyword-based detection to create a comprehensive hybrid approach.

### 🏗️ Architecture Position

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Discord Bot   │◄──►│   NLP Server    │◄──►│   Dashboard     │
│   (ash-bot)     │    │   (THIS REPO)   │    │   (ash-dash)    │
│                 │    │                 │    │                 │
│ 10.20.30.253    │    │ 10.20.30.16     │    │ 10.20.30.16     │
│ Port: 8882      │    │ Port: 8881      │    │ Port: 8883      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                 ▲
                                 │
                       ┌─────────────────┐
                       │  Testing Suite  │
                       │  (ash-thrash)   │
                       │                 │
                       │ 10.20.30.16     │
                       │ Port: 8884      │
                       └─────────────────┘
```

## 🚀 Quick Start

### For NLP Development
If you're working on the NLP server specifically:

```bash
# Clone this repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp

# Setup development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Configure environment
cp .env.template .env
# Edit .env with your Claude API key and configuration

# Run development server
python -m src.main
```

### For Complete Ecosystem
If you need the full Ash system (recommended):

```bash
# Clone the main ecosystem repository
git clone --recursive https://github.com/the-alphabet-cartel/ash.git
cd ash

# Follow setup instructions in main repository
# This includes ash-nlp as a submodule along with all other components
```

## 🔧 Core Features

### Advanced NLP Analysis
- **Crisis Sentiment Detection**: Machine learning models trained on crisis language patterns
- **Context Understanding**: Analyzes conversation flow and emotional progression
- **Multi-model Ensemble**: Combines multiple AI approaches for robust detection
- **Real-time Processing**: Optimized for Discord's fast-paced communication

### Claude AI Integration
- **Advanced Language Understanding**: Leverages Claude 4 Sonnet for sophisticated analysis
- **Contextual Risk Assessment**: Understands nuanced emotional states and crisis indicators
- **Adaptive Responses**: Learns from team feedback to improve detection accuracy
- **Privacy-Preserving**: Processes text without storing personal information

### High-Performance Infrastructure
- **GPU Acceleration**: Utilizes RTX 3050 for fast model inference
- **Caching System**: Redis-based caching for frequently analyzed patterns
- **Load Balancing**: Handles multiple concurrent requests from Discord bot
- **Fail-safe Design**: Graceful degradation when external services unavailable

## 📦 Repository Structure

```
ash-nlp/                          # THIS REPOSITORY
├── src/                          # Main application source
│   ├── main.py                   # FastAPI server entry point
│   ├── api/                      # REST API endpoints
│   │   ├── routes/               # API route definitions
│   │   ├── middleware/           # Request/response middleware
│   │   └── models/               # API data models
│   ├── nlp/                      # NLP processing core
│   │   ├── analyzers/            # Text analysis modules
│   │   ├── models/               # ML model management
│   │   ├── preprocessing/        # Text preprocessing utilities
│   │   └── ensemble/             # Multi-model coordination
│   ├── integrations/             # External service integrations
│   │   ├── claude/               # Claude AI integration
│   │   ├── cache/                # Caching system
│   │   └── monitoring/           # Performance monitoring
│   └── utils/                    # Utility functions
│       ├── config.py             # Configuration management
│       ├── logger.py             # Logging setup
│       └── validators.py         # Input validation
├── models/                       # ML model files and cache
├── tests/                        # Unit and integration tests
├── docs/                         # NLP-specific documentation
├── scripts/                      # Utility and deployment scripts
├── docker/                       # Docker configuration
├── .env.template                 # Environment configuration template
├── docker-compose.yml            # Docker deployment configuration
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
└── README.md                     # This file
```

## 🛠️ Development

### Prerequisites
- Python 3.9+
- NVIDIA GPU with CUDA support (RTX 3050 recommended)
- Claude API key (for advanced analysis)
- Docker with GPU support
- 64GB RAM recommended for model loading

### Environment Configuration

Create `.env` file from template:
```bash
cp .env.template .env
```

Required environment variables:
```bash
# Claude AI Configuration
CLAUDE_API_KEY=your_claude_api_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514

# Server Configuration
API_PORT=8881
API_HOST=0.0.0.0
ENVIRONMENT=development

# GPU Configuration
ENABLE_GPU=true
CUDA_VISIBLE_DEVICES=0

# Performance Settings
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT_SECONDS=30
CACHE_TTL_MINUTES=60

# Model Configuration
MODEL_CACHE_DIR=/app/models
ENABLE_MODEL_CACHING=true
```

### GPU Setup

**NVIDIA Container Toolkit (Required):**
```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Verify GPU access
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### Testing

```bash
# Run unit tests
pytest tests/unit/

# Run with GPU tests
pytest tests/gpu/ --gpu

# Integration tests (requires Claude API)
pytest tests/integration/

# Performance benchmarks
python scripts/benchmark_models.py
```

### Docker Deployment

```bash
# Build with GPU support
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Verify GPU access in container
docker-compose exec ash-nlp nvidia-smi
```

## 🔗 Integration with Ash Ecosystem

### Discord Bot Communication
- **Endpoint**: `/analyze` - Main crisis detection analysis
- **Protocol**: REST API with JSON request/response
- **Authentication**: API key-based authentication
- **Rate Limiting**: Configurable request throttling

**API Example:**
```python
# Request format
{
    "message": "text to analyze",
    "context": {
        "user_id": "discord_user_id",
        "channel_id": "discord_channel_id",
        "conversation_history": ["previous", "messages"]
    },
    "options": {
        "include_confidence": true,
        "detailed_analysis": false
    }
}

# Response format
{
    "risk_level": "high|medium|low|none",
    "confidence": 0.85,
    "analysis": {
        "crisis_indicators": ["indicator1", "indicator2"],
        "emotional_state": "distressed",
        "urgency": "immediate"
    },
    "processing_time_ms": 150
}
```

### Dashboard Integration
- **Metrics Endpoint**: `/metrics` - Performance and accuracy statistics
- **Health Monitoring**: Real-time processing statistics
- **Model Performance**: Accuracy metrics and processing times

### Testing Integration
- **Validation Endpoint**: `/validate` - Used by ash-thrash for accuracy testing
- **Batch Processing**: Handles 350-phrase test suite efficiently
- **Performance Metrics**: Detailed timing and accuracy reports

## 📊 NLP Performance

### Hardware Specifications
- **Server**: Windows 11 (10.20.30.16)
- **CPU**: AMD Ryzen 7 7700X (8 cores, 16 threads)
- **RAM**: 64GB DDR4
- **GPU**: NVIDIA RTX 3050 (8GB VRAM)
- **Storage**: NVMe SSD for model caching

### Performance Metrics
- **Response Time**: <500ms for standard analysis
- **Throughput**: 50+ requests/second sustained
- **Accuracy**: >95% on validation test suite
- **GPU Utilization**: 60-80% during peak load
- **Memory Usage**: ~8GB RAM, ~4GB VRAM

### Monitoring
- **Health Endpoint**: `http://10.20.30.16:8881/health`
- **Metrics Dashboard**: Available via ash-dash
- **Performance Logs**: Detailed timing and accuracy tracking
- **GPU Monitoring**: Real-time GPU utilization metrics

## 🧪 Testing

This repository includes comprehensive testing for NLP functionality. Integration with the complete crisis detection pipeline is tested via [ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash).

```bash
# NLP-specific testing
python -m pytest tests/unit/

# GPU performance testing
python scripts/gpu_benchmark.py

# Model accuracy validation
python scripts/validate_models.py

# Integration testing (requires ecosystem)
python -m pytest tests/integration/
```

## 🤖 Model Management

### Supported Models
- **Claude 4 Sonnet**: Primary analysis engine for sophisticated understanding
- **Local Transformers**: Backup models for offline operation
- **Custom Fine-tuned Models**: LGBTQIA+ community-specific crisis detection

### Model Pipeline
1. **Text Preprocessing**: Cleaning and normalization
2. **Initial Classification**: Fast preliminary risk assessment
3. **Deep Analysis**: Claude-powered contextual understanding
4. **Ensemble Scoring**: Combined results from multiple models
5. **Confidence Calibration**: Reliable confidence scores

### Model Updates
```bash
# Update Claude model version
docker-compose exec ash-nlp python scripts/update_claude_model.py

# Refresh model cache
docker-compose exec ash-nlp python scripts/refresh_model_cache.py

# Validate model performance
python scripts/model_validation.py
```

## 🤝 Contributing

### Development Process
1. **Fork this repository** (ash-nlp specifically)
2. **Create feature branch** for your changes
3. **Write comprehensive tests** including GPU tests
4. **Validate model performance** against test suite
5. **Test integration** with ash-bot
6. **Update documentation** as needed
7. **Submit pull request** to this repository

### Model Development
- **Training Data**: Work with crisis response teams for training examples
- **Validation**: Use ash-thrash for comprehensive accuracy testing
- **Performance**: Ensure changes don't degrade response times
- **Privacy**: Maintain privacy-preserving analysis methods

### Main Ecosystem
For changes affecting multiple components, coordinate with the [main ash repository](https://github.com/the-alphabet-cartel/ash) which includes this repository as a submodule.

## 📞 Support

### NLP-Specific Issues
- **GitHub Issues**: [ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Discord Support**: #ash-nlp-support in https://discord.gg/alphabetcartel

### Ecosystem-Wide Issues
- **Main Repository**: [ash/issues](https://github.com/the-alphabet-cartel/ash/issues)
- **General Discussion**: #tech-help in https://discord.gg/alphabetcartel

### Performance Issues
- **GPU Problems**: Include nvidia-smi output in issue reports
- **Model Performance**: Include validation metrics and test results
- **API Issues**: Include request/response examples and timing data

## 📜 License

This project is part of The Alphabet Cartel's open-source initiatives. See [LICENSE](LICENSE) file for details.

---

## ⚠️ Important Notes

### Repository Scope
This repository contains **ONLY the NLP processing server**. For:
- **Discord Bot**: See [ash-bot](https://github.com/the-alphabet-cartel/ash-bot)
- **Analytics Dashboard**: See [ash-dash](https://github.com/the-alphabet-cartel/ash-dash)
- **Testing Suite**: See [ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash)
- **Complete System**: See [main ash repository](https://github.com/the-alphabet-cartel/ash)

### Development Recommendations
- **New Contributors**: Start with the [main ash repository](https://github.com/the-alphabet-cartel/ash) for complete system overview
- **NLP-Specific Work**: Use this repository for model development and API improvements
- **System Integration**: Test changes against the full ecosystem using ash-thrash

### GPU Requirements
This service **requires NVIDIA GPU support** for optimal performance. While it can run CPU-only for development, production deployment needs proper GPU configuration.

### Privacy Considerations
This service processes potentially sensitive text data. All processing is designed to be stateless and privacy-preserving, with no permanent storage of personal information.

---

**Built with 🖤 for LGBTQIA+ gaming communities by [The Alphabet Cartel](https://discord.gg/alphabetcartel)**