<!-- ash-nlp/docs/tech/managers/analysis_config.md -->
<!--
Analysis Config Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-3d-8.3-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Analysis Config Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-3e-8.3-1
**LAST UPDATED**: 2025-08-26
**PHASE**: 3e
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

**File**: `managers/analysis_config.py`  
**Factory Function**: `create_analysis_config_manager(unified_config_manager)`  
**Dependencies**: UnifiedConfigManager  
**Status**: Production Ready - Phase 3e Consolidation Complete  
**Former Name**: AnalysisParametersManager (renamed in Phase 3e Step 5.7)

---

## Manager Purpose

The **AnalysisConfigManager** provides crisis analysis configuration parameters and algorithm settings for the detection system. After Phase 3e consolidation, it focuses specifically on analysis algorithm configuration while previously shared functionality has been extracted to specialized managers.

**Primary Responsibilities:**
- Provide ensemble analysis parameters and algorithm configuration
- Manage confidence scoring parameters and pattern matching settings
- Handle analysis timeout and performance configuration
- Support contextual weighting and crisis detection parameters
- Maintain integration settings and debugging configuration

**Phase 3e Transformation:**
- **Learning methods extracted** to LearningSystemManager (2 methods)
- **Utility methods moved** to SharedUtilitiesManager (4 methods)  
- **Analysis methods consolidated** to CrisisAnalyzer (5 methods)
- **Remaining focus**: Core analysis algorithm configuration (6 methods)

---

## Core Methods

### Analysis Algorithm Configuration

#### `get_ensemble_parameters() -> Dict[str, Any]`
Retrieves ensemble analysis configuration parameters:
- Model weights for three-model ensemble
- Ensemble modes (consensus, majority, weighted)
- Score normalization methods and thresholds
- Analysis coordination settings

```python
# Example usage
ensemble_config = analysis_manager.get_ensemble_parameters()
# Returns: {
#   'ensemble_weights': [0.4, 0.3, 0.3],
#   'score_normalization': 'sigmoid',
#   'consensus_threshold': 0.7,
#   'weighted_mode_enabled': True
# }
```

#### `get_confidence_scoring_parameters() -> Dict[str, Any]`
Provides confidence scoring algorithm parameters:
- Confidence calculation methods and weights
- Uncertainty quantification settings
- Score aggregation and normalization parameters
- Confidence threshold mappings

#### `get_pattern_matching_parameters() -> Dict[str, Any]`
Returns pattern analysis configuration:
- Pattern detection weights and priorities
- Keyword matching sensitivity settings
- Contextual pattern analysis parameters
- Pattern confidence scoring methods

#### `get_algorithm_parameters() -> Dict[str, Any]`
Core crisis detection algorithm settings:
- Detection sensitivity and threshold parameters
- Algorithm timeout and performance limits
- Processing optimization settings
- Analysis depth and scope configuration

### Performance and Integration Settings

#### `get_performance_parameters() -> Dict[str, Any]`
Analysis performance configuration:
- Timeout settings for analysis operations
- Memory usage limits and optimization flags
- Batch processing parameters
- GPU/CPU utilization settings

#### `get_integration_settings() -> Dict[str, Any]`
System integration configuration:
- API response format settings
- Logging and monitoring parameters  
- Error handling and fallback configuration
- Integration mode and compatibility settings

### Validation and Monitoring

#### `validate_parameters() -> Dict[str, Any]`
Validates all analysis configuration parameters:
- Range validation for numerical parameters
- Type validation for configuration objects
- Logical consistency checking across parameter sets
- Returns comprehensive validation report

#### `get_configuration_summary() -> Dict[str, Any]`
Provides configuration overview for monitoring:
- Manager version and initialization status
- Configuration loading status and metadata
- Parameter category counts and features
- Phase 3e transformation tracking

---

## Phase 3e Consolidation Impact

### Methods Extracted to LearningSystemManager

**`get_learning_parameters()` → LearningSystemManager**
- **Reason**: Learning-specific configuration belongs with learning system
- **Migration Reference**: Use `learning_manager.get_learning_parameters()`
- **Functionality**: Learning rates, adjustment parameters, feedback configuration

