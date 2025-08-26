<!-- ash-nlp/docs/tech/managers/context_analysis.md -->
<!--
Context Analysis Manager Documentation for Ash-NLP Service
FILE VERSION: v3.1-3d-8.3-1
LAST MODIFIED: 2025-08-26
PHASE: 3e
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Context Analysis Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v3.1-3e-8.3-1
**LAST UPDATED**: 2025-08-26
**PHASE**: 3e
**CLEAN ARCHITECTURE**: v3.1 Compliant

---

**File**: `managers/context_analysis.py`  
**Factory Function**: `create_context_analysis_manager(unified_config_manager)`  
**Dependencies**: UnifiedConfigManager  
**Status**: Production Ready - Phase 3e Consolidation Complete  

---

## Manager Purpose

The **ContextAnalysisManager** specializes in analyzing contextual factors that influence crisis detection accuracy. It examines user history, channel context, temporal patterns, and community-specific indicators to enhance the understanding of crisis messages beyond their immediate content.

**Primary Responsibilities:**
- Analyze user interaction history and behavioral patterns
- Examine channel context and community dynamics
- Detect temporal patterns and seasonal influences
- Identify community-specific language and cultural indicators
- Provide contextual weighting for crisis analysis
- Support LGBTQIA+-aware contextual understanding

**Phase 3e Transformation:**
- **Learning methods extracted** to LearningSystemManager (4 methods)
- **Utility methods moved** to SharedUtilitiesManager (6 methods)
- **Core context analysis preserved** - Specialized contextual logic retained (5 methods)
- **Enhanced pattern recognition** with community-specific contextual awareness

---

## Core Methods

### Contextual Analysis Methods

#### `analyze_user_context(user_id: str, message_history: List[Dict] = None) -> Dict[str, Any]`
Analyzes user-specific contextual factors:
- Historical message sentiment and patterns
- User engagement patterns and frequency
- Previous crisis indicators or interventions
- Behavioral change detection over time
- Support system engagement levels

```python
# Example usage
user_context = context_manager.analyze_user_context(
    user_id="user123",
    message_history=recent_messages
)
# Returns: {
#   "sentiment_trend": "declining",
#   "engagement_level": "low",
#   "previous_concerns": True,
#   "support_interaction": "minimal",
#   "risk_factors": ["isolation", "sentiment_decline"]
# }
```

#### `analyze_channel_context(channel_id: str, channel_type: str = None) -> Dict[str, Any]`
Examines channel-specific contextual factors:
- Channel purpose and community dynamics
- Recent crisis events or community stress
- Moderation activity and support availability
- Channel-specific language patterns
- Community response capabilities

#### `analyze_temporal_context(timestamp: str, user_timezone: str = None) -> Dict[str, Any]`
Analyzes temporal factors affecting crisis detection:
- Time of day patterns (late night vulnerability)
- Day of week influences (weekend isolation)
- Seasonal affective patterns
- Holiday and community event impacts
- Peak crisis time identification

#### `get_community_context_indicators(message: str, channel_context: Dict) -> Dict[str, Any]`
Identifies community-specific contextual indicators:
- LGBTQIA+-specific language patterns and concerns
- Community event stress (coming out, transition, discrimination)
- Chosen family dynamics and support structures
- Identity-related crisis indicators
- Community celebration or mourning periods

#### `calculate_contextual_weight(contexts: Dict[str, Any]) -> float`
Calculates overall contextual influence on crisis detection:
- Combines user, channel, and temporal contexts
- Applies community-specific weighting factors
- Returns contextual confidence modifier
- Handles missing context gracefully

### Context Configuration Methods

#### `get_context_analysis_parameters() -> Dict[str, Any]`
Retrieves context analysis configuration:
- Contextual weighting factors and priorities
- Community-specific pattern definitions
- Temporal analysis sensitivity settings
- User history analysis depth parameters

