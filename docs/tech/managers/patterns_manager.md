<!-- ash-nlp/docs/tech/managers/patterns_manager.md -->
<!--
Patterns Detection Manager Documentation for Ash-NLP Service
FILE VERSION: v5.0
LAST MODIFIED: 2025-12-30
CLEAN ARCHITECTURE: Compliant
-->
# Pattern Detection Manager Documentation

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Project**: Ash-NLP v5.0
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
**FILE VERSION**: v5.0
**LAST UPDATED**: 2025-12-30
**CLEAN ARCHITECTURE**: Compliant

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

*Patterns Detection Manager Guide for Ash-NLP v5.0*

**Built with care for chosen family** 🏳️‍🌈
