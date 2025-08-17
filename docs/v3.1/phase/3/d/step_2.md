<!-- ash-nlp/docs/v3.1/phase/3/d/step_2.md -->
<!--
Documentation for Phase 3d, Step 2 for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-2-1
LAST MODIFIED: 2025-08-13
PHASE: 3d, Step 2
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# Phase 3d: Unified Configuration Architecture Design

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp (v3.1 branch)  
**Project**: Ash-NLP v3.1 Configuration Migration  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

---

## 🏗️ **Step 2: Design Unified Configuration Architecture**

**Step Status**: 🚀 **IN PROGRESS**  
**Objective**: Design single, consolidated configuration management system  
**Input**: Complete audit of 150+ environmental variables and 3 competing systems  
**Output**: Unified architecture design with Clean v3.1 compliance

---

## 🎯 **Unified Architecture Design**

### **🔧 Core Architecture Principles**

#### **Single Source of Truth**
- **One ConfigManager**: Consolidate ConfigManager + EnvConfigManager + Direct Usage
- **JSON Defaults**: All variables have sensible defaults in JSON configuration files
- **Environment Overrides**: All variables can be overridden via environment variables
- **Schema Validation**: All variables validated with type checking, ranges, and choices

#### **Clean v3.1 Compliance**
- **Factory Functions**: All managers use `create_*` factory functions
- **Dependency Injection**: ConfigManager passed to all managers as first parameter
- **Fail-Fast Validation**: Invalid configurations prevent system startup
- **JSON + ENV Pattern**: Maintain successful Phase 3a-3c configuration approach

### **🏛️ Unified ConfigManager Design**

#### **New Unified ConfigManager Architecture**
```python
class UnifiedConfigManager:
    """
    Unified Configuration Manager for Ash-NLP v3.1d
    Consolidates JSON configuration with environment variable overrides
    Includes comprehensive schema validation and type checking
    """
    
    def __init__(self, config_dir: str = "/app/config"):
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.variable_schemas = self._load_variable_schemas()
        self.env_override_pattern = re.compile(r'\$\{([^}]+)\}')
        
        # Load configuration files mapping
        self.config_files = {
            'model_ensemble': 'model_ensemble.json',
            'crisis_patterns': 'crisis_patterns.json', 
            'analysis_parameters': 'analysis_parameters.json',
            'threshold_mapping': 'threshold_mapping.json',
            'server_settings': 'server_settings.json',     # NEW
            'storage_settings': 'storage_settings.json',   # NEW
            'logging_settings': 'logging_settings.json',   # NEW
            'feature_flags': 'feature_flags.json'          # NEW
        }
    
    def _load_variable_schemas(self) -> Dict[str, Dict]:
        """Load comprehensive variable schemas for validation"""
        # Implement schema loading from JSON file
    
    def get_environment_variable(self, variable_name: str, default: Any = None) -> Any:
        """Centralized environment variable access with validation"""
        # Replace ALL os.getenv() calls in codebase
    
    def validate_all_variables(self) -> Dict[str, Any]:
        """Comprehensive validation of all environment variables"""
        # Implement fail-fast validation for all variables
    
    def get_variable_by_category(self, category: str) -> Dict[str, Any]:
        """Get all variables for a specific category (models, thresholds, etc.)"""
        # Enable category-based variable access
```

### **📋 Variable Schema Design**

#### **Comprehensive Variable Schemas**
```json
{
  "variable_schemas": {
    "models": {
      "NLP_MODEL_DEPRESSION_NAME": {
        "type": "string",
        "default": "j-hartmann/emotion-english-distilroberta-base",
        "description": "HuggingFace model name for depression detection",
        "category": "model_configuration",
        "validation": {
          "required": true,
          "min_length": 5
        }
      },
      "NLP_MODEL_DEPRESSION_WEIGHT": {
        "type": "float",
        "default": 0.4,
        "description": "Ensemble weight for depression model",
        "category": "model_configuration", 
        "validation": {
          "min": 0.0,
          "max": 1.0,
          "precision": 2
        }
      }
    },
    "server": {
      "NLP_SERVER_HOST": {
        "type": "string", 
        "default": "0.0.0.0",
        "description": "Server host address",
        "category": "server_configuration"
      },
      "GLOBAL_NLP_API_PORT": {
        "type": "integer",
        "default": 8881,
        "description": "Server port (GLOBAL ecosystem variable)",
        "category": "server_configuration",
        "preserve_global": true,
        "validation": {
          "min": 1024,
          "max": 65535
        }
      }
    },
    "thresholds": {
      "NLP_THRESHOLD_CONSENSUS_CRISIS_HIGH": {
        "type": "float",
        "default": 0.50, 
        "description": "Consensus mode crisis to high severity threshold",
        "category": "threshold_configuration",
        "validation": {
          "min": 0.0,
          "max": 1.0,
          "ordering": "high > medium > low"
        }
      }
    }
  }
}
```

