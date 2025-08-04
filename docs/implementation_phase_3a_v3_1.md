# Phase 3a: Crisis Patterns Configuration Migration
## Comprehensive Analysis & Implementation Plan

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Branch**: v3.1  
**Phase**: 3a - Crisis Patterns Configuration Migration  
**Document Date**: August 4, 2025

---

## 🎯 Phase 3a Overview

**Objective**: Migrate all hardcoded crisis patterns from Python files to JSON configuration files with environment variable override capabilities, following the clean v3.1 architecture established in Phase 2C.

**Scope**: **ONLY** ash-nlp service (ash-bot will be addressed in future conversations)

**Architecture**: Continue clean v3.1 approach with **NO backward compatibility**

---

## 📊 Crisis Patterns Inventory Analysis

Based on the **CURRENT** `settings_manager.py` file you provided, here's the comprehensive inventory of crisis patterns currently hardcoded in the system:

### 🗂️ Current File Structure (ACTUAL v3.1 Structure)

```
ash/ash-nlp/
├── analysis/               # Analysis components
│   ├── crisis_analyzer.py  
│   └── phrase_extractor.py 
├── config/                 # JSON configuration files ONLY
│   ├── analysis_parameters.json
│   ├── crisis_patterns.json      # 🎯 TARGET: Will contain migrated patterns
│   ├── label_config.json
│   ├── learning_parameters.json
│   ├── model_ensemble.json
│   ├── performance_settings.json
│   └── threshold_mapping.json
├── managers/               # All manager classes
│   ├── config_manager.py   # 🔧 Will load crisis patterns JSON
│   ├── settings_manager.py # ⚠️ CONTAINS ALL CRISIS PATTERNS (Current)
│   ├── zero_shot_manager.py
│   ├── models_manager.py
│   └── pydantic_manager.py
├── utils/                  # Utility and Helper Files
│   ├── community_patterns.py  
│   ├── context_helpers.py     
│   └── scoring_helpers.py     
```

### 📋 Crisis Patterns Categories (FROM CURRENT settings_manager.py)

From the **actual current** `managers/settings_manager.py` file, these pattern constants need migration:

#### 1. **LGBTQIA+ Patterns** (`LGBTQIA_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 70-134)
- **Description**: Community-specific crisis patterns for LGBTQIA+ users
- **Target JSON**: `config/crisis_lgbtqia_patterns.json`
- **Contains**: 5 categories with 50+ patterns
  - Family rejection patterns (HIGH crisis)
  - Identity crisis patterns (MEDIUM)
  - Dysphoria and transition patterns (MEDIUM)
  - Discrimination and safety patterns (HIGH)
  - Community support patterns (LOW)

#### 2. **Burden Patterns** (`BURDEN_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 264-268)
- **Description**: Expressions of feeling like a burden to others
- **Target JSON**: `config/crisis_burden_patterns.json`
- **Contains**: 6 burden-related expressions
  - 'better off without me', 'everyone would be better without me'
  - 'better off if i was gone', 'better off if i wasn\'t here'
  - 'nobody would miss me', 'wouldn\'t be missed'

#### 3. **Hopelessness Patterns** (`HOPELESSNESS_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 270-274)
- **Description**: Expressions of hopelessness and despair
- **Target JSON**: `config/crisis_hopelessness_patterns.json`
- **Contains**: 6 hopelessness expressions
  - 'everything feels pointless', 'life feels pointless'
  - 'i hate my life', 'hate my life'
  - 'wish i could disappear', 'want to disappear'

#### 4. **Struggle Patterns** (`STRUGGLE_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 276-280)
- **Description**: General struggle and difficulty patterns
- **Target JSON**: `config/crisis_struggle_patterns.json`
- **Contains**: 4 general struggle expressions
  - 'really struggling', 'struggling so much'
  - 'can\'t take it anymore', 'can\'t go on'

#### 5. **Enhanced Idiom Patterns** (`ENHANCED_IDIOM_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 203-244)
- **Description**: False positive reduction patterns with complex logic
- **Target JSON**: `config/crisis_idiom_patterns.json`
- **Contains**: 5 categories with reduction factors
  - Fatigue idioms (dead tired, exhausted)
  - Humor idioms (joke killed me, dying of laughter)
  - Success idioms (killing it, slaying it)
  - Food craving idioms (murder a burger, kill for food)
  - Frustration idioms (driving me crazy, brutal test)

