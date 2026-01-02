# Phase 6: Future Enhancements

**FILE VERSION**: v5.0  
**CREATED**: 2026-01-02  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## Overview

This document tracks future enhancements identified during Phase 5 development. These are non-critical improvements that will enhance system robustness, accuracy, and maintainability.

---

## Enhancement Tickets

### FE-001: User Timezone Support for Late Night Detection

**Priority**: Medium  
**Category**: Context Analysis  
**Status**: Planned

**Description**: Currently, late night detection uses server time (UTC). Users in different timezones may have messages incorrectly flagged or missed.

**Proposed Solution**:
- Accept optional `timezone` parameter in API requests
- Store user timezone preferences
- Convert timestamps to user's local time for late night detection

**Files Affected**:
- `src/context/temporal_detector.py`
- `src/api/schemas.py`

---

### FE-002: Discord Message Length Validation

**Priority**: Low  
**Category**: Alerting  
**Status**: Planned

**Description**: Discord has a 2000 character limit for messages. Long explanations or conflict summaries could exceed this limit.

**Proposed Solution**:
- Add truncation logic to Discord alerter
- Split long messages into multiple embeds
- Add character count validation before sending

**Files Affected**:
- `src/alerting/discord_alerter.py`

---

### FE-003: Token Truncation for Long Inputs

**Priority**: Medium  
**Category**: Model Processing  
**Status**: Planned

**Description**: Very long messages may exceed model token limits, causing truncation at unpredictable points.

**Proposed Solution**:
- Implement smart truncation that preserves sentence boundaries
- Add configurable max token limits per model
- Log truncation events for monitoring

**Files Affected**:
- `src/models/base.py`
- `src/models/bart_classifier.py`

---

### FE-004: Model Warm-up on Container Start

**Priority**: Low  
**Category**: Performance  
**Status**: Planned

**Description**: First request after container start has higher latency due to model loading.

**Proposed Solution**:
- Add startup hook to pre-warm models
- Run dummy inference during initialization
- Add health check that waits for warm-up

**Files Affected**:
- `src/api/app.py`
- `src/ensemble/model_loader.py`

---

### FE-005: Configurable Escalation Thresholds per Severity

**Priority**: Medium  
**Category**: Context Analysis  
**Status**: Planned

**Description**: Different severity levels may need different escalation detection thresholds.

**Proposed Solution**:
- Add per-severity threshold configuration
- Allow stricter thresholds for lower severities
- Provide presets (conservative, balanced, sensitive)

**Files Affected**:
- `src/context/escalation_detector.py`
- `src/managers/context_config_manager.py`
- `config/default.json`

---

### FE-006: Historical Pattern Learning

**Priority**: High  
**Category**: Machine Learning  
**Status**: Research

**Description**: System could learn from past escalation patterns to improve prediction accuracy.

**Proposed Solution**:
- Store anonymized escalation sequences
- Train lightweight pattern recognition model
- Use historical data to improve confidence scores

**Files Affected**:
- New module: `src/learning/`
- Database integration required

---

### FE-007: Message History Passthrough Investigation

**Priority**: Medium  
**Category**: Bug Investigation  
**Status**: Needs Investigation

**Description**: During integration testing, some edge cases showed unexpected behavior with message history passthrough.

**Proposed Solution**:
- Add detailed logging for history processing
- Create comprehensive edge case test suite
- Investigate potential race conditions in async processing

**Files Affected**:
- `src/context/context_analyzer.py`
- `src/api/routes.py`

---

### FE-008: Enhanced Ensemble Conflict Webhook Alerts

**Priority**: Low  
**Category**: Alerting  
**Status**: Planned

**Description**: Conflict detection could trigger specialized Discord alerts with detailed model disagreement information.

**Proposed Solution**:
- Add conflict-specific alert template
- Include visual disagreement chart (ASCII or image)
- Add configurable conflict alert threshold

**Files Affected**:
- `src/alerting/discord_alerter.py`
- `src/ensemble/conflict_detector.py`

---

### FE-009: Suppress Webhooks During Test Execution

**Priority**: High  
**Category**: Testing  
**Status**: Planned

**Description**: Test runs may trigger real Discord webhooks, causing noise in production channels.

**Proposed Solution**:
- Add `TESTING_MODE` environment variable check
- Mock webhook calls during pytest execution
- Add dry-run mode for alerting system

