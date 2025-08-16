# ash-nlp/main.py
"""
Ash-NLP Main Application Entry Point for Ash NLP Service
FILE VERSION: v3.1-3d-10.11-3-1
LAST MODIFIED: 2025-08-15
PHASE: 3d Step 10.11-3 - Models Manager Consolidation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

STEP 10.11-3 CHANGE: Removed models_manager initialization and imports.
All model functionality now handled by model_ensemble_manager.
"""

import os
import sys
import logging
import colorlog
import time
from pathlib import Path
from fastapi import FastAPI
import uvicorn

# ============================================================================
# STEP 9: UNIFIED CONFIGURATION MANAGER IMPORT
# ============================================================================
from managers.unified_config_manager import create_unified_config_manager

# ============================================================================
# MANAGER IMPORTS - ALL USING FACTORY FUNCTIONS (CLEAN V3.1)
# STEP 10.11-3: Updated imports for Models Manager consolidation
# ============================================================================
from managers.analysis_parameters_manager import create_analysis_parameters_manager
from managers.crisis_pattern_manager import create_crisis_pattern_manager
from managers.feature_config_manager import create_feature_config_manager
from managers.logging_config_manager import create_logging_config_manager
from managers.model_ensemble_manager import create_model_ensemble_manager
# STEP 10.11-3: models_manager import REMOVED - functionality consolidated
# from managers.models_manager import create_models_manager  # REMOVED
from managers.performance_config_manager import create_performance_config_manager
from managers.pydantic_manager import create_pydantic_manager
from managers.server_config_manager import create_server_config_manager
from managers.settings_manager import create_settings_manager
from managers.storage_config_manager import create_storage_config_manager
from managers.threshold_mapping_manager import create_threshold_mapping_manager
from managers.zero_shot_manager import create_zero_shot_manager
from managers.context_pattern_manager import create_context_pattern_manager

# Analysis Components
from analysis import create_crisis_analyzer

