<!-- ash-nlp/docs/v3.1/phase/3/d/step_10.8.md -->
<!--
Documentation for Phase 3d, Step 10.8 for Ash-NLP Service v3.1
FILE VERSION: v3.1-3d-10.8-1
LAST MODIFIED: 2025-08-13
PHASE: 3d, Step 10.8
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: 
-->
# Step 10.8: Consolidate `utils/context_helpers.py`

**Objective**: Create `ContextPatternManager` for semantic analysis

**Scope**: Create new manager for context and semantic analysis:
- Review all functions in `utils/context_helpers.py`
- Create new `ContextPatternManager` following Clean v3.1 patterns
- Migrate context analysis functions to new manager
- Integrate with `CrisisAnalyzer` and `AnalysisParametersManager`
- Create factory function and JSON configuration
- **Apply Rule #7**: Check existing environment variables before creating new ones

**Success Criteria**:
- New `ContextPatternManager` fully functional
- All context analysis functionality centralized
- No remaining references to `utils/context_helpers.py`
- File successfully removed from ecosystem
- Clean v3.1 architecture compliance
- **Prefer no new environment variables** (following Rule #7)

---

**The mental health crisis detection system for The Alphabet Cartel community now has cleaner, more maintainable, and better-integrated community pattern functionality!**

**Ready for Step 10.8 - Context Pattern Management! 🚀**