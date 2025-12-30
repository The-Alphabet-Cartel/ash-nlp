<!-- ash-nlp/docs/tech/managers/context_analysis.md -->
<!--
API Guide for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Context Analysis Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

---

**File**: `managers/analysis_config.py`  
**Factory Function**: `create_analysis_config_manager(unified_config_manager)`  
**Dependencies**: UnifiedConfigManager  

---

## Manager Purpose

The **ContextAnalysisManager** provides crisis analysis configuration parameters and algorithm settings for the detection system. After Phase 3e consolidation, it focuses specifically on analysis algorithm configuration while previously shared functionality has been extracted to specialized managers.

**Primary Responsibilities:**
- Provide ensemble analysis parameters and algorithm configuration
- Manage confidence scoring parameters and pattern matching settings
- Handle analysis timeout and performance configuration
- Support contextual weighting and crisis detection parameters
- Maintain integration settings and debugging configuration
---

## Core Methods

### Analysis Algorithm Configuration

### Performance and Integration Settings

---

## Dependencies

### Required Dependencies
- **UnifiedConfigManager** - Configuration access and environment variable management
- **logging** - Error handling and status tracking
- **datetime** - Timestamp generation and validation tracking
- **json** - Configuration file parsing and processing

### Integration Points
- **Called by**: {TBD}
- **Provides to**: {TBD}
- **Critical for**: {TBD}

---

## Environment Variables

**Analysis Configuration Variables:**
- **Ensemble settings** - Model weights and ensemble mode configuration  
- **Confidence parameters** - Confidence scoring and threshold settings
- **Pattern matching** - Pattern detection sensitivity and weights
- **Performance settings** - Timeout limits and optimization flags
- **Integration modes** - System integration and compatibility settings

---

## Architecture Integration

### Clean Compliance
- **Factory Function**: `create_analysis_config_manager()` with dependency validation
- **Dependency Injection**: Accepts UnifiedConfigManager as required dependency
- **Error Handling**: Comprehensive fallback mechanisms for configuration loading
- **Configuration Access**: Uses UnifiedConfigManager patterns throughout system

---

## Configuration Structure

### JSON Configuration Sections
```json
{
...TBD...
}
```

### Environment Variable Overrides
- **NLP_ENSEMBLE_WEIGHTS** - Override model ensemble weights
- **NLP_CONFIDENCE_BOOST** - Override confidence boost settings
- **NLP_PATTERN_SENSITIVITY** - Override pattern detection sensitivity
- **NLP_ANALYSIS_TIMEOUT** - Override analysis timeout limits

---

## Production Considerations

### Performance Impact
- **Reduced complexity**: Fewer methods mean faster initialization
- **Focused responsibility**: Cleaner configuration access patterns
- **Better caching**: Specialized configuration managers enable targeted caching
- **Improved maintainability**: Clear separation of concerns reduces debugging time

### System Reliability
- **Error isolation**: Failures in one configuration area don't affect others
- **Graceful degradation**: Each manager can fall back independently
- **Validation separation**: Specialized validation for each configuration type
- **Monitoring clarity**: Clearer metrics for each configuration area

### Migration Safety
- **Backward compatibility**: Factory function maintains same interface
- **Gradual transition**: Methods include migration references for developers
- **Comprehensive testing**: Phase 3e integration tests validate all changes
- **Documentation coverage**: Complete migration guide for all extracted methods

---

*Context Analysis Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
