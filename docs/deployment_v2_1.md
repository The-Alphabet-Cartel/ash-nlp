# Ash NLP Server - Deployment Guide v2.1

**Production Deployment for Windows 11 AI Server (10.20.30.253)**

Part of The Alphabet Cartel's [Ash Crisis Detection & Community Support Ecosystem](https://github.com/the-alphabet-cartel/ash)

---

## 🎯 Deployment Overview

This guide covers production deployment of the Ash NLP Server on the dedicated Windows 11 AI server (10.20.30.253) with NVIDIA RTX 3050 GPU acceleration.

### Server Specifications
- **Server IP**: 10.20.30.253
- **Operating System**: Windows 11 Pro
- **CPU**: AMD Ryzen 7 7700X
- **RAM**: 64GB DDR5
- **GPU**: NVIDIA RTX 3050 (8GB VRAM)
- **API Port**: 8881

### Integration Architecture
- **Ash Bot Server**: 10.20.30.253:8882 (Debian 12, RTX 3060)
- **Ash Dashboard**: 10.20.30.253:8883
- **Ash Testing**: 10.20.30.253:8884
- **Network**: Internal 10.20.30.x subnet

## 🔧 Prerequisites

### System Requirements

**Windows 11 Configuration:**
```powershell
# Verify Windows version
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion

# Required: Windows 11 Pro (22H2 or later)
# Required: WSL2 enabled for Docker Desktop
```

**NVIDIA GPU Setup:**
```powershell
# Install NVIDIA drivers (535+ required)
# Verify GPU detection
nvidia-smi

# Expected output: RTX 3050, Driver Version: 535+, CUDA Version: 12.0+
```

**Docker Desktop:**
```powershell
# Install Docker Desktop for Windows
# Enable WSL2 backend
# Enable GPU support in Docker settings

# Verify Docker GPU access
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

**Network Configuration:**
```powershell
# Verify network connectivity
ping 10.20.30.253  # Ash bot server
Test-NetConnection -ComputerName 10.20.30.253 -Port 8882
Test-NetConnection -ComputerName 10.20.30.253 -Port 8883
Test-NetConnection -ComputerName 10.20.30.253 -Port 8884

# Configure Windows Firewall
New-NetFirewallRule -DisplayName "Ash NLP Server" -Direction Inbound -Protocol TCP -LocalPort 8881 -Action Allow
```

## 🚀 Production Deployment

### 1. Environment Setup

**Create Deployment Directory:**
```powershell
# Create standardized deployment location
$deployPath = "C:\Deployments\ash-nlp"
New-Item -Path $deployPath -ItemType Directory -Force
Set-Location $deployPath

# Clone repository
git clone https://github.com/the-alphabet-cartel/ash-nlp.git .
```

**Environment Configuration:**
```powershell
# Copy environment template
Copy-Item .env.template .env

# Edit with production settings
notepad .env
```

**Production .env Configuration:**
```bash
# Server Configuration
NLP_SERVICE_HOST=0.0.0.0
NLP_SERVICE_PORT=8881
PYTHONUNBUFFERED=1

# Hardware Optimization
DEVICE=auto  # Auto-detect RTX 3050
GPU_MEMORY_FRACTION=0.8
INFERENCE_THREADS=6  # Optimized for Ryzen 7 7700X
MAX_BATCH_SIZE=32

# AI Models
DEPRESSION_MODEL=rafalposwiata/deproberta-large-depression
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL_CACHE_DIR=./models/cache

# Learning System
ENABLE_LEARNING_SYSTEM=true
LEARNING_RATE=0.1
MAX_LEARNING_ADJUSTMENTS_PER_DAY=50
LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json

# Integration Settings
ENABLE_ANALYTICS_EXPORT=true
ANALYTICS_WEBHOOK_URL=http://10.20.30.253:8883/webhook/nlp_metrics

# Performance Monitoring
ENABLE_PERFORMANCE_LOGGING=true
LOG_LEVEL=INFO
LOG_ROTATION_SIZE=100MB
LOG_RETENTION_DAYS=30

# Security
API_KEY_REQUIRED=false  # Internal network only
CORS_ORIGINS=["http://10.20.30.253:8882", "http://10.20.30.253:8883"]

# Optional: Hugging Face token for model downloads
# HUGGINGFACE_HUB_TOKEN=your_token_here
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

## 🚀 Production Deployment

### 1. Initial Deployment

