# Ash-NLP Changelog

All notable changes to Ash-NLP will be documented in this file.

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | https://alphabetcartel.org

---

## [5.0.5] - 2026-01-02

### 🎉 Phase 5 Complete - Context History Analysis

Context-aware crisis detection with escalation patterns, temporal analysis, and trend tracking.

### Context Analysis Features

- **Escalation Detection**: Identifies rapid, gradual, and sudden escalation patterns
  - Configurable thresholds (rapid: 4hr, gradual: 24hr)
  - Pattern matching against known escalation signatures
  - Intervention point identification
  - Confidence scoring for detected patterns

- **Temporal Pattern Detection**: Time-based risk factors
  - Late night detection (10 PM - 4 AM) with 1.2x risk modifier
  - Rapid posting detection (5+ messages in 30 minutes)
  - Weekend detection with 1.1x risk modifier
  - Combined risk modifier stacking

- **Trend Analysis**: Score trajectory tracking
  - Direction classification (worsening, stable, improving, volatile)
  - Velocity calculation (rapid, moderate, gradual, none)
  - Score smoothing with 3-point moving average
  - Inflection point detection

- **Intervention Urgency**: Smart urgency calculation
  - Levels: none, low, standard, high, immediate
  - Boosted by escalation detection
  - Boosted by late night activity
  - Combined factor consideration

### API Enhancements

- **Message History Input**: `/analyze` endpoint accepts `message_history` array
  - Each item: `message`, `timestamp`, `crisis_score` (optional), `message_id` (optional)
  - Up to 20 messages in history (configurable)
  
- **Context Analysis Response**: New `context_analysis` section in responses
  - `escalation`: detected, rate, confidence, pattern_name
  - `trend`: direction, velocity, score metrics
  - `temporal`: late_night_risk, rapid_posting, is_weekend, time_risk_modifier
  - `intervention`: urgency, recommended_point
  - `trajectory`: scores, start_score, end_score, peak_score
  - `history_metadata`: message_count, time_span_hours

- **Configuration Endpoints**:
  - `GET /config/context` - Get context analysis configuration
  - `PUT /config/context` - Update context analysis configuration

### Discord Alerting

- **Escalation Alerts**: New `ESCALATION` severity level (dark red, 📈 emoji)
- **Async/Sync Methods**: `send_escalation_alert()` and `send_escalation_alert_sync()`
- **Cooldown Tracking**: Separate escalation cooldown (300s default)
- **Urgency-Based Severity**: immediate→CRITICAL, high→ESCALATION, standard→WARNING, low→INFO

### Configuration

- New `config/context_config.json` for context analysis settings
- `ContextConfigManager` with typed dataclasses
- Environment variable overrides for all context settings

### Testing

- **Unit Tests** (`tests/phase5/`):
  - `test_escalation_detector.py` - 11 test classes, 35+ methods
  - `test_temporal_detector.py` - 10 test classes, 30+ methods
  - `test_trend_analyzer.py` - 10 test classes, 30+ methods
  - `test_context_analyzer.py` - 10 test classes, 25+ methods
  - `test_alerting_escalation.py` - 7 test classes, 20+ methods

- **Integration Tests** (`tests/integration/`):
  - `test_engine_context_integration.py` - ContextAnalyzer integration
  - `test_api_context_flow.py` - Full API request/response flow

---

## [5.0.4] - 2026-01-01

### Phase 4 Complete - Ensemble Coordinator Enhancement

Advanced consensus algorithms, conflict detection, and explainability features.

### Consensus Algorithms

- **Weighted Voting** (default): Model weights determine influence
- **Majority Voting**: Democratic model agreement
- **Unanimous**: All models must agree for crisis detection
- **Conflict-Aware**: Detects and resolves model disagreements

### Conflict Detection

- **Score Disagreement**: Models differ significantly on crisis score
- **Irony-Sentiment Conflict**: Ironic positive with negative sentiment
- **Emotion-Crisis Mismatch**: Emotional signals don't match crisis score
- **Label Disagreement**: Models disagree on classification