#### `get_community_patterns() -> Dict[str, List[str]]`
Returns community-specific contextual patterns:
- LGBTQIA+ community language indicators
- Crisis pattern variations by community context
- Cultural sensitivity markers and considerations
- Community support structure indicators

#### `validate_context_analysis_config() -> Dict[str, Any]`
Validates context analysis configuration:
- Parameter range validation for contextual weights
- Community pattern definition consistency
- Temporal analysis setting validation
- Returns comprehensive validation results

---

## Phase 3e Consolidation Impact

### Methods Extracted to LearningSystemManager

**User pattern learning methods** → LearningSystemManager
- **Reason**: User behavioral pattern learning is part of adaptive learning system
- **Migration Reference**: Use `learning_manager.analyze_user_learning_patterns()`
- **Functionality**: Learning from user interaction patterns and feedback

**Context-based learning adjustments** → LearningSystemManager
- **Reason**: Contextual learning adjustments are learning system functionality
- **Migration Reference**: Use `learning_manager.apply_contextual_learning()`
- **Functionality**: Context-aware threshold and confidence adjustments

**Temporal pattern learning** → LearningSystemManager
- **Reason**: Learning temporal crisis patterns over time
- **Migration Reference**: Use `learning_manager.process_temporal_learning()`
- **Functionality**: Adaptive temporal pattern recognition and adjustment

**Community feedback integration** → LearningSystemManager
- **Reason**: Learning from community-specific feedback patterns
- **Migration Reference**: Use `learning_manager.integrate_community_feedback()`
- **Functionality**: Community-aware learning and pattern adaptation

### Methods Moved to SharedUtilitiesManager

**Text preprocessing utilities** → SharedUtilitiesManager
- **Reason**: Universal text processing patterns used across managers
- **Migration Reference**: Use `shared_utils.preprocess_text()` and similar methods
- **Functionality**: Text cleaning, normalization, and preprocessing

**Pattern matching utilities** → SharedUtilitiesManager
- **Reason**: Generic pattern matching applicable to multiple managers
- **Migration Reference**: Use `shared_utils.match_patterns()` and similar methods
- **Functionality**: Regex patterns, keyword matching, pattern validation

**Data structure utilities** → SharedUtilitiesManager
- **Reason**: Common data manipulation patterns
- **Migration Reference**: Use `shared_utils.merge_contexts()` and similar methods
- **Functionality**: Context merging, data aggregation, structure validation

**Temporal utility functions** → SharedUtilitiesManager
- **Reason**: Time-based calculations used throughout system
- **Migration Reference**: Use `shared_utils.calculate_time_factors()` and similar methods
- **Functionality**: Time calculations, timezone handling, temporal normalization

**Validation helper methods** → SharedUtilitiesManager
- **Reason**: Generic validation patterns applicable across system
- **Migration Reference**: Use `shared_utils.validate_context_data()` and similar methods
- **Functionality**: Data validation, structure checking, type validation

**Configuration processing utilities** → SharedUtilitiesManager
- **Reason**: Universal configuration processing patterns
- **Migration Reference**: Use `shared_utils.process_context_config()` and similar methods
- **Functionality**: Configuration loading, processing, and validation

---

## LGBTQIA+ Community Context Awareness

### Community-Specific Indicators

#### Identity and Transition Context
- **Coming out stress**: Language patterns indicating family/social rejection concerns
- **Transition challenges**: Medical, social, and legal transition difficulties
- **Identity questioning**: Uncertainty and exploration language patterns
- **Chosen name usage**: Deadnaming stress and identity affirmation needs

#### Community Support Context
- **Chosen family dynamics**: Non-biological family support structures
- **Community belonging**: Inclusion/exclusion indicators in community spaces
- **Peer support patterns**: Community member mutual support indicators
- **Mentor relationships**: Guidance and support relationship patterns

#### Discrimination and Safety Context
- **Workplace discrimination**: Employment-related LGBTQIA+ stress indicators
- **Healthcare challenges**: Medical discrimination and access concerns
- **Housing instability**: Housing discrimination and safety concerns
- **Legal concerns**: Rights and legal protection worry indicators

