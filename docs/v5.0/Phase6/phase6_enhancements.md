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

## Implementation Priority Matrix

| ID | Enhancement | Priority | Complexity | Dependencies |
|----|-------------|----------|------------|--------------|
| FE-001 | User Timezone Support | High | Medium | Ash-Bot changes |
| FE-002 | Message Length Validation | High | Low | None |
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
