# Phase 3e Step 5.7 - Manager Renaming and Import Updates
## Comprehensive Tracking Document

**Date Started**: 2025-08-21  
**Current Status**: Planning Phase - No files modified yet  
**Next Action**: Get current version of first manager file

---

## 🎯 **COMPLETE RENAMING PLAN**

### **Managers Requiring Rename + Import Updates (5 managers):**

| Current File | New File | Class Name | Factory Function | Status |
|--------------|----------|------------|------------------|--------|
| `managers/analysis_parameters_manager.py` | `managers/analysis_config.py` | `AnalysisConfigManager` | `create_analysis_config_manager()` | 🔄 **PENDING** |
| `managers/threshold_mapping_manager.py` | `managers/crisis_threshold.py` | `CrisisThresholdManager` | `create_crisis_threshold_manager()` | 🔄 **PENDING** |
| `managers/crisis_pattern_manager.py` | `managers/pattern_detection.py` | `PatternDetectionManager` | `create_pattern_detection_manager()` | 🔄 **PENDING** |
| `managers/context_pattern_manager.py` | `managers/context_analysis.py` | `ContextAnalysisManager` | `create_context_analysis_manager()` | 🔄 **PENDING** |
| `managers/model_ensemble_manager.py` | `managers/model_coordination.py` | `ModelCoordinationManager` | `create_model_coordination_manager()` | 🔄 **PENDING** |

### **Managers Requiring Filename-Only Updates (7 managers):**

| Current File | New File | Class Name | Factory Function | Status |
|--------------|----------|------------|------------------|--------|
| `managers/unified_config_manager.py` | `managers/unified_config.py` | `UnifiedConfigManager` | `create_unified_config_manager()` | 🔄 **PENDING** |
| `managers/shared_utilities_manager.py` | `managers/shared_utilities.py` | `SharedUtilitiesManager` | `create_shared_utilities_manager()` | 🔄 **PENDING** |
| `managers/learning_system_manager.py` | `managers/learning_system.py` | `LearningSystemManager` | `create_learning_system_manager()` | 🔄 **PENDING** |
| `managers/feature_config_manager.py` | `managers/feature_config.py` | `FeatureConfigManager` | `create_feature_config_manager()` | 🔄 **PENDING** |
| `managers/performance_config_manager.py` | `managers/performance_config.py` | `PerformanceConfigManager` | `create_performance_config_manager()` | 🔄 **PENDING** |
| `managers/logging_config_manager.py` | `managers/logging_config.py` | `LoggingConfigManager` | `create_logging_config_manager()` | 🔄 **PENDING** |
| `managers/data_storage_manager.py` | `managers/data_storage.py` | `DataStorageManager` | `create_data_storage_manager()` | 🔄 **PENDING** |

---

## 📋 **STEP 5.7 PROCESS WORKFLOW**

### **Phase 1: Planning and Documentation (Current Phase)**
- [x] Create comprehensive renaming plan
- [x] Identify all 12 managers requiring updates
- [ ] Get current versions of all manager files
- [ ] Create import dependency mapping
- [ ] Validate no conflicts with existing files

### **Phase 2: One-by-one Manager Processing**
**Order**: Start with Analysis Config Manager (analysis_parameters_manager.py)

**Per-Manager Workflow:**
1. **File Preparation**
   - Get current manager file version
   - Analyze all import statements referencing this manager
   - Create complete import update list

2. **File Updates**
   - Rename manager file
   - Update class name (if needed)
   - Update factory function name (if needed)
   - Update internal documentation

3. **Import Updates**
   - Update all importing files throughout codebase
   - Update `managers/__init__.py`
   - Update test files
   - Update any documentation references

4. **Validation**
   - Verify no broken imports
   - Run basic import tests
   - Confirm functionality preserved

### **Phase 3: System Validation**
- [ ] Complete import validation across entire system
- [ ] Run integration tests
- [ ] Update all documentation references
- [ ] Final system validation

---

