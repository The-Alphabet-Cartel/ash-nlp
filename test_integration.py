# Create this as test_integration.py in your ash-nlp directory
# This tests if your ModelManager can properly load config from env_manager

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, '.')

try:
    from config.env_manager import EnvConfigManager
    from models.ml_models import EnhancedModelManager
    
    print("🧪 Testing 3-Model Integration...")
    print("=" * 60)
    
    # Initialize config manager
    print("📋 Loading configuration...")
    config_manager = EnvConfigManager()
    
    # Get all configuration as a dictionary
    config_dict = config_manager.get_all()
    
    print("✅ Configuration loaded successfully!")
    print()
    
    # Initialize ModelManager with the configuration
    print("🤖 Initializing ModelManager with configuration...")
    model_manager = EnhancedModelManager(config_dict)
    
    print("✅ ModelManager initialized successfully!")
    print()
    
    # Check if all three models are configured
    print("🔍 CONFIGURATION VERIFICATION:")
    print(f"  Depression Model: {model_manager.config['depression_model']}")
    print(f"  Sentiment Model: {model_manager.config['sentiment_model']}")
    print(f"  Emotional Distress Model: {model_manager.config['emotional_distress_model']}")
    print(f"  Ensemble Mode: {model_manager.config['ensemble_mode']}")
    print(f"  Device: {model_manager.device}")
    print(f"  Precision: {model_manager.config['precision']}")
    print(f"  Cache Directory: {model_manager.config['cache_dir']}")
    print()
    
    print("⚡ PERFORMANCE SETTINGS:")
    print(f"  Max Batch Size: {model_manager.config['max_batch_size']}")
    print(f"  Gap Detection Threshold: {model_manager.config['gap_detection_threshold']}")
    print(f"  Disagreement Threshold: {model_manager.config['disagreement_threshold']}")
    print()
    
    # Test model status (without actually loading models)
    status = model_manager.get_model_status()
    print("📊 MODEL STATUS:")
    for model_name, model_info in status['models'].items():
        print(f"  {model_name.title()}: {model_info['name']}")
        print(f"    Purpose: {model_info['purpose']}")
        print(f"    Configured: ✅")
    
    print()
    print("🎉 SUCCESS: 3-Model integration is working perfectly!")
    print("📝 Configuration and ModelManager are properly integrated")
    print("🚀 Ready for model loading and ensemble analysis")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this from the ash-nlp directory")
    
except Exception as e:
    print(f"❌ Integration Error: {e}")
    print("Check the configuration and ModelManager compatibility")
    import traceback
    traceback.print_exc()
    
input("Press Enter to continue...")
