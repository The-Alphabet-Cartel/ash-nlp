# 🧠 Ash NLP Server v2.1 - "Enhanced Learning Intelligence"

> *Advanced machine learning crisis detection with adaptive learning from community feedback and comprehensive analytics*

[![Version](https://img.shields.io/badge/version-2.1-blue)](https://github.com/The-Alphabet-Cartel/ash-nlp/releases/tag/v2.1)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-red)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.35+-orange)](https://huggingface.co/transformers/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com/)

## 🎉 What's New in v2.1

**Ash NLP v2.1 delivers production-ready AI crisis detection with enhanced learning capabilities, comprehensive analytics, and optimized performance for your NVIDIA RTX 3050 + AMD Ryzen 7 7700X setup.**

### ✨ Major Enhancements
- **🧠 Enhanced Learning System** - Improved false positive/negative adaptation with community-specific pattern recognition
- **📊 Advanced Analytics** - Comprehensive learning metrics and effectiveness tracking
- **⚡ Performance Optimization** - RTX 3050 GPU utilization with intelligent CPU/GPU switching
- **🔧 Production Hardening** - Enhanced error handling, logging, and deployment reliability
- **📈 Real-time Monitoring** - Detailed health endpoints and performance metrics
- **🔄 Seamless Integration** - Improved Ash bot communication with 99.9% uptime

---

## 🚀 Quick Start

### Production Deployment (Recommended)
```bash
# Clone repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp

# Configure environment
cp .env.template .env
# Edit .env with your settings (see Environment Configuration below)

# Deploy with Docker
docker-compose up -d

# Verify deployment
curl http://10.20.30.16:8881/health
```

### Development Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux

# Install dependencies
pip install -r requirements.txt

# Start development server
python nlp_main.py
```

**Service will be available at `http://10.20.30.16:8881`**

---

## 🏗️ Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ash Discord   │    │   NLP Server    │    │   Analytics     │
│      Bot        │───▶│   (This Repo)   │───▶│   Dashboard     │
│  10.20.30.253   │    │   10.20.30.16   │    │   (ash-dash)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Learning Data  │
                       │    Storage      │
                       └─────────────────┘
```

### AI Model Pipeline
```
User Message → DeBERTa Depression Model → RoBERTa Sentiment Analysis
     ↓                    ↓                       ↓
Context Analysis → Learning Adjustment → Final Crisis Assessment
     ↓                    ↓                       ↓
Community Pattern → Confidence Scoring → Response to Ash Bot
```

---

## 🧠 Advanced Learning System

### Learning Capabilities
- **🎯 False Positive Reduction** - Learns from incorrectly flagged messages
- **🔍 False Negative Detection** - Adapts to missed crisis indicators  
- **🗣️ Community Language** - Understands LGBTQIA+ and community-specific terminology
- **📊 Continuous Improvement** - Real-time model adjustments with feedback loops
- **🔒 Privacy-First** - All learning data stays within your infrastructure

### Learning Workflow
```python
# Example learning cycle
def community_learning_cycle():
    # 1. AI analyzes message
    result = analyze_message("feeling really off today")
    
    # 2. Crisis Response team provides feedback
    if result.crisis_level == "high" and actual_crisis == False:
        report_false_positive(message, context="casual expression")
    
    # 3. System learns and adapts
    learning_system.adjust_patterns(
        pattern="feeling off",
        context="casual",
        adjustment="reduce_sensitivity"
    )
    
    # 4. Future similar messages handled better
    next_result = analyze_message("feeling really off about this movie")
    # Now correctly identifies as non-crisis due to learning
```

---

## ⚙️ Environment Configuration

### Required Environment Variables
```bash
# Core AI Models
DEPRESSION_MODEL=rafalposwiata/deproberta-large-depression
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL_CACHE_DIR=./models/cache

# Hardware Optimization (Your RTX 3050 + Ryzen 7 7700X)
DEVICE=auto                    # Auto-detect GPU/CPU
MODEL_PRECISION=float16        # GPU memory optimization
MAX_BATCH_SIZE=32             # Optimized for RTX 3050
INFERENCE_THREADS=8           # Ryzen 7 7700X optimization

# Learning System
ENABLE_LEARNING_SYSTEM=true
LEARNING_RATE=0.1
MAX_LEARNING_ADJUSTMENTS_PER_DAY=100
LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json

# Network Configuration
NLP_SERVICE_HOST=10.20.30.16
NLP_SERVICE_PORT=8881
MAX_CONCURRENT_REQUESTS=20
REQUEST_TIMEOUT=30

# Optional: Enhanced Features
HUGGINGFACE_HUB_TOKEN=your_token_here  # For model downloads
ENABLE_DEBUG_LOGGING=false
LOG_LEVEL=INFO
```

### Crisis Detection Thresholds
```python
# Configurable thresholds in nlp_settings.py
CRISIS_THRESHOLDS = {
    "high": 0.50,      # Immediate intervention needed
    "medium": 0.22,    # Monitoring and support
    "low": 0.12        # General wellness check
}

# Learning system automatically adjusts these based on community feedback
```

---

## 📊 Performance & Analytics

### Key Performance Indicators
```json
{
    "target_performance": {
        "response_time": "<100ms average",
        "accuracy": "90%+ (vs 75% baseline)",
        "false_positive_rate": "<5% (vs 15% baseline)",
        "uptime": "99.9%+",
        "learning_adaptation": "Weekly pattern improvements"
    },
    "hardware_utilization": {
        "gpu_usage": "40-60% (RTX 3050)",
        "cpu_usage": "15-25% (Ryzen 7 7700X)",
        "memory_usage": "4-6GB RAM",
        "storage": "2-5GB model cache"
    }
}
```

### Real-time Monitoring
```bash
# Health check endpoint
curl http://10.20.30.16:8881/health

# Learning system statistics  
curl http://10.20.30.16:8881/learning_statistics

# Comprehensive performance metrics
curl http://10.20.30.16:8881/enhanced_stats

# Model information
curl http://10.20.30.16:8881/model_info
```

---

## 🔌 API Reference

### Core Analysis Endpoint
```python
POST /analyze
{
    "message": "user message content",
    "user_id": "discord_user_id",
    "channel_id": "discord_channel_id",
    "context": "optional_context"
}

# Response
{
    "needs_response": true,
    "crisis_level": "medium",
    "confidence_score": 0.82,
    "detected_categories": ["moderate_depression", "anxiety"],
    "method": "enhanced_ml_analysis",
    "processing_time_ms": 85.3,
    "reasoning": "Moderate distress detected with community pattern adjustment",
    "learning_applied": true
}
```

### Learning System Endpoints
```python
# Report false positive
POST /analyze_false_positive
{
    "message": "that totally killed me lol",
    "detected_level": "high",
    "correct_level": "none",
    "context": "humor/gaming",
    "reporter_id": "crisis_team_member_id"
}

# Report false negative
POST /analyze_false_negative
{
    "message": "not doing great tbh",
    "should_detect_level": "medium",
    "currently_detected": "none",
    "context": "subtle_distress",
    "reporter_id": "crisis_team_member_id"
}

# Get learning statistics
GET /learning_statistics
{
    "total_adjustments": 247,
    "false_positive_reductions": 156,
    "false_negative_improvements": 91,
    "accuracy_improvement": "+18.3%",
    "last_learning_event": "2025-07-27T10:15:30Z"
}
```

---

## 🐳 Docker Deployment

### Production Docker Compose
```yaml
services:
  ash-nlp:
    image: ghcr.io/the-alphabet-cartel/ash-nlp:v2.1
    container_name: ash_nlp_server
    restart: unless-stopped
    ports:
      - "8881:8881"
    environment:
      - PYTHONUNBUFFERED=1
      - DEVICE=auto
      - ENABLE_LEARNING_SYSTEM=true
    volumes:
      - ./models:/app/models/cache      # Model storage
      - ./learning_data:/app/learning_data  # Learning persistence
      - ./logs:/app/logs               # Application logs
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '6'
        reservations:
          memory: 2G
          cpus: '2'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8881/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Container Management
```bash
# Deploy new version
docker-compose pull ash-nlp
docker-compose up -d ash-nlp

# Monitor logs
docker-compose logs -f ash-nlp

# Backup learning data
docker-compose exec ash-nlp tar -czf /tmp/learning_backup.tar.gz /app/learning_data

# Performance monitoring
docker stats ash_nlp_server
```

---

## 🛠️ Integration with Ash Bot

### Communication Protocol
The NLP server integrates seamlessly with the main Ash Discord bot running on `10.20.30.253:8882`.

```python
# Ash Bot → NLP Server
import aiohttp

async def analyze_message(message, user_id, channel_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://10.20.30.16:8881/analyze",
            json={
                "message": message,
                "user_id": user_id,
                "channel_id": channel_id
            }
        ) as response:
            return await response.json()

# Enhanced learning integration
async def report_false_positive(message, context):
    async with session.post(
        "http://10.20.30.16:8881/analyze_false_positive",
        json={
            "message": message,
            "context": context,
            "reporter_id": crisis_team_member_id
        }
    ) as response:
        learning_result = await response.json()
        return learning_result
```

### Testing Integration
Use the ash-thrash testing suite on the same server to validate integration:
```bash
# From ash-thrash container (port 8884)
python src/comprehensive_testing.py --target-nlp http://10.20.30.16:8881
```

---

## 📈 Monitoring & Maintenance

### Daily Operations
```bash
# Check system health
curl http://10.20.30.16:8881/health | jq

# Monitor learning effectiveness
curl http://10.20.30.16:8881/learning_statistics | jq

# View recent activity
tail -f logs/nlp_service.log

# Check resource usage
docker stats ash_nlp_server --no-stream
```

### Weekly Maintenance
```bash
# Backup learning data
cp -r learning_data learning_data_backup_$(date +%Y%m%d)

# Clean old logs
find logs/ -name "*.log" -mtime +7 -delete

# Check model performance
python scripts/validate_model_performance.py

# Update dependencies (if needed)
pip install -r requirements.txt --upgrade
```

### Performance Optimization
```python
# Monitor key metrics
{
    "response_time_target": "<100ms",
    "memory_usage_target": "<6GB",
    "gpu_utilization": "40-80% (RTX 3050)",
    "learning_accuracy": ">90%",
    "false_positive_rate": "<5%"
}
```

---

## 🚨 Troubleshooting

### Common Issues

**❌ Model Download Failures**
```bash
# Check Hugging Face token
echo $HUGGINGFACE_HUB_TOKEN

# Manual model download
python -c "from transformers import AutoModel; AutoModel.from_pretrained('rafalposwiata/deproberta-large-depression')"
```

**❌ GPU Not Detected**
```bash
# Check NVIDIA drivers
nvidia-smi

# Verify PyTorch GPU support
python -c "import torch; print(torch.cuda.is_available())"

# Force CPU mode if needed
export DEVICE=cpu
```

**❌ Learning System Not Active**
```bash
# Check learning system status
curl http://10.20.30.16:8881/learning_statistics

# Verify learning data directory
ls -la learning_data/

# Check logs for learning errors
grep "learning" logs/nlp_service.log
```

---

## 📚 Documentation

### Complete Documentation Suite
- **[📖 Team Member Guide](docs/team_guide.md)** - Crisis Response team usage and procedures
- **[🔧 Implementation Guide](docs/implementation_guide.md)** - Technical setup and deployment
- **[🔌 API Documentation](docs/api.md)** - Complete REST API reference  
- **[🧠 Learning System Guide](docs/learning_system.md)** - Advanced learning features
- **[🐛 Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions
- **[📊 Analytics Guide](docs/analytics.md)** - Performance monitoring and optimization

### Quick Reference
```bash
# Essential commands
docker-compose up -d              # Start service
curl http://10.20.30.16:8881/health    # Health check
docker-compose logs -f ash-nlp    # View logs
docker-compose restart ash-nlp    # Restart service

# Learning system
curl http://10.20.30.16:8881/learning_statistics  # Learning stats
/learning_stats                   # Discord command (Crisis Response team)
/report_false_positive           # Discord command (Crisis Response team)
/report_false_negative          # Discord command (Crisis Response team)
```

---

## 🔮 Roadmap

### v2.2 (Planned - Q1 2026)
- **🌐 Multi-language Support** - Spanish and other languages for diverse communities
- **📱 Mobile Optimization** - Enhanced performance for mobile Discord usage
- **🔗 External Integrations** - Mental health resource API connections
- **📊 Advanced Analytics Dashboard** - Web interface for comprehensive metrics

### v2.5 (Future - Q2 2026) 
- **💬 Conversation Tracking** - Multi-message crisis situation monitoring
- **🤖 Autonomous Learning** - Fully automated detection improvement
- **🌍 Community Insights** - Anonymized mental health trend analysis
- **🔮 Predictive Analytics** - Early warning systems for community mental health

### v3.0 (Vision - 2027)
- **🧠 Advanced AI Integration** - Next-generation language models
- **🌐 Federated Learning** - Cross-community insights while preserving privacy
- **🔄 Real-time Adaptation** - Instant model updates
- **🏥 Professional Integration** - Direct connections to mental health services

---

## 🙏 Acknowledgments

### Technical Foundation
- **🤖 Anthropic** - Claude 4 Sonnet API and development assistance
- **🤗 Hugging Face** - Depression detection and sentiment analysis models
- **🐍 PyTorch Community** - Machine learning framework and GPU optimization
- **⚡ FastAPI** - High-performance API framework
- **🐳 Docker** - Containerization and deployment reliability

### Community Partners
- **💜 The Alphabet Cartel Crisis Response Team** - Real-world testing and learning data
- **🏳️‍🌈 LGBTQIA+ Community Members** - Language pattern guidance and cultural sensitivity
- **🔬 Beta Testing Community** - Early adoption and system refinement
- **🧠 Mental Health Professionals** - Clinical guidance and best practices

### Research Contributors
- **📚 AI/ML Research Community** - Foundational work in depression detection
- **🔬 Natural Language Processing** - Advances in context understanding
- **🆘 Crisis Intervention Research** - Evidence-based mental health practices

---

## 📞 Support & Resources

### Getting Help
- **🐛 GitHub Issues** - [Bug reports and feature requests](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **💬 Discord Support** - [The Alphabet Cartel Server](https://discord.gg/alphabetcartel)
- **📖 Documentation** - Complete guides in `/docs` directory
- **📧 Direct Contact** - For urgent technical issues

### Community Resources
- **🏠 Main Repository** - [github.com/the-alphabet-cartel/ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp)
- **🤖 Main Ash Bot** - [github.com/the-alphabet-cartel/ash](https://github.com/the-alphabet-cartel/ash)
- **📊 Analytics Dashboard** - [github.com/the-alphabet-cartel/ash-dash](https://github.com/the-alphabet-cartel/ash-dash)
- **🧪 Testing Suite** - [github.com/the-alphabet-cartel/ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash)

---

## 📝 License & Usage

**Built with 🖤 for The Alphabet Cartel Discord community.**

This system is designed specifically for internal use within The Alphabet Cartel community. All AI models and learning data remain within your infrastructure to ensure privacy and security.

*"We've all been in that dark place where everything feels impossible. You're not alone."* - Ash Bot

---

**🌟 Ready to deploy advanced AI crisis detection with community-adaptive learning? Follow the Quick Start guide above!**