### Contextual Pattern Examples

```python
# Community-specific contextual patterns
community_patterns = {
    "identity_stress": [
        "family doesn't accept", "kicked out", "deadname", 
        "not safe at home", "hiding who I am"
    ],
    "transition_challenges": [
        "hormone access", "surgery waiting", "insurance denied",
        "medical gatekeeping", "transition timeline"
    ],
    "community_support": [
        "chosen family", "found family", "community support",
        "safe space", "understanding friends"
    ],
    "discrimination_indicators": [
        "workplace harassment", "healthcare discrimination",
        "housing discrimination", "legal concerns", "safety fears"
    ]
}
```

---

## Dependencies

### Required Dependencies
- **UnifiedConfigManager** - Configuration access and community pattern settings
- **datetime** - Temporal analysis and timezone handling
- **re** - Pattern matching and text analysis
- **typing** - Type hints for complex data structures
- **logging** - Context analysis logging and debugging

### Integration Points
- **Called by**: CrisisAnalyzer, API endpoints, analysis pipeline
- **Provides to**: Contextual analysis results, community awareness, temporal insights
- **Critical for**: Crisis detection accuracy, community-sensitive analysis, contextual understanding

---

## Environment Variables

**Context Analysis Variables:**
- **NLP_CONTEXT_ANALYSIS_ENABLED** - Enable/disable contextual analysis
- **NLP_CONTEXT_USER_HISTORY_DEPTH** - Depth of user history analysis
- **NLP_CONTEXT_TEMPORAL_WEIGHT** - Temporal factor weighting
- **NLP_CONTEXT_COMMUNITY_WEIGHT** - Community context weighting

**Community Pattern Variables:**
- **NLP_LGBTQIA_PATTERNS_ENABLED** - Enable LGBTQIA+-specific patterns
- **NLP_COMMUNITY_SENSITIVITY_LEVEL** - Community awareness sensitivity
- **NLP_CHOSEN_FAMILY_INDICATORS** - Chosen family pattern recognition
- **NLP_IDENTITY_STRESS_WEIGHT** - Identity-related stress weighting

**Temporal Analysis Variables:**
- **NLP_TEMPORAL_ANALYSIS_ENABLED** - Enable temporal pattern analysis
- **NLP_LATE_NIGHT_SENSITIVITY** - Late night vulnerability weighting
- **NLP_WEEKEND_ISOLATION_WEIGHT** - Weekend isolation factor
- **NLP_SEASONAL_PATTERN_DETECTION** - Seasonal affective pattern detection

---

## Architecture Integration

### Clean v3.1 Compliance
- **Factory Function**: `create_context_analysis_manager()` with dependency validation
- **Dependency Injection**: Accepts UnifiedConfigManager as required dependency
- **Error Handling**: Comprehensive fallback mechanisms for context analysis
- **Configuration Access**: Uses UnifiedConfigManager patterns throughout

### Phase 3e Integration Pattern
```
UnifiedConfigManager → ContextAnalysisManager → CrisisAnalyzer
                              ↓
                    Contextual Understanding
                 (User, Channel, Temporal, Community)
```

### Learning System Integration
```
ContextAnalysisManager (Static Context Analysis)
            ↓
      LearningSystemManager (Adaptive Context Learning)
            ↓
    Enhanced Contextual Understanding
```

---

## Usage Examples

### User Context Analysis
```python
from managers.context_analysis import create_context_analysis_manager
from managers.unified_config import create_unified_config_manager

# Initialize manager
unified_config = create_unified_config_manager()
context_manager = create_context_analysis_manager(unified_config)

# Analyze user context
user_context = context_manager.analyze_user_context(
    user_id="user123",
    message_history=[
        {"timestamp": "2025-08-26T10:00:00Z", "message": "feeling better today"},
        {"timestamp": "2025-08-25T23:30:00Z", "message": "can't sleep, worried"}
    ]
)

print("User context analysis:", user_context)
# Output includes sentiment trends, engagement patterns, risk factors
```