#### 6. **Positive Context Patterns** (`POSITIVE_CONTEXT_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 47-53)
- **Description**: Patterns indicating positive context
- **Target JSON**: `config/crisis_positive_context_patterns.json`
- **Contains**: 6 categories with multiple patterns each
  - Humor, entertainment, work success, food, fatigue, frustration

#### 7. **Crisis Contexts** (`CRISIS_CONTEXTS`)
- **Current Location**: `managers/settings_manager.py` (lines 136-158)
- **Description**: Contextual modifiers for crisis detection
- **Target JSON**: `config/crisis_context_patterns.json`
- **Contains**: 4 context types with crisis boosts
  - Temporal urgency (HIGH boost), intensity amplifier (MEDIUM)
  - Social isolation (MEDIUM), capability loss (MEDIUM)

#### 8. **Community Vocabulary** (`COMMUNITY_VOCABULARY`)
- **Current Location**: `managers/settings_manager.py` (lines 160-179)
- **Description**: Community-specific vocabulary for semantic analysis
- **Target JSON**: `config/crisis_community_vocabulary.json`
- **Contains**: 4 vocabulary categories
  - Identity terms, experience terms, community terms, struggle terms

#### 9. **Temporal Indicators** (`TEMPORAL_INDICATORS`)
- **Current Location**: `managers/settings_manager.py` (lines 181-187)
- **Description**: Time-based crisis urgency indicators
- **Target JSON**: `config/crisis_temporal_patterns.json`
- **Contains**: 4 temporal categories
  - Immediate, recent, ongoing, future fear indicators

#### 10. **Context Weights** (`CONTEXT_WEIGHTS`)
- **Current Location**: `managers/settings_manager.py` (lines 189-200)
- **Description**: Word weights for context analysis
- **Target JSON**: `config/crisis_context_weights.json`
- **Contains**: 2 weight categories
  - Crisis context words, positive context words

#### 11. **Negation Patterns** (`NEGATION_PATTERNS`)
- **Current Location**: `managers/settings_manager.py` (lines 282-288)
- **Description**: Patterns that negate crisis indicators
- **Target JSON**: `config/crisis_negation_patterns.json`
- **Contains**: 5 regex patterns for negation detection

#### 12. **Basic Idiom Patterns** (`IDIOM_PATTERNS`) 
- **Current Location**: `managers/settings_manager.py` (lines 55-66)
- **Description**: Simple idiom patterns for false positive reduction
- **Target JSON**: `config/basic_idiom_patterns.json`
- **Contains**: 8 tuple patterns with regex and categories

#### 13. **Server/Threshold Constants**
- **Current Location**: `managers/settings_manager.py` (lines 11-45)
- **Description**: Server config and crisis thresholds
- **Target JSON**: Already handled by existing configuration system
- **Contains**: SERVER_CONFIG, CRISIS_THRESHOLDS, DEFAULT_PARAMS

---

## 🎯 Environment Variable Override Strategy

Following your preference to keep the current `.env.template` structure while allowing future expansion with `NLP_CONFIG_*` pattern:

### 🔧 Current .env Variables (Keep As-Is)
All existing threshold and configuration variables remain unchanged:
- `NLP_CONSENSUS_CRISIS_TO_HIGH_THRESHOLD=0.50`
- `NLP_CONSENSUS_CRISIS_TO_MEDIUM_THRESHOLD=0.30`
- `NLP_ENSEMBLE_MODE=consensus`
- etc.

### 🆕 New Pattern Override Variables (Future Expansion)
New environment variables will follow the pattern: `NLP_CONFIG_*something*=*something*`

**Examples for Crisis Patterns**:
```bash
# Pattern weights/multipliers
NLP_CONFIG_LGBTQIA_WEIGHT_MULTIPLIER=1.2
NLP_CONFIG_BURDEN_PATTERN_THRESHOLD=0.7
NLP_CONFIG_HOPELESSNESS_BOOST=0.1

# Enable/disable pattern categories
NLP_CONFIG_ENABLE_LGBTQIA_PATTERNS=true
NLP_CONFIG_ENABLE_IDIOM_FILTERING=true
NLP_CONFIG_ENABLE_TEMPORAL_INDICATORS=true

# Pattern sensitivity levels
NLP_CONFIG_COMMUNITY_VOCABULARY_SENSITIVITY=medium
NLP_CONFIG_CONTEXT_MODIFIER_STRENGTH=1.0
NLP_CONFIG_NEGATION_DETECTION_ENABLED=true
```

