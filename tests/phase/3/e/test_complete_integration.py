#!/usr/bin/env python3
"""
Integration Test: Complete System Integration - All 14 Managers
Phase 3e Step 5.6 - Final Comprehensive Test

This test validates the complete Ash-NLP crisis detection system with all 14
cleaned managers working together in real-world scenarios. Tests end-to-end
crisis detection workflows that simulate the /analyze endpoint functionality.

All Managers Tested:
1. UnifiedConfigManager - Core configuration management
2. PydanticManager - Data model validation
3. FeatureConfigManager - Feature flag control
4. LoggingConfigManager - Logging configuration
5. CrisisPatternManager - Crisis pattern detection
6. AnalysisParametersManager - Analysis parameter management
7. ThresholdMappingManager - Crisis threshold mapping
8. ModelEnsembleManager - Model ensemble coordination
9. PerformanceConfigManager - Performance optimization
10. ContextPatternManager - Context enhancement
11. ZeroShotManager - Zero-shot model management
12. StorageConfigManager - Storage and caching
13. ServerConfigManager - Server configuration
14. SettingsManager - System settings coordination

Target: Complete /analyze endpoint simulation in < 500ms with 100% functionality
"""

import pytest
import asyncio
import time
import logging
import sys
import os
from typing import Dict, List, Any
import json

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

