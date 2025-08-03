#!/usr/bin/env python3
"""
Quick check of models directory and imports
"""

import os
import sys

print("🔍 Quick Model Import Check")
print("=" * 50)

# Check models directory
models_dir = "/app/models"
print(f"📁 Checking models directory: {models_dir}")
if os.path.exists(models_dir):
    files = os.listdir(models_dir)
    print(f"   Files found: {files}")
    
    # Check for specific files
    ml_models_path = os.path.join(models_dir, "ml_models.py")
    if os.path.exists(ml_models_path):
        print(f"   ✅ ml_models.py exists")
        
        # Check file size (empty files might be an issue)
        size = os.path.getsize(ml_models_path)
        print(f"   File size: {size} bytes")
        
        if size == 0:
            print("   ❌ ml_models.py is empty!")
        
        # Show first few lines
        try:
            with open(ml_models_path, 'r') as f:
                first_lines = f.readlines()[:10]
            print(f"   First few lines:")
            for i, line in enumerate(first_lines, 1):
                print(f"   {i:2d}: {line.rstrip()}")
        except Exception as e:
            print(f"   ❌ Cannot read file: {e}")
    else:
        print(f"   ❌ ml_models.py not found")
        
    # Check for __init__.py
    init_path = os.path.join(models_dir, "__init__.py")
    if os.path.exists(init_path):
        print(f"   ✅ __init__.py exists")
    else:
        print(f"   ❌ __init__.py missing")
        
else:
    print(f"   ❌ Models directory not found")

# Try importing models package
print("\n📦 Testing models package import...")
try:
    import models
    print("   ✅ models package imported")
except Exception as e:
    print(f"   ❌ models package import failed: {e}")

# Try importing ml_models specifically
print("\n🧠 Testing models.ml_models import...")
try:
    import models.ml_models
    print("   ✅ models.ml_models imported")
    
    # Check what's in it
    attrs = dir(models.ml_models)
    model_classes = [attr for attr in attrs if 'Manager' in attr]
    print(f"   Manager classes found: {model_classes}")
    
except Exception as e:
    print(f"   ❌ models.ml_models import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Python path check:")
for i, path in enumerate(sys.path):
    print(f"   {i}: {path}")

print("\nDone!")