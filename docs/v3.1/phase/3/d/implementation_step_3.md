# Phase 3d: Step 3 - Models & Thresholds Cleanup Implementation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp (v3.1 branch)  
**Project**: Ash-NLP v3.1 Configuration Migration  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## 🎯 **Step 3: Implement Models & Thresholds Cleanup**

**Step Status**: 🚀 **IN PROGRESS**  
**Priority**: **CRITICAL** - These variables control core NLP functionality  
**Approach**: **Enhance existing JSON files** and **eliminate duplicate variables**  
**Target**: Model configuration duplicates and inconsistent naming

---

## 🔥 **CRITICAL Variables Being Cleaned Up**

### **Model Configuration Issues to Fix**

#### **🚨 Issue 1: Model Weight Variable Duplicates**
```bash
# CURRENT DUPLICATES:
NLP_MODEL_WEIGHT_DEPRESSION=0.4              # ← Used by ModelEnsembleManager
NLP_ANALYSIS_ENSEMBLE_WEIGHT_DEPRESSION=0.4  # ← DUPLICATE in AnalysisParametersManager

# AFTER CLEANUP:
NLP_MODEL_DEPRESSION_WEIGHT=0.4              # ← SINGLE standardized variable
```

#### **🚨 Issue 2: Inconsistent Model Variable Naming**  
```bash
# CURRENT INCONSISTENT PATTERNS:
NLP_MODEL_WEIGHT_DEPRESSION    # Pattern: NLP_MODEL_WEIGHT_[TYPE]
NLP_DEPRESSION_MODEL          # Pattern: NLP_[TYPE]_MODEL

# AFTER CLEANUP (Consistent Pattern):
NLP_MODEL_DEPRESSION_NAME     # Pattern: NLP_MODEL_[TYPE]_[ATTRIBUTE]
NLP_MODEL_DEPRESSION_WEIGHT   # Pattern: NLP_MODEL_[TYPE]_[ATTRIBUTE]
NLP_MODEL_SENTIMENT_NAME      # Pattern: NLP_MODEL_[TYPE]_[ATTRIBUTE]
NLP_MODEL_SENTIMENT_WEIGHT    # Pattern: NLP_MODEL_[TYPE]_[ATTRIBUTE]
```

#### **🚨 Issue 3: Cache Directory Triplicate Variables**
```bash
# CURRENT TRIPLICATES:
NLP_MODELS_DIR=./models/cache           # ← Used in storage settings
NLP_MODEL_CACHE_DIR=./models/cache      # ← Used in ConfigManager
NLP_HUGGINGFACE_CACHE_DIR=./models/cache # ← Used in model loading

# AFTER CLEANUP:
NLP_STORAGE_MODELS_DIR=./models/cache   # ← SINGLE unified variable
```

---

## 🔧 **Implementation Plan**

### **🎯 Task 1: Enhanced model_ensemble.json**

**File**: `config/model_ensemble.json`  
**Action**: **ENHANCE** (not replace) with standardized variable names  
**Status**: 🔄 **READY TO IMPLEMENT**

