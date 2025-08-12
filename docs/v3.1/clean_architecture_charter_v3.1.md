# Clean v3.1 Architecture Charter - Ash-NLP (Production Ready)
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
- **Phase 3a + Phase 3b + Phase 3c + Phase 3d = cumulative enhancement**

### **Rule #4: JSON Configuration + Environment Overrides - STANDARD**
- **All configuration externalized to JSON files**
- **JSON configuration files set default values**
- **Environment variables override JSON defaults**
- **No hardcoded configuration in source code**
- **UnifiedConfigManager handles all configuration loading**

### **Rule #5: Resilient Validation with Smart Fallbacks - PRODUCTION CRITICAL**
- **Invalid configurations trigger graceful fallbacks, not system crashes**
- **Data type validation provides safe defaults with logging**
- **Configuration path issues handled transparently**  
- **System prioritizes **operational continuity** for life-saving functionality**
- **Clear error logging for debugging while maintaining service availability**

---

## 🔧 **MANAGER IMPLEMENTATION STANDARDS**

### **Required Manager Structure:**
```python
class [Manager]Manager:
    def __init__(self, config_manager, [additional_managers...]):
        """Constructor with dependency injection"""
        # Standard initialization pattern with resilient error handling
    
    def get_[functionality](self):
        """Standard getter methods with safe defaults"""
        # Implementation with graceful fallbacks
    
    def validate_[aspect](self):
        """Standard validation methods with resilient behavior"""
        # Validation that logs issues but maintains functionality

def create_[manager]_manager([parameters]) -> [Manager]Manager:
    """Factory function - MANDATORY"""
    return [Manager]Manager([parameters])

__all__ = ['[Manager]Manager', 'create_[manager]_manager']
```

### **Required Integration Pattern:**
```python
# In main.py or integration code - ALWAYS use factory functions
from managers.[manager]_manager import create_[manager]_manager

try:
    manager = create_[manager]_manager(
        config_manager=config_manager,
        [additional_managers...]
    )
except Exception as e:
    logger.error(f"❌ Manager initialization failed: {e}")
    # Use fallback or safe defaults - DO NOT CRASH THE SYSTEM
    manager = create_fallback_manager()
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
      "ordering": "high > medium > low",
      "fallback_behavior": "use_defaults_with_logging"
    }
  },
  [...]
}
```

---

## 🏥 **PRODUCTION RESILIENCE PHILOSOPHY**

### **Mission-Critical System Requirements**
This system serves **The Alphabet Cartel LGBTQIA+ community** by providing **life-saving mental health crisis detection**. Therefore:

#### **🛡️ Operational Continuity Over Perfection**
- **System availability is paramount** - better to run with safe defaults than crash
- **Graceful degradation** when facing configuration issues
- **Comprehensive logging** of all issues for post-incident analysis
- **Self-healing mechanisms** where possible

#### **⚡ Smart Fail-Fast vs. Resilient Behavior**
- **Fail-Fast**: Only for **unrecoverable errors** that would produce dangerous results
- **Resilient**: For **configuration issues**, **missing files**, **invalid data types**
- **Logging**: All issues logged clearly for debugging and monitoring

#### **🔧 Error Handling Hierarchy**
1. **Critical Safety Issues**: Fail-fast (e.g., model corruption, security breaches)
2. **Configuration Problems**: Resilient fallback with logging
3. **Data Type Issues**: Convert to safe defaults with warnings
4. **Path/File Issues**: Use fallbacks or defaults with clear logging
5. **Environment Variable Issues**: Schema-based type conversion with defaults

---

## 📋 **PHASE INTEGRATION REQUIREMENTS**

### **Phase 3a: Crisis Pattern Manager**
- **Principle**: All crisis patterns externalized to JSON
- **Integration**: CrisisPatternManager used throughout system
- **Factory**: `create_crisis_pattern_manager(config_manager)`
- **Resilience**: Falls back to basic patterns if JSON unavailable

