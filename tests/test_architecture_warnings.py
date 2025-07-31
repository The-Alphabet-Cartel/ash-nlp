#!/usr/bin/env python3
"""
Model Architecture Warning Tester
Tests different model architectures for deprecation warnings
Location: ash/ash-nlp/tests/test_architecture_warnings.py
"""

import warnings
import logging
from transformers import pipeline, AutoConfig
import sys
from io import StringIO

# Capture warnings
warnings.filterwarnings("default")

# Models to test with different architectures
TEST_MODELS = [
    {
        "name": "Pure BERT",
        "model": "nlptown/bert-base-multilingual-uncased-sentiment",
        "expected_arch": "bert"
    },
    {
        "name": "ALBERT", 
        "model": "textattack/albert-base-v2-imdb",
        "expected_arch": "albert"
    },
    {
        "name": "DeBERTa v3",
        "model": "microsoft/deberta-v3-base",
        "expected_arch": "deberta-v2"
    },
    {
        "name": "ELECTRA",
        "model": "google/electra-base-discriminator", 
        "expected_arch": "electra"
    },
    {
        "name": "DistilBERT (non-RoBERTa)",
        "model": "distilbert-base-uncased-finetuned-sst-2-english",
        "expected_arch": "distilbert"
    }
]

def capture_warnings_and_test(model_name, model_id):
    """Test a model and capture any warnings"""
    print(f"\n🧪 Testing: {model_name}")
    print(f"   Model: {model_id}")
    
    # Capture stderr to catch warnings
    old_stderr = sys.stderr
    captured_warnings = StringIO()
    
    try:
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Redirect stderr to capture transformers warnings
            sys.stderr = captured_warnings
            
            # Test model config first
            try:
                config = AutoConfig.from_pretrained(model_id)
                print(f"   ✅ Architecture: {config.model_type}")
                
                # Try to load pipeline (this is where warnings usually appear)
                pipe = pipeline("text-classification", model=model_id, device=-1)
                
                # Test with a simple phrase
                result = pipe("I am happy")
                print(f"   ✅ Test result: {result[0]['label']} ({result[0]['score']:.3f})")
                
                # Check for warnings
                stderr_content = captured_warnings.getvalue()
                warning_count = len([warning for warning in w if 'encoder_attention_mask' in str(warning.message)])
                
                if warning_count > 0 or 'encoder_attention_mask' in stderr_content:
                    print(f"   ⚠️  DEPRECATION WARNING DETECTED ({warning_count} warnings)")
                    if 'encoder_attention_mask' in stderr_content:
                        print(f"   ⚠️  stderr also contains encoder_attention_mask warning")
                    return False
                else:
                    print(f"   ✅ NO DEPRECATION WARNINGS!")
                    return True
                    
            except Exception as e:
                print(f"   ❌ Failed to load: {e}")
                return False
                
    finally:
        # Restore stderr
        sys.stderr = old_stderr
    
    return False

def main():
    print("🔍 MODEL ARCHITECTURE DEPRECATION WARNING TESTER")
    print("=" * 60)
    print("Testing various model architectures for encoder_attention_mask warnings")
    print()
    
    clean_models = []
    problematic_models = []
    
    for model_info in TEST_MODELS:
        is_clean = capture_warnings_and_test(model_info["name"], model_info["model"])
        
        if is_clean:
            clean_models.append(model_info)
        else:
            problematic_models.append(model_info)
    
    # Summary
    print(f"\n📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Clean models (no warnings): {len(clean_models)}")
    for model in clean_models:
        print(f"   • {model['name']}: {model['model']}")
    
    print(f"\n⚠️  Problematic models (has warnings): {len(problematic_models)}")
    for model in problematic_models:
        print(f"   • {model['name']}: {model['model']}")
    
    print(f"\n💡 RECOMMENDATIONS:")
    if clean_models:
        print("   Use one of the clean models above for your sentiment analysis")
        print("   Focus on models with BERT, ALBERT, or DeBERTa architectures")
    else:
        print("   All tested models have deprecation warnings")
        print("   Consider suppressing warnings or pinning transformers version")
    
    print(f"\n🔧 NEXT STEPS:")
    if clean_models:
        best_model = clean_models[0]
        print(f"   1. Update .env: NLP_SENTIMENT_MODEL={best_model['model']}")
        print(f"   2. Restart container: docker-compose restart ash-nlp")
        print(f"   3. Test ensemble: docker exec -it ash-nlp python tests/test_ensemble_diagnostic.py")
    
    return len(clean_models) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)