---

## 🏗️ JSON Schema Design

### 📁 Multiple Focused Files Approach

Following your preference for clearly labeled, focused files:

#### File Structure
```
config/
├── crisis_lgbtqia_patterns.json         # LGBTQIA+ specific patterns
├── crisis_burden_patterns.json          # Burden/self-worth patterns  
├── crisis_hopelessness_patterns.json    # Hopelessness/despair patterns
├── crisis_struggle_patterns.json        # General struggle patterns
├── crisis_idiom_patterns.json           # False positive prevention
├── crisis_positive_context_patterns.json # Positive context indicators
├── crisis_context_patterns.json         # Contextual modifiers
├── crisis_community_vocabulary.json     # Community vocabulary
├── crisis_temporal_patterns.json        # Time-based indicators
├── crisis_negation_patterns.json        # Negation patterns
└── crisis_patterns_schema.json          # JSON schema validation
```

#### Standard JSON Schema Template
```json
{
  "metadata": {
    "pattern_type": "lgbtqia_patterns",
    "version": "3.1.0",
    "description": "LGBTQIA+ community specific crisis patterns",
    "last_updated": "2025-08-04",
    "total_patterns": 0,
    "environment_overrides": {
      "weight_multiplier": "NLP_CONFIG_LGBTQIA_WEIGHT_MULTIPLIER",
      "enabled": "NLP_CONFIG_ENABLE_LGBTQIA_PATTERNS"
    }
  },
  "configuration": {
    "enabled": true,
    "weight_multiplier": 1.0,
    "confidence_boost": 0.0,
    "priority_level": "high"
  },
  "patterns": {
    "crisis_indicators": [
      {
        "pattern": "example pattern",
        "weight": 1.0,
        "context_required": false,
        "severity": "high",
        "description": "Pattern description"
      }
    ],
    "context_modifiers": [
      {
        "context": "supportive_response",
        "modifier": 0.8,
        "description": "Reduce crisis score in supportive contexts"
      }
    ]
  }
}
```

---

## 🔧 Integration Architecture

### 🔧 ConfigManager Integration

The existing `ConfigManager` will be enhanced to load crisis patterns from JSON files. Based on the current structure, the integration will work as follows:

```python
# managers/config_manager.py (Enhancement for Phase 3a)
class ConfigManager:
    def __init__(self, config_dir="/app/config"):
        # ... existing initialization ...
        self.crisis_patterns = self._load_crisis_patterns()
        
    def _load_crisis_patterns(self):
        """Load all crisis pattern JSON files"""
        patterns = {}
        
        pattern_files = [
            'crisis_lgbtqia_patterns.json',
            'crisis_burden_patterns.json', 
            'crisis_hopelessness_patterns.json',
            'crisis_struggle_patterns.json',
            'crisis_idiom_patterns.json',
            'crisis_positive_context_patterns.json',
            'crisis_context_patterns.json',
            'crisis_community_vocabulary.json',
            'crisis_temporal_patterns.json',
            'crisis_context_weights.json',
            'crisis_negation_patterns.json',
            'basic_idiom_patterns.json'
        ]
        
        for pattern_file in pattern_files:
            pattern_type = pattern_file.replace('crisis_', '').replace('basic_', '').replace('.json', '')
            patterns[pattern_type] = self._load_pattern_file(pattern_file)
            
        return patterns
    
    def get_crisis_patterns(self, pattern_type: str = None):
        """Get crisis patterns (all or specific type)"""
        if pattern_type:
            return self.crisis_patterns.get(pattern_type, {})
        return self.crisis_patterns
```

### 📦 SettingsManager Integration  

The current `SettingsManager` will be updated to use patterns from `ConfigManager` instead of hardcoded constants:

```python
# managers/settings_manager.py (Phase 3a Updates)
class SettingsManager:
    def __init__(self, config_manager):
        # ... existing initialization ...
        self.crisis_patterns = config_manager.get_crisis_patterns()
        
    def get_lgbtqia_patterns(self):
        """Get LGBTQIA+ patterns from JSON configuration"""
        return self.crisis_patterns.get('lgbtqia_patterns', {})
        
    def get_burden_patterns(self):
        """Get burden patterns from JSON configuration"""  
        return self.crisis_patterns.get('burden_patterns', {})
        
    # ... similar methods for all pattern types ...
```