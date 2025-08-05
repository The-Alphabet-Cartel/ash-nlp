# ash/ash-nlp/main.py - Clean v3.1 Architecture with Phase 3a Crisis Pattern Manager
"""
Enhanced Mental Health Crisis Detection API
Clean v3.1 Architecture - Phase 3a Complete with CrisisPatternManager

CRITICAL UPDATE: Three Zero-Shot Model Ensemble Integration with Crisis Pattern Manager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import sys
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
import logging
import colorlog

log_level = os.getenv('GLOBAL_LOG_LEVEL', 'INFO').upper()
log_file = os.getenv('NLP_LOG_FILE', 'nlp_service.log')

# Create formatters
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s - %(message)s')
console_formatter = colorlog.ColoredFormatter(
    '%(blue)s%(asctime)s%(reset)s %(log_color)s%(levelname)s%(reset)s: %(orange)s%(name)s%(reset)s - %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }
)

# Create handlers
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)

# Configure root logger
logging.basicConfig(
    level=getattr(logging, log_level),
    handlers=[file_handler, console_handler]
)

logger = logging.getLogger(__name__)
logger.info("🚀 Starting Ash NLP Service v3.1 - Clean Architecture (Phase 3a Complete)")

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
# CONFIGURATION VALIDATION
# ============================================================================

def validate_centralized_thresholds():
    """Validate centralized threshold configuration from environment variables"""
    required_thresholds = [
        'NLP_ENSEMBLE_MODE',
        'NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD',      # Updated to match .env.template
        'NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD',    # Updated to match .env.template
        'NLP_CONSENSUS_MILD_CRISIS_TO_LOW_THRESHOLD',  # Updated to match .env.template
        'NLP_DEPRESSION_MODEL_WEIGHT',                 # Updated to match .env.template
        'NLP_SENTIMENT_MODEL_WEIGHT',                  # Updated to match .env.template
        'NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT'          # Updated to match .env.template
    ]
    
    thresholds = {}
    missing_vars = []
    
    for var in required_thresholds:
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)
        else:
            try:
                # Convert to appropriate type
                if var in ['NLP_ENSEMBLE_MODE']:
                    thresholds[var.lower().replace('nlp_', '')] = value
                else:
                    thresholds[var.lower().replace('nlp_', '')] = float(value)
            except ValueError:
                logger.error(f"❌ Invalid value for {var}: {value}")
                missing_vars.append(f"{var} (invalid value)")
    
    if missing_vars:
        logger.error("❌ Missing or invalid centralized threshold configuration:")
        for var in missing_vars:
            logger.error(f"   {var}")
        logger.error("💡 These should be defined in your .env file:")
        logger.error(f"   Depression Weight: {thresholds.get('depression_model_weight', 'MISSING')}")
        logger.error(f"   Sentiment Weight: {thresholds.get('sentiment_model_weight', 'MISSING')}")
        logger.error(f"   Emotional Distress Weight: {thresholds.get('emotional_distress_model_weight', 'MISSING')}")
        sys.exit(1)
    
    logger.info("🐳 Running in Docker mode - using system environment variables")
    logger.info("✅ Centralized threshold configuration validation passed")
    
    logger.debug("🎯 Centralized Threshold Configuration:")
    logger.debug(f"   Ensemble mode: {thresholds['ensemble_mode']}")
    logger.debug("   Consensus Mapping Thresholds:")
    logger.debug(f"     CRISIS → HIGH: {thresholds['consensus_crisis_to_high_threshold']}")
    logger.debug(f"     CRISIS → MEDIUM: {thresholds['consensus_crisis_to_medium_threshold']}")
    logger.debug(f"     MILD_CRISIS → LOW: {thresholds['consensus_mild_crisis_to_low_threshold']}")
    logger.debug("   Model Weights:")
    logger.debug(f"     Depression: {thresholds['depression_model_weight']}")
    logger.debug(f"     Sentiment: {thresholds['sentiment_model_weight']}")
    logger.debug(f"     Emotional Distress: {thresholds['emotional_distress_model_weight']}")
    
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
                
                # Validate pattern loading
                pattern_status = crisis_pattern_manager.get_status()
                logger.debug(f"🔍 Pattern Manager Status: {pattern_status['loaded_pattern_sets']} pattern sets loaded")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CrisisPatternManager: {e}")
                crisis_pattern_manager = None
        else:
            logger.warning("⚠️ CrisisPatternManager not available")
            crisis_pattern_manager = None
        
        # ========================================================================
        # STEP 3: Initialize PydanticManager v3.1 - DIRECT ONLY
        # ========================================================================
        logger.info("📋 Initializing PydanticManager v3.1...")
        
        if PYDANTIC_MANAGER_AVAILABLE:
            try:
                pydantic_manager = create_pydantic_manager()
                if pydantic_manager.is_initialized():
                    logger.info("✅ PydanticManager v3.1 initialized successfully")
                else:
                    logger.error("❌ PydanticManager v3.1 failed to initialize")
                    raise RuntimeError("PydanticManager v3.1 initialization failed")
            except Exception as e:
                logger.error(f"❌ PydanticManager v3.1 initialization failed: {e}")
                raise
        else:
            logger.error("❌ PydanticManager v3.1 not available")
            raise RuntimeError("PydanticManager v3.1 required but not available")
        
        # ========================================================================
        # STEP 4: Initialize ModelsManager v3.1 - DIRECT ONLY
        # ========================================================================
        logger.info("🤖 Initializing ModelsManager v3.1...")
        
        if MODELS_MANAGER_AVAILABLE:
            try:
                model_manager = ModelsManager(config_manager, settings_manager, zero_shot_manager)
                await model_manager.initialize()
                
                if model_manager.models_loaded():
                    logger.info("✅ ModelsManager v3.1 initialized with all models loaded")
                else:
                    logger.error("❌ ModelsManager v3.1 failed to load models")
                    raise RuntimeError("ModelsManager v3.1 model loading failed")
            except Exception as e:
                logger.error(f"❌ ModelsManager v3.1 initialization failed: {e}")
                raise
        else:
            logger.error("❌ ModelsManager v3.1 not available")
            raise RuntimeError("ModelsManager v3.1 required but not available")
        
        # ========================================================================
        # STEP 5: Initialize Learning System (Optional)
        # ========================================================================
        if LEARNING_AVAILABLE:
            try:
                # Pass required arguments: model_manager and config_manager
                learning_manager = EnhancedLearningManager(
                    model_manager=model_manager,
                    config_manager=config_manager
                )
                logger.info("✅ Enhanced Learning Manager initialized")
            except Exception as e:
                logger.warning(f"⚠️  Could not initialize Enhanced Learning Manager: {e}")
                learning_manager = None
        else:
            logger.info("ℹ️ Enhanced Learning Manager not available")
            learning_manager = None
        
        # ========================================================================
        # STEP 6: Initialize Analysis Components with Crisis Pattern Manager
        # ========================================================================
        
        # Initialize CrisisAnalyzer with CrisisPatternManager integration
        if CRISIS_ANALYZER_AVAILABLE:
            try:
                crisis_analyzer = CrisisAnalyzer(
                    model_manager=model_manager,
                    crisis_pattern_manager=crisis_pattern_manager,  # Phase 3a integration
                    learning_manager=learning_manager
                )
                logger.info("✅ CrisisAnalyzer initialized with CrisisPatternManager integration")
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