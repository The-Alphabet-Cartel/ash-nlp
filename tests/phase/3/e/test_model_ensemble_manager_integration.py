# ash-nlp/tests/phase/3/e/test_model_ensemble_manager_integration.py
"""
Integration Test for Optimized ModelEnsembleManager
FILE VERSION: v3.1-3e-5.5-1
LAST MODIFIED: 2025-08-19
PHASE: 3e Step 5.5 - ModelEnsembleManager Optimization Integration Test
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the optimized manager
from managers.model_ensemble_manager import ModelEnsembleManager, create_model_ensemble_manager
from managers.unified_config_manager import UnifiedConfigManager

class TestModelEnsembleManagerIntegration(unittest.TestCase):
    """
    Integration tests for optimized ModelEnsembleManager
    
    These tests verify that the optimization maintains 100% functionality for
    configuration management while properly migrating analysis methods.
    """
    
    def setUp(self):
        """Set up test environment with temporary config directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        
        # Create sample configuration files for testing
        self._create_test_config_files()
        
        # Create UnifiedConfigManager and ModelEnsembleManager
        self.config_manager = UnifiedConfigManager(str(self.config_dir))
        self.manager = ModelEnsembleManager(self.config_manager)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_test_config_files(self):
        """Create sample configuration files for testing"""
        # Create model_ensemble.json
        model_config = {
            "ensemble_models": {
                "model_definitions": {
                    "depression": {
                        "name": "MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
                        "weight": 0.4,
                        "type": "zero-shot-classification",
                        "pipeline_task": "zero-shot-classification"
                    },
                    "sentiment": {
                        "name": "Lowerated/lm6-deberta-v3-topic-sentiment", 
                        "weight": 0.3,
                        "type": "zero-shot-classification",
                        "pipeline_task": "zero-shot-classification"
                    },
                    "emotional_distress": {
                        "name": "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
                        "weight": 0.3,
                        "type": "zero-shot-classification",
                        "pipeline_task": "zero-shot-classification"
                    }
                }
            },
            "ensemble_config": {
                "mode": "majority"
            },
            "hardware_settings": {
                "device": "auto",
                "precision": "float16",
                "max_batch_size": 32,
                "inference_threads": 16
            },
            "validation": {
                "ensure_weights_sum_to_one": True,
                "fail_on_invalid_weights": True
            }
        }
        
        with open(self.config_dir / 'model_ensemble.json', 'w') as f:
            json.dump(model_config, f)
    
    # ========================================================================
    # CORE FUNCTIONALITY TESTS
    # ========================================================================
    
    def test_manager_initialization_with_config(self):
        """Test that manager initializes correctly with configuration"""
        self.assertIsNotNone(self.manager.config)
        self.assertIsInstance(self.manager.config, dict)
        
        # Should have loaded models
        models = self.manager.get_model_definitions()
        self.assertGreater(len(models), 0)
        self.assertIn('depression', models)
        self.assertIn('sentiment', models)
        self.assertIn('emotional_distress', models)
    
    def test_factory_function_creates_optimized_manager(self):
        """Test that factory function creates properly optimized manager"""
        manager = create_model_ensemble_manager(self.config_manager)
        
        self.assertIsInstance(manager, ModelEnsembleManager)
        self.assertIsNotNone(manager.config)
        self.assertTrue(manager.models_loaded())
    
    def test_configuration_access_updated(self):
        """Test that configuration access uses enhanced patterns"""
        # Test model definitions access
        models = self.manager.get_model_definitions()
        self.assertIsInstance(models, dict)
        self.assertGreater(len(models), 0)
        
        # Test ensemble mode access
        ensemble_mode = self.manager.get_ensemble_mode()
        self.assertEqual(ensemble_mode, 'majority')
        
        # Test hardware settings access
        hardware = self.manager.get_hardware_settings()
        self.assertIsInstance(hardware, dict)
        self.assertEqual(hardware['device'], 'auto')
    
    def test_fallback_configuration_with_env_vars(self):
        """Test that fallback configuration works with environment variables"""
        # Create manager without model_ensemble.json
        temp_dir_no_config = tempfile.mkdtemp()
        config_manager_no_config = UnifiedConfigManager(temp_dir_no_config)
        
        # Test with environment variables
        with patch.dict(os.environ, {
            'NLP_MODEL_DEPRESSION_NAME': 'test-depression-model',
            'NLP_MODEL_SENTIMENT_WEIGHT': '0.5',
            'NLP_ENSEMBLE_MODE': 'weighted'
        }):
            manager_fallback = ModelEnsembleManager(config_manager_no_config)
            
            models = manager_fallback.get_model_definitions()
            self.assertIn('depression', models)
            self.assertEqual(models['depression']['name'], 'test-depression-model')
            self.assertEqual(models['sentiment']['weight'], 0.5)
            self.assertEqual(manager_fallback.get_ensemble_mode(), 'weighted')
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir_no_config)
    
    # ========================================================================
    # MODEL CONFIGURATION TESTS
    # ========================================================================
    
    def test_model_configuration_methods(self):
        """Test all model configuration access methods"""
        # Test model definitions
        models = self.manager.get_model_definitions()
        self.assertIsInstance(models, dict)
        self.assertIn('depression', models)
        
        # Test specific model config
        depression_config = self.manager.get_model_config('depression')
        self.assertIsInstance(depression_config, dict)
        self.assertIn('name', depression_config)
        self.assertIn('weight', depression_config)
        
        # Test model name
        depression_name = self.manager.get_model_name('depression')
        self.assertEqual(depression_name, 'MoritzLaurer/deberta-v3-base-zeroshot-v2.0')
        
        # Test model weight
        depression_weight = self.manager.get_model_weight('depression')
        self.assertEqual(depression_weight, 0.4)
        
        # Test model names list
        model_names = self.manager.get_model_names()
        self.assertIsInstance(model_names, list)
        self.assertIn('depression', model_names)
    
    def test_model_weights_functionality(self):
        """Test model weights management"""
        # Test get all weights
        weights = self.manager.get_model_weights()
        self.assertIsInstance(weights, dict)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=1)
        
        # Test normalized weights
        normalized = self.manager.get_normalized_weights()
        self.assertIsInstance(normalized, dict)
        self.assertAlmostEqual(sum(normalized.values()), 1.0, places=3)
        
        # Test with zero weights
        manager_zero_weights = ModelEnsembleManager(self.config_manager)
        manager_zero_weights.config['models']['depression']['weight'] = 0
        manager_zero_weights.config['models']['sentiment']['weight'] = 0
        manager_zero_weights.config['models']['emotional_distress']['weight'] = 0
        
        normalized_zero = manager_zero_weights.get_normalized_weights()
        # Should assign equal weights
        expected_equal = 1.0 / 3
        for weight in normalized_zero.values():
            self.assertAlmostEqual(weight, expected_equal, places=3)
    
    def test_ensemble_configuration_methods(self):
        """Test ensemble configuration access"""
        # Test ensemble mode
        mode = self.manager.get_ensemble_mode()
        self.assertEqual(mode, 'majority')
        
        # Test ensemble settings
        settings = self.manager.get_ensemble_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn('mode', settings)
        self.assertIn('validation', settings)
        
        # Test mode validation
        self.assertTrue(self.manager.validate_ensemble_mode('majority'))
        self.assertTrue(self.manager.validate_ensemble_mode('consensus'))
        self.assertTrue(self.manager.validate_ensemble_mode('weighted'))
        self.assertFalse(self.manager.validate_ensemble_mode('invalid_mode'))
    
    def test_hardware_configuration_methods(self):
        """Test hardware configuration access"""
        # Test hardware settings
        hardware = self.manager.get_hardware_settings()
        self.assertIsInstance(hardware, dict)
        
        # Test specific hardware settings
        self.assertEqual(self.manager.get_device_setting(), 'auto')
        self.assertEqual(self.manager.get_precision_setting(), 'float16')
        self.assertEqual(self.manager.get_max_batch_size(), 32)
        self.assertEqual(self.manager.get_inference_threads(), 16)
    
    # ========================================================================
    # MIGRATION REFERENCE TESTS
    # ========================================================================
    
    def test_analysis_method_migration_references(self):
        """Test that analysis methods provide migration references"""
        # Test analyze_with_ensemble migration reference
        result = self.manager.analyze_with_ensemble("test message")
        self.assertIsInstance(result, dict)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'method_migrated')
        self.assertIn('migration_target', result)
        self.assertIn('CrisisAnalyzer', result['migration_target'])
        
        # Test classify_zero_shot migration reference
        with patch('analysis.crisis_analyzer.create_crisis_analyzer') as mock_create:
            mock_analyzer = MagicMock()
            mock_analyzer.classify_zero_shot.return_value = 0.75
            mock_create.return_value = mock_analyzer
            
            score = self.manager.classify_zero_shot("test text", "test hypothesis")
            self.assertEqual(score, 0.75)
            mock_create.assert_called_once_with(self.config_manager)
    
    async def test_async_analysis_method_migration(self):
        """Test async analysis method migration"""
        with patch('analysis.crisis_analyzer.create_crisis_analyzer') as mock_create:
            mock_analyzer = MagicMock()
            mock_analyzer.analyze_message.return_value = {'result': 'test_analysis'}
            mock_create.return_value = mock_analyzer
            
            result = await self.manager.analyze_message_ensemble("test", "user1", "channel1")
            self.assertEqual(result, {'result': 'test_analysis'})
            mock_create.assert_called_once_with(self.config_manager)
    
    def test_migration_error_handling(self):
        """Test migration error handling when CrisisAnalyzer is unavailable"""
        with patch('analysis.crisis_analyzer.create_crisis_analyzer', side_effect=ImportError("Module not found")):
            score = self.manager.classify_zero_shot("test text", "test hypothesis")
            self.assertEqual(score, 0.0)
    
    # ========================================================================
    # MODEL STATUS AND VALIDATION TESTS
    # ========================================================================
    
    def test_models_loaded_validation(self):
        """Test models_loaded validation logic"""
        # Test with valid configuration
        self.assertTrue(self.manager.models_loaded())
        
        # Test with no models
        manager_no_models = ModelEnsembleManager(self.config_manager)
        manager_no_models.config['models'] = {}
        self.assertFalse(manager_no_models.models_loaded())
        
        # Test with insufficient models
        manager_one_model = ModelEnsembleManager(self.config_manager)
        manager_one_model.config['models'] = {'depression': {'name': 'test', 'weight': 1.0}}
        self.assertFalse(manager_one_model.models_loaded())
        
        # Test with models missing names
        manager_no_names = ModelEnsembleManager(self.config_manager)
        manager_no_names.config['models']['depression']['name'] = ''
        manager_no_names.config['models']['sentiment']['name'] = ''
        manager_no_names.config['models']['emotional_distress']['name'] = ''
        self.assertFalse(manager_no_names.models_loaded())
    
    def test_model_info_generation(self):
        """Test comprehensive model info generation"""
        model_info = self.manager.get_model_info()
        
        self.assertIsInstance(model_info, dict)
        self.assertIn('total_models', model_info)
        self.assertIn('models_configured', model_info)
        self.assertIn('architecture_version', model_info)
        self.assertIn('model_details', model_info)
        self.assertIn('status', model_info)
        
        # Check model details structure
        model_details = model_info['model_details']
        for model_type in ['depression', 'sentiment', 'emotional_distress']:
            self.assertIn(model_type, model_details)
            details = model_details[model_type]
            self.assertIn('name', details)
            self.assertIn('weight', details)
            self.assertIn('configured', details)
            self.assertTrue(details['configured'])
        
        # Check status
        status = model_info['status']
        self.assertTrue(status['models_loaded'])
        self.assertTrue(status['ready_for_analysis'])
    
    def test_validation_settings(self):
        """Test validation settings access"""
        validation = self.manager.get_validation_settings()
        self.assertIsInstance(validation, dict)
        
        # Test weight validation setting
        self.assertTrue(self.manager.is_weights_validation_enabled())
    
    # ========================================================================
    # ZERO-SHOT CAPABILITIES TESTS
    # ========================================================================
    
    def test_zero_shot_capabilities(self):
        """Test zero-shot capabilities reporting"""
        capabilities = self.manager.get_zero_shot_capabilities()
        
        self.assertIsInstance(capabilities, dict)
        self.assertIn('zero_shot_available', capabilities)
        self.assertIn('zero_shot_model', capabilities)
        self.assertIn('classification_method', capabilities)
        
        # Should find a zero-shot model
        self.assertTrue(capabilities['zero_shot_available'])
        self.assertIsNotNone(capabilities['zero_shot_model'])
        
        if capabilities['zero_shot_available']:
            self.assertIn('model_details', capabilities)
            self.assertIsInstance(capabilities['model_details'], dict)
    
    def test_best_zero_shot_model_selection(self):
        """Test best zero-shot model selection logic"""
        best_model = self.manager._get_best_zero_shot_model()
        
        # Should find a model with zero-shot-classification pipeline task
        self.assertIsNotNone(best_model)
        self.assertIn(best_model, self.manager.get_model_names())
        
        # Verify the selected model has appropriate configuration
        model_config = self.manager.get_model_config(best_model)
        pipeline_task = model_config.get('pipeline_task', '')
        self.assertEqual(pipeline_task, 'zero-shot-classification')
    
    # ========================================================================
    # MANAGER STATUS TESTS
    # ========================================================================
    
    def test_manager_status(self):
        """Test comprehensive manager status"""
        status = self.manager.get_manager_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('version', status)
        self.assertIn('architecture', status)
        self.assertIn('optimization_applied', status)
        self.assertIn('migration_status', status)
        
        # Check optimization status
        self.assertTrue(status['optimization_applied'])
        
        # Check migration status
        migration = status['migration_status']
        self.assertTrue(migration['analysis_methods_migrated'])
        self.assertEqual(migration['migration_target'], 'CrisisAnalyzer')
        self.assertTrue(migration['configuration_updated'])
    
    # ========================================================================
    # ERROR HANDLING TESTS
    # ========================================================================
    
    def test_configuration_loading_error_handling(self):
        """Test error handling in configuration loading"""
        # Test with corrupted config manager
        with patch.object(self.config_manager, 'get_config_section', side_effect=Exception("Config error")):
            manager_error = ModelEnsembleManager(self.config_manager)
            
            # Should fall back to environment configuration
            models = manager_error.get_model_definitions()
            self.assertIsInstance(models, dict)
    
    def test_validation_error_handling(self):
        """Test error handling in validation"""
        # Create manager with invalid config
        manager_invalid = ModelEnsembleManager(self.config_manager)
        manager_invalid.config = None
        
        self.assertFalse(manager_invalid._validate_configuration())
    
    def test_model_info_error_handling(self):
        """Test error handling in model info generation"""
        # Test with corrupted model data
        manager_corrupt = ModelEnsembleManager(self.config_manager)
        manager_corrupt.config['models']['depression'] = None
        
        model_info = manager_corrupt.get_model_info()
        self.assertIsInstance(model_info, dict)
        self.assertIn('model_details', model_info)

if __name__ == '__main__':
    unittest.main()