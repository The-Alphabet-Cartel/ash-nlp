# ash-nlp/main.py
"""
Ash-NLP Main Application Entry Point for Ash NLP Service v3.1
Clean v3.1 Architecture
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
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
# ============================================================================
from managers.crisis_pattern_manager import create_crisis_pattern_manager
from managers.analysis_parameters_manager import create_analysis_parameters_manager
from managers.threshold_mapping_manager import create_threshold_mapping_manager
from managers.model_ensemble_manager import create_model_ensemble_manager
from managers.settings_manager import create_settings_manager
from managers.pydantic_manager import create_pydantic_manager

# STEP 9 FIX: Add Models Manager import with error handling
try:
    from managers.models_manager import create_models_manager
    MODELS_MANAGER_AVAILABLE = True
except ImportError:
    MODELS_MANAGER_AVAILABLE = False
    create_models_manager = None

# Phase 3d Step 6-7 Managers
from managers.logging_config_manager import create_logging_config_manager
from managers.feature_config_manager import create_feature_config_manager
from managers.performance_config_manager import create_performance_config_manager
from managers.server_config_manager import create_server_config_manager
from managers.storage_config_manager import create_storage_config_manager
from managers.zero_shot_manager import create_zero_shot_manager

# Analysis Components
from analysis import create_crisis_analyzer

# API Endpoint Registration - FIXED IMPORTS
from api.ensemble_endpoints import add_ensemble_endpoints_v3c  # FIXED: Use correct function name
from api.learning_endpoints import register_learning_endpoints
from api.admin_endpoints import add_admin_endpoints  # FIXED: Use correct function name

# ============================================================================
# PHASE 3D STEP 9: UNIFIED CONFIGURATION LOGGING SETUP
# ============================================================================

def setup_unified_logging(unified_config_manager):
    """
    Setup colorlog logging with unified configuration management
    Phase 3d Step 9: Uses UnifiedConfigManager for all logging configuration
    """
    try:
        # Get logging configuration through unified config
        log_level = unified_config_manager.get_env('GLOBAL_LOG_LEVEL', 'INFO')
        log_format = unified_config_manager.get_env('NLP_LOG_FORMAT', 'detailed')
        enable_file_logging = unified_config_manager.get_env_bool('NLP_LOG_ENABLE_FILE_LOGGING', True)
        log_file = unified_config_manager.get_env('NLP_LOG_FILE', 'nlp_service.log')
        
        # Configure colorlog formatter
        if log_format == 'simple':
            log_format_string = '%(log_color)s%(levelname)s%(reset)s: %(message)s'
        else:  # detailed
            log_format_string = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s%(reset)s: %(message)s'
        
        # Create colorlog formatter
        formatter = colorlog.ColoredFormatter(
            log_format_string,
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Console handler
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # Optional file handler
        if enable_file_logging:
            try:
                file_handler = logging.FileHandler(log_file)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                root_logger.addHandler(file_handler)
                logging.info(f"📁 File logging enabled: {log_file}")
            except Exception as e:
                logging.warning(f"⚠️ Could not setup file logging: {e}")
        
        logging.info("🎨 Unified colorlog logging configured successfully")
        logging.info(f"📊 Log level: {log_level}, Format: {log_format}")
        
    except Exception as e:
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)
        logging.error(f"❌ Failed to setup unified logging: {e}")
        logging.info("🔄 Using fallback basic logging configuration")

# ============================================================================
# PHASE 3D STEP 9: UNIFIED MANAGER INITIALIZATION
# ============================================================================

def initialize_unified_managers():
    """
    Initialize all managers using UnifiedConfigManager
    Phase 3d Step 9: Complete unified configuration architecture
    """
    logger = logging.getLogger(__name__)
    logger.info("🚀 Initializing unified configuration management system...")
    
    try:
        # Step 1: Create UnifiedConfigManager (foundation for everything)
        logger.info("🏗️ Creating UnifiedConfigManager...")
        unified_config = create_unified_config_manager()
        logger.info("✅ UnifiedConfigManager created successfully")
        
        # Step 2: Initialize all Phase 3a-3c managers with unified config
        logger.info("🔧 Initializing Phase 3a-3c managers...")
        crisis_pattern = create_crisis_pattern_manager(unified_config)
        analysis_parameters = create_analysis_parameters_manager(unified_config)
        threshold_mapping = create_threshold_mapping_manager(unified_config)
        logger.info("✅ Phase 3a-3c managers initialized")
        
        # Step 3: Initialize Phase 3d managers with unified config
        logger.info("🔧 Initializing Phase 3d managers...")
        logging_config = create_logging_config_manager(unified_config)
        feature_config = create_feature_config_manager(unified_config)
        performance_config = create_performance_config_manager(unified_config)
        server_config = create_server_config_manager(unified_config)
        # Initialize StorageConfigManager
        storage_config = None
        try:
            storage_config = create_storage_config_manager(unified_config)
            logger.info("✅ StorageConfigManager initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ StorageConfigManager initialization failed: {e}")
            logger.info("ℹ️ Continuing without StorageConfigManager - using fallback storage configuration")
        logger.info("✅ Phase 3d managers initialized")
        
        # Step 4: Initialize core system managers
        logger.info("🔧 Initializing core system managers...")
        model_ensemble = create_model_ensemble_manager(unified_config)
        
        # STEP 9 FIX: Create Models Manager with error handling
        models_manager = None
        if MODELS_MANAGER_AVAILABLE:
            try:
                models_manager = create_models_manager(unified_config)
                logger.info("✅ ModelsManager v3.1 created successfully")
            except Exception as e:
                logger.warning(f"⚠️ ModelsManager creation failed: {e}")
                logger.info("ℹ️ Admin endpoints will run in limited mode")
        else:
            logger.warning("⚠️ ModelsManager not available")
            logger.info("ℹ️ Admin endpoints will run in limited mode")
        
        # Create ZeroShotManager (needed for admin endpoints)
        zero_shot_manager = None
        try:
            zero_shot_manager = create_zero_shot_manager(unified_config)
            logger.info("✅ ZeroShotManager created successfully")
        except Exception as e:
            logger.warning(f"⚠️ ZeroShotManager creation failed: {e}")
            logger.info("ℹ️ Admin endpoints will run with limited functionality")

        pydantic_manager = create_pydantic_manager()
        settings = create_settings_manager(
            unified_config,
            crisis_pattern_manager=crisis_pattern,
            analysis_parameters_manager=analysis_parameters,
            threshold_mapping_manager=threshold_mapping,
            server_config_manager=server_config,
            logging_config_manager=logging_config,
            feature_config_manager=feature_config,
            performance_config_manager=performance_config,
            storage_config_manager=storage_config
        )
        logger.info("✅ Core system managers initialized")
        
        # Step 5: Initialize analysis components
        logger.info("🔧 Initializing analysis components...")
        crisis_analyzer = create_crisis_analyzer(
            models_manager=models_manager,
            crisis_pattern_manager=crisis_pattern,
            learning_manager=None,
            analysis_parameters_manager=analysis_parameters,
            threshold_mapping_manager=threshold_mapping,
            feature_config_manager=feature_config,
            performance_config_manager=performance_config
        )
        logger.info("✅ Analysis components initialized")
        
        # Return all managers in a structured dictionary
        managers = {
            'unified_config': unified_config,
            'crisis_pattern': crisis_pattern,
            'analysis_parameters': analysis_parameters,
            'threshold_mapping': threshold_mapping,
            'logging_config': logging_config,
            'feature_config': feature_config,
            'performance_config': performance_config,
            'server_config': server_config,
            'storage_config': storage_config,
            'model_ensemble': model_ensemble,
            'models_manager': models_manager,
            'pydantic': pydantic_manager,
            'settings': settings,
            'zero_shot_manager': zero_shot_manager,
            'crisis_analyzer': crisis_analyzer
        }
        
        logger.info("🎉 All managers initialized successfully with unified configuration")
        logger.info(f"📊 Total managers created: {len(managers)}")
        
        return managers
        
    except Exception as e:
        logger.error(f"❌ Manager initialization failed: {e}")
        raise

# ============================================================================
# PHASE 3D STEP 9: FASTAPI APPLICATION FACTORY
# ============================================================================

def create_fastapi_app():
    """
    Create FastAPI application with unified configuration
    Phase 3d Step 9: Complete unified configuration integration
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Creating FastAPI application with unified configuration...")
        
        # Initialize unified managers
        managers = initialize_unified_managers()
        
        # Create FastAPI app
        app = FastAPI(
            title="Ash-NLP Crisis Detection Service",
            description="LGBTQIA+ Mental Health Crisis Detection API with Clean v3.1 Architecture",
            version="3.1d-step9",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Add health endpoint with unified configuration status
        @app.get("/health")
        async def health_check():
            """Enhanced health check with unified configuration status"""
            try:
                # Get storage status if available
                storage_status = "available" if managers.get('storage_config') else "unavailable"
                
                return {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "version": "3.1d",
                    "architecture": "clean_v3.1_unified_config",
                    "phase_3d": "operational",
                    "unified_config_manager": "active",
                    "managers_loaded": list(managers.keys()),
                    "total_managers": len(managers),
                    "storage_config_manager": storage_status,
                    "environment_variables": {
                        "total_managed": len(managers['unified_config'].env_config),
                        "validation": "comprehensive_schema_validation",
                        "direct_os_getenv_calls": "eliminated"
                    },
                    "community": "The Alphabet Cartel"
                }
            except Exception as e:
                logger.error(f"❌ Health check error: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "version": "3.1d"
                }
        
        # Register API endpoints with manager dependencies
        logger.info("🔗 Registering API endpoints...")
        
        # Ensemble endpoints
        add_ensemble_endpoints_v3c(
            app, 
            managers['model_ensemble'], 
            managers['pydantic'], 
            crisis_pattern_manager=managers['crisis_pattern'],
            threshold_mapping_manager=managers['threshold_mapping']
        )
        
        # Learning endpoints - STEP 9 FIX: Correct parameters
        register_learning_endpoints(
            app, 
            managers['unified_config'], 
            threshold_mapping_manager=managers['threshold_mapping']
        )
        
        # Admin endpoints - STEP 9 FIX: Graceful ModelsManager handling
        # Admin endpoints with ZeroShotManager
        try:
            add_admin_endpoints(
                app, 
                managers['unified_config'], 
                managers['settings'], 
                zero_shot_manager=managers['zero_shot_manager'],  # FIX: Pass actual ZeroShotManager
                crisis_pattern_manager=managers['crisis_pattern'],
                models_manager=managers['models_manager'],
                analysis_parameters_manager=managers['analysis_parameters'],
                threshold_mapping_manager=managers['threshold_mapping']
            )
            if managers['models_manager'] and managers['zero_shot_manager']:
                logger.info("✅ Full admin endpoints registered with ModelsManager and ZeroShotManager")
            elif managers['models_manager']:
                logger.info("✅ Limited admin endpoints registered with ModelsManager only")
            else:
                logger.info("✅ Basic admin endpoints registered")
        except Exception as e:
            logger.error(f"❌ Admin endpoints registration failed: {e}")
            logger.info("ℹ️ Continuing without admin endpoints")
        
        logger.info("✅ All API endpoints registered")
        
        logger.info("🎉 FastAPI application created successfully with unified configuration")
        return app
        
    except Exception as e:
        logger.error(f"❌ FastAPI application creation failed: {e}")
        raise

# ============================================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import time
    
    try:
        print("🎉 Starting Ash-NLP Crisis Detection Service v3.1d Step 9")
        print("🏳️‍🌈 Serving The Alphabet Cartel LGBTQIA+ Community")
        print("🏛️ Repository: https://github.com/the-alphabet-cartel/ash-nlp")
        print("💬 Discord: https://discord.gg/alphabetcartel")
        print("🌐 Website: https://alphabetcartel.org")
        print("")
        
        # Initialize unified configuration manager first
        unified_config = create_unified_config_manager()
        
        # Setup unified logging
        setup_unified_logging(unified_config)
        
        logger = logging.getLogger(__name__)
        logger.info("=" * 70)
        logger.info("🚀 ASH-NLP SERVICE STARTUP - PHASE 3D STEP 9")
        logger.info("=" * 70)
        
        # Create application
        app = create_fastapi_app()
        
        # Get server configuration from unified config
        host = unified_config.get_env('NLP_SERVER_HOST', '0.0.0.0')
        port = unified_config.get_env_int('GLOBAL_NLP_API_PORT', 8881)
        workers = unified_config.get_env_int('NLP_SERVER_WORKERS', 1)
        reload = unified_config.get_env_bool('NLP_SERVER_RELOAD', False)
        
        logger.info(f"🌐 Server configuration: {host}:{port}")
        logger.info(f"👥 Workers: {workers}")
        logger.info(f"🔄 Auto-reload: {reload}")
        logger.info("=" * 70)
        logger.info("🎉 PHASE 3D STEP 9: UNIFIED CONFIGURATION OPERATIONAL")
        logger.info("🏳️‍🌈 Ready to serve The Alphabet Cartel community!")
        logger.info("=" * 70)
        
        # Start server
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=workers,
            reload=reload,
            log_config=None,  # Use our custom logging
            access_log=False  # Disable default access logging
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise