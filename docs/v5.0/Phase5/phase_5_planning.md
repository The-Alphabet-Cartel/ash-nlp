# Ash-NLP v5.0 Phase 5 Planning Document

**Document Version**: v5.0-5-PLANNING-2  
**Created**: 2026-01-01  
**Status**: 🚧 IN PROGRESS  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [Website](https://alphabetcartel.org)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architectural Decisions](#architectural-decisions)
3. [Phase 5 Objectives](#phase-5-objectives)
4. [Task Breakdown](#task-breakdown)
5. [File Structure](#file-structure)
6. [API Changes](#api-changes)
7. [Configuration Schema](#configuration-schema)
8. [Testing Strategy](#testing-strategy)
9. [Success Criteria](#success-criteria)
10. [Dependencies](#dependencies)
11. [Risk Assessment](#risk-assessment)

---

## Executive Summary

### Phase 5 Goal

Implement **Context History Analysis** capabilities that enable Ash-NLP to detect escalation patterns, temporal trends, and crisis trajectories across message sequences provided by the client (Ash-Bot).

### Key Architectural Decision

**Ash-NLP remains STATELESS.** All message history and persistence is managed by Ash-Bot. Ash-NLP receives message history as part of the request payload and performs analysis algorithms on that data.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Ash-Bot                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Discord   │  │   Rolling   │  │      Persistence        │  │
│  │   Events    │  │   Window    │  │   (Redis/Database)      │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         │                │                     │                │
│         └────────────────┴─────────────────────┘                │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │ POST /analyze
                           │ {message, user_id, message_history[]}
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Ash-NLP (Stateless)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Ensemble  │  │  Consensus  │  │    Context Analysis     │  │
│  │   Models    │  │  Algorithms │  │    (NEW - Phase 5)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Stateless?

| Benefit | Explanation |
|---------|-------------|
| Single Responsibility | NLP does ONE thing: analyze text |
| Horizontal Scaling | Multiple NLP instances without shared state |
| Simpler Deployment | No Redis dependency for Ash-NLP |
| Easier Testing | Pure input → output, no state setup |
| Clean Separation | Clear boundary between storage and analysis |

### What Phase 5 Delivers

- ✅ Escalation detection across message sequences
- ✅ Temporal pattern recognition (late night, rapid posting)
- ✅ Trend analysis (worsening, stable, improving)
- ✅ Pattern classification (rapid, gradual, sudden onset)
- ✅ Intervention urgency scoring
- ✅ API enhancement to accept message history

### What Phase 5 Does NOT Include

- ❌ Message persistence (Ash-Bot responsibility)
- ❌ Rolling window management (Ash-Bot responsibility)
- ❌ User session tracking (Ash-Bot responsibility)
- ❌ Performance benchmarking (Ash-Thrash responsibility)

---

## Architectural Decisions

### AD-5.1: Stateless Context Analysis

**Decision**: Ash-NLP receives message history in request payload, does not store messages.

**Rationale**:
- Maintains single responsibility principle
- Enables horizontal scaling without state coordination
- Simplifies testing and deployment
- Keeps privacy controls at Ash-Bot level

**Consequences**:
- Slightly larger request payloads (~2KB for 10 messages)
- Ash-Bot must implement rolling window logic
- API schema must define message history format

### AD-5.2: Optional Context Analysis

**Decision**: Context analysis is opt-in via `include_context_analysis` flag.

**Rationale**:
- Backward compatibility with existing integrations
- Reduces processing overhead when context isn't needed
- Allows gradual adoption

**Consequences**:
- Two response shapes (with/without context)
- Must handle missing message_history gracefully

### AD-5.3: Escalation Detection Algorithm

**Decision**: Use score trajectory analysis with configurable thresholds.

**Rationale**:
- Leverages existing ensemble scoring for each message
- Detects patterns documented in escalation_patterns.json
- Configurable sensitivity via JSON + environment variables

**Consequences**:
- Must analyze each history message through ensemble (performance consideration)
- Need caching strategy for repeated messages

---

## Phase 5 Objectives

| ID | Objective | Priority | Status |
|----|-----------|----------|--------|
| 5.1 | Context Analyzer Core | P0 | ⏳ Not Started |
| 5.2 | Escalation Detection | P0 | ⏳ Not Started |
| 5.3 | Temporal Pattern Detection | P1 | ⏳ Not Started |
| 5.4 | Trend Analysis | P1 | ⏳ Not Started |
| 5.5 | API Enhancement | P0 | ⏳ Not Started |
| 5.6 | Configuration Management | P1 | ⏳ Not Started |
| 5.7 | Unit Tests | P0 | ⏳ Not Started |
| 5.8 | Integration Tests | P1 | ⏳ Not Started |

---

## Task Breakdown

### 5.1 Context Analyzer Core

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.1.1 | Create `src/context/__init__.py` | ⏳ |
| 5.1.2 | Implement `ContextAnalyzer` class | ⏳ |
| 5.1.3 | Implement `MessageSequence` dataclass | ⏳ |
| 5.1.4 | Implement `ContextAnalysisResult` dataclass | ⏳ |
| 5.1.5 | Create factory function `create_context_analyzer()` | ⏳ |
| 5.1.6 | Integrate with `EnsembleDecisionEngine` | ⏳ |

### 5.2 Escalation Detection

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.2.1 | Implement `EscalationDetector` class | ⏳ |
| 5.2.2 | Implement score trajectory analysis | ⏳ |
| 5.2.3 | Implement escalation rate calculation (rapid/gradual/sudden) | ⏳ |
| 5.2.4 | Implement intervention point identification | ⏳ |
| 5.2.5 | Implement escalation confidence scoring | ⏳ |
| 5.2.6 | Add Discord alerting for detected escalations | ⏳ |

### 5.3 Temporal Pattern Detection

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.3.1 | Implement `TemporalDetector` class | ⏳ |
| 5.3.2 | Implement late-night pattern detection (10PM-4AM) | ⏳ |
| 5.3.3 | Implement rapid posting detection (message frequency) | ⏳ |
| 5.3.4 | Implement time-of-day risk modifiers | ⏳ |
| 5.3.5 | Implement weekend/weekday pattern detection | ⏳ |

### 5.4 Trend Analysis

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.4.1 | Implement `TrendAnalyzer` class | ⏳ |
| 5.4.2 | Implement trend direction (worsening/stable/improving) | ⏳ |
| 5.4.3 | Implement trend velocity calculation | ⏳ |
| 5.4.4 | Implement pattern classification matching | ⏳ |
| 5.4.5 | Map to known patterns (evening deterioration, rejection spiral, etc.) | ⏳ |

### 5.5 API Enhancement

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.5.1 | Add `MessageHistoryItem` schema | ⏳ |
| 5.5.2 | Add `ContextAnalysisResponse` schema | ⏳ |
| 5.5.3 | Update `AnalyzeRequest` with `message_history` field | ⏳ |
| 5.5.4 | Update `AnalyzeResponse` with `context_analysis` field | ⏳ |
| 5.5.5 | Add `include_context_analysis` request parameter | ⏳ |
| 5.5.6 | Update `/analyze` endpoint handler | ⏳ |
| 5.5.7 | Add `GET /config/context` endpoint | ⏳ |
| 5.5.8 | Add `PUT /config/context` endpoint | ⏳ |
| 5.5.9 | Update OpenAPI documentation | ⏳ |

### 5.6 Configuration Management

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.6.1 | Create `src/config/context_config.json` | ✅ |
| 5.6.2 | Define escalation thresholds | ✅ |
| 5.6.3 | Define temporal pattern parameters | ✅ |
| 5.6.4 | Define trend analysis parameters | ✅ |
| 5.6.5 | Add environment variable overrides | ✅ |
| 5.6.6 | Update `.env.template` | ✅ |
| 5.6.7 | Update `ConfigManager` to load `context_config.json` | ⏳ (deferred - using dedicated manager) |
| 5.6.8 | Create `ContextConfigManager` class with factory function | ✅ |
| 5.6.9 | Add `max_history_size` setting (default: 20) | ✅ |
| 5.6.10 | Add `alert_cooldown_seconds` setting (default: 300) | ✅ |

### 5.7 Unit Tests

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.7.1 | Create `tests/phase5/__init__.py` | ⏳ |
| 5.7.2 | Create `tests/phase5/test_context_analyzer.py` | ⏳ |
| 5.7.3 | Create `tests/phase5/test_escalation_detector.py` | ⏳ |
| 5.7.4 | Create `tests/phase5/test_temporal_detector.py` | ⏳ |
| 5.7.5 | Create `tests/phase5/test_trend_analyzer.py` | ⏳ |
| 5.7.6 | Validate against `escalation_patterns.json` dataset | ⏳ |

### 5.8 Integration Tests

| Task ID | Description | Status |
|---------|-------------|--------|
| 5.8.1 | Test full `/analyze` flow with context | ⏳ |
| 5.8.2 | Test backward compatibility (no context) | ⏳ |
| 5.8.3 | Test configuration endpoints | ⏳ |
| 5.8.4 | Test Discord alerting for escalations | ⏳ |

---

## File Structure

### New Files to Create

```
src/context/
├── __init__.py                 # Module exports
├── context_analyzer.py         # Main orchestrator
├── escalation_detector.py      # Escalation detection algorithms
├── temporal_detector.py        # Time-based pattern detection
└── trend_analyzer.py           # Trend direction and velocity

src/config/
└── context_config.json         # Phase 5 configuration

tests/phase5/
├── __init__.py
├── test_context_analyzer.py
├── test_escalation_detector.py
├── test_temporal_detector.py
└── test_trend_analyzer.py
```

### Files to Modify

```
src/managers/config_manager.py   # Add context_config.json loading
src/ensemble/decision_engine.py  # Add context analysis integration
src/api/schemas.py               # Add Phase 5 request/response schemas
src/api/routes.py                # Update /analyze, add config endpoints
src/ensemble/__init__.py         # Export context components
.env.template                    # Add Phase 5 environment variables
```

### New Manager File

```
src/managers/
└── context_config_manager.py    # ContextConfigManager with factory function
```

---

## API Changes

### Enhanced Analyze Request

```json
{
  "message": "I can't do this anymore",
  "user_id": "user_123",
  "channel_id": "channel_456",
  
  "message_history": [
    {
      "message": "Not having the best day",
      "timestamp": "2025-01-01T16:00:00Z",
      "message_id": "msg_001"
    },
    {
      "message": "Things are getting harder to deal with",
      "timestamp": "2025-01-01T18:00:00Z",
      "message_id": "msg_002"
    },
    {
      "message": "I don't know if I can keep doing this",
      "timestamp": "2025-01-01T20:00:00Z",
      "message_id": "msg_003"
    }
  ],
  
  "include_context_analysis": true,
  "include_explanation": true,
  "verbosity": "standard",
  "consensus_algorithm": "weighted_voting"
}
```

### Enhanced Analyze Response

```json
{
  "crisis_detected": true,
  "severity": "critical",
  "crisis_score": 0.91,
  "confidence": 0.89,
  "requires_intervention": true,
  "recommended_action": "immediate_outreach",
  
  "signals": {
    "bart": {"label": "suicide ideation", "score": 0.94, "crisis_signal": 0.94},
    "sentiment": {"label": "negative", "score": 0.87, "crisis_signal": 0.87},
    "irony": {"label": "non_irony", "score": 0.92, "crisis_signal": 0.08},
    "emotions": {"label": "grief", "score": 0.81, "crisis_signal": 0.81}
  },
  
  "context_analysis": {
    "escalation_detected": true,
    "escalation_rate": "rapid",
    "escalation_pattern": "evening_deterioration",
    "pattern_confidence": 0.87,
    
    "trend": {
      "direction": "worsening",
      "velocity": "rapid",
      "score_delta": 0.66,
      "time_span_hours": 6
    },
    
    "temporal_factors": {
      "late_night_risk": false,
      "rapid_posting": false,
      "message_frequency": "normal",
      "time_risk_modifier": 1.0
    },
    
    "trajectory": {
      "start_score": 0.25,
      "end_score": 0.91,
      "peak_score": 0.91,
      "scores": [0.25, 0.45, 0.70, 0.91]
    },
    
    "intervention": {
      "urgency": "immediate",
      "recommended_point": 2,
      "current_position": 3,
      "intervention_delayed": true
    },
    
    "history_analyzed": {
      "message_count": 4,
      "time_span_hours": 6,
      "oldest_timestamp": "2025-01-01T16:00:00Z",
      "newest_timestamp": "2025-01-01T22:00:00Z"
    }
  },
  
  "explanation": {
    "verbosity": "standard",
    "decision_summary": "CRITICAL: Rapid escalation detected over 6 hours with active crisis indicators.",
    "key_factors": [
      "suicide ideation detected (Crisis Classifier - high impact)",
      "rapid escalation from low to critical severity",
      "evening deterioration pattern matched",
      "negative sentiment throughout sequence"
    ],
    "recommended_action": {
      "priority": "IMMEDIATE",
      "action": "Initiate crisis intervention protocol immediately",
      "escalation": "Contact crisis team and community moderators",
      "context": "User has shown rapid deterioration over 6 hours"
    },
    "plain_text": "..."
  },
  
  "consensus": { ... },
  "conflict_analysis": { ... },
  "processing_time_ms": 245
}
```

### New Configuration Endpoints

#### GET /config/context

Returns current context analysis configuration.

```json
{
  "enabled": true,
  "escalation": {
    "detection_enabled": true,
    "rapid_threshold_hours": 4,
    "gradual_threshold_hours": 24,
    "score_increase_threshold": 0.3,
    "minimum_messages": 3
  },
  "temporal": {
    "late_night_start": 22,
    "late_night_end": 4,
    "late_night_risk_modifier": 1.2,
    "rapid_posting_threshold_minutes": 30,
    "rapid_posting_count": 5
  },
  "trend": {
    "worsening_threshold": 0.15,
    "improving_threshold": -0.15,
    "velocity_rapid_threshold": 0.1
  }
}
```

#### PUT /config/context

Updates context analysis configuration at runtime.

---

## Configuration Schema

### context_config.json

```json
{
  "_metadata": {
    "file_version": "v5.0-5-1.0-1",
    "last_modified": "2026-01-01",
    "clean_architecture": "Compliant",
    "description": "Context analysis configuration for Phase 5 escalation and temporal detection"
  },

  "context_analysis": {
    "description": "Master toggle and limits for context analysis features",
    "enabled": "${NLP_CONTEXT_ANALYSIS_ENABLED}",
    "max_history_size": "${NLP_CONTEXT_MAX_HISTORY_SIZE}",
    "defaults": {
      "enabled": true,
      "max_history_size": 20
    },
    "validation": {
      "enabled": {
        "type": "boolean",
        "required": true
      },
      "max_history_size": {
        "type": "integer",
        "range": [3, 50],
        "required": true
      }
    }
  },

  "escalation_detection": {
    "description": "Configuration for escalation pattern detection",
    "enabled": "${NLP_ESCALATION_DETECTION_ENABLED}",
    "rapid_threshold_hours": "${NLP_ESCALATION_RAPID_THRESHOLD_HOURS}",
    "gradual_threshold_hours": "${NLP_ESCALATION_GRADUAL_THRESHOLD_HOURS}",
    "score_increase_threshold": "${NLP_ESCALATION_SCORE_THRESHOLD}",
    "minimum_messages": "${NLP_ESCALATION_MINIMUM_MESSAGES}",
    "alert_on_detection": "${NLP_ESCALATION_ALERT_ENABLED}",
    "alert_cooldown_seconds": "${NLP_ESCALATION_ALERT_COOLDOWN_SECONDS}",
    "defaults": {
      "enabled": true,
      "rapid_threshold_hours": 4,
      "gradual_threshold_hours": 24,
      "score_increase_threshold": 0.3,
      "minimum_messages": 3,
      "alert_on_detection": true,
      "alert_cooldown_seconds": 300
    },
    "validation": {
      "enabled": {
        "type": "boolean",
        "required": true
      },
      "rapid_threshold_hours": {
        "type": "integer",
        "range": [1, 12],
        "required": true
      },
      "gradual_threshold_hours": {
        "type": "integer",
        "range": [12, 168],
        "required": true
      },
      "score_increase_threshold": {
        "type": "float",
        "range": [0.1, 0.8],
        "required": true
      },
      "minimum_messages": {
        "type": "integer",
        "range": [2, 20],
        "required": true
      },
      "alert_on_detection": {
        "type": "boolean",
        "required": true
      },
      "alert_cooldown_seconds": {
        "type": "integer",
        "range": [60, 3600],
        "required": true
      }
    }
  },

  "temporal_detection": {
    "description": "Configuration for time-based pattern detection",
    "enabled": "${NLP_TEMPORAL_DETECTION_ENABLED}",
    "late_night_start_hour": "${NLP_TEMPORAL_LATE_NIGHT_START}",
    "late_night_end_hour": "${NLP_TEMPORAL_LATE_NIGHT_END}",
    "late_night_risk_modifier": "${NLP_TEMPORAL_LATE_NIGHT_MODIFIER}",
    "rapid_posting_threshold_minutes": "${NLP_TEMPORAL_RAPID_POSTING_MINUTES}",
    "rapid_posting_message_count": "${NLP_TEMPORAL_RAPID_POSTING_COUNT}",
    "defaults": {
      "enabled": true,
      "late_night_start_hour": 22,
      "late_night_end_hour": 4,
      "late_night_risk_modifier": 1.2,
      "rapid_posting_threshold_minutes": 30,
      "rapid_posting_message_count": 5
    },
    "validation": {
      "enabled": {
        "type": "boolean",
        "required": true
      },
      "late_night_start_hour": {
        "type": "integer",
        "range": [18, 23],
        "required": true
      },
      "late_night_end_hour": {
        "type": "integer",
        "range": [0, 8],
        "required": true
      },
      "late_night_risk_modifier": {
        "type": "float",
        "range": [1.0, 2.0],
        "required": true
      },
      "rapid_posting_threshold_minutes": {
        "type": "integer",
        "range": [5, 120],
        "required": true
      },
      "rapid_posting_message_count": {
        "type": "integer",
        "range": [3, 20],
        "required": true
      }
    }
  },

  "trend_analysis": {
    "description": "Configuration for trend direction and velocity analysis",
    "enabled": "${NLP_TREND_ANALYSIS_ENABLED}",
    "worsening_threshold": "${NLP_TREND_WORSENING_THRESHOLD}",
    "improving_threshold": "${NLP_TREND_IMPROVING_THRESHOLD}",
    "velocity_rapid_threshold": "${NLP_TREND_VELOCITY_RAPID}",
    "defaults": {
      "enabled": true,
      "worsening_threshold": 0.15,
      "improving_threshold": -0.15,
      "velocity_rapid_threshold": 0.1
    },
    "validation": {
      "enabled": {
        "type": "boolean",
        "required": true
      },
      "worsening_threshold": {
        "type": "float",
        "range": [0.05, 0.5],
        "required": true
      },
      "improving_threshold": {
        "type": "float",
        "range": [-0.5, -0.05],
        "required": true
      },
      "velocity_rapid_threshold": {
        "type": "float",
        "range": [0.01, 0.5],
        "required": true
      }
    }
  },

  "known_patterns": {
    "description": "Named escalation patterns for classification",
    "patterns": [
      "evening_deterioration",
      "week_long_decline",
      "post_rejection_spiral",
      "chronic_low_grade",
      "sudden_onset",
      "late_night_spiral",
      "dysphoria_escalation",
      "relationship_rejection",
      "isolation_indicator",
      "self_harm_urge",
      "substance_use_coping",
      "academic_stress_breakdown",
      "medication_change_crisis",
      "anniversary_trigger",
      "hormonal_cycle",
      "social_media_trigger"
    ]
  }
}
```

---

## Testing Strategy

### Test Dataset

Phase 5 will leverage the existing `tests/test_datasets/escalation_patterns.json` which contains **20 escalation patterns** with:

- **Rapid escalation**: 7 patterns
- **Gradual escalation**: 8 patterns  
- **Sudden onset**: 5 patterns

Each pattern includes:
- Multi-message sequences (3-5 messages)
- Expected crisis scores per message
- Expected escalation detection (true/false)
- Expected escalation rate (rapid/gradual/sudden/none)
- Expected intervention points
- Model expectations for validation

### Test Coverage Targets

| Component | Target | Test Types |
|-----------|--------|------------|
| EscalationDetector | 90%+ | Unit, pattern matching |
| TemporalDetector | 85%+ | Unit, time-based |
| TrendAnalyzer | 85%+ | Unit, statistical |
| ContextAnalyzer | 90%+ | Integration |
| API endpoints | 100% | Integration |

### Test Categories

1. **Unit Tests**: Individual component logic
2. **Pattern Validation**: All 20 escalation patterns from dataset
3. **Edge Cases**: Empty history, single message, very long history
4. **Boundary Conditions**: Threshold boundaries, time zone handling
5. **Integration**: Full flow through API with context

---

## Success Criteria

### Functional Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Escalation detection accuracy | 85%+ | Against escalation_patterns.json |
| False positive rate | < 15% | Non-escalating patterns correctly identified |
| Rapid escalation detection | 100% | All rapid patterns in dataset |
| Gradual escalation detection | 85%+ | Gradual patterns in dataset |
| API backward compatibility | 100% | Existing requests work unchanged |

### Performance Criteria

| Criterion | Target | Notes |
|-----------|--------|-------|
| Context analysis latency | < 100ms | Additional overhead only |
| Full request with context | < 500ms | Total response time |
| Memory overhead | < 50MB | Per request with 20 messages |

### Quality Criteria

| Criterion | Target |
|-----------|--------|
| Test coverage | 85%+ |
| Clean Architecture compliance | 100% |
| Documentation complete | 100% |
| No new linting errors | 0 |

---

## Dependencies

### Internal Dependencies

| Dependency | Required For | Status |
|------------|--------------|--------|
| EnsembleDecisionEngine | Scoring history messages | ✅ Available |
| ConfigManager | Loading context_config.json | ✅ Available |
| AlertingManager | Discord escalation alerts | ✅ Available |
| LoggingConfigManager | Consistent logging | ✅ Available |

### External Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pydantic | >=2.0.0 | Schema validation |
| fastapi | >=0.104.0 | API endpoints |
| python-dateutil | >=2.8.0 | Timestamp parsing |

### No New Infrastructure

Phase 5 does **NOT** require:
- Redis
- Database
- Additional Docker containers
- External APIs

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Performance degradation with large history | Medium | Medium | Limit history to 20 messages, cache scores |
| Time zone handling complexity | Low | Medium | Use UTC internally, convert at API boundary |
| Pattern matching false positives | Medium | High | Conservative thresholds, confidence scoring |

### Integration Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Ash-Bot API contract changes | Low | High | Document API schema clearly, version endpoints |
| Backward compatibility breaks | Low | Critical | Extensive integration testing, optional flags |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Alert fatigue from escalation detection | Medium | Medium | Configurable alert thresholds, cooldowns |
| Missing critical escalations | Low | Critical | Conservative detection, human review flags |

---

## Timeline Estimate

| Week | Focus | Deliverables |
|------|-------|--------------|
| Week 1 | Core Components | 5.1, 5.2, 5.6 |
| Week 2 | Detection & Analysis | 5.3, 5.4 |
| Week 3 | API & Testing | 5.5, 5.7, 5.8 |

**Estimated Duration**: 2-3 weeks

---

## Notes

### Decisions Confirmed

- [x] Ash-NLP remains stateless (confirmed)
- [x] Ash-Bot handles persistence (confirmed)
- [x] Performance testing via Ash-Thrash (confirmed)
- [x] Maximum message history size: **20 messages** (configurable via `NLP_CONTEXT_MAX_HISTORY_SIZE`)
- [x] Alert cooldown for escalation detection: **5 minutes** (configurable via `NLP_ESCALATION_ALERT_COOLDOWN_SECONDS`)

### Future Considerations

- Pattern learning from confirmed crises (v6.0+)
- User-specific baseline adjustment (v6.0+)
- Cross-channel pattern detection (v6.0+)

---

**Built with care for chosen family** 🏳️‍🌈