**Learning parameter validation** → LearningSystemManager
- **Reason**: Specialized validation for learning system bounds
- **Migration Reference**: Use `learning_manager.validate_learning_parameters()`
- **Functionality**: Learning rate bounds, adjustment limits validation

### Methods Moved to SharedUtilitiesManager

**Type conversion with validation** → SharedUtilitiesManager
- **Reason**: Universal utility pattern used across all managers
- **Migration Reference**: Use `shared_utils.safe_float_convert()` and similar methods
- **Functionality**: Safe type conversion with bounds checking

**Generic parameter validation** → SharedUtilitiesManager
- **Reason**: Common validation patterns applicable to all managers
- **Migration Reference**: Use `shared_utils.validate_range()` and similar methods
- **Functionality**: Range validation, type checking, bounds enforcement

**Error handling with fallbacks** → SharedUtilitiesManager
- **Reason**: Standardized error handling across system
- **Migration Reference**: Use `shared_utils.handle_error_with_fallback()`
- **Functionality**: Graceful error recovery with contextual logging

**Configuration loading utilities** → SharedUtilitiesManager
- **Reason**: Universal configuration access patterns
- **Migration Reference**: Use `shared_utils.get_setting_with_type_conversion()`
- **Functionality**: JSON loading with environment variable substitution

### Methods Consolidated to CrisisAnalyzer

**`get_crisis_thresholds()`** → CrisisAnalyzer
- **Reason**: Analysis-specific threshold configuration
- **Migration Reference**: Use `crisis_analyzer.get_analysis_crisis_thresholds()`
- **Functionality**: Crisis level threshold mapping and configuration

**`get_analysis_timeouts()`** → CrisisAnalyzer
- **Reason**: Analysis operation timeout management
- **Migration Reference**: Use `crisis_analyzer.get_analysis_timeouts()`
- **Functionality**: Analysis processing timeout limits and fallback handling

**`get_confidence_boosts()`** → CrisisAnalyzer  
- **Reason**: Analysis confidence adjustment logic
- **Migration Reference**: Use `crisis_analyzer.get_analysis_confidence_boosts()`
- **Functionality**: Context-based confidence score adjustments

**`get_pattern_weights()`** → CrisisAnalyzer
- **Reason**: Analysis pattern weight configuration
- **Migration Reference**: Use `crisis_analyzer.get_analysis_pattern_weights()`
- **Functionality**: Pattern matching weights and priority settings

**Analysis algorithm core settings** → CrisisAnalyzer
- **Reason**: Central analysis coordination and configuration
- **Migration Reference**: Use `crisis_analyzer.get_analysis_algorithm_parameters()`
- **Functionality**: Core detection algorithm parameters and settings

---

## Dependencies

### Required Dependencies
- **UnifiedConfigManager** - Configuration access and environment variable management
- **logging** - Error handling and status tracking
- **datetime** - Timestamp generation and validation tracking
- **json** - Configuration file parsing and processing

### Integration Points
- **Called by**: CrisisAnalyzer, API endpoints, system initialization
- **Provides to**: Algorithm configuration, analysis parameters, performance settings
- **Critical for**: Crisis detection accuracy, analysis performance optimization

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

### Clean v3.1 Compliance
- **Factory Function**: `create_analysis_config_manager()` with dependency validation
- **Dependency Injection**: Accepts UnifiedConfigManager as required dependency
- **Error Handling**: Comprehensive fallback mechanisms for configuration loading
- **Configuration Access**: Uses UnifiedConfigManager patterns throughout system

### Phase 3e Integration Pattern
```
UnifiedConfigManager → AnalysisConfigManager → CrisisAnalyzer
                              ↓
                    Algorithm Configuration
                   (Ensemble, Confidence, Patterns)
```

### Manager Relationship After Consolidation
```
AnalysisConfigManager (Algorithm Config)
├── Extracted to → LearningSystemManager (Learning Config)
├── Moved to → SharedUtilitiesManager (Common Utilities) 
├── Consolidated to → CrisisAnalyzer (Analysis Methods)
└── Remaining → Core Algorithm Configuration
```

---

## Configuration Structure

