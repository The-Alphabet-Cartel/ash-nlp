# Ash-NLP v5.0 Troubleshooting Guide

**Document Version**: v5.0-3-TROUBLESHOOT-1  
**Last Updated**: 2026-01-01  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [Website](https://alphabetcartel.org)

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Container Startup Issues](#container-startup-issues)
3. [GPU and CUDA Problems](#gpu-and-cuda-problems)
4. [Model Loading Failures](#model-loading-failures)
5. [API Errors](#api-errors)
6. [Memory Issues](#memory-issues)
7. [Network and Connectivity](#network-and-connectivity)
8. [Docker Secrets Problems](#docker-secrets-problems)
9. [Performance Issues](#performance-issues)
10. [Common Error Messages](#common-error-messages)
11. [Log Analysis](#log-analysis)
12. [Getting Help](#getting-help)

---

## Quick Diagnostics

### Health Check

First, verify the service is responding:

```bash
# Check container status
docker ps | grep ash-nlp

# Check health endpoint
curl http://localhost:30880/api/v1/health

# Expected healthy response:
# {"status":"healthy","ready":true,"models_loaded":4,...}
```

### Container Logs

```bash
# View recent logs
docker logs ash-nlp --tail 100

# Follow logs in real-time
docker logs ash-nlp -f

# Search for errors
docker logs ash-nlp 2>&1 | grep -i error
```

### Quick Status Commands

```bash
# GPU status
docker exec ash-nlp nvidia-smi

# Memory usage
docker stats ash-nlp --no-stream

# Check if models are loaded
curl -s http://localhost:30880/api/v1/models | jq
```

---

## Container Startup Issues

### Container Won't Start

**Symptoms**: Container exits immediately or fails to start.

**Diagnostic Steps**:

```bash
# Check container exit code
docker ps -a | grep ash-nlp

# View startup logs
docker logs ash-nlp

# Check docker-compose config
docker compose config
```

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| Port already in use | `sudo lsof -i :30880` then stop conflicting service |
| Invalid docker-compose.yml | Run `docker compose config` to validate |
| Missing secrets directory | Create `./secrets/` directory |
| Permission denied | Check file permissions, ensure UID 1001 can read files |

### Container Starts but Unhealthy

**Symptoms**: Container running but health check fails.

```bash
# Check health status
docker inspect ash-nlp | jq '.[0].State.Health'

# View health check logs
docker inspect ash-nlp | jq '.[0].State.Health.Log'
```

**Solutions**:

1. **Wait for model loading**: Initial startup takes ~45 seconds
2. **Check GPU availability**: Models may fail to load without GPU
3. **Verify model cache**: Ensure `/app/models` volume is mounted

### Restart Loop

**Symptoms**: Container keeps restarting.

```bash
# Check restart count
docker inspect ash-nlp | jq '.[0].RestartCount'

# View logs from last run
docker logs ash-nlp --tail 200
```

**Common Causes**:

- Out of memory (OOM killed)
- GPU driver mismatch
- Missing required secrets
- Corrupted model cache

---

## GPU and CUDA Problems

### GPU Not Detected

**Symptoms**: Models load on CPU instead of GPU, slow inference.

**Diagnostic**:

```bash
# Check GPU visibility in container
docker exec ash-nlp nvidia-smi

# Check CUDA availability
docker exec ash-nlp python -c "import torch; print(torch.cuda.is_available())"
```

**Solutions**:

1. **Install NVIDIA Container Toolkit**:
   ```bash
   # Debian/Ubuntu
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

2. **Verify Docker runtime**:
   ```bash
   docker info | grep -i runtime
   # Should show: Runtimes: nvidia runc
   ```

3. **Check docker-compose.yml**:
   ```yaml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: 1
             capabilities: [gpu]
   ```

### CUDA Version Mismatch

**Symptoms**: `CUDA error: no kernel image is available for execution`

**Solution**:

```bash
# Check host CUDA version
nvidia-smi | grep "CUDA Version"

# Ensure container CUDA matches (12.1 in our case)
# If mismatch, rebuild with correct base image
```

### GPU Out of Memory

**Symptoms**: `CUDA out of memory` errors, container crash.

**Diagnostic**:

```bash
# Check GPU memory usage
docker exec ash-nlp nvidia-smi

# Should show ~3.3GB used for 4 models
```

**Solutions**:

1. **Reduce workers to 1**:
   ```yaml
   # docker-compose.yml
   command: ["uvicorn", "src.api.app:app", "--workers", "1", ...]
   ```

2. **Ensure single worker in ALL locations** (7 places in docker-compose.yml):
   - GPU service command
   - GPU service environment
   - GPU service healthcheck
   - CPU service command
   - CPU service environment
   - CPU service healthcheck
   - Dockerfile CMD

3. **Clear GPU cache**:
   ```bash
   docker exec ash-nlp python -c "import torch; torch.cuda.empty_cache()"
   ```

---

## Model Loading Failures

### Models Won't Download

**Symptoms**: Stuck on "Downloading model..." or timeout.

**Diagnostic**:

```bash
# Check network from container
docker exec ash-nlp curl -I https://huggingface.co

# Check HuggingFace token
docker exec ash-nlp printenv | grep HF
```

**Solutions**:

1. **Add HuggingFace token** (for rate limits):
   ```bash
   echo "hf_your_token_here" > secrets/huggingface
   chmod 600 secrets/huggingface
   ```

2. **Use cached models**:
   ```bash
   # Pre-download models on host
   pip install huggingface_hub
   huggingface-cli download facebook/bart-large-mnli
   huggingface-cli download cardiffnlp/twitter-roberta-base-sentiment-latest
   huggingface-cli download cardiffnlp/twitter-roberta-base-irony
   huggingface-cli download SamLowe/roberta-base-go_emotions
   
   # Mount cache to container
   # Add to docker-compose.yml volumes:
   # - ~/.cache/huggingface:/app/models
   ```

3. **Check firewall/proxy**:
   ```bash
   # If behind corporate proxy
   docker exec ash-nlp env | grep -i proxy
   ```

### Specific Model Fails to Load

**Symptoms**: One model fails while others succeed.

**Diagnostic**:

```bash
# Check which models loaded
curl -s http://localhost:30880/api/v1/models | jq '.models[].name'

# Check logs for specific model
docker logs ash-nlp 2>&1 | grep -i "sentiment\|irony\|emotions\|bart"
```

**Solutions**:

1. **Clear model cache**:
   ```bash
   docker exec ash-nlp rm -rf /app/models/models--cardiffnlp--*
   docker restart ash-nlp
   ```

2. **Disable problematic model temporarily**:
   ```bash
   # In .env
   NLP_MODEL_IRONY_ENABLED=false
   ```

### Model Version Mismatch

**Symptoms**: Unexpected classification results, accuracy drop.

**Solution**:

```bash
# Pin model versions in config/production.json
{
  "models": {
    "bart": {
      "model_id": "facebook/bart-large-mnli",
      "revision": "main"  # or specific commit hash
    }
  }
}
```

---

## API Errors

### 500 Internal Server Error

**Diagnostic**:

```bash
# Check recent errors in logs
docker logs ash-nlp 2>&1 | grep -A5 "500\|ERROR\|Exception"

# Test with verbose output
curl -v -X POST http://localhost:30880/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "test message"}'
```

**Common Causes**:

| Error | Cause | Solution |
|-------|-------|----------|
| `Model not loaded` | Startup incomplete | Wait or restart |
| `CUDA error` | GPU issue | Check GPU section |
| `OutOfMemoryError` | RAM exhausted | Reduce workers |

### 422 Validation Error

**Symptoms**: Request rejected with validation error.

**Example**:
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solution**: Ensure request body is valid JSON with required fields:

```bash
# Correct request format
curl -X POST http://localhost:30880/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "Your message here"}'
```

### 429 Rate Limited

**Symptoms**: `Too Many Requests` response.

**Solution**:

1. **Wait and retry** with exponential backoff
2. **Increase rate limit**:
   ```bash
   # In .env
   NLP_API_RATE_LIMIT_RPM=120
   ```

### Connection Refused

**Diagnostic**:

```bash
# Check if container is running
docker ps | grep ash-nlp

# Check if port is listening
docker exec ash-nlp ss -tlnp | grep 30880

# Check host port binding
sudo ss -tlnp | grep 30880
```

**Solutions**:

1. Container not running → `docker compose up -d`
2. Port not bound → Check docker-compose.yml ports section
3. Firewall blocking → `sudo ufw allow 30880`

---

## Memory Issues

### Out of Memory (OOM) Killed

**Symptoms**: Container suddenly stops, `Killed` in logs.

**Diagnostic**:

```bash
# Check if OOM killed
dmesg | grep -i "killed process"

# Check container memory limit
docker inspect ash-nlp | jq '.[0].HostConfig.Memory'
```

**Solutions**:

1. **Increase memory limit**:
   ```yaml
   # docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 12G
   ```

2. **Reduce to single worker** (most common fix)

3. **Monitor memory usage**:
   ```bash
   docker stats ash-nlp
   ```

### High Memory Usage

**Expected Usage**:

| Component | Memory |
|-----------|--------|
| BART model | ~1.5GB |
| Sentiment model | ~0.5GB |
| Irony model | ~0.5GB |
| Emotions model | ~0.5GB |
| Python/FastAPI | ~0.5GB |
| **Total** | **~3.5GB** |

**If significantly higher**:

1. Check for memory leaks:
   ```bash
   # Monitor over time
   watch -n 5 'docker stats ash-nlp --no-stream'
   ```

2. Restart container periodically (temporary fix)

3. Check response cache size:
   ```bash
   curl -s http://localhost:30880/api/v1/health | jq '.cache'
   ```

---

## Network and Connectivity

### Cannot Reach API from Other Hosts

**Diagnostic**:

```bash
# From another host
curl http://10.20.30.253:30880/api/v1/health

# Check if binding to all interfaces
docker exec ash-nlp ss -tlnp
# Should show 0.0.0.0:30880
```

**Solutions**:

1. **Check firewall**:
   ```bash
   sudo ufw status
   sudo ufw allow 30880
   ```

2. **Verify docker-compose.yml**:
   ```yaml
   ports:
     - "30880:30880"  # Not "127.0.0.1:30880:30880"
   ```

3. **Check Docker network**:
   ```bash
   docker network ls
   docker network inspect ash-nlp_default
   ```

### DNS Resolution Failures

**Symptoms**: Cannot download models, connection timeouts.

**Solution**:

```yaml
# docker-compose.yml
services:
  ash-nlp:
    dns:
      - 8.8.8.8
      - 8.8.4.4
```

---

## Docker Secrets Problems

### Secret Not Found

**Symptoms**: `FileNotFoundError: /run/secrets/huggingface`

**Diagnostic**:

```bash
# Check secrets in container
docker exec ash-nlp ls -la /run/secrets/

# Check secrets directory on host
ls -la ./secrets/
```

**Solutions**:

1. **Create secrets directory**:
   ```bash
   mkdir -p secrets
   chmod 700 secrets
   ```

2. **Create secret file**:
   ```bash
   echo "your_token" > secrets/huggingface
   chmod 600 secrets/huggingface
   ```

3. **Verify docker-compose.yml**:
   ```yaml
   secrets:
     huggingface:
       file: ./secrets/huggingface
   
   services:
     ash-nlp:
       secrets:
         - huggingface
   ```

### Secret Has Wrong Permissions

**Symptoms**: Secret visible but empty or permission denied.

**Solution**:

```bash
# Fix permissions
chmod 600 secrets/*
chown 1001:1001 secrets/*  # Match container UID
```

### Secret Contains Newline

**Symptoms**: Token rejected, authentication fails.

**Solution**:

```bash
# Create without trailing newline
echo -n "your_token" > secrets/huggingface

# Or use printf
printf '%s' "your_token" > secrets/huggingface
```

---

## Performance Issues

### Slow Inference (>500ms)

**Diagnostic**:

```bash
# Check response times
curl -w "\nTime: %{time_total}s\n" -X POST http://localhost:30880/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check if using GPU
docker exec ash-nlp python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

**Solutions**:

1. **Ensure GPU is being used** (CPU is 10x slower)
2. **Enable response caching**:
   ```bash
   NLP_CACHE_ENABLED=true
   NLP_CACHE_TTL=300
   ```
3. **Check for thermal throttling**:
   ```bash
   docker exec ash-nlp nvidia-smi -q -d PERFORMANCE
   ```

### High Latency on First Request

**Expected**: First request after startup is slower (model warmup).

**Solution**: This is normal. Subsequent requests should be faster.

```bash
# Verify warmup completed in logs
docker logs ash-nlp | grep -i "warmed up"
```

### Cache Not Working

**Diagnostic**:

```bash
# Check cache stats
curl -s http://localhost:30880/api/v1/health | jq '.cache'

# Expected:
# {"enabled": true, "size": X, "hit_rate": 0.XX}
```

**Solutions**:

1. **Enable caching**:
   ```bash
   NLP_CACHE_ENABLED=true
   ```

2. **Check cache size**:
   ```bash
   NLP_CACHE_MAX_SIZE=1000
   ```

---

## Common Error Messages

### `RuntimeError: CUDA error: out of memory`

**Cause**: GPU VRAM exhausted.

**Solution**: Reduce workers to 1 (see GPU section).

---

### `ModuleNotFoundError: No module named 'xxx'`

**Cause**: Dependency not installed in container.

**Solution**:

```bash
# Rebuild container
docker compose build --no-cache
docker compose up -d
```

---

### `OSError: [Errno 28] No space left on device`

**Cause**: Disk full (often model cache).

**Solution**:

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a

# Clean model cache
rm -rf ~/.cache/huggingface/hub/models--*
```

---

### `ConnectionRefusedError: [Errno 111] Connection refused`

**Cause**: Service not running or wrong port.

**Solution**: See [Connection Refused](#connection-refused) section.

---

### `torch.cuda.OutOfMemoryError: CUDA out of memory`

**Cause**: Multiple workers loading models.

**Solution**:

```bash
# Ensure single worker
grep -r "workers" docker-compose.yml
# Should show --workers 1 everywhere
```

---

### `PermissionError: [Errno 13] Permission denied`

**Cause**: Container user cannot access files.

**Solution**:

```bash
# Fix ownership for container UID 1001
sudo chown -R 1001:1001 ./models ./logs ./secrets
```

---

## Log Analysis

### Understanding Log Levels

| Level | Meaning | Action |
|-------|---------|--------|
| DEBUG | Detailed info | Usually ignore |
| INFO | Normal operation | Informational |
| WARNING | Potential issue | Monitor |
| ERROR | Operation failed | Investigate |
| CRITICAL | System failure | Immediate action |

### Useful Log Searches

```bash
# Find all errors
docker logs ash-nlp 2>&1 | grep -i "error\|exception\|failed"

# Find model loading issues
docker logs ash-nlp 2>&1 | grep -i "loading\|loaded\|model"

# Find performance issues
docker logs ash-nlp 2>&1 | grep -i "timeout\|slow\|latency"

# Find crisis detections
docker logs ash-nlp 2>&1 | grep -i "crisis\|critical\|high"

# Count errors in last hour
docker logs ash-nlp --since 1h 2>&1 | grep -c -i error
```

### Enable Debug Logging

```bash
# Temporarily enable debug logs
NLP_LOG_LEVEL=DEBUG

# Then restart
docker compose restart
```

---

## Getting Help

### Before Asking for Help

1. **Check this guide** for your specific issue
2. **Collect diagnostic info**:
   ```bash
   # Create diagnostic bundle
   mkdir -p /tmp/ash-diag
   docker logs ash-nlp > /tmp/ash-diag/logs.txt 2>&1
   docker inspect ash-nlp > /tmp/ash-diag/inspect.json
   curl -s http://localhost:30880/api/v1/health > /tmp/ash-diag/health.json
   docker exec ash-nlp nvidia-smi > /tmp/ash-diag/gpu.txt 2>&1
   ```

3. **Note the exact error message**
4. **Note when the issue started**

### Community Support

- **Discord**: https://discord.gg/alphabetcartel
- **GitHub Issues**: https://github.com/the-alphabet-cartel/ash-nlp/issues

### Reporting a Bug

Include:
- Ash-NLP version (`docker exec ash-nlp cat /app/VERSION` or check logs)
- Docker version (`docker --version`)
- Host OS and version
- GPU model (if applicable)
- Steps to reproduce
- Error message and logs
- What you've already tried

---

## Quick Reference Card

### Essential Commands

```bash
# Start service
docker compose up -d

# Stop service
docker compose down

# View logs
docker logs ash-nlp -f

# Restart
docker compose restart

# Rebuild
docker compose build --no-cache && docker compose up -d

# Health check
curl http://localhost:30880/api/v1/health

# GPU status
docker exec ash-nlp nvidia-smi

# Enter container shell
docker exec -it ash-nlp /bin/bash
```

### Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Container configuration |
| `.env` | Environment variables |
| `secrets/huggingface` | HuggingFace token |
| `secrets/discord_alert_webhook` | Discord alerts |
| `config/production.json` | App configuration |

### Key Ports

| Port | Service |
|------|---------|
| 30880 | Ash-NLP API |

### Key Paths (in container)

| Path | Purpose |
|------|---------|
| `/app` | Application code |
| `/app/models` | Model cache |
| `/app/logs` | Log files |
| `/run/secrets` | Docker secrets |

---

*Built with care for chosen family* 🏳️‍🌈
