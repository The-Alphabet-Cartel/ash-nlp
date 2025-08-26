<!-- ash-nlp/docs/tech/managers/unified_config.md -->
<!--
Unified Config Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-3d-8.3-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Unified Config Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-3e-8.3-1
**LAST UPDATED**: 2025-08-26
**PHASE**: 3e
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

# UnifiedConfigManager Documentation

The UnifiedConfigManager is the central configuration hub for the Ash-NLP crisis detection system, providing centralized access to all JSON configuration files with environment variable overrides, serving as the foundation for Clean Architecture v3.1 compliance.

---

## Overview

UnifiedConfigManager serves as the single source of truth for all system configuration, implementing the core architectural principle that all configuration access must flow through this centralized manager. It provides the foundation for the entire configuration architecture and enables the 74% performance improvement through optimized configuration access patterns.

### Core Responsibilities
- **Centralized configuration access** - Single point of access for all system configuration
- **JSON configuration loading** - Loading and parsing of all JSON configuration files
- **Environment variable overrides** - Override JSON defaults with environment variables
- **Configuration caching** - Performance-optimized configuration caching
- **Configuration validation** - Ensures configuration consistency and correctness
- **Dynamic configuration updates** - Runtime configuration changes and reloading

### Architectural Significance
UnifiedConfigManager is the **foundational manager** that enables Clean Architecture v3.1 compliance by ensuring **Rule #4: Configuration Access** is consistently followed across all system components.

---

## Manager Interface

### Factory Function
```python
def create_unified_config_manager() -> UnifiedConfigManager
```
*Note: UnifiedConfigManager is the only manager that doesn't require dependencies, as it is the foundation for all other managers.*

### Core Methods
- `get_config_section(section_name: str)` - **Primary method** - Gets configuration section with environment overrides
- `get_full_config()` - Retrieves complete merged configuration
- `reload_configuration()` - Reloads all configuration from files and environment
- `validate_configuration()` - Validates all configuration sections
- `get_environment_overrides()` - Lists all active environment variable overrides
- `update_configuration(section: str, config: dict)` - Runtime configuration updates

---

## Configuration Architecture

### JSON Configuration Files (`config/` directory)
```
config/
├── analysis_config.json       # Crisis analysis configuration
├── crisis_threshold.json      # Crisis detection thresholds
├── feature_flags.json         # System feature toggles
├── label_config.json           # Classification label configuration
├── learning_system.json       # Learning system settings
├── logging_settings.json      # System logging configuration
├── model_coordination.json    # AI model coordination settings
├── patterns_burden.json       # Crisis burden pattern definitions
├── patterns_community.json    # Community-specific patterns
├── patterns_context.json      # Context analysis patterns
├── patterns_crisis.json       # Crisis detection patterns
├── patterns_idiom.json        # Idiomatic expression patterns
├── patterns_temporal.json     # Temporal pattern definitions
├── performance_settings.json  # Performance optimization settings
├── server_config.json         # Server and API configuration
├── setting_config.json        # General application settings
└── storage_settings.json      # Storage and backup configuration
```

### Environment Variable Override System
The UnifiedConfigManager implements a systematic environment variable override system:

```python
# JSON configuration:
{
    "analysis": {
        "max_tokens": 512,
        "confidence_threshold": 0.7
    }
}

# Environment override examples:
ASH_ANALYSIS_MAX_TOKENS=1024
ASH_ANALYSIS_CONFIDENCE_THRESHOLD=0.8
```

### Phase 3e Configuration Pattern
All managers access configuration using the standardized `get_config_section()` pattern:

```python
# Standard Phase 3e configuration access pattern
def create_crisis_analyzer(unified_config: UnifiedConfigManager) -> CrisisAnalyzer:
    config = unified_config.get_config_section('crisis_threshold')
    return CrisisAnalyzer(config)
```

---

## Performance Optimization

### Configuration Caching
- **Lazy loading** - Configuration sections loaded only when requested
- **Parsed configuration caching** - Caches parsed JSON to avoid repeated file I/O
- **Environment variable caching** - Caches environment variable lookups
- **Section-level caching** - Individual configuration sections cached separately

### Phase 3e Performance Integration
The UnifiedConfigManager directly contributes to the 74% performance improvement through:
- **Reduced configuration overhead** - Eliminated redundant configuration loading
- **Optimized environment variable processing** - Efficient environment variable override handling
- **Configuration access patterns** - Standardized access patterns reduce configuration overhead
- **Memory-efficient caching** - Smart caching strategies minimize memory usage

---

## Error Handling and Resilience

### Graceful Degradation
- **Missing configuration files** - Falls back to hardcoded safe defaults with logging
- **JSON parsing errors** - Uses default values for corrupted configuration sections
- **Invalid environment variables** - Ignores invalid overrides and logs warnings
- **Configuration validation failures** - Falls back to safe defaults while logging errors

### Production Safety
- **Non-blocking errors** - Configuration errors never crash the crisis detection system
- **Comprehensive logging** - Clear error messages for all configuration issues
- **Safe defaults** - All configuration sections have safe fallback values
- **Validation before use** - All configuration validated before being used by system components

---

## Clean Architecture v3.1 Compliance

### Foundational Role
UnifiedConfigManager serves as the **architectural foundation** for Clean Architecture compliance:

