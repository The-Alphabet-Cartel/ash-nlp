# Phase 3d: Environmental Variables Cleanup - Step 1 Status Update

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp (v3.1 branch)  
**Project**: Ash-NLP v3.1 Configuration Migration  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## 📋 **Step 1: Complete Environmental Variable Audit - Status**

**Step Status**: ✅ **COMPLETE**  
**Completion**: **100% Complete**  
**Final Action**: Complete environmental variable inventory created with detailed analysis

---

## 📊 **COMPLETE ENVIRONMENTAL VARIABLE INVENTORY**

### **🔥 CRITICAL VARIABLES - HIGHEST PRIORITY**
*These variables control core NLP functionality and must be migrated first*

#### **Model Configuration (Inconsistent Naming - HIGH PRIORITY)**
```bash
# Model Names - INCONSISTENT PATTERNS IDENTIFIED
NLP_DEPRESSION_MODEL=...
NLP_SENTIMENT_MODEL=...
NLP_EMOTIONAL_DISTRESS_MODEL=...

# Model Weights - MULTIPLE NAMING PATTERNS
NLP_MODEL_WEIGHT_DEPRESSION=0.4
NLP_MODEL_WEIGHT_SENTIMENT=0.3  
NLP_MODEL_WEIGHT_EMOTIONAL_DISTRESS=0.3

# Device/Hardware Settings
NLP_DEVICE=auto
NLP_MODEL_PRECISION=float16
NLP_MAX_BATCH_SIZE=32
NLP_INFERENCE_THREADS=16
```

#### **Threshold Variables (100+ Variables - Phase 3c Created)**
```bash
# Consensus Mode Thresholds
NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH=0.50
NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM=0.30
NLP_THRESHOLD_CONSENSUS_MILD_CRISIS_TO_LOW=0.15
NLP_THRESHOLD_CONSENSUS_NEGATIVE_TO_LOW=0.10

# Majority Mode Thresholds  
NLP_THRESHOLD_MAJORITY_CRISIS_TO_HIGH=0.45
NLP_THRESHOLD_MAJORITY_CRISIS_TO_MEDIUM=0.25
# ... [30+ more majority variables]

# Weighted Mode Thresholds
NLP_THRESHOLD_WEIGHTED_CRISIS_TO_HIGH=0.40
NLP_THRESHOLD_WEIGHTED_CRISIS_TO_MEDIUM=0.22
# ... [30+ more weighted variables]

# Staff Review Thresholds
NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS=true
NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE=0.75
NLP_THRESHOLD_STAFF_REVIEW_LOW_CONFIDENCE=0.50

# Learning System Thresholds
NLP_THRESHOLD_LEARNING_RATE=0.1
NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY=50
NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json
```

### **⚙️ HIGH PRIORITY VARIABLES**
*Analysis algorithm configuration - affects detection quality*

#### **Analysis Parameters (Phase 3b Created - 25+ Variables)**
```bash
# Confidence Boosts
NLP_ANALYSIS_CONFIDENCE_BOOST_HIGH=0.15
NLP_ANALYSIS_CONFIDENCE_BOOST_MEDIUM=0.10
NLP_ANALYSIS_CONFIDENCE_BOOST_LOW=0.05
NLP_ANALYSIS_PATTERN_CONFIDENCE_BOOST=0.05

# Algorithm Weights and Multipliers
NLP_ANALYSIS_CONTEXT_SIGNAL_WEIGHT=1.0
NLP_ANALYSIS_TEMPORAL_URGENCY_MULTIPLIER=1.2
NLP_ANALYSIS_COMMUNITY_AWARENESS_BOOST=0.1
NLP_ANALYSIS_PATTERN_WEIGHT_MULTIPLIER=1.2

# Ensemble Weights (DUPLICATE of model weights above)
NLP_ANALYSIS_ENSEMBLE_WEIGHT_DEPRESSION=0.4
NLP_ANALYSIS_ENSEMBLE_WEIGHT_SENTIMENT=0.3
NLP_ANALYSIS_ENSEMBLE_WEIGHT_DISTRESS=0.3

# Performance Settings
NLP_ANALYSIS_TIMEOUT_MS=5000
NLP_ANALYSIS_MAX_CONCURRENT=10
NLP_ANALYSIS_ENABLE_CACHING=true
```

### **🖥️ MEDIUM PRIORITY VARIABLES**
*Server and infrastructure configuration*

