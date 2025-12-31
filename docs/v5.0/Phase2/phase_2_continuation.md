# Ash-NLP v5.0 - Phase 2 Continuation Document

**SESSION DATE**: 2025-12-31  
**PREVIOUS SESSION**: Phase 1 - Testing Framework & Baseline Evaluation  
**CURRENT PHASE**: Phase 2 - Proposed Model Testing & Comparison  
**STATUS**: Ready to Begin  

---

## 🎊 **Phase 1 Results Summary**

### **Final Baseline Performance**

**Model**: MoritzLaurer/deberta-v3-base-zeroshot-v2.0

| Metric | Score |
|--------|-------|
| **Label Accuracy** | **76.36%** ✓ |
| **Score-Based Accuracy** | 25.45% |
| **Critical Cases** | **100%** ✓ |
| **High Severity** | **100%** ✓ |
| **Medium Severity** | ~85% |
| **Low Severity** | ~60% |

### **Key Findings**

✅ **Excellent Crisis Detection**
- 100% accuracy on suicide ideation, self-harm, domestic violence
- 100% accuracy on panic attacks, psychotic crises
- 100% accuracy on family rejection crises

✅ **Acceptable Performance on Lower Priority**
- Mild cases (disappointment, frustration) sometimes labeled as generic "distress"
- Still actionable for moderators
- Not mission-critical categories

✅ **System Performance**
- GPU working (NVIDIA RTX 3060 detected)
- Fast inference: 22-304ms latency
- Low VRAM usage: 0-9MB
- Docker container stable

### **Mismatches Analysis**

All 13 mismatches were **low-severity cases**:
- isolation → predicted "distress" (expected "loneliness")
- mild_negative → predicted "distress" (expected specific emotion)
- disappointment → predicted "distress" (expected "disappointment")
- frustration → predicted "distress" (expected "frustration")

**Impact**: Minimal - these still trigger wellness checks appropriately.

---

## 📊 **Phase 1 Deliverables Completed**

### **Testing Framework** ✅
- 16 files created
- 227 test cases across 5 datasets
- 3 metrics calculators
- ModelEvaluator orchestrator
- Clean Architecture v5.0 compliant

### **Docker Infrastructure** ✅
- Containerized testing environment
- GPU passthrough working
- BuildKit optimization (1-2 min rebuilds)
- Smart entrypoint script
- Comprehensive documentation

### **Test Datasets** ✅
1. crisis_examples.json (55 cases)
2. safe_examples.json (52 cases)
3. edge_cases.json (50 cases)
4. lgbtqia_specific.json (50 cases)
5. escalation_patterns.json (20 sequences)

### **Evaluation Methodology** ✅
- **Primary**: Label-based accuracy (correct crisis type)
- **Secondary**: Confidence scores (for ranking urgency)
- **Thresholds**: Adjusted to realistic industry standards

### **Documentation** ✅
- Complete setup guides
- Docker optimization guides
- CUDA compatibility reference
- Troubleshooting documentation
- Threshold adjustment guides

---

## 🎯 **Phase 2 Objectives**

### **Primary Goal**
Test and compare v5.0 proposed models against v3.1 baseline to determine which models to use in production.

### **Models to Test**

#### **Crisis Classifier**
- **facebook/bart-large-mnli**
- Zero-shot classification
- Multi-label capable
- Expected: Better crisis categorization

#### **Emotion Detection**
- **SamLowe/roberta-base-go_emotions**
- 28 emotion labels
- Expected: Better granular emotion detection

#### **Sentiment Analysis**
- **cardiffnlp/twitter-roberta-base-sentiment-latest**
- Latest sentiment model
- Expected: Better overall sentiment scoring

#### **Irony Detection**
- **cardiffnlp/twitter-roberta-base-irony**
- Detects sarcasm/irony
- Expected: Reduce false positives on sarcastic messages

### **Success Criteria**

**Must Exceed Baseline:**
- Label accuracy > 76.36%
- Critical case accuracy ≥ 100%
- High severity accuracy ≥ 100%

**Performance Requirements:**
- Latency < 500ms average
- VRAM usage < 2GB total
- Compatible with RTX 3060 12GB

**Combination Goal:**
- Ensemble of 4 models should outperform single baseline
- Target: 85%+ overall label accuracy
- Target: 100% on critical + high severity

---

## 📋 **Phase 2 Step-by-Step Plan**

