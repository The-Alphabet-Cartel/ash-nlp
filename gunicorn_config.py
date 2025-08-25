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
FILE VERSION: v3.1-gunicorn-1-2
LAST MODIFIED: 2025-08-24
PHASE: Gunicorn Migration - Production Multi-Worker Setup with CUDA Transfer
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Enable multi-worker production deployment while preserving startup logging
STRATEGY: preload_app=True for model sharing, CPU preload + worker CUDA transfer
"""

import os
from pathlib import Path

# ============================================================================
# SERVER CONFIGURATION - INTEGRATED WITH ASH-NLP ENVIRONMENT VARIABLES
# ============================================================================

# Network Configuration - Uses existing NLP environment variables
bind = f"{os.getenv('NLP_SERVER_HOST', '0.0.0.0')}:{os.getenv('GLOBAL_NLP_API_PORT', '8881')}"
backlog = 2048  # Connection backlog

# Worker Configuration - Uses existing performance environment variables
workers = int(os.getenv('NLP_PERFORMANCE_WORKERS', '3'))  # Default 3 workers for memory optimization
worker_class = "uvicorn.workers.UvicornWorker"  # ASGI support for FastAPI
worker_connections = int(os.getenv('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', '1000'))
max_requests = int(os.getenv('NLP_GUNICORN_MAX_REQUESTS', '1000'))  # Uses gunicorn-specific override
max_requests_jitter = 100  # Add randomness to prevent thundering herd

# ============================================================================
# MEMORY OPTIMIZATION STRATEGY
# ============================================================================

# CRITICAL: Model Memory Sharing Strategy
preload_app = True  # Load models once in master, share via copy-on-write
                   # Memory benefit: ~15GB total vs ~24GB (3x8GB) without preload

# Process Management
proc_name = "ash-nlp-crisis-detection"  # Process name for monitoring
user = None   # Keep as current Docker user
group = None  # Keep as current Docker group

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

# Timeouts - Uses existing performance environment variables  
timeout = int(os.getenv('NLP_PERFORMANCE_WORKER_TIMEOUT', '120'))  # Worker timeout from .env.template (was 60)
graceful_timeout = int(os.getenv('NLP_GUNICORN_GRACEFUL_TIMEOUT', '30'))  # Graceful shutdown time
keepalive = int(os.getenv('NLP_GUNICORN_KEEPALIVE', '2'))  # Keep-alive connections

# Performance Optimizations - Enhanced with environment variable integration
worker_tmp_dir = os.getenv('NLP_GUNICORN_WORKER_TMP_DIR', '/dev/shm')  # Use shared memory for performance
                             # Requires Docker --tmpfs /dev/shm:rw,noexec,nosuid,size=1g

# Request Timeout Integration - Uses global timeout setting
worker_timeout = int(os.getenv('GLOBAL_REQUEST_TIMEOUT', '30'))  # Global request timeout

# ============================================================================
# LOGGING INTEGRATION - USES ASH-NLP ENVIRONMENT VARIABLES
# ============================================================================

# Logging Configuration - Integrated with existing logging system
accesslog = "-" if os.getenv('GLOBAL_LOGGING_ENABLE_CONSOLE', 'true').lower() == 'true' else None
errorlog = "-"   # stderr - integrates with Docker logging  
loglevel = os.getenv('GLOBAL_LOG_LEVEL', 'info').lower()  # Uses global log level
capture_output = True  # Capture stdout/stderr from workers

# Disable gunicorn's default access logging (we have our own)
disable_redirect_access_to_syslog = True

# ============================================================================
# LIFECYCLE HOOKS - PRESERVE STARTUP LOGGING SEQUENCE
# ============================================================================

def on_starting(server):
    """Called just before the master process is initialized"""
    print("🚀 Gunicorn master starting - Ash-NLP Crisis Detection System initializing...")
    print(f"🏳️‍🌈 Serving The Alphabet Cartel LGBTQIA+ Community")
    print(f"⚙️ Configuration: {server.cfg.workers} workers, preload_app={server.cfg.preload_app}")

def when_ready(server):
    """Called just after the server is started"""
    print(f"✅ Ash-NLP ready with {server.cfg.workers} workers - Community protection active")
    print(f"🌐 Listening on: {server.cfg.bind}")
    print(f"🧠 Model memory sharing: {'ENABLED' if server.cfg.preload_app else 'DISABLED'}")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT"""
    print(f"🛑 Worker {worker.pid} shutting down gracefully")

def pre_fork(server, worker):
    """Called just before a worker is forked"""
    print(f"🔄 Forking worker {worker.age} (PID will be assigned)")

def post_fork(server, worker):
    """Called just after a worker has been forked"""
    print(f"👥 Worker {worker.pid} ready for crisis detection")
    print(f"🔧 Worker {worker.pid} will transfer models to CUDA on first request")

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal"""
    print(f"⚠️ Worker {worker.pid} aborted - possible memory/timeout issue")
    print(f"⚠️ Worker exit code: {worker.tmp.returncode}")
    print(f"💡 Check memory usage and CUDA transfer performance")

def pre_request(worker, req):
    """Called just before a worker processes the request (optional monitoring)"""
    # Uncomment for request-level monitoring
    # worker.log.info(f"Processing: {req.method} {req.path}")
    pass

def post_request(worker, req, environ, resp):
    """Called after a worker processes the request (optional monitoring)"""
    # Uncomment for detailed response monitoring  
    # worker.log.info(f"Completed: {req.method} {req.path} - Status: {resp.status}")
    pass

# ============================================================================
# ENVIRONMENT VARIABLE INTEGRATION - ASH-NLP COMPATIBLE
# ============================================================================

# Load environment variables with defaults from Ash-NLP .env.template
# This ensures consistency with the existing configuration system

# Core Server Configuration
bind = f"{os.getenv('NLP_SERVER_HOST', '0.0.0.0')}:{os.getenv('GLOBAL_NLP_API_PORT', '8881')}"
workers = int(os.getenv('NLP_PERFORMANCE_WORKERS', '3'))  # Changed default to 3 for memory optimization
timeout = int(os.getenv('NLP_PERFORMANCE_WORKER_TIMEOUT', '120'))  # Extended for model loading
worker_connections = int(os.getenv('NLP_PERFORMANCE_MAX_CONCURRENT_REQUESTS', '20'))

# Gunicorn-specific overrides (for fine-tuning beyond standard NLP variables)
max_requests = int(os.getenv('NLP_GUNICORN_MAX_REQUESTS', '1000'))
worker_tmp_dir = os.getenv('NLP_GUNICORN_WORKER_TMP_DIR', '/dev/shm')

# Rate Limiting Integration - Uses existing rate limiting configuration
max_requests = min(max_requests, int(os.getenv('NLP_PERFORMANCE_RATE_LIMIT_PER_HOUR', '2000')))

print(f"📋 Gunicorn Configuration Loaded from Environment:")
print(f"   Bind Address: {bind}")
print(f"   Workers: {workers}")
print(f"   Timeout: {timeout}s") 
print(f"   Worker Connections: {worker_connections}")
print(f"   Preload App: {preload_app}")
print(f"   Worker Class: {worker_class}")
print(f"   Log Level: {loglevel}")
print(f"   Max Requests: {max_requests}")
print(f"   Worker Tmp Dir: {worker_tmp_dir}")
print(f"💾 Expected memory usage: ~{8 + (workers * 3)}GB (CPU preload + {workers} CUDA workers)")
print(f"🔧 CUDA transfer strategy: CPU preload → Worker CUDA transfer on first request")