#### **Enhanced Model Ensemble Configuration**
```json
{
  "model_ensemble": {
    "version": "3.1d-enhanced",
    "architecture": "clean-v3.1-unified",
    "model_definitions": {
      "depression": {
        "name": "${NLP_MODEL_DEPRESSION_NAME}",
        "weight": "${NLP_MODEL_DEPRESSION_WEIGHT}",
        "cache_dir": "${NLP_STORAGE_MODELS_DIR}",
        "type": "text-classification",
        "purpose": "Depression and mental health crisis detection",
        "pipeline_task": "text-classification"
      },
      "sentiment": {
        "name": "${NLP_MODEL_SENTIMENT_NAME}",
        "weight": "${NLP_MODEL_SENTIMENT_WEIGHT}",
        "cache_dir": "${NLP_STORAGE_MODELS_DIR}",
        "type": "sentiment-analysis",
        "purpose": "Overall emotional sentiment analysis",
        "pipeline_task": "sentiment-analysis"
      },
      "emotional_distress": {
        "name": "${NLP_MODEL_DISTRESS_NAME}",
        "weight": "${NLP_MODEL_DISTRESS_WEIGHT}",
        "cache_dir": "${NLP_STORAGE_MODELS_DIR}",
        "type": "emotion-classification",
        "purpose": "Emotional distress and urgency detection",
        "pipeline_task": "text-classification"
      }
    },
    "ensemble_settings": {
      "mode": "${NLP_ENSEMBLE_MODE}",
      "validation": {
        "ensure_weights_sum_to_one": true,
        "fail_on_invalid_weights": true,
        "validate_model_accessibility": true
      }
    },
    "hardware_settings": {
      "device": "${NLP_HARDWARE_DEVICE}",
      "precision": "${NLP_HARDWARE_PRECISION}",
      "max_batch_size": "${NLP_HARDWARE_MAX_BATCH_SIZE}"
    },
    "defaults": {
      "model_definitions": {
        "depression": {
          "name": "j-hartmann/emotion-english-distilroberta-base",
          "weight": 0.4,
          "cache_dir": "./models/cache"
        },
        "sentiment": {
          "name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
          "weight": 0.3,
          "cache_dir": "./models/cache"
        },
        "emotional_distress": {
          "name": "j-hartmann/emotion-english-distilroberta-base",
          "weight": 0.3,
          "cache_dir": "./models/cache"
        }
      },
      "ensemble_mode": "consensus",
      "hardware_settings": {
        "device": "auto",
        "precision": "float16",
        "max_batch_size": 32
      }
    }
  }
}
```

### **🎯 Task 2: Create storage_settings.json**

**File**: `config/storage_settings.json`  
**Action**: **NEW FILE** for consolidated storage variables  
**Status**: 🔄 **READY TO IMPLEMENT**

#### **New Storage Configuration File**
```json
{
  "storage_configuration": {
    "version": "3.1d",
    "architecture": "clean-v3.1-unified",
    "directories": {
      "data_directory": "${NLP_STORAGE_DATA_DIR}",
      "models_directory": "${NLP_STORAGE_MODELS_DIR}",
      "logs_directory": "${NLP_STORAGE_LOGS_DIR}",
      "learning_directory": "${NLP_STORAGE_LEARNING_DIR}"
    },
    "file_paths": {
      "log_file": "${NLP_STORAGE_LOG_FILE}",
      "learning_persistence_file": "${NLP_STORAGE_LEARNING_FILE}"
    },
    "cache_settings": {
      "huggingface_cache": "${NLP_STORAGE_MODELS_DIR}",
      "enable_model_caching": true,
      "cache_cleanup_on_startup": false
    },
    "defaults": {
      "directories": {
        "data_directory": "./data",
        "models_directory": "./models/cache",
        "logs_directory": "./logs",
        "learning_directory": "./learning_data"
      },
      "file_paths": {
        "log_file": "nlp_service.log",
        "learning_persistence_file": "./learning_data/adjustments.json"
      }
    },
    "validation": {
      "create_directories_on_startup": true,
      "validate_write_permissions": true,
      "fail_on_inaccessible_directories": false
    }
  }
}
```

### **🎯 Task 3: Update ConfigManager for New Variables**

**File**: `managers/config_manager.py`  
**Action**: **ENHANCE** to handle standardized variable names  
**Status**: 🔄 **READY TO IMPLEMENT**

#### **ConfigManager Enhancements Needed**
```python
class ConfigManager:
    def __init__(self, config_dir: str = "/app/config"):
        # ... existing initialization ...
        
        # Add new configuration files
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json',
            'analysis_parameters': 'analysis_parameters.json',
            'performance_settings': 'performance_settings.json',
            'threshold_mapping': 'threshold_mapping.json',
            'storage_settings': 'storage_settings.json',    # NEW
        }
        
    def get_model_configuration(self) -> Dict[str, Any]:
        """Enhanced model configuration with standardized variables"""
        # Update to use new variable names:
        # NLP_MODEL_DEPRESSION_NAME instead of NLP_DEPRESSION_MODEL
        # NLP_MODEL_DEPRESSION_WEIGHT instead of NLP_MODEL_WEIGHT_DEPRESSION
        
    def get_storage_configuration(self) -> Dict[str, Any]:
        """NEW: Get storage configuration with unified directory variables"""
        return self.load_config_file('storage_settings')
```

