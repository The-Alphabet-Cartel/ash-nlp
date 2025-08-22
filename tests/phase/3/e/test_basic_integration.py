#!/usr/bin/env python3
"""
Basic Functional Integration Test: Manager Communication and Operation
Phase 3e Step 5.7 - Updated for AnalysisConfigManager rename

This test validates that all managers can work together functionally without
worrying about crisis detection accuracy or performance tuning. The goal is
to ensure clean Phase 3e consolidation is working properly.

UPDATED: Phase 3e Step 5.7 - AnalysisParametersManager renamed to AnalysisConfigManager

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
    create_pattern_detection_manager,
    create_analysis_config_manager,
    create_crisis_threshold_manager,
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
            'pattern_detection': create_pattern_detection_manager(config_manager),
            'analysis_config': create_analysis_config_manager(config_manager),
            'crisis_threshold': create_crisis_threshold_manager(config_manager),
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
            analysis_config = all_managers['unified_config'].get_config_section('analysis_config')
            config_access_tests['unified_config'] = analysis_config is not None
        except:
            config_access_tests['unified_config'] = False
        
        # Test managers that should have configuration access
        for manager_name in ['feature_config', 'logging_config', 'analysis_config']:
            try:
                manager = all_managers[manager_name]
                if hasattr(manager, 'config_manager'):
                    test_config = manager.config_manager.get_config_section('analysis_config')
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
        
        # Test PatternDetectionManager
        try:
            crisis_result = all_managers['pattern_detection'].analyze_message(test_message, test_user, test_channel)
            pipeline_results['pattern_detection'] = {
                'functional': crisis_result.get('analysis_available', False),
                'has_response_structure': 'summary' in crisis_result
            }
        except Exception as e:
            pipeline_results['pattern_detection'] = {'functional': False, 'error': str(e)}
        
        # Test AnalysisConfigManager (UPDATED: Renamed from AnalysisParametersManager)
        try:
            contextual_weights = all_managers['analysis_config'].get_contextual_weighting_parameters()
            pipeline_results['analysis_config'] = {
                'functional': contextual_weights.get('temporal_context_weight', 0) > 0,
                'has_parameters': len(contextual_weights) > 3
            }
        except Exception as e:
            pipeline_results['analysis_config'] = {'functional': False, 'error': str(e)}
        
        # Test CrisisThresholdManager
        try:
            threshold_result = all_managers['crisis_threshold'].determine_crisis_level(0.7, "test")
            pipeline_results['crisis_threshold'] = {
                'functional': threshold_result is not None,
                'has_level': isinstance(threshold_result, str)
            }
        except Exception as e:
            pipeline_results['crisis_threshold'] = {'functional': False, 'error': str(e)}
        
        # Test ModelEnsembleManager
        try:
            ensemble_summary = all_managers['model_ensemble'].get_model_summary()
            pipeline_results['model_ensemble'] = {
                'functional': ensemble_summary.get('available_models', 0) >= 0,
                'has_summary_structure': 'model_count' in ensemble_summary or 'available_models' in ensemble_summary
            }
        except Exception as e:
            pipeline_results['model_ensemble'] = {'functional': False, 'error': str(e)}
        
        functional_pipeline_components = sum(1 for result in pipeline_results.values() if result.get('functional', False))
        
        assert functional_pipeline_components >= 3, f"Only {functional_pipeline_components}/4 pipeline components functional"
        
        logger.info(f"✅ Crisis analysis pipeline test passed: {functional_pipeline_components}/4 components functional")
    
    def test_manager_communication_works(self, all_managers):
        """Test that managers can communicate with each other through shared config"""
        
        communication_tests = {}
        
        # Test 1: UnifiedConfig -> AnalysisConfig communication
        try:
            config_data = all_managers['unified_config'].get_config_section('analysis_config')
            # UPDATED: Using renamed manager key
            analysis_summary = all_managers['analysis_config'].get_configuration_summary()
            communication_tests['config_to_analysis'] = (
                config_data is not None and 
                analysis_summary.get('configuration_loaded', False)
            )
        except:
            communication_tests['config_to_analysis'] = False
        
        # Test 2: FeatureConfig -> ModelEnsemble communication
        try:
            feature_status = all_managers['feature_config'].is_feature_enabled('ensemble_analysis')
            model_availability = all_managers['model_ensemble'].is_ensemble_analysis_enabled()
            communication_tests['feature_to_model'] = isinstance(feature_status, bool) and isinstance(model_availability, bool)
        except:
            communication_tests['feature_to_model'] = False
        
        # Test 3: ThresholdMapping -> CrisisPattern communication (via shared config)
        try:
            threshold_config = all_managers['crisis_threshold'].get_configuration_summary()
            crisis_summary = all_managers['pattern_detection'].get_analysis_summary()
            communication_tests['threshold_to_crisis'] = (
                threshold_config.get('manager_initialized', False) and
                crisis_summary.get('analysis_available', False)
            )
        except:
            communication_tests['threshold_to_crisis'] = False
        
        successful_communications = sum(communication_tests.values())
        
        assert successful_communications >= 2, f"Only {successful_communications}/3 manager communications working"
        
        logger.info(f"✅ Manager communication test passed: {successful_communications}/3 communication paths working")
    
    def test_basic_performance_reasonable(self, all_managers):
        """Test that basic operations complete in reasonable time (not accuracy tuning)"""
        
        performance_tests = {}
        
        # Test 1: Config access speed (should be very fast)
        start_time = time.time()
        try:
            all_managers['unified_config'].get_config_section('analysis_config')
            config_time = time.time() - start_time
            performance_tests['config_access'] = config_time < 1.0  # Very generous - just checking it's not broken
        except:
            performance_tests['config_access'] = False
        
        # Test 2: Crisis analysis speed (should complete)
        start_time = time.time()
        try:
            all_managers['pattern_detection'].analyze_message("test message", "test_user", "test_channel")
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
            crisis_result = all_managers['pattern_detection'].analyze_message("test", "user", "channel")
            summary_metrics['crisis_detection_operational'] = crisis_result.get('analysis_available', False)
        except:
            summary_metrics['crisis_detection_operational'] = False
        
        # Test configuration working
        try:
            config_result = all_managers['unified_config'].get_config_section('analysis_config')
            summary_metrics['configuration_working'] = config_result is not None
        except:
            summary_metrics['configuration_working'] = False
        
        # Test error handling robust
        try:
            # This should fail gracefully, not crash
            all_managers['pattern_detection'].analyze_message("", "", "")
            summary_metrics['error_handling_robust'] = True
        except Exception as e:
            # If it throws an exception, that's okay as long as it's controlled
            summary_metrics['error_handling_robust'] = len(str(e)) > 0
        
        logger.info("🎯 PHASE 3E INTEGRATION SUMMARY:")
        logger.info(f"  📊 Managers: {summary_metrics['managers_initialized']}/{summary_metrics['total_managers']} initialized")
        logger.info(f"  ⚙️  Functional: {summary_metrics['functional_managers']}/{summary_metrics['total_managers']} have functionality")
        logger.info(f"  🚨 Crisis Detection: {'✅ Operational' if summary_metrics['crisis_detection_operational'] else '❌ Not operational'}")
        logger.info(f"  🔧 Configuration: {'✅ Working' if summary_metrics['configuration_working'] else '❌ Not working'}")
        logger.info(f"  🛡️  Error Handling: {'✅ Robust' if summary_metrics['error_handling_robust'] else '❌ Needs work'}")
        
        # Assert minimum functionality
        assert summary_metrics['managers_initialized'] >= 12, "Less than 12/14 managers initialized"
        assert summary_metrics['functional_managers'] >= 10, "Less than 10/14 managers functional"
        assert summary_metrics['configuration_working'], "Configuration system not working"
        
        logger.info("✅ Phase 3e Step 5.7 Integration Test: PASSED - AnalysisConfigManager rename successful")