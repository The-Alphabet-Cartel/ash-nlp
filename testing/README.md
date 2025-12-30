# Ash-NLP Testing Framework v5.0

**FILE VERSION**: v5.0  
**LAST MODIFIED**: 2025-12-30  
**CLEAN ARCHITECTURE**: v5.0 Compliant  

---

## Overview

Comprehensive testing framework for evaluating AI models in Ash-NLP's crisis detection system. Built to support the transition from v3.1 to v5.0 with Local Multi-Model Ensemble architecture.

## Directory Structure

```
testing/
├── __init__.py                      # Package initialization
├── model_evaluator.py               # Main evaluation orchestrator
├── test_datasets/                   # Test data for validation
│   ├── crisis_examples.json         # 55 crisis messages (critical → low)
│   ├── safe_examples.json           # 52 non-crisis messages
│   ├── edge_cases.json              # 50 challenging cases (sarcasm, ambiguity)
│   ├── lgbtqia_specific.json        # 50 LGBTQIA+ community-specific cases
│   └── escalation_patterns.json     # 20 temporal escalation sequences
├── metrics/                         # Metrics calculation modules
│   ├── accuracy_calculator.py       # Precision, recall, F1 scores
│   ├── performance_tracker.py       # Latency, VRAM, CPU metrics
│   └── ensemble_analyzer.py         # Multi-model agreement analysis
├── reports/                         # Report generation (Phase 1 Step 1.9)
└── config/
    └── test_config.json             # Testing configuration
```

## Quick Start

### 1. Basic Model Testing

```python
from testing import create_model_evaluator

# Initialize evaluator
evaluator = create_model_evaluator()

# Test a model against crisis examples
results = evaluator.test_dataset(
    model_name="facebook/bart-large-mnli",
    dataset_path="testing/test_datasets/crisis_examples.json",
    task_type="zero-shot-classification"
)

# Generate report
report = evaluator.generate_report(results, output_path="reports/test_results.json")
```

### 2. Model Comparison

```python
# Compare two models
comparison = evaluator.compare_models(
    model_a="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",  # Current v3.1
    model_b="facebook/bart-large-mnli",                     # Proposed v5.0
    dataset_path="testing/test_datasets/crisis_examples.json",
    task_type="zero-shot-classification"
)

print(f"Accuracy improvement: {comparison['improvements']['accuracy']['percentage']:.2f}%")
```

### 3. Single Test Case

```python
# Load model
model = evaluator.load_model("facebook/bart-large-mnli", task="zero-shot-classification")

# Test single message
test_case = {
    "id": "test_001",
    "message": "I'm planning to end it tonight",
    "expected_outputs": {
        "crisis_score": {"min": 0.95, "max": 1.0},
        "crisis_level": "critical"
    }
}

result = evaluator.test_single_case(model, test_case, task_type="zero-shot-classification")
print(f"Predicted score: {result['predicted_score']:.3f}")
print(f"Correct: {result['is_correct']}")
```

## Test Datasets

### Crisis Examples (`crisis_examples.json`)
**55 test cases** covering full crisis severity spectrum:
- **Critical (15 cases)**: Explicit suicide ideation, active self-harm, immediate danger
- **High (20 cases)**: Severe depression, persistent ideation, acute distress
- **Medium (12 cases)**: Moderate depression, anxiety, isolation
- **Low (8 cases)**: Mild negative mood, minor stress

**Purpose**: Validate model's ability to correctly identify and grade crisis severity.

### Safe Examples (`safe_examples.json`)
**52 test cases** of non-crisis messages:
- **Metaphorical Language (15 cases)**: Gaming phrases, idioms ("This game is killing me")
- **Positive Expressions (20 cases)**: Celebrations, achievements, gratitude
- **Neutral Conversations (17 cases)**: General chat, questions, daily activities

**Purpose**: Prevent false positives - ensure safe messages aren't flagged as crises.

### Edge Cases (`edge_cases.json`)
**50 challenging test cases**:
- **Sarcasm/Irony (20 cases)**: "Best day ever" when actually in crisis
- **Ambiguous Severity (15 cases)**: Context-dependent, unclear intent
- **Community Language (15 cases)**: LGBTQIA+ slang, internet memes, neurodivergent language

**Purpose**: Test model robustness on difficult-to-classify messages.

