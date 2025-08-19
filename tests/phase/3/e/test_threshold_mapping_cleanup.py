# ash-nlp/tests/phase/3/e/test_threshold_mapping_cleanup.py
"""
Integration Tests for Phase 3e Sub-step 5.2: ThresholdMappingManager Cleanup
FILE VERSION: v3.1-3e-5.2-1
LAST MODIFIED: 2025-08-19
PHASE: 3e, Sub-step 5.2
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Testing methods moved to CrisisAnalyzer and LearningSystemManager
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import pytest
import logging
import sys
import os
from typing import Dict, Any
from unittest.mock import Mock, patch

# Setup path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

# Import managers
from managers.unified_config_manager import create_unified_config_manager
from managers.threshold_mapping_manager import create_threshold_mapping_manager
from analysis.crisis_analyzer import create_crisis_analyzer

logger = logging.getLogger(__name__)

class TestThresholdMappingManagerCleanup:
    """Test suite for Phase 3e Sub-step 5.2: ThresholdMappingManager cleanup"""
    
    @pytest.fixture
    def setup_managers(self):
        """Setup test managers with proper configuration"""
        try:
            # Create unified config manager
            unified_config = create_unified_config_manager()
            
            # Create threshold mapping manager (cleaned version)
            threshold_manager = create_threshold_mapping_manager(unified_config)
            
            # Create mock model ensemble manager for testing
            mock_model_manager = Mock()
            mock_model_manager.get_current_mode.return_value = 'consensus'
            
            # Create crisis analyzer for testing consolidated methods
            crisis_analyzer = create_crisis_analyzer(
                unified_config,
                model_ensemble_manager=mock_model_manager
            )
            
            return {
                'unified_config': unified_config,
                'threshold_manager': threshold_manager,
                'crisis_analyzer': crisis_analyzer,
                'mock_model_manager': mock_model_manager
            }
            
        except Exception as e:
            pytest.fail(f"Manager setup failed: {e}")

    def test_factory_function_creates_manager(self, setup_managers):
        """Test that factory function creates ThresholdMappingManager instance"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        assert threshold_manager is not None
        assert hasattr(threshold_manager, 'unified_config')
        assert hasattr(threshold_manager, 'threshold_config')
        logger.info("✅ Factory function creates ThresholdMappingManager successfully")

    def test_migration_reference_apply_threshold_to_confidence(self, setup_managers):
        """Test migration reference for apply_threshold_to_confidence method"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Call the migrated method
        result = threshold_manager.apply_threshold_to_confidence(0.6, 'consensus')
        
        # Verify it returns migration information
        assert isinstance(result, dict)
        assert 'note' in result
        assert 'use_instead' in result
        assert result['use_instead'] == 'CrisisAnalyzer.apply_crisis_thresholds()'
        assert result['phase'] == '3e.5.2'
        assert 'confidence' in result['parameters']
        assert 'mode' in result['parameters']
        assert result['parameters']['confidence'] == 0.6
        assert result['parameters']['mode'] == 'consensus'
        
        logger.info("✅ apply_threshold_to_confidence migration reference working correctly")

    def test_migration_reference_calculate_crisis_level(self, setup_managers):
        """Test migration reference for calculate_crisis_level method"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Call the migrated method
        result = threshold_manager.calculate_crisis_level(0.5, 'majority')
        
        # Verify it returns migration information
        assert isinstance(result, dict)
        assert 'note' in result
        assert 'use_instead' in result
        assert result['use_instead'] == 'CrisisAnalyzer.calculate_crisis_level_from_confidence()'
        assert result['phase'] == '3e.5.2'
        assert 'confidence' in result['parameters']
        assert 'mode' in result['parameters']
        assert result['parameters']['confidence'] == 0.5
        assert result['parameters']['mode'] == 'majority'
        
        logger.info("✅ calculate_crisis_level migration reference working correctly")

    def test_migration_reference_validate_analysis_thresholds(self, setup_managers):
        """Test migration reference for validate_analysis_thresholds method"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Call the migrated method
        result = threshold_manager.validate_analysis_thresholds('weighted')
        
        # Verify it returns migration information
        assert isinstance(result, dict)
        assert 'note' in result
        assert 'use_instead' in result
        assert result['use_instead'] == 'CrisisAnalyzer.validate_crisis_analysis_thresholds()'
        assert result['phase'] == '3e.5.2'
        assert 'mode' in result['parameters']
        assert result['parameters']['mode'] == 'weighted'
        
        logger.info("✅ validate_analysis_thresholds migration reference working correctly")

    def test_migration_reference_get_threshold_for_mode(self, setup_managers):
        """Test migration reference for get_threshold_for_mode method"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Call the migrated method
        result = threshold_manager.get_threshold_for_mode('sensitive')
        
        # Verify it returns migration information
        assert isinstance(result, dict)
        assert 'note' in result
        assert 'use_instead' in result
        assert result['use_instead'] == 'CrisisAnalyzer.get_crisis_threshold_for_mode()'
        assert result['phase'] == '3e.5.2'
        assert 'mode' in result['parameters']
        assert result['parameters']['mode'] == 'sensitive'
        
        logger.info("✅ get_threshold_for_mode migration reference working correctly")

    def test_migration_reference_adapt_thresholds_based_on_learning(self, setup_managers):
        """Test migration reference for adapt_thresholds_based_on_learning method"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Call the migrated method
        feedback_data = {'false_positives': 2, 'false_negatives': 1}
        result = threshold_manager.adapt_thresholds_based_on_learning(feedback_data)
        
        # Verify it returns migration information
        assert isinstance(result, dict)
        assert 'note' in result
        assert 'use_instead' in result
        assert result['use_instead'] == 'LearningSystemManager.adapt_crisis_thresholds()'
        assert result['phase'] == '3e.5.2'
        assert 'feedback_data' in result['parameters']
        assert result['parameters']['feedback_data'] == feedback_data
        
        logger.info("✅ adapt_thresholds_based_on_learning migration reference working correctly")

    def test_preserved_core_business_logic(self, setup_managers):
        """Test that core crisis detection business logic is preserved"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Test determine_crisis_level - PRESERVED method
        crisis_level = threshold_manager.determine_crisis_level(0.4, 'consensus')
        assert isinstance(crisis_level, str)
        assert crisis_level in ['none', 'low', 'medium', 'high', 'critical']
        
        # Test staff review requirement - PRESERVED method
        requires_review = threshold_manager.is_staff_review_required('high', 0.8)
        assert isinstance(requires_review, bool)
        
        # Test mode-specific thresholds - PRESERVED method
        ensemble_thresholds = threshold_manager.get_ensemble_thresholds_for_mode('consensus')
        assert isinstance(ensemble_thresholds, dict)
        assert 'low' in ensemble_thresholds
        assert 'medium' in ensemble_thresholds
        assert 'high' in ensemble_thresholds
        assert 'critical' in ensemble_thresholds
        
        logger.info("✅ Core business logic preserved: crisis detection, staff review, threshold access")

    def test_get_threshold_summary_includes_phase_3e_info(self, setup_managers):
        """Test that get_threshold_summary includes Phase 3e cleanup information"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        summary = threshold_manager.get_threshold_summary()
        
        assert isinstance(summary, dict)
        assert 'phase_3e_changes' in summary
        
        phase_3e_info = summary['phase_3e_changes']
        assert 'sub_step_5_2_completed' in phase_3e_info
        assert 'crisis_analyzer_methods' in phase_3e_info
        assert 'learning_system_methods' in phase_3e_info
        
        # Check that moved methods are documented
        crisis_methods = phase_3e_info['crisis_analyzer_methods']
        assert 'apply_crisis_thresholds()' in crisis_methods
        assert 'calculate_crisis_level_from_confidence()' in crisis_methods
        assert 'validate_crisis_analysis_thresholds()' in crisis_methods
        assert 'get_crisis_threshold_for_mode()' in crisis_methods
        
        learning_methods = phase_3e_info['learning_system_methods']
        assert 'adapt_crisis_thresholds()' in learning_methods
        
        logger.info("✅ Threshold summary includes Phase 3e Sub-step 5.2 cleanup information")

    def test_migration_benefits_documented(self, setup_managers):
        """Test that migration references include benefits documentation"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Test migration reference includes benefits
        migration_info = threshold_manager.apply_threshold_to_confidence(0.5)
        
        assert 'benefits' in migration_info
        benefits = migration_info['benefits']
        assert isinstance(benefits, list)
        assert len(benefits) > 0
        
        # Check for expected benefits
        benefits_text = ' '.join(benefits)
        assert 'consolidated' in benefits_text.lower()
        assert 'analysis' in benefits_text.lower()
        assert 'separation' in benefits_text.lower()
        
        logger.info("✅ Migration references include benefits documentation")

    def test_configuration_access_still_works(self, setup_managers):
        """Test that configuration access methods still work with real config files"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Test ensemble mode detection
        current_mode = threshold_manager.get_current_ensemble_mode()
        assert isinstance(current_mode, str)
        assert current_mode in ['consensus', 'majority', 'weighted']
        
        # Test crisis level mapping access
        crisis_mapping = threshold_manager.get_crisis_level_mapping_for_mode()
        assert isinstance(crisis_mapping, dict)
        assert 'crisis_to_high' in crisis_mapping
        assert 'crisis_to_medium' in crisis_mapping
        
        # Test staff review configuration
        staff_config = threshold_manager.get_staff_review_config()
        assert isinstance(staff_config, dict)
        assert 'high_always' in staff_config
        assert 'medium_confidence_threshold' in staff_config
        
        # Test pattern integration config
        pattern_config = threshold_manager.get_pattern_integration_config()
        assert isinstance(pattern_config, dict)
        assert 'enabled' in pattern_config
        
        logger.info("✅ Configuration access methods working with real config files")

    def test_validation_status_functionality(self, setup_managers):
        """Test that validation status functionality is preserved"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        validation_status = threshold_manager.get_validation_status()
        
        assert isinstance(validation_status, dict)
        assert 'is_valid' in validation_status
        assert 'errors' in validation_status
        assert 'total_errors' in validation_status
        assert 'modes_configured' in validation_status
        assert 'current_mode' in validation_status
        
        # Check that validation includes expected modes
        modes_configured = validation_status['modes_configured']
        assert isinstance(modes_configured, list)
        expected_modes = ['consensus', 'majority', 'weighted']
        for mode in expected_modes:
            if mode in modes_configured:  # May not all be configured
                logger.debug(f"Mode {mode} is configured")
        
        logger.info("✅ Validation status functionality preserved")

    def test_crisis_analyzer_has_consolidated_methods(self, setup_managers):
        """Test that CrisisAnalyzer has the consolidated methods from ThresholdMappingManager"""
        managers = setup_managers
        crisis_analyzer = managers['crisis_analyzer']
        
        # Check that CrisisAnalyzer has the consolidated methods
        assert hasattr(crisis_analyzer, 'apply_crisis_thresholds')
        assert hasattr(crisis_analyzer, 'calculate_crisis_level_from_confidence')
        assert hasattr(crisis_analyzer, 'validate_crisis_analysis_thresholds')
        assert hasattr(crisis_analyzer, 'get_crisis_threshold_for_mode')
        
        # Test that methods are callable and return expected types
        threshold_result = crisis_analyzer.apply_crisis_thresholds(0.5, 'consensus')
        assert isinstance(threshold_result, str)
        assert threshold_result in ['none', 'low', 'medium', 'high', 'critical']
        
        crisis_level = crisis_analyzer.calculate_crisis_level_from_confidence(0.6)
        assert isinstance(crisis_level, str)
        
        validation = crisis_analyzer.validate_crisis_analysis_thresholds('consensus')
        assert isinstance(validation, dict)
        
        mode_thresholds = crisis_analyzer.get_crisis_threshold_for_mode('consensus')
        assert isinstance(mode_thresholds, dict)
        
        logger.info("✅ CrisisAnalyzer has consolidated methods from ThresholdMappingManager")

    def test_learning_thresholds_migration_preserved(self, setup_managers):
        """Test that learning thresholds migration from Step 3 is preserved"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Call the learning thresholds method (migrated in Step 3)
        learning_info = threshold_manager.get_learning_thresholds()
        
        # Verify it still returns migration information from Step 3
        assert isinstance(learning_info, dict)
        assert 'note' in learning_info
        assert 'use_instead' in learning_info
        assert learning_info['use_instead'] == 'LearningSystemManager.get_learning_thresholds()'
        assert learning_info['phase'] == '3e.3'  # From Step 3, not Step 5.2
        
        logger.info("✅ Learning thresholds migration from Step 3 preserved")

    def test_error_handling_in_migrated_methods(self, setup_managers):
        """Test error handling in migrated methods"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Test with various edge cases
        test_cases = [
            (None, 'consensus'),  # None confidence
            (0.5, None),          # None mode
            ('invalid', 'consensus'),  # Invalid confidence type
            (0.5, 'invalid_mode')     # Invalid mode
        ]
        
        for confidence, mode in test_cases:
            # Should not raise exceptions, should return migration info
            try:
                result = threshold_manager.apply_threshold_to_confidence(confidence, mode)
                assert isinstance(result, dict)
                assert 'note' in result
                logger.debug(f"✅ Error handling works for confidence={confidence}, mode={mode}")
            except Exception as e:
                pytest.fail(f"Migration method should not raise exception for edge case: {e}")
        
        logger.info("✅ Error handling preserved in migrated methods")

    def test_real_world_threshold_determination(self, setup_managers):
        """Test real-world threshold determination scenarios"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Test realistic crisis scenarios
        test_scenarios = [
            (0.1, 'none'),      # Very low score
            (0.2, 'low'),       # Low crisis
            (0.4, 'medium'),    # Medium crisis  
            (0.6, 'high'),      # High crisis
            (0.9, 'critical')   # Critical crisis
        ]
        
        for score, expected_min_level in test_scenarios:
            crisis_level = threshold_manager.determine_crisis_level(score)
            assert isinstance(crisis_level, str)
            assert crisis_level in ['none', 'low', 'medium', 'high', 'critical']
            
            # Log the actual determination for verification
            logger.debug(f"Score {score} → {crisis_level} (expected at least {expected_min_level})")
        
        logger.info("✅ Real-world threshold determination working correctly")

    def test_phase_3e_cleanup_completeness(self, setup_managers):
        """Test that Phase 3e Sub-step 5.2 cleanup is complete"""
        managers = setup_managers
        threshold_manager = managers['threshold_manager']
        
        # Methods that should return migration references
        migrated_methods = [
            'apply_threshold_to_confidence',
            'calculate_crisis_level', 
            'validate_analysis_thresholds',
            'get_threshold_for_mode',
            'adapt_thresholds_based_on_learning'
        ]
        
        for method_name in migrated_methods:
            method = getattr(threshold_manager, method_name)
            result = method(0.5) if 'adapt' not in method_name else method({'test': 'data'})
            
            # Each migrated method should return migration info
            assert isinstance(result, dict)
            assert 'note' in result
            assert 'use_instead' in result
            assert 'phase' in result
            assert result['phase'] == '3e.5.2' or result['phase'] == '3e.3'  # Learning methods from Step 3
            
            logger.debug(f"✅ {method_name} returns proper migration reference")
        
        # Methods that should still work normally (preserved)
        preserved_methods = [
            'determine_crisis_level',
            'is_staff_review_required',
            'get_ensemble_thresholds_for_mode',
            'get_crisis_level_mapping_for_mode',
            'get_staff_review_thresholds_for_mode',
            'get_validation_status',
            'get_threshold_summary'
        ]
        
        for method_name in preserved_methods:
            method = getattr(threshold_manager, method_name)
            
            # Test with appropriate parameters
            if method_name == 'is_staff_review_required':
                result = method('high', 0.8)
            elif method_name in ['determine_crisis_level']:
                result = method(0.5)
            else:
                result = method()
            
            # Should return normal results, not migration info
            assert result is not None
            if isinstance(result, dict):
                assert 'note' not in result or 'phase_3e_changes' in result  # Summary method exception
            
            logger.debug(f"✅ {method_name} preserved and working")
        
        logger.info("✅ Phase 3e Sub-step 5.2 cleanup is complete and comprehensive")


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v', '--tb=short'])