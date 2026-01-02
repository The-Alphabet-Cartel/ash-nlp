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
Ash-NLP Source Package
---
FILE VERSION: v5.0-3-4.5-4
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 - Production Integration
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

This is the main source package for Ash-NLP containing:
- managers: Configuration and resource management
- models: Individual model wrappers for the ensemble
- ensemble: Decision engine and scoring system
- api: FastAPI application and endpoints

USAGE:
    from src.managers import create_config_manager
    from src.models import create_bart_classifier
    from src.ensemble import create_decision_engine
    from src.api import create_app
"""

__version__ = "5.0.0"
__author__ = "The Alphabet Cartel"
__email__ = "dev@alphabetcartel.org"
__url__ = "https://github.com/the-alphabet-cartel/ash-nlp"

# Package metadata
__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__url__",
]
