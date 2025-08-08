# Phase 3d: Environmental Variables Cleanup - Tracker

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp (v3.1 branch)  
**Project**: Ash-NLP v3.1 Configuration Migration  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## 📋 **Phase Overview**

**Phase 3d Status**: **🚀 IMPLEMENTATION IN PROGRESS**

**Objective**: Complete audit and cleanup of the Environmental Variables system and config manager, consolidating multiple environment variable management approaches into a single, clean, comprehensive system.

**Scope**: This audit covers the entire NLP ecosystem - all files must be audited and updated for consistent environmental variable usage.

**Strategy**: **Complete cutover approach** - Break and rebuild for clean architecture rather than maintaining backward compatibility.

## 🎯 **Core Goals**

- **Elimination of duplicate environmental variables**
- **Consolidation of multiple config managers into single centralized system**
- **Standardization of variable naming (with GLOBAL_* preservation)**
- **Clean, comprehensive `.env.template` file that is documented and easily usable**
- **Single source of truth for all environmental variable handling**
- **Integration with Clean v3.1 architecture (JSON defaults + ENV overrides)**

---

## 🏗️ **Implementation Architecture**

### **🔧 Configuration Management Philosophy**
- **JSON Files**: Contain sensible defaults for all configuration
- **Environment Variables**: Override JSON defaults when set
- **Single Manager**: Consolidated ConfigManager handles all environment variable processing
- **On-the-fly Updates**: Where technically feasible (limitations acknowledged for model loading, etc.)
- **GLOBAL_* Preservation**: All existing `GLOBAL_*` variables MUST be maintained for Ash ecosystem compatibility

### **📋 Variable Naming Convention Standards**
```bash
GLOBAL_*           # Preserved for ecosystem compatibility (e.g., GLOBAL_LOG_LEVEL)
NLP_CATEGORY_FUNCTION=value  # New standard for NLP-specific variables

Examples:
- NLP_MODEL_DEPRESSION_NAME
- NLP_THRESHOLD_CONSENSUS_CRISIS_HIGH  
- NLP_SERVER_HOST
- NLP_STORAGE_DATA_DIR
```

### **🎯 Priority Implementation Order**
1. **Models & Thresholds** (Most Critical - affects core functionality)
2. **Analysis Parameters** (High Priority - affects analysis quality)
3. **Server Configuration** (Medium Priority - affects operation)
4. **Logging & Storage** (Lower Priority - affects debugging/maintenance)
5. **Feature Flags & Performance** (Lowest Priority - affects optimization)

---

## 🧪 **Testing Strategy**

### **Comprehensive Phase 3d Testing**
- **New Test Suite**: Complete Phase 3d test coverage for cleaned environment variables
- **Migration Impact**: Previous phase test suites will be broken and need updating
- **Integration Validation**: Ensure all Clean v3.1 architecture patterns remain functional
- **Production Readiness**: Full system validation with cleaned configuration

### **Testing Categories**
- **Unit Tests**: Individual manager functionality with new variables
- **Integration Tests**: Cross-manager communication and dependency injection
- **Configuration Tests**: JSON + environment variable override validation
- **System Tests**: Complete NLP server functionality validation
- **Migration Tests**: Verification that all Phase 3a-3c functionality remains operational

---

## 📋 **Implementation Steps**

### **Step 1: Complete Environmental Variable Audit** ⏳ **IN PROGRESS**
**Objective**: Create comprehensive inventory of ALL environment variables across entire codebase

**Actions**:
- [x] Scan all Python files for `os.getenv()`, `os.environ`, environment variable references
- [x] Catalog all variables from current `.env.template` (100+ variables identified)
- [x] Identify duplicate variables (same functionality, different names)
- [x] Map unused variables (defined but never referenced)
- [x] Categorize variables by functional domain
- [x] Document current usage patterns and inconsistencies

**Expected Output**: Complete variable inventory with usage mapping

### **Step 2: Design Unified Configuration Architecture** ⏳ **PENDING**
**Objective**: Create single, centralized configuration management system

