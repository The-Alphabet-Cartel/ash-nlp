# Threshold Mapping Manager Documentation

**File**: `managers/crisis_threshold_manager.py`  
**Phase**: 3e Step 1.1 Documentation Audit  
**Status**: 🔄 **IN PROGRESS**  
**Factory Function**: `create_crisis_threshold_manager(unified_config_manager, model_coordination_manager)`  
**Dependencies**: UnifiedConfigManager, ModelCoordinationManager  
**FILE VERSION**: v3.1-6-1  
**LAST MODIFIED**: 2025-08-22  

---

## 🎯 **Manager Purpose**

The **CrisisThresholdManager** is responsible for managing crisis level thresholds and mappings based on different ensemble modes. It determines crisis levels from confidence scores, manages staff review requirements, and provides mode-aware threshold mappings for the crisis detection system.

**Primary Responsibilities:**
- Map confidence scores to crisis levels (none, low, medium, high) based on ensemble mode
- Determine staff review requirements based on confidence and crisis levels
- Provide mode-specific threshold configurations for different ensemble modes
- Handle learning-based threshold adjustments and validation
- Manage threshold bounds and safety controls

---

## 🔧 **Core Methods**

### **Primary Crisis Determination Methods:**
1. **`determine_crisis_level(confidence, context=None)`** - **CRITICAL** - Maps confidence to crisis level
2. **`requires_staff_review(crisis_level, confidence, disagreement=False)`** - Determines human review needs
3. **`get_current_ensemble_mode()`** - Gets current model ensemble operating mode

### **Configuration Access Methods:**
1. **`get_crisis_level_mapping_for_mode(mode=None)`** - Mode-specific crisis level thresholds
2. **`get_staff_review_thresholds_for_mode(mode=None)`** - Staff review threshold configuration
3. **`get_learning_thresholds()`** - Learning system threshold configuration

### **Threshold Management Methods:**
1. **`get_ensemble_thresholds_for_mode(mode)`** - Complete threshold configuration for mode
2. **`_validate_threshold_config()`** - Validates threshold configuration consistency
3. **`get_validation_status()`** - Returns threshold validation status
4. **`get_threshold_summary()`** - Comprehensive threshold configuration summary

---

## 🤝 **Shared Methods (Potential for SharedUtilitiesManager)**

### **Validation and Error Handling:**
- **`_validate_threshold_config()`** - Comprehensive configuration validation
- **Threshold ordering validation** - Ensures high > medium > low thresholds
- **Range validation** - Validates thresholds are within 0.0-1.0 bounds
- **Exception handling with fallbacks** - Standardized error handling patterns

### **Configuration Processing:**
- **Mode-based configuration access** - Pattern used across multiple managers
- **Dictionary merging with defaults** - Configuration loading pattern
- **Environment variable integration** - Via UnifiedConfigManager patterns

### **Type Conversion & Safety:**
- **Float conversion with bounds checking** - Used for threshold values
- **Safe dictionary access** - Nested configuration access patterns
- **Fallback value assignment** - Default value handling on errors

---

## 🧠 **Learning Methods (for LearningSystemManager)**

### **Learning Threshold Configuration:**
1. **`get_learning_thresholds()`** - Learning system threshold parameters
   - Learning rate for threshold adjustments
   - Maximum adjustments per day limits
   - Minimum confidence required for learning
   - Adjustment bounds and safety limits

### **Adaptive Threshold Management:**
1. **Threshold adjustment methods** (implicit in crisis level determination)
   - Learning-based threshold adaptation
   - False positive/negative adjustment logic
   - Threshold drift management and bounds

### **Learning Integration Points:**
- **Confidence-based learning triggers** - When to apply learning adjustments
- **Threshold adaptation rules** - How to modify thresholds based on feedback
- **Safety bounds for learning** - Prevent excessive threshold drift

---

## 📊 **Analysis Methods (Crisis Analysis Specific)**

### **Crisis Level Determination:**
1. **`determine_crisis_level(confidence, context=None)`** - **CORE ANALYSIS METHOD**
   - Maps confidence scores to crisis levels using mode-specific thresholds
   - Handles different ensemble modes (consensus, majority, weighted)
   - Applies context-aware adjustments

### **Staff Review Logic:**
1. **`requires_staff_review(crisis_level, confidence, disagreement=False)`** - **CRITICAL ANALYSIS**
   - Complex business logic for human intervention requirements
   - Multi-rule system for review determination
   - Safety net for potential false positives/negatives

### **Mode-Aware Analysis:**
1. **Mode-specific threshold application** - Different thresholds per ensemble mode
2. **Threshold boundary analysis** - Borderline case detection
3. **Safety threshold enforcement** - Conservative fallbacks for edge cases

---

## 🔗 **Dependencies**

