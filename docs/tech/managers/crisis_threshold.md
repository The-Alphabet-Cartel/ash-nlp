<!-- ash-nlp/docs/tech/managers/crisis_threshold.md -->
<!--
Crisis Threshold Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Crisis Threshold Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-1
**LAST UPDATED**: 2025-08-26
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

**File**: `managers/crisis_threshold.py`  
**Factory Function**: `create_crisis_threshold_manager(unified_config_manager, model_coordination_manager)`  
**Dependencies**: UnifiedConfigManager, ModelCoordinationManager  
**Status**: Production Ready - Phase 3e Consolidation Complete  

---

## Manager Purpose

The **CrisisThresholdManager** is responsible for managing crisis level thresholds and mappings that are critical to the life-saving functionality of the system. It determines crisis levels from confidence scores, manages staff review requirements, and provides mode-aware threshold mappings for the crisis detection system.

**Primary Responsibilities:**
- Map confidence scores to crisis levels (none, low, medium, high, critical) based on ensemble mode
- Determine staff review requirements based on confidence and crisis levels
- Provide mode-specific threshold configurations for different ensemble modes
- Handle threshold bounds and safety controls
- Manage threshold validation and consistency checking

**Phase 3e Transformation:**
- **Learning methods extracted** to LearningSystemManager (2 methods)
- **Utility methods moved** to SharedUtilitiesManager (4 methods)
- **Critical threshold logic preserved** - All life-saving methods retained (4 methods)
- **Enhanced integration** with learning system for adaptive threshold management

---

## Critical Business Logic

### Life-Saving Methods (Never Moved)

#### `determine_crisis_level(confidence: float, context: Dict = None) -> str`
**CRITICAL BUSINESS LOGIC** - Maps confidence scores to crisis levels

This method is the core of the crisis detection system and directly impacts user safety. It uses ensemble-mode-specific thresholds to determine crisis levels:

- **none** (0.0 - 0.2): No crisis indicators detected
- **low** (0.2 - 0.4): Mild distress requiring monitoring
- **medium** (0.4 - 0.6): Moderate distress requiring intervention
- **high** (0.6 - 0.8): Significant crisis requiring immediate response
- **critical** (0.8 - 1.0): Severe crisis requiring emergency protocols

```python
# Example usage
crisis_level = threshold_manager.determine_crisis_level(
    confidence=0.75,
    context={"ensemble_mode": "consensus"}
)
# Returns: "high"
```

#### `requires_staff_review(crisis_level: str, confidence: float, disagreement: bool = False) -> bool`
**CRITICAL SAFETY LOGIC** - Determines when human intervention is required

Implements multiple safety layers to ensure human review for uncertain or high-risk cases:
- Low confidence scores regardless of crisis level
- Borderline cases between crisis levels
- Model disagreement indicating uncertainty
- High and critical crisis levels always require review

```python
# Example usage
needs_review = threshold_manager.requires_staff_review(
    crisis_level="high",
    confidence=0.65,
    disagreement=True
)
# Returns: True (due to model disagreement)
```

### Configuration and Validation Methods

#### `get_crisis_level_mapping_for_mode(mode: str = None) -> Dict[str, float]`
Retrieves mode-specific crisis level threshold mappings:
- Supports different ensemble modes (consensus, majority, weighted)
- Provides fallback to default thresholds
- Handles mode-specific sensitivity adjustments

#### `get_staff_review_thresholds_for_mode(mode: str = None) -> Dict[str, float]`
Returns staff review threshold configuration for specific ensemble modes:
- Confidence thresholds triggering human review
- Mode-specific review requirements
- Disagreement sensitivity settings

#### `get_ensemble_thresholds_for_mode(mode: str) -> Dict[str, Any]`
Complete threshold configuration for specific ensemble mode:
- Crisis level thresholds
- Staff review thresholds
- Mode-specific parameters and settings

#### `get_current_ensemble_mode() -> str`
Retrieves current model ensemble operating mode from ModelCoordinationManager.

### Validation and Health Methods

#### `_validate_threshold_config() -> bool`
Validates threshold configuration consistency:
- Ensures thresholds are in ascending order
- Validates threshold ranges (0.0 - 1.0)
- Checks for logical consistency across modes

#### `get_validation_status() -> Dict[str, Any]`
Returns comprehensive threshold validation status:
- Configuration consistency results
- Threshold range validation
- Mode-specific validation details
- Error reporting and warnings

---

## Phase 3e Consolidation Impact

### Methods Extracted to LearningSystemManager

**`get_learning_thresholds()` → LearningSystemManager**
- **Reason**: Learning-specific threshold configuration belongs with learning system
- **Migration Reference**: Use `learning_manager.get_learning_thresholds()`
- **Functionality**: Learning rate thresholds, adjustment parameters, learning bounds