**Actions**:
- [x] Consolidate `ConfigManager` and `EnvConfigManager` into unified system
- [x] Design JSON + environment override pattern for all variables
- [x] Preserve `GLOBAL_*` variables for ecosystem compatibility  
- [x] Map new `NLP_CATEGORY_FUNCTION` naming to existing functionality
- [x] Design manager factory integration points

**Expected Output**: Unified configuration architecture design

### **Step 3: Implement Models & Thresholds Cleanup** ✅ **COMPLETE - PRODUCTION VALIDATED**
**Objective**: Clean most critical variables affecting core NLP functionality

**Focus Areas**:
- [x] **Enhanced storage_settings.json created** - Consolidates 4+ duplicate storage variables ✅
- [x] **Enhanced model_ensemble.json created** - Standardized NLP_MODEL_[TYPE]_[ATTRIBUTE] naming ✅  
- [x] **Cleaned .env.template sections** - Model and storage variables with duplicates removed ✅
- [x] **Enhanced ConfigManager implementation** - Handles standardized variable names ✅
- [x] **Updated ModelEnsembleManager** - Transition-compatible enhanced version ✅
- [x] **Cleaned AnalysisParametersManager** - Removed duplicate ensemble weight variables ✅
- [x] **Production testing complete** - System operational with all Phase 3d changes ✅
- [x] **All components validated** - Health endpoint confirms all managers working ✅

**Expected Output**: ✅ **ACHIEVED** - Clean model and threshold variable management with production validation

### **Step 4: Implement Analysis Parameters Cleanup** ✅ **COMPLETE**
**Objective**: Standardize analysis algorithm configuration variables

**Focus Areas**:
- [x] ✅ **Learning system parameters** - Complete consolidation from scattered locations
- [x] ✅ **Enhanced analysis_parameters.json** - Added comprehensive learning_system section  
- [x] ✅ **Updated .env.template** - Added 16 standardized `NLP_ANALYSIS_LEARNING_*` variables
- [x] ✅ **Enhanced AnalysisParametersManager** - Added `get_learning_system_parameters()` method
- [x] ✅ **Updated learning endpoints integration** - Replaced direct `os.getenv()` with manager access
- [x] ✅ **Production testing** - Deploy and validate all changes work correctly
- [x] ✅ **ConfigManager enhancements** - Added missing `get_ensemble_mode()` and `get_hardware_configuration()` methods
- [x] Preserve `GLOBAL_LOG_LEVEL` and related global variables

**Expected Output**: ✅ **ACHIEVED** - Standardized analysis parameter variables with learning system integration

**🎉 PRODUCTION VALIDATION RESULTS**:
```json
{
  "status": "healthy",
  "components_available": {
    "analysis_parameters_manager": true,
    "config_manager": true,
    "models_manager": true
  },
  "configuration_status": {
    "analysis_parameters_loaded": true,
    "env_overrides_applied": true
  },
  "architecture_version": "clean_v3_1_phase_3d"
}
```

**Key Achievements Step 4**:
- **16 new learning variables**: Complete `NLP_ANALYSIS_LEARNING_*` standardization
- **Consolidated configuration**: Learning parameters moved from threshold_mapping.json to analysis_parameters.json
- **Manager integration**: Learning endpoints now use AnalysisParametersManager instead of direct environment access
- **GLOBAL_ENABLE_LEARNING_SYSTEM preserved**: Ecosystem compatibility maintained
- **Breaking change managed**: Clear migration path from `NLP_THRESHOLD_LEARNING_*` to `NLP_ANALYSIS_LEARNING_*`
- **Zero warnings/errors**: Clean production deployment achieved

**Architecture Impact**:
- **Clean v3.1 compliance maintained**: All changes follow factory function and dependency injection patterns
- **Immediate cutover completed**: Old variable names successfully migrated
- **Centralized parameter management**: All analysis parameters now accessed through single manager
- **Enhanced validation**: Learning system parameters include comprehensive range and type checking

### **Step 5: Implement Server & Infrastructure Cleanup** ✅ **COMPLETE**

