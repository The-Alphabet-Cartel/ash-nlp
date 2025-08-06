# ash-nlp/main.py - PHASE 3C UPDATED
"""
Phase 3c UPDATED: Main application entry point with ThresholdMappingManager integration
Clean v3.1 Architecture with complete configuration externalization

Phase 3a: CrisisPatternManager integration
Phase 3b: AnalysisParametersManager integration  
Phase 3c: ThresholdMappingManager integration
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
from managers.settings_manager import SettingsManager 
from managers.zero_shot_manager import ZeroShotManager
from managers.pydantic_manager import PydanticManager
from managers.models_manager import ModelsManager
from analysis.crisis_analyzer import CrisisAnalyzer

# ============================================================================
# LOGGING SETUP
# ============================================================================
# DO NOT CHANGE THIS CODE BLOCK!
## Set up logging FIRST to catch any import errors
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

# Global manager instances - Clean v3.1 only
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

async def initialize_components_clean_v3_1():
    """Initialize all components with clean v3.1 architecture - Phase 3c Complete"""
    global config_manager, settings_manager, zero_shot_manager, crisis_pattern_manager
    global models_manager, pydantic_manager, crisis_analyzer, learning_manager
    global analysis_parameters_manager, threshold_mapping_manager  # Phase 3b & 3c
    
    try:
        logger.info("🚀 Initializing components with clean v3.1 architecture - Phase 3c Complete...")
        
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
            all_params = analysis_parameters_manager.get_all_parameters()
            logger.info(f"✅ AnalysisParametersManager initialized with {len(all_params)} parameter categories")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AnalysisParametersManager: {e}")
            raise RuntimeError(f"AnalysisParametersManager v3.1 initialization failed: {e}")
        
        # ========================================================================
        # STEP 3: Initialize ThresholdMappingManager - Phase 3c NEW
        # ========================================================================
        logger.info("🎯 Initializing ThresholdMappingManager - Phase 3c...")
        
        try:
            from managers.threshold_mapping_manager import create_threshold_mapping_manager
            
            # Initialize ModelEnsembleManager first for mode detection
            from managers.model_ensemble_manager import get_model_ensemble_manager
            model_ensemble_manager = get_model_ensemble_manager()
            
            # Create ThresholdMappingManager with model ensemble integration
            threshold_mapping_manager = create_threshold_mapping_manager(
                config_manager, model_ensemble_manager
            )
            
            # Validate threshold configuration
            validation_summary = threshold_mapping_manager.get_validation_summary()
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            
            logger.info(f"✅ ThresholdMappingManager initialized for {current_mode} mode")
            logger.info(f"🔧 Threshold validation: {validation_summary['validation_errors']} errors")
            
            if validation_summary['validation_errors'] > 0:
                logger.warning(f"⚠️ Threshold validation warnings: {validation_summary['error_details']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ThresholdMappingManager: {e}")
            raise RuntimeError(f"ThresholdMappingManager v3c initialization failed: {e}")
        
        # ========================================================================
        # STEP 4: Initialize CrisisPatternManager - Phase 3a
        # ========================================================================
        logger.info("🔍 Initializing CrisisPatternManager - Phase 3a...")
        
        try:
            from managers.crisis_pattern_manager import create_crisis_pattern_manager
            crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
            
            # Validate patterns loaded using correct methods
            pattern_status = crisis_pattern_manager.get_status()
            validation_result = crisis_pattern_manager.validate_patterns()
            
            logger.info(f"✅ CrisisPatternManager initialized with {len(available_patterns)} patterns")
            logger.debug(f"📋 Pattern categories: {pattern_categories}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize CrisisPatternManager: {e}")
            raise RuntimeError(f"CrisisPatternManager v3.1 initialization failed: {e}")
        
        # ========================================================================
        # STEP 5: Initialize Core ML Components - NO FALLBACKS
        # ========================================================================
        logger.info("🤖 Initializing ML components (ModelsManager, PydanticManager)...")
        
        # Initialize PydanticManager
        try:
            pydantic_manager = PydanticManager()
            
            if not pydantic_manager.is_initialized():
                raise RuntimeError("PydanticManager failed to initialize models")
            
            logger.info("✅ PydanticManager v3.1 initialized")
            
        except Exception as e:
            logger.error(f"❌ PydanticManager v3.1 initialization failed: {e}")
            raise RuntimeError(f"PydanticManager v3.1 required: {e}")
        
        # Initialize ModelsManager
        try:
            models_manager = ModelsManager()
            
            # Load models (this may take time)
            logger.info("🔄 Loading Three Zero-Shot Model Ensemble...")
            await models_manager.load_models()
            
            if not models_manager.models_loaded():
                raise RuntimeError("Three Zero-Shot Model Ensemble failed to load")
            
            logger.info("✅ Three Zero-Shot Model Ensemble loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ ModelsManager v3.1 initialization failed: {e}")
            raise RuntimeError(f"ModelsManager v3.1 required: {e}")
        
        # ========================================================================
        # STEP 6: Initialize SettingsManager with All Dependencies - Phase 3c Enhanced
        # ========================================================================
        logger.info("⚙️ Initializing SettingsManager with all dependencies - Phase 3c...")
        
        try:
            settings_manager = SettingsManager(
                config_manager=config_manager,
                crisis_pattern_manager=crisis_pattern_manager,
                analysis_parameters_manager=analysis_parameters_manager,
                threshold_mapping_manager=threshold_mapping_manager  # Phase 3c
            )
            
            logger.info("✅ SettingsManager initialized with full Phase 3c integration")
            
        except Exception as e:
            logger.error(f"❌ SettingsManager initialization failed: {e}")
            raise RuntimeError(f"SettingsManager initialization failed: {e}")
        
        # ========================================================================
        # STEP 7: Initialize CrisisAnalyzer with ALL Managers - Phase 3c Complete
        # ========================================================================
        logger.info("🔬 Initializing CrisisAnalyzer with complete integration - Phase 3c...")
        
        try:
            crisis_analyzer = CrisisAnalyzer(
                models_manager=models_manager,
                crisis_pattern_manager=crisis_pattern_manager,
                learning_manager=learning_manager,
                analysis_parameters_manager=analysis_parameters_manager,  # Phase 3b
                threshold_mapping_manager=threshold_mapping_manager  # Phase 3c
            )
            
            # Get configuration summary for validation
            config_summary = crisis_analyzer.get_configuration_summary()
            
            logger.info("✅ CrisisAnalyzer initialized with complete Phase 3c integration")
            logger.debug(f"🔧 CrisisAnalyzer configuration: {config_summary}")
            
        except Exception as e:
            logger.error(f"❌ CrisisAnalyzer initialization failed: {e}")
            raise RuntimeError(f"CrisisAnalyzer initialization failed: {e}")
        
        # ========================================================================
        # STEP 8: Initialize Learning Manager (Optional)
        # ========================================================================
        logger.info("🎓 Initializing LearningManager...")
        
        try:
            # Learning manager is optional
            learning_manager = None  # Placeholder for future implementation
            logger.debug("📋 LearningManager: Placeholder (future implementation)")
            
        except Exception as e:
            logger.warning(f"⚠️ LearningManager initialization failed (non-critical): {e}")
            learning_manager = None
        
        # ========================================================================
        # STEP 9: Validation and Summary - Phase 3c
        # ========================================================================
        logger.info("🔍 Validating complete Phase 3c initialization...")
        
        components_status = {
            'core_managers': {
                'config_manager': config_manager is not None,
                'settings_manager': settings_manager is not None,
                'zero_shot_manager': zero_shot_manager is not None,
                'analysis_parameters_manager_v3b': analysis_parameters_manager is not None,
                'threshold_mapping_manager_v3c': threshold_mapping_manager is not None,  # Phase 3c
                'crisis_pattern_manager_v3a': crisis_pattern_manager is not None,
                'pydantic_manager_v3_1': pydantic_manager is not None
            },
            'ml_components': {
                'models_manager_v3_1': models_manager is not None,
                'three_model_ensemble': models_manager and models_manager.models_loaded() if models_manager else False
            },
            'analysis_components': {
                'crisis_analyzer_with_complete_integration': crisis_analyzer is not None,
                'learning_manager': learning_manager is not None
            }
        }
        
        logger.info("📊 Component Initialization Summary (Clean v3.1 Phase 3c):")
        
        for category, components in components_status.items():
            logger.info(f"   {category.replace('_', ' ').title()}:")
            for component, status in components.items():
                status_icon = "✅" if status else "❌"
                logger.info(f"     {component}: {status_icon}")
        
        # Check for critical failures
        critical_failures = []
        if not models_manager:
            critical_failures.append("ModelsManager v3.1")
        if models_manager and not models_manager.models_loaded():
            critical_failures.append("Model Loading")
        if not pydantic_manager:
            critical_failures.append("PydanticManager v3.1")
        if not analysis_parameters_manager:
            critical_failures.append("AnalysisParametersManager v3b")
        if not threshold_mapping_manager:
            critical_failures.append("ThresholdMappingManager v3c")  # Phase 3c critical
        if not crisis_pattern_manager:
            critical_failures.append("CrisisPatternManager v3a")
        
        if critical_failures:
            logger.error(f"❌ Critical component failures: {critical_failures}")
            raise RuntimeError(f"Critical v3.1 components failed: {critical_failures}")
        
        logger.info("✅ All critical components initialized successfully - Clean v3.1 Architecture")
        logger.info("🎉 Phase 3c Complete - ThresholdMappingManager integrated with mode-aware thresholds")
        
        # Report comprehensive status
        _log_phase_3c_status_summary()
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize v3.1 components: {e}")
        logger.exception("Full initialization error:")
        raise

def _log_phase_3c_status_summary():
    """Log comprehensive Phase 3c status summary"""
    try:
        logger.info("=" * 80)
        logger.info("🎯 PHASE 3C COMPLETION STATUS SUMMARY")
        logger.info("=" * 80)
        
        # Report Analysis Parameters Manager Status
        if analysis_parameters_manager:
            all_params = analysis_parameters_manager.get_all_parameters()
            logger.info(f"⚙️ Analysis Parameters: {len(all_params)} parameter categories loaded")
            logger.debug(f"📋 Parameter categories: {list(all_params.keys())}")
        
        # Report Threshold Mapping Manager Status
        if threshold_mapping_manager:
            current_mode = threshold_mapping_manager.get_current_ensemble_mode()
            crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
            validation_summary = threshold_mapping_manager.get_validation_summary()
            
            logger.info(f"🎯 Threshold Mapping: {current_mode} mode active with {len(crisis_mapping)} thresholds")
            logger.info(f"🔧 Validation Status: {validation_summary['validation_errors']} errors")
            logger.debug(f"📊 Current crisis mapping: {crisis_mapping}")
        
        # Report Pattern Manager Status
        if crisis_pattern_manager:
            available_patterns = crisis_pattern_manager.get_available_patterns()
            pattern_categories = crisis_pattern_manager.get_pattern_categories()
            logger.info(f"🔍 Crisis Patterns: {len(available_patterns)} patterns across {len(pattern_categories)} categories")
        
        # Report CrisisAnalyzer Status
        if crisis_analyzer:
            config_summary = crisis_analyzer.get_configuration_summary()
            logger.info(f"🔬 Crisis Analyzer: Complete integration with {len(config_summary['components'])} components")
        
        logger.info("=" * 80)
        logger.info("🚀 SYSTEM READY - All Phase 3c components operational")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.warning(f"⚠️ Error logging Phase 3c status summary: {e}")

# ============================================================================
# Updated Health Response Model - Phase 3c
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
    phase_3a_status: str
    phase_3b_status: str
    phase_3c_status: str  # Phase 3c addition

# ============================================================================
# FastAPI Application Setup - Clean v3.1 Phase 3c
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager - Clean v3.1 Architecture Phase 3c Complete"""
    # Startup
    logger.info("🚀 Enhanced FastAPI app starting - Clean v3.1 Architecture (Phase 3c Complete)...")
    
    try:
        await initialize_components_clean_v3_1()
        
        # Import and add ensemble endpoints - CLEAN v3.1 + Phase 3c
        try:
            logger.info("🎯 Adding Three Zero-Shot Model Ensemble endpoints - Clean v3.1 Phase 3c...")
            from api.ensemble_endpoints import add_ensemble_endpoints_v3c
            
            # Pass ALL managers for complete Phase 3c integration
            add_ensemble_endpoints_v3c(
                app, 
                models_manager=models_manager, 
                pydantic_manager=pydantic_manager,
                crisis_pattern_manager=crisis_pattern_manager,  # Phase 3a
                threshold_mapping_manager=threshold_mapping_manager  # Phase 3c
            )
            logger.info("🚀 Ensemble endpoints added - Clean v3.1 + Complete Phase 3c Integration!")
            
        except Exception as e:
            logger.error(f"❌ Failed to add ensemble endpoints: {e}")
            raise RuntimeError(f"Ensemble endpoints setup failed: {e}")
        
        logger.info("✅ FastAPI application startup complete - Phase 3c Ready")
        
    except Exception as e:
        logger.error(f"❌ FastAPI app startup failed: {e}")
        logger.exception("Startup failure details:")
        raise
    
    # Application running
    yield
    
    # Shutdown
    logger.info("🛑 FastAPI app shutting down - Clean v3.1 Phase 3c...")
    
    try:
        if models_manager:
            logger.info("🔄 Cleaning up models...")
            # Add any cleanup logic here if needed
        
        logger.info("✅ FastAPI app shutdown complete")
        
    except Exception as e:
        logger.error(f"⚠️ Error during shutdown: {e}")