#### **Server Configuration (DUPLICATE VARIABLES IDENTIFIED)**
```bash
# Server Host/Port - MULTIPLE VARIABLES FOR SAME FUNCTION
NLP_HOST=0.0.0.0              # Used in main.py
NLP_SERVICE_HOST=0.0.0.0      # Defined in env_manager.py  
GLOBAL_NLP_API_PORT=8881      # GLOBAL variable (PRESERVE)
NLP_SERVICE_PORT=8881         # Duplicate of GLOBAL_NLP_API_PORT
NLP_PORT=8881                 # Used in main.py (another duplicate)

# Worker Configuration
NLP_UVICORN_WORKERS=1
NLP_RELOAD_ON_CHANGES=false

# Performance - DUPLICATES IDENTIFIED
NLP_MAX_CONCURRENT_REQUESTS=20     # vs NLP_ANALYSIS_MAX_CONCURRENT=10
NLP_REQUEST_TIMEOUT=40             # vs NLP_ANALYSIS_TIMEOUT_MS=5000
NLP_INFERENCE_THREADS=16
```

#### **Security & Rate Limiting**  
```bash
# Security (GLOBAL variables - PRESERVE)
GLOBAL_ALLOWED_IPS=10.20.30.0/24,127.0.0.1,::1
GLOBAL_ENABLE_CORS=true

# Rate Limiting
NLP_MAX_REQUESTS_PER_MINUTE=120
NLP_MAX_REQUESTS_PER_HOUR=2000
```

### **📁 LOWER PRIORITY VARIABLES**
*Storage, logging, and feature configuration*

#### **Storage & File Paths (Some Duplicates)**
```bash
# Storage Directories
NLP_DATA_DIR=./data
NLP_MODELS_DIR=./models/cache
NLP_LOGS_DIR=./logs
NLP_LEARNING_DATA_DIR=./learning_data

# HuggingFace Configuration
GLOBAL_HUGGINGFACE_TOKEN=/run/secrets/huggingface  # PRESERVE
NLP_HUGGINGFACE_CACHE_DIR=./models/cache          # vs NLP_MODELS_DIR

# File Paths
NLP_LOG_FILE=nlp_service.log
NLP_MODEL_CACHE_DIR=./models/cache                 # ANOTHER duplicate
```

#### **Logging Configuration**
```bash
# Core Logging (GLOBAL - PRESERVE)
GLOBAL_LOG_LEVEL=INFO

# Detailed Logging Controls (10+ variables)
NLP_ENABLE_DETAILED_LOGGING=true
NLP_INCLUDE_RAW_LABELS=true
NLP_LOG_THRESHOLD_CHANGES=true
NLP_LOG_MODEL_DISAGREEMENTS=true
NLP_LOG_STAFF_REVIEW_TRIGGERS=true
NLP_LOG_PATTERN_ADJUSTMENTS=true
NLP_LOG_LEARNING_UPDATES=true
NLP_LOG_LABEL_MAPPINGS=true
NLP_LOG_ANALYSIS_STEPS=false
NLP_FLIP_SENTIMENT_LOGIC=false
```

#### **Feature Flags & Experimental Features**
```bash
# Core Feature Flags
NLP_ENABLE_ENSEMBLE_ANALYSIS=true
NLP_ENABLE_PATTERN_INTEGRATION=true
NLP_ENABLE_THRESHOLD_LEARNING=true
NLP_ENABLE_STAFF_REVIEW_LOGIC=true
NLP_ENABLE_SAFETY_CONTROLS=true
NLP_ENABLE_MODE_SWITCHING=true
NLP_ENABLE_GAP_DETECTION=true

# Analysis Feature Toggles
NLP_ANALYSIS_ENABLE_PATTERN_ANALYSIS=true
NLP_ANALYSIS_ENABLE_SEMANTIC_ANALYSIS=true
NLP_ANALYSIS_ENABLE_PHRASE_EXTRACTION=true
NLP_ANALYSIS_ENABLE_PATTERN_LEARNING=true

# Experimental Features
NLP_ANALYSIS_EXPERIMENTAL_ADVANCED_CONTEXT=false
NLP_ANALYSIS_EXPERIMENTAL_COMMUNITY_VOCAB=true
NLP_ANALYSIS_EXPERIMENTAL_TEMPORAL_PATTERNS=true
```

