# ash-nlp/main.py - PHASE 3D STEP 7 COMPLETE
"""
Phase 3d Step 7 COMPLETE: FeatureConfigManager and PerformanceConfigManager integration
Clean v3.1 Architecture with comprehensive feature flags and performance management

Phase 3a: CrisisPatternManager integration
Phase 3b: AnalysisParametersManager integration  
Phase 3c: ThresholdMappingManager integration
Phase 3d Step 5: ServerConfigManager integration
Phase 3d Step 6: LoggingConfigManager integration with enhanced colorlog
Phase 3d Step 7: FeatureConfigManager and PerformanceConfigManager integration
"""

import os
import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

# Clean v3.1 Managers - NO backward compatibility imports
from managers.config_manager import ConfigManager
from managers.settings_manager import SettingsManager, create_settings_manager
from managers.zero_shot_manager import ZeroShotManager
from managers.pydantic_manager import PydanticManager
from managers.models_manager import ModelsManager, create_models_manager
from analysis.crisis_analyzer import CrisisAnalyzer
from managers.server_config_manager import create_server_config_manager

# ============================================================================
# ENHANCED LOGGING SETUP - PHASE 3D STEP 6 INTEGRATED
# ============================================================================
import colorlog

# Global manager instances - Clean v3.1 with Phase 3d Step 7
config_manager: Optional[ConfigManager] = None
settings_manager: Optional[SettingsManager] = None
zero_shot_manager: Optional[ZeroShotManager] = None
crisis_pattern_manager = None  # Phase 3a
analysis_parameters_manager = None  # Phase 3b
threshold_mapping_manager = None  # Phase 3c
models_manager: Optional[ModelsManager] = None
pydantic_manager: Optional[PydanticManager] = None
crisis_analyzer: Optional[CrisisAnalyzer] = None
learning_manager = None
server_config_manager = None  # Phase 3d Step 5
logging_config_manager = None  # Phase 3d Step 6
feature_config_manager = None  # Phase 3d Step 7
performance_config_manager = None  # Phase 3d Step 7

def setup_initial_logging():
    """
    Phase 3d Step 6: Set up initial logging before LoggingConfigManager is available
    Uses GLOBAL_LOG_LEVEL and basic colorlog setup for early initialization
    """
    # Get initial log level (preserving GLOBAL_LOG_LEVEL for ecosystem compatibility)
    log_level = os.getenv('GLOBAL_LOG_LEVEL', 'INFO').upper()
    
    # Get log file using Phase 3d Step 6 standardized variable names
    log_file = os.getenv('NLP_STORAGE_LOG_FILE', 
                        os.getenv('NLP_LOG_FILE', 'nlp_service.log'))  # Fallback for compatibility
    
    # Create enhanced formatters
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
        handlers=[file_handler, console_handler],
        force=True  # Override any existing configuration
    )
    
    # Get logger for initial messages
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting Ash NLP Service v3.1d - Phase 3d Step 7 Feature & Performance Management")
    logger.info(f"📝 Initial log level: {log_level} (from GLOBAL_LOG_LEVEL)")
    logger.info(f"📁 Log file: {log_file}")
    
    return logger

# Initialize logging system
logger = setup_initial_logging()

