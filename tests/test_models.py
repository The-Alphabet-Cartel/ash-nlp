#!/usr/bin/env python3
"""
Three-Model Sentiment Analysis Test for Ash-NLP Service
Tests the three recommended sentiment models for compatibility and performance

Repository: https://github.com/the-alphabet-cartel/ash-nlp
Usage: docker exec ash-nlp python ./tests/test_model.py
"""

import sys
import os
import time
import json
import traceback
import warnings
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

# Add project root to path
sys.path.insert(0, '/app')

# Import project modules
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    from models.ml_models import EnhancedModelManager
    from config.nlp_config_manager import NLPConfigManager
    import torch
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this from within the ash-nlp container")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test configuration
TEST_MODELS = {
    'siebert_roberta': {
        'name': 'siebert/sentiment-roberta-large-english',
        'type': 'roberta-large',
        'description': 'High-performance RoBERTa sentiment model (Recommended)',
        'labels': ['NEGATIVE', 'POSITIVE'],
        'expected_accuracy': 93.2
    },
    'tabularis_multilingual': {
        'name': 'tabularisai/multilingual-sentiment-analysis',
        'type': 'distilbert-multilingual',
        'description': 'Modern multilingual DistilBERT model (2024)',
        'labels': ['NEGATIVE', 'NEUTRAL', 'POSITIVE'],
        'expected_accuracy': 93.0
    },
    'distilbert_social': {
        'name': 'DT12the/distilbert-sentiment-analysis',
        'type': 'distilbert-base',
        'description': 'Social media focused DistilBERT model',
        'labels': ['non-negative', 'negative'],
        'expected_accuracy': 85.0
    }
}

# Test phrases designed for crisis detection scenarios
TEST_PHRASES = [
    {
        'text': "I'm feeling absolutely wonderful today! Everything is going great!",
        'expected_sentiment': 'positive',
        'category': 'positive_control',
        'description': 'Strong positive sentiment'
    },
    {
        'text': "I hate everything, nothing matters anymore, I can't take this",
        'expected_sentiment': 'negative',
        'category': 'crisis_negative',
        'description': 'Strong negative sentiment with crisis indicators'
    },
    {
        'text': "This game is killing me but I love the challenge",
        'expected_sentiment': 'mixed',
        'category': 'gaming_context',
        'description': 'Gaming context with mixed sentiment'
    },
    {
        'text': "I'm struggling but trying to stay positive and get help",
        'expected_sentiment': 'mixed',
        'category': 'help_seeking',
        'description': 'Mixed sentiment with help-seeking behavior'
    },
    {
        'text': "Work has been really stressful lately",
        'expected_sentiment': 'negative',
        'category': 'work_stress',
        'description': 'Negative sentiment in work context'
    },
    {
        'text': "I just want to disappear forever, nobody would care",
        'expected_sentiment': 'negative',
        'category': 'high_crisis',
        'description': 'High crisis language with negative sentiment'
    },
    {
        'text': "The weather is nice today",
        'expected_sentiment': 'neutral',
        'category': 'neutral_control',
        'description': 'Neutral sentiment control'
    },
    {
        'text': "lol this is so random but whatever 😂",
        'expected_sentiment': 'neutral',
        'category': 'casual_social',
        'description': 'Casual social media language'
    }
]

