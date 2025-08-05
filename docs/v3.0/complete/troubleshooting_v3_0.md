# Ash NLP v3.0 Troubleshooting Guide

**Comprehensive troubleshooting for the Three Zero-Shot Model Ensemble crisis detection system**

---

## 🚨 Quick Diagnosis

### System Health Check

Start with these basic commands to assess system status:

```bash
# Check if service is responding
curl http://localhost:8881/health

# Check detailed system stats  
curl http://localhost:8881/stats

# Check Docker container status
docker ps | grep ash-nlp

# Check container logs
docker logs ash-nlp --tail 50
```

### Emergency Quick Fixes

#### Service Won't Start
```bash
# Restart the container
docker-compose restart ash-nlp

# Rebuild if configuration changed
docker-compose build ash-nlp
docker-compose up ash-nlp
```

#### Models Not Loading
```bash
# Check available memory
free -h
nvidia-smi  # If using GPU

# Check disk space
df -h

# Restart with more memory
docker-compose down
# Edit docker-compose.yml to increase memory limits
docker-compose up ash-nlp
```

---

## 🔍 Common Issues & Solutions

### 1. Container Startup Issues

#### Issue: Container Exits Immediately
**Symptoms**:
- Container stops right after starting
- Exit code 1 or 137 in logs

**Diagnostic Commands**:
```bash
# Check container exit reason
docker logs ash-nlp

# Check resource limits
docker stats ash-nlp

# Check available system resources
free -h && df -h
```

**Solutions**:

**A. Insufficient Memory**
```yaml
# In docker-compose.yml, increase memory:
deploy:
  resources:
    limits:
      memory: 12G  # Increase from 8G
      cpus: '6.0'  # Increase CPU if needed
```

**B. Missing Environment Variables**
```bash
# Check if all required variables are set
docker exec ash-nlp env | grep NLP_

# Common missing variables:
NLP_EMOTIONAL_DISTRESS_MODEL=facebook/bart-large-mnli
NLP_ENSEMBLE_MODE=weighted
```

**C. Port Conflicts**
```bash
# Check if port 8881 is in use
netstat -tulpn | grep 8881

# Change port if needed
NLP_SERVICE_PORT=8882
```

---

### 2. Model Loading Problems

#### Issue: Models Won't Load
**Symptoms**:
- `"model_loaded": false` in health check
- 503 Service Unavailable responses
- "Models not ready" errors

**Diagnostic Commands**:
```bash
# Check model loading progress
docker logs ash-nlp | grep -E "(Loading|loaded|Model)"

# Check GPU memory if using CUDA
docker exec ash-nlp nvidia-smi

# Check disk space for model cache
docker exec ash-nlp df -h /app/models/cache
```

**Solutions**:

**A. GPU Memory Issues**
```bash
# Check GPU memory usage
nvidia-smi

# If insufficient GPU memory, force CPU mode:
NLP_DEVICE=cpu
```

**B. Network/Download Issues**
```bash
# Check Hugging Face token
docker exec ash-nlp env | grep HUGGINGFACE

# Test manual download
docker exec ash-nlp python -c "
from transformers import pipeline
pipeline('text-classification', model='MoritzLaurer/deberta-v3-base-zeroshot-v2.0')
"
```

**C. Disk Space Issues**
```bash
# Clear old model cache
docker exec ash-nlp rm -rf /app/models/cache/*

# Increase disk allocation or clean system
df -h
```

---

### 3. Performance Issues

#### Issue: Slow Response Times (>100ms)
**Symptoms**:
- API responses taking 100ms+ consistently
- Timeouts on `/analyze` endpoint

**Diagnostic Commands**:
```bash
# Test response time
time curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "user_id": "test", "channel_id": "test"}'

# Check system resources
docker stats ash-nlp

# Check current configuration
curl http://localhost:8881/stats | jq '.hardware_config'
```

**Solutions**:

**A. Optimize Batch Size**
```bash
# For RTX 3060 (12GB VRAM):
NLP_MAX_BATCH_SIZE=48

# For RTX 3050 (8GB VRAM):
NLP_MAX_BATCH_SIZE=32

# For CPU only:
NLP_MAX_BATCH_SIZE=16
```

**B. Increase Thread Count**
```bash
# For Ryzen 7 5800X (8 cores/16 threads):
NLP_INFERENCE_THREADS=16

# For 6-core CPU:
NLP_INFERENCE_THREADS=12

# For 4-core CPU:
NLP_INFERENCE_THREADS=8
```

