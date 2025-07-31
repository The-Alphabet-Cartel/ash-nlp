#!/usr/bin/env python3
"""
DeBERTa Model Test Script for Ash NLP Service
Tests microsoft/deberta-v3-large against actual crisis keywords
without modifying the production system

Place this file in: ash-nlp/tests/test_deberta_model.py
Run with: python tests/test_deberta_model.py
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the parent directory to path so we can import from the main codebase
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import torch
    from transformers import pipeline, AutoConfig
    from huggingface_hub import login
    print("✅ Required packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure transformers, torch, and huggingface_hub are installed")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crisis keywords from your files
HIGH_CRISIS_KEYWORDS = {
    'suicidal_ideation': [
        'kill myself', 'end it all', 'want to die', 'suicide', 'suicidal',
        'better off dead', 'can\'t go on', 'no point living', 'end my life',
        'not worth living', 'want to disappear forever', 'ready to die',
        'take my own life', 'don\'t want to be here', 'tired of living'
    ],
    'self_harm': [
        'cut myself', 'hurt myself', 'self harm', 'want to cut', 'need to cut',
        'deserve pain', 'cutting again', 'relapsed cutting', 'razor blade',
        'burn myself', 'hit myself', 'punish myself', 'make it bleed'
    ],
    'immediate_danger': [
        'have a plan', 'goodbye everyone', 'this is goodbye', 'final message',
        'pills ready', 'bridge tonight', 'gun loaded', 'rope tied',
        'last time', 'won\'t see tomorrow', 'tonight\'s the night', 'it\'s time'
    ]
}

MEDIUM_CRISIS_KEYWORDS = {
    'severe_emotional_distress': [
        'having a breakdown', 'mental breakdown', 'falling apart', 'losing my mind',
        'can\'t stop crying', 'sobbing uncontrollably', 'emotional wreck',
        'completely lost', 'don\'t know what to do', 'everything is falling apart'
    ],
    'severe_depression': [
        'severely depressed', 'deep depression', 'clinical depression',
        'can\'t get out of bed', 'lost all motivation', 'nothing brings joy',
        'feel empty inside', 'life has no meaning', 'everything is pointless'
    ],
    'concerning_ideation': [
        'sometimes think about dying', 'wonder if it would be easier',
        'think about not existing', 'passive suicidal thoughts',
        'wouldn\'t mind not waking up', 'tired of fighting'
    ]
}

LOW_CRISIS_KEYWORDS = {
    'depression_symptoms': [
        'feeling depressed', 'feeling down', 'feeling low', 'feeling sad',
        'feeling blue', 'feeling empty', 'mood is off', 'not feeling great',
        'struggling mentally', 'depression symptoms'
    ],
    'anxiety_symptoms': [
        'feeling anxious', 'anxiety', 'stressed out', 'really stressed',
        'panic', 'worried', 'nervous', 'on edge', 'restless'
    ],
    'daily_functioning': [
        'can\'t get motivated', 'procrastinating everything', 'messy room',
        'haven\'t showered', 'eating poorly', 'sleep schedule messed up'
    ]
}

NORMAL_MESSAGES = [
    "What a beautiful day! I love spending time with friends.",
    "Just finished a great workout, feeling energized!",
    "Looking forward to the weekend plans.",
    "Had an awesome day at work today.",
    "Really enjoying this new book I'm reading.",
    "Thanks for the help with my homework!",
    "The weather is so nice today.",
    "Can't wait for the concert next week!"
]

class MentalHealthModelTester:
    """Test mental health classification models against crisis keywords"""
    
    def __init__(self):
        self.old_model_name = "rafalposwiata/deproberta-large-depression"
        # Better alternatives - these are already fine-tuned for classification
        self.model_candidates = [
            "slimshady07/Mental_BERT",  # Fine-tuned BERT for mental health classification
            "AIMH/mental-roberta-large",  # Mental health specific RoBERTa (may need gating)
            "mental/mental-bert-base-uncased",  # Original MentalBERT (may need gating)
            "siebert/sentiment-roberta-large-english"  # Current working sentiment model
        ]
        self.new_model_name = "slimshady07/Mental_BERT"  # Start with this one
        self.device = self._configure_device()
        self.old_model = None
        self.new_model = None
        self.results = {
            'model_comparison': {},
            'label_analysis': {},
            'performance_metrics': {},
            'recommendation': ''
        }
        
        # Set up Hugging Face authentication
        self._setup_huggingface_auth()
        
    def _setup_huggingface_auth(self):
        """Set up Hugging Face authentication"""
        try:
            # Try multiple token locations
            token_paths = [
                "/run/secrets/huggingface",  # Docker secrets location
                "./secrets/huggingface",     # Local secrets location
                "../secrets/huggingface",    # Parent directory secrets
                "../../secrets/huggingface", # Two levels up
            ]
            
            token = None
            
            # Try environment variable first
            if os.getenv('GLOBAL_HUGGINGFACE_TOKEN'):
                token = os.getenv('GLOBAL_HUGGINGFACE_TOKEN')
                if token.startswith('/run/secrets'):
                    # It's a path, read from file
                    try:
                        with open(token, 'r') as f:
                            token = f.read().strip()
                    except:
                        token = None
                elif token and len(token) > 10:  # Direct token
                    pass
                else:
                    token = None
            
            # Try reading from file paths
            if not token:
                for path in token_paths:
                    try:
                        if os.path.exists(path):
                            with open(path, 'r') as f:
                                token = f.read().strip()
                            if token and len(token) > 10:
                                logger.info(f"✅ Found Hugging Face token at: {path}")
                                break
                    except Exception as e:
                        continue
            
            # Try hardcoded token as fallback (for testing)
            if not token:
                hardcoded_token = "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"
                logger.warning("🔑 Using hardcoded token for testing - replace with secure method")
                token = hardcoded_token
            
            if token and len(token) > 10:
                login(token=token)
                logger.info("🔐 Successfully authenticated with Hugging Face")
            else:
                logger.warning("🔓 No Hugging Face token found - will try without authentication")
                
        except Exception as e:
            logger.warning(f"🔓 Could not authenticate with Hugging Face: {e}")
            logger.info("Will attempt to load models without authentication")
        
    def _configure_device(self):
        """Configure device for testing"""
        if torch.cuda.is_available():
            device = 0
            logger.info(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
            logger.info(f"Available VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            device = -1
            logger.info("Using CPU (CUDA not available)")
        return device
    
    def load_models(self):
        """Load both old and new models for comparison"""
        logger.info("🔄 Loading models for comparison...")
        
        try:
            # Load old model
            logger.info(f"Loading old model: {self.old_model_name}")
            start_time = time.time()
            self.old_model = pipeline(
                "text-classification",
                model=self.old_model_name,
                device=self.device,
                torch_dtype=torch.float16,
                top_k=None
            )
            old_load_time = time.time() - start_time
            logger.info(f"✅ Old model loaded in {old_load_time:.2f}s")
            
            # Try loading new models in order of preference
            for model_name in self.model_candidates:
                logger.info(f"Trying to load: {model_name}")
                start_time = time.time()
                
                try:
                    # First, check the model config to understand its labels
                    try:
                        config = AutoConfig.from_pretrained(model_name)
                        logger.info(f"Model config: {config.model_type}")
                        if hasattr(config, 'id2label'):
                            logger.info(f"Model labels: {config.id2label}")
                        else:
                            logger.info("No predefined labels found in config")
                    except Exception as e:
                        logger.warning(f"Could not load model config: {e}")
                    
                    # Try to load the model
                    self.new_model = pipeline(
                        "text-classification",
                        model=model_name,
                        device=self.device,
                        torch_dtype=torch.float16,
                        top_k=None,
                        use_fast=False  # Use slow tokenizer to avoid protobuf issues
                    )
                    new_load_time = time.time() - start_time
                    self.new_model_name = model_name  # Update the name to what actually worked
                    logger.info(f"✅ New model ({model_name}) loaded in {new_load_time:.2f}s")
                    break
                    
                except Exception as e:
                    logger.warning(f"❌ Failed to load {model_name}: {e}")
                    continue
            else:
                raise Exception("All candidate models failed to load")
            
            # Store load times
            self.results['performance_metrics']['old_model_load_time'] = old_load_time
            self.results['performance_metrics']['new_model_load_time'] = new_load_time
            self.results['performance_metrics']['selected_model'] = self.new_model_name
            
            # Check memory usage
            if self.device != -1:
                memory_used = torch.cuda.memory_allocated(self.device) / 1024**3
                memory_cached = torch.cuda.memory_reserved(self.device) / 1024**3
                logger.info(f"GPU Memory: {memory_used:.2f}GB allocated, {memory_cached:.2f}GB cached")
                self.results['performance_metrics']['gpu_memory_used'] = memory_used
                self.results['performance_metrics']['gpu_memory_cached'] = memory_cached
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            raise
    
    def test_single_message(self, message: str, expected_level: str) -> Dict[str, Any]:
        """Test a single message with both models"""
        results = {
            'message': message,
            'expected_level': expected_level,
            'old_model_result': None,
            'new_model_result': None,
            'old_model_time': 0,
            'new_model_time': 0
        }
        
        try:
            # Test old model
            start_time = time.time()
            old_result = self.old_model(message)
            results['old_model_time'] = time.time() - start_time
            results['old_model_result'] = old_result
            
            # Test new model
            start_time = time.time()
            new_result = self.new_model(message)
            results['new_model_time'] = time.time() - start_time
            results['new_model_result'] = new_result
            
        except Exception as e:
            logger.error(f"Error testing message '{message[:50]}...': {e}")
            results['error'] = str(e)
        
        return results
    
    def analyze_label_differences(self, test_results: List[Dict]):
        """Analyze differences in label formats between models"""
        old_labels = set()
        new_labels = set()
        
        for result in test_results:
            if result.get('old_model_result'):
                if isinstance(result['old_model_result'], list):
                    for pred in result['old_model_result']:
                        old_labels.add(pred.get('label', 'unknown'))
                        
            if result.get('new_model_result'):
                if isinstance(result['new_model_result'], list):
                    for pred in result['new_model_result']:
                        new_labels.add(pred.get('label', 'unknown'))
        
        self.results['label_analysis'] = {
            'old_model_labels': sorted(list(old_labels)),
            'new_model_labels': sorted(list(new_labels)),
            'label_mapping_needed': old_labels != new_labels
        }
        
        logger.info(f"Old model labels: {sorted(list(old_labels))}")
        logger.info(f"New model labels: {sorted(list(new_labels))}")
        
        if old_labels != new_labels:
            logger.warning("⚠️ Label formats differ between models - mapping will be needed")
        else:
            logger.info("✅ Label formats are compatible")
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        logger.info("🚀 Starting comprehensive DeBERTa model test")
        
        # Load models
        self.load_models()
        
        all_test_results = []
        
        # Test high crisis keywords
        logger.info("🔴 Testing HIGH crisis keywords...")
        for category, keywords in HIGH_CRISIS_KEYWORDS.items():
            logger.info(f"  Testing {category}: {len(keywords)} keywords")
            for keyword in keywords[:5]:  # Test first 5 from each category
                message = f"I {keyword} and I can't take it anymore"
                result = self.test_single_message(message, 'high')
                result['category'] = category
                all_test_results.append(result)
        
        # Test medium crisis keywords
        logger.info("🟡 Testing MEDIUM crisis keywords...")
        for category, keywords in MEDIUM_CRISIS_KEYWORDS.items():
            logger.info(f"  Testing {category}: {len(keywords)} keywords")
            for keyword in keywords[:3]:  # Test first 3 from each category
                message = f"I've been {keyword} lately"
                result = self.test_single_message(message, 'medium')
                result['category'] = category
                all_test_results.append(result)
        
        # Test low crisis keywords
        logger.info("🟢 Testing LOW crisis keywords...")
        for category, keywords in LOW_CRISIS_KEYWORDS.items():
            logger.info(f"  Testing {category}: {len(keywords)} keywords")
            for keyword in keywords[:3]:  # Test first 3 from each category
                message = f"I've been {keyword} but I'll be okay"
                result = self.test_single_message(message, 'low')
                result['category'] = category
                all_test_results.append(result)
        
        # Test normal messages
        logger.info("⚪ Testing NORMAL messages...")
        for message in NORMAL_MESSAGES:
            result = self.test_single_message(message, 'none')
            result['category'] = 'normal'
            all_test_results.append(result)
        
        # Analyze results
        self.analyze_label_differences(all_test_results)
        self.analyze_performance(all_test_results)
        self.generate_recommendation()
        
        return all_test_results
    
    def analyze_performance(self, test_results: List[Dict]):
        """Analyze performance differences between models"""
        old_times = [r['old_model_time'] for r in test_results if 'old_model_time' in r]
        new_times = [r['new_model_time'] for r in test_results if 'new_model_time' in r]
        
        self.results['performance_metrics'].update({
            'old_model_avg_inference_time': sum(old_times) / len(old_times) if old_times else 0,
            'new_model_avg_inference_time': sum(new_times) / len(new_times) if new_times else 0,
            'total_test_messages': len(test_results),
        })
        
        old_avg = self.results['performance_metrics']['old_model_avg_inference_time']
        new_avg = self.results['performance_metrics']['new_model_avg_inference_time']
        
        logger.info(f"Average inference time - Old: {old_avg:.4f}s, New: {new_avg:.4f}s")
        
        if new_avg > old_avg:
            speed_diff = ((new_avg - old_avg) / old_avg) * 100
            logger.info(f"New model is {speed_diff:.1f}% slower")
        else:
            speed_diff = ((old_avg - new_avg) / old_avg) * 100
            logger.info(f"New model is {speed_diff:.1f}% faster")
    
    def generate_recommendation(self):
        """Generate recommendation based on test results"""
        recommendation = []
        
        # Check label compatibility
        if self.results['label_analysis']['label_mapping_needed']:
            recommendation.append("⚠️ Label mapping required - different output formats")
        else:
            recommendation.append("✅ Labels compatible - no mapping needed")
        
        # Check performance
        new_load_time = self.results['performance_metrics']['new_model_load_time']
        old_load_time = self.results['performance_metrics']['old_model_load_time']
        
        if new_load_time > old_load_time * 1.5:
            recommendation.append("⚠️ Significantly slower model loading")
        else:
            recommendation.append("✅ Acceptable model loading time")
        
        # Memory usage
        if 'gpu_memory_used' in self.results['performance_metrics']:
            memory_used = self.results['performance_metrics']['gpu_memory_used']
            if memory_used > 8.0:  # More than 8GB
                recommendation.append("⚠️ High memory usage - monitor on production")
            else:
                recommendation.append("✅ Acceptable memory usage")
        
        self.results['recommendation'] = " | ".join(recommendation)
        logger.info(f"Recommendation: {self.results['recommendation']}")
    
    def save_results(self, filename: str = "deberta_test_results.json"):
        """Save test results to file"""
        results_path = Path(__file__).parent / filename
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        logger.info(f"📁 Results saved to: {results_path}")
    
    def print_summary(self, test_results: List[Dict]):
        """Print a summary of test results"""
        print("\n" + "="*80)
        print("🎯 DEBERTA MODEL TEST SUMMARY")
        print("="*80)
        
        print(f"📊 Total messages tested: {len(test_results)}")
        print(f"🏷️ Old model labels: {self.results['label_analysis']['old_model_labels']}")
        print(f"🏷️ New model labels: {self.results['label_analysis']['new_model_labels']}")
        
        if self.results['label_analysis']['label_mapping_needed']:
            print("⚠️ LABEL MAPPING REQUIRED")
        else:
            print("✅ LABELS COMPATIBLE")
        
        print(f"\n⏱️ Performance:")
        print(f"  Old model load time: {self.results['performance_metrics']['old_model_load_time']:.2f}s")
        print(f"  New model load time: {self.results['performance_metrics']['new_model_load_time']:.2f}s")
        print(f"  Old model avg inference: {self.results['performance_metrics']['old_model_avg_inference_time']:.4f}s")
        print(f"  New model avg inference: {self.results['performance_metrics']['new_model_avg_inference_time']:.4f}s")
        
        if 'gpu_memory_used' in self.results['performance_metrics']:
            print(f"  GPU memory used: {self.results['performance_metrics']['gpu_memory_used']:.2f}GB")
        
        print(f"\n💡 Recommendation: {self.results['recommendation']}")
        
        # Show some example predictions
        print(f"\n📝 Example predictions:")
        for i, result in enumerate(test_results[:5]):
            if result.get('old_model_result') and result.get('new_model_result'):
                old_top = max(result['old_model_result'], key=lambda x: x.get('score', 0))
                new_top = max(result['new_model_result'], key=lambda x: x.get('score', 0))
                print(f"  {i+1}. '{result['message'][:50]}...'")
                print(f"     Old: {old_top.get('label')} ({old_top.get('score', 0):.3f})")
                print(f"     New: {new_top.get('label')} ({new_top.get('score', 0):.3f})")
        
        print("="*80)

def main():
    """Main function to run the test"""
    try:
        tester = MentalHealthModelTester()
        test_results = tester.run_comprehensive_test()
        tester.print_summary(test_results)
        tester.save_results()
        
        print(f"\n🎉 Test completed successfully!")
        print(f"📁 Detailed results saved to: deberta_test_results.json")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()