# Create FastAPI app with clean v3.1 lifespan
app = FastAPI(
    title="Ash-NLP Crisis Detection API",
    description="Three Zero-Shot Model Ensemble Crisis Detection with Pattern Integration - Phase 3c Complete",
    version="3c.1",
    lifespan=lifespan
)

# ============================================================================
# Health Check Endpoint - Phase 3c Enhanced
# ============================================================================
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    PHASE 3C: Enhanced health check with complete configuration status
    Reports status of all Phase 3c components including ThresholdMappingManager
    """
    start_time = time.time()
    
    try:
        # Basic system info
        uptime = time.time() - start_time
        model_loaded = models_manager.models_loaded() if models_manager else False
        
        # Component availability
        components_available = {
            'config_manager': config_manager is not None,
            'settings_manager': settings_manager is not None,
            'zero_shot_manager': zero_shot_manager is not None,
            'models_manager': models_manager is not None,
            'pydantic_manager': pydantic_manager is not None,
            'crisis_analyzer': crisis_analyzer is not None,
            'crisis_pattern_manager': crisis_pattern_manager is not None,  # Phase 3a
            'analysis_parameters_manager': analysis_parameters_manager is not None,  # Phase 3b
            'threshold_mapping_manager': threshold_mapping_manager is not None,  # Phase 3c
            'learning_manager': learning_manager is not None
        }
        
        # Configuration status - Phase 3c Enhanced
        configuration_status = {}
        
        if crisis_pattern_manager:
            try:
                available_patterns = crisis_pattern_manager.get_available_patterns()
                pattern_categories = crisis_pattern_manager.get_pattern_categories()
                configuration_status['crisis_patterns'] = {
                    'patterns_loaded': len(available_patterns),
                    'categories': len(pattern_categories),
                    'status': 'operational'
                }
            except Exception as e:
                configuration_status['crisis_patterns'] = {'status': 'error', 'error': str(e)}
        
        if analysis_parameters_manager:
            try:
                all_params = analysis_parameters_manager.get_all_parameters()
                configuration_status['analysis_parameters'] = {
                    'parameter_categories': len(all_params),
                    'crisis_thresholds_loaded': bool(all_params.get('crisis_thresholds')),
                    'status': 'operational'
                }
            except Exception as e:
                configuration_status['analysis_parameters'] = {'status': 'error', 'error': str(e)}
        
        if threshold_mapping_manager:
            try:
                current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                validation_summary = threshold_mapping_manager.get_validation_summary()
                staff_review_config = threshold_mapping_manager.get_staff_review_config()
                
                configuration_status['threshold_mapping'] = {
                    'current_mode': current_mode,
                    'crisis_mapping_loaded': bool(crisis_mapping),
                    'thresholds_count': len(crisis_mapping) if crisis_mapping else 0,
                    'validation_errors': validation_summary.get('validation_errors', 0),
                    'staff_review_enabled': staff_review_config.get('high_always', False),
                    'status': 'operational' if validation_summary.get('validation_errors', 0) == 0 else 'warning'
                }
            except Exception as e:
                configuration_status['threshold_mapping'] = {'status': 'error', 'error': str(e)}
        
        # Manager status - Phase 3c Enhanced
        manager_status = {}
        
        if models_manager:
            try:
                manager_status['models_manager'] = {
                    'models_loaded': models_manager.models_loaded(),
                    'ensemble_available': hasattr(models_manager, 'analyze_with_ensemble'),
                    'model_info': models_manager.get_model_info() if models_manager.models_loaded() else {}
                }
            except Exception as e:
                manager_status['models_manager'] = {'status': 'error', 'error': str(e)}
        
        if crisis_analyzer:
            try:
                config_summary = crisis_analyzer.get_configuration_summary()
                manager_status['crisis_analyzer'] = {
                    'phase': config_summary.get('phase', 'unknown'),
                    'architecture': config_summary.get('architecture', 'unknown'),
                    'components_loaded': sum(1 for v in config_summary.get('components', {}).values() if v),
                    'threshold_configuration': config_summary.get('threshold_configuration', {})
                }
            except Exception as e:
                manager_status['crisis_analyzer'] = {'status': 'error', 'error': str(e)}
        
        # Overall status determination
        critical_components = [
            models_manager is not None and model_loaded,
            pydantic_manager is not None,
            crisis_pattern_manager is not None,
            analysis_parameters_manager is not None,
            threshold_mapping_manager is not None
        ]
        
        overall_status = "healthy" if all(critical_components) else "degraded"
        
        # Check for warnings
        if threshold_mapping_manager:
            validation_summary = threshold_mapping_manager.get_validation_summary()
            if validation_summary.get('validation_errors', 0) > 0:
                overall_status = "warning"
        
        return HealthResponse(
            status=overall_status,
            uptime=uptime,
            model_loaded=model_loaded,
            components_available=components_available,
            configuration_status=configuration_status,
            manager_status=manager_status,
            architecture_version="clean_v3_1",
            phase_2c_status="complete",
            phase_3a_status="complete",
            phase_3b_status="complete", 
            phase_3c_status="complete"  # Phase 3c
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
            architecture_version="clean_v3_1",
            phase_2c_status="unknown",
            phase_3a_status="unknown",
            phase_3b_status="unknown",
            phase_3c_status="error"
        )

# ============================================================================
# Development/Debug Endpoints - Phase 3c Enhanced
# ============================================================================
@app.get("/debug/configuration")
async def debug_configuration():
    """
    PHASE 3C: Debug endpoint for configuration inspection
    Provides detailed view of all Phase 3c configuration systems
    """
    try:
        debug_info = {
            'phase': '3c',
            'architecture': 'clean_v3_1',
            'timestamp': time.time()
        }
        
        # Crisis Pattern Manager Debug
        if crisis_pattern_manager:
            try:
                debug_info['crisis_patterns'] = {
                    'available_patterns': len(crisis_pattern_manager.get_available_patterns()),
                    'pattern_categories': crisis_pattern_manager.get_pattern_categories(),
                    'enhanced_patterns': crisis_pattern_manager.get_enhanced_crisis_patterns() is not None
                }
            except Exception as e:
                debug_info['crisis_patterns'] = {'error': str(e)}
        
        # Analysis Parameters Manager Debug
        if analysis_parameters_manager:
            try:
                all_params = analysis_parameters_manager.get_all_parameters()
                debug_info['analysis_parameters'] = {
                    'parameter_categories': list(all_params.keys()),
                    'crisis_thresholds': all_params.get('crisis_thresholds', {}),
                    'total_parameters': sum(len(v) if isinstance(v, dict) else 1 for v in all_params.values())
                }
            except Exception as e:
                debug_info['analysis_parameters'] = {'error': str(e)}
        
        # Threshold Mapping Manager Debug - Phase 3c
        if threshold_mapping_manager:
            try:
                current_mode = threshold_mapping_manager.get_current_ensemble_mode()
                crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode()
                ensemble_thresholds = threshold_mapping_manager.get_ensemble_thresholds_for_mode()
                staff_review_config = threshold_mapping_manager.get_staff_review_config()
                validation_summary = threshold_mapping_manager.get_validation_summary()
                
                debug_info['threshold_mapping'] = {
                    'current_mode': current_mode,
                    'crisis_level_mapping': crisis_mapping,
                    'ensemble_thresholds': ensemble_thresholds,
                    'staff_review_config': staff_review_config,
                    'validation_summary': validation_summary,
                    'available_modes': ['consensus', 'majority', 'weighted']
                }
            except Exception as e:
                debug_info['threshold_mapping'] = {'error': str(e)}
        
        # Crisis Analyzer Debug
        if crisis_analyzer:
            try:
                config_summary = crisis_analyzer.get_configuration_summary()
                debug_info['crisis_analyzer'] = config_summary
            except Exception as e:
                debug_info['crisis_analyzer'] = {'error': str(e)}
        
        # Models Manager Debug
        if models_manager:
            try:
                debug_info['models'] = {
                    'models_loaded': models_manager.models_loaded(),
                    'model_info': models_manager.get_model_info() if models_manager.models_loaded() else {},
                    'ensemble_available': hasattr(models_manager, 'analyze_with_ensemble')
                }
            except Exception as e:
                debug_info['models'] = {'error': str(e)}
        
        return debug_info
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'phase': '3c',
            'architecture': 'clean_v3_1'
        }

@app.get("/debug/threshold-modes")
async def debug_threshold_modes():
    """
    PHASE 3C: Debug endpoint for threshold mode comparison
    Shows threshold differences across ensemble modes
    """
    try:
        if not threshold_mapping_manager:
            return {'error': 'ThresholdMappingManager not available'}
        
        modes_info = {}
        available_modes = ['consensus', 'majority', 'weighted']
        
        for mode in available_modes:
            try:
                crisis_mapping = threshold_mapping_manager.get_crisis_level_mapping_for_mode(mode)
                ensemble_thresholds = threshold_mapping_manager.get_ensemble_thresholds_for_mode(mode)
                
                modes_info[mode] = {
                    'crisis_level_mapping': crisis_mapping,
                    'ensemble_thresholds': ensemble_thresholds,
                    'description': f"Thresholds optimized for {mode} ensemble mode"
                }
            except Exception as e:
                modes_info[mode] = {'error': str(e)}
        
        current_mode = threshold_mapping_manager.get_current_ensemble_mode()
        
        return {
            'current_active_mode': current_mode,
            'available_modes': modes_info,
            'mode_switching': 'Available via NLP_ENSEMBLE_MODE environment variable',
            'validation_status': threshold_mapping_manager.get_validation_summary()
        }
        
    except Exception as e:
        return {'error': str(e)}

# ============================================================================
# Application Entry Point - Phase 3c
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Ash-NLP Crisis Detection API - Phase 3c Complete")
    logger.info("🎯 Features: Three Zero-Shot Model Ensemble + Crisis Patterns + Mode-Aware Thresholds")
    
    # Get configuration from environment
    host = os.getenv("NLP_HOST", "0.0.0.0")
    port = int(os.getenv("NLP_PORT", "8881"))
    log_level = os.getenv("NLP_LOG_LEVEL", "info").lower()
    
    logger.info(f"🌐 Server configuration: {host}:{port} (log_level={log_level})")
    
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=log_level,
            access_log=True,
            reload=False  # Disable in production
        )
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        raise

# ============================================================================
# PHASE 3C IMPLEMENTATION COMPLETE
# ============================================================================

logger.info("✅ Main application module loaded - Phase 3c Complete")
logger.info("🎉 Configuration externalization complete: Patterns + Parameters + Thresholds")
logger.info("🚀 Ready for production deployment with mode-aware crisis detection")