### **Required Dependencies:**
- **UnifiedConfigManager** - Configuration loading and environment overrides
- **ModelCoordinationManager** - Current ensemble mode detection
- **logging** - Error handling and debugging

### **Configuration Files:**
- **`config/crisis_threshold.json`** - Primary threshold configuration
- **Environment variables** - Via UnifiedConfigManager (e.g., `NLP_THRESHOLD_*`)

### **Integration Points:**
- **Called by**: CrisisAnalyzer, ModelCoordinationManager
- **Provides to**: Crisis level determination, staff review logic
- **Depends on**: Current ensemble mode from ModelCoordinationManager

---

## 🌍 **Environment Variables**

**Accessed via UnifiedConfigManager only - no direct environment access**

### **Threshold Configuration Variables:**
- **`NLP_THRESHOLD_CONSENSUS_*`** - Consensus mode thresholds
- **`NLP_THRESHOLD_MAJORITY_*`** - Majority mode thresholds  
- **`NLP_THRESHOLD_WEIGHTED_*`** - Weighted mode thresholds
- **`NLP_THRESHOLD_STAFF_REVIEW_*`** - Staff review threshold overrides

### **Learning System Variables:**
- **`NLP_THRESHOLD_LEARNING_RATE`** - Learning rate for threshold adjustments
- **`NLP_THRESHOLD_LEARNING_MAX_ADJUSTMENTS_PER_DAY`** - Daily adjustment limits
- **`NLP_THRESHOLD_LEARNING_MIN_CONFIDENCE`** - Minimum confidence for learning

---

## 🏗️ **Integration Points**

### **Upstream Dependencies:**
- **UnifiedConfigManager** - Configuration and environment variable access
- **ModelCoordinationManager** - Current ensemble mode detection

### **Downstream Consumers:**
- **CrisisAnalyzer** - Crisis level determination and staff review logic
- **API endpoints** - Staff review requirements and crisis levels
- **LearningSystemManager** (Future) - Learning threshold configuration

### **Critical Data Flow:**
```
ModelCoordinationManager (mode) → CrisisThresholdManager → Crisis Level → CrisisAnalyzer
```

---

## 🔍 **Method Overlap Analysis**

### **High Overlap Methods (Candidates for SharedUtilitiesManager):**
1. **Configuration validation patterns** - `_validate_threshold_config()` uses common patterns
2. **Range and bounds checking** - Threshold validation logic reusable
3. **Exception handling with fallbacks** - Standardized error handling
4. **Safe dictionary access** - Nested configuration access patterns

### **Learning-Specific Methods (for LearningSystemManager):**
1. **`get_learning_thresholds()`** - Learning system configuration
2. **Threshold adjustment logic** - Adaptive threshold management
3. **Learning bounds validation** - Learning-specific threshold limits

### **Analysis-Specific Methods (Stays in CrisisThresholdManager):**
1. **`determine_crisis_level()`** - **CRITICAL** - Core crisis analysis
2. **`requires_staff_review()`** - **CRITICAL** - Human intervention logic
3. **Mode-specific threshold methods** - Crisis analysis configuration

---

## ⚠️ **Critical Business Logic**

### **Life-Saving Methods (NEVER MOVE):**
1. **`determine_crisis_level()`** - Direct impact on crisis detection accuracy
2. **`requires_staff_review()`** - Human safety intervention logic
3. **Mode-specific threshold access** - Ensures proper crisis level mapping

### **Safety Considerations:**
- **Conservative fallbacks** - Always err on side of higher crisis levels
- **Threshold boundary checks** - Borderline cases require human review
- **Multiple safety nets** - Redundant logic for critical decision points

---

## 📋 **Consolidation Recommendations**

### **Move to SharedUtilitiesManager:**
- Generic configuration validation methods
- Range and bounds checking utilities
- Safe dictionary access patterns
- Error handling with fallback utilities

### **Extract to LearningSystemManager:**
- `get_learning_thresholds()` method
- Learning-based threshold adjustment logic
- Threshold adaptation bounds and validation

### **Keep in CrisisThresholdManager:**
- **`determine_crisis_level()`** - **CRITICAL BUSINESS LOGIC**
- **`requires_staff_review()`** - **CRITICAL SAFETY LOGIC**  
- Mode-specific threshold configuration
- Crisis level mapping logic
- Staff review business rules

---

## ✅ **Phase 3e Step 1.1 Status**

**Manager**: crisis_threshold_manager.py  
**Documentation**: ✅ **COMPLETE**  
**Core Methods**: 8 identified  
**Shared Methods**: 4 identified for SharedUtilitiesManager  
**Learning Methods**: 2 identified for LearningSystemManager  
**Analysis Methods**: 4 remain in current manager (**CRITICAL BUSINESS LOGIC**)  

**Key Finding**: Contains life-saving crisis determination logic that must remain centralized

**Next Manager**: model_coordination_manager.py