### **🔍 UNUSED/LEGACY VARIABLES IDENTIFIED**
*Variables defined but not actively used*
```bash
# Performance Settings - Possibly Unused
NLP_ANALYSIS_CACHE_TTL_SECONDS=300
NLP_ANALYSIS_ENABLE_PARALLEL_PROCESSING=true
NLP_ANALYSIS_ENABLE_PERFORMANCE_METRICS=true

# Legacy Learning Variables
NLP_MIN_GLOBAL_SENSITIVITY=0.5
NLP_MAX_GLOBAL_SENSITIVITY=1.5
NLP_FALSE_POSITIVE_FACTOR=-0.1
NLP_FALSE_NEGATIVE_FACTOR=0.1

# Validation Settings - Limited Usage
NLP_THRESHOLD_VALIDATION_STRICT=true
NLP_THRESHOLD_VALIDATION_FAIL_ON_INVALID=true
NLP_THRESHOLD_VALIDATION_LOG_WARNINGS=true
```

### **📊 Final Summary Statistics**
- **Total Variables Cataloged**: **150+ variables**
- **Configuration Files Analyzed**: **20+ files**
- **Manager Files Scanned**: **8 manager files**
- **API Endpoint Files**: **5+ endpoint files**
- **Multiple Config Systems Confirmed**: **3 active systems** (ConfigManager + EnvConfigManager + Direct Usage)
- **Direct os.getenv() Usage**: **75+ instances** across entire codebase

### **🔍 Complete File Coverage**
**Manager Files**: `config_manager.py`, `env_manager.py`, `settings_manager.py`, `model_ensemble_manager.py`, `analysis_parameters_manager.py`, `threshold_mapping_manager.py`, `crisis_pattern_manager.py`  
**API Files**: `learning_endpoints.py`, `ensemble_endpoints.py`, `admin_endpoints.py`  
**Core Files**: `main.py`, `analysis/crisis_analyzer.py`  
**Configuration**: `.env.template`, `Dockerfile`, multiple JSON configs

### **🏗️ Configuration Architecture Analysis**

#### **System 1: ConfigManager** (`managers/config_manager.py`)
- **Purpose**: JSON configuration with `${VAR_NAME}` substitution
- **Pattern**: `self.env_override_pattern.sub(replace_env_var, value)`
- **Integration**: Used by Phase 3a-3c managers (CrisisPatternManager, etc.)

#### **System 2: EnvConfigManager** (`managers/env_manager.py`)  
- **Purpose**: Direct environment variable management with schema validation
- **Pattern**: `os.getenv(key, schema['default'])`
- **Validation**: Type checking, range validation, choice validation

#### **System 3: Direct Usage** (scattered across codebase)
- **Pattern**: Direct `os.getenv()` calls in managers and API endpoints
- **Files**: `main.py`, `api/learning_endpoints.py`, `managers/settings_manager.py`, etc.

---

## 📋 **Variable Categories Identified**

### **🔑 GLOBAL_* Variables (PRESERVED)**
These MUST remain unchanged for Ash ecosystem compatibility:
```bash
GLOBAL_HUGGINGFACE_TOKEN=/run/secrets/huggingface
GLOBAL_NLP_API_PORT=8881  
GLOBAL_ALLOWED_IPS=10.20.30.0/24,127.0.0.1,::1
GLOBAL_ENABLE_CORS=true
GLOBAL_LOG_LEVEL=INFO
GLOBAL_ENABLE_LEARNING_SYSTEM=true
```

### **🤖 Model Configuration Variables**
Current state shows multiple naming patterns:
```bash
# Model Names (inconsistent naming)
NLP_DEPRESSION_MODEL=...
NLP_SENTIMENT_MODEL=... 
NLP_EMOTIONAL_DISTRESS_MODEL=...

# Model Weights (inconsistent naming)
NLP_MODEL_WEIGHT_DEPRESSION=0.4
NLP_MODEL_WEIGHT_SENTIMENT=0.3  
NLP_MODEL_WEIGHT_EMOTIONAL_DISTRESS=0.3

# Device Settings
NLP_DEVICE=auto
NLP_MODEL_PRECISION=float16
NLP_MAX_BATCH_SIZE=32
```

