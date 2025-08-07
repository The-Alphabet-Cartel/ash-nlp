#!/usr/bin/env python3
"""
Phase 3b Configuration Validation Tests
Tests JSON configuration loading, environment variable validation, and parameter validation

Repository: https://github.com/the-alphabet-cartel/ash-nlp
"""

import os
import json
import pytest
import tempfile
import logging
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
from typing import Dict, Any

# Import the components we're testing
import sys
sys.path.append('/app')

from managers.analysis_parameters_manager import AnalysisParametersManager
from managers.config_manager import ConfigManager

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestAnalysisParametersJSONValidation:
    """Test JSON configuration validation for analysis parameters"""
    
    def create_test_config_file(self, config_data: Dict[str, Any]) -> str:
        """Create a temporary JSON configuration file for testing"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(config_data, temp_file, indent=2)
        temp_file.close()
        return temp_file.name
    
    def test_valid_complete_configuration(self):
        """Test loading a complete, valid analysis parameters configuration"""
        logger.info("🧪 Testing valid complete configuration loading...")
        
        valid_config = {
            "analysis_system": {
                "version": "3.1",
                "phase": "3b",
                "description": "Analysis algorithm parameters for Ash NLP Service",
                "architecture": "clean_v3.1_phase_3b"
            },
            "crisis_thresholds": {
                "description": "Core crisis level mapping thresholds",
                "high": 0.55,
                "medium": 0.28,
                "low": 0.16,
                "defaults": {
                    "high": 0.55,
                    "medium": 0.28,
                    "low": 0.16
                },
                "validation": {
                    "range": {"min": 0.0, "max": 1.0},
                    "ordering": "high > medium > low"
                }
            },
            "phrase_extraction": {
                "description": "Parameters for crisis phrase extraction",
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
                "description": "Parameters for pattern learning",
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
                "description": "Parameters for semantic analysis",
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
                "description": "Advanced analysis parameters",
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
                "description": "Integration settings for analysis components",
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
                "description": "Performance-related parameters",
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
                "description": "Debugging and development parameters",
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
                "description": "Feature flags for experimental features",
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
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(valid_config))), \
             patch('json.load', return_value=valid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = valid_config
            
            # Test that AnalysisParametersManager can load this configuration
            manager = AnalysisParametersManager(mock_config_manager)
            
            # Verify all parameter categories are accessible
            assert manager.get_crisis_thresholds() is not None
            assert manager.get_phrase_extraction_parameters() is not None
            assert manager.get_pattern_learning_parameters() is not None
            assert manager.get_semantic_analysis_parameters() is not None
            assert manager.get_advanced_parameters() is not None
            assert manager.get_integration_settings() is not None
            assert manager.get_performance_settings() is not None
            assert manager.get_debugging_settings() is not None
            assert manager.get_experimental_features() is not None
            
            # Verify validation passes
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is True
            assert len(validation_result['errors']) == 0
            
            logger.info("✅ Valid complete configuration test passed")
    
    def test_missing_configuration_sections(self):
        """Test handling of missing configuration sections"""
        logger.info("🧪 Testing missing configuration sections...")
        
        # Configuration missing some sections
        incomplete_config = {
            "analysis_system": {
                "version": "3.1",
                "phase": "3b"
            },
            "crisis_thresholds": {
                "high": 0.55,
                "medium": 0.28,
                "low": 0.16
            }
            # Missing other sections
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(incomplete_config))), \
             patch('json.load', return_value=incomplete_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = incomplete_config
            
            # Should still work with fallbacks to defaults
            manager = AnalysisParametersManager(mock_config_manager)
            
            # Should get default values for missing sections
            phrase_params = manager.get_phrase_extraction_parameters()
            assert phrase_params['min_phrase_length'] == 2  # Default value
            assert phrase_params['max_phrase_length'] == 6   # Default value
            
            logger.info("✅ Missing configuration sections test passed")
    
    def test_invalid_json_structure(self):
        """Test handling of invalid JSON structure"""
        logger.info("🧪 Testing invalid JSON structure...")
        
        # Completely invalid structure
        invalid_config = {
            "not_analysis_system": {},
            "random_data": "invalid"
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(invalid_config))), \
             patch('json.load', return_value=invalid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = invalid_config
            
            # Should fail gracefully
            with pytest.raises(ValueError):
                AnalysisParametersManager(mock_config_manager)
            
            logger.info("✅ Invalid JSON structure test passed")


class TestEnvironmentVariableValidation:
    """Test environment variable validation and integration"""
    
    def test_environment_variable_data_types(self):
        """Test that environment variables are properly converted to correct data types"""
        logger.info("🧪 Testing environment variable data type conversion...")
        
        env_vars = {
            # Float values
            'NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH': '0.75',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM': '0.35',
            'NLP_ANALYSIS_CRISIS_THRESHOLD_LOW': '0.20',
            
            # Integer values
            'NLP_ANALYSIS_MIN_PHRASE_LENGTH': '3',
            'NLP_ANALYSIS_MAX_PHRASE_LENGTH': '8',
            'NLP_ANALYSIS_TIMEOUT_MS': '7000',
            
            # Boolean values
            'NLP_ANALYSIS_PHRASE_CRISIS_FOCUS': 'true',
            'NLP_ANALYSIS_ENABLE_DETAILED_LOGGING': 'false',
            'NLP_ANALYSIS_EXPERIMENTAL_ADVANCED_CONTEXT': '1',
            
            # String values
            'NLP_ANALYSIS_INTEGRATION_MODE': 'enhanced'
        }
        
        with patch.dict(os.environ, env_vars):
            # Create a configuration that would have been processed by ConfigManager
            processed_config = {
                "crisis_thresholds": {
                    "high": 0.75,      # Converted from string
                    "medium": 0.35,    # Converted from string
                    "low": 0.20,       # Converted from string
                    "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
                },
                "phrase_extraction": {
                    "min_phrase_length": 3,        # Converted from string
                    "max_phrase_length": 8,        # Converted from string
                    "crisis_focus": True,          # Converted from string
                    "defaults": {"min_phrase_length": 2, "max_phrase_length": 6, "crisis_focus": True}
                },
                "performance_settings": {
                    "analysis_timeout_ms": 7000,   # Converted from string
                    "defaults": {"analysis_timeout_ms": 5000}
                },
                "debugging_settings": {
                    "enable_detailed_logging": False,  # Converted from string
                    "defaults": {"enable_detailed_logging": False}
                },
                "feature_flags": {
                    "experimental_analysis_features": {
                        "enable_advanced_context_analysis": True,  # Converted from string
                        "defaults": {"enable_advanced_context_analysis": False}
                    }
                },
                "integration_settings": {
                    "integration_mode": "enhanced",    # String value
                    "defaults": {"integration_mode": "full"}
                }
            }
            
            # FIXED: Create proper mock with file system patches
            with patch('pathlib.Path.exists', return_value=True), \
                 patch('builtins.open', mock_open(read_data=json.dumps(processed_config))), \
                 patch('json.load', return_value=processed_config):
                
                mock_config_manager = Mock()
                mock_config_manager.config_dir = Path("/app/config")
                mock_config_manager.substitute_environment_variables.return_value = processed_config
                
                manager = AnalysisParametersManager(mock_config_manager)
                
                # Verify data types are correct
                thresholds = manager.get_crisis_thresholds()
                assert isinstance(thresholds['high'], float)
                assert thresholds['high'] == 0.75
                
                phrase_params = manager.get_phrase_extraction_parameters()
                assert isinstance(phrase_params['min_phrase_length'], int)
                assert phrase_params['min_phrase_length'] == 3
                assert isinstance(phrase_params['crisis_focus'], bool)
                assert phrase_params['crisis_focus'] is True
                
                performance_settings = manager.get_performance_settings()
                assert isinstance(performance_settings['analysis_timeout_ms'], int)
                assert performance_settings['analysis_timeout_ms'] == 7000
                
                debugging_settings = manager.get_debugging_settings()
                assert isinstance(debugging_settings['enable_detailed_logging'], bool)
                assert debugging_settings['enable_detailed_logging'] is False
                
                experimental_features = manager.get_experimental_features()
                assert isinstance(experimental_features['enable_advanced_context_analysis'], bool)
                assert experimental_features['enable_advanced_context_analysis'] is True
                
                integration_settings = manager.get_integration_settings()
                assert isinstance(integration_settings['integration_mode'], str)
                assert integration_settings['integration_mode'] == 'enhanced'
        
        logger.info("✅ Environment variable data type conversion test passed")
    
    def test_environment_variable_range_validation(self):
        """Test validation of environment variable values within acceptable ranges"""
        logger.info("🧪 Testing environment variable range validation...")
        
        # Test with out-of-range values
        invalid_env_vars = {
            'NLP_ANALYSIS_CRISIS_THRESHOLD_HIGH': '1.5',    # > 1.0
            'NLP_ANALYSIS_CRISIS_THRESHOLD_MEDIUM': '-0.1', # < 0.0
            'NLP_ANALYSIS_MIN_PHRASE_LENGTH': '0',          # < 1
            'NLP_ANALYSIS_TIMEOUT_MS': '-1000'              # < 0
        }
        
        with patch.dict(os.environ, invalid_env_vars):
            # Configuration with invalid values
            invalid_config = {
                "crisis_thresholds": {
                    "high": 1.5,       # Invalid: > 1.0
                    "medium": -0.1,    # Invalid: < 0.0
                    "low": 0.16,
                    "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
                },
                "phrase_extraction": {
                    "min_phrase_length": 0,  # Invalid: < 1
                    "defaults": {"min_phrase_length": 2}
                },
                "performance_settings": {
                    "analysis_timeout_ms": -1000,  # Invalid: < 0
                    "defaults": {"analysis_timeout_ms": 5000}
                }
            }
            
            # FIXED: Create proper mock with file system patches
            with patch('pathlib.Path.exists', return_value=True), \
                 patch('builtins.open', mock_open(read_data=json.dumps(invalid_config))), \
                 patch('json.load', return_value=invalid_config):
                
                mock_config_manager = Mock()
                mock_config_manager.config_dir = Path("/app/config")
                mock_config_manager.substitute_environment_variables.return_value = invalid_config
                
                manager = AnalysisParametersManager(mock_config_manager)
                
                # Validation should catch these issues
                validation_result = manager.validate_parameters()
                assert validation_result['valid'] is False
                assert len(validation_result['errors']) > 0
        
        logger.info("✅ Environment variable range validation test passed")
    
    def test_boolean_environment_variable_parsing(self):
        """Test parsing of various boolean representations in environment variables"""
        logger.info("🧪 Testing boolean environment variable parsing...")
        
        boolean_test_cases = [
            ('true', True),
            ('True', True),
            ('TRUE', True),
            ('1', True),
            ('yes', True),
            ('on', True),
            ('false', False),
            ('False', False),
            ('FALSE', False),
            ('0', False),
            ('no', False),
            ('off', False)
        ]
        
        for env_value, expected_bool in boolean_test_cases:
            config = {
                "debugging_settings": {
                    "enable_detailed_logging": expected_bool,  # Pre-processed boolean
                    "defaults": {"enable_detailed_logging": False}
                }
            }
            
            # FIXED: Create proper mock with file system patches
            with patch('pathlib.Path.exists', return_value=True), \
                 patch('builtins.open', mock_open(read_data=json.dumps(config))), \
                 patch('json.load', return_value=config):
                
                mock_config_manager = Mock()
                mock_config_manager.config_dir = Path("/app/config")
                mock_config_manager.substitute_environment_variables.return_value = config
                
                manager = AnalysisParametersManager(mock_config_manager)
                
                # Test the _parse_bool method directly
                parsed_value = manager._parse_bool(env_value)
                assert parsed_value == expected_bool, f"Failed to parse '{env_value}' as {expected_bool}"
        
        logger.info("✅ Boolean environment variable parsing test passed")


class TestParameterValidationRules:
    """Test parameter validation rules and constraints"""
    
    def test_crisis_threshold_ordering_validation(self):
        """Test that crisis thresholds maintain proper ordering"""
        logger.info("🧪 Testing crisis threshold ordering validation...")
        
        # Valid ordering: high > medium > low
        valid_config = {
            "crisis_thresholds": {
                "high": 0.70,
                "medium": 0.35,
                "low": 0.20,
                "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(valid_config))), \
             patch('json.load', return_value=valid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = valid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is True
        
        # Invalid ordering: high < medium
        invalid_config = {
            "crisis_thresholds": {
                "high": 0.30,   # Invalid: < medium
                "medium": 0.50,
                "low": 0.20,
                "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(invalid_config))), \
             patch('json.load', return_value=invalid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = invalid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is False
            assert any('high > medium > low' in error for error in validation_result['errors'])
        
        logger.info("✅ Crisis threshold ordering validation test passed")
    
    def test_phrase_length_validation(self):
        """Test phrase length parameter validation"""
        logger.info("🧪 Testing phrase length validation...")
        
        # Valid phrase lengths
        valid_config = {
            "phrase_extraction": {
                "min_phrase_length": 2,
                "max_phrase_length": 6,
                "defaults": {"min_phrase_length": 2, "max_phrase_length": 6}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(valid_config))), \
             patch('json.load', return_value=valid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = valid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is True
        
        # Invalid phrase lengths: min >= max
        invalid_config = {
            "phrase_extraction": {
                "min_phrase_length": 6,  # Invalid: >= max
                "max_phrase_length": 6,
                "defaults": {"min_phrase_length": 2, "max_phrase_length": 6}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(invalid_config))), \
             patch('json.load', return_value=invalid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = invalid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is False
            assert any('min_phrase_length must be < max_phrase_length' in error for error in validation_result['errors'])
        
        logger.info("✅ Phrase length validation test passed")
    
    def test_pattern_confidence_threshold_validation(self):
        """Test pattern learning confidence threshold validation"""
        logger.info("🧪 Testing pattern confidence threshold validation...")
        
        # Valid confidence thresholds
        valid_config = {
            "pattern_learning": {
                "confidence_thresholds": {
                    "high_confidence": 0.8,
                    "medium_confidence": 0.5,
                    "low_confidence": 0.2,
                    "defaults": {
                        "high_confidence": 0.7,
                        "medium_confidence": 0.4,
                        "low_confidence": 0.1
                    }
                },
                "defaults": {}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(valid_config))), \
             patch('json.load', return_value=valid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = valid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is True
        
        # Invalid confidence thresholds: wrong ordering
        invalid_config = {
            "pattern_learning": {
                "confidence_thresholds": {
                    "high_confidence": 0.3,  # Invalid: < medium
                    "medium_confidence": 0.5,
                    "low_confidence": 0.2,
                    "defaults": {
                        "high_confidence": 0.7,
                        "medium_confidence": 0.4,
                        "low_confidence": 0.1
                    }
                },
                "defaults": {}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(invalid_config))), \
             patch('json.load', return_value=invalid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = invalid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is False
            assert any('high > medium > low' in error for error in validation_result['errors'])
        
        logger.info("✅ Pattern confidence threshold validation test passed")
    
    def test_performance_parameter_validation(self):
        """Test performance parameter validation"""
        logger.info("🧪 Testing performance parameter validation...")
        
        # Valid performance settings
        valid_config = {
            "performance_settings": {
                "analysis_timeout_ms": 5000,
                "max_concurrent_analyses": 10,
                "cache_ttl_seconds": 300,
                "defaults": {
                    "analysis_timeout_ms": 5000,
                    "max_concurrent_analyses": 10,
                    "cache_ttl_seconds": 300
                }
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(valid_config))), \
             patch('json.load', return_value=valid_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = valid_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            assert validation_result['valid'] is True
        
        # Test that very low timeout generates warning
        warning_config = {
            "performance_settings": {
                "analysis_timeout_ms": 500,  # Very low
                "defaults": {"analysis_timeout_ms": 5000}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(warning_config))), \
             patch('json.load', return_value=warning_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = warning_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            validation_result = manager.validate_parameters()
            # Should still be valid but with warnings
            assert len(validation_result['warnings']) > 0
        
        logger.info("✅ Performance parameter validation test passed")


class TestConfigurationCompatibility:
    """Test configuration compatibility and version handling"""
    
    def test_configuration_version_compatibility(self):
        """Test handling of different configuration versions"""
        logger.info("🧪 Testing configuration version compatibility...")
        
        # Test current version (3.1)
        current_version_config = {
            "analysis_system": {
                "version": "3.1",
                "phase": "3b",
                "architecture": "clean_v3.1_phase_3b"
            },
            "crisis_thresholds": {
                "high": 0.55,
                "medium": 0.28,
                "low": 0.16,
                "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(current_version_config))), \
             patch('json.load', return_value=current_version_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = current_version_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            assert manager.analysis_config['version'] == '3.1'
        
        # Test older version (should still work)
        older_version_config = {
            "analysis_system": {
                "version": "3.0",
                "phase": "3a",
                "architecture": "clean_v3.0"
            },
            "crisis_thresholds": {
                "high": 0.55,
                "medium": 0.28,
                "low": 0.16,
                "defaults": {"high": 0.55, "medium": 0.28, "low": 0.16}
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(older_version_config))), \
             patch('json.load', return_value=older_version_config):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = older_version_config
            
            manager = AnalysisParametersManager(mock_config_manager)
            assert manager.analysis_config['version'] == '3.0'
        
        logger.info("✅ Configuration version compatibility test passed")
    
    def test_missing_defaults_handling(self):
        """Test handling of configuration with missing defaults sections"""
        logger.info("🧪 Testing missing defaults handling...")
        
        # Configuration without defaults sections
        config_without_defaults = {
            "crisis_thresholds": {
                "high": 0.60,
                "medium": 0.30,
                "low": 0.18
                # No defaults section
            },
            "phrase_extraction": {
                "min_phrase_length": 3,
                "max_phrase_length": 7
                # No defaults section
            }
        }
        
        # FIXED: Create proper mock with file system patches
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(config_without_defaults))), \
             patch('json.load', return_value=config_without_defaults):
            
            mock_config_manager = Mock()
            mock_config_manager.config_dir = Path("/app/config")
            mock_config_manager.substitute_environment_variables.return_value = config_without_defaults
            
            # Should still work by using the provided values
            manager = AnalysisParametersManager(mock_config_manager)
            
            thresholds = manager.get_crisis_thresholds()
            assert thresholds['high'] == 0.60
            assert thresholds['medium'] == 0.30
            assert thresholds['low'] == 0.18
            
            phrase_params = manager.get_phrase_extraction_parameters()
            assert phrase_params['min_phrase_length'] == 3
            assert phrase_params['max_phrase_length'] == 7
        
        logger.info("✅ Missing defaults handling test passed")


# ============================================================================
# COMPREHENSIVE TEST RUNNER
# ============================================================================

def run_phase_3b_config_validation_tests():
    """Run all Phase 3b configuration validation tests"""
    logger.info("🧪 Starting Phase 3b Configuration Validation Test Suite")
    logger.info("=" * 70)
    
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
            logger.info("🎉 All Phase 3b configuration validation tests passed!")
            test_results['passed'] = 1
        else:
            logger.error("❌ Some Phase 3b configuration validation tests failed")
            test_results['failed'] = 1
            
    except Exception as e:
        logger.error(f"❌ Configuration validation test suite execution error: {e}")
        test_results['errors'].append(str(e))
    
    logger.info("=" * 70)
    logger.info(f"📊 Configuration Validation Test Results: {test_results['passed']} passed, {test_results['failed']} failed")
    
    return test_results


if __name__ == "__main__":
    # Run configuration validation tests when script is executed directly
    run_phase_3b_config_validation_tests()