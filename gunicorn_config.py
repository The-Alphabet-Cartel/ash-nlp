# gunicorn_config.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Gunicorn Production Server Configuration for Multi-Worker Deployment
---
FILE VERSION: v3.1-gunicorn-1-1
LAST MODIFIED: 2025-08-24
PHASE: Gunicorn Migration - Production Multi-Worker Setup
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Enable multi-worker production deployment while preserving startup logging
STRATEGY: preload_app=True for model sharing, optimized for 64GB RAM + RTX 3060

Optimized for:
- AMD Ryzen 7 5800x (8 cores/16 threads) 
- NVIDIA RTX 3060 (12GB VRAM)
- 64GB RAM
- 3 worker processes
"""

import os
from pathlib import Path

# ========================================================================
# SERVER CONFIGURATION
# ========================================================================

bind = "0.0.0.0:8881"  # Match current uvicorn config
workers = 3  # Reduced from 5 for better memory management
worker_class = "uvicorn.workers.UvicornWorker"  # ASGI support for FastAPI
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# ========================================================================
# PROCESS MANAGEMENT (CRITICAL FOR MODEL SHARING)
# ========================================================================

preload_app = True  # CRITICAL: Enables CPU model preloading and memory sharing
proc_name = "ash-nlp-crisis-detection"
user = None  # Keep as current user in Docker
group = None

# ========================================================================
# TIMEOUTS (IMPORTANT FOR MODEL LOADING AND CUDA TRANSFER)
# ========================================================================

timeout = 120  # Increased for NLP model initialization and CUDA transfers
graceful_timeout = 30
keepalive = 2

# ========================================================================
# LOGGING INTEGRATION
# ========================================================================

accesslog = "-"  # stdout
errorlog = "-"   # stderr  
loglevel = "info"
capture_output = True

# ========================================================================
# PERFORMANCE TUNING
# ========================================================================

worker_tmp_dir = "/dev/shm"  # Use shared memory for better performance

# ========================================================================
# LIFECYCLE HOOKS FOR MONITORING
# ========================================================================

def on_starting(server):
    """Called when the master process is initialized"""
    print("🚀 Ash-NLP Gunicorn Master Starting - Crisis Detection System initializing...")
    print(f"🔧 Configuration: {server.num_workers} workers, preload_app={preload_app}")

def when_ready(server):
    """Called when the server is ready to serve requests"""
    print(f"✅ Ash-NLP ready with {server.num_workers} workers - Community protection active!")
    print("🏳️‍🌈 Serving The Alphabet Cartel LGBTQIA+ Community")

def worker_int(worker):
    """Called when a worker receives a SIGINT signal"""
    print(f"🛑 Worker {worker.pid} shutting down gracefully...")

def pre_fork(server, worker):
    """Called just before a worker process is forked"""
    print(f"🔄 Forking worker {worker.age} (PID will be assigned after fork)")

def post_fork(server, worker):
    """Called after a worker has been forked"""
    print(f"👥 Worker {worker.pid} ready for crisis detection")
    print(f"🔧 Worker {worker.pid} will transfer models to CUDA on first request")

def worker_abort(worker):
    """Called when a worker process is aborted"""
    print(f"⚠️ Worker {worker.pid} aborted - possible memory/timeout issue")
    print("💡 Check memory usage and model loading performance")

def on_exit(server):
    """Called when the master process exits"""
    print("👋 Ash-NLP shutting down - Crisis detection service stopping")

# ========================================================================
# MONITORING AND DEBUG HOOKS
# ========================================================================

def pre_request(worker, req):
    """Optional: Log high-latency requests"""
    # Uncomment for debugging request patterns
    # worker.log.info(f"Processing: {req.method} {req.path}")
    pass

def post_request(worker, req, environ, resp):
    """Optional: Log response metrics"""
    # Uncomment for debugging response patterns  
    # worker.log.info(f"Completed: {req.method} {req.path} - Status: {resp.status}")
    pass

# ========================================================================
# MEMORY AND RESOURCE OPTIMIZATION
# ========================================================================

# Environment-based worker scaling (override via Docker environment)
workers = int(os.environ.get('NLP_GUNICORN_WORKERS', workers))

# Validate worker count for memory constraints
if workers > 5:
    print(f"⚠️ Warning: {workers} workers may exceed memory capacity. Recommended: ≤5")

print(f"🔧 Gunicorn Config Loaded: {workers} workers, preload_app={preload_app}")
print(f"💾 Expected memory usage: ~{8 + (workers * 3)}GB (CPU preload + {workers} CUDA workers)")