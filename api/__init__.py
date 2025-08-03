"""
API Package for Ash NLP Service v3.1
Contains FastAPI endpoint definitions for the NLP server
This is the NEW directory structure (moved from endpoints)
"""

# Make this directory a Python package
__version__ = "3.1.0"

# Import key components for easier access
try:
    from .ensemble_endpoints import add_ensemble_endpoints
    __all__ = ['add_ensemble_endpoints']
except ImportError:
    # If ensemble endpoints can't be imported, just make it an empty package
    __all__ = []

try:
    from .enhanced_learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    __all__.extend(['EnhancedLearningManager', 'add_enhanced_learning_endpoints'])
except ImportError:
    # Learning endpoints are optional
    pass

# Package metadata
__author__ = "The Alphabet Cartel"
__description__ = "API endpoints for Ash NLP Service with clean manager architecture"