# Ash-NLP Testing Suite - Docker Guide

**FILE VERSION**: v5.0  
**LAST MODIFIED**: 2025-12-30  
**CLEAN ARCHITECTURE**: v5.0 Compliant  

---

## 🐳 Docker Setup

Complete Docker containerization for Ash-NLP v5.0 testing suite with GPU support.

## Prerequisites

### Required
- **Docker**: Version 24.0+
- **Docker Compose**: Version 2.20+
- **NVIDIA GPU** (optional but recommended)
- **nvidia-container-toolkit** (for GPU support)

### Install NVIDIA Container Toolkit (Ubuntu/Debian)

```bash
# Add NVIDIA repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Restart Docker
sudo systemctl restart docker
```

### Verify GPU Access

```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

---

## 🚀 Quick Start

### 1. Build the Container

```bash
# Using docker-compose (recommended)
docker-compose -f docker-compose.testing.yml build

# Or using docker directly
docker build -f Dockerfile.testing -t ash-nlp-testing:v5.0 .
```

### 2. Start the Container

```bash
# Start in background
docker-compose -f docker-compose.testing.yml up -d

# Or start interactively
docker-compose -f docker-compose.testing.yml run ash-nlp-testing bash
```

### 3. Run Your First Test

```bash
# Test BART model on crisis examples
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    test-model facebook/bart-large-mnli crisis
```

---

## 📋 Available Commands

The testing container includes several pre-configured commands:

### Testing Commands

```bash
# Test a single model
docker-compose exec ash-nlp-testing test-model <model_name> <dataset>

# Test v3.1 baseline
docker-compose exec ash-nlp-testing test-baseline

# Test all v5.0 proposed models
docker-compose exec ash-nlp-testing test-proposed

# Run comprehensive test suite
docker-compose exec ash-nlp-testing test-all

# Compare two models
docker-compose exec ash-nlp-testing compare <model_a> <model_b>
```

### Interactive Shells

```bash
# Bash shell
docker-compose exec ash-nlp-testing bash

# Python shell
docker-compose exec ash-nlp-testing python

# IPython shell
docker-compose exec ash-nlp-testing ipython
```

---

## 💡 Usage Examples

### Example 1: Test Single Model

```bash
# Test BART model on crisis examples
docker-compose -f docker-compose.testing.yml run ash-nlp-testing \
    test-model facebook/bart-large-mnli crisis

# Test on safe examples
docker-compose -f docker-compose.testing.yml run ash-nlp-testing \
    test-model facebook/bart-large-mnli safe

# Test on edge cases
docker-compose -f docker-compose.testing.yml run ash-nlp-testing \
    test-model SamLowe/roberta-base-go_emotions edge
```

### Example 2: Establish Baseline

```bash
# Test v3.1 baseline model
docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-baseline

# View results
cat testing/reports/output/baseline_v3.1.json
```

### Example 3: Test All Proposed Models

```bash
# Test all 4 v5.0 models
docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-proposed

# Results saved to testing/reports/output/
ls -la testing/reports/output/
```

### Example 4: Compare Models

```bash
# Compare baseline vs BART
docker-compose -f docker-compose.testing.yml run ash-nlp-testing compare \
    MoritzLaurer/deberta-v3-base-zeroshot-v2.0 \
    facebook/bart-large-mnli
```

### Example 5: Comprehensive Testing

```bash
# Run full test suite (all datasets)
docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-all

# View comprehensive report
cat testing/reports/output/comprehensive_test.json
```

### Example 6: Interactive Python Testing

```bash
# Start Python shell
docker-compose -f docker-compose.testing.yml run ash-nlp-testing python

# Then in Python:
>>> from testing import create_model_evaluator
>>> evaluator = create_model_evaluator()
>>> results = evaluator.test_dataset(
...     "facebook/bart-large-mnli",
...     "testing/test_datasets/crisis_examples.json",
...     task_type="zero-shot-classification"
... )
>>> print(results['metrics']['overall']['accuracy'])
```

### Example 7: Custom Python Script

```bash
# Create test script
cat > custom_test.py <<'EOF'
from testing import create_model_evaluator

evaluator = create_model_evaluator()

# Your custom testing logic here
results = evaluator.test_dataset(
    "your-model-here",
    "testing/test_datasets/crisis_examples.json"
)

print(f"Accuracy: {results['metrics']['overall']['accuracy']:.2%}")
EOF

# Run in container
docker-compose -f docker-compose.testing.yml run ash-nlp-testing python custom_test.py
```

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```bash
# Device Configuration
TEST_DEVICE=cuda                    # or 'cpu'
TEST_BATCH_SIZE=8
TEST_TIMEOUT=30
TEST_VERBOSE=true

# Accuracy Thresholds
TEST_ACCURACY_THRESHOLD=0.85
TEST_PRECISION_THRESHOLD=0.80
TEST_RECALL_THRESHOLD=0.85
TEST_F1_THRESHOLD=0.82

# Performance Thresholds  
TEST_LATENCY_THRESHOLD=5000         # milliseconds
TEST_VRAM_THRESHOLD=2000            # MB

