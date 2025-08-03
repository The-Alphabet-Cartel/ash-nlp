# NLP Configuration Migration Implementation Guide

## Overview
This guide outlines the complete recode of the configuration system for clean JSON + environment variable management without backward compatibility concerns.

## Current Issues Identified

1. **Environment Variable Substitution**: The JSON placeholders like `${NLP_DEPRESSION_MODEL}` are not being replaced with actual environment values
2. **Model Mismatch**: The loaded models don't match the `.env` file configuration
3. **Parameter Mismatches**: `PhraseExtractor` and `CrisisAnalyzer` initialization errors due to wrong parameter counts

## Solution Architecture (Clean Implementation)

### 1. Enhanced ConfigManager (`managers/config_manager.py`)
- **Environment Variable Substitution**: Automatically replaces `${VAR_NAME}` with actual environment values
- **Fallback Support**: Uses JSON defaults when environment variables are not set
- **Type Conversion**: Properly converts string environment variables to appropriate types (bool, int, float)
- **Validation**: Ensures configuration integrity
- **No Backward Compatibility**: Clean implementation for managers-only architecture

### 2. Updated ModelManager (`models/ml_models.py`)
- **Configuration Integration**: Accepts processed configuration from ConfigManager
- **Dynamic Model Loading**: Loads models based on environment-overridden configuration
- **Manager-Only Architecture**: Requires ConfigManager, no fallback to environment-only
- **Flexible Ensemble Support**: Handles different ensemble modes (majority, weighted, consensus)

### 3. Clean Initialization (`main.py`)
- **Manager-First Architecture**: All components require proper manager integration
- **No Parameter Detection**: Components must support the new manager parameter structure
- **Comprehensive Logging**: Detailed status reporting and error handling
- **Fail-Fast**: If components don't support managers, initialization fails with clear error messages

## Current Status - Component Imports Resolved ✅

### 🎯 Progress Made
✅ **CrisisAnalyzer**: Import successful - no more pattern constant errors  
✅ **PhraseExtractor**: Import successful - no more pattern constant errors  
✅ **Pattern Constants**: All required constants now available in SettingsManager  
✅ **Manager Architecture**: Core system working cleanly  

### 🔧 Remaining Issue - Learning Module Import

**Issue: Learning Module Path** ⚠️ **LAST REMAINING**
```
⚠️ EnhancedLearningManager import failed: No module named 'endpoints'
```

**Root Cause**: The learning module still has hardcoded imports pointing to old `endpoints` directory

**Solution Options**:
1. **Move/symlink**: Create `endpoints` as symlink to `api`
2. **Update learning module**: Change imports inside learning module from `endpoints` to `api`
3. **Temporarily disable**: Skip learning module to test core environment variable substitution

### 📋 Next Action

**Option A: Quick Test Core System** ⚠️ **RECOMMENDED**
Temporarily disable learning to test environment variable substitution:
```python
# In main.py - temporarily set:
ENHANCED_LEARNING_AVAILABLE = False
```

**Option B: Fix Learning Module** ⚠️ **PERMANENT FIX**
Update any imports inside the learning module files that reference `from endpoints.` to `from api.`

### 🎯 Expected Core System Results

Once learning is bypassed, we should see:
```
✅ ConfigManager initialized with config directory: /app/config
🔍 DEBUG: Key Environment Variables:
   NLP_DEPRESSION_MODEL: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
   NLP_SENTIMENT_MODEL: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
   NLP_EMOTIONAL_DISTRESS_MODEL: Lowerated/lm6-deberta-v3-topic-sentiment
🔄 DEBUG: Substituting ${NLP_SENTIMENT_MODEL} = MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
✅ Model configuration processing complete
```

**Status**: 95% complete - only learning module import path needs fixing. Core architecture and environment substitution ready to test.

### Step 4: Update Component Classes (REQUIRED)
1. **CrisisAnalyzer** must be updated to accept: `(model_manager, config_manager, settings_manager, learning_manager)`
2. **PhraseExtractor** must be updated to accept: `(model_manager, config_manager, zero_shot_manager)`
3. **EnhancedLearningManager** must be updated to accept: `(model_manager, config_manager, settings_manager)`
4. **Status**: ⚠️ COMPONENTS NEED UPDATING