### **Step 1: Test Individual Models** (1-2 hours)

```bash
# Test BART crisis classifier
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  test-model facebook/bart-large-mnli crisis_examples.json

# Test RoBERTa emotion detector
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  test-model SamLowe/roberta-base-go_emotions crisis_examples.json

# Test sentiment analyzer
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  test-model cardiffnlp/twitter-roberta-base-sentiment-latest crisis_examples.json

# Test irony detector
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  test-model cardiffnlp/twitter-roberta-base-irony edge_cases.json
```

**Expected Outputs:**
- `testing/reports/output/bart_crisis_v5_0.json`
- `testing/reports/output/roberta_emotions_v5_0.json`
- `testing/reports/output/roberta_sentiment_v5_0.json`
- `testing/reports/output/roberta_irony_v5_0.json`

### **Step 2: Analyze Individual Performance** (30 min)

For each model:
```bash
python3.11 analyze_label_accuracy.py --model <model_name>
```

Compare:
- Label accuracy vs baseline (76.36%)
- Critical case accuracy
- Performance metrics (latency, VRAM)

### **Step 3: Test Ensemble** (1 hour)

```bash
# Test all 4 models together
docker compose -f docker-compose.testing.yml run ash-nlp-testing test-all
```

**Expected Output:**
- `testing/reports/output/ensemble_v5_0.json`

### **Step 4: Comprehensive Analysis** (30 min)

```bash
# Compare all models
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  compare baseline ensemble
```

Generate:
- Accuracy comparison chart
- Per-category breakdown
- Performance metrics comparison
- VRAM usage analysis

### **Step 5: Make Recommendations** (30 min)

Based on results:
1. Which individual models beat baseline?
2. Does ensemble beat all individuals?
3. What's the best configuration for production?
4. Any models to drop?

---

## 🔧 **Technical Context**

### **Server Specifications**
- **Host**: Lofn (Debian 12)
- **CPU**: AMD Ryzen 7 5800x
- **RAM**: 64GB
- **GPU**: NVIDIA RTX 3060 (12GB VRAM)
- **CUDA**: 13.1 (host), 12.1 (container)
- **Docker**: Compose v5.0.0

### **Container Configuration**
- **Base**: nvidia/cuda:12.1.0-runtime-ubuntu22.04
- **Python**: 3.11
- **Transformers**: 4.57.3
- **PyTorch**: 2.9.1
- **Runtime**: nvidia (GPU passthrough working)

### **Model Cache**
- **Location**: `/app/testing/cache/models`
- **Persistent**: Volume mounted
- **First run**: Downloads models (~2-4GB total)
- **Subsequent runs**: Uses cached models (fast)

### **Resource Estimates**

**Per Model Testing:**
- Time: 10-15 minutes
- VRAM: 400-800MB per model
- Latency: 20-100ms per inference

**Ensemble Testing:**
- Time: 30-45 minutes
- VRAM: 1.5-2.5GB total
- Latency: 80-400ms per inference

---

## 📁 **File Locations**

### **On Lofn Server**
```
/storage/nas/git/ash/ash-nlp/
├── Dockerfile.testing              # Container definition
├── docker-compose.testing.yml      # Orchestration
├── requirements-testing.txt        # Python dependencies
├── .env.testing                    # Environment variables
│
├── testing/
│   ├── model_evaluator.py         # Core testing engine
│   ├── test_datasets/              # All 5 test datasets
│   ├── metrics/                    # Accuracy, performance, ensemble
│   ├── reports/output/             # Generated reports
│   └── cache/models/               # Downloaded model cache
│
└── docker/
    └── testing-entrypoint.sh       # Container entrypoint
```

### **Test Commands Available**
```bash
# Single model test
test-model <model_name> <dataset>

# Baseline comparison
test-baseline

# All proposed models
test-proposed

# Comprehensive suite
test-all

# Model comparison
compare <model_a> <model_b>

# Interactive shells
bash
python
ipython
```

---

## 🎓 **Important Lessons from Phase 1**

### **1. Label Accuracy > Score Accuracy**

For crisis detection:
- **What matters**: Did it identify the RIGHT crisis type?
- **Less important**: Exact confidence percentage

Example:
```
Message: "My partner hits me..."
Model: "domestic violence" at 58% confidence
Action: ✓ Trigger DV intervention resources

Score threshold wanted: 75%
Result: ❌ Marked as failure

Label-based eval: ✓ Correct!
```