### Conflict Resolution

- **Conservative**: Favor higher crisis scores (safety-first)
- **Optimistic**: Favor lower crisis scores
- **Mean**: Average conflicting scores
- **Review Flag**: Flag for human review

### Explainability

- **Verbosity Levels**: minimal, standard, detailed
- **Human-Readable Explanations**: Why crisis was/wasn't detected
- **Contributing Factors**: Which models influenced the decision
- **Agreement Analysis**: Model consensus metrics

### API Enhancements

- `consensus_algorithm` parameter in `/analyze` requests
- `include_explanation` flag for human-readable explanations
- `verbosity` parameter for explanation detail level
- `GET /config/consensus` - Get consensus configuration
- `PUT /config/consensus` - Update consensus configuration

---

## [5.0.0] - 2026-01-01

### 🎉 Major Release - Multi-Model Ensemble Architecture

This release represents a complete architectural evolution from single-model to Local Multi-Model Ensemble architecture.

### Architecture

- **Multi-Model Ensemble**: Four specialized models with weighted decision engine
  - BART Zero-Shot Classification (0.50 weight) - Primary crisis detection
  - Cardiff Sentiment Analysis (0.25 weight) - Emotional context
  - Cardiff Irony Detection (0.15 weight) - Sarcasm filtering
  - RoBERTa Emotions Classification (0.10 weight) - Fine-grained emotions
- **Weighted Scoring**: Configurable model weights with signal boosting
- **Fallback Strategy**: Circuit breaker pattern for graceful degradation

### API

- `POST /analyze` - Single message analysis
- `POST /analyze/batch` - Batch processing (up to 10 messages)
- `GET /health` - Health check with model status
- `GET /status` - Detailed service status
- `GET /models` - Loaded models information
- Interactive documentation at `/docs` (Swagger) and `/redoc`

### Performance

- **Model Warmup**: Consistent latency from first request
- **Async Parallel Inference**: All models run concurrently with `asyncio.gather()`
- **Response Caching**: LRU cache with TTL for repeated messages
- Inference time: ~185-200ms per message
- GPU memory usage: ~3.3GB (single worker)

### Error Handling

- **Retry with Exponential Backoff**: Configurable retry logic
- **Timeout Handling**: Per-model inference timeouts
- **Circuit Breaker**: CLOSED/OPEN/HALF_OPEN states for model failures
- **Discord Alerting**: Webhook notifications for critical failures

### Monitoring

- **Structured JSON Logging**: ELK/Loki compatible log format
- **Request Tracing**: X-Request-ID header propagation
- **Prometheus Metrics**: Optional `/metrics` endpoint
- **Discord Alerts**: System startup, model failures, recovery notifications

### Security

- Docker Secrets integration for sensitive credentials
- Non-root container user (UID 1001)
- Rate limiting middleware
- CORS configuration

### Configuration

- Environment-based configuration with JSON defaults
- Support for development, testing, and production environments
- All settings overridable via environment variables

### Documentation

- `DEPLOYMENT.md` - Production deployment guide
- `docs/v5.0/roadmap.md` - Development roadmap
- `docs/v5.0/Phase4/` - Phase 4 documentation
- `docs/v5.0/Phase5/` - Phase 5 documentation
- `docs/clean_architecture_charter.md` - Architecture guidelines

---

## [4.x] - Previous Versions

Prior versions used a single-model architecture. See git history for details.

---

## Project Completion Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Foundation & Planning | ✅ Complete |
| Phase 1 | Testing Framework | ✅ Complete |
| Phase 2 | Model Migration | ✅ Complete |
| Phase 3 | API & Docker Deployment | ✅ Complete |
| Phase 4 | Ensemble Coordinator Enhancement | ✅ Complete |
| Phase 5 | Context History Analysis | ✅ Complete |

**All phases complete!** 🎉

---

**Built with care for chosen family** 🏳️‍🌈