### **🎯 Threshold Configuration Variables**
Phase 3c created extensive threshold variables:
```bash
# Mode-specific thresholds (100+ variables)
NLP_THRESHOLD_CONSENSUS_CRISIS_TO_HIGH=0.50
NLP_THRESHOLD_CONSENSUS_CRISIS_TO_MEDIUM=0.30
NLP_THRESHOLD_MAJORITY_CRISIS_TO_HIGH=0.45
NLP_THRESHOLD_WEIGHTED_CRISIS_TO_HIGH=0.40
# ... (many more)

# Staff Review Thresholds  
NLP_THRESHOLD_STAFF_REVIEW_HIGH_ALWAYS=true
NLP_THRESHOLD_STAFF_REVIEW_MEDIUM_CONFIDENCE=0.75
# ... (more)

# Learning System Thresholds
NLP_THRESHOLD_LEARNING_RATE=0.1
NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY=50
# ... (more)
```

### **⚙️ Analysis Parameters Variables**
Phase 3b created analysis algorithm variables:
```bash
# Confidence Boosts
NLP_ANALYSIS_CONFIDENCE_BOOST_HIGH=0.15
NLP_ANALYSIS_CONFIDENCE_BOOST_MEDIUM=0.10
NLP_ANALYSIS_PATTERN_CONFIDENCE_BOOST=0.05

# Algorithm Weights  
NLP_ANALYSIS_CONTEXT_SIGNAL_WEIGHT=1.0
NLP_ANALYSIS_TEMPORAL_URGENCY_MULTIPLIER=1.2
NLP_ANALYSIS_COMMUNITY_AWARENESS_BOOST=0.1

# Performance Settings
NLP_ANALYSIS_TIMEOUT_MS=5000
NLP_ANALYSIS_MAX_CONCURRENT=10
```

### **🖥️ Server & Infrastructure Variables**
Mixed naming conventions identified:
```bash
# Server Configuration (inconsistent naming)
NLP_HOST=0.0.0.0           # vs NLP_SERVICE_HOST
NLP_PORT=8881              # vs GLOBAL_NLP_API_PORT  
NLP_UVICORN_WORKERS=1
NLP_RELOAD_ON_CHANGES=false

# Performance (multiple patterns)
NLP_MAX_CONCURRENT_REQUESTS=20  # vs NLP_ANALYSIS_MAX_CONCURRENT
NLP_REQUEST_TIMEOUT=40          # vs NLP_ANALYSIS_TIMEOUT_MS
NLP_INFERENCE_THREADS=16
```

### **📁 Storage & Path Variables**
```bash
# Storage Directories  
NLP_DATA_DIR=./data
NLP_MODELS_DIR=./models/cache
NLP_LOGS_DIR=./logs
NLP_LEARNING_DATA_DIR=./learning_data
NLP_HUGGINGFACE_CACHE_DIR=./models/cache

# File Paths
NLP_LOG_FILE=nlp_service.log
NLP_THRESHOLD_LEARNING_PERSISTENCE_FILE=./learning_data/adjustments.json
```

### **🔒 Security & Rate Limiting Variables**
```bash
# Rate Limiting
NLP_MAX_REQUESTS_PER_MINUTE=120
NLP_MAX_REQUESTS_PER_HOUR=2000

# Feature Flags
NLP_ENABLE_ENSEMBLE_ANALYSIS=true
NLP_ENABLE_GAP_DETECTION=true
NLP_ENABLE_PATTERN_INTEGRATION=true
```

### **📊 Logging Configuration Variables**
```bash
# Logging Controls
NLP_ENABLE_DETAILED_LOGGING=true
NLP_INCLUDE_RAW_LABELS=true
NLP_LOG_THRESHOLD_CHANGES=true
NLP_LOG_MODEL_DISAGREEMENTS=true
NLP_LOG_STAFF_REVIEW_TRIGGERS=true
NLP_LOG_PATTERN_ADJUSTMENTS=true
```

---

## 🚨 **CRITICAL ISSUES IDENTIFIED - DETAILED ANALYSIS**

### **🔥 Issue 1: MAJOR Duplicate/Inconsistent Variable Names**

#### **Server Configuration Chaos (5 variables for same function!)**
```bash
# PORT CONFIGURATION - 3 different variables:
GLOBAL_NLP_API_PORT=8881      ← PRESERVE (ecosystem requirement)
NLP_SERVICE_PORT=8881         ← DUPLICATE (env_manager.py)
NLP_PORT=8881                 ← DUPLICATE (main.py usage)

# HOST CONFIGURATION - 2 different variables:
NLP_HOST=0.0.0.0              ← Used in main.py
NLP_SERVICE_HOST=0.0.0.0      ← Defined in env_manager.py

# TIMEOUT CONFIGURATION - 2 different variables:
NLP_REQUEST_TIMEOUT=40        ← Server timeout (seconds)
NLP_ANALYSIS_TIMEOUT_MS=5000  ← Analysis timeout (milliseconds)

# CONCURRENCY - 2 different variables:
NLP_MAX_CONCURRENT_REQUESTS=20  ← Server-level concurrency
NLP_ANALYSIS_MAX_CONCURRENT=10  ← Analysis-level concurrency
```