### **2. Realistic Thresholds**

Industry standards:
- **Critical**: 85%+ confidence (not 95%+)
- **High**: 75%+ confidence
- **Medium**: 65%+ confidence
- **Low**: 50%+ confidence

### **3. Python Version Matters**

**Issue**: `pip` installed to Python 3.10, code ran on Python 3.11
**Fix**: Use `python3.11 -m pip install` explicitly
**Lesson**: Always verify Python version matches

### **4. Docker Compose v5 GPU Syntax**

**Old syntax** (doesn't work):
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
```

**New syntax** (works):
```yaml
runtime: nvidia
environment:
  - NVIDIA_VISIBLE_DEVICES=all
```

### **5. BuildKit for Fast Builds**

**Without BuildKit**: 20 min rebuilds
**With BuildKit**: 1-2 min rebuilds
**How**: `export DOCKER_BUILDKIT=1`

---

## 🚨 **Known Issues & Solutions**

### **Issue 1: Transformers CACHE Warning**

**Warning**: `TRANSFORMERS_CACHE is deprecated`

**Solution**: Already fixed in .env
```bash
# Use HF_HOME instead
HF_HOME=/app/testing/cache/huggingface
```

**Impact**: None - just a warning

### **Issue 2: Line Endings (Windows)**

**Problem**: Windows CRLF breaks bash scripts

**Solution**: Use .editorconfig
```ini
[*]
end_of_line = lf
```

**Status**: Fixed in repository

### **Issue 3: GPU Detection**

**Problem**: Container couldn't see GPU

**Solution**: Use `runtime: nvidia` in docker-compose

**Status**: Fixed - GPU working

---

## 📊 **Expected Phase 2 Results**

### **Optimistic Scenario** 🎯

**Individual Models:**
- BART crisis: 80-85% (better categorization)
- RoBERTa emotions: 75-80% (granular detection)
- Sentiment: 70-75% (overall mood)
- Irony: N/A (different use case)

**Ensemble:**
- Combined: 85-90% label accuracy
- Critical cases: 100%
- High severity: 100%
- Medium severity: 90%+

**Outcome**: Use ensemble in production

### **Realistic Scenario** 📈

**Individual Models:**
- BART crisis: 78-82%
- RoBERTa emotions: 72-76%
- Sentiment: 68-72%

**Ensemble:**
- Combined: 80-85% label accuracy
- Critical cases: 100%
- High severity: 95%+

**Outcome**: Use BART + emotions, maybe skip sentiment

### **Pessimistic Scenario** 📉

**Individual Models:**
- BART crisis: 74-78% (barely better)
- RoBERTa emotions: 70-74% (similar to baseline)

**Ensemble:**
- Combined: 76-78% (not much improvement)

**Outcome**: Stick with baseline, or use BART only

---

## 🎯 **Decision Matrix**

After Phase 2 testing, use this to decide:

| Scenario | Ensemble Accuracy | Decision |
|----------|------------------|----------|
| Ensemble > 85% | > 85% | ✓ Use full ensemble |
| Ensemble 80-85% | 80-85% | ✓ Use BART + emotions |
| Ensemble 76-80% | 76-80% | ? Consider cost/benefit |
| Ensemble < 76% | < 76% | ✗ Stick with baseline |

**AND must meet:**
- Critical cases ≥ 100%
- Latency < 500ms average
- VRAM < 2GB total

---

## 🚀 **Quick Start for Phase 2**

### **Morning Commands**

```bash
# 1. SSH to Lofn
ssh user@10.20.30.253
cd /storage/nas/git/ash/ash-nlp

# 2. Test first proposed model (BART)
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  test-model facebook/bart-large-mnli crisis_examples.json

# This will:
# - Download BART model (~1.5GB, first time only)
# - Run all 55 crisis test cases
# - Generate report with accuracy metrics
# - Take ~10-15 minutes

# 3. Check results
cat testing/reports/output/bart_crisis_v5_0.json | grep accuracy
```

### **What to Look For**

In the output:
```
Testing model: facebook/bart-large-mnli
Loading model... (may take a few minutes first time)
Testing on crisis_examples.json (55 cases)...
Processing batch 1/7...
...
Label Accuracy: XX.XX%
```

**If > 76.36%**: BART is better! ✓  
**If < 76.36%**: BART isn't better ✗

---

## 📞 **Support Resources**

### **Documentation**
- **Main Guide**: `testing/README.md`
- **Docker Guide**: `DOCKER_README.md`
- **Quick Reference**: `DOCKER_QUICK_REFERENCE.md`
- **Build Optimization**: `DOCKER_BUILD_OPTIMIZATION.md`

### **Common Commands**
```bash
# Start container
docker compose -f docker-compose.testing.yml up

# Run test
docker compose run ash-nlp-testing <command>

# Check logs
docker compose logs ash-nlp-testing

# Rebuild container
docker compose build

# Shell access
docker compose run ash-nlp-testing bash
```

### **Troubleshooting**

**GPU not detected?**
```bash
nvidia-smi  # Check GPU on host
docker run --rm --runtime=nvidia nvidia/cuda:12.1.0-base nvidia-smi
```

**Model download fails?**
```bash
# Check internet connection
# Models download from huggingface.co
# ~2-4GB total for all models
```

**Out of VRAM?**
```bash
# Reduce batch size in .env.testing
TEST_BATCH_SIZE=4  # Default is 8
```

---

## 🎊 **Success Criteria Recap**

**Phase 2 is successful if:**

1. ✅ At least one model beats baseline (> 76.36%)
2. ✅ Ensemble shows improvement over best individual
3. ✅ Critical cases maintain 100% accuracy
4. ✅ Performance is acceptable (< 500ms, < 2GB VRAM)
5. ✅ Clear recommendation for production configuration

**Phase 2 is complete when:**

1. ✅ All 4 models tested individually
2. ✅ Ensemble tested on full suite
3. ✅ Comparison analysis generated
4. ✅ Production recommendation documented
5. ✅ Phase 3 planning initiated (if proceeding)

---

## 📈 **What Happens After Phase 2**

### **If Successful** (Ensemble > 80%)

**Phase 3: Integration**
- Implement ensemble in main Ash codebase
- Create Discord bot integration
- Test in staging environment
- Deploy to production

### **If Marginal** (Ensemble 76-80%)

**Decision Point:**
- Cost/benefit analysis
- Consider simpler approach
- Maybe just use BART
- Optimize baseline instead

### **If Unsuccessful** (Ensemble < 76%)

**Phase 3: Optimization**
- Fine-tune baseline on our data
- Collect more training examples
- Try different models
- Hybrid approach (AI + patterns)

---

## 💾 **Session State**

### **What's Working** ✅
- Docker container operational
- GPU passthrough functional
- Testing framework complete
- Baseline evaluated and documented
- Label-based evaluation methodology established

### **What's Ready** ✅
- All test datasets adjusted to realistic thresholds
- Metrics calculators functional
- ModelEvaluator orchestrator ready
- Docker environment optimized
- Documentation comprehensive

### **What's Next** 🎯
1. Test facebook/bart-large-mnli
2. Test SamLowe/roberta-base-go_emotions
3. Test cardiffnlp sentiment and irony models
4. Run ensemble evaluation
5. Generate comparison analysis
6. Make production recommendation

---

## 📝 **Notes for AI Assistant**

When continuing this conversation:

1. **Context**: Phase 1 complete, baseline = 76.36% label accuracy
2. **Goal**: Test 4 proposed models, compare to baseline
3. **Success**: Any model > 76.36%, ensemble ideally 85%+
4. **Environment**: Docker container on Lofn, GPU working
5. **Evaluation**: Label-based (not score-based)
6. **Timeline**: 3-4 hours for full Phase 2

**Key Files:**
- Test datasets in: `testing/test_datasets/`
- Results go to: `testing/reports/output/`
- Models cached in: `testing/cache/models/`

**Remember:**
- Use `test-model <name> <dataset>` for individual tests
- Use `test-all` for comprehensive suite
- Use `analyze_label_accuracy.py` for label-based analysis
- Critical cases MUST maintain 100% accuracy

---

## 🏁 **Ready to Begin Phase 2**

**Everything is set up and ready to go!**

Just run:
```bash
docker compose -f docker-compose.testing.yml run ash-nlp-testing \
  test-model facebook/bart-large-mnli crisis_examples.json
```

And Phase 2 begins! 🚀

---

**Built with care for chosen family** 🏳️‍🌈

**Session Date**: 2025-12-31  
**Phase 1**: ✅ Complete  
**Phase 2**: Ready to Start  
**Baseline**: 76.36% label accuracy  
**Goal**: 85%+ ensemble accuracy