### **Phase 3b: Analysis Parameters Manager** 
- **Principle**: All algorithm parameters externalized to JSON
- **Integration**: AnalysisParametersManager integrated with SettingsManager
- **Factory**: `create_analysis_parameters_manager(config_manager)`
- **Resilience**: Uses safe algorithm defaults if parameters unavailable

### **Phase 3c: Threshold Mapping Manager**
- **Principle**: All thresholds and mappings externalized to JSON with mode-awareness
- **Integration**: ThresholdMappingManager integrated throughout analysis pipeline
- **Factory**: `create_threshold_mapping_manager(config_manager, model_ensemble_manager)`
- **Resilience**: Provides conservative thresholds if configuration fails

### **Phase 3d: Environmental Variable Cleanup**
- **Principle**: Complete audit and cleanup of the Environmental Variables system
- **Integration**: Single, clean, comprehensive unified configuration system
- **Factory**: `create_unified_config_manager(config_dir)`
- **Resilience**: Schema-based validation with intelligent type conversion

### **Future Phases**
- **MUST follow established patterns**
- **MUST use factory functions**
- **MUST maintain cumulative integration**
- **MUST preserve all previous phase functionality**
- **MUST implement production-ready resilience**

---

## 🚨 **VIOLATION PREVENTION**

### **Before Making ANY Architectural Change:**
1. **Does this maintain factory function pattern?** ✅ Required
2. **Does this preserve all previous phase functionality?** ✅ Required  
3. **Does this follow dependency injection principles?** ✅ Required
4. **Does this maintain JSON + environment configuration?** ✅ Required
5. **Does this implement resilient error handling?** ✅ **PRODUCTION CRITICAL**
6. **Does this maintain operational continuity for crisis detection?** ✅ **LIFE-SAVING REQUIRED**

### **Red Flags - IMMEDIATE STOP:**
- ❌ Direct constructor calls in production code
- ❌ Removing functionality from previous phases
- ❌ Hardcoding configuration values
- ❌ Breaking manager integration patterns
- ❌ Bypassing factory functions
- ❌ **NEW**: Implementing fail-fast for non-critical configuration issues
- ❌ **NEW**: Allowing system crashes for recoverable problems

---

## 🎯 **ARCHITECTURAL SUCCESS METRICS**

### **Code Quality Indicators:**
- ✅ All managers use factory functions
- ✅ All configuration externalized
- ✅ All phases cumulative and functional
- ✅ Clean dependency injection throughout
- ✅ **Production-ready resilient error handling**

### **Integration Health:**
- ✅ Tests use same patterns as production code
- ✅ Factory functions handle all initialization
- ✅ Managers properly integrated across phases
- ✅ Configuration overrides working consistently
- ✅ **System maintains availability under adverse conditions**

### **Production Readiness:**
- ✅ **Operational continuity preserved** under configuration issues
- ✅ **Comprehensive logging** for debugging and monitoring
- ✅ **Safe fallback mechanisms** for all critical functionality
- ✅ **Crisis detection capability** maintained regardless of configuration state

---

## 💪 **COMMITMENT**

**This architecture serves The Alphabet Cartel community by providing:**
- **Reliable mental health crisis detection** that stays operational
- **Maintainable and extensible codebase** with production-ready resilience
- **Clear separation of concerns** with intelligent error recovery
- **Professional-grade system design** optimized for life-saving service delivery

**Every architectural decision supports the mission of providing continuous, reliable mental health support to LGBTQIA+ community members.**

---

**Status**: Living Document - Updated for Production Resilience (Phase 3d)  
**Authority**: Project Lead + AI Assistant Collaboration  
**Enforcement**: Mandatory for ALL code changes  

---

## 🏆 **ARCHITECTURE PLEDGE**

*"I commit to maintaining Clean v3.1 architecture principles with production-ready resilience in every code change, recognizing that system availability and operational continuity directly impact the ability to provide life-saving mental health crisis detection for The Alphabet Cartel community."*