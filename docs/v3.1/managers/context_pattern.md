# Context Pattern Manager Documentation

**File**: `managers/context_pattern_manager.py`  
**Phase**: 3e Step 1.1 Documentation Audit  
**Status**: 🔄 **IN PROGRESS**  
**Factory Function**: `create_context_pattern_manager(unified_config)`  
**Dependencies**: UnifiedConfigManager  
**FILE VERSION**: v3.1-3e-6-1  
**LAST MODIFIED**: 2025-08-22

---

## 🎯 **Manager Purpose**

The **ContextPatternManager** provides advanced context analysis for crisis detection. It extracts context signals from messages, performs semantic analysis to understand message context, and provides context scoring for terms and phrases. This manager was migrated from `utils/context_helpers.py` in Step 10.8 as part of the utility consolidation.

**Primary Responsibilities:**
- Extract basic and advanced context signals from messages
- Perform semantic context analysis using configurable parameters
- Score term relevance within message context windows
- Apply context-based scoring adjustments for crisis detection
- Integrate with PatternDetectionManager for enhanced pattern detection

---

## 🔧 **Core Methods**

### **Context Extraction Methods:**
1. **`extract_context_signals(message)`** - Extract basic context signals from message
2. **`analyze_message_context(message, pattern_detection_manager=None)`** - **ENHANCED** - Advanced context analysis
3. **`score_term_in_context(term, message, context_window=None)`** - Score term relevance in context

### **Context Analysis Methods:**
1. **`identify_negation_context(message)`** - Identify negation patterns that affect meaning
2. **`determine_semantic_context(message)`** - Semantic context classification
3. **`calculate_context_strength(context_data)`** - Calculate overall context strength score

### **Configuration Access Methods:**
1. **`get_manager_status()`** - Manager status and configuration information
2. **`reload_configuration()`** - Reload configuration from files
3. **`is_initialized()`** - Check initialization status

---

## 🤝 **Shared Methods (Potential for SharedUtilitiesManager)**

### **Text Processing Utilities:**
- **Message preprocessing and normalization** - Text cleaning patterns
- **Word tokenization and splitting** - Message parsing utilities
- **Context window calculations** - Text window extraction patterns
- **Term position identification** - String position utilities

### **Configuration Processing:**
- **JSON configuration loading** - Pattern loading utilities
- **Parameter validation and bounds checking** - Configuration validation
- **Safe default value assignment** - Fallback value handling
- **Environment variable integration** - Via UnifiedConfigManager patterns

### **Context Analysis Utilities:**
- **Negation pattern matching** - Regular expression patterns for negation detection
- **Semantic similarity calculations** - Context scoring algorithms
- **Context strength scoring** - Numerical analysis patterns
- **Error handling with graceful degradation** - Fallback analysis methods

---

## 🧠 **Learning Methods (for LearningSystemManager)**

### **Context Learning Configuration:**
1. **Context weight optimization** - Learning-based context weight adjustments
2. **Semantic threshold adaptation** - Adaptive threshold tuning based on feedback
3. **Context window optimization** - Dynamic context window sizing

### **Context Effectiveness Tracking:**
1. **Context signal accuracy** - Track which context signals are most predictive
2. **Negation detection optimization** - Improve negation pattern effectiveness
3. **Semantic analysis calibration** - Optimize semantic similarity thresholds

### **Adaptive Context Analysis:**
- **Context boost weight learning** - Adjust context amplification based on results
- **Context window adaptation** - Learn optimal context windows for different message types
- **Semantic threshold tuning** - Adapt semantic similarity thresholds based on accuracy

---

## 📊 **Analysis Methods (Crisis Analysis Specific)**

### **Context Enhancement for Crisis Detection:**
1. **`analyze_message_context()`** - **CRITICAL** - Enhanced context analysis for crisis detection
2. **`determine_semantic_context()`** - Semantic analysis specifically for crisis context
3. **Context-based crisis amplification** - Apply context to enhance crisis scores

### **Crisis Context Integration:**
1. **Integration with PatternDetectionManager** - Enhanced pattern detection via context
2. **Context signal extraction for crisis** - Extract signals relevant to crisis detection
3. **Temporal context analysis** - Time-based context considerations

### **Context Scoring for Crisis:**
1. **Term scoring in crisis context** - Evaluate crisis-relevant terms in context
2. **Context strength for crisis indicators** - Calculate context impact on crisis detection
3. **Negation impact on crisis detection** - Handle negation in crisis contexts

---

## 🔗 **Dependencies**

### **Required Dependencies:**
- **UnifiedConfigManager** - Configuration loading and environment variable access
- **PatternDetectionManager** (optional) - Enhanced pattern detection integration
- **logging** - Error handling and analysis tracking

### **Configuration Files:**
- **`config/patterns_context.json`** - Context pattern configuration
- **`config/analysis_config.json`** - Semantic analysis parameters
- **Environment variables** - Via UnifiedConfigManager (e.g., `NLP_FEATURE_*`)

### **Integration Points:**
- **Called by**: CrisisAnalyzer (Step 10.8 integration)
- **Works with**: PatternDetectionManager for enhanced pattern detection
- **Provides to**: Context analysis results, semantic context data

---

## 🌍 **Environment Variables**

**Accessed via UnifiedConfigManager only - no direct environment access**