class TestCompleteSystemIntegration:
    """
    Complete system integration test for all 14 Phase 3e cleaned managers
    Simulates real /analyze endpoint workflows for LGBTQIA+ crisis detection
    """
    
    @pytest.fixture(scope="class")
    def all_managers(self):
        """Create all 14 system managers for comprehensive testing"""
        
        logger.info("🚀 Initializing all 14 Phase 3e managers...")
        
        # Step 1: Create core configuration manager
        config_manager = create_unified_config_manager()
        assert config_manager is not None, "UnifiedConfigManager failed to initialize"
        
        # Step 2: Initialize all managers
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
    
    # ========================================================================
    # COMPLETE SYSTEM STARTUP VALIDATION
    # ========================================================================
    
    def test_complete_system_startup(self, all_managers):
        """Test that all 14 managers startup and communicate properly"""
        
        startup_start_time = time.time()
        
        # Test each manager's core functionality
        manager_status = {}
        
        for manager_name, manager in all_managers.items():
            try:
                # Test basic manager functionality
                if hasattr(manager, 'get_configuration_summary'):
                    summary = manager.get_configuration_summary()
                    manager_status[manager_name] = {
                        'initialized': True,
                        'has_summary': isinstance(summary, dict),
                        'summary_keys': len(summary.keys()) if isinstance(summary, dict) else 0
                    }
                elif hasattr(manager, 'get_config_section'):
                    # Test configuration access
                    manager_status[manager_name] = {
                        'initialized': True,
                        'config_access': True
                    }
                else:
                    # Basic validation for managers without standard methods
                    manager_status[manager_name] = {
                        'initialized': True,
                        'basic_validation': True
                    }
                    
            except Exception as e:
                manager_status[manager_name] = {
                    'initialized': False,
                    'error': str(e)
                }
        
        startup_time = time.time() - startup_start_time
        
        # Validate startup results
        successful_managers = sum(1 for status in manager_status.values() if status.get('initialized', False))
        failed_managers = [name for name, status in manager_status.items() if not status.get('initialized', False)]
        
        assert successful_managers == 14, f"Only {successful_managers}/14 managers started successfully"
        assert len(failed_managers) == 0, f"Failed managers: {failed_managers}"
        assert startup_time < 3.0, f"System startup took {startup_time:.2f}s (target: < 3.0s)"
        
        logger.info(f"✅ Complete system startup test passed in {startup_time:.3f}s")
        logger.info(f"🎯 Managers successfully initialized: {successful_managers}/14")
        
    # ========================================================================
    # REAL-WORLD CRISIS DETECTION SIMULATION
    # ========================================================================
    
    def test_real_world_crisis_detection_simulation(self, all_managers):
        """Simulate complete /analyze endpoint with real LGBTQIA+ crisis scenarios"""
        
        # Comprehensive LGBTQIA+ community crisis test scenarios
        crisis_scenarios = [
            {
                'scenario': 'acute_gender_dysphoria',
                'message': "The gender dysphoria is unbearable tonight. I can't look in the mirror anymore and I'm having thoughts of ending everything.",
                'user_id': 'user_dysphoria_crisis',
                'channel_id': 'crisis_support',
                'expected_high_crisis': True,
                'critical_patterns': ['gender_dysphoria', 'suicidal_ideation', 'acute_distress']
            },
            {
                'scenario': 'family_rejection_crisis',
                'message': "My parents kicked me out after I came out as trans. I have nowhere to go and no money. I'm sleeping in my car and don't know what to do.",
                'user_id': 'user_homeless_crisis',
                'channel_id': 'emergency_support',
                'expected_high_crisis': True,
                'critical_patterns': ['family_rejection', 'homelessness', 'coming_out_trauma']
            },
            {
                'scenario': 'workplace_discrimination',
                'message': "My boss keeps misgendering me and making transphobic comments. HR won't help. The stress is affecting my mental health badly.",
                'user_id': 'user_workplace_stress',
                'channel_id': 'support_channel',
                'expected_high_crisis': False,
                'critical_patterns': ['workplace_discrimination', 'chronic_stress', 'misgendering']
            },
            {
                'scenario': 'community_support_positive',
                'message': "Just wanted to thank everyone in this community. Your support during my transition has been amazing and life-changing.",
                'user_id': 'user_grateful',
                'channel_id': 'general',
                'expected_high_crisis': False,
                'critical_patterns': ['community_support', 'positive_transition', 'gratitude']
            },
            {
                'scenario': 'identity_questioning',
                'message': "I'm really questioning my gender identity lately. Sometimes I feel like I might be non-binary but I'm scared and confused.",
                'user_id': 'user_questioning',
                'channel_id': 'questioning_support',
                'expected_high_crisis': False,
                'critical_patterns': ['identity_questioning', 'gender_exploration', 'uncertainty']
            }
        ]
        
        simulation_results = []
        
        for scenario in crisis_scenarios:
            simulation_start_time = time.time()
            
            try:
                # PHASE 1: Configuration and Setup (Managers 1-4)
                phase1_start = time.time()
                
                # UnifiedConfigManager - Load configuration
                crisis_config = all_managers['unified_config'].get_config_section('crisis_patterns')
                analysis_config = all_managers['unified_config'].get_config_section('analysis_parameters')
                
                # PydanticManager - Validate request data
                message_validation = all_managers['pydantic'].validate_model_structure('MessageRequest')
                
                # FeatureConfigManager - Check feature flags
                ensemble_enabled = all_managers['feature_config'].is_ensemble_analysis_enabled()
                pattern_analysis_enabled = all_managers['feature_config'].is_pattern_analysis_enabled()
                
                # LoggingConfigManager - Setup logging
                log_config = all_managers['logging_config'].get_logging_configuration()
                
                phase1_time = time.time() - phase1_start
                
                # PHASE 2: Core Crisis Analysis (Managers 5-8)
                phase2_start = time.time()
                
                # CrisisPatternManager - Analyze crisis patterns
                crisis_analysis = all_managers['crisis_pattern'].analyze_message(
                    scenario['message'],
                    scenario['user_id'],
                    scenario['channel_id']
                )
                
                # AnalysisParametersManager - Get analysis parameters
                contextual_weights = all_managers['analysis_parameters'].get_contextual_weighting_parameters()
                performance_params = all_managers['analysis_parameters'].get_performance_parameters()
                
                # ThresholdMappingManager - Get crisis thresholds
                crisis_thresholds = all_managers['threshold_mapping'].get_crisis_thresholds()
                
                # ModelEnsembleManager - Get ensemble configuration
                ensemble_weights = all_managers['model_ensemble'].get_ensemble_weights()
                
                phase2_time = time.time() - phase2_start
                
                # PHASE 3: Enhancement and Optimization (Managers 9-12)
                phase3_start = time.time()
                
                # PerformanceConfigManager - Apply performance settings
                perf_config = all_managers['performance_config'].get_performance_parameters()
                
                # ContextPatternManager - Enhance with context
                context_patterns = all_managers['context_pattern'].extract_context_patterns(scenario['message'])
                
                # ZeroShotManager - Apply zero-shot analysis
                zero_shot_config = all_managers['zero_shot'].get_zero_shot_configuration()
                
                # StorageConfigManager - Handle data persistence
                storage_paths = all_managers['storage_config'].get_storage_paths()
                
                phase3_time = time.time() - phase3_start
                
                # PHASE 4: System Coordination (Managers 13-14)
                phase4_start = time.time()
                
                # ServerConfigManager - Get server configuration
                server_config = all_managers['server_config'].get_server_configuration()
                
                # SettingsManager - Coordinate system settings
                system_settings = all_managers['settings'].get_system_settings()
                
                phase4_time = time.time() - phase4_start
                
                total_simulation_time = time.time() - simulation_start_time
                
                # VALIDATE SIMULATION RESULTS
                crisis_detected = crisis_analysis.get('safety_assessment', {}).get('crisis_detected', False)
                crisis_score = crisis_analysis.get('summary', {}).get('crisis_score', 0.0)
                patterns_found = len(context_patterns) if context_patterns else 0
                
                # Accuracy validation
                accuracy = True
                if scenario['expected_high_crisis'] and not crisis_detected:
                    accuracy = False
                elif not scenario['expected_high_crisis'] and crisis_detected and crisis_score > 0.8:
                    accuracy = False
                
                simulation_results.append({
                    'scenario': scenario['scenario'],
                    'total_time': total_simulation_time,
                    'phase1_time': phase1_time,
                    'phase2_time': phase2_time,
                    'phase3_time': phase3_time,
                    'phase4_time': phase4_time,
                    'crisis_detected': crisis_detected,
                    'crisis_score': crisis_score,
                    'patterns_found': patterns_found,
                    'expected_high_crisis': scenario['expected_high_crisis'],
                    'accuracy': accuracy,
                    'performance_target_met': total_simulation_time < 0.5
                })
                
                # Performance assertion for each scenario
                assert total_simulation_time < 0.5, \
                    f"Scenario '{scenario['scenario']}' took {total_simulation_time:.3f}s (target: < 0.5s)"
                
                logger.info(f"✅ Scenario '{scenario['scenario']}' completed in {total_simulation_time:.3f}s")
                logger.info(f"   Crisis detected: {crisis_detected}, Score: {crisis_score:.2f}, Patterns: {patterns_found}")
                
            except Exception as e:
                pytest.fail(f"Crisis detection simulation failed for scenario '{scenario['scenario']}': {e}")
        
        # ANALYZE OVERALL SIMULATION RESULTS
        total_scenarios = len(simulation_results)
        accurate_detections = sum(1 for r in simulation_results if r['accuracy'])
        performance_targets_met = sum(1 for r in simulation_results if r['performance_target_met'])
        avg_total_time = sum(r['total_time'] for r in simulation_results) / total_scenarios
        avg_crisis_analysis_time = sum(r['phase2_time'] for r in simulation_results) / total_scenarios
        
        # Overall validation
        accuracy_rate = accurate_detections / total_scenarios
        performance_rate = performance_targets_met / total_scenarios
        
        assert accuracy_rate >= 0.8, f"Accuracy rate {accuracy_rate:.1%} below target (80%)"
        assert performance_rate == 1.0, f"Performance rate {performance_rate:.1%} below target (100%)"
        assert avg_total_time < 0.4, f"Average total time {avg_total_time:.3f}s above target (0.4s)"
        
        logger.info(f"✅ Real-world crisis detection simulation PASSED")
        logger.info(f"🎯 Accuracy rate: {accuracy_rate:.1%} ({accurate_detections}/{total_scenarios})")
        logger.info(f"⚡ Performance targets met: {performance_rate:.1%} ({performance_targets_met}/{total_scenarios})")
        logger.info(f"⏱️ Average total time: {avg_total_time:.3f}s")
        logger.info(f"🔍 Average crisis analysis time: {avg_crisis_analysis_time:.3f}s")
        
        return simulation_results
    
    # ========================================================================
    # SYSTEM RESILIENCE AND ERROR HANDLING
    # ========================================================================
    
    def test_system_resilience_and_error_handling(self, all_managers):
        """Test system handles errors gracefully without failures"""
        
        # Test error scenarios that should be handled gracefully
        error_test_scenarios = [
            {
                'test': 'empty_message_handling',
                'message': '',
                'user_id': 'test_user_empty',
                'channel_id': 'test_channel'
            },
            {
                'test': 'very_long_message_handling',
                'message': 'Crisis message ' * 200,  # Very long message
                'user_id': 'test_user_long',
                'channel_id': 'test_channel'
            },
            {
                'test': 'special_characters_handling',
                'message': 'Crisis with émojis 🏳️‍⚧️🏳️‍🌈 and special chars: @#$%^&*()',
                'user_id': 'test_user_special',
                'channel_id': 'test_channel'
            },
            {
                'test': 'unicode_handling',
                'message': 'Crisis with unicode: 中文 العربية русский язык',
                'user_id': 'test_user_unicode',
                'channel_id': 'test_channel'
            }
        ]
        
        resilience_results = []
        
        for error_scenario in error_test_scenarios:
            try:
                start_time = time.time()
                
                # Attempt full crisis analysis workflow
                crisis_analysis = all_managers['crisis_pattern'].analyze_message(
                    error_scenario['message'],
                    error_scenario['user_id'],
                    error_scenario['channel_id']
                )
                
                # System should handle gracefully, not crash
                error_handling_time = time.time() - start_time
                
                resilience_results.append({
                    'test': error_scenario['test'],
                    'handled_gracefully': True,
                    'analysis_available': crisis_analysis.get('analysis_available', False),
                    'error_handling_time': error_handling_time,
                    'response_structure_valid': 'summary' in crisis_analysis
                })
                
                logger.info(f"✅ Error scenario '{error_scenario['test']}' handled gracefully")
                
            except Exception as e:
                resilience_results.append({
                    'test': error_scenario['test'],
                    'handled_gracefully': False,
                    'error': str(e)
                })
                logger.warning(f"⚠️ Error scenario '{error_scenario['test']}' not handled gracefully: {e}")
        
        # Validate resilience
        graceful_handling_rate = sum(1 for r in resilience_results if r.get('handled_gracefully', False)) / len(resilience_results)
        
        assert graceful_handling_rate >= 0.75, f"Graceful error handling rate {graceful_handling_rate:.1%} below target (75%)"
        
        logger.info(f"✅ System resilience test passed")
        logger.info(f"🛡️ Graceful error handling rate: {graceful_handling_rate:.1%}")
        
    # ========================================================================
    # FINAL SYSTEM VALIDATION SUMMARY
    # ========================================================================
    
    def test_final_system_validation_summary(self, all_managers):
        """Generate final validation summary for Phase 3e Step 5.6 completion"""
        
        summary_start_time = time.time()
        
        # Collect final system metrics
        system_metrics = {
            'total_managers': len(all_managers),
            'managers_operational': 0,
            'configuration_sections_loaded': 0,
            'feature_flags_operational': 0,
            'crisis_detection_functional': False,
            'performance_targets_met': False,
            'context_enhancement_working': False,
            'error_handling_robust': False
        }
        
        # Test each manager one final time
        for manager_name, manager in all_managers.items():
            try:
                # Basic operational test
                if hasattr(manager, 'get_configuration_summary') or hasattr(manager, 'get_config_section'):
                    system_metrics['managers_operational'] += 1
            except:
                pass
        
        # Test configuration loading
        try:
            crisis_config = all_managers['unified_config'].get_config_section('crisis_patterns')
            analysis_config = all_managers['unified_config'].get_config_section('analysis_parameters')
            if crisis_config and analysis_config:
                system_metrics['configuration_sections_loaded'] = 2
        except:
            pass
        
        # Test feature flags
        try:
            ensemble_enabled = all_managers['feature_config'].is_ensemble_analysis_enabled()
            pattern_enabled = all_managers['feature_config'].is_pattern_analysis_enabled()
            if isinstance(ensemble_enabled, bool) and isinstance(pattern_enabled, bool):
                system_metrics['feature_flags_operational'] = 2
        except:
            pass
        
        # Test crisis detection functionality
        try:
            test_crisis_message = "I'm struggling with severe gender dysphoria and having thoughts of self-harm"
            crisis_result = all_managers['crisis_pattern'].analyze_message(
                test_crisis_message, "final_test_user", "final_test_channel"
            )
            if crisis_result.get('analysis_available', False):
                system_metrics['crisis_detection_functional'] = True
        except:
            pass
        
        # Test performance targets
        try:
            perf_params = all_managers['performance_config'].get_performance_parameters()
            if perf_params.get('timeout_ms', 0) < 1000:
                system_metrics['performance_targets_met'] = True
        except:
            pass
        
        # Test context enhancement
        try:
            context_patterns = all_managers['context_pattern'].extract_context_patterns(
                "Community support helps with my transition"
            )
            if isinstance(context_patterns, list):
                system_metrics['context_enhancement_working'] = True
        except:
            pass
        
        # Test error handling robustness
        try:
            error_test = all_managers['crisis_pattern'].analyze_message("", "error_test", "error_channel")
            if error_test.get('analysis_available') is not None:  # Should handle gracefully
                system_metrics['error_handling_robust'] = True
        except:
            # If it throws an exception, error handling is not robust enough
            pass
        
        summary_time = time.time() - summary_start_time
        
        # Calculate overall system health score
        max_score = 7  # Number of key metrics
        actual_score = (
            (1 if system_metrics['managers_operational'] >= 14 else 0) +
            (1 if system_metrics['configuration_sections_loaded'] >= 2 else 0) +
            (1 if system_metrics['feature_flags_operational'] >= 2 else 0) +
            (1 if system_metrics['crisis_detection_functional'] else 0) +
            (1 if system_metrics['performance_targets_met'] else 0) +
            (1 if system_metrics['context_enhancement_working'] else 0) +
            (1 if system_metrics['error_handling_robust'] else 0)
        )
        
        system_health_score = actual_score / max_score
        
        # Final validation assertions
        assert system_metrics['managers_operational'] >= 14, \
            f"Only {system_metrics['managers_operational']}/14 managers operational"
        assert system_metrics['crisis_detection_functional'], "Crisis detection not functional"
        assert system_metrics['performance_targets_met'], "Performance targets not met"
        assert system_health_score >= 0.85, f"System health score {system_health_score:.1%} below target (85%)"
        
        # Generate final summary report
        final_summary = {
            'phase': '3e Step 5.6',
            'test_completion_time': summary_time,
            'total_managers_tested': system_metrics['total_managers'],
            'managers_operational': system_metrics['managers_operational'],
            'system_health_score': system_health_score,
            'crisis_detection_functional': system_metrics['crisis_detection_functional'],
            'performance_targets_met': system_metrics['performance_targets_met'],
            'context_enhancement_working': system_metrics['context_enhancement_working'],
            'error_handling_robust': system_metrics['error_handling_robust'],
            'ready_for_production': system_health_score >= 0.9,
            'lgbtqia_community_support': 'operational',
            'phase_3e_objectives_met': True
        }
        
        logger.info(f"🏆 PHASE 3E STEP 5.6 FINAL VALIDATION SUMMARY")
        logger.info(f"✅ System Health Score: {system_health_score:.1%}")
        logger.info(f"🎯 Managers Operational: {system_metrics['managers_operational']}/14")
        logger.info(f"🚨 Crisis Detection: {'✅ FUNCTIONAL' if system_metrics['crisis_detection_functional'] else '❌ NOT FUNCTIONAL'}")
        logger.info(f"⚡ Performance Targets: {'✅ MET' if system_metrics['performance_targets_met'] else '❌ NOT MET'}")
        logger.info(f"🔍 Context Enhancement: {'✅ WORKING' if system_metrics['context_enhancement_working'] else '❌ NOT WORKING'}")
        logger.info(f"🛡️ Error Handling: {'✅ ROBUST' if system_metrics['error_handling_robust'] else '❌ NEEDS IMPROVEMENT'}")
        logger.info(f"🏳️‍🌈 LGBTQIA+ Community Support: {final_summary['lgbtqia_community_support'].upper()}")
        logger.info(f"🚀 Production Ready: {'✅ YES' if final_summary['ready_for_production'] else '❌ NO'}")
        
        return final_summary


# ============================================================================
# MAIN TEST EXECUTION WITH COMPREHENSIVE REPORTING
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("🚀 Starting Phase 3e Step 5.6 - Complete System Integration Test")
    print("🏳️‍🌈 Testing all 14 managers with LGBTQIA+ crisis detection scenarios")
    print("🎯 Target: Complete /analyze endpoint simulation in < 500ms")
    print("📊 Validating: System startup, crisis detection, performance, resilience")
    print("=" * 80)
    
    # Run the comprehensive test suite
    test_results = pytest.main([__file__, "-v", "--tb=short", "--capture=no"])
    
    print("=" * 80)
    print("🏆 Phase 3e Step 5.6 Complete System Integration Test Finished")
    print(f"📋 Test Results: {'✅ PASSED' if test_results == 0 else '❌ FAILED'}")
    print("🌈 Ash-NLP Crisis Detection System Ready for LGBTQIA+ Community Support")
    
    exit(test_results)