---

## 🎯 **Variable Consolidation Plan**

### **🔥 CRITICAL: Duplicate Variable Resolution**

#### **Server Configuration Consolidation**
```bash
# BEFORE (5 duplicates):
GLOBAL_NLP_API_PORT=8881      # ← KEEP (ecosystem requirement)
NLP_SERVICE_PORT=8881         # ← REMOVE (duplicate)  
NLP_PORT=8881                 # ← REMOVE (duplicate)
NLP_HOST=0.0.0.0              # ← RENAME to NLP_SERVER_HOST
NLP_SERVICE_HOST=0.0.0.0      # ← REMOVE (duplicate)

# AFTER (2 clean variables):  
GLOBAL_NLP_API_PORT=8881      # ← PRESERVED
NLP_SERVER_HOST=0.0.0.0       # ← UNIFIED
```

#### **Model Configuration Consolidation**
```bash
# BEFORE (inconsistent naming):
NLP_MODEL_WEIGHT_DEPRESSION=0.4
NLP_ANALYSIS_ENSEMBLE_WEIGHT_DEPRESSION=0.4  # ← DUPLICATE

# AFTER (consistent naming):
NLP_MODEL_DEPRESSION_WEIGHT=0.4              # ← STANDARDIZED
```

#### **Cache Directory Consolidation**  
```bash
# BEFORE (3 variables for same directory):
NLP_MODELS_DIR=./models/cache
NLP_MODEL_CACHE_DIR=./models/cache         # ← REMOVE
NLP_HUGGINGFACE_CACHE_DIR=./models/cache   # ← REMOVE

# AFTER (1 variable):
NLP_STORAGE_MODELS_DIR=./models/cache      # ← UNIFIED
```

#### **Timeout Configuration Consolidation**
```bash
# BEFORE (2 different timeouts):
NLP_REQUEST_TIMEOUT=40        # Server timeout (seconds)
NLP_ANALYSIS_TIMEOUT_MS=5000  # Analysis timeout (milliseconds)

# AFTER (clear differentiation):
NLP_SERVER_REQUEST_TIMEOUT=40      # Server-level timeout (seconds)
NLP_ANALYSIS_TIMEOUT=5000          # Analysis timeout (milliseconds)  
```

### **📝 Standard Naming Convention Implementation**

#### **Category-Based Naming Standards**
```bash
# GLOBAL Variables (PRESERVE exactly as-is):
GLOBAL_HUGGINGFACE_TOKEN
GLOBAL_NLP_API_PORT
GLOBAL_ALLOWED_IPS
GLOBAL_ENABLE_CORS
GLOBAL_LOG_LEVEL

# Model Configuration:
NLP_MODEL_{MODEL_TYPE}_{ATTRIBUTE}
NLP_MODEL_DEPRESSION_NAME
NLP_MODEL_DEPRESSION_WEIGHT
NLP_MODEL_SENTIMENT_NAME
NLP_MODEL_SENTIMENT_WEIGHT

# Threshold Configuration:  
NLP_THRESHOLD_{MODE}_{MAPPING}_{LEVEL}
NLP_THRESHOLD_CONSENSUS_CRISIS_HIGH
NLP_THRESHOLD_MAJORITY_CRISIS_MEDIUM
NLP_THRESHOLD_WEIGHTED_CRISIS_LOW

# Analysis Configuration:
NLP_ANALYSIS_{FUNCTION}_{ATTRIBUTE}
NLP_ANALYSIS_CONFIDENCE_BOOST_HIGH
NLP_ANALYSIS_CONTEXT_WEIGHT
NLP_ANALYSIS_TIMEOUT

# Server Configuration:
NLP_SERVER_{ATTRIBUTE}
NLP_SERVER_HOST
NLP_SERVER_WORKERS
NLP_SERVER_REQUEST_TIMEOUT

# Storage Configuration:
NLP_STORAGE_{TYPE}_DIR  
NLP_STORAGE_DATA_DIR
NLP_STORAGE_MODELS_DIR
NLP_STORAGE_LOGS_DIR

# Feature Flags:
NLP_ENABLE_{FEATURE}
NLP_ENABLE_ENSEMBLE_ANALYSIS
NLP_ENABLE_THRESHOLD_LEARNING
NLP_ENABLE_PATTERN_INTEGRATION
```

