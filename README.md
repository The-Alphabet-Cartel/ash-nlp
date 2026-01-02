# Ash-NLP v5.0

**Crisis Detection Backend for [The Alphabet Cartel](https://discord.gg/alphabetcartel) Discord Community**

[![Version](https://img.shields.io/badge/version-5.0.0-blue.svg)](https://github.com/the-alphabet-cartel/ash-nlp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/alphabetcartel)

---

## 🎯 Overview

Ash-NLP is a **multi-model ensemble crisis detection system** designed to identify crisis signals in Discord community messages. It uses a weighted combination of four specialized NLP models to provide accurate, contextual crisis assessment.

### Core Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Multi-Model Ensemble Pipeline                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Message → [BART] → [Sentiment] → [Irony] → [Emotions] → Crisis Score  │
│             (0.50)    (0.25)       (0.15)    (0.10)                     │
│                                                                         │
│   PRIMARY   SECONDARY   TERTIARY   SUPPLEMENTARY                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Model Ensemble

| Model | Role | Weight | Purpose |
|-------|------|--------|---------|
| **BART** | Primary | 0.50 | Zero-shot crisis classification |
| **Sentiment** | Secondary | 0.25 | Emotional context (positive/negative/neutral) |
| **Irony** | Tertiary | 0.15 | Sarcasm detection (reduces false positives) |
| **Emotions** | Supplementary | 0.10 | Fine-grained emotion signals (28 labels) |

### Crisis Severity Levels

| Level | Threshold | Action |
|-------|-----------|--------|
| 🔴 **Critical** | ≥ 0.85 | Immediate intervention required |
| 🟠 **High** | ≥ 0.70 | Priority response needed |
| 🟡 **Medium** | ≥ 0.50 | Standard monitoring |
| 🟢 **Low** | ≥ 0.30 | Passive monitoring |
| ⚪ **Safe** | < 0.30 | No crisis detected |

---

## 🚀 Quick Start

### Prerequisites

- Docker Engine 24.0+
- Docker Compose v2.20+
- NVIDIA Container Toolkit (for GPU support)
- 12GB+ VRAM recommended for GPU inference

### Installation

```bash
# Clone the repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp

# Start with Docker Compose (GPU)
docker-compose up -d

# Or CPU-only
docker-compose --profile cpu up -d
```

### Verify Installation

```bash
# Check health
curl http://localhost:30880/health

# Test analysis
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling really happy today!"}'
```

---

## 📡 API Reference

### Analyze Message

**POST** `/analyze`

Analyze a single message for crisis signals.

```bash
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I dont know if I can keep going anymore",
    "user_id": "user_123",
    "channel_id": "general"
  }'
```

**Response:**
```json
{
  "crisis_detected": true,
  "severity": "high",
  "confidence": 0.87,
  "crisis_score": 0.78,
  "requires_intervention": true,
  "recommended_action": "priority_response",
  "signals": {
    "bart": {
      "label": "emotional distress",
      "score": 0.89,
      "crisis_signal": 0.89
    },
    "sentiment": {
      "label": "negative",
      "score": 0.92,
      "crisis_signal": 0.75
    }
  },
  "processing_time_ms": 145.32,
  "models_used": ["bart", "sentiment", "irony", "emotions"]
}
```

### Batch Analysis

**POST** `/analyze/batch`

Analyze multiple messages in a single request (max 100).

```bash
curl -X POST http://localhost:30880/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "I am feeling great!",
      "Everything is falling apart",
      "Just had lunch, it was okay"
    ]
  }'
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:30880/health
```

### Service Status

**GET** `/status`

Detailed service status including model information and statistics.

### API Documentation

- **Swagger UI**: http://localhost:30880/docs
- **ReDoc**: http://localhost:30880/redoc

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NLP_ENVIRONMENT` | `production` | Environment name |
| `NLP_API_HOST` | `0.0.0.0` | Server bind address |
| `NLP_API_PORT` | `30880` | Server port |
| `NLP_API_WORKERS` | `4` | Uvicorn worker count |
| `NLP_LOG_LEVEL` | `INFO` | Logging level |
| `NLP_MODELS_DEVICE` | `auto` | Device (auto/cuda/cpu) |
| `NLP_MODEL_BART_WEIGHT` | `0.50` | BART model weight |
| `NLP_MODEL_SENTIMENT_WEIGHT` | `0.25` | Sentiment model weight |
| `NLP_MODEL_IRONY_WEIGHT` | `0.15` | Irony model weight |
| `NLP_MODEL_EMOTIONS_WEIGHT` | `0.10` | Emotions model weight |
| `NLP_THRESHOLD_CRITICAL` | `0.85` | Critical severity threshold |
| `NLP_THRESHOLD_HIGH` | `0.70` | High severity threshold |
| `NLP_THRESHOLD_MEDIUM` | `0.50` | Medium severity threshold |
| `NLP_THRESHOLD_LOW` | `0.30` | Low severity threshold |

### Configuration Files

```
config/
├── default.json      # Base configuration with validation
├── production.json   # Production overrides
└── testing.json      # Testing overrides
```

---

## 🐳 Docker

### Build

```bash
# Build GPU image
docker build -t ash-nlp:v5.0 .

# Build CPU image
docker build -t ash-nlp:v5.0-cpu --target runtime-cpu .
```

### Run

```bash
# GPU with NVIDIA runtime
docker run --gpus all -p 30880:30880 ash-nlp:v5.0

# CPU only
docker run -p 30880:30880 ash-nlp:v5.0-cpu
```

### Docker Compose

```bash
# Start (GPU)
docker-compose up -d

# Start (CPU)
docker-compose --profile cpu up -d

# View logs
docker-compose logs -f ash-nlp

# Stop
docker-compose down
```

---

## 🧪 Development

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py --reload --env development
```

### Project Structure

```
ash-nlp/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Production orchestration
└── src/
    ├── config/
    │   ├── default.json        # Base configuration
    │   ├── production.json     # Production overrides
    │   └── testing.json        # Testing overrides
    ├── managers/
    │   └── config_manager.py
    ├── models/
    │   ├── base.py
    │   ├── bart_classifier.py
    │   ├── sentiment.py
    │   ├── irony.py
    │   └── emotions.py
    ├── ensemble/
    │   ├── model_loader.py
    │   ├── scoring.py
    │   ├── fallback.py
    │   └── decision_engine.py
    └── api/
        ├── app.py
        ├── routes.py
        ├── schemas.py
        └── middleware.py
```

---

## 🔧 Technical Details

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32+ GB |
| GPU VRAM | 8 GB | 12+ GB |
| Storage | 20 GB | 50+ GB |

### Model Details

- **BART**: `facebook/bart-large-mnli` (~1.5GB)
- **Sentiment**: `cardiffnlp/twitter-roberta-base-sentiment-latest` (~500MB)
- **Irony**: `cardiffnlp/twitter-roberta-base-irony` (~500MB)
- **Emotions**: `SamLowe/roberta-base-go_emotions` (~500MB)

### Performance

- **Latency**: ~50-150ms per message (GPU)
- **Throughput**: ~20-50 requests/second (GPU, 4 workers)
- **Memory**: ~6-8GB GPU VRAM under load

---

## 🏳️‍🌈 Community

**The Alphabet Cartel** is an LGBTQIA+ Discord community centered around gaming, political discourse, activism, and societal advocacy.

- 🌐 **Website**: [alphabetcartel.org](https://alphabetcartel.org)
- 💬 **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- 🐙 **GitHub**: [github.com/the-alphabet-cartel](https://github.com/the-alphabet-cartel)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co/) for transformer models
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- The Alphabet Cartel community for inspiration and support

---

**Built with care for chosen family** 🏳️‍🌈
