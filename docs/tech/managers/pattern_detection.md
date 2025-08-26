<!-- ash-nlp/docs/tech/managers/pattern_detection.md -->
<!--
Pattern Detection Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Pattern Detection Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-1
**LAST UPDATED**: 2025-08-26
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

**File**: `managers/pattern_detection.py`  
**Factory Function**: `create_pattern_detection_manager(unified_config_manager)`  
**Dependencies**: UnifiedConfigManager  
**Status**: Production Ready - Phase 3e Optimization Complete  

---

## Manager Purpose

The **PatternDetectionManager** provides comprehensive crisis pattern detection using both semantic NLP classification and keyword-based fallback patterns. It serves as a critical safety component for detecting crisis indicators that may be missed by AI models alone, ensuring no crisis goes undetected.

**Primary Responsibilities:**
- Detect crisis patterns using semantic NLP classification with zero-shot models
- Provide keyword-based fallback pattern detection for reliability
- Manage community-specific crisis patterns for LGBTQIA+ awareness
- Handle temporal and contextual crisis indicators
- Coordinate with ModelCoordinationManager for enhanced semantic detection
- Maintain critical safety methods that are never extracted (life-saving functionality)

**Phase 3e Transformation:**
- **Learning methods extracted** to LearningSystemManager (4 methods)
- **Utility methods moved** to SharedUtilitiesManager (6 methods)
- **Critical safety methods preserved** - All life-saving pattern detection retained (7 methods)
- **Enhanced performance** through helper file optimization and semantic integration

---

## Critical Safety Methods (Never Moved)

### `analyze_message(message: str, user_id: str, channel_id: str, model_coordination_manager=None) -> Dict[str, Any]`
**CRITICAL SAFETY METHOD** - Primary message analysis for crisis detection

Performs comprehensive crisis pattern analysis combining semantic and keyword detection:
- Semantic classification using zero-shot models when available
- Keyword-based fallback pattern detection for reliability
- Community-specific pattern recognition
- Auto-escalation triggers for emergency responses
- Multi-layered safety assessment

Returns detailed analysis including crisis levels, pattern types, and escalation requirements.

### `find_triggered_patterns(message: str, model_coordination_manager=None) -> List[Dict[str, Any]]`
**CRITICAL SAFETY METHOD** - Core pattern detection engine

Identifies specific crisis patterns triggered by message content:
- Semantic pattern detection using NLP models
- Enhanced fallback pattern matching
- Pattern confidence scoring
- Crisis type categorization
- Emergency indicator identification

### Additional Critical Methods
- **Emergency pattern detection** - Immediate intervention triggers
- **Auto-escalation logic** - Automatic crisis response coordination
- **Community pattern extraction** - LGBTQIA+-specific crisis indicators
- **Context pattern analysis** - Contextual crisis amplification
- **Temporal pattern detection** - Time-sensitive crisis markers

---

## Phase 3e Consolidation Impact

### Methods Extracted to LearningSystemManager

**Pattern weight adjustment methods** → LearningSystemManager
- **Reason**: Pattern learning and effectiveness optimization belongs with learning system
- **Migration Reference**: Use `learning_manager.update_patterns_from_feedback()`
- **Functionality**: Learning from pattern effectiveness and community feedback

**Pattern effectiveness tracking** → LearningSystemManager
- **Reason**: Performance analytics and pattern optimization are learning system concerns
- **Migration Reference**: Use `learning_manager.evaluate_pattern_performance()`
- **Functionality**: Tracking pattern accuracy and effectiveness metrics

**Community vocabulary learning** → LearningSystemManager
- **Reason**: Adaptive community language learning is part of learning system
- **Migration Reference**: Use `learning_manager.adapt_community_patterns()`
- **Functionality**: Learning community-specific language patterns over time

**False positive suppression logic** → LearningSystemManager
- **Reason**: Pattern adjustment based on false positive feedback is learning functionality
- **Migration Reference**: Use `learning_manager.suppress_false_positive_patterns()`
- **Functionality**: Reducing false positive rates through pattern adjustment

### Methods Moved to SharedUtilitiesManager

