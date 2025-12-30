"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification

Testing Framework Package
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: v5.0 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

__version__ = "5.0"
__author__ = "The Alphabet Cartel"

# Export main testing components
from .model_evaluator import ModelEvaluator, create_model_evaluator

__all__ = ["ModelEvaluator", "create_model_evaluator"]
