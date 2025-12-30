<!-- ash-nlp/docs/v5.0/roadmap.md -->
<!--
Ash-NLP v5.0 Complete Rewrite Roadmap
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: v5.0 Compliant
-->
# Ash-NLP v5.0 Complete Rewrite Roadmap

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Project**: Ash-NLP v5.0 - Local Multi-Model Ensemble for Crisis Detection  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org  
**FILE VERSION**: v5.0  
**LAST UPDATED**: 2025-12-30  
**CLEAN ARCHITECTURE**: v5.0 Compliant  

---

## 📋 **TABLE OF CONTENTS**

1. [Executive Summary](#executive-summary)
2. [Architecture Decision](#architecture-decision)
3. [Model Selection](#model-selection)
4. [Project Phases](#project-phases)
5. [Phase Tracking](#phase-tracking)
6. [Dependencies & Prerequisites](#dependencies--prerequisites)
7. [Success Criteria](#success-criteria)
8. [Rollback Procedures](#rollback-procedures)

---

## 🎯 **EXECUTIVE SUMMARY**

### **Project Goal**
Complete rewrite of Ash-NLP from v3.1 to v5.0, implementing Local Multi-Model Ensemble architecture inspired by LLM Council principles while maintaining Clean Architecture Charter v5.0 compliance.

### **Key Changes**
- ✅ **Architecture**: Single model → Local Multi-Model Ensemble (Council-inspired)
- ✅ **Models**: Upgrade from generic zero-shot to specialized crisis detection models
- ✅ **Testing**: Implement comprehensive model evaluation framework
- ✅ **Context**: Add rolling window analysis for temporal pattern detection
- ✅ **Privacy**: Maintain 100% local processing (no external APIs)
- ✅ **Cost**: Maintain $0 ongoing costs (GPU-based, no API fees)

### **Non-Negotiables**
- ⚠️ **Latency**: Must remain < 5 seconds per analysis
- ⚠️ **Privacy**: All data stays on local server (10.20.30.253)
- ⚠️ **Clean Architecture**: 100% v5.0 Charter compliance
- ⚠️ **Availability**: 24/7 uptime for crisis detection
- ⚠️ **VRAM**: Must fit within 12GB RTX 3060 constraints

---

## 🏛️ **ARCHITECTURE DECISION**

### **Selected Approach: Local Multi-Model Ensemble (Option 3)**

**Rationale**:
```
┌─────────────────────────────────────────────────────────────────┐
│              Discord Message → CrisisAnalyzer                   │
├─────────────────────────────────────────────────────────────────┤
│  Local GPU Ensemble (4 models running in parallel)              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────┐  │
│  │ Model 1:     │ │ Model 2:     │ │ Model 3:     │ │Model 4:│  │
│  │ Crisis       │ │ Emotion      │ │ Sentiment    │ │Irony   │  │
│  │ Severity     │ │ Detection    │ │ Analysis     │ │Detect  │  │
│  │ (Zero-Shot)  │ │ (28 classes) │ │ (Pos/Neg/Neu)│ │(Sarc.) │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Consensus Coordinator (Council-inspired logic)                 │
│  - Cross-validation between models                              │
│  - Confidence weighting                                         │
│  - Disagreement detection                                       │
├─────────────────────────────────────────────────────────────────┤
│  Pattern Enhancement (existing functionality)                   │
│  - Temporal modifiers                                           │
│  - Contextual patterns                                          │
├─────────────────────────────────────────────────────────────────┤
│  Context Analyzer (NEW - rolling window)                        │
│  - User message history (last 5-10 messages)                    │
│  - Escalation detection                                         │
│  - Temporal trends                                              │
├─────────────────────────────────────────────────────────────────┤
│  Crisis Score + Alert Decision                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why This Approach**:
- ✅ **Latency**: 3-7 seconds (acceptable for crisis detection)
- ✅ **Privacy**: 100% local, no external APIs
- ✅ **Cost**: $0 ongoing (electricity only)
- ✅ **Accuracy**: Multi-model consensus reduces false positives/negatives
- ✅ **Council Benefits**: Cross-validation without external dependencies
- ✅ **VRAM Efficient**: ~1.5GB total (well within 12GB limit)

**Rejected Alternatives**:
- ❌ Full LLM Council: 30-90s latency unacceptable for crisis detection
- ❌ API-based ensemble: Privacy concerns + $10-150/day costs
- ❌ Single model upgrade: Less robust than ensemble approach

---

## 🎯 **MODEL SELECTION**

### **Current Models (v3.1) - TO BE REPLACED**
```
❌ Depression: MoritzLaurer/deberta-v3-base-zeroshot-v2.0
   - Downloads: 276K | Generic zero-shot, not depression-specific
   
❌ Sentiment: Lowerated/lm6-deberta-v3-topic-sentiment  
   - Downloads: Unknown | Low validation, unclear performance
   
❌ Distress: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
   - Downloads: 7.7M | Good but generic NLI, not distress-specific
```

### **New Model Ensemble (v5.0) - LOCAL DEPLOYMENT**

#### **Model 1: Crisis Severity Classifier (Zero-Shot)**
```yaml
Model: facebook/bart-large-mnli
Downloads: 132.9M (457x more validated than current)
Likes: 1,507
Parameters: 407M
Task: Zero-shot classification with custom crisis labels
VRAM: ~800MB loaded
Latency: ~1-2 seconds

Crisis Labels:
  - "suicide ideation"
  - "self-harm thoughts"
  - "severe depression"
  - "panic attack"
  - "abuse situation"
  - "family rejection"
  - "identity crisis"
  - "mental health emergency"

Why: Industry standard, excellent semantic understanding, flexible labels
```

#### **Model 2: Emotion Detection (28 Classes)**
```yaml
Model: SamLowe/roberta-base-go_emotions
Downloads: 92.8M (most popular emotion detector)
Likes: 640
Parameters: 125M
Task: Multi-label emotion classification
VRAM: ~250MB loaded
Latency: ~0.5-1 second

Key Crisis Emotions:
  - sadness, grief, disappointment
  - fear, nervousness, confusion
  - remorse, disgust (toward self)
  - anger (internalized)

Why: 28 emotion classes provide granular emotional state analysis
Dataset: Google GoEmotions (highest quality emotion dataset)
```

#### **Model 3: Sentiment Analysis (Social Media Optimized)**
```yaml
Model: cardiffnlp/twitter-roberta-base-sentiment-latest
Downloads: 295.9M (most validated sentiment model)
Likes: 746
Parameters: 125M
Task: 3-class sentiment (Negative, Neutral, Positive)
VRAM: ~250MB loaded
Latency: ~0.3-0.5 seconds
Updated: 2025 (most recent)

Classes:
  - Negative (crisis indicator when high)
  - Neutral (context dependent)
  - Positive (reduces crisis score)

Why: Trained on Twitter (similar informal language to Discord)
Specialized: Social media language patterns
```

#### **Model 4: Irony/Sarcasm Detection (NEW)**
```yaml
Model: cardiffnlp/twitter-roberta-base-irony
Downloads: 71.1K
Likes: 29
Parameters: 125M
Task: Binary classification (Ironic / Not Ironic)
VRAM: ~250MB loaded
Latency: ~0.3-0.5 seconds

Critical Use Cases:
  - "I'm just great" (when actually in crisis)
  - "Best day ever" (sarcastic during depression)
  - "Love my life right now" (ironic statement)

Why: Prevents misclassification of sarcastic crisis messages as positive
Essential: LGBTQIA+ community often uses sarcasm to cope
```

### **Total Ensemble Resources**
```
Total VRAM: ~1.55GB (12.9% of 12GB available)
Total Parameters: ~782M
Expected Latency: 3-7 seconds for full ensemble analysis
Remaining VRAM: ~10.45GB for batch processing and caching
```

---

## 📊 **PROJECT PHASES**

### **Phase Dependency Map**
```
Phase 0: Foundation & Planning (Current)
    ↓
Phase 1: Testing Framework Setup ← Prerequisite for all model work
    ↓
Phase 2: Model Migration & Integration
    ↓
Phase 3: Ensemble Coordinator Implementation
    ↓
Phase 4: Context Analysis Integration
    ↓
Phase 5: Pattern Enhancement Integration
    ↓
Phase 6: Production Deployment & Optimization
    ↓
Phase 7: Monitoring & Continuous Improvement
```

---

## 📝 **PHASE 0: FOUNDATION & PLANNING**

### **Status**: ✅ **COMPLETED** (2025-12-30)

### **Deliverables**:
- [x] Architecture decision documented (Local Multi-Model Ensemble)
- [x] Model selection finalized (4 models identified)
- [x] Roadmap created (this document)
- [x] Clean Architecture Charter v5.0 reviewed
- [x] Resource constraints validated (VRAM, latency, cost)

### **Decisions Made**:
1. ✅ Local ensemble approach selected over API-based council
2. ✅ Four-model ensemble composition finalized
3. ✅ Testing-first approach established
4. ✅ Privacy and cost constraints maintained

---

## 📝 **PHASE 1: TESTING FRAMEWORK SETUP**

### **Status**: ⏳ **NOT STARTED**

### **Duration**: 1-2 weeks
### **Priority**: CRITICAL (Prerequisite for all model work)

### **Objectives**:
- Create comprehensive model evaluation framework
- Build test datasets for crisis detection validation
- Establish baseline metrics with current models
- Implement automated model comparison tools

### **Clean Architecture Compliance**:
- ✅ All test classes use factory functions
- ✅ Configuration via JSON + environment variables
- ✅ Dependency injection for test managers
- ✅ File versioning headers on all test files
- ✅ Real-world testing (not mocks) per Rule #8

---

### **Step 1.1: Create Testing Directory Structure**

**Tasks**:
- [ ] Create `testing/` directory in project root
- [ ] Create `testing/model_evaluator.py` (main orchestrator)
- [ ] Create `testing/test_datasets/` directory
- [ ] Create `testing/metrics/` directory  
- [ ] Create `testing/reports/` directory
- [ ] Create `testing/config/` directory for test configuration

**Directory Structure**:
```
ash-nlp/
├── testing/
│   ├── __init__.py
│   ├── model_evaluator.py          # Main evaluation orchestrator
│   ├── test_datasets/
│   │   ├── __init__.py
│   │   ├── crisis_examples.json    # High-severity crisis messages
│   │   ├── safe_examples.json      # Non-crisis messages
│   │   ├── edge_cases.json         # Ambiguous cases (sarcasm, etc.)
│   │   ├── lgbtqia_specific.json   # Community-specific language
│   │   └── escalation_patterns.json # Temporal escalation examples
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── accuracy_calculator.py  # Precision, Recall, F1
│   │   ├── confusion_matrix.py     # Visual confusion analysis
│   │   ├── performance_tracker.py  # Speed, VRAM, latency
│   │   └── ensemble_analyzer.py    # Multi-model agreement metrics
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── model_comparison.py     # Generate comparison reports
│   │   ├── visualization.py        # Charts and graphs
│   │   └── report_templates/       # HTML/JSON report templates
│   └── config/
│       ├── test_config.json        # Testing configuration
│       └── baseline_thresholds.json # Expected performance baselines
```

**File Versioning Requirements**:
```python
# All testing files must include:
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification

Testing Framework - [Component Name]
---
FILE VERSION: v5.0
LAST MODIFIED: YYYY-MM-DD
CLEAN ARCHITECTURE: v5.0 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""
```

**Deliverables**:
- [ ] Directory structure created and validated
- [ ] `__init__.py` files in all directories
- [ ] README.md in `testing/` explaining framework usage

---

### **Step 1.2: Create Test Dataset - Crisis Examples**

**File**: `testing/test_datasets/crisis_examples.json`

**Requirements**:
- Minimum 50 test cases covering spectrum of crisis severity
- Each test case includes expected outputs for validation
- Covers diverse crisis types (suicide, self-harm, abuse, identity crisis)
- Includes temporal urgency markers ("tonight", "right now", "can't wait")

**Test Case Structure**:
```json
{
  "_metadata": {
    "file_version": "v5.0",
    "last_modified": "YYYY-MM-DD",
    "description": "Crisis message test dataset for model evaluation",
    "total_cases": 50,
    "severity_distribution": {
      "critical": 15,
      "high": 20,
      "medium": 10,
      "low": 5
    }
  },
  "test_cases": [
    {
      "id": "crisis_001",
      "message": "I'm planning to end it tonight. I can't take this anymore.",
      "expected_outputs": {
        "crisis_score": {
          "min": 0.95,
          "max": 1.0
        },
        "crisis_level": "critical",
        "model_expectations": {
          "bart_crisis": ["suicide ideation", "mental health emergency"],
          "emotions": ["sadness", "despair", "hopelessness"],
          "sentiment": "negative",
          "irony": "not_ironic"
        },
        "temporal_flags": ["tonight"],
        "pattern_matches": ["suicide_ideation", "temporal_urgency"]
      },
      "context": {
        "severity": "critical",
        "requires_immediate_intervention": true,
        "test_category": "explicit_suicide_ideation"
      }
    }
  ]
}
```

**Test Categories Required**:
1. **Critical Crisis** (15 cases):
   - Explicit suicide ideation
   - Immediate self-harm threats
   - Active abuse situations
   - Urgent temporal markers

2. **High Crisis** (20 cases):
   - Severe depression indicators
   - Self-harm thoughts (not immediate)
   - Family rejection crisis
   - Identity crisis with distress

3. **Medium Crisis** (10 cases):
   - Moderate depression
   - Anxiety/panic indicators
   - Chronic stress/burnout
   - Social isolation

4. **Low Crisis** (5 cases):
   - General negative mood
   - Frustration/anger
   - Disappointment
   - Mild anxiety

**Tasks**:
- [ ] Create crisis_examples.json with 50+ test cases
- [ ] Review with mental health crisis expert (if available)
- [ ] Validate JSON structure and completeness
- [ ] Document test case creation methodology

---

### **Step 1.3: Create Test Dataset - Safe Examples**

**File**: `testing/test_datasets/safe_examples.json`

**Requirements**:
- Minimum 50 test cases of non-crisis messages
- Include false positive triggers (metaphorical language)
- Cover positive emotional expressions
- Include LGBTQIA+ positive identity affirmations

**Test Categories**:
1. **Metaphorical Language** (15 cases):
   ```json
   {
     "id": "safe_001",
     "message": "This game is killing me, it's so hard!",
     "expected_outputs": {
       "crisis_score": {"min": 0.0, "max": 0.2},
       "crisis_level": "none",
       "model_expectations": {
         "emotions": ["frustration", "amusement"],
         "sentiment": "neutral",
         "irony": "not_ironic"
       }
     },
     "context": {
       "test_category": "metaphorical_language",
       "false_positive_risk": "high"
     }
   }
   ```

2. **Positive Expressions** (20 cases):
   - Joy, excitement, pride
   - Celebration of identity
   - Support for others
   - General positive mood

3. **Neutral Conversations** (15 cases):
   - General chat
   - Gaming discussions
   - Information sharing
   - Casual conversation

**Tasks**:
- [ ] Create safe_examples.json with 50+ test cases
- [ ] Include diverse false positive scenarios
- [ ] Cover LGBTQIA+ positive language
- [ ] Validate against crisis false positive triggers

---

### **Step 1.4: Create Test Dataset - Edge Cases**

**File**: `testing/test_datasets/edge_cases.json`

**Critical Edge Cases**:
1. **Sarcasm/Irony** (20 cases):
   ```json
   {
     "id": "edge_001",
     "message": "Best day of my life. Just perfect. Everything's great.",
     "expected_outputs": {
       "crisis_score": {"min": 0.5, "max": 0.8},
       "model_expectations": {
         "sentiment": "positive_surface",
         "irony": "ironic",
         "actual_sentiment": "negative"
       }
     },
     "context": {
       "test_category": "sarcastic_crisis",
       "detection_difficulty": "high"
     }
   }
   ```

2. **Ambiguous Severity** (15 cases):
   - Messages that could be mild or severe
   - Context-dependent severity
   - Need for additional information

3. **Cultural/Community Language** (15 cases):
   - LGBTQIA+ slang
   - Gaming terminology
   - Memes and internet culture

**Tasks**:
- [ ] Create edge_cases.json with 50+ challenging cases
- [ ] Include heavy sarcasm examples
- [ ] Cover ambiguous severity scenarios
- [ ] Document expected model behavior on edge cases

---

### **Step 1.5: Create Test Dataset - LGBTQIA+ Specific**

**File**: `testing/test_datasets/lgbtqia_specific.json`

**Critical Requirements**:
- Community-reviewed for cultural sensitivity
- Covers identity crisis scenarios
- Includes family rejection situations
- Contains positive identity affirmations

**Test Categories**:
1. **Identity Crisis** (15 cases):
   - Coming out distress
   - Dysphoria-related crisis
   - Identity questioning

2. **Family/Social Rejection** (15 cases):
   - Disownment scenarios
   - Religious trauma
   - Social isolation

3. **Positive Identity** (10 cases):
   - Pride celebrations
   - Transition milestones
   - Community support

4. **Community Language** (10 cases):
   - LGBTQIA+ terminology
   - Safe expressions
   - Coded language

**Tasks**:
- [ ] Create lgbtqia_specific.json with 50+ cases
- [ ] Get community feedback on test cases
- [ ] Ensure cultural sensitivity and accuracy
- [ ] Document community-specific patterns

---

### **Step 1.6: Create Test Dataset - Escalation Patterns**

**File**: `testing/test_datasets/escalation_patterns.json`

**Purpose**: Test context analyzer's ability to detect worsening situations

**Structure**:
```json
{
  "escalation_001": {
    "user_id": "test_user_001",
    "message_sequence": [
      {
        "timestamp": "2025-01-01T10:00:00Z",
        "message": "Having a rough day",
        "expected_crisis_score": 0.2
      },
      {
        "timestamp": "2025-01-01T14:00:00Z",
        "message": "Things aren't getting better",
        "expected_crisis_score": 0.4
      },
      {
        "timestamp": "2025-01-01T20:00:00Z",
        "message": "I don't know how much longer I can do this",
        "expected_crisis_score": 0.7
      },
      {
        "timestamp": "2025-01-01T23:00:00Z",
        "message": "I'm done. This is it.",
        "expected_crisis_score": 0.95
      }
    ],
    "expected_escalation_detected": true,
    "escalation_rate": "rapid",
    "intervention_point": 2
  }
}
```

**Tasks**:
- [ ] Create escalation_patterns.json with 20+ sequences
- [ ] Include various escalation speeds (rapid, gradual, sudden)
- [ ] Define clear intervention points
- [ ] Document expected context analyzer behavior

---

### **Step 1.7: Implement ModelEvaluator Class**

**File**: `testing/model_evaluator.py`

**Clean Architecture Requirements**:
- ✅ Factory function: `create_model_evaluator()`
- ✅ Dependency injection for configuration
- ✅ JSON configuration for test parameters
- ✅ File versioning header
- ✅ Real model testing (not mocks)

**Core Functionality**:
```python
class ModelEvaluator:
    """
    Model evaluation and comparison framework for Ash-NLP
    
    Responsibilities:
    - Load and test AI models against standardized datasets
    - Calculate accuracy, precision, recall, F1 scores
    - Compare models against baselines
    - Generate comprehensive performance reports
    - Track VRAM usage and latency metrics
    """
    
    def __init__(self, unified_config_manager):
        """Initialize with UnifiedConfigManager dependency"""
        pass
    
    def load_model(self, model_name: str) -> Pipeline:
        """Load model for testing"""
        pass
    
    def test_single_case(self, model, test_case: Dict) -> Dict:
        """Test model against single test case"""
        pass
    
    def test_dataset(self, model, dataset_file: str) -> Dict:
        """Test model against entire dataset"""
        pass
    
    def compare_models(
        self, 
        model_a: str, 
        model_b: str, 
        dataset: str
    ) -> Dict:
        """Compare two models side-by-side"""
        pass
    
    def generate_report(self, results: Dict) -> str:
        """Generate comprehensive test report"""
        pass
```

**Configuration File**: `testing/config/test_config.json`
```json
{
  "_metadata": {
    "file_version": "v5.0",
    "description": "Testing framework configuration"
  },
  "test_execution": {
    "device": "${TEST_DEVICE}",
    "batch_size": "${TEST_BATCH_SIZE}",
    "timeout_seconds": "${TEST_TIMEOUT}",
    "parallel_tests": "${TEST_PARALLEL}"
  },
  "metrics": {
    "accuracy_threshold": "${TEST_ACCURACY_THRESHOLD}",
    "latency_threshold_ms": "${TEST_LATENCY_THRESHOLD}",
    "vram_threshold_mb": "${TEST_VRAM_THRESHOLD}"
  },
  "defaults": {
    "device": "cuda",
    "batch_size": 8,
    "timeout_seconds": 30,
    "parallel_tests": false,
    "accuracy_threshold": 0.85,
    "latency_threshold_ms": 5000,
    "vram_threshold_mb": 2000
  }
}
```

**Tasks**:
- [ ] Implement ModelEvaluator class with factory function
- [ ] Create test_config.json with environment overrides
- [ ] Implement single test case execution
- [ ] Implement dataset testing
- [ ] Implement model comparison logic
- [ ] Add VRAM and latency tracking
- [ ] Create unit tests for ModelEvaluator
- [ ] Document usage examples

---

### **Step 1.8: Implement Metrics Calculators**

**Files**:
- `testing/metrics/accuracy_calculator.py`
- `testing/metrics/confusion_matrix.py`
- `testing/metrics/performance_tracker.py`
- `testing/metrics/ensemble_analyzer.py`

**AccuracyCalculator Requirements**:
```python
class AccuracyCalculator:
    """Calculate classification metrics"""
    
    def calculate_precision(self, predictions, ground_truth) -> float:
        """Calculate precision score"""
        pass
    
    def calculate_recall(self, predictions, ground_truth) -> float:
        """Calculate recall score"""
        pass
    
    def calculate_f1(self, precision, recall) -> float:
        """Calculate F1 score"""
        pass
    
    def calculate_accuracy(self, predictions, ground_truth) -> float:
        """Calculate overall accuracy"""
        pass
    
    def generate_classification_report(self, results) -> Dict:
        """Generate comprehensive classification metrics"""
        pass
```

**ConfusionMatrix Requirements**:
```python
class ConfusionMatrix:
    """Generate and visualize confusion matrices"""
    
    def generate_matrix(self, predictions, ground_truth) -> np.ndarray:
        """Generate confusion matrix"""
        pass
    
    def plot_matrix(self, matrix, labels) -> None:
        """Plot confusion matrix visualization"""
        pass
    
    def calculate_per_class_accuracy(self, matrix) -> Dict:
        """Calculate accuracy for each class"""
        pass
```

**PerformanceTracker Requirements**:
```python
class PerformanceTracker:
    """Track system performance metrics"""
    
    def measure_latency(self, func, *args) -> Tuple[Any, float]:
        """Measure function execution time"""
        pass
    
    def track_vram_usage(self) -> float:
        """Track GPU VRAM usage in MB"""
        pass
    
    def track_cpu_usage(self) -> float:
        """Track CPU usage percentage"""
        pass
    
    def generate_performance_report(self) -> Dict:
        """Generate system performance report"""
        pass
```

**EnsembleAnalyzer Requirements** (NEW):
```python
class EnsembleAnalyzer:
    """Analyze multi-model ensemble behavior"""
    
    def calculate_agreement_rate(self, model_results: List) -> float:
        """Calculate how often models agree"""
        pass
    
    def identify_disagreements(self, model_results: List) -> List[Dict]:
        """Find cases where models disagree"""
        pass
    
    def calculate_confidence_variance(self, model_results: List) -> float:
        """Calculate variance in model confidence scores"""
        pass
    
    def analyze_ensemble_correlation(self, results: List) -> Dict:
        """Analyze correlation between ensemble models"""
        pass
```

**Tasks**:
- [ ] Implement AccuracyCalculator with all metrics
- [ ] Implement ConfusionMatrix with visualization
- [ ] Implement PerformanceTracker for system metrics
- [ ] Implement EnsembleAnalyzer for multi-model analysis
- [ ] Create factory functions for all metrics classes
- [ ] Add unit tests for each calculator
- [ ] Document calculation methodologies

---

### **Step 1.9: Implement Report Generation**

**Files**:
- `testing/reports/model_comparison.py`
- `testing/reports/visualization.py`

**ModelComparison Requirements**:
```python
class ModelComparisonReport:
    """Generate model comparison reports"""
    
    def compare_accuracy(self, model_a_results, model_b_results) -> Dict:
        """Compare accuracy metrics between models"""
        pass
    
    def compare_performance(self, model_a_perf, model_b_perf) -> Dict:
        """Compare latency and VRAM usage"""
        pass
    
    def generate_html_report(self, comparison_data) -> str:
        """Generate HTML comparison report"""
        pass
    
    def generate_json_report(self, comparison_data) -> Dict:
        """Generate JSON comparison report"""
        pass
```

**Visualization Requirements**:
```python
class TestVisualization:
    """Generate charts and visualizations for test results"""
    
    def plot_accuracy_comparison(self, models_data) -> Figure:
        """Bar chart of accuracy across models"""
        pass
    
    def plot_confusion_matrix(self, matrix, labels) -> Figure:
        """Heatmap of confusion matrix"""
        pass
    
    def plot_latency_comparison(self, models_data) -> Figure:
        """Box plot of latency distribution"""
        pass
    
    def plot_ensemble_agreement(self, agreement_data) -> Figure:
        """Visualization of model agreement rates"""
        pass
```

**Report Templates**:
```html
<!-- testing/reports/report_templates/comparison_report.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Ash-NLP Model Comparison Report</title>
    <style>/* Styling */</style>
</head>
<body>
    <h1>Model Comparison: {{model_a}} vs {{model_b}}</h1>
    
    <section class="metrics">
        <h2>Accuracy Metrics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>{{model_a}}</th>
                <th>{{model_b}}</th>
                <th>Improvement</th>
            </tr>
            <!-- Data populated by template engine -->
        </table>
    </section>
    
    <section class="performance">
        <h2>Performance Metrics</h2>
        <!-- Performance charts -->
    </section>
    
    <section class="recommendations">
        <h2>Recommendations</h2>
        <!-- AI-generated recommendations -->
    </section>
</body>
</html>
```

**Tasks**:
- [ ] Implement ModelComparisonReport class
- [ ] Implement TestVisualization class
- [ ] Create HTML report templates
- [ ] Add chart generation with matplotlib/plotly
- [ ] Implement JSON report export
- [ ] Create example reports with sample data
- [ ] Document report interpretation

---

### **Step 1.10: Baseline Current Models**

**Objective**: Establish performance baseline with current v3.1 models

**Tasks**:
- [ ] Test MoritzLaurer/deberta-v3-base-zeroshot-v2.0
  - [ ] Run against crisis_examples.json
  - [ ] Run against safe_examples.json
  - [ ] Run against edge_cases.json
  - [ ] Record accuracy metrics
  - [ ] Record performance metrics (latency, VRAM)

- [ ] Test Lowerated/lm6-deberta-v3-topic-sentiment
  - [ ] Run against all test datasets
  - [ ] Record metrics

- [ ] Test MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
  - [ ] Run against all test datasets
  - [ ] Record metrics

- [ ] Generate baseline report
  - [ ] Accuracy: Precision, Recall, F1 for each model
  - [ ] Performance: Latency, VRAM usage
  - [ ] False Positive Rate
  - [ ] False Negative Rate
  - [ ] Per-category performance

**Baseline Report Structure**:
```json
{
  "baseline_version": "v3.1",
  "date_tested": "YYYY-MM-DD",
  "models": {
    "depression_model": {
      "name": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
      "accuracy_metrics": {
        "precision": 0.XX,
        "recall": 0.XX,
        "f1": 0.XX,
        "accuracy": 0.XX
      },
      "performance_metrics": {
        "avg_latency_ms": XX,
        "max_vram_mb": XX
      },
      "per_category_performance": {
        "critical": {"precision": 0.XX, "recall": 0.XX},
        "high": {"precision": 0.XX, "recall": 0.XX},
        "medium": {"precision": 0.XX, "recall": 0.XX}
      }
    }
  }
}
```

**Deliverables**:
- [ ] Baseline performance report (JSON + HTML)
- [ ] Identified weaknesses in current models
- [ ] Target improvement areas for v5.0 models
- [ ] Baseline report stored in `testing/reports/baselines/v3.1_baseline.json`

---

### **Step 1.11: Phase 1 Validation & Sign-Off**

**Phase 1 Complete Checklist**:

**Testing Framework**:
- [ ] All directory structure created
- [ ] All test dataset files created and validated
- [ ] ModelEvaluator class implemented and tested
- [ ] All metrics calculators implemented
- [ ] Report generation working
- [ ] Baseline testing completed

**Clean Architecture Compliance**:
- [ ] All files have version headers
- [ ] Factory functions used for all classes
- [ ] Configuration via JSON + environment variables
- [ ] Dependency injection implemented
- [ ] No mocks used (real model testing)

**Documentation**:
- [ ] Testing framework usage documented
- [ ] Test dataset creation methodology documented
- [ ] Baseline results documented
- [ ] Known issues/limitations documented

**Success Criteria**:
- ✅ Can test any model against standardized datasets
- ✅ Can compare models objectively with metrics
- ✅ Baseline v3.1 performance documented
- ✅ Testing infrastructure ready for Phase 2 model migration

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Testing framework validated
- [ ] Baseline metrics accepted
- [ ] Ready to proceed to Phase 2

---

## 📝 **PHASE 2: MODEL MIGRATION & INTEGRATION**

### **Status**: ⏳ **NOT STARTED** (Blocked by Phase 1)

### **Duration**: 2-3 weeks
### **Priority**: HIGH

### **Objectives**:
- Download and validate new model ensemble
- Create model loading and caching infrastructure
- Implement individual model wrappers
- Test each model independently against test datasets
- Validate VRAM and latency requirements met

---

### **Step 2.1: Create Model Management Infrastructure**

**New Files**:
- `managers/model_loader.py` - Model download and caching
- `managers/model_wrapper.py` - Unified model interface
- `config/model_config.json` - Model configuration

**ModelLoader Requirements**:
```python
class ModelLoader:
    """
    Download, cache, and load AI models for Ash-NLP
    
    Responsibilities:
    - Download models from HuggingFace
    - Cache models locally
    - Validate model integrity
    - Handle model versioning
    """
    
    def __init__(self, unified_config_manager):
        """Initialize with configuration"""
        pass
    
    def download_model(self, model_name: str) -> str:
        """Download model from HuggingFace"""
        pass
    
    def load_model(self, model_name: str) -> Pipeline:
        """Load model from cache"""
        pass
    
    def validate_model(self, model_path: str) -> bool:
        """Validate model integrity"""
        pass
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get model metadata"""
        pass
```

**Configuration**: `config/model_config.json`
```json
{
  "_metadata": {
    "file_version": "v5.0",
    "description": "AI model configuration for ensemble"
  },
  "models": {
    "crisis_classifier": {
      "name": "facebook/bart-large-mnli",
      "type": "zero-shot-classification",
      "cache_dir": "${MODEL_CACHE_DIR}/crisis_classifier",
      "device": "${MODEL_DEVICE}",
      "max_length": 1024,
      "batch_size": "${MODEL_BATCH_SIZE}"
    },
    "emotion_detector": {
      "name": "SamLowe/roberta-base-go_emotions",
      "type": "text-classification",
      "cache_dir": "${MODEL_CACHE_DIR}/emotion_detector",
      "device": "${MODEL_DEVICE}",
      "max_length": 512,
      "batch_size": "${MODEL_BATCH_SIZE}"
    },
    "sentiment_analyzer": {
      "name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
      "type": "text-classification",
      "cache_dir": "${MODEL_CACHE_DIR}/sentiment_analyzer",
      "device": "${MODEL_DEVICE}",
      "max_length": 512,
      "batch_size": "${MODEL_BATCH_SIZE}"
    },
    "irony_detector": {
      "name": "cardiffnlp/twitter-roberta-base-irony",
      "type": "text-classification",
      "cache_dir": "${MODEL_CACHE_DIR}/irony_detector",
      "device": "${MODEL_DEVICE}",
      "max_length": 512,
      "batch_size": "${MODEL_BATCH_SIZE}"
    }
  },
  "defaults": {
    "cache_dir": "./models",
    "device": "cuda",
    "batch_size": 8
  }
}
```

**Environment Variables**: `.env.template` additions
```bash
# Model Configuration
MODEL_CACHE_DIR=./models
MODEL_DEVICE=cuda  # or cpu
MODEL_BATCH_SIZE=8
MODEL_DOWNLOAD_TIMEOUT=600
```

**Tasks**:
- [ ] Implement ModelLoader class with factory function
- [ ] Create model_config.json
- [ ] Update .env.template with model variables
- [ ] Implement model caching logic
- [ ] Add model integrity validation
- [ ] Create unit tests for ModelLoader
- [ ] Document model download process

---

### **Step 2.2: Download and Validate Model 1 - Crisis Classifier**

**Model**: `facebook/bart-large-mnli`

**Tasks**:
- [ ] Download model to cache directory
  ```python
  from transformers import pipeline
  
  model = pipeline(
      "zero-shot-classification",
      model="facebook/bart-large-mnli",
      device=0  # GPU
  )
  ```

- [ ] Validate model loads successfully
- [ ] Test with sample crisis message
- [ ] Measure VRAM usage (expected: ~800MB)
- [ ] Measure latency (expected: 1-2 seconds)
- [ ] Test with custom crisis labels:
  ```python
  labels = [
      "suicide ideation",
      "self-harm thoughts",
      "severe depression",
      "panic attack",
      "abuse situation",
      "family rejection",
      "identity crisis",
      "mental health emergency"
  ]
  ```

- [ ] Run ModelEvaluator tests:
  - [ ] Test against crisis_examples.json
  - [ ] Test against safe_examples.json
  - [ ] Test against edge_cases.json
  - [ ] Calculate accuracy metrics
  - [ ] Compare against v3.1 baseline

**Validation Criteria**:
- ✅ Model downloads without errors
- ✅ VRAM usage < 1GB
- ✅ Latency < 3 seconds per message
- ✅ Accuracy improvement over baseline
- ✅ False positive rate acceptable (<10%)

**Deliverables**:
- [ ] Model cached locally
- [ ] Model validation report
- [ ] Performance comparison vs baseline
- [ ] Model integration documentation

---

### **Step 2.3: Download and Validate Model 2 - Emotion Detector**

**Model**: `SamLowe/roberta-base-go_emotions`

**Tasks**:
- [ ] Download model to cache directory
- [ ] Validate model loads successfully
- [ ] Test emotion detection on sample messages
- [ ] Measure VRAM usage (expected: ~250MB)
- [ ] Measure latency (expected: 0.5-1 second)
- [ ] Test all 28 emotion classes
- [ ] Focus on crisis-relevant emotions:
  - sadness, grief, disappointment
  - fear, nervousness, confusion
  - remorse, disgust

- [ ] Run ModelEvaluator tests against all datasets
- [ ] Calculate emotion detection accuracy
- [ ] Analyze multi-label performance

**Validation Criteria**:
- ✅ VRAM usage < 300MB
- ✅ Latency < 1.5 seconds
- ✅ Correctly identifies crisis-related emotions
- ✅ Low false positive on positive emotions

**Deliverables**:
- [ ] Model cached and validated
- [ ] Emotion detection report
- [ ] Crisis emotion identification accuracy
- [ ] Integration documentation

---

### **Step 2.4: Download and Validate Model 3 - Sentiment Analyzer**

**Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`

**Tasks**:
- [ ] Download model to cache directory
- [ ] Validate model loads successfully
- [ ] Test sentiment classification
- [ ] Measure VRAM usage (expected: ~250MB)
- [ ] Measure latency (expected: 0.3-0.5 seconds)
- [ ] Test 3-class sentiment (Negative, Neutral, Positive)
- [ ] Run ModelEvaluator tests
- [ ] Validate social media language understanding

**Validation Criteria**:
- ✅ VRAM usage < 300MB
- ✅ Latency < 1 second
- ✅ Correctly identifies negative sentiment in crisis messages
- ✅ Distinguishes neutral from negative

**Deliverables**:
- [ ] Model cached and validated
- [ ] Sentiment analysis report
- [ ] Comparison with v3.1 sentiment model
- [ ] Integration documentation

---

### **Step 2.5: Download and Validate Model 4 - Irony Detector**

**Model**: `cardiffnlp/twitter-roberta-base-irony`

**Tasks**:
- [ ] Download model to cache directory
- [ ] Validate model loads successfully
- [ ] Test irony detection on sarcastic messages
- [ ] Measure VRAM usage (expected: ~250MB)
- [ ] Measure latency (expected: 0.3-0.5 seconds)
- [ ] Test binary classification (Ironic / Not Ironic)
- [ ] Run ModelEvaluator tests, especially edge_cases.json
- [ ] Validate sarcasm detection on crisis messages

**Critical Test Cases**:
```python
test_cases = [
    "I'm just great",  # Should detect irony if contextually negative
    "Best day ever",   # Should detect irony
    "Love my life right now"  # Should detect irony
]
```

**Validation Criteria**:
- ✅ VRAM usage < 300MB
- ✅ Latency < 1 second
- ✅ Correctly identifies sarcastic crisis expressions
- ✅ Low false positive on genuine positive messages

**Deliverables**:
- [ ] Model cached and validated
- [ ] Irony detection report
- [ ] Sarcasm handling analysis
- [ ] Integration documentation

---

### **Step 2.6: Validate Total Ensemble Resources**

**Objective**: Confirm all 4 models can run simultaneously within constraints

**Tasks**:
- [ ] Load all 4 models simultaneously
- [ ] Measure total VRAM usage
  - Expected: ~1.55GB
  - Maximum acceptable: 2GB
  - Target: < 12.9% of 12GB available

- [ ] Test sequential execution on single message
  - Measure total latency
  - Expected: 3-7 seconds
  - Maximum acceptable: 10 seconds

- [ ] Test batch processing (if needed)
- [ ] Monitor GPU memory fragmentation
- [ ] Test model unloading/reloading
- [ ] Validate model caching effectiveness

**Load Test Scenarios**:
```python
# Scenario 1: Cold start (all models loading from disk)
# Scenario 2: Warm start (models cached in VRAM)
# Scenario 3: 10 messages in rapid succession
# Scenario 4: 100 messages in 1 minute
```

**Validation Criteria**:
- ✅ Total VRAM < 2GB
- ✅ Total latency < 10 seconds per message
- ✅ No memory leaks over 100 messages
- ✅ Models can reload after crash

**Deliverables**:
- [ ] Resource utilization report
- [ ] Load test results
- [ ] Optimization recommendations
- [ ] Resource monitoring dashboard

---

### **Step 2.7: Create Unified Model Wrapper Interface**

**File**: `managers/model_wrapper.py`

**Objective**: Create consistent interface for all 4 models

**ModelWrapper Requirements**:
```python
class ModelWrapper:
    """
    Unified interface for AI models in Ash-NLP ensemble
    
    Provides consistent API regardless of underlying model type
    """
    
    def __init__(
        self, 
        model_name: str,
        model_type: str,
        unified_config_manager
    ):
        """Initialize wrapper with model configuration"""
        pass
    
    def predict(self, text: str) -> Dict:
        """
        Make prediction on input text
        
        Returns standardized format:
        {
            "model": "model_name",
            "predictions": [...],
            "confidence": float,
            "latency_ms": float,
            "metadata": {...}
        }
        """
        pass
    
    def batch_predict(self, texts: List[str]) -> List[Dict]:
        """Batch prediction for efficiency"""
        pass
    
    def get_model_info(self) -> Dict:
        """Get model metadata"""
        pass
```

**Standardized Output Format**:
```python
# Crisis Classifier Output
{
    "model": "crisis_classifier",
    "type": "zero-shot-classification",
    "predictions": [
        {"label": "suicide ideation", "score": 0.87},
        {"label": "severe depression", "score": 0.65},
        {"label": "self-harm thoughts", "score": 0.42}
    ],
    "top_prediction": "suicide ideation",
    "confidence": 0.87,
    "latency_ms": 1247.5,
    "vram_mb": 823.2
}

# Emotion Detector Output
{
    "model": "emotion_detector",
    "type": "multi-label-classification",
    "predictions": [
        {"label": "sadness", "score": 0.92},
        {"label": "fear", "score": 0.78},
        {"label": "grief", "score": 0.61}
    ],
    "crisis_emotions": ["sadness", "fear", "grief"],
    "confidence": 0.92,
    "latency_ms": 567.3,
    "vram_mb": 267.1
}

# Sentiment Analyzer Output
{
    "model": "sentiment_analyzer",
    "type": "sentiment-classification",
    "predictions": [
        {"label": "negative", "score": 0.89},
        {"label": "neutral", "score": 0.08},
        {"label": "positive", "score": 0.03}
    ],
    "sentiment": "negative",
    "confidence": 0.89,
    "latency_ms": 342.8,
    "vram_mb": 245.6
}

# Irony Detector Output
{
    "model": "irony_detector",
    "type": "irony-classification",
    "predictions": [
        {"label": "ironic", "score": 0.76},
        {"label": "not_ironic", "score": 0.24}
    ],
    "is_ironic": true,
    "confidence": 0.76,
    "latency_ms": 298.4,
    "vram_mb": 241.3
}
```

**Tasks**:
- [ ] Implement ModelWrapper base class
- [ ] Create specific wrappers for each model type:
  - [ ] CrisisClassifierWrapper
  - [ ] EmotionDetectorWrapper
  - [ ] SentimentAnalyzerWrapper
  - [ ] IronyDetectorWrapper
- [ ] Implement output standardization
- [ ] Add error handling for model failures
- [ ] Implement caching for repeated queries
- [ ] Create factory function: `create_model_wrapper()`
- [ ] Add unit tests for each wrapper
- [ ] Document wrapper usage

---

### **Step 2.8: Phase 2 Validation & Sign-Off**

**Phase 2 Complete Checklist**:

**Model Infrastructure**:
- [ ] All 4 models downloaded and cached
- [ ] ModelLoader implemented and tested
- [ ] ModelWrapper interface implemented
- [ ] All models validated independently

**Performance Validation**:
- [ ] Total VRAM < 2GB ✓
- [ ] Total latency < 10 seconds ✓
- [ ] Each model tested against all test datasets
- [ ] Performance reports generated for each model

**Comparison vs Baseline**:
- [ ] Crisis classifier vs v3.1 depression model
- [ ] Emotion detector performance validated
- [ ] Sentiment analyzer vs v3.1 sentiment model
- [ ] Irony detector validated (new capability)

**Clean Architecture Compliance**:
- [ ] All files have version headers
- [ ] Factory functions used
- [ ] Configuration via JSON + environment
- [ ] Dependency injection implemented

**Documentation**:
- [ ] Model selection rationale documented
- [ ] Model integration guide completed
- [ ] Performance benchmarks documented
- [ ] Known limitations documented

**Success Criteria**:
- ✅ All 4 models operational independently
- ✅ VRAM and latency within acceptable ranges
- ✅ Accuracy improvements over v3.1 baseline
- ✅ Unified model interface working
- ✅ Ready for ensemble coordinator implementation

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Model performance validated
- [ ] Resource constraints met
- [ ] Ready to proceed to Phase 3

---

## 📝 **PHASE 3: ENSEMBLE COORDINATOR IMPLEMENTATION**

### **Status**: ⏳ **NOT STARTED** (Blocked by Phase 2)

### **Duration**: 2-3 weeks
### **Priority**: HIGH

### **Objectives**:
- Implement multi-model coordination logic
- Create consensus algorithms (Council-inspired)
- Implement confidence weighting and conflict resolution
- Create ensemble result aggregation
- Test ensemble behavior against test datasets

---

### **Step 3.1: Design Ensemble Coordinator Architecture**

**File**: `analysis/ensemble_coordinator.py`

**Core Responsibilities**:
```
Ensemble Coordinator
├── Parallel Model Execution
│   ├── Distribute message to all 4 models
│   ├── Collect results from each model
│   └── Handle model failures gracefully
├── Consensus Algorithm
│   ├── Weighted voting based on model confidence
│   ├── Detect model agreement/disagreement
│   └── Resolve conflicts between models
├── Result Aggregation
│   ├── Combine crisis scores from all models
│   ├── Identify primary crisis indicators
│   └── Calculate final crisis confidence
└── Explainability
    ├── Show which models contributed to decision
    ├── Highlight areas of disagreement
    └── Provide reasoning for final classification
```

**EnsembleCoordinator Class**:
```python
class EnsembleCoordinator:
    """
    Coordinate multiple AI models for crisis detection
    
    Council-inspired multi-model consensus with local models
    """
    
    def __init__(
        self,
        unified_config_manager,
        model_wrappers: Dict[str, ModelWrapper]
    ):
        """Initialize with model wrappers"""
        self.config = unified_config_manager
        self.models = model_wrappers
        self.consensus_algorithm = self._load_consensus_algorithm()
    
    def analyze_message(self, message: str) -> Dict:
        """
        Analyze message with all models
        
        Returns ensemble result with consensus
        """
        # Execute all models in parallel (or sequential)
        model_results = self._execute_models(message)
        
        # Apply consensus algorithm
        consensus = self._calculate_consensus(model_results)
        
        # Aggregate results
        ensemble_result = self._aggregate_results(
            model_results, 
            consensus
        )
        
        return ensemble_result
    
    def _execute_models(self, message: str) -> Dict:
        """Execute all models on message"""
        results = {}
        for model_name, wrapper in self.models.items():
            try:
                results[model_name] = wrapper.predict(message)
            except Exception as e:
                results[model_name] = self._handle_model_failure(
                    model_name, 
                    e
                )
        return results
    
    def _calculate_consensus(self, model_results: Dict) -> Dict:
        """
        Calculate consensus between models
        
        Inspired by LLM Council peer review stage
        """
        pass
    
    def _aggregate_results(
        self, 
        model_results: Dict, 
        consensus: Dict
    ) -> Dict:
        """Combine model results into final ensemble result"""
        pass
    
    def _detect_disagreement(self, model_results: Dict) -> bool:
        """Detect if models significantly disagree"""
        pass
```

**Configuration**: `config/ensemble_config.json`
```json
{
  "_metadata": {
    "file_version": "v5.0",
    "description": "Ensemble coordination configuration"
  },
  "consensus_algorithm": {
    "type": "${ENSEMBLE_CONSENSUS_TYPE}",
    "confidence_threshold": "${ENSEMBLE_CONFIDENCE_THRESHOLD}",
    "disagreement_threshold": "${ENSEMBLE_DISAGREEMENT_THRESHOLD}",
    "require_unanimous": "${ENSEMBLE_REQUIRE_UNANIMOUS}"
  },
  "model_weights": {
    "crisis_classifier": "${ENSEMBLE_WEIGHT_CRISIS}",
    "emotion_detector": "${ENSEMBLE_WEIGHT_EMOTION}",
    "sentiment_analyzer": "${ENSEMBLE_WEIGHT_SENTIMENT}",
    "irony_detector": "${ENSEMBLE_WEIGHT_IRONY}"
  },
  "aggregation": {
    "method": "${ENSEMBLE_AGGREGATION_METHOD}",
    "crisis_score_formula": "${ENSEMBLE_CRISIS_SCORE_FORMULA}"
  },
  "defaults": {
    "consensus_algorithm": {
      "type": "weighted_voting",
      "confidence_threshold": 0.6,
      "disagreement_threshold": 0.3,
      "require_unanimous": false
    },
    "model_weights": {
      "crisis_classifier": 0.4,
      "emotion_detector": 0.3,
      "sentiment_analyzer": 0.2,
      "irony_detector": 0.1
    },
    "aggregation": {
      "method": "weighted_average",
      "crisis_score_formula": "weighted"
    }
  }
}
```

**Tasks**:
- [ ] Design EnsembleCoordinator class structure
- [ ] Create ensemble_config.json
- [ ] Define consensus algorithm options
- [ ] Define model weighting strategy
- [ ] Create architecture documentation

---

### **Step 3.2: Implement Consensus Algorithms**

**File**: `analysis/consensus_algorithms.py`

**Algorithm Options**:

**1. Weighted Voting**:
```python
def weighted_voting_consensus(
    model_results: Dict,
    weights: Dict
) -> Dict:
    """
    Weight each model's prediction by confidence and weight
    
    Formula:
    crisis_score = Σ(model_score * model_weight * model_confidence)
    """
    total_weighted_score = 0
    total_weight = 0
    
    for model_name, result in model_results.items():
        model_weight = weights.get(model_name, 0.25)
        model_confidence = result['confidence']
        model_score = result['crisis_indicator_score']
        
        weighted_contribution = (
            model_score * model_weight * model_confidence
        )
        total_weighted_score += weighted_contribution
        total_weight += model_weight
    
    final_score = total_weighted_score / total_weight
    
    return {
        "consensus_type": "weighted_voting",
        "final_crisis_score": final_score,
        "individual_contributions": {...}
    }
```

**2. Majority Voting**:
```python
def majority_voting_consensus(model_results: Dict) -> Dict:
    """
    Majority vote: Most models agree = final decision
    
    Useful for binary crisis/no-crisis decisions
    """
    crisis_votes = 0
    total_votes = len(model_results)
    
    for result in model_results.values():
        if result['crisis_indicator_score'] > 0.5:
            crisis_votes += 1
    
    is_crisis = crisis_votes > (total_votes / 2)
    confidence = crisis_votes / total_votes
    
    return {
        "consensus_type": "majority_voting",
        "is_crisis": is_crisis,
        "confidence": confidence,
        "votes": {"crisis": crisis_votes, "safe": total_votes - crisis_votes}
    }
```

**3. Unanimous Consensus** (Conservative):
```python
def unanimous_consensus(model_results: Dict) -> Dict:
    """
    All models must agree for crisis classification
    
    Most conservative approach - low false positives
    """
    crisis_threshold = 0.6
    all_agree = all(
        result['crisis_indicator_score'] > crisis_threshold
        for result in model_results.values()
    )
    
    if all_agree:
        avg_score = sum(
            r['crisis_indicator_score'] 
            for r in model_results.values()
        ) / len(model_results)
        return {
            "consensus_type": "unanimous",
            "is_crisis": True,
            "crisis_score": avg_score,
            "agreement": "unanimous"
        }
    else:
        return {
            "consensus_type": "unanimous",
            "is_crisis": False,
            "crisis_score": 0.0,
            "agreement": "not_unanimous"
        }
```

**4. Conflict-Aware Consensus** (NEW - Council-inspired):
```python
def conflict_aware_consensus(model_results: Dict) -> Dict:
    """
    Detect disagreements and flag for review
    
    Inspired by LLM Council's peer review stage
    """
    scores = [r['crisis_indicator_score'] for r in model_results.values()]
    
    # Calculate variance in scores
    mean_score = sum(scores) / len(scores)
    variance = sum((s - mean_score)**2 for s in scores) / len(scores)
    
    # High variance = disagreement
    disagreement_threshold = 0.15
    has_disagreement = variance > disagreement_threshold
    
    if has_disagreement:
        return {
            "consensus_type": "conflict_aware",
            "has_conflict": True,
            "crisis_score": mean_score,
            "variance": variance,
            "requires_review": True,
            "conflicting_models": _identify_outliers(model_results)
        }
    else:
        return {
            "consensus_type": "conflict_aware",
            "has_conflict": False,
            "crisis_score": mean_score,
            "variance": variance,
            "requires_review": False
        }
```

**Tasks**:
- [ ] Implement weighted_voting_consensus
- [ ] Implement majority_voting_consensus
- [ ] Implement unanimous_consensus
- [ ] Implement conflict_aware_consensus
- [ ] Create consensus algorithm selector
- [ ] Add unit tests for each algorithm
- [ ] Document algorithm selection criteria

---

### **Step 3.3: Implement Result Aggregation**

**File**: `analysis/result_aggregator.py`

**ResultAggregator Class**:
```python
class ResultAggregator:
    """
    Aggregate multi-model results into final ensemble output
    """
    
    def aggregate(
        self, 
        model_results: Dict, 
        consensus: Dict
    ) -> Dict:
        """
        Combine model results with consensus
        
        Returns comprehensive ensemble result
        """
        return {
            "ensemble_version": "v5.0",
            "timestamp": datetime.utcnow().isoformat(),
            
            # Final Crisis Assessment
            "crisis_assessment": {
                "crisis_score": consensus['final_crisis_score'],
                "crisis_level": self._determine_crisis_level(
                    consensus['final_crisis_score']
                ),
                "confidence": consensus.get('confidence', 0.0),
                "requires_intervention": self._requires_intervention(
                    consensus['final_crisis_score']
                )
            },
            
            # Individual Model Results
            "model_results": {
                "crisis_classifier": {
                    "top_labels": [...],
                    "confidence": 0.XX,
                    "contribution_weight": 0.XX
                },
                "emotion_detector": {...},
                "sentiment_analyzer": {...},
                "irony_detector": {...}
            },
            
            # Consensus Analysis
            "consensus": {
                "algorithm": consensus['consensus_type'],
                "agreement_level": self._calculate_agreement_level(
                    model_results
                ),
                "has_conflict": consensus.get('has_conflict', False),
                "requires_review": consensus.get('requires_review', False)
            },
            
            # Explainability
            "explanation": {
                "primary_indicators": self._identify_primary_indicators(
                    model_results
                ),
                "contributing_factors": [...],
                "model_agreement": {...},
                "confidence_breakdown": {...}
            },
            
            # Performance Metrics
            "performance": {
                "total_latency_ms": sum(
                    r['latency_ms'] for r in model_results.values()
                ),
                "total_vram_mb": sum(
                    r['vram_mb'] for r in model_results.values()
                )
            }
        }
    
    def _determine_crisis_level(self, score: float) -> str:
        """Map crisis score to severity level"""
        if score >= 0.85:
            return "critical"
        elif score >= 0.65:
            return "high"
        elif score >= 0.40:
            return "medium"
        elif score >= 0.20:
            return "low"
        else:
            return "none"
    
    def _requires_intervention(self, score: float) -> bool:
        """Determine if immediate intervention needed"""
        return score >= 0.70
    
    def _calculate_agreement_level(
        self, 
        model_results: Dict
    ) -> str:
        """Calculate how much models agree"""
        scores = [r['crisis_indicator_score'] for r in model_results.values()]
        variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
        
        if variance < 0.05:
            return "strong_agreement"
        elif variance < 0.15:
            return "moderate_agreement"
        else:
            return "significant_disagreement"
    
    def _identify_primary_indicators(
        self, 
        model_results: Dict
    ) -> List[str]:
        """Identify main crisis indicators from all models"""
        indicators = []
        
        # From crisis classifier
        crisis_labels = model_results['crisis_classifier']['top_predictions']
        indicators.extend([l['label'] for l in crisis_labels if l['score'] > 0.5])
        
        # From emotion detector
        crisis_emotions = ['sadness', 'fear', 'grief', 'despair']
        detected_emotions = model_results['emotion_detector']['predictions']
        indicators.extend([
            e['label'] for e in detected_emotions 
            if e['label'] in crisis_emotions and e['score'] > 0.6
        ])
        
        # From sentiment analyzer
        if model_results['sentiment_analyzer']['sentiment'] == 'negative':
            indicators.append('negative_sentiment')
        
        # From irony detector
        if model_results['irony_detector']['is_ironic']:
            indicators.append('sarcastic_expression')
        
        return list(set(indicators))  # Remove duplicates
```

**Tasks**:
- [ ] Implement ResultAggregator class
- [ ] Create comprehensive output structure
- [ ] Implement crisis level determination
- [ ] Implement agreement level calculation
- [ ] Add primary indicator identification
- [ ] Create explainability report
- [ ] Add unit tests for aggregator
- [ ] Document output format

---

### **Step 3.4: Implement Conflict Detection & Resolution**

**Objective**: Handle cases where models disagree significantly

**ConflictDetector Class**:
```python
class ConflictDetector:
    """
    Detect and handle conflicts between ensemble models
    """
    
    def detect_conflicts(self, model_results: Dict) -> Dict:
        """
        Identify conflicts in model predictions
        
        Returns conflict analysis
        """
        conflicts = []
        
        # Type 1: Score Disagreement
        scores = [r['crisis_indicator_score'] for r in model_results.values()]
        if max(scores) - min(scores) > 0.4:
            conflicts.append({
                "type": "score_disagreement",
                "severity": "high",
                "details": {
                    "max_score": max(scores),
                    "min_score": min(scores),
                    "range": max(scores) - min(scores)
                }
            })
        
        # Type 2: Irony Conflict
        # Sentiment positive but irony detected
        sentiment = model_results['sentiment_analyzer']['sentiment']
        is_ironic = model_results['irony_detector']['is_ironic']
        
        if sentiment == 'positive' and is_ironic:
            conflicts.append({
                "type": "irony_sentiment_conflict",
                "severity": "medium",
                "details": {
                    "surface_sentiment": "positive",
                    "actual_sentiment": "likely_negative",
                    "confidence": model_results['irony_detector']['confidence']
                }
            })
        
        # Type 3: Emotion-Crisis Mismatch
        crisis_score = model_results['crisis_classifier']['confidence']
        crisis_emotions = self._get_crisis_emotions(
            model_results['emotion_detector']
        )
        
        if crisis_score > 0.7 and len(crisis_emotions) == 0:
            conflicts.append({
                "type": "emotion_crisis_mismatch",
                "severity": "medium",
                "details": {
                    "crisis_score": crisis_score,
                    "detected_emotions": crisis_emotions,
                    "expected": "high crisis emotions"
                }
            })
        
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflict_count": len(conflicts),
            "conflicts": conflicts,
            "requires_human_review": self._requires_review(conflicts)
        }
    
    def resolve_conflicts(
        self, 
        model_results: Dict, 
        conflicts: Dict
    ) -> Dict:
        """
        Apply conflict resolution strategies
        """
        resolution_strategy = "conservative"  # Default to safer choice
        
        if conflicts['has_conflicts']:
            # Conservative: Prioritize crisis detection over false negatives
            # Better to over-alert than under-alert for safety
            
            max_crisis_score = max(
                r['crisis_indicator_score'] 
                for r in model_results.values()
            )
            
            return {
                "resolution_method": resolution_strategy,
                "final_score": max_crisis_score,
                "rationale": "Prioritized safety over precision due to conflict",
                "flagged_for_review": True
            }
        else:
            return {
                "resolution_method": "standard_consensus",
                "no_conflicts": True
            }
```

**Tasks**:
- [ ] Implement ConflictDetector class
- [ ] Define conflict types and severity levels
- [ ] Implement conflict detection algorithms
- [ ] Implement conflict resolution strategies
- [ ] Create conflict reporting
- [ ] Add unit tests for conflict detection
- [ ] Document conflict handling procedures

---

### **Step 3.5: Implement Explainability Layer**

**Objective**: Make ensemble decisions transparent and auditable

**ExplainabilityGenerator Class**:
```python
class ExplainabilityGenerator:
    """
    Generate human-readable explanations for ensemble decisions
    """
    
    def generate_explanation(
        self, 
        message: str,
        ensemble_result: Dict
    ) -> Dict:
        """
        Create explanation for ensemble decision
        
        Returns structured explanation
        """
        return {
            "decision_summary": self._create_summary(ensemble_result),
            "model_contributions": self._explain_contributions(
                ensemble_result
            ),
            "key_factors": self._identify_key_factors(ensemble_result),
            "confidence_breakdown": self._explain_confidence(
                ensemble_result
            ),
            "alternative_interpretations": self._provide_alternatives(
                ensemble_result
            ),
            "recommended_action": self._recommend_action(
                ensemble_result
            )
        }
    
    def _create_summary(self, result: Dict) -> str:
        """Generate plain-English summary"""
        crisis_level = result['crisis_assessment']['crisis_level']
        confidence = result['crisis_assessment']['confidence']
        
        if crisis_level == "critical":
            return (
                f"CRITICAL: High-confidence ({confidence:.0%}) crisis "
                f"detected. Immediate intervention recommended."
            )
        elif crisis_level == "high":
            return (
                f"HIGH CONCERN: Models detected significant crisis "
                f"indicators with {confidence:.0%} confidence."
            )
        elif crisis_level == "medium":
            return (
                f"MODERATE CONCERN: Some crisis indicators present. "
                f"Monitoring recommended."
            )
        elif crisis_level == "low":
            return (
                f"LOW CONCERN: Minor negative indicators detected."
            )
        else:
            return "No significant crisis indicators detected."
    
    def _explain_contributions(self, result: Dict) -> List[Dict]:
        """Explain what each model contributed"""
        contributions = []
        
        for model_name, model_result in result['model_results'].items():
            contribution = {
                "model": model_name,
                "finding": self._summarize_model_finding(
                    model_name, 
                    model_result
                ),
                "confidence": model_result['confidence'],
                "weight": model_result['contribution_weight']
            }
            contributions.append(contribution)
        
        return contributions
    
    def _identify_key_factors(self, result: Dict) -> List[str]:
        """List the most important factors in the decision"""
        return result['explanation']['primary_indicators']
    
    def _recommend_action(self, result: Dict) -> Dict:
        """Recommend appropriate response"""
        crisis_score = result['crisis_assessment']['crisis_score']
        
        if crisis_score >= 0.85:
            return {
                "priority": "immediate",
                "action": "alert_staff",
                "message": "Contact user immediately, notify moderators",
                "escalation": "crisis_team"
            }
        elif crisis_score >= 0.65:
            return {
                "priority": "high",
                "action": "monitor_closely",
                "message": "Check user history, consider outreach",
                "escalation": "moderator_review"
            }
        elif crisis_score >= 0.40:
            return {
                "priority": "medium",
                "action": "passive_monitoring",
                "message": "Watch for escalation patterns",
                "escalation": "automated_tracking"
            }
        else:
            return {
                "priority": "low",
                "action": "normal_monitoring",
                "message": "Continue standard monitoring",
                "escalation": "none"
            }
```

**Explanation Output Example**:
```json
{
  "decision_summary": "HIGH CONCERN: Models detected significant crisis indicators with 78% confidence.",
  
  "model_contributions": [
    {
      "model": "crisis_classifier",
      "finding": "Detected 'self-harm thoughts' (0.82) and 'severe depression' (0.67)",
      "confidence": 0.82,
      "weight": 0.4
    },
    {
      "model": "emotion_detector",
      "finding": "Strong sadness (0.91), fear (0.73), and grief (0.58) detected",
      "confidence": 0.91,
      "weight": 0.3
    },
    {
      "model": "sentiment_analyzer",
      "finding": "Highly negative sentiment (0.87)",
      "confidence": 0.87,
      "weight": 0.2
    },
    {
      "model": "irony_detector",
      "finding": "No sarcasm detected - message appears sincere",
      "confidence": 0.89,
      "weight": 0.1
    }
  ],
  
  "key_factors": [
    "self-harm thoughts",
    "severe depression",
    "sadness",
    "fear",
    "negative_sentiment"
  ],
  
  "confidence_breakdown": {
    "model_agreement": "strong_agreement",
    "variance": 0.04,
    "unanimous_concern": true
  },
  
  "recommended_action": {
    "priority": "high",
    "action": "monitor_closely",
    "message": "Check user history, consider outreach",
    "escalation": "moderator_review"
  }
}
```

**Tasks**:
- [ ] Implement ExplainabilityGenerator class
- [ ] Create human-readable summaries
- [ ] Implement contribution explanations
- [ ] Add action recommendations
- [ ] Create explanation templates
- [ ] Add unit tests for explanations
- [ ] Document explanation format

---

### **Step 3.6: Integrate Ensemble with CrisisAnalyzer**

**File**: `analysis/crisis_analyzer.py` (Update existing)

**Integration Requirements**:
```python
class CrisisAnalyzer:
    """
    Updated for v5.0 with ensemble coordination
    """
    
    def __init__(
        self,
        unified_config_manager,
        ensemble_coordinator,  # NEW
        pattern_detection_manager,
        context_analysis_manager  # Will add in Phase 4
    ):
        """Initialize with ensemble coordinator"""
        self.config = unified_config_manager
        self.ensemble = ensemble_coordinator
        self.patterns = pattern_detection_manager
        self.context = context_analysis_manager
    
    def analyze_message(
        self, 
        user_id: str, 
        message: str
    ) -> Dict:
        """
        Analyze message with ensemble + patterns + context
        
        Phase 3: Ensemble only
        Phase 4: Add context analysis
        Phase 5: Add pattern enhancement
        """
        # Step 1: Ensemble Analysis (NEW)
        ensemble_result = self.ensemble.analyze_message(message)
        
        # Step 2: Pattern Detection (existing, will enhance)
        pattern_result = self.patterns.detect_patterns(message)
        
        # Step 3: Context Analysis (Phase 4)
        # context_result = self.context.analyze_with_history(
        #     user_id, message
        # )
        
        # Step 4: Combine all analyses
        final_result = self._combine_analyses(
            ensemble_result,
            pattern_result
            # context_result  # Phase 4
        )
        
        return final_result
    
    def _combine_analyses(
        self,
        ensemble_result: Dict,
        pattern_result: Dict
    ) -> Dict:
        """
        Combine ensemble and pattern results
        
        Pattern detection can boost/reduce ensemble score
        """
        # Start with ensemble score
        base_score = ensemble_result['crisis_assessment']['crisis_score']
        
        # Apply pattern modifiers
        pattern_boost = self._calculate_pattern_boost(pattern_result)
        
        # Calculate final score
        final_score = min(1.0, base_score + pattern_boost)
        
        return {
            "analysis_version": "v5.0",
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            
            # Final Assessment
            "final_assessment": {
                "crisis_score": final_score,
                "crisis_level": self._determine_level(final_score),
                "requires_intervention": final_score >= 0.70
            },
            
            # Component Results
            "ensemble_result": ensemble_result,
            "pattern_result": pattern_result,
            
            # Explanation
            "explanation": ensemble_result['explanation']
        }
```

**Tasks**:
- [ ] Update CrisisAnalyzer to use EnsembleCoordinator
- [ ] Implement analysis combination logic
- [ ] Update factory function
- [ ] Maintain backward compatibility where possible
- [ ] Add integration tests
- [ ] Update API endpoints to use new analyzer
- [ ] Document integration changes

---

### **Step 3.7: Test Ensemble Against All Test Datasets**

**Testing Requirements**:

**Test Suite Execution**:
- [ ] Run ensemble against crisis_examples.json
  - [ ] Calculate accuracy metrics
  - [ ] Compare to individual model performance
  - [ ] Compare to v3.1 baseline
  - [ ] Identify improvement areas

- [ ] Run ensemble against safe_examples.json
  - [ ] Calculate false positive rate
  - [ ] Compare to baseline false positive rate
  - [ ] Validate safe message handling

- [ ] Run ensemble against edge_cases.json
  - [ ] Test sarcasm detection improvement
  - [ ] Test ambiguous case handling
  - [ ] Validate conflict detection

- [ ] Run ensemble against lgbtqia_specific.json
  - [ ] Test community-specific language
  - [ ] Validate cultural sensitivity
  - [ ] Test identity crisis detection

**Performance Testing**:
- [ ] Measure ensemble latency (target: < 10s)
- [ ] Measure ensemble VRAM usage (target: < 2GB)
- [ ] Test load handling (100 messages)
- [ ] Test error recovery

**Consensus Algorithm Testing**:
- [ ] Test weighted voting
- [ ] Test majority voting
- [ ] Test unanimous consensus
- [ ] Test conflict-aware consensus
- [ ] Compare algorithm performance

**Tasks**:
- [ ] Execute all test suites
- [ ] Generate performance reports
- [ ] Create comparison visualizations
- [ ] Document test results
- [ ] Identify optimization opportunities

---

### **Step 3.8: Optimize Ensemble Performance**

**Optimization Targets**:

**Latency Optimization**:
- [ ] Implement parallel model execution
  ```python
  import asyncio
  
  async def execute_models_parallel(message: str):
      tasks = [
          model.predict_async(message) 
          for model in self.models.values()
      ]
      results = await asyncio.gather(*tasks)
      return results
  ```
- [ ] Add result caching for repeated queries
- [ ] Implement early stopping for clear cases
- [ ] Optimize model loading

**VRAM Optimization**:
- [ ] Implement model unloading for unused models
- [ ] Add dynamic batching
- [ ] Optimize model quantization if needed
- [ ] Implement gradient checkpointing

**Accuracy Optimization**:
- [ ] Tune model weights based on test results
- [ ] Tune consensus thresholds
- [ ] Optimize conflict resolution strategies
- [ ] Fine-tune crisis level boundaries

**Tasks**:
- [ ] Implement parallel execution
- [ ] Add caching layer
- [ ] Tune hyperparameters
- [ ] Run optimization tests
- [ ] Document optimization results
- [ ] Validate no accuracy regression

---

### **Step 3.9: Phase 3 Validation & Sign-Off**

**Phase 3 Complete Checklist**:

**Ensemble Implementation**:
- [ ] EnsembleCoordinator implemented and tested
- [ ] All consensus algorithms working
- [ ] Result aggregation functional
- [ ] Conflict detection operational
- [ ] Explainability layer complete

**Integration**:
- [ ] Integrated with CrisisAnalyzer
- [ ] API endpoints updated
- [ ] Factory functions working
- [ ] Dependency injection maintained

**Testing**:
- [ ] All test datasets passed
- [ ] Performance metrics within targets
- [ ] Accuracy improved over baseline
- [ ] False positive rate acceptable
- [ ] Edge cases handled properly

**Performance Validation**:
- [ ] Latency < 10 seconds ✓
- [ ] VRAM < 2GB ✓
- [ ] Can handle 100 messages/minute
- [ ] No memory leaks detected

**Clean Architecture Compliance**:
- [ ] All files have version headers
- [ ] Factory functions used
- [ ] Configuration via JSON + environment
- [ ] Dependency injection maintained

**Documentation**:
- [ ] Ensemble architecture documented
- [ ] Consensus algorithms explained
- [ ] Configuration guide complete
- [ ] Troubleshooting guide created

**Success Criteria**:
- ✅ Ensemble operational with all 4 models
- ✅ Consensus working across algorithms
- ✅ Performance within acceptable ranges
- ✅ Accuracy improved over v3.1 baseline
- ✅ Ready for context analysis integration

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Ensemble performance validated
- [ ] Test coverage sufficient
- [ ] Ready to proceed to Phase 4

---

## 📝 **PHASE 4: CONTEXT ANALYSIS INTEGRATION**

### **Status**: ⏳ **NOT STARTED** (Blocked by Phase 3)

### **Duration**: 1-2 weeks
### **Priority**: MEDIUM

### **Objectives**:
- Implement rolling window message history
- Add temporal pattern detection
- Create escalation detection
- Integrate context with ensemble results
- Test context-aware crisis detection

---

### **Step 4.1: Design Context Analyzer Architecture**

**File**: `analysis/context_analyzer.py`

**Core Concept**: Track user message history to detect:
- **Escalating crisis** (getting worse over time)
- **Chronic distress** (persistent low-level crisis)
- **Sudden onset** (rapid mood change)
- **Communication patterns** (frequency, isolation)

**ContextAnalyzer Class**:
```python
class ContextAnalyzer:
    """
    Analyze message in context of user's message history
    
    Implements rolling window analysis for temporal patterns
    """
    
    def __init__(
        self,
        unified_config_manager,
        window_size: int = 10
    ):
        """
        Initialize context analyzer
        
        Args:
            window_size: Number of previous messages to analyze
        """
        self.config = unified_config_manager
        self.window_size = window_size
        self.user_histories = {}  # user_id -> deque of messages
    
    def analyze_with_context(
        self,
        user_id: str,
        message: str,
        ensemble_result: Dict
    ) -> Dict:
        """
        Analyze message considering user's history
        
        Returns context-enhanced result
        """
        # Get user history
        history = self._get_user_history(user_id)
        
        # Add current message
        message_record = {
            "timestamp": datetime.utcnow(),
            "message": message,
            "crisis_score": ensemble_result['crisis_assessment']['crisis_score'],
            "crisis_level": ensemble_result['crisis_assessment']['crisis_level']
        }
        history.append(message_record)
        
        # Analyze temporal patterns
        temporal_analysis = self._analyze_temporal_patterns(history)
        
        # Detect escalation
        escalation = self._detect_escalation(history)
        
        # Calculate context-adjusted score
        adjusted_score = self._adjust_score_for_context(
            ensemble_result['crisis_assessment']['crisis_score'],
            temporal_analysis,
            escalation
        )
        
        return {
            "base_score": ensemble_result['crisis_assessment']['crisis_score'],
            "context_adjusted_score": adjusted_score,
            "temporal_analysis": temporal_analysis,
            "escalation": escalation,
            "history_summary": self._summarize_history(history)
        }
    
    def _get_user_history(self, user_id: str) -> deque:
        """Get or create user message history"""
        if user_id not in self.user_histories:
            self.user_histories[user_id] = deque(
                maxlen=self.window_size
            )
        return self.user_histories[user_id]
    
    def _analyze_temporal_patterns(self, history: deque) -> Dict:
        """Analyze patterns over time"""
        if len(history) < 3:
            return {"pattern": "insufficient_data"}
        
        # Calculate trend
        scores = [h['crisis_score'] for h in history]
        trend = self._calculate_trend(scores)
        
        # Calculate frequency
        timestamps = [h['timestamp'] for h in history]
        frequency = self._calculate_message_frequency(timestamps)
        
        return {
            "trend": trend,  # "increasing", "stable", "decreasing"
            "frequency": frequency,  # messages per hour
            "avg_score": sum(scores) / len(scores),
            "score_variance": self._calculate_variance(scores)
        }
    
    def _detect_escalation(self, history: deque) -> Dict:
        """Detect if crisis is escalating"""
        if len(history) < 3:
            return {"is_escalating": False}
        
        recent_scores = [h['crisis_score'] for h in list(history)[-3:]]
        
        # Check if each message is worse than the last
        is_escalating = all(
            recent_scores[i] < recent_scores[i+1]
            for i in range(len(recent_scores)-1)
        )
        
        if is_escalating:
            escalation_rate = recent_scores[-1] - recent_scores[0]
            return {
                "is_escalating": True,
                "escalation_rate": escalation_rate,
                "time_window": "last_3_messages",
                "severity": "high" if escalation_rate > 0.3 else "moderate"
            }
        
        return {"is_escalating": False}
    
    def _adjust_score_for_context(
        self,
        base_score: float,
        temporal_analysis: Dict,
        escalation: Dict
    ) -> float:
        """Adjust crisis score based on context"""
        adjusted_score = base_score
        
        # Boost for escalation
        if escalation.get('is_escalating'):
            boost = 0.15 if escalation['severity'] == 'high' else 0.10
            adjusted_score += boost
        
        # Boost for chronic high scores
        if temporal_analysis.get('avg_score', 0) > 0.6:
            adjusted_score += 0.10
        
        # Boost for high frequency (isolation indicator)
        if temporal_analysis.get('frequency', 0) > 5:  # >5 messages/hour
            adjusted_score += 0.05
        
        return min(1.0, adjusted_score)  # Cap at 1.0
```

**Configuration**: `config/context_config.json`
```json
{
  "_metadata": {
    "file_version": "v5.0",
    "description": "Context analysis configuration"
  },
  "history": {
    "window_size": "${CONTEXT_WINDOW_SIZE}",
    "min_messages_for_analysis": "${CONTEXT_MIN_MESSAGES}",
    "max_storage_per_user": "${CONTEXT_MAX_STORAGE}"
  },
  "escalation": {
    "detection_threshold": "${CONTEXT_ESCALATION_THRESHOLD}",
    "time_window": "${CONTEXT_ESCALATION_WINDOW}",
    "boost_amount": "${CONTEXT_ESCALATION_BOOST}"
  },
  "temporal": {
    "high_frequency_threshold": "${CONTEXT_HIGH_FREQ_THRESHOLD}",
    "chronic_score_threshold": "${CONTEXT_CHRONIC_THRESHOLD}",
    "trend_sensitivity": "${CONTEXT_TREND_SENSITIVITY}"
  },
  "defaults": {
    "history": {
      "window_size": 10,
      "min_messages_for_analysis": 3,
      "max_storage_per_user": 100
    },
    "escalation": {
      "detection_threshold": 0.2,
      "time_window": 3,
      "boost_amount": 0.15
    },
    "temporal": {
      "high_frequency_threshold": 5,
      "chronic_score_threshold": 0.6,
      "trend_sensitivity": 0.1
    }
  }
}
```

**Tasks**:
- [ ] Design ContextAnalyzer class structure
- [ ] Create context_config.json
- [ ] Define history storage strategy
- [ ] Define escalation detection algorithm
- [ ] Create architecture documentation

---

### **Step 4.2: Implement Message History Storage**

**Requirements**:
- Store last N messages per user
- Include timestamp, message, scores
- Efficient memory usage
- Thread-safe access
- Persistence optional (Phase 6)

**Implementation Options**:

**Option A: In-Memory (Simple)**:
```python
class InMemoryHistoryStore:
    """Simple in-memory message history"""
    
    def __init__(self, max_window_size: int = 10):
        self.histories = {}  # user_id -> deque
        self.max_window_size = max_window_size
    
    def add_message(
        self, 
        user_id: str, 
        message_record: Dict
    ) -> None:
        """Add message to user history"""
        if user_id not in self.histories:
            self.histories[user_id] = deque(
                maxlen=self.max_window_size
            )
        self.histories[user_id].append(message_record)
    
    def get_history(self, user_id: str) -> List[Dict]:
        """Get user message history"""
        return list(self.histories.get(user_id, []))
    
    def clear_history(self, user_id: str) -> None:
        """Clear user history"""
        if user_id in self.histories:
            del self.histories[user_id]
```

**Option B: Redis Cache (Scalable - Phase 6)**:
```python
class RedisHistoryStore:
    """Redis-backed message history for scalability"""
    
    def __init__(self, redis_client, max_window_size: int = 10):
        self.redis = redis_client
        self.max_window_size = max_window_size
    
    def add_message(
        self, 
        user_id: str, 
        message_record: Dict
    ) -> None:
        """Add message to Redis list"""
        key = f"history:{user_id}"
        self.redis.lpush(key, json.dumps(message_record))
        self.redis.ltrim(key, 0, self.max_window_size - 1)
        self.redis.expire(key, 86400 * 7)  # 7 day TTL
    
    def get_history(self, user_id: str) -> List[Dict]:
        """Get user history from Redis"""
        key = f"history:{user_id}"
        records = self.redis.lrange(key, 0, -1)
        return [json.loads(r) for r in records]
```

**For Phase 4**: Use InMemoryHistoryStore (simpler, faster)
**For Phase 6**: Migrate to RedisHistoryStore (scalable, persistent)

**Tasks**:
- [ ] Implement InMemoryHistoryStore
- [ ] Add thread safety (locks if needed)
- [ ] Implement history cleanup
- [ ] Add unit tests
- [ ] Document storage strategy
- [ ] Plan Redis migration for Phase 6

---

### **Step 4.3: Implement Temporal Pattern Detection**

**File**: `analysis/temporal_patterns.py`

**TemporalPatternDetector Class**:
```python
class TemporalPatternDetector:
    """
    Detect patterns in message history over time
    """
    
    def detect_patterns(self, history: List[Dict]) -> Dict:
        """
        Analyze temporal patterns in message history
        
        Returns pattern analysis
        """
        if len(history) < 3:
            return {"status": "insufficient_data"}
        
        patterns = []
        
        # Pattern 1: Trend Analysis
        trend = self._analyze_trend(history)
        patterns.append(trend)
        
        # Pattern 2: Frequency Analysis
        frequency = self._analyze_frequency(history)
        patterns.append(frequency)
        
        # Pattern 3: Volatility Analysis
        volatility = self._analyze_volatility(history)
        patterns.append(volatility)
        
        # Pattern 4: Time-of-Day Patterns
        time_pattern = self._analyze_time_patterns(history)
        patterns.append(time_pattern)
        
        return {
            "status": "analyzed",
            "patterns": patterns,
            "summary": self._summarize_patterns(patterns)
        }
    
    def _analyze_trend(self, history: List[Dict]) -> Dict:
        """Detect if crisis is getting better/worse"""
        scores = [h['crisis_score'] for h in history]
        
        # Simple linear regression
        n = len(scores)
        x = list(range(n))
        
        # Calculate slope
        x_mean = sum(x) / n
        y_mean = sum(scores) / n
        
        numerator = sum((x[i] - x_mean) * (scores[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        if slope > 0.05:
            trend = "increasing"
        elif slope < -0.05:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "type": "trend",
            "direction": trend,
            "slope": slope,
            "confidence": abs(slope)
        }
    
    def _analyze_frequency(self, history: List[Dict]) -> Dict:
        """Analyze message frequency"""
        if len(history) < 2:
            return {"type": "frequency", "status": "insufficient_data"}
        
        timestamps = [h['timestamp'] for h in history]
        
        # Calculate time differences
        time_diffs = [
            (timestamps[i+1] - timestamps[i]).total_seconds() / 3600
            for i in range(len(timestamps) - 1)
        ]
        
        avg_interval_hours = sum(time_diffs) / len(time_diffs)
        messages_per_hour = 1 / avg_interval_hours if avg_interval_hours > 0 else 0
        
        if messages_per_hour > 5:
            frequency_level = "very_high"
        elif messages_per_hour > 2:
            frequency_level = "high"
        elif messages_per_hour > 0.5:
            frequency_level = "normal"
        else:
            frequency_level = "low"
        
        return {
            "type": "frequency",
            "messages_per_hour": messages_per_hour,
            "level": frequency_level,
            "avg_interval_hours": avg_interval_hours
        }
    
    def _analyze_volatility(self, history: List[Dict]) -> Dict:
        """Analyze score volatility"""
        scores = [h['crisis_score'] for h in history]
        
        # Calculate variance
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        
        if std_dev > 0.3:
            volatility_level = "high"
        elif std_dev > 0.15:
            volatility_level = "moderate"
        else:
            volatility_level = "low"
        
        return {
            "type": "volatility",
            "level": volatility_level,
            "standard_deviation": std_dev,
            "variance": variance
        }
    
    def _analyze_time_patterns(self, history: List[Dict]) -> Dict:
        """Detect time-of-day patterns"""
        timestamps = [h['timestamp'] for h in history]
        hours = [t.hour for t in timestamps]
        
        # Count messages by time period
        night_messages = sum(1 for h in hours if 22 <= h or h < 6)
        
        if night_messages / len(hours) > 0.6:
            pattern = "primarily_night"  # Potential isolation indicator
        else:
            pattern = "normal_distribution"
        
        return {
            "type": "time_pattern",
            "pattern": pattern,
            "night_message_ratio": night_messages / len(hours)
        }
```

**Tasks**:
- [ ] Implement TemporalPatternDetector class
- [ ] Implement trend analysis
- [ ] Implement frequency analysis
- [ ] Implement volatility analysis
- [ ] Implement time-of-day analysis
- [ ] Add unit tests
- [ ] Document pattern detection

---

### **Step 4.4: Implement Escalation Detection**

**File**: `analysis/escalation_detector.py`

**EscalationDetector Class**:
```python
class EscalationDetector:
    """
    Detect escalating crisis situations
    """
    
    def detect_escalation(
        self, 
        history: List[Dict],
        config: Dict
    ) -> Dict:
        """
        Detect if crisis is escalating
        
        Returns escalation analysis
        """
        if len(history) < 3:
            return {
                "is_escalating": False,
                "reason": "insufficient_history"
            }
        
        # Get recent messages
        window_size = config.get('time_window', 3)
        recent_history = history[-window_size:]
        
        # Analyze escalation types
        escalation_analysis = {
            "score_escalation": self._detect_score_escalation(
                recent_history
            ),
            "severity_escalation": self._detect_severity_escalation(
                recent_history
            ),
            "temporal_urgency": self._detect_temporal_urgency(
                recent_history
            ),
            "communication_change": self._detect_communication_change(
                recent_history,
                history
            )
        }
        
        # Determine overall escalation
        is_escalating = any(
            analysis.get('is_escalating', False)
            for analysis in escalation_analysis.values()
        )
        
        if is_escalating:
            severity = self._determine_escalation_severity(
                escalation_analysis
            )
            return {
                "is_escalating": True,
                "severity": severity,
                "escalation_types": escalation_analysis,
                "recommendation": self._get_escalation_recommendation(
                    severity
                )
            }
        
        return {
            "is_escalating": False,
            "analysis": escalation_analysis
        }
    
    def _detect_score_escalation(
        self, 
        recent_history: List[Dict]
    ) -> Dict:
        """Detect if scores are increasing"""
        scores = [h['crisis_score'] for h in recent_history]
        
        # Check if monotonically increasing
        is_increasing = all(
            scores[i] < scores[i+1]
            for i in range(len(scores)-1)
        )
        
        if is_increasing:
            rate = scores[-1] - scores[0]
            return {
                "is_escalating": True,
                "escalation_rate": rate,
                "start_score": scores[0],
                "end_score": scores[-1]
            }
        
        return {"is_escalating": False}
    
    def _detect_severity_escalation(
        self, 
        recent_history: List[Dict]
    ) -> Dict:
        """Detect if crisis level is worsening"""
        levels = [h['crisis_level'] for h in recent_history]
        
        level_order = ["none", "low", "medium", "high", "critical"]
        level_indices = [level_order.index(l) for l in levels]
        
        # Check if levels are increasing
        is_worsening = all(
            level_indices[i] <= level_indices[i+1]
            for i in range(len(level_indices)-1)
        )
        
        if is_worsening and level_indices[-1] > level_indices[0]:
            return {
                "is_escalating": True,
                "start_level": levels[0],
                "end_level": levels[-1],
                "level_jump": level_indices[-1] - level_indices[0]
            }
        
        return {"is_escalating": False}
    
    def _detect_temporal_urgency(
        self, 
        recent_history: List[Dict]
    ) -> Dict:
        """Detect urgent temporal markers"""
        urgent_keywords = [
            "tonight", "right now", "can't wait",
            "immediately", "today", "this moment"
        ]
        
        latest_message = recent_history[-1]['message']
        
        has_urgency = any(
            keyword in latest_message.lower()
            for keyword in urgent_keywords
        )
        
        if has_urgency:
            return {
                "is_escalating": True,
                "urgency_type": "temporal",
                "urgency_indicators": [
                    kw for kw in urgent_keywords 
                    if kw in latest_message.lower()
                ]
            }
        
        return {"is_escalating": False}
    
    def _detect_communication_change(
        self,
        recent_history: List[Dict],
        full_history: List[Dict]
    ) -> Dict:
        """Detect change in communication pattern"""
        if len(full_history) < 6:
            return {"is_escalating": False}
        
        # Compare recent vs. previous frequency
        recent_timestamps = [h['timestamp'] for h in recent_history]
        previous_timestamps = [
            h['timestamp'] for h in full_history[:-len(recent_history)]
        ]
        
        recent_freq = self._calculate_frequency(recent_timestamps)
        previous_freq = self._calculate_frequency(previous_timestamps)
        
        # Sudden increase in frequency can indicate escalation
        if recent_freq > previous_freq * 2:
            return {
                "is_escalating": True,
                "change_type": "increased_frequency",
                "recent_freq": recent_freq,
                "previous_freq": previous_freq
            }
        
        return {"is_escalating": False}
    
    def _calculate_frequency(self, timestamps: List) -> float:
        """Calculate messages per hour"""
        if len(timestamps) < 2:
            return 0
        
        time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600
        return len(timestamps) / time_span if time_span > 0 else 0
    
    def _determine_escalation_severity(
        self, 
        escalation_analysis: Dict
    ) -> str:
        """Determine overall escalation severity"""
        escalation_count = sum(
            1 for analysis in escalation_analysis.values()
            if analysis.get('is_escalating', False)
        )
        
        if escalation_count >= 3:
            return "critical"
        elif escalation_count == 2:
            return "high"
        else:
            return "moderate"
    
    def _get_escalation_recommendation(self, severity: str) -> str:
        """Get recommendation based on escalation severity"""
        if severity == "critical":
            return "IMMEDIATE INTERVENTION REQUIRED"
        elif severity == "high":
            return "Priority monitoring and outreach recommended"
        else:
            return "Increased monitoring recommended"
```

**Tasks**:
- [ ] Implement EscalationDetector class
- [ ] Implement score escalation detection
- [ ] Implement severity escalation detection
- [ ] Implement temporal urgency detection
- [ ] Implement communication change detection
- [ ] Add unit tests with escalation test datasets
- [ ] Document escalation detection logic

---

### **Step 4.5: Integrate Context with Ensemble**

**Update**: `analysis/crisis_analyzer.py`

**Integration Logic**:
```python
class CrisisAnalyzer:
    """
    Updated for Phase 4: Context integration
    """
    
    def __init__(
        self,
        unified_config_manager,
        ensemble_coordinator,
        pattern_detection_manager,
        context_analyzer  # NEW
    ):
        """Initialize with context analyzer"""
        self.config = unified_config_manager
        self.ensemble = ensemble_coordinator
        self.patterns = pattern_detection_manager
        self.context = context_analyzer  # NEW
    
    def analyze_message(
        self, 
        user_id: str, 
        message: str
    ) -> Dict:
        """
        Analyze message with ensemble + context + patterns
        """
        # Step 1: Ensemble Analysis
        ensemble_result = self.ensemble.analyze_message(message)
        
        # Step 2: Context Analysis (NEW)
        context_result = self.context.analyze_with_context(
            user_id,
            message,
            ensemble_result
        )
        
        # Step 3: Pattern Detection
        pattern_result = self.patterns.detect_patterns(message)
        
        # Step 4: Combine all analyses
        final_result = self._combine_all_analyses(
            ensemble_result,
            context_result,
            pattern_result
        )
        
        return final_result
    
    def _combine_all_analyses(
        self,
        ensemble_result: Dict,
        context_result: Dict,
        pattern_result: Dict
    ) -> Dict:
        """
        Combine ensemble + context + patterns
        
        Priority order:
        1. Context escalation (highest priority)
        2. Ensemble consensus
        3. Pattern modifiers
        """
        # Start with context-adjusted score
        base_score = context_result['context_adjusted_score']
        
        # Check for critical escalation
        if context_result['escalation'].get('is_escalating'):
            if context_result['escalation']['severity'] == 'critical':
                base_score = max(base_score, 0.85)  # Force critical level
        
        # Apply pattern modifiers
        pattern_boost = self._calculate_pattern_boost(pattern_result)
        final_score = min(1.0, base_score + pattern_boost)
        
        return {
            "analysis_version": "v5.0-phase4",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            
            # Final Assessment
            "final_assessment": {
                "crisis_score": final_score,
                "crisis_level": self._determine_level(final_score),
                "requires_intervention": self._requires_intervention(
                    final_score,
                    context_result
                ),
                "priority": self._determine_priority(
                    final_score,
                    context_result
                )
            },
            
            # Component Results
            "ensemble_result": ensemble_result,
            "context_result": context_result,
            "pattern_result": pattern_result,
            
            # Enhanced Explanation
            "explanation": self._create_enhanced_explanation(
                ensemble_result,
                context_result,
                pattern_result
            )
        }
    
    def _requires_intervention(
        self, 
        final_score: float,
        context_result: Dict
    ) -> bool:
        """
        Determine if intervention needed
        
        Lower threshold if escalating
        """
        base_threshold = 0.70
        
        # Lower threshold for escalation
        if context_result['escalation'].get('is_escalating'):
            return final_score >= 0.60
        
        return final_score >= base_threshold
    
    def _determine_priority(
        self,
        final_score: float,
        context_result: Dict
    ) -> str:
        """Determine response priority"""
        if context_result['escalation'].get('is_escalating'):
            if context_result['escalation']['severity'] == 'critical':
                return "immediate"
        
        if final_score >= 0.85:
            return "immediate"
        elif final_score >= 0.65:
            return "high"
        elif final_score >= 0.40:
            return "medium"
        else:
            return "low"
```

**Tasks**:
- [ ] Update CrisisAnalyzer for context integration
- [ ] Implement analysis combination logic
- [ ] Update factory function
- [ ] Add priority determination
- [ ] Create enhanced explanation
- [ ] Add integration tests
- [ ] Update API endpoints
- [ ] Document context integration

---

### **Step 4.6: Test Context Analysis**

**Testing Requirements**:

**Use Escalation Patterns Dataset**:
- [ ] Run against escalation_patterns.json
- [ ] Validate escalation detection accuracy
- [ ] Test temporal pattern detection
- [ ] Verify context adjustments working

**Create New Test Scenarios**:
```json
{
  "context_test_001": {
    "description": "User starts okay, gradually worsens",
    "messages": [
      {"time": "10:00", "text": "Morning everyone", "expected_score": 0.1},
      {"time": "12:00", "text": "Not feeling great today", "expected_score": 0.3},
      {"time": "15:00", "text": "Things are getting worse", "expected_score": 0.5},
      {"time": "18:00", "text": "I can't handle this anymore", "expected_score": 0.7},
      {"time": "21:00", "text": "I give up", "expected_score": 0.9}
    ],
    "expected_escalation": true,
    "expected_final_score": ">0.85"
  },
  
  "context_test_002": {
    "description": "Chronic low-level distress",
    "messages": [
      {"time": "09:00", "text": "Struggling today", "expected_score": 0.4},
      {"time": "09:30", "text": "Still not good", "expected_score": 0.4},
      {"time": "10:00", "text": "This isn't getting better", "expected_score": 0.5},
      {"time": "10:30", "text": "Feeling really down", "expected_score": 0.5}
    ],
    "expected_escalation": false,
    "expected_context_boost": true,
    "expected_final_score": ">0.5"
  }
}
```

**Performance Testing**:
- [ ] Measure history storage overhead
- [ ] Test with 100 users
- [ ] Test memory usage
- [ ] Test cleanup effectiveness

**Tasks**:
- [ ] Create context-specific test datasets
- [ ] Run escalation detection tests
- [ ] Run temporal pattern tests
- [ ] Run integration tests
- [ ] Generate context analysis report
- [ ] Document test results

---

### **Step 4.7: Phase 4 Validation & Sign-Off**

**Phase 4 Complete Checklist**:

**Context Implementation**:
- [ ] ContextAnalyzer implemented and tested
- [ ] Message history storage working
- [ ] Temporal pattern detection functional
- [ ] Escalation detection operational
- [ ] Context integration complete

**Testing**:
- [ ] Escalation patterns detected correctly
- [ ] Temporal analysis accurate
- [ ] Context adjustments appropriate
- [ ] False escalation rate acceptable
- [ ] Performance acceptable

**Integration**:
- [ ] Integrated with CrisisAnalyzer
- [ ] Factory functions working
- [ ] Configuration complete
- [ ] API endpoints updated

**Clean Architecture Compliance**:
- [ ] All files have version headers
- [ ] Factory functions used
- [ ] Configuration via JSON + environment
- [ ] Dependency injection maintained

**Documentation**:
- [ ] Context architecture documented
- [ ] Escalation detection explained
- [ ] Configuration guide complete
- [ ] Testing methodology documented

**Success Criteria**:
- ✅ Context analysis operational
- ✅ Escalation detection working
- ✅ Temporal patterns identified
- ✅ Integration with ensemble complete
- ✅ Ready for pattern enhancement

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Context analysis validated
- [ ] Test coverage sufficient
- [ ] Ready to proceed to Phase 5

---

## 📝 **PHASE 5: PATTERN ENHANCEMENT INTEGRATION**

### **Status**: ⏳ **NOT STARTED** (Blocked by Phase 4)

### **Duration**: 1 week
### **Priority**: MEDIUM-LOW

### **Objectives**:
- Integrate existing pattern detection
- Enhance patterns with ensemble insights
- Add new pattern types
- Test complete crisis detection pipeline
- Validate end-to-end performance

---

### **Step 5.1: Review Existing Pattern Detection**

**Current Pattern System** (from v3.1):
- Temporal modifiers ("tonight", "right now")
- Crisis keywords
- Contextual patterns
- Polarity detection

**Tasks**:
- [ ] Audit existing PatternDetectionManager
- [ ] Identify what works well
- [ ] Identify what needs enhancement
- [ ] Document current pattern system
- [ ] Plan integration strategy

---

### **Step 5.2: Enhance Patterns with Ensemble Insights**

**New Pattern Types**:

**1. Ensemble-Informed Patterns**:
- Use emotion detection to refine keyword matching
- Use irony detection to reinterpret sentiment patterns
- Use crisis classifier to validate pattern matches

**2. Multi-Signal Patterns**:
- Combine ensemble + patterns for higher confidence
- Example: "I'm fine" + irony detected + negative emotions = crisis

**3. Community-Specific Patterns**:
- LGBTQIA+ specific language patterns
- Community slang recognition
- Cultural context understanding

**Tasks**:
- [ ] Design ensemble-pattern integration
- [ ] Implement multi-signal patterns
- [ ] Add community-specific patterns
- [ ] Test pattern enhancements
- [ ] Document new patterns

---

### **Step 5.3: Integrate Patterns with CrisisAnalyzer**

**Update**: `analysis/crisis_analyzer.py`

**Final Integration**:
```python
def _combine_all_analyses(
    self,
    ensemble_result: Dict,
    context_result: Dict,
    pattern_result: Dict
) -> Dict:
    """
    Final combination: Ensemble + Context + Patterns
    """
    # Priority order:
    # 1. Context escalation (critical situations)
    # 2. Ensemble consensus (AI models agree)
    # 3. Pattern modifiers (keyword boosts)
    
    base_score = context_result['context_adjusted_score']
    
    # Apply pattern modifiers
    pattern_boost = self._calculate_intelligent_pattern_boost(
        pattern_result,
        ensemble_result  # Use ensemble to validate patterns
    )
    
    final_score = min(1.0, base_score + pattern_boost)
    
    return final_result
```

**Tasks**:
- [ ] Update CrisisAnalyzer with pattern integration
- [ ] Implement intelligent pattern boosting
- [ ] Test complete pipeline
- [ ] Validate performance
- [ ] Document integration

---

### **Step 5.4: End-to-End Testing**

**Complete Pipeline Test**:
```
Message → Ensemble (4 models) → Context Analysis → Pattern Enhancement → Final Score
```

**Test All Datasets**:
- [ ] crisis_examples.json - end-to-end
- [ ] safe_examples.json - end-to-end
- [ ] edge_cases.json - end-to-end
- [ ] lgbtqia_specific.json - end-to-end
- [ ] escalation_patterns.json - end-to-end

**Performance Validation**:
- [ ] Total latency < 15 seconds ✓
- [ ] VRAM < 2GB ✓
- [ ] Accuracy > v3.1 baseline ✓
- [ ] False positive rate acceptable ✓

**Tasks**:
- [ ] Run complete test suite
- [ ] Generate comprehensive report
- [ ] Compare to v3.1 baseline
- [ ] Identify remaining issues
- [ ] Document results

---

### **Step 5.5: Phase 5 Validation & Sign-Off**

**Phase 5 Complete Checklist**:

**Pattern Enhancement**:
- [ ] Patterns integrated with ensemble
- [ ] New pattern types implemented
- [ ] Community patterns added
- [ ] Complete pipeline tested

**Testing**:
- [ ] All datasets passed
- [ ] Performance within targets
- [ ] Accuracy improved
- [ ] Edge cases handled

**Integration**:
- [ ] Complete CrisisAnalyzer functional
- [ ] All components working together
- [ ] API fully operational
- [ ] Documentation complete

**Success Criteria**:
- ✅ Complete v5.0 crisis detection pipeline operational
- ✅ All three analysis layers working together
- ✅ Performance and accuracy targets met
- ✅ Ready for production deployment

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Complete system validated
- [ ] Ready to proceed to Phase 6

---

## 📝 **PHASE 6: PRODUCTION DEPLOYMENT & OPTIMIZATION**

### **Status**: ⏳ **NOT STARTED** (Blocked by Phase 5)

### **Duration**: 2-3 weeks
### **Priority**: HIGH (when ready)

### **Objectives**:
- Deploy to production server
- Implement monitoring and logging
- Add performance optimizations
- Set up alerting system
- Create operational procedures

---

### **Step 6.1: Docker Containerization**

**Requirements**:
- Create production Dockerfile
- Configure for GPU support
- Optimize image size
- Set up Docker Compose

**Dockerfile Example**:
```dockerfile
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Download models during build
RUN python3 scripts/download_models.py

# Expose API port
EXPOSE 30880

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:30880/health || exit 1

# Start application
CMD ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "30880"]
```

**Tasks**:
- [ ] Create production Dockerfile
- [ ] Set up Docker Compose
- [ ] Test GPU access in container
- [ ] Optimize image size
- [ ] Document deployment

---

### **Step 6.2: Monitoring & Logging**

**Implement**:
- Prometheus metrics
- Grafana dashboards
- Log aggregation
- Performance tracking

**Key Metrics**:
```python
# Crisis detection metrics
crisis_detection_total
crisis_detection_by_level
false_positive_rate
false_negative_rate

# Performance metrics
analysis_latency_seconds
model_inference_time
vram_usage_mb
cpu_usage_percent

# System metrics
api_requests_total
api_errors_total
model_failures_total
```

**Tasks**:
- [ ] Set up Prometheus
- [ ] Create Grafana dashboards
- [ ] Configure log aggregation
- [ ] Set up alerting rules
- [ ] Document monitoring

---

### **Step 6.3: Performance Optimization**

**Optimization Targets**:
- [ ] Reduce latency to < 10 seconds
- [ ] Optimize VRAM usage
- [ ] Implement caching
- [ ] Add batch processing
- [ ] Optimize model loading

**Tasks**:
- [ ] Profile system performance
- [ ] Identify bottlenecks
- [ ] Implement optimizations
- [ ] Validate improvements
- [ ] Document optimizations

---

### **Step 6.4: Production Deployment**

**Deployment Steps**:
- [ ] Deploy to production server (10.20.30.253)
- [ ] Configure environment variables
- [ ] Set up SSL/TLS
- [ ] Configure firewall
- [ ] Test production access

**Rollout Strategy**:
- [ ] Deploy to staging first
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Monitor for 24 hours
- [ ] Validate stability

**Tasks**:
- [ ] Execute deployment
- [ ] Validate production functionality
- [ ] Monitor initial performance
- [ ] Document deployment procedures

---

### **Step 6.5: Phase 6 Validation & Sign-Off**

**Phase 6 Complete Checklist**:

**Deployment**:
- [ ] Deployed to production
- [ ] Monitoring operational
- [ ] Logging configured
- [ ] Alerting working
- [ ] Performance optimized

**Operational Readiness**:
- [ ] Runbooks created
- [ ] On-call procedures defined
- [ ] Backup procedures tested
- [ ] Disaster recovery plan documented

**Success Criteria**:
- ✅ System operational in production
- ✅ 24/7 availability achieved
- ✅ Performance targets met
- ✅ Monitoring and alerting working

**Sign-Off Required**:
- [ ] Project Lead approval
- [ ] Production deployment validated
- [ ] Ready for Phase 7

---

## 📝 **PHASE 7: MONITORING & CONTINUOUS IMPROVEMENT**

### **Status**: ⏳ **NOT STARTED** (Ongoing after Phase 6)

### **Duration**: Ongoing
### **Priority**: CONTINUOUS

### **Objectives**:
- Monitor production performance
- Collect real-world feedback
- Iterate on model performance
- Continuous optimization
- Community feedback integration

---

### **Step 7.1: Production Monitoring**

**Daily Tasks**:
- [ ] Review crisis detection metrics
- [ ] Monitor false positive/negative rates
- [ ] Check system performance
- [ ] Review errors and warnings
- [ ] Validate model health

---

### **Step 7.2: Model Performance Analysis**

**Weekly Tasks**:
- [ ] Analyze model accuracy
- [ ] Review edge cases
- [ ] Identify improvement areas
- [ ] Test model updates
- [ ] Document findings

---

### **Step 7.3: Community Feedback Integration**

**Monthly Tasks**:
- [ ] Collect community feedback
- [ ] Review missed crisis cases
- [ ] Update test datasets
- [ ] Enhance patterns
- [ ] Improve documentation

---

### **Step 7.4: Continuous Optimization**

**Quarterly Tasks**:
- [ ] Evaluate new models
- [ ] Update ensemble composition
- [ ] Optimize performance
- [ ] Enhance features
- [ ] Update documentation

---

## 🎯 **SUCCESS CRITERIA**

### **Phase Completion Criteria**:

**Phase 1**: Testing Framework
- ✅ Can test any model objectively
- ✅ Baseline performance documented
- ✅ Test datasets comprehensive

**Phase 2**: Model Migration
- ✅ All 4 models operational
- ✅ Performance within targets
- ✅ Improved over baseline

**Phase 3**: Ensemble Coordinator
- ✅ Multi-model consensus working
- ✅ Explainability implemented
- ✅ Conflict resolution functional

**Phase 4**: Context Analysis
- ✅ Escalation detection working
- ✅ Temporal patterns identified
- ✅ History tracking operational

**Phase 5**: Pattern Enhancement
- ✅ Complete pipeline functional
- ✅ All components integrated
- ✅ End-to-end testing passed

**Phase 6**: Production Deployment
- ✅ Deployed to production
- ✅ Monitoring operational
- ✅ 24/7 availability

**Phase 7**: Continuous Improvement
- ✅ Ongoing monitoring
- ✅ Regular optimization
- ✅ Community feedback integration

---

## 📊 **DEPENDENCIES & PREREQUISITES**

### **Phase Dependencies**:
```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7
  ✅       ⏳        ⏳        ⏳        ⏳        ⏳        ⏳        ⏳
```

### **Technical Prerequisites**:
- **Server**: Debian 12, AMD Ryzen 7 5800x, 64GB RAM
- **GPU**: NVIDIA RTX 3060 12GB VRAM
- **Docker**: Latest version with GPU support
- **Python**: 3.9+
- **CUDA**: 12.2+

### **Software Dependencies**:
```
transformers==4.35.0
torch==2.1.0
fastapi==0.104.0
uvicorn==0.24.0
numpy==1.24.0
pandas==2.1.0
```

---

## 🔄 **ROLLBACK PROCEDURES**

### **If Phase Fails**:

**Testing Framework Issues (Phase 1)**:
- Rollback: Continue with v3.1 models
- Fix testing framework
- Re-baseline

**Model Migration Issues (Phase 2)**:
- Rollback: Keep v3.1 models
- Fix specific model
- Re-test

**Ensemble Issues (Phase 3)**:
- Rollback: Use single best model
- Fix consensus logic
- Re-test ensemble

**Context Issues (Phase 4)**:
- Rollback: Disable context analysis
- Fix context logic
- Re-enable

**Production Issues (Phase 6)**:
- Rollback: Redeploy v3.1
- Fix production issues
- Re-deploy v5.0

---

## 📈 **PROGRESS TRACKING**

### **Current Status**: Phase 0 Complete ✅

### **Phase Completion**:
- [x] Phase 0: Foundation & Planning - 100% ✅
- [ ] Phase 1: Testing Framework - 0%
- [ ] Phase 2: Model Migration - 0%
- [ ] Phase 3: Ensemble Coordinator - 0%
- [ ] Phase 4: Context Analysis - 0%
- [ ] Phase 5: Pattern Enhancement - 0%
- [ ] Phase 6: Production Deployment - 0%
- [ ] Phase 7: Continuous Improvement - 0%

### **Overall Progress**: 12.5% (1/8 phases complete)

---

## 💾 **VERSION CONTROL**

### **Document Version**: v5.0
### **Last Updated**: 2025-12-30
### **Last Updated By**: Project Team

### **Change Log**:
```
2025-12-30: Initial roadmap created (Phase 0 complete)
- Architecture decision documented
- Model selection finalized
- Comprehensive phase plan created
```

---

## 📞 **STAKEHOLDER COMMUNICATION**

### **Update Frequency**:
- **Daily**: Progress updates during active development
- **Weekly**: Phase completion reports
- **Monthly**: Overall project status

### **Escalation Path**:
1. Development Team
2. Project Lead
3. Community Leadership

---

## 🎓 **LEARNING & DOCUMENTATION**

### **Documentation Requirements**:
- [ ] Architecture diagrams
- [ ] API documentation
- [ ] Configuration guides
- [ ] Troubleshooting guides
- [ ] Runbooks
- [ ] Community guides

### **Knowledge Transfer**:
- [ ] Code review sessions
- [ ] Documentation reviews
- [ ] Training materials
- [ ] Community workshops

---

## 🏁 **FINAL NOTES**

This roadmap represents the complete plan for Ash-NLP v5.0 rewrite. It is designed to be:

1. **Comprehensive**: Covers all aspects of the rewrite
2. **Trackable**: Clear checkboxes and progress indicators
3. **Flexible**: Can adapt to changes and discoveries
4. **Collaborative**: Supports multi-conversation development
5. **Compliant**: Follows Clean Architecture Charter v5.0

**Remember**:
- ⚠️ Always update this roadmap as progress is made
- ⚠️ Document lessons learned in each phase
- ⚠️ Update checklist items as completed
- ⚠️ Communicate blockers immediately
- ⚠️ Maintain Clean Architecture compliance throughout

---

**Built with care for chosen family** 🏳️‍🌈
