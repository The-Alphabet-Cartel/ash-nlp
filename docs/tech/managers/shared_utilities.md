<!-- ash-nlp/docs/tech/managers/shared_utilities.md -->
<!--
Shared Utilities Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Shared Utilities Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

## 🎯 **Manager Purpose**

The **SharedUtilitiesManager** is a cornerstone utility manager. It consolidates 150+ duplicate methods from 14 managers into 15 core utilities, achieving approximately 90% code reduction while providing best-in-class implementations for universal patterns.

**Primary Responsibilities:**
- Provide premium utility methods with gold standard implementations
- Offer universal configuration processing patterns used by all managers
- Handle type conversion with comprehensive validation and error handling  
- Manage configuration loading with environment variable substitution
- Provide validation utilities with intelligent fallback mechanisms
- Deliver structured error handling with contextual logging

---

## 🔧 **Core Methods**

### **Premium Utilities (Tier 1 - Best-in-Class Implementations):**

#### **`safe_bool_convert(value: Any, default: bool, param_name: str) -> bool`**
**Source**: logging_config_manager._safe_bool_conversion() - GOLD STANDARD  
**Benefits**: ALL 14 managers

Converts any value to boolean with intelligent fallbacks:
- Handles string values: 'true'/'false', 'yes'/'no', 'on'/'off', '1'/'0', 'enabled'/'disabled'
- Processes numeric values: 1/0, floats converted to boolean logic
- Provides comprehensive logging with parameter context
- Returns safe defaults when conversion impossible
- Eliminates 20+ duplicate boolean conversion methods system-wide

#### **`get_setting_with_type_conversion(section: str, key: str, expected_type: type, default: Any, param_name: str) -> Any`**
**Source**: performance_config_manager._get_performance_setting() - EXCELLENT  
**Benefits**: 12 managers

Retrieves configuration settings with automatic type conversion:
- Supports int, float, bool, str type conversions with validation
- Uses UnifiedConfigManager for configuration access
- Delegates to specialized conversion methods (safe_bool_convert, safe_int_convert)
- Handles missing configurations gracefully with defaults
- Eliminates 15+ duplicate setting retrieval patterns

#### **`get_nested_config_setting(path: str, default: Any, fallback_paths: List[str]) -> Any`**
**Source**: server_config_manager._get_setting_with_defaults() - EXCELLENT  
**Benefits**: 11 managers

Retrieves nested configuration values with intelligent fallback:
- Supports dot-separated paths (e.g., "server.host.port")
- Tries multiple fallback paths automatically
- Provides comprehensive logging of fallback usage
- Handles complex nested dictionary navigation
- Eliminates 12+ duplicate nested access patterns

#### **`get_boolean_setting(key: str, default: bool, environment_override: bool) -> bool`**
**Source**: feature_config_manager._get_feature_flag() - VERY GOOD  
**Benefits**: 10 managers

Retrieves boolean settings with feature flag patterns:
- Supports environment variable overrides
- Uses safe_bool_convert for robust conversion
- Handles feature flag enable/disable patterns
- Provides configuration hierarchy (env → config → default)
- Eliminates 8+ duplicate boolean setting methods

### **Configuration Processing Utilities (Universal Patterns):**

#### **`load_json_with_env_substitution(file_path: str, env_prefix: str, required: bool) -> Dict[str, Any]`**
Loads JSON configuration files with environment variable substitution:
- Supports ${VAR_NAME} and ${VAR_NAME:default_value} patterns  
- Handles missing files based on required flag
- Provides comprehensive error handling for JSON parsing
- Enables dynamic configuration with environment flexibility
- Used by all managers requiring JSON configuration loading

#### **`get_config_section_safely(section_name: str, fallback: Dict) -> Dict[str, Any]`**
Safely retrieves configuration sections with fallback support:
- Returns dictionary copy to prevent modification issues
- Provides fallback dictionaries when sections missing
- Validates section data types for safety
- Comprehensive error handling with logging
- Universal pattern for safe section access

#### **`apply_env_overrides(config_data: Dict, env_prefix: str) -> Dict[str, Any]`**
Applies environment variable overrides to configuration:
- Supports nested key mapping (ENV_SECTION_KEY → section.key)
- Preserves original configuration structure
- Handles underscore-to-dot conversion for hierarchical keys
- Returns modified copy without affecting original
- Standard pattern for environment variable integration

#### **`get_with_fallback(primary_key: str, fallback_keys: List[str], default: Any) -> Any`**
Configuration value retrieval with fallback key chains:
- Tries primary key first, then fallback keys in order
- Logs which fallback key was used for debugging
- Returns default when all keys fail
- Supports complex configuration migration scenarios
- Universal pattern for backward compatibility

#### **`validate_config_structure(config_data: Dict, required_sections: List[str], schema: Dict) -> List[str]`**
Validates configuration structure against requirements:
- Checks for required sections and proper data types
- Validates against optional schema definitions
- Returns list of validation issues for processing
- Supports complex nested structure validation
- Standard validation pattern across all managers

