# Ash-NLP Changelog

All notable changes to Ash-NLP will be documented in this file.

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | https://alphabetcartel.org

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

- `POST /api/v1/analyze` - Single message analysis
- `POST /api/v1/analyze/batch` - Batch processing (up to 10 messages)
- `GET /api/v1/health` - Health check with model status
- `GET /api/v1/models` - Loaded models information
- Interactive documentation at `/docs` (Swagger) and `/redoc`

### Performance (Phase 3.7)

- **Model Warmup** (3.7.1): Consistent latency from first request
- **Async Parallel Inference** (3.7.2): All models run concurrently with `asyncio.gather()`
- **Response Caching** (3.7.4): LRU cache with TTL for repeated messages
- Inference time: ~185-200ms per message
- GPU memory usage: ~3.3GB (single worker)

### Error Handling (Phase 3.5)

- **Retry with Exponential Backoff**: Configurable retry logic
- **Timeout Handling**: Per-model inference timeouts
- **Circuit Breaker**: CLOSED/OPEN/HALF_OPEN states for model failures
- **Discord Alerting**: Webhook notifications for critical failures

### Monitoring (Phase 3.6)

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
- `docs/utilities.md` - Utilities reference
- `docs/api.md` - API documentation
- `docs/configuration.md` - Configuration reference
- `secrets/README.md` - Secrets setup guide

---

## [4.x] - Previous Versions

Prior versions used a single-model architecture. See git history for details.

---

## Future Work

### Phase 3.7 (Deferred)

- [ ] 3.7.3 Request batching optimization
- [ ] 3.7.5 Comprehensive benchmarking and profiling
- [ ] 3.7.6 Memory usage optimization

### Phase 4 (Planned)

- Integration with Ash Discord bot
- Historical trend analysis
- User-specific sensitivity tuning
- Multi-language support

---

**Built with care for chosen family** 🏳️‍🌈