**C. GPU Optimization**
```bash
# Enable GPU if available
NLP_DEVICE=auto  # or cuda:0

# Use appropriate precision
NLP_MODEL_PRECISION=float16  # Faster, less memory
# NLP_MODEL_PRECISION=float32  # Slower, more accurate
```

---

### 4. Gap Detection Issues

#### Issue: Gap Detection Not Working
**Symptoms**:
- `"gaps_detected": false` for all messages
- No staff review flags for ambiguous messages

**Diagnostic Commands**:
```bash
# Test with known gap-triggering message
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "This exam is killing me but I can handle it", "user_id": "test", "channel_id": "test"}' \
  | jq '.ensemble_analysis.gaps_detected'

# Check gap detection configuration
curl http://localhost:8881/stats | jq '.configuration.ensemble'
```

**Solutions**:

**A. Lower Gap Detection Thresholds**
```bash
# Make gap detection more sensitive
NLP_GAP_DETECTION_THRESHOLD=0.3      # Lower from 0.4
NLP_DISAGREEMENT_THRESHOLD=0.4       # Lower from 0.5
```

**B. Verify All Models Are Loaded**
```bash
# Check that all three models are working
curl http://localhost:8881/stats | jq '.models_loaded'

# Should show all three models as loaded:
# depression, sentiment, emotional_distress
```

**C. Test Individual Model Responses**
```bash
# Test each model's response to ambiguous message
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I am dying to see that movie", "user_id": "test", "channel_id": "test"}' \
  | jq '.ensemble_analysis.individual_results'
```

---

### 5. Authentication Issues

#### Issue: API Key/Secrets Problems
**Symptoms**:
- `"huggingface_token": false` in health check
- Models fail to download
- Authentication errors

**Diagnostic Commands**:
```bash
# Check secrets status
curl http://localhost:8881/health | jq '.hardware_info.secrets_status'

# Check if secret files exist
docker exec ash-nlp ls -la /run/secrets/

# Check environment variables
docker exec ash-nlp env | grep -E "(HUGGINGFACE|CLAUDE)"
```

**Solutions**:

**A. Fix Docker Secrets**
```bash
# Ensure secrets directory is mounted
# In docker-compose.yml:
volumes:
  - ./secrets:/run/secrets:ro

# Check secret file contents
cat ./secrets/huggingface
cat ./secrets/claude_api_key
```

**B. Use Environment Variables Instead**
```bash
# If secrets aren't working, use direct env vars:
GLOBAL_HUGGINGFACE_TOKEN=hf_your_token_here
GLOBAL_CLAUDE_API_KEY=your_claude_key_here
```

**C. Create Missing Secret Files**
```bash
# Create secrets directory
mkdir -p ./secrets

# Add your tokens
echo "hf_your_token_here" > ./secrets/huggingface
echo "your_claude_key_here" > ./secrets/claude_api_key

# Set proper permissions
chmod 600 ./secrets/*
```

---

### 6. Memory Issues

#### Issue: Out of Memory Errors
**Symptoms**:
- Container killed with exit code 137
- "CUDA out of memory" errors
- System becomes unresponsive

**Diagnostic Commands**:
```bash
# Check memory usage
free -h
docker stats ash-nlp

# Check GPU memory if applicable
nvidia-smi

# Check Docker memory limits
docker inspect ash-nlp | grep -i memory
```

**Solutions**:

**A. Increase Docker Memory Limits**
```yaml
# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 12G  # Increase from 8G
```

**B. Optimize Model Loading**
```bash
# Use lower precision to save memory
NLP_MODEL_PRECISION=float16

# Reduce batch size
NLP_MAX_BATCH_SIZE=24  # Reduce from 48

# Reduce concurrent requests
NLP_MAX_CONCURRENT_REQUESTS=10  # Reduce from 20
```

**C. Force CPU Mode**
```bash
# If GPU memory is insufficient
NLP_DEVICE=cpu
```

---

### 7. Configuration Issues

#### Issue: Environment Variables Not Applied
**Symptoms**:
- Settings don't change despite updating `.env`
- Default values used instead of configured values

**Diagnostic Commands**:
```bash
# Check current configuration
curl http://localhost:8881/stats | jq '.configuration'

# Check environment variables in container
docker exec ash-nlp env | grep NLP_

# Check if .env file is being read
docker-compose config
```

**Solutions**:

**A. Restart After Config Changes**
```bash
# Always restart after changing .env
docker-compose down
docker-compose up ash-nlp
```

**B. Rebuild After Major Changes**
```bash
# For structural changes, rebuild
docker-compose build ash-nlp
docker-compose up ash-nlp
```

