"""
============================================================================
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Monitor  → Receive messages from Ash-Bot for crisis classification
    Analyze  → Run multi-model ensemble for comprehensive assessment
    Detect   → Identify crisis signals through weighted decision engine
    Respond  → Return actionable crisis assessments to protect our community

============================================================================
Clients Module - External Service Integration
----------------------------------------------------------------------------
FILE VERSION: v5.0-3-1.0-1
LAST MODIFIED: 2026-01-27
PHASE: Phase 3 - Ash-Vigil Integration
CLEAN ARCHITECTURE: v5.2.3 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
============================================================================

This module contains HTTP clients for external service integration.

Current Clients:
- VigilClient: Ash-Vigil mental health risk detection service
"""

from src.clients.vigil_client import (
    # Enums
    VigilStatus,
    
    # Data classes
    VigilResult,
    
    # Classes
    CircuitBreaker,
    VigilClient,
    
    # Factory functions
    create_vigil_client,
    create_circuit_breaker,
)

__all__ = [
    # Enums
    "VigilStatus",
    
    # Data classes
    "VigilResult",
    
    # Classes
    "CircuitBreaker",
    "VigilClient",
    
    # Factory functions
    "create_vigil_client",
    "create_circuit_breaker",
]

__version__ = "v5.0-3-1.0-1"
