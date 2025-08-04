# ash/ash-nlp/models/__init__.py (Clean v3.1 Architecture - Phase 2C Complete)
"""
Models directory - for model storage and caching only

This directory contains only data storage and model caching - no Python code.
All model management code has been migrated to managers/ directory:

- ML Models: managers/models_manager.py (Phase 2A Complete)
- Pydantic Models: managers/pydantic_manager.py (Phase 2B Complete)

Directory structure:
    models/
    ├── __init__.py          # This file - storage directory marker
    └── cache/               # Hugging Face model cache storage
        └── [model files]    # Cached model files and tokenizers

Phase 2C Status: Complete - All backward compatibility removed
"""

# Phase 2C: No exports, no imports, no code - storage directory only
__version__ = "3.1.0"
__status__ = "Phase 2C Complete - Storage Only"
__description__ = "Model storage and caching directory - Code migrated to managers/"