#### **`execute_safely(operation_name: str, operation_func, *args, **kwargs) -> Any`**
Executes operations with comprehensive error handling:
- Tracks operation status and results
- Provides contextual error logging with operation details
- Returns appropriate fallback values based on operation type
- Maintains operation history for debugging
- Universal error handling pattern for critical operations

### **Type Conversion Utilities:**

#### **`safe_int_convert(value: Any, default: int, min_val: int, max_val: int, param_name: str) -> int`**
Converts values to integers with range validation:
- Handles int, float, string conversions with validation
- Enforces minimum and maximum value constraints
- Provides detailed logging for conversion failures
- Returns bounded values when outside acceptable range
- Eliminates 10+ duplicate integer conversion methods

#### **`safe_float_convert(value: Any, default: float, min_val: float, max_val: float, param_name: str) -> float`**
Converts values to floats with range validation:
- Supports all numeric type conversions with validation
- Enforces floating-point range constraints
- Handles precision and boundary condition issues
- Comprehensive error handling with parameter context
- Eliminates 8+ duplicate float conversion methods

### **Validation Utilities:**

#### **`validate_range(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float], param_name: str) -> bool`**
Validates numeric values within specified ranges:
- Supports both integer and float validation
- Handles None values for unbounded ranges
- Provides detailed logging for validation failures
- Returns boolean results for conditional processing
- Universal validation pattern for numeric constraints

#### **`validate_type(value: Any, expected_type: Union[type, tuple], param_name: str) -> bool`**
Validates values match expected types:
- Supports single types or tuple of acceptable types
- Handles numeric type cross-compatibility (int/float)
- Provides meaningful error messages for type mismatches
- Special handling for string conversion scenarios
- Standard type validation across all managers

#### **`validate_bounds(value: Union[int, float], bounds: Dict[str, Union[int, float]], param_name: str) -> bool`**
Validates values against operational bounds dictionaries:
- Uses bounds dictionaries with 'min' and/or 'max' keys
- Delegates to validate_range for actual validation
- Handles malformed bounds dictionaries gracefully
- Supports flexible bounds specification patterns
- Universal bounds checking for configuration values

### **Error Handling Utilities:**

#### **`handle_error_with_fallback(error: Exception, fallback_value: Any, context: str, operation: str) -> Any`**
Comprehensive error handling with structured logging:
- Records detailed error information with full context
- Updates operation status tracking for debugging
- Provides appropriate fallback values based on operation type
- Maintains error history for system monitoring
- Universal error handling pattern preventing system failures

---

## 🤝 **Dependencies**

### **Required Dependencies:**
- **UnifiedConfigManager** - Configuration access and environment variables
- **json** - JSON configuration file parsing and processing
- **os** - Environment variable access and file system operations
- **re** - Regular expressions for environment variable substitution
- **pathlib.Path** - File system path operations and validation
- **logging** - Comprehensive logging for all utility operations

### **Integration Points:**
- **Called by**: ALL 14 managers in the system (universal dependency)
- **Provides to**: Type conversion, validation, configuration processing, error handling
- **Critical for**: System stability, configuration management, code quality, maintainability

---

## 🏗️ **Architecture Integration**

### **Clean Compliance:**
- **Factory Function**: `create_shared_utilities_manager()` with validation
- **Dependency Injection**: Accepts UnifiedConfigManager as sole dependency
- **Error Handling**: Comprehensive fallback mechanisms for all operations
- **Configuration Access**: Uses UnifiedConfigManager patterns throughout

### **Integration Pattern:**
```
UnifiedConfigManager → SharedUtilitiesManager → ALL OTHER MANAGERS
                            ↓
                    Universal Utilities Layer
                  (Type Conversion, Validation, 
                   Configuration, Error Handling)
```

---

## ⚠️ **Critical Production Features**

### **Code Quality Improvements:**
- **Eliminates duplication** - Single source of truth for common operations
- **Best-in-class implementations** - Gold standard methods from top managers
- **Comprehensive testing** - All utilities thoroughly tested and validated
- **Universal patterns** - Consistent behavior across entire system

### **System Reliability:**
- **Comprehensive error handling** - Graceful degradation for all operations
- **Safe type conversions** - Prevents type-related runtime errors
- **Configuration validation** - Ensures system stability through validation
- **Fallback mechanisms** - Maintains system operation during failures

### **Developer Experience:**
- **Single import** - All utilities available from one manager
- **Consistent APIs** - Standardized method signatures and behavior
- **Comprehensive logging** - Detailed context for debugging and monitoring
- **Clear documentation** - Each utility method fully documented with examples

### **Performance Benefits:**
- **Optimized implementations** - Best-performing versions of each utility
- **Reduced memory footprint** - Single implementation vs 150+ duplicates
- **Faster initialization** - Shared utilities reduce manager initialization time
- **Improved maintainability** - Changes in one place benefit entire system

---

*Shared Utilities Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
