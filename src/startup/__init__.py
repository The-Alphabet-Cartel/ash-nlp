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
Startup Module for Ash-NLP Service
---
FILE VERSION: v5.0-7-1.0-1
LAST MODIFIED: 2025-01-02
PHASE: Phase 7 Step 1.0 - Runtime Model Initialization
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

DESCRIPTION:
    This module provides startup utilities for Ash-NLP, including
    runtime model initialization that downloads and caches models
    at container startup rather than build time.

COMPONENTS:
    - model_initializer: Downloads/verifies HuggingFace models at startup
"""

from src.startup.model_initializer import (
    ModelInitializer,
    create_model_initializer,
    initialize_models_sync,
)

__version__ = "v5.0-7-1.0-1"

__all__ = [
    "ModelInitializer",
    "create_model_initializer",
    "initialize_models_sync",
]
