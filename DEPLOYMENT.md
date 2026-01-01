# Ash-NLP v5.0 Deployment Guide

**Target Server**: Lofn (10.20.30.253)  
**Service Port**: 30880  
**Last Updated**: 2025-12-31

---

## 📋 Prerequisites Checklist

Before deploying, verify Lofn has:

- [ ] Docker Engine 24.0+ installed
- [ ] Docker Compose v2.20+ installed
- [ ] NVIDIA Container Toolkit installed (for GPU support)
- [ ] NVIDIA Driver 525+ installed
- [ ] Git installed
- [ ] Network access to Docker Hub and HuggingFace

### Verify Prerequisites

```bash
# SSH into Lofn
ssh user@10.20.30.253

# Check Docker
docker --version
# Expected: Docker version 24.x or higher

# Check Docker Compose
docker compose version
# Expected: Docker Compose version v2.20.x or higher

# Check NVIDIA Driver
nvidia-smi
# Expected: Shows GPU info (RTX 3060 12GB)

# Check NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
# Expected: Shows GPU info inside container
```

---

## 🚀 Deployment Steps

### Step 1: Get the Code

**Option A: Clone from GitHub**
```bash
cd /opt
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp
```

**Option B: Copy from Network Share**
```bash
# If using network share
cp -r /path/to/nas/git/ash/ash-nlp /opt/ash-nlp
cd /opt/ash-nlp
```

### Step 2: Verify File Structure

```bash
# Run verification script
python3 verify_installation.py

# Expected output: All checks pass
```

If verification fails, fix any missing files before proceeding.

### Step 3: Configure Environment (Optional)

The defaults work out of the box, but you can customize:

```bash
# Copy and edit environment template
cp .env.template .env
nano .env

# Key settings to review:
# NLP_API_PORT=30880
# NLP_LOG_LEVEL=INFO
# NLP_MODELS_DEVICE=auto
```

### Step 4: Build Docker Image

```bash
# Build the GPU-enabled image
docker compose build

# This will:
# - Download base images
# - Install Python dependencies
# - Copy application code
# Takes ~5-10 minutes on first build
```

### Step 5: Start the Service

```bash
# Start in detached mode
docker compose up -d

# Watch the startup logs
docker compose logs -f ash-nlp
```

**Expected Startup Sequence:**
```
🚀 Starting Ash-NLP Service...
Creating default configuration...
Initializing Decision Engine...
Loading ensemble models...
📥 Downloading facebook/bart-large-mnli...     # First run only
📥 Downloading cardiffnlp/twitter-roberta...   # First run only
✅ bart loaded in X.XXs (device: cuda:0)
✅ sentiment loaded in X.XXs (device: cuda:0)
✅ irony loaded in X.XXs (device: cuda:0)
✅ emotions loaded in X.XXs (device: cuda:0)
🔥 Warming up engine...
✅ Ash-NLP Service started in XX.XXs
```

**First startup takes 5-15 minutes** (downloading models from HuggingFace).  
**Subsequent startups take 30-60 seconds** (loading from cache).

### Step 6: Verify Deployment

```bash
# Health check
curl http://localhost:30880/health

# Expected response:
# {"status":"healthy","ready":true,"degraded":false,"models_loaded":4,...}

# Test analysis endpoint
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling happy today!"}'

# Expected: crisis_detected: false, severity: safe

# Test crisis detection
curl -X POST http://localhost:30880/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I dont know if I can keep going anymore"}'

# Expected: crisis_detected: true, severity: high or critical
```

### Step 7: Verify from External Machine

From another machine on the network:

```bash
curl http://10.20.30.253:30880/health
curl http://10.20.30.253:30880/docs  # Opens in browser
```

---

## 🔧 Management Commands

### View Logs

```bash
# Follow logs
docker compose logs -f ash-nlp

# Last 100 lines
docker compose logs --tail 100 ash-nlp
```

### Restart Service

```bash
docker compose restart ash-nlp
```

### Stop Service

```bash
docker compose down
```

### Update Code and Rebuild

```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose up -d --build
```

### Check Resource Usage

```bash
# Container stats
docker stats ash-nlp

# GPU usage
nvidia-smi

# Expected GPU memory: ~6-8GB under load
```

### Enter Container for Debugging

```bash
docker exec -it ash-nlp bash

# Inside container:
python -c "from src.ensemble import create_decision_engine; print('OK')"
```

---

## 📊 Monitoring Endpoints

| Endpoint | Purpose | Usage |
|----------|---------|-------|
| `/health` | Load balancer health check | `curl localhost:30880/health` |
| `/healthz` | Kubernetes-style health | `curl localhost:30880/healthz` |
| `/ready` | Readiness probe | `curl localhost:30880/ready` |
| `/status` | Detailed service status | `curl localhost:30880/status` |
| `/docs` | Swagger UI | Browser |

---

## 🐛 Troubleshooting

### Issue: Container Won't Start

```bash
# Check logs
docker compose logs ash-nlp

# Common causes:
# - Port 30880 already in use
# - GPU not available
# - Missing config files
```

### Issue: GPU Not Detected

```bash
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi

# If this fails, reinstall NVIDIA Container Toolkit:
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
```

### Issue: Models Fail to Download

```bash
# Check network access to HuggingFace
curl -I https://huggingface.co

# If blocked, download models manually and mount volume:
# 1. Download models on another machine
# 2. Copy to /opt/ash-nlp/models/
# 3. Mount in docker-compose.yml
```

### Issue: Out of GPU Memory

```bash
# Check GPU memory
nvidia-smi

# Reduce workers in docker-compose.yml:
# command: ... --workers 2

# Or switch to CPU mode:
# docker compose --profile cpu up -d
```

### Issue: Slow First Response

This is normal! First request after startup triggers model warmup.
- First request: 5-30 seconds
- Subsequent requests: 50-150ms

### Issue: High CPU/Memory Usage

```bash
# Check container stats
docker stats ash-nlp

# Normal ranges:
# - CPU: 10-50% per request
# - Memory: 4-8GB
# - GPU Memory: 6-8GB
```

---

## 🔄 Maintenance

### Clear Model Cache

If models become corrupted:

```bash
# Stop service
docker compose down

# Remove model volume
docker volume rm ash-nlp-models

# Restart (will re-download models)
docker compose up -d
```

### View Model Cache Size

```bash
docker exec ash-nlp du -sh /app/models
# Expected: ~3-4GB
```

### Backup Configuration

```bash
# Backup config directory
tar -czvf ash-nlp-config-backup.tar.gz config/
```

---

## ✅ Deployment Checklist

- [ ] Prerequisites verified
- [ ] Code deployed to `/opt/ash-nlp`
- [ ] `verify_installation.py` passes
- [ ] Docker image built
- [ ] Service started with `docker compose up -d`
- [ ] Health check returns healthy
- [ ] Test analysis returns expected results
- [ ] External access verified (port 30880)
- [ ] Logs show no errors

---

## 📞 Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Website**: [alphabetcartel.org](https://alphabetcartel.org)

---

**Built with care for chosen family** 🏳️‍🌈