### LGBTQIA+ Specific (`lgbtqia_specific.json`)
**50 community-focused cases**:
- **Identity Crisis (12 cases)**: Coming out distress, questioning, confusion
- **Family/Social Rejection (12 cases)**: Disownment, religious trauma, isolation
- **Dysphoria (8 cases)**: Gender dysphoria, body image distress
- **Positive Identity (10 cases)**: Pride, celebration, affirmation
- **Community Language (8 cases)**: T4T, enby, transfem, etc.

**Purpose**: Ensure culturally competent crisis detection for LGBTQIA+ community.

### Escalation Patterns (`escalation_patterns.json`)
**20 multi-message sequences**:
- **Rapid Escalation (7 patterns)**: Hours-long deterioration
- **Gradual Escalation (8 patterns)**: Days/weeks of worsening
- **Sudden Onset (5 patterns)**: Acute traumatic events

**Purpose**: Test context analyzer's ability to detect temporal patterns (Phase 4).

## Metrics

### Accuracy Metrics
```python
from testing.metrics import create_accuracy_calculator

calc = create_accuracy_calculator()

# Calculate comprehensive metrics
report = calc.generate_classification_report(
    predictions=[True, True, False, True],
    ground_truth=[True, False, False, True]
)

print(f"Accuracy: {report['metrics']['accuracy']:.3f}")
print(f"Precision: {report['metrics']['precision']:.3f}")
print(f"Recall: {report['metrics']['recall']:.3f}")
print(f"F1 Score: {report['metrics']['f1_score']:.3f}")
```

### Performance Metrics
```python
from testing.metrics import create_performance_tracker

tracker = create_performance_tracker()

# Track latency
result, latency_ms = tracker.measure_latency(model.predict, "test message")
print(f"Latency: {latency_ms:.2f}ms")

# Get VRAM usage
vram_mb = tracker.get_vram_usage()
print(f"VRAM: {vram_mb:.2f}MB")

# Generate performance report
report = tracker.generate_performance_report(
    latencies=[1200, 1150, 1300, 1250],
    vram_usages=[800, 820, 810, 815]
)
```

### Ensemble Analysis (Phase 3)
```python
from testing.metrics import create_ensemble_analyzer

analyzer = create_ensemble_analyzer()

# Analyze model agreement
agreement_rate = analyzer.calculate_agreement_rate(model_results)
print(f"Models agree {agreement_rate*100:.1f}% of the time")

# Find disagreements
disagreements = analyzer.identify_disagreements(model_results, threshold=0.3)
print(f"Found {len(disagreements)} significant disagreements")

# Full ensemble report
report = analyzer.generate_ensemble_report([
    model1_results,
    model2_results,
    model3_results,
    model4_results
])
```

## Configuration

### Environment Variables

Add to `.env.template`:
```bash
# Testing Configuration
TEST_DEVICE=cuda                     # or 'cpu'
TEST_BATCH_SIZE=8
TEST_TIMEOUT=30
TEST_PARALLEL=false
TEST_VERBOSE=true

# Accuracy Thresholds
TEST_ACCURACY_THRESHOLD=0.85
TEST_PRECISION_THRESHOLD=0.80
TEST_RECALL_THRESHOLD=0.85
TEST_F1_THRESHOLD=0.82

# Performance Thresholds
TEST_LATENCY_THRESHOLD=5000          # milliseconds
TEST_VRAM_THRESHOLD=2000             # MB

# Dataset Paths
TEST_DATASET_CRISIS=testing/test_datasets/crisis_examples.json
TEST_DATASET_SAFE=testing/test_datasets/safe_examples.json
TEST_DATASET_EDGE=testing/test_datasets/edge_cases.json
TEST_DATASET_LGBTQIA=testing/test_datasets/lgbtqia_specific.json
TEST_DATASET_ESCALATION=testing/test_datasets/escalation_patterns.json

# Reporting
TEST_REPORT_OUTPUT_DIR=testing/reports/output
TEST_GENERATE_HTML=true
TEST_GENERATE_JSON=true
TEST_SAVE_CHARTS=true

# Baseline Comparison
TEST_BASELINE_MODEL=MoritzLaurer/deberta-v3-base-zeroshot-v2.0
```

## Expected Results

