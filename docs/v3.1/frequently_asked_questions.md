<!-- ash-nlp/docs/v3.1/frequently_asked_questions_v3.1.md -->
<!--
Frequently Asked Questions for Ash-NLP Service
FILE VERSION: v3.1-1
LAST MODIFIED: 2025-08-26
CLEAN ARCHITECTURE: v3.1 Compliant
-->
# ❓Frequently Asked Questions (FAQ)❓

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Project**: Ash-NLP v3.1 Manager Consolidation  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org  
**FILE VERSION**: v3.1-1
**LAST MODIFIED**: 2025-08-26
**CLEAN ARCHITECTURE**: v3.1 Compliant  

---

## Phase 3d
1. **Migration Strategy**
  - *Should we maintain backward compatibility for the old variable names during a transition period, or do a complete cutover?*
    - I would prefer to break the system (as we are using GitHub's sub-versioning, so rolling back if needed is not a big deal) and get things working from there, so let's just cutover and rip the band-aids off.
  - *Should we create migration and/or configuration scripts to help with changes?*
    - No
      - I work on one rig, and test on another.
      - Migration / configuration scripting will only break the server rig.
  - *Should our code be backwards compatible?*
    - Not really
      - The only backwards compatibility we need is within the same phase of implementation.
    - We are ripping off the band-aids with a "break and fix" mentality.
  - *Which category of variables should we tackle first?*
    - We'll be starting with the most critical (models, threshold) and working toward less critical (logging, features).
  - *What naming convention for variables will we be using?*
    - `NLP_CATEGORY_FUNCTION_SETTING=value`
  - *How do we handle existing JSON files?*
    - We keep, extend, and enhance any existing JSON files.
  - *Should we consolidate all duplicate and similar variables into a unified variable?*
    - Yes
      - Any variables that are obvious duplicates and/or similar in functionality should be consolidated into a unified variable using the `NLP_CATEGORY_FUNCTION_SETTING=value` naming convention given previously.
      - Note: All `GLOBAL_*` that are assigned must stay and be used as `GLOBAL_*` variables within the code.
        - These variables are utilized within the greater 'Ash' ecosystem.
  - *How do we handle existing managers?*
    - As with the JSON files, we will be keeping, extending, and enhancing existing managers.
    - We only add new handlers when required to do so for clarity purposes of new functionality.

2. **Variables System Functionality**
  - *How does the variables system function?*
    - The JSON files shall assign defaults.
    - Environmental variables shall be able to override them.
    - Ideally configuration changes shall be able to be done "on the fly".
      - Some of the NLP server's functionality this is an impossible ask, so for those instances we will require server restarts.
  - *Following the established pattern from previous steps, should we implement the same immediate cutover approach where old variable names are immediately replaced with new standardized names?*
    - Yes
    - We are using a "Break and Fix" approach to this recode.

3. **Testing Scope**
  - *Should we create a comprehensive Phase test suite, or focus on testing integration points with the previous phase's test suites?*
    - Each individual phase shall have it's own comprehensive testing suite.
    - Phase implementation steps should only have a testing suite if previous step tests will not suffice to test what we've changed.