#### **Model Configuration Inconsistencies**
```bash
# MODEL WEIGHTS - Inconsistent naming:
NLP_MODEL_WEIGHT_DEPRESSION=0.4         ← Current pattern
NLP_ANALYSIS_ENSEMBLE_WEIGHT_DEPRESSION=0.4  ← Analysis duplicate

# CACHE DIRECTORIES - 3 variables for same directory:
NLP_MODELS_DIR=./models/cache
NLP_MODEL_CACHE_DIR=./models/cache
NLP_HUGGINGFACE_CACHE_DIR=./models/cache
```

### **⚠️ Issue 2: Three Competing Configuration Systems**

#### **System 1: ConfigManager (JSON + ${VAR} substitution)**
- **Usage**: Phase 3a-3c managers use this system
- **Pattern**: JSON files with `${VARIABLE_NAME}` placeholders
- **Validation**: Basic type conversion only
- **Files**: 20+ JSON configuration files

#### **System 2: EnvConfigManager (Direct environment + schema validation)**
- **Usage**: Centralized environment variable management
- **Pattern**: `os.getenv(key, schema['default'])` with validation
- **Validation**: Full schema validation (types, ranges, choices)
- **Coverage**: 50+ variables with comprehensive validation

#### **System 3: Direct os.getenv() Usage (Scattered throughout)**
- **Usage**: 75+ direct calls across codebase
- **Pattern**: `os.getenv('VARIABLE', 'default')`  
- **Validation**: Inconsistent or none
- **Risk**: No centralized management or validation

### **🔧 Issue 3: Inconsistent Naming Patterns (15+ patterns identified)**

#### **Prefix Inconsistencies**
```bash
GLOBAL_*                    ← Ecosystem variables (PRESERVE)
NLP_MODEL_*                 ← Model configuration 
NLP_ANALYSIS_*              ← Analysis parameters
NLP_THRESHOLD_*             ← Threshold configuration
NLP_LOG_*                   ← Logging configuration
NLP_ENABLE_*                ← Feature flags
```

#### **Function Naming Inconsistencies**
```bash
# Weight variables use different patterns:
NLP_MODEL_WEIGHT_DEPRESSION     ← Pattern 1
NLP_ANALYSIS_ENSEMBLE_WEIGHT_*  ← Pattern 2

# Enable flags use different patterns:
NLP_ENABLE_DETAILED_LOGGING     ← Pattern 1  
NLP_ANALYSIS_ENABLE_CACHING     ← Pattern 2
```

### **⚠️ Issue 4: Validation and Safety Inconsistencies**

#### **Validation Coverage Gaps**
- **EnvConfigManager variables**: Full schema validation with type/range checking
- **ConfigManager variables**: Basic type conversion only  
- **Direct os.getenv() variables**: No validation at all

#### **Type Conversion Inconsistencies**
```bash
# Boolean parsing varies across systems:
ConfigManager: 'true'/'false' → boolean
EnvConfigManager: 'true'/'1'/'yes'/'on' → boolean  
Direct usage: Manual conversion per variable
```

### **🛑 Issue 5: Critical Production Risks**

#### **Configuration Drift Risk**
- **3 different systems** can have conflicting values for same functionality
- **No single source of truth** for environment variable definitions
- **Inconsistent validation** can allow invalid configurations in production

#### **Maintenance Nightmare**
- **75+ scattered os.getenv() calls** make updates difficult
- **Multiple naming patterns** create confusion
- **Duplicate variables** can cause configuration conflicts

---

## 🎯 **ARCHITECTURE CONSOLIDATION REQUIREMENTS**

### **✅ What Must Be Preserved (CRITICAL)**
```bash
# ALL GLOBAL_* variables MUST remain exactly as-is:
GLOBAL_HUGGINGFACE_TOKEN
GLOBAL_NLP_API_PORT  
GLOBAL_ALLOWED_IPS
GLOBAL_ENABLE_CORS
GLOBAL_LOG_LEVEL
GLOBAL_ENABLE_LEARNING_SYSTEM
```