# API Endpoint Registration - FIXED IMPORTS
from api.ensemble_endpoints import add_ensemble_endpoints_v3c  # FIXED: Use correct function name
from api.learning_endpoints import register_learning_endpoints
from api.admin_endpoints import add_admin_endpoints  # FIXED: Use correct function name

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management - Step 10.11-3 Updated"""
    global unified_config, model_ensemble_manager, pydantic_manager
    global crisis_pattern_manager, threshold_mapping_manager
    
    logger.info("🚀 Starting Ash NLP Service with Step 10.11-3 Models Manager Consolidation...")
    
    try:
        # ====================================================================
        # STEP 1: Initialize Unified Configuration Manager
        # ====================================================================
        logger.info("🔧 Initializing unified configuration manager...")
        from managers import create_unified_config_manager
        unified_config = create_unified_config_manager("/app/config")
        logger.info("✅ Unified configuration manager initialized")
        
        # ====================================================================
        # STEP 2: Initialize Model Ensemble Manager (PRIMARY MODEL MANAGER)
        # ====================================================================
        logger.info("🔧 Initializing model ensemble manager...")
        from managers import create_model_ensemble_manager
        model_ensemble_manager = create_model_ensemble_manager(unified_config)
        logger.info("✅ Model ensemble manager initialized")
        
        # STEP 10.11-3: models_manager initialization REMOVED
        # logger.info("🔧 Initializing models manager...")  # REMOVED
        # from managers import create_models_manager           # REMOVED
        # models_manager = create_models_manager(unified_config)  # REMOVED
        # logger.info("✅ Models manager initialized")        # REMOVED
        
        # ====================================================================
        # STEP 3: Initialize Pydantic Manager
        # ====================================================================
        logger.info("🔧 Initializing pydantic manager...")
        from managers import create_pydantic_manager
        pydantic_manager = create_pydantic_manager(unified_config)
        logger.info("✅ Pydantic manager initialized")
        
        # ====================================================================
        # STEP 4: Initialize Optional Managers
        # ====================================================================
        
        # Crisis Pattern Manager
        try:
            logger.info("🔧 Initializing crisis pattern manager...")
            from managers import create_crisis_pattern_manager
            crisis_pattern_manager = create_crisis_pattern_manager(unified_config)
            logger.info("✅ Crisis pattern manager initialized")
        except Exception as e:
            logger.warning(f"⚠️ Crisis pattern manager initialization failed: {e}")
            crisis_pattern_manager = None
        
        # Threshold Mapping Manager
        try:
            logger.info("🔧 Initializing threshold mapping manager...")
            from managers import create_threshold_mapping_manager
            threshold_mapping_manager = create_threshold_mapping_manager(unified_config, model_ensemble_manager)
            logger.info("✅ Threshold mapping manager initialized")
        except Exception as e:
            logger.warning(f"⚠️ Threshold mapping manager initialization failed: {e}")
            threshold_mapping_manager = None
        
        # ====================================================================
        # STEP 5: Setup API Endpoints
        # ====================================================================
        logger.info("🔧 Setting up API endpoints...")
        
        # Import endpoint setup functions
        from api.ensemble_endpoints import add_ensemble_endpoints_v3c
        from api.admin_endpoints import add_admin_endpoints
        from api.learning_endpoints import add_learning_endpoints
        
        # STEP 10.11-3: Pass model_ensemble_manager instead of models_manager
        add_ensemble_endpoints_v3c(
            app, 
            model_ensemble_manager,  # UPDATED: Single consolidated manager
            pydantic_manager,
            crisis_pattern_manager,
            threshold_mapping_manager
        )
        
        add_admin_endpoints(
            app,
            unified_config,
            crisis_pattern_manager,
            threshold_mapping_manager
        )
        
        add_learning_endpoints(
            app,
            unified_config,
            pydantic_manager
        )
        
        logger.info("✅ API endpoints configured")
        
        # ====================================================================
        # STEP 6: Validate System Health
        # ====================================================================
        logger.info("🔍 Validating system health...")
        
        # Check model ensemble manager status
        if model_ensemble_manager and model_ensemble_manager.models_loaded():
            logger.info("✅ Model ensemble manager: Models loaded and ready")
        else:
            logger.warning("⚠️ Model ensemble manager: Models not fully loaded")
        
        # STEP 10.11-3: models_manager health check REMOVED
        # if models_manager and models_manager.models_loaded():  # REMOVED
        #     logger.info("✅ Models manager: Models loaded and ready")  # REMOVED
        # else:  # REMOVED
        #     logger.warning("⚠️ Models manager: Models not fully loaded")  # REMOVED
        
        # Check pydantic manager status
        if pydantic_manager and pydantic_manager.is_initialized():
            logger.info("✅ Pydantic manager: Initialized and ready")
        else:
            logger.warning("⚠️ Pydantic manager: Not properly initialized")
        
        logger.info("🎯 Step 10.11-3 Consolidation: Using ModelEnsembleManager as primary model manager")
        logger.info("🚀 Ash NLP Service startup complete - Ready to serve requests!")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise
    
    finally:
        # Cleanup
        logger.info("🔄 Shutting down Ash NLP Service...")
        logger.info("✅ Shutdown complete")

# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Ash NLP Service",
    description="LGBTQIA+ Crisis Detection and Mental Health Analysis Service",
    version="3.1-3d-10.11-3",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with Step 10.11-3 consolidation info"""
    return {
        "service": "Ash NLP Service",
        "version": "3.1-3d-10.11-3",
        "phase": "3d",
        "step": "10.11-3",
        "consolidation": "Models Manager → ModelEnsembleManager",
        "status": "operational",
        "model_manager": "ModelEnsembleManager",
        "endpoints": {
            "analysis": "/analyze",
            "health": "/health", 
            "configuration": "/ensemble/config",
            "status": "/ensemble/status"
        },
        "community": "The Alphabet Cartel",
        "repository": "https://github.com/the-alphabet-cartel/ash-nlp"
    }

# ============================================================================
# DEVELOPMENT SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🔧 Starting development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8881,
        reload=True,
        log_level="info"
    )