### v3.1 Baseline Performance
```
Model: MoritzLaurer/deberta-v3-base-zeroshot-v2.0
├── Accuracy: ~75-80%
├── Precision: ~70-75%
├── Recall: ~75-80%
├── F1 Score: ~72-77%
├── Latency: ~2-3 seconds
└── VRAM: ~400-600MB
```

### v5.0 Target Performance
```
Ensemble: 4 models (BART + RoBERTa variants)
├── Accuracy: >85% (target: 90%)
├── Precision: >80%
├── Recall: >85%
├── F1 Score: >82%
├── Latency: <10 seconds
├── VRAM: <2GB total
└── Agreement Rate: >70%
```

## Common Testing Patterns

### Pattern 1: Baseline Current Model
```python
# Step 1: Test v3.1 models
baseline_results = {}
for model_name in ["deberta-depression", "deberta-sentiment", "deberta-distress"]:
    results = evaluator.test_dataset(model_name, "crisis_examples.json")
    baseline_results[model_name] = results

# Step 2: Save baseline
evaluator.generate_report(baseline_results, "reports/v3.1_baseline.json")
```

### Pattern 2: Validate New Model
```python
# Test proposed model
new_results = evaluator.test_dataset(
    "facebook/bart-large-mnli",
    "crisis_examples.json"
)

# Compare to baseline
comparison = evaluator.compare_models(
    "baseline_model",
    "facebook/bart-large-mnli",
    "crisis_examples.json"
)

# Accept if improvements meet targets
if comparison['improvements']['accuracy']['percentage'] > 5:
    print("✅ Model approved for v5.0")
```

### Pattern 3: Comprehensive Testing
```python
# Test against all datasets
datasets = [
    "crisis_examples.json",
    "safe_examples.json",
    "edge_cases.json",
    "lgbtqia_specific.json"
]

all_results = {}
for dataset in datasets:
    results = evaluator.test_dataset(model_name, f"test_datasets/{dataset}")
    all_results[dataset] = results

# Generate comprehensive report
evaluator.generate_report(all_results, "reports/comprehensive_test.json")
```

## Troubleshooting

### Issue: Models Not Loading
```python
# Check CUDA availability
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0)}")

# Fall back to CPU if needed
evaluator = create_model_evaluator()
evaluator.device = 'cpu'
```

### Issue: Out of Memory
```python
# Clear GPU cache between tests
tracker = create_performance_tracker()
tracker.clear_gpu_cache()

# Reduce batch size in config
# TEST_BATCH_SIZE=4 or TEST_BATCH_SIZE=1
```

### Issue: Slow Performance
```python
# Check system resources
report = tracker.generate_performance_report(latencies, vram_usages)
print(report['system'])

# Profile specific model
with tracker.track_latency() as timer:
    result = model.predict("test message")
print(f"Took {timer.elapsed_ms():.2f}ms")
```

## Clean Architecture Compliance

All testing code follows Clean Architecture Charter v5.0:

✅ **Factory Functions**: All classes use `create_*()` pattern  
✅ **Dependency Injection**: Configuration passed to constructors  
✅ **JSON + Env Config**: Defaults in JSON, overrides via environment  
✅ **Real Testing**: No mocks (Rule #8), actual model inference  
✅ **File Versioning**: All files include version headers  
✅ **Error Handling**: Production-ready resilience  

## Next Steps

### Phase 1 Complete ✅
- Testing framework operational
- All test datasets created
- Metrics calculators functional
- Baseline testing ready

### Phase 2: Model Migration
- Download proposed models (facebook/bart-large-mnli, etc.)
- Test each model independently
- Compare against v3.1 baseline
- Validate VRAM and latency constraints

### Phase 3: Ensemble Coordinator
- Implement multi-model consensus
- Test ensemble agreement patterns
- Use `EnsembleAnalyzer` for validation

### Phase 4: Context Analysis
- Test with `escalation_patterns.json`
- Validate temporal pattern detection
- Ensure context-aware scoring works

## Support

For issues or questions:
- Review Clean Architecture Charter: `docs/clean_architecture_charter.md`
- Check project roadmap: `docs/v5.0/roadmap.md`
- Discord: https://discord.gg/alphabetcartel

---

**Built with care for chosen family** 🏳️‍🌈