**Text preprocessing and normalization** → SharedUtilitiesManager
- **Reason**: Universal text processing patterns used across multiple managers
- **Migration Reference**: Use `shared_utils.preprocess_text()` and related methods
- **Functionality**: Text cleaning, normalization, and preparation for analysis

**JSON configuration loading patterns** → SharedUtilitiesManager
- **Reason**: Configuration loading patterns applicable across all managers
- **Migration Reference**: Use `shared_utils.load_json_with_env_substitution()`
- **Functionality**: Loading and processing JSON pattern configuration files

**Regular expression validation utilities** → SharedUtilitiesManager
- **Reason**: Regex validation patterns used throughout system
- **Migration Reference**: Use `shared_utils.validate_pattern_structure()`
- **Functionality**: Pattern structure validation and regex compilation

**Dictionary traversal and parsing methods** → SharedUtilitiesManager
- **Reason**: Common data structure manipulation patterns
- **Migration Reference**: Use `shared_utils.traverse_nested_dict()`
- **Functionality**: Complex dictionary navigation and data extraction

**String validation and cleaning utilities** → SharedUtilitiesManager
- **Reason**: Universal string processing applicable across managers
- **Migration Reference**: Use `shared_utils.clean_and_validate_string()`
- **Functionality**: String sanitization and validation

**Generic error handling patterns** → SharedUtilitiesManager
- **Reason**: Standardized error handling across entire system
- **Migration Reference**: Use `shared_utils.handle_error_with_fallback()`
- **Functionality**: Consistent error recovery and logging

---

## LGBTQIA+ Community Pattern Recognition

### Community-Specific Crisis Indicators
- **Identity stress patterns**: Coming out difficulties, family rejection, deadnaming
- **Transition challenges**: Medical transition barriers, hormone access, legal issues
- **Discrimination indicators**: Workplace harassment, healthcare discrimination, housing issues
- **Community isolation**: Lack of chosen family, community exclusion, support absence
- **Identity questioning**: Uncertainty, exploration stress, self-acceptance challenges

### Cultural Sensitivity Features
- **Chosen family recognition**: Understanding non-biological family structures
- **Community event awareness**: Pride events, Transgender Day of Remembrance, etc.
- **Identity affirmation language**: Respectful terminology and identity validation
- **Community support indicators**: Peer support, mentor relationships, safe spaces

---

## Pattern Types and Configuration

### Semantic Pattern Detection
- **Zero-shot classification**: Advanced NLP models for semantic understanding
- **Community vocabulary**: LGBTQIA+-specific language recognition
- **Context amplification**: Contextual phrase analysis for meaning enhancement
- **Temporal sensitivity**: Time-based pattern recognition

### Keyword-Based Fallback Patterns
- **Crisis indicators**: Direct crisis language and emergency terms
- **Emotional distress**: Depression, anxiety, and emotional pain indicators
- **Behavioral patterns**: Isolation, withdrawal, and behavioral change indicators
- **Support seeking**: Help-seeking language and intervention requests

### Pattern Configuration Files
- **patterns_crisis.json**: Core crisis detection patterns
- **patterns_community.json**: LGBTQIA+ community-specific patterns
- **patterns_temporal.json**: Time-sensitive crisis indicators
- **patterns_context.json**: Context amplification patterns
- **patterns_idiom.json**: Community slang and idiomatic expressions

---

## Dependencies

### Required Dependencies
- **UnifiedConfigManager** - Pattern configuration and management
- **ModelCoordinationManager** - Semantic pattern detection via zero-shot models
- **logging** - Pattern detection logging and performance tracking
- **re** - Regular expression pattern matching
- **json** - Pattern configuration file processing

### Integration Points
- **Called by**: CrisisAnalyzer, API endpoints, analysis pipeline
- **Provides to**: Crisis pattern detection, community-aware analysis, safety triggers
- **Critical for**: System safety, crisis detection accuracy, emergency response

---

## Environment Variables

**Pattern Detection Variables:**
- **NLP_PATTERN_DETECTION_ENABLED** - Enable/disable pattern detection
- **NLP_SEMANTIC_PATTERNS_ENABLED** - Enable semantic NLP pattern detection
- **NLP_COMMUNITY_PATTERNS_ENABLED** - Enable LGBTQIA+ community patterns
- **NLP_PATTERN_CONFIDENCE_THRESHOLD** - Minimum confidence for pattern triggers