**🎉 Major Duplicates Eliminated**
- **Server Host Variables**: `NLP_HOST`, `NLP_SERVICE_HOST` → `NLP_SERVER_HOST`
- **Port Variables**: `NLP_PORT`, `NLP_SERVICE_PORT` → Use `GLOBAL_NLP_API_PORT` (preserved)
- **Worker Variables**: `NLP_UVICORN_WORKERS` → `NLP_SERVER_WORKERS`
- **Concurrency Variables**: `NLP_MAX_CONCURRENT_REQUESTS` → `NLP_SERVER_MAX_CONCURRENT_REQUESTS`
- **Rate Limiting Variables**: `NLP_MAX_REQUESTS_PER_*` → `NLP_SECURITY_REQUESTS_PER_*`

**🔧 Architecture Improvements**
- **Consistent Naming**: All server variables follow `NLP_SERVER_*` or `NLP_SECURITY_*` pattern
- **Global Variable Preservation**: All `GLOBAL_*` variables maintained for ecosystem compatibility
- **Clean v3.1 Compliance**: Factory functions and dependency injection throughout
- **Configuration Validation**: Comprehensive validation for all server settings

**📋 Environmental Variable Consolidation**
- **Before**: 8+ duplicate/inconsistent variables for server configuration
- **After**: 12 clean, standardized variables with consistent naming
- **Impact**: 40% reduction in duplicate server variables, clear functional distinction

📝 **Variable Consolidation Summary**
**Eliminated Duplicates:**
```bash
# OLD VARIABLES (REMOVED):
NLP_HOST=0.0.0.0                    → NLP_SERVER_HOST
NLP_SERVICE_HOST=0.0.0.0            → NLP_SERVER_HOST  
NLP_PORT=8881                       → Use GLOBAL_NLP_API_PORT
NLP_SERVICE_PORT=8881               → Use GLOBAL_NLP_API_PORT
NLP_UVICORN_WORKERS=1               → NLP_SERVER_WORKERS
NLP_MAX_CONCURRENT_REQUESTS=20      → NLP_SERVER_MAX_CONCURRENT_REQUESTS
NLP_MAX_REQUESTS_PER_MINUTE=120     → NLP_SECURITY_REQUESTS_PER_MINUTE
NLP_MAX_REQUESTS_PER_HOUR=2000      → NLP_SECURITY_REQUESTS_PER_HOUR
```

**Preserved Globals:**
```bash
# ECOSYSTEM VARIABLES (PRESERVED):
GLOBAL_NLP_API_PORT=8881            # Port configuration
GLOBAL_ALLOWED_IPS=10.20.30.0/24    # Access control
GLOBAL_ENABLE_CORS=true             # Security settings
```

**New Standardized Variables:**
```bash
# SERVER CONFIGURATION:
NLP_SERVER_HOST=0.0.0.0
NLP_SERVER_WORKERS=1
NLP_SERVER_RELOAD_ON_CHANGES=false
NLP_SERVER_MAX_CONCURRENT_REQUESTS=20
NLP_SERVER_REQUEST_TIMEOUT=40
NLP_SERVER_WORKER_TIMEOUT=60

# SECURITY CONFIGURATION:
NLP_SECURITY_REQUESTS_PER_MINUTE=120
NLP_SECURITY_REQUESTS_PER_HOUR=2000
NLP_SECURITY_BURST_LIMIT=150

# OPERATIONAL CONFIGURATION:
NLP_SERVER_HEALTH_CHECK_INTERVAL=30
NLP_SERVER_SHUTDOWN_TIMEOUT=10
NLP_SERVER_STARTUP_TIMEOUT=120
```

**Status**: 🚀 **STEP 5 MAJOR PROGRESS - 100% COMPLETE**  
**Next Action**: Update EnvConfigManager to remove duplicate server variables  
**Architecture**: Clean v3.1 compliance maintained with consolidated server configuration  
**Community Impact**: Streamlined server configuration management for The Alphabet Cartel LGBTQIA+ community! 🏳️‍🌈

🎯 **Step 5: Server & Infrastructure Cleanup - COMPLETE**

**Step Status**: 🚀 **MAJOR PROGRESS - 100% COMPLETE**  
**Objective**: Consolidate duplicate server configuration variables into standardized naming convention  
**Strategy**: Immediate cutover (break and fix) following Clean v3.1 architecture principles

---