---

## 🔧 **JSON Configuration Strategy: EXTEND EXISTING FILES**

### **Approach: Enhance Current JSON Files Rather Than Replace**

#### **✅ Files to KEEP and ENHANCE:**
- `config/model_ensemble.json` - **EXTEND** with cleaned model variables
- `config/analysis_parameters.json` - **ENHANCE** with consolidated analysis variables  
- `config/threshold_mapping.json` - **MAINTAIN** (Phase 3c working perfectly)
- `config/performance_settings.json` - **EXTEND** with server performance variables

#### **✅ Files to ADD for New Categories:**
- `config/server_settings.json` - **NEW** (server configuration consolidation)
- `config/storage_settings.json` - **NEW** (storage path consolidation) 
- `config/feature_flags.json` - **NEW** (feature toggle consolidation)

### **Enhanced Configuration Structure**

#### **config/model_ensemble.json** (ENHANCED - not replaced)
```json
{
  "model_ensemble": {
    "version": "3.1d-enhanced",
    "architecture": "clean-v3.1-unified",
    "model_definitions": {
      "depression": {
        "name": "${NLP_MODEL_DEPRESSION_NAME}",
        "weight": "${NLP_MODEL_DEPRESSION_WEIGHT}",
        "type": "text-classification",
        "purpose": "Depression and mental health crisis detection"
      },
      "sentiment": {
        "name": "${NLP_MODEL_SENTIMENT_NAME}",
        "weight": "${NLP_MODEL_SENTIMENT_WEIGHT}",
        "type": "sentiment-analysis", 
        "purpose": "Overall emotional sentiment analysis"
      },
      "emotional_distress": {
        "name": "${NLP_MODEL_DISTRESS_NAME}",
        "weight": "${NLP_MODEL_DISTRESS_WEIGHT}",
        "type": "emotion-classification",
        "purpose": "Emotional distress and urgency detection"
      }
    },
    "ensemble_settings": {
      "mode": "${NLP_ENSEMBLE_MODE}",
      "validation": {
        "ensure_weights_sum_to_one": true,
        "fail_on_invalid_weights": true
      }
    },
    "defaults": {
      "model_definitions": {
        "depression": {
          "name": "j-hartmann/emotion-english-distilroberta-base",
          "weight": 0.4
        },
        "sentiment": {
          "name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
          "weight": 0.3
        },
        "emotional_distress": {
          "name": "j-hartmann/emotion-english-distilroberta-base",
          "weight": 0.3
        }
      },
      "ensemble_mode": "consensus"
    }
  }
}
```

