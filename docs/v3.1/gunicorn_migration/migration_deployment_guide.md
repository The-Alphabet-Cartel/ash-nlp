# Ash-NLP Gunicorn Migration Deployment Guide

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-3e-8-1
**LAST MODIFIED**: 2025-08-24
**PHASE**: 3e
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

## 🚀 **Deployment Steps**

### **Step 1: Pre-Migration Backup**
```bash
# Backup current main.py
cp main.py main_uvicorn_backup.py
echo "✅ Original main.py backed up to main_uvicorn_backup.py"
```

### **Step 2: Deploy New Configuration Files**
1. **Add gunicorn_config.py** to project root
2. **Add dev_server.py** to project root  
3. **Replace main.py** with gunicorn-compatible version
4. **Update Dockerfile** with gunicorn CMD
5. **Update docker-compose.yml** (if used)

### **Step 3: Test Locally (Recommended)**
```bash
# Test module-level initialization works
python -c "import main; print('✅ Module import successful')"

# Test development server
python dev_server.py
# Should start on localhost:8881 with single worker

# Test gunicorn directly (if not using Docker)
gunicorn -c gunicorn_config.py main:app
# Should start with 5 workers
```

### **Step 4: Docker Deployment**
```bash
# Stop current container
docker stop ash-nlp

# Rebuild with new configuration
docker build -t ash-nlp:gunicorn .

# Start with gunicorn
docker run -d --name ash-nlp-gunicorn \
  -p 8881:8881 \
  --shm-size=1g \
  --memory=20g \
  --cpus=6 \
  ash-nlp:gunicorn

# Or use docker-compose
docker-compose up -d --build
```

### **Step 5: Verify Deployment**
```bash
# Check container logs for startup sequence
docker logs ash-nlp-gunicorn

# Look for these success indicators:
# ✅ "Gunicorn master starting"
# ✅ "Model preloading completed"
# ✅ "Worker X ready for crisis detection" (5 workers)
# ✅ "Ash-NLP ready with 5 workers"
```

### **Step 6: Test Functionality**
```bash
# Health check
curl http://localhost:8881/health

# Crisis analysis test
curl -X POST http://localhost:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help", "user_id": "test"}'

# Admin status
curl http://localhost:8881/admin/status
```

## 🔍 **Monitoring and Validation**

### **Memory Usage Monitoring**
```bash
# Check total container memory usage
docker stats ash-nlp-gunicorn

# Expected memory usage:
# - Master process: ~2GB (preloaded models)
# - Worker processes: ~2GB each (5 workers = ~10GB)
# - Total: ~12-15GB (well within 20GB limit)
```

### **Performance Testing**
```bash
# Concurrent request testing
for i in {1..10}; do
  curl -X POST http://localhost:8881/analyze \
    -H "Content-Type: application/json" \
    -d '{"message": "Test message '$i'", "user_id": "test'$i'"}' &
done
wait

# Monitor response times and worker distribution
```

### **Log Monitoring**
```bash
# Follow startup logs
docker logs -f ash-nlp-gunicorn

# Key success patterns to look for:
# - All 17 managers initialize successfully
# - Model preloading completes
# - All 5 workers start successfully
# - No error messages during initialization
```

## 🔧 **Troubleshooting**

### **If Initialization Fails:**
```bash
# Rollback to uvicorn version
cp main_uvicorn_backup.py main.py

# Restart with original configuration
docker build -t ash-nlp:rollback .
docker run -d --name ash-nlp-rollback ash-nlp:rollback
```

### **If Memory Issues Occur:**
```bash
# Reduce worker count in gunicorn_config.py
workers = 3  # Instead of 5

# Or set environment variable
docker run -e GUNICORN_WORKERS=3 ...
```

### **If Model Preloading Fails:**
```bash
# Check for model preloading errors in logs
docker logs ash-nlp-gunicorn | grep -i "preload\|model"

# Models will load on-demand if preload fails (slower but functional)
```

## 📊 **Expected Performance Improvements**

### **Concurrent Request Handling:**
- **Before:** 1 request at a time (single worker)
- **After:** Up to 5 concurrent requests (5 workers)
- **Expected:** 3-5x throughput improvement

### **Memory Efficiency:**
- **Without preload_app:** 5 × 8GB = 40GB (would exceed system RAM)
- **With preload_app:** ~12-15GB total (efficient sharing)
- **Memory saving:** ~25-28GB through shared model memory

### **Response Time:**
- **Cold start:** Similar (~8-10 seconds for first request per worker)
- **Warm requests:** Improved due to worker distribution
- **Concurrent load:** Much better handling of simultaneous requests

## 🎯 **Success Criteria Checklist**

- [ ] All 17 managers initialize successfully
- [ ] 5 gunicorn workers start and remain healthy  
- [ ] Model memory sharing works (total RAM usage < 20GB)
- [ ] Health endpoint responds correctly
- [ ] Crisis analysis endpoint works correctly
- [ ] Startup logging sequence preserved
- [ ] No critical errors in logs
- [ ] Concurrent requests handled properly

## 🏳️‍🌈 **Community Impact**

This migration enables:
- **Higher capacity** crisis detection for The Alphabet Cartel community
- **Better resilience** through worker redundancy
- **Improved response times** during high usage periods
- **Production-ready stability** for critical mental health support

## 📞 **Rollback Instructions**

If any issues occur:
```bash
# Quick rollback
docker stop ash-nlp-gunicorn
cp main_uvicorn_backup.py main.py
docker build -t ash-nlp:rollback .
docker run -d --name ash-nlp-rollback ash-nlp:rollback

# Verify rollback works
curl http://localhost:8881/health
```

---

**Remember:** This migration is designed to improve the system's ability to provide life-saving mental health support to the LGBTQIA+ community through better scalability and reliability.