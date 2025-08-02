#!/usr/bin/env python3
"""
Diagnostic script for models_loaded() issue
Location: ash-nlp/scripts/diagnose_models_loaded.py

This script directly checks the ModelManager state to identify why models_loaded() is False
"""

import requests
import json
import sys
import os

def check_health_endpoint():
    """Check health endpoint for detailed model status"""
    print("🔍 HEALTH ENDPOINT ANALYSIS")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8881/health", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health endpoint accessible")
            print(f"📊 Status: {health_data.get('status', 'unknown')}")
            print(f"🧠 Model Loaded: {health_data.get('model_loaded', 'unknown')}")
            
            # Check hardware info for detailed component status
            hardware_info = health_data.get('hardware_info', {})
            components = hardware_info.get('components_available', {})
            
            print(f"\n🔧 COMPONENT STATUS:")
            print("-" * 30)
            for component, status in components.items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {component}: {status}")
            
            return health_data
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Could not connect to health endpoint: {e}")
        return None

def check_stats_endpoint():
    """Check stats endpoint for detailed model information"""
    print("\n🔍 STATS ENDPOINT ANALYSIS")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8881/stats", timeout=10)
        
        if response.status_code == 200:
            stats_data = response.json()
            
            # Extract models_loaded section
            models_loaded = stats_data.get('models_loaded', {})
            print(f"📊 Models Loaded Status:")
            print(json.dumps(models_loaded, indent=2))
            
            return stats_data
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Could not connect to stats endpoint: {e}")
        return None

def direct_model_manager_check():
    """Try to directly access the model manager for debugging"""
    print("\n🔍 DIRECT MODEL MANAGER CHECK")
    print("=" * 50)
    
    try:
        # This requires running inside the container
        sys.path.append('/app')
        from models.ml_models import get_model_manager
        
        manager = get_model_manager()
        if manager is None:
            print("❌ Global model manager is None")
            return
        
        print(f"📊 Model Manager Status:")
        print(f"   _models_loaded flag: {manager._models_loaded}")
        print(f"   depression_model: {manager.depression_model is not None}")
        print(f"   sentiment_model: {manager.sentiment_model is not None}")
        print(f"   emotional_distress_model: {manager.emotional_distress_model is not None}")
        print(f"   models_loaded() result: {manager.models_loaded()}")
        
        # Try to get detailed status
        try:
            status = manager.get_model_status()
            print(f"\n📋 Detailed Model Status:")
            print(json.dumps(status, indent=2))
        except Exception as e:
            print(f"❌ Could not get detailed model status: {e}")
            
        # Try health check
        try:
            health = manager.health_check()
            print(f"\n🏥 Health Check Results:")
            print(json.dumps(health, indent=2))
        except Exception as e:
            print(f"❌ Could not run health check: {e}")
            
    except Exception as e:
        print(f"❌ Could not access model manager directly: {e}")
        print("   (This is expected if running outside container)")

def check_logs_for_loading():
    """Check recent logs for model loading information"""
    print("\n🔍 LOG ANALYSIS")
    print("=" * 50)
    
    try:
        import subprocess
        
        # Get recent logs related to model loading
        result = subprocess.run([
            'docker', 'logs', '--tail', '100', 'ash-nlp'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            logs = result.stdout
            
            # Look for key loading events
            loading_events = []
            for line in logs.split('\n'):
                if any(keyword in line.lower() for keyword in [
                    'models loaded', 'model loading', 'loading complete', 
                    'models_loaded', 'depression model', 'sentiment model', 
                    'emotional distress', 'three zero-shot'
                ]):
                    loading_events.append(line.strip())
            
            if loading_events:
                print("📋 Recent Model Loading Events:")
                for event in loading_events[-10:]:  # Last 10 events
                    print(f"   {event}")
            else:
                print("❌ No model loading events found in recent logs")
        else:
            print(f"❌ Could not get logs: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Could not analyze logs: {e}")

def test_analyze_endpoint():
    """Test the analyze endpoint to see exact error"""
    print("\n🔍 ANALYZE ENDPOINT TEST")
    print("=" * 50)
    
    try:
        payload = {
            "message": "I am feeling okay today",
            "user_id": "test",
            "channel_id": "test"
        }
        
        response = requests.post(
            "http://localhost:8881/analyze",
            json=payload,
            timeout=10
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Body:")
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                data = response.json()
                print(json.dumps(data, indent=2))
            except:
                print(response.text)
        else:
            print(response.text)
            
    except Exception as e:
        print(f"❌ Could not test analyze endpoint: {e}")

if __name__ == "__main__":
    print("🔍 COMPREHENSIVE MODEL MANAGER DIAGNOSTIC")
    print("=" * 70)
    
    health_data = check_health_endpoint()
    stats_data = check_stats_endpoint()
    direct_model_manager_check()
    check_logs_for_loading()
    test_analyze_endpoint()
    
    print("\n🎯 DIAGNOSIS SUMMARY")
    print("=" * 70)
    
    if health_data:
        model_loaded = health_data.get('model_loaded', False)
        if not model_loaded:
            print("❌ PROBLEM: models_loaded() is returning False")
            print("   This indicates one of these issues:")
            print("   1. _models_loaded flag is False")
            print("   2. One or more model objects are None")
            print("   3. models_loaded() method has a bug")
            print("   4. Model loading failed but wasn't caught")
        else:
            print("✅ models_loaded() is returning True - issue may be elsewhere")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   1. Check if the fixed ml_models.py was actually applied")
    print(f"   2. Look at the 'Direct Model Manager Check' output above")
    print(f"   3. Check the log analysis for loading errors")
    print(f"   4. If all models show as loaded individually but models_loaded() is False,")
    print(f"      there's likely a bug in the models_loaded() method itself")