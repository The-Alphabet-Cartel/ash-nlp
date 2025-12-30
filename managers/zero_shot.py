# ash-nlp/managers/zero_shot_manager.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis
3. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Zero-Shot Manager for Ash NLP Service
---
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ZeroShotManager:
    """
    Manager for zero-shot classification labels and mappings for Ash NLP Service
    """

    def __init__(self, unified_config_manager):
        """
        Initialize zero-shot manager with UnifiedConfigManager

        Args:
                unified_config_manager: UnifiedConfigManager instance (required)
        """
        if unified_config_manager is None:
            raise ValueError("UnifiedConfigManager is required for ZeroShotManager")

        self.unified_config = unified_config_manager

        logger.info("ZeroShotManager v5.0 initialized")


# ============================================================================
# FACTORY FUNCTION - Clean Architecture Compliance
# ============================================================================
def create_zero_shot_manager(unified_config_manager) -> ZeroShotManager:
    """
    Factory function for ZeroShotManager (Clean v3.1 Pattern) - Phase 3e Enhanced

    Args:
            unified_config_manager: UnifiedConfigManager instance (required)

    Returns:
            ZeroShotManager instance with Phase 3e enhancements
    """

    return ZeroShotManager(unified_config_manager)


# ============================================================================
# Export public interface
# ============================================================================
__all__ = ["ZeroShotManager", "create_zero_shot_manager"]

logger.info("ZeroShotManager v5.0 loaded")
