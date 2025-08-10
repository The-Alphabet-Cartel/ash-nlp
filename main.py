"""
Ash-NLP Main Application Entry Point
Phase 3d Step 9: Unified Configuration Manager Integration

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import sys
import logging
import colorlog
from pathlib import Path
from fastapi import FastAPI
import uvicorn

# ============================================================================
# STEP 9: UNIFIED CONFIGURATION MANAGER IMPORT
# ============================================================================
from managers.unified_config_manager import create_unified_config_manager

# ============================================================================
# MANAGER IMPORTS - ALL USING FACTORY FUNCTIONS (CLEAN V3.1)
# ============================================================================
from managers.crisis_pattern_manager import create_crisis_pattern_manager
from managers.analysis_parameters_manager import create_analysis_parameters_manager
from managers.threshold_mapping_manager import create_threshold_mapping_manager
from managers.model_ensemble_manager import create_model_ensemble_manager
from managers.settings_manager import create_settings_manager
from managers.pydantic_manager import create_pydantic_manager

# Phase 3d Step 6-7 Managers
from managers.logging_config_manager import create_logging_config_manager
from managers.feature_config_manager import create_feature_config_manager
from managers.performance_config_manager import create_performance_config_manager
from managers.server_config_manager import create_server_config_manager

# Analysis Components
from analysis import create_crisis_analyzer

# API Endpoint Registration
from api.ensemble_endpoints import register_ensemble_endpoints
from api.learning_endpoints import register_learning_endpoints
from api.admin_endpoints import register_admin_endpoints

# ============================================================================
# LOGGING SETUP WITH UNIFIED CONFIGURATION
# ============================================================================

def setup_unified_logging(unified_config: 'UnifiedConfigManager'):
    """
    Setup logging with unified configuration manager
    Enhanced colorlog integration for Phase 3d Step 9
    """
    # Get logging configuration from unified manager
    log_level = unified_config.get_env('GLOBAL_LOG_LEVEL', 'INFO')
    logs_dir = unified_config.get_env('NLP_STORAGE_LOGS_DIR', './logs')
    enable_console = unified_config.get_env_bool('GLOBAL_LOGGING_ENABLE_CONSOLE', True)
    enable_file = unified_config.get_env_bool('GLOBAL_LOGGING_ENABLE_FILE', True)
    
    # Ensure logs directory exists
    Path(logs_dir).mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colorlog
    if enable_console:
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Enhanced color formatter for Phase 3d
        color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_yellow',
            }
        )
        console_handler.setFormatter(color_formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if enable_file:
        file_handler = logging.FileHandler(f"{logs_dir}/ash-nlp.log")
        file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)

# ============================================================================
# UNIFIED MANAGER INITIALIZATION - CLEAN V3.1 ARCHITECTURE
# ============================================================================

def initialize_unified_managers():
    """
    Initialize all managers using Unified Configuration Manager
    Clean v3.1 architecture with factory functions and dependency injection
    """
    logger = logging.getLogger(__name__)
    logger.info("🎉 Initializing Ash-NLP v3.1d Step 9 - Unified Configuration Architecture")
    logger.info("🏗️ Using Clean v3.1 factory functions with dependency injection")
    
    managers = {}
    
    try:
        # ===== STEP 1: CREATE UNIFIED CONFIGURATION MANAGER =====
        logger.info("📋 Step 1: Creating UnifiedConfigManager...")
        managers['unified_config'] = create_unified_config_manager("/app/config")
        logger.info("✅ UnifiedConfigManager initialized successfully")
        
        # ===== STEP 2: CREATE SPECIALIZED MANAGERS (PHASE 3A-3C) =====
        logger.info("📋 Step 2: Creating Phase 3a-3c managers...")
        
        # Phase 3a: Crisis Pattern Manager
        logger.info("🔍 Creating CrisisPatternManager...")
        managers['crisis_pattern'] = create_crisis_pattern_manager(managers['unified_config'])
        logger.info("✅ CrisisPatternManager initialized")
        
        # Phase 3b: Analysis Parameters Manager
        logger.info("🔬 Creating AnalysisParametersManager...")
        managers['analysis_parameters'] = create_analysis_parameters_manager(managers['unified_config'])
        logger.info("✅ AnalysisParametersManager initialized")
        
        # Phase 3c: Threshold Mapping Manager (requires model ensemble manager)
        logger.info("🎯 Creating ModelEnsembleManager for threshold mapping dependency...")
        managers['model_ensemble'] = create_model_ensemble_manager(managers['unified_config'])
        logger.info("✅ ModelEnsembleManager initialized")
        
        logger.info("📊 Creating ThresholdMappingManager...")
        managers['threshold_mapping'] = create_threshold_mapping_manager(
            managers['unified_config'], 
            managers['model_ensemble']
        )
        logger.info("✅ ThresholdMappingManager initialized")
        
        # ===== STEP 3: CREATE PHASE 3D STEP 6-7 MANAGERS =====
        logger.info("📋 Step 3: Creating Phase 3d Step 6-7 managers...")
        
        # Step 6: Logging Configuration Manager
        logger.info("📝 Creating LoggingConfigManager...")
        managers['logging_config'] = create_logging_config_manager(managers['unified_config'])
        logger.info("✅ LoggingConfigManager initialized")
        
        # Step 7: Feature Configuration Manager
        logger.info("🔧 Creating FeatureConfigManager...")
        managers['feature_config'] = create_feature_config_manager(managers['unified_config'])
        logger.info("✅ FeatureConfigManager initialized")
        
        # Step 7: Performance Configuration Manager
        logger.info("⚡ Creating PerformanceConfigManager...")
        managers['performance_config'] = create_performance_config_manager(managers['unified_config'])
        logger.info("✅ PerformanceConfigManager initialized")
        
        # Step 5: Server Configuration Manager
        logger.info("🌐 Creating ServerConfigManager...")
        managers['server_config'] = create_server_config_manager(managers['unified_config'])
        logger.info("✅ ServerConfigManager initialized")
        
        # ===== STEP 4: CREATE COMPREHENSIVE SETTINGS MANAGER =====
        logger.info("📋 Step 4: Creating comprehensive SettingsManager...")
        managers['settings'] = create_settings_manager(
            managers['unified_config'],
            crisis_pattern_manager=managers['crisis_pattern'],
            analysis_parameters_manager=managers['analysis_parameters'],
            threshold_mapping_manager=managers['threshold_mapping'],
            server_config_manager=managers['server_config'],
            logging_config_manager=managers['logging_config'],
            feature_config_manager=managers['feature_config'],
            performance_config_manager=managers['performance_config']
        )
        logger.info("✅ SettingsManager initialized with all Phase 3d managers")
        
        # ===== STEP 5: CREATE SUPPORTING MANAGERS =====
        logger.info("📋 Step 5: Creating supporting managers...")
        
        # Pydantic Manager
        logger.info("📝 Creating PydanticManager...")
        managers['pydantic'] = create_pydantic_manager(managers['unified_config'])
        logger.info("✅ PydanticManager initialized")
        
        # ===== STEP 6: CREATE CRISIS ANALYZER =====
        logger.info("📋 Step 6: Creating CrisisAnalyzer with all dependencies...")
        managers['crisis_analyzer'] = create_crisis_analyzer(
            models_manager=managers['model_ensemble'],
            crisis_pattern_manager=managers['crisis_pattern'],
            learning_manager=None,  # Will be created when needed
            analysis_parameters_manager=managers['analysis_parameters'],
            threshold_mapping_manager=managers['threshold_mapping'],
            feature_config_manager=managers['feature_config'],
            performance_config_manager=managers['performance_config']
        )
        logger.info("✅ CrisisAnalyzer initialized with full Phase 3d support")
        
        # ===== SUCCESS SUMMARY =====
        logger.info("🎉 All managers initialized successfully!")
        logger.info(f"📊 Total managers created: {len(managers)}")
        logger.info("✅ Phase 3d Step 9: Unified Configuration Architecture operational")
        
        return managers
        
    except Exception as e:
        logger.error(f"❌ Manager initialization failed: {e}")
        logger.error(f"📍 Failed at manager creation step")
        raise

# ============================================================================
# FASTAPI APPLICATION CREATION
# ============================================================================

def create_app():
    """Create FastAPI application with unified configuration"""
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize unified managers
        managers = initialize_unified_managers()
        
        # Get server configuration from unified manager
        server_config = managers['unified_config'].get_server_configuration()
        
        # Create FastAPI app
        app = FastAPI(
            title="Ash-NLP Crisis Detection API",
            description="LGBTQIA+ Mental Health Crisis Detection System - Clean v3.1d Step 9",
            version="3.1d-step9",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Store managers in app state for endpoint access
        app.state.managers = managers
        
        # Health check endpoint with unified configuration reporting
        @app.get("/health")
        async def health_check():
            """Health check endpoint with Phase 3d Step 9 status"""
            try:
                return {
                    "status": "healthy",
                    "version": "3.1d-step9",
                    "architecture": "clean_v3.1_unified_config",
                    "phase_3d_step_9": "operational",
                    "unified_config_manager": "active",
                    "managers_loaded": list(managers.keys()),
                    "total_managers": len(managers),
                    "environment_variables": {
                        "total_managed": len(managers['unified_config'].env_config),
                        "validation": "comprehensive_schema_validation",
                        "direct_os_getenv_calls": "eliminated"
                    },
                    "community": "The Alphabet Cartel LGBTQIA+ Mental Health Support"
                }
            except Exception as e:
                logger.error(f"❌ Health check error: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "version": "3.1d-step9"
                }
        
        # Register API endpoints with manager dependencies
        logger.info("🔗 Registering API endpoints...")
        register_ensemble_endpoints(app, managers['crisis_analyzer'], managers['threshold_mapping'])
        register_learning_endpoints(app, managers['unified_config'])  # STEP 9 CHANGE: Pass UnifiedConfigManager
        register_admin_endpoints(app, managers['settings'])
        logger.info("✅ All API endpoints registered")
        
        logger.info("🎉 FastAPI application created successfully with unified configuration")
        return app
        
    except Exception as e:
        logger.error(f"❌ FastAPI application creation failed: {e}")
        raise

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

def main():
    """Main application entry point with unified configuration"""
    try:
        # Create unified configuration manager for initial logging setup
        initial_config = create_unified_config_manager("/app/config")
        
        # Setup logging with unified configuration
        logger = setup_unified_logging(initial_config)
        
        logger.info("🚀 Starting Ash-NLP v3.1d Step 9 - Unified Configuration Architecture")
        logger.info("🏳️‍🌈 The Alphabet Cartel LGBTQIA+ Mental Health Crisis Detection System")
        logger.info("🎯 Phase 3d Step 9: Complete environment variable unification operational")
        
        # Create FastAPI application
        app = create_app()
        
        # Get server configuration from unified manager
        server_config = initial_config.get_server_configuration()['server']
        
        # Start the server
        logger.info(f"🌐 Starting server on {server_config['host']}:{server_config['port']}")
        logger.info(f"⚙️ Workers: {server_config['workers']}, Timeout: {server_config['timeout']}s")
        
        uvicorn.run(
            app,
            host=server_config['host'],
            port=server_config['port'],
            workers=1,  # Single worker for now to avoid manager duplication
            timeout_keep_alive=server_config['timeout']
        )
        
    except Exception as e:
        print(f"❌ Application startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()