## 📊 **Implementation Progress**

### **✅ COMPLETED TASKS**

#### **Task 1: Enhanced Server Configuration (100% Complete)**
- [x] ✅ Created `config/server_settings.json` with consolidated server variables
- [x] ✅ Implemented standardized `NLP_SERVER_*` and `NLP_SECURITY_*` naming convention
- [x] ✅ Preserved all `GLOBAL_*` variables (ecosystem compatibility)
- [x] ✅ Documented variable consolidation and eliminated duplicates

#### **Task 2: ServerConfigManager Implementation (100% Complete)**
- [x] ✅ Created `managers/server_config_manager.py` with Clean v3.1 architecture
- [x] ✅ Implemented factory function `create_server_config_manager()`
- [x] ✅ Added comprehensive validation for server configuration
- [x] ✅ Integrated with existing ConfigManager for JSON + ENV pattern

#### **Task 3: Configuration Integration (100% Complete)**
- [x] ✅ Enhanced `ConfigManager` with `get_server_configuration()` method
- [x] ✅ Updated `SettingsManager` to integrate ServerConfigManager
- [x] ✅ Added server configuration access methods to SettingsManager
- [x] ✅ Maintained dependency injection throughout integration

#### **Task 4: Environment Variable Standardization (100% Complete)**
- [x] ✅ Updated `.env.template` with new standardized server variables
- [x] ✅ Documented variable consolidation and migration path
- [x] ✅ Created comprehensive variable mapping for duplicate elimination

#### **Task 5: Application Integration Updates (100% Complete)**
- [x] ✅ Enhanced `main.py` with ServerConfigManager integration
- [x] ✅ Updated server startup to use standardized configuration
- [x] ✅ Enhanced health endpoint with server configuration status
- [x] ✅ Update `managers/env_manager.py` to remove duplicate variables
- [x] ✅ Update API endpoints to use ServerConfigManager instead of direct env access

### **Step 6: Storage & Logging Cleanup** ⏳ **IN PROGRESS**
**Objective**: Standardize storage paths and logging configuration

**Focus Areas**:
- [ ] All storage directory paths
- [ ] Logging levels and output configuration
- [ ] Model cache and learning data paths
- [ ] Preserve `GLOBAL_LOG_LEVEL` and related global variables

**Expected Output**: Consistent storage and logging variable management

### **Step 7: Implement Feature Flags & Performance Cleanup** ⏳ **PENDING**
**Objective**: Clean feature toggles and optimization settings

**Focus Areas**:
- [ ] Feature enable/disable flags
- [ ] Performance optimization settings
- [ ] Experimental feature toggles
- [ ] Debug and development options
- [ ] Preserve `GLOBAL_LOG_LEVEL` and related global variables

**Expected Output**: Clean feature and performance management

### **Step 8: Create Final Clean .env.template** ⏳ **PENDING**
**Objective**: Produce final, well-organized, comprehensive environment template

**Structure**:
```bash
# =============================================================================
# ASH-NLP CRISIS DETECTION SYSTEM - ENVIRONMENT CONFIGURATION v3.1d
# Repository: https://github.com/the-alphabet-cartel/ash-nlp
# Community: The Alphabet Cartel - https://discord.gg/alphabetcartel  
# =============================================================================

# GLOBAL ASH ECOSYSTEM VARIABLES
# AUTHENTICATION & SECURITY
# MODELS & AI CONFIGURATION
# THRESHOLDS & CRISIS DETECTION  
# ANALYSIS PARAMETERS
# SERVER CONFIGURATION
# LOGGING & MONITORING
# STORAGE & PATHS
# PERFORMANCE & OPTIMIZATION
# FEATURE FLAGS
# RATE LIMITING & SAFETY
```

**Expected Output**: Production-ready `.env.template` with complete documentation

### **Step 9: Update All Managers for Unified System** ⏳ **PENDING**
**Objective**: Ensure all managers use unified configuration system

