# Ash-NLP v5.0 Production Deployment Guide

**FILE VERSION**: v5.0-3-6.1-1  
**LAST MODIFIED**: 2026-01-01  
**PHASE**: Phase 3 Complete - Production Deployment  
**CLEAN ARCHITECTURE**: v5.1 Compliant  

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | https://alphabetcartel.org

---

## Overview

This document covers the production deployment of Ash-NLP v5.0, including configuration requirements, GPU memory management, and Docker Secrets integration.

## System Requirements

### Hardware (Lofn Server)

| Component | Specification |
|-----------|---------------|
| CPU | AMD Ryzen 7 5800x |
| RAM | 64GB |
| GPU | NVIDIA RTX 3060 12GB |
| Storage | NAS mounted at `/storage/nas/` |

### Software

| Component | Version |
|-----------|---------|
| OS | Debian 12 |
| Docker | 24.x+ with Compose v2 |
| NVIDIA Driver | 590.48+ |
| CUDA | 12.1+ (container runtime) |

---

## Critical Configuration Settings

### Worker Count (GPU Memory)

**CRITICAL**: The worker count MUST be set to `1` for GPU deployments on 12GB VRAM cards.

Each worker loads all 4 models independently:
- BART Zero-Shot: ~1.5GB
- Cardiff Sentiment: ~0.5GB  
- Cardiff Irony: ~0.5GB
- RoBERTa Emotions: ~0.5GB
- **Total per worker**: ~3GB

| Workers | GPU Memory Required | 12GB GPU |
|---------|---------------------|----------|
| 1 | ~3GB | ✅ Works |
| 2 | ~6GB | ⚠️ Tight |
| 4 | ~12GB | ❌ OOM |

**Files that control worker count** (all must be set to `1`):

1. **Dockerfile** (lines ~145 and ~235):
   ```dockerfile
   CMD ["python", "-m", "uvicorn", "src.api.app:app", \
        "--host", "0.0.0.0", \
        "--port", "30880", \
        "--workers", "1", \
        "--log-level", "info"]
   ```

2. **Dockerfile ENV** (lines ~115 and ~205):
   ```dockerfile
   ENV NLP_API_WORKERS=1
   ```

3. **docker-compose.yml**:
   ```yaml
   environment:
     - NLP_API_WORKERS=1
   ```

4. **.env file**:
   ```
   NLP_API_WORKERS=1
   ```

5. **main.py**:
   ```python
   DEFAULT_WORKERS = 1
   ```

### User ID / Group ID (NAS Permissions)

The container runs as UID:GID `1001:1001` to match NAS filesystem ownership:

**Dockerfile** (both GPU and CPU stages):
```dockerfile
RUN groupadd --gid 1001 nlp \
    && useradd --uid 1001 --gid 1001 --shell /bin/bash --create-home nlp
```

**docker-compose.yml**:
```yaml
build:
  args:
    - UID=1001
    - GID=1001
```

---

## Docker Secrets (HuggingFace Token)

### Setup

1. Create the secrets directory and file:
   ```bash
   mkdir -p secrets
   echo "hf_your_token_here" > secrets/huggingface
   chmod 600 secrets/huggingface
   ```

2. Verify format (should show token followed by single `$` for newline):
   ```bash
   cat -A secrets/huggingface
   # Correct: hf_xxxxxxxxxxxx$
   # Wrong: hf_xxxxxxxxxxxx^M$ (Windows line endings)
   # Wrong: "hf_xxxxxxxxxxxx"$ (quotes)
   ```

### How It Works

```
./secrets/huggingface (local file, chmod 600)
    ↓
docker-compose.yml (secrets: huggingface: file: ./secrets/huggingface)
    ↓
/run/secrets/huggingface (inside container, read-only)
    ↓
SecretsManager reads and sets HF_TOKEN environment variable
    ↓
Transformers library uses token for model downloads
```

### docker-compose.yml Configuration

```yaml
secrets:
  huggingface:
    file: ./secrets/huggingface

services:
  ash-nlp:
    secrets:
      - huggingface
```

---

## Deployment Commands

### Initial Deployment

```bash
cd /storage/nas/git/ash/ash-nlp

# Create secrets file
mkdir -p secrets
echo "hf_your_token" > secrets/huggingface
chmod 600 secrets/huggingface

# Copy .env from template
cp .env.template .env
# Edit .env if needed

# Build and start
docker compose up -d --build

# Watch startup (first run downloads ~3GB of models)
docker compose logs -f ash-nlp
```

### Rebuilding After Changes

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
docker compose logs -f ash-nlp
```

### Clearing Model Cache (if corrupted)

```bash
docker compose down
docker volume rm ash-nlp-models
docker compose up -d
# Models will re-download on first startup
```

### Checking GPU Usage

```bash
nvidia-smi
# Should show ~3.3GB usage with 1 worker
```

---

## Health Verification

### Health Check Endpoint

```bash
curl http://localhost:30880/health | jq .
```

Expected response:
```json
{
  "status": "healthy",
  "ready": true,
  "degraded": false,
  "models_loaded": 4,
  "total_models": 4,
  "uptime_seconds": 174.44,
  "version": "v5.0-3-4.4-3",
  "timestamp": "2026-01-01T16:18:34.104805"
}
```

### Test Crisis Detection

```bash
# Safe message (should return severity: "safe")
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "Had a great day gaming with friends!"}' | jq .

# Crisis message (should return severity: "critical")
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I cant do this anymore, I want to end it all"}' | jq .
```

---

## Troubleshooting

### CUDA Out of Memory

**Symptom**: Logs show `CUDA out of memory` errors

**Cause**: Multiple workers trying to load models on GPU

**Solution**: Ensure `--workers 1` in all configuration files (see Critical Configuration Settings above)

### Permission Denied on Model Cache

**Symptom**: `PermissionError: [Errno 13] Permission denied: '/app/models/hub/.locks/...'`

**Cause**: Volume created with wrong UID or stale lock files

**Solution**:
```bash
docker compose down
docker volume rm ash-nlp-models
docker compose up -d
```

### Module Not Found: src.api.schemas

**Symptom**: `ModuleNotFoundError: No module named 'src.api.schemas'`

**Cause**: File named `schema.py` instead of `schemas.py`

**Solution**:
```bash
mv src/api/schema.py src/api/schemas.py
```

### HuggingFace Token Not Working

**Symptom**: 401 errors when downloading gated models

**Check**:
```bash
# Inside container
docker exec ash-nlp cat /run/secrets/huggingface

# Should show your token with no extra characters
```

---

## Production Metrics

After successful deployment:

| Metric | Expected Value |
|--------|----------------|
| GPU Memory | ~3.3GB (27% of 12GB) |
| Startup Time | 30-60 seconds (cached models) |
| First Startup | 5-15 minutes (model download) |
| Inference Time | ~150-200ms per message |
| Health Status | `healthy`, `ready: true` |
| Models Loaded | 4/4 |

---

## Port Assignment

| Service | Port |
|---------|------|
| Ash-NLP API | 30880 |

---

## File Checklist

Before deployment, verify these files exist and are configured:

- [ ] `Dockerfile` - workers set to 1, UID/GID 1001
- [ ] `docker-compose.yml` - secrets configured, workers=1
- [ ] `.env` - copied from template, workers=1
- [ ] `secrets/huggingface` - contains valid HF token, chmod 600
- [ ] `src/api/schemas.py` - NOT `schema.py`

---

**Built with care for chosen family** 🏳️‍🌈