### **🎯 Task 4: Update .env.template with Clean Variables**

**File**: `.env.template`  
**Action**: **UPDATE** variable names and **REMOVE** duplicates  
**Status**: 🔄 **READY TO IMPLEMENT**

#### **Model Configuration Section (Cleaned)**
```bash
# =============================================================================
# MODEL CONFIGURATION - PHASE 3D CLEAN MIGRATION
# =============================================================================
# Model Names - Standardized Naming Pattern
NLP_MODEL_DEPRESSION_NAME=j-hartmann/emotion-english-distilroberta-base
NLP_MODEL_SENTIMENT_NAME=cardiffnlp/twitter-roberta-base-sentiment-latest
NLP_MODEL_DISTRESS_NAME=j-hartmann/emotion-english-distilroberta-base

# Model Weights - Standardized Naming Pattern
NLP_MODEL_DEPRESSION_WEIGHT=0.4
NLP_MODEL_SENTIMENT_WEIGHT=0.3
NLP_MODEL_DISTRESS_WEIGHT=0.3

# Ensemble Configuration
NLP_ENSEMBLE_MODE=consensus

# Hardware Configuration
NLP_HARDWARE_DEVICE=auto
NLP_HARDWARE_PRECISION=float16
NLP_HARDWARE_MAX_BATCH_SIZE=32

# =============================================================================
# STORAGE CONFIGURATION - PHASE 3D UNIFIED
# =============================================================================
# Storage Directories - DUPLICATES ELIMINATED
NLP_STORAGE_DATA_DIR=./data
NLP_STORAGE_MODELS_DIR=./models/cache
NLP_STORAGE_LOGS_DIR=./logs
NLP_STORAGE_LEARNING_DIR=./learning_data

# File Paths
NLP_STORAGE_LOG_FILE=nlp_service.log  
NLP_STORAGE_LEARNING_FILE=./learning_data/adjustments.json
```

#### **Variables Being REMOVED (Duplicates)**
```bash
# REMOVED DUPLICATES:
# NLP_DEPRESSION_MODEL           → Use NLP_MODEL_DEPRESSION_NAME
# NLP_SENTIMENT_MODEL            → Use NLP_MODEL_SENTIMENT_NAME
# NLP_EMOTIONAL_DISTRESS_MODEL   → Use NLP_MODEL_DISTRESS_NAME
# NLP_MODEL_WEIGHT_DEPRESSION    → Use NLP_MODEL_DEPRESSION_WEIGHT
# NLP_MODEL_WEIGHT_SENTIMENT     → Use NLP_MODEL_SENTIMENT_WEIGHT
# NLP_MODEL_WEIGHT_EMOTIONAL_DISTRESS → Use NLP_MODEL_DISTRESS_WEIGHT
# NLP_ANALYSIS_ENSEMBLE_WEIGHT_* → Use NLP_MODEL_*_WEIGHT
# NLP_MODELS_DIR                 → Use NLP_STORAGE_MODELS_DIR
# NLP_MODEL_CACHE_DIR            → Use NLP_STORAGE_MODELS_DIR
# NLP_HUGGINGFACE_CACHE_DIR      → Use NLP_STORAGE_MODELS_DIR
```

---

## 🔄 **Manager Integration Updates**

### **🎯 Task 5: Update ModelEnsembleManager**

**File**: `managers/model_ensemble_manager.py`  
**Action**: **UPDATE** to use standardized variable names  
**Changes Needed**:

```python
# BEFORE:
env_var = model_config.get('environment_variable')  # Uses old names
weight_str = str(model_config.get('weight', model_config.get('default_weight', 0.33)))

# AFTER: 
# Update to use standardized NLP_MODEL_[TYPE]_[ATTRIBUTE] pattern
# Remove duplicate weight handling
```