**Start Services:**
```powershell
# Navigate to deployment directory
Set-Location C:\Deployments\ash-nlp

# Create external network (if not exists)
docker network create ash_network

# Pull latest images
docker-compose pull

# Start services in production mode
docker-compose up -d

# Monitor startup logs
docker-compose logs -f ash-nlp
```

**Verify Deployment:**
```powershell
# Health check
Invoke-RestMethod -Uri "http://10.20.30.253:8881/health" -Method GET

# Check GPU utilization
nvidia-smi

# Test analysis endpoint
$testPayload = @{
    message = "feeling really down today"
    user_id = "test_user"
    channel_id = "test_channel"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://10.20.30.253:8881/analyze" -Method POST -Body $testPayload -ContentType "application/json"
```

### 2. Performance Optimization

**GPU Optimization:**
```powershell
# Check GPU memory usage
docker exec ash_nlp_server nvidia-smi

# Monitor GPU utilization during inference
while ($true) {
    nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits
    Start-Sleep 1
}
```

**Memory Optimization:**
```powershell
# Monitor container memory usage
docker stats ash_nlp_server

# Check system memory
Get-WmiObject -Class Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
```

### 3. Integration Validation

**Test Ash Bot Integration:**
```powershell
# From Ash bot server (10.20.30.253), test connectivity
# This should be run on the bot server
curl http://10.20.30.253:8881/health

# Test analysis from bot server
curl -X POST http://10.20.30.253:8881/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "test integration", "user_id": "bot_test", "channel_id": "integration_test"}'
```

**Test Dashboard Integration:**
```powershell
# Verify analytics webhook is reachable
Test-NetConnection -ComputerName 10.20.30.253 -Port 8883

# Check analytics export is working
docker-compose logs ash-nlp | Select-String "analytics"
```

**Test Testing Suite Integration:**
```powershell
# Verify testing suite can reach NLP server
# This should be run from the testing server
curl http://10.20.30.253:8881/health
curl http://10.20.30.253:8881/model_status
```

## 📊 Monitoring & Maintenance

### Performance Monitoring

**System Metrics:**
```powershell
# Create monitoring script: monitor_ash_nlp.ps1
while ($true) {
    Write-Host "=== Ash NLP Server Status $(Get-Date) ==="
    
    # Docker container status
    docker ps --filter "name=ash_nlp_server" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    # GPU utilization
    nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader
    
    # API health check
    try {
        $health = Invoke-RestMethod -Uri "http://10.20.30.253:8881/health" -TimeoutSec 5
        Write-Host "API Status: $($health.status)"
    } catch {
        Write-Host "API Status: ERROR - $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Memory usage
    $memory = Get-WmiObject -Class Win32_OperatingSystem
    $usedMemory = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / 1MB), 2)
    $totalMemory = [math]::Round(($memory.TotalVisibleMemorySize / 1MB), 2)
    Write-Host "System Memory: $usedMemory GB / $totalMemory GB"
    
    Write-Host "==========================================`n"
    Start-Sleep 30
}
```

**Learning System Monitoring:**
```powershell
# Check learning system status
$learningStats = Invoke-RestMethod -Uri "http://10.20.30.253:8881/learning_statistics"
$learningStats | ConvertTo-Json -Depth 3

# Monitor learning adjustments
Get-Content "C:\Deployments\ash-nlp\learning_data\adjustments.json" | ConvertFrom-Json
```

### Backup Procedures

**Automated Backup Script:**
```powershell
# Create backup script: backup_ash_nlp.ps1
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "C:\Deployments\ash-nlp\backups\$timestamp"

# Create backup directory
New-Item -Path $backupDir -ItemType Directory -Force

# Backup learning data
Copy-Item -Path "C:\Deployments\ash-nlp\learning_data\*" -Destination "$backupDir\learning_data\" -Recurse -Force

# Backup configuration
Copy-Item -Path "C:\Deployments\ash-nlp\.env" -Destination "$backupDir\.env" -Force
Copy-Item -Path "C:\Deployments\ash-nlp\docker-compose.yml" -Destination "$backupDir\docker-compose.yml" -Force

# Backup logs (last 24 hours)
$logFiles = Get-ChildItem "C:\Deployments\ash-nlp\logs\" -Filter "*.log" | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}
Copy-Item -Path $logFiles -Destination "$backupDir\logs\" -Force

# Create backup manifest
@{
    timestamp = $timestamp
    backup_type = "scheduled"
    included_files = @("learning_data", "configuration", "recent_logs")
    ash_nlp_version = (docker inspect ash_nlp_server --format='{{.Config.Image}}')
} | ConvertTo-Json | Out-File "$backupDir\manifest.json"

