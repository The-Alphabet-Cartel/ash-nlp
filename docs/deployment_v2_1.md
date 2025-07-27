# 🚀 Deployment Guide - Ash NLP Server v2.1

> *Complete step-by-step deployment guide for production-ready AI crisis detection with adaptive learning*

[![Deployment Guide](https://img.shields.io/badge/guide-deployment-green)](https://github.com/the-alphabet-cartel/ash-nlp)
[![Version](https://img.shields.io/badge/version-2.1-blue)](https://github.com/the-alphabet-cartel/ash-nlp/releases/tag/v2.1)
[![Production Ready](https://img.shields.io/badge/production-ready-brightgreen)](https://docker.com/)

---

## 📋 Table of Contents

1. [Pre-Deployment Planning](#-pre-deployment-planning)
2. [System Requirements](#-system-requirements)
3. [Environment Preparation](#-environment-preparation)
4. [Installation Methods](#-installation-methods)
5. [Configuration Setup](#-configuration-setup)
6. [Production Deployment](#-production-deployment)
7. [Post-Deployment Verification](#-post-deployment-verification)
8. [Integration Setup](#-integration-setup)
9. [Monitoring & Maintenance](#-monitoring--maintenance)
10. [Troubleshooting](#-troubleshooting)

---

## 📋 Pre-Deployment Planning

### Deployment Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    The Alphabet Cartel Network                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐  │
│  │   Ash Discord   │────│   NLP Server    │────│ Analytics   │  │
│  │      Bot        │    │   (Deploy Here) │    │ Dashboard   │  │
│  │  10.20.30.253   │    │   10.20.30.16   │    │(ash-dash)   │  │
│  │     :8882       │    │     :8881       │    │   :8883     │  │
│  └─────────────────┘    └─────────────────┘    └─────────────┘  │
│                                │                                │
│                                ▼                                │
│                         ┌─────────────┐                         │
│                         │ Testing     │                         │
│                         │ Suite       │                         │
│                         │(ash-thrash) │                         │
│                         │   :8884     │                         │
│                         └─────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Checklist

**Before Starting:**
- [ ] Server specifications verified (RTX 3050 + Ryzen 7 7700X)
- [ ] Windows 11 Pro updated and configured
- [ ] Docker Desktop installed and running
- [ ] Network connectivity to other Alphabet Cartel services verified
- [ ] Backup strategy planned for learning data
- [ ] Crisis Response team notified of deployment schedule

**Required Access:**
- [ ] Administrative access to Windows 11 server (10.20.30.16)
- [ ] GitHub repository access ([The-Alphabet-Cartel/ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp))
- [ ] Docker Hub or GitHub Container Registry access
- [ ] Network access to ports 8881, 8882, 8883, 8884
- [ ] Optional: Hugging Face account for model downloads

**Dependencies:**
- [ ] Ash Discord Bot (10.20.30.253:8882) - Primary integration
- [ ] Ash-Dash Analytics (10.20.30.16:8883) - Optional but recommended
- [ ] Ash-Thrash Testing (10.20.30.16:8884) - Optional for validation

---

## 💻 System Requirements

### Target Hardware (Your Setup) ✅

```yaml
Server Configuration:
  CPU: AMD Ryzen 7 7700X (8 cores, 16 threads)
  GPU: NVIDIA RTX 3050 (8GB VRAM)
  RAM: 64GB DDR5
  Storage: NVMe SSD (minimum 50GB free for models and data)
  Network: Gigabit Ethernet
  OS: Windows 11 Pro

Network Configuration:
  IP Address: 10.20.30.16
  Primary Port: 8881 (NLP API)
  Firewall: Allow inbound on 8881 from 10.20.30.0/24
```

### Software Prerequisites

```yaml
Required Software:
  OS: Windows 11 Pro (latest updates)
  Docker Desktop: v4.15+ with WSL2 backend
  Git: v2.30+
  PowerShell: v7.0+ (recommended)

Optional Development Tools:
  Atom Editor: Latest (your preference)
  GitHub Desktop: Latest (your preference)
  Windows Terminal: Latest (improved PowerShell experience)

GPU Drivers:
  NVIDIA Driver: v535+ (for RTX 3050)
  CUDA Toolkit: v11.8+ (automatically included with Docker)
```

### Resource Planning

```yaml
Disk Space Requirements:
  Base Installation: ~5GB
  AI Models Cache: ~8GB (DeBERTa + RoBERTa)
  Learning Data: ~500MB (grows over time)
  Logs: ~1GB (with rotation)
  Docker Images: ~3GB
  Total Recommended: 50GB free space

Memory Allocation:
  Base System: 2-4GB
  AI Models: 4-6GB
  Learning System: 500MB-1GB
  Docker Overhead: 1-2GB
  Available for Other Services: 50GB+

Network Bandwidth:
  Initial Model Download: ~8GB (one-time)
  Operational: <10MB/day (logs, updates)
  Integration Traffic: Minimal (local network)
```

---

## 🛠️ Environment Preparation

### 1. Windows 11 Server Setup

**Update Windows 11:**
```powershell
# Run as Administrator
# Check for updates
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot

# Verify system specifications
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, TotalPhysicalMemory
Get-WmiObject -Class Win32_VideoController | Select-Object Name, AdapterRAM
```

**Configure Windows Features:**
```powershell
# Enable required Windows features
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart required after enabling features
Restart-Computer
```

**Install Docker Desktop:**
```powershell
# Download Docker Desktop from docker.com
# Install with WSL2 backend enabled
# Verify installation
docker --version
docker-compose --version

# Test Docker functionality
docker run hello-world
```

### 2. GPU Driver Setup

**Install NVIDIA Drivers:**
```powershell
# Download latest drivers from nvidia.com (535+)
# Or use automatic detection
# Verify installation
nvidia-smi

# Expected output should show RTX 3050 with 8GB memory
```

**Verify GPU Docker Support:**
```powershell
# Test GPU access in Docker
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# Should display GPU information inside container
```

### 3. Network Configuration

**Configure Firewall:**
```powershell
# Allow inbound traffic on port 8881
New-NetFirewallRule -DisplayName "Ash NLP Server" -Direction Inbound -Port 8881 -Protocol TCP -Action Allow

# Verify network connectivity to other services
Test-NetConnection -ComputerName 10.20.30.253 -Port 8882  # Ash Bot
Test-NetConnection -ComputerName 10.20.30.16 -Port 8883   # Ash-Dash (same server)
```

**Verify IP Configuration:**
```powershell
# Confirm server IP address
Get-NetIPAddress | Where-Object {$_.IPAddress -eq "10.20.30.16"}

# Test local network connectivity
ping 10.20.30.253  # Ash Bot server
```

---

## 📦 Installation Methods

### Method 1: Docker Deployment (Recommended for Production)

**1. Create Project Directory:**
```powershell
# Create deployment directory
New-Item -Path "C:\Deployments\ash-nlp" -ItemType Directory -Force
Set-Location "C:\Deployments\ash-nlp"
```

**2. Clone Repository:**
```powershell
# Using command line
git clone https://github.com/the-alphabet-cartel/ash-nlp.git .

# Or using GitHub Desktop (your preference)
# File → Clone Repository → URL: https://github.com/the-alphabet-cartel/ash-nlp.git
# Local Path: C:\Deployments\ash-nlp
```

**3. Prepare Environment Configuration:**
```powershell
# Copy environment template
Copy-Item .env.template .env

# Create required directories
New-Item -Path "models", "learning_data", "logs", "data" -ItemType Directory -Force
```

**4. Deploy with Docker Compose:**
```powershell
# Pull latest images
docker-compose pull

# Deploy in production mode
docker-compose up -d

# Verify deployment
docker-compose ps
```

### Method 2: Native Python Installation (Development/Testing)

**1. Create Python Environment:**
```powershell
# Navigate to project directory
Set-Location "C:\Deployments\ash-nlp"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**2. Install Dependencies:**
```powershell
# Update pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install PyTorch with CUDA support for RTX 3050
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**3. Verify Installation:**
```powershell
# Test Python imports
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
```

---

## ⚙️ Configuration Setup

### 1. Environment Configuration (.env)

**Production Configuration Template:**
```bash
# === Core Server Configuration ===
NLP_SERVICE_HOST=10.20.30.16
NLP_SERVICE_PORT=8881
PYTHONUNBUFFERED=1

# === AI Model Configuration ===
DEPRESSION_MODEL=rafalposwiata/deproberta-large-depression
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL_CACHE_DIR=./models/cache

# === Hardware Optimization (RTX 3050 + Ryzen 7 7700X) ===
DEVICE=auto                    # Auto-detect GPU/CPU
MODEL_PRECISION=float16        # GPU memory optimization
MAX_BATCH_SIZE=32             # Optimized for RTX 3050
INFERENCE_THREADS=8           # Ryzen 7 7700X optimization
MAX_CONCURRENT_REQUESTS=25    # Handle multiple requests
GPU_MEMORY_FRACTION=0.8       # Reserve GPU memory

# === Enhanced Learning System ===
ENABLE_LEARNING_SYSTEM=true
LEARNING_RATE=0.1
MAX_LEARNING_ADJUSTMENTS_PER_DAY=100
MAX_LEARNING_ADJUSTMENTS_PER_HOUR=10
LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json
MIN_CONFIDENCE_ADJUSTMENT=0.02
MAX_CONFIDENCE_ADJUSTMENT=0.30

# === Crisis Detection Thresholds ===
CRISIS_HIGH_THRESHOLD=0.50
CRISIS_MEDIUM_THRESHOLD=0.22
CRISIS_LOW_THRESHOLD=0.12

# === Performance Tuning ===
REQUEST_TIMEOUT=30
UVICORN_WORKERS=1             # Single worker for GPU sharing
RELOAD_ON_CHANGES=false       # Disable in production
ENABLE_MODEL_CACHING=true
CACHE_SIZE_GB=2.0

# === Logging Configuration ===
LOG_LEVEL=INFO
LOG_FILE=./logs/nlp_service.log
LOG_ROTATION_SIZE=100MB
LOG_RETENTION_DAYS=30
ENABLE_DEBUG_LOGGING=false

# === Analytics and Monitoring ===
ENABLE_REAL_TIME_ANALYTICS=true
ANALYTICS_UPDATE_INTERVAL=300  # 5 minutes
PERFORMANCE_MONITORING=true
HEALTH_CHECK_INTERVAL=60

# === Optional: External Integrations ===
ENABLE_ANALYTICS_EXPORT=true
ANALYTICS_WEBHOOK_URL=http://10.20.30.16:8883/webhook/nlp_metrics

# === Optional: Hugging Face Token (for model downloads) ===
# HUGGINGFACE_HUB_TOKEN=your_token_here

# === Security Configuration ===
API_KEY_ENABLED=false
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10

# === Data Retention ===
LEARNING_DATA_RETENTION_DAYS=365
ANALYTICS_DATA_RETENTION_DAYS=180
BACKUP_LEARNING_DATA=true
```

### 2. Docker Compose Configuration

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
      # Load all environment variables from .env file
      - PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}
      - NLP_SERVICE_HOST=${NLP_SERVICE_HOST:-0.0.0.0}
      - NLP_SERVICE_PORT=${NLP_SERVICE_PORT:-8881}
      - DEVICE=${DEVICE:-auto}
      - ENABLE_LEARNING_SYSTEM=${ENABLE_LEARNING_SYSTEM:-true}
      - GPU_MEMORY_FRACTION=${GPU_MEMORY_FRACTION:-0.8}
    
    volumes:
      # Persistent storage for models and data
      - ./models:/app/models/cache:rw
      - ./learning_data:/app/learning_data:rw
      - ./logs:/app/logs:rw
      - ./data:/app/data:rw
      - ./analytics:/app/analytics:rw
    
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '6'
        reservations:
          memory: 2G
          cpus: '2'
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${NLP_SERVICE_PORT:-8881}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s  # Allow time for model loading

networks:
  ash-network:
    external: true
    name: ash_network
```

### 3. Directory Structure Setup

**Create Required Directories:**
```powershell
# Create all required directories with proper permissions
$directories = @(
    "C:\Deployments\ash-nlp\models\cache",
    "C:\Deployments\ash-nlp\learning_data",
    "C:\Deployments\ash-nlp\logs",
    "C:\Deployments\ash-nlp\data",
    "C:\Deployments\ash-nlp\analytics",
    "C:\Deployments\ash-nlp\backups"
)

foreach ($dir in $directories) {
    New-Item -Path $dir -ItemType Directory -Force
    Write-Host "Created directory: $dir"
}
```

**Verify Directory Structure:**
```
C:\Deployments\ash-nlp\
├── .env                      # Environment configuration
├── docker-compose.yml        # Docker deployment configuration
├── requirements.txt          # Python dependencies
├── nlp_main.py              # Main application
├── models/
│   └── cache/               # AI model storage
├── learning_data/           # Learning system data
├── logs/                    # Application logs
├── data/                    # General data storage
├── analytics/               # Analytics data
├── backups/                 # Learning data backups
└── docs/                    # Documentation
```

---

## 🚀 Production Deployment

### 1. Pre-Deployment Validation

**System Health Check:**
```powershell
# Verify system resources
Write-Host "=== System Health Check ==="
Write-Host "CPU: $(Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty Name)"
Write-Host "RAM: $([math]::Round((Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)) GB"
Write-Host "GPU: $(Get-WmiObject -Class Win32_VideoController | Where-Object {$_.Name -like "*RTX*"} | Select-Object -ExpandProperty Name)"

# Verify Docker functionality
Write-Host "=== Docker Status ==="
docker version
docker-compose version

# Test GPU access
Write-Host "=== GPU Test ==="
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi
```

**Network Connectivity Test:**
```powershell
# Test network connectivity to other services
Write-Host "=== Network Connectivity ==="
Test-NetConnection -ComputerName 10.20.30.253 -Port 8882 -InformationLevel Detailed  # Ash Bot
Test-NetConnection -ComputerName 127.0.0.1 -Port 8883 -InformationLevel Detailed     # Ash-Dash (local)

# Verify port availability
Get-NetTCPConnection -LocalPort 8881 -ErrorAction SilentlyContinue
if ($?) {
    Write-Warning "Port 8881 is already in use!"
} else {
    Write-Host "Port 8881 is available for deployment"
}
```

### 2. Initial Deployment

**Deploy NLP Server:**
```powershell
# Navigate to deployment directory
Set-Location "C:\Deployments\ash-nlp"

# Pull latest Docker images
Write-Host "Pulling latest Docker images..."
docker-compose pull

# Start deployment
Write-Host "Starting Ash NLP Server v2.1..."
docker-compose up -d

# Monitor startup
Write-Host "Monitoring startup logs..."
docker-compose logs -f ash-nlp
```

**Monitor Initial Startup:**
```powershell
# Watch for successful model loading
docker-compose logs ash-nlp | Select-String -Pattern "models loaded|server started|learning system active"

# Check container status
docker-compose ps

# Expected output:
# ash_nlp_server   /app/entrypoint.sh   Up   0.0.0.0:8881->8881/tcp
```

### 3. Model Download and Caching

**Monitor Model Download Progress:**
```powershell
# Models download on first startup - this may take 10-20 minutes
Write-Host "Monitoring model download progress..."

# Watch logs for download progress
docker-compose logs -f ash-nlp | Select-String -Pattern "Downloading|Loading|model"

# Check disk usage during download
while ($true) {
    $modelSize = (Get-ChildItem -Path ".\models\cache" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
    Write-Host "Models cache size: $([math]::Round($modelSize, 2)) GB"
    Start-Sleep -Seconds 30
    
    # Break when models are loaded (check health endpoint)
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:8881/health" -TimeoutSec 5
        if ($health.status -eq "healthy") {
            Write-Host "Models loaded successfully!"
            break
        }
    } catch {
        # Still loading, continue monitoring
    }
}
```

### 4. Learning System Initialization

**Initialize Learning System:**
```powershell
# Verify learning system is active
$learningStats = Invoke-RestMethod -Uri "http://localhost:8881/learning_statistics"
if ($learningStats.system_status -eq "active") {
    Write-Host "✅ Learning system initialized successfully"
    Write-Host "Learning rate: $($learningStats.learning_rate_info.current_rate)"
    Write-Host "Daily limit: $($learningStats.daily_limits.max_adjustments)"
} else {
    Write-Warning "❌ Learning system not active - check configuration"
}
```

---

## ✅ Post-Deployment Verification

### 1. Health Checks

**Basic Health Verification:**
```powershell
# Test health endpoint
Write-Host "=== Health Check ==="
$health = Invoke-RestMethod -Uri "http://10.20.30.16:8881/health"
Write-Host "Status: $($health.status)"
Write-Host "Version: $($health.version)"
Write-Host "Uptime: $($health.uptime_seconds) seconds"

# Verify services
foreach ($service in $health.services.PSObject.Properties) {
    $status = if ($service.Value -eq "loaded" -or $service.Value -eq "active" -or $service.Value -eq "connected" -or $service.Value -eq "running") { "✅" } else { "❌" }
    Write-Host "$status $($service.Name): $($service.Value)"
}
```

**System Status Verification:**
```powershell
# Get detailed system status
Write-Host "=== System Status ==="
$sysStatus = Invoke-RestMethod -Uri "http://10.20.30.16:8881/system_status"

# Hardware status
Write-Host "CPU Usage: $($sysStatus.hardware_status.cpu_usage)%"
Write-Host "Memory Usage: $($sysStatus.hardware_status.memory_usage.used_gb)GB / $($sysStatus.hardware_status.memory_usage.total_gb)GB"
Write-Host "GPU Available: $($sysStatus.hardware_status.gpu_status.available)"
Write-Host "GPU Utilization: $($sysStatus.hardware_status.gpu_status.utilization_percentage)%"

# AI Models status
foreach ($model in $sysStatus.ai_models.PSObject.Properties) {
    $modelInfo = $model.Value
    $status = if ($modelInfo.status -eq "loaded") { "✅" } else { "❌" }
    Write-Host "$status $($model.Name): $($modelInfo.status) ($($modelInfo.device))"
}
```

### 2. Functionality Testing

**Test Analysis Endpoint:**
```powershell
# Test basic crisis detection
Write-Host "=== Analysis Test ==="
$testMessage = @{
    message = "feeling really down today"
    user_id = "test_user_123"
    channel_id = "test_channel_456"
} | ConvertTo-Json

$analysisResult = Invoke-RestMethod -Uri "http://10.20.30.16:8881/analyze" -Method POST -Body $testMessage -ContentType "application/json"

Write-Host "Crisis Level: $($analysisResult.crisis_level)"
Write-Host "Confidence: $($analysisResult.confidence_score)"
Write-Host "Processing Time: $($analysisResult.processing_time_ms)ms"
Write-Host "Method: $($analysisResult.method)"

if ($analysisResult.needs_response) {
    Write-Host "✅ Crisis detection working correctly"
} else {
    Write-Warning "⚠️ Unexpected analysis result"
}
```

**Test Learning System:**
```powershell
# Test learning system endpoints
Write-Host "=== Learning System Test ==="

# Test false positive reporting
$fpTest = @{
    message = "this test is killing me"
    detected_level = "high"
    correct_level = "none"
    context = "testing"
    severity = 5
    reporter_id = "deployment_test"
} | ConvertTo-Json

try {
    $fpResult = Invoke-RestMethod -Uri "http://10.20.30.16:8881/analyze_false_positive" -Method POST -Body $fpTest -ContentType "application/json"
    if ($fpResult.status -eq "success") {
        Write-Host "✅ Learning system accepting feedback"
    }
} catch {
    Write-Warning "❌ Learning system test failed: $($_.Exception.Message)"
}
```

### 3. Performance Validation

**Performance Metrics Check:**
```powershell
# Get performance metrics
Write-Host "=== Performance Metrics ==="
$perfMetrics = Invoke-RestMethod -Uri "http://10.20.30.16:8881/performance_metrics?period=1hour"

Write-Host "Average Response Time: $($perfMetrics.response_time_metrics.average_ms)ms"
Write-Host "Success Rate: $([math]::Round($perfMetrics.request_metrics.success_rate * 100, 2))%"
Write-Host "CPU Average: $($perfMetrics.resource_usage.cpu_average)%"
Write-Host "Memory Average: $($perfMetrics.resource_usage.memory_average_gb)GB"

# Validate performance targets
$targets = @{
    "Response Time" = @{ actual = $perfMetrics.response_time_metrics.average_ms; target = 100; unit = "ms" }
    "Success Rate" = @{ actual = $perfMetrics.request_metrics.success_rate; target = 0.99; unit = "%" }
    "CPU Usage" = @{ actual = $perfMetrics.resource_usage.cpu_average; target = 30; unit = "%" }
}

foreach ($metric in $targets.GetEnumerator()) {
    $actual = $metric.Value.actual
    $target = $metric.Value.target
    $unit = $metric.Value.unit
    
    if (($unit -eq "ms" -or $unit -eq "%") -and $actual -le $target) {
        Write-Host "✅ $($metric.Key): $actual$unit (target: ≤$target$unit)"
    } elseif ($unit -eq "%" -and $actual -ge $target) {
        Write-Host "✅ $($metric.Key): $actual$unit (target: ≥$target$unit)"
    } else {
        Write-Warning "⚠️ $($metric.Key): $actual$unit (target: $target$unit)"
    }
}
```

---

## 🔗 Integration Setup

### 1. Ash Bot Integration

**Configure Ash Bot Connection:**
```powershell
# Test connectivity from Ash bot server perspective
Write-Host "=== Ash Bot Integration ==="

# From Ash bot server (10.20.30.253), test NLP connectivity
# This would be run on the Ash bot server:
# Invoke-RestMethod -Uri "http://10.20.30.16:8881/health"

# From NLP server, verify we can reach Ash bot
try {
    Test-NetConnection -ComputerName 10.20.30.253 -Port 8882
    Write-Host "✅ Network connectivity to Ash bot verified"
} catch {
    Write-Warning "❌ Cannot reach Ash bot server"
}
```

**Validate Integration API:**
```powershell
# Test integration endpoints that Ash bot will use
$integrationTests = @(
    @{ name = "Health Check"; url = "/health" },
    @{ name = "Learning Statistics"; url = "/learning_statistics" },
    @{ name = "System Status"; url = "/system_status" }
)

foreach ($test in $integrationTests) {
    try {
        $result = Invoke-RestMethod -Uri "http://10.20.30.16:8881$($test.url)"
        Write-Host "✅ $($test.name): Working"
    } catch {
        Write-Warning "❌ $($test.name): Failed"
    }
}
```

### 2. Analytics Dashboard Integration (ash-dash)

**Configure Analytics Integration:**
```powershell
# Verify analytics webhook configuration
if ($env:ENABLE_ANALYTICS_EXPORT -eq "true" -and $env:ANALYTICS_WEBHOOK_URL) {
    Write-Host "=== Analytics Integration ==="
    
    # Test webhook endpoint (if ash-dash is running)
    try {
        Test-NetConnection -ComputerName 127.0.0.1 -Port 8883
        Write-Host "✅ Analytics dashboard port accessible"
        
        # Test webhook endpoint
        $webhook = Invoke-RestMethod -Uri "http://127.0.0.1:8883/health" -ErrorAction SilentlyContinue
        Write-Host "✅ Analytics dashboard responding"
    } catch {
        Write-Warning "⚠️ Analytics dashboard not accessible - this is optional"
    }
} else {
    Write-Host "Analytics export disabled - can be enabled later"
}
```

### 3. Testing Suite Integration (ash-thrash)

**Configure Testing Integration:**
```powershell
# Test integration with ash-thrash if available
Write-Host "=== Testing Suite Integration ==="

try {
    Test-NetConnection -ComputerName 127.0.0.1 -Port 8884
    Write-Host "✅ Testing suite port accessible"
    
    # If ash-thrash is running, test the integration
    $testHealth = Invoke-RestMethod -Uri "http://127.0.0.1:8884/health" -ErrorAction SilentlyContinue
    Write-Host "✅ Testing suite responding"
} catch {
    Write-Host "Testing suite not running - this is optional for deployment"
}
```

---

## 📊 Monitoring & Maintenance

### 1. Automated Monitoring Setup

**Create Monitoring Script:**
```powershell
# Create monitoring script: monitor_ash_nlp.ps1
$monitoringScript = @'
# Ash NLP Server Monitoring Script v2.1
param(
    [int]$IntervalSeconds = 300,  # 5 minutes
    [string]$LogFile = "C:\Deployments\ash-nlp\logs\monitoring.log"
)

function Write-MonitorLog {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry
    Add-Content -Path $LogFile -Value $logEntry
}

function Test-ServiceHealth {
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:8881/health" -TimeoutSec 30
        
        if ($health.status -eq "healthy") {
            Write-MonitorLog "Service health check passed"
            return $true
        } else {
            Write-MonitorLog "Service health check failed: $($health.status)" "WARNING"
            return $false
        }
    } catch {
        Write-MonitorLog "Service health check error: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-LearningSystem {
    try {
        $learning = Invoke-RestMethod -Uri "http://localhost:8881/learning_statistics" -TimeoutSec 15
        
        if ($learning.system_status -eq "active") {
            Write-MonitorLog "Learning system active - Adjustments today: $($learning.daily_limits.used_today)"
            return $true
        } else {
            Write-MonitorLog "Learning system inactive" "WARNING"
            return $false
        }
    } catch {
        Write-MonitorLog "Learning system check error: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-Performance {
    try {
        $perf = Invoke-RestMethod -Uri "http://localhost:8881/performance_metrics?period=1hour" -TimeoutSec 15
        
        $avgResponse = $perf.response_time_metrics.average_ms
        $successRate = $perf.request_metrics.success_rate
        
        Write-MonitorLog "Performance - Avg Response: ${avgResponse}ms, Success Rate: $([math]::Round($successRate * 100, 1))%"
        
        if ($avgResponse -gt 200) {
            Write-MonitorLog "High response time detected: ${avgResponse}ms" "WARNING"
        }
        
        if ($successRate -lt 0.95) {
            Write-MonitorLog "Low success rate detected: $([math]::Round($successRate * 100, 1))%" "WARNING"
        }
        
        return $true
    } catch {
        Write-MonitorLog "Performance check error: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Main monitoring loop
Write-MonitorLog "Starting Ash NLP Server monitoring (interval: ${IntervalSeconds}s)"

while ($true) {
    $healthOk = Test-ServiceHealth
    $learningOk = Test-LearningSystem
    $perfOk = Test-Performance
    
    if (-not $healthOk) {
        Write-MonitorLog "Attempting service restart..." "WARNING"
        try {
            Set-Location "C:\Deployments\ash-nlp"
            docker-compose restart ash-nlp
            Write-MonitorLog "Service restart initiated"
        } catch {
            Write-MonitorLog "Service restart failed: $($_.Exception.Message)" "ERROR"
        }
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}
'@

# Save monitoring script
$monitoringScript | Out-File -FilePath "C:\Deployments\ash-nlp\scripts\monitor_ash_nlp.ps1" -Encoding UTF8
Write-Host "Monitoring script created: C:\Deployments\ash-nlp\scripts\monitor_ash_nlp.ps1"
```

**Schedule Monitoring:**
```powershell
# Create scheduled task for monitoring
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Deployments\ash-nlp\scripts\monitor_ash_nlp.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "Ash NLP Server Monitor" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
Write-Host "Monitoring scheduled task created"
```

### 2. Backup Strategy

**Create Backup Script:**
```powershell
# Create backup script: backup_learning_data.ps1
$backupScript = @'
# Ash NLP Learning Data Backup Script v2.1
param(
    [string]$BackupPath = "C:\Backups\ash-nlp",
    [int]$RetentionDays = 30
)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = Join-Path $BackupPath "backup_$timestamp"

# Create backup directory
New-Item -Path $backupDir -ItemType Directory -Force

# Backup learning data
Copy-Item -Path "C:\Deployments\ash-nlp\learning_data\*" -Destination "$backupDir\learning_data" -Recurse -Force

# Backup configuration
Copy-Item -Path "C:\Deployments\ash-nlp\.env" -Destination "$backupDir\.env" -Force
Copy-Item -Path "C:\Deployments\ash-nlp\docker-compose.yml" -Destination "$backupDir\docker-compose.yml" -Force

# Compress backup
Compress-Archive -Path "$backupDir\*" -DestinationPath "$backupDir.zip" -Force
Remove-Item -Path $backupDir -Recurse -Force

# Clean old backups
Get-ChildItem -Path $BackupPath -Filter "backup_*.zip" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$RetentionDays) } | 
    Remove-Item -Force

Write-Host "Backup completed: $backupDir.zip"
'@

# Save backup script
New-Item -Path "C:\Deployments\ash-nlp\scripts" -ItemType Directory -Force
$backupScript | Out-File -FilePath "C:\Deployments\ash-nlp\scripts\backup_learning_data.ps1" -Encoding UTF8

# Schedule daily backup
$backupAction = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Deployments\ash-nlp\scripts\backup_learning_data.ps1"
$backupTrigger = New-ScheduledTaskTrigger -Daily -At "2:00AM"

Register-ScheduledTask -TaskName "Ash NLP Daily Backup" -Action $backupAction -Trigger $backupTrigger -Principal $principal
Write-Host "Daily backup scheduled for 2:00 AM"
```

### 3. Log Management

**Configure Log Rotation:**
```powershell
# Create log rotation script
$logRotationScript = @'
# Log rotation for Ash NLP Server
$logDir = "C:\Deployments\ash-nlp\logs"
$maxSizeMB = 100
$retentionDays = 30

# Rotate large log files
Get-ChildItem -Path $logDir -Filter "*.log" | ForEach-Object {
    if ($_.Length -gt ($maxSizeMB * 1MB)) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $newName = "$($_.BaseName)_$timestamp$($_.Extension)"
        Rename-Item -Path $_.FullName -NewName $newName
        
        # Create new empty log file
        New-Item -Path $_.FullName -ItemType File -Force
        Write-Host "Rotated log: $($_.Name) -> $newName"
    }
}

# Clean old log files
Get-ChildItem -Path $logDir -Filter "*.log" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$retentionDays) } | 
    Remove-Item -Force

Write-Host "Log rotation completed"
'@

$logRotationScript | Out-File -FilePath "C:\Deployments\ash-nlp\scripts\rotate_logs.ps1" -Encoding UTF8

# Schedule weekly log rotation
$logAction = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Deployments\ash-nlp\scripts\rotate_logs.ps1"
$logTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "3:00AM"

Register-ScheduledTask -TaskName "Ash NLP Log Rotation" -Action $logAction -Trigger $logTrigger -Principal $principal
Write-Host "Weekly log rotation scheduled for Sunday 3:00 AM"
```

---

## 🐛 Troubleshooting

### Common Deployment Issues

#### Issue: Docker Desktop Not Starting

**Symptoms:**
- Docker commands fail with "Docker daemon not running"
- Docker Desktop shows "Starting..." indefinitely

**Solutions:**
```powershell
# 1. Restart Docker Desktop service
Stop-Service -Name "com.docker.service"
Start-Service -Name "com.docker.service"

# 2. Reset Docker Desktop
& "C:\Program Files\Docker\Docker\Docker Desktop.exe" --factory-reset

# 3. Check WSL2 status
wsl --status
wsl --update

# 4. Restart computer if needed
Restart-Computer
```

#### Issue: GPU Not Available in Container

**Symptoms:**
- `nvidia-smi` works on host but not in container
- Models loading on CPU instead of GPU

**Solutions:**
```powershell
# 1. Verify NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# 2. Check Docker Compose GPU configuration
# Ensure docker-compose.yml includes:
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
#           count: 1
#           capabilities: [gpu]

# 3. Update NVIDIA drivers
# Download latest drivers from nvidia.com

# 4. Restart Docker Desktop after driver update
```

#### Issue: Models Not Loading

**Symptoms:**
- Service starts but models don't load
- Health check shows "AI models: error"

**Solutions:**
```powershell
# 1. Check disk space
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, FreeSpace

# 2. Check internet connectivity
Test-NetConnection -ComputerName huggingface.co -Port 443

# 3. Clear model cache and retry
Remove-Item -Path "C:\Deployments\ash-nlp\models\cache\*" -Recurse -Force
docker-compose restart ash-nlp

# 4. Check Hugging Face token (if needed)
# Add HUGGINGFACE_HUB_TOKEN to .env file

# 5. Manual model download test
docker-compose exec ash-nlp python -c "from transformers import AutoModel; AutoModel.from_pretrained('rafalposwiata/deproberta-large-depression')"
```

#### Issue: High Memory Usage

**Symptoms:**
- System running out of memory
- Container getting killed (OOMKilled)

**Solutions:**
```powershell
# 1. Check current memory usage
docker stats ash_nlp_server --no-stream

# 2. Adjust memory limits in docker-compose.yml
# deploy:
#   resources:
#     limits:
#       memory: 6G  # Reduce from 8G

# 3. Optimize model precision
# In .env file:
# MODEL_PRECISION=float16
# MAX_BATCH_SIZE=16  # Reduce from 32

# 4. Restart with new limits
docker-compose down
docker-compose up -d
```

#### Issue: Learning System Not Working

**Symptoms:**
- Learning statistics show "inactive"
- False positive/negative reports not processed

**Solutions:**
```powershell
# 1. Check learning system configuration
cat .env | Select-String "LEARNING"

# 2. Verify learning data directory permissions
Test-Path "C:\Deployments\ash-nlp\learning_data"
Get-Acl "C:\Deployments\ash-nlp\learning_data"

# 3. Check logs for learning system errors
docker-compose logs ash-nlp | Select-String -Pattern "learning|error"

# 4. Reset learning system (CAUTION - loses learning data)
# Stop-Service, backup learning_data, clear directory, restart
```

### Performance Optimization

#### Slow Response Times

**Diagnostic Steps:**
```powershell
# 1. Check current performance
$perf = Invoke-RestMethod -Uri "http://localhost:8881/performance_metrics"
Write-Host "Average response time: $($perf.response_time_metrics.average_ms)ms"

# 2. Check resource utilization
$status = Invoke-RestMethod -Uri "http://localhost:8881/system_status"
Write-Host "CPU: $($status.hardware_status.cpu_usage)%"
Write-Host "Memory: $($status.hardware_status.memory_usage.percentage)%"
Write-Host "GPU: $($status.hardware_status.gpu_status.utilization_percentage)%"

# 3. Optimize settings in .env
# INFERENCE_THREADS=8
# MAX_CONCURRENT_REQUESTS=20
# ENABLE_MODEL_CACHING=true

# 4. Restart with optimizations
docker-compose restart ash-nlp
```

#### High CPU Usage

**Optimization Steps:**
```powershell
# 1. Check CPU thread usage
# In .env file, adjust:
# INFERENCE_THREADS=6  # Reduce from 8
# MAX_CONCURRENT_REQUESTS=15  # Reduce from 25

# 2. Enable GPU processing if available
# DEVICE=cuda  # Force GPU usage

# 3. Implement request throttling
# RATE_LIMIT_REQUESTS_PER_MINUTE=40  # Reduce from 60

# 4. Monitor improvement
docker stats ash_nlp_server --no-stream
```

### Emergency Recovery

#### Complete System Recovery

**Recovery Steps:**
```powershell
# 1. Stop all services
Set-Location "C:\Deployments\ash-nlp"
docker-compose down

# 2. Backup current state (if possible)
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item -Path "learning_data" -Destination "learning_data_backup_$timestamp" -Recurse -ErrorAction SilentlyContinue

# 3. Reset to known good state
git stash
git checkout main
git pull origin main

# 4. Restore configuration
Copy-Item -Path ".env.backup" -Destination ".env" -ErrorAction SilentlyContinue

# 5. Clear Docker cache
docker system prune -a -f

# 6. Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# 7. Verify recovery
Start-Sleep -Seconds 60
Invoke-RestMethod -Uri "http://localhost:8881/health"
```

---

## 📋 Post-Deployment Checklist

### Deployment Verification

**Essential Checks:**
- [ ] Service health endpoint returns "healthy"
- [ ] Both AI models loaded successfully
- [ ] Learning system status shows "active"
- [ ] GPU utilization visible (if GPU enabled)
- [ ] Network connectivity to Ash bot verified
- [ ] Log files being created and rotated
- [ ] Backup system operational

**Performance Validation:**
- [ ] Response times < 100ms average
- [ ] Memory usage < 6GB
- [ ] CPU usage < 30% average
- [ ] Success rate > 99%
- [ ] Learning system accepting feedback

**Integration Testing:**
- [ ] Ash bot can connect and analyze messages
- [ ] Analytics dashboard receiving data (if enabled)
- [ ] Testing suite can run against NLP server (if enabled)
- [ ] Crisis Response team can access learning commands

**Security & Monitoring:**
- [ ] Firewall rules configured correctly
- [ ] Monitoring scripts active
- [ ] Backup schedule verified
- [ ] Log rotation working
- [ ] Access controls in place

### Documentation Completion

**Team Notification:**
- [ ] Crisis Response team notified of deployment
- [ ] Team guide distributed and reviewed
- [ ] Learning system training scheduled
- [ ] Emergency contact procedures updated

**Documentation Updates:**
- [ ] Deployment details documented
- [ ] Configuration backed up
- [ ] Network topology updated
- [ ] Maintenance procedures reviewed

---

## 🎉 Deployment Success!

**Congratulations! You have successfully deployed Ash NLP Server v2.1 with:**

✅ **Production-ready AI crisis detection** optimized for your RTX 3050 + Ryzen 7 7700X setup  
✅ **Advanced learning system** that adapts to community feedback  
✅ **Comprehensive monitoring** and automated maintenance  
✅ **Full integration** with The Alphabet Cartel ecosystem  
✅ **Enterprise-grade reliability** with backup and recovery procedures  

### Next Steps

1. **Train the Crisis Response Team** - Schedule training on the new learning system features
2. **Begin Learning Data Collection** - Start gathering feedback to improve AI accuracy
3. **Monitor Performance** - Use the monitoring tools to ensure optimal operation
4. **Plan Regular Maintenance** - Schedule weekly reviews of system performance
5. **Prepare for Growth** - Monitor usage patterns and plan for scaling

### Quick Reference

**Service URL:** `http://10.20.30.16:8881`  
**Health Check:** `http://10.20.30.16:8881/health`  
**Learning Stats:** `http://10.20.30.16:8881/learning_statistics`  
**Documentation:** `http://10.20.30.16:8881/docs`

**Emergency Contacts:**
- Technical Team: Discord #tech-support
- Crisis Response Lead: [As designated]
- System Administrator: [As designated]

---

**💜 Thank you for deploying advanced AI to help keep The Alphabet Cartel community safe and supported!**

*For questions about this deployment guide, create a GitHub issue or contact the technical team via Discord.*

**Last Updated:** July 27, 2025 | **Version:** 2.1 | **Status:** Production Ready