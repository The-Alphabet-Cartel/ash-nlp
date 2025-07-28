# Ash NLP Server

**Advanced Crisis Detection & Community Support NLP Processing Engine**

Part of The Alphabet Cartel's [Ash Crisis Detection & Community Support Ecosystem](https://github.com/the-alphabet-cartel/ash)

---

## 🌟 Overview

The Ash NLP Server provides sophisticated natural language processing capabilities for real-time crisis detection in Discord communities. This server analyzes messages for signs of mental health crises, self-harm indicators, and community support needs using advanced machine learning models and adaptive learning systems.

### Key Features

🧠 **Advanced AI Models**: Multi-model ensemble with depression detection and sentiment analysis  
🔄 **Adaptive Learning**: Continuous improvement through feedback-based learning  
⚡ **High Performance**: GPU-accelerated processing with sub-200ms response times  
🔒 **Privacy-First**: No permanent message storage, ephemeral analysis only  
📊 **Real-time Analytics**: Live performance metrics and detection statistics  
🎯 **Crisis Classification**: Precise risk level assessment (High/Medium/Low)  

## 🏗️ Architecture

### Server Specifications
- **Primary Server**: Windows 11 (10.20.30.16)
- **CPU**: AMD Ryzen 7 7700X
- **RAM**: 64GB DDR5
- **GPU**: NVIDIA RTX 3050 (8GB VRAM)
- **API Port**: 8881
- **Docker**: Required for deployment

### Integration Points
- **Ash Bot**: Discord bot integration (10.20.30.253:8882)
- **Ash Dashboard**: Analytics visualization (10.20.30.253:8883)
- **Ash Testing**: Automated validation (10.20.30.253:8884)

## 🚀 Quick Start

### Prerequisites
- Windows 11 Pro with Docker Desktop
- NVIDIA RTX 3050 with latest drivers (535+)
- Git for Windows
- Network access to 10.20.30.16:8881

### Installation

**1. Clone Repository:**
```powershell
cd C:\Projects
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp
```

**2. Configure Environment:**
```powershell
# Copy environment template
copy .env.template .env

# Edit configuration (using Atom)
atom .env
```

**3. Deploy with Docker:**
```powershell
# Create required directories
mkdir models, learning_data, logs, data, analytics

# Deploy services
docker-compose up -d

# Verify deployment
curl http://10.20.30.16:8881/health
```

### Environment Configuration

**Required Settings (.env):**
```bash
# Server Configuration
NLP_SERVICE_HOST=0.0.0.0
NLP_SERVICE_PORT=8881
DEVICE=auto

# AI Models
DEPRESSION_MODEL=rafalposwiata/deproberta-large-depression
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL_CACHE_DIR=./models

# Learning System
ENABLE_LEARNING_SYSTEM=true
LEARNING_RATE=0.1
MAX_LEARNING_ADJUSTMENTS_PER_DAY=50

# Performance Optimization
MAX_BATCH_SIZE=32
INFERENCE_THREADS=4
GPU_MEMORY_FRACTION=0.8

# Integration
ENABLE_ANALYTICS_EXPORT=true
ANALYTICS_WEBHOOK_URL=http://10.20.30.253:8883/webhook/nlp_metrics
```

## 🔌 API Reference

### Core Endpoints

**Health Check:**
```bash
GET /health
```

**Message Analysis:**
```bash
POST /analyze
Content-Type: application/json

{
  "message": "feeling really down today",
  "user_id": "123456789",
  "channel_id": "987654321",
  "context": {
    "previous_messages": [],
    "user_history": {}
  }
}
```

**Learning System:**
```bash
POST /learning_feedback
Content-Type: application/json

{
  "message_id": "msg_123",
  "feedback_type": "false_positive",
  "correct_classification": "low"
}
```

**Analytics:**
```bash
GET /learning_statistics
GET /performance_metrics
GET /model_status
```

### Response Format

```json
{
  "risk_level": "medium",
  "confidence": 0.78,
  "analysis": {
    "depression_score": 0.65,
    "sentiment_score": -0.42,
    "crisis_indicators": ["mood_negative", "isolation"]
  },
  "recommendations": ["close_monitoring", "check_in_6h"],
  "processing_time_ms": 145
}
```

## 🧪 Crisis Detection System

### Detection Categories

**High Crisis (Score ≥ 0.50):**
- Suicidal ideation indicators
- Self-harm references
- Immediate danger signals
- Crisis escalation language