**Adaptive threshold adjustment logic** → LearningSystemManager
- **Reason**: Threshold adjustment algorithms are learning system functionality
- **Migration Reference**: Use `learning_manager.adjust_threshold_for_false_positive/negative()`
- **Functionality**: False positive/negative threshold adjustments with bounds enforcement

### Methods Moved to SharedUtilitiesManager

**Configuration validation patterns** → SharedUtilitiesManager
- **Reason**: Generic validation patterns applicable across managers
- **Migration Reference**: Use `shared_utils.validate_range()` and `validate_type()`
- **Functionality**: Range checking, type validation, bounds enforcement

**Safe dictionary access patterns** → SharedUtilitiesManager
- **Reason**: Universal configuration access patterns
- **Migration Reference**: Use `shared_utils.get_nested_config_setting()`
- **Functionality**: Nested configuration access with fallbacks

**Exception handling with fallbacks** → SharedUtilitiesManager
- **Reason**: Standardized error handling across system
- **Migration Reference**: Use `shared_utils.handle_error_with_fallback()`
- **Functionality**: Graceful error recovery with contextual logging

**Range and bounds checking utilities** → SharedUtilitiesManager
- **Reason**: Universal utility pattern for numerical validation
- **Migration Reference**: Use `shared_utils.validate_bounds()`
- **Functionality**: Numerical bounds checking with parameter context

---

## Dependencies

### Required Dependencies
- **UnifiedConfigManager** - Configuration access and threshold settings
- **ModelCoordinationManager** - Ensemble mode information and coordination
- **logging** - Error handling and status tracking
- **typing** - Type hints for method signatures

### Integration Points
- **Called by**: CrisisAnalyzer, API endpoints, analysis pipeline
- **Provides to**: Crisis level determination, staff review decisions, threshold mappings
- **Critical for**: User safety, crisis detection accuracy, human intervention decisions

---

## Environment Variables

**Crisis Threshold Variables:**
- **NLP_THRESHOLD_LOW** - Low crisis level threshold (default: 0.2)
- **NLP_THRESHOLD_MEDIUM** - Medium crisis level threshold (default: 0.4)
- **NLP_THRESHOLD_HIGH** - High crisis level threshold (default: 0.6)
- **NLP_THRESHOLD_CRITICAL** - Critical crisis level threshold (default: 0.8)

**Staff Review Variables:**
- **NLP_REVIEW_CONFIDENCE_THRESHOLD** - Minimum confidence for no review
- **NLP_REVIEW_DISAGREEMENT_ENABLED** - Enable review on model disagreement
- **NLP_REVIEW_BORDERLINE_SENSITIVITY** - Sensitivity for borderline cases

**Ensemble Mode Variables:**
- **NLP_ENSEMBLE_MODE** - Default ensemble mode (consensus/majority/weighted)
- **NLP_MODE_SPECIFIC_THRESHOLDS** - Enable mode-specific threshold sets

---

## Architecture Integration

### Clean v3.1 Compliance
- **Factory Function**: `create_crisis_threshold_manager()` with dependency validation
- **Dependency Injection**: Accepts UnifiedConfigManager and ModelCoordinationManager
- **Error Handling**: Comprehensive fallback mechanisms for all threshold operations
- **Configuration Access**: Uses UnifiedConfigManager patterns throughout

### Phase 3e Integration Pattern
```
UnifiedConfigManager → CrisisThresholdManager ← ModelCoordinationManager
                              ↓
                    Critical Threshold Logic
                 (Crisis Levels, Staff Review)
```

### Learning System Integration
```
CrisisThresholdManager (Static Thresholds)
            ↓
      LearningSystemManager (Adaptive Adjustments)
            ↓
    Applied Threshold Modifications
```

---

## Usage Examples

### Crisis Level Determination
```python
from managers.crisis_threshold import create_crisis_threshold_manager
from managers.unified_config import create_unified_config_manager
from managers.model_coordination import create_model_coordination_manager

# Initialize managers
unified_config = create_unified_config_manager()
model_manager = create_model_coordination_manager(unified_config)
threshold_manager = create_crisis_threshold_manager(unified_config, model_manager)

# Determine crisis level
crisis_level = threshold_manager.determine_crisis_level(
    confidence=0.68,
    context={"user_history": "previous_concerns"}
)
print(f"Crisis level: {crisis_level}")  # Output: "high"

# Check if staff review needed
needs_review = threshold_manager.requires_staff_review(
    crisis_level="high",
    confidence=0.68,
    disagreement=False
)
print(f"Staff review needed: {needs_review}")  # Output: True
```