### JSON Configuration Sections
```json
{
  "ensemble_parameters": {
    "model_weights": [0.4, 0.3, 0.3],
    "consensus_threshold": 0.7,
    "score_normalization": "sigmoid"
  },
  "confidence_scoring": {
    "confidence_boost_factors": {
      "high_certainty": 1.2,
      "medium_certainty": 1.0,
      "low_certainty": 0.8
    }
  },
  "pattern_matching": {
    "pattern_weights": {
      "keyword_patterns": 0.3,
      "semantic_patterns": 0.7
    }
  },
  "performance_parameters": {
    "timeout_ms": 30000,
    "max_memory_mb": 512,
    "optimization_level": "high"
  }
}
```

### Environment Variable Overrides
- **NLP_ENSEMBLE_WEIGHTS** - Override model ensemble weights
- **NLP_CONFIDENCE_BOOST** - Override confidence boost settings
- **NLP_PATTERN_SENSITIVITY** - Override pattern detection sensitivity
- **NLP_ANALYSIS_TIMEOUT** - Override analysis timeout limits

---

## Usage Examples

### Basic Configuration Access
```python
from managers.analysis_config import create_analysis_config_manager
from managers.unified_config import create_unified_config_manager

# Initialize manager
unified_config = create_unified_config_manager()
analysis_manager = create_analysis_config_manager(unified_config)

# Get ensemble parameters
ensemble_config = analysis_manager.get_ensemble_parameters()
model_weights = ensemble_config['ensemble_weights']

# Get confidence scoring parameters
confidence_config = analysis_manager.get_confidence_scoring_parameters()
boost_factors = confidence_config['confidence_boost_factors']
```

### Integration with CrisisAnalyzer
```python
# AnalysisConfigManager provides algorithm configuration
analysis_config = analysis_manager.get_ensemble_parameters()

# CrisisAnalyzer uses configuration for analysis
result = crisis_analyzer.analyze_crisis(
    message="I'm feeling really down",
    user_id="user123", 
    channel_id="general",
    config_override=analysis_config
)
```

### Parameter Validation
```python
# Validate all configuration parameters
validation_result = analysis_manager.validate_parameters()

if not validation_result['valid']:
    print("Configuration errors:")
    for error in validation_result['errors']:
        print(f"  - {error}")
```

---

## Migration Guide

### For Developers Using Extracted Methods

#### Learning Parameters (Now in LearningSystemManager)
```python
# Before Phase 3e
learning_config = analysis_manager.get_learning_parameters()

# After Phase 3e  
learning_config = learning_manager.get_learning_parameters()
```

#### Utility Functions (Now in SharedUtilitiesManager)
```python
# Before Phase 3e
value = analysis_manager._safe_float_convert(raw_value, default=0.5)

# After Phase 3e
value = shared_utils.safe_float_convert(raw_value, default=0.5)
```

#### Analysis Methods (Now in CrisisAnalyzer)
```python
# Before Phase 3e
thresholds = analysis_manager.get_crisis_thresholds()

# After Phase 3e  
thresholds = crisis_analyzer.get_analysis_crisis_thresholds()
```

### Configuration File Updates

If you have custom configuration files referencing the old structure, update section names:
- `learning_parameters` → Access via LearningSystemManager
- `analysis_thresholds` → Access via CrisisAnalyzer  
- Core `ensemble_parameters` → Remain in AnalysisConfigManager

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

## Phase 3e Achievement Summary

**Before Phase 3e**: Monolithic configuration manager with 12+ mixed-purpose methods  
**After Phase 3e**: Focused algorithm configuration manager with 6 core methods

### Consolidation Results
- **Learning methods**: Successfully extracted to LearningSystemManager
- **Utility methods**: Successfully moved to SharedUtilitiesManager  
- **Analysis methods**: Successfully consolidated to CrisisAnalyzer
- **Core focus**: Retained essential algorithm configuration methods
- **Clean architecture**: 100% Clean v3.1 compliance maintained

### Community Impact
Enhanced system maintainability and reliability for The Alphabet Cartel's LGBTQIA+ crisis detection service through focused manager responsibilities and improved code organization, enabling more reliable mental health support for Discord community members.