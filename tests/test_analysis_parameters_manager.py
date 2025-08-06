#!/usr/bin/env python3
"""
Unit Tests for AnalysisParametersManager - Phase 3b
Tests JSON configuration loading, environment variable overrides, and parameter validation

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

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestAnalysisParametersManager:
    """Test suite for AnalysisParametersManager"""
    
    @pytest.fixture
    def mock_config_manager():
        """FIXED: Mock ConfigManager with patched file operations"""
        from pathlib import Path
        import json
        
        mock_manager = Mock()
        mock_manager.config_dir = Path("/app/config")  # Real Path object
        
        # Mock valid analysis parameters configuration
        mock_config = {
            "analysis_system": {
                "version": "3.1",
                "phase": "3b",
                "architecture": "clean_v3.1_phase_3b"
            },
            "crisis_thresholds": {
                "high": 0.55,
                "medium": 0.28,
                "low": 0.16,
                "defaults": {
                    "high": 0.55,
                    "medium": 0.28,
                    "low": 0.16
                }
            },
            "phrase_extraction": {
                "min_phrase_length": 2,
                "max_phrase_length": 6,
                "crisis_focus": True,
                "community_specific": True,
                "min_confidence": 0.3,
                "max_results": 20,
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
                "min_crisis_messages": 10,
                "max_phrases_to_analyze": 200,
                "min_distinctiveness_ratio": 2.0,
                "min_frequency": 3,
                "confidence_thresholds": {
                    "high_confidence": 0.7,
                    "medium_confidence": 0.4,
                    "low_confidence": 0.1,
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
                "context_window": 3,
                "boost_weights": {
                    "high_relevance": 0.1,
                    "medium_relevance": 0.05,
                    "family_rejection": 0.15,
                    "discrimination_fear": 0.15,
                    "support_seeking": -0.05,
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
                "pattern_confidence_boost": 0.05,
                "model_confidence_boost": 0.0,
                "context_signal_weight": 1.0,
                "temporal_urgency_multiplier": 1.2,
                "community_awareness_boost": 0.1,
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
                "enable_pattern_learning": True,
                "integration_mode": "full",
                "defaults": {
                    "enable_pattern_analysis": True,
                    "enable_semantic_analysis": True,
                    "enable_phrase_extraction": True,
                    "enable_pattern_learning": True,
                    "integration_mode": "full"
                }
            },
            "performance_settings": {
                "analysis_timeout_ms": 5000,
                "max_concurrent_analyses": 10,
                "cache_analysis_results": True,
                "cache_ttl_seconds": 300,
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
                "enable_detailed_logging": False,
                "log_analysis_steps": False,
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
                    "enable_advanced_context_analysis": False,
                    "enable_community_vocabulary_boost": False,
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
    def analysis_manager(self, mock_config_manager):
        """Create an AnalysisParametersManager instance for testing"""
        return AnalysisParametersManager(mock_config_manager)
    
    def test_initialization_success(self, mock_config_manager):
        """Test successful AnalysisParametersManager initialization"""
        logger.info("🧪 Testing AnalysisParametersManager initialization...")
        
        manager = AnalysisParametersManager(mock_config_manager)
        
        assert manager.config_manager == mock_config_manager
        assert manager.analysis_config is not None
        mock_config_manager.get_configuration.assert_called_with('analysis_parameters')
        
        logger.info("✅ AnalysisParametersManager initialization test passed")
    
    def test_initialization_failure_no_config(self):
        """Test AnalysisParametersManager initialization failure when no config available"""
        logger.info("🧪 Testing AnalysisParametersManager initialization failure...")
        
        mock_manager = Mock()
        mock_manager.get_configuration.return_value = None
        
        with pytest.raises(ValueError, match="Analysis parameters configuration not available"):
            AnalysisParametersManager(mock_manager)
        
        logger.info("✅ AnalysisParametersManager initialization failure test passed")
    
    def test_get_crisis_thresholds(self, analysis_manager):
        """Test crisis threshold retrieval"""
        logger.info("🧪 Testing crisis thresholds retrieval...")
        
        thresholds = analysis_manager.get_crisis_thresholds()
        
        assert isinstance(thresholds, dict)
        assert 'high' in thresholds
        assert 'medium' in thresholds
        assert 'low' in thresholds
        
        # Validate threshold values
        assert thresholds['high'] == 0.55
        assert thresholds['medium'] == 0.28
        assert thresholds['low'] == 0.16
        
        # Validate threshold ordering
        assert thresholds['high'] > thresholds['medium'] > thresholds['low']
        
        logger.info("✅ Crisis thresholds test passed")
    
    def test_get_phrase_extraction_parameters(self, analysis_manager):
        """Test phrase extraction parameters retrieval"""
        logger.info("🧪 Testing phrase extraction parameters...")
        
        params = analysis_manager.get_phrase_extraction_parameters()
        
        assert isinstance(params, dict)
        assert params['min_phrase_length'] == 2
        assert params['max_phrase_length'] == 6
        assert params['crisis_focus'] is True
        assert params['community_specific'] is True
        assert params['min_confidence'] == 0.3
        assert params['max_results'] == 20
        
        # Validate parameter constraints
        assert params['min_phrase_length'] < params['max_phrase_length']
        assert 0.0 <= params['min_confidence'] <= 1.0
        
        logger.info("✅ Phrase extraction parameters test passed")
    
    def test_get_pattern_learning_parameters(self, analysis_manager):
        """Test pattern learning parameters retrieval"""
        logger.info("🧪 Testing pattern learning parameters...")
        
        params = analysis_manager.get_pattern_learning_parameters()
        
        assert isinstance(params, dict)
        assert params['min_crisis_messages'] == 10
        assert params['max_phrases_to_analyze'] == 200
        assert params['min_distinctiveness_ratio'] == 2.0
        assert params['min_frequency'] == 3
        
        # Test confidence thresholds
        conf_thresholds = params['confidence_thresholds']
        assert conf_thresholds['high_confidence'] == 0.7
        assert conf_thresholds['medium_confidence'] == 0.4
        assert conf_thresholds['low_confidence'] == 0.1
        
        # Validate ordering
        assert conf_thresholds['high_confidence'] > conf_thresholds['medium_confidence'] > conf_thresholds['low_confidence']
        
        logger.info("✅ Pattern learning parameters test passed")
    
    def test_get_semantic_analysis_parameters(self, analysis_manager):
        """Test semantic analysis parameters retrieval"""
        logger.info("🧪 Testing semantic analysis parameters...")
        
        params = analysis_manager.get_semantic_analysis_parameters()
        
        assert isinstance(params, dict)
        assert params['context_window'] == 3
        
        # Test boost weights
        boost_weights = params['boost_weights']
        assert boost_weights['high_relevance'] == 0.1
        assert boost_weights['medium_relevance'] == 0.05
        assert boost_weights['family_rejection'] == 0.15
        assert boost_weights['discrimination_fear'] == 0.15
        assert boost_weights['support_seeking'] == -0.05
        
        # Validate support_seeking is negative (reduces crisis level)
        assert boost_weights['support_seeking'] < 0
        
        logger.info("✅ Semantic analysis parameters test passed")
    
    def test_get_advanced_parameters(self, analysis_manager):
        """Test advanced parameters retrieval"""
        logger.info("🧪 Testing advanced parameters...")
        
        params = analysis_manager.get_advanced_parameters()
        
        assert isinstance(params, dict)
        assert params['pattern_confidence_boost'] == 0.05
        assert params['model_confidence_boost'] == 0.0
        assert params['context_signal_weight'] == 1.0
        assert params['temporal_urgency_multiplier'] == 1.2
        assert params['community_awareness_boost'] == 0.1
        
        # Validate parameter ranges
        assert params['pattern_confidence_boost'] >= 0.0
        assert params['temporal_urgency_multiplier'] >= 1.0
        
        logger.info("✅ Advanced parameters test passed")
    
    def test_get_integration_settings(self, analysis_manager):
        """Test integration settings retrieval"""
        logger.info("🧪 Testing integration settings...")
        
        settings = analysis_manager.get_integration_settings()
        
        assert isinstance(settings, dict)
        assert settings['enable_pattern_analysis'] is True
        assert settings['enable_semantic_analysis'] is True
        assert settings['enable_phrase_extraction'] is True
        assert settings['enable_pattern_learning'] is True
        assert settings['integration_mode'] == 'full'
        
        logger.info("✅ Integration settings test passed")
    
    def test_get_performance_settings(self, analysis_manager):
        """Test performance settings retrieval"""
        logger.info("🧪 Testing performance settings...")
        
        settings = analysis_manager.get_performance_settings()
        
        assert isinstance(settings, dict)
        assert settings['analysis_timeout_ms'] == 5000
        assert settings['max_concurrent_analyses'] == 10
        assert settings['cache_analysis_results'] is True
        assert settings['cache_ttl_seconds'] == 300
        assert settings['enable_parallel_processing'] is True
        
        # Validate performance constraints
        assert settings['analysis_timeout_ms'] > 0
        assert settings['max_concurrent_analyses'] > 0
        assert settings['cache_ttl_seconds'] > 0
        
        logger.info("✅ Performance settings test passed")
    
    def test_get_debugging_settings(self, analysis_manager):
        """Test debugging settings retrieval"""
        logger.info("🧪 Testing debugging settings...")
        
        settings = analysis_manager.get_debugging_settings()
        
        assert isinstance(settings, dict)
        assert settings['enable_detailed_logging'] is False
        assert settings['log_analysis_steps'] is False
        assert settings['include_reasoning_in_response'] is True
        assert settings['enable_performance_metrics'] is True
        
        logger.info("✅ Debugging settings test passed")
    
    def test_get_experimental_features(self, analysis_manager):
        """Test experimental features retrieval"""
        logger.info("🧪 Testing experimental features...")
        
        features = analysis_manager.get_experimental_features()
        
        assert isinstance(features, dict)
        assert features['enable_advanced_context_analysis'] is False
        assert features['enable_community_vocabulary_boost'] is False
        assert features['enable_temporal_pattern_detection'] is False
        assert features['enable_multi_language_support'] is False
        
        logger.info("✅ Experimental features test passed")
    
    def test_get_all_parameters(self, analysis_manager):
        """Test getting all parameters at once"""
        logger.info("🧪 Testing get_all_parameters...")
        
        all_params = analysis_manager.get_all_parameters()
        
        assert isinstance(all_params, dict)
        expected_categories = [
            'crisis_thresholds',
            'phrase_extraction', 
            'pattern_learning',
            'semantic_analysis',
            'advanced_parameters',
            'integration_settings',
            'performance_settings',
            'debugging_settings',
            'experimental_features'
        ]
        
        for category in expected_categories:
            assert category in all_params
            assert isinstance(all_params[category], dict)
        
        logger.info("✅ Get all parameters test passed")
    
    def test_validate_parameters_success(self, analysis_manager):
        """Test parameter validation with valid parameters"""
        logger.info("🧪 Testing parameter validation - success case...")
        
        validation_result = analysis_manager.validate_parameters()
        
        assert isinstance(validation_result, dict)
        assert 'valid' in validation_result
        assert 'errors' in validation_result
        assert 'warnings' in validation_result
        
        assert validation_result['valid'] is True
        assert len(validation_result['errors']) == 0
        
        logger.info("✅ Parameter validation success test passed")
    
    def test_validate_parameters_invalid_thresholds(self, mock_config_manager):
        """Test parameter validation with invalid thresholds"""
        logger.info("🧪 Testing parameter validation - invalid thresholds...")
        
        # Create config with invalid thresholds (high < medium)
        invalid_config = mock_config_manager.get_configuration.return_value.copy()
        invalid_config['crisis_thresholds']['high'] = 0.2
        invalid_config['crisis_thresholds']['medium'] = 0.5
        invalid_config['crisis_thresholds']['low'] = 0.1
        
        mock_config_manager.get_configuration.return_value = invalid_config
        
        manager = AnalysisParametersManager(mock_config_manager)
        validation_result = manager.validate_parameters()
        
        assert validation_result['valid'] is False
        assert len(validation_result['errors']) > 0
        
        logger.info("✅ Parameter validation invalid thresholds test passed")
    
    def test_factory_function(self, mock_config_manager):
        """Test factory function for creating AnalysisParametersManager"""
        logger.info("🧪 Testing factory function...")
        
        manager = create_analysis_parameters_manager(mock_config_manager)
        
        assert isinstance(manager, AnalysisParametersManager)
        assert manager.config_manager == mock_config_manager
        
        logger.info("✅ Factory function test passed")
    
    def test_error_handling_missing_config_section(self, mock_config_manager):
        """Test error handling when configuration sections are missing"""
        logger.info("🧪 Testing error handling - missing config section...")
        
        # Remove a configuration section
        incomplete_config = mock_config_manager.get_configuration.return_value.copy()
        del incomplete_config['crisis_thresholds']
        
        mock_config_manager.get_configuration.return_value = incomplete_config
        
        manager = AnalysisParametersManager(mock_config_manager)
        
        # Should fallback to defaults gracefully
        thresholds = manager.get_crisis_thresholds()
        assert isinstance(thresholds, dict)
        assert 'high' in thresholds
        assert 'medium' in thresholds
        assert 'low' in thresholds
        
        logger.info("✅ Error handling missing config section test passed")


class TestAnalysisParametersManagerEnvironmentOverrides:
    """Test environment variable overrides for AnalysisParametersManager"""
    
    @pytest.fixture
    def mock_config_manager():
        """FIXED: Mock ConfigManager with patched file operations"""
        from pathlib import Path
        import json
        
        mock_manager = Mock()
        mock_manager.config_dir = Path("/app/config")  # Real Path object
        
        # Your analysis config here...
        analysis_config = { /* your config */ }
        
        # Configuration with environment variable placeholders
        mock_config = {
            "crisis_thresholds": {
                "high": "${NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH}",
                "medium": "${NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM}",
                "low": "${NLP_ANALYSIS_CRISIS_THRESHOLD_LOW}",
                "defaults": {
                    "high": 0.55,
                    "medium": 0.28,
                    "low": 0.16
                }
            },
            "phrase_extraction": {
                "min_phrase_length": "${NLP_ANALYSIS_MIN_PHRASE_LENGTH}",
                "max_phrase_length": "${NLP_ANALYSIS_MAX_PHRASE_LENGTH}",
                "defaults": {
                    "min_phrase_length": 2,
                    "max_phrase_length": 6
                }
            }
        }
        
        mock_manager.substitute_environment_variables.return_value = analysis_config
        
        # Patch file operations to avoid actual file system
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(analysis_config))), \
             patch('json.load', return_value=analysis_config):
            yield mock_manager
    
    def test_environment_variable_override_integration(self, mock_config_manager_with_env_vars):
        """Test that the manager can handle environment variable placeholders"""
        logger.info("🧪 Testing environment variable override integration...")
        
        # Note: The actual environment variable substitution happens in ConfigManager
        # This test validates that the manager can handle the structure
        manager = AnalysisParametersManager(mock_config_manager_with_env_vars)
        
        # The manager should initialize successfully even with env var placeholders
        assert manager.config_manager is not None
        
        logger.info("✅ Environment variable override integration test passed")


class TestAnalysisParametersManagerEdgeCases:
    """Test edge cases and error conditions for AnalysisParametersManager"""
    
    def test_parse_bool_method(self):
        """Test the _parse_bool utility method"""
        logger.info("🧪 Testing _parse_bool utility method...")
        
        # Create a manager instance for testing the utility method
        mock_manager = Mock()
        mock_manager.get_configuration.return_value = {"analysis_system": {}}
        
        manager = AnalysisParametersManager(mock_manager)
        
        # Test various boolean representations
        assert manager._parse_bool(True) is True
        assert manager._parse_bool(False) is False
        assert manager._parse_bool("true") is True
        assert manager._parse_bool("false") is False
        assert manager._parse_bool("1") is True
        assert manager._parse_bool("0") is False
        assert manager._parse_bool("yes") is True
        assert manager._parse_bool("no") is False
        assert manager._parse_bool("on") is True
        assert manager._parse_bool("off") is False
        assert manager._parse_bool(1) is True
        assert manager._parse_bool(0) is False
        
        logger.info("✅ _parse_bool utility method test passed")
    
    def test_fallback_to_defaults_on_error(self):
        """Test fallback to default values when configuration errors occur"""
        logger.info("🧪 Testing fallback to defaults on error...")
        
        mock_manager = Mock()
        # Simulate configuration error
        mock_manager.get_configuration.side_effect = Exception("Configuration error")
        
        with pytest.raises(ValueError):
            AnalysisParametersManager(mock_manager)
        
        logger.info("✅ Fallback to defaults on error test passed")


# ============================================================================
# TEST RUNNER AND SUMMARY
# ============================================================================

def run_all_tests():
    """Run all AnalysisParametersManager tests"""
    logger.info("🧪 Starting AnalysisParametersManager Test Suite - Phase 3b")
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
            logger.info("🎉 All AnalysisParametersManager tests passed!")
            test_results['passed'] = 1
        else:
            logger.error("❌ Some AnalysisParametersManager tests failed")
            test_results['failed'] = 1
            
    except Exception as e:
        logger.error(f"❌ Test suite execution error: {e}")
        test_results['errors'].append(str(e))
    
    logger.info("=" * 60)
    logger.info(f"📊 Test Results: {test_results['passed']} passed, {test_results['failed']} failed")
    
    return test_results


if __name__ == "__main__":
    # Run tests when script is executed directly
    run_all_tests()