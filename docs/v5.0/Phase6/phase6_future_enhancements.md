# Phase 6: Identified Future Enhancements

**Document Version**: v6.0-0.1  
**Created**: 2025-01-02  
**Status**: Planning  
**Project**: Ash-NLP v5.0+  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [Website](https://alphabetcartel.org)

---

## Overview

This document tracks identified future enhancements discovered during Phase 5 development and integration testing. These items are deferred to maintain Phase 5 stability while documenting improvements for future development cycles.

---

## Enhancement Categories

### 🕐 Timezone & Temporal Awareness

#### FE-001: User Timezone Support for Late Night Detection

**Priority**: High  
**Complexity**: Medium  
**Identified During**: Phase 5 Integration Testing

**Current Behavior**:
- Late night detection (22:00-04:00) uses UTC timestamps
- Server timezone (`TZ=America/Los_Angeles`) affects logs but not detection logic
- Users in different timezones may have inaccurate late night risk flags

**Proposed Enhancement**:
1. **Ash-Bot Integration**: Fetch user timezone from Discord API when available
   - Discord User object includes `locale` field
   - Guild-specific settings may include timezone preferences
2. **API Schema Update**: Add optional `user_timezone` parameter
   ```python
   user_timezone: Optional[str] = Field(
       default=None,
       description="User's timezone (IANA format)",
       examples=["America/Los_Angeles", "America/New_York", "Europe/London"],
   )
   ```
3. **TemporalDetector Update**: Convert timestamps to user's local time
4. **Fallback Chain**: User timezone → Server timezone → UTC

**Files to Modify**:
- `src/api/schemas.py` - Add user_timezone field
- `src/context/temporal_detector.py` - Timezone-aware calculations
- `src/context/context_analyzer.py` - Pass timezone through pipeline
- `config/context_analysis.json` - Default timezone configuration

**Discord API Reference**:
- [User Object](https://discord.com/developers/docs/resources/user#user-object)
- [Guild Member Object](https://discord.com/developers/docs/resources/guild#guild-member-object)

---

### 📏 Input Validation & Limits

#### FE-002: Discord Message Length Validation

**Priority**: High  
**Complexity**: Low  
**Identified During**: Phase 5 Integration Testing

**Current Behavior**:
- No validation on message length
- Very long messages (>512 tokens) cause model inference errors
- Discord has 2000 character limit for channel messages

**Proposed Enhancement**:
1. **Add validation** for maximum message length (2000 characters)
2. **Graceful handling** for messages exceeding model token limits
3. **Truncation strategy** with indicator for truncated analysis

**Implementation**:
```python
# In schemas.py
message: str = Field(
    ...,
    min_length=1,
    max_length=2000,
    description="Message text (Discord limit: 2000 chars)",
)
```

**Files to Modify**:
- `src/api/schemas.py` - Add max_length validation
- `src/models/base.py` - Add truncation handling for model input

---

### 🔧 Model & Performance

#### FE-003: Token Truncation for Long Inputs

**Priority**: Medium  
**Complexity**: Medium  
**Identified During**: Phase 5 Integration Testing

**Current Behavior**:
- Models fail with tensor size mismatch for inputs >512 tokens
- Error: `The expanded size of the tensor (2002) must match the existing size (514)`

**Proposed Enhancement**:
1. **Pre-inference truncation** to model's max token limit
2. **Configurable truncation strategy** (head, tail, or middle)
3. **Warning flag** in response when truncation occurs

**Files to Modify**:
- `src/models/base.py` - Add truncation logic
- `src/api/schemas.py` - Add `was_truncated` response field

---

#### FE-004: Model Warm-up on Container Start

**Priority**: Low  
**Complexity**: Low  
**Identified During**: Phase 5 Integration Testing

**Current Behavior**:
- First request to each model triggers lazy loading
- Initial requests have higher latency

**Proposed Enhancement**:
1. **Warm-up endpoint** or startup hook
2. **Pre-load models** during container initialization
3. **Health check** that verifies models are loaded

---

### 📊 Context Analysis Improvements

#### FE-005: Configurable Escalation Thresholds per Severity

**Priority**: Medium  
**Complexity**: Medium  
**Identified During**: Phase 5 Integration Testing

**Current Behavior**:
- Single set of escalation thresholds for all cases
- Some edge cases don't trigger escalation as expected

**Proposed Enhancement**:
1. **Tiered thresholds** based on current crisis score
2. **More sensitive detection** for already-elevated users
3. **Configurable via context_analysis.json**

---

#### FE-006: Historical Pattern Learning

**Priority**: Low  
**Complexity**: High  
**Identified During**: Phase 5 Design Review

**Proposed Enhancement**:
1. **Track user-specific patterns** over time
2. **Learn individual baselines** for crisis scores
3. **Personalized escalation detection**

**Note**: Requires persistent storage and privacy considerations.

---

### 🔔 Alerting & Notifications

#### FE-008: Enhanced Ensemble Conflict Webhook Alerts

**Priority**: Medium  
**Complexity**: Low  
**Identified During**: Phase 5 Production Review

**Current Behavior**:
- Discord webhook fires for "Ensemble Conflict: Score Agreement"
- Alert contains minimal information
- Difficult to investigate or understand the conflict

**Proposed Enhancement**:
Include detailed information in the webhook alert:

1. **Message Content**: The message that triggered the conflict
2. **Model Scores**: Individual scores from each model in the ensemble
3. **Score Differences**: Delta between highest and lowest model scores
4. **Labels/Classifications**: What each model classified the message as

**Example Webhook Payload**:
```json
{
  "embeds": [{
    "title": "⚠️ Ensemble Conflict: Score Agreement",
    "color": 16744448,
    "fields": [
      {
        "name": "Message",
        "value": "I don't know what to do anymore...",
        "inline": false
      },
      {
        "name": "BART (Primary)",
        "value": "Label: emotional distress\nScore: 0.82",
        "inline": true
      },
      {
        "name": "Sentiment",
        "value": "Label: negative\nScore: 0.91",
        "inline": true
      },
      {
        "name": "Irony",
        "value": "Label: not_ironic\nScore: 0.95",
        "inline": true
      },
      {
        "name": "Emotions",
        "value": "Label: sadness\nScore: 0.78",
        "inline": true
      },
      {
        "name": "Score Range",
        "value": "Δ 0.17 (0.78 - 0.95)",
        "inline": true
      },
      {
        "name": "Final Score",
        "value": "0.65 (weighted)",
        "inline": true
      }
    ],
    "timestamp": "2025-01-02T02:45:00.000Z"
  }]
}
```

**Files to Modify**:
- `src/ensemble/decision_engine.py` - Capture conflict details
- `src/notifications/webhook.py` (or equivalent) - Format enhanced payload
- `config/webhooks.json` - Add verbosity configuration option

**Privacy Consideration**:
- Consider truncating long messages
- May want configurable redaction for sensitive content

---

#### FE-009: Suppress Webhooks During Test Execution

**Priority**: Medium  
**Complexity**: Low  
**Identified During**: Phase 5 Integration Testing

**Current Behavior**:
- Each test run triggers "Ash-NLP Started" webhook messages
- Running 47+ tests floods the Discord alert channel
- No distinction between test and production environments

**Proposed Enhancement**:
1. **Environment Detection**: Check for `TESTING=true` or `PYTEST_CURRENT_TEST` env var
2. **Webhook Suppression**: Disable startup/status webhooks during tests
3. **Configuration Option**: Add `webhooks.enabled_in_tests: false` to config

**Implementation Options**:

```python
# Option A: Environment variable check
import os

def should_send_webhook() -> bool:
    """Check if webhooks should fire."""
    if os.getenv("TESTING", "").lower() == "true":
        return False
    if os.getenv("PYTEST_CURRENT_TEST"):
        return False
    return True
```

```python
# Option B: Config-based
# In config/webhooks.json
{
    "enabled": true,
    "suppress_in_tests": true,
    "startup_notification": true,
    ...
}
```

```python
# Option C: pytest fixture (conftest.py)
@pytest.fixture(autouse=True)
def suppress_webhooks(monkeypatch):
    """Disable webhooks during all tests."""
    monkeypatch.setenv("WEBHOOKS_ENABLED", "false")
```

**Files to Modify**:
- `src/notifications/webhook.py` - Add suppression check
- `config/webhooks.json` - Add `suppress_in_tests` option
- `tests/conftest.py` - Add autouse fixture for test suppression
- `docker-compose.test.yml` - Set `TESTING=true` environment

---

### 🐛 Known Integration Issues

#### FE-007: Message History Not Reaching Context Analyzer

**Priority**: High  
**Complexity**: Medium  
**Identified During**: Phase 5 Integration Testing

**Observed Behavior**:
- API receives `message_history` in request
- Context analysis returns `message_count: 0`
- History data not being passed through engine to context analyzer

**Expected Behavior**:
- `message_count` should equal `len(message_history)` provided in request
- Context analyzer should receive and process all history items

**Investigation Areas**:
1. `src/api/routes.py` - How message_history is extracted from request
2. `src/ensemble/decision_engine.py` - How history is passed to context analyzer
3. `src/context/context_analyzer.py` - How history is received and counted

**Workaround**: Context analysis still runs, but without historical pattern detection.

---

## Implementation Priority Matrix

| ID | Enhancement | Priority | Complexity | Dependencies |
|----|-------------|----------|------------|--------------|
| FE-007 | History Passthrough Bug | High | Medium | None (Bug Fix) |
| FE-001 | User Timezone Support | High | Medium | Ash-Bot changes |
| FE-002 | Message Length Validation | High | Low | None |
| FE-008 | Enhanced Conflict Alerts | Medium | Low | None |
| FE-009 | Suppress Test Webhooks | Medium | Low | None |
| FE-003 | Token Truncation | Medium | Medium | None |
| FE-004 | Model Warm-up | Low | Low | None |
| FE-005 | Escalation Thresholds | Medium | Medium | Testing |
| FE-006 | Pattern Learning | Low | High | Database |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v6.0-0.1 | 2025-01-02 | Claude/Bubba | Initial document creation |

---

**Built with care for chosen family** 🏳️‍🌈
