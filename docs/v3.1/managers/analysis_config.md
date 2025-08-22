# Analysis Parameters Manager Documentation

**File**: `managers/analysis_config_manager.py`  
**Phase**: 3e Step 1.1 Documentation Audit  
**Status**: 🔄 **IN PROGRESS**  
**Factory Function**: `create_analysis_config_manager(config_manager)`  
**Dependencies**: UnifiedConfigManager  
**FILE VERSION**: v3.1-3e-5.7-1
**LAST MODIFIED**: 2025-08-21

---

## 🎯 **Manager Purpose**

The **AnalysisConfigManager** is responsible for loading, validating, and providing access to all analysis parameters used throughout the crisis detection system. It acts as the single source of truth for configuration parameters that control the behavior of various analysis components.

**Primary Responsibilities:**
- Load analysis parameters from JSON configuration files
- Provide validated configuration for ensemble analysis, thresholds, learning systems
- Handle environment variable overrides via UnifiedConfigManager
- Ensure parameter validation and error handling with sensible fallbacks

---

## 🔧 **Core Methods**

### **Configuration Loading Methods:**
1. **`load_parameters()`** - Main method to load all analysis parameters
2. **`_load_full_config()`** - Internal method to load complete configuration
3. **`_apply_environment_overrides(config)`** - Apply environment variable overrides

### **Primary Parameter Access Methods:**
1. **`get_ensemble_parameters()`** - Parameters for ensemble model analysis
2. **`get_threshold_parameters()`** - Threshold configuration for decision making
3. **`get_learning_parameters()`** - Learning system configuration
4. **`get_pattern_matching_parameters()`** - Pattern matching behavior settings
5. **`get_confidence_scoring_parameters()`** - Confidence calculation settings

### **Specialized Configuration Methods:**
1. **`get_performance_parameters()`** - Performance and timing settings
2. **`get_integration_settings()`** - Integration with other components
3. **`get_debugging_settings()`** - Debug and logging configuration  
4. **`get_experimental_features()`** - Experimental feature flags

---

## 🤝 **Shared Methods (Potential for SharedUtilitiesManager)**

### **Configuration Validation:**
- **`_validate_parameters(params)`** - Comprehensive parameter validation
- **`_validate_ensemble_params(params)`** - Ensemble-specific validation
- **`_validate_threshold_params(params)`** - Threshold-specific validation
- **`_validate_learning_params(params)`** - Learning-specific validation

### **Type Conversion & Error Handling:**
- **Float/int conversion with bounds checking** (used in multiple get methods)
- **Dictionary merging with defaults** (used across all parameter methods)
- **Exception handling with fallback values** (standardized pattern)

### **JSON Processing:**
- **Configuration loading patterns** (could be shared)
- **Environment override application** (used by multiple managers)
- **Nested dictionary access with fallbacks** (common pattern)

---

## 🧠 **Learning Methods (for LearningSystemManager)**

### **Learning Parameter Configuration:**
1. **`get_learning_parameters()`** - Complete learning system configuration
   - Learning rate, decay schedule, momentum settings
   - Feedback weights and sample requirements
   - Sensitivity bounds and adjustment factors
   - Severity multipliers for different crisis levels

### **Learning-Specific Validation:**
1. **Learning parameter bounds validation** (within `_validate_learning_params`)
   - Learning rate validation (0.0001 to 0.1)
   - Decay schedule validation (exponential/linear/constant)
   - Confidence adjustment bounds (0.01 to 1.0)
   - Adjustments per day limits (1 to 1000)

---

## 📊 **Analysis Methods (Crisis Analysis Specific)**

### **Analysis Configuration:**
1. **`get_ensemble_parameters()`** - Ensemble analysis settings
2. **`get_confidence_scoring_parameters()`** - Confidence calculation rules
3. **`get_pattern_matching_parameters()`** - Pattern analysis behavior

### **Analysis Validation:**
1. **Ensemble parameter validation** (model weights, voting strategies)
2. **Confidence parameter validation** (scoring weights, thresholds)
3. **Pattern matching validation** (matching strategies, sensitivity)

---

## 🔗 **Dependencies**

### **Required Dependencies:**
- **UnifiedConfigManager** - All configuration access
- **logging** - Error handling and debugging

### **Configuration Files:**
- **`config/analysis_config.json`** - Primary configuration
- **Environment variables** - Via UnifiedConfigManager overrides

### **Integration Points:**
- **Called by**: CrisisAnalyzer, ModelCoordinationManager, CrisisThresholdManager
- **Provides to**: All managers requiring analysis parameters

---

## 🌍 **Environment Variables**

**Accessed via UnifiedConfigManager only - no direct environment access**

### **Learning System Variables (via UnifiedConfigManager):**
- Learning rate, decay schedule, momentum
- Feedback weights and adjustment limits
- Sensitivity bounds and factors

### **Analysis Configuration Variables:**
- Ensemble weights and voting strategies  
- Confidence scoring parameters
- Pattern matching sensitivity

---

## 🏗️ **Integration Points**

### **Upstream Dependencies:**
- **UnifiedConfigManager** - Configuration loading and environment overrides

### **Downstream Consumers:**
- **CrisisAnalyzer** - Analysis parameters for crisis detection
- **ModelCoordinationManager** - Ensemble configuration
- **CrisisThresholdManager** - Threshold parameters
- **LearningSystemManager** (Future) - Learning parameters

### **Configuration Flow:**
```
JSON Config → UnifiedConfigManager → AnalysisConfigManager → Consumer Managers
```

---

## 🔍 **Method Overlap Analysis**

### **High Overlap Methods (Candidates for SharedUtilitiesManager):**
1. **Parameter validation patterns** - Used across multiple managers
2. **Type conversion with bounds checking** - Common throughout system
3. **Exception handling with fallbacks** - Standardized error handling
4. **Dictionary merging with defaults** - Configuration pattern

### **Learning-Specific Methods (for LearningSystemManager):**
1. **`get_learning_parameters()`** - Core learning configuration
2. **Learning parameter validation** - Learning-specific bounds and rules

### **Analysis-Specific Methods (Stays in AnalysisConfigManager):**
1. **`get_ensemble_parameters()`** - Ensemble analysis configuration
2. **`get_confidence_scoring_parameters()`** - Crisis confidence calculation
3. **`get_pattern_matching_parameters()`** - Pattern analysis settings

---

## 📋 **Consolidation Recommendations**

### **Move to SharedUtilitiesManager:**
- Generic parameter validation methods
- Type conversion with bounds checking
- Error handling patterns with fallbacks
- JSON configuration loading utilities

### **Extract to LearningSystemManager:**
- `get_learning_parameters()` method
- Learning-specific parameter validation
- Learning rate and adjustment calculation methods

### **Keep in AnalysisConfigManager:**
- Crisis analysis specific parameters
- Ensemble configuration methods  
- Confidence scoring parameters
- Pattern matching configuration

---

## ✅ **Phase 3e Step 1.1 Status**

**Manager**: analysis_config_manager.py  
**Documentation**: ✅ **COMPLETE**  
**Core Methods**: 12 identified  
**Shared Methods**: 4 identified for SharedUtilitiesManager  
**Learning Methods**: 2 identified for LearningSystemManager  
**Analysis Methods**: 6 remain in current manager  

**Next Manager**: crisis_threshold_manager.py