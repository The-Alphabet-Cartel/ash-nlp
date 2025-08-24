# Ash-NLP Gunicorn Migration Implementation Plan

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-3e-8-1
**LAST MODIFIED**: 2025-08-24
**PHASE**: 3e
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

## Project Context
- **System**: Ash-NLP Crisis Detection Backend for The Alphabet Cartel Discord Community
- **Current State**: Single worker uvicorn with direct app object passing
- **Goal**: Multi-worker production deployment with gunicorn while preserving startup logging sequence
- **Hardware**: AMD Ryzen 7 5800x (8C/16T), NVIDIA RTX 3060 12GB, 64GB RAM

## Phase 1: Pre-Migration Setup

### 1.1 Requirements Update
```bash
# Add to requirements.txt
gunicorn>=21.2.0
```

### 1.2 Configuration File Creation
Create `gunicorn_config.py` in project root:
```python
# gunicorn_config.py
import os
from pathlib import Path

# Server Configuration
bind = "0.0.0.0:8881"  # Match current uvicorn config
workers = 4  # Start with 4, tune based on performance
worker_class = "uvicorn.workers.UvicornWorker"  # ASGI support for FastAPI
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Process Management  
preload_app = True  # Critical for model sharing across workers
proc_name = "ash-nlp-crisis-detection"
user = None  # Keep as current user in Docker
group = None

# Timeouts (Important for model loading)
timeout = 120  # Increased for NLP model initialization
graceful_timeout = 30
keepalive = 2

# Logging Integration
accesslog = "-"  # stdout
errorlog = "-"   # stderr  
loglevel = "info"
capture_output = True

# Performance Tuning
worker_tmp_dir = "/dev/shm"  # Use shared memory for better performance

# Lifecycle Hooks
def on_starting(server):
    print("🚀 Gunicorn master starting - Crisis Detection System initializing...")

def when_ready(server):
    print(f"✅ Ash-NLP ready with {server.num_workers} workers - Community protection active")

def worker_int(worker):
    print(f"🛑 Worker {worker.pid} shutting down gracefully")

def pre_fork(server, worker):
    print(f"🔄 Forking worker {worker.age}")

def post_fork(server, worker):
    print(f"👥 Worker {worker.pid} ready for crisis detection")
```

## Phase 2: Code Structure Changes

### 2.1 main.py Restructure
**Current Issue**: `if __name__ == "__main__"` block prevents gunicorn import
**Solution**: Move initialization to module level for preload_app compatibility

#### Key Changes:
1. **Remove** `if __name__ == "__main__"` block
2. **Move** all initialization to module level
3. **Create** separate startup script for development
4. **Preserve** sequential logging exactly as designed

#### File Structure After Migration:
```
ash-nlp/
├── main.py                 # Gunicorn-compatible app with module-level init
├── gunicorn_config.py     # Production server configuration  
├── dev_server.py          # Development server (preserves current behavior)
├── requirements.txt       # Updated with gunicorn
└── config/               # Existing config directory
```

### 2.2 main.py Transformation
```python
# main.py - Gunicorn Compatible Version

# All existing imports remain the same
[... existing imports ...]

# Module-level initialization (replaces if __name__ == "__main__")
print("🎉 Starting Ash-NLP Crisis Detection Service v3.1d Step 9")
print("🏳️‍🌈 Serving The Alphabet Cartel LGBTQIA+ Community") 
[... all existing startup prints ...]

# Initialize unified configuration manager
unified_config = create_unified_config_manager()

# Setup unified logging  
setup_unified_logging(unified_config)

# All your existing sequential logging
logger = logging.getLogger(__name__)
logger.info("=" * 70)
logger.info("🚀 ASH-NLP SERVICE STARTUP (Production Mode)")
[... all existing initialization logging ...]

# Create fully initialized app at module level
app = create_fastapi_app()

logger.info("✅ Application ready for gunicorn workers")
```

