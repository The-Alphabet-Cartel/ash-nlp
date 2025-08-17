# ash-nlp/api/__init__.py
"""
API Package for Ash NLP Service v3.1
FILE VERSION: v3.1-3d-10-1
LAST MODIFIED: 2025-08-13
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

# Make this directory a Python package
__version__ = "3.1.0"
__author__ = "The Alphabet Cartel"
__description__ = "API endpoints for Ash NLP Service with clean manager architecture"

# Import key components for easier access
__all__ = []

try:
    from .ensemble_endpoints import add_ensemble_endpoints
    __all__.append('add_ensemble_endpoints')
    ENSEMBLE_ENDPOINTS_AVAILABLE = True
except ImportError:
    ENSEMBLE_ENDPOINTS_AVAILABLE = False
    # Try fallback to old location
    try:
        from ..endpoints.ensemble_endpoints import add_ensemble_endpoints
        __all__.append('add_ensemble_endpoints')
        ENSEMBLE_ENDPOINTS_AVAILABLE = True
    except ImportError:
        pass

try:
    # FIXED: Import from learning_endpoints (not enhanced_learning_endpoints)
    from .learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    __all__.extend(['EnhancedLearningManager', 'add_enhanced_learning_endpoints'])
    LEARNING_ENDPOINTS_AVAILABLE = True
except ImportError:
    LEARNING_ENDPOINTS_AVAILABLE = False

# Package status
def get_package_status():
    """Get the status of available components"""
    return {
        'ensemble_endpoints': ENSEMBLE_ENDPOINTS_AVAILABLE,
        'learning_endpoints': LEARNING_ENDPOINTS_AVAILABLE,
        'version': __version__,
        'architecture': 'clean_manager_v3.1'
    }