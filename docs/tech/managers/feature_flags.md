<!-- ash-nlp/docs/tech/managers/feature_flags.md -->
<!--
API Guide for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Feature Flags Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

# FeatureConfigManager Documentation

The FeatureConfigManager handles configuration for feature flag management and system capability toggles within the Ash-NLP crisis detection system.

---

## Overview

FeatureConfigManager provides centralized management of feature flags and system capabilities, enabling dynamic system behavior control and experimental feature deployment while maintaining production stability.

### Core Responsibilities
- **Feature flag management** - Dynamic enabling/disabling of system capabilities
- **Configuration validation** - Ensures feature flag consistency and validity
- **System capability control** - Manages which analysis features are active
- **Experimental feature support** - Safe deployment of new capabilities

---

## Manager Interface

### Factory Function
```python
def create_feature_config_manager(unified_config: UnifiedConfigManager) -> FeatureConfigManager
```

### Core Methods
- `get_feature_flags()` - Retrieves current feature flag configuration
- `is_feature_enabled(feature_name: str)` - Checks if specific feature is enabled
- `validate_feature_config()` - Validates feature flag configuration consistency
- `update_feature_flag(flag_name: str, enabled: bool)` - Runtime feature flag updates

---

## Configuration Structure

### JSON Configuration (`config/feature_flags.json`)
```json
{
...TBD...
}
```

### Environment Variable Overrides
- `ASH_FEATURE_ANALYSIS_DETAILED_LOGGING` - Override detailed logging feature
- `ASH_FEATURE_API_ADMIN_ENDPOINTS` - Override admin endpoint availability
- `ASH_FEATURE_PERFORMANCE_CACHING` - Override caching feature

---

## Integration Points

### Dependencies
- **UnifiedConfigManager** - Primary configuration access and environment variable integration
- **SharedUtilitiesManager** - Validation utilities and common configuration patterns

### Used By
- **CrisisAnalyzer** - Feature flag checks for analysis capabilities
- **API Endpoints** - Administrative feature availability checks
- **Performance Systems** - Performance feature toggle management

---

## Error Handling and Resilience

### Graceful Degradation
- **Invalid feature flags** - Default to safe, conservative feature settings
- **Configuration errors** - Log warnings and continue with basic feature set
- **Missing feature sections** - Use hardcoded fallback feature configuration

### Production Safety
- **Conservative defaults** - Unknown features default to disabled
- **Validation logging** - Clear error messages for configuration issues
- **Runtime stability** - Feature flag errors never crash the system

---

## Testing and Validation

### Configuration Testing
- **Feature flag validation** - Ensures all feature flags are properly typed
- **Environment override testing** - Validates environment variable precedence
- **Default configuration testing** - Confirms fallback behavior

### Integration Testing
- **Manager interaction testing** - Validates proper integration with dependent managers
- **Runtime feature toggling** - Tests dynamic feature enabling/disabling
- **Performance impact testing** - Ensures feature flags don't degrade performance

---

*Feature Flags Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