### 2.3 Development Server Creation
```python
# dev_server.py - Preserves current development workflow
import uvicorn
from main import app, unified_config

if __name__ == "__main__":
    # Get config for development
    host = unified_config.get_config_section('server_config', 'server_configuration.network_settings.host', '0.0.0.0')
    port = unified_config.get_config_section('server_config', 'server_configuration.network_settings.port', 8881)
    
    # Development mode - single worker, reload enabled
    uvicorn.run(
        "main:app",
        host=host, 
        port=port,
        workers=1,
        reload=True,
        log_config=None,
        access_log=False
    )
```

## Phase 3: Docker Integration

### 3.1 Dockerfile Updates
```dockerfile
# Add gunicorn installation if not using requirements.txt method
# Update CMD instruction:

# Production
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:app"]

# Development (alternative)  
# CMD ["python", "dev_server.py"]
```

### 3.2 Docker Compose Considerations
```yaml
# Update docker-compose.yml if applicable
services:
  ash-nlp:
    # ... existing config ...
    command: ["gunicorn", "-c", "gunicorn_config.py", "main:app"]
    environment:
      # Tune workers based on container resources
      - GUNICORN_WORKERS=4
```

## Phase 4: Memory and Performance Optimization

### 4.1 Model Loading Strategy
**Challenge**: Multiple workers loading same models = memory explosion
**Solution**: Leverage preload_app + copy-on-write memory

#### Memory Estimates:
- Current single worker: ~8GB model memory
- 4 workers without preload: ~32GB model memory  
- 4 workers with preload: ~12GB model memory (shared + worker overhead)

### 4.2 Worker Scaling Guidelines
```
CPU Cores: 8 (Ryzen 7 5800x)
Recommended Workers: 4-6 (leave cores for model inference)
Memory per worker: ~2GB base + shared model memory
```

### 4.3 Performance Monitoring Setup
```python
# Add to gunicorn_config.py for monitoring
def worker_abort(worker):
    print(f"⚠️ Worker {worker.pid} aborted - possible memory/timeout issue")

def pre_request(worker, req):
    # Optional: Log high-latency requests
    worker.log.info(f"Processing: {req.method} {req.path}")
```

## Phase 5: Testing Strategy

### 5.1 Load Testing Plan
1. **Single Worker Baseline**: Measure current performance
2. **Multi-Worker Comparison**: Test with 2, 4, 6 workers
3. **Memory Usage Monitoring**: Ensure model sharing works
4. **Crisis Detection Accuracy**: Verify no accuracy regression
5. **Concurrent Request Handling**: Test Discord message bursts

### 5.2 Rollback Plan
Keep current main.py as main_uvicorn_backup.py for quick rollback if issues occur.

## Phase 6: Deployment Steps

### 6.1 Pre-Deployment Checklist
- [ ] Backup current main.py
- [ ] Test gunicorn config locally  
- [ ] Verify all startup logs appear correctly
- [ ] Confirm model memory usage is acceptable
- [ ] Test graceful shutdown behavior

### 6.2 Migration Sequence
1. Update requirements.txt
2. Add gunicorn_config.py
3. Create dev_server.py  
4. Transform main.py structure
5. Update Docker configuration
6. Deploy and monitor

## Phase 7: Post-Migration Validation

### 7.1 Verification Points
- [ ] All 17 managers initialize correctly
- [ ] Model preloading completes successfully  
- [ ] API endpoints respond correctly
- [ ] Crisis detection accuracy maintained
- [ ] Memory usage within acceptable limits
- [ ] Response times improved for concurrent requests

### 7.2 Performance Metrics to Track
- Request latency (p50, p95, p99)
- Memory usage per worker
- CPU utilization across cores
- Model inference throughput
- Concurrent request handling capacity

## Estimated Implementation Time
- **Planning and Setup**: 30 minutes
- **Code Changes**: 45 minutes  
- **Testing and Validation**: 60 minutes
- **Deployment**: 15 minutes
- **Total**: ~2.5 hours

## Risk Assessment
- **Low Risk**: Configuration and setup changes
- **Medium Risk**: Module-level initialization restructure  
- **High Risk**: Memory usage with multiple model instances
- **Mitigation**: Thorough testing of preload_app behavior

## Success Criteria
1. Startup logging sequence preserved and visible
2. All managers and models initialize correctly
3. Multiple workers handle concurrent requests
4. Memory usage remains reasonable (<20GB total)
5. Crisis detection performance maintained or improved