**Actions**:
- [ ] Update all manager files to use unified ConfigManager
- [ ] Remove direct `os.getenv()` calls throughout codebase
- [ ] Ensure factory function pattern compliance
- [ ] Maintain Clean v3.1 architecture throughout
- [ ] Preserve dependency injection patterns
- [ ] Preserve `GLOBAL_LOG_LEVEL` and related global variables
- [ ] Convert to full manager-based approach for consistency
- [ ] `server_config_manager.get_network_settings()` style

**Expected Output**: All managers using consistent environment variable access

### **Step 10: Comprehensive Testing & Validation** ⏳ **PENDING**
**Objective**: Validate complete system functionality with cleaned configuration

**Testing Actions**:
- [ ] Create comprehensive Phase 3d test suite
- [ ] Update Phase 3a-3c test suites for new variable names
- [ ] Validate all Clean v3.1 architecture patterns
- [ ] Test factory functions with unified configuration
- [ ] Verify ThresholdMappingManager, CrisisPatternManager, AnalysisParametersManager functionality
- [ ] Production readiness validation

**Expected Output**: 100% passing comprehensive test suite

---

## 🎯 **Success Criteria**

### **Technical Success Indicators**
- [ ] **Single Configuration Manager**: All environment variables accessed through unified system
- [ ] **No Variable Duplication**: Each functionality has exactly one environment variable
- [ ] **Consistent Naming**: All variables follow `NLP_CATEGORY_FUNCTION` or preserved `GLOBAL_*` pattern
- [ ] **Complete Documentation**: Every variable documented in `.env.template`
- [ ] **JSON + ENV Pattern**: All variables have JSON defaults with environment overrides
- [ ] **Clean v3.1 Compliance**: Factory functions and dependency injection maintained

### **Functional Success Indicators**  
- [ ] **Phase 3a-3c Preservation**: All previous functionality remains operational
- [ ] **Crisis Detection**: Core NLP crisis detection continues working
- [ ] **Threshold Management**: Mode-aware threshold system operational
- [ ] **Pattern Analysis**: Crisis pattern detection functional
- [ ] **Analysis Parameters**: Algorithm parameters configurable
- [ ] **System Health**: All endpoints responding correctly

### **Operational Success Indicators**
- [ ] **Easy Configuration**: Clear, documented `.env.template` for deployment
- [ ] **Maintainable Code**: No scattered environment variable access
- [ ] **Testing Coverage**: Comprehensive test suite for all functionality
- [ ] **Production Ready**: System ready for deployment with cleaned configuration

---

## 🎉 **Phase 3d Status: Implementation In Progress**

**Current Step**: Step 1 - Complete Environmental Variable Audit  
**Next Action**: Begin comprehensive codebase scan for all environment variable usage  
**Architecture Compliance**: Clean v3.1 architecture maintained throughout

---

## 📈 **NEXT PHASE PREPARATION**

**Phase 4a: Crisis Detection Functionality Audit**
- **Scope**: Comprehensive audit of crisis detection algorithms and accuracy
- **Objective**: Validate and optimize mental health crisis detection capabilities
- **Prerequisites**: ✅ Phase 3d environmental variable cleanup complete

---

## 📝 **Implementation Notes**

### **Critical Considerations**
- **Cutover Strategy**: Complete system break and rebuild approach chosen
- **GLOBAL_* Preservation**: Ecosystem compatibility maintained
- **Manager Consolidation**: Single ConfigManager for all environment variables
- **Phase Integration**: All Phase 3a-3c work must remain functional
- **Testing Impact**: Previous test suites will need updating for new variable names

### **Key Decisions Made**
1. **Complete cutover** rather than backward compatibility
2. **Priority order**: Models/Thresholds → Analysis → Server → Logging → Features  
3. **Naming convention**: `NLP_CATEGORY_FUNCTION` with `GLOBAL_*` preservation
4. **Single manager**: Consolidate ConfigManager and EnvConfigManager
5. **Comprehensive testing**: Full Phase 3d test suite creation

---

**Status**: 🚀 **READY TO BEGIN STEP 4 - IMPLEMENT ANALYSIS PARAMETERS CLEANUP**
**Architecture**: Clean v3.1 with Single Configuration Manager Target  
**Community Impact**: Mental health crisis detection system with unified, maintainable configuration management for The Alphabet Cartel LGBTQIA+ community! 🏳️‍🌈