# Weight Optimization Implementation Plan - Ash-NLP

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Project**: Ash-NLP v3.1  
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org  
**FILE VERSION**: v3.1-wo-1  
**LAST UPDATED**: 2025-09-01  
**CLEAN ARCHITECTURE**: v3.1 Compliant  

---

## Executive Summary

This document outlines the systematic approach to optimize ensemble model weights and modes for the Ash-NLP crisis detection system. The goal is to find the optimal combination of:
- **Ensemble Mode**: consensus, majority, or weighted
- **Model Weights**: Depression (currently 40%), Sentiment (30%), Emotional Distress (30%)

**Success Criteria**: >5% improvement in F1-score with maintained 200ms performance target.

---

## Dataset Analysis

### Available Test Data (345 phrases total)
- **High Priority (50 phrases)**: Target 98% detection rate - immediate crisis requiring urgent intervention
- **Medium Priority (50 phrases)**: Target 85% detection rate - significant distress requiring attention  
- **Low Priority (50 phrases)**: Target 85% detection rate - mild distress benefiting from support
- **None Priority (50 phrases)**: Target 95% detection rate - positive/neutral content (critical for false positive prevention)
- **Borderline Categories (145 phrases)**:
  - Maybe High/Medium (50): Should detect as medium/high (90% target)
  - Maybe Medium/Low (50): Should detect as low/medium (85% target)  
  - Maybe Low/None (50): Should detect as none/low (90% target)

### Performance Requirements
- **Current Performance**: ~200ms average analysis time
- **Performance Target**: Maintain ≤200ms during optimization
- **Accuracy Target**: >5% improvement in F1-score
- **Deployment**: Immediate rollout via .env updates

---

## Technical Implementation Strategy

### Phase 1: Infrastructure Setup ✅ *Complete*
**Status**: Complete
- [x] Analysis of existing codebase and dataset structure
- [x] Review of current model coordination architecture  
- [x] Create weight optimization framework following Clean Architecture
- [x] Implement evolutionary algorithm for joint weight/mode optimization
- [x] Create comprehensive testing infrastructure  
- [x] Create test data loader for 345 classified phrases
- [x] Create main execution runner script
- [ ] Establish baseline performance metrics (ready to execute)

### Phase 2: Optimization Execution 
**Status**: Not Started
- [ ] Run baseline performance assessment on current weights (40/30/30)
- [ ] Execute evolutionary algorithm optimization (50 generations, 20 population)
- [ ] Perform cross-validation on optimal configurations
- [ ] Validate performance requirements (≤200ms)
- [ ] Document optimization results and recommendations

### Phase 3: Deployment and Validation
**Status**: Not Started  
- [ ] Deploy optimal weights to production environment
- [ ] Conduct post-deployment performance validation
- [ ] Monitor system performance and accuracy metrics
- [ ] Document lessons learned and optimization insights

---

## Implementation Details

### Optimization Algorithm: Evolutionary Algorithm
**Rationale**: 
- Naturally handles constraint (weights sum to 1.0)
- Can jointly optimize ensemble mode AND weights
- More thorough exploration than grid search
- Interpretable results

**Parameters**:
- Population Size: 20 individuals
- Generations: 50 iterations  
- Mutation Rate: 0.1 (10%)
- Selection: Tournament selection
- Fitness Function: F1-score with recall bias for crisis detection

### Search Space Definition
- **Ensemble Modes**: ['consensus', 'majority', 'weighted']
- **Weight Ranges**: Each weight ∈ [0.1, 0.8], sum = 1.0
- **Weight Precision**: 0.05 increments for interpretability
- **Total Search Space**: ~3,000 unique combinations

### Validation Strategy  
- **K-Fold Cross-Validation**: 5-fold validation for robust evaluation
- **Stratified Sampling**: Maintain category distribution across folds
- **Performance Testing**: Continuous monitoring of analysis time
- **Holdout Validation**: Final validation on 20% holdout set

---

## Current Architecture Integration

### Key Components
- **ModelCoordinationManager**: Handles ensemble voting and model weights
- **UnifiedConfigManager**: Manages configuration with environment variable overrides
- **Performance Optimizations**: Maintains 200ms target through caching and sync operations

### Environment Variable Updates
Current variables to be optimized:
```bash
NLP_MODEL_DEPRESSION_WEIGHT=0.4
NLP_MODEL_SENTIMENT_WEIGHT=0.3  
NLP_MODEL_DISTRESS_WEIGHT=0.3
NLP_ENSEMBLE_MODE=majority
```

### Clean Architecture Compliance
- Factory function patterns maintained
- Dependency injection preserved
- Configuration externalization continued
- Error handling with graceful fallbacks
- Comprehensive logging throughout optimization

---

## Risk Mitigation

### Performance Risks
- **Risk**: Optimization process exceeds 200ms target
- **Mitigation**: Continuous performance monitoring during optimization
- **Fallback**: Immediate rollback to current 40/30/30 weights

### Accuracy Risks  
- **Risk**: Optimization reduces accuracy instead of improving it
- **Mitigation**: Multiple validation rounds and statistical significance testing
- **Fallback**: Comprehensive baseline comparison before deployment

### System Stability Risks
- **Risk**: New weights cause system instability
- **Mitigation**: Thorough integration testing and gradual deployment
- **Fallback**: Quick revert capability via environment variable changes

---

## Success Metrics

### Primary Metrics
- **F1-Score Improvement**: Target >5% improvement over current performance
- **Precision**: Maintain or improve false positive rate
- **Recall**: Maintain or improve false negative rate (critical for crisis detection)
- **Performance**: Maintain ≤200ms average analysis time

### Secondary Metrics  
- **Category-Specific Accuracy**: Per-category performance analysis
- **Model Agreement**: Consistency between ensemble models
- **Stability**: Performance consistency across different message types
- **Resource Usage**: Memory and CPU utilization during analysis

---

## Next Steps

1. **Complete Phase 1**: Finish infrastructure setup and baseline assessment
2. **Execute Optimization**: Run evolutionary algorithm with comprehensive validation
3. **Validate Results**: Ensure >5% improvement and performance requirements
4. **Deploy Optimal Configuration**: Update .env with optimal weights/mode
5. **Monitor Production Performance**: Track real-world performance post-deployment

---

## Files to be Created/Modified

### New Files
- `optimization/weight_optimizer.py` - Main optimization framework (includes embedded EA)
- `optimization/test_data_loader.py` - Test data parsing and validation
- `optimization/run_weight_optimization.py` - Main execution runner script

### Modified Files  
- `.env` - Updated with optimal weights and ensemble mode
- `config/model_coordination.json` - Default values updated post-optimization
- `docs/optimization_results.md` - Documentation of optimization results

---

*This document will be updated throughout the optimization process to track progress and capture insights.*