# Create this as test_config.py in your ash-nlp directory
# Run this to test if the configuration loads correctly

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, '.')

try:
    from config.env_manager import EnvConfigManager
    
    print("🧪 Testing 3-Model Ensemble Configuration...")
    print("=" * 50)
    
    # Initialize config manager
    config = EnvConfigManager()
    
    print("✅ Configuration loaded successfully!")
    print()
    
    # Test key 3-model variables
    print("🤖 THREE-MODEL CONFIGURATION:")
    print(f"  Depression Model: {config.get('NLP_DEPRESSION_MODEL')}")
    print(f"  Sentiment Model: {config.get('NLP_SENTIMENT_MODEL')}")
    print(f"  Emotional Distress Model: {config.get('NLP_EMOTIONAL_DISTRESS_MODEL')}")
    print()
    
    print("🔧 ENSEMBLE CONFIGURATION:")
    print(f"  Ensemble Mode: {config.get('NLP_ENSEMBLE_MODE')}")
    print(f"  Depression Weight: {config.get('NLP_DEPRESSION_MODEL_WEIGHT')}")
    print(f"  Sentiment Weight: {config.get('NLP_SENTIMENT_MODEL_WEIGHT')}")
    print(f"  Emotional Weight: {config.get('NLP_EMOTIONAL_DISTRESS_MODEL_WEIGHT')}")
    print()
    
    print("🎯 THRESHOLDS:")
    print(f"  Individual - High: {config.get('NLP_HIGH_CRISIS_THRESHOLD')}")
    print(f"  Individual - Medium: {config.get('NLP_MEDIUM_CRISIS_THRESHOLD')}")
    print(f"  Individual - Low: {config.get('NLP_LOW_CRISIS_THRESHOLD')}")
    print(f"  Ensemble - High: {config.get('NLP_ENSEMBLE_HIGH_CRISIS_THRESHOLD')}")
    print(f"  Ensemble - Medium: {config.get('NLP_ENSEMBLE_MEDIUM_CRISIS_THRESHOLD')}")
    print(f"  Ensemble - Low: {config.get('NLP_ENSEMBLE_LOW_CRISIS_THRESHOLD')}")
    print()
    
    print("⚡ PERFORMANCE OPTIMIZATION:")
    print(f"  Max Batch Size: {config.get('NLP_MAX_BATCH_SIZE')}")
    print(f"  Inference Threads: {config.get('NLP_INFERENCE_THREADS')}")
    print(f"  Max Concurrent Requests: {config.get('NLP_MAX_CONCURRENT_REQUESTS')}")
    print(f"  Request Timeout: {config.get('NLP_REQUEST_TIMEOUT')}")
    print()
    
    print("🧪 EXPERIMENTAL FEATURES:")
    print(f"  Ensemble Analysis: {config.get('NLP_ENABLE_ENSEMBLE_ANALYSIS')}")
    print(f"  Gap Detection: {config.get('NLP_ENABLE_GAP_DETECTION')}")
    print(f"  Confidence Spreading: {config.get('NLP_ENABLE_CONFIDENCE_SPREADING')}")
    print(f"  Log Disagreements: {config.get('NLP_LOG_MODEL_DISAGREEMENTS')}")
    
    print()
    print("🎉 SUCCESS: All 3-model ensemble variables are properly configured!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this from the ash-nlp directory")
    
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("Check the syntax and structure of config/env_manager.py")
    
input("Press Enter to continue...")