**Medium Crisis (Score ≥ 0.22):**
- Depression markers
- Anxiety indicators
- Social isolation patterns
- Identity struggles

**Low Crisis (Score ≥ 0.12):**
- Mild mood indicators
- Stress signals
- Gaming frustration
- General support needs

### Model Pipeline

1. **Text Preprocessing**: Cleaning and normalization
2. **Initial Classification**: Fast preliminary risk assessment  
3. **Deep Analysis**: Advanced contextual understanding
4. **Ensemble Scoring**: Combined results from multiple models
5. **Confidence Calibration**: Reliable confidence scores
6. **Learning Integration**: Adaptive improvement based on feedback

### Performance Metrics

- **Overall Accuracy**: 85%+ (vs 75% baseline)
- **High Crisis Detection**: 95%+
- **False Positive Rate**: <8% (vs 15% baseline)
- **Processing Time**: <200ms per analysis
- **Learning Adaptation**: Real-time model improvements

## 🔗 Ecosystem Integration

### Ash Bot Integration

The NLP server integrates seamlessly with the [Ash Discord Bot](https://github.com/the-alphabet-cartel/ash-bot):

```python
# Bot configuration for NLP integration
NLP_CONFIG = {
    "base_url": "http://10.20.30.16:8881",
    "timeout": 30,
    "retry_attempts": 3,
    "fallback_enabled": True
}
```

### Dashboard Analytics

Real-time metrics flow to the [Ash Dashboard](https://github.com/the-alphabet-cartel/ash-dash):
- Live detection statistics
- Performance monitoring
- Learning system analytics
- Historical trend analysis

### Testing Validation

Comprehensive testing via [Ash Testing Suite](https://github.com/the-alphabet-cartel/ash-thrash):
- 350-phrase validation testing
- Performance benchmarking
- Integration testing
- Accuracy monitoring

## 📚 Documentation

### Complete Documentation Suite

- **[Deployment Guide](docs/deployment_v2_1.md)** - Production deployment procedures
- **[GitHub Release Guide](docs/github_release_v2_1.md)** - Release management and versioning
- **[Team Guide](docs/team/team_guide_v2_1.md)** - Operations guide for Crisis Response teams
- **[API Documentation](docs/tech/API_v2_1.md)** - Complete REST API reference
- **[Troubleshooting Guide](docs/tech/troubleshooting_v2_1.md)** - Problem diagnosis and resolution

### Technical Specifications

- **Python 3.11+** with FastAPI framework
- **PyTorch** for deep learning inference
- **Transformers** for pre-trained model integration
- **Docker** for containerized deployment
- **NVIDIA CUDA** for GPU acceleration

## 🛠️ Development

### Development Environment

**Prerequisites:**
- Windows 11 development machine
- Atom editor with Python packages
- GitHub Desktop for version control
- Docker Desktop for containerization

**Setup:**
```powershell
# Clone for development
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run in development mode
python nlp_main.py --dev
```

### Contributing

1. **Fork this repository** (ash-nlp specifically)
2. **Create feature branch** for your changes
3. **Write comprehensive tests** including GPU tests
4. **Validate model performance** against test suite
5. **Test integration** with ash-bot
6. **Update documentation** as needed
7. **Submit pull request** to this repository

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

## ⚠️ Important Notes

### Repository Scope
This repository contains **ONLY the NLP processing server**. For the complete crisis detection system including Discord bot, dashboard, and testing suite, see the [main Ash repository](https://github.com/the-alphabet-cartel/ash).

### Production Deployment
The NLP server runs on dedicated Windows 11 hardware (10.20.30.16) optimized for AI workloads. All production deployments should follow the comprehensive [deployment guide](docs/deployment_v2_1.md).

### Privacy & Security
- **No message storage**: Messages are analyzed in real-time and immediately discarded
- **Ephemeral processing**: No conversation history is retained
- **Local deployment**: All processing occurs on community-controlled servers
- **Audit logs**: System actions are logged without storing message content

## 📜 License

This project is part of The Alphabet Cartel's open-source initiatives. See [LICENSE](LICENSE) file for details.

---

## 🌈 Community

**The Alphabet Cartel** - Building inclusive gaming communities through technology.

**Discord:** https://discord.gg/alphabetcartel | **Website:** https://alphabetcartel.org

*"We've all been in that dark place where everything feels impossible. You're not alone."* - Ash

**Built with 🖤 for chosen family everywhere.**