#### Rule #4: Configuration Access - ENFORCED
- **Single configuration source** - All managers must receive UnifiedConfigManager as first parameter
- **Standardized access patterns** - `get_config_section()` used throughout system
- **No direct configuration access** - All configuration flows through UnifiedConfigManager
- **Environment variable integration** - Centralized environment variable override handling

#### Dependency Injection Support
- **Manager factory pattern** - Enables proper dependency injection for all managers
- **Configuration dependency** - Provides configuration as a service to all system components
- **Testing facilitation** - Enables easy testing through configuration mocking
- **Consistent initialization** - Ensures all managers initialize with proper configuration

---

## Integration Points

### Dependencies
- **None** - UnifiedConfigManager is the foundational manager with no dependencies
- **File System** - Direct access to JSON configuration files in `config/` directory
- **Environment Variables** - Direct access to system environment variables

### Used By
- **All System Managers** - Every manager receives UnifiedConfigManager as first parameter
- **Factory Functions** - All `create_*_manager()` functions use UnifiedConfigManager
- **System Components** - Any component requiring configuration access
- **Testing Framework** - Test utilities for configuration mocking and validation

---

## Configuration Sections

### Core System Configuration
- **`analysis_config`** - Crisis analysis engine configuration
- **`crisis_threshold`** - Crisis detection threshold and severity settings
- **`model_coordination`** - AI model coordination and management settings
- **`performance_settings`** - System performance optimization configuration

### Community and Safety Configuration
- **`patterns_community`** - LGBTQIA+ community-specific pattern definitions
- **`patterns_crisis`** - Crisis detection pattern configurations
- **`feature_flags`** - Community safety and feature toggle settings
- **`logging_settings`** - Privacy-aware logging configuration

### Infrastructure Configuration
- **`server_config`** - API server and deployment configuration
- **`storage_settings`** - Data storage and backup configuration
- **`setting_config`** - General application and operational settings

---

## Dynamic Configuration Management

### Runtime Updates
- **Hot configuration reloading** - Update configuration without system restart
- **Partial configuration updates** - Update individual configuration sections
- **Change propagation** - Notify dependent managers of configuration changes
- **Validation on update** - Ensure configuration updates maintain system consistency

### Configuration Monitoring
- **Change detection** - Monitor configuration files for changes
- **Environment variable monitoring** - Track environment variable changes
- **Configuration drift detection** - Detect when configuration deviates from expected values
- **Audit logging** - Log all configuration changes for compliance and debugging

---

## Testing and Validation

### Configuration Testing
- **JSON schema validation** - Validates all JSON configuration files against schemas
- **Environment override testing** - Tests environment variable override functionality
- **Default value testing** - Ensures all configuration sections have appropriate defaults
- **Cross-section validation** - Validates consistency across related configuration sections

### Integration Testing
- **Manager integration testing** - Tests configuration integration with all system managers
- **Performance testing** - Validates configuration access performance under load
- **Error handling testing** - Tests graceful degradation under various error conditions
- **Hot reload testing** - Tests dynamic configuration updates and reloading

---

## Security and Privacy

### Configuration Security
- **Sensitive data protection** - Ensures sensitive configuration data is properly protected
- **Environment variable security** - Secure handling of sensitive environment variables
- **Configuration access control** - Appropriate access controls for configuration files
- **Audit trail maintenance** - Maintains audit trails for configuration changes

### Community Privacy Protection
- **Privacy-first defaults** - Default configuration values prioritize community member privacy
- **LGBTQIA+ safety configuration** - Configuration options that enhance community safety
- **Data minimization** - Configuration supports data minimization principles
- **Consent management** - Configuration for consent and privacy preference management

---

## Phase 3e Migration Impact

### Configuration Pattern Standardization
- **Universal `get_config_section()` adoption** - All managers now use standardized configuration access
- **Environment variable cleanup** - Systematic cleanup and standardization of environment variables
- **Performance optimization integration** - Configuration patterns optimized for 74% performance improvement
- **Clean Architecture compliance** - 100% Clean Architecture v3.1 Rule #4 compliance achieved

### Consolidation Benefits
- **Reduced configuration complexity** - Simplified configuration access patterns across system
- **Improved maintainability** - Centralized configuration management improves system maintainability
- **Enhanced testability** - Standardized configuration patterns improve testing capabilities
- **Better error handling** - Centralized error handling for all configuration-related issues

---

## Best Practices

### Manager Integration
```python
# Correct Phase 3e pattern for manager creation
def create_example_manager(unified_config: UnifiedConfigManager) -> ExampleManager:
    config = unified_config.get_config_section('example_config')
    return ExampleManager(config)

# Correct configuration access within managers
class ExampleManager:
    def __init__(self, config: dict):
        self.max_retries = config.get('max_retries', 3)
        self.timeout = config.get('timeout_seconds', 30)
```

### Environment Variable Naming
- **Prefix**: Always use `ASH_` prefix for all environment variables
- **Section mapping**: `ASH_SECTION_FIELD_NAME` maps to `section.field_name` in JSON
- **Type conversion**: UnifiedConfigManager handles automatic type conversion
- **Validation**: All environment overrides validated before use

### Configuration Organization
- **Logical grouping**: Group related configuration into appropriate JSON files
- **Minimal nesting**: Keep JSON structure shallow for easier environment variable mapping
- **Clear naming**: Use descriptive names for all configuration keys
- **Documentation**: Document all configuration options and their effects