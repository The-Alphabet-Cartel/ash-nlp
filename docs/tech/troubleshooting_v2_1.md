# Ash NLP Server - Troubleshooting Guide v2.1

**Problem Diagnosis and Resolution for Windows 11 AI Server (10.20.30.253)**

Part of The Alphabet Cartel's [Ash Crisis Detection & Community Support Ecosystem](https://github.com/the-alphabet-cartel/ash)

---

## 🎯 Quick Reference

### Emergency Contacts
- **Discord #tech-support**: Immediate technical assistance
- **GitHub Issues**: [ash-nlp/issues](https://github.com/the-alphabet-cartel/ash-nlp/issues)
- **Emergency Escalation**: Crisis response team lead via Discord DM

### Server Information
- **Server IP**: 10.20.30.253
- **API Port**: 8881
- **OS**: Windows 11 Pro
- **Hardware**: Ryzen 7 7700X, 64GB RAM, RTX 3050 8GB
- **Container**: ash_nlp_server

### Quick Health Check
```powershell
# Basic health check
curl http://10.20.30.253:8881/health

# Container status
docker ps --filter "name=ash_nlp_server"

# GPU status
nvidia-smi

# System resources
Get-WmiObject -Class Win32_OperatingSystem | Select-Object FreePhysicalMemory
```

---

## 🚨 Critical Issues (High Priority)

### Service Completely Down

**Symptoms:**
- API endpoints not responding (connection refused)
- Container not running
- Health check failures

**Immediate Diagnosis:**
```powershell
# Check if container is running
docker ps --filter "name=ash_nlp_server"

# If not running, check why it stopped
docker ps -a --filter "name=ash_nlp_server"
docker logs ash_nlp_server --tail 50

# Check if Docker daemon is running
docker info
```

**Solutions:**

**1. Container Stopped Unexpectedly:**
```powershell
# Restart the container
cd C:\Deployments\ash-nlp
docker-compose up -d ash-nlp

# Monitor startup
docker-compose logs -f ash-nlp

# Wait for startup (models loading can take 2-3 minutes)
Start-Sleep 180
curl http://10.20.30.253:8881/health
```

**2. Docker Daemon Issues:**
```powershell
# Restart Docker Desktop
Stop-Service docker
Start-Service docker

# Or restart Docker Desktop application
Get-Process "*Docker Desktop*" | Stop-Process -Force
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Wait for Docker to fully start
Start-Sleep 60
docker info
```

**3. System-Level Issues:**
```powershell
# Check if Windows needs restart
Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2,3} -MaxEvents 10

# Check disk space
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, @{Name="Free(GB)";Expression={[math]::round($_.FreeSpace/1GB,2)}}

# Check memory usage
Get-WmiObject -Class Win32_OperatingSystem | Select-Object @{Name="Memory Usage(%)";Expression={[math]::round((($_.TotalVisibleMemorySize - $_.FreePhysicalMemory)/$_.TotalVisibleMemorySize)*100,2)}}
```

### GPU Access Failed

**Symptoms:**
- Container starts but analysis fails
- "CUDA device not available" errors
- Performance significantly degraded

**Diagnosis:**
```powershell
# Check if GPU is detected by system
nvidia-smi

# Check GPU access in Docker
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# Check container GPU access
docker exec ash_nlp_server nvidia-smi

# Check container logs for GPU errors
docker logs ash_nlp_server | Select-String "GPU\|CUDA\|cuda"
```

**Solutions:**

**1. NVIDIA Driver Issues:**
```powershell
# Check driver version (needs 535+)
nvidia-smi

# If driver issues, reinstall NVIDIA drivers
# Download from https://www.nvidia.com/drivers
# Install with "Clean Installation" option checked

# Verify after installation
nvidia-smi
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

**2. Docker GPU Configuration:**
```powershell
# Verify Docker Desktop GPU settings
# 1. Open Docker Desktop
# 2. Go to Settings > Resources > WSL Integration
# 3. Ensure WSL2 integration enabled
# 4. Go to Settings > Features in development
# 5. Enable "Use containerd for pulling and storing images"

# Restart Docker after changes
Stop-Service docker
Start-Service docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

**3. Container GPU Access:**
```powershell
# Check docker-compose.yml has correct GPU configuration
# Should include:
<# 
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
#>

# Restart container with GPU access
cd C:\Deployments\ash-nlp
docker-compose down
docker-compose up -d
```

### High CPU/Memory Usage

**Symptoms:**
- System extremely slow
- Out of memory errors
- Container restarts due to resource limits

**Diagnosis:**
```powershell
# Check system resource usage
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Check container resource usage
docker stats ash_nlp_server --no-stream

# Check memory pressure
Get-WmiObject -Class Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
```

**Solutions:**

**1. Memory Optimization:**
```powershell
# Update .env with memory optimization
# GPU_MEMORY_FRACTION=0.6  # Reduce from 0.8
# MAX_BATCH_SIZE=16        # Reduce from 32
# INFERENCE_THREADS=4      # Reduce from 6

# Restart container with new settings
cd C:\Deployments\ash-nlp
docker-compose down
docker-compose up -d
```

**2. Clear Memory Pressure:**
```powershell
# Clear Docker caches
docker system prune -f

# Clear temporary files
Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue

# Restart container
docker-compose restart ash-nlp
```

**3. System Cleanup:**
```powershell
# Run Windows cleanup
cleanmgr /sagerun:1

# Clear Windows update cache
Stop-Service wuauserv
Remove-Item C:\Windows\SoftwareDistribution\Download\* -Recurse -Force
Start-Service wuauserv
```

---

## ⚠️ High Priority Issues

### API Responding But Analysis Failing

**Symptoms:**
- Health endpoint returns healthy
- Analysis requests return errors or timeouts
- Inconsistent response times

**Diagnosis:**
```powershell
# Test analysis endpoint directly
$testPayload = @{
    message = "test message for diagnosis"
    user_id = "test_user"
    channel_id = "test_channel"
} | ConvertTo-Json

# Test analysis
try {
    $response = Invoke-RestMethod -Uri "http://10.20.30.253:8881/analyze" -Method POST -Body $testPayload -ContentType "application/json" -TimeoutSec 30
    Write-Host "Analysis successful: $($response.risk_level)"
} catch {
    Write-Host "Analysis failed: $($_.Exception.Message)"
}

# Check model status
Invoke-RestMethod -Uri "http://10.20.30.253:8881/model_status"

# Check container logs for errors
docker logs ash_nlp_server --tail 100 | Select-String "ERROR\|CRITICAL\|Exception"
```

**Solutions:**

**1. Model Loading Issues:**
```powershell
# Check if models are properly loaded
curl http://10.20.30.253:8881/model_status

# If models not loaded, restart container
docker-compose restart ash-nlp

# Monitor model loading (can take 2-3 minutes)
docker-compose logs -f ash-nlp | Select-String "model\|loading\|loaded"

# If model download issues, clear cache and restart
Remove-Item C:\Deployments\ash-nlp\models\cache\* -Recurse -Force
docker-compose restart ash-nlp
```

**2. Analysis Timeout Issues:**
```powershell
# Increase timeout in .env
# ANALYSIS_TIMEOUT=60  # Increase from default 30

# Reduce concurrent processing
# MAX_CONCURRENT_ANALYSES=3  # Reduce from default 5

# Restart with new settings
docker-compose down
docker-compose up -d
```

**3. Memory/Performance Issues:**
```powershell
# Check if system is under memory pressure
$memory = Get-WmiObject -Class Win32_OperatingSystem
$memoryUsage = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize * 100), 2)
Write-Host "Memory usage: $memoryUsage%"

if ($memoryUsage -gt 85) {
    Write-Host "High memory usage detected - optimizing..."
    
    # Restart container to clear memory
    docker-compose restart ash-nlp
    
    # Consider reducing batch size
    # Update .env: MAX_BATCH_SIZE=8
}
```

### Learning System Malfunction

**Symptoms:**
- Feedback submissions failing
- Learning statistics show errors
- Model performance degrading

**Diagnosis:**
```powershell
# Check learning system status
curl http://10.20.30.253:8881/learning_statistics

# Check learning data directory
Get-ChildItem C:\Deployments\ash-nlp\learning_data\ -Recurse

# Test feedback submission
$feedback = @{
    analysis_id = "test_analysis_123"
    feedback_type = "correct_classification"
    correct_classification = "medium"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://10.20.30.253:8881/learning_feedback" -Method POST -Body $feedback -ContentType "application/json"
    Write-Host "Feedback test successful"
} catch {
    Write-Host "Feedback test failed: $($_.Exception.Message)"
}

# Check learning logs
docker logs ash_nlp_server | Select-String "learning\|feedback\|adjustment"
```

**Solutions:**

**1. Learning Data Corruption:**
```powershell
# Backup current learning data
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item C:\Deployments\ash-nlp\learning_data\ "C:\Deployments\ash-nlp\backups\learning_backup_$timestamp\" -Recurse

# Check data integrity
Get-Content C:\Deployments\ash-nlp\learning_data\adjustments.json | ConvertFrom-Json

# If corrupted, restore from recent backup or reset
# Remove-Item C:\Deployments\ash-nlp\learning_data\adjustments.json -Force
# docker-compose restart ash-nlp
```

**2. Permission Issues:**
```powershell
# Check directory permissions
icacls C:\Deployments\ash-nlp\learning_data

# Fix permissions if needed
icacls C:\Deployments\ash-nlp\learning_data /grant "Everyone:(OI)(CI)F" /T

# Restart container
docker-compose restart ash-nlp
```

**3. Learning System Reset (Last Resort):**
```powershell
# Create backup first
Copy-Item C:\Deployments\ash-nlp\learning_data\ "C:\Deployments\ash-nlp\backups\pre_reset_backup\" -Recurse

# Reset learning system
Remove-Item C:\Deployments\ash-nlp\learning_data\* -Recurse -Force

# Restart container
docker-compose restart ash-nlp

# Verify reset
curl http://10.20.30.253:8881/learning_statistics
```

### Integration Failures

**Symptoms:**
- Ash bot can't connect to NLP server
- Dashboard not receiving analytics
- Testing suite failures

**Diagnosis:**
```powershell
# Test network connectivity from bot server (10.20.30.253)
Test-NetConnection -ComputerName 10.20.30.253 -Port 8881

# Test from local machine
curl http://10.20.30.253:8881/health

# Check firewall settings
Get-NetFirewallRule -DisplayName "*Ash*" | Format-Table

# Check container network
docker network ls
docker network inspect ash_network
```

**Solutions:**

**1. Network/Firewall Issues:**
```powershell
# Ensure firewall rule exists
$rule = Get-NetFirewallRule -DisplayName "Ash NLP Server" -ErrorAction SilentlyContinue
if (-not $rule) {
    New-NetFirewallRule -DisplayName "Ash NLP Server" -Direction Inbound -Protocol TCP -LocalPort 8881 -Action Allow
    Write-Host "Firewall rule created"
}

# Test connectivity
Test-NetConnection -ComputerName 10.20.30.253 -Port 8881

# If still failing, check Windows Defender
# Temporarily disable Windows Defender firewall for testing
# Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
# Test connectivity, then re-enable:
# Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

**2. Docker Network Issues:**
```powershell
# Recreate Docker network
docker network rm ash_network
docker network create ash_network

# Restart container with new network
cd C:\Deployments\ash-nlp
docker-compose down
docker-compose up -d

# Verify network connectivity
docker exec ash_nlp_server ping 10.20.30.253
```

**3. Service Configuration Issues:**
```powershell
# Check if service is binding to correct interface
docker logs ash_nlp_server | Select-String "listening\|bind\|address"

# Verify .env configuration
Get-Content C:\Deployments\ash-nlp\.env | Select-String "HOST\|PORT"

# Should show:
# NLP_SERVICE_HOST=0.0.0.0  (not 127.0.0.1)
# NLP_SERVICE_PORT=8881

# If incorrect, fix and restart
docker-compose restart ash-nlp
```

---

## 🔧 Medium Priority Issues

### Performance Degradation

**Symptoms:**
- Analysis taking >500ms consistently
- High CPU usage
- Slow response times

**Diagnosis:**
```powershell
# Performance monitoring script
$startTime = Get-Date
$testPayload = @{
    message = "performance test message"
    user_id = "perf_test"
    channel_id = "perf_test"
} | ConvertTo-Json

for ($i = 1; $i -le 10; $i++) {
    $requestStart = Get-Date
    try {
        Invoke-RestMethod -Uri "http://10.20.30.253:8881/analyze" -Method POST -Body $testPayload -ContentType "application/json"
        $requestTime = (Get-Date) - $requestStart
        Write-Host "Request $i: $($requestTime.TotalMilliseconds)ms"
    } catch {
        Write-Host "Request $i: FAILED"
    }
}

$totalTime = (Get-Date) - $startTime
Write-Host "Average time: $($totalTime.TotalMilliseconds / 10)ms"
```

**Solutions:**

**1. Optimize GPU Usage:**
```powershell
# Check GPU utilization
nvidia-smi

# If GPU utilization low, check GPU memory fraction
# Update .env:
# GPU_MEMORY_FRACTION=0.9  # Increase if memory available

# If GPU utilization high, reduce batch size
# MAX_BATCH_SIZE=16  # Reduce from 32

# Restart container
docker-compose restart ash-nlp
```

**2. Optimize CPU Usage:**
```powershell
# Reduce inference threads if CPU maxed
# Update .env:
# INFERENCE_THREADS=4  # Reduce from 6

# Optimize container CPU allocation
# Update docker-compose.yml:
# cpus: '4'  # Reduce from '6'

# Restart container
docker-compose down
docker-compose up -d
```

**3. Clear System Bottlenecks:**
```powershell
# Check for background processes consuming resources
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Kill unnecessary processes
# Stop-Process -Name "ProcessName" -Force

# Clear temporary files
Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue

# Defragment if needed (SSD systems usually don't need this)
# Optimize-Volume -DriveLetter C -Analyze
```

### Memory Leaks

**Symptoms:**
- Container memory usage increasing over time
- Eventually hitting memory limits
- Container restarts due to OOM

**Diagnosis:**
```powershell
# Monitor memory usage over time
while ($true) {
    $stats = docker stats ash_nlp_server --no-stream --format "table {{.MemUsage}}\t{{.MemPerc}}"
    Write-Host "$(Get-Date): $stats"
    Start-Sleep 300  # Check every 5 minutes
}

# Check for memory-related errors in logs
docker logs ash_nlp_server | Select-String "memory\|OOM\|killed"
```

**Solutions:**

**1. Container Memory Limits:**
```powershell
# Set explicit memory limits in docker-compose.yml
# deploy:
#   resources:
#     limits:
#       memory: 6G  # Reduce from 8G
#     reservations:
#       memory: 1G

# Restart container
docker-compose down
docker-compose up -d
```

**2. Model Memory Optimization:**
```powershell
# Reduce model precision if available
# Update .env:
# MODEL_PRECISION=float16  # Reduce from float32 (if supported)

# Reduce cache size
# MODEL_CACHE_SIZE=2GB  # Reduce cache

# Clear model cache and restart
Remove-Item C:\Deployments\ash-nlp\models\cache\* -Recurse -Force
docker-compose restart ash-nlp
```

**3. Periodic Container Restart:**
```powershell
# Create scheduled task for periodic restart (if leak persists)
# restart_ash_nlp.ps1
cd C:\Deployments\ash-nlp
docker-compose restart ash-nlp
Write-Host "Ash NLP container restarted at $(Get-Date)"

# Schedule to run daily at 3 AM
# schtasks /create /tn "RestartAshNLP" /tr "powershell.exe -File C:\Scripts\restart_ash_nlp.ps1" /sc daily /st 03:00
```

### Analytics/Webhook Issues

**Symptoms:**
- Dashboard not receiving real-time data
- Analytics export failing
- Webhook delivery errors

**Diagnosis:**
```powershell
# Test webhook endpoint
Test-NetConnection -ComputerName 10.20.30.253 -Port 8883

# Test webhook manually
$webhookData = @{
    timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
    metrics = @{
        test = "true"
    }
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://10.20.30.253:8883/webhook/nlp_metrics" -Method POST -Body $webhookData -ContentType "application/json"
    Write-Host "Webhook test successful"
} catch {
    Write-Host "Webhook test failed: $($_.Exception.Message)"
}

# Check analytics logs
docker logs ash_nlp_server | Select-String "analytics\|webhook\|export"
```

**Solutions:**

**1. Webhook Configuration:**
```powershell
# Verify webhook URL in .env
Get-Content C:\Deployments\ash-nlp\.env | Select-String "WEBHOOK"

# Should be:
# ANALYTICS_WEBHOOK_URL=http://10.20.30.253:8883/webhook/nlp_metrics

# If incorrect, fix and restart
# docker-compose restart ash-nlp
```

**2. Network Connectivity:**
```powershell
# Test dashboard connectivity
curl http://10.20.30.253:8883/health

# If dashboard down, check on dashboard server
# ssh to 10.20.30.253 and run:
# docker-compose ps | grep ash-dash
```

**3. Analytics Export Issues:**
```powershell
# Test analytics export endpoint
curl http://10.20.30.253:8881/analytics_export

# Check analytics directory permissions
icacls C:\Deployments\ash-nlp\analytics

# Clear analytics cache if corrupted
Remove-Item C:\Deployments\ash-nlp\analytics\cache\* -Force -ErrorAction SilentlyContinue
docker-compose restart ash-nlp
```

---

## 🔍 Diagnostic Tools & Scripts

### Comprehensive Health Check Script

```powershell
# ash_nlp_health_check.ps1
param(
    [switch]$Detailed,
    [switch]$Fix
)

Write-Host "=== Ash NLP Server Health Check ===" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray

# 1. Basic connectivity
Write-Host "`n1. Testing Basic Connectivity..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://10.20.30.253:8881/health" -TimeoutSec 10
    Write-Host "✅ API Health: $($health.status)" -ForegroundColor Green
    
    if ($Detailed) {
        Write-Host "   Uptime: $($health.uptime_seconds) seconds" -ForegroundColor Gray
        Write-Host "   Version: $($health.version)" -ForegroundColor Gray
        Write-Host "   Avg Response: $($health.performance.average_response_time_ms)ms" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ API Health: FAILED - $($_.Exception.Message)" -ForegroundColor Red
    
    if ($Fix) {
        Write-Host "   Attempting to restart container..." -ForegroundColor Yellow
        cd C:\Deployments\ash-nlp
        docker-compose restart ash-nlp
        Start-Sleep 30
    }
}

# 2. Container status
Write-Host "`n2. Checking Container Status..." -ForegroundColor Yellow
$containerStatus = docker ps --filter "name=ash_nlp_server" --format "{{.Status}}"
if ($containerStatus -like "*Up*") {
    Write-Host "✅ Container Status: Running" -ForegroundColor Green
    if ($Detailed) {
        Write-Host "   Status: $containerStatus" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ Container Status: Not Running" -ForegroundColor Red
    
    if ($Fix) {
        Write-Host "   Starting container..." -ForegroundColor Yellow
        cd C:\Deployments\ash-nlp
        docker-compose up -d ash-nlp
    }
}

# 3. GPU status
Write-Host "`n3. Checking GPU Status..." -ForegroundColor Yellow
try {
    $gpuOutput = nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits
    Write-Host "✅ GPU Status: Available" -ForegroundColor Green
    if ($Detailed) {
        Write-Host "   GPU Info: $gpuOutput" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ GPU Status: Not Available" -ForegroundColor Red
}

# 4. Model status
Write-Host "`n4. Checking Model Status..." -ForegroundColor Yellow
try {
    $models = Invoke-RestMethod -Uri "http://10.20.30.253:8881/model_status" -TimeoutSec 10
    $allLoaded = ($models.models.depression_model.status -eq "loaded") -and ($models.models.sentiment_model.status -eq "loaded")
    
    if ($allLoaded) {
        Write-Host "✅ Models Status: All Loaded" -ForegroundColor Green
    } else {
        Write-Host "❌ Models Status: Some Not Loaded" -ForegroundColor Red
        
        if ($Fix) {
            Write-Host "   Restarting to reload models..." -ForegroundColor Yellow
            cd C:\Deployments\ash-nlp
            docker-compose restart ash-nlp
        }
    }
    
    if ($Detailed) {
        Write-Host "   Depression Model: $($models.models.depression_model.status)" -ForegroundColor Gray
        Write-Host "   Sentiment Model: $($models.models.sentiment_model.status)" -ForegroundColor Gray
        Write-Host "   Learning System: $($models.learning_system.status)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Models Status: Cannot Check - $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Performance test
Write-Host "`n5. Running Performance Test..." -ForegroundColor Yellow
$testPayload = @{
    message = "health check test message"
    user_id = "health_check"
    channel_id = "health_check"
} | ConvertTo-Json

try {
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $result = Invoke-RestMethod -Uri "http://10.20.30.253:8881/analyze" -Method POST -Body $testPayload -ContentType "application/json"
    $stopwatch.Stop()
    
    $responseTime = $stopwatch.ElapsedMilliseconds
    if ($responseTime -lt 200) {
        Write-Host "✅ Performance: $($responseTime)ms (Good)" -ForegroundColor Green
    } elseif ($responseTime -lt 500) {
        Write-Host "⚠️ Performance: $($responseTime)ms (Acceptable)" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Performance: $($responseTime)ms (Poor)" -ForegroundColor Red
    }
    
    if ($Detailed) {
        Write-Host "   Risk Level: $($result.risk_level)" -ForegroundColor Gray
        Write-Host "   Confidence: $($result.confidence)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Performance: Test Failed - $($_.Exception.Message)" -ForegroundColor Red
}

# 6. System resources
Write-Host "`n6. Checking System Resources..." -ForegroundColor Yellow
$memory = Get-WmiObject -Class Win32_OperatingSystem
$memoryUsage = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize * 100), 2)

if ($memoryUsage -lt 80) {
    Write-Host "✅ Memory Usage: $memoryUsage% (Good)" -ForegroundColor Green
} elseif ($memoryUsage -lt 90) {
    Write-Host "⚠️ Memory Usage: $memoryUsage% (High)" -ForegroundColor Yellow
} else {
    Write-Host "❌ Memory Usage: $memoryUsage% (Critical)" -ForegroundColor Red
}

# Check disk space
$disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
$diskFreeGB = [math]::Round($disk.FreeSpace / 1GB, 2)

if ($diskFreeGB -gt 10) {
    Write-Host "✅ Disk Space: ${diskFreeGB}GB free (Good)" -ForegroundColor Green
} elseif ($diskFreeGB -gt 5) {
    Write-Host "⚠️ Disk Space: ${diskFreeGB}GB free (Low)" -ForegroundColor Yellow
} else {
    Write-Host "❌ Disk Space: ${diskFreeGB}GB free (Critical)" -ForegroundColor Red
}

Write-Host "`n=== Health Check Complete ===" -ForegroundColor Green
```

### Performance Monitoring Script

```powershell
# ash_nlp_monitor.ps1
param(
    [int]$Duration = 300,  # 5 minutes default
    [int]$Interval = 30    # 30 seconds default
)

Write-Host "Starting Ash NLP Performance Monitor for $Duration seconds..." -ForegroundColor Green

$results = @()
$startTime = Get-Date

for ($i = 0; $i -lt ($Duration / $Interval); $i++) {
    $timestamp = Get-Date
    
    # Test API response time
    $testPayload = @{
        message = "monitoring test $i"
        user_id = "monitor"
        channel_id = "monitor"
    } | ConvertTo-Json
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-RestMethod -Uri "http://10.20.30.253:8881/analyze" -Method POST -Body $testPayload -ContentType "application/json" -TimeoutSec 10
        $stopwatch.Stop()
        $responseTime = $stopwatch.ElapsedMilliseconds
        $success = $true
    } catch {
        $responseTime = $null
        $success = $false
    }
    
    # Get system metrics
    $memory = Get-WmiObject -Class Win32_OperatingSystem
    $memoryUsage = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize * 100), 2)
    
    # Get GPU metrics (if available)
    try {
        $gpuInfo = nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits
        $gpuParts = $gpuInfo.Split(',')
        $gpuUtilization = [int]$gpuParts[0].Trim()
        $gpuMemory = [int]$gpuParts[1].Trim()
    } catch {
        $gpuUtilization = $null
        $gpuMemory = $null
    }
    
    $result = [PSCustomObject]@{
        Timestamp = $timestamp
        Success = $success
        ResponseTimeMS = $responseTime
        MemoryUsagePercent = $memoryUsage
        GPUUtilization = $gpuUtilization
        GPUMemoryMB = $gpuMemory
    }
    
    $results += $result
    
    # Display current status
    $status = if ($success) { "✅" } else { "❌" }
    $responseDisplay = if ($responseTime) { "${responseTime}ms" } else { "FAILED" }
    Write-Host "[$timestamp] $status Response: $responseDisplay | Memory: $memoryUsage% | GPU: $gpuUtilization%" -ForegroundColor $(if ($success) { "Green" } else { "Red" })
    
    Start-Sleep $Interval
}

# Generate summary report
Write-Host "`n=== Performance Summary ===" -ForegroundColor Green

$successfulRequests = $results | Where-Object { $_.Success }
$failedRequests = $results | Where-Object { -not $_.Success }

Write-Host "Total Requests: $($results.Count)"
Write-Host "Successful: $($successfulRequests.Count) ($([math]::Round($successfulRequests.Count / $results.Count * 100, 1))%)"
Write-Host "Failed: $($failedRequests.Count) ($([math]::Round($failedRequests.Count / $results.Count * 100, 1))%)"

if ($successfulRequests.Count -gt 0) {
    $avgResponse = [math]::Round(($successfulRequests.ResponseTimeMS | Measure-Object -Average).Average, 1)
    $maxResponse = ($successfulRequests.ResponseTimeMS | Measure-Object -Maximum).Maximum
    $minResponse = ($successfulRequests.ResponseTimeMS | Measure-Object -Minimum).Minimum
    
    Write-Host "Response Time - Avg: ${avgResponse}ms | Min: ${minResponse}ms | Max: ${maxResponse}ms"
}

$avgMemory = [math]::Round(($results.MemoryUsagePercent | Measure-Object -Average).Average, 1)
$maxMemory = ($results.MemoryUsagePercent | Measure-Object -Maximum).Maximum

Write-Host "Memory Usage - Avg: $avgMemory% | Max: $maxMemory%"

if ($results[0].GPUUtilization -ne $null) {
    $avgGPU = [math]::Round(($results.GPUUtilization | Measure-Object -Average).Average, 1)
    $maxGPU = ($results.GPUUtilization | Measure-Object -Maximum).Maximum
    Write-Host "GPU Utilization - Avg: $avgGPU% | Max: $maxGPU%"
}

# Save detailed results
$resultsFile = "ash_nlp_performance_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
$results | Export-Csv -Path $resultsFile -NoTypeInformation
Write-Host "`nDetailed results saved to: $resultsFile" -ForegroundColor Gray
```

---

## 📞 Escalation Procedures

### When to Escalate

**Immediate Escalation (Critical Issues):**
- Complete service outage (>5 minutes)
- Security incidents or breaches
- Data corruption or loss
- Critical crisis detection failures

**Standard Escalation (High Priority Issues):**
- Performance degradation affecting response times
- Integration failures affecting other services
- Recurring errors or system instability
- Learning system malfunctions

**Information Only (Medium/Low Priority):**
- Minor performance optimizations needed
- Configuration updates required
- Documentation updates needed
- Feature requests or enhancements

### Escalation Contacts

**Technical Escalation:**
1. **Discord #tech-support** - First line technical support
2. **GitHub Issues** - Formal bug reports and feature requests
3. **Discord Development Team** - Direct contact for urgent issues
4. **Emergency Contact** - Crisis response team lead for critical outages

**Information Required for Escalation:**
- **Problem Description**: Clear, concise description of the issue
- **Impact Assessment**: How the issue affects operations
- **Steps Taken**: What troubleshooting has been attempted
- **Logs/Evidence**: Relevant error messages, logs, or screenshots
- **Timeline**: When the issue started and how long it has persisted
- **Environment**: Server details, version information, recent changes

### Emergency Recovery Procedures

**Complete System Failure:**
```powershell
# 1. Immediate assessment
Write-Host "=== EMERGENCY RECOVERY PROCEDURE ===" -ForegroundColor Red

# 2. Document current state
Get-Date | Out-File "emergency_recovery_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
docker ps -a >> "emergency_recovery_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
docker logs ash_nlp_server --tail 100 >> "emergency_recovery_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# 3. Attempt service restart
cd C:\Deployments\ash-nlp
docker-compose down
docker-compose up -d

# 4. Wait for recovery
Start-Sleep 120

# 5. Test recovery
try {
    $health = Invoke-RestMethod -Uri "http://10.20.30.253:8881/health"
    Write-Host "Recovery successful: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "Recovery failed - escalating immediately" -ForegroundColor Red
    # Notify emergency contacts
}
```

**Data Recovery:**
```powershell
# 1. Stop services
docker-compose down

# 2. Assess data integrity
Get-ChildItem C:\Deployments\ash-nlp\learning_data\ -Recurse
Get-ChildItem C:\Deployments\ash-nlp\models\ -Recurse

# 3. Restore from backup if needed
$latestBackup = Get-ChildItem C:\Deployments\ash-nlp\backups\ | Sort-Object CreationTime -Descending | Select-Object -First 1
if ($latestBackup) {
    Copy-Item "$($latestBackup.FullName)\*" C:\Deployments\ash-nlp\ -Recurse -Force
    Write-Host "Restored from backup: $($latestBackup.Name)"
}

# 4. Restart services
docker-compose up -d
```

---

## 📚 Additional Resources

### Documentation Links
- **[Deployment Guide](../deployment_v2_1.md)** - Production deployment procedures
- **[API Documentation](API_v2_1.md)** - Complete API reference
- **[Team Guide](../team/team_guide_v2_1.md)** - Crisis response team procedures
- **[Main Repository](https://github.com/the-alphabet-cartel/ash)** - Ecosystem overview

### External Resources
- **[Docker Documentation](https://docs.docker.com/)** - Container management
- **[NVIDIA Docker Documentation](https://github.com/NVIDIA/nvidia-docker)** - GPU support
- **[Windows Container Documentation](https://docs.microsoft.com/en-us/virtualization/windowscontainers/)** - Windows-specific containerization

### Community Support
- **Discord #tech-support**: https://discord.gg/alphabetcartel
- **GitHub Issues**: https://github.com/the-alphabet-cartel/ash-nlp/issues
- **Community Wiki**: https://alphabetcartel.org

---

**The Alphabet Cartel** - Building inclusive gaming communities through technology.

**Discord:** https://discord.gg/alphabetcartel | **Website:** https://alphabetcartel.org

*When things go wrong, we fix them together. No one troubleshoots alone.*