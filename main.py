# main.py
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
Ash-NLP Main Application Entry Point - GUNICORN COMPATIBLE VERSION
---
FILE VERSION: v3.1-gunicorn-1-1
LAST MODIFIED: 2025-08-24
PHASE: Gunicorn Migration - Module-Level Initialization
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

CHANGES FROM ORIGINAL:
- Moved all initialization to module level (no if __name__ == "__main__")
- App creation happens at import time for gunicorn preload_app compatibility
- Preserved all startup logging sequence
- Added gunicorn-specific initialization markers
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
# UNIFIED LOGGING SETUP - EXTRACTED TO FUNCTION
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
# FASTAPI APP CREATION - EXTRACTED TO FUNCTION
# ============================================================================

def create_fastapi_app():
    """Create and configure the FastAPI application"""

    app = FastAPI(
        title="Ash-NLP Crisis Detection API",
        description="Mental Health Crisis Detection for The Alphabet Cartel LGBTQIA+ Community",
        version="3.1-gunicorn",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add admin endpoints
    add_admin_endpoints(app,
                        config_manager=unified_config,
                        settings_manager=settings,
                        zero_shot_manager=zero_shot,
                        pattern_detection_manager=pattern_detection,
                        model_coordination_manager=model_coordination,
                        analysis_config_manager=analysis_config,
                        crisis_threshold_manager=crisis_threshold)

    # Add ensemble endpoints  
    add_ensemble_endpoints(app,
                            crisis_analyzer=crisis_analyzer,
                            model_coordination_manager=model_coordination,
                            pydantic_manager=pydantic,
                            pattern_detection_manager=pattern_detection,
                            crisis_threshold_manager=crisis_threshold)

    return app

# ============================================================================
# MODULE-LEVEL INITIALIZATION - RUNS WHEN IMPORTED BY GUNICORN
# ============================================================================

print("🎉 Starting Ash-NLP Crisis Detection Service v3.1-gunicorn")
print("🏳️‍🌈 Serving The Alphabet Cartel LGBTQIA+ Community")
print("🚀 Module-level initialization for gunicorn compatibility")
print("=" * 70)

# Initialize unified configuration manager
print("🔧 Initializing unified configuration manager...")
unified_config = create_unified_config_manager()
print("✅ Unified configuration manager initialized")

# Setup unified logging  
print("🔧 Setting up unified logging system...")
setup_unified_logging(unified_config)
print("✅ Unified logging system configured")

# Create logger after logging setup
logger = logging.getLogger(__name__)

logger.info("=" * 70)
logger.info("🚀 ASH-NLP SERVICE STARTUP (Gunicorn Production Mode)")
logger.info("=" * 70)
logger.info("🔧 Phase: Gunicorn Migration with Module-Level Initialization")
logger.info("🏳️‍🌈 Community: The Alphabet Cartel LGBTQIA+ Support")
logger.info("=" * 70)

# All manager initialization with preserved logging sequence
try:
    logger.info("=" * 70)
    logger.info("🔧 Initializing analysis config manager...")
    logger.info("=" * 70)
    analysis_config = create_analysis_config_manager(unified_config)
    logger.info("=" * 70)
    logger.info("✅ Analysis config manager initialized...")
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
    logger.info("🔧 Preloading ensemble models for shared memory optimization...")
    logger.info("⏱️ Model loading may take several minutes on first startup...")
    
    start_time = time.time()
    
    # This should preload all models into the master process
    # Workers will inherit them via copy-on-write memory sharing
    model_status = model_coordination.get_preload_status()
    logger.info(f"📊 Model preload status: {model_status}")
    
    if not model_status.get('preload_complete', False):
        logger.info("🔄 Triggering model preload for memory sharing...")
        try:
            # Trigger model loading by accessing model definitions
            models = model_coordination.get_model_definitions()
            logger.info(f"📦 Found {len(models)} models configured for preload")
            
            # Force model initialization for memory sharing
            for model_name, model_info in models.items():
                logger.info(f"🔄 Preloading model: {model_name}")
                # This will cache the model in master process memory
                model_coordination._get_cached_pipeline_sync(model_name)
                
        except Exception as e:
            logger.warning(f"⚠️ Model preload encountered issues: {e}")
            logger.info("🔄 Models will be loaded on-demand by workers")
    
    preload_time = time.time() - start_time
    logger.info(f"✅ Model preloading completed in {preload_time:.2f} seconds")
    
    # ========================================================================
    # CREATE FASTAPI APP AT MODULE LEVEL
    # ========================================================================
    logger.info("🔧 Creating FastAPI application at module level...")
    app = create_fastapi_app()
    logger.info("✅ FastAPI application created and configured")
    
    logger.info("=" * 70)
    logger.info("✅ ALL INITIALIZATION COMPLETE")
    logger.info("🌐 Application ready for gunicorn workers")
    logger.info("🧠 Models preloaded for memory sharing")
    logger.info("🏳️‍🌈 Ready to serve The Alphabet Cartel community")
    logger.info("=" * 70)

except Exception as e:
    logger.error(f"❌ Module-level initialization failed: {e}")
    logger.error("💥 This will prevent gunicorn from starting workers")
    raise

# ============================================================================
# GUNICORN COMPATIBILITY NOTE
# ============================================================================

logger.info("📋 Gunicorn Compatibility Status:")
logger.info("   ✅ Module-level initialization: COMPLETE")
logger.info("   ✅ App object available: READY")
logger.info("   ✅ Models preloaded for sharing: READY")
logger.info("   ✅ All managers initialized: READY")
logger.info("   🚀 Ready for: gunicorn -c gunicorn_config.py main:app")

# ============================================================================
# NO if __name__ == "__main__" BLOCK
# ============================================================================
# The original if __name__ == "__main__" block has been removed
# All initialization now happens at module level when imported
# Use dev_server.py for development with uvicorn
# Use gunicorn -c gunicorn_config.py main:app for production