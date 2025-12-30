# Ash-NLP Testing Suite - Quick Reference

**FILE VERSION**: v5.0  
**LAST MODIFIED**: 2025-12-30

---

## 🚀 Quick Start (Copy & Paste)

```bash
# 1. Build container
docker-compose -f docker-compose.testing.yml build

# 2. Start container
docker-compose -f docker-compose.testing.yml up -d

# 3. Run first test
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing test-baseline

# 4. View results
cat testing/reports/output/baseline_v3.1.json
```

---

## 📋 Common Commands

### Container Management
```bash
# Build
docker-compose -f docker-compose.testing.yml build

# Start (background)
docker-compose -f docker-compose.testing.yml up -d

# Start (foreground with logs)
docker-compose -f docker-compose.testing.yml up

# Stop
docker-compose -f docker-compose.testing.yml down

# Restart
docker-compose -f docker-compose.testing.yml restart

# View logs
docker-compose -f docker-compose.testing.yml logs -f

# Shell access
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing bash
```

### Testing Commands
```bash
# Test single model
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    test-model facebook/bart-large-mnli crisis

# Test baseline (v3.1)
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing test-baseline

# Test all proposed models (v5.0)
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing test-proposed

# Comprehensive test
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing test-all

# Compare models
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    compare model-a model-b
```

### Available Datasets
```bash
crisis      # crisis_examples.json (55 cases)
safe        # safe_examples.json (52 cases)
edge        # edge_cases.json (50 cases)
lgbtqia     # lgbtqia_specific.json (50 cases)
```

---

## 🎯 Typical Workflow

### Day 1: Establish Baseline
```bash
# Build container
docker-compose -f docker-compose.testing.yml build

# Test v3.1 baseline
docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-baseline

# Review results
cat testing/reports/output/baseline_v3.1.json | jq '.metrics'
```

### Day 2: Test New Models
```bash
# Test BART (crisis classifier)
docker-compose -f docker-compose.testing.yml run ash-nlp-testing \
    test-model facebook/bart-large-mnli crisis

# Test RoBERTa emotions
docker-compose -f docker-compose.testing.yml run ash-nlp-testing \
    test-model SamLowe/roberta-base-go_emotions crisis

# Compare to baseline
docker-compose -f docker-compose.testing.yml run ash-nlp-testing \
    compare MoritzLaurer/deberta-v3-base-zeroshot-v2.0 facebook/bart-large-mnli
```

### Day 3: Comprehensive Validation
```bash
# Test all proposed models
docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-proposed

# Run comprehensive suite
docker-compose -f docker-compose.testing.yml run ash-nlp-testing test-all

# Review all reports
ls -lah testing/reports/output/
```

---

## 🔍 Debugging

### Check GPU
```bash
# Verify GPU detected
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing nvidia-smi

# Check PyTorch CUDA
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Check Performance
```bash
# View container stats
docker stats ash-nlp-testing

# Check VRAM usage
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    nvidia-smi --query-gpu=memory.used --format=csv
```

### View Logs
```bash
# Container logs
docker-compose -f docker-compose.testing.yml logs -f

# Python logs
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing \
    tail -f /app/logs/testing.log
```

---

## 🧹 Maintenance

### Clear Cache
```bash
# Remove model cache
docker volume rm ash-nlp-testing-cache

# Clear reports
rm -rf testing/reports/output/*
```

### Rebuild Container
```bash
# Full rebuild
docker-compose -f docker-compose.testing.yml down
docker-compose -f docker-compose.testing.yml build --no-cache
docker-compose -f docker-compose.testing.yml up -d
```

### Update Code
```bash
# Pull latest code
git pull origin main

# Restart container (uses updated mounted volumes)
docker-compose -f docker-compose.testing.yml restart
```

---

## 📊 Viewing Results

### JSON Reports
```bash
# List all reports
ls -lah testing/reports/output/

# Pretty print JSON
cat testing/reports/output/test_results.json | jq '.'

# Extract specific metric
cat testing/reports/output/test_results.json | jq '.metrics.overall.accuracy'
```

### Quick Summary
```bash
# Accuracy only
cat testing/reports/output/test_results.json | \
    jq '.metrics.overall | {accuracy, passed, failed, total_tests}'

# Performance only  
cat testing/reports/output/test_results.json | \
    jq '.metrics.performance | {avg_latency_ms, avg_vram_mb}'
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```bash
TEST_DEVICE=cuda                # or 'cpu'
TEST_BATCH_SIZE=8               # Lower if OOM
TEST_TIMEOUT=30
TEST_VERBOSE=true

TEST_ACCURACY_THRESHOLD=0.85
TEST_LATENCY_THRESHOLD=5000     # ms
TEST_VRAM_THRESHOLD=2000        # MB
```

### Apply Changes
```bash
# After editing .env
docker-compose -f docker-compose.testing.yml restart
```

---

## 💡 Pro Tips

### Background Testing
```bash
# Run test in background, check results later
docker-compose -f docker-compose.testing.yml run -d ash-nlp-testing test-all

# Check if still running
docker ps | grep ash-nlp-testing

# View results when done
cat testing/reports/output/comprehensive_test.json
```

### Multiple Tests in Sequence
```bash
# Create test script
cat > run_tests.sh <<'EOF'
#!/bin/bash
docker-compose -f docker-compose.testing.yml exec -T ash-nlp-testing test-baseline
docker-compose -f docker-compose.testing.yml exec -T ash-nlp-testing test-proposed
docker-compose -f docker-compose.testing.yml exec -T ash-nlp-testing test-all
EOF

chmod +x run_tests.sh
./run_tests.sh
```

### Interactive Development
```bash
# Start Python shell with iPython
docker-compose -f docker-compose.testing.yml exec ash-nlp-testing ipython

# Then experiment interactively:
from testing import create_model_evaluator
evaluator = create_model_evaluator()
# ... your code here
```

---

## 🆘 Help

### Get Help
```bash
# Container help
docker-compose -f docker-compose.testing.yml run ash-nlp-testing --help

# Or view this file
cat DOCKER_QUICK_REFERENCE.md
```

### More Documentation
- Full Docker guide: `DOCKER_README.md`
- Testing framework: `testing/README.md`
- Project roadmap: `docs/v5.0/roadmap.md`

---

**Built with care for chosen family** 🏳️‍🌈
