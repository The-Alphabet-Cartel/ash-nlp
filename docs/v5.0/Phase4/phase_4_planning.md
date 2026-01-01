# Ash-NLP v5.0 Phase 4 Planning Document

**Document Version**: v5.0-4-PLANNING-2  
**Created**: 2026-01-01  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [Website](https://alphabetcartel.org)

---

## ⏳ Phase 4 Status: IN PROGRESS

**Started**: January 1, 2026  
**Target Completion**: January 14, 2026 (2 weeks)  
**Priority**: HIGH

---

## Executive Summary

Phase 4 focuses on **Ensemble Coordinator Enhancement** - building upon the working decision engine from Phase 3 to add intelligent consensus algorithms, comprehensive result aggregation, conflict detection, and human-readable explainability.

### What Phase 3 Delivered
- ✅ Basic weighted decision engine
- ✅ Four-model ensemble (BART, Sentiment, Irony, Emotions)
- ✅ Production API endpoints
- ✅ Docker deployment with GPU acceleration

### What Phase 4 Adds
- 🆕 Multiple consensus algorithm options
- 🆕 Intelligent conflict detection and resolution
- 🆕 Comprehensive result aggregation with metadata
- 🆕 Human-readable explainability layer
- 🆕 Discord alerts for model conflicts
- 🆕 Request batching optimization

---

## Phase 4 Objectives

| Objective | Priority | Description |
|-----------|----------|-------------|
| Consensus Algorithms | P0 | Multiple strategies for model agreement |
| Conflict Detection | P0 | Identify and resolve model disagreements |
| Result Aggregation | P1 | Structured, comprehensive output format |
| Explainability Layer | P1 | Human-readable decision explanations |
| API Enhancement | P2 | New endpoints for consensus config |
| Request Batching | P2 | Optimization from Phase 3 |

**Deferred to Phase 5**: Benchmarking/profiling, memory optimization

---

## Architecture Enhancement

### Current System (Phase 3)

```
┌─────────────────────────────────────────────────────────────────┐
│  Models → Decision Engine (Weighted Scoring) → Crisis Score    │
└─────────────────────────────────────────────────────────────────┘
```

### Enhanced System (Phase 4)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Ash-NLP Ensemble Coordinator                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        Model Layer (Phase 3)                           │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │ │
│  │  │  BART   │  │Sentiment│  │  Irony  │  │Emotions │                   │ │
│  │  │  0.50   │  │  0.25   │  │  0.15   │  │  0.10   │                   │ │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘                   │ │
│  └───────┼───────────┼───────────┼───────────┼───────────────────────────┘ │
│          │           │           │           │                             │
│          └───────────┴─────┬─────┴───────────┘                             │
│                            ▼                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    Consensus Engine (Phase 4 NEW)                      │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────┐       │ │
│  │  │ Conflict       │  │ Consensus      │  │ Algorithm Selector  │       │ │
│  │  │ Detector       │→ │ Resolver       │→ │ - Weighted Voting   │       │ │
│  │  │                │  │                │  │ - Majority Voting   │       │ │
│  │  │                │  │                │  │ - Unanimous         │       │ │
│  │  │                │  │                │  │ - Conflict-Aware    │       │ │
│  │  └────────────────┘  └────────────────┘  └─────────────────────┘       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                            │                                               │
│                            ▼                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    Result Aggregator (Phase 4 NEW)                     │ │
│  │  - Crisis Assessment (score, level, intervention_required)             │ │
│  │  - Model Results (individual contributions)                            │ │
│  │  - Consensus Analysis (algorithm, agreement_level, conflicts)          │ │
│  │  - Performance Metrics (latency, VRAM)                                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                            │                                               │
│                            ▼                                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    Explainability Layer (Phase 4 NEW)                  │ │
│  │  - Decision Summary (plain English)                                    │ │
│  │  - Model Contributions (what each model detected)                      │ │
│  │  - Key Factors (primary crisis indicators)                             │ │
│  │  - Recommended Action (intervention priority)                          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                            │                                               │
│                            ▼                                               │
│                   ┌────────────────┐                                       │
│                   │  Final Output   │                                       │
│                   │  (Comprehensive)│                                       │
│                   └────────────────┘                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Deliverables

### 4.1 Consensus Algorithms ⏳

**Priority**: P0  
**Files**: `src/ensemble/consensus.py`, `src/config/consensus_config.json`

#### Algorithm Implementations

**4.1.1 Weighted Voting Consensus** (Default - enhances existing)
```python
def weighted_voting_consensus(
    model_results: Dict,
    weights: Dict
) -> Dict:
    """
    Weight each model's prediction by confidence and assigned weight
    
    Formula:
    crisis_score = Σ(model_score * model_weight * model_confidence) / Σ(weights)
    """
```

**4.1.2 Majority Voting Consensus**
```python
def majority_voting_consensus(
    model_results: Dict,
    threshold: float = 0.5
) -> Dict:
    """
    Binary decision: More than half of models agree = final decision
    Useful for clear crisis/no-crisis decisions
    """
```

**4.1.3 Unanimous Consensus** (Conservative)
```python
def unanimous_consensus(
    model_results: Dict,
    crisis_threshold: float = 0.6
) -> Dict:
    """
    All models must agree for crisis classification
    Most conservative - minimizes false positives
    """
```

**4.1.4 Conflict-Aware Consensus** (Council-inspired)
```python
def conflict_aware_consensus(
    model_results: Dict,
    disagreement_threshold: float = 0.15
) -> Dict:
    """
    Detect significant disagreements and flag for review
    Inspired by LLM Council peer review concepts
    """
```

#### Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| 4.1.1 | Implement weighted_voting_consensus() | ⬜ |
| 4.1.2 | Implement majority_voting_consensus() | ⬜ |
| 4.1.3 | Implement unanimous_consensus() | ⬜ |
| 4.1.4 | Implement conflict_aware_consensus() | ⬜ |
| 4.1.5 | Create ConsensusSelector class | ⬜ |
| 4.1.6 | Create consensus_config.json | ⬜ |
| 4.1.7 | Add environment variable overrides | ⬜ |
| 4.1.8 | Unit tests for all algorithms | ⬜ |
| 4.1.9 | Integration tests with decision engine | ⬜ |

---

### 4.2 Conflict Detection & Resolution ⏳

**Priority**: P0  
**Files**: `src/ensemble/conflict_detector.py`, `src/ensemble/conflict_resolver.py`

#### ConflictDetector Class

Identifies disagreements between ensemble models:

| Conflict Type | Description | Severity |
|---------------|-------------|----------|
| Score Disagreement | Max-min score > 0.4 | High |
| Irony-Sentiment Conflict | Sentiment positive but irony detected | Medium |
| Emotion-Crisis Mismatch | High crisis score but no crisis emotions | Medium |
| Label Disagreement | Models predict different crisis types | Medium |

#### ConflictResolver Class

Applies resolution strategies:

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Conservative | Use highest crisis score | Safety-first (default) |
| Optimistic | Use lowest crisis score | Reduce false positives |
| Mean | Use average score | Balanced approach |
| Review Flag | Flag for human review | Unresolvable conflicts |

#### Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| 4.2.1 | Implement ConflictDetector class | ⬜ |
| 4.2.2 | Implement score disagreement detection | ⬜ |
| 4.2.3 | Implement irony-sentiment conflict detection | ⬜ |
| 4.2.4 | Implement emotion-crisis mismatch detection | ⬜ |
| 4.2.5 | Implement label disagreement detection | ⬜ |
| 4.2.6 | Implement ConflictResolver class | ⬜ |
| 4.2.7 | Implement conservative strategy | ⬜ |
| 4.2.8 | Implement review flag strategy | ⬜ |
| 4.2.9 | Unit tests for conflict detection | ⬜ |
| 4.2.10 | Integration with decision engine | ⬜ |
| 4.2.11 | Discord webhook alerts for conflicts | ⬜ |

---

### 4.3 Result Aggregation ⏳

**Priority**: P1  
**Files**: `src/ensemble/aggregator.py`

#### ResultAggregator Class

Produces comprehensive, structured output:

```json
{
  "ensemble_version": "v5.0",
  "timestamp": "2026-01-01T12:00:00Z",
  "request_id": "uuid",
  
  "crisis_assessment": {
    "crisis_score": 0.78,
    "crisis_level": "high",
    "confidence": 0.85,
    "requires_intervention": true
  },
  
  "model_results": {
    "bart_classifier": {
      "top_labels": ["self-harm thoughts", "severe depression"],
      "confidence": 0.82,
      "weight": 0.50,
      "contribution": 0.41
    },
    "sentiment_analyzer": { ... },
    "irony_detector": { ... },
    "emotion_detector": { ... }
  },
  
  "consensus": {
    "algorithm": "weighted_voting",
    "agreement_level": "strong_agreement",
    "has_conflict": false,
    "requires_review": false
  },
  
  "explanation": {
    "decision_summary": "HIGH CONCERN: Models detected significant crisis indicators with 85% confidence.",
    "primary_indicators": ["self-harm thoughts", "severe depression", "sadness", "fear"],
    "model_contributions": [ ... ],
    "recommended_action": { ... }
  },
  
  "performance": {
    "total_latency_ms": 185,
    "per_model_latency": { ... },
    "cache_hit": false
  }
}
```

#### Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| 4.3.1 | Implement ResultAggregator class | ⬜ |
| 4.3.2 | Implement crisis level determination | ⬜ |
| 4.3.3 | Implement agreement level calculation | ⬜ |
| 4.3.4 | Implement primary indicator identification | ⬜ |
| 4.3.5 | Update API schemas for new response format | ⬜ |
| 4.3.6 | Backward compatibility with existing responses | ⬜ |
| 4.3.7 | Unit tests for aggregation | ⬜ |

---

### 4.4 Explainability Layer ⏳

**Priority**: P1  
**Files**: `src/ensemble/explainability.py`

#### ExplainabilityGenerator Class

Creates human-readable explanations for crisis decisions:

| Component | Description |
|-----------|-------------|
| Decision Summary | Plain-English summary of the crisis assessment |
| Model Contributions | What each model detected and how it influenced the decision |
| Key Factors | Primary crisis indicators that drove the classification |
| Recommended Action | Priority level and suggested intervention |

#### Example Output

```
DECISION SUMMARY:
HIGH CONCERN: Models detected significant crisis indicators with 85% confidence.

MODEL CONTRIBUTIONS:
• Crisis Classifier: Detected "self-harm thoughts" (82%) and "severe depression" (67%)
• Emotion Detector: Strong sadness (91%), fear (73%), and grief (58%)
• Sentiment Analyzer: Highly negative sentiment (87%)
• Irony Detector: No sarcasm detected - message appears sincere

KEY FACTORS:
• self-harm thoughts
• severe depression
• sadness
• fear
• negative sentiment

RECOMMENDED ACTION:
Priority: HIGH
Action: Check user history, consider outreach
Escalation: Moderator review recommended
```

#### Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| 4.4.1 | Implement ExplainabilityGenerator class | ⬜ |
| 4.4.2 | Implement decision_summary generation | ⬜ |
| 4.4.3 | Implement model_contributions formatting | ⬜ |
| 4.4.4 | Implement key_factors identification | ⬜ |
| 4.4.5 | Implement recommended_action generation | ⬜ |
| 4.4.6 | Template system for explanations | ⬜ |
| 4.4.7 | Unit tests for explainability | ⬜ |
| 4.4.8 | Integration with result aggregator | ⬜ |

---

### 4.5 API Enhancements ⏳

**Priority**: P2  
**Files**: `src/api/routes.py`, `src/api/schemas.py`

#### New/Updated Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/analyze` | POST | Enhanced response with full aggregation + explanation |
| `/api/v1/consensus/config` | GET | Get current consensus configuration |
| `/api/v1/consensus/config` | PUT | Update consensus algorithm selection |

**Note**: Explanations are generated on-demand as part of the `/analyze` response. No separate `/explain/{request_id}` endpoint needed at this time.

#### Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| 4.5.1 | Update analyze endpoint response schema | ⬜ |
| 4.5.2 | Implement consensus config GET endpoint | ⬜ |
| 4.5.3 | Implement consensus config PUT endpoint | ⬜ |
| 4.5.4 | Update OpenAPI documentation | ⬜ |
| 4.5.5 | API integration tests | ⬜ |

---

### 4.6 Deferred Phase 3 Tasks ⏳

**Priority**: P2

Tasks from Phase 3:

| Task ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| 4.6.1 | Request batching optimization (3.7.3) | ⬜ | Include in Phase 4 |
| 4.6.2 | Benchmark and profiling (3.7.5) | ➡️ | Deferred to Phase 5 |
| 4.6.3 | Memory optimization (3.7.6) | ➡️ | Deferred to Phase 5 |

---

## Configuration Files

### consensus_config.json (NEW)

```json
{
  "_metadata": {
    "file_version": "v5.0-4-1",
    "last_modified": "2026-01-01",
    "clean_architecture": "Compliant"
  },
  
  "consensus": {
    "description": "Consensus algorithm configuration for ensemble decision-making",
    "default_algorithm": "${NLP_CONSENSUS_ALGORITHM}",
    "algorithms": {
      "weighted_voting": {
        "enabled": true,
        "description": "Weight-based model contribution scoring"
      },
      "majority_voting": {
        "enabled": true,
        "threshold": "${NLP_CONSENSUS_MAJORITY_THRESHOLD}",
        "description": "Binary majority decision"
      },
      "unanimous": {
        "enabled": true,
        "crisis_threshold": "${NLP_CONSENSUS_UNANIMOUS_THRESHOLD}",
        "description": "All models must agree"
      },
      "conflict_aware": {
        "enabled": true,
        "disagreement_threshold": "${NLP_CONSENSUS_CONFLICT_THRESHOLD}",
        "description": "Detect and handle model disagreements"
      }
    },
    "defaults": {
      "default_algorithm": "weighted_voting",
      "majority_threshold": 0.5,
      "unanimous_threshold": 0.6,
      "conflict_threshold": 0.15
    },
    "validation": {
      "default_algorithm": {
        "type": "string",
        "allowed_values": ["weighted_voting", "majority_voting", "unanimous", "conflict_aware"]
      },
      "majority_threshold": {
        "type": "float",
        "range": [0.3, 0.8]
      },
      "unanimous_threshold": {
        "type": "float",
        "range": [0.4, 0.9]
      },
      "conflict_threshold": {
        "type": "float",
        "range": [0.05, 0.5]
      }
    }
  },
  
  "conflict_resolution": {
    "description": "Configuration for handling model disagreements",
    "default_strategy": "${NLP_CONFLICT_RESOLUTION_STRATEGY}",
    "alert_on_conflict": "${NLP_CONFLICT_ALERT_ENABLED}",
    "strategies": {
      "conservative": {
        "description": "Use highest crisis score (safety-first)"
      },
      "optimistic": {
        "description": "Use lowest crisis score (reduce false positives)"
      },
      "mean": {
        "description": "Use average score (balanced)"
      },
      "review_flag": {
        "description": "Flag for human review"
      }
    },
    "defaults": {
      "default_strategy": "conservative",
      "alert_on_conflict": true
    },
    "validation": {
      "default_strategy": {
        "type": "string",
        "allowed_values": ["conservative", "optimistic", "mean", "review_flag"]
      },
      "alert_on_conflict": {
        "type": "boolean"
      }
    }
  },
  
  "explainability": {
    "description": "Configuration for explanation generation",
    "enabled": "${NLP_EXPLAINABILITY_ENABLED}",
    "verbosity": "${NLP_EXPLAINABILITY_VERBOSITY}",
    "defaults": {
      "enabled": true,
      "verbosity": "standard"
    },
    "validation": {
      "enabled": {
        "type": "boolean"
      },
      "verbosity": {
        "type": "string",
        "allowed_values": ["minimal", "standard", "detailed"]
      }
    }
  }
}
```

---

## File Structure (Phase 4 Additions)

```
ash-nlp/
├── src/
│   ├── ensemble/
│   │   ├── __init__.py
│   │   ├── decision_engine.py    # Phase 3 (enhanced)
│   │   ├── scoring.py            # Phase 3
│   │   ├── model_loader.py       # Phase 3
│   │   ├── fallback.py           # Phase 3
│   │   ├── consensus.py          # NEW - Phase 4
│   │   ├── conflict_detector.py  # NEW - Phase 4
│   │   ├── conflict_resolver.py  # NEW - Phase 4
│   │   ├── aggregator.py         # NEW - Phase 4
│   │   └── explainability.py     # NEW - Phase 4
│   │
│   ├── config/
│   │   ├── default.json          # Phase 3
│   │   ├── production.json       # Phase 3
│   │   ├── testing.json          # Phase 3
│   │   └── consensus_config.json # NEW - Phase 4
│   │
│   └── ... (existing structure)
│
├── docs/
│   └── v5.0/
│       └── Phase4/
│           ├── phase_4_planning.md     # This document
│           └── phase_4_completion.md   # To be created
│
└── tests/
    ├── test_datasets/                  # Copied from testing/test_datasets
    │   ├── crisis_examples.json
    │   ├── safe_examples.json
    │   ├── edge_cases.json
    │   ├── lgbtqia_specific.json
    │   └── escalation_patterns.json
    │
    └── phase4/                         # NEW - Phase 4 tests
        ├── test_consensus.py
        ├── test_conflict_detection.py
        ├── test_aggregation.py
        └── test_explainability.py
```

---

## Environment Variables (New)

Add to `.env.template`:

```bash
# Phase 4: Consensus Configuration
NLP_CONSENSUS_ALGORITHM=weighted_voting
NLP_CONSENSUS_MAJORITY_THRESHOLD=0.5
NLP_CONSENSUS_UNANIMOUS_THRESHOLD=0.6
NLP_CONSENSUS_CONFLICT_THRESHOLD=0.15

# Phase 4: Conflict Resolution
NLP_CONFLICT_RESOLUTION_STRATEGY=conservative
NLP_CONFLICT_ALERT_ENABLED=true

# Phase 4: Explainability
NLP_EXPLAINABILITY_ENABLED=true
NLP_EXPLAINABILITY_VERBOSITY=standard
```

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Consensus algorithms | 4/4 working | Unit tests pass |
| Conflict detection | All types identified | Edge case testing |
| Discord conflict alerts | Working | Manual verification |
| Result aggregation | Complete output | Schema validation |
| Explainability | Human-readable | Manual review |
| API enhancements | All endpoints | Integration tests |
| Request batching | Functional | Load testing |
| Performance impact | < 50ms overhead | Benchmarking |
| Test coverage | > 80% | Coverage report |

---

## Implementation Schedule

### Week 1: Core Components

| Day | Tasks |
|-----|-------|
| Day 1 | 4.1.1-4.1.4: Consensus algorithms |
| Day 2 | 4.1.5-4.1.9: Consensus selector + tests |
| Day 3 | 4.2.1-4.2.5: Conflict detection |
| Day 4 | 4.2.6-4.2.11: Conflict resolution + Discord alerts + tests |
| Day 5 | Buffer / catch-up |

### Week 2: Aggregation & Integration

| Day | Tasks |
|-----|-------|
| Day 6 | 4.3.1-4.3.4: Result aggregation |
| Day 7 | 4.3.5-4.3.7: API schema updates + tests |
| Day 8 | 4.4.1-4.4.4: Explainability core |
| Day 9 | 4.4.5-4.4.8: Templates + integration |
| Day 10 | 4.5.1-4.5.5: API endpoints |
| Day 11 | 4.6.1: Request batching |
| Day 12-14 | Integration testing + documentation |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Performance degradation | High | Profile each component, optimize hot paths |
| Breaking existing API | High | Backward compatibility layer |
| Complex conflict scenarios | Medium | Extensive edge case testing |
| Scope creep | Medium | Strict task prioritization |

---

## Dependencies

### Prerequisites
- ✅ Phase 3 complete and deployed
- ✅ Four-model ensemble operational
- ✅ Testing framework from Phase 1
- ✅ Test datasets in `tests/test_datasets/`

### External Dependencies
- None (all local processing)

---

## Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| Development Lead | PapaBearDoes | ⬜ Pending | |
| AI Assistant | Claude | ✅ Ready | 2026-01-01 |

---

## Notes

### Decisions Made

1. ✅ **Explanations**: Generated on-demand as part of `/analyze` response (no storage needed)
2. ✅ **Conflict Alerts**: Model conflicts will trigger Discord webhook alerts to moderators
3. ✅ **Batching**: Include in Phase 4; defer benchmarking and memory optimization to Phase 5
4. ✅ **Test Data**: Use existing datasets in `tests/test_datasets/`

### Design Decisions

1. **Default to Conservative**: Conflict resolution defaults to "conservative" (highest crisis score) because it's better to over-alert than under-alert for crisis detection.

2. **Backward Compatibility**: The enhanced response includes all fields from Phase 3, plus new fields. Existing integrations continue to work.

3. **Configurable Consensus**: Different use cases may need different consensus algorithms. The API allows runtime configuration.

4. **Explainability as Optional**: Full explanations can be disabled for performance-critical scenarios.

### Open Questions

1. What verbosity levels should explainability support? (minimal/standard/detailed proposed)

---

*Built with care for chosen family* 🏳️‍🌈