## 🎯 **CURRENT MANAGER: Analysis Parameters Manager**

**Current Status**: File analyzed - Ready for detailed import mapping  
**File**: `managers/analysis_parameters_manager.py` (v3.1-3e-5.5-6-1)  
**Target**: `managers/analysis_config.py`  
**Class Rename**: `AnalysisParametersManager` → `AnalysisConfigManager`  
**Factory Rename**: `create_analysis_parameters_manager()` → `create_analysis_config_manager()`

### **FILE ANALYSIS COMPLETE:**

**Dependencies (What this manager imports):**
- `os` (standard library)
- `logging` (standard library)
- `typing.Dict, Any, Optional` (standard library)
- `pathlib.Path` (standard library)
- `datetime.datetime` (standard library)
- **Config Manager**: Uses `self.config_manager` (UnifiedConfigManager)

**Key Internal Components:**
- Class: `AnalysisParametersManager`
- Factory: `create_analysis_parameters_manager(config_manager)`
- Exports: `__all__ = ['AnalysisParametersManager', 'create_analysis_parameters_manager']`

**Key Methods (25+ methods):**
- Crisis analysis methods (migrated to CrisisAnalyzer - provide references)
- Learning methods (migrated to LearningSystemManager - provide references)
- Core parameter methods: `get_confidence_boost_parameters()`, `get_phrase_extraction_parameters()`, etc.

**Configuration Access Pattern**: Uses `self.config_manager.get_config_section('analysis_parameters')` - Phase 3e compliant

### **COMPLETE IMPORT MAPPING ANALYSIS:**

**Files Found That Import AnalysisParametersManager:**

1. **managers/__init__.py** - CONFIRMED
   - Import: `from .analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager`
   - Update needed: YES

2. **docs/v3.1/managers/analysis_parameters.md** - CONFIRMED  
   - References: Factory function and class name documentation
   - Update needed: YES

3. **docs/v3.1/phase/3/e/4.1_analysis_method_consolidation_plan.md** - CONFIRMED
   - References: Multiple references to AnalysisParametersManager in consolidation plan
   - Update needed: YES

4. **tests/phase/3/e/test_basic_integration.py** - CONFIRMED
   - Usage: `all_managers['analysis_parameters']` - manager key reference
   - Update needed: YES (may need manager key update)

**Import Patterns Found:**
- Direct import in `__init__.py`: `from .analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager`
- Manager dictionary key: `'analysis_parameters'` (in test files)
- Documentation references throughout docs
- Method consolidation plan references

**Variable/Key References Found:**
- Manager dictionary key: `'analysis_parameters'` 
- Configuration access: `'analysis_parameters'` (config section name - DO NOT CHANGE)
- Test references: `all_managers['analysis_parameters']`

**CRITICAL NOTE**: The configuration section name `'analysis_parameters'` should NOT be changed - only file names, class names, and import statements.

---

## 📝 **PROGRESS TRACKING**

### **Managers Completed**: 0/12
### **Current Manager**: analysis_parameters_manager.py
### **Import Files Updated**: 0
### **Tests Validated**: 0

---

## 🚨 **CRITICAL REMINDERS**

1. **No file modifications until full understanding confirmed**
2. **One manager at a time approach for safety**
3. **Get current file versions before any changes**
4. **Follow get_config_section() patterns established in Phase 3e**
5. **Maintain 100% functionality preservation**
6. **Update this document as we progress**

---

## 💬 **CONVERSATION CONTINUITY NOTES**

**For Next Conversation**: 
- Reference this tracking document
- Continue with current manager: analysis_parameters_manager.py
- Current step: Get current file version and import analysis
- Maintain one-at-a-time approach
- No file modifications until explicitly approved

**Phase 3e Context**: 
- Step 5.6 COMPLETE: Integration testing validated 14 managers working together
- Step 5.7 ACTIVE: Manager renaming and import updates
- All managers use get_config_section() patterns
- Clean Architecture Charter v3.1 compliance maintained