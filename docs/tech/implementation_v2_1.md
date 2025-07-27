# 🔧 Implementation Guide - Ash NLP Server v2.1

> *Complete technical setup and deployment guide for the enhanced learning-enabled AI crisis detection system*

[![Implementation Guide](https://img.shields.io/badge/guide-implementation-orange)](https://github.com/the-alphabet-cartel/ash-nlp)
[![Version](https://img.shields.io/badge/version-2.1-blue)](https://github.com/the-alphabet-cartel/ash-nlp/releases/tag/v2.1)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com/)

---

## 📋 Table of Contents

1. [System Requirements](#-system-requirements)
2. [Environment Setup](#-environment-setup)
3. [Installation Methods](#-installation-methods)
4. [Configuration](#-configuration)
5. [Deployment Options](#-deployment-options)
6. [Integration Setup](#-integration-setup)
7. [Performance Optimization](#-performance-optimization)
8. [Monitoring & Maintenance](#-monitoring--maintenance)
9. [Troubleshooting](#-troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements
```yaml
Hardware:
  CPU: 4 cores, 2.5GHz
  RAM: 8GB
  Storage: 20GB free space
  Network: 100Mbps local network

Software:
  OS: Windows 11, Linux (Ubuntu 20.04+), macOS 11+
  Docker: v20.10+
  Python: 3.9+ (if running native)
  Git: v2.30+
```

### Recommended (Your Setup) ✅
```yaml
Hardware:
  CPU: AMD Ryzen 7 7700X (8 cores, 4.5GHz)
  GPU: NVIDIA RTX 3050 (8GB VRAM) 
  RAM: 64GB DDR5
  Storage: NVMe SSD (1TB+)
  Network: Gigabit local network

Software:
  OS: Windows 11 Pro
  Docker Desktop: Latest
  GPU Drivers: NVIDIA 535+
  CUDA: 11.8+ (for GPU acceleration)
```

### Network Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ash Discord   │    │   NLP Server    │    │   Analytics     │
│      Bot        │───▶│   (This Setup)  │───▶│   Dashboard     │
│  10.20.30.253   │    │   10.20.30.16   │    │  10.20.30.16    │
│     :8882       │    │     :8881       │    │     :8883       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Testing Suite  │
                       │  10.20.30.16    │
                       │     :8884       │
                       └─────────────────┘
```

---

## 🛠️ Environment Setup

### 1. Windows 11 Setup (Your Environment)

**Install Docker Desktop:**
```powershell
# Download and install Docker Desktop from docker.com
# Ensure WSL2 backend is enabled
# Verify installation:
docker --version
docker-compose --version
```

**Install Git for Windows:**
```powershell
# Download from git-scm.com
# Verify installation:
git --version
```

**Optional: NVIDIA Container Toolkit (for GPU acceleration):**
```powershell
# Follow NVIDIA Container Toolkit installation guide
# This enables GPU passthrough to Docker containers
```

### 2. Development Tools Setup

**Using Atom Editor (Your Preference):**
```powershell
# Recommended Atom packages for this project:
apm install language-docker
apm install language-python
apm install language-json
apm install file-icons
apm install minimap
apm install git-plus
```

**GitHub Desktop Integration:**
```powershell
# Clone repository using GitHub Desktop
# Repository: https://github.com/the-alphabet-cartel/ash-nlp
# Clone to: C:\Projects\ash-nlp
```

---

## 📦 Installation Methods

### Option 1: Docker Deployment (Recommended)

**Quick Production Setup:**
```powershell
# Navigate to project directory
cd C:\Projects\ash-nlp

# Copy environment template
copy .env.template .env

# Edit .env file with your settings (see Configuration section)
# Use Atom: atom .env

# Deploy using Docker Compose
docker-compose up -d

# Verify deployment
curl http://10.20.30.16:8881/health
```

**Development Setup with Hot Reload:**
```powershell
# Use development Docker Compose
docker-compose -f docker-compose.dev.yml up -d

# View logs in real-time
docker-compose logs -f ash-nlp
```

### Option 2: Native Python Installation

**Create Virtual Environment:**
```powershell
# Navigate to project directory
cd C:\Projects\ash-nlp

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install PyTorch with CUDA support (for RTX 3050)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Run Development Server:**
```powershell
# Set environment variables
copy .env.template .env
# Edit .env with your settings

# Start NLP server
python nlp_main.py

# Server will be available at http://10.20.30.16:8881
```

---

## ⚙️ Configuration

### Environment Variables (.env file)

**Core Configuration:**
```bash
# Server Configuration
NLP_SERVICE_HOST=10.20.30.16
NLP_SERVICE_PORT=8881
PYTHONUNBUFFERED=1

# AI Model Configuration
DEPRESSION_MODEL=rafalposwiata/deproberta-large-depression
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL_CACHE_DIR=./models/cache

# Hardware Optimization (RTX 3050 + Ryzen 7 7700X)
DEVICE=auto                    # Auto-detect GPU/CPU
MODEL_PRECISION=float16        # GPU memory optimization
MAX_BATCH_SIZE=32             # Optimized for RTX 3050
INFERENCE_THREADS=8           # Ryzen 7 7700X cores
MAX_CONCURRENT_REQUESTS=20    # Handle multiple requests

# Learning System Configuration
ENABLE_LEARNING_SYSTEM=true
LEARNING_RATE=0.1
MAX_LEARNING_ADJUSTMENTS_PER_DAY=100
LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json
MIN_CONFIDENCE_ADJUSTMENT=0.05
MAX_CONFIDENCE_ADJUSTMENT=0.30

# Crisis Detection Thresholds
CRISIS_HIGH_THRESHOLD=0.50
CRISIS_MEDIUM_THRESHOLD=0.22
CRISIS_LOW_THRESHOLD=0.12

# Performance Tuning
REQUEST_TIMEOUT=30
UVICORN_WORKERS=1
RELOAD_ON_CHANGES=false

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/nlp_service.log
ENABLE_DEBUG_LOGGING=false

# Optional: Hugging Face Token
HUGGINGFACE_HUB_TOKEN=your_token_here

# Optional: External Integrations
ENABLE_ANALYTICS_EXPORT=true
ANALYTICS_WEBHOOK_URL=http://10.20.30.16:8883/webhook
```

**Security Configuration:**
```bash
# API Security (optional)
API_KEY_ENABLED=false
API_KEY=your_secure_api_key_here

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10
```

### Docker Compose Configuration

**Production docker-compose.yml:**
```yaml
version: '3.8'

services:
  ash-nlp:
    image: ghcr.io/the-alphabet-cartel/ash-nlp:v2.1
    container_name: ash_nlp_server
    restart: unless-stopped
    
    networks:
      - ash-network
    
    ports:
      - "${NLP_SERVICE_PORT:-8881}:${NLP_SERVICE_PORT:-8881}"
    
    environment:
      # Load from .env file
      - PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}
      - NLP_SERVICE_HOST=${NLP_SERVICE_HOST:-0.0.0.0}
      - NLP_SERVICE_PORT=${NLP_SERVICE_PORT:-8881}
      - DEVICE=${DEVICE:-auto}
      - ENABLE_LEARNING_SYSTEM=${ENABLE_LEARNING_SYSTEM:-true}
    
    volumes:
      # Persistent storage
      - ./models:/app/models/cache:rw
      - ./learning_data:/app/learning_data:rw
      - ./logs:/app/logs:rw
      - ./data:/app/data:rw
    
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '6'
        reservations:
          memory: 2G
          cpus: '2'
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${NLP_SERVICE_PORT:-8881}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

networks:
  ash-network:
    external: true
```

**Development docker-compose.dev.yml:**
```yaml
version: '3.8'

services:
  ash-nlp-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    
    container_name: ash_nlp_dev
    restart: unless-stopped
    
    ports:
      - "8881:8881"
    
    environment:
      - PYTHONUNBUFFERED=1
      - RELOAD_ON_CHANGES=true
      - LOG_LEVEL=DEBUG
      - ENABLE_DEBUG_LOGGING=true
    
    volumes:
      # Mount source code for hot reload
      - .:/app:rw
      - ./models:/app/models/cache:rw
      - ./learning_data:/app/learning_data:rw
    
    command: ["python", "nlp_main.py", "--reload"]
```

---

## 🚀 Deployment Options

### Production Deployment

**1. Prepare Environment:**
```powershell
# Create project directory
mkdir C:\Projects\ash-nlp
cd C:\Projects\ash-nlp

# Clone repository (using GitHub Desktop or command line)
git clone https://github.com/the-alphabet-cartel/ash-nlp.git .

# Copy environment configuration
copy .env.template .env
```

**2. Configure Environment:**
```powershell
# Edit .env file with Atom
atom .env

# Ensure these critical settings are correct:
# NLP_SERVICE_HOST=10.20.30.16
# NLP_SERVICE_PORT=8881
# DEVICE=auto (for RTX 3050 auto-detection)
# ENABLE_LEARNING_SYSTEM=true
```

**3. Deploy with Docker:**
```powershell
# Create necessary directories
mkdir models, learning_data, logs, data

# Pull latest image
docker-compose pull

# Start services
docker-compose up -d

# Check deployment status
docker-compose ps
docker-compose logs ash-nlp
```

**4. Verify Deployment:**
```powershell
# Health check
curl http://10.20.30.16:8881/health

# Learning system status
curl http://10.20.30.16:8881/learning_statistics

# Test analysis endpoint
curl -X POST http://10.20.30.16:8881/analyze -H "Content-Type: application/json" -d "{\"message\": \"feeling really down today\"}"
```

### Staging/Development Deployment

**1. Development Environment:**
```powershell
# Use development compose file
docker-compose -f docker-compose.dev.yml up -d

# Enable hot reload for code changes
# Code changes will automatically restart the server
```

**2. Testing Integration:**
```powershell
# Test with ash-thrash testing suite
# (Assuming ash-thrash is also deployed on same server)
curl http://10.20.30.16:8884/test_nlp_integration
```

### GPU Optimization Setup

**Enable NVIDIA GPU Support:**
```powershell
# Verify GPU is available
nvidia-smi

# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# Update docker-compose.yml to include GPU support:
```

```yaml
services:
  ash-nlp:
    # ... other configuration
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## 🔗 Integration Setup

### Ash Bot Integration

**1. Configure Ash Bot Environment:**
```bash
# In Ash bot .env file, add:
NLP_SERVICE_HOST=10.20.30.16
NLP_SERVICE_PORT=8881
ENABLE_LEARNING_SYSTEM=true
NLP_TIMEOUT=30
```

**2. Update Ash Bot Configuration:**
```python
# In Ash bot configuration
NLP_CONFIG = {
    "base_url": "http://10.20.30.16:8881",
    "timeout": 30,
    "retry_attempts": 3,
    "fallback_enabled": True
}
```

**3. Test Integration:**
```powershell
# From Ash bot server (10.20.30.253)
curl http://10.20.30.16:8881/health

# Test analysis request
curl -X POST http://10.20.30.16:8881/analyze -H "Content-Type: application/json" -d "{\"message\": \"test message\", \"user_id\": \"123\", \"channel_id\": \"456\"}"
```

### Analytics Dashboard Integration

**1. Configure ash-dash:**
```bash
# In ash-dash .env file:
NLP_SERVER_URL=http://10.20.30.16:8881
ENABLE_NLP_ANALYTICS=true
NLP_METRICS_REFRESH=30  # seconds
```

**2. Setup Analytics Webhook:**
```bash
# In ash-nlp .env file:
ENABLE_ANALYTICS_EXPORT=true
ANALYTICS_WEBHOOK_URL=http://10.20.30.16:8883/webhook/nlp_metrics
```

### Testing Suite Integration

**1. Configure ash-thrash:**
```bash
# In ash-thrash .env file:
TARGET_NLP_SERVER=http://10.20.30.16:8881
ENABLE_NLP_TESTING=true
COMPREHENSIVE_TEST_ENABLED=true
```

**2. Run Integration Tests:**
```powershell
# Test NLP server from ash-thrash
curl http://10.20.30.16:8884/test_nlp_integration

# Run comprehensive test suite
curl -X POST http://10.20.30.16:8884/run_comprehensive_test
```

---

## ⚡ Performance Optimization

### Hardware-Specific Optimizations

**RTX 3050 GPU Optimization:**
```bash
# Environment variables for optimal GPU usage
DEVICE=cuda                    # Force GPU usage
MODEL_PRECISION=float16        # Reduce memory usage
MAX_BATCH_SIZE=16             # Prevent GPU memory overflow
CUDA_VISIBLE_DEVICES=0        # Use first GPU
```

**Ryzen 7 7700X CPU Optimization:**
```bash
# CPU-specific optimizations
INFERENCE_THREADS=8           # Match physical cores
OMP_NUM_THREADS=8            # OpenMP thread count
MKL_NUM_THREADS=8            # Intel MKL optimization
TORCH_NUM_THREADS=8          # PyTorch CPU threads
```

**Memory Optimization:**
```bash
# RAM usage optimization (64GB available)
MAX_CONCURRENT_REQUESTS=25   # Handle more concurrent requests
MODEL_CACHE_SIZE=4GB         # Cache multiple models
LEARNING_DATA_CACHE=1GB      # Cache learning patterns
```

### Application Performance Tuning

**FastAPI Configuration:**
```python
# In nlp_main.py
app = FastAPI(
    title="Ash NLP Server",
    version="2.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    # Performance optimizations
    generate_unique_id_function=generate_unique_id,
    lifespan=lifespan,
    middleware=[
        Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
        Middleware(GZipMiddleware, minimum_size=1000),
        Middleware(CORSMiddleware, 
                  allow_origins=["*"],
                  allow_methods=["*"],
                  allow_headers=["*"])
    ]
)
```

**Uvicorn Server Configuration:**
```bash
# Production server settings
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8881
UVICORN_WORKERS=1            # Single worker for GPU sharing
UVICORN_LOG_LEVEL=info
UVICORN_ACCESS_LOG=true
UVICORN_WORKER_CLASS=uvicorn.workers.UvicornWorker
```

### Model Loading Optimization

**Model Caching Strategy:**
```python
# Model loading configuration
MODEL_LOADING_CONFIG = {
    "local_files_only": False,    # Download if not cached
    "cache_dir": "./models/cache",
    "torch_dtype": torch.float16, # Memory optimization
    "device_map": "auto",         # Auto GPU/CPU allocation
    "low_cpu_mem_usage": True,    # Reduce CPU memory during loading
}
```

**Preload Models at Startup:**
```bash
# Environment variable to preload models
PRELOAD_MODELS=true
PRELOAD_TIMEOUT=300  # 5 minutes timeout for model loading
```

---

## 📊 Monitoring & Maintenance

### Health Monitoring Setup

**Health Check Endpoints:**
```bash
# Basic health check
curl http://10.20.30.16:8881/health

# Detailed system status
curl http://10.20.30.16:8881/system_status

# Learning system health
curl http://10.20.30.16:8881/learning_statistics

# Performance metrics
curl http://10.20.30.16:8881/performance_metrics
```

**Automated Monitoring Script:**
```powershell
# Create monitoring script: monitor_nlp.ps1
$healthUrl = "http://10.20.30.16:8881/health"
$logFile = "C:\Projects\ash-nlp\logs\health_monitor.log"

while ($true) {
    try {
        $response = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 30
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        if ($response.status -eq "healthy") {
            Write-Host "[$timestamp] NLP Server: Healthy"
        } else {
            Write-Host "[$timestamp] NLP Server: Warning - $($response.status)" -ForegroundColor Yellow
        }
    }
    catch {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] NLP Server: ERROR - $($_.Exception.Message)" -ForegroundColor Red
        Add-Content -Path $logFile -Value "[$timestamp] ERROR: $($_.Exception.Message)"
    }
    Start-Sleep -Seconds 60
}
```

**Schedule Monitoring:**
```powershell
# Create scheduled task for monitoring
schtasks /create /tn "Ash NLP Monitor" /tr "powershell.exe -File C:\Projects\ash-nlp\scripts\monitor_nlp.ps1" /sc minute /mo 5
```

### Log Management

**Log Configuration:**
```bash
# Logging setup in .env
LOG_LEVEL=INFO
LOG_FILE=./logs/nlp_service.log
LOG_ROTATION_SIZE=100MB
LOG_RETENTION_DAYS=30
ENABLE_DEBUG_LOGGING=false
```

**Log Rotation Script:**
```powershell
# Create log rotation script: rotate_logs.ps1
$logDir = "C:\Projects\ash-nlp\logs"
$maxSize = 100MB
$retentionDays = 30

# Rotate large log files
Get-ChildItem $logDir -Filter "*.log" | ForEach-Object {
    if ($_.Length -gt $maxSize) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $newName = $_.BaseName + "_$timestamp" + $_.Extension
        Rename-Item $_.FullName -NewName $newName
        # Create new empty log file
        New-Item -Path $_.FullName -ItemType File -Force
    }
}

# Clean old log files
Get-ChildItem $logDir -Filter "*.log" | Where-Object { 
    $_.LastWriteTime -lt (Get-Date).AddDays(-$retentionDays) 
} | Remove-Item -Force
```

**Schedule Log Rotation:**
```powershell
# Schedule daily log rotation
schtasks /create /tn "Ash NLP Log Rotation" /tr "powershell.exe -File C:\Projects\ash-nlp\scripts\rotate_logs.ps1" /sc daily /st 02:00
```

### Performance Monitoring

**Resource Monitoring Script:**
```powershell
# Create performance monitoring: monitor_performance.ps1
$nlpContainer = "ash_nlp_server"
$logFile = "C:\Projects\ash-nlp\logs\performance_monitor.log"

while ($true) {
    try {
        # Get container stats
        $stats = docker stats $nlpContainer --no-stream --format "table {{.CPUPerc}},{{.MemUsage}},{{.NetIO}}"
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        # Parse stats
        $statLine = $stats | Select-Object -Skip 1
        $values = $statLine -split ','
        
        $cpuPercent = $values[0]
        $memUsage = $values[1]
        $netIO = $values[2]
        
        # Log performance data
        $logEntry = "[$timestamp] CPU: $cpuPercent, Memory: $memUsage, Network: $netIO"
        Add-Content -Path $logFile -Value $logEntry
        
        # Check for performance issues
        $cpuValue = [float]($cpuPercent -replace '%', '')
        if ($cpuValue -gt 80) {
            Write-Host "[$timestamp] WARNING: High CPU usage: $cpuPercent" -ForegroundColor Yellow
        }
        
        # Check NLP server response time
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-RestMethod -Uri "http://10.20.30.16:8881/health" -TimeoutSec 10
        $stopwatch.Stop()
        $responseTime = $stopwatch.ElapsedMilliseconds
        
        if ($responseTime -gt 5000) {
            Write-Host "[$timestamp] WARNING: Slow response time: ${responseTime}ms" -ForegroundColor Yellow
        }
        
    }
    catch {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] Performance monitoring error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
```

### Backup and Recovery

**Learning Data Backup Script:**
```powershell
# Create backup script: backup_learning_data.ps1
$sourceDir = "C:\Projects\ash-nlp\learning_data"
$backupDir = "C:\Backups\ash-nlp"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = "$backupDir\learning_data_backup_$timestamp"

# Create backup directory
New-Item -Path $backupPath -ItemType Directory -Force

# Copy learning data
Copy-Item -Path "$sourceDir\*" -Destination $backupPath -Recurse -Force

# Compress backup
Compress-Archive -Path $backupPath -DestinationPath "$backupPath.zip" -Force
Remove-Item -Path $backupPath -Recurse -Force

# Clean old backups (keep last 30 days)
Get-ChildItem $backupDir -Filter "learning_data_backup_*.zip" | Where-Object { 
    $_.LastWriteTime -lt (Get-Date).AddDays(-30) 
} | Remove-Item -Force

Write-Host "Learning data backup completed: $backupPath.zip"
```

**Model Cache Backup:**
```powershell
# Create model backup script: backup_models.ps1
$modelDir = "C:\Projects\ash-nlp\models"
$backupDir = "C:\Backups\ash-nlp"
$timestamp = Get-Date -Format "yyyyMMdd"
$modelBackupPath = "$backupDir\models_backup_$timestamp.zip"

# Only backup if models directory has changed in last 7 days
$lastChange = (Get-ChildItem $modelDir -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime
if ($lastChange -gt (Get-Date).AddDays(-7)) {
    Compress-Archive -Path "$modelDir\*" -DestinationPath $modelBackupPath -Force
    Write-Host "Model cache backup completed: $modelBackupPath"
} else {
    Write-Host "No recent model changes, skipping backup"
}
```

**Automated Backup Schedule:**
```powershell
# Schedule daily learning data backup
schtasks /create /tn "Ash NLP Learning Backup" /tr "powershell.exe -File C:\Projects\ash-nlp\scripts\backup_learning_data.ps1" /sc daily /st 01:00

# Schedule weekly model backup
schtasks /create /tn "Ash NLP Model Backup" /tr "powershell.exe -File C:\Projects\ash-nlp\scripts\backup_models.ps1" /sc weekly /d SUN /st 03:00
```

### Update and Maintenance Procedures

**Update Process Script:**
```powershell
# Create update script: update_nlp_server.ps1
param(
    [Parameter(Mandatory=$false)]
    [string]$Version = "latest"
)

$projectDir = "C:\Projects\ash-nlp"
$backupDir = "C:\Backups\ash-nlp"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

Write-Host "Starting Ash NLP Server update to version: $Version"

try {
    # Step 1: Backup current state
    Write-Host "Creating backup..."
    $backupPath = "$backupDir\pre_update_backup_$timestamp"
    New-Item -Path $backupPath -ItemType Directory -Force
    Copy-Item -Path "$projectDir\learning_data" -Destination "$backupPath\learning_data" -Recurse -Force
    Copy-Item -Path "$projectDir\.env" -Destination "$backupPath\.env" -Force
    
    # Step 2: Stop current service
    Write-Host "Stopping NLP server..."
    Set-Location $projectDir
    docker-compose down
    
    # Step 3: Update code (if using Git)
    Write-Host "Updating code from GitHub..."
    git fetch origin
    if ($Version -eq "latest") {
        git checkout main
        git pull origin main
    } else {
        git checkout "tags/$Version"
    }
    
    # Step 4: Update Docker image
    Write-Host "Pulling latest Docker image..."
    docker-compose pull
    
    # Step 5: Start updated service
    Write-Host "Starting updated NLP server..."
    docker-compose up -d
    
    # Step 6: Verify deployment
    Write-Host "Verifying deployment..."
    Start-Sleep -Seconds 30  # Wait for startup
    
    $healthCheck = Invoke-RestMethod -Uri "http://10.20.30.16:8881/health" -TimeoutSec 30
    if ($healthCheck.status -eq "healthy") {
        Write-Host "Update completed successfully!" -ForegroundColor Green
        
        # Test learning system
        $learningCheck = Invoke-RestMethod -Uri "http://10.20.30.16:8881/learning_statistics" -TimeoutSec 30
        Write-Host "Learning system status: $($learningCheck.status)" -ForegroundColor Green
    } else {
        throw "Health check failed after update"
    }
    
} catch {
    Write-Host "Update failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Rolling back..." -ForegroundColor Yellow
    
    # Rollback procedure
    docker-compose down
    git checkout main  # Or previous stable version
    Copy-Item -Path "$backupPath\learning_data" -Destination "$projectDir\learning_data" -Recurse -Force
    Copy-Item -Path "$backupPath\.env" -Destination "$projectDir\.env" -Force
    docker-compose up -d
    
    Write-Host "Rollback completed. Please check logs and try again." -ForegroundColor Yellow
}
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Installation Issues

**❌ Problem: Docker Desktop not starting**
```powershell
# Solution: Check WSL2 and virtualization
# 1. Enable virtualization in BIOS
# 2. Enable Windows features:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 3. Restart computer
# 4. Update WSL2 kernel
wsl --update
```

**❌ Problem: GPU not detected in Docker**
```powershell
# Solution: Install NVIDIA Container Toolkit
# 1. Install NVIDIA drivers (535+)
nvidia-smi

# 2. Install NVIDIA Container Toolkit
# Follow: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# 3. Restart Docker Desktop
# 4. Test GPU access:
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi
```

**❌ Problem: Model download failures**
```powershell
# Solution: Check internet and storage
# 1. Verify internet connection
curl https://huggingface.co

# 2. Check disk space
Get-WmiObject -Class Win32_LogicalDisk | Select-Object Size,FreeSpace

# 3. Set Hugging Face token (if needed)
# Add to .env file:
# HUGGINGFACE_HUB_TOKEN=your_token_here

# 4. Manual model download
python -c "from transformers import AutoModel; AutoModel.from_pretrained('rafalposwiata/deproberta-large-depression')"
```

#### Runtime Issues

**❌ Problem: High memory usage**
```powershell
# Solution: Optimize memory settings
# 1. Check current usage
docker stats ash_nlp_server --no-stream

# 2. Reduce batch size in .env
# MAX_BATCH_SIZE=16
# MODEL_PRECISION=float16

# 3. Restart container
docker-compose restart ash-nlp

# 4. Monitor improvement
docker stats ash_nlp_server --no-stream
```

**❌ Problem: Slow response times**
```powershell
# Solution: Performance optimization
# 1. Check GPU utilization
nvidia-smi

# 2. Verify GPU is being used
curl http://10.20.30.16:8881/system_status

# 3. Optimize settings in .env:
# DEVICE=cuda
# INFERENCE_THREADS=8
# MAX_CONCURRENT_REQUESTS=15

# 4. Restart service
docker-compose restart ash-nlp
```

**❌ Problem: Learning system not working**
```powershell
# Solution: Debug learning system
# 1. Check learning status
curl http://10.20.30.16:8881/learning_statistics

# 2. Verify learning data directory
ls C:\Projects\ash-nlp\learning_data

# 3. Check permissions
# Ensure learning_data directory is writable

# 4. Check logs for learning errors
docker-compose logs ash-nlp | Select-String "learning"

# 5. Reset learning system if needed (CAUTION)
# Remove learning_data contents and restart
```

#### Integration Issues

**❌ Problem: Ash bot can't connect to NLP server**
```powershell
# Solution: Check network connectivity
# 1. Test from Ash bot server (10.20.30.253)
curl http://10.20.30.16:8881/health

# 2. Check firewall settings on NLP server
# Ensure port 8881 is open

# 3. Verify NLP server is running
docker-compose ps

# 4. Check network configuration
# Ensure both servers are on same network

# 5. Test with specific IP
ping 10.20.30.16
telnet 10.20.30.16 8881
```

**❌ Problem: Analytics dashboard not receiving data**
```powershell
# Solution: Check webhook configuration
# 1. Verify webhook URL in .env
# ANALYTICS_WEBHOOK_URL=http://10.20.30.16:8883/webhook/nlp_metrics

# 2. Test webhook endpoint
curl http://10.20.30.16:8883/webhook/nlp_metrics

# 3. Check analytics export setting
# ENABLE_ANALYTICS_EXPORT=true

# 4. Monitor webhook calls in logs
docker-compose logs ash-nlp | Select-String "webhook"
```

### Advanced Debugging

**Enable Debug Mode:**
```powershell
# 1. Update .env file
# LOG_LEVEL=DEBUG
# ENABLE_DEBUG_LOGGING=true

# 2. Restart with debug logging
docker-compose restart ash-nlp

# 3. Monitor debug logs
docker-compose logs -f ash-nlp
```

**Performance Debugging:**
```powershell
# Create performance debug script: debug_performance.ps1
$nlpUrl = "http://10.20.30.16:8881"

# Test response times
$testMessages = @(
    "feeling really down today",
    "this game is killing me",
    "can't go on like this",
    "having a great day!"
)

foreach ($message in $testMessages) {
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    try {
        $response = Invoke-RestMethod -Uri "$nlpUrl/analyze" -Method POST -Body (@{
            message = $message
            user_id = "test_user"
            channel_id = "test_channel"
        } | ConvertTo-Json) -ContentType "application/json"
        
        $stopwatch.Stop()
        $responseTime = $stopwatch.ElapsedMilliseconds
        
        Write-Host "Message: '$message'"
        Write-Host "Response time: ${responseTime}ms"
        Write-Host "Crisis level: $($response.crisis_level)"
        Write-Host "Confidence: $($response.confidence_score)"
        Write-Host "Method: $($response.method)"
        Write-Host "---"
        
    } catch {
        $stopwatch.Stop()
        Write-Host "Error testing message '$message': $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

**Memory Debugging:**
```powershell
# Monitor memory usage over time
$logFile = "C:\Projects\ash-nlp\logs\memory_debug.log"
$duration = 60  # minutes

for ($i = 0; $i -lt $duration; $i++) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $stats = docker stats ash_nlp_server --no-stream --format "{{.MemUsage}}"
    $logEntry = "[$timestamp] Memory usage: $stats"
    Add-Content -Path $logFile -Value $logEntry
    Write-Host $logEntry
    Start-Sleep -Seconds 60
}
```

### Emergency Recovery Procedures

**Complete System Recovery:**
```powershell
# Emergency recovery script: emergency_recovery.ps1
$projectDir = "C:\Projects\ash-nlp"
$backupDir = "C:\Backups\ash-nlp"

Write-Host "Starting emergency recovery procedure..." -ForegroundColor Red

try {
    # Stop all services
    Set-Location $projectDir
    docker-compose down
    
    # Reset to last known good state
    git checkout main
    git reset --hard HEAD
    
    # Restore latest backup
    $latestBackup = Get-ChildItem $backupDir -Filter "learning_data_backup_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($latestBackup) {
        Write-Host "Restoring from backup: $($latestBackup.Name)"
        Expand-Archive -Path $latestBackup.FullName -DestinationPath $projectDir -Force
    }
    
    # Reset Docker environment
    docker system prune -a -f
    docker-compose pull
    
    # Start services
    docker-compose up -d
    
    # Wait and verify
    Start-Sleep -Seconds 60
    $health = Invoke-RestMethod -Uri "http://10.20.30.16:8881/health" -TimeoutSec 30
    
    if ($health.status -eq "healthy") {
        Write-Host "Emergency recovery completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Recovery verification failed. Manual intervention required." -ForegroundColor Red
    }
    
} catch {
    Write-Host "Emergency recovery failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Contact technical support immediately." -ForegroundColor Red
}
```

---

## 📞 Support and Resources

### Getting Technical Help

**Support Escalation:**
1. **Self-Service** - Use this implementation guide and troubleshooting section
2. **Documentation** - Check [README.md](../README.md) and other guides in `/docs`
3. **GitHub Issues** - Report bugs and request features
4. **Discord Support** - [The Alphabet Cartel server](https://discord.gg/alphabetcartel)
5. **Direct Contact** - For urgent production issues

### Useful Resources

**Official Documentation:**
- [PyTorch Documentation](https://pytorch.org/docs/) - Deep learning framework
- [Transformers Documentation](https://huggingface.co/docs/transformers/) - NLP models
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - API framework
- [Docker Documentation](https://docs.docker.com/) - Containerization

**Community Resources:**
- [Hugging Face Models](https://huggingface.co/models) - Pre-trained AI models
- [NVIDIA Developer](https://developer.nvidia.com/) - GPU optimization guides
- [Microsoft WSL](https://docs.microsoft.com/en-us/windows/wsl/) - Windows Subsystem for Linux

### Related Repositories

**The Alphabet Cartel Ecosystem:**
- **[Main Ash Bot](https://github.com/the-alphabet-cartel/ash)** - Discord bot integration
- **[Analytics Dashboard](https://github.com/the-alphabet-cartel/ash-dash)** - Metrics and monitoring
- **[Testing Suite](https://github.com/the-alphabet-cartel/ash-thrash)** - Automated testing
- **[NLP Server](https://github.com/the-alphabet-cartel/ash-nlp)** - This repository

---

## 📋 Pre-Deployment Checklist

### System Preparation
- [ ] Windows 11 Pro installed and updated
- [ ] Docker Desktop installed and running
- [ ] NVIDIA drivers (535+) installed
- [ ] Git for Windows installed
- [ ] Atom editor configured with recommended packages
- [ ] Network connectivity to 10.20.30.16 verified
- [ ] Firewall configured to allow port 8881

### Environment Configuration
- [ ] Repository cloned to `C:\Projects\ash-nlp`
- [ ] `.env` file created from template
- [ ] Environment variables configured correctly
- [ ] Hardware optimization settings applied
- [ ] Learning system enabled
- [ ] Security settings configured

### Docker Deployment
- [ ] `docker-compose.yml` reviewed and customized
- [ ] Necessary directories created (`models`, `learning_data`, `logs`, `data`)
- [ ] Docker images pulled successfully
- [ ] Container deployed and running
- [ ] Health check endpoint responding
- [ ] Learning system operational

### Integration Testing
- [ ] Ash bot can connect to NLP server
- [ ] Analytics dashboard receiving data
- [ ] Testing suite can run against NLP server
- [ ] All ports accessible from required servers
- [ ] Backup and monitoring scripts operational

### Production Readiness
- [ ] Performance monitoring active
- [ ] Log rotation configured
- [ ] Backup procedures scheduled
- [ ] Update procedures documented
- [ ] Emergency recovery plan tested
- [ ] Team trained on new system

---

**🎉 Congratulations! You now have a fully deployed and optimized Ash NLP Server v2.1 with enhanced learning capabilities, perfectly tuned for your RTX 3050 + Ryzen 7 7700X setup.**

**Next Steps:**
1. **Train the Team** - Share the [Team Guide](team_guide.md) with Crisis Response members
2. **Monitor Performance** - Use the monitoring scripts to ensure optimal operation
3. **Gather Feedback** - Start collecting learning data to improve AI accuracy
4. **Optimize Further** - Fine-tune performance based on real-world usage patterns

**💜 Thank you for deploying advanced AI to help keep The Alphabet Cartel community safe and supported!**

---

*For technical questions about this implementation guide, create a GitHub issue or contact the technical team via Discord.*

**Last Updated:** July 27, 2025 | **Version:** 2.1 | **Guide Status:** Active