async def initialize_components_clean_v3_1():
    """Initialize all components with clean v3.1 architecture - Phase 3d Step 7"""
    global config_manager, settings_manager, zero_shot_manager, crisis_pattern_manager
    global models_manager, pydantic_manager, crisis_analyzer, learning_manager
    global analysis_parameters_manager, threshold_mapping_manager, server_config_manager
    global logging_config_manager, feature_config_manager, performance_config_manager  # Phase 3d Step 7
    
    try:
        logger.info("🚀 Initializing components with clean v3.1 architecture - Phase 3d Step 7...")
        
        # Initialize Core Configuration Managers
        config_manager = ConfigManager("/app/config")
        zero_shot_manager = ZeroShotManager(config_manager)
        
        # Initialize LoggingConfigManager - Phase 3d Step 6
        try:
            from managers.logging_config_manager import create_logging_config_manager
            logging_config_manager = create_logging_config_manager(config_manager)
            logger.info("✅ LoggingConfigManager initialized")
        except Exception as e:
            logger.warning(f"⚠️ LoggingConfigManager initialization failed (non-critical): {e}")
            logging_config_manager = None
        
        # Initialize FeatureConfigManager and PerformanceConfigManager - Phase 3d Step 7
        try:
            from managers.feature_config_manager import create_feature_config_manager
            feature_config_manager = create_feature_config_manager(config_manager)
            logger.info("✅ FeatureConfigManager initialized")
        except Exception as e:
            logger.warning(f"⚠️ FeatureConfigManager initialization failed (non-critical): {e}")
            feature_config_manager = None
        
        try:
            from managers.performance_config_manager import create_performance_config_manager
            performance_config_manager = create_performance_config_manager(config_manager)
            logger.info("✅ PerformanceConfigManager initialized")
        except Exception as e:
            logger.warning(f"⚠️ PerformanceConfigManager initialization failed (non-critical): {e}")
            performance_config_manager = None
        
        # Initialize AnalysisParametersManager - Phase 3b
        from managers.analysis_parameters_manager import create_analysis_parameters_manager
        analysis_parameters_manager = create_analysis_parameters_manager(config_manager)
        
        # Initialize ThresholdMappingManager - Phase 3c
        from managers.threshold_mapping_manager import create_threshold_mapping_manager
        from managers.model_ensemble_manager import get_model_ensemble_manager
        model_ensemble_manager = get_model_ensemble_manager()
        threshold_mapping_manager = create_threshold_mapping_manager(config_manager, model_ensemble_manager)
        
        # Initialize CrisisPatternManager - Phase 3a
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        
        # Initialize ServerConfigManager - Phase 3d Step 5
        try:
            server_config_manager = create_server_config_manager(config_manager)
            logger.info("✅ ServerConfigManager initialized")
        except Exception as e:
            logger.warning(f"⚠️ ServerConfigManager initialization failed (non-critical): {e}")
            server_config_manager = None
        
        # Initialize Core ML Components
        pydantic_manager = PydanticManager()
        models_manager = create_models_manager(config_manager)
        
        # Load models
        logger.info("🔄 Loading Three Zero-Shot Model Ensemble...")
        await models_manager.load_models()
        
        # Initialize SettingsManager with All Dependencies - Phase 3d Step 7 Enhanced
        settings_manager = create_settings_manager(
            config_manager=config_manager,
            analysis_parameters_manager=analysis_parameters_manager,
            crisis_pattern_manager=crisis_pattern_manager,
            threshold_mapping_manager=threshold_mapping_manager,
            server_config_manager=server_config_manager,
            logging_config_manager=logging_config_manager,
            feature_config_manager=feature_config_manager,  # Phase 3d Step 7
            performance_config_manager=performance_config_manager  # Phase 3d Step 7
        )
        
        # Initialize CrisisAnalyzer with ALL Managers - Phase 3d Step 7 Complete
        crisis_analyzer = CrisisAnalyzer(
            models_manager=models_manager,
            crisis_pattern_manager=crisis_pattern_manager,
            learning_manager=learning_manager,
            analysis_parameters_manager=analysis_parameters_manager,
            threshold_mapping_manager=threshold_mapping_manager,
            feature_config_manager=feature_config_manager,  # Phase 3d Step 7
            performance_config_manager=performance_config_manager  # Phase 3d Step 7
        )
        
        # Initialize Learning Manager
        try:
            from api.learning_endpoints import EnhancedLearningManager
            learning_manager = EnhancedLearningManager(
                models_manager=models_manager,
                config_manager=config_manager,
                analysis_parameters_manager=analysis_parameters_manager
            )
            logger.info("✅ EnhancedLearningManager initialized")
        except Exception as e:
            logger.warning(f"⚠️ EnhancedLearningManager initialization failed (non-critical): {e}")
            learning_manager = None
        
        logger.info("✅ All components initialized successfully - Phase 3d Step 7 Complete")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize v3.1 components: {e}")
        raise

# ============================================================================
# Health Response Model - Phase 3d Step 7
# ============================================================================
class HealthResponse(BaseModel):
    status: str
    uptime: float
    model_loaded: bool
    components_available: dict
    configuration_status: dict
    manager_status: dict
    logging_status: dict
    feature_status: dict  # NEW Phase 3d Step 7
    performance_status: dict  # NEW Phase 3d Step 7
    architecture_version: str
    phase_3d_status: str

