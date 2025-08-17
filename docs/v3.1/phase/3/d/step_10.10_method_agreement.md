# Step 10.10 Environmental Variables Audit - Methodology Agreement

**Document Purpose**: Consensus methodology for Step 10.10 environmental variables cleanup  
**Status**: Ready for Implementation  
**Target File**: `config/analysis_parameters.json` (first file to process)  
**Clean Architecture**: v3.1 Rule #7 Compliance  

---

## 🎯 **AGREED METHODOLOGY**

### **Systematic 4-Step Process**

#### **Step 1: Audit Against Unresolved Variables List**
- Start with target JSON file (`analysis_parameters.json`)
- Cross-reference against the ~500 unresolved placeholder variables identified in Step 10.9 testing
- Create comprehensive list of ALL unresolved placeholders in the target file

#### **Step 2: Code Usage Check** 
- For each unresolved placeholder variable, search the entire codebase
- Primary focus: Associated manager file (e.g., `managers/crisis_analyzer.py` for analysis_parameters.json)
- Secondary search: All Python files for actual usage
- **Key Question**: Is this setting actually used anywhere in the code beyond the JSON file?

#### **Step 3: Decision Tree Application**
```
IF setting is NOT used in code:
    → Remove EVERYTHING (placeholder, default, validation block)
    
ELSE IF setting IS used in code:
    IF logical existing .env.template variable exists:
        → Map placeholder to existing variable
    ELSE:
        → Leave placeholder as-is for .env.template addition in next step
```

#### **Step 4: Clean Up Empty Blocks**
- If an entire configuration section becomes empty after cleanup → Remove the whole section
- Preserve pattern expressions and actual detection logic (core functionality)
- Remove only configuration overhead that isn't used

---

## 🔧 **IMPLEMENTATION PRINCIPLES**

### **Usage-Driven Cleanup** (Not Placeholder-Driven)
- **Code usage determines what stays** - not theoretical configuration needs
- **If code doesn't use it** → Remove it completely
- **If code uses it** → Find logical mapping or prepare for .env.template addition

### **Rule #7 Compliance**
- **Check existing .env.template FIRST** before considering new variables
- **Map to existing variables** where logical connections exist
- **No new variables** without explicit approval and .env.template addition

### **System Stability Priority**
- **Preserve all detection logic** (expressions, patterns, core functionality)  
- **Remove only configuration overhead** that creates unresolved placeholder warnings
- **Maintain backwards compatibility** where code expects certain settings

---

## 📋 **DECISION MAPPING EXAMPLES**

### **Scenario A: Unused Setting**
```json
// BEFORE: Unresolved placeholder, not used in code
"some_feature_flag": "${NLP_UNUSED_FEATURE_FLAG}",
"defaults": {
    "some_feature_flag": true
},
"validation": {
    "some_feature_flag": {"type": "boolean"}
}

// AFTER: Complete removal
// (entire setting removed)
```

### **Scenario B: Used Setting with Logical Mapping**  
```json
// BEFORE: Unresolved placeholder, used in code, logical mapping exists
"detection_threshold": "${NLP_CRISIS_BURDEN_THRESHOLD}",

// AFTER: Mapped to existing variable
"detection_threshold": "${NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM}",
```

### **Scenario C: Used Setting, No Logical Mapping**
```json
// BEFORE: Unresolved placeholder, used in code, no existing variable
"specialized_setting": "${NLP_SPECIALIZED_UNIQUE_SETTING}",

// AFTER: Left as-is for .env.template addition
"specialized_setting": "${NLP_SPECIALIZED_UNIQUE_SETTING}",
// Note: Will be added to .env.template in subsequent step
```

---

## 🎯 **SUCCESS CRITERIA**

### **Primary Goals**
- ✅ **Eliminate unresolved placeholder warnings** from unused settings
- ✅ **Preserve all working functionality** through usage-based decisions  
- ✅ **Map to existing variables** where logical connections exist
- ✅ **Maintain Clean Architecture Rule #7 compliance**

### **Quality Metrics**
- **Zero functionality loss** - all code-used settings preserved or mapped
- **Significant warning reduction** - unused placeholders eliminated
- **Clean configuration** - empty blocks removed, structure simplified
- **Documentation clarity** - changes tracked and reasoning documented

---

## 📁 **TARGET FILE SEQUENCE**

### **Phase 1: Start Point**
- **File**: `config/analysis_parameters.json`
- **Manager**: `managers/crisis_analyzer.py` (primary usage check)
- **Reason**: Core analysis functionality, well-understood codebase section

### **Future Files** (After analysis_parameters.json success)
- `config/model_ensemble.json`
- `config/crisis_burden_patterns.json` 
- `config/logging_settings.json`
- Additional files as identified

---

## 🚨 **CRITICAL REMINDERS**

### **What We're NOT Doing**
- ❌ **Adding new functionality** - this is cleanup only
- ❌ **Creating new environment variables** without explicit approval
- ❌ **Removing detection logic** - only configuration overhead
- ❌ **Breaking existing working code** - usage-driven preservation

### **What We ARE Doing**  
- ✅ **Removing unused configuration bloat** that creates warnings
- ✅ **Mapping to existing infrastructure** where logical
- ✅ **Following systematic methodology** for consistent results
- ✅ **Maintaining system stability** throughout cleanup process

---

## 📝 **DOCUMENTATION REQUIREMENTS**

### **Track Changes In**
- `docs/v3.1/phase/3/d/step_10.10.md` - Update with actual results
- `docs/v3.1/phase/3/d/tracker.md` - Update completion status
- **This methodology document** - Reference for consistency across conversations

### **Document For Each File**
- **Variables removed** (with reasoning: "not used in code")
- **Variables mapped** (with mapping logic: "maps to existing X")  
- **Variables preserved** (with reasoning: "used in code, no logical mapping")
- **Blocks removed** (when entire sections become empty)

---

## 🏁 **READY TO BEGIN**

**Next Action**: Start Step 1 with `config/analysis_parameters.json`  
**Expected Outcome**: Clean file with only used settings, mapped where possible, unused bloat removed  
**Success Measure**: Significant reduction in unresolved placeholder warnings while preserving all functionality