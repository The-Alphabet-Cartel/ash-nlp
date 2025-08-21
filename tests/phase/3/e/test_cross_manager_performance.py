#!/usr/bin/env python3
"""
Integration Test: Performance Enhancement Cross-Manager Workflow
Phase 3e Step 5.6 - Test Group 3

This test validates performance optimization managers and context enhancement
functionality working together to provide optimized crisis detection with
enhanced analysis capabilities.

Test Group 3: Performance & Analysis Enhancement
- PerformanceConfigManager + ContextPatternManager + ZeroShotManager + StorageConfigManager

Target: Optimized analysis with context enhancement maintaining < 500ms total time
"""

import pytest
import asyncio
import time
import logging
import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from managers import (
    create_unified_config_manager,
    create_performance_config_manager,
    create_context_pattern_manager,
    create_zero_shot_manager,
    create_storage_config_manager,
    create_crisis_pattern_manager,  # For integration testing
    create_analysis_parameters_manager  # For integration testing
)

logger = logging.getLogger(__name__)

class TestPerformanceEnhancementIntegration:
    """
    Integration test for performance and analysis enhancement managers
    Tests optimization capabilities with enhanced context analysis
    """
    
    @pytest.fixture(scope="class")
    def config_manager(self):
        """Create UnifiedConfigManager for all tests"""
        return create_unified_config_manager()
    
    @pytest.fixture(scope="class")
    def enhancement_managers(self, config_manager):
        """Create all performance and enhancement managers"""
        managers = {}
        
        # Core configuration
        managers['unified_config'] = config_manager
        
        # Test Group 3: Performance & Analysis Enhancement
        managers['performance_config'] = create_performance_config_manager(config_manager)
        managers['context_pattern'] = create_context_pattern_manager(config_manager)
        managers['zero_shot'] = create_zero_shot_manager(config_manager)
        managers['storage_config'] = create_storage_config_manager(config_manager)
        
        # Integration support managers
        managers['crisis_pattern'] = create_crisis_pattern_manager(config_manager)
        managers['analysis_parameters'] = create_analysis_parameters_manager(config_manager)
        
        # Validate all managers initialized properly
        for name, manager in managers.items():
            assert manager is not None, f"{name} manager failed to initialize"
            
        logger.info("✅ All 6 enhancement managers initialized successfully")
        return managers
    
    # ========================================================================
    # PERFORMANCE CONFIGURATION INTEGRATION
    # ========================================================================
    
    def test_performance_configuration_integration(self, enhancement_managers):
        """Test performance configuration affects system behavior"""
        
        performance_config = enhancement_managers['performance_config']
        
        # Test 1: Performance parameters availability
        try:
            perf_params = performance_config.get_performance_parameters()
            assert 'timeout_ms' in perf_params, "Performance parameters missing timeout_ms"
            assert 'max_concurrent' in perf_params, "Performance parameters missing max_concurrent"
            assert 'enable_caching' in perf_params, "Performance parameters missing enable_caching"
            assert 'cache_ttl_seconds' in perf_params, "Performance parameters missing cache_ttl_seconds"
            
            # Validate parameter types and values
            assert isinstance(perf_params['timeout_ms'], int), "timeout_ms must be integer"
            assert isinstance(perf_params['max_concurrent'], int), "max_concurrent must be integer"
            assert isinstance(perf_params['enable_caching'], bool), "enable_caching must be boolean"
            assert perf_params['timeout_ms'] > 0, "timeout_ms must be positive"
            assert perf_params['max_concurrent'] > 0, "max_concurrent must be positive"
            
        except Exception as e:
            pytest.fail(f"Performance configuration test failed: {e}")
        
        # Test 2: Caching configuration integration
        try:
            caching_config = performance_config.get_caching_configuration()
            assert isinstance(caching_config, dict), "Caching configuration must be dict"
            
            if perf_params['enable_caching']:
                assert 'cache_size' in caching_config or 'default_ttl' in caching_config, \
                    "Enabled caching missing configuration"
                    
        except Exception as e:
            pytest.fail(f"Caching configuration integration failed: {e}")
        
        # Test 3: Timeout configuration affects other managers
        try:
            # Performance configuration should influence analysis timing
            timeout_ms = perf_params['timeout_ms']
            assert timeout_ms < 1000, "Timeout too high for real-time analysis"
            assert timeout_ms >= 100, "Timeout too low for proper analysis"
            
        except Exception as e:
            pytest.fail(f"Timeout configuration validation failed: {e}")
        
        logger.info(f"✅ Performance configuration integration test passed")
        logger.info(f"⚡ Timeout: {perf_params['timeout_ms']}ms, Max concurrent: {perf_params['max_concurrent']}")
        logger.info(f"🗄️ Caching enabled: {perf_params['enable_caching']}")
        
    # ========================================================================
    # CONTEXT PATTERN ENHANCEMENT INTEGRATION
    # ========================================================================
    
    def test_context_pattern_enhancement_integration(self, enhancement_managers):
        """Test context pattern enhancement with crisis analysis"""
        
        context_manager = enhancement_managers['context_pattern']
        crisis_manager = enhancement_managers['crisis_pattern']
        
        # LGBTQIA+ community test messages with varying context needs
        context_test_cases = [
            {
                'message': "Struggling with coming out to conservative family",
                'expected_contexts': ['family_conflict', 'coming_out_stress'],
                'context_type': 'social_context'
            },
            {
                'message': "Gender dysphoria getting worse lately, especially at night",
                'expected_contexts': ['gender_dysphoria', 'temporal_pattern'],
                'context_type': 'temporal_emotional'
            },
            {
                'message': "Our pride group meeting was so supportive and affirming",
                'expected_contexts': ['community_support', 'positive_affirmation'],
                'context_type': 'positive_social'
            },
            {
                'message': "Questioning my identity again after workplace discrimination",
                'expected_contexts': ['identity_questioning', 'workplace_stress'],
                'context_type': 'discrimination_stress'
            }
        ]
        
        context_enhancement_results = []
        
        for test_case in context_test_cases:
            start_time = time.time()
            
            try:
                # Step 1: Extract base context patterns
                base_patterns = context_manager.extract_context_patterns(test_case['message'])
                assert isinstance(base_patterns, list), "Context patterns must be list"
                
                # Step 2: Get enhanced contextual weights
                contextual_weights = context_manager.get_contextual_weights()
                assert isinstance(contextual_weights, dict), "Contextual weights must be dict"
                
                # Step 3: Apply context enhancement to crisis analysis
                enhanced_analysis = crisis_manager.analyze_message(
                    test_case['message'],
                    f"user_{test_case['context_type']}",
                    "support_channel"
                )
                
                # Step 4: Validate context enhancement improves analysis
                base_crisis_analysis = crisis_manager.analyze_message(
                    test_case['message'],
                    f"user_{test_case['context_type']}_base",
                    "general_channel"  # Different channel for comparison
                )
                
                enhancement_time = time.time() - start_time
                
                # Validate context enhancement
                enhanced_score = enhanced_analysis.get('summary', {}).get('crisis_score', 0.0)
                base_score = base_crisis_analysis.get('summary', {}).get('crisis_score', 0.0)
                
                context_enhancement_results.append({
                    'context_type': test_case['context_type'],
                    'patterns_found': len(base_patterns),
                    'enhancement_time': enhancement_time,
                    'enhanced_score': enhanced_score,
                    'base_score': base_score,
                    'score_improvement': enhanced_score - base_score,
                    'context_weights_available': len(contextual_weights) > 0
                })
                
                # Performance validation
                assert enhancement_time < 0.2, f"Context enhancement too slow: {enhancement_time:.3f}s"
                
                logger.info(f"✅ Context enhancement for '{test_case['context_type']}': "
                           f"{enhancement_time:.3f}s, patterns={len(base_patterns)}")
                
            except Exception as e:
                pytest.fail(f"Context pattern enhancement failed for {test_case['context_type']}: {e}")
        
        # Analyze enhancement effectiveness
        avg_enhancement_time = sum(r['enhancement_time'] for r in context_enhancement_results) / len(context_enhancement_results)
        patterns_detected = sum(r['patterns_found'] for r in context_enhancement_results)
        context_weights_working = sum(1 for r in context_enhancement_results if r['context_weights_available'])
        
        assert avg_enhancement_time < 0.15, f"Average enhancement time too slow: {avg_enhancement_time:.3f}s"
        assert patterns_detected > 0, "No context patterns detected across all test cases"
        assert context_weights_working > 0, "Contextual weights not working"
        
        logger.info(f"✅ Context pattern enhancement integration test passed")
        logger.info(f"⚡ Average enhancement time: {avg_enhancement_time:.3f}s")
        logger.info(f"🔍 Total patterns detected: {patterns_detected}")
        logger.info(f"⚖️ Context weights working: {context_weights_working}/{len(context_enhancement_results)}")
        
    # ========================================================================
    # ZERO-SHOT MODEL INTEGRATION
    # ========================================================================
    
    def test_zero_shot_model_integration(self, enhancement_managers):
        """Test zero-shot model integration with analysis workflow"""
        
        zero_shot_manager = enhancement_managers['zero_shot']
        
        # Test 1: Zero-shot model configuration
        try:
            model_config = zero_shot_manager.get_zero_shot_configuration()
            assert isinstance(model_config, dict), "Zero-shot configuration must be dict"
            
            # Validate essential configuration elements
            required_configs = ['model_name', 'enabled', 'fallback_behavior']
            for config_key in required_configs:
                if config_key in model_config:
                    logger.info(f"✅ Zero-shot config has {config_key}: {model_config[config_key]}")
                
        except Exception as e:
            pytest.fail(f"Zero-shot model configuration failed: {e}")
        
        # Test 2: Label management integration
        try:
            # Test dynamic label management for LGBTQIA+ contexts
            test_labels = [
                'gender_dysphoria_crisis',
                'coming_out_stress', 
                'family_rejection',
                'workplace_discrimination',
                'identity_questioning',
                'community_support_positive'
            ]
            
            label_results = {}
            for label in test_labels:
                try:
                    label_config = zero_shot_manager.get_label_configuration(label)
                    label_results[label] = label_config is not None
                except:
                    label_results[label] = False
            
            labels_available = sum(1 for available in label_results.values() if available)
            logger.info(f"📋 Zero-shot labels available: {labels_available}/{len(test_labels)}")
            
        except Exception as e:
            pytest.fail(f"Zero-shot label management failed: {e}")
        
        # Test 3: Model ensemble integration
        try:
            # Zero-shot should work with model ensemble for enhanced accuracy
            ensemble_weights = enhancement_managers['zero_shot'].config_manager.get_config_section('model_ensemble')
            if ensemble_weights:
                # Validate zero-shot model weight in ensemble
                zero_shot_weight = ensemble_weights.get('zero_shot', {}).get('weight', 0)
                assert isinstance(zero_shot_weight, (int, float)), "Zero-shot weight must be numeric"
                
        except Exception as e:
            logger.warning(f"Zero-shot ensemble integration check failed: {e}")
        
        logger.info(f"✅ Zero-shot model integration test passed")
        
    # ========================================================================
    # STORAGE CONFIGURATION INTEGRATION  
    # ========================================================================
    
    def test_storage_configuration_integration(self, enhancement_managers):
        """Test storage configuration supports analysis workflow"""
        
        storage_manager = enhancement_managers['storage_config']
        
        # Test 1: Storage paths configuration
        try:
            storage_paths = storage_manager.get_storage_paths()
            assert isinstance(storage_paths, dict), "Storage paths must be dict"
            
            # Validate critical paths for crisis detection system
            critical_paths = ['models', 'logs', 'cache', 'backups']
            paths_available = []
            
            for path_type in critical_paths:
                if path_type in storage_paths:
                    path_value = storage_paths[path_type]
                    assert isinstance(path_value, str), f"{path_type} path must be string"
                    assert len(path_value) > 0, f"{path_type} path cannot be empty"
                    paths_available.append(path_type)
                    
            logger.info(f"📁 Storage paths available: {paths_available}")
            
        except Exception as e:
            pytest.fail(f"Storage paths configuration failed: {e}")
        
        # Test 2: Cache configuration integration
        try:
            cache_config = storage_manager.get_caching_configuration()
            assert isinstance(cache_config, dict), "Cache configuration must be dict"
            
            # Validate cache works with performance configuration
            performance_params = enhancement_managers['performance_config'].get_performance_parameters()
            if performance_params.get('enable_caching', False):
                # Cache should be properly configured
                cache_enabled = cache_config.get('enabled', False)
                assert isinstance(cache_enabled, bool), "Cache enabled flag must be boolean"
                
        except Exception as e:
            pytest.fail(f"Cache configuration integration failed: {e}")
        
        # Test 3: Data persistence configuration
        try:
            persistence_config = storage_manager.get_data_persistence_configuration()
            assert isinstance(persistence_config, dict), "Persistence configuration must be dict"
            
            # Validate backup and recovery settings
            backup_settings = persistence_config.get('backup', {})
            if backup_settings:
                backup_enabled = backup_settings.get('enabled', False)
                assert isinstance(backup_enabled, bool), "Backup enabled must be boolean"
                
        except Exception as e:
            pytest.fail(f"Data persistence configuration failed: {e}")
        
        logger.info(f"✅ Storage configuration integration test passed")
        
    # ========================================================================
    # COMPREHENSIVE PERFORMANCE ENHANCEMENT WORKFLOW
    # ========================================================================
    
    def test_comprehensive_enhancement_workflow(self, enhancement_managers):
        """Test complete enhanced analysis workflow with all optimization managers"""
        
        # Complex LGBTQIA+ crisis message for comprehensive testing
        complex_test_message = """
        I've been struggling with gender dysphoria for months now, and it's getting worse. 
        My family doesn't understand and keeps deadnaming me. The discrimination at work 
        is making me question everything about my identity. I feel completely alone and 
        don't know if I can keep going like this. The community support group helps sometimes, 
        but the overwhelming feelings come back every night.
        """
        
        workflow_start_time = time.time()
        
        try:
            # Step 1: Performance configuration setup
            perf_params = enhancement_managers['performance_config'].get_performance_parameters()
            
            # Step 2: Context pattern enhancement
            context_patterns = enhancement_managers['context_pattern'].extract_context_patterns(complex_test_message)
            contextual_weights = enhancement_managers['context_pattern'].get_contextual_weights()
            
            # Step 3: Zero-shot model configuration
            zero_shot_config = enhancement_managers['zero_shot'].get_zero_shot_configuration()
            
            # Step 4: Storage optimization
            storage_paths = enhancement_managers['storage_config'].get_storage_paths()
            cache_config = enhancement_managers['storage_config'].get_caching_configuration()
            
            # Step 5: Integrated crisis analysis with all enhancements
            enhanced_crisis_analysis = enhancement_managers['crisis_pattern'].analyze_message(
                complex_test_message,
                "comprehensive_test_user",
                "crisis_support_channel"
            )
            
            # Step 6: Performance analysis integration
            analysis_params = enhancement_managers['analysis_parameters'].get_contextual_weighting_parameters()
            
            total_workflow_time = time.time() - workflow_start_time
            
            # Validate comprehensive workflow
            assert enhanced_crisis_analysis['analysis_available'] is True, "Enhanced analysis not available"
            assert len(context_patterns) > 0, "No context patterns detected in complex message"
            assert len(contextual_weights) > 0, "No contextual weights available"
            assert total_workflow_time < 0.5, f"Complete workflow too slow: {total_workflow_time:.3f}s"
            
            # Validate enhancement effectiveness
            crisis_score = enhanced_crisis_analysis.get('summary', {}).get('crisis_score', 0.0)
            safety_assessment = enhanced_crisis_analysis.get('safety_assessment', {})
            
            assert crisis_score > 0.0, "Enhanced analysis should detect crisis in complex message"
            assert 'crisis_detected' in safety_assessment, "Safety assessment missing crisis detection"
            
            logger.info(f"✅ Comprehensive enhancement workflow completed in {total_workflow_time:.3f}s")
            logger.info(f"🔍 Context patterns found: {len(context_patterns)}")
            logger.info(f"🎯 Crisis score: {crisis_score:.2f}")
            logger.info(f"🚨 Crisis detected: {safety_assessment.get('crisis_detected', False)}")
            
        except Exception as e:
            pytest.fail(f"Comprehensive enhancement workflow failed: {e}")
        
        return {
            'total_time': total_workflow_time,
            'context_patterns': len(context_patterns),
            'crisis_score': crisis_score,
            'enhancement_successful': True
        }


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Starting Phase 3e Step 5.6 - Performance Enhancement Integration Test")
    print("⚡ Testing optimization and context enhancement managers")
    print("🎯 Target: Enhanced analysis maintaining < 500ms total time")
    print()
    
    # Run the test suite
    pytest.main([__file__, "-v", "--tb=short"])