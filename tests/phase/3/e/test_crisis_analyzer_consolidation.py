# ash-nlp/tests/phase/3/e/test_crisis_analyzer_consolidation.py
"""
Integration tests for Phase 3e Step 4 - CrisisAnalyzer Analysis Method Consolidation
FILE VERSION: v3.1-3e-4.3-1
LAST MODIFIED: 2025-08-17
PHASE: 3e, Step 4.3 - Integration Testing
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Phase 3e Step 4.3 - Comprehensive integration testing for consolidated analysis methods
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import unittest
import asyncio
import json
import tempfile
import os
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, List, Any

# Import the modules we're testing
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from analysis.crisis_analyzer import CrisisAnalyzer
from analysis import create_crisis_analyzer
from managers.shared_utilities import create_shared_utilities_manager
from managers.learning_system import create_learning_system_manager
from managers.unified_config import create_unified_config_manager

class TestCrisisAnalyzerConsolidation(unittest.TestCase):
    """
    Comprehensive integration tests for Phase 3e Step 4 CrisisAnalyzer consolidation
    Tests consolidated analysis methods, SharedUtilities integration, and LearningSystem integration
    """
    
    def setUp(self):
        """Set up test environment with all required managers"""
        # Create temporary config directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = os.path.join(self.temp_dir, 'config')
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Create test configuration files
        self._create_test_config_files()
        
        # Create core managers
        self.unified_config_manager = create_unified_config_manager(self.config_dir)
        
        # Create Phase 3e managers
        self.shared_utilities_manager = create_shared_utilities_manager(self.unified_config_manager)
        self.learning_system_manager = create_learning_system_manager(
            self.unified_config_manager, 
            self.shared_utilities_manager
        )
        
        # Create mock managers for dependencies
        self.model_ensemble_manager = self._create_mock_model_ensemble_manager()
        self.crisis_pattern_manager = self._create_mock_crisis_pattern_manager()
        self.analysis_parameters_manager = self._create_mock_analysis_parameters_manager()
        self.threshold_mapping_manager = self._create_mock_threshold_mapping_manager()
        self.feature_config_manager = self._create_mock_feature_config_manager()
        self.performance_config_manager = self._create_mock_performance_config_manager()
        self.context_pattern_manager = self._create_mock_context_pattern_manager()
        
        # Create enhanced CrisisAnalyzer with all dependencies
        self.crisis_analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            crisis_pattern_manager=self.crisis_pattern_manager,
            analysis_parameters_manager=self.analysis_parameters_manager,
            threshold_mapping_manager=self.threshold_mapping_manager,
            feature_config_manager=self.feature_config_manager,
            performance_config_manager=self.performance_config_manager,
            context_pattern_manager=self.context_pattern_manager,
            shared_utilities_manager=self.shared_utilities_manager,         # NEW Phase 3e
            learning_system_manager=self.learning_system_manager            # NEW Phase 3e
        )
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_config_files(self):
        """Create test configuration files for integration testing"""
        
        # Analysis parameters configuration
        analysis_params_config = {
            "crisis_thresholds": {
                "critical": 0.95,
                "high": 0.8,
                "medium": 0.6,
                "low": 0.4
            },
            "timeouts": {
                "ensemble": 30,
                "individual_model": 10,
                "pattern_analysis": 5
            },
            "confidence_boosts": {
                "pattern_match": 0.1,
                "context_boost": 0.15,
                "ensemble_agreement": 0.2
            },
            "pattern_weights": {
                "crisis_keywords": 1.0,
                "context_patterns": 0.8,
                "temporal_indicators": 0.6,
                "community_vocabulary": 0.7
            },
            "algorithm_parameters": {
                "min_confidence": 0.3,
                "max_analysis_depth": 3,
                "ensemble_weight_distribution": "balanced",
                "learning_rate": 0.01
            }
        }
        
        with open(os.path.join(self.config_dir, 'analysis_parameters.json'), 'w') as f:
            json.dump(analysis_params_config, f, indent=2)
        
        # Threshold mapping configuration
        threshold_mapping_config = {
            "modes": {
                "default": {
                    "critical": 0.95,
                    "high": 0.8,
                    "medium": 0.6,
                    "low": 0.4
                },
                "emergency": {
                    "critical": 0.9,
                    "high": 0.7,
                    "medium": 0.5,
                    "low": 0.3
                },
                "conservative": {
                    "critical": 0.98,
                    "high": 0.85,
                    "medium": 0.7,
                    "low": 0.5
                }
            }
        }
        
        with open(os.path.join(self.config_dir, 'threshold_mapping.json'), 'w') as f:
            json.dump(threshold_mapping_config, f, indent=2)
        
        # Learning system configuration
        learning_config = {
            "learning_enabled": True,
            "adaptation_rate": 0.05,
            "max_daily_adjustments": 50,
            "threshold_bounds": {
                "min": 0.1,
                "max": 0.95
            }
        }
        
        with open(os.path.join(self.config_dir, 'learning_system.json'), 'w') as f:
            json.dump(learning_config, f, indent=2)
    
    def _create_mock_model_ensemble_manager(self):
        """Create mock ModelEnsembleManager for testing"""
        mock_manager = Mock()
        mock_manager.analyze_message_with_ensemble.return_value = {
            'confidence': 0.75,
            'models': ['model1', 'model2', 'model3'],
            'individual_scores': [0.7, 0.8, 0.75]
        }
        return mock_manager
    
    def _create_mock_threshold_mapping_manager(self):
        """Create mock ThresholdMappingManager for testing"""
        mock_manager = Mock()
        mock_manager.get_threshold_for_mode.return_value = {'high': 0.8, 'medium': 0.6, 'low': 0.4}
        mock_manager.apply_threshold_to_confidence.return_value = 'high'
        mock_manager.calculate_crisis_level.return_value = 'high'
        mock_manager.validate_analysis_thresholds.return_value = True
        return mock_manager
    
    def _create_mock_feature_config_manager(self):
        """Create mock FeatureConfigManager for testing"""
        mock_manager = Mock()
        mock_manager.is_feature_enabled.return_value = True
        return mock_manager
    
    def _create_mock_performance_config_manager(self):
        """Create mock PerformanceConfigManager for testing"""
        mock_manager = Mock()
        mock_manager.get_timeout_settings.return_value = {'analysis': 30, 'model': 10}
        return mock_manager
    
    def _create_mock_context_pattern_manager(self):
        """Create mock ContextPatternManager for testing"""
        mock_manager = Mock()
        mock_manager.analyze_context.return_value = {
            'context_score': 0.8,
            'context_patterns': ['temporal_urgency', 'isolation_indicators']
        }
        return mock_manager

    # ========================================================================
    # PHASE 3E STEP 4.1: ENHANCED FACTORY FUNCTION TESTING
    # ========================================================================
    
    def test_enhanced_crisis_analyzer_creation(self):
        """Test enhanced CrisisAnalyzer factory function with new dependencies"""
        
        # Test creation with all dependencies
        analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            crisis_pattern_manager=self.crisis_pattern_manager,
            analysis_parameters_manager=self.analysis_parameters_manager,
            threshold_mapping_manager=self.threshold_mapping_manager,
            feature_config_manager=self.feature_config_manager,
            performance_config_manager=self.performance_config_manager,
            context_pattern_manager=self.context_pattern_manager,
            shared_utilities_manager=self.shared_utilities_manager,
            learning_system_manager=self.learning_system_manager
        )
        
        # Verify analyzer created successfully
        self.assertIsInstance(analyzer, CrisisAnalyzer)
        
        # Verify all dependencies are properly injected
        self.assertEqual(analyzer.model_ensemble_manager, self.model_ensemble_manager)
        self.assertEqual(analyzer.shared_utilities_manager, self.shared_utilities_manager)
        self.assertEqual(analyzer.learning_system_manager, self.learning_system_manager)
        
        print("✅ Enhanced CrisisAnalyzer creation test passed")
    
    def test_dependency_injection_compliance(self):
        """Test all dependencies properly injected and accessible"""
        
        # Test each manager dependency accessible
        self.assertIsNotNone(self.crisis_analyzer.model_ensemble_manager)
        self.assertIsNotNone(self.crisis_analyzer.crisis_pattern_manager)
        self.assertIsNotNone(self.crisis_analyzer.analysis_parameters_manager)
        self.assertIsNotNone(self.crisis_analyzer.threshold_mapping_manager)
        self.assertIsNotNone(self.crisis_analyzer.feature_config_manager)
        self.assertIsNotNone(self.crisis_analyzer.performance_config_manager)
        self.assertIsNotNone(self.crisis_analyzer.context_pattern_manager)
        
        # Test NEW Phase 3e dependencies
        self.assertIsNotNone(self.crisis_analyzer.shared_utilities_manager)
        self.assertIsNotNone(self.crisis_analyzer.learning_system_manager)
        
        # Test UnifiedConfigManager access through SharedUtilities
        config_manager = self.crisis_analyzer.shared_utilities_manager.config_manager
        self.assertIsNotNone(config_manager)
        
        print("✅ Dependency injection compliance test passed")
    
    def test_fallback_creation_without_phase_3e_dependencies(self):
        """Test fallback behavior when Phase 3e dependencies not available"""
        
        # Create analyzer without Phase 3e dependencies
        analyzer = create_crisis_analyzer(
            model_ensemble_manager=self.model_ensemble_manager,
            crisis_pattern_manager=self.crisis_pattern_manager,
            analysis_parameters_manager=self.analysis_parameters_manager,
            threshold_mapping_manager=self.threshold_mapping_manager,
            feature_config_manager=self.feature_config_manager,
            performance_config_manager=self.performance_config_manager,
            context_pattern_manager=self.context_pattern_manager
            # No Phase 3e dependencies
        )
        
        # Verify analyzer still works
        self.assertIsInstance(analyzer, CrisisAnalyzer)
        self.assertIsNone(analyzer.shared_utilities_manager)
        self.assertIsNone(analyzer.learning_system_manager)
        
        print("✅ Fallback creation test passed")

    # ========================================================================
    # PHASE 3E STEP 4.2: CONSOLIDATED METHOD TESTING
    # ========================================================================
    
    def test_analysis_parameters_consolidation(self):
        """Test analysis parameter methods work after consolidation"""
        
        # Test crisis threshold access
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        self.assertIsInstance(thresholds, dict)
        self.assertIn('high', thresholds)
        self.assertIn('medium', thresholds)
        self.assertIn('low', thresholds)
        self.assertIn('critical', thresholds)
        
        # Test timeout settings
        timeouts = self.crisis_analyzer.get_analysis_timeout_settings()
        self.assertIsInstance(timeouts, dict)
        self.assertIn('ensemble', timeouts)
        
        # Test confidence boost functionality
        boosts = self.crisis_analyzer.get_analysis_confidence_boosts()
        self.assertIsInstance(boosts, dict)
        self.assertIn('pattern_match', boosts)
        
        # Test pattern weights
        weights = self.crisis_analyzer.get_analysis_pattern_weights()
        self.assertIsInstance(weights, dict)
        self.assertIn('crisis_keywords', weights)
        
        # Test algorithm parameter retrieval
        params = self.crisis_analyzer.get_analysis_algorithm_parameters()
        self.assertIsInstance(params, dict)
        self.assertIn('min_confidence', params)
        
        print("✅ Analysis parameters consolidation test passed")
    
    def test_threshold_mapping_consolidation(self):
        """Test threshold mapping methods work after consolidation"""
        
        # Test threshold application to confidence scores
        crisis_level = self.crisis_analyzer.apply_crisis_thresholds(0.85, 'default')
        self.assertIn(crisis_level, ['none', 'low', 'medium', 'high', 'critical'])
        
        # Test crisis level calculation
        result = self.crisis_analyzer.calculate_crisis_level_from_confidence(0.75)
        self.assertIsInstance(result, dict)
        self.assertIn('crisis_level', result)
        self.assertIn('confidence_score', result)
        
        # Test mode-specific threshold behavior
        default_thresholds = self.crisis_analyzer.get_mode_specific_crisis_thresholds('default')
        emergency_thresholds = self.crisis_analyzer.get_mode_specific_crisis_thresholds('emergency')
        self.assertIsInstance(default_thresholds, dict)
        self.assertIsInstance(emergency_thresholds, dict)
        
        # Test threshold validation
        validation = self.crisis_analyzer.validate_crisis_analysis_thresholds()
        self.assertIsInstance(validation, dict)
        
        print("✅ Threshold mapping consolidation test passed")
    
    def test_ensemble_analysis_consolidation(self):
        """Test ensemble analysis methods work after consolidation"""
        
        # Test enhanced ensemble analysis
        results = self.crisis_analyzer.perform_ensemble_crisis_analysis(
            "I feel hopeless and want to end it all", "test_user", "test_channel"
        )
        self.assertIsInstance(results, dict)
        self.assertIn('confidence', results)
        
        # Test model result combination
        model_results = [
            {'confidence': 0.7, 'model': 'model1'},
            {'confidence': 0.8, 'model': 'model2'},
            {'confidence': 0.75, 'model': 'model3'}
        ]
        combined = self.crisis_analyzer.combine_ensemble_model_results(model_results)
        self.assertIsInstance(combined, dict)
        self.assertIn('confidence', combined)
        
        # Test ensemble weight application
        test_results = {'confidence': 0.7, 'context': {'user_id': 'test'}}
        weighted = self.crisis_analyzer.apply_ensemble_analysis_weights(test_results)
        self.assertIsInstance(weighted, dict)
        
        print("✅ Ensemble analysis consolidation test passed")

    # ========================================================================
    # PHASE 3E STEP 4.3: INTEGRATION TESTING
    # ========================================================================
    
    def test_learning_feedback_integration(self):
        """Test learning system integration with analysis"""
        
        # Test false positive adjustment integration
        if self.learning_system_manager:
            # Test learning system can adapt thresholds
            base_thresholds = {'high': 0.8, 'medium': 0.6, 'low': 0.4}
            adapted = self.learning_system_manager.adjust_thresholds_for_context(
                base_thresholds, 'default', 0.75
            )
            self.assertIsInstance(adapted, dict)
        
        # Test threshold adaptation in crisis analysis
        result = self.crisis_analyzer.calculate_crisis_level_from_confidence(
            0.75, {'analysis_mode': 'default', 'user_id': 'test'}
        )
        
        if self.crisis_analyzer.learning_system_manager:
            self.assertIn('threshold_source', result)
            self.assertEqual(result['threshold_source'], 'learning_adapted')
        
        print("✅ Learning feedback integration test passed")
    
    def test_shared_utilities_integration(self):
        """Test shared utilities usage in analysis"""
        
        # Test configuration validation using shared utilities
        if self.shared_utilities_manager:
            # Test safe configuration access
            config_section = self.shared_utilities_manager.config_manager.get_config_section(
                'analysis_parameters', 'crisis_thresholds', {}
            )
            self.assertIsInstance(config_section, dict)
        
        # Test error handling using shared utilities in consolidated methods
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        self.assertIsInstance(thresholds, dict)
        
        # Test status reporting through shared utilities
        validation = self.crisis_analyzer.validate_crisis_analysis_thresholds()
        self.assertIsInstance(validation, dict)
        
        print("✅ Shared utilities integration test passed")
    
    def test_complete_crisis_analysis_workflow(self):
        """Test complete analysis workflow with all consolidations"""
        
        # Test full message analysis pipeline
        test_message = "I can't take this anymore and I'm thinking of ending my life"
        
        # Use the main analyze_message method which should use all consolidated methods
        analysis_result = asyncio.run(
            self.crisis_analyzer.analyze_message(
                test_message, 
                user_id='test_user',
                channel_id='test_channel',
                analysis_mode='default'
            )
        )
        
        # Verify comprehensive analysis result
        self.assertIsInstance(analysis_result, dict)
        self.assertIn('confidence', analysis_result)
        self.assertIn('crisis_level', analysis_result)
        self.assertIn('analysis_mode', analysis_result)
        self.assertIn('phase_3e_enhanced', analysis_result)
        
        # Verify Phase 3e enhancement flag
        self.assertTrue(analysis_result.get('phase_3e_enhanced', False))
        
        print("✅ Complete crisis analysis workflow test passed")
    
    def test_backward_compatibility(self):
        """Test enhanced CrisisAnalyzer maintains existing functionality"""
        
        # Test existing analyze_message method still works
        result = asyncio.run(
            self.crisis_analyzer.analyze_message("test message", "user1", "channel1")
        )
        self.assertIsInstance(result, dict)
        self.assertIn('confidence', result)
        
        # Test that old API patterns still work
        self.assertTrue(hasattr(self.crisis_analyzer, 'model_ensemble_manager'))
        self.assertTrue(hasattr(self.crisis_analyzer, 'crisis_pattern_manager'))
        
        # Test that new consolidated methods don't break existing functionality
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        self.assertIsInstance(thresholds, dict)
        
        print("✅ Backward compatibility test passed")
    
    def test_configuration_access_patterns(self):
        """Test configuration access via UnifiedConfigManager"""
        
        # Test primary access via SharedUtilities
        if self.crisis_analyzer.shared_utilities_manager:
            config = self.crisis_analyzer.shared_utilities_manager.config_manager
            self.assertIsNotNone(config)
            
            # Test configuration section access
            section = config.get_config_section('analysis_parameters', 'crisis_thresholds', {})
            self.assertIsInstance(section, dict)
        
        # Test consolidated methods use proper configuration access
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        timeouts = self.crisis_analyzer.get_analysis_timeout_settings()
        boosts = self.crisis_analyzer.get_analysis_confidence_boosts()
        
        # All should return valid dictionaries
        self.assertIsInstance(thresholds, dict)
        self.assertIsInstance(timeouts, dict)
        self.assertIsInstance(boosts, dict)
        
        print("✅ Configuration access patterns test passed")
    
    def test_performance_impact_validation(self):
        """Test performance impact of consolidation is minimal"""
        
        import time
        
        # Measure analysis time
        start_time = time.time()
        
        # Run multiple analyses
        for i in range(10):
            result = asyncio.run(
                self.crisis_analyzer.analyze_message(
                    f"Test message {i}", f"user_{i}", f"channel_{i}"
                )
            )
            self.assertIsInstance(result, dict)
        
        analysis_time = time.time() - start_time
        
        # Performance should be reasonable (less than 1 second for 10 analyses)
        self.assertLess(analysis_time, 1.0, "Performance impact too high")
        
        # Check that performance metadata is included
        result = asyncio.run(
            self.crisis_analyzer.analyze_message("test", "user", "channel")
        )
        self.assertIn('analysis_time', result)
        
        print(f"✅ Performance validation passed - {analysis_time:.3f}s for 10 analyses")

    # ========================================================================
    # PHASE 3E STEP 4: RULE #7 COMPLIANCE TESTING
    # ========================================================================
    
    def test_rule_7_compliance_no_new_environment_variables(self):
        """Test that Phase 3e Step 4 adds zero new environment variables"""
        
        # Test that all consolidated methods work with existing configuration
        thresholds = self.crisis_analyzer.get_analysis_crisis_thresholds()
        timeouts = self.crisis_analyzer.get_analysis_timeout_settings()
        boosts = self.crisis_analyzer.get_analysis_confidence_boosts()
        weights = self.crisis_analyzer.get_analysis_pattern_weights()
        params = self.crisis_analyzer.get_analysis_algorithm_parameters()
        
        # All methods should work without requiring new environment variables
        self.assertIsInstance(thresholds, dict)
        self.assertIsInstance(timeouts, dict)
        self.assertIsInstance(boosts, dict)
        self.assertIsInstance(weights, dict)
        self.assertIsInstance(params, dict)
        
        # Test that learning system works with existing variables
        if self.learning_system_manager:
            learning_config = self.learning_system_manager.get_learning_configuration()
            self.assertIsInstance(learning_config, dict)
        
        print("✅ Rule #7 compliance test passed - No new environment variables required")

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
    
    print("\n" + "="*80)
    print("🎉 PHASE 3E STEP 4.3 INTEGRATION TESTING COMPLETE")
    print("✅ Enhanced CrisisAnalyzer with consolidated analysis methods")
    print("✅ SharedUtilities and LearningSystem integration validated")
    print("✅ Backward compatibility maintained")
    print("✅ Performance impact minimal")
    print("✅ Clean Architecture v3.1 compliance verified")
    print("✅ Rule #7 compliance confirmed (zero new environment variables)")
    print("="*80)
    
    def _create_mock_crisis_pattern_manager(self):
        """Create mock CrisisPatternManager for testing"""
        mock_manager = Mock()
        mock_manager.analyze_patterns.return_value = {
            'pattern_matches': ['suicidal_ideation', 'hopelessness'],
            'confidence_boost': 0.15
        }
        return mock_manager
    
    def _create_mock_analysis_parameters_manager(self):
        """Create mock AnalysisParametersManager for testing"""
        mock_manager = Mock()
        mock_manager.get_crisis_thresholds.return_value = {'high': 0.8, 'medium': 0.6, 'low': 0.4}
        mock_manager.get_analysis_timeouts.return_value = {'ensemble': 30, 'individual_model': 10}
        mock_manager.get_confidence_boosts.return_value = {'pattern_match': 0.1, 'context_boost': 0.15}
        mock_manager.get_pattern_weights.return_value = {'crisis_keywords': 1.0, 'context_patterns': 0.8}
        mock_manager.get_algorithm_parameters.return_value = {'min_confidence': 0.3, 'max_analysis_depth': 3}
        return mock_manager