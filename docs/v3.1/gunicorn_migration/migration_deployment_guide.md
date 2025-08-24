# Ash-NLP Gunicorn Migration Deployment Guide

## 🚀 **Current Migration Status: CUDA Multiprocessing Solution**

### **Issue Encountered:**
During testing, encountered CUDA multiprocessing error: "Cannot re-initialize CUDA in forked subprocess." This prevents model preloading with CUDA across gunicorn workers.

### **Solution Implemented: CPU Preload + Worker CUDA Transfer**
- Master process preloads models on CPU (enables memory sharing)
- Workers transfer models to CUDA on first request (avoids CUDA context conflicts)
- Memory efficient: ~15-20GB total vs ~45GB without preloading
- Preserves warmup benefits while enabling multi-worker CUDA

### **Required Code Changes:**
1. **gunicorn_config.py**: Keep `preload_app = True`
2. **main.py**: Force CPU during model preloading
3. **ModelCoordinationManager**: Add worker-level CUDA transfer logic

### **Memory Analysis with Other Containers:**
- Current usage: 15GB
- Available: 49GB  
- With 5 workers (no preload): 50-65GB (EXCEEDS CAPACITY)
- With CPU preload + CUDA transfer: 20-25GB (SAFE)

---

## 🔧 **Implementation Steps for CPU Preload + CUDA Transfer**

### **Step 1: Update Model Preloading in main.py**
```python
# In main.py model preloading section
logger.info("🔧 Preloading models on CPU for memory sharing...")

# Force CPU for master process preloading (avoid CUDA context issues)
original_device = os.environ.get('NLP_HARDWARE_DEVICE', 'auto')
os.environ['NLP_HARDWARE_DEVICE'] = 'cpu'

try:
    # Preload models on CPU
    model_status = model_coordination.get_preload_status()
    if not model_status.get('preload_complete', False):
        models = model_coordination.get_model_definitions()
        for model_name, model_info in models.items():
            logger.info(f"🔄 Preloading model on CPU: {model_name}")
            model_coordination._get_cached_pipeline(model_name, model_info)
            
    logger.info("✅ CPU model preloading complete - workers will transfer to CUDA")
    
finally:
    # Restore original device setting for workers
    os.environ['NLP_HARDWARE_DEVICE'] = original_device
```

### **Step 2: Add Worker CUDA Transfer Logic**
Modify ModelCoordinationManager to transfer CPU models to CUDA on first worker use:

```python
def _get_worker_cuda_pipeline(self, model_name, model_info):
    """Transfer CPU-preloaded model to CUDA for worker use"""
    if hasattr(self, '_worker_cuda_cache'):
        if model_name in self._worker_cuda_cache:
            return self._worker_cuda_cache[model_name]
    else:
        self._worker_cuda_cache = {}
    
    # Get CPU model from master process cache
    cpu_pipeline = self._model_cache.get(model_name)
    
    if cpu_pipeline and self._should_use_cuda():
        # Transfer to CUDA
        cuda_pipeline = cpu_pipeline.to('cuda')
        self._worker_cuda_cache[model_name] = cuda_pipeline
        return cuda_pipeline
    
    return cpu_pipeline
```

### **Step 3: Environment Configuration**
Update .env.template:
```bash
NLP_GUNICORN_WORKERS=5
NLP_GUNICORN_PRELOAD_APP=true
NLP_HARDWARE_DEVICE=auto  # Workers will use CUDA, master uses CPU for preload
```

---

## 🚀 **Deployment Steps** (Updated)

### **Step 1-6: [Previous steps remain the same]**

### **Step 7: Monitor Memory and CUDA Usage**
```bash
# Memory monitoring
docker stats ash-nlp-gunicorn

# Expected memory pattern:
# - Initial spike during CPU preloading (~12GB)
# - Stable usage after worker startup (~15-20GB)
# - First requests per worker show brief CUDA transfer delay

# CUDA monitoring
nvidia-smi
# Should show 5 worker processes using GPU after warmup
```

---

## 🎯 **Expected Performance Characteristics**

### **Memory Usage:**
- Master process: ~8-12GB (CPU-loaded models)
- Workers: ~2-3GB each (CUDA contexts + overhead)
- Total: ~15-20GB (within 49GB available capacity)

### **Warmup Behavior:**
- First request per worker: 2-3 second delay (CPU→CUDA transfer)
- Subsequent requests: Full CUDA performance
- Much faster than cold model loading (8-10 seconds)

### **Concurrent Performance:**
- 5 workers handling simultaneous CUDA inference
- Memory efficient through CPU model sharing
- No CUDA context conflicts

---

## ⚠️ **Current Status: IMPLEMENTATION REQUIRED**

**Next Steps for Completion:**
1. Implement CPU preload + CUDA transfer in ModelCoordinationManager
2. Test memory usage patterns
3. Validate CUDA transfer performance
4. Deploy and monitor production behavior

**Conversation Continuation:**
Due to conversation length limits, continue implementation in next session with focus on ModelCoordinationManager modifications for worker CUDA transfer logic.

---

## 🏳️‍🌈 **Community Impact**

This solution enables production-ready multi-worker crisis detection while respecting hardware constraints, ensuring reliable mental health support for The Alphabet Cartel LGBTQIA+ community with optimal resource utilization.

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