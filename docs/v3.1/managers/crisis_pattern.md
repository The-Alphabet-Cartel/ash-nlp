# Crisis Pattern Manager Documentation

**File**: `managers/crisis_pattern_manager.py`  
**Phase**: 3e Step 1.1 Documentation Audit  
**Status**: 🔄 **IN PROGRESS**  
**Factory Function**: `create_crisis_pattern_manager(config_manager)`  
**Dependencies**: UnifiedConfigManager  
**FILE VERSION**: v3.1-3e-1.1-1  
**LAST MODIFIED**: 2025-08-17  

---

## 🎯 **Manager Purpose**

The **CrisisPatternManager** is responsible for crisis pattern detection and analysis. It loads crisis patterns from JSON configuration, performs pattern matching (both keyword-based and semantic), and provides comprehensive pattern analysis for crisis detection. This manager is critical for identifying specific crisis indicators in user messages.

**Primary Responsibilities:**
- Load and manage crisis patterns from JSON configuration
- Perform keyword-based pattern matching for crisis indicators
- Provide semantic pattern detection using zero-shot classification
- Extract community-specific patterns and context phrases
- Analyze temporal indicators and enhanced crisis patterns
- Generate comprehensive crisis pattern analysis results

---

## 🔧 **Core Methods**

### **Primary Analysis Methods:**
1. **`analyze_message(message, user_id, channel_id)`** - **COMPREHENSIVE** - Main pattern analysis entry point
2. **`find_triggered_patterns(message, model_ensemble_manager)`** - Pattern detection with semantic fallback
3. **`extract_community_patterns(message)`** - Community-specific pattern detection
4. **`extract_crisis_context_phrases(message)`** - Context phrase extraction

### **Configuration Access Methods:**
1. **`get_crisis_patterns()`** - Core crisis pattern configuration
2. **`get_community_vocabulary()`** - Community-specific vocabulary patterns
3. **`get_crisis_context_patterns()`** - Context phrase configuration
4. **`get_temporal_indicators()`** - Temporal crisis indicators

### **Advanced Analysis Methods:**
1. **`analyze_temporal_indicators(message)`** - Time-sensitive crisis indicators
2. **`check_enhanced_crisis_patterns(message)`** - Enhanced pattern matching
3. **`apply_context_weights(message, base_score)`** - Context-based scoring adjustments

---

## 🤝 **Shared Methods (Potential for SharedUtilitiesManager)**

### **Pattern Matching Utilities:**
- **Text preprocessing and normalization** - Message cleaning patterns
- **Keyword matching with case handling** - String matching utilities
- **Regular expression pattern matching** - Regex validation and execution
- **Dictionary/list traversal patterns** - Configuration parsing utilities

### **Configuration Processing:**
- **JSON pattern loading** - Configuration file processing
- **Pattern validation and structure checking** - Pattern format validation
- **Environment variable integration** - Via UnifiedConfigManager patterns
- **Fallback value assignment** - Default pattern handling

### **Error Handling and Validation:**
- **Pattern matching error recovery** - Graceful degradation on pattern errors
- **Configuration validation** - Pattern structure validation
- **Exception handling with logging** - Standardized error handling
- **Safe string operations** - Null/empty string handling

---

## 🧠 **Learning Methods (for LearningSystemManager)**

### **Pattern Learning Configuration:**
1. **Pattern weight adjustment** - Learning-based pattern weight modification
2. **False positive pattern suppression** - Reduce sensitivity for incorrectly triggered patterns
3. **Pattern effectiveness tracking** - Monitor which patterns are most accurate

### **Dynamic Pattern Adaptation:**
1. **Community vocabulary learning** - Adapt patterns based on community-specific language
2. **Context phrase optimization** - Learn effective context indicators
3. **Temporal pattern adjustment** - Adapt temporal indicators based on feedback

### **Pattern Performance Analytics:**
- **Pattern trigger frequency tracking** - Monitor pattern usage statistics
- **Pattern accuracy measurement** - Track true/false positive rates
- **Pattern effectiveness scoring** - Rank patterns by detection quality

---

## 📊 **Analysis Methods (Crisis Analysis Specific)**

### **Core Pattern Detection:**
1. **`analyze_message()`** - **CRITICAL** - Comprehensive pattern analysis
2. **`find_triggered_patterns()`** - **CRITICAL** - Multi-method pattern detection
3. **Crisis level determination** - Map patterns to crisis severity levels
4. **Safety assessment generation** - Determine intervention requirements

### **Semantic Pattern Analysis:**
1. **`_find_patterns_semantic()`** - Zero-shot classification pattern detection
2. **`_find_patterns_enhanced_fallback()`** - Enhanced keyword-based fallback
3. **Hypothesis-based classification** - Semantic similarity detection

### **Specialized Pattern Analysis:**
1. **Community pattern extraction** - Community-specific crisis indicators
2. **Context phrase analysis** - Crisis context amplification
3. **Temporal indicator analysis** - Time-sensitive crisis markers
4. **Enhanced pattern consolidation** - Multi-pattern integration

---

## 🔗 **Dependencies**

### **Required Dependencies:**
- **UnifiedConfigManager** - Pattern configuration loading and environment overrides
- **ModelEnsembleManager** (optional) - Semantic pattern detection via zero-shot classification
- **logging** - Error handling and pattern analysis tracking

### **Configuration Files:**
- **`config/crisis_patterns.json`** - Primary crisis pattern definitions
- **`config/community_vocabulary.json`** - Community-specific patterns
- **`config/crisis_context_patterns.json`** - Context phrase patterns
- **`config/temporal_indicators.json`** - Temporal crisis indicators

