# ash-nlp/main.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Ash-NLP Main Application Entry Point for Ash NLP Service
---
FILE VERSION: v3.1-3e-6-2
LAST MODIFIED: 2025-08-22
PHASE: 3d, Step 10.11-3
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import os
import sys
import logging
import colorlog
import time
import asyncio
from pathlib import Path
from fastapi import FastAPI
import uvicorn

# ============================================================================
# MANAGER IMPORTS - ALL USING FACTORY FUNCTIONS
# ============================================================================
from managers.unified_config import create_unified_config_manager
from managers.analysis_config import create_analysis_config_manager
from managers.pattern_detection import create_pattern_detection_manager
from managers.feature_config import create_feature_config_manager
from managers.learning_system import create_learning_system_manager
from managers.logging_config import create_logging_config_manager
from managers.model_coordination import create_model_coordination_manager
from managers.performance_config import create_performance_config_manager
from managers.pydantic import create_pydantic_manager
from managers.server_config import create_server_config_manager
from managers.settings import create_settings_manager
from managers.shared_utilities import create_shared_utilities_manager
from managers.storage_config import create_storage_config_manager
from managers.crisis_threshold import create_crisis_threshold_manager
from managers.zero_shot import create_zero_shot_manager
from managers.context_analysis import create_context_analysis_manager

# Analysis Components
from analysis import create_crisis_analyzer

# API Endpoint Registration - FIXED IMPORTS
from api.admin_endpoints import add_admin_endpoints
from api.ensemble_endpoints import add_ensemble_endpoints

# ============================================================================
# UNIFIED CONFIGURATION LOGGING SETUP
# ============================================================================

def setup_unified_logging(unified_config_manager):
    """
    Setup colorlog logging with unified configuration management
    Phase 3d Step 9: Uses UnifiedConfigManager for all logging configuration
    """
    try:
        # Get logging configuration through unified config
        log_level = unified_config_manager.get_config_section('logging_settings', 'global_settings.log_level', 'INFO')
        log_detailed = unified_config_manager.get_config_section('logging_settings', 'detailed_logging.enable_detailed', True)
        enable_file_logging = unified_config_manager.get_config_section('logging_settings', 'global_settings.enable_file_output', False)
        log_file = unified_config_manager.get_config_section('logging_settings', 'global_settings.log_file', 'nlp_service.log')
        
        # Configure colorlog formatter
        if log_detailed == False:
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
        logging.info(f"📊 Log level: {log_level}")
        
    except Exception as e:
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)
        logging.error(f"❌ Failed to setup unified logging: {e}")
        logging.info("🔄 Using fallback basic logging configuration")

# ============================================================================
# UNIFIED MANAGER INITIALIZATION
# ============================================================================