### **Context Analysis Variables:**
- **`NLP_FEATURE_PATTERN_ANALYSIS`** - Enable pattern analysis features
- **`NLP_FEATURE_CONTEXT_ANALYSIS`** - Enable context analysis features
- **`NLP_TEMPORAL_CONTEXT_WINDOW`** - Context window size
- **`NLP_CONFIG_CRISIS_CONTEXT_BOOST_MULTIPLIER`** - Crisis context amplification

### **Semantic Analysis Variables:**
- **`NLP_ANALYSIS_CONTEXT_BOOST_WEIGHT`** - Context boost weight for scoring
- **Semantic similarity thresholds** - Via analysis parameters configuration
- **Context window configurations** - Via temporal and context settings

---

## 🏗️ **Integration Points**

### **Upstream Dependencies:**
- **UnifiedConfigManager** - Configuration loading and environment variable access

### **Downstream Integration:**
- **CrisisAnalyzer** - **PRIMARY CONSUMER** - Context analysis for crisis detection (Step 10.8)
- **PatternDetectionManager** - Enhanced pattern detection via context integration
- **API endpoints** - Context analysis data for response enrichment

### **Critical Data Flow:**
```
Message → ContextPatternManager → Context Analysis → CrisisAnalyzer → Enhanced Detection
```

---

## 🔍 **Method Overlap Analysis**

### **High Overlap Methods (Candidates for SharedUtilitiesManager):**
1. **Text preprocessing and tokenization** - Message parsing utilities used across system
2. **Configuration loading and validation** - JSON loading patterns
3. **Parameter bounds checking** - Configuration validation utilities
4. **Regular expression pattern matching** - Negation pattern detection utilities
5. **Error handling with fallbacks** - Graceful degradation patterns
6. **Context window calculations** - Text window extraction utilities

### **Learning-Specific Methods (for LearningSystemManager):**
1. **Context weight optimization** - Learning-based context parameter tuning
2. **Semantic threshold adaptation** - Adaptive threshold learning
3. **Context effectiveness tracking** - Performance analytics for context analysis
4. **Context window optimization** - Dynamic window sizing based on effectiveness

### **Analysis-Specific Methods (Stays in ContextPatternManager):**
1. **`analyze_message_context()`** - **CRITICAL** - Enhanced context analysis for crisis
2. **`extract_context_signals()`** - Context signal extraction
3. **`score_term_in_context()`** - Context-aware term scoring
4. **`identify_negation_context()`** - Negation handling for crisis context
5. **`determine_semantic_context()`** - Crisis-specific semantic analysis

---

## 🔄 **Migration History (Step 10.8)**

### **Migrated from `utils/context_helpers.py`:**
This manager was created by consolidating utility functions into the manager architecture as part of Clean v3.1 compliance:

1. **`extract_context_signals()`** - Migrated from utils function
2. **`score_term_in_context()`** - Migrated from utils function
3. **Context analysis patterns** - Consolidated from various utility functions

### **Integration with CrisisAnalyzer:**
As part of Step 10.8, this manager was integrated directly into CrisisAnalyzer to eliminate the need for separate utility imports and improve architecture compliance.

---

## ⚠️ **Configuration Dependency**

### **Complex Configuration Requirements:**
- **Multiple JSON files** - Requires both context patterns and analysis parameters
- **Environment variable integration** - Multiple environment variables for configuration
- **Fallback mechanisms** - Safe defaults when configuration loading fails
- **Cross-manager dependencies** - Integration with PatternDetectionManager

### **Initialization Resilience:**
- **Graceful fallback** - Continues to function with basic defaults if configuration fails
- **Error logging** - Comprehensive error tracking for configuration issues
- **Safe defaults** - Minimal functionality maintained even with configuration errors

---

## 📋 **Consolidation Recommendations**

### **Move to SharedUtilitiesManager:**
- Text preprocessing and tokenization utilities
- JSON configuration loading patterns
- Parameter validation and bounds checking
- Regular expression pattern utilities
- Context window calculation utilities
- Error handling with fallback patterns

### **Extract to LearningSystemManager:**
- Context weight optimization methods
- Semantic threshold adaptation logic
- Context effectiveness tracking
- Context window optimization algorithms

### **Keep in ContextPatternManager:**
- **`analyze_message_context()`** - **CRITICAL** - Enhanced crisis context analysis
- **`extract_context_signals()`** - Crisis-specific context signal extraction
- **`score_term_in_context()`** - Context-aware scoring for crisis detection
- **`identify_negation_context()`** - Negation handling for crisis contexts
- **`determine_semantic_context()`** - Crisis-specific semantic analysis
- **PatternDetectionManager integration** - Crisis-specific context enhancement

---

## ✅ **Phase 3e Step 1.1 Status**

**Manager**: context_pattern_manager.py  
**Documentation**: ✅ **COMPLETE**  
**Core Methods**: 8 identified  
**Shared Methods**: 6 identified for SharedUtilitiesManager  
**Learning Methods**: 4 identified for LearningSystemManager  
**Analysis Methods**: 5 remain in current manager (crisis-specific context analysis)  

**Key Finding**: Recently migrated from utils (Step 10.8) - represents successful utility consolidation pattern

**Next Manager**: feature_config_manager.py