### **Integration Points:**
- **Called by**: CrisisAnalyzer (primary), API endpoints
- **Uses**: ModelEnsembleManager for semantic classification
- **Provides to**: Crisis pattern detection results, pattern analysis data

---

## 🌍 **Environment Variables**

**Accessed via UnifiedConfigManager only - no direct environment access**

### **Pattern Configuration Variables:**
- **`NLP_PATTERN_*`** - Pattern-specific overrides via UnifiedConfigManager
- **`NLP_CRISIS_*`** - Crisis pattern configuration overrides
- **`NLP_COMMUNITY_*`** - Community vocabulary overrides

### **Analysis Configuration:**
- Pattern matching sensitivity settings
- Semantic classification thresholds
- Pattern weight adjustment parameters

---

## 🏗️ **Integration Points**

### **Upstream Dependencies:**
- **UnifiedConfigManager** - Pattern configuration access
- **ModelEnsembleManager** - Zero-shot classification for semantic patterns

### **Downstream Consumers:**
- **CrisisAnalyzer** - **PRIMARY CONSUMER** - Pattern analysis results
- **API endpoints** - Pattern detection for direct analysis
- **Learning systems** - Pattern effectiveness data

### **Critical Data Flow:**
```
Message → CrisisPatternManager → Pattern Analysis → CrisisAnalyzer → Crisis Decision
```

---

## 🔍 **Method Overlap Analysis**

### **High Overlap Methods (Candidates for SharedUtilitiesManager):**
1. **Text preprocessing and normalization** - Message cleaning patterns used across system
2. **JSON configuration loading** - Pattern loading utilities reusable
3. **Regular expression validation** - Regex pattern handling
4. **Dictionary traversal and parsing** - Configuration processing patterns
5. **Error handling with fallbacks** - Pattern-specific error recovery
6. **String validation and cleaning** - Safe string operations

### **Learning-Specific Methods (for LearningSystemManager):**
1. **Pattern weight adjustment** - Learning-based pattern optimization
2. **Pattern effectiveness tracking** - Performance analytics for patterns
3. **False positive suppression** - Pattern sensitivity learning
4. **Community vocabulary adaptation** - Dynamic pattern learning

### **Analysis-Specific Methods (Stays in CrisisPatternManager):**
1. **`analyze_message()`** - **CRITICAL** - Main analysis method
2. **`find_triggered_patterns()`** - **CRITICAL** - Pattern detection
3. **Community pattern extraction** - Crisis-specific pattern matching
4. **Context phrase analysis** - Crisis context detection
5. **Temporal indicator analysis** - Time-sensitive crisis detection
6. **Semantic pattern detection** - Advanced NLP-based pattern matching

---

## ⚠️ **Critical Safety Methods**

### **Life-Saving Pattern Detection:**
1. **`analyze_message()`** - **NEVER MOVE** - Contains critical safety assessment logic
2. **`find_triggered_patterns()`** - **NEVER MOVE** - Core pattern detection for crisis identification
3. **Emergency pattern detection** - Immediate intervention triggers
4. **Auto-escalation logic** - Automatic crisis response triggers

### **Safety Considerations:**
- **Multiple detection methods** - Semantic + keyword fallback for reliability
- **Conservative pattern matching** - Err on side of detecting crisis
- **Pattern validation** - Ensure pattern integrity for safety
- **Fallback mechanisms** - Always provide some level of pattern detection

---

## 📊 **Configuration Complexity**

### **Large Configuration Files:**
- **`crisis_patterns.json`** - Hundreds of crisis indicators
- **`community_vocabulary.json`** - Community-specific language patterns
- **`temporal_indicators.json`** - Time-sensitive crisis markers
- **`crisis_context_patterns.json`** - Context amplification phrases

### **Pattern Types Managed:**
- **Keyword-based patterns** - Exact match and substring detection
- **Regular expression patterns** - Complex pattern matching
- **Semantic patterns** - NLP-based similarity detection
- **Community patterns** - Domain-specific crisis indicators
- **Temporal patterns** - Time-sensitive crisis markers

---

## 📋 **Consolidation Recommendations**

### **Move to SharedUtilitiesManager:**
- Text preprocessing and normalization utilities
- JSON configuration loading patterns
- Regular expression validation utilities
- Dictionary traversal and parsing methods
- String validation and cleaning utilities
- Generic error handling patterns

### **Extract to LearningSystemManager:**
- Pattern weight adjustment methods
- Pattern effectiveness tracking
- False positive suppression logic
- Community vocabulary learning
- Pattern performance analytics

### **Keep in CrisisPatternManager:**
- **`analyze_message()`** - **CRITICAL SAFETY METHOD**
- **`find_triggered_patterns()`** - **CRITICAL SAFETY METHOD**
- All pattern extraction methods (community, context, temporal)
- Crisis-specific pattern matching logic
- Safety assessment and auto-escalation logic
- Semantic pattern detection coordination

---

## ✅ **Phase 3e Step 1.1 Status**

**Manager**: crisis_pattern_manager.py  
**Documentation**: ✅ **COMPLETE**  
**Core Methods**: 10 identified  
**Shared Methods**: 6 identified for SharedUtilitiesManager  
**Learning Methods**: 4 identified for LearningSystemManager  
**Analysis Methods**: 7 remain in current manager (**CRITICAL SAFETY METHODS**)  

**Key Finding**: Contains critical life-saving pattern detection that must remain centralized for safety

**Next Manager**: context_pattern_manager.py