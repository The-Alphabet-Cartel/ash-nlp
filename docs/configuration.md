# Ash-NLP Configuration Guide

**Version**: v5.0  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## Table of Contents

1. [Overview](#overview)
2. [Configuration Hierarchy](#configuration-hierarchy)
3. [Configuration Files](#configuration-files)
4. [Environment Variables](#environment-variables)
5. [Model Configuration](#model-configuration)
6. [Threshold Configuration](#threshold-configuration)
7. [API Configuration](#api-configuration)
8. [Performance Configuration](#performance-configuration)
9. [Logging Configuration](#logging-configuration)
10. [Docker Configuration](#docker-configuration)
11. [Examples](#examples)

---

## Overview

Ash-NLP uses a layered configuration system that allows flexibility across different deployment environments while maintaining sensible defaults.

### Configuration Priority (Highest to Lowest)

1. **Environment Variables** - Override everything
2. **Environment-specific JSON** - `production.json`, `testing.json`
3. **Default JSON** - `default.json` base configuration

### Key Principles

- **Immutable Defaults**: `default.json` contains validated, production-safe defaults
- **Environment Overrides**: Specific environments only override what's different
- **12-Factor Compliance**: All settings can be overridden via environment variables
- **Validation**: Invalid configurations fail fast with descriptive errors

---

## Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Environment Variables                         │
│                    (NLP_API_PORT=9999)                          │
│                         ↓ overrides                              │
├─────────────────────────────────────────────────────────────────┤
│                  Environment JSON                                │
│              (production.json / testing.json)                    │
│                         ↓ overrides                              │
├─────────────────────────────────────────────────────────────────┤
│                     Default JSON                                 │
│                    (default.json)                                │
│                    Base configuration                            │
└─────────────────────────────────────────────────────────────────┘
```

### Example Override Flow

```
default.json:     {"api": {"port": 30880}}
production.json:  {}  (no override)
NLP_API_PORT:     9999

Final value:      port = 9999  (env var wins)
```

---

## Configuration Files

### File Locations

```
ash-nlp/
└── config/
    ├── default.json      # Base configuration (required)
    ├── production.json   # Production overrides
    └── testing.json      # Testing overrides
```

### default.json

Complete base configuration with all required fields:

```json
{
  "_metadata": {
    "version": "5.0.0",
    "description": "Ash-NLP Default Configuration",
    "updated": "2025-12-31"
  },
  
  "api": {
    "host": "0.0.0.0",
    "port": 30880,
    "workers": 4,
    "timeout": 30,
    "rate_limit_enabled": true,
    "rate_limit_rpm": 60
  },
  
  "models": {
    "device": "auto",
    "warmup_enabled": true,
    "lazy_load": true,
    "max_concurrent": 4,
    
    "bart": {
      "enabled": true,
      "model_id": "facebook/bart-large-mnli",
      "weight": 0.50,
      "max_length": 512
    },
    "sentiment": {
      "enabled": true,
      "model_id": "cardiffnlp/twitter-roberta-base-sentiment-latest",
      "weight": 0.25,
      "max_length": 512
    },
    "irony": {
      "enabled": true,
      "model_id": "cardiffnlp/twitter-roberta-base-irony",
      "weight": 0.15,
      "max_length": 512
    },
    "emotions": {
      "enabled": true,
      "model_id": "SamLowe/roberta-base-go_emotions",
      "weight": 0.10,
      "max_length": 512
    }
  },
  
  "thresholds": {
    "critical": 0.85,
    "high": 0.70,
    "medium": 0.50,
    "low": 0.30
  },
  
  "performance": {
    "cache_enabled": true,
    "cache_ttl": 300,
    "cache_max_size": 1000,
    "async_inference": true,
    "batch_size": 1
  },
  
  "fallback": {
    "failure_threshold": 3,
    "recovery_timeout": 60,
    "critical_model": "bart"
  },
  
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    "include_request_id": true
  }
}
```

### production.json

Production-specific overrides:

```json
{
  "_metadata": {
    "environment": "production",
    "description": "Production overrides"
  },
  
  "api": {
    "workers": 4,
    "rate_limit_enabled": true
  },
  
  "models": {
    "device": "auto",
    "warmup_enabled": true
  },
  
  "logging": {
    "level": "INFO"
  }
}
```

### testing.json

Testing-specific overrides:

```json
{
  "_metadata": {
    "environment": "testing",
    "description": "Testing overrides"
  },
  
  "api": {
    "workers": 1,
    "rate_limit_enabled": false
  },
  
  "models": {
    "device": "cpu",
    "warmup_enabled": false,
    "lazy_load": true
  },
  
  "logging": {
    "level": "DEBUG"
  }
}
```

---

## Environment Variables

All configuration settings can be overridden via environment variables using the `NLP_` prefix.

### Naming Convention

```
JSON Path                    → Environment Variable
─────────────────────────────────────────────────────
api.port                     → NLP_API_PORT
models.device                → NLP_MODELS_DEVICE
models.bart.weight           → NLP_MODEL_BART_WEIGHT
thresholds.critical          → NLP_THRESHOLD_CRITICAL
```

### Complete Environment Variable Reference

#### Core Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_ENVIRONMENT` | string | `production` | Environment name (production/testing/development) |
| `NLP_LOG_LEVEL` | string | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |

#### API Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_API_HOST` | string | `0.0.0.0` | Server bind address |
| `NLP_API_PORT` | int | `30880` | Server port |
| `NLP_API_WORKERS` | int | `4` | Uvicorn worker processes |
| `NLP_API_TIMEOUT` | int | `30` | Request timeout (seconds) |
| `NLP_API_RATE_LIMIT_ENABLED` | bool | `true` | Enable rate limiting |
| `NLP_API_RATE_LIMIT_RPM` | int | `60` | Requests per minute limit |

#### Model Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_MODELS_DEVICE` | string | `auto` | Device for inference (auto/cuda/cpu) |
| `NLP_MODELS_WARMUP_ENABLED` | bool | `true` | Run warmup on startup |
| `NLP_MODELS_LAZY_LOAD` | bool | `true` | Load models on first use |
| `NLP_MODELS_MAX_CONCURRENT` | int | `4` | Max concurrent inferences |

#### Model Weight Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_MODEL_BART_WEIGHT` | float | `0.50` | BART model weight |
| `NLP_MODEL_SENTIMENT_WEIGHT` | float | `0.25` | Sentiment model weight |
| `NLP_MODEL_IRONY_WEIGHT` | float | `0.15` | Irony model weight |
| `NLP_MODEL_EMOTIONS_WEIGHT` | float | `0.10` | Emotions model weight |

#### Model Enable/Disable

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_MODEL_BART_ENABLED` | bool | `true` | Enable BART model |
| `NLP_MODEL_SENTIMENT_ENABLED` | bool | `true` | Enable Sentiment model |
| `NLP_MODEL_IRONY_ENABLED` | bool | `true` | Enable Irony model |
| `NLP_MODEL_EMOTIONS_ENABLED` | bool | `true` | Enable Emotions model |

#### Threshold Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_THRESHOLD_CRITICAL` | float | `0.85` | Critical severity threshold |
| `NLP_THRESHOLD_HIGH` | float | `0.70` | High severity threshold |
| `NLP_THRESHOLD_MEDIUM` | float | `0.50` | Medium severity threshold |
| `NLP_THRESHOLD_LOW` | float | `0.30` | Low severity threshold |

#### Performance Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_PERFORMANCE_CACHE_ENABLED` | bool | `true` | Enable response caching |
| `NLP_PERFORMANCE_CACHE_TTL` | int | `300` | Cache TTL (seconds) |
| `NLP_PERFORMANCE_ASYNC_INFERENCE` | bool | `true` | Enable parallel inference |

#### Fallback Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NLP_FALLBACK_FAILURE_THRESHOLD` | int | `3` | Failures before circuit opens |
| `NLP_FALLBACK_RECOVERY_TIMEOUT` | int | `60` | Seconds before retry |

#### HuggingFace Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HF_HOME` | string | `/app/models` | Model cache directory |
| `TRANSFORMERS_OFFLINE` | int | `0` | Offline mode (0=online, 1=offline) |

---

## Model Configuration

### Model Weights

Weights determine each model's contribution to the final crisis score. Weights should sum to 1.0.

```json
{
  "models": {
    "bart": {"weight": 0.50},      // Primary - Zero-shot classification
    "sentiment": {"weight": 0.25}, // Secondary - Emotional context
    "irony": {"weight": 0.15},     // Tertiary - Sarcasm detection
    "emotions": {"weight": 0.10}   // Supplementary - Fine-grained emotions
  }
}
```

### Adjusting Weights

**Higher BART weight** (e.g., 0.60): More emphasis on direct crisis classification
**Higher Sentiment weight** (e.g., 0.35): More emphasis on emotional negativity
**Higher Irony weight** (e.g., 0.25): More false-positive reduction

### Device Configuration

```json
{
  "models": {
    "device": "auto"  // Options: "auto", "cuda", "cuda:0", "cpu"
  }
}
```

| Value | Behavior |
|-------|----------|
| `auto` | Use CUDA if available, else CPU |
| `cuda` | Use default CUDA device |
| `cuda:0` | Use specific CUDA device |
| `cpu` | Force CPU inference |

### HuggingFace Model IDs

Default models can be overridden:

```json
{
  "models": {
    "bart": {
      "model_id": "facebook/bart-large-mnli"
    },
    "sentiment": {
      "model_id": "cardiffnlp/twitter-roberta-base-sentiment-latest"
    }
  }
}
```

---

## Threshold Configuration

Thresholds determine crisis severity levels:

```json
{
  "thresholds": {
    "critical": 0.85,  // ≥ 0.85 = CRITICAL
    "high": 0.70,      // ≥ 0.70 = HIGH
    "medium": 0.50,    // ≥ 0.50 = MEDIUM
    "low": 0.30        // ≥ 0.30 = LOW, < 0.30 = SAFE
  }
}
```

### Threshold Tuning

**Lower thresholds**: More sensitive, more false positives
**Higher thresholds**: Less sensitive, fewer false positives

| Use Case | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| High sensitivity | 0.75 | 0.60 | 0.40 | 0.20 |
| Balanced (default) | 0.85 | 0.70 | 0.50 | 0.30 |
| Conservative | 0.90 | 0.80 | 0.60 | 0.40 |

---

## API Configuration

### Server Settings

```json
{
  "api": {
    "host": "0.0.0.0",        // Bind address
    "port": 30880,            // Port number
    "workers": 4,             // Uvicorn workers
    "timeout": 30             // Request timeout (seconds)
  }
}
```

### Rate Limiting

```json
{
  "api": {
    "rate_limit_enabled": true,
    "rate_limit_rpm": 60      // Requests per minute
  }
}
```

Disable rate limiting for internal services:

```bash
export NLP_API_RATE_LIMIT_ENABLED=false
```

---

## Performance Configuration

### Caching

Response caching reduces load for repeated messages:

```json
{
  "performance": {
    "cache_enabled": true,
    "cache_ttl": 300,         // 5 minutes
    "cache_max_size": 1000    // Max cached responses
  }
}
```

### Async Inference

Parallel model inference (faster but uses more memory):

```json
{
  "performance": {
    "async_inference": true,
    "batch_size": 1
  }
}
```

---

## Logging Configuration

```json
{
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    "include_request_id": true
  }
}
```

### Log Levels

| Level | Description |
|-------|-------------|
| `DEBUG` | Verbose debugging information |
| `INFO` | Normal operational messages |
| `WARNING` | Warning conditions |
| `ERROR` | Error conditions |

### Environment Override

```bash
export NLP_LOG_LEVEL=DEBUG
```

---

## Docker Configuration

### Docker Secrets

Sensitive credentials are managed via Docker Secrets, not environment variables.

#### Supported Secrets

| Secret | File | Description |
|--------|------|-------------|
| `huggingface` | `./secrets/huggingface` | HuggingFace API token |

#### Setup

```bash
# Create secrets directory
mkdir -p secrets

# Add HuggingFace token
echo "hf_your_token_here" > secrets/huggingface
chmod 600 secrets/huggingface
```

#### docker-compose.yml

```yaml
secrets:
  huggingface:
    file: ./secrets/huggingface

services:
  ash-nlp:
    secrets:
      - huggingface
```

#### Reading Secrets in Code

```python
from src.managers import create_secrets_manager

secrets = create_secrets_manager()
token = secrets.get_huggingface_token()
```

See `secrets/README.md` for detailed setup instructions.

### Environment Variables in docker-compose.yml

```yaml
services:
  ash-nlp:
    environment:
      - NLP_ENVIRONMENT=production
      - NLP_API_PORT=30880
      - NLP_API_WORKERS=4
      - NLP_MODELS_DEVICE=auto
      - NLP_LOG_LEVEL=INFO
      - HF_HOME=/app/models
```

### Using .env File

Create `.env` in project root:

```bash
# .env
NLP_ENVIRONMENT=production
NLP_API_PORT=30880
NLP_API_WORKERS=4
NLP_MODELS_DEVICE=auto
NLP_LOG_LEVEL=INFO

# Model weights (optional - defaults are usually fine)
# NLP_MODEL_BART_WEIGHT=0.50
# NLP_MODEL_SENTIMENT_WEIGHT=0.25

# Thresholds (optional - defaults are usually fine)
# NLP_THRESHOLD_CRITICAL=0.85
# NLP_THRESHOLD_HIGH=0.70
```

Reference in docker-compose.yml:

```yaml
services:
  ash-nlp:
    env_file:
      - .env
```

---

## Examples

### Example 1: Development Configuration

```bash
# .env.development
NLP_ENVIRONMENT=development
NLP_API_WORKERS=1
NLP_MODELS_DEVICE=cpu
NLP_MODELS_WARMUP_ENABLED=false
NLP_LOG_LEVEL=DEBUG
NLP_API_RATE_LIMIT_ENABLED=false
```

### Example 2: High-Sensitivity Production

```bash
# Lower thresholds = more sensitive detection
NLP_THRESHOLD_CRITICAL=0.75
NLP_THRESHOLD_HIGH=0.60
NLP_THRESHOLD_MEDIUM=0.40
NLP_THRESHOLD_LOW=0.20
```

### Example 3: CPU-Only Deployment

```bash
NLP_MODELS_DEVICE=cpu
NLP_API_WORKERS=2
NLP_MODELS_WARMUP_ENABLED=true
```

### Example 4: Custom Model Weights

```bash
# Emphasize BART and sentiment over irony/emotions
NLP_MODEL_BART_WEIGHT=0.55
NLP_MODEL_SENTIMENT_WEIGHT=0.30
NLP_MODEL_IRONY_WEIGHT=0.10
NLP_MODEL_EMOTIONS_WEIGHT=0.05
```

### Example 5: Programmatic Configuration

```python
from src.managers import create_config_manager

# Create with specific environment
config = create_config_manager(environment="production")

# Access configuration
api_config = config.get_api_config()
print(f"Port: {api_config['port']}")

weights = config.get_model_weights()
print(f"BART weight: {weights['bart']}")

thresholds = config.get_thresholds()
print(f"Critical threshold: {thresholds['critical']}")
```

---

## Validation

Configuration is validated on load. Invalid configurations cause startup failure:

```
ERROR: Invalid configuration
- models.bart.weight: Value must be between 0.0 and 1.0
- thresholds.critical: Must be greater than thresholds.high
```

### Weight Validation

- All weights must be between 0.0 and 1.0
- Weights should sum to approximately 1.0 (warning if not)

### Threshold Validation

- All thresholds must be between 0.0 and 1.0
- critical > high > medium > low

### Port Validation

- Port must be between 1 and 65535

---

## Troubleshooting

### Configuration Not Loading

```bash
# Check environment
echo $NLP_ENVIRONMENT

# Verify config files exist
ls -la config/

# Run verification script
python verify_installation.py
```

### Environment Variable Not Applied

```bash
# Verify variable is set
env | grep NLP_

# Check Docker passes it correctly
docker exec ash-nlp env | grep NLP_
```

### Invalid JSON

```bash
# Validate JSON syntax
python -m json.tool config/default.json
```

---

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Website**: [alphabetcartel.org](https://alphabetcartel.org)

---

**Built with care for chosen family** 🏳️‍🌈
