# ash/ash-nlp/main.py - Clean v3.1 Architecture with Phase 3a Crisis Pattern Manager
"""
Enhanced Mental Health Crisis Detection API
Clean v3.1 Architecture - Phase 3a Complete with CrisisPatternManager

CRITICAL UPDATE: Three Zero-Shot Model Ensemble Integration with Crisis Pattern Manager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import sys
import logging
import time
import os
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ============================================================================
# LOGGING SETUP
# ============================================================================
## Set up logging FIRST to catch any import errors
## !!!Leave this block alone during development!!!
log_level = os.getenv('GLOBAL_LOG_LEVEL', 'INFO').upper()
log_file = os.getenv('NLP_LOG_FILE', 'nlp_service.log')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s %(levelname)s: %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("🚀 Starting Ash NLP Service v3.1 - Clean Architecture (Phase 2C Complete)")

# ============================================================================
# CLEAN V3.1 IMPORTS - Phase 3a Updated with CrisisPatternManager
# ============================================================================

# Core Manager Imports - DIRECT ONLY (NO FALLBACKS)
try:
    logger.info("📋 Importing Core Managers v3.1...")
    from managers.config_manager import ConfigManager
    from managers.settings_manager import SettingsManager
    from managers.zero_shot_manager import ZeroShotManager
    CORE_MANAGERS_AVAILABLE = True
    logger.info("✅ Core managers imported successfully")
except ImportError as e:
    CORE_MANAGERS_AVAILABLE = False
    logger.error(f"❌ Core manager imports failed: {e}")
    logger.error("💡 Ensure core managers are properly installed in managers/")
    sys.exit(1)

# Import ModelsManager v3.1 - DIRECT IMPORT ONLY (No Fallback)
try:
    logger.info("🤖 Importing ModelsManager v3.1...")
    from managers.models_manager import ModelsManager
    MODELS_MANAGER_AVAILABLE = True
    logger.info("✅ ModelsManager v3.1 imported from managers/")
except ImportError as e:
    MODELS_MANAGER_AVAILABLE = False
    logger.error(f"❌ ModelsManager v3.1 import failed: {e}")
    logger.error("💡 Ensure ModelsManager is properly installed in managers/models_manager.py")
    sys.exit(1)

# Import PydanticManager v3.1 - DIRECT IMPORT ONLY (No Fallback)
try:
    logger.info("📋 Importing PydanticManager v3.1...")
    from managers.pydantic_manager import PydanticManager, create_pydantic_manager
    PYDANTIC_MANAGER_AVAILABLE = True
    logger.info("✅ PydanticManager v3.1 imported from managers/")
except ImportError as e:
    PYDANTIC_MANAGER_AVAILABLE = False
    logger.error(f"❌ PydanticManager v3.1 import failed: {e}")
    logger.error("💡 Ensure PydanticManager is properly installed in managers/pydantic_manager.py")
    sys.exit(1)

# Import CrisisPatternManager v3.1 - Phase 3a Integration
try:
    logger.info("🔍 Importing CrisisPatternManager v3.1...")
    from managers.crisis_pattern_manager import CrisisPatternManager, create_crisis_pattern_manager
    CRISIS_PATTERN_MANAGER_AVAILABLE = True
    logger.info("✅ CrisisPatternManager v3.1 imported from managers/ (Phase 3a)")
except ImportError as e:
    CRISIS_PATTERN_MANAGER_AVAILABLE = False
    logger.error(f"❌ CrisisPatternManager v3.1 import failed: {e}")
    logger.error("💡 Ensure CrisisPatternManager is properly installed in managers/crisis_pattern_manager.py")
    sys.exit(1)

# Import Analysis Components (Optional)
try:
    logger.info("🔍 Importing CrisisAnalyzer...")
    from analysis.crisis_analyzer import CrisisAnalyzer
    CRISIS_ANALYZER_AVAILABLE = True
    logger.info("✅ CrisisAnalyzer import successful")
except ImportError as e:
    CRISIS_ANALYZER_AVAILABLE = False
    logger.warning(f"⚠️ CrisisAnalyzer import failed: {e}")

# Import Learning System (Optional)
try:
    logger.info("🧠 Importing Learning System...")
    from api.learning_endpoints import EnhancedLearningManager, add_enhanced_learning_endpoints
    LEARNING_AVAILABLE = True
    logger.info("✅ Learning system import successful")
except ImportError as e:
    LEARNING_AVAILABLE = False
    logger.warning(f"⚠️ Learning system import failed: {e}")

# ============================================================================
# GLOBAL MANAGER INSTANCES - Phase 3a Updated
# ============================================================================

# Core managers
config_manager = None
settings_manager = None
zero_shot_manager = None
crisis_pattern_manager = None  # Phase 3a addition

# ML and analysis managers
model_manager = None
pydantic_manager = None
crisis_analyzer = None
learning_manager = None

# ============================================================================
# CLEAN MODEL ACCESS - Direct Manager Usage Only
# ============================================================================

def get_pydantic_models():
    """
    Get Pydantic models from PydanticManager v3.1 - NO FALLBACKS
    """
    if pydantic_manager and pydantic_manager.is_initialized():
        logger.debug("🏗️ Using PydanticManager v3.1 for model access")
        return pydantic_manager.get_core_models()
    else:
        logger.error("❌ PydanticManager v3.1 not available or not initialized")
        raise RuntimeError(
            "Clean v3.1: PydanticManager not available. "
            "Ensure PydanticManager is properly initialized."
        )

# ============================================================================
# CENTRALIZED ENVIRONMENT VALIDATION - Clean v3.1
# ============================================================================

def validate_centralized_thresholds():
    """Validate and display centralized threshold configuration - Clean v3.1"""
    
    # Define environment variables for centralized configuration
    centralized_env_vars = {
        # Ensemble mode and gap detection thresholds
        'NLP_ENSEMBLE_MODE': {'default': 'consensus', 'type': str},
        'NLP_GAP_DETECTION_THRESHOLD': {'default': 0.4, 'type': float},
        'NLP_DISAGREEMENT_THRESHOLD': {'default': 0.5, 'type': float},
        
        # Model weights for weighted ensemble mode
        'NLP_DEPRESSION_MODEL_WEIGHT': {'default': 0.5, 'type': float},
        'NLP_SENTIMENT_MODEL_WEIGHT': {'default': 0.2, 'type': float},
        'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT': {'default': 0.3, 'type': float},
        
        # Ensemble decision thresholds
        'NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD': {'default': 0.60, 'type': float},
        'NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD': {'default': 0.35, 'type': float},
        'NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD': {'default': 0.20, 'type': float},
        
        # Crisis level mapping thresholds  
        'NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD': {'default': 0.85, 'type': float},
        'NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD': {'default': 0.65, 'type': float},
        'NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD': {'default': 0.45, 'type': float}
    }
    
    thresholds = {}
    
    for var_name, config in centralized_env_vars.items():
        raw_value = os.getenv(var_name, config['default'])
        
        try:
            if config['type'] == float:
                thresholds[var_name.lower()] = float(raw_value)
            elif config['type'] == str:
                thresholds[var_name.lower()] = str(raw_value)
            else:
                thresholds[var_name.lower()] = raw_value
        except ValueError:
            logger.warning(f"⚠️ Invalid value for {var_name}: {raw_value}, using default: {config['default']}")
            thresholds[var_name.lower()] = config['default']
    
    logger.debug("🎯 CENTRALIZED Ensemble Configuration:")
    logger.debug(f"   Ensemble Mode: {thresholds['nlp_ensemble_mode']}")
    logger.debug(f"   Gap Detection Threshold: {thresholds['nlp_gap_detection_threshold']}")
    logger.debug(f"   Disagreement Threshold: {thresholds['nlp_disagreement_threshold']}")
    logger.debug("   Ensemble Thresholds:")
    logger.debug(f"     HIGH: {thresholds['nlp_ensemble_high_crisis_threshold']}")
    logger.debug(f"     MEDIUM: {thresholds['nlp_ensemble_medium_crisis_threshold']}")
    logger.debug(f"     LOW: {thresholds['nlp_ensemble_low_crisis_threshold']}")
    logger.debug("   Crisis Level Mapping Thresholds:")
    logger.debug(f"     CRISIS → HIGH: {thresholds['nlp_consensus_crisis_to_high_threshold']}")
    logger.debug(f"     CRISIS → MEDIUM: {thresholds['nlp_consensus_crisis_to_medium_threshold']}")
    logger.debug(f"     MILD_CRISIS → LOW: {thresholds['nlp_consensus_mild_crisis_to_low_threshold']}")
    logger.debug("   Model Weights:")
    logger.debug(f"     Depression: {thresholds['nlp_depression_model_weight']}")
    logger.debug(f"     Sentiment: {thresholds['nlp_sentiment_model_weight']}")
    logger.debug(f"     Emotional Distress: {thresholds['nlp_emotional_distress_model_weight']}")
    
    logger.debug("🎯 CENTRALIZED Ensemble endpoints configured - All thresholds from environment variables")
    
    return thresholds

# ============================================================================
# CLEAN INITIALIZATION - Phase 3a Updated with CrisisPatternManager
# ============================================================================

async def initialize_components_clean_v3_1():
    """Initialize all components with clean v3.1 architecture - Phase 3a Complete"""
    global config_manager, settings_manager, zero_shot_manager, crisis_pattern_manager
    global model_manager, pydantic_manager, crisis_analyzer, learning_manager
    
    try:
        logger.info("🚀 Initializing components with clean v3.1 architecture - Phase 3a Complete...")
        
        # ========================================================================
        # STEP 1: Initialize Core Configuration Managers - DIRECT ONLY
        # ========================================================================
        logger.info("📋 Initializing core configuration managers...")
        
        config_manager = ConfigManager("/app/config")
        settings_manager = SettingsManager(config_manager)
        zero_shot_manager = ZeroShotManager(config_manager)
        
        logger.info("✅ Core configuration managers initialized (ConfigManager, SettingsManager, ZeroShotManager)")
        
        # ========================================================================
        # STEP 2: Initialize CrisisPatternManager - Phase 3a
        # ========================================================================
        logger.info("🔍 Initializing CrisisPatternManager v3.1 (Phase 3a)...")
        
        if CRISIS_PATTERN_MANAGER_AVAILABLE:
            try:
                crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
                logger.info("✅ CrisisPatternManager v3.1 initialized with JSON configuration")
            except Exception as e:
                logger.error(f"❌ CrisisPatternManager initialization failed: {e}")
                crisis_pattern_manager = None
        else:
            logger.warning("⚠️ CrisisPatternManager not available - pattern analysis will be limited")
            crisis_pattern_manager = None
        
        # ========================================================================
        # STEP 3: Initialize PydanticManager v3.1 - DIRECT ONLY
        # ========================================================================
        logger.info("📋 Initializing PydanticManager v3.1...")
        
        if PYDANTIC_MANAGER_AVAILABLE:
            try:
                pydantic_manager = create_pydantic_manager()
                logger.info("✅ PydanticManager v3.1 initialized")
            except Exception as e:
                logger.error(f"❌ PydanticManager initialization failed: {e}")
                pydantic_manager = None
        else:
            logger.error("❌ PydanticManager not available")
            pydantic_manager = None
            
        # ========================================================================
        # STEP 4: Initialize ModelsManager v3.1 - DIRECT ONLY
        # ========================================================================
        logger.info("🤖 Initializing ModelsManager v3.1...")
        
        if MODELS_MANAGER_AVAILABLE:
            try:
                model_manager = ModelsManager(config_manager)
                logger.info("✅ ModelsManager v3.1 initialized")
            except Exception as e:
                logger.error(f"❌ ModelsManager initialization failed: {e}")
                model_manager = None
        else:
            logger.error("❌ ModelsManager not available")
            model_manager = None
            
        # ========================================================================
        # STEP 5: Initialize Learning Manager - Optional
        # ========================================================================
        logger.info("🧠 Initializing Enhanced Learning Manager...")
        
        if LEARNING_AVAILABLE and model_manager:
            try:
                learning_manager = EnhancedLearningManager(model_manager, config_manager)
                logger.info("✅ Enhanced Learning Manager initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize Learning Manager: {e}")
                learning_manager = None
        else:
            logger.info("ℹ️ Learning system not available")
            learning_manager = None
            
        # ========================================================================
        # STEP 6: Initialize CrisisAnalyzer - Optional 
        # ========================================================================
        logger.info("🔍 Initializing CrisisAnalyzer...")
        
        if CRISIS_ANALYZER_AVAILABLE and model_manager:
            try:
                crisis_analyzer = CrisisAnalyzer(
                    model_manager=model_manager
                )
                logger.info("✅ CrisisAnalyzer initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CrisisAnalyzer: {e}")
                crisis_analyzer = None
        else:
            logger.info("ℹ️ CrisisAnalyzer not available")
            crisis_analyzer = None
        
        # ========================================================================
        # STEP 7: Final Status Report - Clean v3.1 Phase 3a
        # ========================================================================
        logger.debug("📊 Component Initialization Summary (Clean v3.1 Phase 3a):")
        
        components_status = {
            'core_managers': {
                'config_manager': config_manager is not None,
                'settings_manager': settings_manager is not None,
                'zero_shot_manager': zero_shot_manager is not None,
                'crisis_pattern_manager_v3_1': crisis_pattern_manager is not None,  # Phase 3a
                'pydantic_manager_v3_1': pydantic_manager is not None
            },
            'ml_components': {
                'models_manager_v3_1': model_manager is not None,
                'three_model_ensemble': model_manager and model_manager.models_loaded() if model_manager else False
            },
            'analysis_components': {
                'crisis_analyzer_with_patterns': crisis_analyzer is not None,  # Phase 3a enhanced
                'learning_manager': learning_manager is not None
            }
        }
        
        for category, components in components_status.items():
            logger.debug(f"   {category.replace('_', ' ').title()}:")
            for component, status in components.items():
                status_icon = "✅" if status else "❌"
                logger.debug(f"     {component}: {status_icon}")
        
        # Check for critical failures
        critical_failures = []
        if not model_manager:
            critical_failures.append("ModelsManager v3.1")
        if model_manager and not model_manager.models_loaded():
            critical_failures.append("Model Loading")
        if not pydantic_manager:
            critical_failures.append("PydanticManager v3.1")
        
        if critical_failures:
            logger.error(f"❌ Critical component failures: {critical_failures}")
            raise RuntimeError(f"Critical v3.1 components failed: {critical_failures}")
        
        logger.info("✅ All critical components initialized successfully - Clean v3.1 Architecture")
        logger.info("🎉 Phase 3a Complete - CrisisPatternManager integrated with JSON configuration")
        
        # Report Pattern Manager Status
        if crisis_pattern_manager:
            logger.info("🔍 Crisis Pattern Manager Status: Operational with JSON patterns")
        else:
            logger.warning("⚠️ Crisis Pattern Manager: Not available - pattern analysis limited")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize v3.1 components: {e}")
        logger.exception("Full initialization error:")
        raise

# ============================================================================
# Health Response Model
# ============================================================================
class HealthResponse(BaseModel):
    status: str
    uptime: float
    model_loaded: bool
    components_available: dict
    configuration_status: dict
    manager_status: dict
    architecture_version: str
    phase_2c_status: str
    phase_3a_status: str  # Phase 3a addition

# ============================================================================
# FastAPI Application Setup - Clean v3.1 Phase 3a
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager - Clean v3.1 Architecture Phase 3a"""
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting - Clean v3.1 Architecture (Phase 3a Complete)...")
    
    try:
        await initialize_components_clean_v3_1()
        
        # Import and add ensemble endpoints - CLEAN v3.1 + Phase 3a
        try:
            logger.info("🎯 Adding Three Zero-Shot Model Ensemble endpoints - Clean v3.1...")
            from api.ensemble_endpoints import add_ensemble_endpoints
            
            # Pass crisis_pattern_manager for Pattern Integration (Phase 3a)
            add_ensemble_endpoints(
                app, 
                model_manager=model_manager, 
                pydantic_manager=pydantic_manager,
                crisis_pattern_manager=crisis_pattern_manager
            )
            logger.info("🚀 Ensemble endpoints added - Clean v3.1 + Pattern Integration!")
            
        except Exception as e:
            logger.error(f"❌ Could not add ensemble endpoints: {e}")
            raise

        # Import and add admin endpoints - CLEAN v3.1
        try:
            logger.info("🔧 Adding admin endpoints - Clean v3.1...")
            from api.admin_endpoints import add_admin_endpoints
            
            # Direct manager usage with all managers
            add_admin_endpoints(
                app, 
                config_manager=config_manager,
                settings_manager=settings_manager,
                zero_shot_manager=zero_shot_manager,
                crisis_pattern_manager=crisis_pattern_manager,
                model_manager=model_manager
            )
            logger.info("🎯 Admin endpoints added - Clean v3.1!")
            
        except Exception as e:
            logger.error(f"❌ Could not add admin endpoints: {e}")
            raise
        
        # Import and add learning endpoints - CLEAN v3.1
        if LEARNING_AVAILABLE and learning_manager:
            try:
                logger.info("🧠 Adding enhanced learning endpoints - Clean v3.1...")
                add_enhanced_learning_endpoints(
                    app, 
                    learning_manager=learning_manager
                )
                logger.info("🎓 Enhanced learning endpoints added - Clean v3.1!")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not add learning endpoints: {e}")
        
        logger.info("🎉 FastAPI app startup complete - All v3.1 Phase 3a components operational!")
        
    except Exception as e:
        logger.error(f"❌ FastAPI app startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🔄 FastAPI app shutting down...")

