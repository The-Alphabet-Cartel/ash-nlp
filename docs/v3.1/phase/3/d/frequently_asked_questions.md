# Frequently Asked Questions
1. **Migration Strategy**
  - *Should we maintain backward compatibility for the old variable names during a transition period, or do a complete cutover?*
    - I would prefer to break the system (as we are using GitHub's sub-versioning, so rolling back if needed is not a big deal) and get things working from there, so let's just cutover and rip the band-aids off.

2. **Priority Order**
  - *Which category of variables should we tackle first?*
    - We'll be starting with the most critical (models, threshold) and working toward less critical (logging, features).

3. **Naming Convention**
  - *What naming convention for variables will we be using?*
    - NLP_CATEGORY_SPECIFIC_FUNCTION=value

4. **Variables System Functionality**
  - *How does the variables system function?*
    - The JSON files shall assign defaults.
    - Environmental variables shall be able to override them.
    - Ideally configuration changes shall be able to be done "on the fly".
      - Some of the NLP server's functionality this is an impossible ask, so for those instances we will require server restarts.

5. **Testing Scope**
  - *Should we create a comprehensive Phase test suite, or focus on testing integration points with the previous phase's test suites?*
    - Each phase should have it's own comprehensive testing suite.

6. **Existing JSON Files**
  - *How do we handle existing JSON files?*
    - We keep, extend, and enhance any existing JSON files.

7. **Existing Managers**
  - *How do we handle existing managers?*
    - As with the JSON files, we will be keeping, extending, and enhancing existing managers.
    - We only add new handlers when required to do so for clarity purposes of new functionality.

8. **Backward Compatibility**
  - *Should our code be backwards compatible?*
    - Not really.
      - The only backwards compatibility we need is within the same phase of implementation.
    - We are ripping off the band-aids with a "break and fix" mentality.

9. **Migration / Configuration Scripting**
  - *Should we create migration and/or confirugation scripts to help with changes?*
    - No.
    - I work on one rig, and test on another.
    - Migration / configuration scripting will only break the server rig.