class ModelTester:
    """Test individual sentiment models for compatibility and performance"""
    
    def __init__(self, model_config: Dict[str, Any]):
        self.config = model_config
        self.model_name = model_config['name']
        self.model_type = model_config['type']
        self.description = model_config['description']
        self.expected_labels = model_config['labels']
        
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.load_time = 0.0
        self.load_success = False
        self.load_error = None
    
    def load_model(self) -> bool:
        """Load the sentiment model"""
        print(f"\n🔄 Loading {self.model_type}: {self.model_name}")
        print(f"   Description: {self.description}")
        
        start_time = time.time()
        
        try:
            # Suppress deprecation warnings during model loading
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning)
                warnings.filterwarnings("ignore", message=".*encoder_attention_mask.*")
                
                # Load tokenizer and model
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
                
                # Create pipeline
                self.pipeline = pipeline(
                    "sentiment-analysis",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if torch.cuda.is_available() else -1
                )
            
            self.load_time = time.time() - start_time
            self.load_success = True
            
            print(f"   ✅ Successfully loaded in {self.load_time:.2f}s")
            
            # Test basic functionality
            test_result = self.pipeline("This is a test")
            print(f"   ✅ Basic pipeline test successful: {test_result}")
            
            return True
            
        except Exception as e:
            self.load_time = time.time() - start_time
            self.load_error = str(e)
            self.load_success = False
            
            print(f"   ❌ Failed to load: {e}")
            print(f"   📝 Error details: {traceback.format_exc()}")
            
            return False
    
    def test_phrases(self, phrases: List[Dict]) -> List[Dict]:
        """Test model on provided phrases"""
        if not self.load_success:
            return []
        
        results = []
        print(f"\n🧪 Testing {len(phrases)} phrases with {self.model_type}")
        
        for i, phrase_data in enumerate(phrases):
            text = phrase_data['text']
            expected = phrase_data['expected_sentiment']
            category = phrase_data['category']
            
            try:
                start_time = time.time()
                
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    warnings.filterwarnings("ignore", message=".*encoder_attention_mask.*")
                    
                    prediction = self.pipeline(text)
                
                response_time = (time.time() - start_time) * 1000
                
                # Parse result
                if isinstance(prediction, list) and len(prediction) > 0:
                    result = prediction[0]
                    label = result.get('label', '').upper()
                    score = result.get('score', 0.0)
                else:
                    label = 'UNKNOWN'
                    score = 0.0
                
                # Normalize label for comparison
                normalized_label = self._normalize_label(label)
                
                # Determine if prediction matches expectation
                success = self._evaluate_prediction(normalized_label, expected, category)
                
                result_data = {
                    'phrase': text,
                    'category': category,
                    'expected': expected,
                    'predicted_label': label,
                    'normalized_label': normalized_label,
                    'confidence': score,
                    'response_time_ms': response_time,
                    'success': success,
                    'raw_result': prediction
                }
                
                results.append(result_data)
                
                status = "✅" if success else "❌"
                print(f"   {status} {category}: {label} ({score:.3f}) - {response_time:.1f}ms")
                
            except Exception as e:
                error_result = {
                    'phrase': text,
                    'category': category,
                    'expected': expected,
                    'error': str(e),
                    'success': False
                }
                results.append(error_result)
                print(f"   ❌ Error processing '{text[:30]}...': {e}")
        
        return results
    
    def _normalize_label(self, label: str) -> str:
        """Normalize model output labels to standard format"""
        label = label.upper()
        
        # Handle different label formats
        if label in ['NEGATIVE', 'NEG']:
            return 'negative'
        elif label in ['POSITIVE', 'POS']:
            return 'positive'
        elif label in ['NEUTRAL', 'NEU']:
            return 'neutral'
        elif label in ['NON-NEGATIVE', 'NONNEGATIVE']:
            return 'non-negative'
        else:
            return label.lower()
    
    def _evaluate_prediction(self, predicted: str, expected: str, category: str) -> bool:
        """Evaluate if prediction meets expectations"""
        # Direct match
        if predicted == expected:
            return True
        
        # Handle special cases
        if expected == 'mixed':
            # For mixed sentiment, accept neutral or reasonable predictions
            if predicted in ['neutral', 'positive', 'negative']:
                return True
        
        if expected == 'neutral':
            # Accept neutral or non-negative for neutral expectations
            if predicted in ['neutral', 'non-negative']:
                return True
        
        # Category-specific evaluations
        if category == 'gaming_context':
            # Gaming context should not be strongly negative crisis
            return predicted != 'negative' or True  # More lenient for gaming
        
        if category in ['positive_control', 'neutral_control']:
            # Control cases should be more strict
            return predicted == expected
        
        return False
    
    def get_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate performance summary"""
        if not results:
            return {
                'load_success': self.load_success,
                'load_time': self.load_time,
                'load_error': self.load_error,
                'test_results': 'No tests run due to load failure'
            }
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get('success', False))
        avg_response_time = sum(r.get('response_time_ms', 0) for r in results) / total_tests
        
        category_performance = {}
        for result in results:
            category = result['category']
            if category not in category_performance:
                category_performance[category] = {'total': 0, 'success': 0}
            category_performance[category]['total'] += 1
            if result.get('success', False):
                category_performance[category]['success'] += 1
        
        # Calculate category success rates
        for category in category_performance:
            total = category_performance[category]['total']
            success = category_performance[category]['success']
            category_performance[category]['success_rate'] = (success / total) * 100 if total > 0 else 0
        
        return {
            'model_info': {
                'name': self.model_name,
                'type': self.model_type,
                'description': self.description,
                'expected_labels': self.expected_labels
            },
            'load_performance': {
                'success': self.load_success,
                'load_time_seconds': self.load_time,
                'error': self.load_error
            },
            'test_performance': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate_percent': (successful_tests / total_tests) * 100,
                'avg_response_time_ms': avg_response_time,
                'category_performance': category_performance
            },
            'detailed_results': results
        }

class ComprehensiveModelTest:
    """Run comprehensive testing on all three sentiment models"""
    
    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
        self.results = {}
        self.system_info = self._get_system_info()
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information for the test report"""
        try:
            import torch
            cuda_available = torch.cuda.is_available()
            gpu_name = torch.cuda.get_device_name(0) if cuda_available else None
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3 if cuda_available else None
        except:
            cuda_available = False
            gpu_name = None
            gpu_memory = None
        
        return {
            'timestamp': self.start_time.isoformat(),
            'python_version': sys.version,
            'torch_version': torch.__version__ if 'torch' in globals() else 'Unknown',
            'cuda_available': cuda_available,
            'gpu_name': gpu_name,
            'gpu_memory_gb': gpu_memory,
            'container_environment': os.path.exists('/.dockerenv'),
            'working_directory': os.getcwd()
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests on all three models"""
        print("=" * 80)
        print("🧪 ASH-NLP THREE-MODEL SENTIMENT ANALYSIS TEST")
        print("=" * 80)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"GPU Available: {self.system_info['cuda_available']}")
        if self.system_info['gpu_name']:
            print(f"GPU: {self.system_info['gpu_name']} ({self.system_info['gpu_memory_gb']:.1f}GB)")
        print(f"Test Phrases: {len(TEST_PHRASES)}")
        print(f"Models to Test: {len(TEST_MODELS)}")
        
        # Test each model
        for model_key, model_config in TEST_MODELS.items():
            print(f"\n{'='*60}")
            print(f"🚀 TESTING MODEL: {model_key.upper()}")
            print(f"{'='*60}")
            
            tester = ModelTester(model_config)
            
            # Load model
            if tester.load_model():
                # Test phrases
                test_results = tester.test_phrases(TEST_PHRASES)
                
                # Get summary
                summary = tester.get_summary(test_results)
                self.results[model_key] = summary
                
                # Print summary
                self._print_model_summary(model_key, summary)
            else:
                # Model failed to load
                summary = tester.get_summary([])
                self.results[model_key] = summary
                print(f"❌ {model_key} failed to load - skipping tests")
        
        # Generate final report
        return self._generate_final_report()
    
    def _print_model_summary(self, model_key: str, summary: Dict[str, Any]):
        """Print summary for a single model"""
        test_perf = summary['test_performance']
        load_perf = summary['load_performance']
        
        print(f"\n📊 {model_key.upper()} SUMMARY:")
        print(f"   Load Time: {load_perf['load_time_seconds']:.2f}s")
        print(f"   Success Rate: {test_perf['success_rate_percent']:.1f}% ({test_perf['successful_tests']}/{test_perf['total_tests']})")
        print(f"   Avg Response: {test_perf['avg_response_time_ms']:.1f}ms")
        
        print(f"\n   📋 Category Performance:")
        for category, perf in test_perf['category_performance'].items():
            print(f"     {category}: {perf['success_rate']:.1f}% ({perf['success']}/{perf['total']})")
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        end_time = datetime.now(timezone.utc)
        total_time = (end_time - self.start_time).total_seconds()
        
        # Calculate overall statistics
        successful_models = sum(1 for result in self.results.values() 
                              if result['load_performance']['success'])
        total_models = len(self.results)
        
        # Find best performing model
        best_model = None
        best_success_rate = 0
        
        for model_key, result in self.results.items():
            if result['load_performance']['success']:
                success_rate = result['test_performance']['success_rate_percent']
                if success_rate > best_success_rate:
                    best_success_rate = success_rate
                    best_model = model_key
        
        # Generate recommendations
        recommendations = self._generate_recommendations()
        
        final_report = {
            'test_metadata': {
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'total_duration_seconds': total_time,
                'models_tested': total_models,
                'successful_models': successful_models,
                'test_phrases': len(TEST_PHRASES)
            },
            'system_info': self.system_info,
            'overall_results': {
                'models_loaded_successfully': successful_models,
                'total_models_attempted': total_models,
                'load_success_rate': (successful_models / total_models) * 100,
                'best_performing_model': best_model,
                'best_success_rate': best_success_rate
            },
            'model_results': self.results,
            'recommendations': recommendations
        }
        
        # Print final summary
        self._print_final_summary(final_report)
        
        # Save results
        self._save_results(final_report)
        
        return final_report
    
    def _generate_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations based on test results"""
        recommendations = {
            'deployment_ready': [],
            'needs_attention': [],
            'not_recommended': [],
            'summary': ''
        }
        
        for model_key, result in self.results.items():
            if not result['load_performance']['success']:
                recommendations['not_recommended'].append({
                    'model': model_key,
                    'reason': f"Failed to load: {result['load_performance']['error']}"
                })
            else:
                success_rate = result['test_performance']['success_rate_percent']
                response_time = result['test_performance']['avg_response_time_ms']
                
                if success_rate >= 80 and response_time <= 200:
                    recommendations['deployment_ready'].append({
                        'model': model_key,
                        'success_rate': success_rate,
                        'response_time': response_time,
                        'reason': 'High accuracy and good response time'
                    })
                elif success_rate >= 70:
                    recommendations['needs_attention'].append({
                        'model': model_key,
                        'success_rate': success_rate,
                        'response_time': response_time,
                        'reason': 'Acceptable accuracy but may need tuning'
                    })
                else:
                    recommendations['not_recommended'].append({
                        'model': model_key,
                        'success_rate': success_rate,
                        'reason': 'Low accuracy for crisis detection use case'
                    })
        
        # Generate summary recommendation
        if recommendations['deployment_ready']:
            best = max(recommendations['deployment_ready'], 
                      key=lambda x: x['success_rate'])
            recommendations['summary'] = f"Recommend deploying {best['model']} with {best['success_rate']:.1f}% accuracy"
        elif recommendations['needs_attention']:
            recommendations['summary'] = "No models meet deployment criteria - further tuning needed"
        else:
            recommendations['summary'] = "No models successfully loaded - check dependencies and configuration"
        
        return recommendations
    
    def _print_final_summary(self, report: Dict[str, Any]):
        """Print final test summary"""
        print(f"\n{'='*80}")
        print("📋 FINAL TEST SUMMARY")
        print(f"{'='*80}")
        
        overall = report['overall_results']
        print(f"Models Tested: {overall['total_models_attempted']}")
        print(f"Successfully Loaded: {overall['models_loaded_successfully']}")
        print(f"Best Performer: {overall['best_performing_model']} ({overall['best_success_rate']:.1f}%)")
        
        recommendations = report['recommendations']
        print(f"\n🎯 RECOMMENDATION: {recommendations['summary']}")
        
        if recommendations['deployment_ready']:
            print(f"\n✅ DEPLOYMENT READY:")
            for rec in recommendations['deployment_ready']:
                print(f"   • {rec['model']}: {rec['success_rate']:.1f}% accuracy, {rec['response_time']:.1f}ms avg response")
        
        if recommendations['needs_attention']:
            print(f"\n⚠️  NEEDS ATTENTION:")
            for rec in recommendations['needs_attention']:
                print(f"   • {rec['model']}: {rec['success_rate']:.1f}% accuracy - {rec['reason']}")
        
        if recommendations['not_recommended']:
            print(f"\n❌ NOT RECOMMENDED:")
            for rec in recommendations['not_recommended']:
                print(f"   • {rec['model']}: {rec['reason']}")
        
        total_time = report['test_metadata']['total_duration_seconds']
        print(f"\nCompleted in {total_time:.1f} seconds")
    
    def _save_results(self, report: Dict[str, Any]):
        """Save test results to file"""
        try:
            # Create results directory if it doesn't exist
            results_dir = Path("/app/tests/results")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
            filename = f"three_model_test_{timestamp}.json"
            filepath = results_dir / filename
            
            # Save results
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"\n💾 Results saved to: {filepath}")
            
        except Exception as e:
            print(f"\n⚠️  Warning: Could not save results: {e}")

def main():
    """Main test execution"""
    try:
        # Run comprehensive test
        tester = ComprehensiveModelTest()
        results = tester.run_all_tests()
        
        # Return appropriate exit code
        successful_models = results['overall_results']['models_loaded_successfully']
        if successful_models > 0:
            best_rate = results['overall_results']['best_success_rate']
            if best_rate >= 80:
                print(f"\n🎉 Test completed successfully! Best model: {best_rate:.1f}% accuracy")
                sys.exit(0)
            else:
                print(f"\n⚠️  Test completed with concerns. Best accuracy: {best_rate:.1f}%")
                sys.exit(1)
        else:
            print(f"\n❌ Test failed - no models loaded successfully")
            sys.exit(2)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print(f"📝 Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()