def initialize_unified_managers():
    """
    Initialize all managers using UnifiedConfigManager
    Phase 3d Step 9: Complete unified configuration architecture
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 70)
    logger.info("🚀 Initializing unified configuration management system...")
    logger.info("=" * 70)
    
    try:
        logger.info("=" * 70)
        logger.info("🏗️ Creating UnifiedConfigManager...")
        logger.info("=" * 70)
        unified_config = create_unified_config_manager()
        logger.info("=" * 70)
        logger.info("✅ UnifiedConfigManager created successfully")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing analysis parameters manager...")
        logger.info("=" * 70)
        analysis_config = create_analysis_config_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Analysis parameters manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing context pattern manager...")
        logger.info("=" * 70)
        context_analysis = create_context_analysis_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Context pattern manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing crisis pattern manager...")
        logger.info("=" * 70)
        pattern_detection = create_pattern_detection_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Crisis pattern manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing feature config manager...")
        logger.info("=" * 70)
        feature_config = create_feature_config_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Feature config manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing logging config manager...")
        logger.info("=" * 70)
        logging_config = create_logging_config_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Logging config manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing models ensemble manager...")
        logger.info("=" * 70)
        model_coordination = create_model_coordination_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Models ensemble manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing performance config manager...")
        logger.info("=" * 70)
        performance_config = create_performance_config_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Performance config manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing pydantic manager...")
        logger.info("=" * 70)
        pydantic = create_pydantic_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Pydantic manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing server config manager...")
        logger.info("=" * 70)
        server_config = create_server_config_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Server config manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing shared utilities manager...")
        logger.info("=" * 70)
        shared_utilities = create_shared_utilities_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Shared utilities manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing storage manager...")
        logger.info("=" * 70)
        storage_config = create_storage_config_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Storage manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing threshold mapping manager...")
        logger.info("=" * 70)
        crisis_threshold = create_crisis_threshold_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Threshold mapping manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing zero shot manager...")
        logger.info("=" * 70)
        zero_shot = create_zero_shot_manager(unified_config)
        logger.info("=" * 70)
        logger.info("✅ Zero shot manager initialized...")
        logger.info("=" * 70)
        
        logger.info("=" * 70)
        logger.info("🔧 Initializing learning system manager...")
        logger.info("=" * 70)
        learning_system = create_learning_system_manager(
            unified_config,
            shared_utils=shared_utilities
        )
        logger.info("=" * 70)
        logger.info("✅ Learning system manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing settings manager...")
        logger.info("=" * 70)
        settings = create_settings_manager(
            unified_config,
            analysis_config_manager=analysis_config,
            pattern_detection_manager=pattern_detection,
            feature_config_manager=feature_config,
            learning_system_manager=learning_system,
            logging_config_manager=logging_config,
            model_coordination_manager=model_coordination,
            performance_config_manager=performance_config,
            pydantic_manager=pydantic,
            server_config_manager=server_config,
            shared_utilities_manager=shared_utilities,
            storage_config_manager=storage_config,
            crisis_threshold_manager=crisis_threshold,
            zero_shot_manager=zero_shot
        )
        logger.info("=" * 70)
        logger.info("✅ Settings manager initialized...")
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("🔧 Initializing analysis components...")
        logger.info("=" * 70)
        crisis_analyzer = create_crisis_analyzer(
            unified_config,
            model_coordination_manager=model_coordination,
            pattern_detection_manager=pattern_detection,
            analysis_config_manager=analysis_config,
            crisis_threshold_manager=crisis_threshold,
            feature_config_manager=feature_config,
            performance_config_manager=performance_config,
            context_analysis_manager=context_analysis,
            shared_utilities_manager=shared_utilities,
            learning_system_manager=learning_system,
            zero_shot_manager=zero_shot
        )
        logger.info("=" * 70)
        logger.info("✅ Analysis components initialized")
        logger.info("=" * 70)
        
    # ========================================================================
    # PRELOAD THOSE BIG-ASS MODELS!
    # ========================================================================
        if model_coordination:
            try:
                logger.info("=" * 70)
                logger.info("📊 Preloading AI models...")
                logger.info("=" * 70)
                asyncio.run(model_coordination.preload_models())
                
                # Log preload status
                status = model_coordination.get_preload_status()
                logger.info("🎉 ======================================================== 🎉")
                logger.info(f"🎉 Model preload status: {status}")
                logger.info("🎉 ======================================================== 🎉")
                
            except Exception as e:
                logger.info("❌ ======================================================== ❌")
                logger.error(f"❌ Model preloading failed during startup: {e}")
                logger.info("❌ ======================================================== ❌")

        managers = {
            'unified_config': unified_config,
            'analysis_config': analysis_config,
            'context_analysis': context_analysis,
            'crisis_analyzer': crisis_analyzer,
            'pattern_detection': pattern_detection,
            'feature_config': feature_config,
            'learning_system': learning_system,
            'logging_config': logging_config,
            'model_coordination': model_coordination,
            'performance_config': performance_config,
            'pydantic': pydantic,
            'server_config': server_config,
            'settings': settings,
            'shared_utilities': shared_utilities,
            'storage_config': storage_config,
            'crisis_threshold': crisis_threshold,
            'zero_shot': zero_shot
        }
        
        logger.info("🎉 ======================================================== 🎉")
        logger.info("🎉 All managers initialized successfully with unified configuration 🎉")
        logger.info(f"📊 Total managers created: {len(managers)}")
        logger.info("🎉 ======================================================== 🎉")
        
        return managers
        
    except Exception as e:
        logger.error(f"❌ Manager initialization failed: {e}")
        raise

# ============================================================================
# FASTAPI APPLICATION FACTORY
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
        add_ensemble_endpoints(
            app, 
            managers['crisis_analyzer'],
            managers['pydantic'],
            pattern_detection_manager=managers['pattern_detection'],
            crisis_threshold_manager=managers['crisis_threshold']
        )
        
        # Admin endpoints with ZeroShotManager
        try:
            add_admin_endpoints(
                app, 
                managers['unified_config'], 
                managers['settings'], 
                zero_shot_manager=managers['zero_shot'],
                pattern_detection_manager=managers['pattern_detection'],
                model_coordination_manager=managers['model_coordination'],
                analysis_config_manager=managers['analysis_config'],
                crisis_threshold_manager=managers['crisis_threshold']
            )
            if managers['model_coordination'] and managers['zero_shot']:
                logger.info("✅ Full admin endpoints registered with Model Ensemble Manager and ZeroShotManager")
            elif managers['model_coordination']:
                logger.info("✅ Limited admin endpoints registered with Model Ensemble Manager only")
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
        logger.info("            🚀 ASH-NLP SERVICE STARTUP")
        logger.info("=" * 70)
        
        # Clear cache first to ensure validation applies
        try:
            cache_cleared = unified_config.clear_configuration_cache()
            logger.info(f"🧹 Cleared {cache_cleared} cache entries to ensure validation applies")
        except Exception as e:
            logger.warning(f"⚠️ Could not clear cache: {e}")
        
        # Get server configuration from unified config with CORRECT paths
        host = unified_config.get_config_section('server_config', 'server_configuration.network_settings.host', '0.0.0.0')
        port = unified_config.get_config_section('server_config', 'server_configuration.network_settings.port', 8881)
        
        logger.info(f"🔍 Debug - host: '{host}' (type: {type(host).__name__})")
        logger.info(f"🔍 Debug - port: '{port}' (type: {type(port).__name__})")
        
        logger.info("=" * 70)
        logger.info("🏳️‍🌈 Ready to serve The Alphabet Cartel community!")
        logger.info("=" * 70)
        
        # *** CREATE AND INITIALIZE APP HERE - BEFORE UVICORN STARTS ***
        logger.info("🔧 Creating and initializing FastAPI application...")
        app = create_fastapi_app()
        logger.info("✅ FastAPI application fully initialized and ready")
        
        # Now start uvicorn with the already-initialized app object
        logger.info("=" * 70)
        logger.info("🚀 Starting uvicorn server with initialized application...")
        logger.info("=" * 70)
        uvicorn.run(
            app,  # Pass the initialized app object directly
            host=host,
            port=port,
            workers=1,  # Force single worker when passing app object
            reload=False,  # Force reload=False when passing app object  
            log_config=None,
            access_log=False
        )
        logger.info("=" * 70)
        logger.info("🎉 Server initialized 🎉")
        logger.info("=" * 70)
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise

# ============================================================================
# NO MODULE-LEVEL APP CREATION - ONLY FOR DIRECT EXECUTION
# ============================================================================