# Model Cache (persisted between runs)
TRANSFORMERS_CACHE=/app/testing/cache/models
HF_HOME=/app/testing/cache/huggingface
```

### Volume Mounts

The container mounts the following directories:

```yaml
volumes:
  - ./testing:/app/testing              # Testing code (read-write)
  - ./testing/reports:/app/testing/reports  # Test reports (read-write)
  - ./logs:/app/logs                    # Logs (read-write)
  - ash-nlp-testing-cache:/app/testing/cache  # Model cache (persistent)
```

**Model Cache**: Downloaded models are cached in a Docker volume and persist between container restarts.

---

## 🔍 Monitoring & Debugging

### View Container Logs

```bash
# Follow logs in real-time
docker-compose -f docker-compose.testing.yml logs -f

# View last 100 lines
docker-compose -f docker-compose.testing.yml logs --tail=100
```

### Check GPU Status

```bash
# Inside container
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing nvidia-smi

# Or run directly
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0))"
```

### Check Resource Usage

```bash
# Container stats
docker stats ash-nlp-testing

# Detailed inspection
docker inspect ash-nlp-testing
```

### Access Test Reports

```bash
# List all reports
ls -lah testing/reports/output/

# View JSON report
cat testing/reports/output/test_results.json | jq '.'

# View with Python
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    python -c "import json; print(json.dumps(json.load(open('testing/reports/output/test_results.json')), indent=2))"
```

---

## 🐛 Troubleshooting

### Issue: GPU Not Detected

**Check:**
```bash
# Verify nvidia-smi works on host
nvidia-smi

# Verify Docker can access GPU
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Check container GPU access
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing nvidia-smi
```

**Fix:**
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Rebuild container
docker-compose -f docker-compose.testing.yml build --no-cache
```

### Issue: Out of Memory (VRAM)

**Solution:**
```bash
# Reduce batch size in .env
TEST_BATCH_SIZE=4  # or 2, or 1

# Force CPU mode
TEST_DEVICE=cpu

# Clear model cache
docker volume rm ash-nlp-testing-cache
```

### Issue: Slow Performance

**Check:**
```bash
# Verify GPU is being used
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    python -c "import torch; print('Using device:', 'cuda' if torch.cuda.is_available() else 'cpu')"

# Check model cache location
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    ls -lah /app/testing/cache/models/
```

### Issue: Permission Errors

**Fix:**
```bash
# Fix permissions on host
sudo chown -R $USER:$USER testing/reports
sudo chown -R $USER:$USER logs
sudo chmod -R 755 testing/reports
sudo chmod -R 755 logs
```

### Issue: Container Won't Start

**Debug:**
```bash
# Check container status
docker-compose -f docker-compose.testing.yml ps

# View logs
docker-compose -f docker-compose.testing.yml logs

# Start with specific command
docker-compose -f docker-compose.testing.yml run ash-nlp-testing bash

# Inside container, check Python
python -c "import torch; import transformers; print('OK')"
```

---

## 🧹 Cleanup

### Stop and Remove Container

```bash
# Stop container
docker-compose -f docker-compose.testing.yml down

# Remove container and volumes
docker-compose -f docker-compose.testing.yml down -v

# Remove image
docker rmi ash-nlp-testing:v5.0
```

### Clear Model Cache

```bash
# Remove cache volume (models will re-download)
docker volume rm ash-nlp-testing-cache

# Or manually clear inside container
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    rm -rf /app/testing/cache/models/*
```

### Clear Test Reports

```bash
# On host
rm -rf testing/reports/output/*

# Or inside container
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    rm -rf /app/testing/reports/output/*
```

---

## 🔧 Advanced Usage

### Custom Dockerfile Modifications

To add additional dependencies:

```dockerfile
# In Dockerfile.testing, add:
RUN pip install your-package-here
```

Then rebuild:
```bash
docker-compose -f docker-compose.testing.yml build --no-cache
```

### Mount Additional Directories

Edit `docker-compose.testing.yml`:

```yaml
volumes:
  - ./your-custom-dir:/app/custom-dir:ro
```

### Run on Different Port

Edit `docker-compose.testing.yml`:

```yaml
ports:
  - "YOUR_PORT:30880"
```

### Use Different GPU

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: ['1']  # Use GPU 1 instead of 0
          capabilities: [gpu]
```

---

## 📊 Integration with CI/CD

### GitHub Actions Example

```yaml
name: Test Models

on: [push, pull_request]

jobs:
  test:
    runs-on: self-hosted  # Requires GPU runner
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build testing container
        run: docker-compose -f docker-compose.testing.yml build
      
      - name: Run baseline tests
        run: docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-baseline
      
      - name: Upload test reports
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: testing/reports/output/
```

---

## 🎯 Production Deployment

For production testing on server **Lofn** (10.20.30.253):

```bash
# SSH to server
ssh user@10.20.30.253

# Clone repository
cd /path/to/ash-nlp
git pull origin main

# Build and start
docker-compose -f docker-compose.testing.yml up -d

# Run scheduled tests (example with cron)
# Add to crontab:
# 0 2 * * * cd /path/to/ash-nlp && docker-compose -f docker-compose.testing.yml exec -T ash-nlp-testing test-all
```

---

## 📚 Additional Resources

- Main Testing README: `testing/README.md`
- Project Roadmap: `docs/v5.0/roadmap.md`
- Clean Architecture Charter: `docs/clean_architecture_charter.md`
- Discord: https://discord.gg/alphabetcartel
- Repository: https://github.com/the-alphabet-cartel/ash-nlp

---

**Built with care for chosen family** 🏳️‍🌈