**C. Check Variable Names**
```bash
# Ensure variables match exactly:
NLP_ENSEMBLE_MODE=weighted                    # Correct
NLP_ENSEMBLE_MODE="consensus"                  # Also correct
ENSEMBLE_MODE=consensus                        # Wrong - missing NLP_ prefix
```

---

## 🔧 Advanced Troubleshooting

### Debug Mode

Enable comprehensive logging:

```bash
# Enable debug mode
GLOBAL_LOG_LEVEL=DEBUG

# Restart and check detailed logs
docker-compose restart ash-nlp
docker logs ash-nlp -f
```

### Model-Specific Debugging

#### Test Individual Models

```bash
# Test depression model specifically
docker exec ash-nlp python -c "
from transformers import pipeline
model = pipeline('text-classification', 
                model='MoritzLaurer/deberta-v3-base-zeroshot-v2.0', 
                device=0)
print(model('I am feeling down'))
"

# Test sentiment model
docker exec ash-nlp python -c "
from transformers import pipeline
model = pipeline('sentiment-analysis',
                model='Lowerated/lm6-deberta-v3-topic-sentiment',
                device=0)
print(model('I am feeling down'))
"

# Test emotional distress model
docker exec ash-nlp python -c "
from transformers import pipeline
model = pipeline('sentiment-analysis',
                model='facebook/bart-large-mnli',
                device=0)
print(model('I am feeling down'))
"
```

### Performance Profiling

```bash
# Monitor resource usage during requests
# Terminal 1: Start monitoring
docker stats ash-nlp

# Terminal 2: Send test requests
for i in {1..10}; do
  time curl -X POST http://localhost:8881/analyze \
    -H "Content-Type: application/json" \
    -d '{"message": "test message '$i'", "user_id": "test", "channel_id": "test"}' \
    > /dev/null 2>&1
done
```

### Database/Cache Issues

```bash
# Clear learning data if corrupted
docker exec ash-nlp rm -f /app/learning_data/adjustments.json

# Clear model cache and re-download
docker exec ash-nlp rm -rf /app/models/cache/*
docker-compose restart ash-nlp
```

---

## 🚨 Error Code Reference

### HTTP Status Codes

| Code | Issue | Solution |
|------|-------|----------|
| 400 | Invalid request format | Check JSON syntax and required fields |
| 422 | Empty/invalid message | Ensure message content is non-empty string |
| 429 | Rate limit exceeded | Reduce request frequency or increase limits |
| 500 | Internal server error | Check container logs for detailed error |
| 503 | Models not ready | Wait for model loading or check memory |

### Common Error Messages

#### "Models not loaded"
**Cause**: Models still loading or failed to load  
**Solution**: Wait 60-90 seconds or check model loading logs

#### "CUDA out of memory"
**Cause**: GPU memory insufficient for all three models  
**Solution**: Reduce batch size or use CPU mode

#### "PermissionError at ./models/cache"
**Cause**: File permission issues in model cache  
**Solution**: Fix cache directory permissions

```bash
docker exec ash-nlp chown -R nlpuser:nlpuser /app/models/cache
```

#### "Gap detection threshold invalid"
**Cause**: Invalid threshold values in configuration  
**Solution**: Ensure thresholds are between 0.0 and 1.0

---

## 🔄 Recovery Procedures

### Complete System Reset

If all else fails, complete reset procedure:

```bash
# 1. Stop all services
docker-compose down

# 2. Remove containers and images
docker-compose rm -f ash-nlp
docker rmi $(docker images | grep ash-nlp | awk '{print $3}')

# 3. Clear caches
rm -rf ./ash-nlp/models/cache/*
rm -rf ./ash-nlp/logs/*
rm -rf ./ash-nlp/learning_data/*

# 4. Rebuild from scratch
docker-compose build --no-cache ash-nlp

# 5. Start with debug enabled
GLOBAL_LOG_LEVEL=DEBUG docker-compose up ash-nlp
```

### Rollback to Previous Version

```bash
# Switch to previous stable branch
cd ash-nlp
git checkout v2.1.0  # or previous stable version

# Rebuild with old configuration
docker-compose build ash-nlp
docker-compose up ash-nlp
```

### Data Recovery

```bash
# Backup learning data before reset
cp ./ash-nlp/learning_data/adjustments.json ./learning_backup.json

# Restore after reset
cp ./learning_backup.json ./ash-nlp/learning_data/adjustments.json
```

---

## 📊 Monitoring & Alerts

