# Ash-NLP Testing Suite - Environment Variables Reference

**FILE VERSION**: v5.0  
**LAST MODIFIED**: 2025-12-30

---

## 📋 Quick Answer

### **Minimum Required Variables**

```bash
# Copy to .env - That's it!
TEST_DEVICE=cuda
TEST_BATCH_SIZE=8
TRANSFORMERS_CACHE=testing/cache/models
HF_HOME=testing/cache/huggingface
```

**All other variables have sensible defaults and are optional!**

---

## 📊 Complete Variable Reference

### **Required Variables** ✅

| Variable | Default | Description | Your Server (Lofn) |
|----------|---------|-------------|-------------------|
| `TEST_DEVICE` | `cuda` | Device type (cuda/cpu) | `cuda` (RTX 3060) |
| `TEST_BATCH_SIZE` | `8` | Inference batch size | `8` (12GB VRAM) |
| `TRANSFORMERS_CACHE` | - | Model cache directory | `testing/cache/models` |
| `HF_HOME` | - | HuggingFace config directory | `testing/cache/huggingface` |

### **Recommended Variables** ⭐

| Variable | Default | Description | Notes |
|----------|---------|-------------|-------|
| `LOG_LEVEL` | `INFO` | Logging verbosity | `DEBUG` for troubleshooting |
| `LOG_FILE` | `logs/testing.log` | Log file path | Auto-created |

### **Optional: Performance Thresholds** ⚙️

These define "passing" test criteria. Defaults are based on v5.0 targets:

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_ACCURACY_THRESHOLD` | `0.85` | Min accuracy (85%) |
| `TEST_PRECISION_THRESHOLD` | `0.80` | Min precision (80%) |
| `TEST_RECALL_THRESHOLD` | `0.85` | Min recall (85%) |
| `TEST_F1_THRESHOLD` | `0.82` | Min F1 score (82%) |
| `TEST_LATENCY_THRESHOLD` | `5000` | Max latency (5000ms) |
| `TEST_VRAM_THRESHOLD` | `2000` | Max VRAM (2000MB) |

### **Optional: Test Execution** 🔧

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_TIMEOUT` | `30` | Test timeout (seconds) |
| `TEST_VERBOSE` | `true` | Verbose output |
| `TEST_PARALLEL` | `false` | Parallel testing (future) |

### **Optional: Dataset Paths** 📂

Only needed if you move datasets to non-standard locations:

| Variable | Default |
|----------|---------|
| `TEST_DATASET_CRISIS` | `testing/test_datasets/crisis_examples.json` |
| `TEST_DATASET_SAFE` | `testing/test_datasets/safe_examples.json` |
| `TEST_DATASET_EDGE` | `testing/test_datasets/edge_cases.json` |
| `TEST_DATASET_LGBTQIA` | `testing/test_datasets/lgbtqia_specific.json` |
| `TEST_DATASET_ESCALATION` | `testing/test_datasets/escalation_patterns.json` |

### **Optional: Report Output** 📊

| Variable | Default |
|----------|---------|
| `TEST_REPORT_OUTPUT_DIR` | `testing/reports/output` |
| `TEST_GENERATE_HTML` | `true` |
| `TEST_GENERATE_JSON` | `true` |
| `TEST_SAVE_CHARTS` | `true` |

### **Optional: Baseline Comparison** 📈

| Variable | Default |
|----------|---------|
| `TEST_BASELINE_MODEL` | `MoritzLaurer/deberta-v3-base-zeroshot-v2.0` |

### **Optional: Advanced GPU** 🎮

Only needed for multi-GPU systems or specific GPU selection:

| Variable | Default | Description |
|----------|---------|-------------|
| `CUDA_VISIBLE_DEVICES` | `0` | Which GPU to use |
| `CUDA_TF32` | `true` | TF32 acceleration (Ampere+) |

### **Optional: Authentication** 🔐

Only needed for gated HuggingFace models (not required for v5.0):

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | - | HuggingFace API token |

---

## 🚀 Setup Options

### **Option 1: Copy Minimal Template (Recommended)**

```bash
# Copy minimal template
cp .env.minimal.testing.template .env.testing

# Edit if needed
nano .env.testing
```

**Minimal `.env` contents:**
```bash
TEST_DEVICE=cuda
TEST_BATCH_SIZE=8
TRANSFORMERS_CACHE=testing/cache/models
HF_HOME=testing/cache/huggingface
LOG_LEVEL=INFO
LOG_FILE=logs/testing.log
```

### **Option 2: Copy Full Template**

```bash
# Copy full template with all options
cp .env.testing.template .env.testing

# Uncomment and customize as needed
nano .env
```

### **Option 3: Bare Minimum**

The testing suite will work with ZERO environment variables! It uses these defaults:

```python
# Automatic defaults from test_config.json
TEST_DEVICE: "cuda" (auto-fallback to cpu)
TEST_BATCH_SIZE: 8
TEST_TIMEOUT: 30
TEST_VERBOSE: true
TEST_ACCURACY_THRESHOLD: 0.85
# ... etc (see test_config.json for all defaults)
```