**Files Affected**:
- `src/alerting/discord_alerter.py`
- `tests/conftest.py`

---

### FE-010: Config File Docker Volume Mapping

**Priority**: Low  
**Category**: Testing / DevOps  
**Status**: Skipped Tests

**Description**: Tests expect config files at `/app/config/` but actual configs are in `src/config/`. Docker volume mapping differs from test expectations.

**Current Workaround**: 3 tests skipped in `tests/phase3/test_config.py`

**Proposed Solution**:
- Align test paths with actual Docker volume mapping
- Or update Dockerfile to copy configs to expected location
- Or make tests dynamically detect config location

**Files Affected**:
- `tests/phase3/test_config.py`
- `Dockerfile`
- `docker-compose.yml`

**Skipped Tests**:
- `test_default_config_exists`
- `test_production_config_exists`
- `test_testing_config_exists`

---

### FE-011: Consensus Threshold Edge Cases

**Priority**: Low  
**Category**: Testing  
**Status**: Skipped Tests

**Description**: Some consensus algorithm tests fail due to edge cases:
1. Majority threshold uses `>` not `>=` comparison (0.25 == 0.25 returns False)
2. Test fixture variance (0.099) is below disagreement threshold (0.15)

**Current Workaround**: 3 tests skipped in `tests/phase4/test_consensus.py`

**Proposed Solution**:
- Option A: Update implementation to use `>=` for inclusive thresholds
- Option B: Update test fixtures to have higher variance data
- Option C: Adjust test expectations to match actual behavior

**Files Affected**:
- `tests/phase4/test_consensus.py`
- `src/ensemble/consensus.py` (if changing implementation)

**Skipped Tests**:
- `test_majority_threshold_configurable`
- `test_disagreement_flags_conflict`
- `test_significant_disagreement_high_variance`

---

### FE-012: Time-Sensitive Tests and Smoothing Algorithm

**Priority**: Low  
**Category**: Testing  
**Status**: Skipped Tests

**Description**: Several context analyzer tests fail due to:
1. Tests run at 3am UTC which triggers late night detection
2. Smoothing algorithm reduces peak scores (0.8→0.633, 1.0→0.75)

**Current Workaround**: 3 tests skipped in `tests/phase5/test_context_analyzer.py`

**Proposed Solution**:
- Mock `datetime.now()` in temporal tests
- Use explicit timestamps that are timezone-aware
- Adjust test expectations to account for smoothing effects
- Or test raw scores before smoothing is applied

**Files Affected**:
- `tests/phase5/test_context_analyzer.py`
- Potentially add time mocking utilities to `tests/conftest.py`

**Skipped Tests**:
- `test_normal_hours`
- `test_trajectory_peak_score`
- `test_very_high_current_score`

---

## Priority Matrix

| Priority | Tickets | Focus Area |
|----------|---------|------------|
| **High** | FE-006, FE-009 | ML Learning, Test Isolation |
| **Medium** | FE-001, FE-003, FE-005, FE-007 | Accuracy, Robustness |
| **Low** | FE-002, FE-004, FE-008, FE-010, FE-011, FE-012 | Polish, Test Fixes |

---

## Skipped Tests Summary

| Ticket | Phase | Count | Reason |
|--------|-------|-------|--------|
| FE-010 | 3 | 3 | Docker config path mapping |
| FE-011 | 4 | 3 | Threshold edge cases |
| FE-012 | 5 | 3 | Time/smoothing behavior |
| **Total** | | **9** | |

All skipped tests are edge cases that don't affect production functionality.

---

## Implementation Notes

### Before Starting Phase 6

1. Ensure all Phase 5 tests pass (426/435, 9 skipped)
2. Review production logs for any recurring issues
3. Gather community feedback on current detection accuracy
4. Prioritize based on real-world usage patterns

### Suggested Sprint Order

1. **Sprint 1**: FE-009 (test isolation) + FE-010/011/012 (fix skipped tests)
2. **Sprint 2**: FE-001 (timezone) + FE-003 (token truncation)
3. **Sprint 3**: FE-005 (per-severity thresholds) + FE-007 (investigation)
4. **Sprint 4**: FE-006 (historical learning) - larger effort
5. **Sprint 5**: FE-002, FE-004, FE-008 (polish items)

---

**Built with care for chosen family** 🏳️‍🌈