### Health Monitoring Script

```bash
#!/bin/bash
# health_monitor.sh - Monitor Ash NLP health

while true; do
    # Check health endpoint
    HEALTH=$(curl -s http://localhost:8881/health | jq -r '.status')
    
    if [ "$HEALTH" != "healthy" ]; then
        echo "⚠️ $(date): System unhealthy - $HEALTH"
        
        # Try to restart
        docker-compose restart ash-nlp
        
        # Wait for restart
        sleep 60
        
        # Check again
        HEALTH=$(curl -s http://localhost:8881/health | jq -r '.status')
        if [ "$HEALTH" != "healthy" ]; then
            echo "🚨 $(date): Restart failed - manual intervention required"
        else
            echo "✅ $(date): System recovered"
        fi
    else
        echo "✅ $(date): System healthy"
    fi
    
    sleep 300  # Check every 5 minutes
done
```

### Performance Alert Script

```bash
#!/bin/bash
# performance_monitor.sh - Monitor response times

THRESHOLD=100  # 100ms threshold

RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total_ms}" \
  -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "user_id": "test", "channel_id": "test"}')

RESPONSE_TIME_INT=${RESPONSE_TIME%.*}  # Convert to integer

if [ "$RESPONSE_TIME_INT" -gt "$THRESHOLD" ]; then
    echo "⚠️ $(date): Slow response time: ${RESPONSE_TIME}ms (threshold: ${THRESHOLD}ms)"
    
    # Check system resources
    echo "CPU Usage:"
    docker stats ash-nlp --no-stream --format "table {{.CPUPerc}}"
    
    echo "Memory Usage:"
    docker stats ash-nlp --no-stream --format "table {{.MemUsage}}"
    
else
    echo "✅ $(date): Response time normal: ${RESPONSE_TIME}ms"
fi
```

---

## 📞 Getting Help

### Information to Collect

Before reporting issues, collect this information:

```bash
# System information
uname -a
docker --version
docker-compose --version

# Service information
curl http://localhost:8881/health
curl http://localhost:8881/stats

# Container information
docker logs ash-nlp --tail 100
docker inspect ash-nlp

# Resource usage
docker stats ash-nlp --no-stream
free -h
df -h

# Configuration
docker exec ash-nlp env | grep NLP_
```

### Support Channels

**Discord**: [#ash-support](https://discord.gg/alphabetcartel)  
**GitHub Issues**: [Report bugs](https://github.com/the-alphabet-cartel/ash-nlp/issues)  
**Documentation**: [API Guide](./tech/api_v3_0.md)  

### Issue Template

```markdown
**Issue Description**:
Brief description of the problem

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happens

**Environment**:
- OS: [e.g., Ubuntu 22.04]
- Docker Version: [e.g., 24.0.0]
- Hardware: [e.g., RTX 3060, 64GB RAM]

**Configuration**:
```bash
# Relevant environment variables
NLP_ENSEMBLE_MODE=weighted
NLP_DEVICE=auto
# etc.
```

**Logs**:
```
# Relevant log excerpts
[paste logs here]
```

**Steps to Reproduce**:
1. Step one
2. Step two
3. etc.
```

---

## 🎯 Prevention Best Practices

### Regular Maintenance

```bash
# Weekly health check
curl http://localhost:8881/health
curl http://localhost:8881/stats

# Monthly cleanup
docker system prune
docker exec ash-nlp rm -rf /app/logs/*.old

# Quarterly updates
git pull origin Organic-Learning
docker-compose build ash-nlp
```

### Configuration Management

```bash
# Always backup configuration before changes
cp .env .env.backup.$(date +%Y%m%d)

# Test configuration changes on staging first
docker-compose -f docker-compose.test.yml up ash-nlp

# Document all configuration changes
echo "$(date): Changed NLP_BATCH_SIZE to 48" >> config_changes.log
```

### Monitoring Setup

```bash
# Set up automated monitoring
crontab -e

# Add these entries:
# Check health every 5 minutes
*/5 * * * * /path/to/health_monitor.sh >> /var/log/ash-nlp-health.log

# Performance check every hour
0 * * * * /path/to/performance_monitor.sh >> /var/log/ash-nlp-performance.log

# Daily log rotation
0 0 * * * docker exec ash-nlp logrotate /etc/logrotate.conf
```

---

**🏳️‍🌈 Remember: Every challenge makes the system stronger. Your troubleshooting helps improve the service for all LGBTQIA+ communities.**

*This troubleshooting guide is continuously updated based on community feedback and real-world deployment experiences.*