# ============================================================================
# FastAPI Application Setup - Clean v3.1 Phase 3d Step 7
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager - Clean v3.1 Architecture Phase 3d Step 7 Complete"""
    # Startup
    logger.info("🚀 FastAPI app starting - Clean v3.1 Architecture (Phase 3d Step 7)...")
    
    try:
        await initialize_components_clean_v3_1()
        logger.info("✅ FastAPI application startup complete - Phase 3d Step 7 Ready")
    except Exception as e:
        logger.error(f"❌ FastAPI app startup failed: {e}")
        raise
    
    # Application running
    yield
    
    # Shutdown
    logger.info("🛑 FastAPI app shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Ash-NLP Crisis Detection API",
    description="Three Zero-Shot Model Ensemble Crisis Detection - Phase 3d Step 7 Complete",
    version="3d.7",
    lifespan=lifespan
)

# ============================================================================
# Health Check Endpoint - Phase 3d Step 7 Enhanced
# ============================================================================
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    PHASE 3D STEP 7: Enhanced health check with Feature & Performance management status
    """
    start_time = time.time()
    
    try:
        # Basic system info
        uptime = time.time() - start_time
        model_loaded = models_manager.models_loaded() if models_manager else False
        
        # Component availability - Phase 3d Step 7 enhanced
        components_available = {
            'config_manager': config_manager is not None,
            'settings_manager': settings_manager is not None,
            'zero_shot_manager': zero_shot_manager is not None,
            'models_manager': models_manager is not None and model_loaded,
            'pydantic_manager': pydantic_manager is not None,
            'crisis_pattern_manager': crisis_pattern_manager is not None,
            'analysis_parameters_manager': analysis_parameters_manager is not None,
            'threshold_mapping_manager': threshold_mapping_manager is not None,
            'server_config_manager': server_config_manager is not None,
            'logging_config_manager': logging_config_manager is not None,
            'feature_config_manager': feature_config_manager is not None,  # Phase 3d Step 7
            'performance_config_manager': performance_config_manager is not None  # Phase 3d Step 7
        }
        
        # Configuration status
        configuration_status = {}
        
        if crisis_pattern_manager:
            try:
                pattern_count = len(crisis_pattern_manager.get_available_patterns())
                configuration_status['crisis_patterns_loaded'] = pattern_count > 0
                configuration_status['pattern_count'] = pattern_count
            except:
                configuration_status['crisis_patterns_loaded'] = False
                
        if analysis_parameters_manager:
            try:
                all_params = analysis_parameters_manager.get_all_parameters()
                configuration_status['analysis_parameters_loaded'] = len(all_params) > 0
                configuration_status['json_config_loaded'] = True
            except:
                configuration_status['analysis_parameters_loaded'] = False
                
        if threshold_mapping_manager:
            try:
                current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                validation_summary = threshold_mapping_manager.get_validation_summary()
                
                configuration_status['threshold_mapping_loaded'] = len(crisis_mapping) > 0
                configuration_status['threshold_mode'] = current_mode
                configuration_status['env_overrides_applied'] = True
                configuration_status['threshold_validation_passed'] = validation_summary.get('validation_errors', 0) == 0
            except:
                configuration_status['threshold_mapping_loaded'] = False
        
        if logging_config_manager:
            try:
                status = logging_config_manager.get_configuration_status()
                configuration_status['logging_config_loaded'] = True
                configuration_status['global_log_level_preserved'] = status.get('global_log_level_preserved', False)
            except:
                configuration_status['logging_config_loaded'] = False
        
        if feature_config_manager:
            try:
                all_features = feature_config_manager.get_all_features()
                configuration_status['feature_flags_loaded'] = len(all_features) > 0
                configuration_status['feature_validation_passed'] = len(feature_config_manager.get_validation_errors()) == 0
            except:
                configuration_status['feature_flags_loaded'] = False
        
        if performance_config_manager:
            try:
                all_settings = performance_config_manager.get_all_performance_settings()
                configuration_status['performance_settings_loaded'] = len(all_settings) > 0
                configuration_status['performance_validation_passed'] = len(performance_config_manager.get_validation_errors()) == 0
            except:
                configuration_status['performance_settings_loaded'] = False
        
        # Manager status
        manager_status = {
            'pattern_analysis_available': crisis_pattern_manager is not None,
            'parameter_analysis_available': analysis_parameters_manager is not None,
            'threshold_aware_analysis': threshold_mapping_manager is not None,
            'server_config_available': server_config_manager is not None,
            'logging_config_available': logging_config_manager is not None,
            'feature_config_available': feature_config_manager is not None,  # Phase 3d Step 7
            'performance_config_available': performance_config_manager is not None,  # Phase 3d Step 7
            'three_model_ensemble': model_loaded,
            'crisis_detection_operational': all([
                crisis_pattern_manager is not None,
                analysis_parameters_manager is not None, 
                threshold_mapping_manager is not None,
                model_loaded
            ])
        }
        
        # Logging status
        logging_status = {}
        if logging_config_manager:
            try:
                status = logging_config_manager.get_configuration_status()
                global_settings = logging_config_manager.get_global_logging_settings()
                logging_status = {
                    'logging_config_manager': 'operational',
                    'status': 'enhanced_integrated',
                    'log_level': global_settings.get('log_level', 'INFO'),
                    'global_log_level_preserved': status.get('global_log_level_preserved', False)
                }
            except Exception as e:
                logging_status = {'logging_config_manager': 'error', 'error': str(e)}
        else:
            logging_status = {'logging_config_manager': 'not_initialized', 'status': 'initial_colorlog'}
        
        # Feature status - NEW Phase 3d Step 7
        feature_status = {}
        if feature_config_manager:
            try:
                core_features = feature_config_manager.get_core_system_features()
                experimental_features = feature_config_manager.get_experimental_features()
                
                feature_status = {
                    'manager_available': True,
                    'core_features_enabled': sum(1 for v in core_features.values() if v),
                    'total_core_features': len(core_features),
                    'experimental_features_enabled': sum(1 for v in experimental_features.values() if v),
                    'total_experimental_features': len(experimental_features),
                    'validation_errors': len(feature_config_manager.get_validation_errors()),
                    'key_features': {
                        'ensemble_analysis': core_features.get('ensemble_analysis', False),
                        'pattern_integration': core_features.get('pattern_integration', False),
                        'safety_controls': core_features.get('safety_controls', False)
                    }
                }
            except Exception as e:
                feature_status = {'manager_available': True, 'error': str(e)}
        else:
            feature_status = {'manager_available': False, 'status': 'fallback_mode'}
        
        # Performance status - NEW Phase 3d Step 7
        performance_status = {}
        if performance_config_manager:
            try:
                analysis_perf = performance_config_manager.get_analysis_performance_settings()
                model_perf = performance_config_manager.get_model_performance_settings()
                profiles = performance_config_manager.get_available_profiles()
                
                performance_status = {
                    'manager_available': True,
                    'analysis_timeout_ms': analysis_perf.get('analysis_timeout_ms', 0),
                    'max_concurrent': analysis_perf.get('analysis_max_concurrent', 0),
                    'device': model_perf.get('device', 'unknown'),
                    'model_precision': model_perf.get('model_precision', 'unknown'),
                    'batch_size': model_perf.get('max_batch_size', 0),
                    'available_profiles': len(profiles),
                    'validation_errors': len(performance_config_manager.get_validation_errors())
                }
            except Exception as e:
                performance_status = {'manager_available': True, 'error': str(e)}
        else:
            performance_status = {'manager_available': False, 'status': 'fallback_mode'}
        
        # Overall status
        critical_components = [
            config_manager is not None,
            settings_manager is not None,
            zero_shot_manager is not None and model_loaded,
            pydantic_manager is not None,
            crisis_pattern_manager is not None,
            analysis_parameters_manager is not None,
            threshold_mapping_manager is not None
        ]
        
        overall_status = "healthy" if all(critical_components) else "degraded"
        
        return HealthResponse(
            status=overall_status,
            uptime=uptime,
            model_loaded=model_loaded,
            components_available=components_available,
            configuration_status=configuration_status,
            manager_status=manager_status,
            logging_status=logging_status,
            feature_status=feature_status,  # NEW Phase 3d Step 7
            performance_status=performance_status,  # NEW Phase 3d Step 7
            architecture_version="clean_v3_1_phase_3d_step_7",
            phase_3d_status="step_7_complete"
        )
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return HealthResponse(
            status="error",
            uptime=time.time() - start_time,
            model_loaded=False,
            components_available={},
            configuration_status={'error': str(e)},
            manager_status={'error': str(e)},
            logging_status={'error': str(e)},
            feature_status={'error': str(e)},
            performance_status={'error': str(e)},
            architecture_version="clean_v3_1_phase_3d_step_7",
            phase_3d_status="error"
        )

