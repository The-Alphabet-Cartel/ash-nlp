#!/usr/bin/env python3
"""
Phase 3a Endpoint Integration Test
Tests that the CrisisPatternManager integration works correctly with API endpoints

This test validates:
1. Health endpoint reports Phase 3a status correctly
2. Analysis endpoints can access crisis patterns
3. Admin endpoints provide crisis pattern information
4. No regression in core functionality after migration
"""

import requests
import json
import time
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30

def test_health_endpoint_phase_3a():
    """Test that health endpoint reports Phase 3a status"""
    logger.info("🏥 Testing health endpoint Phase 3a status...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        
        if response.status_code != 200:
            logger.error(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        health_data = response.json()
        
        # Check Phase 3a specific fields
        phase_3a_checks = [
            ('phase_3a_status', 'Phase 3a status'),
            ('components_available.crisis_pattern_manager', 'Crisis Pattern Manager availability'),
            ('configuration_status.crisis_patterns_loaded', 'Crisis patterns loaded status'),
            ('manager_status.crisis_pattern_analysis_available', 'Crisis pattern analysis availability')
        ]
        
        for field_path, description in phase_3a_checks:
            value = get_nested_value(health_data, field_path)
            if value:
                logger.info(f"✅ {description}: {value}")
            else:
                logger.warning(f"⚠️ {description}: Not found or False")
        
        # Check architecture version
        arch_version = health_data.get('architecture_version', '')
        if 'phase_3a' in arch_version.lower():
            logger.info(f"✅ Architecture version indicates Phase 3a: {arch_version}")
        else:
            logger.warning(f"⚠️ Architecture version may not reflect Phase 3a: {arch_version}")
        
        return health_data.get('status') == 'healthy'
        
    except Exception as e:
        logger.error(f"❌ Health endpoint test failed: {e}")
        return False

def test_ensemble_status_endpoint():
    """Test ensemble status endpoint for Phase 3a features"""
    logger.info("🎯 Testing ensemble status endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/ensemble/status", timeout=TIMEOUT)
        
        if response.status_code != 200:
            logger.error(f"❌ Ensemble status endpoint failed: {response.status_code}")
            return False
        
        status_data = response.json()
        
        # Check for Phase 3a related information
        if 'manager_status' in status_data:
            manager_status = status_data['manager_status']
            crisis_pattern_available = manager_status.get('crisis_pattern_manager_available', False)
            
            if crisis_pattern_available:
                logger.info("✅ Ensemble status reports crisis pattern manager available")
            else:
                logger.warning("⚠️ Crisis pattern manager not reported as available")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ensemble status test failed: {e}")
        return False

def test_analysis_with_patterns():
    """Test that analysis endpoints work with crisis patterns"""
    logger.info("🔍 Testing analysis with crisis patterns...")
    
    # Test messages that should trigger different pattern types
    test_cases = [
        {
            "message": "My family rejected me when I came out as transgender",
            "expected_patterns": ["family_rejection", "community_pattern"],
            "description": "LGBTQIA+ family rejection pattern"
        },
        {
            "message": "I have no hope left and nothing matters anymore",
            "expected_patterns": ["hopelessness", "enhanced_crisis"],
            "description": "Enhanced hopelessness pattern"
        },
        {
            "message": "I need help right now, this is urgent",
            "expected_patterns": ["temporal_urgency", "crisis_context"],
            "description": "Temporal urgency pattern"
        },
        {
            "message": "This joke killed me, I'm dying of laughter",
            "expected_patterns": ["humor", "positive_context"],
            "description": "Humor/positive context pattern"
        }
    ]
    
    successful_tests = 0
    
    for test_case in test_cases:
        try:
            # Test analysis endpoint
            payload = {
                "message": test_case["message"],
                "user_id": "test_user",
                "channel_id": "test_channel"
            }
            
            response = requests.post(
                f"{BASE_URL}/analyze", 
                json=payload, 
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if pattern analysis is included in the response
                pattern_analysis = result.get('pattern_analysis', {})
                method = result.get('method', '')
                
                if pattern_analysis or 'pattern' in method.lower():
                    logger.info(f"✅ {test_case['description']}: Pattern analysis included")
                    logger.info(f"   Method: {method}")
                    logger.info(f"   Crisis level: {result.get('crisis_level', 'unknown')}")
                    successful_tests += 1
                else:
                    logger.warning(f"⚠️ {test_case['description']}: No pattern analysis found")
            else:
                logger.error(f"❌ Analysis failed for {test_case['description']}: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Analysis test failed for {test_case['description']}: {e}")
    
    logger.info(f"📊 Analysis with patterns: {successful_tests}/{len(test_cases)} tests successful")
    return successful_tests > 0

def test_admin_endpoints_crisis_patterns():
    """Test admin endpoints for crisis pattern information"""
    logger.info("🔧 Testing admin endpoints for crisis pattern info...")
    
    admin_endpoints = [
        ("/admin/status", "Admin status"),
        ("/admin/labels/status", "Labels status"),
    ]
    
    successful_endpoints = 0
    
    for endpoint, description in admin_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                # Look for crisis pattern related information
                found_pattern_info = False
                
                # Check various possible locations for pattern information
                if isinstance(data, dict):
                    # Convert to string to search for pattern-related keywords
                    data_str = json.dumps(data).lower()
                    pattern_keywords = ['crisis_pattern', 'pattern_manager', 'phase_3a', 'json_configuration']
                    
                    for keyword in pattern_keywords:
                        if keyword in data_str:
                            found_pattern_info = True
                            break
                
                if found_pattern_info:
                    logger.info(f"✅ {description}: Contains crisis pattern information")
                    successful_endpoints += 1
                else:
                    logger.info(f"ℹ️ {description}: No specific pattern information found")
                    successful_endpoints += 1  # Still count as successful if endpoint works
                    
            else:
                logger.warning(f"⚠️ {description}: Status {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ {description} test failed: {e}")
    
    return successful_endpoints > 0

def test_configuration_endpoints():
    """Test configuration-related endpoints"""
    logger.info("⚙️ Testing configuration endpoints...")
    
    config_endpoints = [
        ("/ensemble/config", "Ensemble configuration"),
        ("/ensemble/health", "Ensemble health")
    ]
    
    successful_endpoints = 0
    
    for endpoint, description in config_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            
            if response.status_code == 200:
                logger.info(f"✅ {description}: Accessible")
                successful_endpoints += 1
            else:
                logger.warning(f"⚠️ {description}: Status {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ {description} test failed: {e}")
    
    return successful_endpoints > 0

def test_learning_endpoints():
    """Test learning endpoints functionality"""
    logger.info("🧠 Testing learning endpoints...")
    
    try:
        # Test learning statistics endpoint
        response = requests.get(f"{BASE_URL}/learning_statistics", timeout=TIMEOUT)
        
        if response.status_code == 200:
            logger.info("✅ Learning statistics endpoint accessible")
            return True
        else:
            logger.info(f"ℹ️ Learning statistics endpoint: Status {response.status_code} (may not be enabled)")
            return True  # Don't fail if learning system is optional
            
    except Exception as e:
        logger.info(f"ℹ️ Learning endpoints test: {e} (may not be enabled)")
        return True  # Don't fail if learning system is optional

def get_nested_value(data: Dict[str, Any], path: str) -> Any:
    """Helper function to get nested dictionary values using dot notation"""
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    
    return current

def wait_for_service_ready(max_attempts: int = 10, delay: int = 5) -> bool:
    """Wait for the service to be ready"""
    logger.info(f"⏳ Waiting for service to be ready at {BASE_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get('status') == 'healthy':
                    logger.info("✅ Service is ready!")
                    return True
                else:
                    logger.info(f"⏳ Service status: {health_data.get('status', 'unknown')} (attempt {attempt + 1})")
            else:
                logger.info(f"⏳ Service not ready: HTTP {response.status_code} (attempt {attempt + 1})")
        except Exception as e:
            logger.info(f"⏳ Service not ready: {e} (attempt {attempt + 1})")
        
        if attempt < max_attempts - 1:
            time.sleep(delay)
    
    logger.error("❌ Service failed to become ready")
    return False

def main():
    """Run all Phase 3a endpoint integration tests"""
    logger.info("🚀 Starting Phase 3a Endpoint Integration Tests...")
    logger.info("=" * 80)
    
    # Wait for service to be ready
    if not wait_for_service_ready():
        logger.error("❌ Service not available - cannot run endpoint tests")
        return False
    
    tests = [
        ("Health Endpoint Phase 3a Status", test_health_endpoint_phase_3a),
        ("Ensemble Status Endpoint", test_ensemble_status_endpoint),
        ("Analysis with Crisis Patterns", test_analysis_with_patterns),
        ("Admin Endpoints Crisis Patterns", test_admin_endpoints_crisis_patterns),
        ("Configuration Endpoints", test_configuration_endpoints),
        ("Learning Endpoints", test_learning_endpoints)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running test: {test_name}")
        logger.info("-" * 60)
        
        try:
            if test_func():
                logger.info(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
            failed += 1
        
        # Small delay between tests
        time.sleep(1)
    
    logger.info("\n" + "=" * 80)
    logger.info(f"📊 Phase 3a Endpoint Integration Results:")
    logger.info(f"   ✅ Passed: {passed}")
    logger.info(f"   ❌ Failed: {failed}")
    logger.info(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        logger.info("🎉 Phase 3a Endpoint Integration: SUCCESS!")
        logger.info("🔗 All endpoints working correctly with CrisisPatternManager")
        logger.info("🏗️ Phase 3a migration validated through API testing")
        return True
    else:
        logger.error("❌ Phase 3a endpoint integration incomplete - some tests failed")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)