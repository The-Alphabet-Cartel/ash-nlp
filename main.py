# ash/ash-nlp/main.py - Clean v3.1 Architecture with Phase 3a Crisis Pattern Manager
"""
Enhanced Mental Health Crisis Detection API
Clean v3.1 Architecture - Phase 3a Complete with CrisisPatternManager

CRITICAL UPDATE: Three Zero-Shot Model Ensemble Integration with Crisis Pattern Manager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import logging
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
import colorlog

log_level = os.getenv('GLOBAL_LOG_LEVEL', 'INFO').upper()
log_file = os.getenv('NLP_LOG_FILE', 'nlp_service.log')

# Create formatters
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s - %(message)s')
console_formatter = colorlog.ColoredFormatter(
    '%(blue)s%(asctime)s%(reset)s %(log_color)s%(levelname)s%(reset)s: %(purple)s%(name)s%(reset)s - %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
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
models_manager = None
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
    """Initialize all components with clean v3.1 architecture - Phase 3b Complete"""
    global config_manager, settings_manager, zero_shot_manager, crisis_pattern_manager
    global models_manager, pydantic_manager, crisis_analyzer, learning_manager
    global analysis_parameters_manager  # Phase 3b addition
    
    try:
        logger.info("🚀 Initializing components with clean v3.1 architecture - Phase 3b Complete...")
        
        # ========================================================================
        # STEP 1: Initialize Core Configuration Managers - DIRECT ONLY
        # ========================================================================
        logger.info("📋 Initializing core configuration managers...")
        
        config_manager = ConfigManager("/app/config")
        zero_shot_manager = ZeroShotManager(config_manager)
        
        logger.info("✅ Core configuration managers initialized (ConfigManager, ZeroShotManager)")
        
        # ========================================================================
        # STEP 2: Initialize AnalysisParametersManager - Phase 3b
        # ========================================================================
        logger.info("⚙️ Initializing AnalysisParametersManager - Phase 3b...")
        
        try:
            from managers.analysis_parameters_manager import create_analysis_parameters_manager
            analysis_parameters_manager = create_analysis_parameters_manager(config_manager)
            
            # Validate analysis parameters
            validation_result = analysis_parameters_manager.validate_parameters()
            if validation_result['valid']:
                logger.info("✅ AnalysisParametersManager v3.1 initialized and validated")
                logger.debug(f"📊 Analysis parameters loaded: {len(analysis_parameters_manager.get_all_parameters())} categories")
            else:
                logger.error(f"❌ Analysis parameters validation failed: {validation_result['errors']}")
                raise ValueError("Analysis parameters validation failed")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize AnalysisParametersManager: {e}")
            analysis_parameters_manager = None
            raise
        
        # ========================================================================
        # STEP 3: Initialize SettingsManager with AnalysisParametersManager - Phase 3b
        # ========================================================================
        logger.info("🔧 Initializing SettingsManager with AnalysisParametersManager - Phase 3b...")
        
        try:
            from managers.settings_manager import create_settings_manager
            settings_manager = create_settings_manager(config_manager, analysis_parameters_manager)
            
            # Validate settings
            settings_validation = settings_manager.validate_settings()
            if settings_validation['valid']:
                logger.info("✅ SettingsManager v3.1 initialized with AnalysisParametersManager integration")
            else:
                logger.error(f"❌ Settings validation failed: {settings_validation['errors']}")
                if settings_validation['warnings']:
                    logger.warning(f"⚠️ Settings warnings: {settings_validation['warnings']}")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize SettingsManager: {e}")
            raise
        
        # ========================================================================
        # STEP 4: Initialize CrisisPatternManager - Phase 3a (FIXED)
        # ========================================================================
        logger.info("🔍 Initializing CrisisPatternManager - Phase 3a...")

        try:
            from managers.crisis_pattern_manager import create_crisis_pattern_manager
            crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
            
            # Test pattern loading - FIXED: Use pattern_status correctly
            pattern_status = crisis_pattern_manager.get_status()
            if pattern_status:
                # FIXED: Use pattern_status data instead of undefined available_patterns
                pattern_count = pattern_status.get('loaded_pattern_sets', 0)
                available_types = pattern_status.get('available_pattern_types', [])
                logger.info(f"✅ CrisisPatternManager v3.1 initialized with {pattern_count} pattern sets")
                logger.debug(f"📋 Available pattern types: {available_types}")
            else:
                logger.warning("⚠️ CrisisPatternManager initialized but no patterns loaded")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize CrisisPatternManager: {e}")
            crisis_pattern_manager = None
            # Don't fail initialization for pattern manager issues
        
        # ========================================================================
        # STEP 5: Initialize PydanticManager - Clean v3.1 
        # ========================================================================
        logger.info("📝 Initializing PydanticManager - Clean v3.1...")
        
        try:
            from managers.pydantic_manager import create_pydantic_manager
            pydantic_manager = create_pydantic_manager(config_manager)
            
            if pydantic_manager.is_initialized():
                logger.info("✅ PydanticManager v3.1 initialized")
            else:
                logger.error("❌ PydanticManager initialization failed")
                raise RuntimeError("PydanticManager failed to initialize")
        except Exception as e:
            logger.error(f"❌ Failed to initialize PydanticManager: {e}")
            raise
        
        # ========================================================================
        # STEP 6: Initialize ModelsManager - Clean v3.1
        # ========================================================================
        logger.info("🤖 Initializing ModelsManager - Clean v3.1...")
        
        try:
            from managers.models_manager import create_models_manager
            models_manager = create_models_manager(config_manager, settings_manager)
            
            # Initialize models
            await models_manager.initialize()
            
            if models_manager.models_loaded():
                ensemble_status = models_manager.get_ensemble_status()
                model_count = ensemble_status.get('model_count', 3)
                logger.info(f"✅ ModelsManager v3.1 initialized with {model_count} models loaded")
            else:
                logger.error("❌ ModelsManager failed to load models")
                raise RuntimeError("ModelsManager failed to load models")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize ModelsManager: {e}")
            raise
        
        # ========================================================================
        # STEP 7: Initialize Learning Manager (Optional)
        # ========================================================================
        logger.info("🧠 Initializing Enhanced Learning Manager...")
        
        global LEARNING_AVAILABLE
        try:
            from api.learning_endpoints import EnhancedLearningManager
            learning_manager = EnhancedLearningManager(
                models_manager=models_manager,
                config_manager=config_manager
            )
            LEARNING_AVAILABLE = True
            logger.info("✅ Enhanced Learning Manager initialized - Clean v3.1")
            
        except Exception as e:
            logger.warning(f"⚠️ Learning Manager not available: {e}")
            learning_manager = None
            LEARNING_AVAILABLE = False
        
        # ========================================================================
        # STEP 8: Initialize CrisisAnalyzer with Full Integration
        # ========================================================================
        logger.info("🔍 Initializing CrisisAnalyzer with full manager integration...")
        
        try:
            from analysis.crisis_analyzer import CrisisAnalyzer
            crisis_analyzer = CrisisAnalyzer(
                models_manager=models_manager,
                crisis_pattern_manager=crisis_pattern_manager,
                learning_manager=learning_manager,
                analysis_parameters_manager=analysis_parameters_manager  # Phase 3b integration
            )
            logger.info("✅ CrisisAnalyzer initialized with full manager integration (Phase 3b)")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize CrisisAnalyzer: {e}")
            crisis_analyzer = None
        
        # ========================================================================
        # STEP 9: Final Status Report - Clean v3.1 Phase 3b
        # ========================================================================
        logger.debug("📊 Component Initialization Summary (Clean v3.1 Phase 3b):")
        
        components_status = {
            'core_managers': {
                'config_manager': config_manager is not None,
                'settings_manager': settings_manager is not None,
                'zero_shot_manager': zero_shot_manager is not None,
                'analysis_parameters_manager_v3_1': analysis_parameters_manager is not None,  # Phase 3b
                'crisis_pattern_manager_v3_1': crisis_pattern_manager is not None,  # Phase 3a
                'pydantic_manager_v3_1': pydantic_manager is not None
            },
            'ml_components': {
                'models_manager_v3_1': models_manager is not None,
                'three_model_ensemble': models_manager and models_manager.models_loaded() if models_manager else False
            },
            'analysis_components': {
                'crisis_analyzer_with_full_integration': crisis_analyzer is not None,  # Phase 3b enhanced
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
        if not models_manager:
            critical_failures.append("ModelsManager v3.1")
        if models_manager and not models_manager.models_loaded():
            critical_failures.append("Model Loading")
        if not pydantic_manager:
            critical_failures.append("PydanticManager v3.1")
        if not analysis_parameters_manager:
            critical_failures.append("AnalysisParametersManager v3.1")  # Phase 3b critical
        
        if critical_failures:
            logger.error(f"❌ Critical component failures: {critical_failures}")
            raise RuntimeError(f"Critical v3.1 components failed: {critical_failures}")
        
        logger.info("✅ All critical components initialized successfully - Clean v3.1 Architecture")
        logger.info("🎉 Phase 3b Complete - AnalysisParametersManager integrated with JSON configuration")
        
        # Report Analysis Parameters Manager Status
        if analysis_parameters_manager:
            all_params = analysis_parameters_manager.get_all_parameters()
            logger.info(f"⚙️ Analysis Parameters Manager Status: Operational with {len(all_params)} parameter categories")
            logger.debug(f"📋 Parameter categories: {list(all_params.keys())}")
        else:
            logger.warning("⚠️ Analysis Parameters Manager: Not available - using fallback parameters")
        
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
# Updated Health Response Model - Phase 3b
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
    phase_3b_status: str  # Phase 3b addition

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
                models_manager=models_manager, 
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
                models_manager=models_manager
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
# Enhanced Health Check - Phase 3b Updated
# ============================================================================
@app.get("/health", response_model=HealthResponse)
async def enhanced_health_check():
    """Enhanced health check with Phase 3b AnalysisParametersManager status"""
    
    uptime = time.time() - startup_time
    model_loaded = models_manager is not None and models_manager.models_loaded()
    
    components_available = {
        "config_manager": config_manager is not None,
        "settings_manager": settings_manager is not None,
        "zero_shot_manager": zero_shot_manager is not None,
        "analysis_parameters_manager": analysis_parameters_manager is not None,  # Phase 3b
        "crisis_pattern_manager": crisis_pattern_manager is not None,  # Phase 3a
        "models_manager_v3_1": models_manager is not None,
        "pydantic_manager_v3_1": pydantic_manager is not None,
        "learning_manager_enhanced": learning_manager is not None,
        "crisis_analyzer_integrated": crisis_analyzer is not None
    }
    
    configuration_status = {
        "model_ensemble_loaded": models_manager.models_loaded() if models_manager else False,
        "analysis_parameters_loaded": analysis_parameters_manager is not None,  # Phase 3b
        "crisis_patterns_loaded": crisis_pattern_manager is not None,  # Phase 3a
        "ensemble_thresholds_configured": True,
        "learning_system_available": LEARNING_AVAILABLE
    }
    
    manager_status = {
        "models_manager_operational": models_manager is not None and models_manager.models_loaded(),
        "analysis_parameters_analysis_available": analysis_parameters_manager is not None,  # Phase 3b
        "crisis_pattern_analysis_available": crisis_pattern_manager is not None,  # Phase 3a
        "pydantic_validation_available": pydantic_manager is not None,
        "learning_adjustments_available": learning_manager is not None
    }
    
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        uptime=uptime,
        model_loaded=model_loaded,
        components_available=components_available,
        configuration_status=configuration_status,
        manager_status=manager_status,
        architecture_version="clean_v3.1_phase_3b_complete",
        phase_2c_status="complete",
        phase_3a_status="complete",  # Phase 3a
        phase_3b_status="complete"   # Phase 3b
    )

# ============================================================================
# PRODUCTION READY - Clean v3.1 Architecture Phase 3b Complete
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