### Step 5: Update Endpoint Integration
1. Ensemble endpoints need ConfigManager parameter
2. Learning endpoints need ConfigManager parameter  
3. **Status**: ⚠️ ENDPOINTS NEED UPDATING

### Step 6: Verify Configuration
1. Check that your `.env` file values are being used
2. Monitor startup logs for environment override confirmations
3. **Status**: Ready for testing after implementation

## Expected Results (Clean Architecture)

After implementation, you should see:

```
🎯 Final Model Configuration (JSON + Environment Overrides):
   Depression Model: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
   Depression Weight: 0.75
   Sentiment Model: Lowerated/lm6-deberta-v3-topic-sentiment  
   Sentiment Weight: 0.10
   Emotional_Distress Model: Lowerated/lm6-deberta-v3-topic-sentiment
   Emotional_Distress Weight: 0.15
   Ensemble Mode: majority
   Gap Detection: ✅ Enabled
```

And clean component status:
```
📊 Component Initialization Summary:
   Core Managers:
     config_manager: ✅
     settings_manager: ✅  
     zero_shot_manager: ✅
   Ml Components:
     model_manager: ✅
     three_model_ensemble: ✅
   Analysis Components:
     crisis_analyzer: ❌ (needs manager support)
     phrase_extractor: ❌ (needs manager support)
     enhanced_learning: ❌ (needs manager support)
```

**Note**: Analysis components will fail until updated to support the new manager architecture.

## Key Features

### Environment Override Priority
```
Environment Variable > JSON Configuration > Hardcoded Defaults
```

### Dynamic Parameter Handling
The system automatically detects what parameters each class accepts:
- `CrisisAnalyzer(model_manager)` - Basic
- `CrisisAnalyzer(model_manager, learning_manager)` - With learning
- `CrisisAnalyzer(model_manager, learning_manager, config_manager)` - Full support

### Configuration Validation
- Model weights must sum to 1.0
- All required models must be present
- Environment variables are properly typed

## Configuration File Structure

The system loads configuration from:
- `ash/ash-nlp/config/model_ensemble.json` - Main ensemble configuration (current)
- `ash/ash-nlp/config/crisis_patterns.json` - Crisis patterns (planned)
- `ash/ash-nlp/config/analysis_parameters.json` - Analysis settings (planned)
- `ash/ash-nlp/config/performance_settings.json` - Performance tuning (planned)
- `ash/ash-nlp/config/threshold_mapping.json` - Threshold mappings (planned)

## Testing the Implementation

1. **Start the Container**:
   ```bash
   docker compose up -d ash-nlp
   ```

2. **Check Logs**:
   ```bash
   docker logs ash-nlp
   ```

3. **Look for**:
   - ✅ Environment override messages
   - Correct model names from your `.env` file
   - No parameter mismatch errors
   - All three models loading successfully

## Troubleshooting

### If Environment Variables Aren't Being Applied
- Check that the `.env` file is in the correct location (`ash/.env`)
- Verify Docker Compose is reading the environment file
- Check for typos in variable names

### If Parameter Errors Persist
- The system should auto-detect parameter requirements
- Check that the classes are importing correctly
- Review initialization logs for specific error messages

### If Models Don't Match .env
- Verify the ConfigManager is properly substituting variables
- Check the configuration validation output
- Ensure environment variables are properly formatted

## Benefits

1. **Environment Override Support**: JSON serves as defaults, ENV variables override
2. **Backward Compatibility**: Works with existing classes that don't support managers
3. **Future-Proof**: Easy to add new configuration files and managers
4. **Comprehensive Logging**: Detailed status and error reporting
5. **Configuration Validation**: Ensures system integrity

## Next Steps

After implementing these changes:
1. Test with your current `.env` configuration
2. Gradually populate the empty JSON files with additional settings
3. Migrate hardcoded values to the JSON configuration system
4. Add hot-reload capability if needed in the future