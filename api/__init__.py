# ash-nlp/api/__init__.py
"""
API Package for Ash NLP Service v3.1
FILE VERSION: v3.1-3e-4.2-1
LAST MODIFIED: 2025-08-13
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

# Make this directory a Python package
__author__ = "The Alphabet Cartel"
__description__ = "API endpoints for Ash NLP Service with clean manager architecture"

# Import key components for easier access
__all__ = []

try:
    from .admin_endpoints import add_admin_endpoints
    __all__.append('add_admin_endpoints')
    ADMIN_ENDPOINTS_AVAILABLE = True
except ImportError:
    ADMIN_ENDPOINTS_AVAILABLE = False

try:
    from .ensemble_endpoints import add_ensemble_endpoints
    __all__.append('add_ensemble_endpoints')
    ENSEMBLE_ENDPOINTS_AVAILABLE = True
except ImportError:
    ENSEMBLE_ENDPOINTS_AVAILABLE = False

# Package status
def get_package_status():
    """Get the status of available components"""
    return {
        'description': __description__,
        'admin_endpoints': ADMIN_ENDPOINTS_AVAILABLE,
        'ensemble_endpoints': ENSEMBLE_ENDPOINTS_AVAILABLE,
        'architecture': "clean_manager_v3.1"
    }