### **🎯 Task 6: Remove Duplicates from AnalysisParametersManager**

**File**: `managers/analysis_parameters_manager.py`  
**Action**: **REMOVE** duplicate ensemble weight variables  
**Changes Needed**:

```python
# REMOVE duplicate ensemble weight handling:
# NLP_ANALYSIS_ENSEMBLE_WEIGHT_DEPRESSION → Use ModelEnsembleManager instead
# NLP_ANALYSIS_ENSEMBLE_WEIGHT_SENTIMENT → Use ModelEnsembleManager instead
# NLP_ANALYSIS_ENSEMBLE_WEIGHT_DISTRESS → Use ModelEnsembleManager instead
```

### **🎯 Task 7: Remove EnvConfigManager Duplicates**

**File**: `managers/env_manager.py`  
**Action**: **REMOVE** duplicate variables and **CONSOLIDATE** into ConfigManager  
**Status**: Will be handled in later step (Step 9)

---

## ✅ **Step 3 Success Criteria**

### **Technical Success**
- [ ] **Model variables standardized**: All use `NLP_MODEL_[TYPE]_[ATTRIBUTE]` pattern
- [ ] **Duplicates eliminated**: No more duplicate model/storage variables  
- [ ] **JSON files enhanced**: Existing files updated with new variable names
- [ ] **Storage unified**: Single variable for models directory
- [ ] **ConfigManager enhanced**: Handles new standardized variables

### **Functional Success**
- [ ] **Models load correctly**: All three models initialize with new variable names
- [ ] **Ensemble weights work**: Model weights sum to 1.0 and function correctly
- [ ] **Storage paths work**: All directories created and accessible
- [ ] **Phase 3a-3c preserved**: ThresholdMappingManager and CrisisPatternManager continue working
- [ ] **System stability**: No breaking changes to core functionality

### **Configuration Success**
- [ ] **Environment overrides work**: All new variables can override JSON defaults
- [ ] **Validation working**: Invalid configurations caught during startup
- [ ] **Clean .env.template**: Variables organized and duplicates removed
- [ ] **Factory functions working**: All managers initialize via factory functions

---

## 🚀 **Implementation Order**

### **Phase 1: JSON Configuration Files**
1. ✅ **Create storage_settings.json** - New storage configuration file
2. ✅ **Enhance model_ensemble.json** - Update with standardized variable names
3. ✅ **Update .env.template** - Clean model and storage sections

### **Phase 2: Manager Updates**  
4. ✅ **Update ConfigManager** - Add storage_settings support
5. ✅ **Update ModelEnsembleManager** - Use standardized variable names
6. ✅ **Update AnalysisParametersManager** - Remove duplicate variables

### **Phase 3: Testing & Validation**
7. ✅ **Test model loading** - Verify all models initialize correctly
8. ✅ **Test storage access** - Verify all directories accessible
9. ✅ **Test environment overrides** - Verify all variables can be overridden

---

**Status**: 🚀 **STEP 3 READY FOR IMPLEMENTATION**  
**Next Action**: Create enhanced JSON configuration files  
**Priority**: Start with storage_settings.json and model_ensemble.json enhancements  
**Architecture**: Clean v3.1 compliance maintained throughout implementation

---

## 📝 **Critical Notes**

### **Files to NEVER Modify**
- ✅ `config/threshold_mapping.json` - Phase 3c perfect, don't touch
- ✅ `config/crisis_patterns.json` + pattern files - Phase 3a working, preserve
- ✅ `managers/threshold_mapping_manager.py` - No changes needed
- ✅ `managers/crisis_pattern_manager.py` - No changes needed

### **Preserve During Changes**
- ✅ **Factory function pattern**: All managers continue using `create_*` functions  
- ✅ **Dependency injection**: ConfigManager passed as first parameter
- ✅ **JSON + ENV pattern**: All variables have JSON defaults + environment overrides
- ✅ **Fail-fast validation**: Invalid configurations prevent startup

**Ready to begin Step 3 implementation!** 🚀