But you **should** set at least cache directories to avoid re-downloading models:
```bash
TRANSFORMERS_CACHE=testing/cache/models
HF_HOME=testing/cache/huggingface
```

---

## 🎯 Recommended Setup for Lofn Server

Based on your Lofn server specs (Ryzen 7 5800x, RTX 3060 12GB, 64GB RAM):

```bash
# .env - Optimized for Lofn
TEST_DEVICE=cuda
TEST_BATCH_SIZE=8                # 12GB VRAM can handle this
TRANSFORMERS_CACHE=testing/cache/models
HF_HOME=testing/cache/huggingface
LOG_LEVEL=INFO
LOG_FILE=logs/testing.log

# Optional: Raise thresholds for better validation
TEST_ACCURACY_THRESHOLD=0.90     # Aim higher on powerful hardware
TEST_LATENCY_THRESHOLD=7000      # 7s for 4-model ensemble
TEST_VRAM_THRESHOLD=2000         # 2GB for ensemble
```

---

## 🐳 Docker Considerations

### **Host .env File**

Docker Compose automatically loads `.env` from the repository root and passes variables to the container.

```bash
# Host: .env file location
ash-nlp/
├── .env                          # ← Docker Compose reads this
├── docker-compose.testing.yml
└── testing/
```

### **Variables Docker Needs**

Docker Compose specifically uses these from `.env`:

```bash
# Device and performance
TEST_DEVICE=cuda
TEST_BATCH_SIZE=8
TEST_TIMEOUT=30
TEST_VERBOSE=true

# Thresholds
TEST_ACCURACY_THRESHOLD=0.85
TEST_LATENCY_THRESHOLD=5000
TEST_VRAM_THRESHOLD=2000

# Caching (mapped to container paths)
TRANSFORMERS_CACHE=/app/testing/cache/models  # Container path
HF_HOME=/app/testing/cache/huggingface       # Container path
```

### **Container vs Host Paths**

| Environment | Cache Path |
|-------------|------------|
| **Host** | `./testing/cache/models` |
| **Container** | `/app/testing/cache/models` |
| **Volume** | `ash-nlp-testing-cache` |

Docker automatically maps these via volumes in `docker-compose.testing.yml`.

---

## 🔧 Troubleshooting

### **Out of Memory Errors**

```bash
# Reduce batch size progressively
TEST_BATCH_SIZE=4   # Try this first
TEST_BATCH_SIZE=2   # If still OOM
TEST_BATCH_SIZE=1   # Last resort
```

### **CPU Fallback**

```bash
# Force CPU if GPU causes issues
TEST_DEVICE=cpu
TEST_BATCH_SIZE=2   # Lower for CPU
```

### **Slow First Run**

First run downloads models (~2-3GB). Check cache:

```bash
# Verify cache directory exists
mkdir -p testing/cache/models
mkdir -p testing/cache/huggingface

# Check cache contents after first run
ls -lah testing/cache/models/
```

### **Permission Issues**

```bash
# Fix permissions
chmod -R 755 testing/cache
chmod -R 755 testing/reports
chmod -R 755 logs

# Or with sudo if needed
sudo chown -R $USER:$USER testing/cache
```

---

## ✅ Validation

### **Check Your Configuration**

```bash
# In Docker container
docker-compose -f docker-compose.testing.yml run ash-nlp-testing bash

# Then check variables
echo $TEST_DEVICE
echo $TEST_BATCH_SIZE
echo $TRANSFORMERS_CACHE

# Or check all at once
env | grep TEST_
```

### **Test Configuration**

```python
# In Python shell
docker-compose -f docker-compose.testing.yml run ash-nlp-testing python

>>> import os
>>> print("Device:", os.getenv('TEST_DEVICE', 'cuda'))
>>> print("Batch Size:", os.getenv('TEST_BATCH_SIZE', '8'))
>>> print("Cache:", os.getenv('TRANSFORMERS_CACHE'))
```

---

## 📝 Summary

### **Absolute Minimum**
```bash
# Just these 4 lines!
TEST_DEVICE=cuda
TEST_BATCH_SIZE=8
TRANSFORMERS_CACHE=testing/cache/models
HF_HOME=testing/cache/huggingface
```

### **Recommended**
Add logging:
```bash
LOG_LEVEL=INFO
LOG_FILE=logs/testing.log
```

### **Full Control**
Use `.env.template.testing` for all 30+ variables.

### **Docker Users**
Docker Compose handles everything automatically - just create `.env` with minimum variables!

---

## 🆘 Still Confused?

**Just copy the minimal template:**

```bash
cp .env.minimal.testing .env
```

**Or create .env manually with just these 4 lines:**

```bash
cat > .env <<'EOF'
TEST_DEVICE=cuda
TEST_BATCH_SIZE=8
TRANSFORMERS_CACHE=testing/cache/models
HF_HOME=testing/cache/huggingface
EOF
```

**Done!** 🎉

---

**Built with care for chosen family** 🏳️‍🌈
