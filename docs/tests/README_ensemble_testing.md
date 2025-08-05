# Ensemble Mode Testing Suite

This directory contains comprehensive tests to validate that changing the `NLP_ENSEMBLE_MODE` environment variable actually produces different responses from the Ash-NLP server.

## 🎯 Purpose

These tests ensure that the three ensemble modes (consensus, majority, weighted) are properly implemented and produce meaningfully different results when analyzing the same messages.

## 📁 Test Files

### 1. `test_ensemble_mode_quick.py` - Quick Validation
**Purpose**: Fast validation that ensemble modes are working
**Usage**: 
```bash
python tests/test_ensemble_mode_quick.py
python tests/test_ensemble_mode_quick.py --mode weighted
python tests/test_ensemble_mode_quick.py --message "Custom test message"
```

**What it tests**:
- Changes `.env` file to set different ensemble modes
- Analyzes the same message with each mode
- Compares results to verify differences
- Quick verification of basic functionality

### 2. `test_ensemble_configuration.py` - Configuration Deep Dive
**Purpose**: Comprehensive configuration system validation
**Usage**:
```bash
python tests/test_ensemble_configuration.py
```

**What it tests**:
- Weighted mode with different model weight configurations
- Consensus mode with different threshold settings
- Majority mode behavior across different message types
- Configuration loading and application verification

### 3. `test_ensemble_mode_switching.py` - Comprehensive Suite
**Purpose**: Full ensemble mode validation with detailed analysis
**Usage**:
```bash
python tests/test_ensemble_mode_switching.py
```

**What it tests**:
- Multiple test messages across all ensemble modes
- Detailed comparison analysis
- Gap detection differences
- Confidence variations
- Pattern matching integration

### 4. `run_ensemble_tests.py` - Test Runner
**Purpose**: Coordinates all tests and provides summary reporting
**Usage**:
```bash
# Run all tests
python tests/run_ensemble_tests.py

# Run specific test types
python tests/run_ensemble_tests.py --quick
python tests/run_ensemble_tests.py --config
python tests/run_ensemble_tests.py --full --save
```

## 🚀 Quick Start

### Prerequisites
1. **NLP Server Running**: Ensure your Ash-NLP server is running on `localhost:8881`
2. **Environment File**: Have a `.env` file in your project root (tests will modify it)
3. **Python Dependencies**: `requests` module installed
4. **Models Loaded**: All three models (depression, sentiment, emotional_distress) should be loaded

### Running the Tests

**Option 1: Quick Test (Recommended for development)**
```bash
python tests/test_ensemble_mode_quick.py
```

**Option 2: Full Test Suite**
```bash
python tests/run_ensemble_tests.py --full --save
```

**Option 3: Individual Tests**
```bash
# Test just configuration
python tests/test_ensemble_configuration.py

# Test comprehensive mode switching  
python tests/test_ensemble_mode_switching.py
```

## 📊 Expected Results

### ✅ Success Indicators
- **Different Predictions**: Same message produces different crisis levels across modes
- **Confidence Variations**: Confidence scores vary between ensemble modes
- **Method Differences**: Consensus method changes (weighted_average, majority_vote, etc.)
- **Gap Detection Changes**: Different modes trigger gap detection differently

### ❌ Failure Indicators
- **Identical Results**: All modes produce exactly the same output
- **No Configuration Changes**: Service doesn't pick up .env changes
- **Service Errors**: HTTP errors or timeouts during analysis

## 🔧 Configuration Testing

The tests specifically validate these environment variables:

### Ensemble Mode Selection
```bash
NLP_ENSEMBLE_MODE=consensus   # All models must agree
NLP_ENSEMBLE_MODE=majority    # Democratic voting
NLP_ENSEMBLE_MODE=weighted    # Configurable weights
```

### Model Weights (for weighted mode)
```bash
NLP_DEPRESSION_MODEL_WEIGHT=0.6      # Default: Depression model priority
NLP_SENTIMENT_MODEL_WEIGHT=0.15     # Default: Lower sentiment weight  
NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT=0.25  # Default: Moderate distress weight
```

### Gap Detection Thresholds
```bash
NLP_GAP_DETECTION_THRESHOLD=0.25     # When to detect model disagreement
NLP_DISAGREEMENT_THRESHOLD=0.35     # When to flag for review
```

## 📋 Test Messages

The tests use carefully selected messages that should trigger different responses:

1. **High Crisis Explicit**: `"I want to kill myself tonight"`
2. **Ambiguous Crisis**: `"This exam is killing me but I think I can handle it"`
3. **Moderate Crisis**: `"I don't want to be here anymore"`
4. **Hopelessness Pattern**: `"Everything is meaningless and I have no hope left"`
5. **False Positive Candidate**: `"I'm dying of laughter watching this comedy show"`

## 🐛 Troubleshooting

### Test Fails: "All modes produce identical results"
**Possible causes**:
- Service not restarting after .env changes
- Configuration not being reloaded
- Docker container needs restart
- Environment variables not being read

**Solutions**:
```bash
# If using Docker
docker-compose restart ash-nlp

# If running locally
# Kill and restart the Python service

# Verify configuration is loaded
curl http://localhost:8881/ensemble/status
```

### Test Fails: "Service not reachable"
**Solutions**:
- Check if service is running: `curl http://localhost:8881/health`
- Verify port 8881 is correct
- Check Docker containers: `docker-compose ps`

### Test Fails: "Models not loaded"
**Solutions**:
- Wait for models to finish loading (can take several minutes)
- Check service logs for loading errors
- Verify GPU/CPU resources are available

## 📁 Log Files

Test results are automatically saved to `tests/logs/` with timestamps:
- `ensemble_mode_test_YYYYMMDD_HHMMSS.log` - Detailed test execution logs
- `ensemble_mode_test_results_YYYYMMDD_HHMMSS.json` - Structured test results
- `ensemble_config_test_results_TIMESTAMP.json` - Configuration test results

## 🔗 Integration with CI/CD

These tests can be integrated into your continuous integration pipeline:

```yaml
# Example GitHub Actions step
- name: Test Ensemble Mode Switching
  run: |
    python tests/run_ensemble_tests.py --full
  env:
    NLP_ENSEMBLE_MODE: weighted
```

## 📖 Understanding the Results

### Successful Test Output
```
🎯 ENSEMBLE MODES ARE WORKING - Different modes produce different results!
✅ TEST PASSED - Ensemble modes are working!
```

### Failed Test Output  
```
❌ ENSEMBLE MODES MAY NOT BE WORKING - All modes produce identical results
❌ TEST FAILED - Ensemble modes may not be working!
```

### Configuration Analysis
The tests will show:
- **Prediction Differences**: Different crisis levels (high/medium/low)
- **Confidence Variations**: Numerical confidence score differences
- **Method Changes**: Algorithm method used (weighted_average, majority_vote, consensus)
- **Gap Detection**: Whether model disagreement was detected

## 🤝 Contributing

When adding new tests:
1. Follow the existing test pattern
2. Use descriptive test messages
3. Include both positive and negative test cases
4. Add appropriate logging and error handling
5. Update this README with new test descriptions

## 📞 Support

If tests consistently fail:
1. Check the implementation guide: `docs/implementation_guide_v3_1.md`
2. Verify your v3.1 architecture is complete
3. Review the ensemble configuration in `config/model_ensemble.json`
4. Check Discord: https://discord.gg/alphabetcartel