<!-- ash-nlp/README.md -->
<!--
README Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: v5.0 Compliant
-->
# Ash-NLP v5.0 - Crisis Detection Service

**Mental health crisis detection**

[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da)](https://discord.gg/alphabetcartel)
[![Website](https://img.shields.io/badge/Website-alphabetcartel.org-blue)](https://alphabetcartel.org)
[![GitHub](https://img.shields.io/badge/Version-v3.1-green)](https://github.com/the-alphabet-cartel/ash-nlp)

---

## What is Ash-NLP v5.0?

**Ash-NLP v5.0** is a mental health crisis detection service engineered for The Alphabet Cartel LGBTQIA+ Discord community. Built with Clean Architecture v5.0 principles, it provides intelligent mental health crisis detection with adaptive learning capabilities.

### Core System Vision
1. **FIRST**: Uses Zero-Shot AI models for primary semantic classification
2. **SECOND**: Enhances AI results with contextual pattern analysis
3. **PURPOSE**: Detect crisis messages in Discord community communications

---

## Key Features

### Advanced Crisis Detection
- **Multi-model ensemble** with intelligent consensus algorithms
- **Zero-shot classification** for semantic understanding beyond keywords
- **Pattern-based fallback** ensuring continuous operation

### System Architecture
- **Clean Architecture v5.0 compliant** with 100% validated compliance
- **Specialized managers** with factory function patterns
- **Dependency injection** throughout system architecture
- **Comprehensive error handling** with graceful degradation
- **Docker-first deployment** with production-ready configuration

---

## Architecture Overview

### Manager System
Ash-NLP v5.0 uses a clean architecture with specialized managers:

- **UnifiedConfigManager** - Configuration foundation
- **SharedUtilitiesManager** - Common utilities
- **ModelCoordinationManager** - AI model ensemble management
- **CrisisAnalyzer** - Primary analysis coordination
- **PatternDetectionManager** - Crisis pattern recognition
- **ContextAnalysisManager** - Community context understanding

### Dependencies
```
UnifiedConfigManager (Foundation)
├── SharedUtilitiesManager (Universal utilities)
├── ModelCoordinationManager (AI models)
├── CrisisAnalyzer (Analysis coordination)
└── All other specialized managers
```

### Data Flow
```
Discord Message → API → CrisisAnalyzer → AI Models → Pattern Analysis → Context Analysis → Response
```

---

## Integration with Ash Ecosystem

Ash-NLP v5.0 integrates with The Alphabet Cartel ecosystem:

- **[Ash Bot](https://github.com/the-alphabet-cartel/ash-bot)** - Discord crisis response bot
- **[The Alphabet Cartel](https://github.com/the-alphabet-cartel)** - Community organization

---

## Development

### Project Structure
```
ash-nlp/
├── .env                        # Environment Variables
├── analysis/                   # Crisis analysis components
|   └── crisis_analysis.py      # Crisis Analysis Module
├── api/                        # FastAPI endpoints
|   ├── admin_endpoints.py      # Admin endpoints
|   └── user_endpoints.py       # User endpoints
├── backups/                    # Backup management
|   ├── daily                   # Daily backups
|   ├── monthly                 # Monthly backups
|   ├── weekly                  # Weekly backups
|   └── yearly                  # Yearly backups
├── cache/                      # Cache management
|   └── models/                 # Models Cache
|       └── offload/            # Offloaded models
├── config/                     # Configuration files
|   ├── analysis_config.json    # Analysis Configuration
|   ├── feature_flags.json      # Feature Flags Configuration
|   ├── logging_config.json     # Logging Configuration
|   ├── model_config.json       # Model Configuration
|   ├── patterns_config.json    # Patterns Configuration
|   ├── performance_config.json # Performance Configuration
|   ├── server_config.json      # Server Configuration
|   ├── settings_config.json    # Settings Configuration
|   ├── storage_config.json     # Storage Configuration
|   ├── threshold_config.json   # Crisis Threshold Configuration
|   └── zero_shot.json          # Zero Shot Label Configuration
├── data/                       # Data management
|   ├── analysis                # Analysis data
|   ├── learning                # Learning data (Future)
|   └── patterns                # Patterns data
├── docker-compose.yml          # Docker Configuration
├── docs/                       # Documentation
├── logs/                       # Logs management
├── main.py                     # Application entry point
└── managers/                   # Core managers
|   ├── context_analysis.py     # Context Analysis Manager
|   ├── feature_flags.py        # Feature Flags Manager
|   ├── logging_manager.py      # Logging Manager
|   ├── model_manager.py        # Model Manager
|   ├── patterns_manager.py     # Patterns Manager
|   ├── performance_manager.py  # Performance Manager
|   ├── server_config.py        # Server Configuration Manager
|   ├── settings_config.py      # Settings Configuration Manager
|   ├── shared_utilities.py     # Shared Utilities Manager
|   ├── storage_config.py       # Storage Configuration Manager
|   ├── threshold_manager.py    # Threshold Manager
|   ├── unified_config.py       # Unified Configuration Manager
|   └── zero_shot.py            # Zero-Shot Manager
└── tests/                      # Testing Suites
    ├── fixtures                # Fixtures for testing
    ├── integrations            # Integration tests
    ├── performance             # Performance tests
    └── unit                    # Unit tests
```

### Code Quality
- **Clean Architecture v5.0** with 100% compliance validation
- **Factory function patterns** for all managers
- **Comprehensive error handling** with graceful degradation
- **Type hints** throughout codebase
- **Docker-first** development and deployment

---

## Security & Privacy

### Data Protection
- **No persistent storage** - Messages analyzed in-memory only
- **Docker secrets** for sensitive configuration
- **Environment variable validation** preventing exposure
- **Audit logging** for security monitoring

### API Security
- **Rate limiting** preventing abuse
- **Input validation** with comprehensive sanitization
- **Error handling** preventing information disclosure

---

## Community Impact

**Serving The Alphabet Cartel LGBTQIA+ Discord Community**

### Mental Health Focus
- **Crisis pattern recognition** specific to LGBTQIA+ experiences
- **Community-aware language** understanding chosen family dynamics
- **Adaptive learning** from community feedback patterns
- **Immediate response capability** for mental health emergencies

### Technology for Good
- **Open source** for transparency and community improvement
- **Privacy-first** design with no data persistence
- **Community-driven** development with user feedback integration
- **Accessible deployment** with Docker-based setup

---

## Documentation

### Complete Documentation Suite
- **[API Guide](docs/api/api_guide.md)** - Complete API reference and integration guide
- **[Team Guide](docs/team/team_guide.md)** - Crisis response team operational guide
- **[Technical Guide](docs/tech/technical_guide.md)** - Architecture and development guide
- **[Manager Documentation](docs/tech/managers/)** - Individual manager specifications

---

## Contributing

We welcome contributions to enhance crisis detection capabilities for LGBTQIA+ communities:

1. **Fork the repository** and create a feature branch
2. **Follow Clean Architecture v5.0** principles in all code changes
3. **Add comprehensive tests** for new functionality
4. **Update documentation** to reflect changes
5. **Submit pull request** with detailed description

### Development Environment
```bash
# Set up development environment
git clone https://github.com/the-alphabet-cartel/ash-nlp.git
cd ash-nlp
cp .env.template .env
docker-compose -f docker-compose.yml up --build
```

---

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

**Open source for community mental health support.**

---

## Community

**The Alphabet Cartel** - Building technology for LGBTQIA+ communities

### Core Values
- **Safety First** - Every design decision prioritizes user wellbeing
- **Community-Driven** - Built with and for the communities we serve  
- **Transparency** - Open source, auditable, and improvable by all
- **Chosen Family** - Technology supporting found family connections

### Connect With Us
- **Discord**: [Join our community](https://discord.gg/alphabetcartel)
- **Website**: [alphabetcartel.org](https://alphabetcartel.org)
- **GitHub**: [github.com/the-alphabet-cartel](https://github.com/the-alphabet-cartel)

---

*Ash-NLP v5.0: Engineered for community mental health support, one conversation at a time.*

**Built with care for chosen family** 🏳️‍🌈