**Community Pattern Variables:**
- **NLP_LGBTQIA_SENSITIVITY_LEVEL** - Community pattern sensitivity
- **NLP_CHOSEN_FAMILY_RECOGNITION** - Enable chosen family pattern recognition
- **NLP_IDENTITY_STRESS_PATTERNS** - Enable identity-related stress detection
- **NLP_DISCRIMINATION_INDICATORS** - Enable discrimination pattern detection

**Performance Variables:**
- **NLP_PATTERN_CACHE_SIZE** - Pattern configuration cache size
- **NLP_PATTERN_RELOAD_INTERVAL** - Pattern configuration reload frequency
- **NLP_FALLBACK_ENABLED** - Enable keyword fallback when semantic fails

---

## Usage Examples

### Basic Pattern Detection
```python
from managers.pattern_detection import create_pattern_detection_manager
from managers.unified_config import create_unified_config_manager
from managers.model_coordination import create_model_coordination_manager

# Initialize managers
unified_config = create_unified_config_manager()
model_manager = create_model_coordination_manager(unified_config)
pattern_manager = create_pattern_detection_manager(unified_config)

# Analyze message for crisis patterns
result = pattern_manager.analyze_message(
    message="I can't handle this anymore, my family kicked me out",
    user_id="user123",
    channel_id="support",
    model_coordination_manager=model_manager
)

print(f"Crisis score: {result['crisis_score']}")
print(f"Patterns found: {result['triggered_patterns']}")
print(f"Requires attention: {result['requires_attention']}")
```

### Community-Specific Pattern Detection
```python
# Message with LGBTQIA+ specific content
message = "Family won't accept me being trans, feeling so alone"

result = pattern_manager.analyze_message(
    message=message,
    user_id="user456", 
    channel_id="transgender-support",
    model_coordination_manager=model_manager
)

# Check for community-specific patterns
community_patterns = [p for p in result['triggered_patterns'] 
                     if p.get('pattern_type') == 'community']
print(f"Community patterns detected: {len(community_patterns)}")
```

---

## Safety Considerations

### Multiple Detection Layers
- **Primary**: Semantic NLP classification for sophisticated understanding
- **Secondary**: Keyword-based fallback for reliability and coverage
- **Tertiary**: Community-specific patterns for cultural awareness
- **Emergency**: Auto-escalation triggers for immediate intervention

### Conservative Pattern Matching
- **Err on side of detection**: Better false positive than missed crisis
- **Multiple confirmation**: Require multiple indicators for lower confidence
- **Context consideration**: Evaluate patterns within message context
- **Community awareness**: Recognize cultural and identity-specific indicators

### Performance and Reliability
- **Fast fallback**: Keyword detection when semantic processing fails
- **Pattern validation**: Ensure pattern integrity through configuration validation
- **Error resilience**: Continue operation even with partial pattern loading failures
- **Monitoring integration**: Track pattern effectiveness and system health

---

## Migration Guide

### For Developers Using Extracted Methods

#### Learning Methods (Now in LearningSystemManager)
```python
# Before Phase 3e
pattern_manager.update_pattern_weights(feedback)

# After Phase 3e
learning_manager.update_patterns_from_feedback(pattern_feedback)
```

#### Utility Methods (Now in SharedUtilitiesManager)
```python
# Before Phase 3e
clean_text = pattern_manager._preprocess_message(message)

# After Phase 3e
clean_text = shared_utils.preprocess_text(message)
```

---

## Phase 3e Achievement Summary

**Before Phase 3e**: Pattern detection with mixed learning and utility concerns  
**After Phase 3e**: Focused pattern detection with enhanced safety and performance

### Consolidation Results
- **Learning methods**: Successfully extracted to specialized learning system
- **Utility methods**: Successfully moved to shared utilities for consistency
- **Critical safety**: All life-saving pattern detection logic preserved
- **Enhanced performance**: Helper file optimization improving detection speed

### Community Impact
Maintained critical safety functionality while improving system organization for The Alphabet Cartel's LGBTQIA+ crisis detection, ensuring reliable pattern detection that recognizes community-specific crisis indicators and maintains the highest safety standards for mental health support.