#### **config/performance_settings.json** (ENHANCED - not replaced)  
```json
{
  "performance_configuration": {
    "version": "3.1d-enhanced",
    "hardware_settings": {
      "device": "${NLP_HARDWARE_DEVICE}",
      "precision": "${NLP_HARDWARE_PRECISION}",
      "max_batch_size": "${NLP_HARDWARE_MAX_BATCH_SIZE}",
      "inference_threads": "${NLP_HARDWARE_INFERENCE_THREADS}"
    },
    "server_performance": {
      "max_concurrent_requests": "${NLP_SERVER_MAX_CONCURRENT}",
      "request_timeout": "${NLP_SERVER_REQUEST_TIMEOUT}",
      "analysis_timeout": "${NLP_ANALYSIS_TIMEOUT}"
    },
    "memory_optimization": {
      "enable_caching": "${NLP_PERFORMANCE_ENABLE_CACHING}",
      "cache_ttl": "${NLP_PERFORMANCE_CACHE_TTL}",
      "enable_parallel_processing": "${NLP_PERFORMANCE_ENABLE_PARALLEL}"
    },
    "defaults": {
      "hardware_settings": {
        "device": "auto",
        "precision": "float16", 
        "max_batch_size": 32,
        "inference_threads": 16
      },
      "server_performance": {
        "max_concurrent_requests": 20,
        "request_timeout": 40,
        "analysis_timeout": 5000
      },
      "memory_optimization": {
        "enable_caching": true,
        "cache_ttl": 300,
        "enable_parallel_processing": true
      }
    }
  }
}
```

#### **config/server_settings.json** (NEW - for consolidated server variables)
```json
{
  "server_configuration": {
    "version": "3.1d",
    "network_settings": {
      "host": "${NLP_SERVER_HOST}",
      "workers": "${NLP_SERVER_WORKERS}",
      "reload_on_changes": "${NLP_SERVER_RELOAD_ON_CHANGES}"
    },
    "security_settings": {
      "rate_limiting": {
        "requests_per_minute": "${NLP_PERFORMANCE_RATE_LIMIT_PER_MINUTE}",
        "requests_per_hour": "${NLP_SECURITY_REQUESTS_PER_HOUR}"
      }
    },
    "defaults": {
      "network_settings": {
        "host": "0.0.0.0",
        "workers": 1,
        "reload_on_changes": false
      },
      "security_settings": {
        "rate_limiting": {
          "requests_per_minute": 120,
          "requests_per_hour": 2000
        }
      }
    }
  }
}
```

---

## 🧪 **Migration Strategy**

### **Phase 1: Models & Thresholds (CRITICAL)**
1. **Consolidate model configuration variables** (10+ variables)
2. **Standardize threshold variable naming** (100+ variables) 
3. **Remove model weight duplicates** (6 duplicate variables)
4. **Update all Phase 3a-3c managers** to use unified system

### **Phase 2: Analysis Parameters (HIGH PRIORITY)**
1. **Consolidate analysis parameter variables** (25+ variables)
2. **Remove analysis-related duplicates** (5+ duplicates)
3. **Update AnalysisParametersManager** for unified system

### **Phase 3: Server & Infrastructure (MEDIUM PRIORITY)**  
1. **Resolve server configuration duplicates** (5+ duplicates)
2. **Standardize server variable naming**
3. **Create new server_settings.json** configuration file

### **Phase 4: Storage, Logging, Features (LOW PRIORITY)**
1. **Consolidate storage directory variables** (4+ duplicates) 
2. **Organize logging configuration variables** (10+ variables)
3. **Clean up feature flag variables** (15+ variables)

---

## ✅ **Implementation Validation**

### **Success Criteria**
- [ ] **Single ConfigManager**: All environment variables accessed through unified system
- [ ] **Schema Validation**: All 150+ variables have schema validation  
- [ ] **Zero Duplicates**: All duplicate variables eliminated
- [ ] **Standard Naming**: All variables follow naming conventions (except GLOBAL_*)
- [ ] **JSON + ENV Pattern**: All variables have JSON defaults with environment overrides
- [ ] **Clean v3.1 Compliance**: Factory functions and dependency injection maintained
- [ ] **Phase 3a-3c Preservation**: All previous functionality continues working

### **Validation Tests**
- [ ] **Variable Schema Tests**: All schemas validate correctly
- [ ] **Environment Override Tests**: All variables can be overridden  
- [ ] **Manager Integration Tests**: All managers work with unified system
- [ ] **Factory Function Tests**: All factory functions use unified ConfigManager
- [ ] **Production Functionality Tests**: Core NLP functionality remains operational

---

**Status**: 🚀 **STEP 2 DESIGN COMPLETE**  
**Next Action**: Begin Step 3 - Implement Models & Thresholds Cleanup  
**Architecture**: Unified ConfigManager design ready for implementation  
**Priority**: Start with CRITICAL variables (models & thresholds) affecting core functionality