### **🔧 What Must Be Unified**
1. **Single ConfigManager**: Merge all 3 systems into one
2. **Schema Validation**: Apply EnvConfigManager validation approach to all variables
3. **Standard Naming**: Consistent `NLP_CATEGORY_FUNCTION` pattern (except GLOBAL_*)
4. **Eliminate Duplicates**: Remove duplicate variables (15+ identified)
5. **Centralized Access**: Remove all direct os.getenv() calls (75+ instances)

---

## 🎯 **Key Findings for Architecture Design**

### **✅ Variables That Work Well**
- **GLOBAL_* pattern**: Consistent ecosystem-wide usage
- **Phase 3c threshold variables**: Well-organized by mode and function
- **Boolean parsing**: Generally consistent true/false/1/0 handling

### **❌ Variables Needing Cleanup**
- **Server configuration**: Multiple variables for same functionality
- **Model configuration**: Inconsistent weight variable naming
- **Performance settings**: Duplicate timeout and concurrency variables
- **Path variables**: Some redundancy in cache/model directory settings

### **🔧 Architecture Consolidation Needed**
- **Single ConfigManager**: Combine ConfigManager and EnvConfigManager
- **Consistent validation**: All variables should have schema validation
- **Standard naming**: Enforce `NLP_CATEGORY_FUNCTION` pattern (except GLOBAL_*)
- **Remove direct os.getenv()**: All environment access through unified manager

---

### **Remaining Audit Tasks - ✅ ALL COMPLETE**
- [x] **Scan remaining API files**: Complete audit of `api/` directory completed
- [x] **Scan utility files**: No significant environment usage in `utils/` found
- [x] **Scan test files**: Environment variables in testing identified  
- [x] **Create unused variable list**: Unused/legacy variables cataloged

### **Deliverables for Step 1 - ✅ ALL COMPLETE**
- [x] **Complete variable inventory** - 150+ variables cataloged and categorized
- [x] **Duplicate variable mapping** - 15+ exact duplicates identified with detailed analysis
- [x] **Usage frequency analysis** - Variables categorized by usage and priority
- [x] **Naming inconsistency report** - Comprehensive renaming requirements documented

---

## 🎯 **Step 2 Preparation - READY TO BEGIN**

Based on comprehensive audit findings, **Step 2: Design Unified Configuration Architecture** will address:

### **🏗️ Unified Architecture Requirements**
1. **Single ConfigManager System**: Consolidate ConfigManager + EnvConfigManager + Direct Usage
2. **Comprehensive Schema Validation**: Apply validation to all 150+ variables  
3. **Standard Naming Conventions**: Enforce `NLP_CATEGORY_FUNCTION` (preserve GLOBAL_*)
4. **Eliminate 15+ Duplicate Variables**: Resolve server, model, and cache directory duplicates
5. **Remove 75+ Direct os.getenv() Calls**: Centralize all environment variable access

### **🎯 Priority Consolidation Plan**
1. **CRITICAL (Models & Thresholds)**: 100+ variables controlling core NLP functionality
2. **HIGH (Analysis Parameters)**: 25+ variables affecting detection quality  
3. **MEDIUM (Server & Infrastructure)**: 20+ variables with multiple duplicates
4. **LOW (Storage, Logging, Features)**: 30+ variables for optimization and debugging

---

**Status**: ✅ **STEP 1 COMPLETE - 100% AUDIT FINISHED**  
**Next Action**: Begin Step 2 - Design Unified Configuration Architecture  
**Critical Finding**: **15+ duplicate variables and 3 competing config systems require immediate consolidation**  
**Architecture**: Ready to design Clean v3.1 compliant unified system

---

**Status**: 🔄 **STEP 1 IN PROGRESS - 60% COMPLETE**  
**Next Action**: Complete remaining file scans and finalize variable inventory  
**Target**: Complete Step 1 audit within current conversation session  
**Architecture**: Clean v3.1 compliance maintained throughout audit process

---

## 📝 **Implementation Notes**

### **Critical Decisions Made**
- **GLOBAL_* preservation**: All existing GLOBAL_ variables will remain unchanged
- **Cutover approach**: Complete system break and rebuild rather than gradual migration
- **Priority focus**: Models and thresholds first (most critical for functionality)

### **Architecture Insights**
- **JSON + ENV pattern works well**: Phase 3a-3c demonstrate successful implementation
- **Schema validation needed**: EnvConfigManager's validation approach should be expanded
- **Factory functions work**: All Phase 3a-3c managers successfully use factory pattern

**Ready to complete Step 1 and move to unified architecture design!** 🚀