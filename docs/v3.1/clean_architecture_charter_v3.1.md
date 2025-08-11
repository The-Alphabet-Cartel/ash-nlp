# Clean v3.1 Architecture Charter - Ash-NLP
## Sacred Principles - NEVER TO BE VIOLATED

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## 🏛️ **IMMUTABLE ARCHITECTURE RULES**

### **Rule #1: Factory Function Pattern - MANDATORY**
- **ALL managers MUST use factory functions** - `create_[manager_name]()`
- **NEVER call constructors directly**
- **Factory functions enable**: dependency injection, testing, consistency
- **Examples**: `create_models_manager()`, `create_crisis_pattern_manager()`, `create_settings_manager()`

### **Rule #2: Dependency Injection - REQUIRED**
- **All managers accept dependencies through constructor parameters**
- **UnifiedConfigManager is always the first parameter**
- **Additional managers passed as named parameters**
- **Clean separation of concerns maintained**

### **Rule #3: Phase-Additive Development - SACRED**
- **New phases ADD functionality, never REMOVE**
- **Maintain backward compatibility within phase**
- **Each phase builds on previous phases' foundations**
- **Phase 3a + Phase 3b + Phase 3c = cumulative enhancement**

### **Rule #4: JSON Configuration + Environment Overrides - STANDARD**
- **All configuration externalized to JSON files**
- **JSON configuration files set default values**
- **Environment variables override JSON defaults**
- **No hardcoded configuration in source code**
- **UnifiedConfigManager handles all configuration loading**

### **Rule #5: Fail-Fast Validation - CRITICAL**
- **Invalid configurations prevent system startup**
- **Comprehensive validation at initialization**
- **Clear error messages for configuration issues**
- **Graceful fallbacks where appropriate, fail-fast where critical**

---

## 🔧 **MANAGER IMPLEMENTATION STANDARDS**

### **Required Manager Structure:**
```python
class [Manager]Manager:
    def __init__(self, config_manager, [additional_managers...]):
        """Constructor with dependency injection"""
        # Standard initialization pattern
    
    def get_[functionality](self):
        """Standard getter methods"""
        # Implementation
    
    def validate_[aspect](self):
        """Standard validation methods"""
        # Implementation

def create_[manager]_manager([parameters]) -> [Manager]Manager:
    """Factory function - MANDATORY"""
    return [Manager]Manager([parameters])

__all__ = ['[Manager]Manager', 'create_[manager]_manager']
```

### **Required Integration Pattern:**
```python
# In main.py or integration code - ALWAYS use factory functions
from managers.[manager]_manager import create_[manager]_manager

manager = create_[manager]_manager(
    config_manager=config_manager,
    [additional_managers...]
)
```

---

## 🔧 **JSON CONFIGURATION FILE STANDARDS**

### **Required JSON Structure:**
**Filename**:
- `*descriptiveName*_*configurationType*.json`
- Examples:
  - analysis_parameters.json
  - learning_settings.json
  - crisis_patterns.json

**JSON Structure**
```json
{
  [...]
  "*setting_category*": {
    "description": "*settingDescription*",
    "*setting_name*": "${*ENV_VAR*}",
    [...moreSettings...],
    "defaults": {
      "*setting_name*": *default_value*,
      [...moreSettings...],
    },
    "validation": {
      [...categoryValidationValues...],
    }
  },
  [...],
}
```

**Example**
```json
{
  [...]
  "crisis_thresholds": {
    "description": "Core crisis level mapping thresholds for analysis algorithms",
    "high": "${NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH}",
    "medium": "${NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM}",
    "low": "${NLP_ANALYSIS_CRISIS_THRESHOLD_LOW}",
    "defaults": {
      "high": 0.55,
      "medium": 0.28,
      "low": 0.16
    },
    "validation": {
      "range": [0.0, 1.0],
      "type": "float",
      "ordering": "high > medium > low"
    }
  },
  [...]
}
```

---

## 📋 **PHASE INTEGRATION REQUIREMENTS**

### **Phase 3a: Crisis Pattern Manager**
- **Principle**: All crisis patterns externalized to JSON
- **Integration**: CrisisPatternManager used throughout system
- **Factory**: `create_crisis_pattern_manager(config_manager)`

### **Phase 3b: Analysis Parameters Manager** 
- **Principle**: All algorithm parameters externalized to JSON
- **Integration**: AnalysisParametersManager integrated with SettingsManager
- **Factory**: `create_analysis_parameters_manager(config_manager)`

### **Phase 3c: Threshold Mapping Manager**
- **Principle**: All thresholds and mappings externalized to JSON with mode-awareness
- **Integration**: ThresholdMappingManager integrated throughout analysis pipeline
- **Factory**: `create_threshold_mapping_manager(config_manager, model_ensemble_manager)`

### **Phase 3d: Environmental Variable Cleanup**
- **Principle**: Complete audit and cleanup of the Environmental Variables system and config manager
- **Integration**: consolidating multiple environment variable management approaches into a single, clean, comprehensive system
- **Factory**: `create_server_config_manager(config_manager)`

### **Future Phases**
- **MUST follow established patterns**
- **MUST use factory functions**
- **MUST maintain cumulative integration**
- **MUST preserve all previous phase functionality**

---

## 🚨 **VIOLATION PREVENTION**

### **Before Making ANY Architectural Change:**
1. **Does this maintain factory function pattern?** ✅ Required
2. **Does this preserve all previous phase functionality?** ✅ Required  
3. **Does this follow dependency injection principles?** ✅ Required
4. **Does this maintain JSON + environment configuration?** ✅ Required
5. **Does this include proper validation and error handling?** ✅ Required

### **Red Flags - IMMEDIATE STOP:**
- ❌ Direct constructor calls in production code
- ❌ Removing functionality from previous phases
- ❌ Hardcoding configuration values
- ❌ Breaking manager integration patterns
- ❌ Bypassing factory functions

---

## 🎯 **ARCHITECTURAL SUCCESS METRICS**

### **Code Quality Indicators:**
- ✅ All managers use factory functions
- ✅ All configuration externalized
- ✅ All phases cumulative and functional
- ✅ Clean dependency injection throughout
- ✅ Comprehensive error handling

### **Integration Health:**
- ✅ Tests use same patterns as production code
- ✅ Factory functions handle all initialization
- ✅ Managers properly integrated across phases
- ✅ Configuration overrides working consistently

---

## 💪 **COMMITMENT**

**This architecture serves The Alphabet Cartel community by providing:**
- **Reliable mental health crisis detection**
- **Maintainable and extensible codebase** 
- **Clear separation of concerns**
- **Professional-grade system design**

**Every architectural decision supports the mission of providing life-saving mental health support to LGBTQIA+ community members.**

---

**Status**: Living Document - Updated with each phase  
**Authority**: Project Lead + AI Assistant Collaboration  
**Enforcement**: Mandatory for ALL code changes  

---

## 🏆 **ARCHITECTURE PLEDGE**

*"I commit to maintaining Clean v3.1 architecture principles in every code change, recognizing that architectural consistency directly impacts the reliability of mental health crisis detection for The Alphabet Cartel community."*