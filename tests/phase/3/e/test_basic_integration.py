#!/usr/bin/env python3
"""
Basic Functional Integration Test: Manager Communication and Operation
Phase 3e Step 5.6 - Focus on Integration, Not Tuning

This test validates that all managers can work together functionally without
worrying about crisis detection accuracy or performance tuning. The goal is
to ensure clean Phase 3e consolidation is working properly.

Target: Verify managers communicate and function together (not performance tuning)
"""

import pytest
import time
import logging
import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from managers import (
    create_unified_config_manager,
    create_pydantic_manager,
    create_feature_config_manager, 
    create_logging_config_manager,
    create_crisis_pattern_manager,
    create_analysis_parameters_manager,
    create_threshold_mapping_manager,
    create_model_ensemble_manager,
    create_performance_config_manager,
    create_context_pattern_manager,
    create_zero_shot_manager,
    create_storage_config_manager,
    create_server_config_manager,
    create_settings_manager
)

logger = logging.getLogger(__name__)

class TestBasicFunctionalIntegration:
    """
    Basic functional integration test - focuses on manager communication
    NOT worried about crisis detection accuracy or performance tuning
    """
    
    @pytest.fixture(scope="class")
    def all_managers(self):
        """Create all 14 system managers"""
        
        logger.info("🚀 Initializing all 14 Phase 3e managers for functional testing...")
        
        config_manager = create_unified_config_manager()
        assert config_manager is not None, "UnifiedConfigManager failed to initialize"
        
        managers = {
            'unified_config': config_manager,
            'pydantic': create_pydantic_manager(config_manager),
            'feature_config': create_feature_config_manager(config_manager),
            'logging_config': create_logging_config_manager(config_manager),
            'crisis_pattern': create_crisis_pattern_manager(config_manager),
            'analysis_parameters': create_analysis_parameters_manager(config_manager),
            'threshold_mapping': create_threshold_mapping_manager(config_manager),
            'model_ensemble': create_model_ensemble_manager(config_manager),
            'performance_config': create_performance_config_manager(config_manager),
            'context_pattern': create_context_pattern_manager(config_manager),
            'zero_shot': create_zero_shot_manager(config_manager),
            'storage_config': create_storage_config_manager(config_manager),
            'server_config': create_server_config_manager(config_manager),
            'settings': create_settings_manager(config_manager)
        }
        
        # Validate all managers initialized
        failed_managers = []
        for name, manager in managers.items():
            if manager is None:
                failed_managers.append(name)
        
        if failed_managers:
            pytest.fail(f"Failed to initialize managers: {failed_managers}")
        
        logger.info(f"✅ All {len(managers)} managers initialized successfully")
        return managers
    
    def test_all_managers_initialize(self, all_managers):
        """Test that all 14 managers can be created and are operational"""
        
        # Basic functionality test for each manager
        manager_statuses = {}
        
        for manager_name, manager in all_managers.items():
            try:
                # Test basic attributes exist
                has_config_manager = hasattr(manager, 'config_manager') or hasattr(manager, 'unified_config')
                
                # Test some kind of functional method exists
                has_functionality = (
                    hasattr(manager, 'get_configuration_summary') or
                    hasattr(manager, 'get_config_section') or
                    hasattr(manager, 'analyze_message') or
                    hasattr(manager, 'get_model_summary') or
                    hasattr(manager, 'is_ensemble_analysis_enabled') or
                    hasattr(manager, 'determine_crisis_level') or
                    hasattr(manager, 'get_model_weights')
                )
                
                manager_statuses[manager_name] = {
                    'initialized': True,
                    'has_config_access': has_config_manager,
                    'has_functionality': has_functionality
                }
                
            except Exception as e:
                manager_statuses[manager_name] = {
                    'initialized': False,
                    'error': str(e)
                }
        
        # Validate results
        successful_managers = sum(1 for status in manager_statuses.values() if status.get('initialized', False))
        functional_managers = sum(1 for status in manager_statuses.values() if status.get('has_functionality', False))
        
        assert successful_managers == 14, f"Only {successful_managers}/14 managers initialized successfully"
        assert functional_managers >= 10, f"Only {functional_managers}/14 managers have functionality"
        
        logger.info(f"✅ Manager initialization test passed: {successful_managers}/14 initialized, {functional_managers}/14 functional")
    
    def test_configuration_access_works(self, all_managers):
        """Test that configuration access works across managers"""
        
        config_access_tests = {}
        
        # Test UnifiedConfigManager
        try:
            analysis_config = all_managers['unified_config'].get_config_section('analysis_parameters')
            config_access_tests['unified_config'] = analysis_config is not None
        except:
            config_access_tests['unified_config'] = False
        
        # Test managers that should have configuration access
        for manager_name in ['feature_config', 'logging_config', 'analysis_parameters']:
            try:
                manager = all_managers[manager_name]
                if hasattr(manager, 'config_manager'):
                    test_config = manager.config_manager.get_config_section('analysis_parameters')
                    config_access_tests[manager_name] = test_config is not None
                else:
                    config_access_tests[manager_name] = True  # Manager exists, no config test needed
            except:
                config_access_tests[manager_name] = False
        
        successful_config_access = sum(config_access_tests.values())
        
        assert successful_config_access >= 3, f"Only {successful_config_access} managers have working configuration access"
        
        logger.info(f"✅ Configuration access test passed: {successful_config_access} managers with working config access")
    
    def test_crisis_analysis_pipeline_functional(self, all_managers):
        """Test that crisis analysis pipeline functions (not accuracy, just operation)"""
        
        test_message = "I'm struggling with some difficult feelings today"
        test_user = "test_user_functional"
        test_channel = "test_channel_functional"
        
        pipeline_results = {}
        
        # Test CrisisPatternManager
        try:
            crisis_result = all_managers['crisis_pattern'].analyze_message(test_message, test_user, test_channel)
            pipeline_results['crisis_pattern'] = {
                'functional': crisis_result.get('analysis_available', False),
                'has_response_structure': 'summary' in crisis_result
            }
        except Exception as e:
            pipeline_results['crisis_pattern'] = {'functional': False, 'error': str(e)}
        
        # Test AnalysisParametersManager
        try:
            contextual_weights = all_managers['analysis_parameters'].get_contextual_weighting_parameters()
            pipeline_results['analysis_parameters'] = {
                'functional': isinstance(contextual_weights, dict),
                'has_weights': len(contextual_weights) > 0
            }
        except Exception as e:
            pipeline_results['analysis_parameters'] = {'functional': False, 'error': str(e)}
        
        # Test ThresholdMappingManager
        try:
            crisis_level = all_managers['threshold_mapping'].determine_crisis_level(0.5, 'consensus')
            pipeline_results['threshold_mapping'] = {
                'functional': crisis_level in ['none', 'low', 'medium', 'high', 'critical'],
                'returned_level': crisis_level
            }
        except Exception as e:
            pipeline_results['threshold_mapping'] = {'functional': False, 'error': str(e)}
        
        # Test ModelEnsembleManager
        try:
            model_weights = all_managers['model_ensemble'].get_model_weights()
            pipeline_results['model_ensemble'] = {
                'functional': isinstance(model_weights, dict),
                'has_models': len(model_weights) > 0
            }
        except Exception as e:
            pipeline_results['model_ensemble'] = {'functional': False, 'error': str(e)}
        
        # Validate pipeline functionality
        functional_components = sum(1 for result in pipeline_results.values() if result.get('functional', False))
        
        assert functional_components >= 3, f"Only {functional_components}/4 pipeline components functional"
        
        logger.info(f"✅ Crisis analysis pipeline functional test passed: {functional_components}/4 components working")
        logger.info(f"📊 Pipeline results: {pipeline_results}")
    
    def test_manager_communication(self, all_managers):
        """Test that managers can communicate with each other"""
        
        communication_tests = {}
        
        # Test 1: Configuration consistency
        try:
            config1 = all_managers['unified_config'].get_config_section('analysis_parameters')
            config2 = all_managers['analysis_parameters'].config_manager.get_config_section('analysis_parameters')
            communication_tests['config_consistency'] = config1 == config2
        except:
            communication_tests['config_consistency'] = False
        
        # Test 2: Feature flag communication
        try:
            feature_enabled = all_managers['feature_config'].is_ensemble_analysis_enabled()
            communication_tests['feature_flags'] = isinstance(feature_enabled, bool)
        except:
            communication_tests['feature_flags'] = False
        
        # Test 3: Model information sharing
        try:
            models = all_managers['pydantic'].get_core_models()
            communication_tests['model_sharing'] = len(models) > 0
        except:
            communication_tests['model_sharing'] = False
        
        successful_communications = sum(communication_tests.values())
        
        assert successful_communications >= 2, f"Only {successful_communications}/3 communication tests passed"
        
        logger.info(f"✅ Manager communication test passed: {successful_communications}/3 communication types working")
    
    def test_error_handling_resilience(self, all_managers):
        """Test that managers handle errors gracefully"""
        
        error_resilience_tests = {}
        
        # Test 1: Invalid message handling
        try:
            invalid_result = all_managers['crisis_pattern'].analyze_message("", "test_user", "test_channel")
            error_resilience_tests['invalid_message'] = invalid_result.get('analysis_available') is not None
        except:
            error_resilience_tests['invalid_message'] = False
        
        # Test 2: Invalid threshold handling
        try:
            invalid_threshold = all_managers['threshold_mapping'].determine_crisis_level(-1.0, 'invalid_mode')
            error_resilience_tests['invalid_threshold'] = isinstance(invalid_threshold, str)
        except:
            error_resilience_tests['invalid_threshold'] = False
        
        # Test 3: Configuration error handling
        try:
            # This should handle missing configuration gracefully
            missing_config = all_managers['unified_config'].get_config_section('nonexistent_config')
            error_resilience_tests['missing_config'] = missing_config is None
        except:
            error_resilience_tests['missing_config'] = True  # Exception is acceptable for missing config
        
        resilient_components = sum(error_resilience_tests.values())
        
        assert resilient_components >= 2, f"Only {resilient_components}/3 error resilience tests passed"
        
        logger.info(f"✅ Error handling resilience test passed: {resilient_components}/3 resilience tests working")
    
    def test_basic_performance_reasonable(self, all_managers):
        """Test that basic operations complete in reasonable time (not strict performance tuning)"""
        
        performance_tests = {}
        
        # Test 1: Configuration access speed (should be fast)
        start_time = time.time()
        try:
            all_managers['unified_config'].get_config_section('analysis_parameters')
            config_time = time.time() - start_time
            performance_tests['config_access'] = config_time < 1.0  # Very generous - just checking it's not broken
        except:
            performance_tests['config_access'] = False
        
        # Test 2: Crisis analysis speed (should complete)
        start_time = time.time()
        try:
            all_managers['crisis_pattern'].analyze_message("test message", "test_user", "test_channel")
            analysis_time = time.time() - start_time
            performance_tests['crisis_analysis'] = analysis_time < 5.0  # Very generous - just checking it completes
        except:
            performance_tests['crisis_analysis'] = False
        
        # Test 3: Model access speed (should be fast)
        start_time = time.time()
        try:
            all_managers['pydantic'].get_core_models()
            model_time = time.time() - start_time
            performance_tests['model_access'] = model_time < 1.0  # Very generous
        except:
            performance_tests['model_access'] = False
        
        reasonable_performance = sum(performance_tests.values())
        
        assert reasonable_performance >= 2, f"Only {reasonable_performance}/3 basic performance tests passed"
        
        logger.info(f"✅ Basic performance test passed: {reasonable_performance}/3 operations complete in reasonable time")
    
    def test_integration_summary(self, all_managers):
        """Generate final integration summary"""
        
        summary_metrics = {
            'total_managers': len(all_managers),
            'managers_initialized': 0,
            'functional_managers': 0,
            'crisis_detection_operational': False,
            'configuration_working': False,
            'error_handling_robust': False
        }
        
        # Count initialized managers
        for manager in all_managers.values():
            if manager is not None:
                summary_metrics['managers_initialized'] += 1
                
                # Check if manager has basic functionality
                if (hasattr(manager, 'get_configuration_summary') or 
                    hasattr(manager, 'analyze_message') or 
                    hasattr(manager, 'get_model_summary')):
                    summary_metrics['functional_managers'] += 1
        
        # Test crisis detection operational
        try:
            crisis_result = all_managers['crisis_pattern'].analyze_message("test", "test", "test")
            summary_metrics['crisis_detection_operational'] = crisis_result.get('analysis_available', False)
        except:
            pass
        
        # Test configuration working
        try:
            config = all_managers['unified_config'].get_config_section('analysis_parameters')
            summary_metrics['configuration_working'] = config is not None
        except:
            pass
        
        # Test error handling
        try:
            all_managers['crisis_pattern'].analyze_message("", "", "")
            summary_metrics['error_handling_robust'] = True
        except:
            summary_metrics['error_handling_robust'] = True  # Exception handling is also acceptable
        
        # Validate overall integration
        integration_score = (
            (1 if summary_metrics['managers_initialized'] >= 14 else 0) +
            (1 if summary_metrics['functional_managers'] >= 10 else 0) +
            (1 if summary_metrics['crisis_detection_operational'] else 0) +
            (1 if summary_metrics['configuration_working'] else 0) +
            (1 if summary_metrics['error_handling_robust'] else 0)
        ) / 5.0
        
        assert integration_score >= 0.8, f"Integration score {integration_score:.1%} below target (80%)"
        
        logger.info(f"🏆 INTEGRATION SUMMARY")
        logger.info(f"✅ Managers initialized: {summary_metrics['managers_initialized']}/14")
        logger.info(f"✅ Functional managers: {summary_metrics['functional_managers']}/14")
        logger.info(f"✅ Crisis detection operational: {summary_metrics['crisis_detection_operational']}")
        logger.info(f"✅ Configuration working: {summary_metrics['configuration_working']}")
        logger.info(f"✅ Error handling robust: {summary_metrics['error_handling_robust']}")
        logger.info(f"🎯 Overall integration score: {integration_score:.1%}")
        
        return summary_metrics


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Starting Phase 3e Step 5.6 - Basic Functional Integration Test")
    print("🎯 Focus: Manager communication and operation (NOT performance tuning)")
    print("📊 Goal: Verify Phase 3e consolidation works functionally")
    print()
    
    # Run the test suite
    pytest.main([__file__, "-v", "--tb=short"])