# Phase 3e Step 5.7 - Manager Renaming and Import Updates
## Comprehensive Tracking Document

**Date Started**: 2025-08-21  
**Current Status**: First Manager 95% Complete - Finishing Remaining Updates  
**Current Manager**: AnalysisParametersManager → AnalysisConfigManager

---

## COMPLETE RENAMING PLAN

### **Managers Requiring Rename + Import Updates (5 managers):**

| Current File | New File | Class Name | Factory Function | Status |
|--------------|----------|------------|------------------|--------|
| `managers/analysis_parameters_manager.py` | `managers/analysis_config.py` | `AnalysisConfigManager` | `create_analysis_config_manager()` | 95% **COMPLETE** |
| `managers/threshold_mapping_manager.py` | `managers/crisis_threshold.py` | `CrisisThresholdManager` | `create_crisis_threshold_manager()` | PENDING |
| `managers/crisis_pattern_manager.py` | `managers/pattern_detection.py` | `PatternDetectionManager` | `create_pattern_detection_manager()` | PENDING |
| `managers/context_pattern_manager.py` | `managers/context_analysis.py` | `ContextAnalysisManager` | `create_context_analysis_manager()` | PENDING |
| `managers/model_ensemble_manager.py` | `managers/model_coordination.py` | `ModelCoordinationManager` | `create_model_coordination_manager()` | PENDING |

### **Managers Requiring Filename-Only Updates (7 managers):**

| Current File | New File | Class Name | Factory Function | Status |
|--------------|----------|------------|------------------|--------|
| `managers/unified_config_manager.py` | `managers/unified_config.py` | `UnifiedConfigManager` | `create_unified_config_manager()` | PENDING |
| `managers/shared_utilities_manager.py` | `managers/shared_utilities.py` | `SharedUtilitiesManager` | `create_shared_utilities_manager()` | PENDING |
| `managers/learning_system_manager.py` | `managers/learning_system.py` | `LearningSystemManager` | `create_learning_system_manager()` | PENDING |
| `managers/feature_config_manager.py` | `managers/feature_config.py` | `FeatureConfigManager` | `create_feature_config_manager()` | PENDING |
| `managers/performance_config_manager.py` | `managers/performance_config.py` | `PerformanceConfigManager` | `create_performance_config_manager()` | PENDING |
| `managers/logging_config_manager.py` | `managers/logging_config.py` | `LoggingConfigManager` | `create_logging_config_manager()` | PENDING |
| `managers/data_storage_manager.py` | `managers/data_storage.py` | `DataStorageManager` | `create_data_storage_manager()` | PENDING |

---

## CURRENT MANAGER: AnalysisParametersManager → AnalysisConfigManager

**Status**: 95% Complete - Finishing remaining updates  
**File**: `managers/analysis_parameters_manager.py` → `managers/analysis_config.py`  
**Class**: `AnalysisParametersManager` → `AnalysisConfigManager`  
**Factory**: `create_analysis_parameters_manager()` → `create_analysis_config_manager()`

### **COMPLETED SUCCESSFULLY:**

1. **NEW FILE CREATED**: `managers/analysis_config.py` (v3.1-3e-5.7-1)
   - Class renamed: `AnalysisParametersManager` → `AnalysisConfigManager`
   - Factory renamed: `create_analysis_parameters_manager` → `create_analysis_config_manager`
   - All 25+ methods preserved exactly
   - All Phase 3e patterns maintained
   - Configuration section `'analysis_parameters'` preserved
   - All migration references intact

2. **MAIN IMPORTS UPDATED**: `managers/__init__.py` (v3.1-3e-5.7-1)
   - Import: `from .analysis_config import AnalysisConfigManager, create_analysis_config_manager`
   - Availability flag: `ANALYSIS_CONFIG_MANAGER_AVAILABLE` (renamed)
   - Exports: Updated to new class and factory names
   - Manager status: Updated key from `'analysis_parameters_manager'` to `'analysis_config_manager'`

### **REMAINING UPDATES TO COMPLETE:**

3. **Test Files** - Update manager key references
   - `tests/phase/3/e/test_basic_integration.py`: Update `all_managers['analysis_parameters']` references

4. **Documentation Updates**
   - `docs/v3.1/managers/analysis_parameters.md` → `docs/v3.1/managers/analysis_config.md`
   - Update references in `docs/v3.1/phase/3/e/4.1_analysis_method_consolidation_plan.md`

5. **File Cleanup**
   - Remove old file `managers/analysis_parameters_manager.py` (after validation)

### **CRITICAL PRESERVATION ACHIEVED:**
- Configuration section name `'analysis_parameters'` unchanged
- All 25+ methods preserved exactly
- Phase 3e `get_config_section()` patterns maintained
- All functionality intact
- Migration references preserved

---

## IMPORT MAPPING ANALYSIS COMPLETE

**Files Found That Import AnalysisParametersManager:**

1. **managers/__init__.py** - UPDATED
   - OLD: `from .analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager`
   - NEW: `from .analysis_config import AnalysisConfigManager, create_analysis_config_manager`

2. **tests/phase/3/e/test_basic_integration.py** - NEEDS UPDATE
   - Usage: `all_managers['analysis_parameters']` - manager key reference
   - Update needed: Change key to match new availability flag

3. **docs/v3.1/managers/analysis_parameters.md** - NEEDS UPDATE
   - References: Factory function and class name documentation
   - Update needed: Rename file and update all references

4. **docs/v3.1/phase/3/e/4.1_analysis_method_consolidation_plan.md** - NEEDS UPDATE
   - References: Multiple references to AnalysisParametersManager in consolidation plan
   - Update needed: Update class name references

---

## DETAILED COMPLETION STEPS

### **Step 1: Update Test Files**
- Search for `'analysis_parameters'` key references in test files
- Update to `'analysis_config'` to match new manager status key
- Validate test functionality

### **Step 2: Update Documentation**
- Rename documentation file
- Update all class and factory function references
- Update consolidation plan references

### **Step 3: Final Validation**
- Test import functionality
- Verify all methods work correctly
- Confirm no broken references

### **Step 4: Cleanup**
- Remove old `managers/analysis_parameters_manager.py` file
- Update tracking document to mark complete

---

## COMMUNICATION CONTINUITY NOTES

**Current Progress**: First manager rename 95% complete  
**Next Action**: Complete remaining updates for AnalysisConfigManager  
**Approach**: One-manager-at-a-time for safety  
**Phase 3e Context**: All managers use get_config_section() patterns  
**Quality Standard**: 100% functionality preservation maintained