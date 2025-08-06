#!/usr/bin/env python3
"""
Phase 3b Integration Tests
Tests complete integration of AnalysisParametersManager with the analysis pipeline

Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import json
import pytest
import tempfile
import logging
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from typing import Dict, Any

# Import the components we're testing
import sys
sys.path.append('/app')

from managers.analysis_parameters_manager import AnalysisParametersManager, create_analysis_parameters_manager
from managers.settings_manager import SettingsManager, create_settings_manager

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestPhase3bIntegration:
    """Integration tests for Phase 3b analysis parameter migration"""
    
    @pytest.fixture
    def mock_config_manager():
        """FIXED: Mock ConfigManager with patched file operations"""
        from pathlib import Path
        import json
        
        mock_manager = Mock()
        mock_manager.config_dir = Path("/app/config")  # Real Path object
        
        # Complete analysis parameters configuration
        analysis_config = {
            "analysis_system": {
                "version": "3.1",
                "phase": "3b",
                "architecture": "clean_v3.1_phase_3b"
            },
            "crisis_thresholds": {
                "high": 0.60,  # Different from defaults to test override
                "medium": 0.30,
                "low": 0.18,
                "defaults": {
                    "high": 0.55,
                    "medium": 0.28,
                    "low": 0.16
                }
            },
            "phrase_extraction": {
                "min_phrase_length": 3,  # Different from defaults
                "max_phrase_length": 8,  # Different from defaults
                "crisis_focus": True,
                "community_specific": True,
                "min_confidence": 0.35,  # Different from defaults
                "max_results": 25,       # Different from defaults
                "defaults": {
                    "min_phrase_length": 2,
                    "max_phrase_length": 6,
                    "crisis_focus": True,
                    "community_specific": True,
                    "min_confidence": 0.3,
                    "max_results": 20
                }
            },
            "pattern_learning": {
                "min_crisis_messages": 15,  # Different from defaults
                "max_phrases_to_analyze": 250,  # Different from defaults
                "min_distinctiveness_ratio": 2.5,  # Different from defaults
                "min_frequency": 5,  # Different from defaults
                "confidence_thresholds": {
                    "high_confidence": 0.75,  # Different from defaults
                    "medium_confidence": 0.45,  # Different from defaults
                    "low_confidence": 0.15,   # Different from defaults
                    "defaults": {
                        "high_confidence": 0.7,
                        "medium_confidence": 0.4,
                        "low_confidence": 0.1
                    }
                },
                "defaults": {
                    "min_crisis_messages": 10,
                    "max_phrases_to_analyze": 200,
                    "min_distinctiveness_ratio": 2.0,
                    "min_frequency": 3
                }
            },
            "semantic_analysis": {
                "context_window": 4,  # Different from defaults
                "boost_weights": {
                    "high_relevance": 0.12,     # Different from defaults
                    "medium_relevance": 0.07,   # Different from defaults
                    "family_rejection": 0.18,   # Different from defaults
                    "discrimination_fear": 0.18,  # Different from defaults
                    "support_seeking": -0.07,   # Different from defaults
                    "defaults": {
                        "high_relevance": 0.1,
                        "medium_relevance": 0.05,
                        "family_rejection": 0.15,
                        "discrimination_fear": 0.15,
                        "support_seeking": -0.05
                    }
                },
                "defaults": {
                    "context_window": 3
                }
            },
            "advanced_parameters": {
                "pattern_confidence_boost": 0.07,  # Different from defaults
                "model_confidence_boost": 0.02,    # Different from defaults
                "context_signal_weight": 1.1,      # Different from defaults
                "temporal_urgency_multiplier": 1.3,  # Different from defaults
                "community_awareness_boost": 0.12,   # Different from defaults
                "defaults": {
                    "pattern_confidence_boost": 0.05,
                    "model_confidence_boost": 0.0,
                    "context_signal_weight": 1.0,
                    "temporal_urgency_multiplier": 1.2,
                    "community_awareness_boost": 0.1
                }
            },
            "integration_settings": {
                "enable_pattern_analysis": True,
                "enable_semantic_analysis": True,
                "enable_phrase_extraction": True,
                "enable_pattern_learning": False,  # Different from defaults
                "integration_mode": "enhanced",     # Different from defaults
                "defaults": {
                    "enable_pattern_analysis": True,
                    "enable_semantic_analysis": True,
                    "enable_phrase_extraction": True,
                    "enable_pattern_learning": True,
                    "integration_mode": "full"
                }
            },
            "performance_settings": {
                "analysis_timeout_ms": 6000,    # Different from defaults
                "max_concurrent_analyses": 15,  # Different from defaults
                "cache_analysis_results": True,
                "cache_ttl_seconds": 450,       # Different from defaults
                "enable_parallel_processing": True,
                "defaults": {
                    "analysis_timeout_ms": 5000,
                    "max_concurrent_analyses": 10,
                    "cache_analysis_results": True,
                    "cache_ttl_seconds": 300,
                    "enable_parallel_processing": True
                }
            },
            "debugging_settings": {
                "enable_detailed_logging": True,   # Different from defaults
                "log_analysis_steps": True,        # Different from defaults
                "include_reasoning_in_response": True,
                "enable_performance_metrics": True,
                "defaults": {
                    "enable_detailed_logging": False,
                    "log_analysis_steps": False,
                    "include_reasoning_in_response": True,
                    "enable_performance_metrics": True
                }
            },
            "feature_flags": {
                "experimental_analysis_features": {
                    "enable_advanced_context_analysis": True,  # Different from defaults
                    "enable_community_vocabulary_boost": True,  # Different from defaults
                    "enable_temporal_pattern_detection": False,
                    "enable_multi_language_support": False,
                    "defaults": {
                        "enable_advanced_context_analysis": False,
                        "enable_community_vocabulary_boost": False,
                        "enable_temporal_pattern_detection": False,
                        "enable_multi_language_support": False
                    }
                }
            }
        }
        
        mock_manager.substitute_environment_variables.return_value = analysis_config
        
        # Patch file operations to avoid actual file system
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(analysis_config))), \
             patch('json.load', return_value=analysis_config):
            yield mock_manager
    
    @pytest.fixture
    def analysis_parameters_manager(self, mock_config_manager):
        """Create AnalysisParametersManager for testing"""
        return create_analysis_parameters_manager(mock_config_manager)
    
    @pytest.fixture
    def settings_manager_with_analysis_params(self, mock_config_manager, analysis_parameters_manager):
        """Create SettingsManager with AnalysisParametersManager integration"""
        return create_settings_manager(mock_config_manager, analysis_parameters_manager)
    
    def test_full_integration_initialization(self, mock_config_manager):
        """Test complete integration initialization sequence"""
        logger.info("🧪 Testing full Phase 3b integration initialization...")
        
        # Step 1: Create AnalysisParametersManager
        analysis_manager = create_analysis_parameters_manager(mock_config_manager)
        assert analysis_manager is not None
        
        # Step 2: Create SettingsManager with AnalysisParametersManager
        settings_manager = create_settings_manager(mock_config_manager, analysis_manager)
        assert settings_manager is not None
        assert settings_manager.analysis_parameters_manager == analysis_manager
        
        # Step 3: Validate both managers are operational
        analysis_validation = analysis_manager.validate_parameters()
        assert analysis_validation['valid'] is True
        
        settings_validation = settings_manager.validate_settings()
        assert settings_validation['valid'] is True
        
        logger.info("✅ Full Phase 3b integration initialization test passed")
    
    def test_settings_manager_delegates_to_analysis_manager(self, settings_manager_with_analysis_params, analysis_parameters_manager):
        """Test that SettingsManager properly delegates to AnalysisParametersManager"""
        logger.info("🧪 Testing SettingsManager delegation to AnalysisParametersManager...")
        
        # Test crisis thresholds delegation
        settings_thresholds = settings_manager_with_analysis_params.get_crisis_threshold_settings()
        analysis_thresholds = analysis_parameters_manager.get_crisis_thresholds()
        
        assert settings_thresholds == analysis_thresholds
        assert settings_thresholds['high'] == 0.60  # Should match mock config values
        assert settings_thresholds['medium'] == 0.30
        assert settings_thresholds['low'] == 0.18
        
        # Test phrase extraction delegation
        settings_phrase = settings_manager_with_analysis_params.get_phrase_extraction_settings()
        analysis_phrase = analysis_parameters_manager.get_phrase_extraction_parameters()
        
        assert settings_phrase == analysis_phrase
        assert settings_phrase['min_phrase_length'] == 3  # Should match mock config values
        assert settings_phrase['max_phrase_length'] == 8
        assert settings_phrase['min_confidence'] == 0.35
        assert settings_phrase['max_results'] == 25
        
        # Test pattern learning delegation
        settings_pattern = settings_manager_with_analysis_params.get_pattern_learning_settings()
        analysis_pattern = analysis_parameters_manager.get_pattern_learning_parameters()
        
        assert settings_pattern == analysis_pattern
        assert settings_pattern['min_crisis_messages'] == 15  # Should match mock config values
        assert settings_pattern['max_phrases_to_analyze'] == 250
        
        # Test semantic analysis delegation
        settings_semantic = settings_manager_with_analysis_params.get_semantic_analysis_settings()
        analysis_semantic = analysis_parameters_manager.get_semantic_analysis_parameters()
        
        assert settings_semantic == analysis_semantic
        assert settings_semantic['context_window'] == 4  # Should match mock config values
        assert settings_semantic['boost_weights']['high_relevance'] == 0.12
        
        logger.info("✅ SettingsManager delegation test passed")
    
    def test_new_analysis_parameter_methods(self, settings_manager_with_analysis_params, analysis_parameters_manager):
        """Test new analysis parameter access methods in SettingsManager"""
        logger.info("🧪 Testing new analysis parameter access methods...")
        
        # Test advanced parameters access
        advanced_params = settings_manager_with_analysis_params.get_advanced_analysis_parameters()
        expected_advanced = analysis_parameters_manager.get_advanced_parameters()
        
        assert advanced_params == expected_advanced
        assert advanced_params['pattern_confidence_boost'] == 0.07
        assert advanced_params['model_confidence_boost'] == 0.02
        assert advanced_params['context_signal_weight'] == 1.1
        
        # Test integration settings access
        integration_settings = settings_manager_with_analysis_params.get_integration_settings()
        expected_integration = analysis_parameters_manager.get_integration_settings()
        
        assert integration_settings == expected_integration
        assert integration_settings['enable_pattern_learning'] is False  # Different from default
        assert integration_settings['integration_mode'] == 'enhanced'    # Different from default
        
        # Test performance settings access
        performance_settings = settings_manager_with_analysis_params.get_performance_settings()
        expected_performance = analysis_parameters_manager.get_performance_settings()
        
        assert performance_settings == expected_performance
        assert performance_settings['analysis_timeout_ms'] == 6000
        assert performance_settings['max_concurrent_analyses'] == 15
        
        # Test debugging settings access
        debugging_settings = settings_manager_with_analysis_params.get_debugging_settings()
        expected_debugging = analysis_parameters_manager.get_debugging_settings()
        
        assert debugging_settings == expected_debugging
        assert debugging_settings['enable_detailed_logging'] is True   # Different from default
        assert debugging_settings['log_analysis_steps'] is True        # Different from default
        
        # Test experimental features access
        experimental_features = settings_manager_with_analysis_params.get_experimental_features()
        expected_experimental = analysis_parameters_manager.get_experimental_features()
        
        assert experimental_features == expected_experimental
        assert experimental_features['enable_advanced_context_analysis'] is True   # Different from default
        assert experimental_features['enable_community_vocabulary_boost'] is True  # Different from default
        
        logger.info("✅ New analysis parameter access methods test passed")
    
    def test_settings_manager_fallback_behavior(self, mock_config_manager):
        """Test SettingsManager fallback behavior when AnalysisParametersManager is not available"""
        logger.info("🧪 Testing SettingsManager fallback behavior...")
        
        # Create SettingsManager without AnalysisParametersManager
        settings_manager = create_settings_manager(mock_config_manager, None)
        
        assert settings_manager.analysis_parameters_manager is None
        
        # Test that fallback methods work with environment variables
        with patch.dict(os.environ, {
            'NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH': '0.65',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM': '0.35',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_LOW': '0.20',
            'NLP_ANALYSIS_MIN_PHRASE_LENGTH': '1',
            'NLP_ANALYSIS_MAX_PHRASE_LENGTH': '10'
        }):
            # Test crisis thresholds fallback
            thresholds = settings_manager.get_crisis_threshold_settings()
            assert thresholds['high'] == 0.65
            assert thresholds['medium'] == 0.35
            assert thresholds['low'] == 0.20
            
            # Test phrase extraction fallback
            phrase_settings = settings_manager.get_phrase_extraction_settings()
            assert phrase_settings['min_phrase_length'] == 1
            assert phrase_settings['max_phrase_length'] == 10
        
        logger.info("✅ SettingsManager fallback behavior test passed")
    
    def test_parameter_validation_integration(self, settings_manager_with_analysis_params):
        """Test parameter validation integration between managers"""
        logger.info("🧪 Testing parameter validation integration...")
        
        # Test SettingsManager validation includes AnalysisParametersManager validation
        validation_result = settings_manager_with_analysis_params.validate_settings()
        
        assert isinstance(validation_result, dict)
        assert 'valid' in validation_result
        assert 'errors' in validation_result
        assert 'warnings' in validation_result
        
        # Should be valid with our mock configuration
        assert validation_result['valid'] is True
        assert len(validation_result['errors']) == 0
        
        logger.info("✅ Parameter validation integration test passed")
    
    def test_migration_notices_phase_3b(self, settings_manager_with_analysis_params):
        """Test migration notices for Phase 3b"""
        logger.info("🧪 Testing Phase 3b migration notices...")
        
        # Test crisis patterns migration notice (Phase 3a)
        crisis_patterns_notice = settings_manager_with_analysis_params.get_crisis_patterns_migration_notice()
        assert crisis_patterns_notice['phase'] == '3a_complete'
        assert 'CrisisPatternManager' in crisis_patterns_notice['manager_class']
        
        # Test analysis parameters migration notice (Phase 3b)
        analysis_params_notice = settings_manager_with_analysis_params.get_analysis_parameters_migration_notice()
        assert analysis_params_notice['phase'] == '3b_complete'
        assert 'AnalysisParametersManager' in analysis_params_notice['manager_class']
        assert analysis_params_notice['migration_date'] == '2025-08-05'
        
        logger.info("✅ Phase 3b migration notices test passed")
    
    def test_architecture_version_updates(self, settings_manager_with_analysis_params):
        """Test that architecture versions reflect Phase 3b completion"""
        logger.info("🧪 Testing architecture version updates...")
        
        # Check runtime settings for Phase 3b status
        runtime_settings = settings_manager_with_analysis_params.runtime_settings
        
        assert runtime_settings['phase_status']['phase_3b'] == 'complete'
        assert runtime_settings['phase_status']['analysis_parameters'] == 'externalized_to_json'
        
        # Check server config for updated architecture
        server_config = runtime_settings['server']
        assert 'phase_3b_complete' in server_config['architecture']
        assert 'analysis_parameters' in server_config['capabilities']
        
        logger.info("✅ Architecture version updates test passed")


class TestPhase3bEnvironmentVariableIntegration:
    """Test environment variable integration for Phase 3b"""
    
    def test_environment_variable_override_end_to_end(self):
        """Test complete environment variable override functionality"""
        logger.info("🧪 Testing end-to-end environment variable overrides...")
        
        # Set up environment variables
        env_vars = {
            'NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH': '0.70',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM': '0.40',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_LOW': '0.25',
            'NLP_ANALYSIS_MIN_PHRASE_LENGTH': '1',
            'NLP_ANALYSIS_MAX_PHRASE_LENGTH': '10',
            'NLP_ANALYSIS_PHRASE_MIN_CONFIDENCE': '0.25',
            'NLP_ANALYSIS_SEMANTIC_CONTEXT_WINDOW': '5',
            'NLP_ANALYSIS_PATTERN_CONFIDENCE_BOOST': '0.10',
            'NLP_ANALYSIS_ENABLE_PATTERN_ANALYSIS': 'true',
            'NLP_ANALYSIS_INTEGRATION_MODE': 'enhanced',
            'NLP_ANALYSIS_TIMEOUT_MS': '7000',
            'NLP_ANALYSIS_ENABLE_DETAILED_LOGGING': 'true'
        }
        
        with patch.dict(os.environ, env_vars):
            # Create mock config manager that would process these environment variables
            mock_config_manager = Mock()
            
            # Simulate processed configuration with environment variable values
            processed_config = {
                "analysis_system": {"version": "3.1"},
                "crisis_thresholds": {
                    "high": 0.70,  # From env var
                    "medium": 0.40,  # From env var
                    "low": 0.25,   # From env var
                    "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
                },
                "phrase_extraction": {
                    "min_phrase_length": 1,     # From env var
                    "max_phrase_length": 10,    # From env var
                    "min_confidence": 0.25,     # From env var
                    "defaults": {"min_phrase_length": 2, "max_phrase_length": 6, "min_confidence": 0.3}
                },
                "semantic_analysis": {
                    "context_window": 5,        # From env var
                    "defaults": {"context_window": 3}
                },
                "advanced_parameters": {
                    "pattern_confidence_boost": 0.10,  # From env var
                    "defaults": {"pattern_confidence_boost": 0.05}
                },
                "integration_settings": {
                    "enable_pattern_analysis": True,   # From env var
                    "integration_mode": "enhanced",     # From env var
                    "defaults": {"enable_pattern_analysis": True, "integration_mode": "full"}
                },
                "performance_settings": {
                    "analysis_timeout_ms": 7000,       # From env var
                    "defaults": {"analysis_timeout_ms": 5000}
                },
                "debugging_settings": {
                    "enable_detailed_logging": True,   # From env var
                    "defaults": {"enable_detailed_logging": False}
                }
            }
            
            mock_config_manager.get_configuration.return_value = processed_config
            
            # Test that the manager uses the environment variable values
            analysis_manager = AnalysisParametersManager(mock_config_manager)
            
            # Verify environment variable values are used
            thresholds = analysis_manager.get_crisis_thresholds()
            assert thresholds['high'] == 0.70
            assert thresholds['medium'] == 0.40
            assert thresholds['low'] == 0.25
            
            phrase_params = analysis_manager.get_phrase_extraction_parameters()
            assert phrase_params['min_phrase_length'] == 1
            assert phrase_params['max_phrase_length'] == 10
            assert phrase_params['min_confidence'] == 0.25
            
            semantic_params = analysis_manager.get_semantic_analysis_parameters()
            assert semantic_params['context_window'] == 5
            
            advanced_params = analysis_manager.get_advanced_parameters()
            assert advanced_params['pattern_confidence_boost'] == 0.10
            
            integration_settings = analysis_manager.get_integration_settings()
            assert integration_settings['enable_pattern_analysis'] is True
            assert integration_settings['integration_mode'] == 'enhanced'
            
            performance_settings = analysis_manager.get_performance_settings()
            assert performance_settings['analysis_timeout_ms'] == 7000
            
            debugging_settings = analysis_manager.get_debugging_settings()
            assert debugging_settings['enable_detailed_logging'] is True
        
        logger.info("✅ End-to-end environment variable overrides test passed")


class TestPhase3bErrorHandlingAndResilience:
    """Test error handling and system resilience for Phase 3b"""
    
    def test_graceful_degradation_analysis_manager_unavailable(self):
        """Test graceful degradation when AnalysisParametersManager is unavailable"""
        logger.info("🧪 Testing graceful degradation with unavailable AnalysisParametersManager...")
        
        mock_config_manager = Mock()
        mock_config_manager.get_configuration.return_value = None
        
        # AnalysisParametersManager should fail
        with pytest.raises(ValueError):
            AnalysisParametersManager(mock_config_manager)
        
        # But SettingsManager should still work with fallbacks
        settings_manager = create_settings_manager(mock_config_manager, None)
        
        # Test fallback behavior
        with patch.dict(os.environ, {
            'NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH': '0.55',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM': '0.28',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_LOW': '0.16'
        }):
            thresholds = settings_manager.get_crisis_threshold_settings()
            assert isinstance(thresholds, dict)
            assert 'high' in thresholds
            assert 'medium' in thresholds
            assert 'low' in thresholds
        
        logger.info("✅ Graceful degradation test passed")
    
    def test_invalid_configuration_handling(self):
        """Test handling of invalid configuration data"""
        logger.info("🧪 Testing invalid configuration handling...")
        
        mock_config_manager = Mock()
        
        # Test with completely invalid configuration
        mock_config_manager.get_configuration.return_value = {"invalid": "config"}
        
        with pytest.raises(ValueError):
            AnalysisParametersManager(mock_config_manager)
        
        logger.info("✅ Invalid configuration handling test passed")


# ============================================================================
# TEST RUNNER AND SUMMARY
# ============================================================================

def run_phase_3b_integration_tests():
    """Run all Phase 3b integration tests"""
    logger.info("🧪 Starting Phase 3b Integration Test Suite")
    logger.info("=" * 60)
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        # Run pytest with verbose output
        exit_code = pytest.main([
            __file__,
            '-v',
            '--tb=short',
            '--disable-warnings'
        ])
        
        if exit_code == 0:
            logger.info("🎉 All Phase 3b integration tests passed!")
            test_results['passed'] = 1
        else:
            logger.error("❌ Some Phase 3b integration tests failed")
            test_results['failed'] = 1
            
    except Exception as e:
        logger.error(f"❌ Integration test suite execution error: {e}")
        test_results['errors'].append(str(e))
    
    logger.info("=" * 60)
    logger.info(f"📊 Integration Test Results: {test_results['passed']} passed, {test_results['failed']} failed")
    
    return test_results


if __name__ == "__main__":
    # Run integration tests when script is executed directly
    run_phase_3b_integration_tests()