### Threshold Configuration Access
```python
# Get mode-specific thresholds
consensus_thresholds = threshold_manager.get_crisis_level_mapping_for_mode("consensus")
print("Consensus thresholds:", consensus_thresholds)
# Output: {"low": 0.25, "medium": 0.45, "high": 0.65, "critical": 0.85}

# Get staff review thresholds
review_config = threshold_manager.get_staff_review_thresholds_for_mode("consensus")
print("Review config:", review_config)

# Validate configuration
validation = threshold_manager.get_validation_status()
if not validation["valid"]:
    print("Threshold configuration issues:", validation["errors"])
```

### Integration with Learning System
```python
# CrisisThresholdManager provides base thresholds
base_thresholds = threshold_manager.get_crisis_level_mapping_for_mode("weighted")

# LearningSystemManager applies adaptive adjustments
adjusted_thresholds = learning_manager.process_learning_feedback(
    feedback_type="false_positive",
    current_thresholds=base_thresholds,
    crisis_level="medium"
)

# Use adjusted thresholds for analysis
final_crisis_level = threshold_manager.determine_crisis_level(
    confidence=0.55,
    context={"adjusted_thresholds": adjusted_thresholds["adjusted_thresholds"]}
)
```

---

## Safety Considerations

### Conservative Fallbacks
- **Unknown ensemble modes**: Default to most conservative thresholds
- **Invalid confidence scores**: Trigger automatic staff review
- **Configuration errors**: Use hardcoded safe thresholds
- **Borderline cases**: Always err on side of higher crisis level

### Multiple Safety Layers
1. **Threshold validation**: Ensures thresholds are logically ordered
2. **Bounds checking**: Prevents invalid threshold values
3. **Fallback mechanisms**: Safe defaults when configuration fails
4. **Staff review triggers**: Multiple conditions requiring human review
5. **Conservative mapping**: Uncertain cases mapped to higher crisis levels

### Production Reliability
- **Zero tolerance for false negatives**: System designed to catch all potential crises
- **Graceful degradation**: Maintains functionality even with configuration issues
- **Audit logging**: All threshold decisions logged for review and improvement
- **Performance monitoring**: Threshold decision timing tracked for system health

---

## Migration Guide

### For Developers Using Extracted Methods

#### Learning Thresholds (Now in LearningSystemManager)
```python
# Before Phase 3e
learning_thresholds = threshold_manager.get_learning_thresholds()

# After Phase 3e
learning_thresholds = learning_manager.get_learning_thresholds()
```

#### Threshold Adjustments (Now in LearningSystemManager)
```python
# Before Phase 3e (not implemented)
# threshold_manager.adjust_threshold_for_false_positive(0.6, "medium")

# After Phase 3e
adjustment_result = learning_manager.adjust_threshold_for_false_positive(
    current_threshold=0.6,
    crisis_level="medium"
)
new_threshold = adjustment_result["new_threshold"]
```

#### Validation Utilities (Now in SharedUtilitiesManager)
```python
# Before Phase 3e (internal methods)
# threshold_manager._validate_range(value, min_val, max_val)

# After Phase 3e
is_valid = shared_utils.validate_range(value, min_val, max_val, "threshold_name")
```

---

## Production Impact

### Enhanced Reliability
- **Focused responsibility**: Clear separation between static and adaptive thresholds
- **Improved maintainability**: Reduced complexity in threshold logic
- **Better error handling**: Specialized error handling for threshold operations
- **Clearer testing**: Isolated threshold logic enables targeted testing

### Learning System Integration
- **Adaptive capabilities**: Thresholds can now learn from false positives/negatives
- **Bounds enforcement**: Learning adjustments respect safety boundaries
- **Audit tracking**: Complete history of threshold adjustments maintained
- **Gradual improvement**: System accuracy improves over time through learning

### Performance Optimization
- **Reduced complexity**: Fewer methods mean faster threshold decisions
- **Better caching**: Threshold configurations can be cached more effectively
- **Cleaner code paths**: Simplified logic reduces decision overhead
- **Focused optimization**: Threshold-specific optimizations possible

---

## Phase 3e Achievement Summary

**Before Phase 3e**: Threshold manager with mixed responsibilities  
**After Phase 3e**: Focused threshold determination with learning system integration

### Consolidation Results
- **Learning methods**: Successfully extracted to LearningSystemManager
- **Utility methods**: Successfully moved to SharedUtilitiesManager
- **Critical logic preserved**: All life-saving threshold logic maintained
- **Enhanced integration**: Improved connection with learning system for adaptation

### Community Impact
Maintained critical safety functions while enabling adaptive learning capabilities for The Alphabet Cartel's LGBTQIA+ crisis detection system, ensuring reliable threshold decisions that protect community members while continuously improving accuracy through learning from feedback.