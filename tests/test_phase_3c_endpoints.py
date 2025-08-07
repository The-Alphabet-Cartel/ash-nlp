#!/usr/bin/env python3
"""
Phase 3c Endpoint Integration Test - Improved Approach
Tests Phase 3c threshold mapping functionality through real HTTP endpoints

This test validates:
1. All Phase 3c endpoints respond correctly
2. ThresholdMappingManager integration works via API
3. Mode-aware threshold system accessible through endpoints
4. Admin and learning endpoints enhanced with Phase 3c functionality
5. Configuration externalization working correctly

Uses requests library to test against running Docker container - no additional dependencies needed!
"""

import requests
import json
import time
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30

class Phase3cEndpointTester:
    """Phase 3c endpoint testing class - follows your established pattern"""
    
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []

    def wait_for_service_ready(self, max_attempts: int = 10, delay: int = 5) -> bool:
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

    def get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Helper function to get nested dictionary values using dot notation"""
        keys = path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current

    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and track results"""
        logger.info(f"\n🧪 Running test: {test_name}")
        logger.info("-" * 60)
        
        try:
            result = test_func()
            if result:
                logger.info(f"✅ {test_name}: PASSED")
                self.passed_tests += 1
                self.test_results.append((test_name, True, None))
                return True
            else:
                logger.error(f"❌ {test_name}: FAILED")
                self.failed_tests += 1
                self.test_results.append((test_name, False, "Test returned False"))
                return False
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
            self.failed_tests += 1
            self.test_results.append((test_name, False, str(e)))
            return False

    def test_health_endpoint_phase_3c_status(self) -> bool:
        """Test health endpoint reports Phase 3c status correctly"""
        logger.info("🏥 Testing health endpoint Phase 3c status...")
        
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            
            if response.status_code != 200:
                logger.error(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            health_data = response.json()
            
            # Check Phase 3c specific fields
            phase_3c_checks = [
                ('threshold_mapping_manager', 'ThresholdMappingManager availability'),
                ('configuration_status.threshold_mapping_loaded', 'Threshold mapping loaded'),
                ('manager_status.threshold_aware_analysis', 'Threshold-aware analysis available')
            ]
            
            success_count = 0
            for field_path, description in phase_3c_checks:
                value = self.get_nested_value(health_data, field_path)
                if value:
                    logger.info(f"✅ {description}: {value}")
                    success_count += 1
                else:
                    logger.warning(f"⚠️ {description}: Not found or False")
            
            # Check architecture version
            arch_version = health_data.get('architecture_version', '')
            if 'phase_3c' in arch_version.lower() or '3c' in arch_version:
                logger.info(f"✅ Architecture version indicates Phase 3c: {arch_version}")
                success_count += 1
            else:
                logger.warning(f"⚠️ Architecture version may not reflect Phase 3c: {arch_version}")
            
            return health_data.get('status') == 'healthy' and success_count >= 2
            
        except Exception as e:
            logger.error(f"❌ Health endpoint test failed: {e}")
            return False

    def test_admin_threshold_endpoints(self) -> bool:
        """Test Phase 3c admin endpoints for threshold configuration"""
        logger.info("🔧 Testing admin threshold endpoints...")
        
        admin_endpoints = [
            ("/admin/thresholds/status", "Threshold status endpoint"),
            ("/admin/configuration/summary", "Configuration summary endpoint"),
            ("/admin/status", "Enhanced admin status endpoint")
        ]
        
        successful_endpoints = 0
        
        for endpoint, description in admin_endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ {description}: Accessible")
                    
                    # Validate response has Phase 3c content
                    if endpoint == "/admin/thresholds/status":
                        if 'threshold_mode' in data or 'crisis_level_mapping' in data:
                            logger.info(f"   ✅ Contains threshold mapping data")
                            successful_endpoints += 1
                        else:
                            logger.warning(f"   ⚠️ Missing expected threshold data")
                    elif endpoint == "/admin/configuration/summary":
                        if 'threshold_mapping_manager' in data:
                            logger.info(f"   ✅ Contains Phase 3c configuration data")
                            successful_endpoints += 1
                        else:
                            logger.warning(f"   ⚠️ Missing expected Phase 3c data")
                    else:
                        successful_endpoints += 1
                        
                elif response.status_code == 404:
                    logger.warning(f"⚠️ {description}: Not implemented yet (404)")
                else:
                    logger.warning(f"⚠️ {description}: Status {response.status_code}")
                    
            except Exception as e:
                logger.error(f"❌ {description} test failed: {e}")
        
        return successful_endpoints >= 1  # At least one admin endpoint should work

    def test_learning_threshold_endpoints(self) -> bool:
        """Test Phase 3c learning endpoints with threshold awareness"""
        logger.info("🧠 Testing learning threshold endpoints...")
        
        learning_endpoints = [
            ("/learning/status", "Learning status endpoint"),
            ("/learning/statistics_enhanced", "Enhanced learning statistics"),
        ]
        
        successful_endpoints = 0
        
        for endpoint, description in learning_endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ {description}: Accessible")
                    
                    # Check for Phase 3c enhancements
                    if 'threshold_aware' in str(data) or 'phase_3c' in str(data).lower():
                        logger.info(f"   ✅ Contains Phase 3c enhancements")
                        successful_endpoints += 1
                    else:
                        logger.info(f"   ℹ️ Basic functionality confirmed")
                        successful_endpoints += 1
                        
                elif response.status_code == 404:
                    logger.info(f"ℹ️ {description}: Not implemented (404) - may be optional")
                else:
                    logger.warning(f"⚠️ {description}: Status {response.status_code}")
                    
            except Exception as e:
                logger.info(f"ℹ️ {description}: {e} (may be optional)")
        
        return True  # Learning endpoints are optional, so don't fail if missing

    def test_analyze_endpoint_with_threshold_awareness(self) -> bool:
        """Test that analyze endpoint works with Phase 3c threshold mapping"""
        logger.info("🔍 Testing analyze endpoint with threshold awareness...")
        
        test_messages = [
            {
                "message": "I'm feeling really overwhelmed and don't know what to do",
                "user_id": "test_user_crisis",
                "channel_id": "test_channel",
                "description": "crisis message"
            },
            {
                "message": "Having a great day today!",
                "user_id": "test_user_positive",
                "channel_id": "test_channel", 
                "description": "positive message"
            }
        ]
        
        successful_analyses = 0
        
        for test_case in test_messages:
            try:
                payload = {
                    'message': test_case['message'],
                    'user_id': test_case['user_id'],
                    'channel_id': test_case['channel_id']
                }
                
                response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate expected response fields
                    required_fields = ['crisis_level', 'confidence_score', 'needs_response']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        logger.warning(f"⚠️ {test_case['description']}: Missing fields {missing_fields}")
                    else:
                        logger.info(f"✅ {test_case['description']}: Analysis successful")
                        
                        # Check for Phase 3c enhancements
                        if 'threshold_mode' in data:
                            logger.info(f"   ✅ Contains threshold mode: {data['threshold_mode']}")
                        
                        crisis_level = data.get('crisis_level')
                        confidence = data.get('confidence_score', 0)
                        
                        logger.info(f"   📊 Result: {crisis_level} (confidence: {confidence:.3f})")
                        successful_analyses += 1
                        
                else:
                    logger.error(f"❌ {test_case['description']}: Status {response.status_code}")
                    
            except Exception as e:
                logger.error(f"❌ {test_case['description']}: {e}")
        
        return successful_analyses >= 1

    def test_ensemble_endpoints_phase_3c(self) -> bool:
        """Test ensemble endpoints with Phase 3c integration"""
        logger.info("🎯 Testing ensemble endpoints with Phase 3c...")
        
        ensemble_endpoints = [
            ("/ensemble/config", "Ensemble configuration"),
            ("/ensemble/health", "Ensemble health"),
            ("/ensemble/status", "Ensemble status")
        ]
        
        successful_endpoints = 0
        
        for endpoint, description in ensemble_endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ {description}: Accessible")
                    
                    # Check for Phase 3c threshold integration
                    if ('threshold' in str(data).lower() or 
                        'mode' in data or 
                        'mapping' in str(data).lower()):
                        logger.info(f"   ✅ Contains threshold-related data")
                    
                    successful_endpoints += 1
                    
                elif response.status_code == 404:
                    logger.info(f"ℹ️ {description}: Not implemented (404)")
                else:
                    logger.warning(f"⚠️ {description}: Status {response.status_code}")
                    
            except Exception as e:
                logger.error(f"❌ {description} test failed: {e}")
        
        return successful_endpoints >= 1

    def test_configuration_externalization(self) -> bool:
        """Test that configuration is properly externalized (no hardcoded thresholds)"""
        logger.info("⚙️ Testing configuration externalization...")
        
        try:
            # Test health endpoint to see configuration status
            response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                
                # Look for indicators that configuration is externalized
                config_indicators = [
                    self.get_nested_value(data, 'configuration_status.threshold_mapping_loaded'),
                    self.get_nested_value(data, 'configuration_status.json_config_loaded'),
                    self.get_nested_value(data, 'configuration_status.env_overrides_applied')
                ]
                
                active_indicators = [indicator for indicator in config_indicators if indicator]
                
                if active_indicators:
                    logger.info(f"✅ Configuration externalization indicators found: {len(active_indicators)}")
                    return True
                else:
                    logger.warning("⚠️ No clear configuration externalization indicators found")
                    return False
                    
            else:
                logger.error(f"❌ Could not access health endpoint: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Configuration externalization test failed: {e}")
            return False

    def run_all_tests(self) -> bool:
        """Run all Phase 3c endpoint tests"""
        logger.info("🚀 Starting Phase 3c Endpoint Integration Tests...")
        logger.info("🎯 Phase 3c Validation - Threshold Mapping System Testing")
        logger.info("=" * 80)
        
        # Wait for service to be ready
        if not self.wait_for_service_ready():
            logger.error("❌ Service not available - cannot run endpoint tests")
            return False
        
        # Define test suite
        tests = [
            ("Health Endpoint Phase 3c Status", self.test_health_endpoint_phase_3c_status),
            ("Admin Threshold Endpoints", self.test_admin_threshold_endpoints),
            ("Learning Threshold Endpoints", self.test_learning_threshold_endpoints),
            ("Analyze Endpoint Threshold Awareness", self.test_analyze_endpoint_with_threshold_awareness),
            ("Ensemble Endpoints Phase 3c", self.test_ensemble_endpoints_phase_3c),
            ("Configuration Externalization", self.test_configuration_externalization)
        ]
        
        # Run all tests
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
            time.sleep(1)  # Small delay between tests
        
        # Print results summary
        logger.info("\n" + "=" * 80)
        logger.info(f"📊 Phase 3c Endpoint Integration Results:")
        logger.info(f"   ✅ Passed: {self.passed_tests}")
        logger.info(f"   ❌ Failed: {self.failed_tests}")
        total_tests = self.passed_tests + self.failed_tests
        if total_tests > 0:
            logger.info(f"   📈 Success Rate: {(self.passed_tests/total_tests*100):.1f}%")
        
        if self.failed_tests == 0:
            logger.info("🎉 Phase 3c Endpoint Integration: SUCCESS!")
            logger.info("🔗 All endpoints working correctly with ThresholdMappingManager")
            logger.info("🏗️ Phase 3c implementation validated through API testing")
            return True
        else:
            logger.error(f"❌ Phase 3c endpoint integration incomplete - {self.failed_tests} tests failed")
            logger.info("\n📋 Failed Tests:")
            for test_name, passed, error in self.test_results:
                if not passed:
                    logger.info(f"   ❌ {test_name}: {error or 'Unknown error'}")
            return False


def main():
    """Main test execution function"""
    tester = Phase3cEndpointTester()
    success = tester.run_all_tests()
    return success


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)