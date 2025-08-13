<!-- ash-nlp/README.md -->
<!--
README Documentation for Ash-NLP Service
FILE VERSION: v3.1-3d-10-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Ash NLP Service v3.0 - Three-Model Crisis Detection Ensemble

**Revolutionary mental health crisis detection using advanced AI ensemble methods**

[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da)](https://discord.gg/alphabetcartel)
[![Website](https://img.shields.io/badge/Website-alphabetcartel.org-blue)](http://alphabetcartel.org)
[![GitHub](https://img.shields.io/badge/Branch-Main-green)](https://github.com/the-alphabet-cartel/ash-nlp)

## 🚀 What is Ash NLP v3.0?

Ash NLP v3.0 is a cutting-edge **Three Zero-Shot Model Ensemble system** designed specifically for mental health crisis detection in LGBTQIA+ Discord communities. Unlike traditional single-model approaches, our system combines three specialized AI models to provide:

- **🧠 Enhanced accuracy** through model consensus and disagreement detection
- **⚡ Sub-35ms response times** optimized for real-time Discord interactions
- **🔍 Gap detection** to identify when models disagree and require human review
- **🏳️‍🌈 Community-aware** patterns specific to LGBTQIA+ experiences
- **🛡️ Safety-first** approach with transparent decision-making

## 🤖 Three-Model Architecture

### Model 1: Depression Detection 🧠
- **Model**: `MoritzLaurer/deberta-v3-base-zeroshot-v2.0`
- **Architecture**: DeBERTa-based classification
- **Purpose**: Primary crisis classification with clinical depression focus
- **Labels**: `[Dynamic Zero-Shot Labels]`

### Model 2: Sentiment Analysis 💭
- **Model**: `Lowerated/lm6-deberta-v3-topic-sentiment`
- **Architecture**: DeBERTa-based sentiment analysis
- **Purpose**: Contextual validation and emotional tone analysis
- **Labels**: `[Dynamic Zero-Shot Labels]`

### Model 3: Emotional Distress Detection 😰
- **Model**: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`
- **Architecture**: DeBERTa-based emotional analysis
- **Purpose**: Additional emotional state detection and validation
- **Labels**: `[Dynamic Zero-Shot]`

## 🎯 Key Features

### Ensemble Decision Making
- **Consensus Mode**: All models must agree for high confidence
- **Majority Mode**: Democratic voting with confidence weighting
- **Weighted Mode**: Configurable model importance (Depression: 75%, Sentiment: 10%, Distress: 15%)

### Gap Detection System
- **Meaningful Disagreement Detection**: Identifies when models fundamentally disagree
- **Automatic Staff Flagging**: Routes uncertain cases to human review
- **Confidence Spread Analysis**: Detects when model confidence varies significantly

### Hardware Optimization
- **RTX 3060 Optimized**: 12GB VRAM utilization with 48-item batch processing
- **CPU Performance**: 16-thread processing for Ryzen 7 5800X
- **Memory Efficient**: ~1GB GPU memory for all three models

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- NVIDIA GPU with 4GB+ VRAM (recommended)
- 8GB+ system RAM

### Installation

```bash
# Clone the repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp
git checkout Organic-Learning

# Copy environment template
cp .env.template .env

# Configure your environment variables
# See docs/tech/api_v3_0.md for detailed configuration

# Build and start the service
docker-compose build ash-nlp
docker-compose up ash-nlp
```

### Quick Test

```bash
# Health check
curl http://localhost:8881/health

# Three Zero-Shot Model Ensemble analysis
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling really down", "user_id": "test", "channel_id": "test"}'
```

## 📊 Performance Benchmarks

| Metric | Single Model | Three Zero-Shot Model Ensemble |
|--------|--------------|---------------------|
| **Response Time** | 25ms | 31ms |
| **Accuracy** | 61.7% | 75%+ |
| **False Positive Rate** | 15% | <8% |
| **High Crisis Detection** | 85% | 95%+ |
| **GPU Memory Usage** | 350MB | 1.03GB |

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Three-Model Configuration
NLP_DEPRESSION_MODEL=MoritzLaurer/deberta-v3-base-zeroshot-v2.0
NLP_SENTIMENT_MODEL=Lowerated/lm6-deberta-v3-topic-sentiment
NLP_EMOTIONAL_DISTRESS_MODEL=MoritzLaurer/mDeBERTa-v3-base-mnli-xnli

# Ensemble Configuration
NLP_ENSEMBLE_MODE=weighted  # consensus, majority, weighted
NLP_GAP_DETECTION_THRESHOLD=0.4
NLP_THRESHOLD_GAP_DISAGREEMENT=0.5

# Hardware Optimization
NLP_PERFORMANCE_MAX_BATCH_SIZE=32
NLP_PERFORMANCE_INFERENCE_THREADS=16
NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS=20
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Depression    │    │    Sentiment     │    │ Emotional       │
│     Model       │    │     Model        │    │ Distress Model  │
│   (DeBERTa)     │    │   (DeBERTa)      │    │ (DeBERTa)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Ensemble Processor   │
                    │  • Consensus Algorithm │
                    │  • Gap Detection       │
                    │  • Confidence Analysis │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Decision Engine     │
                    │  • Crisis Level Map    │
                    │  • Staff Review Flag   │
                    │  • Response Required   │
                    └─────────────────────────┘
```

> ## 📚 Documentation
>
>- **[API Documentation](docs/tech/api_v3_0.md)** - Complete API reference
>- **[Team Guide](docs/team/team_guide_v3_0.md)** - Guide for crisis response teams
>- **[Troubleshooting](docs/troubleshooting_v3_0.md)** - Common issues and solutions
>- **[GitHub Release Notes](docs/github/github_release_v3_0.md)** - Version 3.0 details
>
## 🤝 Integration with Ash Ecosystem

Ash NLP v3.0 integrates seamlessly with:

- **[Ash Bot](https://github.com/the-alphabet-cartel/ash-bot)** - Discord crisis response bot
- **[Ash Dashboard](https://github.com/the-alphabet-cartel/ash-dash)** - Analytics and monitoring (Not Yet Implemented)
- **[Ash Thrash](https://github.com/the-alphabet-cartel/ash-thrash)** - Testing and validation (Not Yet Implemented)

## 🔒 Security & Privacy

- **Docker Secrets Support**: Secure API key management
- **No Data Persistence**: Messages are analyzed in-memory only
- **CORS Protection**: Configurable origin restrictions
- **Rate Limiting**: Prevents abuse and ensures fair usage

## 🧪 Experimental Features

Version 3.1 includes cutting-edge features:

- **Confidence Spreading**: Dynamic threshold adjustment based on model agreement
- **Community Pattern Learning**: Adaptive recognition of LGBTQIA+ specific language
- **Real-time Gap Analytics**: Live monitoring of model disagreement patterns

## 📈 Monitoring & Analytics

Access real-time metrics:

```bash
# Service statistics
curl http://localhost:8881/stats

# Model performance
curl http://localhost:8881/health

# Learning system status
curl http://localhost:8881/learning_statistics
```

## 🤝 Contributing

We welcome contributions! Please see our:
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Development Setup](docs/development.md)

## 📄 License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 - see the [LICENSE](LICENSE) file for details.

## 🏳️‍🌈 Community

**The Alphabet Cartel** builds technology for LGBTQIA+ communities with:
- **Safety First**: Every design decision prioritizes user wellbeing
- **Community Input**: Built with and for the communities we serve
- **Open Source**: Transparent, auditable, and improvable by all
- **Chosen Family**: Technology that supports found family connections

---

**Discord**: [Join our community](https://discord.gg/alphabetcartel)  
**Website**: [alphabetcartel.org](http://alphabetcartel.org)  
**Support**: Available through Discord or GitHub issues

*Built with ❤️ for chosen family, one conversation at a time.*