# ============================================================================
# Application Entry Point - Phase 3d Step 7
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Ash-NLP Crisis Detection API - Phase 3d Step 7")
    logger.info("🎯 Features: Feature Flags + Performance Management + Enhanced Logging")
    
    # Phase 3d Step 7: Use standardized variables
    host = os.getenv("NLP_SERVER_HOST", "0.0.0.0")  # Phase 3d Step 5
    port = int(os.getenv("GLOBAL_NLP_API_PORT", "8881"))  # Preserved
    workers = int(os.getenv("NLP_PERFORMANCE_WORKERS", "1"))  # Phase 3d Step 7
    reload_on_changes = os.getenv("NLP_FEATURE_RELOAD_ON_CHANGES", "false").lower() == "true"  # Phase 3d Step 7
    log_level = os.getenv("GLOBAL_LOG_LEVEL", "info").lower()  # Preserved
    
    logger.info(f"🌐 Server: {host}:{port} workers={workers} reload={reload_on_changes}")
    
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=workers,
            reload=reload_on_changes,
            log_level=log_level,
            access_log=True
        )
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        raise

logger.info("✅ Main application module loaded - Phase 3d Step 7 Complete")
logger.info("🚩 Feature flags management: FeatureConfigManager integrated")
logger.info("⚡ Performance settings management: PerformanceConfigManager integrated")
logger.info("🚀 Ready for production deployment")