### Community Context Analysis
```python
# Analyze community-specific indicators
message = "Family won't accept me being trans, feeling so alone"
channel_context = {"type": "support", "community": "lgbtqia"}

community_indicators = context_manager.get_community_context_indicators(
    message, channel_context
)

print("Community indicators:", community_indicators)
# Output: {
#   "identity_stress": True,
#   "family_rejection": True, 
#   "isolation_indicators": True,
#   "community_type": "transgender_support",
#   "risk_level": "elevated"
# }
```

### Temporal Context Analysis
```python
# Analyze temporal factors
temporal_context = context_manager.analyze_temporal_context(
    timestamp="2025-08-26T02:30:00Z",
    user_timezone="America/Los_Angeles"
)

print("Temporal context:", temporal_context)
# Output: {
#   "time_of_day": "late_night",
#   "vulnerability_factor": 1.3,
#   "day_of_week": "Monday",
#   "seasonal_factor": 1.0
# }
```

### Integrated Context Analysis
```python
# Combine all contextual factors
contexts = {
    "user": user_context,
    "channel": {"type": "support", "activity": "moderate"},
    "temporal": temporal_context,
    "community": community_indicators
}

contextual_weight = context_manager.calculate_contextual_weight(contexts)
print(f"Contextual weight modifier: {contextual_weight}")
# Output: 1.25 (25% increase in crisis detection sensitivity)
```

---

## Migration Guide

### For Developers Using Extracted Methods

#### Learning Methods (Now in LearningSystemManager)
```python
# Before Phase 3e
pattern_learning = context_manager.analyze_user_learning_patterns(user_id)

# After Phase 3e
pattern_learning = learning_manager.analyze_user_learning_patterns(user_id)
```

#### Utility Methods (Now in SharedUtilitiesManager)
```python
# Before Phase 3e
clean_text = context_manager._preprocess_text(message)

# After Phase 3e
clean_text = shared_utils.preprocess_text(message)
```

#### Pattern Matching (Now in SharedUtilitiesManager)
```python
# Before Phase 3e
matches = context_manager._match_community_patterns(text, patterns)

# After Phase 3e  
matches = shared_utils.match_patterns(text, patterns, "community_context")
```

---

## Community Impact Considerations

### LGBTQIA+ Sensitivity
- **Language awareness**: Recognition of community-specific terminology and concerns
- **Identity affirmation**: Contextual understanding of identity-related stress
- **Community support**: Recognition of chosen family and support structures
- **Discrimination context**: Understanding of unique discrimination challenges

### Contextual Crisis Detection
- **Enhanced accuracy**: Community context improves crisis detection precision
- **Reduced false positives**: Cultural awareness prevents misinterpretation
- **Improved support**: Context-aware crisis response enables better intervention
- **Community trust**: Sensitive analysis builds trust within LGBTQIA+ community

### Temporal Awareness
- **Vulnerability timing**: Recognition of high-risk time periods
- **Seasonal patterns**: Understanding of seasonal affective influences
- **Community events**: Awareness of community celebration and mourning periods
- **Crisis timing**: Enhanced response during high-vulnerability periods

---

## Phase 3e Achievement Summary

**Before Phase 3e**: Context analysis with mixed learning and utility methods  
**After Phase 3e**: Focused contextual analysis with enhanced community awareness

### Consolidation Results
- **Learning methods**: Successfully extracted to LearningSystemManager
- **Utility methods**: Successfully moved to SharedUtilitiesManager
- **Core context analysis**: Enhanced community-specific contextual understanding
- **LGBTQIA+ awareness**: Improved community-sensitive pattern recognition

### Community Impact
Enhanced contextual understanding for The Alphabet Cartel's LGBTQIA+ crisis detection system, providing more accurate and culturally sensitive crisis analysis that recognizes community-specific stressors and support structures, leading to better mental health outcomes for Discord community members.