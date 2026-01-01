"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Managers Package for Ash-NLP Service
---
FILE VERSION: v5.0-5-1.0-1
LAST MODIFIED: 2026-01-01
PHASE: Phase 5 - Context History Analysis
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This package contains resource managers for Ash-NLP:

MANAGERS:
- ConfigManager: Configuration loading and validation
- ContextConfigManager: Phase 5 context analysis configuration (NEW)
- SecretsManager: Secure secrets management

USAGE:
    from src.managers import create_config_manager, create_context_config_manager

    config = create_config_manager(environment="production")
    context_config = create_context_config_manager()
    
    api_config = config.get_api_config()
    escalation_config = context_config.get_escalation_detection_config()
"""

# Module version
__version__ = "v5.0-5-1.0-1"

# =============================================================================
# Configuration Manager
# =============================================================================

from .config_manager import (
    ConfigManager,
    create_config_manager,
)

# =============================================================================
# Context Configuration Manager (Phase 5)
# =============================================================================

from .context_config_manager import (
    ContextConfigManager,
    create_context_config_manager,
    # Config dataclasses
    ContextAnalysisConfig,
    EscalationDetectionConfig,
    TemporalDetectionConfig,
    TrendAnalysisConfig,
    InterventionConfig,
    KnownPattern,
)

# =============================================================================
# Secrets Manager
# =============================================================================

from .secrets_manager import (
    SecretsManager,
    create_secrets_manager,
    get_secrets_manager,
    get_secret,
    SecretNotFoundError,
    KNOWN_SECRETS,
)

# =============================================================================
# Public API
# =============================================================================

__all__ = [
    "__version__",
    # Config
    "ConfigManager",
    "create_config_manager",
    # Context Config (Phase 5)
    "ContextConfigManager",
    "create_context_config_manager",
    "ContextAnalysisConfig",
    "EscalationDetectionConfig",
    "TemporalDetectionConfig",
    "TrendAnalysisConfig",
    "InterventionConfig",
    "KnownPattern",
    # Secrets
    "SecretsManager",
    "create_secrets_manager",
    "get_secrets_manager",
    "get_secret",
    "SecretNotFoundError",
    "KNOWN_SECRETS",
]