# Initialize FastAPI app with clean v3.1 architecture
app = FastAPI(
    title="Ash NLP Service v3.1 - Phase 3a Complete",
    description="Enhanced Mental Health Crisis Detection with CrisisPatternManager",
    version="3.1.0",
    lifespan=lifespan
)

# Track startup time
startup_time = time.time()

# ============================================================================
# Enhanced Health Check - Phase 3a Updated
# ============================================================================
@app.get("/health", response_model=HealthResponse)
async def enhanced_health_check():
    """Enhanced health check with Phase 3a CrisisPatternManager status"""
    
    uptime = time.time() - startup_time
    model_loaded = model_manager is not None and model_manager.models_loaded()
    
    components_available = {
        "config_manager": config_manager is not None,
        "settings_manager": settings_manager is not None,
        "zero_shot_manager": zero_shot_manager is not None,
        "crisis_pattern_manager": crisis_pattern_manager is not None,  # Phase 3a
        "models_manager_v3_1": model_manager is not None,
        "pydantic_manager_v3_1": pydantic_manager is not None,
        "crisis_analyzer": crisis_analyzer is not None,
        "learning_manager": learning_manager is not None
    }
    
    configuration_status = {
        "json_config_loaded": config_manager is not None,
        "settings_validated": settings_manager is not None,
        "crisis_patterns_loaded": crisis_pattern_manager is not None,  # Phase 3a
        "zero_shot_labels_loaded": zero_shot_manager is not None,
        "pydantic_models_available": pydantic_manager is not None and pydantic_manager.is_initialized()
    }
    
    manager_status = {
        "models_manager_operational": model_manager is not None and model_manager.models_loaded(),
        "ensemble_analysis_available": model_manager is not None and hasattr(model_manager, 'analyze_with_ensemble'),
        "crisis_pattern_analysis_available": crisis_pattern_manager is not None,  # Phase 3a
        "learning_system_operational": learning_manager is not None
    }
    
    overall_status = "healthy" if all([
        config_manager is not None,
        settings_manager is not None, 
        model_manager is not None and model_manager.models_loaded(),
        pydantic_manager is not None and pydantic_manager.is_initialized()
    ]) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        uptime=uptime,
        model_loaded=model_loaded,
        components_available=components_available,
        configuration_status=configuration_status,
        manager_status=manager_status,
        architecture_version="v3.1_clean_phase_3a_complete",
        phase_2c_status="complete",
        phase_3a_status="complete" if crisis_pattern_manager is not None else "pattern_manager_unavailable"
    )

# ============================================================================
# PRODUCTION READY - Clean v3.1 Architecture Phase 3a Complete
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Ash NLP Service v3.1 - Phase 3a Complete")
    logger.info("🔧 Clean Architecture: Direct manager access only")
    logger.info("🔍 Crisis Pattern Manager: JSON configuration with ENV overrides")
    logger.info("🎯 Three Zero-Shot Model Ensemble: Enhanced with pattern analysis")
    
    # Validate configuration before starting
    validate_centralized_thresholds()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8881,
        log_level="info"
    )