Write-Host "Backup completed: $backupDir"

# Cleanup old backups (keep last 30 days)
Get-ChildItem "C:\Deployments\ash-nlp\backups\" | Where-Object {$_.CreationTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Recurse -Force
```

### Update Procedures

**Production Update Process:**
```powershell
# 1. Create pre-update backup
& "C:\Deployments\ash-nlp\scripts\backup_ash_nlp.ps1"

# 2. Pull latest image
docker-compose pull

# 3. Stop current service
docker-compose stop ash-nlp

# 4. Start updated service
docker-compose up -d ash-nlp

# 5. Verify deployment
Start-Sleep 30
$health = Invoke-RestMethod -Uri "http://10.20.30.253:8881/health"
if ($health.status -eq "healthy") {
    Write-Host "Update successful!" -ForegroundColor Green
} else {
    Write-Host "Update failed - rolling back..." -ForegroundColor Red
    # Rollback procedure would go here
}

# 6. Test integration
curl http://10.20.30.253:8881/analyze -X POST -H "Content-Type: application/json" -d '{"message": "post-update test"}'
```

## 🚨 Troubleshooting

### Common Issues

**Container Won't Start:**
```powershell
# Check Docker logs
docker-compose logs ash-nlp

# Common causes and solutions:
# 1. Port conflict
netstat -an | findstr :8881

# 2. GPU access issues
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# 3. Insufficient memory
Get-WmiObject -Class Win32_OperatingSystem | Select-Object FreePhysicalMemory
```

**API Not Responding:**
```powershell
# Check container status
docker ps --filter "name=ash_nlp_server"

# Check network connectivity
Test-NetConnection -ComputerName 10.20.30.253 -Port 8881

# Check firewall rules
Get-NetFirewallRule -DisplayName "Ash NLP Server"
```

**Learning System Issues:**
```powershell
# Check learning data permissions
icacls "C:\Deployments\ash-nlp\learning_data"

# Reset learning system if corrupted
Remove-Item "C:\Deployments\ash-nlp\learning_data\adjustments.json" -Force
docker-compose restart ash-nlp
```

### Emergency Recovery

**Complete System Recovery:**
```powershell
# 1. Stop all services
docker-compose down

# 2. Clear corrupt data (CAUTION: Data loss)
Remove-Item "C:\Deployments\ash-nlp\models\cache\*" -Recurse -Force
Remove-Item "C:\Deployments\ash-nlp\learning_data\*" -Recurse -Force

# 3. Restore from backup (if available)
$latestBackup = Get-ChildItem "C:\Deployments\ash-nlp\backups\" | Sort-Object CreationTime -Descending | Select-Object -First 1
Copy-Item -Path "$($latestBackup.FullName)\learning_data\*" -Destination "C:\Deployments\ash-nlp\learning_data\" -Recurse -Force

# 4. Restart services
docker-compose up -d

# 5. Verify recovery
Start-Sleep 60
Invoke-RestMethod -Uri "http://10.20.30.253:8881/health"
```

## 📞 Support

### Production Support
- **GitHub Issues**: [ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Discord Support**: #ash-nlp-support in https://discord.gg/alphabetcartel
- **Emergency Contact**: Use Discord for urgent production issues

### Documentation References
- **[API Documentation](tech/API_v2_1.md)** - Complete API reference
- **[Troubleshooting Guide](tech/troubleshooting_v2_1.md)** - Detailed problem resolution
- **[Team Guide](team/team_guide_v2_1.md)** - Operations procedures

---

## 🔐 Security Considerations

### Network Security
- **Internal Network Only**: Server accessible only on 10.20.30.x subnet
- **Firewall Configuration**: Only port 8881 exposed for API access
- **No External Access**: No internet-facing endpoints

### Data Security
- **Ephemeral Processing**: No message content stored permanently
- **Local AI Models**: All processing occurs on community-controlled hardware
- **Audit Logging**: System actions logged without sensitive content

### Access Control
- **Physical Security**: Server located in secure facility
- **Administrative Access**: Limited to authorized personnel
- **Container Isolation**: Docker provides process isolation

---

**The Alphabet Cartel** - Building inclusive gaming communities through technology.

**Discord:** https://discord.gg/alphabetcartel | **Website:** https://alphabetcartel.org

*Deployment completed successfully! The NLP server is ready to support our community.*